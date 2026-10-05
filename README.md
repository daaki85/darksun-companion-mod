# Templar's Ledger: a companion and mod for Dark Sun: Shattered Lands

Templar's Ledger runs next to **Dark Sun: Shattered Lands** (the GOG release, in
DOSBox) and shows what the game keeps to itself: every roll it makes, what each
roll was compared against, and where every bonus comes from. It also adds to the
game itself, in the game's own lettering and windows. Nearly everything it adds
can be switched off on its Options tab.

## Contents

- [What it does](#what-it-does)
  - [In the Ledger's window](#in-the-ledgers-window)
  - [In the game](#in-the-game)
  - [Rule changes](#rule-changes)
  - [New content](#new-content)
  - [On the screen](#on-the-screen)
  - [Controls](#controls)
  - [Smoother play, and help when something goes wrong](#smoother-play-and-help-when-something-goes-wrong)
- [Getting started](#getting-started)
- [What's new](#whats-new)
- [Changelog](CHANGELOG.md)
- [The full guide](darksun-companion/README.md)

## What it does

### In the Ledger's window

- **The rolls behind the scenes:** attacks, damage, saving throws, magic
  resistance, initiative, thief skills, character creation and level-up HP, with
  each bonus named.
- **A party viewer:** THAC0 with each weapon, saves as they stand now, AC and
  what makes it up, spell slots, thief skills, equipment and active effects.
- **Dialogue and spells tabs:** a scrollable record of every conversation, and
  what each spell and psionic power really does, from the game's own records.

(More in [In the Ledger's window](darksun-companion/README.md#the-ledgers-window).)

### In the game

- **In the game:**
  - THAC0, saves, thief skills and DEX adjustments on the inventory screen,
    THAC0 and saves on View Character;
  - spell slots on the USE screen;
  - each turn's rolls in a pop-up during fights, if you tick it (three levels
    of detail);
  - what hurts a monster in the Look box;
  - a party member's spell no longer ended by a click on the Effects screen.

(More in [In the game](darksun-companion/README.md#in-the-game).)

### Rule changes

- **Optional AD&D rule changes**, all on by default and each one switchable:
  - helms give AC;
  - boots give an extra move in a fight ("Boots (Speed+1)");
  - two-weapon penalties;
  - spells saved against with the spell save;
  - DEX on saves against fire, cold and electricity instead of a doubled d20;
  - a new spell, Cat's Grace;
  - thieves hiding in shadows and moving silently to backstab, and rangers
    to attack from behind (a cloak and boots help, and say so in their item
    boxes);
  - a worn belt helping a thief pick pockets and open locks;
  - thief skills from AD&D's table, with Dark Sun's race and DEX adjustments;
  - half-giants wielding two-handed weapons in one hand;
  - class levels up to 10 (the game stops at 9).

(More in [Rule changes](darksun-companion/README.md#rule-changes).)

### New content

- **New items and thief play:** a Ring of Protection +1 to find in the arena
  (and 50 XP for finding it);
  gear for Kurzak, Legcrusher and Pehtucl in the slave pens (a short sword
  and a Cloak of Protection among it), with icons of their own; the rest of
  the bone scale armour, with a Bone Helm, where its chest piece lies; Thieves'
  Tools for every thief;
  picking anyone's pockets; and no more thief skill penalty for what a thief
  holds.
- **Two named magic weapons:** the Bone Gythka on the dead body in the arena
  becomes **Kreenfang** (+1), and Kurzak's short sword **Shadowseeker** (+1),
  whose wielder sees the invisible; lifting it from Kurzak is worth 200 XP,
  and Alagorn, the Painted Badlands' wizard who identifies magic items, tells
  the story of each.
- **A mini-quest:** the cooked vulture, at last good for something (Dinos
  cooks it for the party, to the game's own quest-done sound).
- **A new person in the slave pens:** Kalzith, a defiler slave who, treated
  with respect, sells arcane spell scrolls that a preserver can learn from.
- **Semyon kept his word:** after he leaves the arena through the entrance to
  the pens, he is in the pens to talk to, as the game promised and never did;
  and if he is still beside the party when they break out with Scar, he breaks
  out with them.

(More in [New content](darksun-companion/README.md#new-content).)

### On the screen

- **What the party wears, on the map:** weapons, shields, bows, armour, helms,
  cloaks, boots and belts on their figures, walking and fighting, changing as
  their gear does.
- **Shadows under every figure:** see-through, cast toward the lower right as
  the walls' are, in the floor's own colours, with the walls and figures in
  front standing on them.
- **Dust** raised behind the feet of anyone walking on sand or dirt.

(More in [On the screen](darksun-companion/README.md#on-the-screen).)

### Controls

- **Scrolling the map with the mouse:** press the wheel and drag the map, or
  turn the wheel.
- **Choosing an enemy with Tab:** in a fight Tab chooses an enemy, marked by a
  red ring (or rings under all of them, or none: an option), and Enter attacks
  it even behind someone.

(More in [Controls](darksun-companion/README.md#controls).)

### Smoother play, and help when something goes wrong

- **More saves:** 40 instead of the game's 10, on four pages of the save and
  load window (PAGE 1 to PAGE 4 buttons, or PgUp and PgDn).
- **More characters:** 29 saved characters instead of the game's 19, and
  DELETE in the roster deletes the one chosen even with the list scrolled.
- **Game speed:** DOSBox is given more of the computer (20,000 cycles by
  default, on its faster dynamic core), for smoother walking with the whole
  party in view; GOG's own speed and a faster one can be chosen. At the
  fastest (35,000), the whole party walks as fast as the leader alone.
- **Crash reports:** if DOSBox crashes or the game stops with an error, the
  game's message stays on screen and what happened is saved in a file to send.

(More in [More saves](darksun-companion/README.md#more-saves), [More characters](darksun-companion/README.md#more-characters), [Game speed](darksun-companion/README.md#game-speed) and [Crash reports](darksun-companion/README.md#crash-reports).)

The game folder is never modified, and your save files only keep what you'd
expect from play: the items the Ledger hands out, the XP it gives. For the dice
log, the launcher runs a patched copy of the game that it keeps in its own
folder.

**Everything else is in [`darksun-companion/README.md`](darksun-companion/README.md):**
requirements, how to start it on Windows, every log line explained, each
addition in detail, and how it works.

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

In [pull request #17](https://github.com/daaki85/darksun-companion-mod/pull/17)
(in review):
- **Kreenfang and Shadowseeker:** two named magic weapons, Shadowseeker
  letting its wielder see the invisible; 200 XP for lifting it from Kurzak;
  Alagorn tells of both.
- **Cloaks, boots and belts:** their item boxes say what they give a thief,
  a worn belt helps pick pockets and open locks, and plain ones cost 24.
- **Faster walking:** shadows and dust drawn much more cheaply; at the fastest
  game speed, the whole party walks as fast as the leader alone.
- **More saves:** 40, on four pages of the save and load window.
- **More characters:** 29 saved characters instead of 19.
- **Options tab:** its sections open and close.
- **The Look box:** a monster's alignment, and its magic resistance beside its
  level.

In [pull request #16](https://github.com/daaki85/darksun-companion-mod/pull/16)
(merged): Semyon breaks out with Scar, the game speed setting, switches for
all the new content, crash reports, a crash in the opening fight fixed, and
fixes from a review of the code.

Everything that changed, pull request by pull request, is in
[`CHANGELOG.md`](CHANGELOG.md). Release **1.0.0** is pull requests #1 to #13;
its notes are in [`release-notes/v1.0.0.md`](release-notes/v1.0.0.md).
