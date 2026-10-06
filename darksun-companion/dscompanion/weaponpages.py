"""The weapon pages of the character creation panel (weapon specialization; DSCLOG's PROBE_WP_*).

The creation screen's panel shows the psionic disciplines (WIND 3012 in RESOURCE.GFF) or, for a
cleric, druid or ranger, the clerical spheres (WIND 3013), each a column of rows to mark and a
button under them that changes between the two. With weapon specialization, a fighter, gladiator
or ranger also chooses a weapon kind there: four more windows like the spheres', four kinds each
(specialize.KINDS, in order), their button MORE SPECS, the last's VIEW PSIONICS. The windows a
warrior is shown (3018 for the disciplines, 3019 for the spheres) have WEAPON SPEC in place of
VIEW SPHERES or VIEW PSIONICS.

The rows' and buttons' pictures (ICON, three frames: as they are, out of use, marked) are made in
the game's small carved letters, taken from its own rows (CLERIC, P-KINESIS and the rest); the
game has no X, Q or Z in them, so those are drawn here in the same hand. They go in the
Ledger's copy of RESOURCE.GFF (icons.write_resources), with the buttons (BUTN, copies of the
spheres') and the windows.
"""

import struct
from typing import Dict, List, Optional, Tuple

from . import gff, specialize
from .art import decode_frame

DISCIPLINES, SPHERES = 3012, 3013  # the game's windows
PAGES = (3014, 3015, 3016, 3017)  # the weapon pages
WARRIOR_DISCIPLINES, WARRIOR_SPHERES = 3018, 3019
PICKER = 3021  # the level-up window (like the psionicists', 17501)
PSIONIC_PICKER = 17501
PICK_FIRST = 0x860  # its rows, 0x860 + kind (the carved names without the mark's room)
PICK_COUNT_BUTTON, PICK_EXIT = 0x2C37, 0x4396  # (the psionicists' window's: picks left, EXIT)
PICK_X, PICK_GAP_X, PICK_Y, PICK_PITCH = 6, 82, 6, 8  # the rows' place: two columns of eight
# The rows' letters outlined in black, so that they read clearly over the marble: near-white
# 19.4:1 against the outline, light grey out of use 8.1:1 (WCAG 2.0 AA asks 4.5:1); the
# interface's own greys, which no region's palette changes. (DSCLOG's PROBE_PK_TITLE has the
# window's line under them drawn in the same near-white.)
PICK_COLOURS = [255, 214, 214]
PICK_OUTLINE = 254
# The Effects screen: under the selected character's effects (in the panel the game fills only
# past 21 of them), a heading for the skill and the kinds' rows (DSCLOG's PROBE_EF_ROWS); by
# skill (DSCLOG's SPEC_SPECIAL to SPEC_GRAND, then expertise)
HEADINGS = ((0x871, "SPECIALIZED IN"), (0x872, "MASTER OF"), (0x873, "GRAND MASTER OF"), (0x874, "EXPERT IN"))
HEADING_COLOURS = [214, 214, 214]
ROW_FIRST = 0x840  # the 16 kinds' rows, 0x840 + kind (after the dialogue window's and others', 81Ch-833h)
MORE, BACK, VIEW = 0x850, 0x851, 0x852  # MORE SPECS, VIEW PSIONICS, WEAPON SPEC
ROW_TEMPLATE, TOGGLE_TEMPLATE = 0x7FA, 0x7FF  # (AIR's row and VIEW PSIONICS's button)
SPHERE_TOGGLE, DISCIPLINE_TOGGLE = 0x7FF, 0x7FE
WIND_COUNT, ITEM_AT, ITEM_SIZE = 243, 0x105, 30
ROW_PAD = 10  # a row's letters start this far in (the mark goes before them)
HEIGHT = 7

# The game's labels and what they say, to take letters from: each run of columns with ink is a
# letter where the counts agree; CUTS takes the rest from where letters touch (icon, first and
# past-the-last column, letter)
LABELS = {0x7D2: "CLERIC", 0x7D3: "DRUID", 0x7D4: "FIGHTER", 0x7D7: "PSIONICIST", 0x7D8: "RANGER",
          0x7D9: "THIEF", 0x7FA: "AIR", 0x7FB: "EARTH", 0x7FC: "FIRE", 0x7FE: "VIEW SPHERES",
          0x7FF: "VIEW PSIONICS"}
