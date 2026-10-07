import os
import struct
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dscompanion import game, icons, worldgear  # noqa: E402


class WorldGearTests(unittest.TestCase):
    def test_weapons(self):
        """Each weapon given is one of the Ledger's own, with its picture, in no list or slot."""
        for spec, name in ((worldgear.BONE_SHORT_SWORD, "Bone Short Sword"),
                           (worldgear.OBSIDIAN_SHORT_SWORD, "Obsidian Short Sword"),
                           (worldgear.BONE_AXE, "Bone Axe"), (worldgear.OBSIDIAN_AXE, "Obsidian Axe"),
                           (worldgear.OBSIDIAN_MACE, "Obsidian Mace")):
            rec = worldgear.weapon(spec)
            self.assertEqual(len(rec), game.ITEM_SIZE)
            self.assertEqual(icons.which(rec), name)
            self.assertEqual(struct.unpack_from("<H", rec, 0)[0], icons.PICTURES[name])
            self.assertEqual(struct.unpack_from("<H", rec, game.ITEM_NEXT)[0], game.NO_ITEM)
            self.assertEqual(rec[game.ITEM_SLOT], 0xFF)
            self.assertEqual(rec[game.ITEM_PLUS], 0)

    def test_merchants(self):
        """Both merchants stock every one of the new weapons but Jark's obsidian axe."""
        self.assertEqual(len(worldgear.WHO[(0x0B, "Weapon Merchant")]), 5)
        self.assertIn(worldgear.OBSIDIAN_MACE, worldgear.WHO[(0x1A, "Jark")])


if __name__ == "__main__":
    unittest.main()
