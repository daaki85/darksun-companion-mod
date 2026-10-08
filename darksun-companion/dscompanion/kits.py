"""The kits' effects, as DSCLOG makes them (its KIT_* routines): for the Ledger and the dice log.

A kit is a sheet's KIT_BYTE (kitpages.py, which also numbers them: kitpages.kit_id); these take
that number, 0 for none (the rule off, more than one class, none chosen).
"""

from typing import Optional, Tuple

from .kitpages import KIT_IDS, KITS

RAVAGER, SENTINEL, STALKER = KIT_IDS["Ravager"], KIT_IDS["Sentinel"], KIT_IDS["Stalker"]
MYRMIDON, CHAMPION = KIT_IDS["Myrmidon"], KIT_IDS["Arena Champion"]
ASSASSIN, SWASHBUCKLER = KIT_IDS["Assassin"], KIT_IDS["Swashbuckler"]
CRUSADER, SCHOLAR, BATTLE_MAGE, MIND_WARRIOR = (KIT_IDS["Crusader"], KIT_IDS["Scholar"], KIT_IDS["Battle Mage"],
                                                KIT_IDS["Mind Warrior"])
ELEMENTALIST, SEEKER, JUSTIFIER = KIT_IDS["Elementalist"], KIT_IDS["Seeker"], KIT_IDS["Justifier"]
WIZARD, PRIEST = 1, 2  # (the kinds of magic, as game.MAGIC_KINDS has their bits)
# a Seeker's priest slots at spell levels 1, 2 and 3, by ranger level from 6 (the 10th's on: DSCLOG's
# SEEKER_SLOTS); a Justifier's one 1st-level slot from 10th level
SEEKER_SLOTS = ((1, 0, 0), (2, 0, 0), (2, 1, 0), (2, 2, 0), (2, 2, 1))
SEEKER_FIRST, JUSTIFIER_FIRST = 6, 10
MIND_BENDER, KINETICIST = KIT_IDS["Mind Bender"], KIT_IDS["Kineticist"]
# the psionic powers' disciplines, by power (0-33: spells 138-171): psychokinesis to PK_LAST,
# psychometabolism, telepathy from TP_FIRST (the defences among them)
PK_LAST, TP_FIRST = 5, 20
HEALER = KIT_IDS["Healer"]
# the healing spells' dice (DSCLOG's CURE_SPELLS): Cure Light, Serious and Critical Wounds, Blood Flow
CURE_LIGHT, CURE_SERIOUS, CURE_CRITICAL, BLOOD_FLOW = 71, 112, 127, 108
CURE_DICE = {CURE_LIGHT: (1, 8), CURE_SERIOUS: (2, 8), CURE_CRITICAL: (3, 8), BLOOD_FLOW: (2, 6)}
# the kits with a warrior's THAC0 (PROBE_THAC0)
WARRIOR_THAC0 = frozenset((SWASHBUCKLER, CRUSADER, BATTLE_MAGE, MIND_WARRIOR))
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


def thac0(kid: int, level: int, game_thac0: int) -> int:
    """The THAC0 the game gives a character of kit KID (PROBE_THAC0), its own GAME_THAC0 at class
    level LEVEL: a Swashbuckler's, Crusader's, Battle Mage's or Mind Warrior's a warrior's (21 less
    the level, 1 at best) where better; a Scholar's 1 worse."""
    if kid == SCHOLAR:
        return game_thac0 + 1
    if kid in WARRIOR_THAC0:
        return min(game_thac0, max(1, 21 - level))
    return game_thac0


def slot_level(kid: int, level: int) -> int:
    """The class level the spell slots are counted from (PROBE_SLOT_LEVEL): an Elementalist's a
    level behind."""
    return max(0, level - 1) if kid == ELEMENTALIST else level


