import threading
import time


def trigger(fps=15, duration=0.7, original_fps=2147483647):
    def _run():
        try:
            from core.injector import _instance, _FLAG_OFFSETS

            if not _instance.pm or not _instance.is_process_alive():
                _instance.detach()
                if not _instance.attach():
                    return

            base   = _instance.module.lpBaseOfDll
            offset = (_FLAG_OFFSETS.get("TaskSchedulerTargetFps") or
                      _FLAG_OFFSETS.get("DFIntTaskSchedulerTargetFps"))
            if not offset:
                return

            addr = base + offset
            _instance.set_value_raw(addr, fps, "int")
            time.sleep(duration)
            _instance.set_value_raw(addr, original_fps, "int")

        except Exception as e:
            print(f"[LS] {e}")

    threading.Thread(target=_run, daemon=True).start()
