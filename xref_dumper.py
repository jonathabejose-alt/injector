"""
SacredWare XRef FFlag Dumper v3
--------------------------------
1. Downloads ~20k flag names from Roblox API
2. Strips prefixes to get bare names (e.g. TaskSchedulerTargetFps)
3. Scans ALL Roblox memory regions (not just module) for those strings
4. XRef: scans module .text for LEA instructions pointing to each string
5. Near each LEA: finds entry struct with value ptr → RVA

Usage:
    1. Launch Roblox (in-game or main menu)
    2. Run: python xref_dumper.py
    3. Output: offsets/fflags_xref.json
"""

import sys, os, json, struct, time, ctypes
sys.path.insert(0, os.path.dirname(__file__))

try:
    import pymem
    import pymem.process
except ImportError:
    print("[!] pymem not installed. Run: pip install pymem")
    sys.exit(1)

# ── Win32 memory enumeration ───────────────────────────────────────────────

class MEMORY_BASIC_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("BaseAddress",       ctypes.c_ulonglong),
        ("AllocationBase",    ctypes.c_ulonglong),
        ("AllocationProtect", ctypes.c_ulong),
        ("__alignment1",      ctypes.c_ulong),
        ("RegionSize",        ctypes.c_ulonglong),
        ("State",             ctypes.c_ulong),
        ("Protect",           ctypes.c_ulong),
        ("Type",              ctypes.c_ulong),
        ("__alignment2",      ctypes.c_ulong),
    ]

MEM_COMMIT  = 0x1000
PAGE_NOACCESS = 0x01
PAGE_GUARD    = 0x100

def enum_memory_regions(handle):
    """Enumerate all committed readable memory regions in the process."""
    regions = []
    addr = 0
    mbi = MEMORY_BASIC_INFORMATION()
    size = ctypes.sizeof(mbi)
    k32 = ctypes.windll.kernel32
    while addr < 0x7FFFFFFFFFFF:
        ret = k32.VirtualQueryEx(handle, ctypes.c_ulonglong(addr),
                                  ctypes.byref(mbi), size)
        if ret == 0:
            break
        if (mbi.State == MEM_COMMIT
                and not (mbi.Protect & PAGE_NOACCESS)
                and not (mbi.Protect & PAGE_GUARD)):
            regions.append((mbi.BaseAddress, mbi.RegionSize))
        addr = mbi.BaseAddress + mbi.RegionSize
    return regions

# ── Helpers ────────────────────────────────────────────────────────────────

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

# ── Prefix stripping ───────────────────────────────────────────────────────

PREFIXES = [
    'DFFlagDebug', 'FFlagDebug',
    'DFFlag', 'FFlag',
    'DFInt',  'FInt',
    'DFString', 'FString',
    'DFLog',  'FLog',
    'SFFlag', 'SFInt', 'SFString', 'SFLog',
]

def strip_prefix(name):
    for pfx in sorted(PREFIXES, key=len, reverse=True):
        if name.startswith(pfx):
            return name[len(pfx):]
    return name

# ── Step 0: Get flag names from API ───────────────────────────────────────

def fetch_api_names():
    import urllib.request
    urls = [
        "https://clientsettingscdn.roblox.com/v2/settings/application/PCDesktopClient",
        "https://clientsettings.roblox.com/v2/settings/application/PCDesktopClient",
    ]
    for url in urls:
        try:
            print(f"[*] Fetching from {url.split('/')[2]}...")
            req = urllib.request.Request(url, headers={"User-Agent": "RobloxStudio/WinInet"})
            with urllib.request.urlopen(req, timeout=15) as r:
                data = json.loads(r.read().decode())
            names = list(data.get("applicationSettings", {}).keys())
            print(f"[*] Got {len(names)} flag names")
            return names
        except Exception as e:
            print(f"[!] Failed: {e}")
    return []

# ── Step 1: Scan ALL memory for flag name strings ─────────────────────────

