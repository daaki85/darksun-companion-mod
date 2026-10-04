"""The rest of the bone scale armour, where its chest piece is.

The game has Bone Scale Chest Armor, Arm Armor and Leg Armor (objects 1033-1035, the arm and leg
pieces never placed anywhere in play) but no helm of bone. The first time the Ledger sees the
chest piece in the region (on the ground, in a container, or carried), it puts the arm and leg
pieces and a Bone Helm (an item type of the companion's own: the Helm's, of bone, with an icon
of its own in the bone scale's colours, icons.py) with it: in the same pile or container, or in
the carrier's backpack. Once a game (the key in the tools_given set, kept in settings), and
never where any of the three is already (a save made after they were added).

They are never given again, whatever becomes of them. Should one go missing other than in the
game's ways, Watch writes up what became of it (its item record, the game's free list, the
Ledger's own use of that list), for its cause to be found.
"""

import os
import struct
import time
from typing import Dict, List, NamedTuple, Optional, Sequence, Set, Tuple

from . import game, npcitems, pickpocket, ring
from .game import GameData

KEY = "bone scale set"  # (after the leader's name: once each game, as the other things given)
CHEST_PICTURE, CHEST_TYPE = 0xFBF7, 15  # Bone Scale Chest Armor (object 1033)
HELM_NAME = 6  # "Helm" (the game shows the material before it: "Bone Helm")
# the game's own records (SEGOBJEX), in no list and no slot
ARM = npcitems._item("f6fb000000003000000037000000000005ff260100")  # Bone Scale Arm Armor
LEG = npcitems._item("f5fb000000003000000038000000000005ff270100")  # Bone Scale Leg Armor
# the leather Helm's, of the companion's bone helm type (its picture the Helm's until icons.py
# gives it its own)
HELM = npcitems._item("03fc000000000500000005000000000004ff060000", type_=game.BONE_HELM_TYPE, name=HELM_NAME)
PIECES = (ARM, LEG, HELM)
NAMES = {ARM: "Bone Scale Arm Armor", LEG: "Bone Scale Leg Armor", HELM: "Bone Helm"}


def key(gd: GameData) -> str:
    """The set's given-once key, for this game (the leader's name, as the other given keys)."""
    return f"{gd.creature_name(0)}|{KEY}"


def which_piece(rec: bytes) -> Optional[bytes]:
    """Which of the three REC is (ARM, LEG, HELM), or None."""
    if len(rec) < game.ITEM_SIZE:
        return None
    if struct.unpack_from("<H", rec, game.ITEM_TYPE)[0] == game.BONE_HELM_TYPE:
        return HELM
    return {0xFBF6: ARM, 0xFBF5: LEG}.get(struct.unpack_from("<H", rec, 0)[0])


def is_chest(rec: bytes) -> bool:
    return len(rec) >= game.ITEM_SIZE and struct.unpack_from("<HH", rec, 0)[0] == CHEST_PICTURE and \
        struct.unpack_from("<H", rec, game.ITEM_TYPE)[0] == CHEST_TYPE


def is_piece(rec: bytes) -> bool:
    """One of the pieces the Ledger adds (the arm or leg piece, or the Bone Helm)."""
    return len(rec) >= game.ITEM_SIZE and (struct.unpack_from("<H", rec, 0)[0] in (0xFBF6, 0xFBF5) or
                                           struct.unpack_from("<H", rec, game.ITEM_TYPE)[0] == game.BONE_HELM_TYPE)


def find_chest(gd: GameData) -> Optional[int]:
    """The chest piece's item number, wherever it is in the region (a pile, a container, carried),
    or None, also when any of the other pieces is already there (a game saved after they were
    added, loaded again)."""
    it = ring.Items(gd)
    chest = None
    for thing in range(ring.THING_COUNT):
        for item, rec in it.chain(thing):
            if is_piece(rec):
                return None
            if is_chest(rec) and chest is None:
                chest = item
    return chest


