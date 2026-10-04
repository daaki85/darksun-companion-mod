# Templar's Ledger: a companion and mod for Dark Sun: Shattered Lands

Templar's Ledger runs next to **Dark Sun: Shattered Lands** (the GOG release, in
DOSBox) and shows what the game keeps to itself: every roll it makes, what each
roll was compared against, and where every bonus comes from. It also adds to the
game itself, in the game's own lettering and windows:

- **The rolls behind the scenes:** attacks, damage, saving throws, magic
  resistance, initiative, thief skills, character creation and level-up HP, with
  each bonus named.
- **A party viewer:** THAC0 with each weapon, saves as they stand now, AC and
  what makes it up, spell slots, thief skills, equipment and active effects.
- **In the game:**
  - THAC0, saves, thief skills and DEX adjustments on the inventory screen,
    THAC0 and saves on View Character;
  - spell slots on the USE screen;
  - each turn's rolls in a pop-up during fights, if you tick it (three levels
    of detail);
  - what hurts a monster in the Look box;
  - a party member's spell no longer ended by a click on the Effects screen.
- **Dialogue and spells tabs:** a scrollable record of every conversation, and
  what each spell and psionic power really does, from the game's own records.
- **Optional AD&D rule changes**, all on by default and each one switchable:
  - helms give AC;
  - boots give an extra move;
  - two-weapon penalties;
  - spells saved against with the spell save;
  - DEX on saves against fire, cold and electricity instead of a doubled d20;
  - a new spell, Cat's Grace;
  - thieves hiding in shadows and moving silently to backstab, and rangers
    to attack from behind (a cloak and boots help);
  - thief skills from AD&D's table, with Dark Sun's race and DEX adjustments;
  - half-giants wielding two-handed weapons in one hand;
  - class levels up to 10 (the game stops at 9).
- **New items and thief play:** a Ring of Protection +1 to find in the arena;
  gear for Kurzak, Legcrusher and Pehtucl in the slave pens (a short sword
  and a Cloak of Protection among it), with icons of their own; the rest of
  the bone scale armour, with a Bone Helm, where its chest piece lies; Thieves'
  Tools for every thief;
  picking anyone's pockets; and no more thief skill penalty for what a thief
  holds.
