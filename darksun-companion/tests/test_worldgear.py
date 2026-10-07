import os
import struct
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

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
        self.assertEqual([gift(n).objects for n in ("Tari", "Renegade", "Wild Mul")], [(60, 243), (289,), (290,)])

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
        self.assertEqual(gift("Keldar").objects, (28,))

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
        where = {g.items[0]: (g.name, g.objects) for g in worldgear.MAGIC if set(g.items) & set(worldgear.WARDENS_PLATE)}
        self.assertEqual(where, {helm: ("Dagolar", (26,)), arms: ("Treasure chest", (1360,)),
                                 legs: ("Gemfields chest", (1065,)), chest: ("Balkazar", (14,))})

    def test_elvenkind(self):
        """The Cloak and Boots of Elvenkind: their own types (the Cloak's, the Boots'), names and
        icons, no plus; the cloak with the Elven Leader's Gythka +1, the boots in the caravan's
        buried chest."""
        for item, type_, slot, name in ((worldgear.ELVEN_CLOAK, game.ELVEN_CLOAK_TYPE, 8, "Cloak of Elvenkind"),
                                        (worldgear.ELVEN_BOOTS, game.ELVEN_BOOTS_TYPE, 4, "Boots of Elvenkind")):
            self.assertEqual(struct.unpack_from("<H", item, game.ITEM_TYPE)[0], type_)
            self.assertEqual((item[game.ITEM_PLUS], item[worldgear.ITEM_SPELL]), (0, 0))
            self.assertEqual(npcitems.TYPES[type_ - game.GAME_TYPES][9], slot)
            self.assertEqual(npcitems.TYPES[type_ - game.GAME_TYPES][0x10:0x12], b"\x00\x06")  # (thieves, rangers)
            self.assertEqual(icons.which(item), name)
        self.assertEqual(names.NAMES[worldgear.CLOAK_OF_ELVENKIND], b"Cloak/Elvenkind")
        self.assertEqual(gift("Buried chest").objects, (worldgear.CARAVAN_CHEST,))

    def test_flame_blade(self):
        """The Flame Blade: the obsidian long sword +1 (a fire cleric's to wield), Focus Heat on
        what it hits (one past the game's number, its icon shown too), on the Hot Springs'
        Templar with the Drake Shield."""
        item = worldgear.FLAME_BLADE
        self.assertEqual(struct.unpack_from("<H", item, game.ITEM_TYPE)[0], 45)
        self.assertEqual((item[game.ITEM_PLUS], item[worldgear.ITEM_SPELL]), (1, 117))
        self.assertEqual(struct.unpack_from("<H", item, worldgear.ITEM_SPELL_SHOWN)[0], 117)
        self.assertEqual(icons.which(item), "Flame Blade")
        self.assertEqual(names.NAMES[worldgear.FLAME_BLADE_NAME], b"Flame Blade")
        templar = next(g for g in worldgear.MAGIC if item in g.items)
        self.assertEqual((templar.region, templar.name, templar.objects), (0x23, "Templar", (34,)))

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



def rdff(head: bytes, items=()) -> bytes:
    """An object's record (as the game's): HEAD (a person, 58 bytes, naming itself object 55;
    or an item, a chest) and ITEMS, each with its type and name, then the end."""
    from dscompanion import dataitems as d
    recs = [d.Record(1, 0, 2 if len(head) != game.ITEM_SIZE else 1, 7, 71, head)]
    for i, item in enumerate(items):
        at = len(recs)
        recs.append(d.Record(2 if i == 0 else 4, 0 if i == 0 else at - 3, 1, 16 + i, 79 if i == 0 else 1, item))
        recs.append(d.Record(3, at, 5, struct.unpack_from("<H", item, 0x0A)[0], 4, b""))
        recs.append(d.Record(3, at, 3, struct.unpack_from("<H", item, 0x12)[0], 2, b""))
    return d.chunk(recs, b"\xff" + bytes(9))


GUARD = bytes(6) + struct.pack("<h", -55) + bytes(50)
ITEM = bytes.fromhex("0cfc000000002d000000510000000000" "04ff1c0000")  # (the bone long sword)


