from __future__ import annotations

import os
from pathlib import Path
import threading
import time

from core.app_state import AppState
from core.config_manager import (
    count_flags,
    create_backup,
    ensure_config_exists,
    get_pretty_json,
    load_flags,
    reset_config_to_empty,
    save_json_from_text,
    validate_flags,
)
from core.logger import write_log
from core.injector import apply_flags, re_apply_loop, auto_apply_loop

def open_folder(path: Path) -> None:
    os.startfile(path)  # type: ignore[attr-defined]


def open_file(path: Path) -> None:
    os.startfile(path)  # type: ignore[attr-defined]


def action_startup_load(state: AppState) -> str:
    ensure_config_exists(state.config_file)
    data = load_flags(state.config_file)
    state.last_loaded_data = data
    state.loaded_flags_count = count_flags(data)
    message = f"Loaded {state.loaded_flags_count} flags from {state.config_file}"
    write_log(state.logs_dir, message)
    return message


def action_manager(state: AppState) -> str:
    ensure_config_exists(state.config_file)
    open_folder(state.config_dir)
    message = f"Opened config folder: {state.config_dir}"
    write_log(state.logs_dir, message)
    return message


def action_open_config_file(state: AppState) -> str:
    ensure_config_exists(state.config_file)
    open_file(state.config_file)
    message = f"Opened config file: {state.config_file}"
    write_log(state.logs_dir, message)
    return message


def action_show_config(state: AppState) -> str:
    pretty = get_pretty_json(state.config_file)
    write_log(state.logs_dir, "Displayed current config in console.")
    return pretty


def action_validate(state: AppState) -> str:
    data = load_flags(state.config_file)
    is_valid, message = validate_flags(data)
    if is_valid:
        state.loaded_flags_count = count_flags(data)
        final_message = f"{message} Total flags: {state.loaded_flags_count}"
    else:
        final_message = f"Validation failed: {message}"

    write_log(state.logs_dir, final_message)
    return final_message


def action_backup(state: AppState) -> str:
    backup_file = create_backup(state.config_file, state.backup_dir)
    message = f"Backup created: {backup_file}"
    write_log(state.logs_dir, message)
    return message


def action_apply_all(state: AppState) -> str:
    data = load_flags(state.config_file)
    is_valid, message = validate_flags(data)
    if not is_valid:
        final_message = f"Apply aborted. {message}"
        write_log(state.logs_dir, final_message)
        return final_message

    state.last_loaded_data = data
    state.loaded_flags_count = len(data)

    apply_result = apply_flags(data)
    write_log(state.logs_dir, apply_result)

    if not state.injection_thread_running:
        state.injection_thread_running = True
        state.injection_thread = threading.Thread(
            target=re_apply_loop, 
            args=(data, state), 
            daemon=True
        )
        state.injection_thread.start()
        write_log(state.logs_dir, "Re-apply loop started.")

    return f"Processed {state.loaded_flags_count} flags. {apply_result}"

def action_kill_switch(state: AppState) -> str:
    state.last_loaded_data = {}
    state.loaded_flags_count = 0
    state.integration_enabled = False
    message = "Kill switch executed. Runtime state cleared."
    write_log(state.logs_dir, message)
    return message


def action_reset_config(state: AppState) -> str:
    reset_config_to_empty(state.config_file)
    state.last_loaded_data = {}
    state.loaded_flags_count = 0
    message = "flags.json was reset to an empty object."
    write_log(state.logs_dir, message)
    return message


def action_auto_apply(state: AppState) -> str:
    if not state.auto_apply_enabled:
        # Включаем Auto Apply
        state.auto_apply_enabled = True
        state.auto_apply_thread = threading.Thread(
            target=auto_apply_loop,
            args=(state,),
            daemon=True
        )
        state.auto_apply_thread.start()
        message = "Auto Apply turned on. FFlags will be injected every 5 seconds while Roblox is running."
        write_log(state.logs_dir, message)
        return message
    else:
        # Выключаем Auto Apply
        state.auto_apply_enabled = False
        message = "Auto Apply turned off."
        write_log(state.logs_dir, message)
        return message


def action_exit(state: AppState) -> str:
    state.running = False
    message = "Closing sacredware..."
    write_log(state.logs_dir, message)
    return message
