from __future__ import annotations

from datetime import datetime
from pathlib import Path


def ensure_logs_dir(logs_dir: Path) -> None:
    logs_dir.mkdir(parents=True, exist_ok=True)


def write_log(logs_dir: Path, message: str) -> None:
    ensure_logs_dir(logs_dir)
    log_file = logs_dir / "app.log"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with log_file.open("a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")