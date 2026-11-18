import unittest

from pricing import apply_discount


class ApplyDiscountTest(unittest.TestCase):
    def test_zero_percent_keeps_total(self):
        self.assertEqual(apply_discount(1000, 0), 1000)

    def test_negative_percent_rejected(self):
        with self.assertRaises(ValueError):
            apply_discount(1000, -5)


if __name__ == "__main__":
    unittest.main()
