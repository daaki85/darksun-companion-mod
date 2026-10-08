"""The kits' effects, as DSCLOG makes them (its KIT_* routines): for the Ledger and the dice log.

A kit is a sheet's KIT_BYTE (kitpages.py, which also numbers them: kitpages.kit_id); these take
that number, 0 for none (the rule off, more than one class, none chosen).
"""

from typing import Optional

from .kitpages import KIT_IDS, KITS

RAIDER, SENTINEL, STALKER = KIT_IDS["Raider"], KIT_IDS["Sentinel"], KIT_IDS["Stalker"]
MYRMIDON, CHAMPION = KIT_IDS["Myrmidon"], KIT_IDS["Arena Champion"]
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
