"""Alagorn tells of the Ledger's magic weapons: Kreenfang and Shadowseeker (arms.py), Gutterknot,
Deepbiter, Windlash and Greenbright (worldgear.py).

Alagorn, the wizard wandering the Painted Badlands, identifies magic items from menus by kind
(script 213): magic swords, magic weapons, fruit and wands. Each kind's part sees which of the
items he knows the party carries (a local for each, from a query on the item's picture: the
Bloodwrath's is -1576), says there are none, or shows a menu of those, one reply each; a reply's
story clears its local, and when none is left the menu's loop ends.

With the Ledger, Shadowseeker and Greenbright join the swords, and Kreenfang, Gutterknot, Deepbiter
and Windlash the weapons, by their pictures of their own (icons.py: without the icons' copy he
doesn't know them), each only with its content switch on. As pensasks.py does, nothing
of the game's script moves: commands of it become jumps (64h) to code put after the script's end,
which jumps back:

- each kind's first test for none carried: the new items' locals set too, and none of them all
  carried goes on to "no magic swords" / "no magic weapons", any to the menu's part;
- the kind's menu: a copy with the new items' replies after the game's last;
- each of the kind's stories' test for none left: the new items counted too.

The new stories are subroutines, as the game's replies are.
"""

from typing import Dict, List, Optional, Tuple

from . import gpl, icons
from .kalzith import _Script
from .pensasks import GOTO, LONGEST, MENU, TEST

SCRIPT = 213  # Alagorn's
LOCAL_READ, LOCAL_SET = 0x8E, 14
QUERY, PARTY, HAS_PICTURE = 0x33, 32766, 72  # a query on the party's items: picture equal
DONE = 15  # the menu loop's local (1: leave it)
SET, SAY = 0x16, 0x4F
NOTHING = "  Nothing"  # each menu's last reply, leaving it


class Kind:
    def __init__(self, first_reply: str, none_text: str, items: Tuple[Tuple[str, str], ...]):
        self.first_reply, self.none_text, self.items = first_reply, none_text, items


SWORDS, WEAPONS = ("  Darkflame", "It's too bad that you have no magic swords I know about. "), \
    ("  Balkazar's Staff", "I don't see any magic weapons that I know anything about. ")
# (item, story): the slave pens' two (arms.py)
ARMS = {
    SWORDS: (("Shadowseeker",
              "Shadowseeker! The head guards of the Draj slave pens have passed it down, one to the "
              "next. With it in hand, no slave could hide from them: not in the pens' shadows, not "
              "behind an illusion, not even made invisible by a friend's magic. Many an escape ended "
              "at its point. Better that it is in your hands now."),),
    WEAPONS: (("Kreenfang",
               "Kreenfang! The tohr-kreen say a gythka's blades are grown, not carved, and a clutch's "
               "elder blessed this one before the hunt. It strikes truer and deeper than any common "
               "gythka. A kreen does not part with such a weapon while it lives; whoever carried it "
               "into the arena died with it in hand."),),
}
# ... and the world's (worldgear.py)
MAGIC = {
    SWORDS: (("Greenbright",
              "Greenbright! True iron, forged in the Green Age, when Athas still had forests and "
              "smiths who knew more than how to knap stone. It was a long sword once; a thousand "
              "years of sharpening have worn it short, and the old enchantment only grew keener "
              "for it. Arant took it from a gladiator who would not kneel. He never fought fair "
              "again, and never needed to."),),
    WEAPONS: (("Gutterknot",
               "Gutterknot! A knot of agafari root, the hardest wood under the sun, with the stub "
               "of an iron spike driven through it. Every boss of the Draj low warrens has beaten "
               "his way up with it and held it until someone beat him down with it in turn. The "
               "warrens say whoever holds it can't be made to kneel. Churrr believed that."),
              ("Deepbiter",
               "Deepbiter! A dwarf of the Undermountain made it his focus: to dig to the root of "
               "the world. He cut its head from a vein of stone no other pick could mark and sang "
               "into it every day of his life. It breaks rock as other picks break earth, and "
               "bone more easily still. His kin kept it after he died, still digging."),
              ("Windlash",
               "Windlash! The desert elves make their staff slings to run and hunt with at once. "
               "This one was made for a chieftain's son, its cords braided with his own hair, and "
               "a wind spirit's blessing sung over it. Its stones fly farther and strike harder "
               "than any other's. How a village bowyer came by it, I'd rather not ask."),),
}


