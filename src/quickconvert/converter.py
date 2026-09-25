"""Conversion helpers for bytes and binary data-size units."""

from __future__ import annotations

from enum import Enum
import re


class BinaryUnit(str, Enum):
    """Supported binary units, where each step is 1024."""

    B = "B"
    KiB = "KiB"
    MiB = "MiB"
    GiB = "GiB"
    TiB = "TiB"

    @property
    def multiplier(self) -> int:
        """Return the number of bytes represented by one unit."""
        return 1024 ** list(BinaryUnit).index(self)


_UNIT_ALIASES = {
    "b": BinaryUnit.B,
    "byte": BinaryUnit.B,
    "bytes": BinaryUnit.B,
    "kib": BinaryUnit.KiB,
    "kb": BinaryUnit.KiB,
    "kibibyte": BinaryUnit.KiB,
    "kibibytes": BinaryUnit.KiB,
    "mib": BinaryUnit.MiB,
    "mb": BinaryUnit.MiB,
    "mibibyte": BinaryUnit.MiB,
    "mibibytes": BinaryUnit.MiB,
    "gib": BinaryUnit.GiB,
    "gb": BinaryUnit.GiB,
    "gibibyte": BinaryUnit.GiB,
    "gibibytes": BinaryUnit.GiB,
    "tib": BinaryUnit.TiB,
    "tb": BinaryUnit.TiB,
    "tibibyte": BinaryUnit.TiB,
    "tibibytes": BinaryUnit.TiB,
}


def _unit(value: BinaryUnit | str) -> BinaryUnit:
    if isinstance(value, BinaryUnit):
        return value
    try:
        return _UNIT_ALIASES[value.strip().lower()]
    except (AttributeError, KeyError) as exc:
        raise ValueError(f"Unsupported binary unit: {value!r}") from exc


def convert(value: float, from_unit: BinaryUnit | str, to_unit: BinaryUnit | str) -> float:
    """Convert a numeric value between binary units.

    ``KB`` and similar short aliases are accepted for convenience and are
    interpreted as their binary counterparts (1024 bytes per KiB).
    """
    if value < 0:
        raise ValueError("value must be non-negative")
    source = _unit(from_unit)
    target = _unit(to_unit)
    return value * source.multiplier / target.multiplier


_SIZE_PATTERN = re.compile(r"^\s*(?P<value>\d+(?:\.\d+)?)\s*(?P<unit>[a-zA-Z]+)\s*$")


def parse(size: str) -> tuple[float, BinaryUnit]:
    """Parse a string such as ``\"2.5 GiB\"`` into a value and unit."""
    match = _SIZE_PATTERN.match(size)
    if match is None:
        raise ValueError(f"Invalid size: {size!r}")
    return float(match.group("value")), _unit(match.group("unit"))


def format_size(value: float, unit: BinaryUnit | str = BinaryUnit.B, precision: int = 2) -> str:
    """Format a size with a normalized unit, such as ``\"1.50 MiB\"``."""
    if precision < 0:
        raise ValueError("precision must be non-negative")
    normalized = _unit(unit)
    return f"{value:.{precision}f} {normalized.value}"
