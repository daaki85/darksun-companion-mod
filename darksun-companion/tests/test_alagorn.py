"""Alagorn tells of Kreenfang and Shadowseeker (alagorn.py), on a script shaped as his: a part
for each kind with its queries, "none carried" and a menu whose stories end the loop."""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dscompanion import alagorn, gpl
from dscompanion.kalzith import _Script

GOTO, MENU, SET, TEST, IF_NOT, END_IF, RETURN, BACK = 0x64, 0x48, 0x16, 0x18, 0x3E, 0x67, 0x15, 0x19
FIELDS = bytes(alagorn.HAS_PICTURE) + b"\x10" + bytes(16)  # (the game's field types: the picture's a word)


def query(picture):
    return ("op", gpl.Op(0, alagorn.QUERY, [("n", alagorn.PARTY), 77, 80, [(alagorn.HAS_PICTURE, 4, ("n", picture))]]))


def zero(*locals_):
    return alagorn._zero(list(locals_))


def alagorns(last="Other", kinds=alagorn.KINDS, done=alagorn.DONE, split=False):
    """Two kinds, each of two items: (part, menu, stories), the game's way (SPLIT: the test for
    none carried in two, each of a local, as script 212's clothes)."""
    s = _Script()
    for k, kind in enumerate(kinds):
        first = kind.first_reply.strip()
        s.op(SET, query(-30000 - 2 * k), ("var", 14, 0))
        s.op(SET, query(-30001 - 2 * k), ("var", 14, 1))
        if split:
            s.op(TEST, zero(0))
            s.op(IF_NOT, ("label", f"has {k}"))
            s.op(TEST, zero(1))
        else:
            s.op(TEST, zero(0, 1))
        s.op(IF_NOT, ("label", f"has {k}"))
        s.op(0x4F, ("n", 115), ("str", kind.none_text))
        s.op(BACK)
        s.label(f"has {k}")
        s.op(END_IF)
        s.op(0x4F, ("n", 115), ("str", "Let me see. "))
        s.label(f"loop {k}")
        s.op(TEST, ("expr", ["(", ("var", 0x8E, done), "==", ("n", 0), ")"]))
        s.op(0x63, ("label", f"out {k}"))
        s.op(MENU, {"before": [], "title": ("str", "What item do you show him?"), "replies": [
            {"text": ("str", f"  {name}"), "goto": ("label", f"story {k} {i}"), "if": ("var", 0x8E, i),
             "before": [], "after": []} for i, name in enumerate((first, last))]})
        s.op(GOTO, ("label", f"loop {k}"))
        s.label(f"out {k}")
        s.op(BACK)
    for k in range(len(kinds)):
        for i in range(2):
            s.label(f"story {k} {i}")
            s.op(0x4F, ("n", 115), ("str", f"Story {k} {i}. "))
            s.op(SET, ("n", 0), ("var", 14, i))
            s.op(TEST, zero(1 - i))
            s.op(IF_NOT, ("label", f"end {k} {i}"))
            s.op(SET, ("n", 1), ("var", 14, done))
            s.label(f"end {k} {i}")
            s.op(END_IF)
            s.op(RETURN)
    return s.bytes(end=False)


