import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dscompanion import game, kitpages, weaponpages  # noqa: E402


class KitPageTests(unittest.TestCase):
    def test_ids_clear(self):
        """The kit pages' buttons come after the weapon pages' and the level-up window's rows (to
        86Fh), and their windows are none of the game's (3000-3013, 3020, 3024) nor the weapon
        pages' (3014-3019, 3021)."""
        buttons = [kitpages.KIT_ROW + i for i in range(24)] + [kitpages.KIT_NONE, kitpages.KIT_VIEW]
        self.assertEqual(len(set(buttons)), 26)
        self.assertTrue(all(0x870 <= b < 0xBB8 for b in buttons))
        windows = [kitpages.KIT_DISCIPLINES, kitpages.KIT_SPHERES, kitpages.KIT_LAST_PAGE] \
            + [kitpages.KIT_WINDOW + c for c in range(8)]
        taken = set(range(3000, 3014)) | {3020, 3024, weaponpages.PICKER, weaponpages.WARRIOR_DISCIPLINES,
                                          weaponpages.WARRIOR_SPHERES} | set(weaponpages.PAGES)
        self.assertEqual(len(set(windows)), 11)
        self.assertFalse(taken & set(windows))

    def test_rows(self):
        self.assertEqual(sorted(kitpages.KITS), list(game.CREATION_CLASS_NAMES))
        self.assertEqual(kitpages.KITS[4], ("Arena Champion", "Twin-blade", "Brute"))
        texts = [kitpages.row_text(n) for names in kitpages.KITS.values() for n in names]
        self.assertEqual(len(texts), 24)
        self.assertIn("CHAMPION", texts)
        self.assertIn("M-WARRIOR", texts)
        self.assertTrue(all(len(t) <= 11 for t in texts))

    def test_kit_name(self):
        sheet = bytearray(game.SHEET_SIZE)
        sheet[0x21], sheet[kitpages.KIT_BYTE] = 10, 1  # a gladiator
        self.assertEqual(kitpages.kit_name(bytes(sheet)), "Arena Champion")
        sheet[0x21] = 15  # a fire ranger
        self.assertEqual(kitpages.kit_name(bytes(sheet)), "Stalker")
        sheet[0x22] = 12  # and a psionicist: no kit
        self.assertIsNone(kitpages.kit_name(bytes(sheet)))
        sheet[0x22], sheet[kitpages.KIT_BYTE] = 0, 0
        self.assertIsNone(kitpages.kit_name(bytes(sheet)))

    def test_panel_windows(self):
        both = game.RULE_SPECIALIZE | game.RULE_KITS
        self.assertEqual(kitpages.SPECIALIZE, game.RULE_SPECIALIZE)
        self.assertEqual(kitpages.KITS_ON, game.RULE_KITS)
        self.assertEqual(kitpages.panel_windows((8, 0, 0), both), (3022, 3023))
        self.assertEqual(kitpages.panel_windows((3, 0, 0), both), (3018, 3019))  # (KITS on the last page)
        self.assertEqual(kitpages.panel_windows((3, 0, 0), game.RULE_KITS), (3022, 3023))
        self.assertEqual(kitpages.panel_windows((1, 0, 0), both), (3012, 3023))
        self.assertEqual(kitpages.panel_windows((7, 0, 0), both), (3012, 3019))
        self.assertEqual(kitpages.panel_windows((8, 6, 0), both), (3012, 3013))


if __name__ == "__main__":
    unittest.main()
