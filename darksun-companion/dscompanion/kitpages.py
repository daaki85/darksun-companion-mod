"""Kits: the creation panel's KIT page (DSCLOG's KIT_* routines) and the kits' names.

A character of one class may take one of its class's three kits, or none (the class as it is).
The kit is the sheet's byte KIT_BYTE: 0 none, 1 to 3 the class's kits in KITS's order. It is
chosen on the creation panel, on a page of its own (a window for each class, its rows the
NO KIT and the class's kits, its button VIEW PSIONICS back to the disciplines), which KITS opens:
the button of the disciplines' window for a class with no sphere, of the spheres' for a
cleric, druid or ranger, of the last weapon page for a warrior choosing weapons. The rows'
pictures are carved as the weapon pages' are (weaponpages.py), names too long for the panel
shortened as the game shortens its own (P-KINESIS).
"""

from typing import Dict, List, Optional, Sequence, Tuple

from . import gff, specialize
from . import weaponpages as wp

KIT_BYTE = 0x43
# By class as the creation screen numbers them (game.CREATION_CLASS_NAMES): the kits' names
KITS = {1: ("Elementalist", "Healer", "Crusader"),
        2: ("Grove Warden", "Lifebinder", "Wanderer"),
        3: ("Myrmidon", "Sentinel", "Ravager"),
        4: ("Arena Champion", "Twin-blade", "Brute"),
        5: ("Scholar", "Battle Mage", "Arcanist"),
        6: ("Mind Bender", "Mind Warrior", "Kineticist"),
        7: ("Stalker", "Justifier", "Seeker"),
        8: ("Swashbuckler", "Assassin", "Shinobi")}
# the rows' text where the name is too long for the panel
SHORT = {"Arena Champion": "CHAMPION", "Swashbuckler": "SWASHBUCK", "Elementalist": "ELEMENTAL",
         "Grove Warden": "WARDEN", "Battle Mage": "BATTLMAGE", "Mind Bender": "M-BENDER", "Mind Warrior": "M-WARRIOR"}
# the widest a row's picture may be, its mark's room in: the panel's frame comes in to about 95
# pixels past the rows' left at the second kit's row, and a few more are kept clear of it
ROW_WIDTH = 88
# a sheet's class (game.CLASS_NAMES, 1-17) as the creation screen numbers them
CREATION_CLASS = {**{c: 1 for c in range(1, 5)}, **{c: 2 for c in range(5, 9)}, 9: 3, 10: 4, 11: 5, 12: 6,
                  **{c: 7 for c in range(13, 17)}, 17: 8}

KIT_DISCIPLINES, KIT_SPHERES, KIT_LAST_PAGE = 3022, 3023, 3025  # (3020 and 3024 are the game's)
KIT_WINDOW = 3026  # + creation class - 1
KIT_ROW, KIT_NONE, KIT_VIEW = 0x870, 0x888, 0x889  # rows: KIT_ROW + 3 * (class - 1) + kit - 1
DRAWN = {
    "J": ("..####",
          "...##.",
          "...##.",
          "...##.",
          "...##.",
          "##.##.",
          ".###.."),
    "-": ("...",
          "...",
          "...",
          "...",
          "###",
          "...",
          "..."),
}

# the rules' bits (game.RULE_SPECIALIZE, game.RULE_KITS), here to keep this module standalone
SPECIALIZE, KITS_ON = 4096, 65536
WARRIORS, SPHERES = {3, 4, 7}, {1, 2, 7}  # (creation classes: fighter, gladiator, ranger; cleric, druid)


def row_text(name: str) -> str:
    return SHORT.get(name, name.upper())


def kit_id(sheet: bytes) -> int:
    """The kit of a sheet as DSCLOG's KIT_ID numbers it (the creation class x 4 + the kit: RAVAGER
    15), or 0: none chosen, or more than one class. (The rule is the caller's to weigh.)"""
    if len(sheet) <= KIT_BYTE or sheet[0x22] or sheet[0x23]:
        return 0
    kit, cls = sheet[KIT_BYTE], CREATION_CLASS.get(sheet[0x21])
    return cls * 4 + kit if cls is not None and 1 <= kit <= 3 else 0


# KIT_ID's numbers, by name
KIT_IDS = {name: cls * 4 + k + 1 for cls, names in KITS.items() for k, name in enumerate(names)}