def slots(kid: int, magic: int, level: int, spell_level: int, game_slots: int) -> int:
    """The spell slots at SPELL_LEVEL of a character of kit KID and class level LEVEL, the game
    giving GAME_SLOTS of MAGIC (WIZARD or PRIEST) (PROBE_SLOTS): an Arcanist's wizard slots 1 more
    at each spell level it has any, a Battle Mage's 1 fewer, a Crusader's priest slots 1 fewer; a
    Seeker's and a Justifier's priest slots their own tables' (SEEKER_SLOTS), WIS's left out."""
    if kid == ARCANIST and magic == WIZARD:
        return game_slots + 1 if game_slots else 0
    if (kid == BATTLE_MAGE and magic == WIZARD) or (kid == CRUSADER and magic == PRIEST):
        return max(0, game_slots - 1)
    if kid in (SEEKER, JUSTIFIER) and magic == PRIEST:
        if not 1 <= spell_level <= 3:
            return 0
        if kid == JUSTIFIER:
            return int(level >= JUSTIFIER_FIRST and spell_level == 1)
        if level < SEEKER_FIRST:
            return 0
        return SEEKER_SLOTS[min(level, SEEKER_FIRST + len(SEEKER_SLOTS) - 1) - SEEKER_FIRST][spell_level - 1]
    return game_slots


def psp_cost(kid: int, power: int, cost: int) -> int:
    """The PSP power POWER (0-33) costs a character of kit KID to use, the game asking COST
    (KIT_PSP): a Mind Bender's telepathy 2 less and its psychokinesis 2 more, a Kineticist's the
    other way about, never below 1; psychometabolism, and a cost of 0, as they are."""
    if cost <= 0 or kid not in (MIND_BENDER, KINETICIST):
        return cost
    change = -2 if kid == MIND_BENDER else 2
    if power <= PK_LAST:
        change = -change
    elif power < TP_FIRST:
        change = 0
    return max(1, cost + change)


def cure_bonus(kid: int, spell: int) -> int:
    """Added to the healing of SPELL cast by a character of kit KID (PROBE_CURE): a Healer's 1 a
    die of Cure Light, Serious and Critical Wounds."""
    if kid == HEALER and spell in CURE_DICE and spell != BLOOD_FLOW:
        return CURE_DICE[spell][0]
    return 0


def cure_die(kid: int, spell: int) -> int:
    """The sides of the die more a Lifebinder's SPELL heals (PROBE_CURE: the cures and Blood
    Flow), or 0."""
    return CURE_DICE[spell][1] if kid == LIFEBINDER and spell in CURE_DICE else 0


def ranger_cast_drop(kid: int) -> int:
    """How much less than its ranger level a ranger casts at (PROBE_RANGER_CAST; the game's 7): a
    Seeker's 5 (1st at 6th level, 5th at 10th), a Justifier's 9 (1st at 10th)."""
    return {SEEKER: 5, JUSTIFIER: 9}.get(kid, 7)


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
    -15 to pick pockets (0) and open locks (1), a Swashbuckler's -10 to every one."""
    if kid == SWASHBUCKLER:
        return -10
    return -15 if kid == ASSASSIN and skill in (0, 1) else 0


def stealth(kid: int) -> int:
    """Added to a ranger's hiding in shadows and moving silently (the stealth rule's, rolled by
    the Ledger): a Stalker's 15."""
    return 15 if kid == STALKER else 0


def forbids(kid: int, typ: bytes, kind: Optional[int], half_giant: bool, spec: bool = False,
            off_hand: bool = False) -> bool:
    """Whether the kit keeps a character from an item type (TYP its record; KIND its weapon kind,
    or None), as DSCLOG's KIT_FORBIDS: a Ravager a shield, a missile or thrown weapon and armour that isn't
    light; a Twin-blade a shield, and a two-handed weapon (but a
    half-giant's, HALF_GIANT: with the rule for its hands); a Brute a one-handed melee weapon, a
    shield (but a half-giant's), and, choosing a weapon spec (SPEC), a missile weapon; a Stalker
    armour that isn't light; a Grove Warden a metal weapon; a Lifebinder a weapon of a kind not
    blunt; a Shinobi a shield, armour that isn't light, a weapon not of SHINOBI_KINDS. Going to the
    off hand (OFF_HAND): nothing for a Battle Mage, no weapon for a Healer."""
    flags, kinds, mat = typ[0], typ[0x0F], typ[8] & 0x4F
    weapon = bool(flags & (MELEE | MISSILE))
    if off_hand and (kid == BATTLE_MAGE or kid == HEALER and flags & (MELEE | MISSILE | THROWN)):
        return True
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
