"""Fast, dependency-free data size conversions."""

from .converter import BinaryUnit, convert, parse, format_size

__all__ = ["BinaryUnit", "convert", "parse", "format_size"]
__version__ = "0.1.0"
