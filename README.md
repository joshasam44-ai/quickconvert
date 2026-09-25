# quickconvert

A tiny, dependency-free Python library for converting data sizes between bytes and binary units.

## Install

```bash
python -m pip install quickconvert
```

## Usage

```python
from quickconvert import convert, format_size, parse

megabytes = convert(2, "GiB", "MiB")
print(megabytes)  # 2048

value, unit = parse("2.5 GiB")
print(format_size(value, unit))  # 2.50 GiB
```

`B`, `KiB`, `MiB`, `GiB`, and `TiB` are supported. Common aliases such as `KB`, `MB`, and `GB` are accepted and use a 1024-byte step.

## Development

```bash
python -m unittest discover -s tests -v
python -m pip install build
python -m build
```

The project uses a `src/` layout and requires Python 3.9 or newer.
