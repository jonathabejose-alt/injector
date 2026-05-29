"""
SacredWare FFlag Dumper v7
---------------------------
Confirmed node layout:
  +08: next ptr
  +10: str_ptr (heap, when cap>15) or inline string
  +20: str_sz
  +28: str_cap
  +30: value_obj_ptr (heap runtime FFlag object)

The value_obj_ptr points to a heap FFlag object.
Inside that object there should be a pointer back to .data (static value).
OR the value_obj_ptr+ToValue(0xC0) IS the static address directly.

We scan the value object for any pointer into base..base+size range.
That pointer - base = our RVA.
"""

import sys, os, json, struct, time
sys.path.insert(0, os.path.dirname(__file__))

try:
    import pymem
    import pymem.process
except ImportError:
    print("[!] pymem not installed. Run: pip install pymem")
    sys.exit(1)

def _is_ptr(v):
    return 0x10000 < v < 0x7FFFFFFFFFFF

def _ru64(pm, addr):
    try:
        return struct.unpack('<Q', pm.read_bytes(addr, 8))[0]
    except:
        return 0

def _rb(pm, addr, n):
    try:
        return pm.read_bytes(addr, n)
    except:
        return b''

FLAG_PREFIXES = (
    'FFlag', 'FInt', 'FString', 'FLog',
    'DFFlag', 'DFInt', 'DFString', 'DFLog',
    'SFFlag', 'SFInt', 'SFString', 'SFLog',
)

def looks_like_flag(s):
    if not s or not (3 < len(s) < 128):
        return False
    if not s.isascii():
        return False
    if not all(c.isalnum() or c == '_' for c in s):
        return False
    for p in FLAG_PREFIXES:
        if s.startswith(p) and len(s) > len(p):
            return True
    return False

def find_static_rva(pm, base, size, value_obj_ptr):
    """
    Read the heap FFlag object and find a pointer into module .data.
    Returns RVA (offset from base) or 0.
    """
    # Read 256 bytes from the value object
    obj = _rb(pm, value_obj_ptr, 256)
    if not obj:
        return 0

    module_end = base + size

    # Scan for any pointer that lands inside the module
    for off in range(0, len(obj) - 7, 8):
        try:
            v = struct.unpack_from('<Q', obj, off)[0]
        except:
            continue
        if base <= v < module_end:
            rva = v - base
            if 0x1000 < rva < size:
                return rva

    # Also try: value is at value_obj_ptr + ToValue(0xC0)
    # and that address itself might be the static location
    # Check if value_obj_ptr is actually a static .data ptr somehow
    # (unlikely since it's heap, but worth checking)

    return 0

def parse_node(pm, base, size, node):
    """
    Parse FFlag hash-map node:
      +08: next ptr
      +10: str_ptr or inline
      +20: str_sz
      +28: str_cap
      +30: value_obj_ptr → search inside for .data ptr → RVA
    """
    entry = _rb(pm, node, 64)
    if len(entry) < 56:
        return None, None, 0

    try:
        nxt          = struct.unpack_from('<Q', entry, 0x08)[0]
        str_field    = struct.unpack_from('<Q', entry, 0x10)[0]
        str_sz       = struct.unpack_from('<Q', entry, 0x20)[0]
        str_cap      = struct.unpack_from('<Q', entry, 0x28)[0]
        value_obj    = struct.unpack_from('<Q', entry, 0x30)[0]
    except:
        return None, None, 0

    if not (3 < str_sz < 128):
        return None, None, 0
    if not _is_ptr(value_obj):
        return None, None, 0

    # Read name
    if str_cap > 15:
        if not _is_ptr(str_field):
            return None, None, 0
        raw = _rb(pm, str_field, int(str_sz))
    else:
        raw = entry[0x10:0x10 + int(str_sz)]

    if not raw or len(raw) != int(str_sz):
        return None, None, 0

    try:
        name = raw.decode('utf-8', errors='strict')
    except:
        return None, None, 0

    if not looks_like_flag(name):
        return None, None, 0

    # Find static RVA from value object
    rva = find_static_rva(pm, base, size, value_obj)
    if not rva:
        return None, None, 0

    next_ptr = nxt if _is_ptr(nxt) else 0
    return name, rva, next_ptr

