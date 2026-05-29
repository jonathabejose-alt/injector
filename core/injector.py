"""
SacredWare – Hybrid FFlag Injector  v4.0
==========================================
Aggressive dual-method injection:

  Method 1 (FAST)  – Direct offset from fflags.json
      value_ptr = module_base + FFlags[name] + ToValue(0xC0)

  Method 2 (DEEP)  – Singleton hash-map walk (fallback)
      Used for flags NOT in the offset table.

Both methods use WriteProcessMemory. Together they maximise coverage.
"""
import time
import os
import json
import struct
import ctypes
import ctypes.wintypes
from ctypes import c_int32, c_float, c_void_p, c_size_t, POINTER, byref
import pymem
import pymem.process

kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
_WriteProcessMemory = kernel32.WriteProcessMemory
_WriteProcessMemory.argtypes = [
    ctypes.wintypes.HANDLE, c_void_p, c_void_p, c_size_t, POINTER(c_size_t),
]
_WriteProcessMemory.restype = ctypes.wintypes.BOOL

PROCESS_VM_READ      = 0x0010
PROCESS_VM_WRITE     = 0x0020
PROCESS_VM_OPERATION = 0x0008
PROCESS_QUERY_LIMITED_INFORMATION = 0x1000

_FLAG_OFFSETS: dict = {}
_ACTIVE_OFFSET_COUNT: int = 0
_FLAG_TYPES:   dict = {}
_TO_VALUE: int = 0xC0
_TO_FLAG:  int = 0x30
_LIST_POINTER_OFF: int = 0

_PREFIXES = ["DFString","DFInt","DFFlag","FString","FFlag","FInt","FLog","DFLog"]
_PREFIX_TYPE = {
    "FFlag":   "bool",  "DFFlag":   "bool",
    "FInt":    "int",   "DFInt":    "int",
    "FLog":    "int",   "DFLog":    "int",
    "FString": "string","DFString": "string",
}

_PATTERNS = [
    (b"\x48\x8B\x0D....\x48\x85\xC9", 3, 7),
    (b"\x48\x8B\x0D....\x4C\x8B",     3, 7),
    (b"\x48\x8B\x05....\x48\x85\xC0", 3, 7),
    (b"\x4C\x8B\x0D....\x49\x8B",     3, 7),
    (b"\x48\x8B\x0D....\x48\x8B",     3, 7),
    (b"\x48\x83\xEC\x38\x48\x8B\x0D", 7, 11),
    (b"\x48\x83\xEC\x28\x48\x8B\x0D", 7, 11),
    (b"\x48\x83\xEC\x20\x48\x8B\x0D", 7, 11),
    (b"\x48\x83\xEC\x20\x48\x8B\x05", 7, 11),
    (b"\x53\x48\x83\xEC\x20\x48\x8B\x0D", 8, 12),
]



def _load_tables(fflags_path: str, types_path: str = ""):
    global _FLAG_OFFSETS, _FLAG_TYPES, _TO_VALUE, _LIST_POINTER_OFF
    try:
        with open(fflags_path, 'r', encoding='utf-8') as f:
            d = json.load(f)
        ff  = d.get("FFlagOffsets", {})
        ffl = ff.get("FFlagList", {})
        _TO_VALUE        = ffl.get("ToValue", 0xC0)
        _TO_FLAG         = ffl.get("ToFlag",  0x30)
        _LIST_POINTER_OFF = ffl.get("Pointer", 0)
        _FLAG_OFFSETS.clear()
        _FLAG_OFFSETS.update(ff.get("FFlags", {}))
        global _ACTIVE_OFFSET_COUNT
        _ACTIVE_OFFSET_COUNT = sum(1 for v in _FLAG_OFFSETS.values() if v >= 0x9E000000) or sum(1 for v in _FLAG_OFFSETS.values() if 0x7400000 <= v <= 0x8200000)
        print(f"[Injector] Loaded {_ACTIVE_OFFSET_COUNT} offsets, "
              f"ToValue=0x{_TO_VALUE:X}, ListPointer=0x{_LIST_POINTER_OFF:X}")
    except Exception as e:
        print(f"[Injector] fflags.json load failed: {e}")

    if types_path and os.path.isfile(types_path):
        try:
            with open(types_path, 'r', encoding='utf-8') as f:
                d = json.load(f)
            ft = d.get("FlagTypes", {})
            _FLAG_TYPES.clear()
            _FLAG_TYPES.update(ft)
            print(f"[Injector] Loaded {len(_FLAG_TYPES)} flag types")
        except Exception as e:
            print(f"[Injector] types.json load failed: {e}")


