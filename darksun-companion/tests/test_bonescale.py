"""The rest of the bone scale armour, put with its chest piece."""

import os
import struct
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dscompanion import bonescale, game, icons, ring
from test_dicelog import CREATURES, ITEMS
import test_npcitems
from test_ring import THINGS

CHEST = bytes.fromhex("f7fb00000000180000000f000000000005ff280100")  # the game's, in no list
PILE = 404  # an object: a pile on the ground


def chain(gd, thing):
    return [(struct.unpack_from("<H", rec, 0)[0], struct.unpack_from("<H", rec, game.ITEM_TYPE)[0], rec[game.ITEM_SLOT])
            for _, rec in ring.Items(gd).chain(thing)]


class BoneScaleTests(unittest.TestCase):
    setUp = test_npcitems.NpcItemTests.setUp

    def put_chest(self, slot=0xFF):
        rec = bytearray(CHEST)
        struct.pack_into("<h", rec, game.ITEM_NEXT, game.NO_ITEM)
        rec[game.ITEM_SLOT] = slot
        self.m[ITEMS + 83 * game.ITEM_SIZE:ITEMS + 84 * game.ITEM_SIZE] = rec
        struct.pack_into("<Bh", self.m, THINGS + PILE * 3, game.THING_ITEM, 83)

    def test_with_the_chest_on_the_ground(self):
        self.put_chest()
        given = set()
        self.assertEqual(bonescale.place(self.gd, given), [])  # (nothing for the log)
        self.assertEqual(chain(self.gd, PILE), [(0xFBF7, 15, 0xFF), (0xFBF6, 55, 0xFF), (0xFBF5, 56, 0xFF),
                                                (0xFC03, game.BONE_HELM_TYPE, 0xFF)])
        self.assertEqual(given, {bonescale.key(self.gd)})
        self.assertEqual(bonescale.place(self.gd, given), [])  # once a game
        self.assertEqual(len(chain(self.gd, PILE)), 4)

    def test_carried(self):
        """Already in a pack (Dag's): the rest goes in free cells of it."""
        self.put_chest(slot=0x0E)
        struct.pack_into("<hhh", self.m, CREATURES + 8, game.NO_ITEM, game.NO_ITEM, PILE)
        given = set()
        bonescale.place(self.gd, given)
        self.assertEqual(given, {bonescale.key(self.gd)})
        items = chain(self.gd, PILE)
        self.assertEqual(sorted(p for p, _, _ in items), sorted([0xFBF7, 0xFBF6, 0xFBF5, 0xFC03]))
        self.assertEqual(len({slot for _, _, slot in items}), 4)  # each in a cell of its own
        self.assertTrue(all(slot >= 0x0E for _, _, slot in items))

    def test_not_again_in_a_save_that_has_them(self):
        """A game saved after the set was added, loaded where the Ledger doesn't have the key (or
        has forgotten it): the pieces are there already, so nothing is added again."""
        self.put_chest()
        bonescale.place(self.gd, set())
        self.assertEqual(bonescale.place(self.gd, set()), [])
        self.assertEqual(len(chain(self.gd, PILE)), 4)

    def test_no_chest_nothing(self):
        given = set()
        self.assertEqual(bonescale.place(self.gd, given), [])
        self.assertEqual(given, set())

    def drop(self, piece):
        """PIECE taken out of the pile's list (its record left as the game would, reused)."""
        it = ring.Items(self.gd)
        first = it.thing(PILE)[1]
        before, index = None, first
        while 0 <= index < game.NO_ITEM:
            rec = it.item(index)
            after = struct.unpack_from("<h", rec, game.ITEM_NEXT)[0]
            if bonescale.which_piece(rec) is piece:
                if before is None:
                    struct.pack_into("<Bh", self.m, THINGS + PILE * 3, game.THING_ITEM, after)
                else:
                    struct.pack_into("<h", self.m, ITEMS + before * game.ITEM_SIZE + game.ITEM_NEXT, after)
                self.m[ITEMS + index * game.ITEM_SIZE:ITEMS + (index + 1) * game.ITEM_SIZE] = bytes(game.ITEM_SIZE)
                return
            before, index = index, after
        raise AssertionError("no such piece")

    def test_missing_piece_back(self):
        """The helm gone from the set: back with the chest piece, a line for the log, once a game;
        the arm or leg piece the same."""
        self.put_chest()
        given = set()
        bonescale.place(self.gd, given)
        self.drop(bonescale.HELM)
        out = bonescale.place(self.gd, given)
        self.assertEqual(out, ["The Bone Helm had gone missing from the bone scale set: it is back, with the "
                               "Bone Scale Chest Armor."])
        self.assertIn((0xFC03, game.BONE_HELM_TYPE, 0xFF), chain(self.gd, PILE))
        self.assertEqual(bonescale.place(self.gd, given), [])  # (there again: nothing)
        self.drop(bonescale.HELM)
        self.assertEqual(bonescale.place(self.gd, given), [])  # (once a game)
        self.drop(bonescale.LEG)
        self.assertEqual(len(bonescale.place(self.gd, given)), 1)
        self.assertIn((0xFBF5, 56, 0xFF), chain(self.gd, PILE))

    def test_missing_piece_back_in_the_carriers_pack(self):
        self.put_chest(slot=0x0E)
        struct.pack_into("<hhh", self.m, CREATURES + 8, game.NO_ITEM, game.NO_ITEM, PILE)
        given = set()
        bonescale.place(self.gd, given)
        self.drop(bonescale.HELM)
        out = bonescale.place(self.gd, given)
        self.assertEqual(len(out), 1)
        self.assertIn("in Dag's backpack", out[0])
        self.assertIn(game.BONE_HELM_TYPE, [t for _, t, _ in chain(self.gd, PILE)])

    def test_the_key_of_before(self):
        """Settings with the key of before (not yet the game's own): with a piece in the region it
        is this game's set, so a missing one comes back; with none, a new game, the set is given."""
        self.put_chest()
        bonescale.place(self.gd, set())
        self.drop(bonescale.HELM)
        given = {bonescale.KEY}
        self.assertEqual(len(bonescale.place(self.gd, given)), 1)
        self.assertIn(bonescale.key(self.gd), given)

    def test_new_game_with_the_key_of_before(self):
        self.put_chest()
        given = {bonescale.KEY}
        bonescale.place(self.gd, given)
        self.assertEqual(len(chain(self.gd, PILE)), 4)

    def test_no_room_for_all(self):
        """The carrier with room for fewer than the three: none yet."""
        self.put_chest(slot=0x0E)
        struct.pack_into("<hhh", self.m, CREATURES + 8, game.NO_ITEM, game.NO_ITEM, PILE)
        it = ring.Items(self.gd)
        free = [c for c in range(0x0F, 0x1A)]
        # fill all but two cells with copies of the chest record, in the same list
        prev = 83
        for n, cell in enumerate(free[:-2]):
            item = 120 + n
            rec = bytearray(CHEST)
            struct.pack_into("<h", rec, game.ITEM_NEXT, game.NO_ITEM)
            rec[game.ITEM_SLOT] = cell
            self.m[ITEMS + item * game.ITEM_SIZE:ITEMS + (item + 1) * game.ITEM_SIZE] = rec
            struct.pack_into("<h", self.m, ITEMS + prev * game.ITEM_SIZE + game.ITEM_NEXT, item)
            prev = item
        given = set()
        bonescale.place(self.gd, given)
        self.assertEqual(given, set())
        self.assertFalse(any(bonescale.which_piece(rec) for _, rec in ring.Items(self.gd).chain(PILE)))

    def test_helm_icon(self):
        self.assertEqual(icons.which(bonescale.HELM), "Bone Helm")
        self.assertEqual(icons.recolour([[129, 140, None, 208]], icons.BONE), [[207, 61, None, 208]])


if __name__ == "__main__":
    unittest.main()