class DataTests(unittest.TestCase):
    """The items written into the objects' data (dataitems.py) and the clones' entities."""

    def setUp(self):
        self.chunks = {("RDFF", 55): rdff(GUARD, [ITEM]), ("OJFF", 55): b"guard's look",
                       ("RDFF", 1065): rdff(ITEM, [ITEM]), ("RDFF", 26): rdff(GUARD),
                       ("RDFF", 1564): rdff(ITEM, [ITEM, ITEM])}

    def test_read_and_written_back(self):
        from dscompanion import dataitems as d
        for data in self.chunks.values():
            if data[:1] == b"\x01":
                self.assertEqual(d.chunk(*d.records(data)), data)

    def test_after_their_own(self):
        """Into a chest with an item of its own, and to a person with none: after theirs, each
        with its type and name, in no slot and no list."""
        from dscompanion import dataitems as d
        gifts = [worldgear.Gift("Gemfields chest", (worldgear.WARDENS_PLATE[2],), (1065,)),
                 worldgear.Gift("Dagolar", (worldgear.bracers(2), worldgear.WARDENS_PLATE[3]), (26,))]
        out = worldgear.object_chunks(self.chunks, gifts)
        chest = d.items_of(out[("RDFF", 1065)])
        self.assertEqual(len(chest), 2)
        self.assertEqual(icons.which(chest[1]), "Warden's Legs")
        self.assertEqual([icons.which(r) for r in d.items_of(out[("RDFF", 26)])], ["Bracers of Defense", "Warden's Helm"])
        recs, _ = d.records(out[("RDFF", 26)])
        self.assertEqual([(r.level, r.of, r.kind) for r in recs[1:]],
                         [(2, 0, 1), (3, 1, 5), (3, 1, 3), (4, 1, 1), (3, 4, 5), (3, 4, 3)])
        self.assertEqual((recs[2].number, recs[3].number), (game.BRACERS_TYPE, worldgear.BRACERS_NAME))
        for rec in chest[1:]:
            self.assertEqual((rec[game.ITEM_SLOT], rec[4:6], rec[8:10]), (0xFF, b"\0\0", b"\0\0"))

    def test_one_of_a_kind(self):
        """One Castle Guard's polearm: a new object for him (the kind's look, his record naming
        itself), the kind's own unchanged; his region's entity pointed to it."""
        from dscompanion import dataitems as d
        guard = worldgear.Gift("Castle Guard", (worldgear.weapon(worldgear.METAL_POLEARM),), (55,), 0x1C, clone=(1, 2560))
        out = worldgear.object_chunks(self.chunks, [guard])
        self.assertNotIn(("RDFF", 55), out)
        self.assertEqual(out[("OJFF", 2560)], b"guard's look")
        self.assertEqual(struct.unpack_from("<h", out[("RDFF", 2560)], 10 + 6)[0], -2560)
        self.assertEqual([icons.which(r) for r in d.items_of(out[("RDFF", 2560)])], [None, "Metal Polearm"])
        entity = struct.Struct("<HHBBh")
        etab = entity.pack(1, 2, 0, 14, -9) + entity.pack(3, 4, 0, 14, -55) + entity.pack(5, 6, 0, 14, -55)
        new = worldgear.region_chunks(0x1C, {("ETAB", 0x1C): etab}, [guard])[("ETAB", 0x1C)]
        self.assertEqual([entity.unpack_from(new, i * 8)[4] for i in range(3)], [-9, -2560, -55])
        self.assertEqual(worldgear.region_chunks(0x1C, {("ETAB", 0x1C): new}, [guard]), {})  # (not twice)

    def test_switches(self):
        """The plain weapons, the magic ones (and the cloak's object), the bone scale set: each by
        its switch."""
        from dscompanion import bonescale, dataitems as d
        none = worldgear.data_chunks(self.chunks, {"world_gear": False, "world_magic": False, "pens_gear": False})
        self.assertEqual(none, {})
        pens = worldgear.data_chunks(self.chunks, {"world_gear": False, "world_magic": False})
        self.assertEqual(set(pens), {("RDFF", 1564)})
        self.assertEqual([icons.which(r) for r in d.items_of(pens[("RDFF", 1564)])[2:]], [None, None, "Bone Helm"])
        self.assertEqual([r[:2] for r in d.items_of(pens[("RDFF", 1564)])[2:4]], [bonescale.ARM[:2], bonescale.LEG[:2]])
        magic = worldgear.data_chunks(self.chunks, {"world_gear": False, "pens_gear": False})
        self.assertIn(("RDFF", worldgear.ELVEN_CLOAK_OBJECT), magic)
        self.assertEqual(d.items_of(magic[("RDFF", worldgear.ELVEN_CLOAK_OBJECT)]), [])
        recs, _ = d.records(magic[("RDFF", worldgear.ELVEN_CLOAK_OBJECT)])
        self.assertEqual(icons.which(recs[0].data), "Cloak of Elvenkind")

    def test_every_object_named(self):
        """Every gift names objects; the clones' new numbers are free (past the icons' 2419-2551)."""
        for g in worldgear.GIFTS + worldgear.MAGIC:
            self.assertTrue(g.objects, g.name)
            if g.clone:
                self.assertGreater(g.clone[1], 2551)
        self.assertEqual(worldgear.regions(worldgear.GIFTS + worldgear.MAGIC), [0x1C, 0x1E])


if __name__ == "__main__":
    unittest.main()
