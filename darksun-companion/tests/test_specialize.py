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


def sheet(chosen=(), classes=(9, 0, 0), levels=(4, 0, 0)):
    s = bytearray(game.SHEET_SIZE)
    for i, k in enumerate(chosen):
        s[game.SPEC_SLOTS + i] = k + 1
    s[game.SHEET_CLASSES:game.SHEET_CLASSES + 3] = bytes(classes)
    s[game.SHEET_LEVELS:game.SHEET_LEVELS + 3] = bytes(levels)
    return bytes(s)


class SkillTests(unittest.TestCase):
    """specialize.skill: as DSCLOG's SPEC_OF (tests/test_dsclog.py SpecializeTests)."""
    LONG_SWORD, AXE = 45, 22

    def test_levels(self):
        S = specialize
        self.assertEqual(S.skill(sheet(), self.AXE), S.NONE)
        self.assertEqual(S.skill(sheet((0,)), self.AXE), S.PLAIN)
        self.assertEqual(S.skill(sheet((0,)), self.LONG_SWORD), S.SPECIAL)
        self.assertEqual(S.skill(sheet((0,), levels=(5, 0, 0)), self.LONG_SWORD), S.MASTER)
        self.assertEqual(S.skill(sheet((0,), levels=(9, 0, 0)), self.LONG_SWORD), S.GRAND)
        self.assertEqual(S.skill(sheet((0, 5), classes=(10, 0, 0), levels=(9, 0, 0)), self.AXE), S.SPECIAL)
        self.assertEqual(S.skill(sheet((0,), classes=(13, 0, 0)), self.LONG_SWORD), S.EXPERT)
        self.assertEqual(S.skill(sheet((0,), classes=(11, 17, 9), levels=(5, 5, 5)), self.LONG_SWORD), S.MASTER)

    def test_bonuses(self):
        S = specialize
        self.assertEqual([(S.to_hit(l), S.damage(l)) for l in range(6)],
                         [(0, 0), (0, 0), (0, 0), (1, 2), (3, 3), (3, 3)])



class PageLabelTests(unittest.TestCase):
    def test_short_forms(self):
        from dscompanion import weaponpages
        labels = [weaponpages.page_text(k) for k in range(16)]
        self.assertEqual(labels[:4], ["LNG SWORD", "CLUB", "DAGGER", "SHRT SWORD"])
        self.assertEqual(labels[8], "QTR STAFF")
        self.assertEqual(labels[15], "STF SLING")
        self.assertTrue(all(len(t) <= 10 for t in labels))


if __name__ == "__main__":
    unittest.main()