class AlagornTests(unittest.TestCase):
    def setUp(self):
        self.script = alagorns()
        self.out = alagorn.with_items(self.script, FIELDS, alagorn.kinds(arms=True, magic=False))
        self.ops = gpl.decode(self.script, FIELDS)
        r = gpl._Reader(self.out, FIELDS)
        r.i = len(self.script)
        self.added = []
        while r.i < len(self.out):
            self.added.append(gpl._op(r))

    def jump_from(self, op):
        """Where a command of the game's now jumps (None: left as it was)."""
        if self.out[op.at] == self.script[op.at]:
            return None
        r = gpl._Reader(self.out, FIELDS)
        r.i = op.at
        jump = gpl._op(r)
        self.assertEqual(jump.code, GOTO)
        return jump.args[0][1]

    def test_game_commands_stay(self):
        """The game's script is all there (but the commands made jumps), longer only at its end."""
        self.assertGreater(len(self.out), len(self.script))
        jumped = [op for op in self.ops if self.jump_from(op) is not None]
        # each kind: its first test, its menu, its two stories' tests
        self.assertEqual([op.code for op in jumped], [TEST, MENU, TEST, MENU, TEST, TEST, TEST, TEST])
        self.assertTrue(all(self.jump_from(op) >= len(self.script) for op in jumped))

    def test_items_looked_for_by_picture(self):
        sets = [op for op in self.added if op.code == SET and op.args[0][0] == "op"]
        self.assertEqual([alagorn._sets(op) for op in sets],
                         [(2, alagorn._picture("Shadowseeker")), (2, alagorn._picture("Kreenfang"))])

    def test_menus_have_the_new_reply(self):
        menus = [op.args[0]["replies"] for op in self.added if op.code == MENU]
        self.assertEqual([[r["text"][1] for r in m] for m in menus],
                         [["  Darkflame", "  Other", "  Shadowseeker"],
                          ["  Balkazar's Staff", "  Other", "  Kreenfang"]])
        self.assertEqual([m[2]["if"] for m in menus], [("var", 0x8E, 2)] * 2)

    def test_stories_wait_for_the_new_one(self):
        tests = [alagorn._locals(op.args[0]) for op in self.added if op.code == TEST]
        self.assertIn([1, 2], tests)  # (the first story: the second and the new one left)
        self.assertIn([0, 2], tests)
        self.assertIn([0, 1, 2], tests)  # (the new story, and none carried)

    def test_new_story_said(self):
        lines = " ".join(s for s in gpl.strings(self.added))
        self.assertIn("Shadowseeker! The head guards of the Draj slave pens", lines)
        self.assertIn("Kreenfang!", lines)

    def test_once(self):
        self.assertEqual(alagorn.with_items(self.out, FIELDS), self.out)

    def test_the_worlds_too(self):
        """With the world's magic weapons: Greenbright and the Flame Blade with the swords, Gutterknot, Deepbiter and
        Windlash with the weapons, each its own local and story, before a "Nothing" reply."""
        script = alagorns(last=alagorn.NOTHING.strip())
        out = alagorn.with_items(script, FIELDS)
        r = gpl._Reader(out, FIELDS)
        r.i = len(script)
        added = []
        while r.i < len(out):
            added.append(gpl._op(r))
        menus = [[x["text"][1] for x in op.args[0]["replies"]] for op in added if op.code == MENU]
        self.assertEqual(menus, [["  Darkflame", "  Shadowseeker", "  Greenbright", "  Flame Blade", alagorn.NOTHING],
                                 ["  Balkazar's Staff", "  Kreenfang", "  Gutterknot", "  Deepbiter", "  Windlash",
                                  alagorn.NOTHING]])
        sets = [alagorn._sets(op) for op in added if op.code == SET and op.args[0][0] == "op"]
        self.assertEqual(sets, [(2, alagorn._picture("Shadowseeker")), (3, alagorn._picture("Greenbright")),
                                (4, alagorn._picture("Flame Blade")),
                                (2, alagorn._picture("Kreenfang")), (3, alagorn._picture("Gutterknot")),
                                (4, alagorn._picture("Deepbiter")), (5, alagorn._picture("Windlash"))])
        lines = " ".join(gpl.strings(added))
        for name in ("Greenbright!", "A Flame Blade!", "Gutterknot!", "Deepbiter!", "Windlash!"):
            self.assertIn(name, lines)
        self.assertIn([0, 1, 2, 3, 4, 5], [alagorn._locals(op.args[0]) for op in added if op.code == TEST])

    def test_switches(self):
        """Only the switches' items; none, no change."""
        self.assertEqual([[i for i, _ in k.items] for k in alagorn.kinds(arms=False, magic=True)],
                         [["Greenbright", "Flame Blade"], ["Gutterknot", "Deepbiter", "Windlash"]])
        self.assertEqual(alagorn.kinds(arms=False, magic=False), ())
        self.assertEqual(alagorn.script_chunks({("GPL ", alagorn.SCRIPT): self.script}, FIELDS, False, False), {})

    def test_armour_and_clothes(self):
        """Script 212's armour and clothes: the Warden's Plate's four pieces and the Cloak and Boots
        of Elvenkind, their locals past the loop's own (6 there), and its test for none carried in
        two."""
        kinds = alagorn.kinds(script=alagorn.OTHER_SCRIPT)
        script = alagorns(last="Nothing", kinds=kinds, done=6, split=True)
        self.assertTrue(alagorn._nothing({"text": ("str", "Nothing")}))  # (script 212's, unindented)
        out = alagorn.with_items(script, FIELDS, kinds)
        r = gpl._Reader(out, FIELDS)
        r.i = len(script)
        added = []
        while r.i < len(out):
            added.append(gpl._op(r))
        menus = [[x["text"][1] for x in op.args[0]["replies"]] for op in added if op.code == MENU]
        self.assertEqual(menus, [["  Tanelyv's Armor", "  Warden's Helm", "  Warden's Arms", "  Warden's Legs",
                                  "  Warden's Chest", "  Nothing"],
                                 ["  Belt of Might", "  Cloak of Elvenkind", "  Boots of Elvenkind", "  Nothing"]])
        sets = [alagorn._sets(op) for op in added if op.code == SET and op.args[0][0] == "op"]
        self.assertEqual([n for n, _ in sets], [2, 3, 4, 5, 2, 3])
        self.assertIn([0, 1, 2, 3, 4, 5], [alagorn._locals(op.args[0]) for op in added if op.code == TEST])
        flags = [op.args for op in added if op.code == SET and op.args[0] == ("n", 1)]
        self.assertTrue(flags and all(f == [("n", 1), ("var", 14, 6)] for f in flags))
        lines = " ".join(gpl.strings(added))
        for name in ("The Warden's Helm!", "The Warden's Chest!", "A Cloak of Elvenkind!", "Boots of Elvenkind!"):
            self.assertIn(name, lines)

    def test_past_the_loops_local(self):
        """The new items' locals skip the loop's own."""
        kinds = alagorn.kinds(script=alagorn.OTHER_SCRIPT)
        script = alagorns(last="Nothing", kinds=kinds, done=4)
        out = alagorn.with_items(script, FIELDS, kinds)
        r = gpl._Reader(out, FIELDS)
        r.i = len(script)
        added = []
        while r.i < len(out):
            added.append(gpl._op(r))
        sets = [alagorn._sets(op)[0] for op in added if op.code == SET and op.args[0][0] == "op"]
        self.assertEqual(sets, [2, 3, 5, 6, 2, 3])

    def test_other_script_unchanged(self):
        other = _Script()
        other.op(0x4F, ("n", 115), ("str", "Hello. "))
        script = other.bytes(end=False)
        self.assertEqual(alagorn.with_items(script, FIELDS), script)
        self.assertEqual(alagorn.script_chunks({("GPL ", 1): script}, FIELDS), {})


if __name__ == "__main__":
    unittest.main()