def dump_hashmap(pm, base, size, hmap_ptr):
    m_end  = _ru64(pm, hmap_ptr + 0x08)
    m_list = _ru64(pm, hmap_ptr + 0x18)
    m_mask = _ru64(pm, hmap_ptr + 0x30)

    print(f"[*] hash-map @ 0x{hmap_ptr:X}")
    print(f"    m_list=0x{m_list:X} m_mask=0x{m_mask:X} ({m_mask+1} buckets)")

    if not _is_ptr(m_list) or not (0x3F < m_mask < 0x1FFFFFF):
        print("[!] Invalid layout")
        return {}

    bucket_count = int(m_mask) + 1
    flags   = {}
    visited = set()
    empty   = 0
    no_rva  = 0

    # Debug first 3 nodes in detail
    debug_done = False

    for b in range(bucket_count):
        try:
            node = _ru64(pm, m_list + b * 16 + 8)
        except:
            empty += 1
            continue

        if not _is_ptr(node) or node == m_end or node == 0:
            empty += 1
            continue

        depth = 0
        while _is_ptr(node) and node != m_end and node not in visited and depth < 64:
            visited.add(node)
            depth += 1

            # Detailed debug for first 3 nodes
            if not debug_done and len(visited) <= 3:
                entry = _rb(pm, node, 64)
                try:
                    str_field = struct.unpack_from('<Q', entry, 0x10)[0]
                    str_sz    = struct.unpack_from('<Q', entry, 0x20)[0]
                    str_cap   = struct.unpack_from('<Q', entry, 0x28)[0]
                    value_obj = struct.unpack_from('<Q', entry, 0x30)[0]
                    print(f"\n[DBG] Node 0x{node:X}:")
                    print(f"  str_field=0x{str_field:X} sz={str_sz} cap={str_cap}")
                    print(f"  value_obj=0x{value_obj:X}")
                    if _is_ptr(value_obj):
                        obj = _rb(pm, value_obj, 128)
                        print(f"  value_obj contents:")
                        for off in range(0, min(128, len(obj))-7, 8):
                            v = struct.unpack_from('<Q', obj, off)[0]
                            in_mod = base <= v < base+size
                            print(f"    +{off:02X}: 0x{v:016X} {'<-- IN MODULE rva=0x{:X}'.format(v-base) if in_mod else ''}")
                except Exception as ex:
                    print(f"[DBG] Error: {ex}")
                if len(visited) == 3:
                    debug_done = True

            name, rva, nxt = parse_node(pm, base, size, node)
            if name and rva:
                flags[name] = rva
            elif name:
                no_rva += 1

            node = nxt if nxt else 0

        if b % 4000 == 0 and b > 0:
            print(f"\r[*] {b}/{bucket_count} buckets, {len(visited)} nodes, {len(flags)} flags, {no_rva} no_rva...", end='', flush=True)

    print(f"\r[*] Done: {len(visited)} nodes, {empty} empty, {len(flags)} flags, {no_rva} name_found_but_no_rva        ")
    return flags

def main():
    print("=" * 60)
    print("  SacredWare FFlag Dumper v7")
    print("=" * 60)
    print("[*] Attaching to RobloxPlayerBeta.exe...")

    try:
        pm     = pymem.Pymem("RobloxPlayerBeta.exe")
        module = pymem.process.module_from_name(pm.process_handle, "RobloxPlayerBeta.exe")
    except Exception as e:
        print(f"[!] Failed: {e}")
        input("Press Enter to exit...")
        sys.exit(1)

    base = module.lpBaseOfDll
    size = module.SizeOfImage
    print(f"[*] Base: 0x{base:X} Size: 0x{size:X}")

    existing_path = os.path.join(os.path.dirname(__file__), "offsets", "fflags.json")
    existing_flags = {}
    meta = {"ToValue": 0xC0, "ToFlag": 0x30, "Pointer": 0}
    roblox_ver = "unknown"

    if os.path.exists(existing_path):
        try:
            with open(existing_path) as f:
                d = json.load(f)
            existing_flags = d.get("FFlagOffsets", {}).get("FFlags", {})
            fl = d.get("FFlagOffsets", {}).get("FFlagList", {})
            meta = {
                "ToValue": fl.get("ToValue", 0xC0) or 0xC0,
                "ToFlag":  fl.get("ToFlag",  0x30) or 0x30,
                "Pointer": fl.get("Pointer", 0),
            }
            roblox_ver = d.get("Roblox Version", "unknown")
            print(f"[*] Loaded {len(existing_flags)} existing offsets")
        except Exception as e:
            print(f"[!] {e}")

    hmap_ptr = _ru64(pm, base + meta["Pointer"])
    print(f"[*] hmap=0x{hmap_ptr:X}")

    t0 = time.time()
    flags = dump_hashmap(pm, base, size, hmap_ptr)
    print(f"[*] {len(flags)} flags in {time.time()-t0:.1f}s")

    if not flags:
        print("[!] No flags. Check [DBG] above — need to find correct ptr in value_obj.")
        input("Press Enter to exit...")
        sys.exit(1)

    print(f"[*] Sample:")
    for n, r in list(flags.items())[:5]:
        print(f"  {n}: 0x{r:X}")

    merged = dict(existing_flags)
    new_c = upd_c = 0
    for name, rva in flags.items():
        if name not in merged:
            new_c += 1
        elif merged[name] != rva:
            upd_c += 1
        merged[name] = rva
    print(f"[*] Merged: {len(merged)} ({new_c} new, {upd_c} updated)")

    out_path = os.path.join(os.path.dirname(__file__), "offsets", "fflags_dumped.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    out = {
        "Roblox Version": roblox_ver,
        "Total Offsets":  len(merged),
        "FFlagOffsets": {"FFlagList": meta, "FFlags": merged}
    }
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2)
    print(f"[+] Saved → {out_path}")
    print("=" * 60)

    ans = input("Replace fflags.json now? (y/n): ").strip().lower()
    if ans == 'y':
        import shutil
        shutil.copy2(out_path, existing_path)
        print(f"[+] Updated!")
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