CUTS = ((0x7F6, 20, 28, "K"), (0x7F7, 20, 31, "M"), (0x7F7, 56, 64, "B"), (0x7F8, 79, 88, "Y"))
DRAWN = {
    "X": ("###..###",
          ".##...#.",
          "..##.#..",
          "...##...",
          "..#.##..",
          ".#...##.",
          "###..###"),
    "Q": (".#####..",
          "##...##.",
          "##...##.",
          "##...##.",
          "##.#.##.",
          "##..##..",
          ".####.##"),
    "Z": ("#######",
          "#...##.",
          "...##..",
          "..##...",
          ".##....",
          "##...#.",
          "#######"),
}
GAP, SPACE = 1, 4  # columns between letters, and for a space

Glyph = List[List[bool]]
Rows = List[List[Optional[int]]]


def _ink(chunk: bytes) -> Glyph:
    _, _, rows = decode_frame(chunk, 0)
    return [[p is not None for p in r] for r in rows]


def _runs(ink: Glyph) -> List[Tuple[int, int]]:
    width = len(ink[0]) if ink else 0
    cols = [any(r[x] for r in ink) for x in range(width)]
    out, x = [], 0
    while x < width:
        if cols[x]:
            start = x
            while x < width and cols[x]:
                x += 1
            out.append((start, x))
        else:
            x += 1
    return out


def glyphs(resource: gff.Chunks) -> Dict[str, Glyph]:
    """Each letter's ink, HEIGHT rows."""
    out: Dict[str, Glyph] = {}
    for cid, text in LABELS.items():
        ink = _ink(resource[("ICON", cid)])
        letters = text.replace(" ", "")
        runs = _runs(ink)
        if len(runs) == len(letters):
            for (a, b), ch in zip(runs, letters):
                out.setdefault(ch, [r[a:b] for r in ink])
    for cid, a, b, ch in CUTS:
        ink = _ink(resource[("ICON", cid)])
        cut = [r[a:b] for r in ink]
        inked = [x for x in range(b - a) if any(r[x] for r in cut)]
        out.setdefault(ch, [r[inked[0]:inked[-1] + 1] for r in cut])
    for ch, art in DRAWN.items():
        out[ch] = [[c == "#" for c in line] for line in art]
    return out


def label(font: Dict[str, Glyph], text: str, pad: int, colour: int) -> Rows:
    """TEXT in the carved letters, PAD columns in, in COLOUR."""
    rows: Rows = [[None] * pad for _ in range(HEIGHT)]
    for i, ch in enumerate(text):
        if ch == " ":
            for r in rows:
                r.extend([None] * SPACE)
            continue
        if i and text[i - 1] != " ":
            for r in rows:
                r.extend([None] * GAP)
        g = font[ch]
        for y in range(HEIGHT):
            rows[y].extend(colour if on else None for on in g[y])
    return rows


def _colours(chunk: bytes) -> List[int]:
    """The ink's colour in each frame of a label."""
    count, = struct.unpack_from("<H", chunk, 4)
    out = []
    for f in range(count):
        _, _, rows = decode_frame(chunk, f)
        out.append(next(p for r in rows for p in r if p is not None))
    return out


def picture(font: Dict[str, Glyph], text: str, pad: int, colours: List[int]) -> bytes:
    from .savepages import encode_frames
    return encode_frames([label(font, text, pad, c) for c in colours])


def _encode(frames: List[Rows]) -> bytes:
    from .savepages import encode_frames
    return encode_frames(frames)


def outlined(font: Dict[str, Glyph], text: str, colours: List[int]) -> bytes:
    """TEXT with a black outline a pixel wide (the picture a pixel bigger all round than the
    letters); a frame for each colour."""
    frames = []
    for colour in colours:
        rows = label(font, text, 1, colour)
        width = len(rows[0]) + 1
        rows = [[None] * width] + [r + [None] for r in rows] + [[None] * width]
        ink = {(x, y) for y, r in enumerate(rows) for x, p in enumerate(r) if p is not None}
        for y, r in enumerate(rows):
            for x in range(width):
                if (x, y) not in ink and any((x + dx, y + dy) in ink for dx in (-1, 0, 1) for dy in (-1, 0, 1)):
                    r[x] = PICK_OUTLINE
        frames.append(rows)
    return _encode(frames)


def _button(template: bytes, template_id: int, new_id: int) -> bytes:
    return template.replace(struct.pack("<I", template_id), struct.pack("<I", new_id))


