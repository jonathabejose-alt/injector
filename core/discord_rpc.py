import time
import threading

CLIENT_ID = "1501965679966945453"

_rpc        = None
_start_time = None
_connected  = False
_lock       = threading.Lock()
_stop_evt   = threading.Event()


def _connect():
    global _rpc, _start_time, _connected
    try:
        from pypresence import Presence
        _rpc = Presence(CLIENT_ID)
        _rpc.connect()
        _start_time = int(time.time())
        _connected  = True
        return True
    except Exception as e:
        print(f"[RPC] {e}")
        _connected = False
        return False


def _push():
    try:
        with _lock:
            _rpc.update(
                state = "Best FFlags Injector for Roblox",
                start = _start_time,
            )
    except Exception:
        pass


def _loop():
    while not _stop_evt.is_set():
        if _connected:
            _push()
        _stop_evt.wait(14)


def start():
    _stop_evt.clear()
    def _bg():
        if not _connect():
            time.sleep(5)
            _connect()
        if _connected:
            _push()
        _loop()
    threading.Thread(target=_bg, daemon=True).start()


def stop():
    global _connected
    _stop_evt.set()
    try:
        if _rpc and _connected:
            _rpc.close()
    except Exception:
        pass
    _connected = False