- **A mini-quest:** the cooked vulture, at last good for something (Dinos
  cooks it for the party, to the game's own quest-done sound).
- **A new person in the slave pens:** Kalzith, a defiler slave who, treated
  with respect, sells arcane spell scrolls that a preserver can learn from.
- **Semyon kept his word:** after he leaves the arena through the entrance to
  the pens, he is in the pens to talk to, as the game promised and never did;
  and if he is still beside the party when they break out with Scar, he breaks
  out with them.
- **What the party wears, on the map:** weapons, shields, bows, armour, helms,
  cloaks, boots and belts on their figures, walking and fighting, changing as
  their gear does.
- **Shadows under every figure:** see-through, cast toward the lower right as
  the walls' are, in the floor's own colours, with the walls and figures in
  front standing on them.
- **Scrolling the map with the mouse:** press the wheel and drag the map, or
  turn the wheel.
- **Dust** raised behind the feet of anyone walking on sand or dirt.
- **Choosing an enemy with Tab:** in a fight Tab chooses an enemy, marked by a
  red ring (or rings under all of them, or none: an option), and Enter attacks
  it even behind someone.

The game folder is never modified, and your save files only keep what you'd
expect from play: the items the Ledger hands out, the XP it gives. For the dice
log, the launcher runs a patched copy of the game that it keeps in its own
folder.

**Everything else is in [`darksun-companion/README.md`](darksun-companion/README.md):**
- requirements;
- how to start it on Windows;
- every log line explained;
- how it works.

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

## Changelog

Release **1.0.0** is pull requests #1 to #13. Its notes are in
[`release-notes/v1.0.0.md`](release-notes/v1.0.0.md).

### Pull request #16 (in review)

**Added**
- **Semyon breaks out with Scar:** recruit Semyon before the fight with Scar,
  take up Scar's offer to break out, and Semyon comes along to the slave pens
  with Scar's men, fights the guards on the party's side, and has a line of his
  own for the breakout. In the game he was left behind in the arena.

- **Game speed on the Options tab:** the launcher gives DOSBox 20,000 cycles
  by default, at which walking with shadows, dust and rings on is as smooth as
  the game without them (at GOG's speed it was slower and choppy); GOG's own
  speed and 30,000 can be chosen, with suggested system requirements for each
  in the companion's README. DOSBox runs on its dynamic core, smoother at the
  same cycles and lighter on the computer.
- **Faster walking with gear shown:** the party's figure pictures keep only the
  room their gear needs while walking (they had 10 pixels all round, which the
  game drew again at every step). Each picture is now exactly as long as its
  outfit: a new outfit is written into the Ledger's copy of the game's file
  and the game loads it from there (as fast as before), instead of being
  written into pictures kept with spare room, which the game drew too. With
  plain figures and everything else off, the party walks as smoothly as in the
  game without the Ledger.
- **New content switches:** Kalzith, Semyon, the cooked vulture, the slave
  pens' gear, a worn cloak's and boots' bonuses to hiding, and the Effects
  screen's click keeping a spell can each be switched off on the Options tab.
  The Options tab is regrouped so related switches sit together: Dice log, In
  the game, Rule changes, New content, On the screen, Controls and Game speed.
- **Crash reports:** when DOSBox crashes or the game stops with an error (such
  as "Null pointer assignment", which used to close DOSBox at once), the
  game's message stays on screen and the Ledger saves a report in
  `crash-logs` with how it closed, what was on screen, the switches, and the
  end of the dice log and dialogue.
- **The Trustee knows Semyon got away:** if Semyon broke out with the party and
  lived, the Trustee says so after the escape (the game's own line for a Semyon
  who escaped), instead of "Every single one" for all the pens.

**Fixed** (from a review of the code)
- **Clicks after Tab + Enter:** for a few seconds after Enter, anything the
  next character clicked could still count as the enemy chosen before. The
  enemy is now let go as soon as the choice is (at the next turn).
- **Kalzith and Semyon in fights:** people past the map's 256th thing (as they
  are in the pens) were missing from the Ledger's list of who is in a fight:
  no ring, no Tab, no HP lines, no "killed" line for them.
- **A thief who went last and is next** after someone first who can't act (out
  cold, dead) lost their turn line and hiding roll.
- **Two halved hits seen together** (non-magical weapons on a creature that
  halves them) were put down to the first, and the second later logged as
  doing nothing.
- **The mouse wheel's watch** (Windows) was started again on every reconnect
  without stopping the last one.