def _window(template: bytes, wid: int, items: List[Tuple[int, int, int]]) -> bytes:
    """A window like TEMPLATE (its frame and place), its own id WID, with these buttons (id, x, y)."""
    head = bytearray(template[:ITEM_AT])
    struct.pack_into("<I", head, 8, wid)
    body = b"".join(bytes(4) + b"BUTN" + struct.pack("<IHH", cid, x, y) + bytes(ITEM_SIZE - 16)
                    for cid, x, y in items)
    out = bytearray(bytes(head) + body + template[ITEM_AT + ITEM_SIZE * struct.unpack_from("<H", template, WIND_COUNT)[0]:])
    struct.pack_into("<I", out, 4, len(out))
    struct.pack_into("<H", out, WIND_COUNT, len(items))
    return bytes(out)


def _items(window: bytes) -> List[Tuple[int, int, int]]:
    count, = struct.unpack_from("<H", window, WIND_COUNT)
    return [struct.unpack_from("<IHH", window, ITEM_AT + i * ITEM_SIZE + 8) for i in range(count)]


SHORT = {"long sword": "LNG SWORD", "short sword": "SHRT SWORD", "quarterstaff": "QTR STAFF",
         "staff sling": "STF SLING"}  # (rows the panel is too narrow for)


def page_text(kind: int) -> str:
    name = specialize.KINDS[kind]
    return SHORT.get(name, name.upper())


def chunks(resource: gff.Chunks) -> Dict[Tuple[str, int], bytes]:
    """For the Ledger's copy of RESOURCE.GFF: the weapon pages, the warriors' windows, and their
    rows' and buttons' pictures and buttons."""
    font = glyphs(resource)
    row_colours = _colours(resource[("ICON", ROW_TEMPLATE)])
    toggle_colours = _colours(resource[("ICON", TOGGLE_TEMPLATE)])
    row_button, toggle_button = resource[("BUTN", ROW_TEMPLATE)], resource[("BUTN", TOGGLE_TEMPLATE)]
    added: Dict[Tuple[str, int], bytes] = {}
    for kind in range(len(specialize.KINDS)):
        cid = ROW_FIRST + kind
        added[("ICON", cid)] = picture(font, page_text(kind), ROW_PAD, row_colours)
        added[("BUTN", cid)] = _button(row_button, ROW_TEMPLATE, cid)
    for cid, text in ((MORE, "MORE SPECS"), (BACK, "VIEW PSIONICS"), (VIEW, "WEAPON SPEC")):
        added[("ICON", cid)] = picture(font, text, 0, toggle_colours)
        added[("BUTN", cid)] = _button(toggle_button, TOGGLE_TEMPLATE, cid)
    spheres = resource[("WIND", SPHERES)]
    sphere_items = _items(spheres)  # (four rows, then the button)
    rows_at = [(x, y) for _, x, y in sphere_items[:4]]
    toggle_at = sphere_items[4][1:]
    for page, wid in enumerate(PAGES):
        items = [(ROW_FIRST + page * specialize.PAGE_SIZE + r, x, y) for r, (x, y) in enumerate(rows_at)]
        items.append((MORE if page < len(PAGES) - 1 else BACK, *toggle_at))
        added[("WIND", wid)] = _window(spheres, wid, items)
    added[("WIND", WARRIOR_SPHERES)] = _window(
        spheres, WARRIOR_SPHERES, [(VIEW if c == SPHERE_TOGGLE else c, x, y) for c, x, y in sphere_items])
    disciplines = resource[("WIND", DISCIPLINES)]
    added[("WIND", WARRIOR_DISCIPLINES)] = _window(
        disciplines, WARRIOR_DISCIPLINES, [(VIEW if c == DISCIPLINE_TOGGLE else c, x, y) for c, x, y in _items(disciplines)])
    psionic = resource[("WIND", PSIONIC_PICKER)]
    keep = [(c, x, y) for c, x, y in _items(psionic) if c in (PICK_COUNT_BUTTON, PICK_EXIT)]
    for kind in range(len(specialize.KINDS)):
        cid = PICK_FIRST + kind
        added[("ICON", cid)] = outlined(font, page_text(kind), PICK_COLOURS)
        added[("BUTN", cid)] = _button(row_button, ROW_TEMPLATE, cid)
    rows = [(PICK_FIRST + k, PICK_X - 1 + PICK_GAP_X * (k // 8), PICK_Y - 1 + PICK_PITCH * (k % 8))
            for k in range(len(specialize.KINDS))]  # (the outline a pixel out from the letters)
    added[("WIND", PICKER)] = _window(psionic, PICKER, rows + keep)
    for cid, text in HEADINGS:
        added[("ICON", cid)] = outlined(font, text, HEADING_COLOURS)
    return added
