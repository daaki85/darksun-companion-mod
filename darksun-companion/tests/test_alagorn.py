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


def alagorns():
    """Two kinds, each of two items: (part, menu, stories), the game's way."""
    s = _Script()
    for k, kind in enumerate(alagorn.KINDS):
        first = kind.first_reply.strip()
        s.op(SET, query(-30000 - 2 * k), ("var", 14, 0))
        s.op(SET, query(-30001 - 2 * k), ("var", 14, 1))
        s.op(TEST, zero(0, 1))
        s.op(IF_NOT, ("label", f"has {k}"))
        s.op(0x4F, ("n", 115), ("str", kind.none_text))
        s.op(BACK)
        s.label(f"has {k}")
        s.op(END_IF)
        s.op(0x4F, ("n", 115), ("str", "Let me see. "))
        s.label(f"loop {k}")
        s.op(TEST, ("expr", ["(", ("var", 0x8E, alagorn.DONE), "==", ("n", 0), ")"]))
        s.op(0x63, ("label", f"out {k}"))
        s.op(MENU, {"before": [], "title": ("str", "What item do you show him?"), "replies": [
            {"text": ("str", f"  {name}"), "goto": ("label", f"story {k} {i}"), "if": ("var", 0x8E, i),
             "before": [], "after": []} for i, name in enumerate((first, "Other"))]})
        s.op(GOTO, ("label", f"loop {k}"))
        s.label(f"out {k}")
        s.op(BACK)
    for k in range(len(alagorn.KINDS)):
        for i in range(2):
            s.label(f"story {k} {i}")
            s.op(0x4F, ("n", 115), ("str", f"Story {k} {i}. "))
            s.op(SET, ("n", 0), ("var", 14, i))
            s.op(TEST, zero(1 - i))
            s.op(IF_NOT, ("label", f"end {k} {i}"))
            s.op(SET, ("n", 1), ("var", 14, alagorn.DONE))
            s.label(f"end {k} {i}")
            s.op(END_IF)
            s.op(RETURN)
    return s.bytes(end=False)


class AlagornTests(unittest.TestCase):
    def setUp(self):
        self.script = alagorns()
        self.out = alagorn.with_items(self.script, FIELDS)
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
        self.assertIn("Shadowseeker! A blade of true metal", lines)
        self.assertIn("Kreenfang!", lines)

    def test_once(self):
        self.assertEqual(alagorn.with_items(self.out, FIELDS), self.out)

    def test_other_script_unchanged(self):
        other = _Script()
        other.op(0x4F, ("n", 115), ("str", "Hello. "))
        script = other.bytes(end=False)
        self.assertEqual(alagorn.with_items(script, FIELDS), script)
        self.assertEqual(alagorn.script_chunks({("GPL ", 1): script}, FIELDS), {})


if __name__ == "__main__":
    unittest.main()