def find_strings_in_all_memory(pm, handle, base, mod_size, bare_names):
    """
    Scan all committed memory regions for flag name strings (bare, no prefix).
    Returns {string_address: bare_name}
    """
    print(f"[*] Enumerating memory regions...")
    regions = enum_memory_regions(handle)
    print(f"[*] Found {len(regions)} committed regions")

    # Build search set — bare names encoded
    target_bytes = {}
    for name in bare_names:
        b = name.encode('ascii')
        if len(b) > 3:
            target_bytes[b] = name

    results = {}
    PAGE = 0x40000  # 256KB chunks
    total_scanned = 0
    total_size = sum(r[1] for r in regions)

    print(f"[*] Scanning {len(target_bytes)} bare names across all memory...")

    for reg_base, reg_size in regions:
        offset = 0
        while offset < reg_size:
            chunk_size = min(PAGE, reg_size - offset)
            try:
                chunk = pm.read_bytes(reg_base + offset, chunk_size)
            except:
                offset += PAGE
                continue

            for name_b, name_s in target_bytes.items():
                pos = 0
                plen = len(name_b)
                while True:
                    idx = chunk.find(name_b, pos)
                    if idx == -1:
                        break
                    pos = idx + 1
                    # Check null terminator
                    end = idx + plen
                    if end < len(chunk) and chunk[end] == 0:
                        # Also check character before is not alphanumeric (avoid substrings)
                        if idx == 0 or not (chunk[idx-1:idx].isalnum() or chunk[idx-1:idx] == b'_'):
                            str_addr = reg_base + offset + idx
                            results[str_addr] = name_s

            total_scanned += chunk_size
            offset += PAGE

        if total_scanned % (PAGE * 32) == 0:
            pct = 100 * total_scanned // max(total_size, 1)
            print(f"\r[*] Memory scan: {pct}% ({len(results)} strings found)...", end='', flush=True)

    print(f"\r[*] Found {len(results)} flag strings across all memory        ")
    return results

# ── Step 2: XRef — scan module .text for LEA pointing to each string ──────

LEA_OPCODES = [
    b'\x48\x8D\x05', b'\x48\x8D\x0D', b'\x48\x8D\x15',
    b'\x48\x8D\x1D', b'\x48\x8D\x25', b'\x48\x8D\x2D',
    b'\x48\x8D\x35', b'\x48\x8D\x3D',
    b'\x4C\x8D\x05', b'\x4C\x8D\x0D', b'\x4C\x8D\x15',
    b'\x4C\x8D\x1D', b'\x4C\x8D\x25', b'\x4C\x8D\x2D',
    b'\x4C\x8D\x35', b'\x4C\x8D\x3D',
    # MOV reg, imm64 won't work but try absolute MOV via RIP
    b'\x48\x8D\x05', b'\x4C\x8D\x05',
]

def build_xref_map(pm, base, mod_size, string_addrs):
    """Single pass over module — find all LEA refs to our string addresses."""
    print(f"[*] XRef scan: {len(string_addrs)} string addresses...")
    addr_set = set(string_addrs)
    xref_map = {}

    PAGE = 0x10000
    offset = 0
    scanned = 0

    while offset < mod_size:
        chunk_size = min(PAGE, mod_size - offset)
        try:
            chunk = pm.read_bytes(base + offset, chunk_size)
        except:
            offset += PAGE
            continue

        for pfx in set(LEA_OPCODES):  # deduplicate
            plen = 3
            pos = 0
            while True:
                idx = chunk.find(pfx, pos)
                if idx == -1 or idx + 7 > len(chunk):
                    break
                pos = idx + 1
                try:
                    disp = struct.unpack_from('<i', chunk, idx + plen)[0]
                    instr_addr = base + offset + idx
                    rip = instr_addr + 7
                    target = (rip + disp) & 0xFFFFFFFFFFFFFFFF
                    if target in addr_set:
                        xref_map.setdefault(target, []).append(instr_addr)
                except:
                    pass

        scanned += chunk_size
        offset += PAGE
        if scanned % (PAGE * 64) == 0:
            pct = 100 * scanned // mod_size
            print(f"\r[*] XRef: {pct}% ({len(xref_map)} hits)...", end='', flush=True)

    print(f"\r[*] XRef done: {len(xref_map)} strings referenced in module        ")
    return xref_map