def _auto_load():
    import sys as _sys
    here    = os.path.dirname(os.path.abspath(__file__))
    meipass = getattr(_sys, '_MEIPASS', None)
    exe_dir = os.path.dirname(os.path.abspath(_sys.executable))
    search  = []
    if meipass:
        search.append(os.path.join(meipass, "offsets"))
    search += [
        os.path.join(exe_dir, "offsets"),
        os.path.join(os.getcwd(), "offsets"),
        os.path.join(here, "..", "offsets"),
    ]
    for folder in search:
        ff = os.path.join(folder, "fflags.json")
        if os.path.isfile(ff):
            tp = os.path.join(folder, "types.json")
            _load_tables(ff, tp if os.path.isfile(tp) else "")
            return
    print("[Injector] WARNING: fflags.json not found.")

_auto_load()


def reload_offsets(fflags_path: str = "", types_path: str = ""):
    if fflags_path and os.path.isfile(fflags_path):
        _load_tables(fflags_path, types_path)
    else:
        _auto_load()
    try:
        _instance.flag_cache.clear()
        _instance.cached_singleton = 0
    except Exception:
        pass



_OFFSETS_URL_PRIMARY = __import__('base64').b64decode('aHR0cHM6Ly9pbXRoZW8ubG9sL09mZnNldHMvRkZsYWdzLmpzb24=').decode()
_OFFSETS_URL_SOUL = __import__('base64').b64decode('aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL3NvdWxvdmVyeWFsbC9KU09OT2Zmc2V0cy5qc29uL3JlZnMvaGVhZHMvbWFpbi9PZmZzZXRzLmpzb24=').decode()
_OFFSETS_URL_FALLBACK = __import__('base64').b64decode('aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL2RhdmVsb3Zlc3RhcnMvb2Zmc2V0cy1nbmcvcmVmcy9oZWFkcy9tYWluL29mZnNldHMuaHBw').decode()
_OFFSETS_TIMEOUT = 10


def _parse_hpp(hpp: str) -> dict:
    """Parse offsets.hpp → {name: offset_int}"""
    result = {}
    for line in hpp.splitlines():
        line = line.strip().rstrip(';')
        if not line.startswith("uintptr_t "):
            continue
        parts = line.split('=')
        if len(parts) != 2:
            continue
        name = parts[0].replace("uintptr_t", "").strip()
        val_str = parts[1].strip()
        try:
            if val_str.lower().startswith("0x"):
                result[name] = int(val_str, 16)
            else:
                result[name] = int(val_str)
        except ValueError:
            continue
    return result


def _get_offsets_path() -> str:
    """Return path to local fflags.json (same logic as _auto_load)."""
    import sys as _sys
    here    = os.path.dirname(os.path.abspath(__file__))
    meipass = getattr(_sys, '_MEIPASS', None)
    exe_dir = os.path.dirname(os.path.abspath(_sys.executable))
    search  = []
    if meipass:
        search.append(os.path.join(meipass, "offsets"))
    search += [
        os.path.join(exe_dir, "offsets"),
        os.path.join(os.getcwd(), "offsets"),
        os.path.join(here, "..", "offsets"),
    ]
    for folder in search:
        ff = os.path.join(folder, "fflags.json")
        if os.path.isfile(ff):
            return ff
    return os.path.join(exe_dir, "offsets", "fflags.json")


