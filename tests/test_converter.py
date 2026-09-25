import unittest

from quickconvert import BinaryUnit, convert, format_size, parse


class ConverterTests(unittest.TestCase):
    def test_converts_between_units(self):
        self.assertEqual(convert(2, "MiB", "KiB"), 2048)
        self.assertEqual(convert(1, BinaryUnit.GiB, "bytes"), 1024**3)

    def test_accepts_decimal_values(self):
        self.assertEqual(convert(1.5, "GiB", "MiB"), 1536)

    def test_rejects_negative_values(self):
        with self.assertRaises(ValueError):
            convert(-1, "B", "KiB")

    def test_parses_size_strings(self):
        self.assertEqual(parse(" 2.5 GiB "), (2.5, BinaryUnit.GiB))

    def test_formats_size(self):
        self.assertEqual(format_size(1.5, "GiB"), "1.50 GiB")

    def test_rejects_invalid_input(self):
        with self.assertRaises(ValueError):
            parse("not a size")
        with self.assertRaises(ValueError):
            convert(1, "stones", "B")

    def test_parses_decimal_formats_and_rejects_non_finite_input(self):
        self.assertEqual(parse("1. GiB"), (1.0, BinaryUnit.GiB))
        self.assertEqual(parse(".5 KiB"), (0.5, BinaryUnit.KiB))
        with self.assertRaises(ValueError):
            convert(float("nan"), "B", "KiB")
        with self.assertRaises(ValueError):
            format_size(float("inf"), "B")


if __name__ == "__main__":
    unittest.main()
