import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dscompanion import kits  # noqa: E402


class KitEffectTests(unittest.TestCase):
    def test_raider(self):
        self.assertEqual((kits.melee_damage(kits.RAIDER), kits.ac(kits.RAIDER, False), kits.move(kits.RAIDER)), (1, 1, 2))
        self.assertEqual(kits.name(kits.RAIDER), "Raider")

    def test_sentinel(self):
        self.assertEqual((kits.ac(kits.SENTINEL, True), kits.ac(kits.SENTINEL, False)), (-2, 0))
        self.assertEqual((kits.melee_damage(kits.SENTINEL), kits.move(kits.SENTINEL)), (0, 0))

    def test_none(self):
        self.assertEqual((kits.melee_damage(0), kits.ac(0, True), kits.move(0), kits.name(0)), (0, 0, 0, ""))


if __name__ == "__main__":
    unittest.main()