def update_offsets_from_remote(status_cb=None) -> str:
    """
    Download offsets from ALL known sources and merge into fflags.json.
    Sources (tried in parallel threads):
      Remote offset sources are fetched on startup and merged.

    All results are merged — more sources = more total valid flags.
    status_cb(msg: str) — optional callback for progress updates.
    Returns a status string.
    """
    import urllib.request
    import urllib.error
    import threading

    def _cb(msg):
        print(f"[Injector] {msg}")
        if status_cb:
            try: status_cb(msg)
            except: pass

    SOURCES = [
        (_OFFSETS_URL_PRIMARY,  "json"),
        (__import__('base64').b64decode('aHR0cHM6Ly9pbXRoZW8ubG9sL09mZnNldHMvRkZsYWdzLmhwcA==').decode(), 'hpp'),
        (_OFFSETS_URL_SOUL,     "soul_json"),
        (_OFFSETS_URL_FALLBACK, "hpp"),
        (__import__('base64').b64decode('aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL050UmVhZFZpcnR1YWxNZW1vcnkvUm9ibG94LU9mZnNldHMtV2Vic2l0ZS9tYWluL0ZGbGFncy5ocHA=').decode(), 'hpp'),
    ]

    results = {}
    lock    = threading.Lock()
    primary_meta = {}

    def _fetch(url, fmt):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "SacredWare/1.0"})
            with urllib.request.urlopen(req, timeout=_OFFSETS_TIMEOUT) as resp:
                raw = resp.read().decode("utf-8", errors="replace")

            if fmt == "json":
                data = json.loads(raw)
                flags = data.get("FFlagOffsets", {}).get("FFlags", {})
                with lock:
                    primary_meta["version"] = data.get("Roblox Version", "unknown")
                    primary_meta["list"]    = data.get("FFlagOffsets", {}).get("FFlagList", {})
            elif fmt == "soul_json":
                lines = raw.split('\n')
                json_start = next((i for i, l in enumerate(lines) if l.strip().startswith('{')), 0)
                clean = '\n'.join(lines[json_start:])
                soul_data = json.loads(clean)
                flags = {}
                for k, v in soul_data.items():
                    try:
                        flags[k] = int(v, 16) if isinstance(v, str) else int(v)
                    except:
                        pass
            else:
                flags = _parse_hpp(raw)

            if flags:
                with lock:
                    results[url] = flags
                _cb(f"  ✓ {url.split('/')[2]}: {len(flags)} flags")
            else:
                _cb(f"  ⚠ {url.split('/')[2]}: 0 flags parsed")
        except Exception as ex:
            _cb(f"  ✗ {url.split('/')[2]}: {ex}")

    _cb("Fetching offsets from all sources...")
    threads = []
    for url, fmt in SOURCES:
        t = threading.Thread(target=_fetch, args=(url, fmt), daemon=True)
        t.start()
        threads.append(t)
    for t in threads:
        t.join(timeout=_OFFSETS_TIMEOUT + 2)

    if not results:
        return "⚠ All offset sources failed — check internet connection."

    merged = dict(_FLAG_OFFSETS)
    before = len(merged)

    primary_url = _OFFSETS_URL_PRIMARY
    if primary_url in results:
        merged.update(results[primary_url])

    for url, fmt in SOURCES:
        if url != primary_url and url in results:
            for name, offset in results[url].items():
                if name not in merged:
                    merged[name] = offset

    added = len(merged) - before
    roblox_ver = primary_meta.get("version", "unknown")
    _cb(f"Merged: {len(merged)} total flags (+{added} new from sources)")

    fl = primary_meta.get("list", {})
    to_value  = fl.get("ToValue")  or _TO_VALUE  or 0xC0
    to_flag   = fl.get("ToFlag")   or _TO_FLAG   or 0x30
    to_ptr    = fl.get("Pointer")  or _LIST_POINTER_OFF or 0
    out = {
        "Roblox Version": roblox_ver,
        "Total Offsets": len(merged),
        "FFlagOffsets": {
            "FFlagList": {
                "ToValue":  to_value,
                "ToFlag":   to_flag,
                "Pointer":  to_ptr,
            },
            "FFlags": merged,
        }
    }

    path = _get_offsets_path()
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(out, f, indent=2)
    except Exception as e:
        return f"⚠ Save failed: {e}"

    _load_tables(path)
    try:
        _instance.flag_cache.clear()
        _instance.cached_singleton = 0
    except Exception:
        pass

    src_count = len(results)
    ver_str = f" (Roblox {roblox_ver})" if roblox_ver != "unknown" else ""
    return (
        f"✓ Offsets updated: {_ACTIVE_OFFSET_COUNT} flags from {src_count} source(s){ver_str}"
    )


def update_offsets_async(status_cb=None, done_cb=None):
    """
    Run update_offsets_from_remote in a background thread.
    done_cb(result: str) called on completion.
    """
    import threading

    def _run():
        result = update_offsets_from_remote(status_cb=status_cb)
        if done_cb:
            try: done_cb(result)
            except: pass

    t = threading.Thread(target=_run, daemon=True)
    t.start()
    return t


def get_offset_debug() -> str:
    return (f"Offsets={_ACTIVE_OFFSET_COUNT}, "
            f"ToValue=0x{_TO_VALUE:X}, "
            f"Types={len(_FLAG_TYPES)}")



def _fnv1a64(name: str) -> int:
    h = 0xcbf29ce484222325
    for c in name:
        h ^= ord(c)
        h  = (h * 0x100000001b3) & 0xFFFFFFFFFFFFFFFF
    return h

def _is_ptr(p) -> bool:
    return bool(p and 0x10000 < p < 0x7FFFFFFFFFFF)

def _guess_type(name: str) -> str:
    for pfx, t in _PREFIX_TYPE.items():
        if name.startswith(pfx):
            return t
    return "int"

_INT32_MIN = -2147483648
_INT32_MAX =  2147483647

def _clamp_int32(v: int) -> int:
    """Clamp to signed int32 — WriteProcessMemory writes exactly 4 bytes."""
    return max(_INT32_MIN, min(_INT32_MAX, v))

