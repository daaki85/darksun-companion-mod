import os
import struct
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dscompanion import game, icons, names, npcitems, restrict, ring, worldgear  # noqa: E402


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
                                 worldgear.CLUB_1 + ("Gutterknot",), worldgear.PICK_1 + ("Deepbiter",),
                                 worldgear.STAFF_SLING_1 + ("Windlash",),
                                 worldgear.SHORT_SWORD_2 + ("Greenbright",),
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
        self.assertEqual(icons.which(gift("Churrr").items[0]), "Gutterknot")

    def test_priced_as_the_game(self):
        """Melee weapons 20,800 a plus, as the game's Obsidian Bloodwrath +1; the staff sling as
        its Sling +1."""
        for spec, plus in (worldgear.CLUB_1, worldgear.PICK_1, worldgear.SHORT_SWORD_2):
            self.assertEqual(spec[3], 20800 * plus)
        self.assertEqual(worldgear.STAFF_SLING_1[0][3], 2800)

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

    def test_head_items(self):
        """Arrowbane and the Sunking Crown: worn on the head, not armour, each with its spell (one
        past the game's number, its icon shown too), Kel's and Keldar's (worn)."""
        for item, type_, spell, name in ((worldgear.ARROWBANE_ITEM, game.CIRCLET_TYPE, 36, "Arrowbane"),
                                         (worldgear.CROWN_ITEM, game.CROWN_TYPE, 121, "Sunking Crown")):
            self.assertEqual(struct.unpack_from("<H", item, game.ITEM_TYPE)[0], type_)
            self.assertEqual(item[worldgear.ITEM_SPELL], spell + 1)
            self.assertEqual(struct.unpack_from("<H", item, worldgear.ITEM_SPELL_SHOWN)[0], spell + 1)
            self.assertEqual(icons.which(item), name)
            typ = npcitems.TYPES[type_ - game.GAME_TYPES]
            self.assertEqual(typ[9], 6)  # (the head)
            self.assertFalse(restrict.is_armour(typ))
            self.assertEqual(names.NAMES[struct.unpack_from("<H", item, game.ITEM_NAME)[0]], name.encode())
        self.assertEqual(gift("Kel").items, (worldgear.ARROWBANE_ITEM,))
        self.assertEqual(gift("Keldar").slot, game.EQUIP_SLOTS.index("head"))

    def test_wardens_plate(self):
        """The Warden's Plate: plate +1 of AC 3, 2, 2 (metal armour to the class rules) and the
        game's metal helm +1; the chest Resist Fire, the helm Cloak of Bravery, the arms and legs
        none; the helm on Dagolar, the arms in the Lower Castle's chest with Dark Flame, the legs
        in the Gemfields' chest, the chest on Balkazar."""
        chest, arms, legs, helm = worldgear.WARDENS_PLATE
        for item, type_, slot, ac, spell, name in (
                (chest, game.PLATE_CHEST_TYPE, 1, 3, 87, "Warden's Chest"),
                (arms, game.PLATE_ARMS_TYPE, 3, 2, 0, "Warden's Arms"),
                (legs, game.PLATE_LEGS_TYPE, 0x0A, 2, 0, "Warden's Legs"),
                (helm, 89, None, None, 109, "Warden's Helm")):
            self.assertEqual(struct.unpack_from("<H", item, game.ITEM_TYPE)[0], type_)
            self.assertEqual(item[game.ITEM_PLUS], 1)
            self.assertEqual(item[worldgear.ITEM_SPELL], spell + 1 if spell else 0)
            self.assertEqual(struct.unpack_from("<H", item, worldgear.ITEM_SPELL_SHOWN)[0], spell + 1 if spell else 0)
            self.assertEqual(icons.which(item), name)
            self.assertEqual(names.NAMES[struct.unpack_from("<H", item, game.ITEM_NAME)[0]], name.encode())
            if slot is not None:
                typ = npcitems.TYPES[type_ - game.GAME_TYPES]
                self.assertEqual((typ[9], typ[0x12], typ[8]), (slot, ac, 4))  # (metal)
                self.assertTrue(restrict.is_armour(typ))
        where = {g.items[0]: (g.region, g.name, g.container, g.carrying) for g in worldgear.MAGIC
                 if set(g.items) & set(worldgear.WARDENS_PLATE)}
        self.assertEqual(where, {helm: (None, "Dagolar", None, 0x75), arms: (0x1D, "Treasure chest", 1360, None),
                                 legs: (0x08, "Gemfields chest", 1065, None), chest: (0x0D, "Balkazar", None, None)})

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


class ContainerTests(unittest.TestCase):
    """A piece put in a chest of the region's (the Lower Castle's, with Dark Flame): first in its
    contents, once; an emptied chest given a new list of contents."""

    def setUp(self):
        from test_dicelog import DS, ITEMS
        from test_ring import THINGS, arena
        self.log = log = arena()
        self.gd, self.m, self.items, self.things = log.game, log.guest.mem, ITEMS, THINGS
        struct.pack_into("<H", self.m, DS * 16 + ring.REGION, 0x1D)
        for item in range(60, 70):
            struct.pack_into("<h", self.m, ITEMS + item * game.ITEM_SIZE + game.ITEM_NEXT, item + 1 if item < 69 else game.NO_ITEM)
        # the chest (item 90, on the map as object 300), its contents object 301: Dark Flame (item 91)
        self.put(90, 0x10000 - worldgear.DARK_FLAME_CHEST, contents=301)
        self.put(91, 0xFAB1)
        struct.pack_into("<Bh", self.m, THINGS + 300 * 3, game.THING_ITEM, 90)
        struct.pack_into("<Bh", self.m, THINGS + 301 * 3, game.THING_ITEM, 91)

    def put(self, item, picture, contents=game.NO_ITEM):
        rec = bytearray(game.ITEM_SIZE)
        struct.pack_into("<HhH", rec, 0, picture, 0, 0)
        struct.pack_into("<h", rec, game.ITEM_NEXT, game.NO_ITEM)
        struct.pack_into("<H", rec, ring.ITEM_CONTENTS, contents)
        self.m[self.items + item * game.ITEM_SIZE:self.items + (item + 1) * game.ITEM_SIZE] = rec

    def inside(self):
        it = ring.Items(self.gd)
        thing, = struct.unpack_from("<H", it.item(90), ring.ITEM_CONTENTS)
        return [(struct.unpack_from("<H", rec, game.ITEM_NAME)[0], rec[game.ITEM_SLOT]) for _, rec in it.chain(thing)]

    def test_in_the_chest_once(self):
        given = set()
        worldgear.place(self.gd, given, worldgear.MAGIC)
        self.assertEqual(self.inside(), [(worldgear.WARDENS_ARMS, 0xFF), (0, 0)])
        worldgear.place(self.gd, given, worldgear.MAGIC)
        worldgear.place(self.gd, set(), worldgear.MAGIC)  # (a save from after: found there)
        self.assertEqual(len(self.inside()), 2)

    def test_an_emptied_chest(self):
        struct.pack_into("<H", self.m, self.items + 90 * game.ITEM_SIZE + ring.ITEM_CONTENTS, game.NO_ITEM)
        struct.pack_into("<Bh", self.m, self.things + 301 * 3, 0, 0)
        worldgear.place(self.gd, set(), worldgear.MAGIC)
        self.assertEqual(self.inside(), [(worldgear.WARDENS_ARMS, 0xFF)])
        self.assertEqual(struct.unpack_from("<H", self.m, self.items + 90 * game.ITEM_SIZE + ring.ITEM_CONTENTS)[0], 505)
