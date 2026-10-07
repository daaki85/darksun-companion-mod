"""Runs DSCLOG's interrupt handlers in a CPU emulator (needs `pip install unicorn`).

Checks its rand() returns what Borland's rand() returns, keeps the registers
the game relies on, and records the entries the companion decodes; and that
the probes do the game instructions they replace.
"""

import os
import struct
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dscompanion.dicelog import FILTERS, HDR_SIG, Entry
from dscompanion.textlog import TextBuffer
from dscompanion.gamepatch import (VEC_MC_ROLL, VEC_MC_CON, VEC_MC_UNCON, VEC_NO_CAST, VEC_CAN_USE, VEC_VIEW_DAM, VEC_DAM_LINE, VEC_SPEC_DAMAGE, VEC_ATTACKS, VEC_XP_NEXT, VEC_SCRIPT_RAND, VEC_ITEM_ARMOUR, VEC_ITEM_SKIP, VEC_ITEM_WEAPON, VEC_AC, VEC_DOUBLE, VEC_MSG, VEC_NEXT, VEC_RAND, VEC_RING_AC, VEC_USE_ITEM,
                                  VEC_RING_SAVE, VEC_SAVE, VEC_TEXT, VEC_TWO, VEC_GRACE_CAST, VEC_GRACE_EFFECT,
                                  VEC_GRACE_ABILITY, VEC_NAMES_FILL, VEC_NAMES_SIZE, VEC_STEALTH, VEC_TYPES_FILL,
                                  VEC_TYPES_SIZE, VEC_LEVEL, VEC_HD_ROLL, VEC_HD_CON, VEC_THIEF_SKILL, VEC_TWO_HANDED,
                                  VEC_SPELL_TEXT, VEC_CHUNK_ID)
from dscompanion import game, restrict, specialize

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import test_restrict  # noqa: E402 (its item types and sheets)

try:
    from unicorn import Uc, UC_ARCH_X86, UC_HOOK_CODE, UC_HOOK_INTR, UC_HOOK_MEM_WRITE, UC_MODE_16
    from unicorn import x86_const as r
except ImportError:  # optional dependency
    Uc = None

EXE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dos", "DSCLOG.EXE")
TSR, GAME_DS, SS, CALLER, PARENT, RAND = 0x2000, 0x3000, 0x4000, 0x5000, 0x6000, 0x7000
IF = 0x200  # the interrupt flag
BP, PARENT_BP = 0x1000, 0x1100


def borland_rand(seed):
    seed = (seed * 0x015A4E35 + 1) & 0xFFFFFFFF
    high = seed >> 16
    return seed, high & 0x7FFF, 0xFFFF if high & 0x8000 else 0


def load_image():
    with open(EXE, "rb") as f:
        exe = f.read()
    return exe[struct.unpack_from("<H", exe, 8)[0] * 16:]


def fill_probes(image):
    """PROBE_NAMES_FILL and PROBE_TYPES_FILL, in that order: "add sp,0Ch", its three pushes back,
    then "or ax,ax" (other probes replace an "add sp,0Ch" the same way)."""
    import re
    return [m.start() - 15 for m in re.finditer(re.escape(bytes.fromhex("83c40c" "2eff36")), image)
            if image[m.start() + 18:m.start() + 20] == bytes.fromhex("09c0")]


def real_mode_interrupt(mu, intno, _):
    """Unicorn stops at INT; do what a real-mode CPU does: push FLAGS, CS, IP and jump via the IVT."""
    sp, ss = mu.reg_read(r.UC_X86_REG_SP), mu.reg_read(r.UC_X86_REG_SS)
    flags = mu.reg_read(r.UC_X86_REG_EFLAGS) & 0xFFFF
    frame = struct.pack("<HHH", mu.reg_read(r.UC_X86_REG_IP), mu.reg_read(r.UC_X86_REG_CS), flags)
    mu.mem_write(ss * 16 + sp - 6, frame)
    mu.reg_write(r.UC_X86_REG_SP, sp - 6)
    mu.reg_write(r.UC_X86_REG_EFLAGS, flags & ~(IF | 0x100))
    off, seg = struct.unpack("<HH", mu.mem_read(intno * 4, 4))
    mu.reg_write(r.UC_X86_REG_CS, seg)
    mu.reg_write(r.UC_X86_REG_IP, off)


class HeaderTests(unittest.TestCase):
    def test_built_in_filters_match_the_companion(self):
        image = load_image()
        hdr = struct.unpack_from("<H", image, 20)[0]
        self.assertEqual(image[hdr:hdr + 8], HDR_SIG)
        n = struct.unpack_from("<H", image, hdr + 32)[0]
        built_in = tuple(image[hdr + 34 + i * 9 + 1:hdr + 34 + i * 9 + 1 + image[hdr + 34 + i * 9]]
                         for i in range(n))
        self.assertEqual(built_in, FILTERS)
        self.assertEqual(tuple(image[hdr + 112:hdr + 117]), (VEC_RAND, VEC_SAVE, VEC_AC, VEC_TEXT, VEC_MSG))


@unittest.skipIf(Uc is None, "unicorn is not installed")
class StubTests(unittest.TestCase):
    def test_matches_borland_rand_and_logs_entries(self):
        image = load_image()
        hdr_off = struct.unpack_from("<H", image, 20)[0]
        ring = struct.unpack_from("<H", image, 16)[0]
        probe_save, probe_ac = struct.unpack_from("<HH", image, hdr_off + 108)
        int_rand = struct.unpack_from("<H", image, hdr_off + 118)[0]

        mu = Uc(UC_ARCH_X86, UC_MODE_16)
        mu.mem_map(0, 0x100000)
        mu.mem_write(TSR * 16, image)
        mu.mem_write(TSR * 16 + hdr_off + 32, struct.pack("<H", 0))  # no filters: record every call
        for vec, off in ((VEC_RAND, int_rand), (VEC_SAVE, probe_save), (VEC_AC, probe_ac)):
            mu.mem_write(vec * 4, struct.pack("<HH", off, TSR))
        mu.hook_add(UC_HOOK_INTR, real_mode_interrupt)
        mu.mem_write(TSR * 16 + hdr_off + 24, struct.pack("<4H", 0x494A, 0, 0, 0))
        seed = 0x12345678
        mu.mem_write(GAME_DS * 16 + 0x4122, struct.pack("<I", seed))
        mu.mem_write(GAME_DS * 16 + 0x494A, struct.pack("<H", 0xBEEF))
        # the caller's frame: saved BP, return address into PARENT, arguments; its locals below BP
        mu.mem_write(SS * 16 + BP, struct.pack("<HHH", PARENT_BP, 0x40, PARENT) + bytes(range(1, 29)))
        mu.mem_write(SS * 16 + BP - 16, bytes(range(200, 216)))
        mu.mem_write(SS * 16 + PARENT_BP + 2, bytes(range(100, 132)))
        mu.mem_write(SS * 16 + PARENT_BP - 0x28, bytes(range(150, 190)))
        mu.mem_write(PARENT * 16 + 0x40, bytes(range(50, 66)))
        # the patched rand(): INT VEC_RAND; the caller: CALL FAR rand; then code the log copies
        mu.mem_write(RAND * 16 + 0x822, bytes((0xCD, VEC_RAND, 0x90, 0x90, 0x90)))
        call = b"\x9a" + struct.pack("<HH", 0x822, RAND)
        after = bytes(range(0x80, 0x98))
        mu.mem_write(CALLER * 16 + 0x10, call + after)

        for n in range(70):  # more than the ring holds
            mu.reg_write(r.UC_X86_REG_CS, CALLER)
            mu.reg_write(r.UC_X86_REG_DS, GAME_DS)
            mu.reg_write(r.UC_X86_REG_SS, SS)
            mu.reg_write(r.UC_X86_REG_ES, 0x1234)
            mu.reg_write(r.UC_X86_REG_ESP, 0x800)
            mu.reg_write(r.UC_X86_REG_EBP, BP)
            mu.reg_write(r.UC_X86_REG_EAX, 0xAAAA0000 | n)
            mu.reg_write(r.UC_X86_REG_ESI, 0x5151)
            mu.reg_write(r.UC_X86_REG_EDI, 0x7171)
            mu.reg_write(r.UC_X86_REG_EFLAGS, IF | 2)
            mu.emu_start(CALLER * 16 + 0x10, CALLER * 16 + 0x10 + len(call))
            self.assertTrue(mu.reg_read(r.UC_X86_REG_EFLAGS) & IF)  # interrupts are back on

            seed, value, dx = borland_rand(seed)
            self.assertEqual(mu.reg_read(r.UC_X86_REG_EAX), 0xAAAA0000 | value)
            self.assertEqual(mu.reg_read(r.UC_X86_REG_DX), dx)
            self.assertEqual(struct.unpack("<I", mu.mem_read(GAME_DS * 16 + 0x4122, 4))[0], seed)
            for reg, want in ((r.UC_X86_REG_SI, 0x5151), (r.UC_X86_REG_DI, 0x7171),
                              (r.UC_X86_REG_ES, 0x1234), (r.UC_X86_REG_DS, GAME_DS),
                              (r.UC_X86_REG_BP, BP), (r.UC_X86_REG_SP, 0x800)):
                self.assertEqual(mu.reg_read(reg), want)

            nent = struct.unpack("<H", mu.mem_read(TSR * 16 + hdr_off + 12, 2))[0]
            e = Entry.parse(bytes(mu.mem_read(TSR * 16 + ring + (n % nent) * Entry.SIZE, Entry.SIZE)))
            self.assertEqual((e.seq, e.ip, e.cs, e.raw, e.bp, e.ss, e.ds, e.parent_bp),
                             (n + 1, 0x15, CALLER, value, BP, SS, GAME_DS, PARENT_BP))
            self.assertEqual(e.arg(2), 0x40)
            self.assertEqual(e.frame[4:], bytes(range(1, 29)))
            self.assertEqual(e.parent, bytes(range(100, 132)))
            self.assertEqual(e.glob, (0xBEEF, 0, 0, 0))
            self.assertEqual(e.locals, bytes(range(200, 216)))
            self.assertEqual(e.code, after)
            self.assertEqual(e.parent_code, bytes(range(50, 66)))
            self.assertEqual(e.parent_locals, bytes(range(150, 190)))

        seq, widx, nent = struct.unpack("<HHH", mu.mem_read(TSR * 16 + hdr_off + 8, 6))
        self.assertEqual((seq, widx), (70, 70 % nent))

        def call_with_filters(*filters):
            packed = b"".join(bytes([len(f)]) + f.ljust(8, b"\0") for f in filters)
            mu.mem_write(TSR * 16 + hdr_off + 32, struct.pack("<H", len(filters)) + packed)
            mu.reg_write(r.UC_X86_REG_CS, CALLER)
            mu.reg_write(r.UC_X86_REG_DS, GAME_DS)
            mu.reg_write(r.UC_X86_REG_SS, SS)
            mu.reg_write(r.UC_X86_REG_ESP, 0x800)
            mu.reg_write(r.UC_X86_REG_EBP, BP)
            mu.emu_start(CALLER * 16 + 0x10, CALLER * 16 + 0x10 + len(call))
            self.assertEqual(mu.reg_read(r.UC_X86_REG_SP), 0x800)
            self.assertEqual(mu.reg_read(r.UC_X86_REG_DS), GAME_DS)
            return struct.unpack("<H", mu.mem_read(TSR * 16 + hdr_off + 8, 2))[0], \
                struct.unpack("<H", mu.mem_read(TSR * 16 + hdr_off + 106, 2))[0]

        # no filter matches: the call is counted as skipped, not recorded, and rand() still works
        self.assertEqual(call_with_filters(b"\x11" * 8, after[:7] + b"\x00"), (70, 1))
        seed, value, _ = borland_rand(seed)
        self.assertEqual(mu.reg_read(r.UC_X86_REG_AX), value)
        # the second filter matches: recorded
        self.assertEqual(call_with_filters(b"\x11" * 8, after[:8]), (71, 1))
        # a shorter filter matches on its own length
        self.assertEqual(call_with_filters(after[:3]), (72, 1))
        self.assertEqual(call_with_filters(after[:2] + b"\x00"), (72, 2))

        call_at = [0x400]

        def run_probe(vector, bp_bytes, si, rest=b"\x90\x90\x90\x90\xf4"):
            mu.mem_write(SS * 16 + BP - 8, bp_bytes)
            code = bytes((0xCD, vector)) + rest
            call_at[0] += 0x10  # fresh code each time: the emulator caches translated code
            at = call_at[0]
            mu.mem_write(CALLER * 16 + at, code)
            # the saving throw's "mov ax, <spell table segment>", where DSUN.EXE has it
            mu.mem_write(CALLER * 16 + at - (0x79BB7 - 0x79A85), struct.pack("<H", 0x3E56))
            mu.reg_write(r.UC_X86_REG_CS, CALLER)
            mu.reg_write(r.UC_X86_REG_DS, GAME_DS)
            mu.reg_write(r.UC_X86_REG_SS, SS)
            mu.reg_write(r.UC_X86_REG_ESP, 0x800)
            mu.reg_write(r.UC_X86_REG_EBP, BP)
            mu.reg_write(r.UC_X86_REG_ESI, si)
            mu.reg_write(r.UC_X86_REG_EBX, 0xB0B0)
            mu.reg_write(r.UC_X86_REG_EAX, 0x12340000)
            mu.reg_write(r.UC_X86_REG_EFLAGS, IF | 2)
            mu.emu_start(CALLER * 16 + at, CALLER * 16 + at + len(code) - 1)
            seq = struct.unpack("<H", mu.mem_read(TSR * 16 + hdr_off + 8, 2))[0]
            nent = struct.unpack("<H", mu.mem_read(TSR * 16 + hdr_off + 12, 2))[0]
            e = Entry.parse(bytes(mu.mem_read(TSR * 16 + ring + ((seq - 1) % nent) * Entry.SIZE, Entry.SIZE)))
            return e

        # the save probe: [bp-2] = total 15, [bp-1] = needs 12 -> CMP leaves carry clear (JAE taken)
        e = run_probe(VEC_SAVE, bytes([0] * 6 + [15, 12]), 0x5151)
        self.assertEqual((e.kind, e.raw & 0xFF, e.raw >> 8, e.bp, e.extra), (1, 15, 12, BP, 0x3E56))
        self.assertTrue(mu.reg_read(r.UC_X86_REG_EFLAGS) & IF)
        self.assertEqual(mu.reg_read(r.UC_X86_REG_AL), 15)
        self.assertFalse(mu.reg_read(r.UC_X86_REG_EFLAGS) & 1)
        self.assertEqual((mu.reg_read(r.UC_X86_REG_SI), mu.reg_read(r.UC_X86_REG_BX)), (0x5151, 0xB0B0))
        self.assertEqual(mu.reg_read(r.UC_X86_REG_SP), 0x800)
        e = run_probe(VEC_SAVE, bytes([0] * 6 + [9, 12]), 0x5151)
        self.assertTrue(mu.reg_read(r.UC_X86_REG_EFLAGS) & 1)  # 9 < 12: carry set, JAE not taken
        # the AC probe: [bp-6] = 7 and SI = -3 -> AX = 4
        e = run_probe(VEC_AC, bytes([0, 0, 7, 0, 0, 0, 0, 0]), 0xFFFD, rest=b"\x90\x90\x90\xf4")
        self.assertEqual((e.kind, e.raw, e.extra), (2, 4, 0))
        self.assertEqual(mu.reg_read(r.UC_X86_REG_AX), 4)
        self.assertEqual((mu.reg_read(r.UC_X86_REG_SI), mu.reg_read(r.UC_X86_REG_BX)), (0xFFFD, 0xB0B0))
        self.assertEqual(mu.reg_read(r.UC_X86_REG_SP), 0x800)


    def test_text_probes_copy_the_text_and_do_the_routines_prologue(self):
        image = load_image()
        hdr_off = struct.unpack_from("<H", image, 20)[0]
        mu = Uc(UC_ARCH_X86, UC_MODE_16)
        mu.mem_map(0, 0x100000)
        mu.mem_write(TSR * 16, image)
        probe_text, probe_msg = struct.unpack_from("<HH", image, hdr_off + 132)
        for vec, off in ((VEC_TEXT, probe_text), (VEC_MSG, probe_msg)):
            mu.mem_write(vec * 4, struct.pack("<HH", off, TSR))
        mu.hook_add(UC_HOOK_INTR, real_mode_interrupt)
        mu.mem_write(GAME_DS * 16 + 0x100, b"Do not worry, \0")
        mu.mem_write(GAME_DS * 16 + 0x200, b"Long Sword is broken !\0")
        buf = TextBuffer(lambda a, n: bytes(mu.mem_read(a, n)), TSR * 16 + hdr_off)

        def call(vector, args, at):
            # the routine starts with INT (was PUSH BP / MOV BP,SP) then a NOP; its caller's
            # return address and arguments are on the stack
            mu.mem_write(CALLER * 16 + at, bytes((0xCD, vector, 0x90, 0xF4)))
            mu.mem_write(SS * 16 + 0x800, struct.pack("<HH", 0x1234, 0x5678) + args)
            for reg, value in ((r.UC_X86_REG_CS, CALLER), (r.UC_X86_REG_SS, SS), (r.UC_X86_REG_DS, GAME_DS),
                               (r.UC_X86_REG_ESP, 0x800), (r.UC_X86_REG_EBP, BP), (r.UC_X86_REG_ESI, 0x5151),
                               (r.UC_X86_REG_EAX, 0xAAAA), (r.UC_X86_REG_EFLAGS, IF | 2)):
                mu.reg_write(reg, value)
            mu.emu_start(CALLER * 16 + at, CALLER * 16 + at + 3)
            # as if PUSH BP / MOV BP,SP had run
            self.assertEqual(mu.reg_read(r.UC_X86_REG_SP), 0x7FE)
            self.assertEqual(mu.reg_read(r.UC_X86_REG_BP), 0x7FE)
            self.assertEqual(struct.unpack("<H", mu.mem_read(SS * 16 + 0x7FE, 2))[0], BP)
            for reg, want in ((r.UC_X86_REG_SI, 0x5151), (r.UC_X86_REG_AX, 0xAAAA), (r.UC_X86_REG_DS, GAME_DS)):
                self.assertEqual(mu.reg_read(reg), want)
            self.assertTrue(mu.reg_read(r.UC_X86_REG_EFLAGS) & IF)
            return buf.poll()

        recs = call(VEC_TEXT, struct.pack("<HHHH", 1, 0, 0, 119), 0x100)  # a portrait
        self.assertEqual([(x.kind, x.value, x.text) for x in recs], [(1, 119, "")])
        recs = call(VEC_TEXT, struct.pack("<HHHH", 2, 0x100, GAME_DS, 115), 0x110)
        self.assertEqual([(x.kind, x.value, x.text) for x in recs], [(2, 115, "Do not worry, ")])
        recs = call(VEC_MSG, struct.pack("<HH", 0x200, GAME_DS), 0x120)
        self.assertEqual([(x.kind, x.text) for x in recs], [(16, "Long Sword is broken !")])
        # "show the replies" passes no pointer: whatever lies above its arguments is not text
        recs = call(VEC_TEXT, struct.pack("<HHHH", 3, 0x100, GAME_DS, 0), 0x130)
        self.assertEqual([(x.kind, x.text) for x in recs], [(3, "")])