def _infer_type(name: str, value) -> tuple:
    t = _FLAG_TYPES.get(name, "").lower() or _guess_type(name)
    v = str(value).strip().lower()
    if t == "bool" or v in ("true", "false"):
        return (1 if v in ("true", "1") else 0), "bool"
    if t == "float":
        try: return float(value), "float"
        except: return 0.0, "float"
    if t == "string":
        return str(value), "string"
    try:
        if "." in str(value): return float(value), "float"
        return _clamp_int32(int(value)), "int"
    except:
        return 0, "int"



class SingletonInjector:
    def __init__(self):
        self.pm               = None
        self.module           = None
        self._write_handle    = None
        self.cached_singleton = 0
        self._list_off        = 24
        self._mask_off        = 48
        self.flag_cache: dict = {}


    def is_process_alive(self) -> bool:
        if not self.pm or not self.pm.process_handle:
            return False
        ec = ctypes.wintypes.DWORD()
        if not kernel32.GetExitCodeProcess(self.pm.process_handle, byref(ec)):
            return False
        return ec.value == 259

    def attach(self) -> bool:
        try:
            self.pm     = pymem.Pymem("RobloxPlayerBeta.exe")
            self.module = pymem.process.module_from_name(
                self.pm.process_handle, "RobloxPlayerBeta.exe")
            self.flag_cache.clear()
            self.cached_singleton = 0
            self._skipped_logged  = False
            if self._write_handle:
                try: kernel32.CloseHandle(self._write_handle)
                except: pass
            self._write_handle = kernel32.OpenProcess(
                PROCESS_VM_WRITE | PROCESS_VM_OPERATION |
                PROCESS_VM_READ  | PROCESS_QUERY_LIMITED_INFORMATION,
                False, self.pm.process_id)
            return True
        except Exception as e:
            print(f"[Injector] attach failed: {e}")
            self.pm = self.module = self._write_handle = None
            return False

    def detach(self):
        if self._write_handle:
            try: kernel32.CloseHandle(self._write_handle)
            except: pass
        self._write_handle    = None
        self.pm               = None
        self.module           = None
        self.cached_singleton = 0
        self.flag_cache.clear()


    def _ru64(self, addr: int) -> int:
        try: return self.pm.read_ulonglong(addr)
        except: return 0

    def _rb(self, addr: int, n: int) -> bytes:
        try: return self.pm.read_bytes(addr, n)
        except: return b'\x00' * n


    def _val_ptr_via_offset(self, name: str) -> int:
        """
        Direct RVA formula: value_addr = module_base + RVA
        Offsets in fflags.json are direct RVAs to the value field.
        No +ToValue, no +0x08 — just module_base + offset.
        Verifies the resulting address is readable before returning.
        """
        offset = _FLAG_OFFSETS.get(name)
        if offset is None:
            clean = name
            for pfx in sorted(_PREFIX_TYPE, key=len, reverse=True):
                if name.startswith(pfx):
                    clean = name[len(pfx):]
                    break
            for pfx in ("", *_PREFIX_TYPE):
                cand = pfx + clean
                if cand in _FLAG_OFFSETS:
                    offset = _FLAG_OFFSETS[cand]
                    break
        if offset is None:
            return 0
        vp = self.module.lpBaseOfDll + offset
        try:
            self.pm.read_bytes(vp, 4)
            return vp
        except Exception:
            return 0


    def _scan_pattern(self, pat: bytes, rel_off: int, next_off: int):
        try:
            base  = self.module.lpBaseOfDll
            chunk = self.pm.read_bytes(base, min(0x800000, self.module.SizeOfImage))
            plen  = len(pat)
            for i in range(len(chunk) - plen - 8):
                ok = True
                for j, b in enumerate(pat):
                    if b != ord('.') and chunk[i+j] != b:
                        ok = False; break
                if not ok: continue
                rel = struct.unpack_from('<i', chunk, i + rel_off)[0]
                abs_ptr = base + i + next_off + rel
                if _is_ptr(abs_ptr):
                    val = self._ru64(abs_ptr)
                    if _is_ptr(val):
                        yield val
        except: pass

    def _probe_singleton(self, ptr: int, flag_name: str):
        clean = flag_name
        for pfx in sorted(_PREFIX_TYPE, key=len, reverse=True):
            if flag_name.startswith(pfx):
                clean = flag_name[len(pfx):]
                break
        for name in (clean, flag_name):
            h = _fnv1a64(name)
            for lo in (24, 32, 40, 56, 16, 8):
                for mo in (lo+16, lo+24, lo+32, lo+8):
                    try:
                        ml = self._ru64(ptr + lo)
                        mm = self._ru64(ptr + mo)
                        if not _is_ptr(ml) or not mm or mm > 0xFFFFF: continue
                        idx  = h & mm
                        node = self._ru64(ml + idx*16 + 8)
                        for _ in range(100):
                            if not _is_ptr(node): break
                            for so in (32, 40, 24, 48):
                                try:
                                    d  = self._rb(node, so+24)
                                    sz = struct.unpack_from('<Q', d, so)[0]
                                    cp = struct.unpack_from('<Q', d, so+8)[0]
                                    if sz != len(name) or sz==0 or sz>128: continue
                                    if not 0 < cp < 0x10000000: continue
                                    sa = struct.unpack_from('<Q', d, 16)[0] if cp > 15 else node+16
                                    if not _is_ptr(sa): continue
                                    if self._rb(sa, sz).decode('ascii','replace') == name:
                                        return lo, mo
                                except: continue
                            try: node = self._ru64(node+8)
                            except: break
                    except: continue
        return None

    def get_singleton(self) -> int:
        if self.cached_singleton:
            return self.cached_singleton
        if not self.pm or not self.module:
            return 0

        PATTERNS = [
            (bytes([0x48,0x83,0xEC,0x38,0x48,0x8B,0x0D]), 7, 11),
            (bytes([0x48,0x8B,0x0D]), 3, 7),
            (bytes([0x4C,0x8B,0x05]), 3, 7),
            (bytes([0x48,0x8B,0x05]), 3, 7),
            (bytes([0x4C,0x8B,0x0D]), 3, 7),
            (bytes([0x48,0x83,0xEC,0x28,0x48,0x8B,0x0D]), 7, 11),
            (bytes([0x48,0x83,0xEC,0x20,0x48,0x8B,0x0D]), 7, 11),
            (bytes([0x53,0x48,0x83,0xEC,0x20,0x48,0x8B,0x0D]), 8, 12),
            (bytes([0x48,0x83,0xEC,0x20,0x48,0x8B,0x05]), 7, 11),
        ]
        PAGE = 0x10000

        try:
            base  = self.module.lpBaseOfDll
            total = min(self.module.SizeOfImage, 0x800000)
            found = None
            candidates = set()

            for PATTERN, rel_off, next_off in PATTERNS:
                plen   = len(PATTERN)
                offset = 0
                while offset < total:
                    chunk_size = min(PAGE, total - offset)
                    try:
                        chunk = self.pm.read_bytes(base + offset, chunk_size)
                    except:
                        offset += PAGE
                        continue
                    for i in range(len(chunk) - plen - 8):
                        match = True
                        for j in range(plen):
                            if chunk[i+j] != PATTERN[j]:
                                match = False; break
                        if not match:
                            continue
                        try:
                            rel = struct.unpack_from('<i', chunk, i + rel_off)[0]
                            ptr = self._ru64(base + offset + i + next_off + rel)
                            if _is_ptr(ptr):
                                candidates.add(ptr)
                        except:
                            pass
                    offset += PAGE

            scored = []
            for ptr in candidates:
                try:
                    score = 0
                    for list_off, mask_off in [(24, 48), (0, 8), (8, 16), (16, 24)]:
                        m_list = self._ru64(ptr + list_off)
                        m_mask = self._ru64(ptr + mask_off)
                        if _is_ptr(m_list) and 0 < m_mask < 0x1FFFFFF:
                            score += 1
                    if score > 0:
                        scored.append((score, ptr))
                except:
                    pass

            if scored:
                scored.sort(reverse=True)
                found = scored[0][1]

            if found:
                self.cached_singleton = found
                print(f"[Injector] Singleton: 0x{found:X}")
                return found

        except Exception as e:
            print(f"[Injector] Singleton scan error: {e}")

        if _LIST_POINTER_OFF:
            try:
                base = self.module.lpBaseOfDll
                ptr  = self._ru64(base + _LIST_POINTER_OFF)
                if _is_ptr(ptr):
                    self.cached_singleton = ptr
                    print(f"[Injector] Singleton via ListPointer: 0x{ptr:X}")
                    return ptr
            except: pass

        print("[Injector] Singleton not found.")
        return 0

    def _find_in_map(self, s_ptr: int, name: str) -> int:
        """
        Walk singleton hash-map.
        Based on reverse-engineered AHK injector (cyphstrap):

        m_list = ReadUInt64(sgl + 24)
        m_mask = ReadUInt64(sgl + 48)
        bucket = hash & m_mask
        node   = ReadUInt64(m_list + bucket*16 + 8)

        Per node (read 64 bytes):
          next    = entry[8]   (Int64)
          str_ptr = entry[16]  (Int64) — ptr if capacity > 15, else inline
          str_sz  = entry[32]  (Int64)
          str_alc = entry[40]  (Int64)
          vpr     = entry[48]  (Int64)  ← key field

        vp = ReadUInt64(vpr + 0xC0)
        WriteProcessMemory(vp, value)
        """
        try:
            ml = self._ru64(s_ptr + 24)
            mm = self._ru64(s_ptr + 48)
            if not _is_ptr(ml) or not mm or mm > 0xFFFFFF:
                return 0
            h    = _fnv1a64(name)
            idx  = h & mm
            node = self._ru64(ml + idx*16 + 8)
            nl   = len(name)
            m_end = self._ru64(s_ptr + 8)

            for _ in range(300):
                if node == 0 or node == m_end or not _is_ptr(node):
                    break
                try:
                    entry = self._rb(node, 64)
                except:
                    break

                try:
                    str_sz  = struct.unpack_from('<q', entry, 32)[0]
                    str_alc = struct.unpack_from('<q', entry, 40)[0]
                    vpr     = struct.unpack_from('<q', entry, 48)[0]

                    if str_sz == nl and 0 < str_sz < 256:
                        if str_alc > 15:
                            str_ptr = struct.unpack_from('<Q', entry, 16)[0]
                            if _is_ptr(str_ptr):
                                raw = self._rb(str_ptr, nl)
                            else:
                                raw = b''
                        else:
                            raw = entry[16:16+nl]

                        if raw.decode('ascii', 'replace') == name:
                            if not vpr:
                                return 0
                            return vpr + 0x08
                except:
                    pass

                try:
                    nxt = struct.unpack_from('<q', entry, 8)[0]
                    node = nxt if _is_ptr(nxt) else 0
                except:
                    break

        except:
            pass
        return 0

    def _val_ptr_via_singleton(self, name: str) -> int:
        """
        Singleton fallback — walk hash-map.
        _find_in_map now returns vp directly (ReadUInt64(vpr+0xC0)).
        Try exact name first, then stripped variants.
        """
        s = self.get_singleton()
        if not s: return 0

        clean = name
        for pfx in sorted(_PREFIX_TYPE, key=len, reverse=True):
            if name.startswith(pfx):
                clean = name[len(pfx):]
                break

        variants, seen = [], set()
        for v in [name, clean] + [p+clean for p in _PREFIXES]:
            if v not in seen:
                seen.add(v); variants.append(v)

        for v in variants:
            vp = self._find_in_map(s, v)
            if vp: return vp
        return 0


    def find_flag(self, name: str) -> int:
        """
        Returns val_ptr using Method 1 first, then Method 2 as fallback.
        Result is cached so subsequent calls are free.
        """
        if name in self.flag_cache:
            return self.flag_cache[name]

        vp = self._val_ptr_via_offset(name)

        if not vp:
            vp = self._val_ptr_via_singleton(name)

        if vp:
            self.flag_cache[name] = vp
        return vp


    def set_value_raw(self, val_ptr: int, value, ftype: str) -> bool:
        try:
            buf     = c_float(float(value)) if ftype == "float" else c_int32(int(value))
            written = c_size_t(0)
            handle  = self._write_handle or self.pm.process_handle
            ok = _WriteProcessMemory(handle, val_ptr, byref(buf), 4, byref(written))
            if ok and written.value == 4: return True
            if ctypes.get_last_error() == 5:
                raise PermissionError("ACCESS_DENIED")
            return False
        except PermissionError: raise
        except Exception as e:
            if "error_code: 5" in str(e).lower():
                raise PermissionError("ACCESS_DENIED")
            return False

    def set_value(self, name: str, value) -> bool:
        vp = self.find_flag(name)
        if not vp: return False
        python_val, ftype = _infer_type(name, value)
        if ftype == "string": return False
        return self.set_value_raw(vp, python_val, ftype)

    def get_val_raw(self, val_ptr: int, ftype: str):
        try:
            if ftype == "float": return round(self.pm.read_float(val_ptr), 3)
            return self.pm.read_int(val_ptr)
        except: return None

    def _resolve_val_ptr(self, flag_addr):
        return flag_addr, 0xC0


