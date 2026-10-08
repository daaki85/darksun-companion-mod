# Templar's Ledger: development

How Templar's Ledger works inside: the patched game and its helper, what's known
of the game's data, the tools for mapping it, and how each part of the
[README](README.md) is done.

## How the dice log works

Every roll in the game goes through one function, Borland C++'s `rand()`.

1. When you start the game with the dice log, the launcher writes
   `dos\DSUNLOG.EXE`: a copy of the game's `DSUN.EXE` with a few small changes
   (`dscompanion/gamepatch.py`). The start of `rand()`, the end of the saving
   throw, the end of the AC calculation, the start of the routine that fills
   the dialogue window and the start of the message box routine become
   `INT 60h` to `64h`, the inventory screen's panel calls `INT 65h`, the
   combat loop `INT F1h`, the USE screen `INT F2h`, the View Character screen
   `INT F3h`, the end of the window redraw `INT F4h`, the Look box `INT F5h`
   and `INT F6h`, the start of a monster's turn `INT F7h` (see In the
   game; that one is in overlay code, which the game moves or unloads to load
   the dialogue window's, so the helper puts its way back in a stack frame the
   game's overlay manager fixes up, rather than returning to a stale address:
   that used to restart a fight, or stop the game with "Stack overflow!"), and the places where AC and a saving throw's modifiers are added up
   `INT F8h` and `INT F9h` (for [the Ring +1](README.md#new-items), helms and
   [rings and cloaks of protection](README.md#rings-and-cloaks-of-protection)), each
   weapon's line on the inventory screen `INT FAh`, and the start of a round's
   movement `INT FBh` (for boots), a key the conversation window doesn't know
   `INT FCh` and an item used on the map `INT FDh` (for
   [picking pockets](README.md#picking-pockets)), the two-weapon adjustment `INT FEh`
   and the doubling of a save's d20 `INT F0h`, Cat's Grace `INT EDh`-`INT EFh` and a hidden thief's attack `INT EAh` and the class level cap `INT E7h` and a thief's hit dice `INT E6h` and `INT E5h` and the thief skills `INT E4h` and two-handed weapons `INT E3h` and the Tome of Understanding `INT B9h` and Cat's
   Grace's description and icon `INT E2h` and `INT E1h` (for
   [rule changes](README.md#rule-changes)), and
   where the game makes room for its name table and reads it in `INT ECh` and
   `INT EBh` (for [new item names](README.md#new-items)), and its item type table
   `INT E9h` and `INT E8h` (for [the new items](README.md#new-items)), and
   the start of the routines drawing the map's floor `INT E0h` and `INT DFh`
   and of two that draw a rectangle of it again `INT DEh` and `INT DDh` (for
   [shadows](README.md#shadows)), and where the main loop asks where the pointer is
   `INT DCh` (for [scrolling the map](README.md#scrolling-the-map) and the
   [dust](README.md#dust)), and the start of the routine finding what is under the
   pointer `INT DBh` (for [choosing an enemy](README.md#choosing-an-enemy-tab-enter-and-the-rings)), and
   the end of the routines filling an item's box `INT DAh` and working out a
   thief skill's chance `INT D9h` (for a cloak's, boots' and belt's bonuses,
   see [rule changes](README.md#rule-changes)), and in the save and load window's
   events, where a key and a button it has no use for go, `INT D8h` and
   `INT D7h` (for [more saves](README.md#more-saves)), and in the routines that
   destroy an item hit by acid or a corroding touch `INT D6h`, `INT D5h` and
   `INT D4h` (for [items saving against acid](README.md#items-saving-against-acid)), and in the scripts'
   random command `INT D3h` (for [searching junk, hay and wardrobes](README.md#searching-junk-hay-and-wardrobes)), and where View Character adds the bracket after the XP for the next level `INT D2h` (to name the class). The
   copy keeps 29 characters rather than 19, deletes the one chosen in the
   roster and counts a New character as Okay (see
   [more characters](README.md#more-characters)), lets Enter load only a save that is
   there (see [more saves](README.md#more-saves)), and also allocates a bigger buffer for the game's scripts (11,776 bytes
   rather than 10,000, for
   [Dinos and the Trustee](README.md#what-dinos-and-the-trustee-say-about-them)), and
   looks for its data files in the current folder rather than next to itself. The helper also hooks DOS's `INT 21h`, to
   open the launcher's copies of `SEGOBJEX.GFF`, `RESOURCE.GFF` (see
   [Item icons](README.md#new-items)), `RGN1C.GFF`, `RGN1E.GFF`, `RGN08.GFF` (see
   [new items](README.md#new-items)), `GPLDATA.GFF` and `RGN29.GFF` (see
   [Kalzith](README.md#kalzith), [Semyon](README.md#semyon),
   [Dinos and the Trustee](README.md#what-dinos-and-the-trustee-say-about-them) and
   [no manual check](README.md#no-manual-check)), the mouse driver's `INT 33h`
   (for [scrolling the map](README.md#scrolling-the-map)) and the keyboard's `INT 16h`
   (for Tab and Enter). DOSBox runs it from the game folder, so
   it uses your saves as usual.
2. `dos\DSCLOG.EXE` (source in `dos\dsclog.asm`) is a tiny DOS program loaded
   into upper memory before the game, so the game loses no memory. It answers
   those interrupts. Its `rand()` returns exactly the numbers the original
   would and also records each call, what code called it, and that code's
   arguments (dice count and sides, THAC0, AC...) in a ring buffer. Others
   record the final saving throw total, the AC the game uses, and the text
   of dialogues and messages (in a second buffer); the rest draw the in-game
   additions and make the new items and the rule changes count.
3. Templar's Ledger finds the buffer in DOSBox's memory and reads it every 50 ms.
   It works out what each roll was for from the code that asked for it, and
   reads the rest (names, weapons, spells, effects) from the game's own data.
4. To keep bursts of unimportant randomness from crowding out the rolls that
   matter, the helper only records calls from code it knows how to label,
   unless **Show unlabelled rolls** is ticked.

Because the replacement produces identical numbers, the game plays exactly as
it would without it, apart from what you choose on the Options tab (picking
pockets, the [rule changes](README.md#rule-changes)), the Ledger's other
additions (the new items and the Ring +1, the cooked vulture, Kalzith, Semyon,
what the party wears, shadows, dust, rings, Tab and Enter, scrolling) and the
fixes always in the patched copy: no equipment penalty on thief skills (see
[Thief skills](README.md#how-the-game-works-out-thief-skills)), the roster's DELETE and New characters counting
as Okay (see [More characters](README.md#more-characters)), and no manual check
(see [No manual check](README.md#no-manual-check)).

Limitations:
- Only the GOG release (`DSUN.EXE` of 611,408 bytes) is supported. With
  another version the launcher starts the game without the dice log and says
  why.
- Outside combat, the thief skill, trap and ability checks, the character
  creation rolls and searching junk, hay and wardrobes are labelled; other
  rolls there (for example treasure or
  random encounters) show up only with **Show unlabelled rolls**, as raw
  numbers.
- A save-file load from the main menu is recognised, so the spells already
  active in it aren't reported as new. Loading a save of the same party in the
  middle of play isn't, and its effects may be listed as if just cast.
- Dialogue speakers are portrait numbers until the log learns their names or
  you name them (see above): the game doesn't keep a name with the dialogue.
  A learned name is the creature the conversation was started on, so a scene
  in which one face speaks for someone else would get that someone's name.
- Weapon breaking was checked against the game's code, and the check's rolls
  were seen in play, but no weapon happened to break during testing; the
  game's own "is broken !" message is logged either way.


## What is known

A save file (`SAVEnn.SAV`) is an SSI **GFF** archive. Two of its chunks hold
the party:

- **`SAVE` chunk 5, creature table.** 58-byte records (`0x3a`) for everyone in
  the current region, party first.
- **`SAVE` chunk 6, character sheets.** 71-byte records (`0x47`).

The game keeps the same records in memory, with the party's sheets one after
another. Old copies of a record can linger elsewhere in memory, so the viewer
prefers the sheet at the party's stride position. Offsets are relative to the
start of each record. The evidence comes from five save files covering three
parties, plus the in-game View Character screens.

| Record | Offset | Type | Field | Evidence |
|---|---|---|---|---|
| creature | `+0x00` | s16 | Current HP | ≤ max HP everywhere; wounded characters lower |
| creature | `+0x02` | s16 | Current PSP | ≤ max PSP everywhere |
| creature | `+0x06` | u16 | Entity ID (`0x80nn` for the party) | same value in the sheet at `+0x10` |
| creature | `+0x1a` | s8 | Base AC, before armour and DEX | 10 for humanoids, 5 for the thri-kreen; the AC the game shows is worked out from this |
| creature | `+0x1b` | u8 | Movement | 12, 15 for the thri-kreen; each round of a fight gives Move × 10 movement points |
| creature | `+0x1f` | u8 | THAC0 | matches the AD&D warrior table at levels 3, 4, 7 and 8 |
| creature | `+0x22` | u8 ×6 | STR DEX CON INT WIS CHA | same as the sheet |
| creature | `+0x28` | str 18 | Name | |
| sheet | `+0x00` | u32 | XP | matches the game |
| sheet | `+0x04` | u32 | For monsters, the XP they're worth; for the party, usually equals XP | matches the XP the party gets for a kill |
| sheet | `+0x08` | s16 | Max HP | |
| sheet | `+0x0a` | s16 | The hit points rolled (or gained) for every class level, added up | the game's level-up code (DSUN.EXE 87250h) adds each new level's to it; max HP = this ÷ the number of classes + CON's bonus |
| sheet | `+0x0c` | s16 | Max PSP | worked out at each level-up (873B2h): CON, INT and WIS bonuses, and for a psionicist +10 a level after the first, plus 1 a level for each WIS point above 15 |
| sheet | `+0x10` | u16 | Entity ID | links the sheet to its creature record |
| sheet | `+0x18` | u8 | Race: 1 Human, 2 Dwarf, 3 Elf, 4 Half-elf, 5 Half-giant, 6 Halfling, 7 Mul, 8 Thri-kreen | ability modifiers fit; 2, 6 and 7 from the character creation code's race table |
| sheet | `+0x19` | u8 | Gender: 1 male, 2 female | |
| sheet | `+0x1a` | u8 | Alignment: 1 LG, 2 LN, 3 LE, 4 NG, 5 TN, 6 NE, 7 CG, 8 CN, 9 CE | 1, 5, 7 confirmed in game |
| sheet | `+0x1b` | u8 ×6 | STR DEX CON INT WIS CHA | |
| sheet | `+0x1d` | u8 | CON (among the abilities at `+0x1b`); sets the least a level's hit point roll counts for | read by the game's level-up code |
| sheet | `+0x21` | u8 ×3 | Class: 1–4 Cleric, 5–8 Druid, 9 Fighter, 10 Gladiator, 11 Preserver, 12 Psionicist, 13–16 Ranger, 17 Thief (0 = none); each four is air, earth, fire, water | 2, 7, 8, 9, 11, 12, 13, 14, 17 confirmed in game; the elements from the spheres in the game's class and spell tables (see Spells and effects) |
| sheet | `+0x24` | u8 ×3 | Level in each class | |
| sheet | `+0x27` | s8 | Base AC for the AC calculation | read by the game's AC code |
| sheet | `+0x29` | u8 | Magic resistance (%) | read by the game's magic resistance check |
| sheet | `+0x2a` | u8 | Attacks per round × 2 | read by the game's combat code |
| sheet | `+0x37` | u8 ×5 | Saves: para/poison, rod/staff, petrify, breath, spell | match the AD&D warrior table exactly |

In memory, the game reaches both tables through far pointers in its data
segment: `DS:0x1665` points to the creature table and `DS:0x1661` to the
sheets (a creature's sheet number is its word at `+0x04`). The data segment
starts with Borland's copyright string at `DS:0x0004`, which is how the viewer
finds the party by itself (`dscompanion/game.py`).

**Items.** A creature's items hang off its record at `+0x08`, `+0x0a` and
`+0x0c`: each is an object number (the object table has a kind, 1 for an item
and 2 for a creature, and an index), the first item of a list, whose own
records then name the next. Items are 21-byte records (`DS:0x165D`), item
types 20-byte ones (`DS:0x1669`, 115 of them, from GPLDATA.GFF):

| Record | Offset | Field |
|---|---|---|
| item | `+0x04` | the next item in the list (9999: the end) |
| item | `+0x08` | a container's contents (an object number), as in a Dead Body |
| item | `+0x0a` | its type |
| item | `+0x11` | where it's worn: 0-13 the game's slots (arm, ammo, missile, right hand, finger, waist, legs, head, neck, chest, left hand, finger, cloak, foot), 14-25 a backpack cell |
| item | `+0x0f` | a spell it carries, one past the spell's number (0: none): readied, the game casts a helpful one on the wearer; the acid's check reads it as the item's "magical power" |
| item | `+0x12` | its name (an entry of the game's name table, 25 bytes each) |
| item | `+0x14` | its plus |
| type | `+0x04` | weight, in tenths of a pound |
| type | `+0x08` | material in the low four bits (wood, bone, stone, obsidian, metal, leather); `0x80` spares a weapon the material's to-hit penalty |
| type | `+0x0c`, `+0x0d`, `+0x0e` | damage dice: sides, count, bonus |
| type | `+0x0f` | `0x80`: counts for AC |
| type | `+0x12` | its AC (on top of the item's plus) |

Free item records and free objects are kept in lists (`DS:0x4D76`,
`DS:0x4D72`), which is how the Ledger adds [the Ring +1](README.md#new-items) and
Kalzith's scrolls as the game would.

Also seen: per-region `RGnn` chunks hold a combined creature record, sheet and
inventory for each character. Region *nn* uses `SAVE` chunks *nn*×60+1 and up
for its own copy of the region state.

The saved characters are `CHAR` chunks of `CHARSAVE.GFF`, 314 bytes each: the
creature record at `+0x0A` (its name at `+0x32`, its status at `+0x26`), the
sheet at `+0x4E`, then its items. The game's own party, which START GAME uses
when no party has been made (Cermak, Cilla, Gerakis and K'ratchek), is objects
300, 307, 308 and 313 in `SEGOBJEX.GFF`: a creature record and a sheet each,
already Okay, with no items. The game gives them their gear as the game
starts (see [the game's own party](#the-games-own-party)).

**Spells.** They are numbered 0 to 137: 0 to 68 wizard spells (0 is Armor, the
first of the 1st level; its scroll is Old One-Eye's), 69 to 137 priest
spells, a 7-byte record each from 0 (its level first, its name's DS offset at
+5). What the party knows is a table of 138 bytes for each member, 1 for a
spell known, through the far pointer at `DS:0x132A` (in a save, `SAVE` chunk
19).


## Reading the game's memory

DOSBox keeps the emulated PC's RAM in one block of its own process memory. The
tool finds that block by looking for the BIOS date string DOSBox writes at
guest address `0xFFFF5` ("01/01/92"), and checks it against the interrupt
table at guest address 0. After that, reading the game's memory is a plain
`ReadProcessMemory` at `block + guest address`. Dark Sun is a 16-bit real-mode
program, so a `segment:offset` address is simply `segment × 16 + offset` in
guest memory. If detection fails on an unusual DOSBox build, you can pass the
block's host address with `--host-base`.


## Development

```
python -m unittest discover -s tests
```

`tests/test_dsclog.py` runs the helper's interrupt handlers in a CPU emulator
when `unicorn` is installed (`pip install unicorn`), and is skipped otherwise.
After changing `dos/dsclog.asm`, rebuild the helper with
[NASM](https://www.nasm.us/):

```
nasm -f bin -o dos/DSCLOG.EXE dos/dsclog.asm
```

The header's signature (`DSCLOGvY` now) goes up whenever the helper and the
Ledger must change together (`HDR_SIG` in `dscompanion/dicelog.py`), so a
Ledger never talks to an older helper.

The post-game check that keeps an error on screen for the crash report is
built the same way:

```
nasm -f bin -o dos/GAMEEND.COM dos/gameend.asm
```

### From a command prompt

What the `.bat` files do, from a command prompt (`dscompanion` is the
program's internal name):

```
python -m dscompanion launch                        # start the game with the dice log, and the viewer
python -m dscompanion view                          # the viewer only
python -m dscompanion play                          # the game with the in-game additions, no viewer
python -m dscompanion dicelog                       # the dice log in the command prompt
python -m dscompanion save C:\path\to\SAVE01.SAV   # the party stored in a save
python -m dscompanion processes                     # is DOSBox found?
```

If more than one DOSBox is running, add `--pid <number>` (from `processes`).

### Mapping memory

For Shattered Lands the party is found automatically. The steps below are for
mapping new fields, or for other layouts:

1. Type a party member's name under **Locate by name** and press **Search**.
2. Select the hit that is the character's record and press **Assign**.
   In the hit list, the record shows its name followed by dots, since binary
   data follows the name. A copy in a text buffer is followed by more text.
   Slots 2–4 follow automatically if the party's records sit next to each other
   in memory, as they do in save files. Otherwise assign each slot by name.
3. The **character sheet** (XP, classes, levels, saves) is found automatically:
   it carries the same ability scores and entity ID as the creature record.
4. **Save layout** (beside **Search**) stores the addresses. They may change when you load a save
   or restart the game. If a slot starts showing garbage, locate it again.

The **Record bytes** panel shows the raw record. Bytes that change light up
orange, and clicking a byte decodes it as u8/s8/u16/s16/u32. Use it to map
fields that aren't known yet. Watch a byte change as you take damage, spend
PSP, or equip armour, then add it to `layouts/shattered_lands.json` and press
**Reload layout**.

### Command-line mapping tools

```
python -m dscompanion find-text Daaki               # hex dump around each hit
python -m dscompanion dump 0x1a2c 128               # hex dump an address
python -m dscompanion search u8 23 --near 0x1a2c    # Cheat-Engine-style value search
python -m dscompanion next 17                       # ...narrow after the value changes
python -m dscompanion next decreased                # also: changed, unchanged, increased
```

## How each part works

For each part of the README, how it's done: where the patched game calls the
helper (DSCLOG), and what the Ledger reads and writes. The heading names the
README's section.

### The Dialogue tab

([In the README](README.md#the-dialogue-tab).)

The game keeps the clicked reply's row at DS:1F0A while it flashes it; the log
reads the reply's text from the game's own list.

### Two weapons: AD&D's penalties

([In the README](README.md#two-weapons).)

How: the game reads the attacker's DEX adjustment when it works out the
two-weapon adjustment; the helper takes over from there (`INT FEh`) and gives
AD&D's for the hand the attack's weapon is in.

### Searching junk, hay and wardrobes

([In the README](README.md#searching-junk-hay-and-wardrobes).)

How: the scripts' random command has a routine of its own in the game; the
patched game has DSCLOG look in there (`INT D3h`), which records the roll, its
range, where the running script is (which tells the three searches and their
damage rolls apart) and the three counts (`dscompanion/searches.py`). Tested
in play: a haystack search in the slave pens logged `0-10 = 7, an old, soiled
loincloth (the party's 2nd find of 6 in hay)`, as the game's own message said.

### Thief skills from AD&D's table

([In the README](README.md#thief-skills-from-adds-table).)

How: where the game's thief skill routine adds 4 a level, the helper
(`INT E4h`) puts AD&D's number for the level in place of the game's base and
level, adds the DEX table's, and jumps past the game's DEX formula to its
armour and effects. The Ledger's screens and the inventory screen's panel
work the chances out the same way.

### Hiding in shadows to backstab

([In the README](README.md#hiding-in-shadows-to-backstab).)

How: the patched game's item box (`INT DAh`, where it has drawn the name) asks
the helper, which draws the line with the game's own text routine when the
item's type is worn as a cloak, on the feet or as a belt; and at the end of the
game's thief skill routine (`INT D9h`, where it returns the chance, armour and
effects counted) the helper adds the belt's 5 to picking pockets and opening
locks for a thief wearing one.

How: the Ledger rolls both when the turn passes to the thief and tells the
helper, which, where the game has just worked out whether an attack is from
behind and a backstab (`INT EAh`), makes the hidden thief's next one so, by
the game's own conditions for a backstab (a thief, in melee, a weapon of
weight 40 or less).

### Spells saved against with the spell save

([In the README](README.md#spells-saved-against-with-the-spell-save).)

How: the Ledger writes the game's own table that turns a spell's kind of save
into one of the five (a table of words at DS:1E75h, read afresh for every
save), and puts it back when the rule is unticked.

### Fire, cold and electricity: DEX instead of a doubled d20

([In the README](README.md#fire-cold-and-electricity-dex-instead-of-a-doubled-d20).)

How: the helper does the save's doubling (`INT F0h`) only while this rule is
off, and the Ledger marks the fire, cold and electricity spells with the game's
own "can be dodged" flag (bit 40h of the spell's category word), which no spell
has, so the game's save routine adds the DEX defensive adjustment from its own
table.

### THAC0, saves and thief skills

([In the README](README.md#thac0-saves-and-thief-skills).)

How: the patched game calls the helper (`INT 65h`) just after the panel's
weapon lines; the helper prints the lines with the game's own text routine,
whose address, like the selected character, it reads from the game's code
around the patch (overlays move, so nothing is fixed in advance). The View
Character screen does the same through `INT F3h`, called while it draws the
character's panel, and the routine that lists the weapons through `INT FAh`
after each one. The Ledger keeps the numbers in the helper's memory, with the
time it last did: older than 5 seconds, the helper shows the sheet's numbers
instead. Before a screen is drawn, the helper asks the Ledger to update them
and waits for its answer, half a second at most. Nothing else in the game changes.

Which class levels up next, on View Character: the game looks up the XP for
each class's next level in its tables and shows the lowest. Where it adds the
closing bracket, the helper (`INT D2h`) finds which classes that number
belongs to and adds their letters first.

### Each turn's rolls

([In the README](README.md#each-turns-rolls).)

How: the patched game calls the helper (`INT F1h`) in its combat loop, right
after the call that may pass the turn on. When whose turn it is has changed,
the helper counts it and waits up to a third of a second for the Ledger,
which writes the summary into the helper's memory; the helper then feeds it to
the game's dialogue window the way the game's scripts do for a narration
(the emblem, the text, "Press continue"). If the Ledger isn't running, or the
box is unticked, the game doesn't wait at all. (INT 66h-6Fh can't be used: the
game calls those itself, looking for sound drivers.)

### What hurts a monster (the Look box)

([In the README](README.md#what-hurts-a-monster-the-look-box).)

How: the patched game calls the helper (`INT F5h`) where the box has drawn its
first status rows; the helper asks the Ledger (as for each turn's rolls), and
prints the lines with the game's text routine. `INT F6h`, at the end of the
routine that closes the box, shows the whole description.

### No manual check

([In the README](README.md#no-manual-check).)

How: the dragon's question is the game's script 20, which script 120 runs (a
call into another script, command 14h) when the party leaves the warrens
(region 28h) until bit 12 of the game's variable (135, 73) is set. The right
answer goes on to script 86 at 1087, which sets 255 in the variable (7, 4)
and, in region 28h, that bit. In the Ledger's copy of the scripts
(`dscompanion/manualcheck.py`), script 20 does just that and ends: the same
start (offset 1, its one entry in the game's table of entry points), no words
and no question. It is replaced only if it is the dragon's (its
`" word on page "` line).

### Weapon specialization

([In the README](README.md#weapon-specialization).)

How: the kinds are kept in four bytes of each character's own record that the
game never uses (+14h to +17h), so saves and the saved-characters roster keep
them. The helper adds the bonuses and attacks where the game makes a weapon
attack (`INT D1h`, `INT D0h`), on the DAM lines (`INT CFh`, `INT CEh`), runs
the creation pages (`INT C8h` to `INT C3h`, windows 3014 to 3019 in the
Ledger's copy of `RESOURCE.GFF`), calls the game's psionic pop-up in weapon
mode at a level gained (`INT C2h`, then `INT C1h` to `INT BCh` in the pop-up,
window 3021), and prints the Effects screen's lines (`INT BBh`).
A missile weapon's attacks a round are its item type's (+0Bh, in halves: a
bow 4, the rest 2), not the character's (sheet +2Ah) as in melee; `INT D1h`
raises them to a specialist's (`MISSILE_RATE`, by the fighter, gladiator or
ranger level; a grand master one more; a kind not chosen, from 7th level, a
specialist's a band lower), and the Ledger's Characters tab does the same
(`specialize.missile_attacks`).
Every ranger's expertise with the bow is in `SPEC_OF_SHEET` (`specialize.skill`),
not in its chosen kinds, so `KINDS_ALLOWED` (`restrict.allowed_kinds`) leaves
the bow out of a ranger's choices.

### Class restrictions

([In the README](README.md#class-restrictions).)

How: the helper adds the classes' limits where the game checks an item against
the classes allowed to use it (`INT CDh`), and a multiclass preserver's armour
where the game checks for "No spell use" (`INT CCh`). (`dscompanion/restrict.py`
says the same in Python, for the tests.)
A weapon the character has made its own is left as the game has it, past the
classes' limits (`SPECIALIZED_BACK`, `restrict.specialized_back`): a dual-classed
human's chosen weapon specs once its new class's level has passed the warrior
class's, and a ranger's bow (every ranger has expertise with it, but never
chooses it): a multiclass ranger's always, a human's while a ranger or once past.

### Multiclass hit points

([In the README](README.md#multiclass-hit-points).)

How: the helper divides the die where the game adds a level's hit points to
the sheet's total (`INT CBh`), and shares CON's bonus where the game adds it
to the maximum (`INT CAh`, and `INT C9h` where it takes it off again to work
back to the total when CON changes).

### Hit dice: the better of two

([In the README](README.md#hit-dice-the-better-of-two).)

How: where the game has rolled a level's die (`INT BAh`, in place of the
`mov cx,ax` after the roll, DSUN.EXE 87319h), the helper keeps the first roll
and sends the game back to the start of its roll (872FDh), so both rolls are
the game's own and the dice log sees both; the second time it keeps the
better. Creation goes through the same routine, a die for each starting
level.

### Levels up to 10

([In the README](README.md#levels-up-to-10).)

How: the game holds a class level against 9 in two places, where a character
goes up a level and where View Character shows the XP for the next one; the
helper (`INT E7h`) holds it against 10 instead while the rule is on.

### Items saving against acid

([In the README](README.md#items-saving-against-acid).)

How: where the game works out the number a weapon's d20 must reach
(`INT D6h`), where it skips the roll for armour with no magical power
(`INT D5h`) and where it works out armour's number (`INT D4h`), the helper
gives the easier of the two and records the check for the dice log.

### Bracers of defense

([In the README](README.md#bracers-of-defense).)

How: where the game's AC routine asks the helper about each worn item
(`INT F8h`) and where it starts a saving throw's modifiers (`INT F9h`), the
helper looks at what else the character wears.

### Half-giants' two-handed weapons

([In the README](README.md#half-giants-two-handed-weapons).)

How: the inventory screen checks a weapon type's two-handed bit (+0Fh, 40h)
twice when something goes into a hand: the other hand's ("Two handed weapon in
use") and the one going in ("Need two free hands"). The helper (`INT E3h`)
answers both for the character on show, "not two-handed" for a half-giant.

### Cat's Grace

([In the README](README.md#cats-grace).)

How: the Ledger gives Flaming Sphere (spell 14) Strength's record (range,
duration, whom it can be cast on) and the name, in the game's memory. The
helper sends it to Strength's own code (`INT EDh`), which rolls the 1d6;
gives it an effect of its own (`INT EEh`: number 54, which the game leaves
unused) holding the roll; and, in the routine that works out a creature's
abilities from its own scores and its effects, adds that to DEX the way
Strength's adds to STR (`INT EFh`). When the spell runs out, the game works
the abilities out again without it. A game saved while Cat's Grace lasts and
loaded without the dice log simply ignores the effect it doesn't know.
On the Effects screen, Cat's Grace shows as the game's own effects do: its icon
(the cat's paw), and its name on the bar below when the pointer is over it.
The game's table of effects (6 bytes each, from the load segment + 3F8Dh: a far
pointer to the name, then the icon) has an empty name and no icon for 54, and
the screen shows only effects with an icon; with the rule on, the Ledger gives
54 Flaming Sphere's icon (21014, read as Cat's Grace's) and the spell's name.
The description: the game reads a spell's text from RESOURCE.GFF (chunk SPIN,
the spell's number + 1) into a buffer for the box; after the read
(`INT E2h`) the helper puts Cat's Grace's in, in the game's words for
Strength's. The icon: the launcher writes `dos\RESOURCE.GFF`, the game's file
(only read) with the icon added (number 21900), which the helper has the game
open in place of its own (as `SEGOBJEX.GFF`); where the game's two routines
that read a chunk begin (`INT E1h`), the helper has Flaming Sphere's icon
(21014) read as that one.

A click on an effect's icon on the Effects screen
([In the README](README.md#spells-on-the-effects-screen)) ends it in the game;
with the switch on, a spell's effect is left on: two jumps in the screen's
click handler (DSUN.EXE 7F226h and 7F236h, `effects_click_low` and
`effects_click_high` in `dscompanion/gamepatch.py`) go to its way out instead
of to the routine ending an effect. A psionic power's (spells 8Ah-ABh) still
ends, as stopping it there is how a power is dropped.

### Helms and boots

([In the README](README.md#helms-and-boots).)

How: the helper sets the helm types' AC as the game's AC routine reads it
(`INT F8h`, the Ring +1's place), and adds the move where the game sets a
round's movement, Move x 10 (`INT FBh`).

### The game's own party

([In the README](README.md#the-games-own-party).)

How: the four are objects in `SEGOBJEX.GFF` (32000 to 32003, and 300, 307,
308 and 313 for their figures), a creature record and a sheet each, already
Okay and with no items; the game gives them their gear and spells as it
starts. So the Ledger (`dscompanion/defaultparty.py`) changes them in memory
while the game is new (its first hour, in the arena, as with Thieves' Tools),
each change once, knowing each by name, race and classes together: their
weapon kinds in the sheet's spare bytes, Gerakis's club item made a bone
gythka in its place, Cilla's plain armour given back to the free item list
(her chest armour is alone in its list, which is left empty, as a new list
is), and her byte for spell 0 set in the known-spells table. Seen in play: Cilla's
USE screen lists ARMOR among her 1st-level spells and her inventory has no
chest armour (AC 5); Gerakis holds the gythka and the long sword.

### New items

([In the README](README.md#new-items).)

How: the new items (the slave pens' and the world's, the bone scale set,
Kreenfang) are in the game's data (`dscompanion/dataitems.py`, `worldgear.py`,
`npcitems.py`, `arms.py`): in the
Ledger's copy of `SEGOBJEX.GFF`, each person's or chest's object (its RDFF: the
object's record, then its items, each a child or the next of the one before,
with its type and name as attributes) has the new items after its own, so the
game makes them where it makes the object. Kreenfang is the arena's dead
body's (object 1204) own gythka made +1 and renamed, its name attribute with
it. One Castle Guard, one Undermountain miner and one Magera (Drakejaw's) have
an object of their own (2560, 2561, 2562: copies of their kind's, their record
renumbered), their entity in the Ledger's copies of `RGN1C.GFF`, `RGN1E.GFF`
and `RGN08.GFF` pointing to it. So does the slave pens' weapon rack (2563: the
Lower Castle's rack is the same object 1647; a thing's record has its number
first, a person's at +6), with Thornwall in place of its first bone polearm,
in Kalzith's copy of `RGN29.GFF` (one copy of the pens: with Kalzith off, the
rack's alone). The Elven Leader's Gythka +2 is his own
Gythka +1 (in his pack, object 124, and the item object 2534 his script gives)
made +2. (People of a kind share an
object, so every Tari, Renegade and Wild Mul carries theirs; the caravan's
buried chest is an object the dig's script makes, and has the Boots of
Elvenkind in it.) The Elven Leader's script (46, in
the scripts' copy: `elvenleader.py`) gives the Cloak of Elvenkind (object 2546,
an item object of its own) after the Gythka, as the game's scripts give items
(command 39h, a new item of the object; 25h on the ground when it can't be
carried); Father Garyn's (174: `garyn.py`) gives the Tome of Understanding the
same way, the first time the pith is delivered (flag 625). The tome
(`dscompanion/tome.py`) is a scroll of the game's kind: object 1446, among the
game's scrolls' numbers (1400-1499: its object record the first scroll's, as
only a scroll's kind of object has its box's icon clicked; the picture that
number had, the icon of two objects, moved to 2552), its spell byte one past
176. Clicked, the icon has the game's routine (DSUN.EXE 8B690h) teach a scroll
of those numbers its spell, or a psionic power from 138 to 171; from 172 to 195
it would show "CANNOT LEARN FROM THIS ITEM" and keep the scroll (from 196 on,
the icon can't be clicked). There the helper (`INT B9h`) raises the reader's
WIS, in the sheet and the creature record, writes its message in the game's
buffer, and goes on as for a power taught: the game uses the tome up and shows
it. The short sword, the cloak whose plus counts, the bone helm and the rest
(25: Galefang's, a metal dagger whose class list has the air cleric's
bit, which none of the game's daggers have; then the bone and obsidian great
axes, the metal one's of those materials, and a bone dagger, the only dagger a
water cleric may use) are item types the helper adds
after the game's 115 each time the game reads its table in (`TYPES_EXTRA`; its
weapon kinds by type, `kind_of_type`, cover them too); the Ledger's item names (`dscompanion/names.py`) are entries it adds
after the game's 322 (the game puts the item type's material before the name
when it shows one); and the icons are objects in the Ledger's copy of
`SEGOBJEX.GFF` (`dscompanion/icons.py`), which the helper has the game open
instead of its own (its `INT 21h` hook). Where the game adds up AC and saving
throws, the helper counts the rings and the cloak (`INT F8h` and the save
probes). Shadowseeker's sight is the game's own way with a magic item's spell:
readied, it puts Detect Invisibility on its wielder. In the original game the
rings are plain rings without a name, and the sword, cloak and helm types it
doesn't have: don't load a save that has them without the dice log.

Alagorn's new menu lines are in the Ledger's copy of his scripts
(`dscompanion/alagorn.py`); he knows an item by its picture.
- Scripts 212 and 213 with every story would overflow the script buffer, as
  the [Trustee's](#what-dinos-and-the-trustee-say-about-them) once did, so
  212's clothes are told by a copy of it (script 220), its rings and other
  items by another (221), and 213's weapons by a copy of 213 (222). His talk
  (script 211) calls each part by its offset in its script, so only the
  called script's number changes.
- The added "none carried" check replays the game's own tests with their own
  jump targets: skipping one leaves the game's if/else nesting one level
  short.
- The two Rings of Protection have different pictures, so their one menu line
  joins two queries with "or", as the game's own tests do.
- Each item a menu shows needs a value saying it's carried, and a script has 16
  locals: the weapons menu's six game items, its loop's own and ten new ones
  are one too many, so items past the locals use the Ledger's flags from 784
  on (set afresh as the part starts, as the locals are). The new stories'
  "none left" test is one subroutine they all call.

The icons in the guide's item tables (`docs/items/*.png`) are drawn from the
game's data by `python -m dscompanion.docicons GAME_FOLDER`, from the Ledger's
copy of `SEGOBJEX.GFF` in `dos/` (start the game from the Ledger once first)
and the game's palette: each picture twice its size, the rest transparent.
`docicons.ICONS` names each image's object; a new item needs its line there,
and `tests/test_docicons.py` checks that every icon the guide shows is there.

### Kalzith

([In the README](README.md#kalzith).)

How: he is the game's own kind of person, in the Ledger's copies of three of
its files, which the dice log's helper has the game open instead of the
originals:

- `SEGOBJEX.GFF`: object 1000 (a person's object with the Defiler's picture,
  and a slave's record, Dinos's, with his name and a defiler's class), and his
  scrolls' objects 1440 to 1445 (copies of the game's scroll object, with a
  scroll's picture). The game teaches a scroll's spell only from an object
  numbered 1400 to 1499 (any other it casts); its own end at 1432, and the
  numbers after are pictures, most of them other objects' icons, which the copy
  moves to pictures of their own (2440 to 2445). None of these objects is the
  game's. Scrolls bought with earlier builds (objects 1001 to 1006, which cast
  their spell) are renumbered wherever they are.
- `RGN29.GFF`, the slave pens: an entry setting him in his pen.
- `GPLDATA.GFF`: his conversation (script 218, after the game's 217), its entry
  in the game's table of script entry points (which saves go by), the command
  in the pens' script that runs it when he's talked to, and his portrait
  (portrait 101, a number the game leaves free).

His state is in the game's own flags (760 to 763: met, friendly, cold, his
scrolls given; the game uses flags up to 755), so a save keeps it. The first
time the party is in the pens, the Ledger puts his six scrolls among his
things (from the game's free list, as for [the arena's ring](README.md#new-items)),
once a game. If he is killed, the Ledger marks it (flag 772) and the others
speak of him as dead (see
[Dinos and the Trustee](README.md#what-dinos-and-the-trustee-say-about-them)); after
the party's escape he is gone from the pens with everyone else.

Killed, he leaves one of the scrolls he still had, chosen at random, a Cloak
and a Quarterstaff (the game's own), in his body where he fell, and the Ledger
logs it ("Kalzith leaves: Scroll of Blur, Quarterstaff, Cloak"). The game puts
everything a dead person carried in the body; the Ledger takes the other
scrolls out of it and puts the two in (flag 777, once). He can't carry the two
while he still has scrolls to sell, since his shop offers everything he has.
Once the party has bought all six, his shop isn't offered any more ("Anything
left to sell?" "Nothing. You've bought every scrap of hide I had, and more
takes time I don't have.", flag 778), and the Ledger gives him the two, worn
(flag 776): only while the map is running, so never into an open talk or shop.
(The dice log's helper counts the game's map loop; it doesn't run while a talk,
menu or shop is open.) Killed then, he leaves the Cloak and the Quarterstaff in
his body, as the game does with anything a dead person carried.

He is a slave of the pens like the game's own (his record is Dinos's): attacked,
he turns on the party as they do, and only the guards near him join the fight.

### Semyon

([In the README](README.md#semyon).)

How: in the Ledger's copy of `GPLDATA.GFF`, the command that takes him off the
map when he walks out after the fight (script 5 at 2400, run only from there)
first sets the Ledger's flag 770; the game's other exits don't reach it. The
Ledger sets flag 771 if it ever sees him dead (his record's hit points or
status). The pens' script ends with, "if flag 770 is set, 771 isn't, and he
isn't in his pen yet, make him there", the command the arena's script uses
when he is untied (25h, his object 280), and the command that runs his
conversation (script 219) when he's talked to, with its entry in the game's
table of entry points. Flags 764 and 765 (his own: placed, met) keep the rest,
so a save keeps him.

How: the arena's script 3 moves Scar and his henchman to the pens (5Eh to region
41) when the party reaches the west exit after Scar's plan is agreed. In the
Ledger's copy, the henchman's move (at 1828) becomes a jump past the script's
end, where that move is made, then Semyon's, to a square beside them (74, 68),
if he is recruited (the game's flag 6), not seen dead (771), in the arena and
not against the party (his field 74, the side, not 2); then the Ledger's flag
782 is set and the script goes on where it was. With 782 set, the pens' script
leaves him on the party's side, and his conversation has the breakout's line
instead of his menu, until the escape (the game's flag 503).

His object is the arena's, made for a man who fights beside the party: on the
party's side, and with 0 in a byte where every slave of the pens has 12. In his
pen the pens' script makes him as they are, with the command the game's scripts
use to change someone (40h: his fields 74, the side, to 4, theirs, and 70 to
12), once (flag 779). Attacked, he is then like any of them: he turns on the
party, and only guards near him join the fight; in a fight in the pens he isn't
on the party's side. Like Kalzith's, his commands come after everything of the
game's, which keeps its place.

### What Dinos and the Trustee say about them

([In the README](README.md#what-dinos-and-the-trustee-say-about-them).)

How: in the Ledger's copy of `GPLDATA.GFF`, their scripts (139 and 146) keep
every byte where it was, since the game's jumps go to fixed places. Two
commands become jumps to code after the script's end: the one starting the
menu's part goes to the same command followed by the new questions' flags
(766-769, 773, 774), and the menu goes to a copy of it (the game's own bytes) with the
new questions after its last about someone. Each then jumps back to where the
game's script carries on.

That makes the Trustee's script 10,898 bytes, and the game reads every script
into one buffer of 10,000 bytes (a script that calls into another reads it in
over its own). One of 9,800 bytes ran; one of 10,000 ended with "BAD GPL
EXIT" (the game's own largest is 9,792). So the Ledger's copy of the game
makes the buffer 11,776 bytes where it is allocated (`push dword 10000` at
6A692h becomes 2E00h), about 1.7 KB more of the game's memory.

### Picking pockets

([In the README](README.md#picking-pockets).)

How: the patched game's conversation window sends a key it doesn't know to
the helper (`INT FCh`), which has the Ledger roll and move the item, then adds
the result to the window's text; and the routine that uses the item on the
pointer on something on the map tells the helper what was used on what
(`INT FDh`): for the thieving tools on someone, the Ledger does the same, and
the helper shows the result instead of the game's "nothing happens".

### The cooked vulture

([In the README](README.md#the-cooked-vulture).)

How: in the Ledger's copy of `GPLDATA.GFF`, Dinos's talk (script 139) has the
question in its first menu (a copy of the game's with the question added, as for
the questions about Kalzith and Semyon, see
[Dinos and the Trustee](README.md#what-dinos-and-the-trustee-say-about-them)), shown
while the game's own test says someone in the party carries the cooked vulture
(33h, as the campfire's script asks about the plucked one; the game's object
A4Ch), the test being the question's own condition in the menu. Chosen, the script takes it (5Ch, as the campfire takes the plucked one)
and sets the Ledger's flag 780, then gives the XP through the game's own routine
for quests (the amount in its variable, then script 74 at 135: the window, the
words and the quest's sound), as Dinos's own script does when he heals Gilal
(350). The Ledger then refills the party, once (flag 781), only while the party
is talking with him (never from a game being loaded).

### What the party wears

([In the README](README.md#what-the-party-wears).)

How: the party's figures are objects 300 to 313 in `SEGOBJEX.GFF` (300 and
the figure picked at character creation). The launcher's copy of the file
(see [Item icons](README.md#new-items)) gives each its own walking and fighting
pictures, the game's with room round them for gear (walking, 6 pixels at the
sides and 2 above, as much as anything worn reaches; in a fight, 10), and free
space after each in the file. The game draws a figure's whole picture at every
step, so each picture is exactly as long as it needs to be. While the game
runs, when someone's worn items change, the Ledger draws their pictures anew
(`dscompanion/spritegear.py`, from where `dscompanion/spriteparts.py` finds the
head, hair, hands and the rest in each frame), writes them into its copy of the
file with their new lengths in the file's index (the game reads a picture's
place and length there each time it loads one), takes the old ones out of the
game's table of loaded pictures (the game frees them itself, as any it no
longer uses), and empties the figure's slot on the map: the game loads the new
pictures and draws them at once, in a few thousandths of a second
(`dscompanion/sprites.py`). It then has the helper draw the view again (see
[Shadows](README.md#shadows)), so the shadows show the new outfit too. A picture the
game loads later (in a fight, in another area) comes dressed, from the file.
The copy also has a spare pair of pictures for each party place. Each thing on
the map names the picture it is drawn with and the slot in the game's picture
table it is drawn from; for a second member of the same figure the Ledger names
their spare there and empties the slot, and the game loads the picture and
fills it.

### Shadows

([In the README](README.md#shadows).)

How: the launcher's copy of `DSUN.EXE` (see [How the dice log
works](#how-the-dice-log-works)) calls DSCLOG when the game draws the floor of
the view or of a rectangle of it. DSCLOG then lays each casting figure's
current picture, flattened and stretched, onto the floor just drawn, darkening
each pixel to the closest clearly darker colour of the area's palette (a table
it makes from the palette when the Ledger asks: after each area change, once
its fade-in is over, and now and then; the colours the game cycles, for water
and fire, are never picked as darker ones). The rectangles the game draws again when a figure
moves are widened by the length of a shadow, so none is left behind. The
Ledger keeps DSCLOG's list of who casts one (`dscompanion/shadows.py`) and has
DSCLOG draw the view again when it changes (from the game's main loop, as
centring the view does: marking the figures changed instead, as the game's own
code does to draw one again, can set one in a fight walking again).

### Dust

([In the README](README.md#dust).)

How: DSCLOG notes, each time round the game's main loop, how far each figure
that casts a shadow has walked, and raises a puff a little behind and to one
side of its feet every 6 pixels (the feet in turn). The puffs are drawn on the
floor after the shadows, lightening it through a table of each colour's lighter
one, which the Ledger makes from the area's palette (`dscompanion/dust.py`):
only warm, middling colours (sand, dirt) have one, so stone, water and the
figures take none. Each puff is dithered thinner toward its edge and as it
fades, by a pattern fixed to the map, so a puff looks the same however much of
it the game draws again. While anyone walks, the rectangle the game draws again
round what moved is made to take the puffs in; once everyone stands, DSCLOG has
the view drawn again a few times a second until the last puff is gone.

### Game speed

([In the README](README.md#game-speed).)

The Ledger's drawing is as cheap as it can be without looking any different:
a shadow is darkened a plane of the video memory at a time (the graphics
card's registers set four times for a figure, not four times for each of its
rows), and a dust puff's pixels are worked out a row at a time, only within
its outline and the part of the view being drawn again. The pictures the
Ledger draws the party's gear on are each exactly as long as their outfit,
with only the room gear needs round the figure while walking (6 pixels at the
sides, 2 above; 10 in a fight), since the game draws a walking figure's whole
picture at every step.

### Choosing an enemy: Tab, Enter and the rings

([In the README](README.md#choosing-an-enemy-tab-enter-and-the-rings).)

How: DSCLOG hooks the keyboard (`INT 16h`) and takes Tab, Shift+Tab and, with an
enemy chosen, Enter from what the game reads, counting them for the Ledger
(`dscompanion/targeting.py`), which keeps the enemies marked and the chosen one
(`dscompanion/rings.py`). The rings are drawn in the floor pass, after the
shadows, through a table of each colour's redder one made from the palette. For
Enter, DSCLOG puts the pointer at the enemy's feet and gives the game a left
click there, from the main loop, while the routine that finds what is under the
pointer (`DSUN.EXE` 25B52h, `INT DBh`) answers with the chosen enemy for half a
second, whatever stands in front of it.

### Scrolling the map

([In the README](README.md#scrolling-the-map).)

How: the game hears of the mouse's buttons from the mouse driver, through a
handler it gives it (`INT 33h`, function 0Ch). DSCLOG hooks `INT 33h` and puts
its own handler in between, which keeps the middle button (the wheel pressed)
from the game, and, with the right button dragging too, keeps the right button
from it while it is held: a click reaches the game when it is let go (pressed
and released where it was pressed), a drag never does. The game's main loop asks where the pointer
is (to scroll at the screen's edge); there DSCLOG has the game centre its view
where the drag puts it, with the game's own routine (the one clicking on the
overview map uses, which draws the view again), and keeps the pointer it reports
off the edges meanwhile. DOSBox 0.74, GOG's, never passes the wheel on to the
game, so the Ledger watches for it in Windows (a low-level mouse hook, only
while DOSBox's window is in front) and tells DSCLOG how far to scroll
(`dscompanion/scrolling.py`).

### More saves

([In the README](README.md#more-saves).)

How: the save names the game searches the folder for and writes a save to
(`SAVE??.SAV`, `SAVE%.2d.SAV`) are two strings in its memory; DSCLOG changes
their fourth letter for the page. The window's event routine leaves keys and
buttons it has no use for to a jump to its end; the patched game has DSCLOG
take them there (`INT D8h`, `INT D7h`), and for a new page run the window's
own routines that search the folder, draw the rows and draw the window. Enter
is taken out of the window's key table, so it comes to DSCLOG too, which goes
on to LOAD (or SAVE) as the table did, but not on a row with no save. The
buttons are the game's kind, in the Ledger's copy of `RESOURCE.GFF`: placed
in the window under EXIT, with pictures made from EXIT's, its letters taken
away and the page's put in with the game's text font
(`dscompanion/savepages.py`; the buttons' own carved letters have no P, G or
digits).

### More characters

([In the README](README.md#more-characters).)

How: the game's file routines take any number; only its loops over the
characters stop at 20, its roster list has room for 20 and its "Maximum
characters" check counts to 19. The patched game has 30 and 29 there
(`dscompanion/gamepatch.py`, a byte each).

A New character counts as Okay wherever the game tests for Okay: a jump each
(`NEW_AS_OKAY` in `dscompanion/gamepatch.py`), and `game.py` does the same.

## Planned: kits

Being built: the choice is made (the KIT page, the kit's byte, the Effects
screen's line, the Characters tab, the Options switch); the kits' effects are
not. A kit is a choice a single-class character makes at creation: three for
each class, or none (the class as it is). Each gives something and costs
something, as AD&D's kits do. The **Kits** rule change on the Options tab
(`game.RULE_KITS`, bit 0 of the helper's second rules word, `RULES_HI` at the
header's +270) switches them all off.

### The kits

| Class | Kit | Benefit | Drawback |
|---|---|---|---|
| Fighter | Myrmidon | a second weapon spec at 1st level, on to mastery and grand mastery as the first | −4 on saves against charm |
| | Sentinel | +2 AC with a shield, +2 initiative | −1 on saves against spells |
| | Ravager | +1 to hit and damage in melee; a base AC by level (7 at 1st, 1 better every 2 levels to 3 at 9th, then every 3 to 0 at 18th), armour bettering it | no missile or thrown weapons, no shield, light armour only |
| Gladiator | Arena Champion | with a shield in a hand: +1 to hit and damage in melee, AC 1 better | −1 to hit in melee with no shield |
| | Twin-blade | no two-weapon penalty | no shield; no two-handed weapon, but a half-giant's held in one hand |
| | Brute | +2 to hit and damage with a two-handed melee weapon | two-handed melee weapons only (a half-giant may add a shield); missile weapons, but not as a weapon spec |
| Ranger | Stalker | +2 movement in a fight, +15 hide in shadows, +15 move silently | light armour only |
| | Justifier | the bow's expertise and the chosen weapon spec's become specialization | priest spells on the Justifier's table: one 1st-level slot at 10th level |
| | Seeker | priest spells on the Seeker's table: from 6th level | its sphere's weapon limits (but it keeps the bow) |
| Thief | Swashbuckler | a warrior's THAC0 | −10 to all thief skills |
| | Assassin | hiding in shadows isn't halved in daylight | −15 pick pockets and open locks |
| | Shinobi | preserver spells on the Seeker's table, cast in light armour too | the Seeker's few slots; its own short list of spells, one learnt at each level up from its first slots, none from scrolls; only the dagger, short sword, quarterstaff, chatkcha, sling, staff sling and bow; light armour only; no shield |
| Cleric | Elementalist | a second sphere: its spells and its weapons | spell slots one level slower (none at 1st level) |
| | Healer | Cure spells heal 1 more per die | harmful spells do 1 less per die |
| | Crusader | a fighter's THAC0 | one fewer spell slot at each spell level |
| Druid | Grove Warden | AC 1 better for every 3 druid levels | no metal weapons |
| | Lifebinder | healing spells heal a die more | blunt weapons only |
| | Wanderer | +3 on saves against fire and cold spells (the game's Resist Fire and Resist Cold) | AC 1 worse |
| Preserver | Scholar | a spell more learnt at each level up | −1 to hit |
| | Battle Mage | a warrior's THAC0, a d6 hit die, expertise in one weapon spec (a one-handed melee weapon: long sword, short sword, dagger, club, mace, axe or pick; no thrown weapon), which it may use as well as a preserver's own weapons; light armour worn and spells cast in it; spells cast though hit in a fight (if the game stops them) | one fewer spell slot at each spell level; nothing in the off hand |
| | Arcanist | a spell slot more at each spell level | −2 CON |
| Psionicist | Mind Bender | telepathy powers cost 2 PSP less | psychokinesis powers 2 more |
| | Mind Warrior | a warrior's THAC0, a d8 hit die | a tenth fewer PSP |
| | Kineticist | psychokinesis powers cost 2 PSP less | telepathy powers 2 more |

The Seeker's and the Justifier's tables are AD&D's (*The Complete Ranger's
Handbook*), up to 10th level; their spells are cast at the table's casting
level, not the ranger's:

| Ranger level | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|
| Seeker: casting level | 1 | 2 | 3 | 4 | 5 |
| Seeker: 1st, 2nd, 3rd level slots | 1 | 2 | 2, 1 | 2, 2 | 2, 2, 1 |
| Justifier: casting level, slots | | | | | 1; one 1st-level |

The Shinobi's spells, all the game's (thief level 6 on, the Seeker's slots):

| Spell level | Spells |
|---|---|
| 1st | Gaze Reflection, Charm Person, Shield, Color Spray, Wall of Fog |
| 2nd | Invisibility, Mirror Image, Blur, Detect Invisibility, Fog Cloud |
| 3rd | Blink, Haste, Protection from Normal Missiles, Hold Person |

No kit is the kit page's first row, and what a new character has.

### Room in the helper

Done. DSCLOG keeps its code and data in one 64 KB segment, all reached
through CS; the dice log's ring buffer (`NENT` 128 entries of `ESIZE` 192
bytes, 24 KB) was in it too, and the image had grown to 63 KB. The ring now
follows the resident part in memory, in a segment of its own: the install code
sets `ring_seg` (the header's +268, read by `dicelog.py`) to the paragraphs
after the resident image, and its last step (`KEEP`, in the resident part, as
the ring lies over the install code) clears the ring and stays resident with
it. The image is 40 KB, about 25 KB short of the segment's end.

Measured with `mem` in DOSBox (GOG's settings: one upper memory block of
63 KB): the old helper, asking for its 63 KB image and a stack when loaded,
didn't fit in upper memory, so `LH` loaded it low, and the game had 570 KB of
conventional memory free rather than 632 KB. Now it asks for the resident part
and the ring (`LOAD_EXTRA`), 63 KB in all with its PSP, and loads high: 632 KB
free, and 1 KB of upper memory left. The KIT page took 736 bytes of that
(the image 40,752 bytes), and the helper still loads high. More code for the
kits than the 300 bytes or so left goes low again (the game losing 62 KB, as
before) unless room is made in upper memory too: the ring at 96 entries would
give 6 KB, the text buffer (`TSIZE`, 8 KB) a little more.

### The kit's byte

Sheet `+43h`: zero in every sheet of the saves and saved characters at hand
(176), and nothing in DSUN.EXE reads or writes it (no `es:[bx+43h]` access of
any kind), as with the weapon specs' `+14h` to `+17h`, which saves and the
roster keep. `+45h` is the same, if a second byte is needed. 0: no kit; 1 to 3
the class's kits.

### Choosing one

Built. The creation panel's lower window shows the psionic disciplines or the
clerical spheres, each with a button that swaps them (VIEW SPHERES is there,
out of use, for a class with no sphere), and for a warrior with weapon
specialization the WEAPON SPEC pages. The **KIT** page is at the end of that
chain, opened with a **KITS** button where the last page's button was:

| The class (one only) | Where KITS is |
|---|---|
| preserver, psionicist, thief; a fighter or gladiator without weapon specialization | the disciplines' window (3022, a copy of 3012) |
| cleric, druid; a ranger without weapon specialization | the spheres' window (3023, a copy of 3013) |
| fighter, gladiator, ranger with weapon specialization | the fourth weapon page (3025, a copy of 3017) |

`WP_IDS` (`kitpages.panel_windows`) picks the windows for the classes being
made, for the probes that open them (`PROBE_WP_DISC_WIN`,
`PROBE_WP_SPHERE_WIN`, and `PROBE_WP_CLASS` when the classes change). The
kit page itself is a window for each class (3026 to 3033, by the creation
screen's class numbers), its rows NO KIT and the class's three kits
(buttons `888h`, and `870h` + 3 × (class − 1) + kit − 1), its button VIEW
PSIONICS (the weapon pages' `851h`) back to the disciplines. Like the weapon
pages, it is kept at `DS:EA6h` with the spheres' own routine answering its
buttons, so `PROBE_WP_SPHERE_CLICK` gets its clicks and `PROBE_WP_SHOWN`
lets the game close it when another class is clicked. `KIT_ROW` puts the
kit in the creation sheet's `+43h`, and `KIT_MARKS` marks the rows. As the
game's spheres do, the rows not chosen are out of use (greyed) while one is;
the one chosen, clicked, is taken back (`KIT_OPEN`, `FFh`: none chosen, no
kit), and the rows are all in use again. The game keeps the whole sheet when DONE is pressed: `+43h`
is in the roster's CHAR record (the sheet at its `+4Eh`). It also keeps the
creation sheet from one character to the next, so the kit is put back to none
whenever the disciplines' window is opened other than on the way back to it
(`KIT_KEEP`, set by VIEW PSIONICS): for a new character, or another class.

The rows' letters are carved from the game's own labels, as the weapon
pages' (`kitpages.py`, with a J and a hyphen drawn). The panel's frame comes
in to about 95 pixels past the rows' left at the second kit's row, so a row
is held to 88 (`ROW_WIDTH`, its mark's room in), clear of it: ARENA CHAMPION,
SWASHBUCKLER, ELEMENTALIST, GROVE WARDEN, BATTLE MAGE, MIND BENDER and MIND
WARRIOR are shortened (CHAMPION, SWASHBUCK, ELEMENTAL, WARDEN, BATTLMAGE,
M-BENDER, M-WARRIOR), the last two as the game's P-KINESIS.

The Effects screen's lower panel (`PROBE_EF_ROWS`) has the kit's line first,
`KIT: RAVAGER`, before the weapon specs; the Characters tab has `Kit: Ravager`
(`GameData.kit`).

The kits' score changes are made when the character is first played, not on
the creation screen (the game keeps no record of which scores the player
rolled, so a change made there couldn't be taken back cleanly when the kit is).

### Where each effect goes

Built (step 2). `KIT_ID` gives a sheet's kit as one number (the creation
class × 4 + the kit: `kitpages.kit_id`), `KIT_OF_CREATURE` a creature's; each
effect has its twin in `kits.py`, which the Ledger and the dice log use, and
emulated tests hold the helper to it:

| Effect | Kits | Where |
|---|---|---|
| damage with a weapon | Ravager, Brute (melee: `KIT_MELEE`, by the item type), Arena Champion (melee, a shield in a hand: `KIT_CHAMPION`, by `PROT_SCAN` of the attacker's thing, `[BP+18h]`) | `PROBE_SPEC_DAMAGE` (`KIT_ATTACK_DAMAGE`), and the DAM lines (`PROBE_DAM_LINE`, `PROBE_VIEW_DAM`: `KIT_MELEE` only) |
| to hit | Ravager, Brute, Arena Champion | `PROBE_ATTACKS` (`KIT_TO_HIT`: `KIT_CHAMPION`, and `KIT_MELEE` in melee) |
| AC | Ravager (`RAVAGER_AC` by level against the sheet's base AC, `+27h`), Wanderer, Sentinel and Arena Champion (a shield in a hand: `PROT_SCAN`), Grove Warden | `PROBE_AC` (`INT 62h`, the end of the AC routine: `KIT_AC`) |
| movement | Stalker | `PROBE_MOVE` (`KIT_MOVE`) |
| spell slots | Arcanist (+1 wizard), Battle Mage (−1 wizard), Crusader (−1 priest), Seeker and Justifier (their priest tables, `SEEKER_SLOTS`, by ranger level, in place of the game's), Elementalist (a level behind) | `PROBE_SLOTS` (`INT B6h`, new: the end of the game's slot routine, `mov ax,[bp-2]` at DSUN.EXE 5E255h) and `PROBE_SLOT_LEVEL` (`INT B5h`, new: where it takes a class's level, `mov al,es:[bx+24h]` at 5E1F6h); `GameData.max_spell_slots` with `kits.slots` and `kits.slot_level` |
| THAC0 | Swashbuckler, Crusader, Battle Mage, Mind Warrior (a warrior's: 21 less the level, where better), Scholar (1 worse) | `PROBE_THAC0` (`INT B7h`, new: the end of the game's THAC0 routine, `mov ax,14h / sub ax,si` at DSUN.EXE 876BBh, which every write of a creature's THAC0, `+1Fh`, uses: on making a character, 66CE0h, and at a level up, 86D7Eh and 87A91h) |
| initiative | Sentinel | `PROBE_INIT` (`INT B8h`, new: the round's 20 added at DSUN.EXE 5750Eh) |
| saves | Myrmidon (charms), Sentinel (spells, 0-137), Wanderer (fire and cold: the spell record's `+1Ah`, 2 or 4, as the game's Resist Fire and Resist Cold read it) | `PROBE_RING_SAVE` (the modifier routine's start: `KIT_SAVE`) |
| thief skills | Assassin (pick pockets, open locks), Swashbuckler (all) | `PROBE_BELT` (the thief skill routine's end) |
| hiding, moving silently | Stalker, Assassin | the stealth rule's rolls (`stealth.py`, `GameData.ranger_skill_parts`) |
| the two-weapon penalty | Twin-blade | `PROBE_TWO` |
| gear allowed | Ravager, Twin-blade, Brute, Stalker, Grove Warden, Lifebinder, Shinobi | `PROBE_CAN_USE` and `KINDS_ALLOWED` (`KIT_FORBIDS`: `restrict.kit_forbids`), whatever the class restrictions |
| weapon specs | Myrmidon (two, the second to grand mastery), Brute (no missile spec) | `WP_TWO`, `SPEC_OF_SHEET`, `KIT_FORBIDS` |
| scores | Arcanist | `kits.finish_new`, once, before the character is first played (the sheet's `+45h` marks it) |

Still to build, a new hook at a place already found:

| Effect | Kits | Where |
|---|---|---|
| max PSP | Mind Warrior | the level-up's sum at 873B2h |
| spells learnt at a level up | Scholar, Shinobi (one, from its list) | the CHOOSE A SPELL screen (see levels up to 10) |

Still to find:

| Effect | Kits | What |
|---|---|---|
| a power's PSP cost | Mind Bender, Kineticist | where the game takes the cost off: the costs are one table for everyone, so a kit's is a change there, by who uses the power |
| a spell's dice | Healer, Lifebinder | where the game rolls a spell's damage or healing (the dice log reads it; nothing changes it yet) |
| casting level | Seeker, Justifier, Shinobi | where the game takes it from the class level |
| a second sphere | Elementalist | how the game gives a priest its element's spells (the USE screen) and counts caster level 0 for another's |
| wizard spells for a thief | Shinobi | slots, spells known and learning for a class that has none; learning from a scroll refused (where the game learns one: the tome's probe is beside it, 8B80Ch) |
| spells stopped by a hit | Battle Mage | whether the game spoils a spell when its caster is hit in a fight at all: none of the research so far has seen it do so (a spell is cast at once, on the caster's turn) |

Every kit also needs its Python side: the Characters tab and the in-game
THAC0 and saves (`game.py`), the dice log's lines, and tests that hold the
helper's code (emulated) to the Python.

### Order

1. Done: the ring out of the segment, the memory measured; the kit's byte, the
   KIT page, the Effects screen's line, the Characters tab, the rule switch.
2. Done: the kits on hooks there already: Ravager, Sentinel (with an
   initiative hook), Myrmidon, Arena Champion, Twin-blade, Brute, Stalker,
   Assassin, Grove Warden, Wanderer, Arcanist's CON, Lifebinder's weapons; and
   the ring at 96 entries, for room in upper memory.
3. THAC0 and spell slot hooks. Done: the THAC0 (Swashbuckler, Crusader,
   Battle Mage, Mind Warrior, Scholar) and the Swashbuckler's thief skills.
   Done too: the spell slots (Crusader, Battle Mage, Arcanist, Elementalist,
   Justifier, Seeker), checked against the game's own routine run on a
   running game's memory. Left for later: the Scholar's spell learnt, with the
   CHOOSE A SPELL screen (the Shinobi's step), and whether the game lets a
   Seeker below 8th level choose priest spells for its slots.
4. After finding them: PSP costs (Mind Bender, Kineticist), spell dice
   (Healer, Lifebinder), casting level (Seeker, Justifier), a hit spoiling a
   spell (Battle Mage, if the game has it).
5. The Shinobi.
