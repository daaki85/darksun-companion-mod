"""The rest of the bone scale armour, where its chest piece is.

The game has Bone Scale Chest Armor, Arm Armor and Leg Armor (objects 1033-1035, the arm and leg
pieces never placed anywhere in play) but no helm of bone. The first time the Ledger sees the
chest piece in the region (on the ground, in a container, or carried), it puts the arm and leg
pieces and a Bone Helm (an item type of the companion's own: the Helm's, of bone, with an icon
of its own in the bone scale's colours, icons.py) with it: in the same pile or container, or in
the carrier's backpack. Once a game (the key in the tools_given set, kept in settings), and
never where any of the three is already (a save made after they were added).

Should one of the three go missing afterwards, while the chest piece is in the region (an item
record of the game's taken back for something else, say), it is put back with the chest piece,
once each a game (restore).
"""

import struct
from typing import List, Optional, Set

from . import game, npcitems, pickpocket, ring
from .game import GameData

KEY = "bone scale set"  # (after the leader's name: once each game, as the other things given)
CHEST_PICTURE, CHEST_TYPE = 0xFBF7, 15  # Bone Scale Chest Armor (object 1033)
HELM_NAME = 6  # "Helm" (the game shows the material before it: "Bone Helm")
# the game's own records (SEGOBJEX), in no list and no slot
ARM = npcitems._item("f6fb000000003000000037000000000005ff260100")  # Bone Scale Arm Armor
LEG = npcitems._item("f5fb000000003000000038000000000005ff270100")  # Bone Scale Leg Armor
# the leather Helm's, of the companion's bone helm type (its picture the Helm's until icons.py
# gives it its own)
HELM = npcitems._item("03fc000000000500000005000000000004ff060000", type_=game.BONE_HELM_TYPE, name=HELM_NAME)
PIECES = (ARM, LEG, HELM)
NAMES = {ARM: "Bone Scale Arm Armor", LEG: "Bone Scale Leg Armor", HELM: "Bone Helm"}


def key(gd: GameData) -> str:
    """The set's given-once key, for this game (the leader's name, as the other given keys)."""
    return f"{gd.creature_name(0)}|{KEY}"


def which_piece(rec: bytes) -> Optional[bytes]:
    """Which of the three REC is (ARM, LEG, HELM), or None."""
    if len(rec) < game.ITEM_SIZE:
        return None
    if struct.unpack_from("<H", rec, game.ITEM_TYPE)[0] == game.BONE_HELM_TYPE:
        return HELM
    return {0xFBF6: ARM, 0xFBF5: LEG}.get(struct.unpack_from("<H", rec, 0)[0])


def is_chest(rec: bytes) -> bool:
    return len(rec) >= game.ITEM_SIZE and struct.unpack_from("<HH", rec, 0)[0] == CHEST_PICTURE and \
        struct.unpack_from("<H", rec, game.ITEM_TYPE)[0] == CHEST_TYPE


def is_piece(rec: bytes) -> bool:
    """One of the pieces the Ledger adds (the arm or leg piece, or the Bone Helm)."""
    return len(rec) >= game.ITEM_SIZE and (struct.unpack_from("<H", rec, 0)[0] in (0xFBF6, 0xFBF5) or
                                           struct.unpack_from("<H", rec, game.ITEM_TYPE)[0] == game.BONE_HELM_TYPE)


def find_chest(gd: GameData) -> Optional[int]:
    """The chest piece's item number, wherever it is in the region (a pile, a container, carried),
    or None, also when any of the other pieces is already there (a game saved after they were
    added, loaded again)."""
    it = ring.Items(gd)
    chest = None
    for thing in range(ring.THING_COUNT):
        for item, rec in it.chain(thing):
            if is_piece(rec):
                return None
            if is_chest(rec) and chest is None:
                chest = item
    return chest


def carrier(gd: GameData, it: ring.Items, item: int) -> Optional[int]:
    """The party member carrying the item, if one is."""
    for member in range(game.PARTY_SIZE):
        rec = gd.creature(member)
        if len(rec) < game.CREATURE_SIZE or not rec[game.CREATURE_NAME]:
            continue
        for offset in game.CREATURE_ITEM_LISTS:
            thing, = struct.unpack_from("<h", rec, offset)
            if any(i == item for i, _ in it.chain(thing)):
                return member
    return None


