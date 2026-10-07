"""New weapons and bracers in the world: merchants' stock and people's packs.

- The Ledger's plain weapons (weaponchoice.py): the bone and obsidian short swords and axes, the
  obsidian mace and a plain metal short sword. The game has no other short sword than Kurzak's,
  no axe but a metal one, and no obsidian mace but Blackmace. The two merchants who sell plain
  weapons stock them, and a few kinds of people carry one, as their loot.
- Metal versions of the plain weapons the game has in no metal (a dagger but Dag's Dagger +3, a
  mace, a great axe, a pick, a polearm): one each, on people who fight with the like.
- Magic weapons of the kinds the game has none of (a club, a pick, a staff sling; a short sword
  but Shadowseeker): one each, priced as the game's magic weapons of the like.
- A circlet and a crown, worn on the head and not armour (no AC; bracers of defense and a
  preserver's spells go with them), each with a spell the game keeps on its wearer while it's
  worn, as it does its own magic items': Arrowbane, Protection from Normal Missiles, sold by
  Kel; the Sunking Crown, Protection from Evil 10' Radius (the party round its wearer warded),
  worn by Keldar, the templar of Dagolar's tunnels.
- The Warden's Plate, plate mail +1 (DSCLOG's plate types: AC 3 chest, 2 arms, 2 legs, as AD&D's
  piecemeal plate; the helm the game's metal one), its four pieces scattered: the helm on
  Dagolar's body; the arms in the Lower Castle's treasure chest with Dark Flame (behind the
  wall the Serpent Boots show, the vrock's cliff); the legs in the Gemfields' chest; the chest
  on Balkazar's body. The chest puts Resist Fire on its wearer while worn, the helm Cloak of
  Bravery; the arms and legs are plain.
- The Cloak and Boots of Elvenkind (DSCLOG's types, the game's Cloak's and Boots'; their stealth:
  stealth.py): the cloak comes with the Elven Leader's gift of his Gythka +1 (to whoever has it),
  the boots are in the buried chest of Kel's caravan, with the Cahulaks +1.
- Bracers of defense (DSCLOG's BRACERS type, worn on the arms: their plus counts for AC while neither
  armour nor a helm is worn), now that a preserver can't cast in armour: on four
  of the game's wizards, better the later they're met.

Each once a game (the key in the tools_given set, kept in settings), where its owner is, and never
where the owner has one like it already (a save made after it was given). Merchants and named
people get theirs once; people of a kind (EVERY), each of them.
"""

import struct
from typing import Callable, List, NamedTuple, Optional, Set, Tuple

from . import game, npcitems, ring, specialize, weaponchoice
from .game import GameData

# the bone long sword the game's merchants sell (SEGOBJEX's), which the weapons are made from
TEMPLATE = npcitems._item("0cfc000000002d000000510000000000" "04ff1c0000")
KIND = specialize.KINDS.index
BONE_SHORT_SWORD = weaponchoice.PLAIN[KIND("short sword")]
OBSIDIAN_SHORT_SWORD = weaponchoice.OTHERS[KIND("short sword")][0]
BONE_AXE = weaponchoice.PLAIN[KIND("axe")]
OBSIDIAN_AXE = weaponchoice.OTHERS[KIND("axe")][0]
OBSIDIAN_MACE = weaponchoice.OTHERS[KIND("mace")][0]
METAL_SHORT_SWORD = (game.METAL_SHORT_SWORD_TYPE, 0x144, 0x10000 - 2427, 300)  # (the metal long sword: 500)
METAL_DAGGER = (game.METAL_DAGGER_TYPE, 0x10, 0x10000 - 2504, 50)
METAL_MACE = (game.METAL_MACE_TYPE, 0x13, 0x10000 - 2506, 200)
METAL_GREAT_AXE = weaponchoice.OTHERS[KIND("great axe")][0]  # (300; an earth cleric's starting one)
METAL_PICK = (game.METAL_PICK_TYPE, 0xAD, 0x10000 - 2510, 150)
METAL_POLEARM = weaponchoice.OTHERS[KIND("polearm")][0]  # (250)
# (type, name entry, picture, price) and plus, priced as the game prices its own: a melee weapon as
# the Obsidian Bloodwrath +1 (20,800, as its Hornblade +1 and Gythka +1), 20,800 a plus; a missile
# weapon far less, as its Sling +1 (2,800; the Chatkcha +1 1,800, the Sling +2 3,500)
PLUS_VALUE, SLING_VALUE = 20800, 2800
# each with a name of its own (DSCLOG's names; Alagorn tells their stories, alagorn.py)
GUTTERKNOT, DEEPBITER, WINDLASH, GREENBRIGHT = 0x14A, 0x14B, 0x14C, 0x14D
NAMES = {GUTTERKNOT: b"Gutterknot", DEEPBITER: b"Deepbiter", WINDLASH: b"Windlash", GREENBRIGHT: b"Greenbright"}
CLUB_1 = ((18, GUTTERKNOT, 0x10000 - 2494, PLUS_VALUE), 1)  # a club +1
PICK_1 = ((112, DEEPBITER, 0x10000 - 2496, PLUS_VALUE), 1)  # a stone pick +1
STAFF_SLING_1 = ((0, WINDLASH, 0x10000 - 2498, SLING_VALUE), 1)  # a staff sling +1
SHORT_SWORD_2 = ((game.METAL_SHORT_SWORD_TYPE, GREENBRIGHT, 0x10000 - 2500, 2 * PLUS_VALUE), 2)  # a metal short sword +2

