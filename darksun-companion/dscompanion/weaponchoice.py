"""New characters' weapon kinds and starting weapon (weapon specialization).

A character is chosen its kinds on the creation panel (weaponpages.py); before it is first
played (its status New) the Ledger makes them whole:

- a fighter or ranger has one kind, the long sword if none was marked; a gladiator two, the
  long sword and the club if none were; any other class none (marked as a warrior, then made
  something else);
- the game's starting weapon, the bone long sword in the right hand, becomes a plain weapon of
  the first kind, of bone or obsidian where the game has one (the axe is metal, the great axe
  and the pick its only ones), with its picture and name; a bow, sling or staff sling goes to the
  missile slot, and a bow comes with arrows.
"""

import struct
from typing import List, Optional, Tuple

from . import game, specialize

FIGHTER, GLADIATOR = 9, 10
RANGERS = range(13, 17)
START_TYPE, START_NAME = 81, 0x1C  # the bone long sword the game starts warriors with
MISSILE_SLOT = game.EQUIP_SLOTS.index("missile")
AMMO_SLOT = game.EQUIP_SLOTS.index("ammo")
ITEM_PICTURE, ITEM_COUNT, ITEM_VALUE = 0x00, 0x02, 0x06
ARROWS = (0xFBD2, 62, 0x36, 1, 20)  # (picture, type, name, price, how many)

# By kind (specialize.KINDS): the plain weapon's type, name entry, picture (an item's +0: the
# object's number negated) and price
PLAIN: Tuple[Tuple[int, int, int, int], ...] = (
    (81, 0x1C, 0xFC0C, 45),    # long sword (bone)
    (18, 0x11, 0xFB5F, 1),     # club
    (17, 0x10, 0xFB60, 2),     # dagger (obsidian)
    (game.SHORT_SWORD_TYPE, 0x144, 0xF685, 10),  # short sword (the Ledger's)
    (20, 0x13, 0xFB5D, 8),     # mace (bone)
    (22, 0x1A, 0xFB61, 100),   # axe (metal: the game's only axe)
    (2, 0x03, 0xFC06, 12),     # great axe
    (112, 0xAD, 0xFB46, 8),    # pick (stone)
    (3, 0x04, 0xFC05, 1),      # quarterstaff
    (19, 0x12, 0xFB5E, 7),     # polearm (bone)
    (44, 0x3A, 0xFC0D, 6),     # gythka (bone)
    (21, 0x14, 0xFB5C, 10),    # cahulaks (bone)
    (48, 0x39, 0xFC0E, 2),     # chatkcha (obsidian)
    (1, 0x02, 0xFC07, 30),     # bow
    (64, 0x00, 0xFC09, 1),     # sling
    (0, 0x01, 0xFC08, 2),      # staff sling
)
MISSILE_KINDS = frozenset(specialize.KINDS.index(k) for k in ("bow", "sling", "staff sling"))
BOW = specialize.KINDS.index("bow")


def kinds_for(sheet: bytes) -> List[int]:
    """The kinds (+1 each, as in the sheet) a new character ends up with."""
    classes = set(sheet[game.SHEET_CLASSES:game.SHEET_CLASSES + 3])
    chosen = list(sheet[game.SPEC_SLOTS:game.SPEC_SLOTS + game.SPEC_COUNT])
    if GLADIATOR in classes:
        first = chosen[0] or 1
        second = chosen[1] if chosen[1] and chosen[1] != first else (2 if first != 2 else 1)
        return [first, second, 0, 0]
    if FIGHTER in classes or classes & set(RANGERS):
        return [chosen[0] or 1, 0, 0, 0]
    return [0, 0, 0, 0]


def plain_weapon(start: bytes, kind: int) -> Tuple[bytes, Optional[int]]:
    """The starting weapon's record made the kind's plain weapon, and the slot it goes to (None:
    where it is)."""
    type_, name, picture, price = PLAIN[kind]
    rec = bytearray(start)
    struct.pack_into("<H", rec, ITEM_PICTURE, picture)
    struct.pack_into("<H", rec, ITEM_VALUE, price)
    struct.pack_into("<H", rec, game.ITEM_TYPE, type_)
    struct.pack_into("<H", rec, game.ITEM_NAME, name)
    struct.pack_into("<H", rec, 0x0C, 0)  # (the game's cache of the item's icon: loaded anew)
    rec[game.ITEM_PLUS] = 0
    slot = MISSILE_SLOT if kind in MISSILE_KINDS else None
    if slot is not None:
        rec[game.ITEM_SLOT] = slot
    return bytes(rec), slot


def arrows(template: bytes) -> bytes:
    picture, type_, name, price, count = ARROWS
    rec = bytearray(template)
    struct.pack_into("<HH", rec, ITEM_PICTURE, picture, count)
    struct.pack_into("<H", rec, ITEM_VALUE, price)
    struct.pack_into("<H", rec, game.ITEM_TYPE, type_)
    struct.pack_into("<H", rec, game.ITEM_NAME, name)
    struct.pack_into("<H", rec, 0x0C, 0)
    rec[game.ITEM_PLUS] = 0
    return bytes(rec)


def finish_new(gd) -> List[str]:
    """The party's New characters' kinds made whole, and their starting weapons changed: lines
    for the log."""
    from . import npcitems
    out: List[str] = []
    sheets = game.far_pointer(gd.guest, gd.ds, game.SHEETS_PTR)
    items = game.far_pointer(gd.guest, gd.ds, game.ITEMS_PTR)
    for member in range(game.PARTY_SIZE):
        rec = gd.creature(member)
        if len(rec) < game.CREATURE_SIZE or not rec[game.CREATURE_NAME] or rec[game.CREATURE_STATUS] != game.STATUS_NEW:
            continue
        index = struct.unpack_from("<H", rec, game.CREATURE_SHEET_INDEX)[0]
        sheet = gd.guest.read(sheets + index * game.SHEET_SIZE, game.SHEET_SIZE)
        if len(sheet) < game.SHEET_SIZE:
            continue
        kinds = kinds_for(sheet)
        if bytes(kinds) != sheet[game.SPEC_SLOTS:game.SPEC_SLOTS + game.SPEC_COUNT]:
            gd.guest.write(sheets + index * game.SHEET_SIZE + game.SPEC_SLOTS, bytes(kinds))
        if not kinds[0] or kinds[0] == 1:
            continue
        for item_index, item, _ in gd._worn(member):
            if struct.unpack_from("<H", item, game.ITEM_TYPE)[0] == START_TYPE \
                    and struct.unpack_from("<H", item, game.ITEM_NAME)[0] == START_NAME \
                    and item[game.ITEM_SLOT] in game.WEAPON_HANDS and item[game.ITEM_PLUS] == 0:
                kind = kinds[0] - 1
                new, _ = plain_weapon(item, kind)
                gd.guest.write(items + item_index * game.ITEM_SIZE, new)
                if kind == BOW:
                    npcitems.add_to(gd, member, arrows(new), AMMO_SLOT)
                out.append(f"{gd.creature_name(member)} starts with a plain {specialize.KINDS[kind]} "
                           f"for the weapon specialization chosen, in place of the long sword")
                break
    return out