_instance = SingletonInjector()



def _get_main_thread_id(pid: int) -> int:
    """Return the main thread ID of a process (earliest created thread)."""
    TH32CS_SNAPTHREAD = 0x00000004
    class THREADENTRY32(ctypes.Structure):
        _fields_ = [
            ("dwSize",             ctypes.wintypes.DWORD),
            ("cntUsage",           ctypes.wintypes.DWORD),
            ("th32ThreadID",       ctypes.wintypes.DWORD),
            ("th32OwnerProcessID", ctypes.wintypes.DWORD),
            ("tpBasePri",          ctypes.c_long),
            ("tpDeltaPri",         ctypes.c_long),
            ("dwFlags",            ctypes.wintypes.DWORD),
        ]
    snap = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPTHREAD, 0)
    if snap == ctypes.wintypes.HANDLE(-1).value:
        return 0
    try:
        te = THREADENTRY32()
        te.dwSize = ctypes.sizeof(THREADENTRY32)
        tid = 0
        if kernel32.Thread32First(snap, byref(te)):
            while True:
                if te.th32OwnerProcessID == pid:
                    tid = te.th32ThreadID
                    break
                if not kernel32.Thread32Next(snap, byref(te)):
                    break
        return tid
    finally:
        kernel32.CloseHandle(snap)