BRACERS_NAME = 0x149  # the name entry DSCLOG adds ("Bracers/Defense")
ARROWBANE, SUNKING_CROWN = 0x14E, 0x14F  # and the circlet's and crown's
NAMES[ARROWBANE], NAMES[SUNKING_CROWN] = b"Arrowbane", b"Sunking Crown"
ITEM_SPELL, ITEM_SPELL_SHOWN = 0x0F, 0x02  # a magic item's spell, one past its number (as arms.py's)
PROT_MISSILES, PROT_EVIL_10 = 36, 121  # the game's Prot'n from Normal Missiles, Prot'n from Evil 10' Rad.
HEAD = game.EQUIP_SLOTS.index("head")
BRACERS_PICTURE = 0x10000 - 2502
ARM = game.EQUIP_SLOTS.index("arm")


def weapon(spec: Tuple[int, int, int, int], plus: int = 0) -> bytes:
    """A weapon's item record, in no list and no slot."""
    rec = bytearray(weaponchoice.plain_weapon(TEMPLATE, 0, spec)[0])
    rec[game.ITEM_PLUS] = plus
    return bytes(rec)


def bracers(ac: int) -> bytes:
    """Bracers of defense of armour class AC (AD&D's 2-8): a plus of 10 - AC, priced 5,000 a
    point (AC 6 20,000, as the game's magic armour and shields: Shimmer Armor +3 24,000, the Drake
    Shield +1 25,400; AC 2 40,000, as its magic rings, 30,000-50,000)."""
    rec = bytearray(TEMPLATE)
    struct.pack_into("<H", rec, 0, BRACERS_PICTURE)
    struct.pack_into("<H", rec, weaponchoice.ITEM_VALUE, 5000 * (10 - ac))
    struct.pack_into("<H", rec, game.ITEM_TYPE, game.BRACERS_TYPE)
    struct.pack_into("<H", rec, game.ITEM_NAME, BRACERS_NAME)
    rec[game.ITEM_PLUS] = 10 - ac
    return bytes(rec)


def head_item(type_: int, name: int, picture: int, value: int, spell: int) -> bytes:
    """A circlet's or crown's item record: its spell put on its wearer while worn."""
    rec = bytearray(TEMPLATE)
    struct.pack_into("<H", rec, 0, picture)
    struct.pack_into("<H", rec, ITEM_SPELL_SHOWN, spell + 1)  # (as the game keeps it)
    struct.pack_into("<H", rec, weaponchoice.ITEM_VALUE, value)
    struct.pack_into("<H", rec, game.ITEM_TYPE, type_)
    struct.pack_into("<H", rec, game.ITEM_NAME, name)
    rec[ITEM_SPELL] = spell + 1
    return bytes(rec)


# priced as the game's magic helms: the Helm of Might 30,000, the Helm of Contemplation 35,000
ARROWBANE_ITEM = head_item(game.CIRCLET_TYPE, ARROWBANE, 0x10000 - 2514, 30000, PROT_MISSILES)
CROWN_ITEM = head_item(game.CROWN_TYPE, SUNKING_CROWN, 0x10000 - 2516, 40000, PROT_EVIL_10)


WARDENS_CHEST, WARDENS_ARMS, WARDENS_LEGS, WARDENS_HELM = 0x150, 0x151, 0x152, 0x153
NAMES.update({WARDENS_CHEST: b"Warden's Chest", WARDENS_ARMS: b"Warden's Arms", WARDENS_LEGS: b"Warden's Legs",
              WARDENS_HELM: b"Warden's Helm"})
