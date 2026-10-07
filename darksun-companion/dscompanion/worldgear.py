"""The new plain weapons in the world: merchants' stock and a few people's packs.

The Ledger's bone and obsidian short swords and axes and its obsidian mace (weaponchoice.py)
were made for new warriors; the game has no other short sword than Kurzak's, no axe but a metal
one, and no obsidian mace but Blackmace. So the two merchants who sell plain weapons stock them,
and a few people carry one to be found (put in their backpack, as the slave pens' gear,
npcitems.py). Each once a game (the key in the tools_given set, kept in settings), where its
owner is, and never where the owner has one like it already (a save made after it was given).
"""

import struct
from typing import Dict, List, Set, Tuple

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

# (region, name): the weapons they're given. Region None: wherever they are (the game's people of
# its RGNFF, met in more than one place)
WHO: Dict[Tuple[object, str], Tuple[Tuple[int, int, int, int], ...]] = {
    (0x0B, "Weapon Merchant"): (BONE_SHORT_SWORD, OBSIDIAN_SHORT_SWORD, BONE_AXE, OBSIDIAN_AXE, OBSIDIAN_MACE),
    (0x1A, "Jark"): (BONE_SHORT_SWORD, OBSIDIAN_SHORT_SWORD, BONE_AXE, OBSIDIAN_MACE),
    (0x29, "Merzol"): (OBSIDIAN_AXE,),         # the slave pens' gladiator
    (0x1F, "Krikor"): (BONE_AXE,),
    (0x1D, "Chaero"): (OBSIDIAN_SHORT_SWORD,),
    (0x28, "Tari"): (OBSIDIAN_MACE,),
    (None, "Renegade"): (BONE_SHORT_SWORD,),
    (None, "Wild Mul"): (BONE_AXE,),
}


def weapon(spec: Tuple[int, int, int, int]) -> bytes:
    """A plain weapon's item record, in no list and no slot."""
    return weaponchoice.plain_weapon(TEMPLATE, 0, spec)[0]


def _carries(gd: GameData, it: ring.Items, index: int, rec: bytes) -> bool:
    lists = [struct.unpack_from("<h", gd.creature(index), o)[0] for o in game.CREATURE_ITEM_LISTS]
    return any(npcitems._same(data, rec) for t in lists for _, data in it.chain(t))


def place(gd: GameData, given: Set[str]) -> List[str]:
    """Each of WHO in the area gets the weapons of theirs not yet given this game (GIVEN: a key
    for each, updated)."""
    region = gd.region()
    wanted = {name: specs for (where, name), specs in WHO.items() if where in (None, region)}
    if not wanted:
        return []
    it = ring.Items(gd)
    for index in sorted(set(gd.combatants().values())):
        name = gd.creature_name(index)
        rec = gd.creature(index)
        if name not in wanted or len(rec) < game.CREATURE_SIZE or struct.unpack_from("<h", rec, 0)[0] <= 0:
            continue
        for spec in wanted[name]:
            item = weapon(spec)
            key = f"{gd.creature_name(0)}|world:{name}:{spec[0]}"
            if key in given:
                continue
            if _carries(gd, it, index, item):
                given.add(key)
                continue
            if npcitems.add_to(gd, index, item):
                given.add(key)
                it = ring.Items(gd)
        wanted.pop(name)  # (one of each name: the first met)
    return []  # (nothing in the log: they're there to be found)
