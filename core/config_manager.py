from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


def ensure_config_exists(config_file: Path) -> None:
    config_file.parent.mkdir(parents=True, exist_ok=True)
    if not config_file.exists():
        config_file.write_text("{}", encoding="utf-8")


def ensure_backup_dir(backup_dir: Path) -> None:
    backup_dir.mkdir(parents=True, exist_ok=True)


def load_flags(config_file: Path) -> dict[str, Any]:
    ensure_config_exists(config_file)

    with config_file.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, dict):
        raise ValueError("flags.json must contain a JSON object.")

    return data


def save_flags(config_file: Path, data: dict[str, Any]) -> None:
    ensure_config_exists(config_file)

    with config_file.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def count_flags(data: dict[str, Any]) -> int:
    return len(data)


def validate_flags(data: Any) -> tuple[bool, str]:
    if not isinstance(data, dict):
        return False, "Config must be a JSON object."

    for key, value in data.items():
        if not isinstance(key, str):
            return False, "All flag names must be strings."

        if not isinstance(value, (str, int, float, bool)):
            return False, f"Invalid value type for flag '{key}'."

    return True, "Config is valid."


def create_backup(config_file: Path, backup_dir: Path) -> Path:
    ensure_config_exists(config_file)
    ensure_backup_dir(backup_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = backup_dir / f"flags_backup_{timestamp}.json"
    backup_file.write_text(config_file.read_text(encoding="utf-8"), encoding="utf-8")
    return backup_file


def reset_config_to_empty(config_file: Path) -> None:
    save_flags(config_file, {})


def get_pretty_json(config_file: Path) -> str:
    data = load_flags(config_file)
    return json.dumps(data, indent=4, ensure_ascii=False)


def save_json_from_text(config_file: Path, raw_text: str) -> None:
    parsed = json.loads(raw_text)
    if not isinstance(parsed, dict):
        raise ValueError("JSON root must be an object.")
    save_flags(config_file, parsed)