def _suspend_process(pid: int):
    """Suspend all threads of a process."""
    TH32CS_SNAPTHREAD = 0x00000004
    THREAD_SUSPEND_RESUME = 0x0002

    class THREADENTRY32(ctypes.Structure):
        _fields_ = [
            ("dwSize",             ctypes.wintypes.DWORD),
            ("cntUsage",           ctypes.wintypes.DWORD),
            ("th32ThreadID",       ctypes.wintypes.DWORD),
            ("th32OwnerProcessID", ctypes.wintypes.DWORD),
            ("tpBasePri",         ctypes.c_long),
            ("tpDeltaPri",         ctypes.c_long),
            ("dwFlags",            ctypes.wintypes.DWORD),
        ]

    snap = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPTHREAD, 0)
    if snap == ctypes.wintypes.HANDLE(-1).value:
        return
    try:
        te = THREADENTRY32()
        te.dwSize = ctypes.sizeof(THREADENTRY32)
        if kernel32.Thread32First(snap, byref(te)):
            while True:
                if te.th32OwnerProcessID == pid:
                    h = kernel32.OpenThread(THREAD_SUSPEND_RESUME, False, te.th32ThreadID)
                    if h:
                        kernel32.SuspendThread(h)
                        kernel32.CloseHandle(h)
                if not kernel32.Thread32Next(snap, byref(te)):
                    break
    finally:
        kernel32.CloseHandle(snap)