@unittest.skipIf(Uc is None, "unicorn is not installed")
class NextTests(unittest.TestCase):
    """PROBE_NEXT, in the game's overlaid combat routine: it goes on where the compare and the
    JNE it replaces would have, by way of a frame the overlay manager can fix up while the
    turn's summary is up."""
    DLG = (GAME_DS + 0x42CA - 0x4356) & 0xFFFF  # the dialogue window's overlay stub
    MOVED = (0x7777, 0x0100)  # where the fake overlay manager says the combat routine is now

    def setUp(self):
        image = load_image()
        self.mu = mu = Uc(UC_ARCH_X86, UC_MODE_16)
        mu.mem_map(0, 0x100000)
        mu.mem_write(TSR * 16, image)
        self.hdr = TSR * 16 + image.find(HDR_SIG)
        handler = image.find(bytes.fromhex("fb66600689e3368b4722"))  # sti, pushad, push es, ...
        self.assertGreater(handler, 0)
        mu.mem_write(VEC_NEXT * 4, struct.pack("<HH", handler, TSR))
        mu.hook_add(UC_HOOK_INTR, real_mode_interrupt)
        mu.mem_write(GAME_DS * 16 + 0x4979, struct.pack("<H", 44))  # a monster's turn now
        mu.mem_write(self.DLG * 16 + 0x25, b"\xCB")  # feeding the window: retf
        # waiting for Continue: the combat routine is moved meanwhile, and the overlay manager
        # fixes up the return address in the frame BP points at (push bp / mov bp,sp /
        # mov bx,[bp] / mov word [ss:bx+2],IP / mov word [ss:bx+4],CS / pop bp / retf)
        mu.mem_write(self.DLG * 16 + 0x34, bytes.fromhex("5589e58b5e00") + bytes.fromhex("36c74702") +
                     struct.pack("<H", self.MOVED[1]) + bytes.fromhex("36c74704") +
                     struct.pack("<H", self.MOVED[0]) + bytes.fromhex("5dcb"))

    def run_next(self, local, popups, until):
        """INT VEC_NEXT + 2 NOPs + the game's JNE +5 at CALLER:0600h, [BP-2] = LOCAL."""
        mu = self.mu
        mu.mem_write(CALLER * 16 + 0x600, bytes((0xCD, VEC_NEXT, 0x90, 0x90, 0x75, 0x05)))
        mu.mem_write(SS * 16 + BP - 2, struct.pack("<H", local))
        mu.mem_write(self.hdr + 140, struct.pack("<HH", 1, popups))  # the summary is ready
        msg = TSR * 16 + struct.unpack("<H", mu.mem_read(self.hdr + 144, 2))[0]
        mu.mem_write(msg, b"Slig attacks\0")
        regs = dict(cs=CALLER, ds=GAME_DS, ss=SS, esp=0x800, ebp=BP, eflags=IF | 2, eax=0x1111, ebx=0x2222,
                    ecx=0x3333, edx=0x4444, esi=0x5555, edi=0x6666, es=0x7070)
        for name, value in regs.items():
            mu.reg_write(getattr(r, "UC_X86_REG_" + name.upper()), value)
        mu.emu_start(CALLER * 16 + 0x600, until[0] * 16 + until[1], count=200000)
        self.assertEqual((mu.reg_read(r.UC_X86_REG_CS), mu.reg_read(r.UC_X86_REG_IP)), until)
        kept = [name for name in regs if name not in ("cs", "eflags")]
        self.assertEqual([mu.reg_read(getattr(r, "UC_X86_REG_" + name.upper())) for name in kept],
                         [regs[name] for name in kept])

    def test_no_summary_goes_on_as_the_jump_would(self):
        self.run_next(0, popups=0, until=(CALLER, 0x606))  # [BP-2] = 0: past the JNE
        self.run_next(3, popups=0, until=(CALLER, 0x60B))  # not 0: to its target

    def test_back_where_the_overlay_manager_says(self):
        """The summary shown, the way back is the one the overlay manager left in the frame."""
        self.run_next(3, popups=1, until=self.MOVED)
        self.assertEqual(self.mu.mem_read(self.hdr + 138, 2), struct.pack("<H", 1))  # the turn counted


@unittest.skipIf(Uc is None, "unicorn is not installed")
class UseItemTests(unittest.TestCase):
    """PROBE_USE_ITEM, where the game uses the item on the pointer on what's under it: on as the
    compare and JNE it replaces would go, or, for the Ledger's thieving tools, to the routine's
    end (DSUN.EXE: 7361Ah, 7361Dh and 7371Dh, less the address after the INT)."""
    NONE, SOME, DONE = 0x605, 0x608, 0x602 + 0x106

    def setUp(self):
        image = load_image()
        self.mu = mu = Uc(UC_ARCH_X86, UC_MODE_16)
        mu.mem_map(0, 0x100000)
        mu.mem_write(TSR * 16, image)
        self.hdr = TSR * 16 + image.find(HDR_SIG)
        handler = image.find(bytes.fromhex("fb66600689e3ba0300"))  # sti, pushad, push es, mov bx,sp, mov dx,3
        self.assertGreater(handler, 0)
        mu.mem_write(VEC_USE_ITEM * 4, struct.pack("<HH", handler, TSR))
        mu.hook_add(UC_HOOK_INTR, real_mode_interrupt)
        self.taken = 0

        def companion(uc, access, address, size, value, _):  # answers as soon as it's asked
            if address == self.hdr + 180:
                uc.mem_write(self.hdr + 182, struct.pack("<H", value))
                uc.mem_write(self.hdr + 186, struct.pack("<H", self.taken))
        mu.hook_add(UC_HOOK_MEM_WRITE, companion, begin=self.hdr + 180, end=self.hdr + 181)

    def run_use(self, si, until, on=1):
        mu = self.mu
        mu.mem_write(CALLER * 16 + 0x600, bytes((0xCD, VEC_USE_ITEM, 0x90, 0x90, 0x90)))
        mu.mem_write(self.hdr + 178, struct.pack("<H", on))
        mu.mem_write(TSR * 16 + struct.unpack("<H", mu.mem_read(self.hdr + 176, 2))[0], b"\0")
        for name, value in dict(cs=CALLER, ds=GAME_DS, ss=SS, esp=0x800, ebp=BP, eflags=IF | 2, esi=si).items():
            mu.reg_write(getattr(r, "UC_X86_REG_" + name.upper()), value)
        mu.emu_start(CALLER * 16 + 0x600, CALLER * 16 + until, count=100000)
        self.assertEqual((mu.reg_read(r.UC_X86_REG_IP), mu.reg_read(r.UC_X86_REG_SP), mu.reg_read(r.UC_X86_REG_SI)),
                         (until, 0x800, si))

    def test_nothing_there(self):
        self.run_use(0xFFFF, self.NONE)

    def test_not_ours(self):
        """The Ledger is told what was used on what: the pointer's item 1, item 231 in the
        segment the routine's "mov dx,<segment>" (3FEh past the INT) loads."""
        mu = self.mu
        mu.mem_write(GAME_DS * 16 + 0x17A0, struct.pack("<h", 1))
        mu.mem_write(CALLER * 16 + 0x602 + 0x3FE, struct.pack("<H", 0x9000))
        mu.mem_write(0x9000 * 16 + 1 * 10 + 0x44, struct.pack("<H", 231))
        self.run_use(300, self.SOME, on=0)
        self.run_use(300, self.SOME)  # the Ledger says it's not its tools
        self.assertEqual(struct.unpack("<HH", mu.mem_read(self.hdr + 184, 2) + mu.mem_read(self.hdr + 188, 2)),
                         (300, 231))

    def test_the_tools(self):
        self.taken = 1
        self.run_use(300, self.DONE)

    def test_xp(self):
        """What was lifted is worth XP (Kurzak's sword): before its text, DSCLOG's GIVE_XP calls
        the game's routine for a quest's XP (who, amount) and plays the quest's sound, once."""
        mu, calls = self.mu, []
        image = load_image()
        xp_who = image.find(HDR_SIG) + 262
        give_xp = image.find(bytes.fromhex("2e833e") + struct.pack("<H", xp_who) + bytes.fromhex("ff74"))
        self.assertGreater(give_xp, 0)
        to_game = GAME_DS - 0x4356  # (the game's segments, from its DS)
        xp, sound = (to_game + 0x4251) * 16 + 0x005C, (to_game + 0x1A0A) * 16 + 0x0663
        for at in (xp, sound):
            mu.mem_write(at, b"\xcb")  # retf

        def called(uc, address, size, _):
            sp = uc.reg_read(r.UC_X86_REG_SS) * 16 + uc.reg_read(r.UC_X86_REG_SP)
            args = struct.unpack("<HH", uc.mem_read(sp + 4, 4))
            calls.append(("xp", args) if address == xp else ("sound", args[:1]))
        mu.hook_add(UC_HOOK_CODE, called, begin=xp, end=xp)
        mu.hook_add(UC_HOOK_CODE, called, begin=sound, end=sound)
        back = 0xE000  # (past the image: where its RET comes back to)

        def run():
            for name, value in dict(cs=TSR, ds=GAME_DS, ss=SS, esp=0x7FE, ebp=BP).items():
                mu.reg_write(getattr(r, "UC_X86_REG_" + name.upper()), value)
            mu.mem_write(SS * 16 + 0x7FE, struct.pack("<H", back))
            mu.emu_start(TSR * 16 + give_xp, TSR * 16 + back, count=10000)
            self.assertEqual((mu.reg_read(r.UC_X86_REG_IP), mu.reg_read(r.UC_X86_REG_SP)), (back, 0x800))
        mu.mem_write(self.hdr + 262, struct.pack("<HH", 3, 200))  # Cilla (3), 200
        run()
        self.assertEqual(calls, [("xp", (3, 200)), ("sound", (53,))])
        self.assertEqual(struct.unpack("<H", mu.mem_read(self.hdr + 262, 2))[0], 0xFFFF)
        run()
        self.assertEqual(len(calls), 2)  # (asked for once)


@unittest.skipIf(Uc is None, "unicorn is not installed")
class PickKeyTests(unittest.TestCase):
    """PROBE_PICK, where the conversation window passes on a key it doesn't know: P asks the
    Ledger to pick a pocket only with that switched on too (bit 1), not for the tools alone."""
    JUMP = 0x7DD70 - 0x7D9FF

    def setUp(self):
        from dscompanion.gamepatch import VEC_PICK
        image = load_image()
        self.mu = mu = Uc(UC_ARCH_X86, UC_MODE_16)
        mu.mem_map(0, 0x100000)
        mu.mem_write(TSR * 16, image)
        self.hdr = TSR * 16 + image.find(HDR_SIG)
        handler = image.find(bytes.fromhex("fb66600689e3368147"))  # sti, pushad, push es, mov bx,sp, add [ss:bx+..]
        self.assertGreater(handler, 0)
        mu.mem_write(VEC_PICK * 4, struct.pack("<HH", handler, TSR))
        mu.hook_add(UC_HOOK_INTR, real_mode_interrupt)

        def companion(uc, access, address, size, value, _):  # answers at once, with nothing to show
            uc.mem_write(self.hdr + 174, struct.pack("<H", value))
        mu.hook_add(UC_HOOK_MEM_WRITE, companion, begin=self.hdr + 172, end=self.hdr + 173)
        mu.mem_write(TSR * 16 + struct.unpack("<H", mu.mem_read(self.hdr + 176, 2))[0], b"\0")

    def press(self, key, on):
        mu = self.mu
        mu.mem_write(CALLER * 16 + 0x600, bytes((0xCD, 0xFC, 0x90)))
        mu.mem_write(self.hdr + 178, struct.pack("<H", on))
        mu.mem_write(SS * 16 + BP - 0x0C, struct.pack("<H", key))
        for name, value in dict(cs=CALLER, ds=GAME_DS, ss=SS, esp=0x800, ebp=BP, eflags=IF | 2).items():
            mu.reg_write(getattr(r, "UC_X86_REG_" + name.upper()), value)
        before = struct.unpack("<H", mu.mem_read(self.hdr + 172, 2))[0]
        mu.emu_start(CALLER * 16 + 0x600, CALLER * 16 + 0x602 + self.JUMP, count=200000)
        self.assertEqual(mu.reg_read(r.UC_X86_REG_IP), 0x602 + self.JUMP)
        return struct.unpack("<H", mu.mem_read(self.hdr + 172, 2))[0] != before

    def test_p_only_with_its_switch(self):
        P = 0x1950
        self.assertFalse(self.press(P, 0))
        self.assertFalse(self.press(P, 1))  # (the tools only)
        self.assertTrue(self.press(P, 3))
        self.assertTrue(self.press(0x1970, 3))  # (p too)
        self.assertFalse(self.press(0x1E41, 3))  # (another key)


@unittest.skipIf(Uc is None, "unicorn is not installed")
class BeltTests(unittest.TestCase):
    """PROBE_BELT, at the end of the game's thief skill routine (where "mov ax,si" was): a thief
    wearing a belt gets 5 more to pick pockets and open locks, with SKILLS_ON's belt bit."""
    CREATURES, ITEMS = 0x9000, 0xA000

    def setUp(self):
        from dscompanion.gamepatch import VEC_BELT
        image = load_image()
        self.mu = mu = Uc(UC_ARCH_X86, UC_MODE_16)
        mu.mem_map(0, 0x100000)
        mu.mem_write(TSR * 16, image)
        self.hdr = TSR * 16 + image.find(HDR_SIG)
        skills_on = image.find(HDR_SIG) + 266
        handler = image.find(bytes.fromhex("fb2ef606") + struct.pack("<H", skills_on) + b"\x02")
        self.assertGreater(handler, 0)
        mu.mem_write(VEC_BELT * 4, struct.pack("<HH", handler, TSR))
        mu.hook_add(UC_HOOK_INTR, real_mode_interrupt)
        mu.mem_write(GAME_DS * 16 + 0x1665, struct.pack("<HH", 0, self.CREATURES))
        mu.mem_write(GAME_DS * 16 + 0x165D, struct.pack("<HH", 0, self.ITEMS))
        things = (GAME_DS + 0x3972 - 0x4356) * 16 + 0xC36  # (the things table, from the game's DS)
        # object 3: creature 1, whose first list is object 10: item 4
        for thing, kind, index in ((3, 2, 1), (10, 1, 4)):
            mu.mem_write(things + thing * 3, struct.pack("<BH", kind, index))
        mu.mem_write(self.CREATURES * 16 + 0x3A + 8, struct.pack("<HHH", 10, 9999, 9999))
        self.wear(5)

    def wear(self, slot):
        rec = bytearray(21)
        struct.pack_into("<H", rec, 4, 9999)
        rec[0x11] = slot
        self.mu.mem_write(self.ITEMS * 16 + 4 * 21, bytes(rec))

    def chance(self, skill, on=2, si=40):
        mu = self.mu
        mu.mem_write(self.hdr + 266, struct.pack("<H", on))
        mu.mem_write(SS * 16 + BP + 8, struct.pack("<I", skill))
        mu.mem_write(CALLER * 16 + 0x600, bytes((0xCD, 0xD9)))
        for name, value in dict(cs=CALLER, ds=GAME_DS, ss=SS, esp=0x800, ebp=BP, eflags=IF | 2,
                                esi=si, edi=3, ebx=0x1234, ecx=0x5678, edx=0x9ABC, es=0x4444).items():
            mu.reg_write(getattr(r, "UC_X86_REG_" + name.upper()), value)
        mu.emu_start(CALLER * 16 + 0x600, CALLER * 16 + 0x602, count=10000)
        self.assertEqual([mu.reg_read(x) for x in (r.UC_X86_REG_SP, r.UC_X86_REG_SI, r.UC_X86_REG_DI, r.UC_X86_REG_BX,
                                                   r.UC_X86_REG_CX, r.UC_X86_REG_DX, r.UC_X86_REG_ES)],
                         [0x800, si, 3, 0x1234, 0x5678, 0x9ABC, 0x4444])
        return mu.reg_read(r.UC_X86_REG_AX)

    def test_pockets_and_locks(self):
        self.assertEqual([self.chance(skill) for skill in range(4)], [45, 45, 40, 40])

    def test_off(self):
        self.assertEqual(self.chance(0, on=1), 40)  # (the stealth bit alone)
        self.assertEqual(self.chance(0, on=0), 40)

    def test_no_belt(self):
        self.wear(20)  # (in the pack)
        self.assertEqual(self.chance(1), 40)