def carrier(gd: GameData, it: ring.Items, item: int) -> Optional[int]:
    """The party member carrying the item, if one is."""
    for member in range(game.PARTY_SIZE):
        rec = gd.creature(member)
        if len(rec) < game.CREATURE_SIZE or not rec[game.CREATURE_NAME]:
            continue
        for offset in game.CREATURE_ITEM_LISTS:
            thing, = struct.unpack_from("<h", rec, offset)
            if any(i == item for i, _ in it.chain(thing)):
                return member
    return None


def insert_after(gd: GameData, it: ring.Items, after: int, rec: bytes) -> bool:
    """An item from the game's free list, made REC, put right after item AFTER in its list
    (the same pile or container), in its slot. False if no item record is to be had."""
    item = it.word(ring.FREE_ITEMS)
    if item >= game.NO_ITEM:
        return False
    gd.guest.write(gd.ds * 16 + ring.FREE_ITEMS, it.item(item)[game.ITEM_NEXT:game.ITEM_NEXT + 2])
    ring.took(item, NAMES.get(rec, "a bone scale piece"))
    before = it.item(after)
    rec = bytearray(rec)
    rec[game.ITEM_NEXT:game.ITEM_NEXT + 2] = before[game.ITEM_NEXT:game.ITEM_NEXT + 2]
    rec[game.ITEM_SLOT] = before[game.ITEM_SLOT]
    gd.guest.write(it.items + item * game.ITEM_SIZE, bytes(rec))
    gd.guest.write(it.items + after * game.ITEM_SIZE + game.ITEM_NEXT, struct.pack("<h", item))
    return True


def free_cells(gd: GameData, it: ring.Items, member: int) -> int:
    """How many of the member's backpack cells are empty."""
    rec = gd.creature(member)
    used = set()
    for offset in game.CREATURE_ITEM_LISTS:
        thing, = struct.unpack_from("<h", rec, offset)
        used.update(data[game.ITEM_SLOT] for _, data in it.chain(thing))
    return sum(1 for cell in pickpocket.BACKPACK if cell not in used)


def _put(gd: GameData, chest: int, pieces) -> List[bytes]:
    """PIECES put with the chest piece: in its carrier's backpack (all of them, or none while
    there isn't room for all), or after it in its pile or container. Those put."""
    it = ring.Items(gd)
    member = carrier(gd, it, chest)
    if member is not None:
        if free_cells(gd, it, member) < len(pieces):
            return []  # (no room in the pack for them all: the next time there is)
        return [rec for rec in pieces if npcitems.add_to(gd, member, rec)]
    return [rec for rec in reversed(pieces) if insert_after(gd, ring.Items(gd), chest, rec)]


def place(gd: GameData, given: Set[str]) -> List[str]:
    """The arm and leg pieces and the Bone Helm with the chest piece, once a game (GIVEN: the
    key, added; and never where one of them already is). Never again after that, whatever
    becomes of them (sold, dropped, lost: Watch notes a loss). Nothing for the log."""
    if key(gd) not in given and KEY in given and _any_piece(gd):
        given.add(key(gd))  # (the key of before it was this game's: the set is here, so this one's)
    if key(gd) in given:
        return []
    chest = find_chest(gd)
    if chest is None:
        return []
    if _put(gd, chest, PIECES):
        given.add(key(gd))
    return []  # (nothing in the log: the items are there to be found)


def _any_piece(gd: GameData) -> bool:
    it = ring.Items(gd)
    return any(is_piece(rec) for thing in range(ring.THING_COUNT) for _, rec in it.chain(thing))


class Seen(NamedTuple):
    """Where a piece was last seen: its item record's number and bytes, where that was (words for
    the report), whether a party member had it, the region, the time (Ledger's and game's)."""
    item: int
    rec: bytes
    where: str
    carried: bool
    region: int
    at: float
    game_time: Optional[int]


