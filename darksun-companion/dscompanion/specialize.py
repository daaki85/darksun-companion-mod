"""Weapon specialization (the Options tab's rule): the weapon kinds a fighter, gladiator or ranger
can choose, and which of the game's item types each takes in.

The game has no notion of a weapon's kind: its item types are one per weapon and material (a
metal, a bone and an obsidian long sword are three), and its named weapons are types of their
own (Bloodwrath, Swiftbite). KIND_OF_TYPE sorts every weapon type into one of the sixteen KINDS,
by its dice, weight and name; the spell-made weapons (Flame Blade, Shillelagh, Spiritual
Hammer), the gloves and the broken weapon are none.

The kinds come in the order of the character creation panel's four weapon pages, four to a
page, long sword first: the default, as the game marks the first psionic discipline and
clerical sphere; a gladiator's two at creation are the long sword and the club, the first two.
"""

from typing import Dict, List, Optional, Tuple

from . import game

KINDS = ("long sword", "club", "dagger", "short sword",
         "mace", "axe", "great axe", "pick",
         "quarterstaff", "polearm", "gythka", "cahulaks",
         "chatkcha", "bow", "sling", "staff sling")
PAGE_SIZE = 4
DEFAULT = 0  # long sword

# The game's item types (DSUN's IT1R, numbered from 0) by kind, and the companion's own short sword
_TYPES = {
    "long sword": (45, 63, 81, 47, 41, 50, 85, 97, 98),  # obsidian, metal, bone; Dragonsbane and El's
    # Drinker (47), Draketooth, Swiftbite, Dark Flame, Hornblade, Bloodwrath: all 1d8 blades
    "dagger": (17, 33, 84, 94),  # obsidian, stone; Dag's Dagger, Terror Blade
    "short sword": (game.SHORT_SWORD_TYPE, game.BONE_SHORT_SWORD_TYPE, game.OBSIDIAN_SHORT_SWORD_TYPE,
                    game.METAL_SHORT_SWORD_TYPE),  # Kurzak's (metal); the Ledger's
    "mace": (20, 46),  # bone (Mace, Wyvern Hook); Blackmace
    "club": (18,),  # Club, Striker
    "axe": (22, game.BONE_AXE_TYPE, game.OBSIDIAN_AXE_TYPE),  # Axe, Soulcrusher (metal); the Ledger's
    "great axe": (2,),
    "pick": (112,),
    "quarterstaff": (3, 80),  # Quarterstaff, Parting Staff; Balk's Staff
    "polearm": (19, 111),
    "gythka": (game.GYTHKA_TYPE,),
    "cahulaks": (21,),
    "chatkcha": (48,),
    "bow": (1, 69),  # Bow, Seeker; Phrain's Bow
    "sling": (64,),
    "staff sling": (0,),
}
KIND_OF_TYPE: Dict[int, int] = {t: KINDS.index(kind) for kind, types in _TYPES.items() for t in types}


def kind_of(item_type: int) -> Optional[int]:
    """The weapon kind (its number in KINDS) of an item type, or None for one that is none."""
    return KIND_OF_TYPE.get(item_type)


def page_of(kind: int) -> int:
    """The creation panel's weapon page a kind is on (0-3), and its row there is kind % PAGE_SIZE."""
    return kind // PAGE_SIZE


# A character's skill with a weapon, as DSCLOG's SPEC_OF works it out (game.SPEC_SLOTS holds the
# chosen kinds, kind + 1 each): NONE when it has chosen none (monsters too: the game's numbers),
# PLAIN with a weapon of another kind (or as a dual-classed warrior whose warrior class isn't
# back yet), EXPERT a ranger's (no fighter or gladiator class: the
# attacks only), SPECIAL, MASTER (a fighter's own kind, its first, from 5th level), GRAND (9th)
NONE, PLAIN, EXPERT, SPECIAL, MASTER, GRAND = range(6)
SKILL_NAMES = {SPECIAL: "specialized", MASTER: "mastery", GRAND: "grand mastery"}
FIGHTER, GLADIATOR = 9, 10
MASTERY, GRAND_MASTERY = 5, 9


RANGERS = range(13, 17)


def active_classes(sheet: bytes) -> List[Tuple[int, int]]:
    """(class, level) for the classes whose abilities a character has now: all of them, but a
    human's earlier ones (dual-classed: the class it has now is the first) only once the new
    class's level has passed theirs."""
    classes = sheet[game.SHEET_CLASSES:game.SHEET_CLASSES + 3]
    levels = sheet[game.SHEET_LEVELS:game.SHEET_LEVELS + 3]
    human = sheet[game.SHEET_RACE] == game.HUMAN
    return [(classes[i], levels[i]) for i in range(3)
            if classes[i] and not (human and i and levels[i] >= levels[0])]


def skill(sheet: bytes, item_type: Optional[int]) -> int:
    chosen = sheet[game.SPEC_SLOTS:game.SPEC_SLOTS + game.SPEC_COUNT]
    if not any(chosen):
        return NONE
    kind = kind_of(item_type) if item_type is not None else None
    if kind is None or kind + 1 not in chosen:
        return PLAIN
    active = active_classes(sheet)
    classes = {c for c, _ in active}
    if not classes & ({FIGHTER, GLADIATOR} | set(RANGERS)):
        return PLAIN  # (a dual-classed warrior, until the new class's level passes the old)
    if not {FIGHTER, GLADIATOR} & classes:
        return EXPERT
    if chosen.index(kind + 1):
        return SPECIAL
    fighter = next((level for c, level in active if c == FIGHTER), 0)
    return GRAND if fighter >= GRAND_MASTERY else MASTER if fighter >= MASTERY else SPECIAL


def attacks(halves: int, level: int, missile: bool = False) -> int:
    """The attacks a round (in halves) with a weapon, from the game's (sheet +2Ah) and the skill
    with it, as DSCLOG's PROBE_ATTACKS has them: a warrior (more than 2 halves) in melee half an
    attack less with a kind not chosen, a grand master one more; missiles as the game has them."""
    if missile or halves <= 2:
        return halves
    return halves - 1 if level == PLAIN else halves + 2 if level == GRAND else halves


def to_hit(level: int) -> int:
    """What the skill adds to hit (takes off THAC0)."""
    return 3 if level >= MASTER else 1 if level == SPECIAL else 0


def damage(level: int) -> int:
    """What the skill adds to the damage."""
    return 3 if level >= MASTER else 2 if level == SPECIAL else 0
