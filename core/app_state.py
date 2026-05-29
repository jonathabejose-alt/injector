from __future__ import annotations

import threading
from dataclasses import dataclass, field
from pathlib import Path

@dataclass
class AppState:
    app_name: str = "sacredware"
    config_dir: Path = Path.home() / "AppData" / "Roaming" / "SacredWare"
    config_file: Path = Path.home() / "AppData" / "Roaming" / "SacredWare" / "flags.json"
    backup_dir: Path = Path.home() / "AppData" / "Roaming" / "SacredWare" / "backups"
    logs_dir: Path = Path.cwd() / "logs"

    loaded_flags_count: int = 0
    last_status: str = "Ready"
    running: bool = True
    last_loaded_data: dict = field(default_factory=dict)
    integration_enabled: bool = False
    injection_thread_running: bool = False  # Флаг для re-apply loop
    injection_thread: threading.Thread | None = None  # Ссылка на поток
    auto_apply_enabled: bool = False  # Флаг Auto Apply (on/off)
    auto_apply_thread: threading.Thread | None = None  # Поток Auto Apply