def kinds(arms: bool = True, magic: bool = True) -> Tuple[Kind, ...]:
    """Each kind with the new items of the switches on."""
    out = []
    for kind in (SWORDS, WEAPONS):
        items = (ARMS[kind] if arms else ()) + (MAGIC[kind] if magic else ())
        if items:
            out.append(Kind(kind[0], kind[1], items))
    return tuple(out)


KINDS = kinds()


def _picture(name: str) -> int:
    """The item's picture of its own, as an item has it (negative)."""
    return icons.PICTURES[name] - 0x10000


def _zero(locals_: List[int]) -> tuple:
    out: list = []
    for n in locals_:
        out += (["and"] if out else []) + ["(", ("var", LOCAL_READ, n), "==", ("n", 0), ")"]
    return ("expr", out)


def _locals(expr) -> Optional[List[int]]:
    """The locals an "all of these are 0" test names, or None for another test."""
    if not (isinstance(expr, tuple) and expr[0] == "expr"):
        return None
    parts, out = expr[1], []
    for i in range(0, len(parts), 6):
        group = parts[i:i + 5]
        if len(group) != 5 or group[0] != "(" or group[2] != "==" or group[3] != ("n", 0) \
                or not (isinstance(group[1], tuple) and group[1][:2] == ("var", LOCAL_READ)):
            return None
        out.append(group[1][2])
    return out


def _sets(op) -> Optional[Tuple[int, int]]:
    """(local, picture) for a "local = the party carries an item with this picture" command."""
    if op.code != SET or len(op.args) != 2 or op.args[1][:2] != ("var", LOCAL_SET):
        return None
    value = op.args[0]
    if not (isinstance(value, tuple) and value[0] == "op" and value[1].code == QUERY):
        return None
    tests = value[1].args[3]
    if len(tests) != 1 or tests[0][0] != HAS_PICTURE or not isinstance(tests[0][2], tuple):
        return None
    return op.args[1][2], tests[0][2][1]


def _story_end(ops, start: int) -> int:
    """The index of the return (15h) ending the story starting at ops[START]."""
    return next(i for i in range(start, len(ops)) if ops[i].code == 0x15)


