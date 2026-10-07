"""New weapons and bracers in the world: merchants' stock, people's packs, a reward.

- The Ledger's plain weapons (weaponchoice.py): the bone and obsidian short swords and axes, the
  obsidian mace and a plain metal short sword. The game has no other short sword than Kurzak's,
  no axe but a metal one, and no obsidian mace but Blackmace. The two merchants who sell plain
  weapons stock them, and a few kinds of people carry one, as their loot.
- Magic weapons of the kinds the game has none of (a club, a pick, a staff sling; a short sword
  but Shadowseeker): one each.
- Bracers of defense (DSCLOG's BRACERS type, worn on the arms: their plus counts for AC while no
  armour is worn on the arms, legs or chest), now that a preserver can't cast in armour: on four
  of the game's wizards, better the later they're met.

Each once a game (the key in the tools_given set, kept in settings), where its owner is, and never
where the owner has one like it already (a save made after it was given). Merchants and named
people get theirs once; people of a kind (EVERY), each of them. The Warren Chief's Club +1 comes
with his reward: whoever of the party first carries his Helm of Contemplation gets the club too.
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
# (type, name entry, picture, price) and plus: priced as the game's magic weapons of the like
CLUB_1 = ((18, 0x11, 0x10000 - 2494, 2000), 1)
PICK_1 = ((112, 0xAD, 0x10000 - 2496, 3000), 1)
STAFF_SLING_1 = ((0, 0x01, 0x10000 - 2498, 3000), 1)
SHORT_SWORD_2 = ((game.METAL_SHORT_SWORD_TYPE, 0x144, 0x10000 - 2500, 25000), 2)

BRACERS_NAME = 0x149  # the name entry DSCLOG adds ("Bracers/Defense")
BRACERS_PICTURE = 0x10000 - 2502
ARM = game.EQUIP_SLOTS.index("arm")


def weapon(spec: Tuple[int, int, int, int], plus: int = 0) -> bytes:
    """A weapon's item record, in no list and no slot."""
    rec = bytearray(weaponchoice.plain_weapon(TEMPLATE, 0, spec)[0])
    rec[game.ITEM_PLUS] = plus
    return bytes(rec)


def bracers(ac: int) -> bytes:
    """Bracers of defense of armour class AC (AD&D's 2-8): a plus of 10 - AC, priced 3,000 a
    point (AD&D's 6,000 for AC 8 to 24,000 for AC 2)."""
    rec = bytearray(TEMPLATE)
    struct.pack_into("<H", rec, 0, BRACERS_PICTURE)
    struct.pack_into("<H", rec, weaponchoice.ITEM_VALUE, 3000 * (10 - ac))
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
)
MAGIC: Tuple[Gift, ...] = (
    Gift(0x0B, "Bowyer", (weapon(*STAFF_SLING_1),)),
    Gift(0x03, "Melkor", (weapon(*PICK_1),)),
    Gift(None, "Elite Guard", (weapon(*SHORT_SWORD_2),)),
    # bracers of defense on the wizards, worn where nothing else is (Mikquetzl's arm armour stays)
    Gift(0x28, "Mikquetzl", (bracers(6),), slot=ARM),
    Gift(0x03, "Wyrmias", (bracers(5),), slot=ARM),
    Gift(0x0D, "Balkazar", (bracers(4),), slot=ARM),
    Gift(None, "Dagolar", (bracers(2),), slot=ARM, carrying=0x75),  # (the one with Dag's Dagger)
)
HELM_OF_CONTEMPLATION = 0x6B  # the Warren Chief's reward (its name entry)
CLUB_KEY = "Warren Chief's Club +1"


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


def reward(gd: GameData, given: Set[str]) -> List[str]:
    """The Warren Chief's Club +1, with his Helm of Contemplation: to the first of the party
    seen carrying the helm, once a game."""
    key = f"{gd.creature_name(0)}|world:{CLUB_KEY}"
    if key in given:
        return []
    it = ring.Items(gd)
    for member in range(game.PARTY_SIZE):
        rec = gd.creature(member)
        if len(rec) < game.CREATURE_SIZE or not rec[game.CREATURE_NAME]:
            continue
        if _carries(gd, it, member, _named(HELM_OF_CONTEMPLATION)):
            if npcitems.add_to(gd, member, weapon(*CLUB_1)):
                given.add(key)
                return [f"{gd.creature_name(member)} is given a Club +1 with the Helm of Contemplation."]
            return []
    return []
