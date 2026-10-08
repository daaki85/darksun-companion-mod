"""The kits' effects, as DSCLOG makes them (its KIT_* routines): for the Ledger and the dice log.

A kit is a sheet's KIT_BYTE (kitpages.py, which also numbers them: kitpages.kit_id); these take
that number, 0 for none (the rule off, more than one class, none chosen).
"""

from typing import Optional, Tuple

from .kitpages import KIT_IDS, KITS

RAVAGER, SENTINEL, STALKER = KIT_IDS["Ravager"], KIT_IDS["Sentinel"], KIT_IDS["Stalker"]
MYRMIDON, CHAMPION = KIT_IDS["Myrmidon"], KIT_IDS["Arena Champion"]
ASSASSIN = KIT_IDS["Assassin"]
TWIN_BLADE, BRUTE = KIT_IDS["Twin-blade"], KIT_IDS["Brute"]
GROVE_WARDEN, LIFEBINDER = KIT_IDS["Grove Warden"], KIT_IDS["Lifebinder"]
WANDERER, ARCANIST = KIT_IDS["Wanderer"], KIT_IDS["Arcanist"]
# the scores a kit changes (STR, DEX, CON, INT, WIS, CHA), once, before the character is first
# played (apply_scores); SCORES_DONE the sheet's byte that says it has been
SCORES = {ARCANIST: (0, 0, -2, 0, 0, 0)}
SCORES_DONE = 0x45
SCORE_LEAST, SCORE_MOST = 3, 25
ABILITY_NAMES = ("STR", "DEX", "CON", "INT", "WIS", "CHA")
# the item type's +00h flags and +0Fh kind flags, +08h material (restrict.py's)
MELEE, MISSILE, SHIELD, THROWN, TWO_HANDED, ARMOUR = 0x01, 0x02, 0x04, 0x10, 0x40, 0x80
METAL, LEATHER, NO_MATERIAL = 4, 5, 0x40
# a Lifebinder's weapon kinds (specialize.KINDS' numbers): club, mace, quarterstaff, sling, staff sling
BLUNT = frozenset((1, 4, 8, 14, 15))
# a Shinobi's: dagger, short sword, quarterstaff, chatkcha, bow, sling, staff sling
SHINOBI_KINDS = frozenset((2, 3, 8, 12, 13, 14, 15))
SHINOBI = KIT_IDS["Shinobi"]
# the charms (DSCLOG's KIT_CHARMS): Charm Person, Charm Monster, Domination, Charm Person or
# Mammal, and the psionic Domination and Mass Domination
CHARMS = (2, 40, 61, 82, 158, 159)
SPELL_LAST = 137  # (the wizards' and priests' spells: 0 to this; psionic powers and monsters' after)
FIRE, COLD = 0x02, 0x04  # (a spell record's +1Ah: what it is, as the game's Resist Fire and Resist Cold read it)
# a Ravager's base AC by level, 1-18 and on (DSCLOG's RAVAGER_AC)
RAVAGER_AC = (7, 7, 6, 6, 5, 5, 4, 4, 3, 3, 3, 2, 2, 2, 1, 1, 1, 0)