@unittest.skipIf(Uc is None, "unicorn is not installed")
class RingTests(unittest.TestCase):
    """The ring probes: a worn ring's plus counts for AC and (all worn rings) on saves."""
    THINGS_SEG, CREATURES, ITEMS, TYPES = 0x8000, 0x9000, 0xA000, 0xB000

    def setUp(self):
        image = load_image()
        self.mu = mu = Uc(UC_ARCH_X86, UC_MODE_16)
        mu.mem_map(0, 0x100000)
        mu.mem_write(TSR * 16, image)
        # the handlers aren't in the header: find them by their first instructions
        ac = image.find(bytes.fromhex("268a470f98" "83f966"))
        save = image.find(bytes.fromhex("5589e5505351520631f6c45e02"))
        self.assertGreater(min(ac, save), 0)
        mu.mem_write(VEC_RING_AC * 4, struct.pack("<HH", ac, TSR))
        mu.mem_write(VEC_RING_SAVE * 4, struct.pack("<HH", save, TSR))
        mu.hook_add(UC_HOOK_INTR, real_mode_interrupt)
        mu.mem_write(GAME_DS * 16 + 0x1665, struct.pack("<HH", 0, self.CREATURES))
        mu.mem_write(GAME_DS * 16 + 0x165D, struct.pack("<HH", 0, self.ITEMS))
        things = self.THINGS_SEG * 16 + 0xC36
        # object 3: creature 1, whose lists start at objects 10 (item 4, then 5) and 11 (item 7)
        for thing, kind, index in ((3, 2, 1), (10, 1, 4), (11, 1, 7), (12, 1, 5)):
            mu.mem_write(things + thing * 3, struct.pack("<BH", kind, index))
        mu.mem_write(self.CREATURES * 16 + 0x3A + 8, struct.pack("<HHH", 10, 9999, 11))
        # items: type, slot, plus, next
        for item, typ, slot, plus, nxt in ((4, 102, 4, 1, 5), (5, 102, 0xFF, 2, 9999), (7, 102, 4, 2, 9999)):
            rec = bytearray(21)
            struct.pack_into("<H", rec, 4, nxt)
            struct.pack_into("<H", rec, 0x0A, typ)
            rec[0x11], rec[0x14] = slot, plus
            mu.mem_write(self.ITEMS * 16 + item * 21, bytes(rec))
        self.at = 0x600

    def run_at(self, code, **regs):
        mu = self.mu
        self.at += 0x20
        mu.mem_write(CALLER * 16 + self.at, code)
        for name, value in dict(cs=CALLER, ds=GAME_DS, ss=SS, esp=0x800, ebp=BP, eflags=IF | 2, **regs).items():
            mu.reg_write(getattr(r, "UC_X86_REG_" + name.upper()), value)
        mu.emu_start(CALLER * 16 + self.at, CALLER * 16 + self.at + 2)
        self.assertEqual(mu.reg_read(r.UC_X86_REG_SP), 0x800)

    def save(self, thing):
        """INT VEC_RING_SAVE where "xor si,si" was, then the code after it in the game."""
        code = bytes((0xCD, VEC_RING_SAVE)) + bytes.fromhex("8bdf6bdb03b8") + struct.pack("<H", self.THINGS_SEG)
        self.run_at(code, edi=thing, esi=0x5555, eax=0x1111, ebx=0x2222, ecx=0x3333, edx=0x4444, es=0x6666)
        mu = self.mu
        self.assertEqual([mu.reg_read(x) for x in (r.UC_X86_REG_AX, r.UC_X86_REG_BX, r.UC_X86_REG_CX,
                                                   r.UC_X86_REG_DX, r.UC_X86_REG_ES, r.UC_X86_REG_DI,
                                                   r.UC_X86_REG_BP, r.UC_X86_REG_DS)],
                         [0x1111, 0x2222, 0x3333, 0x4444, 0x6666, thing, BP, GAME_DS])
        return mu.reg_read(r.UC_X86_REG_SI)

    def test_saves_count_worn_rings(self):
        self.assertEqual(self.save(3), 3)  # items 4 and 7 (+1, +2); item 5 is only carried

    def test_saves_not_a_creature(self):
        self.assertEqual(self.save(10), 0)

    def test_saves_count_a_cloak_of_protection(self):
        """Item 7 made a cloak of protection (+2, the second of DSCLOG's types) worn on the back:
        counted once the types are in (TYPES_FIRST, the header's +212), with ring 4's +1."""
        mu = self.mu
        rec = self.ITEMS * 16 + 7 * 21
        mu.mem_write(rec + 0x0A, struct.pack("<H", 116))
        mu.mem_write(rec + 0x11, bytes([12]))
        hdr = TSR * 16 + load_image().find(HDR_SIG)
        self.assertEqual(self.save(3), 1)  # no types yet: the ring alone
        mu.mem_write(hdr + 212, struct.pack("<H", 115))
        self.assertEqual(self.save(3), 3)
        mu.mem_write(rec + 0x11, bytes([0xFF]))  # only carried
        self.assertEqual(self.save(3), 1)

    def test_ac_counts_rings(self):
        """AX gets the type's flags (sign-extended); bit 80h is set for the ring type."""
        mu = self.mu
        for typ, flags, want in ((102, 0x00, 0x0080), (6, 0x80, 0xFF80), (6, 0x00, 0), (102, 0x02, 0x0082)):
            mu.mem_write(self.TYPES * 16 + 0x0F, bytes([flags]))
            self.run_at(bytes((0xCD, VEC_RING_AC)), es=self.TYPES, ebx=0, ecx=typ, eax=0x1234)
            self.assertEqual(mu.reg_read(r.UC_X86_REG_AX), want)
            self.assertEqual((mu.reg_read(r.UC_X86_REG_CX), mu.reg_read(r.UC_X86_REG_BX)), (typ, 0))



@unittest.skipIf(Uc is None, "unicorn is not installed")
class ProtectionRuleTests(RingTests):
    """RULE_PROTECTION: the better ring only, a ring's AC lost to magical armour, a cloak of
    protection lost to magical or metal armour (helms too) or a shield."""
    RULES, TYPES_FIRST = 170, 212  # the header's words
    CLOAK = 116  # (the second of DSCLOG's types, the first being 115)
    # (RingTests' own are the game's way, without the rule)
    test_saves_count_worn_rings = test_saves_count_a_cloak_of_protection = test_ac_counts_rings = None

    def setUp(self):
        super().setUp()
        mu = self.mu
        hdr = TSR * 16 + load_image().find(HDR_SIG)
        mu.mem_write(hdr + self.RULES, struct.pack("<H", 1024))
        mu.mem_write(hdr + self.TYPES_FIRST, struct.pack("<H", 115))
        mu.mem_write(GAME_DS * 16 + 0x1669, struct.pack("<HH", 0, self.TYPES))
        # types: flags word, material (+08h), AC flag (+0Fh)
        for typ, flags, material, ac in ((4, 4, 5, 0x80), (6, 0, 5, 0x80), (57, 0, 4, 0x80), (89, 0, 0x84, 0x84),
                                         (15, 0, 1, 0x80), (self.CLOAK, 0, 5, 0x80), (102, 0, 0x40, 0)):
            rec = bytearray(0x14)
            struct.pack_into("<H", rec, 0, flags)
            rec[0x08], rec[0x0F] = material, ac
            mu.mem_write(self.TYPES * 16 + typ * 0x14, bytes(rec))
        self.wear(7, 102, 11, 2)  # creature 1: ring 4 (+1) on the left hand's finger, ring 7 (+2) the right's

    def wear(self, item, typ, slot, plus=0):
        rec = self.ITEMS * 16 + item * 21
        self.mu.mem_write(rec + 0x0A, struct.pack("<H", typ))
        self.mu.mem_write(rec + 0x11, bytes([slot]))
        self.mu.mem_write(rec + 0x14, bytes([plus & 0xFF]))

    def counts(self, item, typ):
        """INT VEC_RING_AC for creature 1's item ITEM of type TYPE: whether bit 80h is left set
        (the things table's segment where the game's code has it, A8h bytes past the INT)."""
        self.mu.mem_write(CALLER * 16 + self.at + 0x20 + 2 + 0xA8, struct.pack("<H", self.THINGS_SEG))
        self.run_at(bytes((0xCD, VEC_RING_AC)), es=self.TYPES, ebx=typ * 0x14, ecx=typ, edx=item, edi=3,
                    eax=0x1234)
        mu = self.mu
        self.assertEqual([mu.reg_read(x) for x in (r.UC_X86_REG_BX, r.UC_X86_REG_CX, r.UC_X86_REG_DX,
                                                   r.UC_X86_REG_DI, r.UC_X86_REG_ES)],
                         [typ * 0x14, typ, item, 3, self.TYPES])
        return bool(mu.reg_read(r.UC_X86_REG_AX) & 0x80)

    def test_the_better_ring(self):
        self.assertEqual((self.counts(4, 102), self.counts(7, 102)), (False, True))
        self.assertEqual(self.save(3), 2)
        self.wear(7, 102, 11, 1)  # equal: the left hand's
        self.assertEqual((self.counts(4, 102), self.counts(7, 102)), (True, False))
        self.assertEqual(self.save(3), 1)

    def test_rule_off(self):
        self.mu.mem_write(TSR * 16 + load_image().find(HDR_SIG) + self.RULES, struct.pack("<H", 0))
        self.assertEqual((self.counts(4, 102), self.counts(7, 102)), (True, True))
        self.assertEqual(self.save(3), 3)

    def test_ring_ac_lost_to_magical_armour(self):
        self.wear(5, 6, 9, 1)  # leather chest armour +1 worn
        self.assertEqual((self.counts(4, 102), self.counts(7, 102)), (False, False))
        self.assertEqual(self.save(3), 2)  # (the saves stay)

    def test_cloak(self):
        self.wear(7, self.CLOAK, 12, 1)
        self.wear(5, 15, 9)  # bone scale: natural
        self.assertTrue(self.counts(7, self.CLOAK))
        self.assertEqual(self.save(3), 2)  # ring 4 and the cloak
        for typ, slot, plus in ((57, 9, 0), (6, 9, 1), (4, 10, 0), (4, 3, 0), (89, 7, 0), (6, 7, 1)):
            self.wear(5, typ, slot, plus)  # metal, magical leather, a shield in either hand, metal or magic helm
            self.assertFalse(self.counts(7, self.CLOAK), (typ, slot, plus))
            self.assertEqual(self.save(3), 1, (typ, slot, plus))
        self.wear(5, 57, 0xFF)  # only carried
        self.assertTrue(self.counts(7, self.CLOAK))


@unittest.skipIf(Uc is None, "unicorn is not installed")
class BracersTests(ProtectionRuleTests):
    """Bracers of defense (the ninth of DSCLOG's types, worn in the arm armour's slot): their plus
    counts for AC without armour on the arms, legs or chest, with or without RULE_PROTECTION, and
    they aren't armour to a ring's or cloak's rule."""
    BRACERS = 123
    test_the_better_ring = test_rule_off = test_ring_ac_lost_to_magical_armour = test_cloak = None

    def setUp(self):
        super().setUp()
        rec = bytearray(0x14)
        rec[0x08], rec[0x09], rec[0x0F] = 0x40, 3, 0x80
        self.mu.mem_write(self.TYPES * 16 + self.BRACERS * 0x14, bytes(rec))
        self.wear(7, self.BRACERS, 0, 4)  # creature 1: ring 4 (+1) on a finger, the bracers on the arms

    def test_alone(self):
        self.assertTrue(self.counts(7, self.BRACERS))
        self.assertTrue(self.counts(4, 102))  # (not magical armour: the ring counts)

    def test_lost_to_armour(self):
        for typ, slot, plus in ((6, 9, 0), (15, 6, 0), (57, 9, 1)):  # leather, bone scale legs, metal +1
            self.wear(5, typ, slot, plus)
            self.assertFalse(self.counts(7, self.BRACERS), (typ, slot))
        for typ, slot in ((4, 10), (89, 7)):  # a shield, a helm: they stay
            self.wear(5, typ, slot)
            self.assertTrue(self.counts(7, self.BRACERS), (typ, slot))
        self.wear(5, 6, 0xFF)  # armour only carried
        self.assertTrue(self.counts(7, self.BRACERS))

    def test_without_the_rule(self):
        self.mu.mem_write(TSR * 16 + load_image().find(HDR_SIG) + self.RULES, struct.pack("<H", 0))
        self.wear(5, 6, 9)
        self.assertFalse(self.counts(7, self.BRACERS))
        self.wear(5, 6, 0xFF)
        self.assertTrue(self.counts(7, self.BRACERS))

    def test_not_before_the_types(self):
        """Before DSCLOG's types are in, type 123 is nothing of its own: the game's way."""
        self.mu.mem_write(TSR * 16 + load_image().find(HDR_SIG) + self.TYPES_FIRST, struct.pack("<H", 0))
        self.wear(5, 6, 9)
        self.assertTrue(self.counts(7, self.BRACERS))


@unittest.skipIf(Uc is None, "unicorn is not installed")
class ScriptRandTests(unittest.TestCase):
    """The scripts' random command (PROBE_SCRIPT_RAND): EAX and EDX N + 1, as the replaced code
    leaves them, and the command recorded with its result, N, the script's position and the
    searches' counts."""
    COUNTS = 0xA000

    def setUp(self):
        image = load_image()
        self.mu = mu = Uc(UC_ARCH_X86, UC_MODE_16)
        mu.mem_map(0, 0x100000)
        mu.mem_write(TSR * 16, image)
        self.hdr_off = struct.unpack_from("<H", image, 20)[0]
        self.ring = struct.unpack_from("<H", image, 16)[0]
        at = image.find(bytes.fromhex("fb66406689c25589e5"))
        self.assertGreater(at, 0)
        mu.mem_write(VEC_SCRIPT_RAND * 4, struct.pack("<HH", at, TSR))
        mu.hook_add(UC_HOOK_INTR, real_mode_interrupt)
        data = (GAME_DS + 0x3781 - 0x4356) * 16
        mu.mem_write(data + 0x192, b"\x01")  # the running script's slot: 1, at 2116
        mu.mem_write(data + 0x295 + 2, struct.pack("<H", 2116))
        mu.mem_write(GAME_DS * 16 + 0x1356, struct.pack("<HH", 0, self.COUNTS))
        mu.mem_write(self.COUNTS * 16 + 21 * 2, struct.pack("<3H", 4, 3, 2))  # junk, hay, wardrobe

    def test_recorded(self):
        mu = self.mu
        mu.mem_write(SS * 16 + 0x7FC, struct.pack("<I", 0x7000))  # rand(), pushed
        mu.mem_write(CALLER * 16 + 0x600, bytes((0xCD, VEC_SCRIPT_RAND)))
        for name, value in dict(cs=CALLER, ds=GAME_DS, ss=SS, esp=0x7FC, ebp=BP, eflags=IF | 2, eax=10,
                                ebx=0x2222, ecx=0x3333, edx=0x4444, esi=0x1111, edi=0x5555, es=0x6666).items():
            mu.reg_write(getattr(r, "UC_X86_REG_" + name.upper()), value)
        mu.emu_start(CALLER * 16 + 0x600, CALLER * 16 + 0x602)
        self.assertEqual([mu.reg_read(x) for x in (r.UC_X86_REG_SP, r.UC_X86_REG_EAX, r.UC_X86_REG_EDX, r.UC_X86_REG_BX,
                                                   r.UC_X86_REG_CX, r.UC_X86_REG_SI, r.UC_X86_REG_DI, r.UC_X86_REG_BP,
                                                   r.UC_X86_REG_DS, r.UC_X86_REG_ES)],
                         [0x7FC, 11, 11, 0x2222, 0x3333, 0x1111, 0x5555, BP, GAME_DS, 0x6666])
        seq, _, nent = struct.unpack("<HHH", mu.mem_read(TSR * 16 + self.hdr_off + 8, 6))
        e = Entry.parse(bytes(mu.mem_read(TSR * 16 + self.ring + ((seq - 1) % nent) * Entry.SIZE, Entry.SIZE)))
        self.assertEqual((e.kind, e.raw & 0xFF, e.raw >> 8 & 0xFF, e.extra), (5, 0x7000 * 11 >> 15, 10, 2116))
        self.assertEqual((e.arg(2), e.arg(4), e.arg(6)), (4, 3, 2))
        self.assertEqual((e.ip, e.cs), (0x602, CALLER))  # (the code after the INT)


class KindTableTests(unittest.TestCase):
    def test_kinds_match_the_companion(self):
        """DSCLOG's weapon kinds by item type are specialize.py's."""
        from dscompanion import specialize
        image = load_image()
        want = bytearray(128)
        for t, k in specialize.KIND_OF_TYPE.items():
            want[t] = k + 1
        self.assertGreater(image.find(bytes(want)), 0)