def _resume_process(pid: int):
    """Resume all threads of a process."""
    TH32CS_SNAPTHREAD = 0x00000004
    THREAD_SUSPEND_RESUME = 0x0002

    class THREADENTRY32(ctypes.Structure):
        _fields_ = [
            ("dwSize",             ctypes.wintypes.DWORD),
            ("cntUsage",           ctypes.wintypes.DWORD),
            ("th32ThreadID",       ctypes.wintypes.DWORD),
            ("th32OwnerProcessID", ctypes.wintypes.DWORD),
            ("tpBasePri",         ctypes.c_long),
            ("tpDeltaPri",         ctypes.c_long),
            ("dwFlags",            ctypes.wintypes.DWORD),
        ]

    snap = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPTHREAD, 0)
    if snap == ctypes.wintypes.HANDLE(-1).value:
        return
    try:
        te = THREADENTRY32()
        te.dwSize = ctypes.sizeof(THREADENTRY32)
        if kernel32.Thread32First(snap, byref(te)):
            while True:
                if te.th32OwnerProcessID == pid:
                    h = kernel32.OpenThread(THREAD_SUSPEND_RESUME, False, te.th32ThreadID)
                    if h:
                        kernel32.ResumeThread(h)
                        kernel32.CloseHandle(h)
                if not kernel32.Thread32Next(snap, byref(te)):
                    break
    finally:
        kernel32.CloseHandle(snap)


_BATCH_SIZE = 50