RESIST_FIRE, CLOAK_OF_BRAVERY = 87, 109
METAL_HELM_TYPE = 89  # (the game's metal helm: the Helm of Contemplation's)


def armour(type_: int, name: int, picture: int, value: int, spell: Optional[int] = None, plus: int = 1) -> bytes:
    """A piece of magic armour's item record: SPELL, if any, put on its wearer while worn."""
    rec = bytearray(head_item(type_, name, picture, value, spell or 0))
    if spell is None:
        struct.pack_into("<H", rec, ITEM_SPELL_SHOWN, 0)
        rec[ITEM_SPELL] = 0
    rec[game.ITEM_PLUS] = plus
    return bytes(rec)


# priced as the game's own: the arms and legs (AC 3) as a piece of Grey's Scale (27,000, now AC 3
# too), the chest (AC 4, a spell) 36,000, the helm as the Helm of Might (30,000)
WARDENS_PLATE = (
    armour(game.PLATE_CHEST_TYPE, WARDENS_CHEST, 0x10000 - 2538, 36000, RESIST_FIRE),
    armour(game.PLATE_ARMS_TYPE, WARDENS_ARMS, 0x10000 - 2540, 27000),
    armour(game.PLATE_LEGS_TYPE, WARDENS_LEGS, 0x10000 - 2542, 27000),
    armour(METAL_HELM_TYPE, WARDENS_HELM, 0x10000 - 2544, 30000, CLOAK_OF_BRAVERY),
)


DARK_FLAME_CHEST, GEMFIELDS_CHEST = 1360, 1065  # (SEGOBJEX objects: their item records' picture, negated)
CARAVAN_CHEST = 2293  # the elven caravan's buried chest (with the Cahulaks +1)
CLOAK_OF_ELVENKIND, BOOTS_OF_ELVENKIND = 0x154, 0x155
NAMES.update({CLOAK_OF_ELVENKIND: b"Cloak/Elvenkind", BOOTS_OF_ELVENKIND: b"Boots/Elvenkind"})
# priced as the game's magic clothes: its Serpent Boots 20,000, Chameleon Gloves 30,000
ELVEN_CLOAK = armour(game.ELVEN_CLOAK_TYPE, CLOAK_OF_ELVENKIND, 0x10000 - 2546, 25000, plus=0)
ELVEN_BOOTS = armour(game.ELVEN_BOOTS_TYPE, BOOTS_OF_ELVENKIND, 0x10000 - 2548, 20000, plus=0)
GYTHKA_1 = (game.GYTHKA_TYPE, 1)  # the Elven Leader's gift (the game's own: its own name, not Kreenfang)


NAMES_OWN = 0x142  # the game's names: those before the Ledger's (DSCLOG's NAMES_OWN)


class Gift(NamedTuple):
    region: Optional[int]  # None: wherever they are (the game's people of its RGNFF)
    name: str
    items: Tuple[bytes, ...]
    every: bool = False  # each of that name, not only the first met
    slot: Optional[int] = None  # worn there if it's free (else in the backpack)
    carrying: Optional[int] = None  # only one carrying an item of this name entry
    container: Optional[int] = None  # not a person's: in the container of this object (SEGOBJEX's)
    beside: Optional[Tuple[int, int]] = None  # not a person's: to the party member with an item of
    #   this (type, plus) of a name of the game's own (a gift given by the game's script)


