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

    def test_scores(self):
        self.assertEqual(kits.scores_after(kits.BRUTE, [16, 17, 15, 10, 12, 9]), [16, 18, 16, 9, 11, 9])
        self.assertEqual(kits.scores_after(kits.WANDERER, [16, 17, 15, 10, 12, 9]), [15, 17, 16, 10, 13, 8])
        self.assertEqual(kits.scores_after(kits.ARCANIST, [16, 17, 4, 18, 12, 9]), [16, 17, 3, 18, 12, 9])
        self.assertEqual(kits.scores_after(kits.BRUTE, [25, 25, 25, 3, 3, 3]), [25, 25, 25, 3, 3, 3])
        self.assertEqual(kits.scores_after(kits.RAIDER, [1, 2, 3, 4, 5, 6]), [1, 2, 3, 4, 5, 6])


if __name__ == "__main__":
    unittest.main()
