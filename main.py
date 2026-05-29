import sys
import os
import traceback

if getattr(sys, 'frozen', False):
    base = sys._MEIPASS
else:
    base = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, base)

def _show_error(msg):
    try:
        from PyQt6.QtWidgets import QApplication, QMessageBox
        app = QApplication.instance() or QApplication(sys.argv)
        QMessageBox.critical(None, "SacredWare - Error", msg)
    except Exception:
        print(msg, file=sys.stderr)

def _check_dependencies():
    missing = []
    for pkg, imp in [("PyQt6", "PyQt6.QtWidgets"), ("pymem", "pymem"), ("Pillow", "PIL")]:
        try:
            __import__(imp)
        except ImportError:
            missing.append(pkg)
    return missing

if __name__ == "__main__":
    missing = _check_dependencies()
    if missing:
        _show_error(
            f"Missing required packages:\n  {', '.join(missing)}\n\n"
            f"Install with:\n  pip install {' '.join(missing)}"
        )
        sys.exit(1)

    try:
        from core.app_state import AppState
        from core.config_manager import ensure_config_exists, load_flags
        from ui.gui import run_gui
    except Exception:
        _show_error(f"Failed to load SacredWare:\n\n{traceback.format_exc()}")
        sys.exit(1)

    state = AppState()
    try:
        ensure_config_exists(state.config_file)
    except Exception:
        pass
    try:
        state.last_loaded_data = load_flags(state.config_file)
    except Exception:
        pass
    try:
        from core.discord_rpc import start as rpc_start
        rpc_start()
    except Exception:
        pass
    try:
        run_gui(state)
    except Exception:
        _show_error(f"Fatal error:\n\n{traceback.format_exc()}")
        sys.exit(1)