PLAIN = (BONE_SHORT_SWORD, OBSIDIAN_SHORT_SWORD, BONE_AXE, OBSIDIAN_AXE, OBSIDIAN_MACE)
GIFTS: Tuple[Gift, ...] = (
    Gift(0x0B, "Weapon Merchant", tuple(weapon(w) for w in PLAIN + (METAL_SHORT_SWORD,))),
    Gift(0x1A, "Jark", tuple(weapon(w) for w in (BONE_SHORT_SWORD, OBSIDIAN_SHORT_SWORD, BONE_AXE, OBSIDIAN_MACE))),
    Gift(0x29, "Merzol", (weapon(OBSIDIAN_AXE),)),  # the slave pens' gladiator
    Gift(0x1F, "Krikor", (weapon(BONE_AXE),)),
    Gift(0x1D, "Chaero", (weapon(OBSIDIAN_SHORT_SWORD),)),
    Gift(0x28, "Tari", (weapon(OBSIDIAN_MACE),), every=True),  # the warrens' Tari
    Gift(None, "Renegade", (weapon(BONE_SHORT_SWORD),), every=True),
    Gift(None, "Wild Mul", (weapon(BONE_AXE),), every=True),
    # the metal ones, on people who fight with the like
    Gift(0x1A, "Tobrian", (weapon(METAL_DAGGER),)),  # (a stone dagger)
    Gift(0x14, "Templar", (weapon(METAL_MACE),)),  # the slavers' camp's (a bone mace)
    Gift(0x1F, "Uskuye", (weapon(METAL_GREAT_AXE),)),  # (a metal long sword)
    Gift(0x0B, "Kwerin", (weapon(METAL_PICK),)),
    Gift(0x1C, "Castle Guard", (weapon(METAL_POLEARM),)),
)
MAGIC: Tuple[Gift, ...] = (
    Gift(0x0B, "Bowyer", (weapon(*STAFF_SLING_1),)),
    Gift(0x1E, "Undermt Folk", (weapon(*PICK_1),)),  # (the Undermountain's miners: the first met)
    Gift(0x28, "Churrr", (weapon(*CLUB_1),)),  # (the warrens' fighter, with his club)
    Gift(0x04, "Arant", (weapon(*SHORT_SWORD_2),)),  # (the gladiators' captor, Silt Sea Summoning)
    # bracers of defense on the wizards, worn where nothing else is (Mikquetzl's arm armour stays)
    Gift(0x28, "Mikquetzl", (bracers(6),), slot=ARM),
    Gift(0x03, "Wyrmias", (bracers(5),), slot=ARM),
    Gift(0x0D, "Balkazar", (bracers(4),), slot=ARM),
    Gift(None, "Dagolar", (bracers(2),), slot=ARM, carrying=0x75),  # (the one with Dag's Dagger)
    # the circlet sold by Kel (the game's magic items' merchant), the crown worn by Keldar
    Gift(0x1A, "Kel", (ARROWBANE_ITEM,)),
    Gift(0x27, "Keldar", (CROWN_ITEM,), slot=HEAD),
    # the Warden's Plate, scattered: the helm on Dagolar (a boss's body, early on), the arms in the
    # Lower Castle's treasure chest (object 1360, with Dark Flame: behind the barrier the Serpent
    # Boots show, the vrock near), the legs in the Gemfields' chest (object 1065), the chest on
    # Balkazar (the hardest kill, after his mirror)
    Gift(None, "Dagolar", (WARDENS_PLATE[3],), carrying=0x75),
    Gift(0x1D, "Treasure chest", (WARDENS_PLATE[1],), container=DARK_FLAME_CHEST),
    Gift(0x08, "Gemfields chest", (WARDENS_PLATE[2],), container=GEMFIELDS_CHEST),
    Gift(0x0D, "Balkazar", (WARDENS_PLATE[0],)),
    # the Cloak of Elvenkind with the Elven Leader's Gythka +1, the boots in the caravan's buried chest
    Gift(0x14, "Elven Leader's gift", (ELVEN_CLOAK,), beside=GYTHKA_1),
    Gift(0x1A, "Buried chest", (ELVEN_BOOTS,), container=CARAVAN_CHEST),
)
def _lists(gd: GameData, index: int) -> List[int]:
    return [struct.unpack_from("<h", gd.creature(index), o)[0] for o in game.CREATURE_ITEM_LISTS]


def _carries(gd: GameData, it: ring.Items, index: int, test: Callable[[bytes], bool]) -> bool:
    return any(test(data) for t in _lists(gd, index) for _, data in it.chain(t))


def _named(entry: int) -> Callable[[bytes], bool]:
    return lambda rec: len(rec) >= game.ITEM_SIZE and struct.unpack_from("<H", rec, game.ITEM_NAME)[0] == entry


def _same(item: bytes) -> Callable[[bytes], bool]:
    """Like ITEM: the same type, name and plus."""
    return lambda rec: npcitems._same(rec, item) and rec[game.ITEM_PLUS] == item[game.ITEM_PLUS]


def _in_region(it: ring.Items, test: Callable[[bytes], bool]) -> bool:
    return any(test(rec) for thing in range(ring.THING_COUNT) for _, rec in it.chain(thing))


def _container(it: ring.Items, obj: int) -> Optional[int]:
    """The item number of the container of SEGOBJEX object OBJ in the region, if there."""
    for thing in range(ring.THING_COUNT):
        for item, rec in it.chain(thing, inside=False):
            if struct.unpack_from("<H", rec, 0)[0] == 0x10000 - obj:
                return item
    return None