# ── Step 3: From XRef instr, find entry struct and value ptr ──────────────

ENTRY_LAYOUTS = [
    # (nxt_o, strptr_o, strsz_o, strcap_o, val_o)
    (8,  16, 32, 40, 48),
    (0,  8,  24, 32, 40),
    (8,  24, 40, 48, 56),
    (0,  16, 32, 40, 56),
    (8,  16, 24, 32, 48),
    (0,  8,  16, 24, 32),
    (8,  16, 40, 48, 64),
    (0,  16, 40, 48, 32),
    (8,  32, 48, 56, 64),
    (0,  24, 40, 48, 56),
    (8,  16, 32, 48, 56),
    (0,  8,  32, 40, 48),
]

def try_entry(pm, base, entry_ptr, str_addr, bare_name):
    """Check if entry_ptr looks like a valid FFlag entry. Return RVA or 0."""
    entry = _rb(pm, entry_ptr, 96)
    if len(entry) < 64:
        return 0

    name_b = bare_name.encode('ascii')
    name_len = len(name_b)

    for nxt_o, sptr_o, ssz_o, scap_o, val_o in ENTRY_LAYOUTS:
        if max(sptr_o, ssz_o, scap_o, val_o) + 8 > len(entry):
            continue
        try:
            str_sz  = struct.unpack_from('<q', entry, ssz_o)[0]
            str_cap = struct.unpack_from('<q', entry, scap_o)[0]
            vpr     = struct.unpack_from('<q', entry, val_o)[0]

            if str_sz != name_len:
                continue
            if not _is_ptr(vpr):
                continue

            matched = False
            if str_cap > 15:
                sp = struct.unpack_from('<Q', entry, sptr_o)[0]
                if sp == str_addr:
                    matched = True
            else:
                inline = entry[sptr_o:sptr_o + name_len]
                if inline == name_b:
                    matched = True

            if matched:
                rva = vpr - base
                if 0 < rva < 0x10000000:
                    return rva
        except:
            continue
    return 0

def extract_rva(pm, base, mod_size, xref_addr, str_addr, bare_name):
    """
    Given LEA instruction at xref_addr loading str_addr,
    scan surrounding code for heap pointers that are FFlag entries.
    """
    # Scan 256 bytes around the instruction
    win_start = max(0, xref_addr - 128)
    win_size  = 384
    window = _rb(pm, win_start, win_size)
    if not window:
        return 0

    for i in range(0, len(window) - 8, 4):
        try:
            v = struct.unpack_from('<Q', window, i)[0]
        except:
            continue
        if not _is_ptr(v):
            continue
        # Must be heap (not inside module)
        if base <= v < base + mod_size:
            continue
        rva = try_entry(pm, base, v, str_addr, bare_name)
        if rva:
            return rva

    # Also try: the LEA itself may be inside a constructor that stores
    # the string ptr into the entry. Look for RIP-relative refs nearby
    # that point INTO the module (static entry in .data/.rdata)
    for i in range(0, len(window) - 7, 1):
        b = window[i:i+3]
        if b not in [p for p in set(LEA_OPCODES)]:
            continue
        try:
            disp = struct.unpack_from('<i', window, i + 3)[0]
            instr = win_start + i
            rip   = instr + 7
            tgt   = (rip + disp) & 0xFFFFFFFFFFFFFFFF
            if base <= tgt < base + mod_size:
                # This could be a static entry in .data
                rva = try_entry(pm, base, tgt, str_addr, bare_name)
                if rva:
                    return rva
        except:
            pass

    return 0

