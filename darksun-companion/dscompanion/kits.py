"""The kits' effects, as DSCLOG makes them (its KIT_* routines): for the Ledger and the dice log.

A kit is a sheet's KIT_BYTE (kitpages.py, which also numbers them: kitpages.kit_id); these take
that number, 0 for none (the rule off, more than one class, none chosen).
"""

from typing import Optional

from .kitpages import KIT_IDS, KITS

RAIDER, SENTINEL, STALKER = KIT_IDS["Raider"], KIT_IDS["Sentinel"], KIT_IDS["Stalker"]
MYRMIDON, CHAMPION = KIT_IDS["Myrmidon"], KIT_IDS["Arena Champion"]
ASSASSIN = KIT_IDS["Assassin"]
TWIN_BLADE, BRUTE = KIT_IDS["Twin-blade"], KIT_IDS["Brute"]
GROVE_WARDEN, LIFEBINDER = KIT_IDS["Grove Warden"], KIT_IDS["Lifebinder"]
# the item type's +00h flags and +0Fh kind flags, +08h material (restrict.py's)
MELEE, MISSILE, SHIELD, TWO_HANDED, ARMOUR = 0x01, 0x02, 0x04, 0x40, 0x80
METAL, LEATHER, NO_MATERIAL = 4, 5, 0x40
# a Lifebinder's weapon kinds (specialize.KINDS' numbers): club, mace, quarterstaff, sling, staff sling
BLUNT = frozenset((1, 4, 8, 14, 15))
# the charms (DSCLOG's KIT_CHARMS): Charm Person, Charm Monster, Domination, Charm Person or
# Mammal, and the psionic Domination and Mass Domination
CHARMS = (2, 40, 61, 82, 158, 159)
SPELL_LAST = 137  # (the wizards' and priests' spells: 0 to this; psionic powers and monsters' after)


def name(kid: int) -> str:
    return KITS[kid // 4][kid % 4 - 1] if kid else ""


def melee_damage(kid: int) -> int:
    """Added to a melee attack's damage (KIT_MELEE): a Raider's 1."""
    return 1 if kid == RAIDER else 0


def ac(kid: int, shield: bool) -> int:
    """Added to AC (KIT_AC; lower is better): a Raider's 1 worse, a Sentinel's 2 better with a
    shield in a hand."""
    if kid == RAIDER:
        return 1
    if kid == SENTINEL and shield:
        return -2
    return 0


def move(kid: int) -> int:
    """Added to Move in a fight (KIT_MOVE): a Raider's and a Stalker's 2."""
    return 2 if kid in (RAIDER, STALKER) else 0


def initiative(kid: int) -> int:
    """Added to initiative (PROBE_INIT): a Sentinel's 2."""
    return 2 if kid == SENTINEL else 0


def save(kid: int, spell: int) -> int:
    """Added to a saving throw against SPELL (KIT_SAVE): a Sentinel's -1 against a wizard's or
    priest's spell, a Myrmidon's -4 against a charm."""
    if kid == SENTINEL and 0 <= spell <= SPELL_LAST:
        return -1
    if kid == MYRMIDON and spell in CHARMS:
        return -4
    return 0


def champion(kid: int, open_ground: Optional[bool]) -> int:
    """Added to hit and to damage (KIT_CHAMPION): an Arena Champion's 1 under the open sky
    (stealth.daylight), -1 under a roof or underground; 0 when that isn't known (None)."""
    if kid != CHAMPION or open_ground is None:
        return 0
    return 1 if open_ground else -1


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
    or None), as DSCLOG's KIT_FORBIDS: a Twin-blade a shield, and a two-handed weapon (but a
    half-giant's, HALF_GIANT: with the rule for its hands); a Brute a one-handed melee weapon, a
    shield (but a half-giant's), and, choosing a weapon spec (SPEC), a missile weapon; a Stalker
    armour that isn't light; a Grove Warden a metal weapon; a Lifebinder a weapon of a kind not
    blunt."""
    flags, kinds, mat = typ[0], typ[0x0F], typ[8] & 0x4F
    weapon = bool(flags & (MELEE | MISSILE))
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
    return False