class Watch:
    """The three pieces, once given, followed every look (the ring's, 3 s): where each is. One
    gone from the region (not left on the ground of another area, not a save loaded: the game's
    clock going back) on two looks in a row is written up, as it was found the first time, in
    crash-logs (report), with a line for the log saying so. Each piece once a run of the Ledger."""

    def __init__(self, folder: Optional[str] = None):
        self.folder = folder
        self.seen: Dict[str, Seen] = {}
        self.missing: Dict[str, str] = {}  # piece -> the report's text, from its first look gone
        self.reported: Set[str] = set()
        self.game_key: Optional[str] = None
        self.clock: Optional[int] = None

    def check(self, gd: GameData, given: Set[str], recent: Sequence[str] = (), now: Optional[float] = None) -> List[str]:
        now = time.time() if now is None else now
        if key(gd) not in given:
            return []
        clock, region = gd.game_time(), gd.region()
        if key(gd) != self.game_key or (clock is not None and self.clock is not None and clock < self.clock):
            self.seen, self.missing = {}, {}  # (another game, or a save loaded: start again)
        self.game_key, self.clock = key(gd), clock
        it = ring.Items(gd)
        holders = _holders(gd, it)
        if not holders:
            return []  # (the party's lists empty: memory in the middle of being filled)
        found: Dict[str, Seen] = {}
        for thing in range(ring.THING_COUNT):
            for item, rec in it.chain(thing, inside=False):
                piece = which_piece(rec)
                if piece is not None and NAMES[piece] not in found:
                    who = holders.get(item)
                    found[NAMES[piece]] = Seen(item, rec, _where(gd, item, rec, thing, who), who is not None,
                                               region, now, clock)
        out: List[str] = []
        for name, last in self.seen.items():
            if name in found or name in self.reported:
                continue
            if not last.carried and last.region != region:
                continue  # (on the ground or in a chest of another area: not in memory now)
            if name not in self.missing:
                self.missing[name] = report(gd, it, name, last, holders, recent, now)
                continue  # (gone on one look: again on the next before it's a loss)
            text = self.missing.pop(name)
            path = write_report(text, now, self.folder)
            self.reported.add(name)
            if FREED in text:
                out.append(f"The {name} is gone (last seen {last.where}): the game took it back. If you sold it "
                           f"or it was taken in the story, nothing is wrong; if not, please send {path}.")
            else:
                out.append(f"The {name} has vanished (last seen {last.where}). What became of it is written up in "
                           f"{path}: please send that file.")
        for name in found:
            self.missing.pop(name, None)
        self.seen.update(found)
        return out


def _holders(gd: GameData, it: ring.Items) -> Dict[int, int]:
    """Each item a party member has (worn, in the pack, or in a container of theirs) -> member."""
    out: Dict[int, int] = {}
    for member in range(game.PARTY_SIZE):
        rec = gd.creature(member)
        if len(rec) < game.CREATURE_SIZE or not rec[game.CREATURE_NAME]:
            continue
        for offset in game.CREATURE_ITEM_LISTS:
            thing, = struct.unpack_from("<h", rec, offset)
            for item, _ in it.chain(thing):
                out[item] = member
    return out


def _where(gd: GameData, item: int, rec: bytes, thing: int, member: Optional[int]) -> str:
    if member is not None:
        if rec[game.ITEM_SLOT] in pickpocket.BACKPACK:
            return f"in {gd.creature_name(member)}'s backpack (item {item})"
        return f"worn by {gd.creature_name(member)} (slot {rec[game.ITEM_SLOT]}, item {item})"
    return f"in the list of object {thing}, on the ground or in a container (item {item})"