def with_items(script: bytes, field_types: bytes, kinds=KINDS) -> bytes:
    """SCRIPT (the game's) with each kind's new item (unchanged if it isn't as expected)."""
    if any(gpl.encode_expr(("str", f"  {item}")) in script for kind in kinds for item, _ in kind.items):
        return script  # (done already: the commands made jumps no longer decode)
    ops = gpl.decode(script, field_types)
    at_index = {op.at: i for i, op in enumerate(ops)}
    s = _Script()
    jumps: List[Tuple[int, str]] = []
    for k, kind in enumerate(kinds):
        # the kind's part: its "none carried" line, and the queries and tests before it
        none = next((i for i, o in enumerate(ops) if o.code == SAY and o.args[1] == ("str", kind.none_text)), None)
        menu_i = next((i for i, o in enumerate(ops) if o.code == MENU and o.args[0]["replies"]
                       and o.args[0]["replies"][0]["text"] == ("str", kind.first_reply)), None)
        if none is None or menu_i is None:
            return script
        queries = []
        i = none - 1
        while i >= 0 and not _sets(ops[i]):
            i -= 1
        while i >= 0 and _sets(ops[i]):
            queries.insert(0, _sets(ops[i]))
            i -= 1
        first_test = i + 1 + len(queries)
        if not queries or ops[first_test].code != TEST:
            return script
        first = max(n for n, _ in queries) + 1
        mine = list(range(first, first + len(kind.items)))
        if mine[-1] >= DONE:
            return script
        all_of = [n for n, _ in queries] + mine
        # ... after "none carried" (a return), the part going on to the menu
        go_on = none + 1
        while go_on < len(ops) and ops[go_on].code != SAY:
            go_on += 1
        entry = f"entry {k}"
        s.label(entry)
        for (item, _), n in zip(kind.items, mine):
            s.op(SET, ("op", gpl.Op(0, QUERY, [("n", PARTY), 77, 80, [(HAS_PICTURE, 4, ("n", _picture(item)))]])),
                 ("var", LOCAL_SET, n))
        s.op(TEST, _zero(all_of))
        s.op(0x3E, ("n", ops[go_on].at))  # (any carried: on to the menu)
        s.op(GOTO, ("n", ops[none].at))
        jumps.append((ops[first_test].at, entry))

        # the menu: the game's replies, then the new ones
        menu = ops[menu_i].args[0]
        replies = list(menu["replies"])
        # (before the game's "Nothing", which leaves: it stays last)
        at = next((r for r, reply in enumerate(replies) if reply["text"] == ("str", NOTHING)), len(replies))
        for j, ((item, text), n) in enumerate(zip(kind.items, mine)):
            story = f"story {k} {j}"
            s.sub(story, lambda text=text, n=n, all_of=all_of: (
                s.say(text), s.set(n, 0),
                s.when(_zero(all_of), lambda: s.set(DONE, 1))))
            replies.insert(at + j, {"text": ("str", f"  {item}"), "goto": ("label", story),
                                    "if": ("var", LOCAL_READ, n), "before": [], "after": []})
        copy = f"menu {k}"
        s.label(copy)
        s.op(MENU, dict(menu, replies=replies))
        s.op(GOTO, ("n", ops[menu_i + 1].at))
        jumps.append((ops[menu_i].at, copy))

        # the game's stories: their test for none left counts the new item too
        for r, reply in enumerate(menu["replies"]):
            start = at_index.get(reply["goto"][1]) if reply["goto"][0] == "n" else None
            if start is None:
                return script
            end = _story_end(ops, start)
            for t in range(start, end - 2):
                names = _locals(ops[t].args[0]) if ops[t].code == TEST else None
                if names is None or ops[t + 1].code != 0x3E or ops[t + 2].args != [("n", 1), ("var", LOCAL_SET, DONE)]:
                    continue
                left = f"left {k} {r}"
                s.label(left)
                s.op(TEST, _zero(names + mine))
                s.op(0x3E, ops[t + 1].args[0])  # (some left: past the end of the loop's flag)
                s.op(GOTO, ("n", ops[t + 2].at))
                jumps.append((ops[t].at, left))
    added = s.bytes(base=len(script), end=False)
    out = bytearray(script) + added
    if len(out) > LONGEST:
        return script
    for at, label in jumps:
        jump = gpl.encode_op((GOTO, [("n", s.at[label])]))
        out[at:at + len(jump)] = jump
    return bytes(out)


def script_chunks(chunks, field_types: bytes, arms: bool = True, magic: bool = True) -> Dict[Tuple[str, int], bytes]:
    """For the Ledger's copy of GPLDATA: Alagorn's talk with the magic weapons of the switches on
    (ARMS: Kreenfang and Shadowseeker; MAGIC: the world's)."""
    key = ("GPL ", SCRIPT)
    chosen = kinds(arms, magic)
    if key not in chunks or not chosen:
        return {}
    changed = with_items(chunks[key], field_types, chosen)
    return {key: changed} if changed != chunks[key] else {}
