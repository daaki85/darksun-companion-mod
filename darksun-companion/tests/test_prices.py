"""The leader's CHA and shop prices (prices.py), as Baldur's Gate has them."""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dscompanion import prices


class PricesTests(unittest.TestCase):
    def test_discount(self):
        self.assertEqual([prices.discount(c) for c in (3, 15, 16, 17, 18, 19, 20, 25)],
                         [0, 0, 5, 10, 15, 20, 25, 25])

    def test_price(self):
        self.assertEqual(prices.price(1000, 18), 850)
        self.assertEqual(prices.price(1000, 12), 1000)
        self.assertEqual(prices.price(10, 20), 7)
        self.assertEqual(prices.price(1, 25), 1)
        self.assertEqual(prices.price(prices.NOT_FOR_SALE, 25), prices.NOT_FOR_SALE)
        self.assertEqual(prices.price(0, 25), 0)


if __name__ == "__main__":
    unittest.main()
