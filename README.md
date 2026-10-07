# Templar's Ledger: a companion and mod for Dark Sun: Shattered Lands

Templar's Ledger runs next to **Dark Sun: Shattered Lands** (the GOG release, in
DOSBox) and shows what the game keeps to itself: every roll it makes, what each
roll was compared against, and where every bonus comes from. It also adds to the
game itself, in the game's own lettering and windows. Nearly everything it adds
can be switched off on its Options tab.

## Contents

- [What it does](#what-it-does)
- [Getting started](#getting-started)
- [What's new](#whats-new)
- [Changelog](CHANGELOG.md)
- [The full guide](darksun-companion/README.md)

## What it does

- **Shows what the game hides.** A window beside the game shows the party as
  they stand: THAC0 with each weapon, saves, AC and what makes it up, spell
  slots and thief skills. A dice log lists every roll, what it needed and where
  each bonus came from. Tabs keep every conversation and what each spell really
  does. ([The Ledger's window](darksun-companion/README.md#the-ledgers-window),
  [the dice log](darksun-companion/README.md#the-dice-log))
- **Shows it in the game too**, in the game's own lettering: THAC0, saves and
  thief skills on the character screens, spell slots on the USE screen, each
  turn's rolls in a fight, and what hurts a monster in the Look box.
  ([In the game](darksun-companion/README.md#in-the-game))
- **Changes rules, each one switchable:** fifteen of AD&D's, among them weapon
  specialization, class restrictions, thief skills from AD&D's table, saving
  throws and levels up to 10.
  ([Rule changes](darksun-companion/README.md#rule-changes))
- **Adds to the game:** new weapons, armour and magic items across Athas, with
  stories Alagorn tells; Kalzith, a defiler slave who sells scrolls; Semyon
  keeping his word; picking pockets; a use for the cooked vulture.
  ([New content](darksun-companion/README.md#new-content))
- **On the screen and at hand:** the party's gear drawn on their figures,
  shadows and dust on the map, choosing an enemy with Tab, and scrolling with
  the mouse. ([On the screen](darksun-companion/README.md#on-the-screen),
  [Controls](darksun-companion/README.md#controls))
- **Smoother play:** 40 saves and 29 saved characters, a game speed setting,
  no manual check, two of the game's bugs fixed, and crash reports.
  ([More saves and characters](darksun-companion/README.md#more-saves-and-characters),
  [Game speed](darksun-companion/README.md#game-speed))

The game's own files are never modified: the Ledger runs a patched copy of the
game, and copies of its data files, from its own folder. Play writes to the game
folder only what you'd expect: your saves (pages 2 to 4 as files of their own,
`SAVB`, `SAVC` and `SAVD`) and your characters (20 to 29 in the game's own
`CHARSAVE.GFF`).

## Getting started

1. Download the latest release from the
   [Releases page](https://github.com/daaki85/darksun-companion-mod/releases)
   (`Templars-Ledger-<version>.zip`) and unzip it anywhere. (Or this repository
   as it stands: **Code → Download ZIP**.)
2. In the `darksun-companion` folder, double-click **`Start Templar's Ledger.bat`**.
   The first time, it offers to install 64-bit Python if you don't have it.
   If Windows shows "Open File - Security Warning" (it does for any `.bat`
   from a download), press **Run**: the Ledger then unblocks its own files, so
   it asks only that once. (Or, before unzipping, tick **Unblock** in the zip's
   Properties.)
3. On the Ledger's **Options** tab, pick the rule changes and additions you
   want (they're remembered).
4. Press **Start the game** at the top left. The game starts with your options,
   and the Ledger follows it.

(`Start Game with Dice Log.bat` starts the game and the Ledger together in one
double-click, with the options as last set.)

## What's new

In [pull request #21](https://github.com/daaki85/darksun-companion-mod/pull/21)
(in review):
- **No manual check:** the dragon's question, the game's copy protection, is
  gone; the game goes on as if it had been answered.
- **New magic items:** the **Warden's Plate**, plate mail +1 in four pieces
  across the world; the **Cloak and Boots of Elvenkind** for thieves and
  rangers, the cloak given by the Elven Leader with his Gythka +1; and the
  **Flame Blade**, an obsidian long sword +1 for fire clerics.
- **The Tome of Understanding:** Father Garyn's gift for the ranike pith; read
  like a scroll, it gives a point of Wisdom for good.
- **Alagorn knows every new magic item,** with a story for each kind, the tome
  among them; Legcrusher's leather is now **Inixhide**.
- **Every new item is in the game's own data,** so a new game makes them where
  they belong.
- **The game's own party is ready for the rule changes** when you press START
  GAME: weapon kinds to match their weapons, a bone gythka for Gerakis, and
  Armor in place of leather armour for Cilla, a druid.
- **Arrowbane** and the **Sunking Crown,** worn on the head and not armour;
  Grey's Scale's arm and leg armour AC 3; bracers of defense give nothing with
  a helm on.

Earlier changes, pull request by pull request, are in
[`CHANGELOG.md`](CHANGELOG.md). Releases have notes of their own:
[1.1.0](release-notes/v1.1.0.md) (pull requests #14 to #18) and
[1.0.0](release-notes/v1.0.0.md) (#1 to #13).
