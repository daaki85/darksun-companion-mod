"""Class restrictions (the Options tab's rule): what a character's classes keep it from equipping,
on top of the game's own class lists (each item type's mask of the classes that may use it, of
which one of the character's classes is enough). The strictest class wins. DSCLOG's
PROBE_CAN_USE does this in the game; this is its model, for the tests and the Ledger.

- A psionicist, whatever its other classes allow: light armour only (leather, hide, silk), a
  leather shield only, and of weapons only daggers, short swords, maces, clubs, chatkchas, bows
  and slings.
- A multiclass thief: light armour only, and a shield only a leather one that another of its
  classes allows.
- A preserver of that one class: no armour and no shield.
- A druid: no armour, no shield.
- A cleric: only the weapons of its sphere, or of any of its spheres (a ranger who became a
  cleric keeps the ranger's): air, missile and thrown weapons and daggers; earth, stone,
  obsidian, metal and wood; fire, obsidian; water, bone and wood.

- A multiclass preserver: no spells, wizard or priest, while it wears armour (DSCLOG's
  PROBE_NO_CAST, at the game's test for its "No spell use" effect); a shield doesn't count.

Helms count as armour. A human who has changed class (dual-classed: the class it has now is the
first) is held only by that class; another race's classes (multiclass) all hold it. Weapons of
no kind (spell-made weapons, gloves, the broken weapon) are as the game has them.
"""

from typing import Iterable, Set

from . import game, specialize

# Item type record fields (DSUN's IT1R, 20 bytes each)
TYPE_FLAGS, TYPE_MATERIAL, TYPE_KIND_FLAGS, TYPE_CLASSES = 0x00, 0x08, 0x0F, 0x10
MELEE, MISSILE, SHIELD, THROWN = 0x01, 0x02, 0x04, 0x10
ARMOUR = 0x80  # (+0Fh: shields have it too)
WOOD, BONE, STONE, OBSIDIAN, METAL, LEATHER = range(6)  # (the material's low nibble)
NO_MATERIAL = 0x40  # (with a low nibble of 0)

# Class numbers (game.CLASS_NAMES): a cleric, druid and ranger for each element
CLERICS, DRUIDS, RANGERS = range(1, 5), range(5, 9), range(13, 17)
PRESERVER, PSIONICIST, THIEF = 11, 12, 17
AIR, EARTH, FIRE, WATER = range(4)
THIEF_BIT = 0x400  # (the sheet's class flags, +12h)

PSIONICIST_KINDS = frozenset(specialize.KINDS.index(k) for k in
                             ("dagger", "short sword", "mace", "club", "chatkcha", "bow", "sling"))


def material(typ: bytes) -> int:
    """The material's number (WOOD..LEATHER), or -1 for none."""
    low = typ[TYPE_MATERIAL] & 0x0F
    return -1 if typ[TYPE_MATERIAL] & NO_MATERIAL and not low else low


def is_weapon(typ: bytes) -> bool:
    return bool(typ[TYPE_FLAGS] & (MELEE | MISSILE))


def is_shield(typ: bytes) -> bool:
    return bool(typ[TYPE_FLAGS] & SHIELD)


def is_armour(typ: bytes) -> bool:
    """Body, arm and leg armour and helms: not shields."""
    return bool(typ[TYPE_KIND_FLAGS] & ARMOUR) and not is_shield(typ)


def is_light(typ: bytes) -> bool:
    return material(typ) in (LEATHER, -1)


def spheres(classes: Iterable[int]) -> Set[int]:
    return {(c - 1) % 4 for c in classes if c in CLERICS or c in RANGERS}


def sphere_allows(sphere: int, typ: bytes, kind: int) -> bool:
    if sphere == AIR:
        return bool(typ[TYPE_FLAGS] & (MISSILE | THROWN)) or kind == specialize.KINDS.index("dagger")
    return material(typ) in {EARTH: (STONE, OBSIDIAN, METAL, WOOD), FIRE: (OBSIDIAN,), WATER: (BONE, WOOD)}[sphere]


def allowed(sheet: bytes, item_type: int, typ: bytes) -> bool:
    """Whether the character may equip an item of this type, given that the game lets it."""
    classes = [c for c in sheet[game.SHEET_CLASSES:game.SHEET_CLASSES + 3] if c]
    human = sheet[game.SHEET_RACE] == game.HUMAN
    holding = classes[:1] if human else classes
    multiclass = not human and len(classes) > 1
    armour, shield = is_armour(typ), is_shield(typ)
    kind = specialize.kind_of(item_type) if is_weapon(typ) else None
    if PSIONICIST in holding:
        if armour and not is_light(typ) or shield and material(typ) != LEATHER:
            return False
        if kind is not None and kind not in PSIONICIST_KINDS:
            return False
    if THIEF in holding and multiclass:
        if armour and not is_light(typ):
            return False
        if shield:
            others = int.from_bytes(typ[TYPE_CLASSES:TYPE_CLASSES + 2], "little")
            others &= int.from_bytes(sheet[game.SHEET_FLAGS:game.SHEET_FLAGS + 2], "little") & ~THIEF_BIT
            if material(typ) != LEATHER or not others:
                return False
    if holding == [PRESERVER] and (armour or shield):
        return False
    if any(c in DRUIDS for c in holding) and (armour or shield):
        return False
    if any(c in CLERICS for c in holding) and kind is not None:
        if not any(sphere_allows(s, typ, kind) for s in spheres(classes)):
            return False
    return True


def no_spells(sheet: bytes, worn: Iterable[bytes]) -> bool:
    """Whether a character can't cast for the armour it wears (the type records of what it has on
    its arms, legs, head and chest)."""
    classes = [c for c in sheet[game.SHEET_CLASSES:game.SHEET_CLASSES + 3] if c]
    if sheet[game.SHEET_RACE] == game.HUMAN or len(classes) < 2 or PRESERVER not in classes:
        return False
    return any(is_armour(t) for t in worn)
