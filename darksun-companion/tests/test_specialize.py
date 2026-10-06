"""Weapon specialization's kinds (specialize.py)."""

import os
import struct
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dscompanion import game, restrict, specialize

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

    def test_dual_class(self):
        """A human fighter turned preserver: no specialization until the new class's level passes
        the fighter's, then the fighter's again."""
        S = specialize
        s = bytearray(sheet((0,), classes=(11, 9, 0), levels=(3, 5, 0)))
        s[game.SHEET_RACE] = game.HUMAN
        self.assertEqual(S.skill(bytes(s), self.LONG_SWORD), S.PLAIN)
        s[game.SHEET_LEVELS] = 6
        self.assertEqual(S.skill(bytes(s), self.LONG_SWORD), S.MASTER)
        s[game.SHEET_RACE] = 2  # (an elf's are multiclass: all at once)
        s[game.SHEET_LEVELS] = 3
        self.assertEqual(S.skill(bytes(s), self.LONG_SWORD), S.MASTER)

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

    def test_ids_clear_of_the_game(self):
        """The game's own buttons and pictures run to 833h (the dialogue window's replies are
        81Ch-821h): the pages' come after."""
        from dscompanion import weaponpages
        ids = [weaponpages.ROW_FIRST + k for k in range(16)] + [weaponpages.MORE, weaponpages.BACK, weaponpages.VIEW]
        self.assertTrue(all(0x834 <= i < 0xBB8 for i in ids))

    def test_picker_clear_of_the_game(self):
        """The level-up window's rows come after the pages', and its id is none of the game's
        windows (3000-3013, 3020, 3024...) nor the panel's."""
        from dscompanion import weaponpages
        rows = [weaponpages.PICK_FIRST + k for k in range(16)]
        pages = [weaponpages.ROW_FIRST + k for k in range(16)] + [weaponpages.MORE, weaponpages.BACK, weaponpages.VIEW]
        self.assertTrue(all(0x834 <= i < 0xBB8 and i not in pages for i in rows))
        self.assertNotIn(weaponpages.PICKER, set(range(3000, 3014)) | {3020, 3024} | set(weaponpages.PAGES)
                         | {weaponpages.WARRIOR_DISCIPLINES, weaponpages.WARRIOR_SPHERES})
        # (two columns of eight, inside the psionicists' window, 159 wide, above its words at 73)
        xs = [weaponpages.PICK_X + weaponpages.PICK_GAP_X * (k // 8) for k in range(16)]
        ys = [weaponpages.PICK_Y + weaponpages.PICK_PITCH * (k % 8) for k in range(16)]
        self.assertLess(max(ys) + 7, 73)
        self.assertEqual(sorted(set(xs)), [6, 88])



class NewCharacterTests(unittest.TestCase):
    """weaponchoice: a new character's kinds made whole, and its starting weapon."""

    def kinds(self, chosen, classes):
        from dscompanion import weaponchoice
        return weaponchoice.kinds_for(sheet(chosen, classes=classes))

    def test_defaults(self):
        self.assertEqual(self.kinds((), (10, 0, 0)), [1, 2, 0, 0])  # a gladiator: long sword, club
        self.assertEqual(self.kinds((), (9, 0, 0)), [1, 0, 0, 0])
        self.assertEqual(self.kinds((), (15, 0, 0)), [1, 0, 0, 0])  # a ranger
        self.assertEqual(self.kinds((2,), (10, 0, 0)), [3, 2, 0, 0])  # (kinds + 1 in the sheet)
        self.assertEqual(self.kinds((1,), (10, 0, 0)), [2, 1, 0, 0])

    def test_allowed_kinds(self):
        """A fighter/psionicist's choice kept to what the psionicist may use: its long sword
        default becomes the club, the first allowed."""
        from dscompanion import weaponchoice
        psi_kinds = sorted(restrict.PSIONICIST_KINDS)
        s = sheet((0,), classes=(9, 12, 0))
        self.assertEqual(weaponchoice.kinds_for(s, psi_kinds), [2, 0, 0, 0])
        s = sheet((2,), classes=(9, 12, 0))  # (the dagger: allowed)
        self.assertEqual(weaponchoice.kinds_for(s, psi_kinds), [3, 0, 0, 0])

    def test_extra_kinds_cleared(self):
        self.assertEqual(self.kinds((2, 5), (9, 0, 0)), [3, 0, 0, 0])
        self.assertEqual(self.kinds((2,), (11, 0, 0)), [0, 0, 0, 0])

    def test_plain_weapon(self):
        from dscompanion import weaponchoice
        start = bytes.fromhex("0cfc00001f002d000f27510000000000040a1c0000")
        new, slot = weaponchoice.plain_weapon(start, specialize.KINDS.index("dagger"))
        self.assertEqual(new.hex(), "60fb00001f0002000f271100000000000403100000"[:6] + new.hex()[6:])
        self.assertEqual((struct.unpack_from("<H", new, 0x0A)[0], struct.unpack_from("<H", new, 0x12)[0], slot), (17, 0x10, None))
        self.assertEqual(struct.unpack_from("<H", new, 0x0C)[0], 0)
        _, slot = weaponchoice.plain_weapon(start, specialize.KINDS.index("bow"))
        self.assertEqual(slot, game.EQUIP_SLOTS.index("missile"))
        self.assertEqual(len(weaponchoice.PLAIN), len(specialize.KINDS))


if __name__ == "__main__":
    unittest.main()
