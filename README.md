# Obsidian Edition

Obsidian Edition is a mod for **Dark Sun: Shattered Lands** (the GOG release)
in DOSBox, with its own companion window, **Templar's Ledger**, beside the
game. (Up to its 1.2.0 release, the whole mod was called Templar's Ledger.)

## Contents

- [What it does](#what-it-does)
- [Getting started](#getting-started)
- [What's new](#whats-new)
- [Changelog](CHANGELOG.md)
- [The player's guide](darksun-companion/GUIDE.md): the rules and tables, without spoilers
- [The full documentation](darksun-companion/README.md): everything in detail

## What it does

It shows what the game keeps hidden. Every roll is logged as it happens:
attacks, damage, saving throws, thief skills, initiative, even the dice at
character creation. Each comes with what it needed and where every bonus came
from ([the dice log](darksun-companion/README.md#the-dice-log)). The game's own
screens gain THAC0, saves, thief skills and spell slots, and the Look box tells
you what can hurt a monster ([In the
game](darksun-companion/README.md#in-the-game)).

It brings the rules closer to AD&D: weapon specialization and mastery, kits
(three for each class), class restrictions, INT's limits on learning spells,
thief skills from the Player's Handbook, saving throws as the books have them,
and levels up to 10 ([Rule
changes](darksun-companion/README.md#rule-changes)). Thieves can hide in
shadows to backstab, and pick pockets
([Picking pockets](darksun-companion/README.md#picking-pockets)).

It adds to Athas: new weapons in every material, magic items with stories of
their own, Kalzith (a defiler who sells scrolls), more of Semyon's story, and a
use for the cooked vulture ([New
content](darksun-companion/README.md#new-content)). Graphical additions show the
weapons and armour the party wears, have characters cast shadows, and kick up
dirt as they walk ([On the screen](darksun-companion/README.md#on-the-screen)).

Quality of life changes: choosing an enemy with Tab and attacking it with Enter,
scrolling the map with the mouse wheel
([Controls](darksun-companion/README.md#controls)), 40 saves and 29 saved
characters ([More saves and
characters](darksun-companion/README.md#more-saves-and-characters)), a game
speed setting ([Game speed](darksun-companion/README.md#game-speed)), crash
reports, and no dragon asking for a word from the manual, the game's copy
protection ([No manual check](darksun-companion/README.md#no-manual-check)).

The game's own files are never modified: the Ledger runs a patched copy of the
game, and copies of its data files, from its own folder. Play writes to the game
folder only what you'd expect: your saves (pages 2 to 4 as files of their own,
`SAVB`, `SAVC` and `SAVD`) and your characters (20 to 29 in the game's own
`CHARSAVE.GFF`).

## Getting started

1. Download the latest release from the
   [Releases page](https://github.com/daaki85/darksun-obsidian-edition/releases)
   (`Obsidian-Edition-<version>.zip`; `Templars-Ledger-<version>.zip` up to
   1.2.0) and unzip it anywhere. (Or this repository as it stands: **Code →
   Download ZIP**.)
2. In the unzipped folder (`Obsidian-Edition-<version>`, or `darksun-companion`
   in a download of the repository), double-click **`Start Obsidian Edition.bat`**
   (`Start Templar's Ledger.bat` up to 1.2.0).
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

**Templar's Ledger 1.2.0**, the mod's last release under that name, is out ([release notes](release-notes/v1.2.0.md)):
weapon specialization and class restrictions, new weapons and magic items
across Athas, and more, from pull requests #19 to #29.

**Since 1.2.0** (in the repository, not yet in a release): kits, three for
each class, and up to three for a human who changes class; preservers' INT
(the chance to learn a scroll's spell, and the most spells of each level);
rangers' casting level; the off hand's one attack a round with two weapons;
the charges left in a wand's item box; and [a spoiler-free player's
guide](darksun-companion/GUIDE.md).

Earlier changes, pull request by pull request, are in
[`CHANGELOG.md`](CHANGELOG.md). Releases have notes of their own:
[1.2.0](release-notes/v1.2.0.md) (pull requests #19 to #29),
[1.1.0](release-notes/v1.1.0.md) (#14 to #18) and
[1.0.0](release-notes/v1.0.0.md) (#1 to #13).
