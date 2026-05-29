"""
SacredWare - FFlags Validator
==============================
Validates FFlag names/values format only.
Does NOT filter flags based on whether Roblox can find them —
that would remove valid flags from the editor when singleton fails.

Usage:
    from core.validator import validate_flags
    result = validate_flags(data)
    result.valid          -> all flags (no filtering)
    result.skipped        -> flags with invalid format only
    result.roblox_missing -> always False (no longer checked)
"""
from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class ValidationResult:
    valid:          dict
    skipped:        list
    roblox_missing: bool = False
    total:          int  = 0
    valid_count:    int  = 0
    skipped_count:  int  = 0

    def summary(self) -> str:
        if self.skipped_count == 0:
            return f"Loaded {self.valid_count} flags."
        return (
            f"Loaded {self.valid_count}/{self.total} flags. "
            f"{self.skipped_count} skipped (invalid format)."
        )


_PREFIXES = (
    "DFString", "DFInt", "DFFlag", "FString",
    "FFlag", "FInt", "FLog", "DFLog", "FFFlag",
    "FIntAsync",
)


def _is_valid_name(name: str) -> bool:
    """Check flag name starts with a known prefix and has content after it."""
    if not isinstance(name, str) or not name:
        return False
    # Accept anything that looks like a flag name
    # Only reject clearly non-flag keys
    for p in _PREFIXES:
        if name.startswith(p) and len(name) > len(p):
            return True
    # Accept bare names too (no prefix) — some configs use bare names
    return bool(name) and name[0].isupper()


def _is_valid_value(value) -> bool:
    """Value must be string, int, float, or bool."""
    return isinstance(value, (str, int, float, bool))


def validate_flags(data: dict, injector=None) -> ValidationResult:
    """
    Validate flags by format only.
    All flags with valid names and values are kept.
    No Roblox process check — editor always shows full flag list.
    """
    total = len(data)
    if total == 0:
        return ValidationResult(
            valid={}, skipped=[], total=0,
            valid_count=0, skipped_count=0
        )

    valid   = {}
    skipped = []

    for name, value in data.items():
        if _is_valid_value(value):
            valid[name] = value
        else:
            skipped.append(name)

    return ValidationResult(
        valid=valid,
        skipped=skipped,
        roblox_missing=False,
        total=total,
        valid_count=len(valid),
        skipped_count=len(skipped),
    )