def _describe(rec: bytes) -> str:
    """An item record, for the report: its picture, type, name entry, plus, slot, and bytes."""
    if len(rec) < game.ITEM_SIZE:
        return "(not readable)"
    picture, = struct.unpack_from("<H", rec, 0)
    kind, = struct.unpack_from("<H", rec, game.ITEM_TYPE)
    name, = struct.unpack_from("<H", rec, game.ITEM_NAME)
    piece = which_piece(rec)
    what = NAMES[piece] if piece is not None else "Bone Scale Chest Armor" if is_chest(rec) else "another item"
    return (f"{what}: picture {picture:04X}h, type {kind}, name entry {name}, plus {struct.unpack_from('b', rec, game.ITEM_PLUS)[0]}, "
            f"slot {rec[game.ITEM_SLOT]}, next {struct.unpack_from('<h', rec, game.ITEM_NEXT)[0]}; bytes {rec.hex()}")


def _free_list(it: ring.Items) -> Tuple[List[int], bool]:
    """The game's free item records, in order, and whether the list ended as it should (rather
    than going round or out of range)."""
    out, seen, index = [], set(), it.word(ring.FREE_ITEMS)
    for _ in range(FREE_WALK):
        if index >= game.NO_ITEM:
            return out, True
        if index in seen:
            return out, False
        seen.add(index)
        out.append(index)
        index, = struct.unpack_from("<H", it.item(index), game.ITEM_NEXT)
    return out, False


FREE_WALK = 3000  # free records followed for the report
FREED = "is in the game's free list"


def report(gd: GameData, it: ring.Items, name: str, last: Seen, holders: Dict[int, int],
           recent: Sequence[str], now: float) -> str:
    """The text of a vanished piece's report: where it was, what its item record holds now and
    where that is, the game's free list, the Ledger's own takings from it, and the log's end."""
    stamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now))
    lines = [f"Templar's Ledger: the {name} vanished, {stamp}", "",
             f"Last seen {now - last.at:.0f} s before, {last.where}, in region {last.region:02X}h "
             f"(game time {last.game_time}).",
             f"Now: region {gd.region():02X}h, game time {gd.game_time()}, whose turn {gd.whose_turn()}.",
             f"Its record then: {_describe(last.rec)}"]
    now_rec = it.item(last.item)
    lines.append(f"Item {last.item} now: {_describe(now_rec)}")
    free, ended = _free_list(it)
    holder = next((thing for thing in range(ring.THING_COUNT)
                   if any(i == last.item for i, _ in it.chain(thing, inside=False))), None)
    if last.item in free:
        lines.append(f"Item {last.item} {FREED} (place {free.index(last.item)} of {len(free)}): the game took "
                     "the piece away (sold, used up, or destroyed by a script) and the record is free for "
                     "another item.")
    elif holder is not None:
        who = holders.get(last.item)
        lines.append(f"Item {last.item} is in the list of object {holder}"
                     + (f" ({gd.creature_name(who)}'s)" if who is not None else "")
                     + ": the record was taken for another item while still the piece's (one record given twice).")
    else:
        lines.append(f"Item {last.item} is in no list and not free: cut out of its list and not given back.")
    lines.append(f"The free list: {len(free)} records{'' if ended else ' (not ended as it should: damaged)'}, "
                 f"first {free[:12]}.")
    lines += ["", "The Ledger's own takings from (and givings back to) the free list, the last ones:"]
    taken = [f"  {now - when:.0f} s before: item {item}, {what}" for when, item, what in ring.TAKEN]
    lines += taken or ["  (none while this ran)"]
    lines += ["", "The dice log's last lines:"] + [f"  {line}" for line in list(recent)[-60:]] + [""]
    return "\n".join(lines)


def write_report(text: str, now: float, folder: Optional[str] = None) -> str:
    """The report saved as crash-logs/vanished-YYYY-MM-DD-HHMMSS.txt (a number after it if there
    is one already); its path."""
    if folder is None:
        from .launch import CRASH_DIR
        folder = CRASH_DIR
    os.makedirs(folder, exist_ok=True)
    stem = os.path.join(folder, time.strftime("vanished-%Y-%m-%d-%H%M%S", time.localtime(now)))
    path, n = stem + ".txt", 1
    while os.path.exists(path):
        n += 1
        path = f"{stem}-{n}.txt"
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return path
