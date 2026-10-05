"""The arena's gythka and Kurzak's short sword made magic: Kreenfang and Shadowseeker (arms.py)."""

import os
import struct
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dscompanion import arms, game, names, npcitems, ring
from test_dicelog import CREATURES, DS, ITEMS
import test_npcitems
from test_npcitems import KURZAK, PEHTUCL

GYTHKA, PARTY_THING = 90, 410


def record(m, item):
    rec = bytes(m[ITEMS + item * game.ITEM_SIZE:ITEMS + (item + 1) * game.ITEM_SIZE])
    shown, = struct.unpack_from("<H", rec, arms.ITEM_SPELL_SHOWN)
    assert shown == rec[arms.ITEM_SPELL], (shown, rec[arms.ITEM_SPELL])  # (its box's icon: the same spell)
    return (rec[game.ITEM_PLUS], struct.unpack_from("<H", rec, game.ITEM_NAME)[0],
            struct.unpack_from("<H", rec, arms.ITEM_VALUE)[0], rec[arms.ITEM_SPELL])


class ArmsTests(unittest.TestCase):
    setUp = test_npcitems.NpcItemTests.setUp

    def sword(self):
        """Kurzak's short sword, once given: its item number."""
        npcitems.place(self.gd, set())
        thing, = struct.unpack_from("<h", self.gd.creature(KURZAK), 8 + 4)
        return next(i for i, rec in ring.Items(self.gd).chain(thing)
                    if struct.unpack_from("<H", rec, game.ITEM_TYPE)[0] == game.SHORT_SWORD_TYPE)

    def give_party_gythka(self, plus=0, name=0x3A, value=6):
        """A plain gythka (the kreen's) in Dag's (creature 0's) first list."""
        rec = bytearray(game.ITEM_SIZE)
        struct.pack_into("<h", rec, game.ITEM_NEXT, game.NO_ITEM)
        struct.pack_into("<H", rec, game.ITEM_TYPE, game.GYTHKA_TYPE)
        struct.pack_into("<H", rec, game.ITEM_NAME, name)
        struct.pack_into("<H", rec, arms.ITEM_VALUE, value)
        rec[game.ITEM_PLUS], rec[game.ITEM_SLOT] = plus, 3
        self.m[ITEMS + GYTHKA * game.ITEM_SIZE:ITEMS + (GYTHKA + 1) * game.ITEM_SIZE] = rec
        struct.pack_into("<Bh", self.m, ring.Items(self.gd).things + PARTY_THING * 3, game.THING_ITEM, GYTHKA)
        struct.pack_into("<h", self.m, CREATURES + 8, PARTY_THING)

    def in_arena(self):
        struct.pack_into("<H", self.m, DS * 16 + ring.REGION, ring.ARENA)

    def test_names_in_dsclog(self):
        """The names are the ones DSCLOG copies into the game's table, after the others'."""
        self.assertEqual(names.NAMES[arms.SWORD_NAME], b"Shadowseeker")
        self.assertEqual(names.NAMES[arms.GYTHKA_NAME], b"Kreenfang")
        self.assertEqual(sorted(names.NAMES), list(range(names.OWN, names.OWN + len(names.NAMES))))

    def test_sword(self):
        """Shadowseeker: +1, its name, priced near the Bloodwrath, Detect Invisibility (one past
        its number) for whoever readies it; once."""
        sword = self.sword()
        given = set()
        lines = arms.upgrade(self.gd, given)
        self.assertEqual(lines, ["Kurzak's Short Sword is Shadowseeker, a short sword +1: its wielder sees the invisible."])
        self.assertEqual(record(self.m, sword), (1, arms.SWORD_NAME, arms.SWORD_VALUE, game.DETECT_INVISIBILITY + 1))
        self.assertEqual(arms.upgrade(self.gd, given), [])

    def test_sword_from_an_earlier_version(self):
        """A sword made +1 before it had a name, a spell and this price: given them."""
        sword = self.sword()
        at = ITEMS + sword * game.ITEM_SIZE
        self.m[at + game.ITEM_PLUS] = 1
        struct.pack_into("<H", self.m, at + arms.ITEM_VALUE, 2500)
        lines = arms.upgrade(self.gd, set())
        self.assertEqual(lines, ["Kurzak's Short Sword +1 is named Shadowseeker.",
                                 "Shadowseeker lets its wielder see the invisible (from the next time it's readied)."])
        self.assertEqual(record(self.m, sword), (1, arms.SWORD_NAME, arms.SWORD_VALUE, game.DETECT_INVISIBILITY + 1))
        self.assertEqual(arms.upgrade(self.gd, set()), [])

    def test_gythka_only_in_the_arena(self):
        """A gythka out of the arena (here the party's, in the pens) stays plain; in the arena, off
        any living monster, it becomes Kreenfang, once a game."""
        self.give_party_gythka()
        given = set()
        self.assertEqual(arms.upgrade(self.gd, given), [line for line in arms.upgrade(self.gd, set())
                                                         if "Gythka" not in line])
        self.assertEqual(record(self.m, GYTHKA)[0], 0)
        self.in_arena()
        lines = arms.upgrade(self.gd, given)
        self.assertIn("The arena's 2 handed Bone Gythka (the Tohr-kreen's) is Kreenfang, a gythka +1.", lines)
        self.assertEqual(record(self.m, GYTHKA), (1, arms.GYTHKA_NAME, arms.GYTHKA_VALUE, 0))
        self.assertIn(arms.key(self.gd), given)

    def test_gythka_a_living_monster_holds(self):
        """The Tohr-kreen's while it lives (here Pehtucl's list stands for its): left plain."""
        self.give_party_gythka()
        struct.pack_into("<h", self.m, CREATURES + 8, game.NO_ITEM)  # (not the party's)
        struct.pack_into("<h", self.m, CREATURES + PEHTUCL * game.CREATURE_SIZE + 8, PARTY_THING)
        self.in_arena()
        arms.upgrade(self.gd, set())
        self.assertEqual(record(self.m, GYTHKA)[0], 0)

    def test_gythka_once_a_game(self):
        self.give_party_gythka()
        self.in_arena()
        arms.upgrade(self.gd, {arms.key(self.gd)})
        self.assertEqual(record(self.m, GYTHKA)[0], 0)

    def test_gythka_from_an_earlier_version(self):
        self.give_party_gythka(plus=1, value=2000)
        self.assertIn("The arena's Gythka +1 is named Kreenfang.", arms.upgrade(self.gd, set()))
        self.assertEqual(record(self.m, GYTHKA), (1, arms.GYTHKA_NAME, arms.GYTHKA_VALUE, 0))

    def test_icon_keeps_the_spell(self):
        """Its own icon given, the picture cache (a word) cleared: the spell after it kept."""
        from dscompanion import icons
        sword = self.sword()
        arms.upgrade(self.gd, set())
        at = ITEMS + sword * game.ITEM_SIZE
        struct.pack_into("<H", self.m, at + icons.PICTURE_CACHE, 0x0991)
        self.assertGreater(icons.repaint(self.gd, True), 0)  # (the others given too)
        rec = bytes(self.m[at:at + game.ITEM_SIZE])
        self.assertEqual(struct.unpack_from("<H", rec, 0)[0], icons.PICTURES["Shadowseeker"])
        self.assertEqual(struct.unpack_from("<H", rec, icons.PICTURE_CACHE)[0], 0)
        self.assertEqual(rec[arms.ITEM_SPELL], game.DETECT_INVISIBILITY + 1)

    def test_icon_byte_from_the_last_version(self):
        """Its spell given before its box's icon byte was: the byte set, quietly."""
        sword = self.sword()
        arms.upgrade(self.gd, set())
        at = ITEMS + sword * game.ITEM_SIZE
        struct.pack_into("<H", self.m, at + arms.ITEM_SPELL_SHOWN, 0)
        self.assertEqual(arms.upgrade(self.gd, set()), [])
        self.assertEqual(struct.unpack_from("<H", self.m, at + arms.ITEM_SPELL_SHOWN)[0], arms.SWORD_SPELL)

    def test_given_sword_seen_by_type(self):
        """Renamed and +1, Kurzak's sword still counts as given (not a second one)."""
        sword = self.sword()
        arms.upgrade(self.gd, set())
        it = ring.Items(self.gd)
        self.assertTrue(npcitems.already_there(self.gd, it, KURZAK, npcitems.SWORD))
        self.assertEqual(record(self.m, sword)[1], arms.SWORD_NAME)


if __name__ == "__main__":
    unittest.main()