def kit_name(sheet: bytes) -> Optional[str]:
    """The kit of a sheet (the game's classes, 1-17), or None: none chosen, or more than one class."""
    kid = kit_id(sheet)
    return KITS[kid // 4][kid % 4 - 1] if kid else None


def kit_class(classes: Sequence[int], rules: int) -> int:
    """The creation class with kits to choose (CLASSES as the creation sheet has them, 0 for
    none), or 0: the rule off, or more than one class."""
    if not rules & KITS_ON or any(classes[1:3]) or not 1 <= classes[0] <= 8:
        return 0
    return classes[0]


def panel_windows(classes: Sequence[int], rules: int, kit: int = 0) -> Tuple[int, int]:
    """The windows the panel shows for the sheet being made: the disciplines' and the spheres'
    (DSCLOG's WP_IDS); KIT its kit byte (a Battle Mage, a preserver's second, counts as a warrior
    with weapon specialization, for its weapon spec)."""
    warrior = any(c in WARRIORS for c in classes) or bool(rules & KITS_ON) and kit_class(classes, rules) == 5 and kit == 2
    sphere = any(c in SPHERES for c in classes)
    if rules & SPECIALIZE and warrior:
        return (wp.DISCIPLINES if sphere else wp.WARRIOR_DISCIPLINES), wp.WARRIOR_SPHERES
    if kit_class(classes, rules):
        return (wp.DISCIPLINES if sphere else KIT_DISCIPLINES), KIT_SPHERES
    return wp.DISCIPLINES, wp.SPHERES


def chunks(resource: gff.Chunks) -> Dict[Tuple[str, int], bytes]:
    """For the Ledger's copy of RESOURCE.GFF: the kit pages, the windows with KITS for their
    button, and their rows' and buttons' pictures and buttons."""
    font = wp.glyphs(resource)
    for ch, art in DRAWN.items():
        font[ch] = [[c == "#" for c in line] for line in art]
    row_colours = wp._colours(resource[("ICON", wp.ROW_TEMPLATE)])
    toggle_colours = wp._colours(resource[("ICON", wp.TOGGLE_TEMPLATE)])
    row_button, toggle_button = resource[("BUTN", wp.ROW_TEMPLATE)], resource[("BUTN", wp.TOGGLE_TEMPLATE)]
    added: Dict[Tuple[str, int], bytes] = {}
    rows: List[Tuple[int, str]] = [(KIT_ROW + 3 * (cls - 1) + k, row_text(name))
                                   for cls, names in KITS.items() for k, name in enumerate(names)]
    for cid, text in rows + [(KIT_NONE, "NO KIT")]:
        added[("ICON", cid)] = wp.picture(font, text, wp.ROW_PAD, row_colours)
        added[("BUTN", cid)] = wp._button(row_button, wp.ROW_TEMPLATE, cid)
    added[("ICON", KIT_VIEW)] = wp.picture(font, "KITS", 0, toggle_colours)
    added[("BUTN", KIT_VIEW)] = wp._button(toggle_button, wp.TOGGLE_TEMPLATE, KIT_VIEW)
    spheres = resource[("WIND", wp.SPHERES)]
    sphere_items = wp._items(spheres)  # (four rows, then the button)
    rows_at = [(x, y) for _, x, y in sphere_items[:4]]
    toggle_at = sphere_items[4][1:]
    for cls in KITS:
        ids = [KIT_NONE] + [KIT_ROW + 3 * (cls - 1) + k for k in range(3)]
        items = [(cid, x, y) for cid, (x, y) in zip(ids, rows_at)] + [(wp.BACK, *toggle_at)]
        added[("WIND", KIT_WINDOW + cls - 1)] = wp._window(spheres, KIT_WINDOW + cls - 1, items)
    added[("WIND", KIT_SPHERES)] = wp._window(
        spheres, KIT_SPHERES, [(KIT_VIEW if c == wp.SPHERE_TOGGLE else c, x, y) for c, x, y in sphere_items])
    disciplines = resource[("WIND", wp.DISCIPLINES)]
    added[("WIND", KIT_DISCIPLINES)] = wp._window(
        disciplines, KIT_DISCIPLINES,
        [(KIT_VIEW if c == wp.DISCIPLINE_TOGGLE else c, x, y) for c, x, y in wp._items(disciplines)])
    last = len(wp.PAGES) - 1
    page_rows = [(wp.ROW_FIRST + last * specialize.PAGE_SIZE + r, x, y) for r, (x, y) in enumerate(rows_at)]
    added[("WIND", KIT_LAST_PAGE)] = wp._window(spheres, KIT_LAST_PAGE, page_rows + [(KIT_VIEW, *toggle_at)])
    return added


def row_widths(resource: gff.Chunks) -> Dict[str, int]:
    """Each row's picture's width (to hold them to ROW_WIDTH)."""
    font = wp.glyphs(resource)
    for ch, art in DRAWN.items():
        font[ch] = [[c == "#" for c in line] for line in art]
    out = {}
    for names in KITS.values():
        for name in names:
            out[name] = len(wp.label(font, row_text(name), wp.ROW_PAD, 1)[0])
    out["NO KIT"] = len(wp.label(font, "NO KIT", wp.ROW_PAD, 1)[0])
    return out