- **Kalzith only with his object:** a copy of the game whose objects lack what
  he is made from no longer gets his scripts (which would name an object that
  isn't there); a clash over his scrolls' pictures no longer loses every icon.
- **Speed:** the gear writer's look through the game's memory sizes each
  picture once instead of searching again for every copy; the rings' and dust's
  colour tables are worked out once for a palette, not every 30 seconds.

### Pull request #14 ([merged 2026-10-04](https://github.com/daaki85/darksun-companion-mod/pull/14))

**Added**
- **What the party wears, on the map:** each character's figure shows their
  weapons and shields (each kind its shape, in its material's colours), bow
  and quiver on the back, armour (their own clothing recoloured toward its
  material), helms as circlets, cloaks (the game's own cloak, fitted to them),
  boots and belts, walking and fighting, and changes as soon as their gear
  does. Walking, a one-handed weapon hangs at the belt; in a fight it is in
  the hand. Two characters of the same race and sex each show their own
  gear. On by default; a switch on the Options tab.
- **Kalzith, a defiler in the slave pens:** a slave the templars put in the
  arena now and then, kept in a pen of his own, with a face of his own (the
  game's portrait 61 with a slave's brand). Talk to him (Look, then Talk):
  treated with respect, he sells six spell scrolls, one of each (Magic Missile
  and Color Spray 100, Blur and Cat's Grace 250, Lightning Bolt and Haste
  500; Cat's Grace only with its rule on), in the game's own shop screen. A
  preserver learns them as from any scroll. Accuse him and threaten to tell
  the templars, and he won't trade until the party pays 50 ceramic or wins
  him over (a Charisma check). Once all six are bought, his shop closes and
  he wears a Cloak and carries a Quarterstaff. Killed, he leaves one random
  scroll of those he still had, the Cloak and the Quarterstaff. Attacked, he
  is like any of the pens' slaves. New games only.
- **Semyon in the slave pens,** once he has left the arena (after the fight he
  helps in, if the party recruits him): in a pen of his own above Kalzith's,
  with his own conversation (why he was tied up in the arena, who carries keys, where
  his gem is hidden, the Alliance's plans). The game itself never puts him
  there; if he was killed, or left the arena another way, he isn't there. In
  the pens he is one of the slaves, no longer on the party's side: attacked,
  he is like any of them.
- **Dinos and the Trustee know about them:** their "who else is in here"
  questions also ask about Kalzith, and about Semyon once he is in the pens;
  if either is killed, they speak of him as of the game's dead ("What was
  Kalzith like?"). After the party's escape both are gone from the pens with
  everyone else.
- **Shadows under every figure on the map:** each living creature's outline,
  laid down toward the lower right (the light on the maps comes from the upper
  left, as the walls' shadows show), see-through and in the floor's own
  colours, drawn on the floor before the walls and figures, so everything in
  front stands on them. They follow figures as they move, in fights too. A
  switch on the Options tab, on by default.
- **Scrolling the map with the mouse:** pressing the wheel and moving drags
  the map with the pointer, in fights too, and in Windows turning the wheel
  scrolls it (sideways with Shift). Optionally the right button drags it too (a
  right click still changes the pointer). Switches on the Options tab.
- **Dust behind walking feet:** puffs on sand and dirt behind anyone walking,
  spreading and fading in about a second, under the walls and figures. A
  switch on the Options tab, on by default.
- **Choosing an enemy with Tab, attacking it with Enter:** on a party member's
  turn in a fight, Tab picks an enemy (nearest first; Shift+Tab back), marked
  by a red ring, with the view scrolled to it; Enter attacks it as a click on
  it would, even when someone stands in front of it. Rings on the Options tab:
  none, only the chosen enemy's (the default) or all the enemies'.
- **Hits that do less than rolled** in the dice log: a weapon hit that took
  part of its damage, or none, with what the monster's defences say (`Skeleton
  takes none of the 6 damage: crushing weapons can't hurt it`).
- **The quest sound for the vulture:** giving Dinos the cooked vulture plays
  the sound the game plays when a quest is done (the Trustee's key, the
  filled water jug).
- **Cloaks and boots help thieves and rangers hide:** with the stealth rule, a
  worn cloak adds 10 to hiding in shadows (before daylight halves it) and worn
  boots 10 to moving silently, up to 95.
- **Regeneration in the dice log:** a hit point back by itself, which the game
  gives anyone with CON 20 or more, is logged as such (`Gerrard regenerates 1
  HP (CON 22)`).
- **A safety net against stray writes:** the Ledger never writes over the start
  of memory or the first bytes of the game's data (what "Null pointer
  assignment" checks); a write stopped there is named in the dice log.

**Changed**
- **The Effects screen no longer ends a spell's effect when its icon is clicked**
  (the game's own behaviour, which dispelled a party member's buff by accident).
  A psionic power's can still be stopped there, as it costs PSP to maintain.
- **Windows' security warning only once:** after the first `.bat` file is let
  through ("Open File - Security Warning", Run), the Ledger takes the download
  mark off the files in its own folder, so the others start without asking.
- **The vulture quest is part of Dinos's talk:** while the party carries the
  cooked vulture, his first menu has "We cooked the vulture from the arena."
  just before "Goodbye." His answer is in his own dialogue window, with his
  portrait, and the XP comes as the game's quests give it, in the game's own
  window ("Each party member receives 100 experience points!"); the vulture
  is no longer used on him from the inventory.
- **Cat's Grace's icon** is a cat's paw print instead of a cat's face.
- **Dinos's vulture lines** are his own words, without narration (the game's
  conversations are people speaking).

**Fixed**
- **DOSBox crashes, garbled figures, freezes and "Null pointer assignment"**
  (in this pull request's earlier builds): the gear writer kept writing a party
  picture over memory the game had freed and given to something else (a
  monster's figure after a fight, a portrait). It now writes only over its own
  pictures. Gear then failed to show after an area change in one build (an
  older copy of a picture not recognised as the Ledger's); fixed too.
- **Kalzith said he had nothing left to sell** after one purchase: while a save
  loaded, the Ledger could read the new game's flags with the last game's
  Kalzith (emptied by pickpocketing) and mark it sold out. A game marked so by
  mistake gets his shop back.
- **The vulture's reward in the dice log when a game was loaded,** and its XP
  and rest given then: the flag was read from memory still being loaded.
- **A thief first in a round didn't hide:** someone who had the last turn of one
  round and the first of the next got no new turn in the log, so no hide in
  shadows or move silently roll.
- **Tab + Enter froze the game:** after Enter, the walk to the chosen enemy
  stalled, sometimes until a mouse click. The helper answered the game's "what is
  under the pointer" with the enemy and returned without giving back the game's
  interrupt state, so the game ran on with its timer stopped. Fixed; the
  helper's waits for the Ledger also no longer depend on the BIOS clock, so
  they can't hang if it stands still.
- **The party's gear showed late after an area change:** the Ledger looked for the
  area's newly loaded pictures only every 10 seconds, and dressed the party with
  its slower checks (every 3 seconds); a party walking off as the area loaded
  stayed plain meanwhile. It now dresses them four times a second and looks for
  the new pictures half a second, 2 and 5 seconds after the area changes.
- **Cat's Grace was missing from the Effects screen:** its effect (54, one the
  game leaves unused) had no icon in the game's table of effects, and the
  screen shows only effects with one. It now has its paw and its name.
- **Kalzith's scrolls cast their spell instead of teaching it:** the game
  teaches only from scroll objects numbered 1400 to 1499, and his were 1001 to
  1006. They are now 1440 to 1445; scrolls bought before are renumbered.
- **Figures' shadows fell the wrong way:** they lay toward the lower left, while
  the walls', bones' and stones' shadows on the maps fall toward the lower right
  (the light comes from the upper left). They now fall the same way.
- **Kalzith's and Semyon's Look box** sometimes lacked the HP, AC and THAC0
  lines: the Ledger only looked among the map's first 256 things, and the game
  numbers them anew, sometimes past that.
- **The slave pens broken by Kalzith** (in this pull request's earlier
  builds): Kurzak vanished after leading the party in, people were missing,
  Merzol didn't stop the party, the doors' "pick the lock" and "knock" and the
  main door's "Summon Kurzak!" were gone and the water jug couldn't be filled.
  Kalzith was put in among the pens' people and their scripts, moving what came
  after him; he now comes after everything of the game's. A game whose party
  has already been in the pens with an earlier build keeps the damage: start
  a new game, or load a save from before the pens.
- **Kalzith's scrolls taught the spell before their own** (Flame Arrow for
  Haste, Grease for Magic Missile...). Ones already bought or in his stock are
  put right by the Ledger.
- **"Who are you?" hung the game** when asked of Kalzith.
- **Pickpocketing said "won't get another chance" to everyone** in a new game
  with the same party: the last game's tries were remembered.
- **Figures taking extra steps after their turn in a fight:** to have figures
  drawn again with their shadows, the Ledger marked them "changed", which in a
  fight could set one walking again after its turn (in this pull request's
  earlier builds). The view is now drawn again whole instead.
- **"Killed" lines for everyone in an area the party left:** walking from the
  slave pens into the arena logged most of the pens as "is killed (7261 XP)".

### Pull request #13 ([merged 2026-10-02](https://github.com/daaki85/darksun-companion-mod/pull/13))

**Added**
- **The Release workflow can be run by hand**, making the version's tag.

### Pull request #12 ([merged 2026-10-02](https://github.com/daaki85/darksun-companion-mod/pull/12))

**Added**
- **Release 1.0.0:** the version, its release notes, and a workflow that
  builds the release zip.

### Pull request #11 ([merged 2026-10-02](https://github.com/daaki85/darksun-companion-mod/pull/11))

**Added**
- **Cat's Grace looks like itself:** its own icon (a lean, fox-like cat's face
  on gold) and its own description in the spell box, instead of Flaming
  Sphere's.

**Fixed**
- **The slave pens' gear given twice** (a second short sword on Kurzak after
  his was lifted, two Leather Chest Armor +1 on Legcrusher) to a game loaded
  after it was given: none of it is given where it is already in the game.
- **Prices:** Leather Chest Armor +1 is worth 3000 (it was 10), the Cloak of
  Protection +1 5000 and the Rings of Protection +1 5000, as magic items;
  ones already in a game are repriced.
- **Dinos takes the vulture as soon as a fight is over** (he wouldn't until the
  party rested): the Ledger now reads the game's own combat flag.
- **Thieves' Tools can't be used in a fight**, only out of one.
- **The dice log and the Dialogue tab keep up with the newest lines** (they
  stopped following them, and lines that came while another tab was open
  were out of view); scrolling up to read back still holds the place.
- **The bone scale set added twice** to a game loaded after it was added: it is
  now added only where none of its pieces is.
- **No more log lines for the Ledger's items** handed out (the slave pens'
  gear, the bone scale set): they're there to be found.
- **The Bone Helm** can only be worn by those who can wear bone scale armour
  (not thieves).

**Changed**
- **Getting started:** open the Ledger first, pick the options, then **Start
  the game** from it.

### Pull request #10 ([merged 2026-10-02](https://github.com/daaki85/darksun-companion-mod/pull/10))

**Fixed**
- **Half-giants' two-handed weapons in one hand:** the rule didn't take
  effect (the helper looked for the character on show in the wrong place).

### Pull request #9 ([merged 2026-10-02](https://github.com/daaki85/darksun-companion-mod/pull/9))

**Added**
- **Rule change: thief skills from AD&D's table.** A skill is AD&D's average
  for the thief level, plus the race's adjustment, plus Dark Sun's DEX
  adjustment (AD&D's table to 19, the Dark Sun rules' to 22). The game added 4
  a level to a base of its own and used a DEX formula, which gave a 3rd-level
  thief move silently and hide in shadows 10 to 20 points too high. Rangers'
  two chances take the same adjustments.
- **The bone scale set:** where the Bone Scale Chest Armor is found, its arm and
  leg pieces (the game's own, never placed) and a new Bone Helm, coloured to
  match, are found with it.
- **Rule change: half-giants wield two-handed weapons in one hand,** with a
  shield or a light weapon in the other (the game's rule against two heavy
  weapons still stands).
- **Names in colour in the dice log:** each party member's in a colour of
  their own, monsters' in red, bold, all at 4.5:1 contrast or more.

**Fixed**
- **A game that stops with an error** leaves its message on screen (DOSBox
  waits for a key instead of closing), and the dice log says how DOSBox
  closed, telling a crash of DOSBox's own apart.
- **Picking a pocket after loading a save:** a try made after the save (the
  thief caught) is forgotten when it's loaded, so that person can be tried
  again.
- **XP taken away and given back between areas** (the game does it as the
  party moves on) is no longer logged as a loss and a gain; a loss that stays
  is logged after a minute.
- **A monster's AC in its Look box** could be an earlier fight's creature's
  (the game reuses creature records): a slig in the first arena fight showed
  the opening fight's Defiler's AC −9. The Ledger now forgets monsters' ACs
  when a new fight begins.

**Changed**
- **The Options tab scrolls** when the window is too small to show it all.
- **Options:** the Ring +1, picking pockets and the thieving tools button sit
  under Rule changes, with the other changes to play.

### Pull request #8 ([merged 2026-10-02](https://github.com/daaki85/darksun-companion-mod/pull/8))

**Added**
- **Rule change: levels up to 10.** Every class can reach 10th level, at
  AD&D's XP (the game stops at 9). The game's own tables and formulas give
  the rest: hit points, THAC0, saves, spell slots (still no higher than 5th
  level), thief skills, a gladiator's armour bonus, a preserver's new spell
  and a psionicist's new power. Thieves roll their 10th hit die (the game
  would give them a psionicist's fixed +2).
- **Gear for the slave pens' bosses** (with the Ledger running, given once a
  game):
  - Kurzak: a metal Short Sword (1d6, a new item type; a thief can lift it)
    and a leather Helm;
  - Legcrusher: Leather Chest Armor +1;
  - Pehtucl: a Cloak of Protection +1 (a new item type: +1 AC and +1 on saves,
    as the ring) and a Ring of Protection +1 (a thief can lift it).
- **Rangers hide in shadows and move silently too** (the stealth rule), with
  AD&D's ranger chances: the full chance outdoors and half indoors, the
  reverse of thieves. Their attack from behind is +2 to hit and ignores the
  target's DEX and shield, but is no backstab. Their two chances show on the
  inventory screen where a thief's MOVE and HIDE go, and on the Characters
  tab.
- **Item icons of their own** for the Short Sword (a shorter blade), Leather
  Chest Armor +1 (fire), the Cloak of Protection +1 (violet) and the two Rings
  of Protection +1 (Pehtucl's violet, the arena's fire), made from the game's
  plain ones. The launcher writes a copy of the game's objects file with them
  in its own folder; the game folder is untouched.

**Changed**
- **Thief skills: no equipment penalty.** The game took 5 to 10 off some
  thief skills for anything in the legs slot, the quiver or either hand
  (whatever it was); it no longer does in games started with the dice log.
- **The inventory screen shows hide in shadows** in hear noise's place (which
  one script check uses); the Ledger's own screens show both.
- **Pick pockets lifts a short sword** too, though it weighs more than other
  small things.

### Pull request #7 ([merged 2026-10-01](https://github.com/daaki85/darksun-companion-mod/pull/7))

**Added**
- **Rule change: AD&D's two-weapon penalties.** A non-ranger with a melee weapon
  in each hand attacks at −2 with the main hand and −4 with the off hand, offset
  by the DEX reaction adjustment.
  - No penalty for one weapon, a two-handed weapon, a weapon and shield, or a
    ranger.
- **Rule change: the spell save.** Spells are saved against with the spell save,
  not petrification/polymorph.
- **Rule change: DEX instead of a doubled d20.** On saves against fire, cold and
  electricity, the DEX defensive adjustment counts instead of a doubled d20. The
  game's own dormant AD&D code does the work.
- **Cat's Grace**, a new 2nd-level wizard spell in Flaming Sphere's place.
  - +1d6 DEX, at most 24, working exactly as Strength does for STR.
  - Untick the rule and Flaming Sphere is back.
- **REAC and DEF on the inventory screen.** REAC (the DEX reaction adjustment)
  sits beside SP; DEF (the defensive adjustment) sits on the AC line.
- **Rule change: hiding in shadows to backstab.** A thief whose turn comes with
  no enemy beside them rolls hide in shadows (half the chance in daylight),
  then move silently. If both succeed, their next attack that turn is from
  behind, and a backstab with a weapon that can.
  - Daylight goes by the map: outdoors, or on maps with buildings, by the
    floor under the thief.
  - The game itself never rolls hide in shadows.
- **The cooked vulture quest.** Take the cooked vulture to Dinos in the slave
  pens: he cooks it for the party, who eat with him. Each member gets 100 XP
  and a full rest (HP, PSP, spell slots), and the vulture is used up.
- **32 new entries in the game's item name table**, for the Ledger's own items.
  The Ring of Protection and Thieves' Tools no longer borrow the game's entries:
  the game's "Rest icon" label is back.

**Changed**
- **Turn pop-ups in the game are off by default**, and have three levels: at the
  least (only what came of each attack and spell, no dice), in short, or in
  detail.
- **Spell slots** (on the USE screen and the Characters tab) only show the spell
  levels the character can cast. More levels appear as they level up. The game
  gives WIS bonus slots at levels a character can't use yet, and those are no
  longer listed.

**Fixed**
- Item names numbered past 255 were read wrongly by the Ledger (for example,
  Serpent Boots).

### Pull request #6 ([merged 2026-09-30](https://github.com/daaki85/darksun-companion-mod/pull/6))

**Fixed**
- **Boots gave no extra move.** The rule looked at the wrong equipment slot (the
  feet are slot 13, not 12).

**Changed**
- README screenshots retaken (move silently, boots, Thieves' Tools, Options).

### Pull request #5 ([merged 2026-09-30](https://github.com/daaki85/darksun-companion-mod/pull/5))

**Added**
- A **Give thieving tools now** button on the Options tab.
- **Thieves' Tools** get a name of their own and a leather satchel's picture
  instead of a key's.

**Fixed**
- The arena ring, and the backpack cell the thieving tools went into.
- Only one set of tools per thief.
- Long lines on the Options tab wrap to the window.

### Pull request #4 ([merged 2026-09-30](https://github.com/daaki85/darksun-companion-mod/pull/4))

**Added**
- **Picking pockets:**
  - press P in a conversation, with a thief leading;
  - small things only;
  - a move silently roll decides whether a fumble is noticed;
  - a few coins when there's nothing else to take.
- **Thieving tools:** every thief starts a new game with a set. Pick them up and
  click someone to try their pockets.
- **Ring of Protection +1**, found on the Tied-up Prisoner in the arena.
- Items named for the rule changes ("Helm (AC 1)", "Boots (+1 Move)").
- **Thief skills as they stand:** equipment penalties and effects, in the game
  and in the Ledger.
- **Start the game** from the Ledger's window, and a triple-size game window.

**Fixed**
- Fights restarting or crashing after a pop-up's Continue.
- The arena's opening show.
- The Announcer's name being replaced by one learned mid-fight.

### Pull request #3 ([merged 2026-09-30](https://github.com/daaki85/darksun-companion-mod/pull/3))

**Added**
- **In the game:**
  - THAC0, saves and thief skills on the inventory and View Character screens;
  - spell slots on the USE screen;
  - each turn's rolls in the game's own window, with monsters' turns in a
    pop-up of their own;
  - monsters' defences in the Look box.
- **Spells tab:** what every spell and psionic power does.
- **Launchers:** one for the game alone with the in-game additions, and one for
  the game and the Ledger together. DOSBox runs in a window, with a choice of
  size.
- **Script decoder:** every thief and ability check in the game's scripts.
- **The first rule changes:** helms give AC 1; boots give a move more in a fight.
- **Saving throws** with each modifier named.
- **THAC0** shown with each weapon, fresh on every redraw.
- The Ring +1 (+1 AC and saves).

**Changed**
- No packaged .exe: the .bat files offer to install Python instead.

### Pull request #2 ([merged 2026-09-29](https://github.com/daaki85/darksun-companion-mod/pull/2))

**Added**
- The game's own **portraits and font**, read from your install at run time.
- **A Characters tab** laid out like the game's View Character screen.
  - Each character's equipment by slot.
  - Effects with rounds or charges left.
  - Spell slots.
- **Spell detail in the dice log:**
  - damage formulas, durations, and what a save does;
  - rules for 20 more effects;
  - healing, Magic Missile and Slay Living dice labelled;
  - Dispel Magic per effect.
- **Thief skill rolls**, with what each chance is made of.
- **Psionics:** powers named, PSP spent logged, magic resistance changes.
- **Saves:** the chance to save, and what the save left.
- **Dialogue:** the reply you picked, and named speakers.
- **The log at a glance:** round headers, hit chances, HP left, and a details
  switch.

### Pull request #1 ([merged 2026-09-28](https://github.com/daaki85/darksun-companion-mod/pull/1))

**Added**
- **The party viewer**, reading Shattered Lands' character records live.
- **The dice log:**
  - attack bonuses, weapons, saving throws, spells and buffs;
  - kills and XP, weapon breaks, level-up HP and AC make-up;
  - attacks from behind and backstabs (with the damage multiplier);
  - each round's initiative order and how each score was made up;
  - the two-weapon adjustment, and character creation rolls.
- **A dialogue tab.**
- **Accessibility** (AODA / WCAG 2.0 AA):
  - contrast checked in tests;
  - text size controls;
  - full keyboard access;
  - logs you can save.
- Double-click launchers and a step-by-step Windows guide.
- The name *Templar's Ledger*, and a window in the game's colours.
