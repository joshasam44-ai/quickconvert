"""Conversion helpers for bytes and binary data-size units."""

from __future__ import annotations

from enum import Enum
import math
import re
from numbers import Real


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


def _coerce_finite_number(value: float, *, name: str) -> float:
    """Coerce a numeric input to a finite float, rejecting invalid values."""
    if isinstance(value, bool) or not isinstance(value, Real):
        raise ValueError(f"{name} must be a finite number")
    try:
        numeric_value = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be a finite number") from exc
    if not math.isfinite(numeric_value):
        raise ValueError(f"{name} must be a finite number")
    return numeric_value


def convert(value: float, from_unit: BinaryUnit | str, to_unit: BinaryUnit | str) -> float:
    """Convert a numeric value between binary units.

    ``KB`` and similar short aliases are accepted for convenience and are
    interpreted as their binary counterparts (1024 bytes per KiB).
    """
    numeric_value = _coerce_finite_number(value, name="value")
    if numeric_value < 0:
        raise ValueError("value must be non-negative")
    source = _unit(from_unit)
    target = _unit(to_unit)
    return numeric_value * source.multiplier / target.multiplier


_SIZE_PATTERN = re.compile(r"^\s*(?P<value>\d+(?:\.\d*)?|\.\d+)\s*(?P<unit>[a-zA-Z]+)\s*$")


def parse(size: str) -> tuple[float, BinaryUnit]:
    """Parse a string such as ``\"2.5 GiB\"`` into a value and unit."""
    if not isinstance(size, str):
        raise ValueError(f"Invalid size: {size!r}")
    match = _SIZE_PATTERN.match(size)
    if match is None:
        raise ValueError(f"Invalid size: {size!r}")
    numeric_value = _coerce_finite_number(float(match.group("value")), name="value")
    return numeric_value, _unit(match.group("unit"))


def format_size(value: float, unit: BinaryUnit | str = BinaryUnit.B, precision: int = 2) -> str:
    """Format a size with a normalized unit, such as ``\"1.50 MiB\"``."""
    if isinstance(precision, bool) or not isinstance(precision, int):
        raise ValueError("precision must be a non-negative integer")
    if precision < 0:
        raise ValueError("precision must be non-negative")
    numeric_value = _coerce_finite_number(value, name="value")
    normalized = _unit(unit)
    return f"{numeric_value:.{precision}f} {normalized.value}"
