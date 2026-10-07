"""New weapons and bracers in the world: merchants' stock and people's packs.

- The Ledger's plain weapons (weaponchoice.py): the bone and obsidian short swords and axes, the
  obsidian mace and a plain metal short sword. The game has no other short sword than Kurzak's,
  no axe but a metal one, and no obsidian mace but Blackmace. The two merchants who sell plain
  weapons stock them, and a few kinds of people carry one, as their loot.
- Metal versions of the plain weapons the game has in no metal (a dagger but Dag's Dagger +3, a
  mace, a great axe, a pick, a polearm): one each, on people who fight with the like.
- Magic weapons of the kinds the game has none of (a club, a pick, a staff sling; a short sword
  but Shadowseeker): one each, priced as the game's magic weapons of the like.
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


class Gift(NamedTuple):
    region: Optional[int]  # None: wherever they are (the game's people of its RGNFF)
    name: str
    items: Tuple[bytes, ...]
    every: bool = False  # each of that name, not only the first met
    slot: Optional[int] = None  # worn there if it's free (else in the backpack)
    carrying: Optional[int] = None  # only one carrying an item of this name entry


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


def place(gd: GameData, given: Set[str], gifts: Tuple[Gift, ...] = GIFTS) -> List[str]:
    """Each of GIFTS in the area gets its items not yet given this game (GIVEN: a key for each,
    updated)."""
    region = gd.region()
    here = [g for g in gifts if g.region in (None, region)]
    if not here:
        return []
    leader = gd.creature_name(0)
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