def name(kid: int) -> str:
    return KITS[kid // 4][kid % 4 - 1] if kid else ""


def melee(kid: int, two_handed: bool) -> int:
    """Added to hit and to damage with a melee weapon (KIT_MELEE; TWO_HANDED: one that takes both
    hands, its type's +0Fh 40h): a Ravager's 1, a Brute's 2 with a two-handed one."""
    if kid == RAVAGER:
        return 1
    return 2 if kid == BRUTE and two_handed else 0


def ac(kid: int, shield: bool, level: int = 0, base: int = 10) -> int:
    """Added to AC (KIT_AC; lower is better): a Ravager's base AC by its level (RAVAGER_AC) where
    better than its sheet's BASE, armour improving it as before; a Wanderer's 1 worse; a Sentinel's
    2 better with a shield in a hand, an Arena Champion's 1; a Grove Warden's 1 better for every 3 levels (LEVEL, its
    class level)."""
    if kid == RAVAGER:
        table = RAVAGER_AC[min(max(level, 1), len(RAVAGER_AC)) - 1]
        return -max(0, base - table)
    if kid == WANDERER:
        return 1
    if kid == SENTINEL and shield:
        return -2
    if kid == CHAMPION and shield:
        return -1
    if kid == GROVE_WARDEN:
        return -(level // 3)
    return 0


def move(kid: int) -> int:
    """Added to Move in a fight (KIT_MOVE): a Stalker's 2."""
    return 2 if kid == STALKER else 0


def initiative(kid: int) -> int:
    """Added to initiative (PROBE_INIT): a Sentinel's 2."""
    return 2 if kid == SENTINEL else 0


def save(kid: int, spell: int, kinds: int = 0) -> int:
    """Added to a saving throw against SPELL (KIT_SAVE; KINDS its record's +1Ah): a Sentinel's -1
    against a wizard's or priest's spell, a Myrmidon's -4 against a charm, a Wanderer's +3 against
    fire and cold (as the game's Resist Fire and Resist Cold)."""
    if kid == SENTINEL and 0 <= spell <= SPELL_LAST:
        return -1
    if kid == MYRMIDON and spell in CHARMS:
        return -4
    if kid == WANDERER and 0 <= spell < 256 and kinds & (FIRE | COLD):
        return 3
    return 0


def champion(kid: int, shield: bool, melee: bool) -> Tuple[int, int]:
    """(to hit, damage) an Arena Champion adds to an attack (KIT_CHAMPION), in melee only: with a
    shield in a hand +1 and +1; with none, -1 to hit."""
    if kid != CHAMPION or not melee:
        return 0, 0
    return (1, 1) if shield else (-1, 0)


def thief_skill(kid: int, skill: int) -> int:
    """Added to a thief skill (game.THIEF_SKILLS' numbers; the helper's PROBE_BELT): an Assassin's
    -15 to pick pockets (0) and open locks (1)."""
    return -15 if kid == ASSASSIN and skill in (0, 1) else 0


def stealth(kid: int) -> int:
    """Added to a ranger's hiding in shadows and moving silently (the stealth rule's, rolled by
    the Ledger): a Stalker's 15."""
    return 15 if kid == STALKER else 0


def forbids(kid: int, typ: bytes, kind: Optional[int], half_giant: bool, spec: bool = False) -> bool:
    """Whether the kit keeps a character from an item type (TYP its record; KIND its weapon kind,
    or None), as DSCLOG's KIT_FORBIDS: a Ravager a shield, a missile or thrown weapon and armour that isn't
    light; a Twin-blade a shield, and a two-handed weapon (but a
    half-giant's, HALF_GIANT: with the rule for its hands); a Brute a one-handed melee weapon, a
    shield (but a half-giant's), and, choosing a weapon spec (SPEC), a missile weapon; a Stalker
    armour that isn't light; a Grove Warden a metal weapon; a Lifebinder a weapon of a kind not
    blunt; a Shinobi a shield, armour that isn't light, a weapon not of SHINOBI_KINDS."""
    flags, kinds, mat = typ[0], typ[0x0F], typ[8] & 0x4F
    weapon = bool(flags & (MELEE | MISSILE))
    light = not kinds & ARMOUR or bool(flags & SHIELD) or mat in (LEATHER, NO_MATERIAL)
    if kid == RAVAGER:
        return bool(flags & (SHIELD | MISSILE | THROWN)) or not light
    if kid == TWIN_BLADE:
        return bool(flags & SHIELD) or weapon and bool(kinds & TWO_HANDED) and not half_giant
    if kid == BRUTE:
        if flags & SHIELD:
            return not half_giant
        if flags & MELEE:
            return not kinds & TWO_HANDED
        return bool(flags & MISSILE) and spec
    if kid == STALKER:
        return bool(kinds & ARMOUR) and not flags & SHIELD and mat not in (LEATHER, NO_MATERIAL)
    if kid == GROVE_WARDEN:
        return weapon and mat == METAL
    if kid == LIFEBINDER:
        return kind is not None and kind not in BLUNT
    if kid == SHINOBI:
        if flags & SHIELD:
            return True
        if kinds & ARMOUR:
            return mat not in (LEATHER, NO_MATERIAL)
        return kind is not None and kind not in SHINOBI_KINDS
    return False


def scores_after(kid: int, scores) -> list:
    """The six scores after the kit's changes (SCORES), each kept within 3 to 25."""
    change = SCORES.get(kid, (0,) * 6)
    return [max(SCORE_LEAST, min(SCORE_MOST, v + d)) if d else v for v, d in zip(scores, change)]


def apply_scores(gd, member: int) -> list:
    """A New party member's kit's score changes (SCORES), in its sheet and creature record, once
    (the sheet's SCORES_DONE byte): lines for the log."""
    import struct
    from . import game
    kid = gd.kit_id(member)
    if kid not in SCORES:
        return []
    rec = gd.creature(member)
    index = struct.unpack_from("<H", rec, game.CREATURE_SHEET_INDEX)[0]
    at = game.far_pointer(gd.guest, gd.ds, game.SHEETS_PTR) + index * game.SHEET_SIZE
    sheet = gd.guest.read(at, game.SHEET_SIZE)
    if len(sheet) < game.SHEET_SIZE or sheet[SCORES_DONE]:
        return []
    before = list(sheet[game.SHEET_ABILITIES:game.SHEET_ABILITIES + 6])
    after = scores_after(kid, before)
    gd.guest.write(at + game.SHEET_ABILITIES, bytes(after))
    table = game.far_pointer(gd.guest, gd.ds, game.CREATURES_PTR) + member * game.CREATURE_SIZE
    gd.guest.write(table + game.CREATURE_ABILITIES, bytes(after))
    gd.guest.write(at + SCORES_DONE, b"\x01")
    changes = ", ".join(f"{ABILITY_NAMES[i]} {b} to {a}" for i, (b, a) in enumerate(zip(before, after)) if a != b)
    return [f"{gd.creature_name(member)}, a {name(kid)}: {changes}"] if changes else []


def finish_new(gd) -> list:
    """The kits' score changes for the party's New characters (apply_scores): lines for the log."""
    from . import game
    out = []
    for member in range(game.PARTY_SIZE):
        rec = gd.creature(member)
        if len(rec) >= game.CREATURE_SIZE and rec[game.CREATURE_NAME] and rec[game.CREATURE_STATUS] == game.STATUS_NEW:
            out += apply_scores(gd, member)
    return out
