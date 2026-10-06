"""Weapon specialization's kinds (specialize.py)."""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dscompanion import game, specialize

# The game's weapon types (DSUN's IT1R: a weapon's flags at +0, 1 melee, 2 missile, 10h thrown),
# and the ones that are no kind: spell-made weapons, gloves, the broken weapon
WEAPON_TYPES = (0, 1, 2, 3, 17, 18, 19, 20, 21, 22, 28, 29, 30, 31, 32, 33, 37, 41, 44, 45, 46, 47, 48, 50,
                63, 64, 69, 80, 81, 84, 85, 93, 94, 97, 98, 107, 111, 112, 113)
NO_KIND = (28, 29, 30, 31, 32, 37, 93, 107, 113)


class KindTests(unittest.TestCase):
    def test_sixteen_kinds_four_pages(self):
        self.assertEqual(len(specialize.KINDS), 16)
        self.assertEqual(specialize.KINDS[specialize.DEFAULT], "long sword")
        self.assertEqual([specialize.page_of(k) for k in range(16)], [0] * 4 + [1] * 4 + [2] * 4 + [3] * 4)

    def test_every_weapon_sorted(self):
        """Every weapon type is a kind, or one of the few that are none; every kind has a type."""
        for t in WEAPON_TYPES:
            self.assertEqual(specialize.kind_of(t) is None, t in NO_KIND, t)
        self.assertEqual(set(specialize.KIND_OF_TYPE.values()), set(range(16)))

    def test_some_kinds(self):
        name = lambda t: specialize.KINDS[specialize.kind_of(t)]
        self.assertEqual(name(98), "long sword")  # Bloodwrath
        self.assertEqual(name(game.GYTHKA_TYPE), "gythka")
        self.assertEqual(name(game.SHORT_SWORD_TYPE), "short sword")
        self.assertEqual(name(0), "staff sling")
        self.assertIsNone(specialize.kind_of(game.CLOAK_TYPE))


if __name__ == "__main__":
    unittest.main()
