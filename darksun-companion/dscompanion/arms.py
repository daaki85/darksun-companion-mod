"""Two plain weapons made magic (the MAGIC_ARMS switch, on unless turned off).

- The 2 handed Bone Gythka on the dead body lying by the stone arch in the arena, where every game
  starts: Kreenfang, a gythka +1. The body is the game's object 1204, "Dead Body" (an item, its
  picture BODY_PICTURE, whose contents are a list: SEGOBJEX's RDFF 1204 has the gythka in it),
  lying where the arena puts it (BODY_AT): no other body, wherever it lies, ever counts.
  That gythka, while still in the body, is made Kreenfang, once a game (the key in the
  tools_given set, kept in settings): the Ledger looks from the game's start, before anyone can
  take it. Every other gythka stays plain: the one the arena also has lying loose (object 1011),
  those in kreen hands, and this one if it was taken without the Ledger running.
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
from typing import List, Optional, Set

from . import game, ring
from .game import GameData

ARENA = ring.ARENA
KEY = "arena gythka +1"
GYTHKA_PICTURE = 0xFC0D  # the game's gythka
BODY_PICTURE = 0x10000 - 1204  # the arena's dead body with the gythka (object 1204)
# ... where the arena puts it (RGN2A's entity table): on the map, a thing's x and y are at +9 of
# its entry in the game's table of things on the map (32 bytes each)
BODY_AT = (688, 590)
MAP_ENTRIES, MAP_ENTRY_SIZE, MAP_XY = 0x6694, 32, 0x09
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


def _arena_gythka(gd: GameData, it: ring.Items) -> Optional[int]:
    """The plain gythka still in the arena's dead body (BODY_PICTURE, lying at BODY_AT), or None."""
    for thing in range(ring.THING_COUNT):
        for _, rec in it.chain(thing, inside=False):
            if struct.unpack_from("<H", rec, 0)[0] != BODY_PICTURE:
                continue
            at = gd.ds * 16 + MAP_ENTRIES + thing * MAP_ENTRY_SIZE + MAP_XY
            if struct.unpack("<HH", gd.guest.read(at, 4)) != BODY_AT:
                continue  # (another body: never this one)
            contents, = struct.unpack_from("<H", rec, ring.ITEM_CONTENTS)
            for item, inside in it.chain(contents, inside=False):
                if struct.unpack_from("<H", inside, game.ITEM_TYPE)[0] == game.GYTHKA_TYPE \
                        and inside[game.ITEM_PLUS] == 0:
                    return item
    return None


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
    """Kurzak's Short Sword made +1 wherever it is; in the arena, the gythka still in the dead body
    there made +1, once a game (GIVEN: the key, added). Lines for the log."""
    out: List[str] = []
    it = ring.Items(gd)
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
            elif kind == game.GYTHKA_TYPE and plus == 1:  # (only the companion's has a plus)
                done.add(item)
                if _rename(gd, it, item, rec, GYTHKA_VALUE, GYTHKA_NAME):
                    out.append("The arena's Gythka +1 is named Kreenfang.")
    if key(gd) not in given and it.word(ring.REGION) == ARENA:
        body = _arena_gythka(gd, it)
        if body is not None:
            _make_magic(gd, it, body, GYTHKA_VALUE, GYTHKA_NAME)
            given.add(key(gd))
            out.append("The 2 handed Bone Gythka on the dead body in the arena is Kreenfang, a gythka +1.")
    return out