@unittest.skipIf(Uc is None, "unicorn is not installed")
class SpecializeTests(unittest.TestCase):
    """Weapon specialization in the weapon attack routine (PROBE_ATTACKS, PROBE_SPEC_DAMAGE): the
    attacks a round, the THAC0, the damage bonus and dice, by the attacker's chosen kinds."""
    SHEETS = 0x8000
    RULES = 170
    LONG_SWORD, AXE = 45, 22  # (item types: obsidian long sword, axe)

    def setUp(self):
        image = load_image()
        self.mu = mu = Uc(UC_ARCH_X86, UC_MODE_16)
        mu.mem_map(0, 0x100000)
        mu.mem_write(TSR * 16, image)
        attacks = image.find(bytes.fromhex("982ef706"))
        damage = image.find(bytes.fromhex("0146ee2ef706"))
        self.assertGreater(attacks, 0)
        self.assertGreater(damage, 0)
        mu.mem_write(VEC_ATTACKS * 4, struct.pack("<HH", attacks, TSR))
        mu.mem_write(VEC_SPEC_DAMAGE * 4, struct.pack("<HH", damage, TSR))
        mu.hook_add(UC_HOOK_INTR, real_mode_interrupt)
        mu.mem_write(GAME_DS * 16 + 0x1661, struct.pack("<HH", 0, self.SHEETS))

    def attack(self, halves, weapon, chosen=(), classes=(9, 0, 0), levels=(5, 0, 0), rules=4096, missile=False, race=0):
        """(attacks in halves, THAC0, damage bonus, sides) after both probes, with THAC0 15, a
        damage bonus of 1 before the STR bonus of 2 is added, 1d8."""
        mu = self.mu
        mu.mem_write(TSR * 16 + load_image().find(HDR_SIG) + self.RULES, struct.pack("<H", rules))
        sheet = bytearray(0x47)
        for i, k in enumerate(chosen):
            sheet[0x14 + i] = k + 1
        sheet[0x21:0x24], sheet[0x24:0x27] = bytes(classes), bytes(levels)
        sheet[0x18] = race
        mu.mem_write(self.SHEETS * 16 + 3 * 0x47, bytes(sheet))  # (sheet 3)
        mu.mem_write(SS * 16 + BP + 0x0A, struct.pack("<H", 15))
        mu.mem_write(SS * 16 + BP + 0x10, struct.pack("<H", 3))
        mu.mem_write(SS * 16 + BP + 0x14, struct.pack("<HH", weapon, 2 if missile else 0))
        mu.mem_write(SS * 16 + BP - 0x12, struct.pack("<HHH", 1, 8, 1))  # damage bonus, sides, count
        mu.mem_write(CALLER * 16 + 0x600, bytes((0xCD, VEC_ATTACKS, 0x90, 0x90, 0xB8, 2, 0, 0xCD, VEC_SPEC_DAMAGE, 0x90)))
        for name, value in dict(cs=CALLER, ds=GAME_DS, ss=SS, esp=0x7FC, ebp=BP, eflags=IF | 2, eax=halves,
                                ebx=0x2222, ecx=0x3333, edx=0x4444, esi=0x5555, es=0x6666).items():
            mu.reg_write(getattr(r, "UC_X86_REG_" + name.upper()), value)
        mu.emu_start(CALLER * 16 + 0x600, CALLER * 16 + 0x60A)
        self.assertEqual([mu.reg_read(x) for x in (r.UC_X86_REG_SP, r.UC_X86_REG_BX, r.UC_X86_REG_CX, r.UC_X86_REG_DX,
                                                   r.UC_X86_REG_SI, r.UC_X86_REG_ES)],
                         [0x7FC, 0x2222, 0x3333, 0x4444, 0x5555, 0x6666])
        attacks, = struct.unpack("<h", mu.mem_read(SS * 16 + BP - 8, 2))
        thac0, = struct.unpack("<h", mu.mem_read(SS * 16 + BP + 0x0A, 2))
        bonus, sides = struct.unpack("<hh", mu.mem_read(SS * 16 + BP - 0x12, 4))
        return attacks, thac0, bonus, sides

    def test_off(self):
        self.assertEqual(self.attack(3, self.AXE, chosen=(0,), rules=0), (3, 15, 3, 8))

    def test_no_choices_as_the_game(self):
        """Monsters, and characters who haven't chosen yet: the game's own numbers."""
        self.assertEqual(self.attack(3, self.AXE), (3, 15, 3, 8))

    def test_specialization(self):
        self.assertEqual(self.attack(3, self.LONG_SWORD, chosen=(0,), levels=(4, 0, 0)), (3, 14, 5, 8))

    def test_other_kind_plain_rate(self):
        self.assertEqual(self.attack(3, self.AXE, chosen=(0,)), (2, 15, 3, 8))
        self.assertEqual(self.attack(4, self.AXE, chosen=(0,), levels=(7, 0, 0)), (3, 15, 3, 8))
        self.assertEqual(self.attack(3, 9999, chosen=(0,)), (2, 15, 3, 8))  # (bare hands: no kind)

    def test_mastery(self):
        self.assertEqual(self.attack(3, self.LONG_SWORD, chosen=(0,), levels=(5, 0, 0)), (3, 12, 6, 8))

    def test_grand_mastery(self):
        self.assertEqual(self.attack(4, self.LONG_SWORD, chosen=(0,), levels=(9, 0, 0)), (6, 12, 6, 10))

    def test_gladiator_weapons(self):
        """A gladiator: specialization with each chosen kind, never mastery."""
        glad = dict(classes=(10, 0, 0), levels=(9, 0, 0))
        self.assertEqual(self.attack(4, self.AXE, chosen=(0, 5), **glad), (4, 14, 5, 8))
        self.assertEqual(self.attack(4, self.LONG_SWORD, chosen=(0, 5), **glad), (4, 14, 5, 8))

    def test_ranger_expertise(self):
        """A ranger: the rate with the chosen kind, no bonuses; another kind, the plain rate."""
        ranger = dict(classes=(13, 0, 0), levels=(4, 0, 0))
        self.assertEqual(self.attack(3, self.LONG_SWORD, chosen=(0,), **ranger), (3, 15, 3, 8))
        self.assertEqual(self.attack(3, self.AXE, chosen=(0,), **ranger), (2, 15, 3, 8))

    def test_missile_keeps_its_rate(self):
        self.assertEqual(self.attack(4, 1, chosen=(13,), levels=(4, 0, 0), missile=True), (4, 14, 5, 8))  # (a bow)

    def test_dual_class(self):
        """A human fighter turned preserver: the game's numbers until its preserver level passes
        the fighter's, then mastery again (specialize.skill)."""
        human = dict(classes=(11, 9, 0), race=1)
        self.assertEqual(self.attack(2, self.LONG_SWORD, chosen=(0,), levels=(3, 5, 0), **human), (2, 15, 3, 8))
        self.assertEqual(self.attack(2, self.LONG_SWORD, chosen=(0,), levels=(6, 5, 0), **human), (2, 12, 6, 8))

    def test_not_a_warrior(self):
        self.assertEqual(self.attack(2, self.AXE, chosen=(0,), classes=(11, 0, 0)), (2, 15, 3, 8))

    def dam_line(self, halves, weapon, chosen=(), classes=(9, 0, 0), levels=(5, 0, 0), rules=4096):
        """(attacks, bonus, sides, count) for the DAM line (PROBE_DAM_LINE): bonus 4, 1d8 pushed."""
        mu = self.mu
        at = load_image().find(bytes.fromhex("268a472a2ef706"))
        self.assertGreater(at, 0)
        mu.mem_write(VEC_DAM_LINE * 4, struct.pack("<HH", at, TSR))
        mu.mem_write(TSR * 16 + load_image().find(HDR_SIG) + self.RULES, struct.pack("<H", rules))
        sheet = bytearray(0x47)
        sheet[0x2A] = halves
        for i, k in enumerate(chosen):
            sheet[0x14 + i] = k + 1
        sheet[0x21:0x24], sheet[0x24:0x27] = bytes(classes), bytes(levels)
        mu.mem_write(self.SHEETS * 16, bytes(sheet))
        mu.mem_write(SS * 16 + 0x7F6, struct.pack("<HHH", 1, 8, 4))  # pushed: count, sides, bonus
        mu.mem_write(CALLER * 16 + 0x600, bytes((0xCD, VEC_DAM_LINE, 0x90, 0x90)))
        for name, value in dict(cs=CALLER, ds=GAME_DS, ss=SS, esp=0x7F6, ebp=BP, eflags=IF | 2, eax=0x1200,
                                ebx=0, edx=0x4444, esi=weapon, es=self.SHEETS).items():
            mu.reg_write(getattr(r, "UC_X86_REG_" + name.upper()), value)
        mu.emu_start(CALLER * 16 + 0x600, CALLER * 16 + 0x604)
        self.assertEqual([mu.reg_read(x) for x in (r.UC_X86_REG_SP, r.UC_X86_REG_BP, r.UC_X86_REG_DX, r.UC_X86_REG_SI)],
                         [0x7F6, BP, 0x4444, weapon])
        count, sides, bonus = struct.unpack("<HHH", mu.mem_read(SS * 16 + 0x7F6, 6))
        return mu.reg_read(r.UC_X86_REG_AX) & 0xFF, bonus, sides, count

    def test_dam_line(self):
        self.assertEqual(self.dam_line(3, self.AXE, rules=0), (3, 4, 8, 1))
        self.assertEqual(self.dam_line(3, self.AXE, chosen=(0,)), (2, 4, 8, 1))
        self.assertEqual(self.dam_line(3, self.LONG_SWORD, chosen=(0,), levels=(4, 0, 0)), (3, 6, 8, 1))
        self.assertEqual(self.dam_line(4, self.LONG_SWORD, chosen=(0,), levels=(9, 0, 0)), (6, 7, 10, 1))


    ITEMS, TYPES, WHO = 0x8800, 0x9000, 0x9800

    def view_dam(self, halves, weapon, chosen=(), classes=(9, 0, 0), levels=(5, 0, 0), rules=4096, missile=False):
        """(attacks, bonus, sides) for View Character's DAM line (PROBE_VIEW_DAM): DX the bonus 4,
        1d8, character 2 on show, its weapon item 1."""
        mu = self.mu
        at = load_image().find(bytes.fromhex("8956f22ef706"))
        self.assertGreater(at, 0)
        mu.mem_write(VEC_VIEW_DAM * 4, struct.pack("<HH", at, TSR))
        mu.mem_write(TSR * 16 + load_image().find(HDR_SIG) + self.RULES, struct.pack("<H", rules))
        sheet = bytearray(0x47)
        for i, k in enumerate(chosen):
            sheet[0x14 + i] = k + 1
        sheet[0x21:0x24], sheet[0x24:0x27] = bytes(classes), bytes(levels)
        mu.mem_write(self.SHEETS * 16 + 2 * 0x47, bytes(sheet))
        mu.mem_write(GAME_DS * 16 + 0x165D, struct.pack("<HH", 0, self.ITEMS))
        mu.mem_write(GAME_DS * 16 + 0x1669, struct.pack("<HH", 0, self.TYPES))
        mu.mem_write(self.ITEMS * 16 + 0x15 + 0x0A, struct.pack("<H", weapon))
        mu.mem_write(self.TYPES * 16 + weapon * 0x14, bytes((2 if missile else 1,)))
        mu.mem_write(self.WHO * 16 + 0x25B, struct.pack("<H", 2))
        mu.mem_write(CALLER * 16 + 0x602 - 0x84, struct.pack("<H", self.WHO))
        mu.mem_write(SS * 16 + BP - 0x0E, struct.pack("<HHHHHHH", 0, 0, 1, 0, halves, 8, 1))  # bonus .. count
        mu.mem_write(CALLER * 16 + 0x600, bytes((0xCD, VEC_VIEW_DAM, 0x90)))
        for name, value in dict(cs=CALLER, ds=GAME_DS, ss=SS, esp=0x7FC, ebp=BP, eflags=IF | 2, eax=0x1111,
                                ebx=0x2222, ecx=0x3333, edx=4, esi=0x5555, edi=0x7777, es=0x6666).items():
            mu.reg_write(getattr(r, "UC_X86_REG_" + name.upper()), value)
        mu.emu_start(CALLER * 16 + 0x600, CALLER * 16 + 0x603)
        self.assertEqual([mu.reg_read(getattr(r, "UC_X86_REG_" + x)) for x in ("SP", "AX", "BX", "CX", "DX", "SI", "DI", "ES")],
                         [0x7FC, 0x1111, 0x2222, 0x3333, 4, 0x5555, 0x7777, 0x6666])
        bonus, = struct.unpack("<h", mu.mem_read(SS * 16 + BP - 0x0E, 2))
        attacks, sides = struct.unpack("<hh", mu.mem_read(SS * 16 + BP - 6, 2) + mu.mem_read(SS * 16 + BP - 4, 2))
        return attacks, bonus, sides

    def test_view_dam(self):
        self.assertEqual(self.view_dam(3, self.AXE, chosen=(0,), rules=0), (3, 4, 8))
        self.assertEqual(self.view_dam(3, self.AXE), (3, 4, 8))
        self.assertEqual(self.view_dam(3, self.AXE, chosen=(0,)), (2, 4, 8))
        self.assertEqual(self.view_dam(3, self.LONG_SWORD, chosen=(0,), levels=(4, 0, 0)), (3, 6, 8))
        self.assertEqual(self.view_dam(4, self.LONG_SWORD, chosen=(0,), levels=(9, 0, 0)), (6, 7, 10))
        self.assertEqual(self.view_dam(4, 1, chosen=(13,), levels=(4, 0, 0), missile=True), (4, 6, 8))
        self.assertEqual(self.view_dam(3, 1, chosen=(0,), missile=True), (3, 4, 8))



@unittest.skipIf(Uc is None, "unicorn is not installed")
class CanUseTests(unittest.TestCase):
    """PROBE_CAN_USE (class restrictions) against restrict.py, for every class pairing, race and
    item type of tests/test_restrict.py."""
    TYPES_SEG, SHEET = 0x8000, 0x9000
    RULES = 170

    def setUp(self):
        image = load_image()
        self.mu = mu = Uc(UC_ARCH_X86, UC_MODE_16)
        mu.mem_map(0, 0x100000)
        mu.mem_write(TSR * 16, image)
        at = image.find(bytes.fromhex("26234712"))
        self.assertGreater(at, 0)
        mu.mem_write(VEC_CAN_USE * 4, struct.pack("<HH", at, TSR))
        mu.hook_add(UC_HOOK_INTR, real_mode_interrupt)
        mu.mem_write(GAME_DS * 16 + 0x1669, struct.pack("<HH", 0, self.TYPES_SEG))
        for t in test_restrict.TYPES:
            mu.mem_write(self.TYPES_SEG * 16 + t * 0x14, test_restrict.record(t))
        mu.mem_write(CALLER * 16 + 0x600, bytes((0xCD, VEC_CAN_USE, 0x90, 0x90)))

    def can_use(self, sheet, t, rules=8192):
        mu = self.mu
        mu.mem_write(TSR * 16 + load_image().find(HDR_SIG) + self.RULES, struct.pack("<H", rules))
        mu.mem_write(self.SHEET * 16 + 0x100, sheet)
        for name, value in dict(cs=CALLER, ds=GAME_DS, ss=SS, esp=0x7FC, ebp=BP, eflags=IF | 2, eax=test_restrict.TYPES[t][3],
                                ebx=0x100, ecx=0x3333, edx=t, esi=0x5555, edi=0x7777, es=self.SHEET).items():
            mu.reg_write(getattr(r, "UC_X86_REG_" + name.upper()), value)
        mu.emu_start(CALLER * 16 + 0x600, CALLER * 16 + 0x604)
        self.assertEqual([mu.reg_read(getattr(r, "UC_X86_REG_" + x)) for x in ("SP", "BX", "CX", "DX", "SI", "DI", "ES", "DS")],
                         [0x7FC, 0x100, 0x3333, t, 0x5555, 0x7777, self.SHEET, GAME_DS])
        return mu.reg_read(r.UC_X86_REG_AX)

    def test_dual_class(self):
        """A fighter turned psionicist (or cleric): its long sword back once the new level passes."""
        for new in (12, 3):
            for first in (3, 4, 5, 6):
                s = bytearray(test_restrict.sheet(new, 9, race=game.HUMAN))
                s[0x14] = 1
                s[0x24:0x26] = bytes((first, 5))
                for t in (45, 81, 22, 17):
                    with self.subTest(new=new, level=first, type=t):
                        mask = test_restrict.TYPES[t][3] & int.from_bytes(s[0x12:0x14], "little")
                        expected = mask if mask and restrict.allowed(bytes(s), t, test_restrict.record(t)) else 0
                        self.assertEqual(self.can_use(bytes(s), t), expected)

    def test_off_as_the_game(self):
        psi = test_restrict.sheet(12)
        self.assertEqual(self.can_use(psi, 57, rules=0), 0x100 & 0x126F)
        self.assertEqual(self.can_use(test_restrict.sheet(11), 57, rules=0), 0)

    def test_every_pairing(self):
        sheet, classes = test_restrict.sheet, range(18)
        for race in (game.HUMAN, 2):
            for a in range(1, 18):
                for b in classes:
                    s = sheet(a, b, race=race) if b else sheet(a, race=race)
                    for t in test_restrict.TYPES:
                        with self.subTest(race=race, classes=(a, b), type=t):
                            mask = test_restrict.TYPES[t][3] & int.from_bytes(s[0x12:0x14], "little")
                            expected = mask if mask and restrict.allowed(s, t, test_restrict.record(t)) else 0
                            self.assertEqual(self.can_use(s, t), expected)



@unittest.skipIf(Uc is None, "unicorn is not installed")
class NoCastTests(unittest.TestCase):
    """PROBE_NO_CAST: a multiclass preserver in armour can't cast (restrict.no_spells)."""
    SHEETS, CREATURES, ITEMS, TYPES_SEG = 0x8000, 0x8400, 0x8800, 0x9000
    THINGS_SEG = GAME_DS + 0x3972 - 0x4356
    RULES = 170
    WHO = 1

    def setUp(self):
        image = load_image()
        self.mu = mu = Uc(UC_ARCH_X86, UC_MODE_16)
        mu.mem_map(0, 0x100000)
        mu.mem_write(TSR * 16, image)
        at = image.find(bytes.fromhex("5589e5508b460689460a"), image.find(bytes.fromhex("26234712")))
        self.assertGreater(at, 0)
        mu.mem_write(VEC_NO_CAST * 4, struct.pack("<HH", at, TSR))
        mu.hook_add(UC_HOOK_INTR, real_mode_interrupt)
        for ptr, seg in ((0x1661, self.SHEETS), (0x1665, self.CREATURES), (0x165D, self.ITEMS), (0x1669, self.TYPES_SEG)):
            mu.mem_write(GAME_DS * 16 + ptr, struct.pack("<HH", 0, seg))
        for t in test_restrict.TYPES:
            mu.mem_write(self.TYPES_SEG * 16 + t * 0x14, test_restrict.record(t))
        mu.mem_write(CALLER * 16 + 0x600, bytes((0xCD, VEC_NO_CAST, 0x90)))

    def no_cast(self, sheet, worn, ax=0, rules=8192):
        """AX after the probe, the character wearing (type, slot) pairs: list +8 one thing, the
        items chained, and list +0Ah empty."""
        mu = self.mu
        mu.mem_write(TSR * 16 + load_image().find(HDR_SIG) + self.RULES, struct.pack("<H", rules))
        mu.mem_write(self.SHEETS * 16 + self.WHO * 0x47, sheet)
        rec = bytearray(0x3A)
        rec[8:14] = struct.pack("<HHH", 4 if worn else 0x270F, 0x270F, 0x270F)
        mu.mem_write(self.CREATURES * 16 + self.WHO * 0x3A, bytes(rec))
        mu.mem_write(self.THINGS_SEG * 16 + 0xC36 + 4 * 3, struct.pack("<Bh", 1, 10))
        for n, (t, slot) in enumerate(worn):
            item = bytearray(0x15)
            item[4:6] = struct.pack("<H", 10 + n + 1 if n + 1 < len(worn) else 0x270F)
            item[0x0A:0x0C] = struct.pack("<H", t)
            item[0x11] = slot
            mu.mem_write(self.ITEMS * 16 + (10 + n) * 0x15, bytes(item))
        mu.mem_write(SS * 16 + 0x7F8, struct.pack("<HH", self.WHO, 0))
        for name, value in dict(cs=CALLER, ds=GAME_DS, ss=SS, esp=0x7F8, ebp=BP, eflags=IF | 2, eax=ax,
                                ebx=0x2222, ecx=0x3333, edx=self.WHO, esi=0x5555, edi=0x7777, es=0x6666).items():
            mu.reg_write(getattr(r, "UC_X86_REG_" + name.upper()), value)
        mu.emu_start(CALLER * 16 + 0x600, CALLER * 16 + 0x603)
        self.assertEqual([mu.reg_read(getattr(r, "UC_X86_REG_" + x)) for x in ("SP", "BP", "BX", "CX", "DX", "SI", "DI", "ES", "DS")],
                         [0x7FC, BP, 0x2222, 0x3333, self.WHO, 0x5555, 0x7777, 0x6666, GAME_DS])
        return mu.reg_read(r.UC_X86_REG_AX)

    def test_preserver_in_armour(self):
        sheet = test_restrict.sheet
        chest, head, hand, cloak = 9, 7, 3, 12
        self.assertEqual(self.no_cast(sheet(9, 11), [(65, cloak), (5, head)]), 1)
        self.assertEqual(self.no_cast(sheet(11, 17), [(6, chest)]), 1)
        self.assertEqual(self.no_cast(sheet(9, 11), [(4, hand), (65, cloak)]), 0)  # a shield
        self.assertEqual(self.no_cast(sheet(9, 11), [(6, 20)]), 0)  # (carried, not worn)
        self.assertEqual(self.no_cast(sheet(9, 11), []), 0)
        self.assertEqual(self.no_cast(sheet(11), [(6, chest)]), 0)
        self.assertEqual(self.no_cast(sheet(11, 9, race=game.HUMAN), [(6, chest)]), 0)
        self.assertEqual(self.no_cast(sheet(9, 11), [(6, chest)], rules=0), 0)
        self.assertEqual(self.no_cast(sheet(9, 17), [(6, chest)], ax=1), 1)  # (the game's own reasons)



