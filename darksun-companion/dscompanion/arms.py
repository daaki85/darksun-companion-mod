"""Two plain weapons made magic (the MAGIC_ARMS switch, on unless turned off).

- The arena's 2 handed Bone Gythka, the Tohr-kreen's: Kreenfang, a gythka +1. The game has gythkas
  only in the hands of kreen, none with a plus. Only the arena's becomes Kreenfang: in the arena
  (where every game starts), once no living monster holds it (on the Tohr-kreen's body, on the
  ground, or taken by the party there), once a game (the key in the tools_given set, kept in
  settings). The Tohr-kreen fights with its plain one, and gythkas anywhere else stay plain.
- Kurzak's Short Sword (npcitems.py): Shadowseeker, a short sword +1, wherever it is (on him or
  taken). Whoever wields it (in either hand) can see the invisible: the game's own way with a
  magic item's spell (its +0Fh, one past the spell's number), which it puts on the wearer when the
  item is readied and takes off when it's put away, for a spell it counts as helpful (Detect
  Invisibility is; a weapon's other spells are cast on what it hits instead). A sword already
  in hand when the Ledger made it so has it from the next time it is readied. Its item box shows
  the spell's icon (its +02h: right-clicked, the spell's description).

Each has a name of its own, as the Templar's Bloodwrath (an obsidian long sword +1, 20800) has, in
entries DSCLOG adds (names.py); is priced near it; and has an icon of its own (icons.py:
Kreenfang's blades in the fire colours, Shadowseeker's night steel). The game shows the plus with the
name ("+1 Kreenfang"), and it counts for hitting and damage as any magic weapon's. Weapons an
earlier version made +1 get the name and price too.
"""

import struct
from typing import List, Set

from . import game, ring
from .game import GameData

ARENA = ring.ARENA
KEY = "arena gythka +1"
GYTHKA_PICTURE = 0xFC0D  # the game's gythka
SWORD_NAME, GYTHKA_NAME = 0x147, 0x148  # name entries DSCLOG adds
NAMES = {SWORD_NAME: b"Shadowseeker", GYTHKA_NAME: b"Kreenfang"}  # as DSCLOG's EXTRA_NAMES has them
# near the Bloodwrath's 20800 (the plain ones: 6 and 500); metal is the dearer, on Athas
GYTHKA_VALUE, SWORD_VALUE = 18000, 22000
ITEM_VALUE = 0x06  # an item's price (npcitems.ITEM_VALUE)
ITEM_SPELL = 0x0F  # an item's spell, one past the spell's number (0: none)
ITEM_SPELL_SHOWN = 0x02  # (a word) the spell whose icon its box shows, the same
SWORD_SPELL = game.DETECT_INVISIBILITY + 1
OLD_VALUES = (2000, 2500)  # what an earlier version priced them at


def key(gd: GameData) -> str:
    return f"{gd.creature_name(0)}|{KEY}"


def _held_by_monsters(gd: GameData, it: ring.Items) -> Set[int]:
    """The items of the living creatures in the area who aren't in the party."""
    out: Set[int] = set()
    for index in set(gd.combatants().values()):
        if index < game.PARTY_SIZE:
            continue
        rec = gd.creature(index)
        if len(rec) < game.CREATURE_SIZE or struct.unpack_from("<h", rec, 0)[0] <= 0:
            continue
        for offset in game.CREATURE_ITEM_LISTS:
            thing, = struct.unpack_from("<h", rec, offset)
            out.update(item for item, _ in it.chain(thing))
    return out


def _make_magic(gd: GameData, it: ring.Items, item: int, value: int, name: int, spell: int = 0) -> None:
    at = it.items + item * game.ITEM_SIZE
    gd.guest.write(at + game.ITEM_PLUS, b"\x01")
    if spell:
        _give_spell(gd, at, spell)
    gd.guest.write(at + ITEM_VALUE, struct.pack("<H", value))
    gd.guest.write(at + game.ITEM_NAME, struct.pack("<H", name))


def _give_spell(gd: GameData, at: int, spell: int) -> None:
    gd.guest.write(at + ITEM_SPELL, bytes((spell,)))
    gd.guest.write(at + ITEM_SPELL_SHOWN, struct.pack("<H", spell))


def _rename(gd: GameData, it: ring.Items, item: int, rec: bytes, value: int, name: int) -> bool:
    """One an earlier version made +1 (its plain name, its price then): today's. True if it was."""
    if struct.unpack_from("<H", rec, game.ITEM_NAME)[0] == name:
        return False
    at = it.items + item * game.ITEM_SIZE
    gd.guest.write(at + game.ITEM_NAME, struct.pack("<H", name))
    if struct.unpack_from("<H", rec, ITEM_VALUE)[0] in OLD_VALUES:
        gd.guest.write(at + ITEM_VALUE, struct.pack("<H", value))
    return True


def upgrade(gd: GameData, given: Set[str]) -> List[str]:
    """Kurzak's Short Sword made +1 wherever it is; in the arena, its gythka once no living monster
    holds it, made +1, once a game (GIVEN: the key, added). Lines for the log."""
    out: List[str] = []
    it = ring.Items(gd)
    gythkas: List[int] = []
    done = set()
    for thing in range(ring.THING_COUNT):
        for item, rec in it.chain(thing):
            if item in done:
                continue
            kind, = struct.unpack_from("<H", rec, game.ITEM_TYPE)
            plus = rec[game.ITEM_PLUS]
            if kind == game.SHORT_SWORD_TYPE and plus == 0:
                _make_magic(gd, it, item, SWORD_VALUE, SWORD_NAME, SWORD_SPELL)
                done.add(item)
                out.append("Kurzak's Short Sword is Shadowseeker, a short sword +1: its wielder sees the invisible.")
            elif kind == game.SHORT_SWORD_TYPE and plus == 1:
                done.add(item)
                if _rename(gd, it, item, rec, SWORD_VALUE, SWORD_NAME):
                    out.append("Kurzak's Short Sword +1 is named Shadowseeker.")
                if rec[ITEM_SPELL] != SWORD_SPELL:
                    _give_spell(gd, it.items + item * game.ITEM_SIZE, SWORD_SPELL)
                    out.append("Shadowseeker lets its wielder see the invisible (from the next time it's readied).")
                elif struct.unpack_from("<H", rec, ITEM_SPELL_SHOWN)[0] != SWORD_SPELL:
                    _give_spell(gd, it.items + item * game.ITEM_SIZE, SWORD_SPELL)  # (its box's icon)
            elif kind == game.GYTHKA_TYPE and plus == 0:
                gythkas.append(item)
            elif kind == game.GYTHKA_TYPE and plus == 1:  # (only the companion's has a plus)
                done.add(item)
                if _rename(gd, it, item, rec, GYTHKA_VALUE, GYTHKA_NAME):
                    out.append("The arena's Gythka +1 is named Kreenfang.")
    if gythkas and key(gd) not in given and it.word(ring.REGION) == ARENA:
        held = _held_by_monsters(gd, it)  # (the Tohr-kreen's while it lives)
        free = next((item for item in gythkas if item not in held), None)
        if free is not None:
            _make_magic(gd, it, free, GYTHKA_VALUE, GYTHKA_NAME)
            given.add(key(gd))
            out.append("The arena's 2 handed Bone Gythka (the Tohr-kreen's) is Kreenfang, a gythka +1.")
    return out
