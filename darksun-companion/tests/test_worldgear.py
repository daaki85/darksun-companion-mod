import os
import struct
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dscompanion import game, icons, names, npcitems, restrict, worldgear  # noqa: E402


def gift(name):
    return next(g for g in worldgear.GIFTS + worldgear.MAGIC if g.name == name)


class WorldGearTests(unittest.TestCase):
    def test_weapons(self):
        """Each weapon given is one of the Ledger's own, with its picture, in no list or slot."""
        for spec, plus, name in ((worldgear.BONE_SHORT_SWORD, 0, "Bone Short Sword"),
                                 (worldgear.OBSIDIAN_SHORT_SWORD, 0, "Obsidian Short Sword"),
                                 (worldgear.BONE_AXE, 0, "Bone Axe"), (worldgear.OBSIDIAN_AXE, 0, "Obsidian Axe"),
                                 (worldgear.OBSIDIAN_MACE, 0, "Obsidian Mace"),
                                 (worldgear.METAL_SHORT_SWORD, 0, "Short Sword"),
                                 worldgear.CLUB_1 + ("Club +1",), worldgear.PICK_1 + ("Pick +1",),
                                 worldgear.STAFF_SLING_1 + ("Staff Sling +1",),
                                 worldgear.SHORT_SWORD_2 + ("Short Sword +2",),
                                 (worldgear.METAL_DAGGER, 0, "Metal Dagger"), (worldgear.METAL_MACE, 0, "Metal Mace"),
                                 (worldgear.METAL_GREAT_AXE, 0, "Metal Great Axe"),
                                 (worldgear.METAL_PICK, 0, "Metal Pick"), (worldgear.METAL_POLEARM, 0, "Metal Polearm")):
            rec = worldgear.weapon(spec, plus)
            self.assertEqual(len(rec), game.ITEM_SIZE)
            self.assertEqual(icons.which(rec), name)
            self.assertEqual(struct.unpack_from("<H", rec, 0)[0], icons.PICTURES[name])
            self.assertEqual(struct.unpack_from("<H", rec, game.ITEM_NEXT)[0], game.NO_ITEM)
            self.assertEqual(rec[game.ITEM_SLOT], 0xFF)
            self.assertEqual(rec[game.ITEM_PLUS], plus)

    def test_merchants(self):
        """The Weapon Merchant stocks every new plain weapon, Jark all but the axes of obsidian and
        the metal short sword; the kinds of people carry theirs each."""
        self.assertEqual(len(gift("Weapon Merchant").items), 6)
        self.assertEqual(len(gift("Jark").items), 4)
        self.assertTrue(all(gift(n).every for n in ("Tari", "Renegade", "Wild Mul")))

    def test_metal_kinds(self):
        """Each metal weapon is of its kind and of metal (an earth cleric's, not a fire cleric's)."""
        from dscompanion import specialize
        for spec, kind in ((worldgear.METAL_DAGGER, "dagger"), (worldgear.METAL_MACE, "mace"),
                           (worldgear.METAL_GREAT_AXE, "great axe"), (worldgear.METAL_PICK, "pick"),
                           (worldgear.METAL_POLEARM, "polearm"), (worldgear.METAL_SHORT_SWORD, "short sword")):
            self.assertEqual(specialize.KINDS[specialize.KIND_OF_TYPE[spec[0]]], kind)
            self.assertEqual(npcitems.TYPES[spec[0] - game.GAME_TYPES][8], 4)

    def test_churrr(self):
        """The Club +1 is Churrr's own, as loot."""
        self.assertEqual(icons.which(gift("Churrr").items[0]), "Club +1")

    def test_priced_as_bloodwrath(self):
        """20,800 a plus, as the game's Obsidian Bloodwrath +1."""
        for spec, plus in (worldgear.CLUB_1, worldgear.PICK_1, worldgear.STAFF_SLING_1, worldgear.SHORT_SWORD_2):
            self.assertEqual(spec[3], 20800 * plus)

    def test_bracers(self):
        """AC 6, 5, 4 and 2, as a plus of 10 - AC, worn on the arms; the Ledger's icon and name."""
        acs = {}
        for name in ("Mikquetzl", "Wyrmias", "Balkazar", "Dagolar"):
            g = gift(name)
            rec, = g.items
            self.assertEqual(g.slot, game.EQUIP_SLOTS.index("arm"))
            self.assertEqual(icons.which(rec), "Bracers of Defense")
            self.assertEqual(struct.unpack_from("<H", rec, game.ITEM_TYPE)[0], game.BRACERS_TYPE)
            self.assertEqual(struct.unpack_from("<H", rec, game.ITEM_NAME)[0], worldgear.BRACERS_NAME)
            acs[name] = 10 - rec[game.ITEM_PLUS]
            self.assertEqual(struct.unpack_from("<H", rec, 6)[0], 5000 * rec[game.ITEM_PLUS])
        self.assertEqual(acs, {"Mikquetzl": 6, "Wyrmias": 5, "Balkazar": 4, "Dagolar": 2})
        self.assertEqual(names.NAMES[worldgear.BRACERS_NAME], b"Bracers/Defense")

    def test_bracers_not_armour(self):
        """The bracers' type (as DSCLOG has it) isn't armour to the class rules; arm armour is."""
        bracers = npcitems.TYPES[game.BRACERS_TYPE - game.GAME_TYPES]
        self.assertFalse(restrict.is_armour(bracers))
        self.assertTrue(restrict.is_bracers(bracers))
        arm = bytes.fromhex("000000002400fa00" "0503000000000080" "6f170100")  # the leather Arm Armor's (7)
        self.assertTrue(restrict.is_armour(arm))
        self.assertFalse(restrict.is_bracers(arm))


if __name__ == "__main__":
    unittest.main()