def apply_flags(data: dict) -> str:
    if _instance.pm and not _instance.is_process_alive():
        _instance.detach()
    if not _instance.pm:
        if not _instance.attach():
            return "Roblox not found."

    _instance.flag_cache.clear()

    if not _FLAG_OFFSETS:
        return "⚠ Offset table empty — place fflags.json in offsets/ folder."

    offset_resolved: list[tuple] = []
    singleton_needed: list[tuple] = []

    for name, value in data.items():
        try:
            vp = _instance._val_ptr_via_offset(name)
            if vp:
                python_val, ftype = _infer_type(name, value)
                if ftype != "string":
                    offset_resolved.append((name, vp, python_val, ftype))
                    _instance.flag_cache[name] = vp
            else:
                singleton_needed.append((name, value))
        except Exception:
            singleton_needed.append((name, value))

    success = 0
    for i, (name, vp, pv, ft) in enumerate(offset_resolved):
        try:
            if _instance.set_value_raw(vp, pv, ft):
                success += 1
        except PermissionError:
            raise
        except Exception:
            pass
        if i > 0 and i % 50 == 0:
            time.sleep(0.001)

    if singleton_needed and _instance.cached_singleton:
        for name, value in singleton_needed:
            try:
                vp = _instance._val_ptr_via_singleton(name)
                if not vp:
                    continue
                _instance.flag_cache[name] = vp
                python_val, ftype = _infer_type(name, value)
                if ftype == "string":
                    continue
                if _instance.set_value_raw(vp, python_val, ftype):
                    success += 1
            except PermissionError:
                raise
            except Exception:
                pass

    applied_names = {name for name, *_ in offset_resolved}
    if _instance.cached_singleton:
        applied_names |= {name for name, value in singleton_needed
                          if name in _instance.flag_cache}
    skipped = [name for name in data if name not in applied_names]
    _instance._last_skipped = skipped
    if skipped and not getattr(_instance, '_skipped_logged', False):
        _instance._skipped_logged = True
        print(f"[Injector] Skipped {len(skipped)} flags (not in offset table):")
        for name in skipped:
            print(f"  ✗ {name}")

    total = len(data)
    return f"Applied {success}/{total} FFlags."


def auto_apply_loop(state):
    while getattr(state, 'auto_apply_enabled', False):
        try:
            if not _instance.is_process_alive():
                _instance.detach()
                if not _instance.attach():
                    time.sleep(5); continue

            from core.config_manager import load_flags
            data = load_flags(state.config_file)
            _instance.flag_cache.clear()
            result = apply_flags(data)

            try:
                from core.logger import write_log
                write_log(state.logs_dir, f"[AUTO] {result}")
            except: pass

            if result.startswith("⚠"):
                state.auto_apply_enabled = False
                if hasattr(state, '_auto_apply_error_cb') and state._auto_apply_error_cb:
                    state._auto_apply_error_cb(result)
                return

        except PermissionError as e:
            state.auto_apply_enabled = False
            err = f"⚠ {e}"
            try:
                from core.logger import write_log
                write_log(state.logs_dir, f"[AUTO] {err}")
            except: pass
            if hasattr(state, '_auto_apply_error_cb') and state._auto_apply_error_cb:
                state._auto_apply_error_cb(err)
            return
        except: _instance.detach()
        time.sleep(5.0)


def re_apply_loop(data: dict, state):
    last_mtime:   float = 0.0
    last_pid:     int   = 0
    cached_flags: list  = []
    config_path = str(state.config_file)

    while getattr(state, 'injection_thread_running', True):
        try:
            if not _instance.is_process_alive():
                _instance.detach()
                cached_flags = []; last_mtime = 0.0; last_pid = 0
                time.sleep(5)
                if not _instance.attach(): continue
                _instance.flag_cache.clear()
                continue

            pid = _instance.pm.process_id if _instance.pm else 0
            if pid != last_pid:
                _instance.flag_cache.clear()
                _instance.cached_singleton = 0
                cached_flags = []; last_mtime = 0.0; last_pid = pid

            try:
                mtime = os.path.getmtime(config_path)
                if mtime != last_mtime:
                    from core.config_manager import load_flags
                    new_data = load_flags(state.config_file)
                    _instance.flag_cache.clear()
                    _instance.cached_singleton = 0

                    temp = []
                    for name, value in new_data.items():
                        vp = _instance.find_flag(name)
                        if not vp: continue
                        pv, ft = _infer_type(name, value)
                        if ft == "string": continue
                        temp.append((vp, pv, ft, name))

                    cached_flags = temp; last_mtime = mtime; data = new_data
            except: pass

            restored = 0
            for vp, target, ftype, name in cached_flags:
                try:
                    cur = _instance.get_val_raw(vp, ftype)
                    if cur is not None and cur != target:
                        if _instance.set_value_raw(vp, target, ftype):
                            restored += 1
                except:
                    cached_flags = []; last_mtime = 0.0; break

            if restored > 0:
                try:
                    from core.logger import write_log
                    write_log(state.logs_dir, f"[RE-APPLY] Restored {restored} flag(s).")
                except: pass

        except:
            _instance.detach()
            cached_flags = []; last_mtime = 0.0; last_pid = 0

        time.sleep(2.0)


def warmup_singleton():
    """
    Call this in a background thread right after Roblox is detected.
    Finds and caches the singleton so Apply is instant when user clicks it.
    """
    import threading
    def _bg():
        try:
            if not _instance.pm:
                if not _instance.attach():
                    return
            _instance.get_singleton()
            print(f"[Injector] Warmup done, singleton=0x{_instance.cached_singleton:X}")
        except Exception as e:
            print(f"[Injector] Warmup failed: {e}")
    t = threading.Thread(target=_bg, daemon=True)
    t.start()
