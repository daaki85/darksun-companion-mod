"""The rest of the bone scale armour, put with its chest piece."""

import os
import shutil
import struct
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dscompanion import bonescale, game, icons, ring
from test_dicelog import CREATURES, DS, ITEMS
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

    def sell(self, piece):
        """PIECE taken out of its list and its record given back to the free list, as the game
        does with an item sold."""
        it = ring.Items(self.gd)
        index = next(i for i, rec in it.chain(PILE) if bonescale.which_piece(rec) is piece)
        self.drop(piece)
        struct.pack_into("<H", self.m, ITEMS + index * game.ITEM_SIZE + game.ITEM_NEXT, it.word(ring.FREE_ITEMS))
        struct.pack_into("<H", self.m, DS * 16 + ring.FREE_ITEMS, index)
        return index

    def test_never_again(self):
        """A piece gone (sold, say): never given again."""
        self.put_chest()
        given = set()
        bonescale.place(self.gd, given)
        self.sell(bonescale.HELM)
        self.assertEqual(bonescale.place(self.gd, given), [])
        self.assertNotIn(game.BONE_HELM_TYPE, [t for _, t, _ in chain(self.gd, PILE)])

    def test_the_key_of_before(self):
        """Settings with the key of before (not yet the game's own): with a piece in the region it
        is this game's set, so nothing is added; with none, a new game, the set is given."""
        self.put_chest()
        bonescale.place(self.gd, set())
        self.drop(bonescale.HELM)
        given = {bonescale.KEY}
        self.assertEqual(bonescale.place(self.gd, given), [])
        self.assertIn(bonescale.key(self.gd), given)
        self.assertEqual(len(chain(self.gd, PILE)), 3)

    def test_new_game_with_the_key_of_before(self):
        self.put_chest()
        given = {bonescale.KEY}
        bonescale.place(self.gd, given)
        self.assertEqual(len(chain(self.gd, PILE)), 4)

    def watched(self, carried=True):
        """The set given (carried by Dag, or on the ground), a Watch that has seen it, its folder."""
        if carried:
            self.put_chest(slot=0x0E)
            struct.pack_into("<hhh", self.m, CREATURES + 8, game.NO_ITEM, game.NO_ITEM, PILE)
        else:
            self.put_chest()
        given = set()
        bonescale.place(self.gd, given)
        folder = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, folder)
        watch = bonescale.Watch(folder)
        self.assertEqual(watch.check(self.gd, given, now=1000.0), [])
        return watch, given, folder

    def test_vanished_reported(self):
        """Gone on two looks in a row: one line for the log, and the report in a file of its own,
        as found on the first look; once."""
        watch, given, folder = self.watched()
        index = self.sell(bonescale.HELM)
        ring.TAKEN.clear()
        ring.took(61, "an item for creature 3")
        self.assertEqual(watch.check(self.gd, given, ["Dag hits a gith"], now=1003.0), [])  # (once: not yet)
        out = watch.check(self.gd, given, now=1006.0)
        self.assertEqual(len(out), 1)
        self.assertTrue(out[0].startswith("The Bone Helm is gone (last seen in Dag's backpack"), out[0])
        self.assertIn("the game took it back. If you sold it", out[0])
        files = os.listdir(folder)
        self.assertEqual(len(files), 1)
        self.assertTrue(files[0].startswith("vanished-"))
        with open(os.path.join(folder, files[0]), encoding="utf-8") as f:
            text = f.read()
        self.assertIn(f"Item {index} is in the game's free list", text)
        self.assertIn("Last seen 3 s before", text)
        self.assertIn("item 61, an item for creature 3", text)
        self.assertIn("  Dag hits a gith", text)
        self.assertEqual(watch.check(self.gd, given, now=1009.0), [])  # (once)

    def test_taken_twice(self):
        """Its record now another item's, in another list: said so in the report."""
        watch, given, folder = self.watched()
        index = next(i for i, rec in ring.Items(self.gd).chain(PILE) if bonescale.which_piece(rec) is bonescale.LEG)
        rec = bytearray(ring.Items(self.gd).item(index))
        struct.pack_into("<H", rec, 0, 0x1234)  # (another item's picture, the same list)
        self.m[ITEMS + index * game.ITEM_SIZE:ITEMS + (index + 1) * game.ITEM_SIZE] = rec
        watch.check(self.gd, given, now=1003.0)
        out = watch.check(self.gd, given, now=1006.0)
        self.assertEqual(len(out), 1)
        self.assertIn("The Bone Scale Leg Armor has vanished", out[0])
        with open(os.path.join(folder, os.listdir(folder)[0]), encoding="utf-8") as f:
            self.assertIn(f"Item {index} is in the list of object {PILE} (Dag's): the record was taken", f.read())

    def test_back_on_the_next_look(self):
        """Gone on one look only (memory being filled): nothing."""
        watch, given, folder = self.watched()
        it = ring.Items(self.gd)
        index = next(i for i, rec in it.chain(PILE) if bonescale.which_piece(rec) is bonescale.HELM)
        saved = it.item(index)
        self.m[ITEMS + index * game.ITEM_SIZE:ITEMS + (index + 1) * game.ITEM_SIZE] = bytes(game.ITEM_SIZE)
        self.assertEqual(watch.check(self.gd, given, now=1003.0), [])
        self.m[ITEMS + index * game.ITEM_SIZE:ITEMS + (index + 1) * game.ITEM_SIZE] = saved
        self.assertEqual(watch.check(self.gd, given, now=1006.0), [])
        self.assertEqual(watch.check(self.gd, given, now=1009.0), [])
        self.assertEqual(os.listdir(folder), [])

    def test_left_in_another_area(self):
        """On the ground of an area the party has left: not in memory, not gone."""
        watch, given, folder = self.watched(carried=False)
        struct.pack_into("<Bh", self.m, THINGS + PILE * 3, 0, game.NO_ITEM)  # (the area's things gone)
        struct.pack_into("<H", self.m, DS * 16 + ring.REGION, 0x2A)
        self.assertEqual(watch.check(self.gd, given, now=1003.0), [])
        self.assertEqual(watch.check(self.gd, given, now=1006.0), [])
        self.assertEqual(os.listdir(folder), [])

    def test_not_given_not_watched(self):
        self.assertEqual(bonescale.Watch(tempfile.mkdtemp()).check(self.gd, set()), [])

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