@unittest.skipIf(Uc is None, "unicorn is not installed")
class MultiHpTests(unittest.TestCase):
    """PROBE_MC_ROLL, PROBE_MC_CON, PROBE_MC_UNCON against game.multiclass_gain and con_share."""
    SHEETS = 0x8000
    RULES = 170

    def setUp(self):
        image = load_image()
        self.mu = mu = Uc(UC_ARCH_X86, UC_MODE_16)
        mu.mem_map(0, 0x100000)
        mu.mem_write(TSR * 16, image)
        add = image.find(bytes.fromhex("26014f0acf"))  # PROBE_MC_ROLL's last two instructions
        self.assertGreater(add, 0)
        start = image.rfind(bytes.fromhex("2ef706"), 0, add)  # its rule test, its first instruction
        con = image.find(bytes.fromhex("01c7cf"), add)  # PROBE_MC_CON: call con_share, add di,ax, iret
        uncon = image.find(bytes.fromhex("29c2cf"), add)
        self.assertGreater(con, 0)
        self.assertGreater(uncon, 0)
        mu.mem_write(VEC_MC_ROLL * 4, struct.pack("<HH", start, TSR))
        mu.mem_write(VEC_MC_CON * 4, struct.pack("<HH", con - 3, TSR))
        mu.mem_write(VEC_MC_UNCON * 4, struct.pack("<HH", uncon - 3, TSR))
        mu.hook_add(UC_HOOK_INTR, real_mode_interrupt)
        mu.mem_write(GAME_DS * 16 + 0x1661, struct.pack("<HH", 0, self.SHEETS))

    def run_probe(self, vector, sheet, rules, **regs):
        mu = self.mu
        mu.mem_write(TSR * 16 + load_image().find(HDR_SIG) + self.RULES, struct.pack("<H", rules))
        mu.mem_write(self.SHEETS * 16 + 2 * 0x47, sheet)
        mu.mem_write(CALLER * 16 + 0x600, bytes((0xCD, vector)))
        values = dict(cs=CALLER, ds=GAME_DS, ss=SS, esp=0x7FC, ebp=BP, eflags=IF | 2, eax=0x1111, ebx=2 * 0x47,
                      ecx=0x3333, edx=0x4444, esi=2, edi=0x7777, es=self.SHEETS)
        values.update(regs)
        for name, value in values.items():
            mu.reg_write(getattr(r, "UC_X86_REG_" + name.upper()), value)
        mu.emu_start(CALLER * 16 + 0x600, CALLER * 16 + 0x602)
        return {x: mu.reg_read(getattr(r, "UC_X86_REG_" + x.upper())) for x in ("sp", "ax", "bx", "cx", "dx", "si", "di", "es")}

    def sheets(self):
        sheet = test_restrict.sheet
        return [sheet(9), sheet(9, 11), sheet(9, 11, 17), sheet(11, 9, race=game.HUMAN)]

    def test_roll(self):
        for s in self.sheets():
            for gain in range(0, 21):
                for rules in (0, 16384):
                    with self.subTest(sheet=s[0x21:0x24], gain=gain, rules=rules):
                        self.mu.mem_write(self.SHEETS * 16 + 2 * 0x47 + 0x0A, struct.pack("<H", 0))
                        out = self.run_probe(VEC_MC_ROLL, s[:0x0A] + struct.pack("<H", 100) + s[0x0C:], rules, ecx=gain)
                        base, = struct.unpack("<H", self.mu.mem_read(self.SHEETS * 16 + 2 * 0x47 + 0x0A, 2))
                        added = game.multiclass_gain(s, gain) if rules else gain
                        self.assertEqual(base, 100 + added)
                        self.assertEqual((out["sp"], out["ax"], out["dx"], out["si"], out["di"]), (0x7FC, 0x1111, 0x4444, 2, 0x7777))

    def test_con(self):
        for s in self.sheets():
            for bonus in range(-3, 13):
                for rules in (0, 16384):
                    with self.subTest(sheet=s[0x21:0x24], bonus=bonus, rules=rules):
                        share = game.con_share(s, bonus) if rules else bonus
                        out = self.run_probe(VEC_MC_CON, s, rules, eax=bonus & 0xFFFF, edi=50)
                        self.assertEqual(out["di"], 50 + share)
                        self.assertEqual((out["sp"], out["bx"], out["cx"], out["dx"], out["si"], out["es"]),
                                         (0x7FC, 2 * 0x47, 0x3333, 0x4444, 2, self.SHEETS))
                        out = self.run_probe(VEC_MC_UNCON, s, rules, eax=bonus & 0xFFFF, edx=50)
                        self.assertEqual(out["dx"], (50 - share) & 0xFFFF)


@unittest.skipIf(Uc is None, "unicorn is not installed")
class KindsAllowedTests(unittest.TestCase):
    """DSCLOG's KINDS_ALLOWED against restrict.allowed_kinds, on the game's weapon types (their
    flags, material and classes, as DSUN's IT1R has them): a kind open if any of its types is
    usable, so a fire or earth cleric's long sword (obsidian or metal) and mace (obsidian)."""
    # type: (flags, material byte, classes)
    WEAPONS = {45: (1, 3, 0x167E), 63: (1, 4, 0x1672), 81: (1, 1, 0x1678), 47: (1, 4, 0x1672),
               41: (1, 1, 0x1672), 50: (1, 1, 0x1772), 85: (1, 3, 0x1676), 97: (1, 1, 0x1FF2),
               98: (1, 3, 0x1776), 17: (1, 3, 0x1FF6), 33: (1, 2, 0x1FF2), 84: (0x11, 4, 0x1FF2),
               94: (1, 3, 0x1FF2), 20: (1, 1, 0x167A), 46: (1, 3, 0x167E), 18: (1, 0, 0x177A),
               22: (1, 4, 0x177A), 2: (1, 0x40, 0x166C), 112: (1, 2, 0x177A), 3: (1, 0, 0x1EFA),
               80: (1, 0, 0x1EFA), 19: (1, 1, 0x167A), 111: (1, 1, 0x167A), 44: (1, 1, 0x177B),
               21: (1, 1, 0x167B), 48: (0x12, 3, 0x1F77), 1: (0x0A, 0, 0x177B), 69: (0x0A, 0, 0x177B),
               64: (2, 5, 0x1EF9), 0: (2, 5, 0x1EF1), game.SHORT_SWORD_TYPE: (1, 4, 0x1672),
               game.BONE_SHORT_SWORD_TYPE: (1, 1, 0x1778), game.BONE_AXE_TYPE: (1, 1, 0x1778),
               game.OBSIDIAN_SHORT_SWORD_TYPE: (1, 3, 0x177E), game.OBSIDIAN_AXE_TYPE: (1, 3, 0x177E)}
    TYPES = 0x8000  # (segment)

    def record(self, t):
        rec = bytearray(game.ITEM_TYPE_SIZE)
        if t in self.WEAPONS:
            flags, material, classes = self.WEAPONS[t]
            rec[0], rec[8] = flags, material
            rec[0x10:0x12] = classes.to_bytes(2, "little")
        return bytes(rec)

    def test_as_the_python(self):
        image = load_image()
        start = image.find(bytes.fromhex("5152565731d231ff89d62e8a8c"))
        self.assertGreater(start, 0)
        mu = Uc(UC_ARCH_X86, UC_MODE_16)
        mu.mem_map(0, 0x100000)
        mu.mem_write(TSR * 16, image)
        mu.mem_write(TSR * 16 + 0xFFF0, bytes((0xF4,)))  # (hlt: where KINDS_ALLOWED returns)
        mu.mem_write(GAME_DS * 16 + 0x1669, struct.pack("<HH", 0, self.TYPES))
        mu.mem_write(self.TYPES * 16, b"".join(self.record(t) for t in range(128)))
        sheet = test_restrict.sheet
        combos = [(9,), (13,), (10,), (11,), (12,), (17,), (9, 12), (9, 17), (9, 11), (13, 5), (13, 12)]
        for c in range(1, 5):
            combos += [(c,), (9, c), (12 + c, c)]
        for classes in combos:
            s = sheet(*classes)
            with self.subTest(classes=classes):
                mu.mem_write(SS * 16 + 0x500, s)
                mu.mem_write(SS * 16 + 0x7FC, struct.pack("<H", 0xFFF0))
                for name, value in dict(cs=TSR, ds=GAME_DS, es=SS, ebx=0x500, ss=SS, esp=0x7FC).items():
                    mu.reg_write(getattr(r, "UC_X86_REG_" + name.upper()), value)
                mu.emu_start(TSR * 16 + start, TSR * 16 + 0xFFF0)
                got = mu.reg_read(r.UC_X86_REG_AX)
                want = restrict.allowed_kinds(s, self.record)
                self.assertEqual([k for k in range(16) if got >> k & 1], want)
        fire = restrict.allowed_kinds(sheet(9, 3), self.record)
        self.assertEqual([specialize.KINDS[k] for k in fire],
                         ["long sword", "dagger", "short sword", "mace", "axe", "chatkcha"])


