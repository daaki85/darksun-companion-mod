# Templar's Ledger: the player's guide

A guide to **Dark Sun: Shattered Lands** as it plays with Templar's Ledger,
laid out like the game's own rule book: playing, making a party, the races and
classes, fighting, magic, psionics, equipment and levels, then the tables.

It is **spoiler-free**. It names no places past the opening arena, no people,
no quests, and no item by name or by where it is found. What it does give is
the rules: the game's own, as its code really works them (where that differs
from the manual, this guide follows the game and says so), and the mod's
changes to them.

Every rule change below has a switch on the Ledger's **Options** tab, and all
are on by default. Untick one and the game's own rule is back. The
[README](README.md) has the same rules in full detail, with how the Ledger
shows them; this guide is the short way through.

## Contents

- [Getting started](#getting-started)
- [Playing the game](#playing-the-game)
  - [The mouse and the map](#the-mouse-and-the-map)
  - [Keys](#keys)
  - [Resting, saving and characters](#resting-saving-and-characters)
  - [What the Ledger adds to the game's screens](#what-the-ledger-adds-to-the-games-screens)
- [Making a party](#making-a-party)
  - [Ability scores](#ability-scores)
  - [Races](#races)
  - [Hit points](#hit-points)
  - [Alignment](#alignment)
  - [Multi-class and dual-class characters](#multi-class-and-dual-class-characters)
  - [Starting gear](#starting-gear)
- [The classes](#the-classes)
  - [Fighters, gladiators and rangers](#fighters-gladiators-and-rangers)
  - [Thieves](#thieves)
  - [Preservers](#preservers)
  - [Clerics and druids](#clerics-and-druids)
  - [Psionicists](#psionicists)
  - [Class restrictions](#class-restrictions)
- [Kits](#kits)
- [Weapon specialization](#weapon-specialization)
- [Fighting](#fighting)
  - [Initiative and turns](#initiative-and-turns)
  - [Hitting: THAC0 and AC](#hitting-thac0-and-ac)
  - [Two weapons](#two-weapons)
  - [From behind, and backstabs](#from-behind-and-backstabs)
  - [Hiding in shadows](#hiding-in-shadows)
  - [Saving throws](#saving-throws)
  - [Monsters](#monsters)
- [Magic](#magic)
  - [Spell slots](#spell-slots)
  - [Learning spells](#learning-spells)
  - [How spells work in this game](#how-spells-work-in-this-game)
  - [Effects](#effects)
- [Psionics](#psionics)
- [Equipment](#equipment)
  - [Weapons](#weapons)
  - [Armour, helms and boots](#armour-helms-and-boots)
  - [Protection, bracers and stealth gear](#protection-bracers-and-stealth-gear)
  - [Acid and breaking](#acid-and-breaking)
- [Experience and levels](#experience-and-levels)
- [Thief skills](#thief-skills)
- [The Options tab at a glance](#the-options-tab-at-a-glance)

## Getting started

1. Unzip the Ledger anywhere and double-click **`Start Templar's Ledger.bat`**
   (it offers to install Python the first time; see the
   [README](README.md#running-it-windows)).
2. Look over the **Options** tab ([at a glance](#the-options-tab-at-a-glance)
   below). Everything is on except each turn's rolls in the game, P in a
   conversation and right-button scrolling.
3. Press **Start the game**. The game opens beside the Ledger, whose dice log
   shows every roll as it happens.

Kits, weapon specialization and the class rules are chosen when a character is
made, so for a first game with the mod, make your own party rather than take
the four the game offers.

## Playing the game

### The mouse and the map

The pointer has three modes, changed with a right-click: **Walk**, **Attack**
and **Look**. Left-click acts.

- **Walk** moves the party. In a fight, clicking an enemy walks up to it and
  attacks.
- **Attack** attacks the enemy clicked: hand to hand next to it, or with a
  readied missile weapon at a distance. The game picks which; ready both kinds.
- **Look** examines things. A box offers what can be done: **Talk**, **Use**,
  **Pick Up**. Look at a monster in a fight for what the Ledger adds (below);
  look at a party member for their character screen.
- **Scrolling:** move the pointer to the screen's edge, as in the game, or
  with the mod press the mouse wheel and drag; turning the wheel scrolls too
  (Shift for sideways).
- **Choosing an enemy without aiming:** on a party member's turn in a fight,
  **Tab** chooses the nearest enemy (Tab again for the next, Shift+Tab back)
  and **Enter** attacks it. A red ring marks it.
- Aim spells and icons with the icon's upper-left corner.

Only the leader walks the map unless you turn on the whole party (the Game
Menu's Collapse Party, or 5 and 6). Four walkers cost the game more drawing;
see **Game speed** on the Options tab if it slows.

### Keys

The game's own:

| Key | Does |
|---|---|
| A | animations on or off |
| C or U | Cast Spells / Use Psionics |
| E | Current Spell / Effects |
| G | Guard (in a fight) |
| H | centre on the leader |
| I | View Inventory |
| N, P | next or previous opponent (in a fight) |
| O | the overhead map |
| Q | end the character's turn (in a fight) |
| V | View Character |
| W | Wait (in a fight): act later in the round |
| Y, N | answer yes or no |
| 1 to 4 | make that character the leader; in a conversation, pick a reply (1 to 5) |
| 5, 6 | the whole party on the map, or the leader alone |
| Space | take a character off computer control (in a fight) |
| F1, F2, F3 | save, load, quit |
| F4, F5, F6 | music, sound effects, animations on or off |
| Esc | close menus (quits with none open) |
| Alt+X | quit |

The mod's: **Tab**, **Shift+Tab** and **Enter** in a fight (above), **PgUp**
and **PgDn** in the save and load window (four pages of saves), and **P** in a
conversation to pick a pocket (if switched on; see [Thieves](#thieves)).

### Resting, saving and characters

- **Resting** (Look at a fire ring) fills HP, PSP and spell slots, and casters
  cure the wounded first.
- **Saves:** 40, on four pages of ten. A game can't be saved during a fight.
- **Characters kept on disk:** 29 (the game kept 19). DELETE in the roster
  deletes the one you chose (the game's own bug deleted another when the list
  was scrolled).
- **Effects screen:** clicking a spell's icon there no longer ends the spell by
  accident. A psionic power's icon still ends the power, which is how you stop
  one.
- **No manual check:** the game's copy protection never comes.

### What the Ledger adds to the game's screens

- **Inventory screen:** THAC0 and all five saving throws; THAC0 with each
  weapon (`T14`); a thief's skills; DEX's reaction (`REAC`) and defensive
  (`DEF`) adjustments.
- **View Character:** THAC0 and saves; for a character of more than one class,
  which class goes up next (`EXP:87230 (90000 Pr)`).
- **USE screen:** spells left of each level and the most after resting
  (`WIZ 2/2`, `PRI 5/5 3/3`).
- **Look box in a fight:** the monster's HP, AC, THAC0, alignment, magic
  resistance and its chief defence (`NEEDS +1 WEAPON`, `NO CRUSH`...). Closing
  the box tells the rest.
- **Item boxes** (right-click an item): charges left in a wand or other charged
  item; a cloak's, boots' or belt's bonus to thief skills.
- **Each turn's rolls** in the game's own window (off unless you tick it).
- **The Effects screen** names a character's kits and weapon specs.

The Ledger's own window has the dice log (every roll, with what it needed and
where each bonus came from), the party's character sheets and the spells'
records.

## Making a party

On the main menu, **CREATE CHARACTERS**, then right-click an empty slot and
**NEW**. Click the portrait to choose race and sex, mark one to three classes,
choose a cleric's or ranger's sphere or a character's psionic discipline,
click the die to roll, and **DONE**. The mod adds two pages to the panel under
the classes: **WEAPON SPEC** for warriors (see
[Weapon specialization](#weapon-specialization)) and **KITS** (see
[Kits](#kits)).

A party has one to four characters; four is best. Your party must be good or
neutral.

### Ability scores

Each click of the die rolls a whole character. In the game's code:

- Each score is rolled **four times as 4d4 + 4**, and the best counts (8 to
  20), then the race's adjustment is added.
- A score below the classes' minimum is raised to it: **17 in the prime
  requisite**, otherwise **9** (clerics, fighters, preservers, thieves), **12**
  (druids, psionicists), **13** (gladiators) or **14** (rangers). A
  multi-class character takes the highest of its classes'.

| Class | Prime requisite |
|---|---|
| Fighter, gladiator | STR |
| Cleric, druid, psionicist, ranger | WIS |
| Preserver | INT |
| Thief | DEX |

(The manual's per-class minimums, such as a gladiator's DEX 12 and CON 15,
aren't what the game checks.) Scores go up to 25 with magic. The scores
matter so:

- **STR:** to-hit and damage in melee, and how much is carried.
- **DEX:** AC (−1 at 15, down to −6 at 24), to-hit with missiles, initiative,
  thief skills and, with the mod, dodging fire, cold and electricity.
- **CON:** hit points, saves against paralysis, poison and death; CON 20 or
  more regenerates a hit point now and then.
- **INT:** a preserver's spells (with the mod, how many it can know and its
  chance to learn one).
- **WIS:** a priest's bonus spells, and saves against mind-affecting magic.
- **CHA:** how some people take to the party.

### Races

The adjustments the game's code makes (the manual's half-giant is wrong):

| Race | STR | DEX | CON | INT | WIS | CHA | Notes |
|---|---|---|---|---|---|---|---|
| Human | | | | | | | one class at a time; can change class (dual-class) |
| Dwarf | +1 | −1 | +2 | | | −2 | good CON saves |
| Elf | | +2 | −2 | +1 | −1 | | |
| Half-elf | | +1 | −1 | | | | |
| Half-giant | +4 | −5 | +2 | −5 | −3 | −3 | double hit dice; with the mod, two-handed weapons in one hand |
| Halfling | −2 | +2 | −1 | | +2 | −1 | good CON saves |
| Mul | +2 | | +1 | −1 | | −2 | male only |
| Thri-kreen | | +2 | | −1 | +1 | −2 | female only; base AC 5, move 15; no armour, cloaks, belts, boots or rings |

Classes each race may take, as the manual gives them:

| Race | Fighter | Gladiator | Ranger | Preserver | Cleric | Druid | Thief | Psionicist |
|---|---|---|---|---|---|---|---|---|
| Human | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Dwarf | ✓ | ✓ | | | ✓ | | ✓ | ✓ |
| Elf | ✓ | ✓ | ✓ | ✓ | ✓ | | ✓ | ✓ |
| Half-elf | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Half-giant | ✓ | ✓ | ✓ | | ✓ | | | ✓ |
| Halfling | ✓ | ✓ | ✓ | | ✓ | ✓ | ✓ | ✓ |
| Mul | ✓ | ✓ | | | ✓ | | ✓ | ✓ |
| Thri-kreen | ✓ | ✓ | ✓ | | ✓ | ✓ | | ✓ |

The creation screen greys what a race can't take, and what can't go with the
classes already marked (a cleric and a druid together, for one).

### Hit points

Each class level rolls its die:

| Class | Hit die | After 9th level (with levels up to 10) |
|---|---|---|
| Fighter, gladiator, ranger | d10 | +3 |
| Cleric, druid | d8 | +2 |
| Psionicist | d6 | +2 |
| Thief | d6 | d6 (the mod's 10th-level roll) |
| Preserver | d4 | d4 |

- Half-giants roll double.
- A roll is never less than 2 with CON 20, 3 with CON 21-22, 4 with CON 23+.
- **CON's bonus**, for every level: a warrior's full bonus (+1 at CON 15, +2 at
  16, +3 at 17, +4 at 18, +5 at 19-20, +6 at 21-23, +7 at 24-25; −1 at 4-6),
  at most +2 for other classes.
- There is no automatic maximum at 1st level: it rolls like the rest.
- **Hit dice: the better of two** (mod): every hit die is rolled twice and the
  better kept, at creation and at each level.
- **Multiclass hit points** (mod): a multi-class character gets each class's
  die divided by the number of classes (at least 1), and CON's bonus shared
  too, as in AD&D. The game adds the dice and divides the total, and gives
  CON's bonus whole.
- Three [kits](#kits) have their own die (Battle Mage d6, Mind Warrior d8,
  Arcanist d3).

A character at 0 HP falls Out Cold; at −10, it dies.

### Alignment

Good or neutral for the party (no evil). It decides little in play, mostly
how some magic treats a character.

### Multi-class and dual-class characters

- **Multi-class** (any race but human): two or three classes at once. Each
  kill's XP is split between the classes, so each goes up slower. Hit points
  are divided between them.
- **Dual-class** (humans only): **DUAL** on a portrait's right-click menu, from
  2nd level, starts a new class at 1st level. The old class can't go up again,
  and what it gives (its hit points, THAC0, saves, weapon specs and kit) sleeps
  until the new class's level passes the old. A human can do this twice.
  With the mod, the new class can take a kit of its own (up to three kits).

### Starting gear

What the game gives each class when its first game starts (with the mod's
kits and weapon specs, it is changed to suit them; the dice log says how):

| Class | Starting gear |
|---|---|
| Fighter | bone long sword, shield, leather chest, arm and leg armour |
| Gladiator | bone long sword, club in the off hand, leather arm armour |
| Ranger | bone long sword, bow and arrows, leather chest and arm armour |
| Cleric | shield, leather chest and arm armour, a club in the backpack |
| Druid | club, sling |
| Preserver | quarterstaff, sling |
| Psionicist | club, bow and arrows, leather chest armour |
| Thief | bone long sword, sling, leather chest armour, and with the mod a set of Thieves' Tools |

A new preserver chooses its first spells on the game's CHOOSE A SPELL window
(two at 1st level) rather than being handed them.

## The classes

### Fighters, gladiators and rangers

The warriors: the best THAC0 (21 less the level) and hit dice, and any
armour or weapon.

- **Attacks:** the game gives every warrior 3/2 attacks a round in melee, 2
  from 7th level. With [weapon specialization](#weapon-specialization), that
  is only with a weapon of a chosen kind; others are at the plain rate, half
  an attack less.
- **Fighters** specialize, then master, a kind of weapon.
- **Gladiators** specialize in two kinds, then a third at 6th and a fourth at
  9th. They make the most of armour: AC 1 better at 5th level and 2 better at
  10th (the game gives it with or without armour).
- **Rangers** fight with two weapons at no penalty, get expertise with the bow
  and one other kind, hide and move silently with the stealth rule (best
  outdoors), and cast priest spells of their sphere from 8th level, as a
  priest of their level less 7.

### Thieves

- **Skills:** pick pockets, open locks, find/remove traps, move silently, hide
  in shadows, hear noise, climb walls and read languages. The game rolls them
  for locks, traps and so on in its scripts; its own chances run high, so with
  the mod (on by default) they come from AD&D's table, with Dark Sun's race and
  DEX adjustments: see [Thief skills](#thief-skills). A thief who isn't Okay,
  or is Blind, Afraid, Confused, Berserk or Paralyzed, can't use them.
- No equipment penalty on skills (in the mod's game), whatever the manual
  says of armour.
- **Backstab:** see [From behind, and backstabs](#from-behind-and-backstabs).
  With the stealth rule, a thief can hide and creep up to make one.
- **Picking pockets** (mod): every thief starts with **Thieves' Tools**. On
  the inventory screen pick them up, go back to the map with them on the
  pointer, and click someone in sight (not in a fight). Success lifts one small
  thing: something light that isn't worn on the body. Failure needs a move
  silently roll to get away unseen; fail both and that person keeps their
  hands on their pockets from then on. When there's nothing left worth taking,
  a few coins, and that's the last try on them. With **P in a conversation**
  switched on, the leader can try the person talked to with **P**.

### Preservers

Wizards who cast without harming the land. A d4 hit die, the worst THAC0, no
armour, few weapons, and the most powerful magic.

- A new spell is chosen at each level up (CHOOSE A SPELL), and more are learnt
  from scrolls: right-click a scroll in the inventory and click its icon.
- **Preservers' INT** (mod): INT limits learning, as in AD&D: see
  [Learning spells](#learning-spells).
- With [class restrictions](#class-restrictions), a multi-class preserver may
  wear what its other class allows, but casts nothing while wearing armour (a
  helm counts, a shield doesn't). Bracers and other non-armour protection are
  fine.

### Clerics and druids

Priests of an element: air, earth, fire or water.

- **Clerics:** a d8 hit die, any armour, but only their sphere's weapons:
  - air: missile weapons, thrown weapons and daggers;
  - earth: stone, obsidian, metal and wood;
  - fire: obsidian;
  - water: bone and wood.
- **Druids:** a d8 hit die, any weapon, no armour.
- Both know every spell of their spheres from the start, and get bonus slots
  for WIS (see [Spell slots](#spell-slots)). An elemental spell counts for a
  priest of that element only.

### Psionicists

Masters of the mind's powers: psychokinesis, psychometabolism and telepathy.
A d6 hit die, and with [class restrictions](#class-restrictions) light
armour only (leather and the like) and small weapons: daggers, short swords,
maces, clubs, chatkchas, bows and slings. A new power
comes with each level (two at odd levels and 4th).

Every character has one psionic discipline and works its powers at 1st level;
a psionicist has all three and uses its own level. See [Psionics](#psionics).

### Class restrictions

The game lets a character use an item if **any** of its classes may. With
**Class restrictions** (mod), **every** class must allow it, as in AD&D,
the strictest winning:

| Class | Armour and helms | Shields | Weapons |
|---|---|---|---|
| Psionicist, whatever its other classes | light only (leather, hide, silk) | leather only | daggers, short swords, maces, clubs, chatkchas, bows and slings |
| Thief, multi-class | light only | a leather one, if another class allows shields | as its classes allow |
| Preserver, one class | none | none | as the game has it |
| Druid | none | none | any |
| Cleric | any | any | its sphere's |

A multi-class preserver casts no spells in armour. A ranger's bow is always
its own. A human who changed class is held by its new class; once the old
class wakes, it may use the weapons it specialized in.

## Kits

With **Kits** (mod), a character takes one of three kits for its class when
it is made, or none. Each gives something and costs something. Choose it on
the creation panel's **KIT** page (the **KITS** button at the end of the
panel's pages).

| Kit | Gives | Costs |
|---|---|---|
| **Myrmidon** (fighter) | a second weapon spec at 1st level, on to mastery as the first | −4 on saves against charms |
| **Sentinel** (fighter) | AC 2 better with a shield; +2 initiative | −1 on saves against wizards' and priests' spells |
| **Ravager** (fighter) | +1 to hit and damage in melee; a base AC by level (7 at 1st and 2nd, 6 at 3rd and 4th, 5 at 5th and 6th, 4 at 7th and 8th, 3 at 9th and 10th), armour bettering it as usual | no missile or thrown weapons; no shield; leather armour or none |
| **Arena Champion** (gladiator) | with a shield: +1 to hit and damage in melee, and AC 1 better | −1 to hit in melee without a shield |
| **Twin-blade** (gladiator) | no penalty for two weapons | no shield; no two-handed weapon |
| **Brute** (gladiator) | +2 to hit and damage with a two-handed melee weapon | two-handed melee weapons only |
| **Stalker** (ranger) | +2 movement in a fight; +15 hide in shadows and move silently, and hiding not halved indoors | leather armour or none |
| **Seeker** (ranger) | priest spells from 6th level (on its own slot table), cast at its level less 5 | its sphere's weapon limits, as a cleric's (but it keeps the bow) |
| **Justifier** (ranger) | its expertise becomes specialization (+1 to hit, +2 damage) | one 1st-level priest slot from 10th level, in place of a ranger's spells |
| **Assassin** (thief) | hiding in shadows not halved in daylight | −15 pick pockets and open locks |
| **Swashbuckler** (thief) | a warrior's THAC0 | −10 to every thief skill |
| **Shinobi** (thief) | preserver spells from 6th level, from its own list of 14, cast at its thief level less 5, in light armour too | none learnt from scrolls; dagger, short sword, quarterstaff, chatkcha, sling, staff sling and bow only; light armour; no shield |
| **Arcanist** (preserver) | a spell slot more at each spell level it has; in a fight, two preserver spells in a turn | a d3 hit die |
| **Scholar** (preserver) | a spell more learnt at each level up | THAC0 1 worse |
| **Battle Mage** (preserver) | a warrior's THAC0; casts though hit earlier in the round; a d6 hit die; leather armour, cast in; expertise in one weapon kind (with weapon specialization) | one fewer spell slot at each spell level; nothing in the off hand |
| **Healer** (cleric) | Cure Light, Serious and Critical Wounds heal 1 more a die | no weapon in the off hand |
| **Crusader** (cleric) | a warrior's THAC0; a warrior's extra attacks in melee (3/2 a round from 7th level) | one fewer spell slot at each spell level |
| **Elementalist** (cleric) | a second sphere: its spells and its weapons | spell slots a level behind |
| **Grove Warden** (druid) | AC 1 better for every 3 druid levels | no metal weapons |
| **Wanderer** (druid) | +3 on saves against fire and cold | AC 1 worse |
| **Lifebinder** (druid) | Cure Wounds spells heal a d8 more, Blood Flow a d6 | blunt weapons only (club, mace, quarterstaff, sling, staff sling) |
| **Mind Warrior** (psionicist) | a warrior's THAC0; a warrior's extra attacks in melee (3/2 a round from 7th level); a d8 hit die | a tenth fewer PSP |
| **Mind Bender** (psionicist) | telepathy powers cost 2 PSP less | psychokinesis powers cost 2 PSP more |
| **Kineticist** (psionicist) | psychokinesis powers cost 2 PSP less | telepathy powers cost 2 PSP more |

- A **Myrmidon**, **Battle Mage** or **Elementalist** makes its extra choice
  after taking the kit: the weapon pages for the first two, a second sphere on
  the CLERICAL SPHERE list for the last.
- A kit belongs to its class. A human who changes class keeps it, asleep until
  the new class's level passes the old; the new class may take a kit too.
- Some kits rule out classes a human may change to, and some can't go
  together:

  | Kit | Can't become |
  |---|---|
  | Seeker, Justifier | cleric, druid |
  | Shinobi | preserver |
  | Swashbuckler, Crusader, Battle Mage, Mind Warrior | fighter, gladiator, ranger |
  | Arena Champion, Sentinel | druid, preserver |
  | Brute | psionicist, air cleric |

  | Kit | Can't go with |
  |---|---|
  | Arena Champion, Sentinel | Twin-blade, Shinobi, Ravager |
  | Twin-blade | Healer |
  | Brute | Shinobi, Lifebinder |

## Weapon specialization

With **Weapon specialization** (mod), warriors train in kinds of weapon, as
in AD&D. Choose them on the creation panel's **WEAPON SPEC** pages; later
picks come in a window at a level up.

| Who | Chooses | With a chosen kind |
|---|---|---|
| Fighter | 1 kind | specialized: +1 to hit, +2 damage; **mastery** from 5th level (+3 to hit, +3 damage); **grand mastery** from 9th (the same, the damage die a size larger and one more attack a round) |
| Gladiator | 2 kinds, a 3rd at 6th, a 4th at 9th | specialized in each: +1 to hit, +2 damage |
| Ranger | the bow from the start, and 1 kind | expertise: a specialist's attacks, no other bonus |

The sixteen kinds: long sword, club, dagger, short sword, mace, axe, great
axe, pick, quarterstaff, polearm, gythka, cahulaks, chatkcha, bow, sling,
staff sling. A multi-class warrior chooses only kinds its other classes let it
use. A new character starts with a plain weapon of its first kind.

**Attacks a round** (a warrior's level: its best fighter, gladiator or ranger
level):

| Skill with the weapon | Melee 1-6 | Melee 7-10 | Bow 1-6 | Bow 7-10 | Sling, staff sling, chatkcha 1-6 | 7-10 |
|---|---|---|---|---|---|---|
| a non-warrior | 1 | 1 | 2 | 2 | 1 | 1 |
| a warrior, not a chosen kind | 1 | 3/2 | 2 | 3 | 1 | 3/2 |
| expertise, specialized or mastery | 3/2 | 2 | 3 | 4 | 3/2 | 2 |
| grand mastery (9th level on) | | 3 | | 5 | | 3 |

3/2 means one attack one round, two the next.

## Fighting

### Initiative and turns

At the start of each round everyone's initiative is **20 + a 0-9 roll + DEX's
adjustment**, +2 Hasted, −2 Slowed, −2 Blind. Highest acts first. The weapon
makes no difference. **Wait** drops a character to 10 to act later.

| DEX | 1 | 2 | 3 | 4 | 5 | 6-15 | 16 | 17-18 | 19-20 | 21-23 | 24-25 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Initiative and reaction | −6 | −4 | −3 | −2 | −1 | 0 | +1 | +2 | +3 | +4 | +5 |

A character hit in a round can't cast a spell until the next (the Battle Mage
can).

### Hitting: THAC0 and AC

An attack hits when **d20 ≥ THAC0 − the target's AC**. A natural 20 always
hits and a 1 always misses, but **there are no critical hits**: a 20 does
normal damage. Lower AC is better. To-hit changes with:

- STR (melee) or DEX (missiles);
- the weapon's plus; plain weapons of other materials than metal are worse:
  **wood −3, stone and obsidian −2, bone −1**;
- Bless and Prayer +1, Curse −1, Slow −4;
- +2 from behind, +2 more for a backstab;
- the difficulty setting, for monsters.

Damage is the weapon's dice, its plus and STR's bonus (melee), at least 1.

### Two weapons

The manual says the second weapon is at a disadvantage unless the wielder is a
ranger or has high DEX. The game's code does the opposite of a penalty: a small
bonus at DEX 5 or less, nothing above. With **Two weapons** (mod), two melee
weapons ready mean, as in AD&D:

- **−2 to hit with the main (right) hand, −4 with the off (left) hand,** plus
  the DEX reaction adjustment (above), which can cancel the penalty but never
  make it a bonus: DEX 17 is 0 and −2, DEX 21 is 0 and 0.
- **Rangers** (and Twin-blades) have no penalty.
- **The off hand attacks once a round.** Extra attacks are the main hand's: a
  warrior at 3/2 attacks 3/2 + 1 a round (1 + 1, then 2 + 1).

A weapon and a shield, or a weapon and a bow or sling, aren't two weapons.

### From behind, and backstabs

- A creature turns to face the first attacker each round, and keeps facing
  that way. An attacker standing in the square directly behind it attacks
  **from behind**: +2 to hit, and the target loses its DEX bonus and shield.
- A **backstab** is a thief's attack from behind, in melee, with a weapon no
  heavier than a long sword (see [Weapons](#weapons)): +4 to hit in all, and
  the thief's first attack of the round does **×2** damage (levels 1-4), ×3
  (5-8) or ×4 (9-10), STR bonus included.

### Hiding in shadows

With **Thieves hide in shadows and move silently to backstab, rangers to
attack from behind** (mod): a thief or ranger whose turn comes with no enemy
in the eight squares around rolls to hide in shadows, then to move silently;
with both, their next attack that turn is from behind (a thief's a backstab
with a light enough weapon). Attacking, or ending the turn, gives them away.

- Thieves' hiding is **halved in daylight** (under the open sky); rangers' is
  halved indoors instead.
- A worn cloak adds 10 to hiding, worn boots 10 to moving silently, up to 95;
  a worn belt adds 5 to a thief's picking pockets and opening locks.

### Saving throws

A save succeeds when **d20 + modifiers ≥ the save's number**; a natural 1
always fails and a 20 always saves. Each character has five: paralysis,
poison and death (`PPD`), rod, staff and wand (`RSW`), petrification and
polymorph (`PP`), breath weapon (`BW`) and spell (`SP`).

What the game does that the manual doesn't say:

- **Almost every spell is saved against with petrification/polymorph**, never
  the spell save. With **Spells saved against with the spell save** (mod),
  the spell save is used, as in AD&D; poisons and death spells keep
  paralysis/poison/death.
- **Against fire, cold and electricity spells the d20 counts double,** so
  most Fireball victims save. With **Fire, cold and electricity: DEX instead
  of a doubled d20** (mod), the roll isn't doubled and DEX's defensive
  adjustment is added instead:

  | DEX | 1 | 2 | 3 | 4 | 5 | 6 | 7-14 | 15 | 16 | 17 | 18-20 | 21-23 | 24-25 |
  |---|---|---|---|---|---|---|---|---|---|---|---|---|---|
  | Dodging fire, cold, electricity | −5 | −5 | −4 | −3 | −2 | −1 | 0 | +1 | +2 | +3 | +4 | +5 | +6 |

Other modifiers:

| Modifier | Saves |
|---|---|
| WIS: −6 at 1, −4 at 2, −3 at 3, −2 at 4, −1 at 5-7, +1 at 15, +2 at 16, +3 at 17, +4 at 18+ | against mind-affecting spells, charms, holds, fear and illusions |
| CON: −2 at 1, −1 at 2, +1 at 19-20, +2 at 21-22, +3 at 23-24, +4 at 25; dwarves and halflings +1 for every 3.5 points of CON | paralysis/poison/death |
| Druids +2 | against fire and electricity |
| Psionicists +2 | against mind-affecting spells and charms |
| Bless +1, Barkskin +1, Spirit Armor +3 (not PPD), Prayer ±1 | all |
| Protection from Evil +2, from Fire and Cold +3, from Lightning +4 | against the matching caster or spell |
| +4 | against a one-target spell when the caster can't see you |

Some spells have rules of their own: creatures of 6th level or less can't save
against Cloudkill; only warriors save against Chaos; against Scare, 6th level
and up always save and others can't.

### Monsters

Every monster has defences of its own: some need magic weapons, some are hurt
only by edged weapons or immune to crushing ones, some shrug off fire, cold,
poison or the mind's powers, some can't be charmed or held. **Look** at one in
a fight and the box says its chief defence (`NEEDS +1 WEAPON`, `IMM FIRE
COLD`, `NO CRUSH`, `HALF FROM WPNS`, `UNDEAD`); close the box for the rest.
Undead take nothing from poison or draining, and mind-affecting spells don't
work on them. A monster's own hits count as magical by its level.

## Magic

### Spell slots

Casting uses one slot of the spell's level; resting fills them. The game's
own tables (they differ from the manual's):

| Level | 1st | 2nd | 3rd | 4th | 5th |
|---|---|---|---|---|---|
| 1 | 1 | | | | |
| 2 | 2 | | | | |
| 3 | 2 | 1 | | | |
| 4 | 2 | 2 | | | |
| 5 | 3 | 2 | 1 | | |
| 6 | 3 | 2 | 2 | | |
| 7 | 4 | 3 | 2 | 1 | |
| 8 | 4 | 3 | 2 | 2 | |
| 9 | 5 | 4 | 3 | 2 | 1 |
| 10 | 5 | 4 | 3 | 2 | 2 |

This is the same for preservers, clerics and druids. **Rangers** get one
1st-level slot at 8th level, two at 9th, and a 2nd-level slot at 10th. No
spell is higher than 5th level.

**Clerics and druids** add slots for WIS, but only at spell levels their class
level reaches:

| WIS | 1st | 2nd | 3rd | 4th | 5th |
|---|---|---|---|---|---|
| 13 | 1 | | | | |
| 14 | 2 | | | | |
| 15 | 2 | 1 | | | |
| 16 | 2 | 2 | | | |
| 17 | 3 | 2 | 1 | | |
| 18 | 3 | 2 | 2 | | |
| 19 | 3 | 3 | 2 | 1 | |
| 20 | 3 | 3 | 2 | 2 | |
| 21 | 3 | 3 | 3 | 2 | 1 |
| 22 | 3 | 3 | 3 | 2 | 2 |
| 23-24 | 3 | 3 | 3 | 3 | 2 |
| 25 | 3 | 3 | 3 | 3 | 3 |

A multi-class character's classes add up. Several [kits](#kits) have more or
fewer slots.

### Learning spells

Priests know every spell of their spheres. Preservers learn one at each level
up and more from scrolls. A scroll of a spell too high for the preserver's
level can't be learnt yet.

With **Preservers' INT** (mod), AD&D's table holds: reading a scroll rolls
d100 against the chance (a failed roll uses the scroll up), and a preserver
that knows the most spells of a level learns no more of it (the scroll is
kept). CHOOSE A SPELL at a level up leaves out levels already full.

| INT | Chance to learn | Most spells of each level |
|---|---|---|
| 9 | 35% | 6 |
| 10 | 40% | 7 |
| 11 | 45% | 7 |
| 12 | 50% | 7 |
| 13 | 55% | 9 |
| 14 | 60% | 9 |
| 15 | 65% | 11 |
| 16 | 70% | 11 |
| 17 | 75% | 14 |
| 18 | 85% | 18 |
| 19 | 95% | all |
| 20-23 | 96-99% | all |
| 24-25 | 100% | all |

### How spells work in this game

- **Damage** grows with the caster's level up to **10th**: Fireball and
  Lightning Bolt at most 10d6. A creature that is Out Cold gets no save and
  takes the most the dice can do.
- **Duration** is so much per caster level plus dice; a round is a minute of
  game time.
- **Caster level** is the caster's best level in a class whose sphere has the
  spell. A ranger casts as a priest of its level less 7; with **Rangers'
  casting level** (mod), its spells' damage and duration take that level too
  (the game used the whole ranger level for those).
- **Areas catch the caster** and the party.
- Shillelagh, Flame Blade and Spiritual Hammer need an empty hand.
- Cause Serious and Critical Wounds roll 2d9 and 3d9; the Cure spells are
  AD&D's (1d8, 2d8+1, 3d8+3).
- **Cat's Grace** (mod) takes Flaming Sphere's place among 2nd-level wizard
  spells: DEX + 1d6 (at most 24) for an hour of game time a caster level, which raises AC,
  initiative, thief skills and dodging.

### Effects

| Effect | In the game |
|---|---|
| Blessed / Cursed | +1 / −1 to hit (Bless +1 on saves too); they cancel each other |
| Hasted / Slowed | Hasted: double movement and attacks, +2 initiative. Slowed: half, loses every other turn, −4 to hit, AC 4 worse, −2 initiative |
| Paralyzed | no turns, fails every save |
| Stuck (Grease, Web, Entangle and the like) | can't move; Free Action stops it |
| Afraid | runs; can't attack or cast |
| Charmed | fights for the caster |
| Confused | each turn: runs off, does nothing, fights for a random side or acts normally |
| Berserk | fights for a random side; can't cast |
| Can't attack | can't attack or cast harmful spells |
| Blind | AC 4 worse, −2 initiative, can't cast spells that need sight |
| Acid | 2d4 a round |
| Poisoned | fatal if time passes out of a fight (resting, say) before it wears off or is cured |
| Stoneskin, Mirror Image | stop blows or images, a charge each |
| Invisibility | ends with an attack or harmful spell (Improved Invisibility doesn't) |

A click on a spell's icon on the Effects screen no longer ends it (mod).

## Psionics

Powers cost PSP to use, and those kept up cost more at the start of each
round; when PSP run short, the power drops. A defence mode is raised
automatically against a psionic attack, if the character knows one and can
pay. What each costs in the game (it differs from the manual in places):

| Power | Discipline | PSP to use | Each round kept up |
|---|---|---|---|
| Detonate | psychokinesis | 18 | |
| Disintegrate | psychokinesis | 40 | |
| Project Force | psychokinesis | 10 | |
| Ballistic Attack | psychokinesis | 5 | |
| Control Body | psychokinesis | 8 | |
| Inertial Barrier | psychokinesis | 7 | 5 |
| Animal Affinity | psychometabolism | 15 | 4 |
| Energy Containment | psychometabolism | 10 | |
| Life Draining | psychometabolism | 11 | |
| Absorb Disease | psychometabolism | 12 | |
| Adrenalin Control | psychometabolism | 8 | 4 |
| Biofeedback | psychometabolism | 6 | 3 |
| Body Weaponry | psychometabolism | 9 | 4 |
| Cell Adjustment | psychometabolism | 5 | |
| Displacement | psychometabolism | 6 | 3 |
| Enhanced Strength | psychometabolism | 0 | 8 |
| Flesh Armor | psychometabolism | 8 | 4 |
| Graft Weapon | psychometabolism | 10 | 1 |
| Lend Health | psychometabolism | 4 | |
| Share Strength | psychometabolism | 6 | 2 |
| Domination | telepathy | 0 | |
| Mass Domination | telepathy | 0 | |
| Psychic Crush (attack) | telepathy | 7 | |
| Superior Invisibility | telepathy | 5 | 5 |
| Tower of Iron Will (defence) | telepathy | 6 | |
| Ego Whip (attack) | telepathy | 4 | |
| Id Insinuation (attack) | telepathy | 5 | |
| Intellect Fortress (defence) | telepathy | 4 | |
| Mental Barrier (defence) | telepathy | 3 | |
| Mind Bar | telepathy | 6 | 4 |
| Mind Blank (defence) | telepathy | 0 | |
| Psionic Blast (attack) | telepathy | 10 | |
| Synaptic Static | telepathy | 15 | 10 |
| Thought Shield (defence) | telepathy | 1 | |

Mind Bar gives 75% magic resistance against mind-affecting spells. Body
Weaponry makes unarmed blows 2d4.

## Equipment

### Weapons

Athas has little metal: most weapons are wood, bone, stone or obsidian, and
plain ones of those are worse to hit with (above). They can also break: a
plain wood, bone, stone or obsidian weapon (not a club or quarterstaff) breaks
1 chance in 160 after a hit. The mod adds weapons in every material, among them the
short sword, which the game lacked.

| Weapon | Damage | Backstab? |
|---|---|---|
| Dagger | 1d4 | yes |
| Short sword | 1d6 | yes |
| Long sword | 1d8 | yes (metal at the limit) |
| Club | 1d6 | yes |
| Quarterstaff | 1d6 | yes |
| Axe | 1d8 | bone only |
| Pick | 1d4+1 | yes |
| Great axe | 1d10, two-handed | no |
| Mace | 1d6+1 | no |
| Cahulaks | 1d6 | no |
| Gythka | 2d4, two-handed | no |
| Polearm | 1d10 | no |
| Bow, sling, staff sling, chatkcha | by ammunition | missile: never |

Missile weapons fire at their own rate (a bow twice a round, the others once),
faster with specialization. With **Half-giants wield two-handed weapons in
one hand** (mod), a half-giant may hold one with a shield or a light weapon.

### Armour, helms and boots

Armour lowers AC; DEX lowers it more. The mod changes:

- **Helms give AC 1** (the game's give 0).
- **Boots give movement in a fight:** one more move a round.
- Plain cloaks, boots and belts cost 24.

### Protection, bracers and stealth gear

The game has no rings or cloaks of protection, nor bracers of defense; the mod
adds some, to be found. Their rules:

- **Rings and cloaks of protection:** +1 AC and +1 on every save. With **Rings
  and cloaks of protection as in AD&D** (mod): two rings don't add up; a ring
  gives no AC with magical armour (saves still count); a cloak does nothing
  with magical or metal armour or a shield.
- **Bracers of defense:** worn on the arms; their AC (6, 5, 4 or 2) counts
  only with no armour worn. A preserver casts in them.
- **Gear of elvenkind** (thieves and rangers only): with the hiding rule, a
  cloak that hides its wearer almost surely and boots that make no sound.

### Acid and breaking

Some monsters' acid or corroding touch destroys worn armour or a held weapon.
The game destroys non-magical armour without a roll. With **Items save against
acid as in AD&D** (mod), each item saves by its material (wood 8, bone 11,
stone and obsidian 5, metal 13, leather 10, cloth 12, less its plus), or the
game's number if that is easier.

## Experience and levels

XP for each level, as the game's tables have them (not all match the manual).
The 10th level comes with **Class levels go up to 10** (mod); the game stops at
9th.

| Level | Fighter, gladiator | Ranger | Cleric | Druid | Preserver | Psionicist | Thief |
|---|---|---|---|---|---|---|---|
| 2 | 2,000 | 2,200 | 1,500 | 2,000 | 2,500 | 2,200 | 1,200 |
| 3 | 4,000 | 4,500 | 3,000 | 4,000 | 5,000 | 4,400 | 2,500 |
| 4 | 8,000 | 9,000 | 6,000 | 7,500 | 10,000 | 8,800 | 5,000 |
| 5 | 16,000 | 18,000 | 13,000 | 12,500 | 20,000 | 16,500 | 10,000 |
| 6 | 32,000 | 36,000 | 27,500 | 20,000 | 40,000 | 30,000 | 20,000 |
| 7 | 64,000 | 75,000 | 55,000 | 35,000 | 60,000 | 55,000 | 40,000 |
| 8 | 125,000 | 150,000 | 110,000 | 60,000 | 90,000 | 100,000 | 70,000 |
| 9 | 250,000 | 300,000 | 225,000 | 90,000 | 135,000 | 200,000 | 110,000 |
| 10 | 500,000 | 600,000 | 450,000 | 125,000 | 250,000 | 400,000 | 160,000 |

- XP comes from kills (an equal share for each character, split again
  between a multi-class character's classes) and from deeds along the way.
- A level up is automatic, with its hit points, a better THAC0 and saves, more
  spell slots, a new preserver spell or psionic power, and any weapon spec
  due.
- At 10th level: preservers and thieves still roll hit dice, the others gain
  a fixed amount; gladiators' armour bonus grows to 2; preservers, clerics and
  druids get 5 4 3 2 2 slots.

## Thief skills

With **Thief skills from AD&D's table** (mod, on by default), each skill is
AD&D's average for the thief level, plus the race's and DEX's adjustments.
Untick it for the game's own (higher) numbers. The inventory screen and the
Ledger show each thief's chances as they stand.

| Thief level | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| Pick pockets | 30 | 35 | 40 | 45 | 50 | 55 | 60 | 65 | 70 | 80 |
| Open locks | 25 | 29 | 33 | 37 | 42 | 47 | 52 | 57 | 62 | 67 |
| Find/remove traps | 20 | 25 | 30 | 35 | 40 | 45 | 50 | 55 | 60 | 65 |
| Move silently | 15 | 21 | 27 | 33 | 40 | 47 | 55 | 62 | 70 | 78 |
| Hide in shadows | 10 | 15 | 20 | 25 | 31 | 37 | 43 | 49 | 56 | 63 |
| Hear noise | 10 | 10 | 15 | 15 | 20 | 20 | 25 | 25 | 30 | 30 |
| Climb walls | 85 | 86 | 87 | 88 | 90 | 92 | 94 | 96 | 98 | 99 |
| Read languages | 0 | 0 | 0 | 20 | 25 | 30 | 35 | 40 | 45 | 50 |

Rangers hide and move silently by their ranger level with the same numbers as
a thief's hide in shadows and move silently.

| Race | Pick pockets | Open locks | Find/remove traps | Move silently | Hide in shadows | Hear noise | Climb walls | Read languages |
|---|---|---|---|---|---|---|---|---|
| Dwarf | 0 | +10 | +15 | 0 | 0 | 0 | −10 | −5 |
| Elf | +5 | −5 | 0 | +5 | +10 | +5 | 0 | 0 |
| Half-elf | +10 | 0 | 0 | 0 | +5 | 0 | 0 | 0 |
| Halfling | +5 | +5 | +5 | +10 | +15 | +5 | −15 | −5 |
| Mul | 0 | −5 | 0 | +5 | 0 | 0 | +5 | −5 |

(Humans, half-giants and thri-kreen have none.)

| DEX | Pick pockets | Open locks | Find/remove traps | Move silently | Hide in shadows |
|---|---|---|---|---|---|
| 9 | −15 | −10 | −10 | −20 | −10 |
| 10 | −10 | −5 | −10 | −15 | −5 |
| 11 | −5 | 0 | −5 | −10 | 0 |
| 12 | 0 | 0 | 0 | −5 | 0 |
| 13-15 | 0 | 0 | 0 | 0 | 0 |
| 16 | 0 | +5 | 0 | 0 | 0 |
| 17 | +5 | +10 | 0 | +5 | +5 |
| 18 | +10 | +15 | +5 | +10 | +10 |
| 19 | +15 | +20 | +10 | +15 | +15 |
| 20 | +20 | +25 | +12 | +20 | +17 |
| 21 | +25 | +27 | +15 | +25 | +20 |
| 22 | +27 | +30 | +17 | +30 | +22 |

The game itself rolls only pick pockets, open locks, find/remove traps, hear
noise and climb walls, when its scripts ask. The mod rolls move silently and
hide in shadows for picking pockets and for the hiding rule.

## The Options tab at a glance

| Section | Switch | Default |
|---|---|---|
| In the game | each turn's rolls in the game's window | off |
| | describe monsters when you Look in a fight | on |
| Rule changes | weapon specialization, kits, class restrictions, multiclass hit points, hit dice the better of two, rangers' casting level, preservers' INT, the spell save, DEX instead of a doubled d20, two weapons, levels up to 10, items saving against acid, rings and cloaks of protection, half-giants' two-handed weapons, Cat's Grace, helms AC 1, boots for movement | all on |
| Thieves | AD&D's thief skills; hiding in shadows to backstab (and the cloak, boots and belt); picking pockets | on |
| | P in a conversation | off |
| New content | new people, a small quest, new items | on |
| On the screen | what the party wears, shadows, dust | on |
| Controls | Tab and Enter, rings under enemies (the chosen one only), wheel scrolling | on |
| | right button drags the map | off |
| Game speed | GOG's own, faster (default) or fastest | faster |

Rule changes take effect at once; new content from the next time the game is
started (a saved game keeps what it has).
