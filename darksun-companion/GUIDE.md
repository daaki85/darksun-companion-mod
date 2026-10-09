# Templar's Ledger: the player's guide

How **Dark Sun: Shattered Lands** plays with Templar's Ledger: making a party,
the classes and kits, fighting, magic, psionics, equipment and levels, with
the tables you need.

It is **spoiler-free**: no places past the opening arena, no people, no quests,
no items by name or by where they are found.

Everything here is the mod with its **default options**, which is how the
Ledger starts. Every rule change has a switch on the Ledger's **Options** tab
([at a glance](#the-options-tab-at-a-glance)); where it helps to know what a
switch changes, a **Without the mod** note says what the game does with it off.
The [README](README.md) has every rule in full detail.

## Contents

- [Getting started](#getting-started)
- [Playing](#playing)
- [Quality of life](#quality-of-life)
- [Making a party](#making-a-party)
  - [Ability scores](#ability-scores)
  - [Races](#races)
  - [Hit points](#hit-points)
  - [More than one class](#more-than-one-class)
  - [Starting gear and spells](#starting-gear-and-spells)
- [The classes](#the-classes)
  - [What each class may use](#what-each-class-may-use)
- [Kits](#kits)
  - [Kits' starting gear](#kits-starting-gear)
  - [Kits' spell slots](#kits-spell-slots)
- [Weapon specialization and attacks](#weapon-specialization-and-attacks)
- [Fighting](#fighting)
  - [Initiative](#initiative)
  - [Hitting](#hitting)
  - [Two weapons](#two-weapons)
  - [From behind, and backstabs](#from-behind-and-backstabs)
  - [Hiding in shadows](#hiding-in-shadows)
  - [Saving throws](#saving-throws)
  - [Monsters](#monsters)
- [Thieves' skills and picking pockets](#thieves-skills-and-picking-pockets)
- [Magic](#magic)
  - [Spell slots](#spell-slots)
  - [Learning preserver spells](#learning-preserver-spells)
  - [How spells work](#how-spells-work)
  - [Spell lists](#spell-lists)
  - [Effects](#effects)
- [Psionics](#psionics)
- [Equipment](#equipment)
- [Experience and levels](#experience-and-levels)
- [Worth knowing](#worth-knowing)
- [What the Ledger shows you](#what-the-ledger-shows-you)
- [The Options tab at a glance](#the-options-tab-at-a-glance)

## Getting started

1. Unzip the Ledger anywhere and double-click **`Start Templar's Ledger.bat`**
   (the first time, it offers to install Python; see the
   [README](README.md#running-it-windows)).
2. Press **Start the game**. The game opens beside the Ledger, whose dice log
   shows every roll as it happens.
3. Make your own party (**CREATE CHARACTERS**): weapon specs and kits are
   chosen when a character is made, so the four the game offers have none.

## Playing

The pointer has three modes, changed with a right-click: **Walk**, **Attack**
and **Look**; a left-click acts. Look at someone to **Talk**, at a thing to
**Use** or **Pick Up** it, and at a monster in a fight to see what the Ledger
tells of it. Resting at a fire ring fills hit points, PSP and spell slots.

The [quality of life changes](#quality-of-life) list what the mod makes
easier.

## Quality of life

**In the game:**

| Change | What it does |
|---|---|
| **Tab and Enter** | On a party member's turn in a fight, **Tab** chooses the nearest enemy (Tab again for the next, **Shift+Tab** back) and **Enter** attacks it, walking up to it first if need be, even behind someone else: no aiming with the mouse. A red ring marks the enemy chosen (or, on the Options tab, every enemy). |
| **Scrolling with the mouse** | Press the wheel and drag the map, or turn the wheel (Shift for sideways). Optionally, hold the right button and drag. |
| **40 saves** | Four pages of ten in the save and load window (**PAGE 1** to **PAGE 4**, or **PgUp** and **PgDn**). *Without the mod:* 10. |
| **29 characters on disk** | The roster keeps 29 characters made with CREATE CHARACTERS. *Without the mod:* 19. |
| **DELETE in the roster** | Deletes the character you chose. *Without the mod:* with the list scrolled, it deleted another one. |
| **New characters' thief skills** | A character not yet played shows its thief skills. *Without the mod:* they showed as 0. |
| **Spells on the Effects screen** | A stray click on a spell's icon no longer ends the spell. A psionic power's icon still ends the power, which is how you stop one. |
| **No copy protection** | The question from the manual never comes. |
| **THAC0, saves and thief skills on screen** | The inventory screen shows THAC0, all five saves, THAC0 with each weapon, DEX's adjustments and a thief's skills; View Character shows THAC0 and the saves, and for a character of several classes which class goes up next. |
| **Spell slots on the USE screen** | Spells left of each level, and the most after resting. |
| **The Look box** | In a fight, a monster's hit points, AC, THAC0, alignment, magic resistance and chief defence; closing the box tells the rest. |
| **Item boxes** | A wand's or other charged item's charges left; a cloak's, boots' or belt's bonus to thief skills. |
| **The Effects screen** | Names each kit and weapon spec, a page at a time when there are many. |
| **Each turn's rolls** (off unless ticked) | At the end of each turn in a fight, its rolls in the game's own window: at the least, in short or in detail. |
| **Game speed** | DOSBox runs the game faster than GOG's settings (choose GOG's own, faster or fastest), so the party walks smoothly with shadows and dust. |
| **Game window** | Double, triple or quadruple size, or full screen, chosen at the top of the Ledger. |
| **On the map** | The party's figures show what they wear, everyone casts a shadow, and walkers raise dust (each can be switched off). |
| **Crash reports** | If the game or DOSBox stops with an error, the message stays on screen and the Ledger writes a report to send. |

**In the Ledger's window:**

- **The dice log:** every roll as it happens, with what it needed and where
  each bonus came from; **Save...** keeps it as a text file.
- **Characters:** each character's sheet as the game's View Character lays it
  out, with THAC0 by weapon, saves, attacks a round, what they wear, spell
  slots and thief skills.
- **Dialogue:** everything said, with the speaker and the replies offered.
- **Spells:** every spell's and psionic power's dice, saves, effects and
  duration, and each party member's caster level for it.
- **Text size** (**A+** and **A-**, or Ctrl + and Ctrl −) and keyboard access to
  everything.
- **`Play Dark Sun (in-game rolls).bat`** plays with all of the above in the
  game but no Ledger window; **`Show Save.bat`** shows the party in a save file.

## Making a party

On the main menu choose **CREATE CHARACTERS**, right-click an empty slot and
choose **NEW**. Click the portrait for race and sex, mark one to three classes,
choose a cleric's or ranger's sphere, click the die to roll, and press
**DONE**. The panel under the classes has the mod's pages: **WEAPON SPEC** for
warriors ([weapon specialization](#weapon-specialization-and-attacks)) and
**KITS** ([kits](#kits)). A party has one to four characters, all good or
neutral.

### Ability scores

Each click of the die rolls a whole character:

- Each score is rolled **four times as 4d4 + 4** and the best kept (8 to 20),
  then the race's adjustment is added.
- A score below the classes' minimum is raised to it: **17 in the prime
  requisite**, otherwise **9** (clerics, fighters, preservers, thieves), **12**
  (druids, psionicists), **13** (gladiators) or **14** (rangers). A character
  of several classes takes the highest minimum of each score.

| Class | Prime requisite |
|---|---|
| Fighter, gladiator | STR |
| Cleric, druid, psionicist, ranger | WIS |
| Preserver | INT |
| Thief | DEX |

What the scores do:

- **STR:** to-hit and damage in melee, and how much is carried.
- **DEX:** AC (−1 at 15, down to −6 at 24), to-hit with missiles,
  [initiative](#initiative), thief skills, the
  [two-weapon penalty](#two-weapons), and dodging fire, cold and electricity
  ([saving throws](#saving-throws)).
- **CON:** hit points, saves against paralysis, poison and death; at 20 or
  more, a hit point comes back now and then.
- **INT:** for preservers, the chance to learn a spell from a scroll and how
  many spells of each level they can know
  ([learning spells](#learning-preserver-spells)).
- **WIS:** priests' bonus spell slots, and saves against mind-affecting magic.
- **CHA:** how some people take to the party.

### Races

| Race | STR | DEX | CON | INT | WIS | CHA | Notes |
|---|---|---|---|---|---|---|---|
| Human | | | | | | | one class at a time, but can change class |
| Dwarf | +1 | −1 | +2 | | | −2 | better CON saves |
| Elf | | +2 | −2 | +1 | −1 | | |
| Half-elf | | +1 | −1 | | | | |
| Half-giant | +4 | −5 | +2 | −5 | −3 | −3 | double hit dice; holds a two-handed weapon in one hand |
| Halfling | −2 | +2 | −1 | | +2 | −1 | better CON saves |
| Mul | +2 | | +1 | −1 | | −2 | |
| Thri-kreen | | +2 | | −1 | +1 | −2 | base AC 5, moves 15 (others 12); no armour |

The creation screen shows which classes a race may take, and greys classes
that can't go together.

### Hit points

| Class | Hit die | At 10th level |
|---|---|---|
| Fighter, gladiator, ranger | d10 | +3 |
| Cleric, druid | d8 | +2 |
| Psionicist | d6 | +2 |
| Thief | d6 | d6 |
| Preserver | d4 | d4 |

- **Every hit die is rolled twice and the better kept,** at creation (one die
  for every starting level) and at every level up. *Without the mod:* one roll.
- Half-giants roll double. A roll counts at least 2 with CON 20, 3 with CON
  21-22 and 4 with CON 23 or more.
- **CON's bonus** comes with every level: for a fighter, gladiator or ranger
  +1 at CON 15, +2 at 16, +3 at 17, +4 at 18, +5 at 19-20, +6 at 21-23 and +7 at
  24-25 (−1 at 4-6); for anyone else at most +2.
- **A character of several classes** gets each class's die divided by the
  number of classes (at least 1), and CON's bonus divided too. *Without the
  mod:* the dice are added and the total divided, and CON's bonus is whole.
- Three [kits](#kits) have a die of their own.
- At 0 hit points a character is Out Cold; at −10, dead.

### More than one class

- **Any race but human** can take two or three classes at once. Experience is
  split between them, so each rises more slowly.
- **A human** has one class, and from 2nd level can change to another
  (**DUAL** on a portrait's right-click menu), starting it at 1st level. The
  old class stops rising, and what it gives (its hit points, THAC0, saves,
  weapon specs and kit) sleeps until the new class's level passes the old
  one's. A human can change class twice, but never from one warrior class
  (fighter, gladiator, ranger) to another. The new class can take a kit of its
  own, so a human may end up with three.

### Starting gear and spells

Each class starts with:

| Class | Starting gear |
|---|---|
| Fighter | a weapon of its first weapon spec, shield, leather chest, arm and leg armour |
| Gladiator | a weapon of its first weapon spec, a club in the off hand, leather arm armour |
| Ranger | a weapon of its first weapon spec, bow and arrows, leather chest and arm armour |
| Cleric | shield, leather chest and arm armour, a club in the backpack |
| Druid | club, sling |
| Preserver | quarterstaff, sling |
| Psionicist | club, bow and arrows, leather chest armour |
| Thief | bone long sword, sling, leather chest armour, Thieves' Tools |

A warrior's starting weapon is a plain one of its first chosen weapon spec, in
a material its classes allow. A kit changes gear it can't use (a shield for a
kit that forbids one goes to the backpack, for instance); the dice log says
what changed.

A new preserver **chooses its first spells** on the CHOOSE A SPELL window: two
1st-level spells at 1st level.

## The classes

**Warriors: fighters, gladiators and rangers.** The best hit dice and THAC0
(it improves by 1 a level). They train in weapons
([weapon specialization](#weapon-specialization-and-attacks)):

- **Fighters** specialize in one kind of weapon, then master it (5th level) and
  become grand masters (9th).
- **Gladiators** specialize in two kinds, a third at 6th level and a fourth at
  9th. Their AC is 1 better from 5th level and 2 better at 10th.
- **Rangers** have expertise with the bow and one more kind, fight with two
  weapons at no penalty, hide and move silently best under the open sky, and
  cast priest spells of their sphere from 8th level, as a priest of their
  level less 7.

**Thieves** have the skills (see
[Thieves' skills](#thieves-skills-and-picking-pockets)), backstab
([from behind](#from-behind-and-backstabs)), can
[hide in shadows](#hiding-in-shadows) in a fight to get behind someone, and
pick pockets. A d6 hit die.

**Preservers** cast wizard spells: a d4 hit die, the weakest fighters, the
strongest magic. They choose a new spell at each level up and learn more from
scrolls ([learning spells](#learning-preserver-spells)).

**Clerics** are priests of one element (air, earth, fire or water): a d8 hit
die, any armour, and only their sphere's weapons. **Druids** are priests too: a
d8 hit die, any weapon, no armour. Both know every spell of their spheres from
the start, and get bonus slots for WIS.

**Psionicists** master the mind's three disciplines (psychokinesis,
psychometabolism and telepathy) and gain a new power at each level (two at odd
levels and at 4th). A d6 hit die. Every other character has one discipline and
uses its powers as a 1st-level psionicist.

### What each class may use

A character may use an item only if **every** one of its classes allows it,
the strictest winning:

| Class | Armour and helms | Shields | Weapons |
|---|---|---|---|
| Psionicist, whatever its other classes | light only (leather, hide, silk) | leather only | daggers, short swords, maces, clubs, chatkchas, bows and slings |
| Thief with another class | light only | a leather one, if another class allows shields | as its classes allow |
| Preserver, one class | none | none | a preserver's |
| Druid | none | none | any |
| Cleric | any | any | air: missile and thrown weapons, daggers; earth: stone, obsidian, metal, wood; fire: obsidian; water: bone, wood |

- A preserver with another class may wear what that class allows, but casts
  no spells while wearing armour (a helm counts, a shield doesn't). Bracers
  of defense aren't armour.
- A ranger may always use a bow.
- A human who changed class is held by its new class, but may use the kinds
  of weapon it specialized in once its old class wakes.

*Without the mod:* an item was allowed if **any** of the character's classes
allowed it, and a preserver with another class cast in armour.

## Kits

A character of one class takes one of three kits for its class when it is
made, or none, on the creation panel's **KIT** page. Each gives something and
costs something.

| Kit | Gives | Costs |
|---|---|---|
| **Myrmidon** (fighter) | a second weapon spec at 1st level, on to mastery as the first | −4 on saves against charms |
| **Sentinel** (fighter) | AC 2 better with a shield; +2 initiative | −1 on saves against wizards' and priests' spells |
| **Ravager** (fighter) | +1 to hit and damage in melee; a base AC by level (7 at 1st-2nd, 6 at 3rd-4th, 5 at 5th-6th, 4 at 7th-8th, 3 at 9th-10th), armour bettering it as usual | no missile or thrown weapons; no shield; leather armour or none |
| **Arena Champion** (gladiator) | with a shield: +1 to hit and damage in melee, and AC 1 better | −1 to hit in melee without a shield |
| **Twin-blade** (gladiator) | no penalty for two weapons | no shield; no two-handed weapon |
| **Brute** (gladiator) | +2 to hit and damage with a two-handed melee weapon | two-handed melee weapons only |
| **Stalker** (ranger) | +2 movement in a fight; +15 to hide in shadows and move silently, and hiding not halved indoors | leather armour or none |
| **Seeker** (ranger) | priest spells from 6th level, cast at its level less 5 | its sphere's weapons only, as a cleric's (but it keeps the bow) |
| **Justifier** (ranger) | its expertise becomes specialization (+1 to hit, +2 damage) | its only spell slot is one 1st-level slot, from 10th level |
| **Assassin** (thief) | hiding in shadows not halved in daylight | −15 to pick pockets and open locks |
| **Swashbuckler** (thief) | a warrior's THAC0 | −10 to every thief skill |
| **Shinobi** (thief) | preserver spells from 6th level, from its own list of 14, cast at its thief level less 5, in light armour too | no spells from scrolls; dagger, short sword, quarterstaff, chatkcha, sling, staff sling and bow only; light armour; no shield |
| **Arcanist** (preserver) | a spell slot more at each spell level it has; in a fight, two preserver spells in a turn | a d3 hit die |
| **Scholar** (preserver) | a spell more learnt at each level up | THAC0 1 worse |
| **Battle Mage** (preserver) | a warrior's THAC0; casts though hit earlier in the round; a d6 hit die; leather armour, cast in; expertise in one kind of weapon | one fewer spell slot at each spell level; nothing in the off hand |
| **Healer** (cleric) | Cure Light, Serious and Critical Wounds heal 1 more a die | no weapon in the off hand |
| **Crusader** (cleric) | a warrior's THAC0; a warrior's extra attacks in melee (3/2 a round from 7th level) | one fewer spell slot at each spell level |
| **Elementalist** (cleric) | a second sphere: its spells and its weapons | spell slots a level behind |
| **Grove Warden** (druid) | AC 1 better for every 3 druid levels | no metal weapons |
| **Wanderer** (druid) | +3 on saves against fire and cold | AC 1 worse |
| **Lifebinder** (druid) | Cure Wounds spells heal a d8 more, Blood Flow a d6 | blunt weapons only (club, mace, quarterstaff, sling, staff sling) |
| **Mind Warrior** (psionicist) | a warrior's THAC0; a warrior's extra attacks in melee (3/2 a round from 7th level); a d8 hit die | a tenth fewer PSP |
| **Mind Bender** (psionicist) | telepathy powers cost 2 PSP less | psychokinesis powers cost 2 PSP more |
| **Kineticist** (psionicist) | psychokinesis powers cost 2 PSP less | telepathy powers cost 2 PSP more |

- The **Myrmidon** and **Battle Mage** choose their extra weapon spec on the
  weapon pages after taking the kit, and the **Elementalist** its second sphere
  on the CLERICAL SPHERE list.
- A kit belongs to its class: a human who changes class keeps it, asleep until
  the new class's level passes the old.
- Some kits rule out classes a human could change to, and some can't go
  together in a human who changes class (one kit for each class); the DUAL
  window and the kit menu leave them out:

  | Kit | Can't become |
  |---|---|
  | Seeker, Justifier | cleric, druid |
  | Shinobi | preserver |
  | Swashbuckler, Crusader, Battle Mage, Mind Warrior | fighter, gladiator, ranger |
  | Arena Champion, Sentinel | druid, preserver |
  | Brute | psionicist, air cleric |

  | Kit | Can't go with |
  |---|---|
  | Arena Champion, Sentinel | Shinobi |
  | Twin-blade | Healer |
  | Brute | Shinobi, Lifebinder |

### Kits' starting gear

A new character's gear is its class's ([starting gear](#starting-gear-and-spells)),
changed where its kit can't use it:

| Kit | Starts with |
|---|---|
| Myrmidon, Sentinel | the fighter's gear |
| Ravager | the fighter's gear, its shield in the backpack |
| Arena Champion | the gladiator's gear, with a shield in place of the off-hand club |
| Twin-blade | the gladiator's gear: its weapon and the club are its two weapons |
| Brute | a two-handed weapon in place of the gladiator's (a bone great axe without weapon specialization), the club in the backpack |
| Stalker, Justifier | the ranger's gear |
| Seeker | the ranger's gear, its weapon in a material its sphere allows |
| Assassin, Swashbuckler | the thief's gear |
| Shinobi | the thief's gear with a bone short sword in place of the long sword |
| Arcanist, Scholar | the preserver's gear |
| Battle Mage | the preserver's gear; with weapon specialization, a plain weapon of its chosen kind in place of the quarterstaff |
| Healer, Crusader, Elementalist | the cleric's gear (the club is in the backpack) |
| Grove Warden, Wanderer, Lifebinder | the druid's gear |
| Mind Warrior, Mind Bender, Kineticist | the psionicist's gear |

The dice log names each change.

### Kits' spell slots

The kits that change spell slots, by the level of the kit's class (spells of
1st to 5th level):

| Level | Preserver | Arcanist | Battle Mage | Cleric | Crusader | Elementalist | Seeker (ranger) | Justifier (ranger) | Shinobi (thief) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 1 | 2 | — | 1 | — | — | | | |
| 2 | 2 | 3 | 1 | 2 | 1 | 1 | | | |
| 3 | 2 1 | 3 2 | 1 | 2 1 | 1 | 2 | | | |
| 4 | 2 2 | 3 3 | 1 1 | 2 2 | 1 1 | 2 1 | | | |
| 5 | 3 2 1 | 4 3 2 | 2 1 | 3 2 1 | 2 1 | 2 2 | | | |
| 6 | 3 2 2 | 4 3 3 | 2 1 1 | 3 2 2 | 2 1 1 | 3 2 1 | 1 | | 1 |
| 7 | 4 3 2 1 | 5 4 3 2 | 3 2 1 | 4 3 2 1 | 3 2 1 | 3 2 2 | 2 | | 2 |
| 8 | 4 3 2 2 | 5 4 3 3 | 3 2 1 1 | 4 3 2 2 | 3 2 1 1 | 4 3 2 1 | 2 1 | | 2 1 |
| 9 | 5 4 3 2 1 | 6 5 4 3 2 | 4 3 2 1 | 5 4 3 2 1 | 4 3 2 1 | 4 3 2 2 | 2 2 | | 2 2 |
| 10 | 5 4 3 2 2 | 6 5 4 3 3 | 4 3 2 1 1 | 5 4 3 2 2 | 4 3 2 1 1 | 5 4 3 2 1 | 2 2 1 | 1 | 2 2 1 |

- A **Crusader** and an **Elementalist** add WIS's bonus slots as a cleric
  does; the Crusader still has one fewer at each spell level with them.
- A **Seeker** casts priest spells of its sphere at its ranger level less 5
  (1st-level spells from 6th, 2nd from 8th, 3rd at 10th); a **Justifier** at
  its level less 9. Neither gets bonus slots for WIS, and both have these in
  place of a ranger's own slots.
- A **Shinobi** casts preserver spells at its thief level less 5, from its own
  list, learning one at each level up from 6th: **1st level** Gaze Reflection,
  Charm Person, Shield, Color Spray, Wall of Fog; **2nd** Invisibility, Mirror
  Image, Blur, Detect Invisibility, Fog Cloud; **3rd** Blink, Haste, Protection
  from Normal Missiles, Hold Person.
- An **Arcanist** casts two preserver spells in a turn in a fight (a hit before
  the second still stops it); a **Scholar** chooses two spells at each level
  up.

## Weapon specialization and attacks

Warriors train in kinds of weapon. Choose them on the creation panel's
**WEAPON SPEC** pages; picks due later come in a window at the level up.

| Who | Chooses | With a chosen kind |
|---|---|---|
| Fighter | 1 kind | specialized: +1 to hit, +2 damage; **mastery** from 5th level: +3 to hit, +3 damage; **grand mastery** from 9th: the same, the damage die a size larger and one more attack a round |
| Gladiator | 2 kinds, a 3rd at 6th level, a 4th at 9th | specialized in each: +1 to hit, +2 damage |
| Ranger | the bow, and 1 kind | expertise: a specialist's attacks, no other bonus |

The sixteen kinds: long sword, club, dagger, short sword, mace, axe, great
axe, pick, quarterstaff, polearm, gythka, cahulaks, chatkcha, bow, sling and
staff sling. A warrior with another class chooses only kinds that class lets
it use.

**Attacks a round**, by the warrior's level (its best fighter, gladiator or
ranger level). 3/2 means one attack one round and two the next.

| With the weapon | Melee, 1-6 | Melee, 7-10 | Bow, 1-6 | Bow, 7-10 | Sling, staff sling, chatkcha, 1-6 | 7-10 |
|---|---|---|---|---|---|---|
| anyone who isn't a warrior | 1 | 1 | 2 | 2 | 1 | 1 |
| a warrior, a kind it hasn't chosen | 1 | 3/2 | 2 | 3 | 1 | 3/2 |
| a chosen kind (specialized, mastery, expertise) | 3/2 | 2 | 3 | 4 | 3/2 | 2 |
| grand mastery (9th level on) | | 3 | | 5 | | 3 |

The Crusader, Mind Warrior and Battle Mage [kits](#kits) have extra attacks of
their own. With [two weapons](#two-weapons), the off hand attacks once a round
whatever the rate.

*Without the mod:* every warrior has 3/2 attacks a round in melee (2 from 7th
level) with any weapon, and no other bonus; missile weapons shoot at the
weapon's own rate for everyone.

## Fighting

### Initiative

At the start of each round everyone's initiative is **20 + a 0-9 roll + DEX's
adjustment**, +2 Hasted, −2 Slowed, −2 Blind; highest acts first. The weapon
makes no difference. **Wait** drops a character to act later.

| DEX | 1 | 2 | 3 | 4 | 5 | 6-15 | 16 | 17-18 | 19-20 | 21-23 | 24-25 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Adjustment | −6 | −4 | −3 | −2 | −1 | 0 | +1 | +2 | +3 | +4 | +5 |

A character hit in a round can't cast a spell until the next round (the Battle
Mage can).

### Hitting

An attack hits on **d20 ≥ THAC0 − the target's AC**. A 20 always hits and a 1
always misses, but **there are no critical hits**: a 20 does ordinary damage.
To-hit changes with:

- STR in melee, DEX with missiles;
- the weapon's plus; a plain weapon of wood is −3, of stone or obsidian −2, of
  bone −1 (metal has no penalty);
- weapon specialization;
- Bless and Prayer +1, Curse −1, Slow −4;
- attacking from behind +2, a backstab +2 more;
- two weapons ([below](#two-weapons)).

Damage is the weapon's dice, its plus, specialization's bonus and, in melee,
STR's bonus; at least 1.

### Two weapons

With a melee weapon in each hand:

- **−2 to hit with the main (right) hand and −4 with the off (left) hand,** and
  the DEX adjustment from [initiative](#initiative) added, which can lessen the
  penalty to 0 but never make it a bonus: DEX 17 is 0 and −2, DEX 21 is 0 and 0,
  DEX 3 is −5 and −7.
- **Rangers and Twin-blades** have no penalty.
- **The off hand attacks once a round.** Extra attacks are the main hand's: a
  warrior at 3/2 attacks 3/2 + 1 (one round 1 + 1, the next 2 + 1).

A weapon and a shield, or a weapon and a bow or sling, aren't two weapons.

*Without the mod:* no penalty (a small bonus at DEX 5 or less), and each hand
attacks at the character's full rate.

### From behind, and backstabs

- Each round a creature turns to face the first one to attack it, and keeps
  facing that way. An attacker in the square directly behind it attacks
  **from behind**: +2 to hit, and the target loses its DEX bonus and its
  shield.
- A **backstab** is a thief's attack from behind, in melee, with a weapon no
  heavier than a long sword (see [Equipment](#equipment)): +4 to hit in all,
  and the thief's first attack of the round does **×2** damage at levels 1-4,
  **×3** at 5-8 and **×4** at 9-10, STR's bonus included.

### Hiding in shadows

A thief or ranger whose turn comes in a fight **with no enemy in the eight
squares around** first tries to **hide in shadows**, then to **move
silently**. With both, their next attack that turn is from behind: a thief's is
a backstab with a light enough weapon. Attacking, or ending the turn, gives
them away. An enemy beside them when the turn comes means no hiding: get clear
first.

- Thieves' hiding is **halved in daylight** (under the open sky); rangers'
  is halved indoors instead.
- A worn cloak adds 10 to hiding in shadows and worn boots 10 to moving
  silently, up to 95. A worn belt adds 5 to a thief's picking pockets and
  opening locks.

*Without the mod:* thieves backstab only a target that has turned to face
someone else, and no one hides in a fight.

### Saving throws

A save succeeds when **d20 + its modifiers reaches the save's number**; a 1
always fails and a 20 always saves. Everyone has five: paralysis, poison and
death (`PPD`), rod, staff and wand (`RSW`), petrification and polymorph
(`PP`), breath weapon (`BW`) and spell (`SP`).

- **Spells are saved against with the spell save**, except poisons, death
  spells and psionic attacks (paralysis, poison and death).
- **Against fire, cold and electricity spells, DEX helps you dodge:**

  | DEX | 1-2 | 3 | 4 | 5 | 6 | 7-14 | 15 | 16 | 17 | 18-20 | 21-23 | 24-25 |
  |---|---|---|---|---|---|---|---|---|---|---|---|---|
  | Modifier | −5 | −4 | −3 | −2 | −1 | 0 | +1 | +2 | +3 | +4 | +5 | +6 |

*Without the mod:* almost every spell is saved against with petrification and
polymorph, and against fire, cold and electricity the d20 counts double, so
most saves against a Fireball succeed.

Other modifiers:

| Modifier | On |
|---|---|
| WIS: −6 at 1, −4 at 2, −3 at 3, −2 at 4, −1 at 5-7, +1 at 15, +2 at 16, +3 at 17, +4 at 18 or more | mind-affecting spells, charms, holds, fear and illusions |
| CON: −2 at 1, −1 at 2, +1 at 19-20, +2 at 21-22, +3 at 23-24, +4 at 25; dwarves and halflings +1 more for every 3.5 points of CON | paralysis, poison and death |
| Druids +2 | fire and electricity |
| Psionicists +2 | mind-affecting spells and charms |
| Bless +1, Barkskin +1, Spirit Armor +3 (not PPD), Prayer ±1, a ring or cloak of protection +1 | every save |
| Protection from Evil +2; from Fire, from Cold +3; from Lightning +4 | against the matching caster or spell |
| +4 | against a spell at you alone, when its caster can't see you |

Creatures of 6th level or less can't save against Cloudkill; only warriors
save against Chaos; against Scare, 6th level and up always save and others
can't.

### Monsters

Monsters have defences of their own: some need magic weapons, some are hurt
only by edged weapons or immune to crushing ones, some shrug off fire, cold,
poison or the powers of the mind, some can't be charmed or held. **Look** at
one in a fight: the box shows its hit points, AC, THAC0, alignment, magic
resistance and chief defence (`NEEDS +1 WEAPON`, `IMM FIRE COLD`, `NO
CRUSH`, `HALF FROM WPNS`, `UNDEAD`), and closing it tells the rest. Undead
take nothing from poison or draining, and mind-affecting spells don't work on
them.

## Thieves' skills and picking pockets

A thief's skills come from the table by thief level, plus the race's and
DEX's adjustments. A thief who isn't Okay, or is Blind, Afraid, Confused,
Berserk or Paralyzed, can't use them; nothing worn stands in the way.

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

Rangers hide and move silently with the thief's numbers for their ranger level
and the same race and DEX adjustments.

**When the skills are rolled:**

- **Open locks, find/remove traps, climb walls, hear noise** and the one
  pocket the game has to pick: when the game asks, at certain locks, traps
  and walls.
- **Hide in shadows and move silently:** at the start of a thief's or ranger's
  turn in a fight ([hiding in shadows](#hiding-in-shadows)).
- **Picking pockets** (the mod's): pick a thief's **Thieves' Tools** up on the
  inventory screen, go back to the map with them on the pointer, and click
  someone in sight (not in a fight). The thief rolls **pick pockets**:
  - **success:** one small thing from them goes into the thief's backpack:
    something light that isn't worn on the body;
  - **failure:** the thief rolls **move silently** to slip away. Made, they can
    try again; missed, they are caught, and that person keeps a hand on their
    pockets from then on.

  When nothing worth taking is left, the thief takes a few coins from the
  purse, and that is the last try on them. Every thief starts with a set of
  tools.
- **Read languages** is never rolled.

*Without the mod:* the game's own chances, which run much higher (a base of its
own plus 4 a level), and a penalty when a thief holds anything in either hand,
or has anything in the quiver or on the legs.

## Magic

### Spell slots

Casting uses a slot of the spell's level; resting fills them.

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

That is for preservers, clerics and druids alike. **Rangers** have one
1st-level slot at 8th level, two at 9th, and a 2nd-level slot at 10th. No spell
is above 5th level.

**Clerics and druids** have more for WIS, only at spell levels their class
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

A character's classes add up their slots. Several [kits](#kits) have more or
fewer. The game's USE screen shows what is left of each level.

### Learning preserver spells

A preserver chooses a spell at each level up, and can learn more from scrolls
(right-click the scroll in the inventory, then click its icon), of a level it
can cast. INT sets two limits:

| INT | Chance to learn from a scroll | Most spells of each level |
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

- **A failed roll uses the scroll up.**
- **A full spell level** learns no more: the scroll is kept.
- The level-up choice leaves out levels already full.

*Without the mod:* every scroll is learnt, and there is no limit.

### How spells work

- **Damage** grows with the caster's level up to **10th**: Fireball and
  Lightning Bolt do at most 10d6. Someone Out Cold gets no save and takes the
  most the dice can do.
- **Duration** is so much a caster level plus dice; a round is a minute of game
  time.
- **Caster level** is the caster's best level in a class whose sphere has the
  spell. A ranger casts at its level less 7, for what it may cast and for
  damage and duration alike. An elemental spell works only for a priest of
  that element.
- **Area spells catch the caster** and the party.
- Shillelagh, Flame Blade and Spiritual Hammer need an empty hand.
- Cause Serious and Critical Wounds roll 2d9 and 3d9; Cure Light, Serious and
  Critical Wounds heal 1d8, 2d8+1 and 3d8+3.
- **Cat's Grace** is a 2nd-level wizard spell in Flaming Sphere's place: DEX +
  1d6 (at most 24) for an hour of game time a caster level, which betters AC,
  initiative, thief skills and dodging.

### Spell lists

**Preservers' spells** (the game's Flaming Sphere is Cat's Grace):

| Level | Spells |
|---|---|
| 1 | Armor, Burning Hands, Charm Person, Chill Touch, Color Spray, Enlarge, Gaze Reflection, Grease, Magic Missile, Shield, Shocking Grasp, Wall of Fog |
| 2 | Acid Arrow, Blur, Cat's Grace, Detect Invisibility, Fog Cloud, Glitterdust, Invisibility, Mirror Image, Protection from Paralysis, Scare, Stinking Cloud, Strength, Web |
| 3 | Blink, Dispel Magic, Fireball, Flame Arrow, Haste, Hold Person, Hold Undead, Lightning Bolt, Minor Malison, Minute Meteors, Monster Summoning I, Protection from Normal Missiles, Slow, Spirit Armor, Vampiric Touch |
| 4 | Black Tentacles, Charm Monster, Confusion, Fear, Fire Shield, Ice Storm, Improved Invisibility, Minor Globe of Invulnerability, Minor Spell Turning, Monster Summoning II, Rainbow Pattern, Solid Fog, Stoneskin, Turn Pebble into Boulder, Wall of Fire, Wall of Ice |
| 5 | Chaos, Cloudkill, Cone of Cold, Conjure Elemental, Dismissal, Domination, Feeblemind, Hold Monster, Lower Resistance to Magic, Monster Summoning III, Summon Shadow, Wall of Force, Wall of Stone |

**Priests' spells.** Every cleric, druid and ranger has the common ones of the
levels it can cast; druids alone have the common 4th and 5th-level ones; and
each has its own element's.

| Level | Every priest | Druids only |
|---|---|---|
| 1 | Bless, Cause Fear, Cause Light Wounds, Cure Light Wounds, Curse, Entangle, Invisibility to Undead, Protection from Evil, Remove Fear, Shillelagh | |
| 2 | Aid, Barkskin, Charm Person or Mammal, Find Traps, Hold Person, Spiritual Hammer | |
| 3 | Bestow Curse, Cause Blindness or Deafness, Cause Disease, Cure Blindness or Deafness, Cure Disease, Dispel Magic, Magical Vestments, Negative Plane Protection, Prayer, Remove Curse, Remove Paralysis | |
| 4 | | Abjure, Cause Serious Wounds, Cloak of Bravery, Cloak of Fear, Cure Serious Wounds, Free Action, Neutralize Poison, Poison, Protection from Evil 10' Radius |
| 5 | | Cause Critical Wounds, Cure Critical Wounds, Dispel Evil, Raise Dead, Slay Living |

| Level | Air | Earth | Fire | Water |
|---|---|---|---|---|
| 1 | | Magical Stone | | |
| 2 | Dust Devil | Dust Devil | Flame Blade, Resist Cold, Resist Fire | |
| 3 | Conjure Lesser Air Elemental, Summon Insects | Conjure Lesser Earth Elemental | Conjure Lesser Fire Elemental, Protection from Fire | Conjure Lesser Water Elemental |
| 4 | Dust Cloud, Protection from Lightning | Condense, Dust Cloud | Focus Heat, Produce Fire | Blood Flow, Dehydrate |
| 5 | Conjure Air Elemental, Deflection, Insect Plague | Conjure Earth Elemental, Ironskin, Quicksand | Conjure Fire Elemental, Flame Strike, Wall of Fire | Conjure Water Elemental, Quicksand |

An Elementalist has its second sphere's column too.

### Effects

| Effect | Does |
|---|---|
| Blessed / Cursed | +1 / −1 to hit (Bless also +1 on saves); they cancel each other |
| Hasted / Slowed | Hasted: double movement and attacks, +2 initiative. Slowed: half, loses every other turn, −4 to hit, AC 4 worse, −2 initiative |
| Paralyzed | no turns; fails every save |
| Stuck (Grease, Web, Entangle and the like) | can't move; Free Action stops it |
| Afraid | runs; can't attack or cast |
| Charmed | fights for the caster |
| Confused | each turn: runs off, does nothing, fights for a side picked at random, or acts normally |
| Berserk | fights for a side picked at random; can't cast |
| Can't attack | can't attack or cast harmful spells |
| Blind | AC 4 worse, −2 initiative; can't cast spells that need sight |
| Acid | 2d4 a round |
| Poisoned | fatal if time passes out of a fight (resting, for one) before it wears off or is cured |
| Stoneskin, Mirror Image | each blow stopped, or image struck, uses a charge |
| Invisible | ends with an attack or a harmful spell (Improved Invisibility doesn't) |

## Psionics

A power costs PSP to use, and one kept up costs more at the start of each
round; when the PSP run short, it drops. Against a psionic attack, a character
raises the best defence mode it knows and can pay for, by itself.

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

Mind Bar gives 75% magic resistance to mind-affecting spells. Body Weaponry
makes unarmed blows 2d4. The Mind Bender and Kineticist [kits](#kits) change
some costs.

## Equipment

**Weapons.** Most are wood, bone, stone or obsidian; plain ones of those hit
worse than metal ([hitting](#hitting)), and can break (1 chance in 160 after a
hit; not clubs or quarterstaffs). Weapons of every kind come in several
materials, the short sword among them.

| Weapon | Damage | Can backstab |
|---|---|---|
| Dagger | 1d4 | yes |
| Short sword | 1d6 | yes |
| Long sword | 1d8 | yes |
| Club | 1d6 | yes |
| Quarterstaff | 1d6 | yes |
| Axe | 1d8 | bone ones |
| Pick | 1d4+1 | yes |
| Great axe (two-handed) | 1d10 | no |
| Mace | 1d6+1 | no |
| Cahulaks | 1d6 | no |
| Gythka (two-handed) | 2d4 | no |
| Polearm | 1d10 | no |
| Bow, sling, staff sling, chatkcha | by the missile | no: missiles never backstab |

A half-giant holds a two-handed weapon in one hand, with a shield or a light
weapon in the other.

**Armour** lowers AC, and DEX lowers it more. **Helms give AC 1**, and
**boots give one more move** each round of a fight. *Without the mod:* helms
give no AC and boots no movement.

**Protection.** Rings and cloaks of protection give +1 AC and +1 on every save,
by AD&D's rules: two rings don't add up; a ring gives no AC with magical armour
(its saves still count); a cloak does nothing with magical or metal armour or
a shield. **Bracers of defense** give their AC (6, 5, 4 or 2) only with no
armour worn, and a preserver casts in them. These are rare finds.

**Acid.** Some monsters' acid or corroding touch can destroy worn armour or a
held weapon. Each item gets a saving throw by its material: wood 8, bone 11,
stone and obsidian 5, metal 13, leather 10, cloth 12, less its plus (a weapon
uses the game's own number where that's easier). *Without the mod:* plain
armour is destroyed outright.

**Item boxes** (right-click an item in the inventory) show a wand's or other
charged item's charges left, and a cloak's, boots' or belt's bonus to thief
skills.

## Experience and levels

Experience comes from kills (an equal share for each character, split again
between a character's classes) and from deeds along the way. A level up comes
by itself, with hit points, a better THAC0 and saves, spell slots, a new
preserver spell or psionic power, and any weapon spec due.

Every class goes up to **10th level**. *Without the mod:* 9th.

| To reach level | Fighter, gladiator | Ranger | Cleric | Druid | Preserver | Psionicist | Thief |
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

## Worth knowing

- **Cure poison before resting.** A character still Poisoned when time passes
  out of a fight dies.
- **Area spells catch the caster and the party.** Aim fireballs and clouds
  away from your own.
- **Act before you are hit if you mean to cast.** A character hit earlier in
  the round can't cast (a Battle Mage can).
- **Someone Out Cold takes the most a spell's dice can do,** with no save.
- **Two weapons cost to-hit** unless your DEX is high or you are a ranger or
  Twin-blade, and the off hand attacks only once a round.
- **A warrior's weapon specs matter:** outside them it attacks once a round
  until 7th level.
- **Multi-class preservers take off their armour to cast** (a helm counts).
- **Thieves hide with no enemy beside them** when their turn comes; step away
  first. Daylight halves their chance, and rangers' indoors.
- **Plain wood, bone, stone and obsidian weapons can break** (clubs and
  quarterstaffs can't); magic ones never do.
- **Spell damage stops growing at caster level 10.**
- **Wait** puts a character later in the round.
- **Ready a missile weapon and a melee weapon:** the game uses whichever fits
  the target's distance.

## What the Ledger shows you

- **In the game's own screens:** THAC0 and all five saves on the inventory
  screen and View Character, THAC0 with each weapon, a thief's skills, spell
  slots left on the USE screen, and, for a character of several classes, which
  class goes up next. The Effects screen names kits and weapon specs.
- **The Look box in a fight:** a monster's hit points, AC, THAC0, magic
  resistance and defences.
- **The dice log** in the Ledger's window: every roll as it happens, with what
  it needed and where each bonus came from. Tick **Show each turn's rolls in
  the game** for them in the game's own window at the end of each turn.
- **The Ledger's Characters tab:** each character's sheet, what they wear,
  spell slots and thief skills; the **Spells** tab has every spell's dice,
  saves and durations.

## The Options tab at a glance

| Section | Switch | Default |
|---|---|---|
| In the game | show each turn's rolls in the game | off |
| | describe monsters when you Look at them in a fight | on |
| Rule changes | weapon specialization; kits; class restrictions; multiclass hit points; rangers' casting level; preservers' INT; hit dice rolled twice; the spell save; DEX instead of a doubled d20; two weapons; levels up to 10; items saving against acid; rings and cloaks of protection; half-giants' two-handed weapons; Cat's Grace; helms AC 1; boots for movement | all on |
| Thieves | thief skills from AD&D's table; hiding in shadows to backstab; the cloak, boots and belt; picking pockets | on |
| | ... or P in a conversation (the leader, a thief, picks the pocket of the one talked to) | off |
| New content | new people, a small quest, new items | on |
| On the screen | what the party wears, shadows, dust | on |
| Controls | Tab and Enter; rings under the enemy chosen with Tab; scrolling with the mouse wheel; spells kept on a click on the Effects screen | on |
| | scrolling by holding the right button | off |
| Game speed | GOG's own, faster or fastest | faster |

Rule changes count at once in a game started from the Ledger; new content
comes the next time the game is started (a saved game keeps what it has).