# ── Main ──────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  SacredWare XRef FFlag Dumper v3")
    print("=" * 60)
    print("[*] Attaching to RobloxPlayerBeta.exe...")

    try:
        pm     = pymem.Pymem("RobloxPlayerBeta.exe")
        module = pymem.process.module_from_name(pm.process_handle, "RobloxPlayerBeta.exe")
    except Exception as e:
        print(f"[!] Failed: {e}")
        input("Press Enter to exit...")
        sys.exit(1)

    base     = module.lpBaseOfDll
    mod_size = module.SizeOfImage
    handle   = pm.process_handle
    print(f"[*] Base: 0x{base:X}, Size: 0x{mod_size:X}")

    # Load existing
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
            print(f"[!] fflags.json: {e}")

    # Get flag names
    api_names = fetch_api_names()
    if not api_names:
        # Fallback: reconstruct from existing
        api_names = []
        for bare in existing_flags:
            for pfx in PREFIXES:
                api_names.append(pfx + bare)
        print(f"[*] Fallback: {len(api_names)} names from fflags.json")

    # Strip prefixes → bare names (deduplicated)
    bare_set = {}  # bare_name → full_name (keep first)
    for full in api_names:
        bare = strip_prefix(full)
        if bare not in bare_set:
            bare_set[bare] = full
    print(f"[*] {len(bare_set)} unique bare names to search")

    # Scan all memory for strings
    t0 = time.time()
    str_map = find_strings_in_all_memory(pm, handle, base, mod_size, list(bare_set.keys()))
    print(f"[*] String scan: {time.time()-t0:.1f}s")

    if not str_map:
        print("[!] No strings found at all — something is wrong.")
        input("Press Enter to exit...")
        sys.exit(1)

    # Build XRef map
    t1 = time.time()
    xref_map = build_xref_map(pm, base, mod_size, set(str_map.keys()))
    print(f"[*] XRef build: {time.time()-t1:.1f}s")

    if not xref_map:
        print("[!] No XRefs found. Strings may be in heap only (no static refs).")
        print("[*] Trying direct entry scan from string addresses...")
        # Alternative: treat nearby heap data as potential entries
        flags = {}
        for str_addr, bare_name in str_map.items():
            # The entry struct often sits just before or after the string
            # Try ±256 bytes around the string addr as potential entry base
            for delta in range(-256, 256, 8):
                cand = str_addr + delta
                if not _is_ptr(cand):
                    continue
                rva = try_entry(pm, base, cand, str_addr, bare_name)
                if rva:
                    flags[bare_name] = rva
                    break
        print(f"[*] Direct scan: {len(flags)} flags")
    else:
        # Extract RVAs from XRefs
        print(f"[*] Extracting RVAs from {len(xref_map)} xrefs...")
        t2 = time.time()
        flags = {}
        for str_addr, xref_addrs in xref_map.items():
            bare_name = str_map.get(str_addr, "")
            if not bare_name:
                continue
            for xref_addr in xref_addrs[:5]:
                rva = extract_rva(pm, base, mod_size, xref_addr, str_addr, bare_name)
                if rva:
                    flags[bare_name] = rva
                    break
        print(f"[*] RVA extract: {len(flags)} flags in {time.time()-t2:.1f}s")

    if not flags:
        print("[!] No flags extracted.")
        input("Press Enter to exit...")
        sys.exit(1)

    print(f"[*] Total found: {len(flags)}")

    merged = dict(existing_flags)
    new_c = upd_c = 0
    for name, rva in flags.items():
        if name not in merged:
            new_c += 1
        elif merged[name] != rva:
            upd_c += 1
        merged[name] = rva
    print(f"[*] Merged: {len(merged)} total ({new_c} new, {upd_c} updated)")

    out_path = os.path.join(os.path.dirname(__file__), "offsets", "fflags_xref.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    out = {
        "Roblox Version": roblox_ver,
        "Total Offsets":  len(merged),
        "FFlagOffsets": {
            "FFlagList": meta,
            "FFlags":    merged,
        }
    }
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2)
    print(f"[+] Saved → {out_path}")
    print("=" * 60)

    ans = input("Replace fflags.json now? (y/n): ").strip().lower()
    if ans == 'y':
        import shutil
        shutil.copy2(out_path, existing_path)
        print(f"[+] fflags.json updated!")
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
