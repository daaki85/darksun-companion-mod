"""Weapon specialization (the Options tab's rule): the weapon kinds a fighter, gladiator or ranger
can choose, and which of the game's item types each takes in.

The game has no notion of a weapon's kind: its item types are one per weapon and material (a
metal, a bone and an obsidian long sword are three), and its named weapons are types of their
own (Bloodwrath, Swiftbite). KIND_OF_TYPE sorts every weapon type into one of the sixteen KINDS,
by its dice, weight and name; the spell-made weapons (Flame Blade, Shillelagh, Spiritual
Hammer), the gloves and the broken weapon are none.

The kinds come in the order of the character creation panel's four weapon pages, four to a
page, long sword first: the default, marked when Fighter, Gladiator or Ranger is chosen, as
the game marks the first psionic discipline and clerical sphere.
"""

from typing import Dict, Optional

from . import game

KINDS = ("long sword", "dagger", "short sword", "mace",
         "club", "axe", "great axe", "pick",
         "quarterstaff", "polearm", "gythka", "cahulaks",
         "chatkcha", "bow", "sling", "staff sling")
PAGE_SIZE = 4
DEFAULT = 0  # long sword

# The game's item types (DSUN's IT1R, numbered from 0) by kind, and the companion's own short sword
_TYPES = {
    "long sword": (45, 63, 81, 47, 41, 50, 85, 97, 98),  # obsidian, metal, bone; Dragonsbane and El's
    # Drinker (47), Draketooth, Swiftbite, Dark Flame, Hornblade, Bloodwrath: all 1d8 blades
    "dagger": (17, 33, 84, 94),  # obsidian, stone; Dag's Dagger, Terror Blade
    "short sword": (game.SHORT_SWORD_TYPE,),
    "mace": (20, 46),  # bone (Mace, Wyvern Hook); Blackmace
    "club": (18,),  # Club, Striker
    "axe": (22,),  # Axe, Soulcrusher
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