def insert_after(gd: GameData, it: ring.Items, after: int, rec: bytes) -> bool:
    """An item from the game's free list, made REC, put right after item AFTER in its list
    (the same pile or container), in its slot. False if no item record is to be had."""
    item = it.word(ring.FREE_ITEMS)
    if item >= game.NO_ITEM:
        return False
    gd.guest.write(gd.ds * 16 + ring.FREE_ITEMS, it.item(item)[game.ITEM_NEXT:game.ITEM_NEXT + 2])
    before = it.item(after)
    rec = bytearray(rec)
    rec[game.ITEM_NEXT:game.ITEM_NEXT + 2] = before[game.ITEM_NEXT:game.ITEM_NEXT + 2]
    rec[game.ITEM_SLOT] = before[game.ITEM_SLOT]
    gd.guest.write(it.items + item * game.ITEM_SIZE, bytes(rec))
    gd.guest.write(it.items + after * game.ITEM_SIZE + game.ITEM_NEXT, struct.pack("<h", item))
    return True


def free_cells(gd: GameData, it: ring.Items, member: int) -> int:
    """How many of the member's backpack cells are empty."""
    rec = gd.creature(member)
    used = set()
    for offset in game.CREATURE_ITEM_LISTS:
        thing, = struct.unpack_from("<h", rec, offset)
        used.update(data[game.ITEM_SLOT] for _, data in it.chain(thing))
    return sum(1 for cell in pickpocket.BACKPACK if cell not in used)


def _put(gd: GameData, chest: int, pieces) -> List[bytes]:
    """PIECES put with the chest piece: in its carrier's backpack (all of them, or none while
    there isn't room for all), or after it in its pile or container. Those put."""
    it = ring.Items(gd)
    member = carrier(gd, it, chest)
    if member is not None:
        if free_cells(gd, it, member) < len(pieces):
            return []  # (no room in the pack for them all: the next time there is)
        return [rec for rec in pieces if npcitems.add_to(gd, member, rec)]
    return [rec for rec in reversed(pieces) if insert_after(gd, ring.Items(gd), chest, rec)]


def place(gd: GameData, given: Set[str]) -> List[str]:
    """The arm and leg pieces and the Bone Helm with the chest piece, once a game (GIVEN: the
    key, added; and never where one of them already is). Nothing for the log."""
    if key(gd) not in given and KEY in given and _any_piece(gd):
        given.add(key(gd))  # (the key of before it was this game's: the set is here, so this one's)
    if key(gd) in given:
        return restore(gd, given)
    chest = find_chest(gd)
    if chest is None:
        return []
    if _put(gd, chest, PIECES):
        given.add(key(gd))
    return []  # (nothing in the log: the items are there to be found)


def _any_piece(gd: GameData) -> bool:
    it = ring.Items(gd)
    return any(is_piece(rec) for thing in range(ring.THING_COUNT) for _, rec in it.chain(thing))


def restore(gd: GameData, given: Set[str]) -> List[str]:
    """The set given this game (its key in GIVEN): any of the three missing from the region while
    the chest piece is in it, put back with the chest piece, once each a game (a key for each,
    added). A line for the log for each."""
    it = ring.Items(gd)
    chest, present = None, set()
    for thing in range(ring.THING_COUNT):
        for item, rec in it.chain(thing):
            piece = which_piece(rec)
            if piece is not None:
                present.add(NAMES[piece])
            elif is_chest(rec) and chest is None:
                chest = item
    if chest is None:
        return []
    missing = [rec for rec in PIECES if NAMES[rec] not in present and f"{key(gd)}|again:{NAMES[rec]}" not in given]
    if not missing:
        return []
    member = carrier(gd, it, chest)
    put = _put(gd, chest, missing)
    out = []
    for rec in put:
        given.add(f"{key(gd)}|again:{NAMES[rec]}")
        where = f"in {gd.creature_name(member)}'s backpack" if member is not None else "with the Bone Scale Chest Armor"
        out.append(f"The {NAMES[rec]} had gone missing from the bone scale set: it is back, {where}.")
    return out
