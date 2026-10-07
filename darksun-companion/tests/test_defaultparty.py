"""The game's own party made ready for the rule changes (defaultparty.py)."""

import os
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dscompanion import defaultparty as dp, game, specialize


def sheet(race, classes):
    s = bytearray(game.SHEET_SIZE)
    s[game.SHEET_RACE] = race
    s[game.SHEET_CLASSES:game.SHEET_CLASSES + 3] = bytes(classes)
    return bytes(s)


class FakeGame:
    def __init__(self, party):
        self.party = party  # [(name, sheet)]

    def creature_name(self, member):
        return self.party[member][0] if member < len(self.party) else ""

    def sheet(self, member):
        return self.party[member][1] if member < len(self.party) else b""


DEFAULT = [(name, sheet(m.race, m.classes)) for name, m in dp.PARTY.items()]


class DefaultPartyTests(unittest.TestCase):
    def test_known_by_name_race_and_classes(self):
        gd = FakeGame(DEFAULT + [("Gerakis", sheet(1, (10, 0, 0)))])  # (a human of that name)
        self.assertEqual([dp.who(gd, m) for m in range(5)], list(dp.PARTY) + [""])

    def test_kinds(self):
        """Each one past the kind's number, as the creation panel keeps them."""
        kinds = specialize.KINDS
        self.assertEqual(dp.kinds_bytes(dp.PARTY["Gerakis"]),
                         bytes((kinds.index("long sword") + 1, kinds.index("gythka") + 1, 0, 0)))
        self.assertEqual(dp.kinds_bytes(dp.PARTY["K'ratchek"]), bytes((kinds.index("chatkcha") + 1, 0, 0, 0)))
        self.assertEqual(dp.kinds_bytes(dp.PARTY["Cermak"]),
                         bytes((kinds.index("long sword") + 1, kinds.index("axe") + 1, 0, 0)))
        self.assertEqual(dp.kinds_bytes(dp.PARTY["Cilla"]), bytes(4))

    def ready(self, rules, done=None, new=True):
        calls = []
        stub = lambda key: (lambda gd, member, name: calls.append((name, key)) or [f"{name} {key}"])
        with mock.patch("dscompanion.tools.new_game", return_value=new), \
                mock.patch.object(dp, "set_kinds", stub("kinds")), \
                mock.patch.object(dp, "club_to_gythka", stub("gythka")), \
                mock.patch.object(dp, "take_armour", stub("armour")), \
                mock.patch.object(dp, "learn", stub("armor spell")):
            lines = dp.ready(FakeGame(DEFAULT), rules, set() if done is None else done)
        return calls, lines

    def test_by_the_rules(self):
        everything = game.RULE_SPECIALIZE | game.RULE_HALF_GIANT | game.RULE_RESTRICT
        calls, _ = self.ready(everything)
        self.assertEqual(calls, [("Gerakis", "kinds"), ("Gerakis", "gythka"), ("K'ratchek", "kinds"),
                                 ("Cermak", "kinds"), ("Cilla", "kinds"), ("Cilla", "armour"), ("Cilla", "armor spell")])
        calls, _ = self.ready(game.RULE_SPECIALIZE)  # (no gythka without the half-giants' rule)
        self.assertNotIn(("Gerakis", "gythka"), calls)
        calls, _ = self.ready(game.RULE_RESTRICT)
        self.assertEqual(calls, [("Cilla", "armour"), ("Cilla", "armor spell")])

    def test_once_and_only_while_new(self):
        done = set()
        self.assertTrue(self.ready(game.RULE_RESTRICT, done)[0])
        self.assertEqual(self.ready(game.RULE_RESTRICT, done)[0], [])
        self.assertEqual(self.ready(game.RULE_RESTRICT, new=False)[0], [])


class SpellZeroTests(unittest.TestCase):
    def test_armor_is_a_spell(self):
        """Spell 0 (Armor) is one of the game's: named, levelled and listed."""
        self.assertEqual(game.SPELL_FIRST, 0)
        self.assertEqual(dp.KNOWN_STRIDE, 138)


if __name__ == "__main__":
    unittest.main()