def _with_item(gd: GameData, it: ring.Items, kind: Tuple[int, int]) -> Optional[int]:
    """The party member carrying an item of KIND (type, plus) named by the game (not the Ledger)."""
    def test(rec: bytes) -> bool:
        return len(rec) >= game.ITEM_SIZE and struct.unpack_from("<H", rec, game.ITEM_TYPE)[0] == kind[0] \
            and rec[game.ITEM_PLUS] == kind[1] and struct.unpack_from("<H", rec, game.ITEM_NAME)[0] < NAMES_OWN
    return next((m for m in range(game.PARTY_SIZE) if _carries(gd, it, m, test)), None)


def add_inside(gd: GameData, obj: int, rec: bytes) -> bool:
    """An item from the game's free list, made REC, put first in the container of object OBJ (a
    new list of its contents, from the game's free objects, if it's empty)."""
    it = ring.Items(gd)
    box, item = _container(it, obj), it.word(ring.FREE_ITEMS)
    if box is None or item >= game.NO_ITEM:
        return False
    contents, = struct.unpack_from("<H", it.item(box), ring.ITEM_CONTENTS)
    ds = gd.ds * 16
    if contents >= ring.THING_COUNT:
        contents = it.word(ring.FREE_THINGS)
        if contents >= ring.THING_COUNT:
            return False
        gd.guest.write(ds + ring.FREE_THINGS, struct.pack("<H", it.thing(contents)[1] & 0xFFFF))
        gd.guest.write(ds + ring.THINGS_USED, struct.pack("<H", it.word(ring.THINGS_USED) + 1))
        gd.guest.write(it.things + contents * 3, struct.pack("<BH", game.THING_ITEM, game.NO_ITEM))
        gd.guest.write(it.items + box * game.ITEM_SIZE + ring.ITEM_CONTENTS, struct.pack("<H", contents))
        it = ring.Items(gd)
    kind, first = it.thing(contents)
    if kind != game.THING_ITEM:
        return False
    gd.guest.write(ds + ring.FREE_ITEMS, it.item(item)[game.ITEM_NEXT:game.ITEM_NEXT + 2])
    ring.took(item, f"an item (picture {struct.unpack_from('<H', rec, 0)[0]:04X}h) for object {obj}")
    rec = bytearray(rec)
    struct.pack_into("<h", rec, game.ITEM_NEXT, first)
    rec[game.ITEM_SLOT] = 0xFF
    gd.guest.write(it.items + item * game.ITEM_SIZE, bytes(rec))
    gd.guest.write(it.things + contents * 3, struct.pack("<Bh", game.THING_ITEM, item))
    return True


def place(gd: GameData, given: Set[str], gifts: Tuple[Gift, ...] = GIFTS) -> List[str]:
    """Each of GIFTS in the area gets its items not yet given this game (GIVEN: a key for each,
    updated)."""
    region = gd.region()
    here = [g for g in gifts if g.region in (None, region)]
    if not here:
        return []
    leader = gd.creature_name(0)
    it = ring.Items(gd)
    for gift in here:
        if gift.container is None and gift.beside is None:
            continue
        for item in gift.items:
            key = f"{leader}|world:{gift.name}:{struct.unpack_from('<H', item, game.ITEM_TYPE)[0]}:{item[game.ITEM_PLUS]}"
            if key in given:
                continue
            if _in_region(it, _same(item)):  # (a save from after it was put there)
                given.add(key)
            elif gift.container is not None:
                if add_inside(gd, gift.container, item):
                    given.add(key)
                    it = ring.Items(gd)
            else:
                member = _with_item(gd, it, gift.beside)
                if member is not None and npcitems.add_to(gd, member, item):
                    given.add(key)
                    it = ring.Items(gd)
    for index in sorted(set(gd.combatants().values())):
        if index < game.PARTY_SIZE:
            continue
        name = gd.creature_name(index)
        rec = gd.creature(index)
        if len(rec) < game.CREATURE_SIZE or struct.unpack_from("<h", rec, 0)[0] <= 0:
            continue
        for gift in here:
            if gift.name != name:
                continue
            if gift.carrying is not None and not _carries(gd, it, index, _named(gift.carrying)):
                continue
            who = f"{name}#{region:02X}:{index}" if gift.every else name
            for item in gift.items:
                key = f"{leader}|world:{who}:{struct.unpack_from('<H', item, game.ITEM_TYPE)[0]}:{item[game.ITEM_PLUS]}"
                if key in given:
                    continue
                if _carries(gd, it, index, _same(item)):  # (a save from after it was given)
                    given.add(key)
                    continue
                if npcitems.add_to(gd, index, item, gift.slot):
                    given.add(key)
                    it = ring.Items(gd)
    return []  # (nothing in the log: they're there to be found)