@unittest.skipIf(Uc is None, "unicorn is not installed")
class XpNextTests(unittest.TestCase):
    """View Character's next-level XP (PROBE_XP_NEXT): for more than one class, the class (or
    classes) whose next level it is before the ")", by the game's own XP tables; for one, the
    game's ")" as before, and for a human (who dual-classes: the game counts the first class
    only). (The screen's copy of the sheet numbers classes 1-8: 3 fighter, 5 preserver, 6
    psionicist, 8 thief; its +18h is the race, 1 human, 3 elf.)"""
    SHEET, TABLE = 0x8000, 0x9000
    RULES = 170

    def setUp(self):
        image = load_image()
        self.mu = mu = Uc(UC_ARCH_X86, UC_MODE_16)
        mu.mem_map(0, 0x100000)
        mu.mem_write(TSR * 16, image)
        at = image.find(bytes.fromhex("50535152565706" "0fa8"))
        self.assertGreater(at, 18)
        mu.mem_write(VEC_XP_NEXT * 4, struct.pack("<HH", at - 15, TSR))  # (past the three pops)
        mu.hook_add(UC_HOOK_INTR, real_mode_interrupt)
        mu.mem_write(CALLER * 16 + 0x602 - 0x8B, bytes((0xB8,)) + struct.pack("<H", self.TABLE))  # mov ax,seg
        mu.mem_write(SS * 16 + BP + 0x0A, struct.pack("<HH", 0, self.SHEET))
        for cls, level, xp in ((3, 4, 16000), (5, 4, 20000), (8, 5, 20000), (6, 4, 20000), (3, 9, 0), (3, 10, 0)):
            mu.mem_write(self.TABLE * 16 + cls * 40 + level * 2 + 0x27C, struct.pack("<H", xp // 100))

    def run_with(self, classes, levels, least, rules=0, race=3):
        mu = self.mu
        mu.mem_write(TSR * 16 + load_image().find(HDR_SIG) + self.RULES, struct.pack("<H", rules))
        sheet = bytearray(0x30)
        sheet[0x18] = race
        sheet[0x21:0x24], sheet[0x24:0x27] = bytes(classes), bytes(levels)
        mu.mem_write(self.SHEET * 16, bytes(sheet))
        mu.mem_write(SS * 16 + BP - 6, struct.pack("<I", least))
        mu.mem_write(SS * 16 + 0x7FC, struct.pack("<HH", GAME_DS, 0x50))  # pushed: DS, the length
        mu.mem_write(CALLER * 16 + 0x600, bytes((0xCD, VEC_XP_NEXT, 0x90)))
        for name, value in dict(cs=CALLER, ds=GAME_DS, ss=SS, esp=0x7FC, ebp=BP, eflags=IF | 2, eax=0x1111,
                                ebx=0x2222, ecx=0x3333, edx=0x4444, esi=0x5555, edi=0x6666, es=0x7777).items():
            mu.reg_write(getattr(r, "UC_X86_REG_" + name.upper()), value)
        mu.emu_start(CALLER * 16 + 0x600, CALLER * 16 + 0x603)
        self.assertEqual([mu.reg_read(x) for x in (r.UC_X86_REG_SP, r.UC_X86_REG_AX, r.UC_X86_REG_BX, r.UC_X86_REG_CX,
                                                   r.UC_X86_REG_DX, r.UC_X86_REG_SI, r.UC_X86_REG_DI, r.UC_X86_REG_BP,
                                                   r.UC_X86_REG_DS, r.UC_X86_REG_ES)],
                         [0x7FA, 0x1111, 0x2222, 0x3333, 0x4444, 0x5555, 0x6666, BP, GAME_DS, 0x7777])
        off, seg, length = struct.unpack("<HHH", mu.mem_read(SS * 16 + 0x7FA, 6))
        self.assertEqual(length, 0x50)
        if seg == GAME_DS:
            return off
        return bytes(mu.mem_read(seg * 16 + off, 12)).split(b"\0")[0].decode()

    def test_one_class_due(self):
        self.assertEqual(self.run_with((3, 5, 8), (4, 4, 5), 16000), " F)")  # (Xan)

    def test_two_due_at_once(self):
        self.assertEqual(self.run_with((3, 5, 8), (5, 4, 5), 20000), " Pr/T)")

    def test_preserver_and_psionicist(self):
        self.assertEqual(self.run_with((5, 6, 0), (4, 4, 0), 20000), " Pr/Ps)")

    def test_one_class_as_the_game(self):
        """An elf fighter: one class, nothing to tell apart."""
        self.assertEqual(self.run_with((3, 0, 0), (4, 0, 0), 16000), 0x10F4)

    def test_human_as_the_game(self):
        """A dual-classed human: the game's own line, whatever the slots hold."""
        self.assertEqual(self.run_with((3, 8, 0), (4, 5, 0), 16000, race=1), 0x10F4)

    def test_at_the_cap(self):
        """A class at the level cap (9, or 10 with that rule) has no next level, so isn't named."""
        self.assertEqual(self.run_with((3, 5, 0), (9, 4, 0), 20000), " Pr)")
        self.assertEqual(self.run_with((3, 5, 0), (10, 4, 0), 20000, rules=128), " Pr)")


@unittest.skipIf(Uc is None, "unicorn is not installed")
class ItemSaveTests(unittest.TestCase):
    """The acid's and corroding touch's item checks (PROBE_ITEM_*): the number a d20 needs, the
    game's or (RULE_ITEM_SAVES) the easier of it and AD&D's, and each check recorded."""
    ITEMS, TYPES = 0xA000, 0xB000
    RULES = 170
    # item: (type, material, plus, power)
    GEAR = {4: (6, 5, 0, 0), 5: (57, 4, 0, 0), 6: (79, 5, 1, 89), 7: (81, 1, 0, 0), 8: (63, 4, 1, 0),
            9: (17, 3, 0, 0), 10: (90, 0x40, 2, 0)}

    def setUp(self):
        image = load_image()
        self.mu = mu = Uc(UC_ARCH_X86, UC_MODE_16)
        mu.mem_map(0, 0x100000)
        mu.mem_write(TSR * 16, image)
        self.hdr_off = struct.unpack_from("<H", image, 20)[0]
        self.ring = struct.unpack_from("<H", image, 16)[0]
        for vec, head in ((VEC_ITEM_WEAPON, "5650535157ba08002b56fe"), (VEC_ITEM_ARMOUR, "5650535157ba0a002b56fe"),
                          (VEC_ITEM_SKIP, "5589e5836606bf")):
            at = image.find(bytes.fromhex(head))
            self.assertGreater(at, 0, head)
            mu.mem_write(vec * 4, struct.pack("<HH", at, TSR))
        mu.hook_add(UC_HOOK_INTR, real_mode_interrupt)
        mu.mem_write(GAME_DS * 16 + 0x165D, struct.pack("<HH", 0, self.ITEMS))
        mu.mem_write(GAME_DS * 16 + 0x1669, struct.pack("<HH", 0, self.TYPES))
        for item, (typ, material, plus, power) in self.GEAR.items():
            rec = bytearray(21)
            struct.pack_into("<H", rec, 0x0A, typ)
            rec[0x0F], rec[0x14] = power & 0xFF, plus & 0xFF
            mu.mem_write(self.ITEMS * 16 + item * 21, bytes(rec))
            mu.mem_write(self.TYPES * 16 + typ * 0x14 + 8, bytes([material]))
        # the routine's frame: the saved BP (its caller's, the special attack's: 187 on target 3
        # from 44), its argument (the target); the list's entry 2 holds the item
        mu.mem_write(SS * 16 + BP, struct.pack("<HHHH", PARENT_BP, 0, 0, 3))
        mu.mem_write(SS * 16 + PARENT_BP, struct.pack("<HHHHHHHH", 0, 0, 0, 3, 44, 0, 0, 187))
        self.at = 0x600

    def rules(self, value):
        self.mu.mem_write(TSR * 16 + load_image().find(HDR_SIG) + self.RULES, struct.pack("<H", value))

    def run_int(self, vec, item, word, roll, armour):
        """INT VEC with the list's entry 2 the item, [BP-2] WORD (the plus or the power), AX the
        d20: DX, ZF and the entry recorded (None if none)."""
        mu = self.mu
        list_at = BP - (0x31E if armour else 0x320) + 2 * 0x0A
        mu.mem_write(SS * 16 + list_at, struct.pack("<H", item))
        mu.mem_write(SS * 16 + BP - 2, struct.pack("<h", word))
        seq_at = TSR * 16 + self.hdr_off + 8
        before = struct.unpack("<H", mu.mem_read(seq_at, 2))[0]
        self.at += 0x20
        mu.mem_write(CALLER * 16 + self.at, bytes((0xCD, vec)))
        for name, value in dict(cs=CALLER, ds=GAME_DS, ss=SS, esp=0x800, ebp=BP, eflags=IF | 2, eax=roll,
                                esi=2, ebx=0x2222, ecx=0x3333, edx=0x4444, edi=0x5555, es=0x6666).items():
            mu.reg_write(getattr(r, "UC_X86_REG_" + name.upper()), value)
        mu.emu_start(CALLER * 16 + self.at, CALLER * 16 + self.at + 2)
        self.assertEqual([mu.reg_read(x) for x in (r.UC_X86_REG_SP, r.UC_X86_REG_AX, r.UC_X86_REG_BX,
                                                   r.UC_X86_REG_CX, r.UC_X86_REG_SI, r.UC_X86_REG_DI,
                                                   r.UC_X86_REG_BP, r.UC_X86_REG_DS, r.UC_X86_REG_ES)],
                         [0x800, roll, 0x2222, 0x3333, 2, 0x5555, BP, GAME_DS, 0x6666])
        seq, widx, nent = struct.unpack("<HHH", mu.mem_read(seq_at, 6))
        entry = None
        if seq != before:
            entry = Entry.parse(bytes(mu.mem_read(TSR * 16 + self.ring + ((seq - 1) % nent) * Entry.SIZE,
                                                  Entry.SIZE)))
        dx = struct.unpack("<h", struct.pack("<H", mu.reg_read(r.UC_X86_REG_DX)))[0]
        return dx, bool(mu.reg_read(r.UC_X86_REG_EFLAGS) & 0x40), entry

    def weapon(self, item, roll=10):
        return self.run_int(VEC_ITEM_WEAPON, item, self.GEAR[item][2], roll, False)

    def armour(self, item, roll=10):
        return self.run_int(VEC_ITEM_ARMOUR, item, self.GEAR[item][3], roll, True)

    def test_weapons_the_games(self):
        self.rules(0)
        for item, want in ((7, 8), (8, 7), (9, 8)):
            dx, _, e = self.weapon(item, 12)
            self.assertEqual(dx, want, item)
            self.assertEqual((e.kind, e.raw, e.extra, e.arg(6), e.parent_arg(0x0E)), (4, 12 | want << 8, item, 3, 187))

    def test_weapons_the_easier(self):
        """Bone (11) and metal +1 (12) keep the game's 8 and 7; obsidian gets AD&D's 5."""
        self.rules(2048)
        self.assertEqual([self.weapon(item)[0] for item in (7, 8, 9)], [8, 7, 5])

    def test_armour_the_games(self):
        """No magical power: destroyed without a roll (ZF set, recorded with no d20); with one,
        10 less it (Drake Armor's 89: never)."""
        self.rules(0)
        for item in (4, 5, 10):
            dx, zf, e = self.run_int(VEC_ITEM_SKIP, item, 0, 0x1234, True)
            self.assertTrue(zf, item)
            self.assertEqual((e.kind, e.raw & 0xFF, e.extra), (4, 0, 0x8000 | item))
        dx, zf, e = self.run_int(VEC_ITEM_SKIP, 6, 89, 0x1234, True)
        self.assertEqual((zf, e), (False, None))
        self.assertEqual(self.armour(6)[0], 10 - 89)

    def test_armour_the_easier(self):
        """Leather 10, metal 13, cloth +2 10; Drake Armor keeps the game's (never)."""
        self.rules(2048)
        for item in (4, 5, 6, 10):
            dx, zf, e = self.run_int(VEC_ITEM_SKIP, item, self.GEAR[item][3], 0x1234, True)
            self.assertEqual((zf, e), (False, None), item)
        self.assertEqual([self.armour(item)[0] for item in (4, 5, 6, 10)], [10, 13, 10 - 89, 10])
        dx, _, e = self.armour(5, 14)
        self.assertEqual((e.raw, e.extra), (14 | 13 << 8, 0x8000 | 5))


@unittest.skipIf(Uc is None, "unicorn not installed")
class RuleTests(RingTests):
    """The companion's rule changes: two weapons' to-hit, and the doubled save d20."""
    RULES = 170  # the header's RULES word

    def setUp(self):
        super().setUp()
        image = load_image()
        two = image.find(bytes.fromhex("2ef606") + struct.pack("<H", self.RULES) + bytes([4]))
        double = image.find(bytes.fromhex("2ef606") + struct.pack("<H", self.RULES) + bytes([16]))
        self.assertGreater(min(two, double), 0)
        self.mu.mem_write(VEC_TWO * 4, struct.pack("<HH", two, TSR))
        self.mu.mem_write(VEC_DOUBLE * 4, struct.pack("<HH", double, TSR))

    def rules(self, value):
        self.mu.mem_write(TSR * 16 + self.RULES, struct.pack("<H", value))

    def two(self, dex_adjust, item):
        """INT VEC_TWO with AX the DEX's initiative adjustment, [BP+0Ah] the attack's item and
        CX the attacker's object (3: creature 1): the adjustment in DX."""
        self.mu.mem_write(SS * 16 + BP + 0x0A, struct.pack("<H", item))
        self.run_at(bytes((0xCD, VEC_TWO)), eax=dex_adjust & 0xFFFF, ebx=0x2222, ecx=3, es=0x6666)
        self.assertEqual([self.mu.reg_read(x) for x in (r.UC_X86_REG_BX, r.UC_X86_REG_CX, r.UC_X86_REG_ES)],
                         [0x2222, 3, 0x6666])
        return struct.unpack("<h", struct.pack("<H", self.mu.reg_read(r.UC_X86_REG_DX)))[0]

    def hands(self, right=(81, 3), left=(81, 10)):
        """Creature 1's items 4 and 7 as (type, slot); type 81 is a melee weapon (class 1),
        type 90 a shield (class 0)."""
        self.mu.mem_write(GAME_DS * 16 + 0x1669, struct.pack("<HH", 0, self.TYPES))
        things = (GAME_DS + 0x3972 - 0x4356) * 16 + 0xC36  # where the game keeps them, from DS
        for thing, kind, index in ((3, 2, 1), (10, 1, 4), (11, 1, 7), (12, 1, 5)):
            self.mu.mem_write(things + thing * 3, struct.pack("<BH", kind, index))
        for typ, cls in ((81, 1), (90, 0), (60, 2)):
            self.mu.mem_write(self.TYPES * 16 + typ * 0x14 + 0x0A, bytes([cls]))
        for item, (typ, slot) in ((4, right), (7, left)):
            rec = bytearray(self.mu.mem_read(self.ITEMS * 16 + item * 21, 21))
            struct.pack_into("<H", rec, 0x0A, typ)
            rec[0x11] = slot
            self.mu.mem_write(self.ITEMS * 16 + item * 21, bytes(rec))

    def test_two_weapons_the_games(self):
        self.rules(0)
        self.hands()
        self.assertEqual([self.two(adj, 4) for adj in (-6, -1, 0, 3)], [6, 1, 0, 0])

    def test_two_weapons_adnd(self):
        """A weapon in each hand: item 4 in the right (main), item 7 in the left (off)."""
        self.rules(4)
        self.hands()
        self.assertEqual([self.two(adj, 4) for adj in (-3, 0, 1, 2, 5)], [-5, -2, -1, 0, 0])
        self.assertEqual([self.two(adj, 7) for adj in (-3, 0, 2, 3, 4, 5)], [-7, -4, -2, -1, 0, 0])

    def test_one_weapon_no_penalty(self):
        """A shield in the other hand, a bow in the missile slot, or the weapon not in a hand:
        no penalty, whatever the DEX."""
        self.rules(4)
        for right, left in (((81, 3), (90, 10)), ((81, 3), (60, 2)), ((81, 3), (81, 0xFF)), ((81, 2), (81, 10))):
            self.hands(right, left)
            self.assertEqual([self.two(adj, 4) for adj in (-3, 0)], [0, 0], (right, left))

    def test_doubled_save(self):
        for rules, want in ((0, 14), (16, 7)):
            self.rules(rules)
            self.run_at(bytes((0xCD, VEC_DOUBLE)), eax=7)
            self.assertEqual(self.mu.reg_read(r.UC_X86_REG_AL), want)

    def level(self, level):
        """INT VEC_LEVEL with ES:BX a sheet whose class level (+24h) is LEVEL: (below the cap,
        at it), from the flags the game's JL and JZ read; AX and interrupts as they were."""
        image = load_image()
        probe = image.find(bytes.fromhex("fb50b0092ef606") + struct.pack("<H", self.RULES) + bytes([128]))
        self.assertGreater(probe, 0)
        self.mu.mem_write(VEC_LEVEL * 4, struct.pack("<HH", probe, TSR))
        self.mu.mem_write(self.TYPES * 16 + 0x100 + 0x24, bytes([level]))
        self.run_at(bytes((0xCD, VEC_LEVEL)), es=self.TYPES, ebx=0x100, eax=0x1234)
        flags = self.mu.reg_read(r.UC_X86_REG_EFLAGS)
        self.assertEqual((self.mu.reg_read(r.UC_X86_REG_AX), bool(flags & IF)), (0x1234, True))
        return bool(flags & 0x80) != bool(flags & 0x800), bool(flags & 0x40)

    def test_level_cap(self):
        """The game's cap of 9, or 10 with rule 128."""
        self.rules(0)
        self.assertEqual([self.level(n) for n in (1, 8, 9, 10)],
                         [(True, False), (True, False), (False, True), (False, False)])
        self.rules(128)
        self.assertEqual([self.level(n) for n in (8, 9, 10, 11)],
                         [(True, False), (True, False), (False, True), (False, False)])

    def hit_dice(self, cls, levels=9):
        """INT VEC_HD_ROLL with ES:BX a hit point group whose dice go up to LEVELS and the
        game's [BP+8] the class: the levels that roll dice, in AL."""
        image = load_image()
        probe = image.find(bytes.fromhex("268a4701") + bytes.fromhex("2ef606") + struct.pack("<H", self.RULES))
        self.assertGreater(probe, 0)
        self.mu.mem_write(VEC_HD_ROLL * 4, struct.pack("<HH", probe, TSR))
        self.mu.mem_write(self.TYPES * 16 + 0x200, bytes([6, levels, 2, 6]))
        self.mu.mem_write(SS * 16 + BP + 8, struct.pack("<H", cls))
        self.run_at(bytes((0xCD, VEC_HD_ROLL)), es=self.TYPES, ebx=0x200, eax=0x1200)
        self.assertEqual(self.mu.reg_read(r.UC_X86_REG_AH), 0x12)
        return self.mu.reg_read(r.UC_X86_REG_AL)

    def test_thief_hit_dice(self):
        """A thief (17) rolls up to 10th with rule 128; a psionicist (12) still stops at 9th."""
        self.rules(0)
        self.assertEqual([self.hit_dice(c) for c in (17, 12)], [9, 9])
        self.rules(128)
        self.assertEqual([self.hit_dice(c) for c in (17, 12)], [10, 9])
        self.assertEqual(self.hit_dice(17, levels=10), 10)  # (a preserver's group: as it was)

    def thief_skill(self, skill, level, dex, base_race):
        """INT VEC_THIEF_SKILL with DX the skill's base + race adjustment (the game's bases at
        ES:0), SI the thief level, the game's [BP+8] the skill and [BP-0Ch] DEX: (SI, CF), with
        DX and ES as they were."""
        image = load_image()
        probe = image.find(bytes.fromhex("fb2ef706") + struct.pack("<HH", self.RULES, 256))
        self.assertGreater(probe, 0)
        self.mu.mem_write(VEC_THIEF_SKILL * 4, struct.pack("<HH", probe, TSR))
        self.mu.mem_write(self.TYPES * 16, bytes([28, 18, 13, 28, 18, 23, 78, 252]))  # the game's bases
        self.mu.mem_write(SS * 16 + BP + 8, struct.pack("<I", skill))
        self.mu.mem_write(SS * 16 + BP - 0x0C, struct.pack("<H", dex))
        self.run_at(bytes((0xCD, VEC_THIEF_SKILL)), es=self.TYPES, esi=level, edx=base_race, eax=0x1234, ebx=0x5678)
        regs = [self.mu.reg_read(x) for x in (r.UC_X86_REG_AX, r.UC_X86_REG_BX, r.UC_X86_REG_ES, r.UC_X86_REG_BP)]
        self.assertEqual(regs, [0x1234, 0x5678, self.TYPES, BP])
        return self.mu.reg_read(r.UC_X86_REG_SI), self.mu.reg_read(r.UC_X86_REG_EFLAGS) & 1

    def test_thief_skills(self):
        """The game's sum without rule 256 (on to its DEX formula); with it, AD&D's table, the race
        and Dark Sun's DEX adjustment (past the game's formula). Azil: 3rd level elf, DEX 22."""
        self.rules(0)
        self.assertEqual(self.thief_skill(1, 3, 22, 18 - 5), (13 + 12, 0))  # open locks
        self.rules(256)
        self.assertEqual(self.thief_skill(0, 3, 22, 28 + 5), (40 + 5 + 27, 1))  # pick pockets
        self.assertEqual(self.thief_skill(1, 3, 22, 18 - 5), (33 - 5 + 30, 1))
        self.assertEqual(self.thief_skill(3, 3, 22, 28 + 5), (27 + 5 + 30, 1))  # move silently
        self.assertEqual(self.thief_skill(4, 3, 22, 18 + 10), (20 + 10 + 22, 1))  # hide
        self.assertEqual(self.thief_skill(5, 3, 22, 23 + 5), (15 + 5, 1))  # hear noise: no DEX
        self.assertEqual(self.thief_skill(6, 3, 22, 78), (87, 1))  # climb walls
        self.assertEqual(self.thief_skill(4, 1, 9, 18), (10 - 10, 1))  # DEX 9
        self.assertEqual(self.thief_skill(3, 1, 7, 28), ((15 - 20) & 0xFFFF, 1))  # below 9: as 9 (the game clamps at 0 later)
        self.assertEqual(self.thief_skill(0, 12, 24, 28), (80 + 27, 1))  # past 10th and DEX 22
        self.assertEqual(self.thief_skill(7, 3, 22, (252 - 256) & 0xFFFF), (0, 1))  # read languages
        self.assertEqual(self.thief_skill(0, 0, 22, 28), (28, 0))  # no thief level: the game's

    def test_bone_helm_counts_as_a_helm(self):
        """Helms give AC 1 (rule 1): the companion's bone helm (type 117) as the game's (5)."""
        for typ in (5, 117):
            for rules, want in ((1, 1), (0, 0)):
                self.rules(rules)
                self.mu.mem_write(self.TYPES * 16 + 0x12, bytes([9]))
                self.run_at(bytes((0xCD, VEC_RING_AC)), es=self.TYPES, ebx=0, ecx=typ, eax=0)
                self.assertEqual(self.mu.mem_read(self.TYPES * 16 + 0x12, 1)[0], want, (typ, rules))

    def two_handed(self, race, flags=0x40):
        """INT VEC_TWO_HANDED with ES:BX an item type whose +0Fh is FLAGS, for the character on
        show (number 2, at the game's 0348h:25Bh) of RACE: ZF (the game's JE: not two-handed),
        with AX, BX and ES as they were."""
        image = load_image()
        probe = image.find(bytes.fromhex("fb2ef706") + struct.pack("<HH", self.RULES, 512))
        self.assertGreater(probe, 0)
        self.mu.mem_write(VEC_TWO_HANDED * 4, struct.pack("<HH", probe, TSR))
        who = (GAME_DS + 0x3931 - 0x4356) & 0xFFFF  # (as the running game has it: DS - 0A25h)
        self.mu.mem_write(who * 16 + 0x25B, struct.pack("<H", 2))
        sheets = self.TYPES * 16 + 0x400
        self.mu.mem_write(GAME_DS * 16 + 0x1661, struct.pack("<HH", 0x400, self.TYPES))
        self.mu.mem_write(sheets + 2 * 0x47 + 0x18, bytes([race]))
        self.mu.mem_write(self.TYPES * 16 + 0x300 + 0x0F, bytes([flags]))
        self.run_at(bytes((0xCD, VEC_TWO_HANDED)), es=self.TYPES, ebx=0x300, eax=0x1234)
        regs = [self.mu.reg_read(x) for x in (r.UC_X86_REG_AX, r.UC_X86_REG_BX, r.UC_X86_REG_ES)]
        self.assertEqual(regs, [0x1234, 0x300, self.TYPES])
        return bool(self.mu.reg_read(r.UC_X86_REG_EFLAGS) & 0x40)

    def test_half_giants_two_handed_in_one_hand(self):
        """Rule 512: a half-giant's two-handed weapon counts as one-handed; anyone else's, or
        without the rule, as the game has it; a one-handed weapon is one-handed for all."""
        self.rules(0)
        self.assertEqual([self.two_handed(r) for r in (5, 1)], [False, False])  # (ZF clear: two-handed)
        self.rules(512)
        self.assertEqual([self.two_handed(r) for r in (5, 1)], [True, False])
        self.assertEqual([self.two_handed(r, flags=0) for r in (5, 1)], [True, True])

    def spell_text(self, spin, length=112):
        """INT VEC_SPELL_TEXT after the game read SPIN chunk SPIN (LENGTH bytes) into the buffer
        at the game's [BP-8]: (the buffer's text, AX), with SP back past the read's arguments."""
        image = load_image()
        # its rule test and "cmp di,0Fh", after three pops, "add sp,0Ch" and three pushes (33 bytes)
        anchor = image.find(bytes.fromhex("2ef606") + struct.pack("<H", self.RULES) + bytes.fromhex("207425" "83ff0f"))
        self.assertGreater(anchor, 0)
        probe = anchor - 33
        self.assertEqual(image[probe:probe + 3], bytes.fromhex("2e8f06"))
        self.mu.mem_write(VEC_SPELL_TEXT * 4, struct.pack("<HH", probe, TSR))
        buf = self.TYPES * 16 + 0x500
        self.mu.mem_write(buf, b"FLAMING SPHERE:  Creates a burning globe.\r\n\0".ljust(200, b"\0"))
        self.mu.mem_write(SS * 16 + BP - 8, struct.pack("<HH", 0x500, self.TYPES))
        code = bytes.fromhex("666a00666a00666a00") + bytes((0xCD, VEC_SPELL_TEXT))  # 12 bytes of arguments
        self.at += 0x20
        self.mu.mem_write(CALLER * 16 + self.at, code)
        for name, value in dict(cs=CALLER, ds=GAME_DS, ss=SS, esp=0x800, ebp=BP, eflags=IF | 2, edi=spin, eax=length).items():
            self.mu.reg_write(getattr(r, "UC_X86_REG_" + name.upper()), value)
        self.mu.emu_start(CALLER * 16 + self.at, CALLER * 16 + self.at + len(code))
        self.assertEqual(self.mu.reg_read(r.UC_X86_REG_SP), 0x800)
        text = bytes(self.mu.mem_read(buf, 200)).split(b"\0")[0]
        return text, self.mu.reg_read(r.UC_X86_REG_AX)

    def test_cats_grace_description(self):
        """Rule 32: Flaming Sphere's description (SPIN 15) is Cat's Grace's; others, and without
        the rule, the game's."""
        grace = b"CAT'S GRACE:  Raises the target's dexterity by 1 to 6 pts. Maximum dexterity is 24.\r\n"
        self.rules(32)
        self.assertEqual(self.spell_text(15), (grace, len(grace)))
        self.assertEqual(self.spell_text(14)[0][:15], b"FLAMING SPHERE:")
        self.assertEqual(self.spell_text(15, 0xFFFF)[1], 0xFFFF)  # (no chunk read)
        self.rules(0)
        self.assertEqual(self.spell_text(15), (b"FLAMING SPHERE:  Creates a burning globe.\r\n", 112))

    def chunk_id(self, kind, number, resources_on=1, limit=0x0100):
        """INT VEC_CHUNK_ID at the start of a chunk-loading routine whose [BP+6] is KIND and
        [BP+0Ah] NUMBER, the game's stack limit (DS:9Ch) LIMIT: (the number it then loads, CF from
        the stack check)."""
        image = load_image()
        icon = image.find(bytes.fromhex("66817e06") + b"ICON")
        self.assertGreater(icon, 0)
        probe = image.rfind(bytes.fromhex("2ef606") + struct.pack("<H", self.RULES), 0, icon) - 1
        self.assertEqual(image[probe], 0xFB)  # (its STI)
        on, = struct.unpack_from("<H", image, image.find(bytes.fromhex("2e833e"), probe) + 3)
        self.mu.mem_write(TSR * 16 + on, struct.pack("<H", resources_on))
        self.mu.mem_write(VEC_CHUNK_ID * 4, struct.pack("<HH", probe, TSR))
        self.mu.mem_write(SS * 16 + BP + 6, kind + struct.pack("<I", number))
        self.mu.mem_write(GAME_DS * 16 + 0x9C, struct.pack("<H", limit))
        self.run_at(bytes((0xCD, VEC_CHUNK_ID)), eax=0x1234)
        self.assertEqual(self.mu.reg_read(r.UC_X86_REG_AX), 0x1234)
        number, = struct.unpack("<I", self.mu.mem_read(SS * 16 + BP + 0x0A, 4))
        self.assertTrue(self.mu.reg_read(r.UC_X86_REG_EFLAGS) & IF)  # (interrupts on: RETF 2 keeps flags)
        return number, self.mu.reg_read(r.UC_X86_REG_EFLAGS) & 1

    def test_cats_grace_icon(self):
        """Rule 32, with the copy of RESOURCE.GFF open: Flaming Sphere's icon (21014) is asked for as
        Cat's Grace's (21900); other icons and chunks, or without the rule or the copy, as asked.
        The stack check as the game's: CF when its limit is below SP (0x800), not when above."""
        self.rules(32)
        self.assertEqual(self.chunk_id(b"ICON", 21014), (21900, 1))
        self.assertEqual(self.chunk_id(b"ICON", 21015)[0], 21015)
        self.assertEqual(self.chunk_id(b"SPIN", 21014)[0], 21014)
        self.assertEqual(self.chunk_id(b"ICON", 21014, resources_on=0)[0], 21014)
        self.assertEqual(self.chunk_id(b"ICON", 21014, limit=0x900)[1], 0)
        self.rules(0)
        self.assertEqual(self.chunk_id(b"ICON", 21014)[0], 21014)

    def con_levels(self, cls, level):
        """INT VEC_HD_CON with AL a class's level, ES:BX its group (dice up to 9), the game's
        [BP-4] a sheet whose second class (CX = 1) is CLS: whether the level is past the cap
        (the game's JNG not taken); DX and the sheet's ES:BX as they were."""
        image = load_image()
        probe = image.find(bytes.fromhex("fb52268a5701"))
        self.assertGreater(probe, 0)
        self.mu.mem_write(VEC_HD_CON * 4, struct.pack("<HH", probe, TSR))
        self.mu.mem_write(self.TYPES * 16 + 0x200, bytes([6, 9, 2, 6]))
        self.mu.mem_write(self.CREATURES * 16 + 0x300 + 0x21, bytes([12, cls, 0]))
        self.mu.mem_write(SS * 16 + BP - 4, struct.pack("<HH", 0x300, self.CREATURES))
        self.run_at(bytes((0xCD, VEC_HD_CON)), es=self.TYPES, ebx=0x200, ecx=1, edx=0x5555, eax=level)
        mu = self.mu
        self.assertEqual([mu.reg_read(x) for x in (r.UC_X86_REG_DX, r.UC_X86_REG_ES, r.UC_X86_REG_BX)],
                         [0x5555, self.TYPES, 0x200])
        flags = mu.reg_read(r.UC_X86_REG_EFLAGS)
        return not (flags & 0x40 or bool(flags & 0x80) != bool(flags & 0x800))

    def test_thief_con_levels(self):
        self.rules(0)
        self.assertEqual([self.con_levels(17, n) for n in (9, 10)], [False, True])
        self.rules(128)
        self.assertEqual([self.con_levels(c, n) for c, n in ((17, 9), (17, 10), (12, 10))], [False, False, True])



@unittest.skipIf(Uc is None, "unicorn not installed")
class GraceTests(RuleTests):
    """Cat's Grace (spell 14, rule 32): Strength's code, its own effect (54), DEX."""

    def setUp(self):
        super().setUp()
        image = load_image()
        for vector, start in ((VEC_GRACE_CAST, "8b460e2ef606aa0020"), (VEC_GRACE_EFFECT, "c746ec4300817e0e9400"),
                              (VEC_GRACE_ABILITY, "8946f6b90700")):
            at = image.find(bytes.fromhex(start))
            self.assertGreater(at, 0)
            self.mu.mem_write(vector * 4, struct.pack("<HH", at, TSR))

    def word(self, offset, value=None):
        at = SS * 16 + (BP + offset) % 0x10000
        if value is not None:
            self.mu.mem_write(at, struct.pack("<h", value))
        return struct.unpack("<h", self.mu.mem_read(at, 2))[0]

    def test_cast_goes_to_strength(self):
        for rules, spell, want in ((32, 14, 23), (0, 14, 14), (32, 20, 20), (32, 23, 23)):
            self.rules(rules)
            self.word(0x0E, spell)
            self.run_at(bytes((0xCD, VEC_GRACE_CAST)))
            self.assertEqual((self.word(-0x1A), self.mu.reg_read(r.UC_X86_REG_AX)), (want, spell if want == spell else 23))

    def test_its_own_effect(self):
        for rules, spell, want in ((32, 14, 54), (0, 14, 0x43), (32, 23, 0x43), (32, 0x94, 0x42), (0, 0x94, 0x42)):
            self.rules(rules)
            self.word(0x0E, spell)
            self.run_at(bytes((0xCD, VEC_GRACE_EFFECT)))
            self.assertEqual(self.word(-0x14), want, (rules, spell))

    def test_adds_to_dex(self):
        effects = 0x9800
        self.mu.mem_write(effects * 16 + 0x10F, bytes([5]))
        for effect, dex, want in ((54, 15, 20), (54, 21, 24), (67, 15, 15)):
            self.word(-0x340, dex)
            self.word(-0x342, 18)  # STR, untouched
            self.run_at(bytes((0xCD, VEC_GRACE_ABILITY)), eax=effect, ebx=0, es=effects, ecx=0)
            self.assertEqual((self.word(-0x340), self.word(-0x342), self.word(-0x0A)), (want, 18, effect))
            self.assertEqual(self.mu.reg_read(r.UC_X86_REG_CX), 7)


@unittest.skipIf(Uc is None, "unicorn not installed")
class NamesTests(unittest.TestCase):
    """The game's name table: room for NAMES_EXTRA more names, and DSCLOG's copied in."""
    NAMES_SEG = 0x5000

    def setUp(self):
        self.image = image = load_image()
        self.mu = mu = Uc(UC_ARCH_X86, UC_MODE_16)
        mu.mem_map(0, 0x100000)
        mu.mem_write(TSR * 16, image)
        size = image.find(bytes.fromhex("8146fc2003" "8356fe00"))
        fill = fill_probes(image)[0]
        self.assertGreater(min(size, fill), 0)
        mu.mem_write(VEC_NAMES_SIZE * 4, struct.pack("<HH", size, TSR))
        mu.mem_write(VEC_NAMES_FILL * 4, struct.pack("<HH", fill, TSR))
        mu.hook_add(UC_HOOK_INTR, real_mode_interrupt)
        mu.mem_write(GAME_DS * 16 + 0x166D, struct.pack("<HH", 4, self.NAMES_SEG))
        self.hdr = TSR * 16 + image.find(HDR_SIG)

    def interrupt(self, vector, **regs):
        mu = self.mu
        mu.mem_write(CALLER * 16 + 0x600, bytes((0xCD, vector, 0x90)))
        for name, value in dict(cs=CALLER, ds=GAME_DS, ss=SS, esp=0x800, ebp=BP, eflags=IF | 2, **regs).items():
            mu.reg_write(getattr(r, "UC_X86_REG_" + name.upper()), value)
        mu.emu_start(CALLER * 16 + 0x600, CALLER * 16 + 0x602)
        return mu.reg_read(r.UC_X86_REG_SP)

    def test_room(self):
        """In place of "push dword 1": the chunk's size (the dword at [BP-4]) gets the room."""
        for size, want in ((8050, 8850), (0xFF00, 0xFF00 + 800)):
            self.mu.mem_write(SS * 16 + BP - 4, struct.pack("<I", size))
            self.assertEqual(self.interrupt(VEC_NAMES_SIZE), 0x7FC)
            self.assertEqual(struct.unpack("<II", self.mu.mem_read(SS * 16 + 0x7FC, 4) +
                                           self.mu.mem_read(SS * 16 + BP - 4, 4)), (1, want))

    def test_filled(self):
        """In place of "add sp,0Ch": with the chunk read (AX 0), DSCLOG's names after the game's."""
        names = self.NAMES_SEG * 16 + 4 + 0x142 * 25
        self.assertEqual(self.interrupt(VEC_NAMES_FILL, eax=0), 0x80C)
        self.assertEqual(bytes(self.mu.mem_read(names, 50)),
                         b"Ring/Protection".ljust(25, b"\0") + b"Thieves' Tools".ljust(25, b"\0"))
        self.assertEqual(struct.unpack("<HH", self.mu.mem_read(self.hdr + 200, 4)), (4, self.NAMES_SEG))
        self.assertEqual([self.mu.reg_read(x) for x in (r.UC_X86_REG_AX, r.UC_X86_REG_DS, r.UC_X86_REG_BP)],
                         [0, GAME_DS, BP])

    def test_not_read(self):
        self.assertEqual(self.interrupt(VEC_NAMES_FILL, eax=1), 0x80C)
        self.assertEqual(bytes(self.mu.mem_read(self.NAMES_SEG * 16 + 4 + 0x142 * 25, 4)), bytes(4))
        self.assertEqual(bytes(self.mu.mem_read(self.hdr + 200, 4)), bytes(4))
        self.assertEqual(self.mu.reg_read(r.UC_X86_REG_AX), 1)


@unittest.skipIf(Uc is None, "unicorn not installed")
class StealthTests(unittest.TestCase):
    """A hidden thief's attack (RULE_STEALTH, 64): from behind, a backstab when it can be."""
    SHEETS, TYPES = 0x8000, 0x9000

    def setUp(self):
        self.image = image = load_image()
        self.mu = mu = Uc(UC_ARCH_X86, UC_MODE_16)
        mu.mem_map(0, 0x100000)
        mu.mem_write(TSR * 16, image)
        self.hdr = TSR * 16 + image.find(HDR_SIG)
        at = image.find(bytes.fromhex("2ef606") + struct.pack("<H", 170) + bytes([64]))
        self.assertGreater(at, 0)
        mu.mem_write(VEC_STEALTH * 4, struct.pack("<HH", at - 15, TSR))  # (after its three pops)
        mu.hook_add(UC_HOOK_INTR, real_mode_interrupt)
        mu.mem_write(GAME_DS * 16 + 0x1661, struct.pack("<HH", 0, self.SHEETS))
        mu.mem_write(GAME_DS * 16 + 0x1669, struct.pack("<HH", 0, self.TYPES))
        mu.mem_write(TSR * 16 + 170, struct.pack("<H", 64))

    def word(self, offset, value=None):
        at = SS * 16 + (BP + offset) % 0x10000
        if value is not None:
            self.mu.mem_write(at, struct.pack("<h", value))
        return struct.unpack("<h", self.mu.mem_read(at, 2))[0]

    def attack(self, attacker=2, hidden=0b0100, behind=0, stab=0, thac0=15, thief=True, melee=1,
               weight=20, target_object=0):
        """INT VEC_STEALTH with SI the attacker; its sheet 5 ([BP-12h]) a thief or not, its
        weapon of type 7 ([BP-4]): ([BP-1Ah], [BP-24h], [BP-20h], what was pushed, STEALTH,
        STEALTH_USED)."""
        mu = self.mu
        mu.mem_write(self.hdr + 204, struct.pack("<HH", hidden, 0))
        mu.mem_write(self.SHEETS * 16 + 5 * 0x47 + 0x12, struct.pack("<H", 0x400 if thief else 0))
        mu.mem_write(self.TYPES * 16 + 7 * 0x14 + 4, struct.pack("<H", weight))
        for offset, value in ((-0x12, 5), (-4, 7), (-0x1A, behind), (-0x24, stab), (-0x20, thac0),
                              (-0x1C, target_object), (0x0E, melee)):
            self.word(offset, value)
        mu.mem_write(CALLER * 16 + 0x600, bytes((0xCD, VEC_STEALTH, 0x90)))
        for name, value in dict(cs=CALLER, ds=GAME_DS, ss=SS, esp=0x800, ebp=BP, eflags=IF | 2, esi=attacker,
                                eax=0x1111, ebx=0x2222, es=0x6666).items():
            mu.reg_write(getattr(r, "UC_X86_REG_" + name.upper()), value)
        mu.emu_start(CALLER * 16 + 0x600, CALLER * 16 + 0x602)
        self.assertEqual(mu.reg_read(r.UC_X86_REG_SP), 0x7FE)
        self.assertEqual([mu.reg_read(x) for x in (r.UC_X86_REG_AX, r.UC_X86_REG_BX, r.UC_X86_REG_ES)],
                         [0x1111, 0x2222, 0x6666])
        pushed, = struct.unpack("<h", mu.mem_read(SS * 16 + 0x7FE, 2))
        stealth, used = struct.unpack("<HH", mu.mem_read(self.hdr + 204, 4))
        return self.word(-0x1A), self.word(-0x24), self.word(-0x20), pushed, stealth, used

    def test_backstab(self):
        self.assertEqual(self.attack(), (1, 1, 11, 1, 0, 1))

    def test_behind_already(self):
        """The game had it from behind: only the backstab's +2 more."""
        self.assertEqual(self.attack(behind=1, thac0=13), (1, 1, 11, 1, 0, 1))

    def test_no_backstab(self):
        """From behind only: not a thief, a missile, a weapon too heavy."""
        for kw in (dict(thief=False), dict(melee=2), dict(weight=41)):
            self.assertEqual(self.attack(**kw), (1, 0, 13, 1, 0, 1), kw)

    def test_not_hidden(self):
        self.assertEqual(self.attack(hidden=0b1011), (0, 0, 15, 0, 0b1011, 0))
        self.assertEqual(self.attack(attacker=0x29, hidden=0b1111), (0, 0, 15, 0, 0b1111, 0))

    def test_an_object(self):
        """Attacking an object (no back): nothing, but the hiding is over."""
        self.assertEqual(self.attack(target_object=1), (0, 0, 15, 0, 0, 1))

    def test_rule_off(self):
        self.mu.mem_write(TSR * 16 + 170, struct.pack("<H", 0))
        self.assertEqual(self.attack(), (0, 0, 15, 0, 0b0100, 0))


@unittest.skipIf(Uc is None, "unicorn not installed")
class TypesTests(unittest.TestCase):
    """The game's item type table: room for TYPES_EXTRA more, and DSCLOG's copied in after."""
    TYPES_SEG = 0x5000

    def setUp(self):
        image = load_image()
        self.mu = mu = Uc(UC_ARCH_X86, UC_MODE_16)
        mu.mem_map(0, 0x100000)
        mu.mem_write(TSR * 16, image)
        size = image.find(bytes.fromhex("8146fcf000" "8356fe00"))  # 12 types of 20 bytes: F0h
        names_fill, fill = fill_probes(image)
        self.assertGreater(min(size, fill - names_fill), 0)
        mu.mem_write(VEC_TYPES_SIZE * 4, struct.pack("<HH", size, TSR))
        mu.mem_write(VEC_TYPES_FILL * 4, struct.pack("<HH", fill, TSR))
        mu.hook_add(UC_HOOK_INTR, real_mode_interrupt)
        mu.mem_write(GAME_DS * 16 + 0x1669, struct.pack("<HH", 0, self.TYPES_SEG))
        self.hdr = TSR * 16 + image.find(HDR_SIG)

    def interrupt(self, vector, **regs):
        mu = self.mu
        mu.mem_write(CALLER * 16 + 0x600, bytes((0xCD, vector, 0x90)))
        for name, value in dict(cs=CALLER, ds=GAME_DS, ss=SS, esp=0x800, ebp=BP, eflags=IF | 2, **regs).items():
            mu.reg_write(getattr(r, "UC_X86_REG_" + name.upper()), value)
        mu.emu_start(CALLER * 16 + 0x600, CALLER * 16 + 0x602)
        return mu.reg_read(r.UC_X86_REG_SP)

    def test_room_and_filled(self):
        """The game's 115 types (2300 bytes): 240 bytes more reserved, and after the read
        DSCLOG's types at 115 on, the number noted."""
        from dscompanion import npcitems
        self.mu.mem_write(SS * 16 + BP - 4, struct.pack("<I", 2300))
        self.assertEqual(self.interrupt(VEC_TYPES_SIZE), 0x7FC)
        self.assertEqual(struct.unpack("<I", self.mu.mem_read(SS * 16 + BP - 4, 4))[0], 2540)
        self.mu.mem_write(SS * 16 + 0x7FC, bytes(4))
        self.assertEqual(self.interrupt(VEC_TYPES_FILL, eax=0), 0x80C)
        at = self.TYPES_SEG * 16 + 115 * 20
        self.assertEqual(bytes(self.mu.mem_read(at, 20 * len(npcitems.TYPES))), b"".join(npcitems.TYPES))
        first, off, seg = struct.unpack("<HHH", self.mu.mem_read(self.hdr + 212, 6))
        self.assertEqual((first, off, seg), (115, 0, self.TYPES_SEG))
        self.assertEqual([self.mu.reg_read(x) for x in (r.UC_X86_REG_AX, r.UC_X86_REG_DS)], [0, GAME_DS])

    def test_not_read(self):
        self.mu.mem_write(SS * 16 + BP - 4, struct.pack("<I", 2460))
        self.assertEqual(self.interrupt(VEC_TYPES_FILL, eax=1), 0x80C)
        self.assertEqual(bytes(self.mu.mem_read(self.hdr + 212, 6)), bytes(6))


if __name__ == "__main__":
    unittest.main()


@unittest.skipIf(Uc is None, "unicorn is not installed")
class SavePageTests(unittest.TestCase):
    """PROBE_SAVE_PAGE (PgUp, PgDn) and PROBE_SAVE_CLICK (PAGE 1, PAGE 2) in the save/load window's
    event routine: the page's letter in the game's two save names, the window's own routines run
    (here each a RETF, counted), and the routine going on where it should."""
    DS, OV = 0x9000, 0xA000  # the game's DS; the window's overlay segment (DSUN.EXE 74300h)
    SAVE = DS + 0x3BA7 - 0x4356
    KEY_AT, CLICK_AT = 0x601, 0x89F  # (where the patches are, in the overlay: 74901h, 74B9Fh)
    DONE, KEY_END, CLICK_END, ENTER = 0x721, 0xAEC, 0xAE5, 0x968  # 74A21h, 74DECh, 74DE5h, 74C68h
    STUBS = {"scan": (OV, 0xE2), "row": (OV, 0xB36), "pick": (OV, 0xBCD),
             "button": (DS + 0x2A1D - 0x4356, 0x71A), "window": (DS + 0x25EC - 0x4356, 0x618)}

    def setUp(self):
        import re
        from dscompanion.gamepatch import VEC_SAVE_CLICK, VEC_SAVE_PAGE
        image = load_image()
        self.mu = mu = Uc(UC_ARCH_X86, UC_MODE_16)
        mu.mem_map(0, 0x100000)
        mu.mem_write(TSR * 16, image)
        mu.hook_add(UC_HOOK_INTR, real_mode_interrupt)
        # the two handlers: "push bp / mov bp,sp / sti / pushad / push es", then sp_done's value
        starts = {struct.unpack_from("<H", image, m.end() + 2)[0]: m.start()
                  for m in re.finditer(re.escape(bytes.fromhex("5589e5fb6660062ec706")), image)}
        mu.mem_write(VEC_SAVE_PAGE * 4, struct.pack("<HH", starts[0x74A21 - 0x74903], TSR))
        mu.mem_write(VEC_SAVE_CLICK * 4, struct.pack("<HH", starts[(0x74A21 - 0x74BA1) & 0xFFFF], TSR))
        mu.mem_write(self.OV * 16 + self.KEY_AT, bytes((0xCD, VEC_SAVE_PAGE, 0x90)))
        mu.mem_write(self.OV * 16 + self.CLICK_AT, bytes((0xCD, VEC_SAVE_CLICK, 0x90)))
        self.calls = {}
        for name, (seg, off) in self.STUBS.items():
            mu.mem_write(seg * 16 + off, b"\xcb")  # RETF
            mu.hook_add(UC_HOOK_CODE, lambda *_, n=name: self.calls.__setitem__(n, self.calls.get(n, 0) + 1),
                        begin=seg * 16 + off, end=seg * 16 + off)
        mu.mem_write(self.DS * 16 + 0x1DCF, b"SAVE??.SAV\0SAVE%.2d.SAV\0")
        mu.mem_write(self.SAVE * 16 + 0x4E4, struct.pack("<HIH", 3, 0x12345678, 0))  # row 3, saving

    def page(self):
        return bytes(self.mu.mem_read(self.DS * 16 + 0x1DCF + 3, 1)) + bytes(self.mu.mem_read(self.DS * 16 + 0x1DDA + 3, 1))

    def run_at(self, at, word, value):
        """The event routine (its BP+WORD holding VALUE) at the patch AT: where it goes on, and SI."""
        mu = self.mu
        self.calls.clear()
        mu.mem_write(SS * 16 + BP + word, struct.pack("<H", value))
        for name, v in dict(cs=self.OV, ds=self.DS, ss=SS, esp=0x800, ebp=BP, eflags=IF | 2, esi=0x4321,
                            edi=1, es=0x4444).items():
            mu.reg_write(getattr(r, "UC_X86_REG_" + name.upper()), v)
        ends = (self.DONE, self.KEY_END, self.CLICK_END, self.ENTER)
        mu.hook_add(UC_HOOK_CODE, lambda m, *_: m.emu_stop() if m.reg_read(r.UC_X86_REG_CS) == self.OV
                    and m.reg_read(r.UC_X86_REG_IP) in ends else None)
        mu.emu_start(self.OV * 16 + at, 0, count=20000)
        self.assertEqual([mu.reg_read(x) for x in (r.UC_X86_REG_SP, r.UC_X86_REG_DI, r.UC_X86_REG_ES)],
                         [0x800, 1, 0x4444])
        return mu.reg_read(r.UC_X86_REG_IP), mu.reg_read(r.UC_X86_REG_SI)

    def test_keys(self):
        self.assertEqual(self.run_at(self.KEY_AT, 0x12, 0x5100), (self.DONE, 0x4321))  # PgDn
        self.assertEqual(self.page(), b"BB")
        self.assertEqual(self.calls, {"scan": 1, "row": 10, "button": 2, "pick": 1, "window": 1})
        self.run_at(self.KEY_AT, 0x12, 0x5100)
        self.run_at(self.KEY_AT, 0x12, 0x5100)
        self.assertEqual(self.page(), b"DD")
        self.assertEqual(self.run_at(self.KEY_AT, 0x12, 0x5100), (self.KEY_END, 0x4321))  # (the last page)
        self.assertEqual((self.page(), self.calls), (b"DD", {}))
        self.assertEqual(self.run_at(self.KEY_AT, 0x12, 0x49E0), (self.DONE, 0x4321))  # PgUp, the grey key
        self.assertEqual(self.page(), b"CC")
        self.run_at(self.KEY_AT, 0x12, 0x4900)
        self.run_at(self.KEY_AT, 0x12, 0x4900)
        self.assertEqual(self.page(), b"EE")
        self.assertEqual(self.run_at(self.KEY_AT, 0x12, 0x4900), (self.KEY_END, 0x4321))  # (the first page)
        self.assertEqual(self.run_at(self.KEY_AT, 0x12, 0x1E61), (self.KEY_END, 0x4321))  # another key
        self.assertEqual((self.page(), self.calls), (b"EE", {}))

    def test_buttons(self):
        for button, page in ((0x818, b"DD"), (0x816, b"BB"), (0x817, b"CC"), (0x815, b"EE")):
            self.assertEqual(self.run_at(self.CLICK_AT, 8, button), (self.DONE, 0))  # (the routine returns 0)
            self.assertEqual(self.page(), page)
        self.assertEqual(self.run_at(self.CLICK_AT, 8, 0x815), (self.CLICK_END, 0x4321))  # (the page shown)
        self.assertEqual(self.run_at(self.CLICK_AT, 8, 0x819), (self.CLICK_END, 0x4321))  # another button
        self.assertEqual((self.page(), self.calls), (b"EE", {}))

    def test_loading_a_page_with_no_saves(self):
        self.mu.mem_write(self.SAVE * 16 + 0x4EA, struct.pack("<H", 1))  # the load window; no saves found
        self.assertEqual(self.run_at(self.KEY_AT, 0x12, 0x5100), (self.KEY_END, 0x4321))
        self.assertEqual(self.page(), b"EE")  # (back)
        self.assertEqual(self.calls, {"scan": 4})  # (pages 2, 3 and 4 looked at)
        # a button's page is shown even with none, its first row chosen (SAVE_LABEL greys LOAD)
        self.assertEqual(self.run_at(self.CLICK_AT, 8, 0x817), (self.DONE, 0))
        self.assertEqual(self.page(), b"CC")
        self.assertEqual(self.calls, {"scan": 1, "row": 10, "button": 2, "pick": 1, "window": 1})
        self.assertEqual(struct.unpack("<H", self.mu.mem_read(self.SAVE * 16 + 0x4E4, 2))[0], 0)

    def test_enter(self):
        """Enter (out of the window's key table) goes on to LOAD or SAVE, as the table took it, but
        not in the load window on a row with no save (the game would start a new game)."""
        mu = self.mu
        self.assertEqual(self.run_at(self.KEY_AT, 0x12, 0x1C0D), (self.ENTER, 0x4321))  # (saving)
        mu.mem_write(self.SAVE * 16 + 0x4EA, struct.pack("<H", 1))  # loading, row 3
        self.assertEqual(self.run_at(self.KEY_AT, 0x12, 0x1C0D), (self.KEY_END, 0x4321))  # (no save there)
        mu.mem_write(self.SAVE * 16 + 2 + 3 * 0x7D, b"SAVE04.SAV\0")
        self.assertEqual(self.run_at(self.KEY_AT, 0x12, 0x1C0D), (self.ENTER, 0x4321))
        self.assertEqual(self.calls, {})

    def test_loading_passes_a_page_with_no_saves(self):
        """PgDn in the load window: page 2 has none, page 3 a save in its third row."""
        mu = self.mu
        mu.mem_write(self.SAVE * 16 + 0x4EA, struct.pack("<H", 1))
        rows = self.SAVE * 16 + 2 + 2 * 0x7D
        scan = self.STUBS["scan"]
        # the folder search: a save in the third row when the page's letter is C
        mu.hook_add(UC_HOOK_CODE, lambda m, *_: m.mem_write(rows, b"x" if bytes(m.mem_read(self.DS * 16 + 0x1DD2, 1)) == b"C"
                                                             else b"\0"),
                    begin=scan[0] * 16 + scan[1], end=scan[0] * 16 + scan[1])
        self.assertEqual(self.run_at(self.KEY_AT, 0x12, 0x5100), (self.DONE, 0x4321))
        self.assertEqual(self.page(), b"CC")
        self.assertEqual(struct.unpack("<H", mu.mem_read(self.SAVE * 16 + 0x4E4, 2))[0], 2)  # (chosen: that row)


@unittest.skipIf(Uc is None, "unicorn not installed")
class LevelPickTests(unittest.TestCase):
    """PROBE_LV_PICK: at a level gained, a warrior short of weapon kinds has the psionicists' pop-up
    called (here a stand-in that counts its calls), if there is a kind it can pick (the stand-in
    weapons are bone: none for a fire cleric); the PROBE_PK_* probes in that pop-up, out of weapon
    mode, do just what they replaced."""
    SHEETS, TYPES_SEG = 0x8000, 0x9000
    RULES = 170
    STAND_IN, CALLS = 0x700, 0x7F0
    PLAIN_TYPES = (81, 18, 17, 115, 20, 22, 2, 112, 3, 19, 44, 21, 48, 1, 64, 0)

    def setUp(self):
        import re
        from dscompanion.gamepatch import VEC_LV_PICK
        self.image = image = load_image()
        self.mu = mu = Uc(UC_ARCH_X86, UC_MODE_16)
        mu.mem_map(0, 0x100000)
        mu.mem_write(TSR * 16, image)
        at = image.find(bytes.fromhex("fb66600689e31e5636c57722"))
        self.assertGreater(at, 0)
        mu.mem_write(VEC_LV_PICK * 4, struct.pack("<HH", at, TSR))
        mu.hook_add(UC_HOOK_INTR, real_mode_interrupt)
        mu.mem_write(GAME_DS * 16 + 0x1661, struct.pack("<HH", 0, self.SHEETS))
        mu.mem_write(GAME_DS * 16 + 0x1669, struct.pack("<HH", 0, self.TYPES_SEG))
        for t in self.PLAIN_TYPES:  # (every class may use them; melee, bone)
            rec = bytearray(game.ITEM_TYPE_SIZE)
            rec[0], rec[8] = 1, 1
            rec[0x10:0x12] = b"\xff\xff"
            mu.mem_write(self.TYPES_SEG * 16 + t * game.ITEM_TYPE_SIZE, bytes(rec))
        # the level-up routine: the INT, its NOPs and the JNZ; the far call to the pop-up 13h on
        mu.mem_write(CALLER * 16 + 0x600, bytes((0xCD, VEC_LV_PICK, 0x90, 0x90, 0x75, 0x07)))
        mu.mem_write(CALLER * 16 + 0x602 + 0x13, struct.pack("<HH", self.STAND_IN, CALLER))
        mu.mem_write(CALLER * 16 + self.STAND_IN, bytes.fromhex("2eff06f007cb"))  # inc word [cs:7F0h]; retf
        self.stops = []

        def stop(uc, address, size, _):
            uc.emu_stop()
            self.stops.append(address - CALLER * 16)
        mu.hook_add(UC_HOOK_CODE, stop, begin=CALLER * 16 + 0x606, end=CALLER * 16 + 0x606)
        mu.hook_add(UC_HOOK_CODE, stop, begin=CALLER * 16 + 0x60D, end=CALLER * 16 + 0x60D)

    def level_up(self, classes, levels, chosen=(), member=1, cls=None, rules=4096, race=2):
        """(the pop-up's calls, where the routine went on) for a level gained in class CLS."""
        mu = self.mu
        mu.mem_write(TSR * 16 + self.image.find(HDR_SIG) + self.RULES, struct.pack("<H", rules))
        mu.mem_write(CALLER * 16 + self.CALLS, bytes(2))
        sheet = bytearray(test_restrict.sheet(*classes, race=race))
        sheet[0x24:0x24 + len(levels)] = bytes(levels)
        sheet[0x12:0x14] = b"\xff\x07"
        for i, k in enumerate(chosen):
            sheet[0x14 + i] = k + 1
        mu.mem_write(self.SHEETS * 16 + member * 0x47, bytes(sheet))
        mu.mem_write(SS * 16 + BP + 8, struct.pack("<H", classes[0] if cls is None else cls))
        self.stops.clear()
        for name, value in dict(cs=CALLER, ds=GAME_DS, ss=SS, esp=0x7FC, ebp=BP, eflags=IF | 2, esi=member,
                                es=0x6666).items():
            mu.reg_write(getattr(r, "UC_X86_REG_" + name.upper()), value)
        mu.emu_start(CALLER * 16 + 0x600, CALLER * 16 + 0x6FF, count=200000)
        self.assertEqual([mu.reg_read(getattr(r, "UC_X86_REG_" + x)) for x in ("SP", "SI", "ES", "DS")],
                         [0x7FC, member, 0x6666, GAME_DS])
        return struct.unpack("<H", mu.mem_read(CALLER * 16 + self.CALLS, 2))[0], self.stops[0]

    def test_asked_while_short(self):
        cases = [  # (classes, levels, kinds it has, asked)
            ((10,), (5,), (), True), ((10,), (5,), (0,), True), ((10,), (5,), (0, 1), False),
            ((10,), (6,), (0, 1), True), ((10,), (6,), (0, 1, 2), False), ((10,), (9,), (0, 1, 2), True),
            ((9,), (2,), (), True), ((9,), (2,), (3,), False), ((14,), (3,), (), True),
            ((9, 4), (4, 4), (), True), ((9, 3), (4, 4), (), False), ((11,), (5,), (), False), ((12,), (5,), (), False),
        ]
        for classes, levels, chosen, asked in cases:
            with self.subTest(classes=classes, levels=levels, chosen=chosen):
                self.assertEqual(self.level_up(classes, levels, chosen)[0], int(asked))

    def test_not_asked(self):
        self.assertEqual(self.level_up((10,), (5,), rules=0)[0], 0)
        self.assertEqual(self.level_up((10,), (5,), member=4)[0], 0)  # (not in the party)
        # a human fighter turned preserver: not until the preserver's level passes the fighter's
        self.assertEqual(self.level_up((11, 9), (3, 4), race=game.HUMAN)[0], 0)
        self.assertEqual(self.level_up((11, 9), (5, 4), race=game.HUMAN)[0], 1)

    def test_goes_on_as_the_compare(self):
        """A preserver's level on to its spell (past the JNZ), any other to the JNZ's target."""
        self.assertEqual(self.level_up((11,), (5,), cls=11)[1], 0x606)
        self.assertEqual(self.level_up((10,), (5,), cls=10)[1], 0x60D)
        self.assertEqual(self.level_up((10,), (5,), cls=10, rules=0)[1], 0x60D)

    def run_probe(self, pattern, vector, code, regs, stop):
        import re
        at = re.search(pattern, self.image, re.S).start()
        mu = self.mu
        mu.mem_write(vector * 4, struct.pack("<HH", at, TSR))
        self.code_at = getattr(self, "code_at", 0x800) + 0x20  # (each its own: the emulator keeps
        mu.mem_write(CALLER * 16 + self.code_at, bytes(code))    #  the code it has translated)
        values = dict(cs=CALLER, ds=GAME_DS, ss=SS, esp=0x7FC, ebp=BP, eflags=IF | 2)
        values.update(regs)
        for name, value in values.items():
            mu.reg_write(getattr(r, "UC_X86_REG_" + name.upper()), value)
        mu.emu_start(CALLER * 16 + self.code_at, CALLER * 16 + self.code_at + stop)

    def test_popup_probes_as_the_game(self):
        from dscompanion.gamepatch import VEC_PK_COUNT, VEC_PK_WIN, VEC_PK_LEFT, VEC_PK_TITLE, VEC_PK_FILL, VEC_PK_CLICK
        mu = self.mu
        mu.mem_write(GAME_DS * 16 + 0x4AEC, bytes((3,)))
        self.run_probe(rb"\xa0\xec\x4a\x2e\x80\x3e", VEC_PK_LEFT, (0xCD, VEC_PK_LEFT, 0x90), dict(eax=0x1200), 3)
        self.assertEqual(mu.reg_read(r.UC_X86_REG_AX), 0x1203)
        for ax, zero in ((0, True), (5, False)):
            self.run_probe(rb"\x89\xc2\x2e\x80\x3e..\x00\x74\x03\xba\x02\x00", VEC_PK_COUNT, (0xCD, VEC_PK_COUNT, 0x90, 0x90), dict(eax=ax, edx=0x99), 4)
            self.assertEqual(mu.reg_read(r.UC_X86_REG_DX), ax)
            self.assertEqual(bool(mu.reg_read(r.UC_X86_REG_EFLAGS) & 0x40), zero)
        self.run_probe(rb"\x83\xec\x02\x55\x89\xe5\x50.{18}\xc7\x46\x08\x5d\x44", VEC_PK_WIN, (0xCD, VEC_PK_WIN, 0x90), {}, 3)
        self.assertEqual(mu.reg_read(r.UC_X86_REG_SP), 0x7FA)
        self.assertEqual(struct.unpack("<H", mu.mem_read(SS * 16 + 0x7FA, 2))[0], 0x445D)
        self.run_probe(rb"\x83\xec\x04\x55\x89\xe5\x50.{18}\x8c\x5e\x0a", VEC_PK_TITLE, bytes((0xCD, VEC_PK_TITLE, 0x90, 0x90)) + bytes(16), {}, 4)
        self.assertEqual(mu.reg_read(r.UC_X86_REG_SP), 0x7F8)
        self.assertEqual(struct.unpack("<HH", mu.mem_read(SS * 16 + 0x7F8, 4)), (0x3026, GAME_DS))
        after = CALLER * 16 + self.code_at + 2  # (the line's colours, in the pushes after it: the game's)
        self.assertEqual((mu.mem_read(after + 6, 1)[0], mu.mem_read(after + 0xC, 1)[0]), (0xD0, 0xD3))
        self.run_probe(rb"\x31\xff\x89\xfe\x2e\x80\x3e", VEC_PK_FILL, (0xCD, VEC_PK_FILL, 0x90, 0x90), dict(esi=5, edi=6), 4)
        self.assertEqual((mu.reg_read(r.UC_X86_REG_SI), mu.reg_read(r.UC_X86_REG_DI)), (0, 0))
        mu.mem_write(SS * 16 + BP + 8, struct.pack("<H", 0x2C38))
        self.run_probe(rb"\x55\x89\xe5\x53\x8b\x5e\x00\x36\x8b\x47\x08", VEC_PK_CLICK, (0xCD, VEC_PK_CLICK, 0x90), {}, 3)
        self.assertEqual(mu.reg_read(r.UC_X86_REG_AX), 0x2C38)
        self.assertEqual(mu.reg_read(r.UC_X86_REG_SP), 0x7FC)

    def test_hit_die_best_of_two(self):
        """PROBE_HP_BEST: with the rule, the first roll sends the game back to roll again (872FDh,
        1Eh before the INT's return); the second gives CX the better of the two. Without, CX the
        roll, as the "mov cx,ax" it replaced."""
        import re
        from dscompanion.gamepatch import VEC_HP_BEST
        mu = self.mu
        at = re.search(rb"\x2e\xf7\x06..\x00\x80\x74", self.image, re.S).start()
        mu.mem_write(VEC_HP_BEST * 4, struct.pack("<HH", at, TSR))
        int_at = 0xA00 + 0x8731B - 0x872FD - 2  # (the INT, so that going back lands on 0xA00)
        mu.mem_write(CALLER * 16 + int_at, bytes((0xCD, VEC_HP_BEST)))

        def roll(ax):
            for name, value in dict(cs=CALLER, ds=GAME_DS, ss=SS, esp=0x7FC, ebp=BP, eflags=IF | 2, eax=ax,
                                    ecx=0x3333).items():
                mu.reg_write(getattr(r, "UC_X86_REG_" + name.upper()), value)
            mu.emu_start(CALLER * 16 + int_at, 0, count=40)
            return mu.reg_read(r.UC_X86_REG_IP), mu.reg_read(r.UC_X86_REG_CX), mu.reg_read(r.UC_X86_REG_SP)
        for rules, first, second in ((32768, 3, 8), (32768, 9, 2), (32768, 5, 5)):
            with self.subTest(first=first, second=second):
                mu.mem_write(TSR * 16 + self.image.find(HDR_SIG) + self.RULES, struct.pack("<H", rules))
                mu.mem_write(CALLER * 16 + 0xA00, bytes((0xF4,)))  # (hlt: back at the roll)
                mu.mem_write(CALLER * 16 + int_at + 2, bytes((0xF4,)))
                self.assertEqual(roll(first)[:3:2], (0xA01, 0x7FC))  # back to roll again (past the hlt)
                self.assertEqual(roll(second), (int_at + 3, max(first, second), 0x7FC))
        mu.mem_write(TSR * 16 + self.image.find(HDR_SIG) + self.RULES, struct.pack("<H", 0))
        self.assertEqual(roll(4)[:2], (int_at + 3, 4))

    def test_effects_rows_pops(self):
        """PROBE_EF_ROWS does the "pop di / pop si" it replaced (nothing drawn: the rule off, or
        the lower panel in use, past 21 cells)."""
        from dscompanion.gamepatch import VEC_EF_ROWS
        mu = self.mu
        for rules, cells in ((0, 3), (4096, 30)):
            with self.subTest(rules=rules, cells=cells):
                mu.mem_write(TSR * 16 + self.image.find(HDR_SIG) + self.RULES, struct.pack("<H", rules))
                mu.mem_write(SS * 16 + BP - 4, struct.pack("<H", cells))
                mu.mem_write(SS * 16 + 0x7F8, struct.pack("<HH", 0x1111, 0x2222))  # (DI's, then SI's)
                self.run_probe(rb"\xfb\x66\x60\x06\x2e\xf7\x06..\x00\x10", VEC_EF_ROWS,
                               (0xCD, VEC_EF_ROWS), dict(esp=0x7F8, esi=5, edi=6), 2)
                self.assertEqual([mu.reg_read(getattr(r, "UC_X86_REG_" + x)) for x in ("DI", "SI", "SP", "BP")],
                                 [0x1111, 0x2222, 0x7FC, BP])
