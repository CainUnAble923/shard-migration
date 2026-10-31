"""cc-P690 (SoS swap S17): the swapped world played through by one real character, after the isle.

Iron Islander, who played the whole Wakening Isle in isle.py and came through the dock moongate to Rook, goes on into
the world, through the play-test bot's client (the packets a real client sends): every public moongate on Trammel and
Felucca, a walk to each of the author's new towns, Rootdeep by the cellar hatch, a boat from Haven's dock, a treasure
map read and dug, and a Felucca champion's altar seen. Staff help (the private shard's owner) is used only where a
player would have spent hours (long voyages, a treasure spot across the map) and is logged as STAFF on its own line.

    python -P tour.py --port 2596 --out <folder> --secrets <owner secrets.json> [--parts gates,towns,hatch,boat,treasure,champion]

Walking plans on P688's whole-map walk grid (notes/cc-P688-tools/walkgrid.py, cached in %TEMP%\\p688-walkgrid.npz:
pinned Movement.cs reduced to the SoS files), steps through the server, and learns any step the server refuses
(re-planning), as P480's walker does. Teleporter sources (server/data/teleporters-sos.json) are avoided unless they are
the goal. Writes <out>/tour-log.txt (the evidence: PASS/FAIL checks, arrivals, System lines) and <out>/transcript.txt.
Test ports only (safety.check_test_target). ASCII only.
"""
import argparse
import heapq
import json
import os
import re
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
NOTES = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(os.path.dirname(NOTES), "scripts"))
CODE = r"D:\UO\golems\Iron\ShatteredLegacy"
NONE = -32768
STEP = 2
DIRS8 = ((0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1))   # UO direction 0..7
GATE_IDS = (0x0F6C, 0x0DDA, 0x1FD4, 0x1FE7)
PK = None   # uobot.packets, set in main
ADM = None  # the owner's client, set in main


def server_loc(name):
    """The server's own location for a character (staff [global get), for when the client's is stale: the bot does
    not read a ship's move packet (0xF6), so its position stays where it boarded (run 13)."""
    out = ADM.command('[global get Location where playermobile Name == "%s"' % name, settle=2.0)
    for m in out:
        r = re.search(r"Location = \((-?\d+), (-?\d+), (-?\d+)\)", m.get("text") or "")
        if r:
            return tuple(int(v) for v in r.groups())
    return None

# -- the places -----------------------------------------------------------------------------------------------------
# P679's PMList (server/patches/PublicMoongate-sos-gates.patch), pinned's order; New Haven is HavenSpots.PublicMoongate.
TRAM_GATES = [("Moonglow", (4467, 1283)), ("Britain", (1336, 1997)), ("Jhelom", (1499, 3771)), ("Yew", (771, 752)),
              ("Minoc", (2701, 692)), ("Trinsic", (1828, 2948)), ("Skara Brae", (643, 2067)),
              ("Magincia", (3563, 2139)), ("New Haven", (3696, 2570))]
FEL_GATES = TRAM_GATES[:8] + [("Buccaneer's Den", (2711, 2234))]
# P688 out/places.csv: each new town's bank, and the place (a gate or a bank) the walk starts from.
TOWNS = [   # (town, its bank, where the walk starts, that place, the gate walked back to, an entry walked exactly)
    ("Elmhaven", (1965, 3159), "Trinsic gate", (1828, 2948), (1828, 2948), None),
    ("Kameron Kove", (1297, 2461), "Britain gate", (1336, 1997), None, None),
    ("Kettleburg", (632, 2395), "Kameron Kove bank", (1297, 2461), (1336, 1997), None),
    ("Hammerhill", (1538, 985), "Britain gate", (1336, 1997), (1336, 1997), None),
    # P688: the fort's gate is two static doors; the way in is up the gatehouse stairs to a z20 walkway, which one level
    # a tile cannot follow: the last stretch from 3419,311 is walked by P688's exact.py (every level of a tile)
    ("Fort Yondall", (3393, 337), "Minoc gate", (2701, 692), None, (3419, 311)),
]
VALUNSTEAD = (482, 430)
HATCH, BESIDE_HATCH = (3618, 2620), (3621, 2620)       # ClusterFRootdeepSeeder (cc-P678)
LADDER_FOOT = (5193, 1132)                             # ClusterFRootdeepSeeder: the teleporter up
HAVEN_BANK = (3620, 2617)
HAVEN_DOCK = (3650, 2653)


class Log:
    def __init__(self, path):
        self.f = open(path, "a", encoding="ascii", errors="replace")
        self.t0 = time.time()
        self.fails = []
        self.passes = 0

    def __call__(self, text):
        line = "[%7.1f] %s" % (time.time() - self.t0, text)
        print(line, flush=True)
        self.f.write(line + "\n")
        self.f.flush()

    def check(self, ok, what):
        self("%s %s" % ("PASS" if ok else "FAIL", what))
        if ok:
            self.passes += 1
        else:
            self.fails.append(what)
        return ok


def make_client_class(Client, P):
    class TourClient(Client):
        """The bot's client, plus what a player's client shows that the tour needs: the facet (0xBF 0x08), and a
        map's bounds (0x90 / 0xF5) and pins (0x56), read the way the client draws them."""

        def __init__(self, *a, **k):
            super().__init__(*a, **k)
            self.facet = None
            self.mapdetails = {}
            self.mappins = {}

        def _handle(self, p):
            pid = p[0]
            try:
                if pid == 0xBF and len(p) >= 6 and P.u16(p, 3) == 0x08:
                    if self.facet is not None and p[5] != self.facet:
                        # run 3: a real client forgets the old facet's world; the bot kept Trammel's gate and clicked it
                        for k in [k for k, it in list(self.items.items()) if it.get("world")]:
                            self.items.pop(k, None)
                        for k in [k for k in list(self.mobiles) if k != self.serial]:
                            self.mobiles.pop(k, None)
                    self.facet = p[5]
                elif pid in (0x90, 0xF5) and len(p) >= 19:
                    s = P.u32(p, 1)
                    self.mapdetails[s] = tuple(P.u16(p, o) for o in (7, 9, 11, 13, 15, 17))
                elif pid == 0x99 and len(p) >= 6:
                    # run 7: a ship deed asks with a MULTI target cursor (0x99); the answer is a normal 0x6C ground
                    # target with its id (as a client does); the bot read only 0x6C
                    self.target = (P.i32(p, 2), 1)
                elif pid == 0x56 and len(p) >= 11:
                    s = P.u32(p, 1)
                    if p[5] == 1:
                        self.mappins.setdefault(s, []).append((P.u16(p, 7), P.u16(p, 9)))
            except Exception:
                pass
            return super()._handle(p)
    return TourClient


class Grid:
    """P688's whole-map arrays (stand, low, top; index [x, y]); the step rule of walkgrid.steps."""

    def __init__(self, items):
        d = np.load(os.path.join(os.environ["TEMP"], "p688-walkgrid.npz"))
        self.stand, self.low, self.top = d["stand"], d["low"], d["top"]
        self.items = items
        self.learned = set()
        self.avoid = set()
        try:
            for t in json.load(open(os.path.join(CODE, "server", "data", "teleporters-sos.json"), encoding="utf-8")):
                self.avoid.add((t["src"]["loc"][0], t["src"]["loc"][1]))
        except Exception:
            pass
        # run 14: the two cellar hatches are server items (not in teleporters-sos.json); avoid them unless the goal
        self.avoid |= {(3618, 2620), (1519, 1437)}

    def ok(self, x, y):
        return 0 <= x < 7168 and 0 <= y < 4096 and self.stand[x, y] != NONE

    def can(self, a, b, blocked):
        if b in blocked or not self.ok(*b) or not self.ok(*a):
            return False
        return int(self.top[a]) + STEP >= int(self.low[b])

    def path(self, start, goals, blocked, pad=60, limit=1500000):
        goals = set(goals)
        gx = [g[0] for g in goals] + [start[0]]
        gy = [g[1] for g in goals] + [start[1]]
        box = (min(gx) - pad, min(gy) - pad, max(gx) + pad, max(gy) + pad)
        tx, ty = sum(g[0] for g in goals) / len(goals), sum(g[1] for g in goals) / len(goals)
        blocked = (blocked | self.avoid) - goals
        prev = {start: None}
        cost = {start: 0}
        q = [(0, 0, start)]
        n = 0
        while q:
            _, c0, c = heapq.heappop(q)
            n += 1
            if n > limit:
                return None
            if c in goals:
                out = []
                while c is not None:
                    out.append(c)
                    c = prev[c]
                return out[::-1]
            if c0 > cost.get(c, 1 << 30):
                continue
            for dx, dy in DIRS8:
                nb = (c[0] + dx, c[1] + dy)
                if not (box[0] <= nb[0] <= box[2] and box[1] <= nb[1] <= box[3]):
                    continue
                if not self.can(c, nb, blocked) and not (c == start and not self.ok(*start) and self.ok(*nb) and nb not in blocked):
                    continue   # run 6: a start the one-level grid cannot stand on (a gate's circle) may step to any neighbour
                if c != start and dx and dy and not (self.can(c, (c[0] + dx, c[1]), blocked) and self.can(c, (c[0], c[1] + dy), blocked)):
                    continue
                nc = c0 + (3 if dx and dy else 2)
                if nc < cost.get(nb, 1 << 30):
                    cost[nb] = nc
                    prev[nb] = c
                    h = 2 * max(abs(nb[0] - tx), abs(nb[1] - ty))
                    heapq.heappush(q, (nc + h, nc, nb))
        return None


class Walker:
    def __init__(self, c, grid, log):
        self.c, self.g, self.log = c, grid, log
        self.seen = 0

    def drain(self):
        for m in self.c.messages[self.seen:]:
            t = m.get("text") or ""
            if m.get("name") in (None, "", "System") or re.search(r"moongate|ship|treasure|dig|hatch|fog|guard|young", t, re.I):
                self.log("  say  %s: %s" % (m.get("name") or "-", t))
        self.seen = len(self.c.messages)

    def pos(self):
        return (self.c.pos[0], self.c.pos[1])

    def blocked_now(self):
        out = set(self.g.learned)
        for s, it in list(self.c.items.items()):
            g = it.get("graphic")
            if it.get("world") and g is not None and g < len(self.g.items):
                td = self.g.items[g]
                if td["flags"] & 0x40 and not td["flags"] & 0x200 and "door" not in td["name"].lower():
                    out.add((it["x"], it["y"]))
        for s, m in list(self.c.mobiles.items()):
            if s != self.c.serial and "x" in m:
                out.add((m["x"], m["y"]))
        return out

    def door_at(self, xy):
        for s, it in list(self.c.items.items()):
            g = it.get("graphic")
            if it.get("world") and (it.get("x"), it.get("y")) == xy and g is not None and g < len(self.g.items) \
                    and "door" in self.g.items[g]["name"].lower():
                return s
        return None

    def step(self, d):
        before = self.pos()
        for _ in range(2):
            if self.c.walk(d, 1, run=True, pause=0.04) != 1:
                return False
            if self.pos() != before:
                return True
        return self.pos() != before

    def go_exact(self, target, rect, what=""):
        """P688's exact.py over rect: pinned Movement.cs with every level of a tile; then the steps, as go() takes them."""
        sys.path.insert(0, os.path.join(NOTES, "cc-P688-tools"))
        import exact
        t0 = time.time()
        e = exact.Exact(rect)
        z = int(self.c.pos[2])
        if ADM is not None:   # run 14: the client's Z is stale after walks; start from the server's own
            sl = server_loc(self.c.name if hasattr(self.c, "name") and self.c.name else "Iron Islander")
            if sl and (sl[0], sl[1]) == self.pos():
                z = sl[2]
        prev, end = e.flood(self.pos()[0], self.pos()[1], z, target)
        if end is None:
            self.log("  exact walk %s: no way from %s to %s inside %s" % (what, self.c.pos[:3], target, rect))
            return False
        path = []
        c = end
        while c is not None:
            path.append((c[0], c[1]))
            c = prev[c]
        path = path[::-1]
        n = 0
        for a, b in zip(path, path[1:]):
            if self.pos() != a:
                break
            if not self.step(DIRS8.index((b[0] - a[0], b[1] - a[1]))):
                self.log("  exact walk %s: the server refused %s -> %s" % (what, a, b))
                break
            n += 1
        ok = self.pos() == target
        self.log("  exact walk %s: %s at %s after %d of %d steps, %.0f s" % (what, "arrived" if ok else "STOPPED", self.c.pos[:3], n, len(path) - 1, time.time() - t0))
        self.drain()
        return ok

    def go(self, target, within=0, tries=25, what=""):
        t0 = time.time()
        goals = [(target[0] + dx, target[1] + dy) for dx in range(-within, within + 1) for dy in range(-within, within + 1)]
        start = self.pos()
        steps = 0
        opened = []
        for attempt in range(tries):
            if self.pos() in goals:
                break
            p = None
            for pad in (60, 220, 450):   # run 4: a 60-tile box cut off the detours round hills and water
                p = self.g.path(self.pos(), goals, self.blocked_now(), pad=pad, limit=6000000)
                if not p:
                    p = self.g.path(self.pos(), goals, set(self.g.learned), pad=pad, limit=6000000)
                if p:
                    break
            if not p:
                bl = self.blocked_now()
                self.log("  walk: no path from %s to %s within %d (start standable %s; %d blocked tiles, %d learned, start blocked %s)" % (
                    self.pos(), target, within, self.g.ok(*self.pos()), len(bl), len(self.g.learned), self.pos() in bl))
                break
            for a, b in zip(p, p[1:]):
                if self.pos() != a:
                    if max(abs(self.pos()[0] - a[0]), abs(self.pos()[1] - a[1])) > 3:
                        self.log("  walk: moved by the world from %s to %s (a teleporter?)" % (a, self.pos()))
                    break
                if not self.step(DIRS8.index((b[0] - a[0], b[1] - a[1]))):
                    door = self.door_at(b)
                    if door and opened.count(door) < 3:
                        opened.append(door)
                        self.c.dclick(door)
                        self.c.sleep(0.8)
                    else:
                        self.g.learned.add(b)
                    break
                steps += 1
                if steps % 200 == 0:
                    self.c.keepalive()
            self.drain()
        ok = self.pos() in goals
        if not ok and max(abs(self.pos()[0] - target[0]), abs(self.pos()[1] - target[1])) <= 25:
            # run 5: one level a tile stalled at Kameron Kove's bank; finish with every level of a tile (P688 exact.py)
            self.log("  walk %s: stalled at %s, %d steps in; the last stretch walked exactly" % (what, self.c.pos[:3], steps))
            x, y = self.pos()
            ok = self.go_exact(target, (min(x, target[0]) - 30, min(y, target[1]) - 30, max(x, target[0]) + 30, max(y, target[1]) + 30), what)
        self.log("  walk %s: %s from %s to %s in %d steps, %.0f s (target %s within %d)" % (
            what, "arrived" if ok else "STUCK", start, self.pos(), steps, time.time() - t0, target, within))
        return ok


def staff(adm, log, text, settle=2.0):
    log("  STAFF %s" % text)
    out = adm.command(text, settle=settle)
    for m in out:
        log("    staff reply: %s" % m.get("text"))
    return out


def to_pack(c, P, serial, log):
    """Lift and drop into the backpack, waiting out the action delay (cliloc 500119) as P480's walker does."""
    bp = c.backpack()
    for attempt in range(6):
        c.sleep(1.3)
        n = len(c.messages)
        c.send(P.lift(serial, 1))
        c.sleep(0.8)
        if any(m.get("cliloc") in (500119, 3000000 + 500119) or "must wait" in (m.get("text") or "") for m in c.messages[n:]):
            continue
        c.send(P.drop(serial, 60, 60, 0, bp))
        c.sleep(1.2)
        if c.items.get(serial, {}).get("container") == bp:
            return True
        log("  lift try %d: %s" % (attempt + 1, [m.get("text") for m in c.messages[n:]][:3]))
    return c.items.get(serial, {}).get("container") == bp


def give(adm, c, log, typename):
    """Staff: the owner goes to the character ([go <serial>) and adds an item at its feet, where a target is in range
    (run 6: from another facet the target never landed)."""
    staff(adm, log, "[go 0x%X" % c.serial, settle=2.0)
    staff(adm, log, "[add %s" % typename, settle=0.5)
    if adm.wait_target(5):
        # run 8: the client's Z after a walk is stale, so a ground target put the deed at the wrong height and the lift
        # was refused; targeting the character places the item at the server's own location for it
        adm.target_obj(c.serial)
        adm.sleep(1.5)
        return True
    log("  no target cursor for [add %s" % typename)
    return False


def move_to(adm, log, name, xyz, facet):
    staff(adm, log, '[global set Map %s where playermobile Name == "%s"' % (facet, name))
    staff(adm, log, '[global set Location (%d,%d,%d) where playermobile Name == "%s"' % (xyz[0], xyz[1], xyz[2], name))


def gate_here(c, r=1):
    p = c.pos
    for s, it in c.world_items_near(p[0], p[1], r).items():
        if it.get("graphic") in GATE_IDS:
            return s, it
    return None, None


def use_gate(c, w, log, switch, where):
    s, it = gate_here(c, 1)
    if not s:
        log("  no moongate within 1 of %s" % (c.pos[:3],))
        return False
    n = len(c.gumps)
    c.dclick(s)
    g = c.wait_gump(lambda g: any("destination" in (t or "").lower() for t in c.gump_text(g)), timeout=6, since=n)
    if not g:
        g = c.wait_gump(None, timeout=4, since=n)
    if not g:
        log("  the moongate opened no window")
        return False
    c.reply_gump(g, 1, switches=(switch,))
    c.sleep(2.5)
    w.drain()
    return True


def part_graduate(c, w, adm, log, name):
    """Run 1 found the island gate: "Finish the main tutorial lessons, then double-click Rook on the New Haven plaza and
    choose Graduate. You can leave Haven Island afterward." So the character graduates at Rook first, as a player
    must (P480's graduate: Rook's page, button 3)."""
    log("=== graduation at Rook (the way off Haven Island)")
    w.go((3632, 2585), 1, what="to Rook")
    rook = None
    for s, m in list(c.mobiles.items()):
        if "x" in m and abs(m["x"] - 3631) <= 3 and abs(m["y"] - 2584) <= 3 and "rook" in (m.get("name") or c.mobile_name(s) or "").lower():
            rook = s
    if not log.check(rook is not None, "Rook stands on the plaza"):
        return
    n, m0 = len(c.gumps), len(c.messages)
    c.dclick(rook)
    g = c.wait_gump(lambda g: any("Rook" in (t or "") for t in c.gump_text(g)), 8, since=n)
    texts = [t for t in c.gump_text(g) if t] if g else []
    log("  Rook's page: %s" % " | ".join(texts)[:500])
    log("  its buttons: %s" % ([b[2] for b in c.gump_buttons(g)] if g else None))
    if not log.check(g is not None and any("Graduate" in t for t in texts), "Rook's page offers Graduate"):
        return
    c.reply_gump(g, 3)
    c.sleep(3.0)
    w.drain()
    log.check(c.find_text(r"^System: (Graduated|You finished the tutorial)|graduat", since=m0) is not None,
              "graduated: %s" % [m.get("text") for m in c.messages[m0:]][:5])
    for g2 in c.gumps[n:]:
        if g2 is not g:
            log("  then a window: %s" % " | ".join(t for t in c.gump_text(g2) if t)[:300])
            c.reply_gump(g2, 0)


def part_gates(c, w, adm, log, name):
    log("=== gates: every public moongate, Trammel then Felucca")
    w.go(TRAM_GATES[-1][1], 0, what="to New Haven's moongate")
    log.check(gate_here(c, 0)[0] is not None, "New Haven's public moongate stands at %s (at %s)" % (TRAM_GATES[-1][1], c.pos[:3]))
    for facet_name, gates, facet_id, base in (("Trammel", TRAM_GATES, 1, 0), ("Felucca", FEL_GATES, 0, 100)):
        for i, (gname, xy) in enumerate(gates):
            if facet_name == "Trammel" and gname == "New Haven":
                continue
            # the gump lists the facet the player stands on first (PublicMoongate.cs: lists swapped to index 0)
            on = c.facet
            sw = (0 if (on == facet_id) else 100) + i
            ok = use_gate(c, w, log, sw, gname)
            arrived = ok and abs(c.pos[0] - xy[0]) <= 1 and abs(c.pos[1] - xy[1]) <= 1 and c.facet == facet_id
            log.check(arrived, "%s gate -> %s: at %s on facet %s" % (facet_name, gname, c.pos[:3], c.facet))
            if arrived:
                log.check(gate_here(c, 0)[0] is not None, "  a moongate stands at %s's arrival" % gname)
            if facet_name == "Trammel" and i == 0 and arrived:
                pass
        if facet_name == "Trammel":
            # Felucca's list is only for a player who is not Young (PublicMoongate.cs: the *Young lists)
            log("  the character renounces Young status before Felucca, as a player would")
            n = len(c.gumps)
            c.say("I want to grow up!")   # run 2: the shard's phrase (the login line says so); pinned's renounce line did nothing
            g = c.wait_gump(None, timeout=6, since=n)
            if g:
                log("  gump: %s" % " | ".join(t for t in c.gump_text(g) if t)[:300])
                btns = c.gump_buttons(g)
                ids = [b[2] for b in btns if b[2] > 0]
                log("  its buttons: %s" % (ids,))
                c.reply_gump(g, max(ids) if ids else 1)
                c.sleep(1.5)
            w.drain()
    # back to Trammel's Britain for the walks
    use_gate(c, w, log, 101, "Britain (Trammel)")
    log.check(c.facet == 1, "back on Trammel at %s" % (c.pos[:3],))


def part_towns(c, w, adm, log, name):
    log("=== towns: one walk to each of the author's new towns")
    if not gate_here(c, 2)[0]:
        move_to(adm, log, name, (1337, 1998, 15), "Trammel")
        c.sleep(2.5)
        log("  STAFF put %s beside Britain's moongate to begin (at %s)" % (name, c.pos[:3]))
    only = os.environ.get("P690_TOWNS")
    for town, bank, frm, start, back, entry in TOWNS:
        if only and town not in only.split(","):
            continue
        here = w.pos()
        if max(abs(here[0] - start[0]), abs(here[1] - start[1])) > 3:
            names = [g for g, _ in TRAM_GATES]
            gname = frm.replace(" gate", "")
            if frm.endswith("gate") and gname in names and gate_here(c, 2)[0]:
                use_gate(c, w, log, names.index(gname), frm)   # as a player: from the gate we stand by
                log.check(w.pos() == start, "by the gates to %s (at %s)" % (frm, c.pos[:3]))
            else:
                log("  not at %s and no gate here (%s)" % (frm, c.pos[:3]))
        log("--- %s: from %s %s to the bank %s" % (town, frm, w.pos(), bank))
        if entry:
            ok = w.go(entry, 1, what="to %s's gatehouse" % town)
            ok = ok and w.go_exact(bank, (entry[0] - 180, entry[1] - 130, entry[0] + 130, entry[1] + 180), what="into %s" % town)
        else:
            ok = w.go(bank, 3, what="to %s" % town)
        log.check(ok, "walked from %s to %s's bank %s (at %s)" % (frm, town, bank, c.pos[:3]))
        if ok:
            near = [m.get("name") or "?" for s, m in c.mobiles.items() if "x" in m and s != c.serial
                    and abs(m["x"] - bank[0]) <= 10 and abs(m["y"] - bank[1]) <= 10]
            log("  people within 10 of the bank: %d %s" % (len(near), near[:8]))
        if back:
            okb = w.go(back, 0, what="back to the gate at %s" % (back,))
            log.check(okb, "walked back from %s to the gate at %s (at %s)" % (town, back, c.pos[:3]))
    log("--- Valunstead: an island with no dock, gate or teleporter (P688 group 7); a walk on the island only")
    move_to(adm, log, name, (447, 466, 20), "Trammel")
    c.sleep(2.5)
    log("  STAFF put %s on Valunstead's south shore at %s (a player would sail or use magic)" % (name, c.pos[:3]))
    ok = w.go(VALUNSTEAD, 3, what="to Valunstead")
    log.check(ok, "walked on Valunstead to its bank %s (at %s)" % (VALUNSTEAD, c.pos[:3]))


def part_hatch(c, w, adm, log, name):
    log("=== Rootdeep by the hatch (New Haven's Second Bank)")
    if max(abs(c.pos[0] - HAVEN_BANK[0]), abs(c.pos[1] - HAVEN_BANK[1])) > 40:
        move_to(adm, log, name, (3634, 2586, 0), "Trammel")   # HavenSpots.Start
        c.sleep(2.0)
    w.go(BESIDE_HATCH, 0, what="into the bank, beside the hatch")
    log.check(c.world_items_near(HATCH[0], HATCH[1], 0) != {}, "the hatch is there at %s (%s)" % (
        HATCH, [hex(it.get("graphic", 0)) for it in c.world_items_near(HATCH[0], HATCH[1], 0).values()]))
    before = c.pos[:3]
    w.go(HATCH, 0, what="onto the hatch")
    c.sleep(2.0)
    down = c.pos[0] > 5000
    log.check(down, "down the hatch: from %s to %s" % (before, c.pos[:3]))
    if not down:
        # run 7: the player stands on the hatch at Z 2 (its top) and the teleporter is at Z 0; pinned Mobile.Move fires a
        # zero-height item only at the mover's own Z. Prove it: raise this one teleporter to Z 2, step off and on again.
        r = staff(adm, log, '[global get Z where teleporter X == %d Y == %d' % HATCH, settle=2.0)
        staff(adm, log, '[global set Z 2 where teleporter X == %d Y == %d' % HATCH, settle=2.0)
        log("  STAFF raised the hatch's teleporter to Z 2 (a probe of the cause, not the fix)")
        w.go(BESIDE_HATCH, 0, what="off the hatch")
        w.go(HATCH, 0, what="onto the hatch again")
        c.sleep(2.0)
        down = c.pos[0] > 5000
        log.check(down, "with the teleporter at Z 2, down the hatch: at %s" % (c.pos[:3],))
    w.drain()
    if down:
        # the Burrows are our map patch (void on the plain SoS file the walk grids read): straight north to the ladder
        n0 = c.pos[:3]
        for i in range(12):
            if c.pos[0] < 5000:
                break
            c.walk(0, 1, run=False, pause=0.3)
        c.sleep(2.0)
        log("  walked north from the Landing %s; now at %s" % (n0, c.pos[:3]))
        log.check(abs(c.pos[0] - BESIDE_HATCH[0]) <= 2 and abs(c.pos[1] - BESIDE_HATCH[1]) <= 2,
                  "up the ladder: back in the bank beside the hatch (at %s)" % (c.pos[:3],))


PIER = (3645, 2681)      # the west pier of Haven Docks (surface statics x 3645-3650, y 2658-2682 on SoS), its west edge
# run 8: between the piers "A ship cannot be created here" (pinned BaseBoat.CanFit wants water under every tile of the
# hull); shipfit.py found the nearest spot where a 7 x 13 hull is all water at Z -5: west of the pier's end
SHIP_AT = (3641, 2684)


def part_boat(c, w, adm, log, name):
    log("=== a boat from Haven's dock")
    w.go(HAVEN_DOCK, 1, what="to Haven Docks")
    w.go(PIER, 0, what="out along the west pier")
    c.sleep(1.5)
    PLANKS = (0x3EB1, 0x3EB2, 0x3E84, 0x3E85, 0x3E8A, 0x3E89, 0x3ED4, 0x3ED5)
    if [s for s, it in c.world_items_near(SHIP_AT[0], SHIP_AT[1], 7).items() if it.get("graphic") in PLANKS]:
        log("  the ship placed in the run before lies off the pier; boarding it")
        return board(c, w, log, name)
    give(adm, c, log, "SmallBoatDeed")
    log("  STAFF gave a small boat deed at the character's feet (a player buys one from a shipwright)")
    deed = None
    for s, it in c.world_items_near(c.pos[0], c.pos[1], 1).items():
        if it.get("graphic") in (0x14F1, 0x14F2):
            deed = s
    if not log.check(deed is not None, "the deed lies at the character's feet"):
        return
    log.check(to_pack(c, PK, deed, log), "the deed is in the backpack")
    n = len(c.messages)
    c.dclick(deed)
    if not c.wait_target(15):   # run 6: the cursor came about 10 s after the double-click
        log.check(False, "the deed asks where to place the ship (lines: %s)" % [m.get("text") for m in c.messages[n:]][:4])
        return
    log("  placing the ship at %s from the pier %s" % (SHIP_AT, c.pos[:3]))
    # run 9: a ground target with graphic 0 becomes pinned's LandTarget, which takes the land's Z (-15, under the sea
    # statics), so the hull found no water; a client clicking the sea sends the water static (0x179C at Z -5 here)
    c.target_xyz(SHIP_AT[0], SHIP_AT[1], -5, 0x179C)
    c.sleep(4.0)
    w.drain()
    lines = [m.get("text") for m in c.messages[n:]]
    # run 9: the bot does not mark multis by a graphic over 0x4000; the ship shows as its parts (tillerman, hold,
    # planks) as world items round the spot
    parts = c.world_items_near(SHIP_AT[0], SHIP_AT[1], 7)
    boats = list(parts)
    log.check(any("key" in (t or "") for t in lines) and boats != [], "a ship stands in the water off the pier: the keys came, and %d of its parts show (%s)" % (
        len(boats), sorted(set(hex(it.get("graphic", 0)) for it in parts.values()))[:12]))
    key = None
    for s, it in c.items.items():
        if it.get("container") == c.backpack() and it.get("graphic") in (0x100E, 0x100F, 0x1010, 0x1013):
            key = s
    log.check(key is not None, "a ship's key is in the backpack")
    if not boats:
        return
    board(c, w, log, name)


def board(c, w, log, name):
    planks = sorted([s for s, it in c.items.items() if it.get("world") and it.get("graphic") in
                     (0x3EB1, 0x3EB2, 0x3E84, 0x3E85, 0x3E8A, 0x3E89, 0x3ED4, 0x3ED5)],
                    key=lambda s: abs(c.items[s]["x"] - c.pos[0]) + abs(c.items[s]["y"] - c.pos[1]))
    log("  planks seen: %s" % [(hex(c.items[s]["graphic"]), c.items[s]["x"], c.items[s]["y"]) for s in planks])
    boarded = False
    keys = []
    bp = c.backpack()
    c.dclick(bp)   # run 11: the bot knows a container's contents once it is opened
    c.wait(lambda: bp in c.containers, 5)
    c.sleep(1.0)
    for s, it in c.items.items():
        if it.get("container") == c.backpack() and it.get("graphic") in (0x100E, 0x100F, 0x1010, 0x1013):
            keys.append(s)
    for s in planks[:1]:
        # run 10: a ship's planks are locked (pinned Plank: Locked = true); its owner unlocks one with the key.
        # run 12: the key toggles the lock, so only when the plank says so. Then: open, then step aboard.
        n0 = len(c.messages)
        c.dclick(s)          # opens it, or "That is locked."
        c.sleep(1.2)
        msgs = [m.get("text") for m in c.messages[n0:]]
        log("  the plank, double-clicked: %s" % msgs[:2])
        if keys and any("locked" in (t or "").lower() for t in msgs):
            for key in keys:   # run 13: two ships, two keys; each key fits one ship
                n = len(c.messages)
                c.dclick(key)
                if c.wait_target(6):
                    c.target_obj(s)
                    c.sleep(1.5)
                w.drain()
                said = [m.get("text") for m in c.messages[n:]]
                log("  a key on the plank: %s" % said[:3])
                if any("unlock it" in (t or "") for t in said):
                    break
            c.dclick(s)      # opens it
            c.sleep(1.2)
        c.dclick(s)          # steps aboard, onto the plank's tile
        c.sleep(1.5)
        boarded = not w.g.ok(*w.pos())
    log.check(boarded, "boarded by the plank (at %s)" % (c.pos[:3],))
    if boarded:
        start = server_loc(name)
        n = len(c.messages)
        # run 11: pinned BaseBoat.OnSpeech reads speech KEYWORD ids (0x46 back, 0x4F stop), which a client encodes
        # for the phrases in its speech table; plain text moved nothing
        c.say("raise anchor", keywords=(0x6B,))   # run 12: "Ar, the anchor is down sir!"
        c.sleep(2.0)
        c.say("back", keywords=(0x46,))      # astern: the bow points north, so south, out to the open sea
        c.sleep(6.0)
        c.say("stop", keywords=(0x4F,))
        c.sleep(2.0)
        w.drain()
        c.say("lower anchor", keywords=(0x6A,))
        c.sleep(1.5)
        end = server_loc(name)
        moved = start is not None and end is not None and (end[0], end[1]) != (start[0], start[1])
        log.check(moved, "the ship sails ('back', then 'stop'): the server has the character from %s to %s; the tillerman: %s" % (
            start, end, [m.get("text") for m in c.messages[n:] if m.get("name") not in (name,)][:4]))


BT_BESIDE, BT_HATCH, BT_LANDING = (1521, 1437), (1519, 1437), (6472, 3927)   # BlackthornFold.cs (cc-P691)


def part_blackthorn(c, w, adm, log, name):
    log("=== Blackthorn (P691): from Britain's gate to the castle keep's storeroom, down the hatch to the Fold")
    if not gate_here(c, 2)[0]:
        move_to(adm, log, name, (1337, 1998, 15), "Trammel")
        c.sleep(2.5)
        log("  STAFF put %s beside Britain's moongate to begin (at %s)" % (name, c.pos[:3]))
    # run 14: one level a tile found no path to the storeroom's floor (the keep stands on the castle's z15 floors);
    # walk to the castle near the hatch, then the last stretch with every level of a tile
    w.go(BT_BESIDE, 6, what="to Blackthorn Castle's keep")
    ok = w.pos() == BT_BESIDE or w.go_exact(BT_BESIDE, (BT_BESIDE[0] - 40, BT_BESIDE[1] - 40, BT_BESIDE[0] + 40, BT_BESIDE[1] + 40),
                                         what="into the storeroom")
    log.check(ok, "walked from Britain's gate into the keep's storeroom (at %s)" % (c.pos[:3],))
    items = c.world_items_near(BT_HATCH[0], BT_HATCH[1], 0)
    log.check(any(it.get("graphic") == 0x3E65 for it in items.values()), "the hatch is at %s" % (BT_HATCH,))
    agent = [m.get("name") for s, m in c.mobiles.items() if "x" in m and abs(m["x"] - 1521) <= 2 and abs(m["y"] - 1434) <= 2]
    log("  beside it: %s" % agent)
    before = c.pos[:3]
    w.go(BT_HATCH, 0, what="onto the hatch")
    c.sleep(2.5)
    down = abs(c.pos[0] - BT_LANDING[0]) <= 3 and abs(c.pos[1] - BT_LANDING[1]) <= 3
    log.check(down, "down Blackthorn's hatch: from %s to %s (facet %s; the Fold is map 32)" % (before, c.pos[:3], c.facet))
    w.drain()


def part_treasure(c, w, adm, log, name):
    log("=== a treasure map, read and dug")
    staff(adm, log, '[global set Blessed True where playermobile Name == "%s"' % name)
    n = len(c.messages)
    c.say("set mining 100")
    c.sleep(1.0)
    c.say("set cartography 100")
    c.sleep(1.0)
    w.drain()
    log("  test centre skills: %s" % [m.get("text") for m in c.messages[n:]][:3])
    # a level-1 map and a shovel, as a player buys or loots them (staff here: the bank's gift needs a banker trip)
    for t in ("TreasureMap 1 Trammel", "Shovel"):
        give(adm, c, log, t)
    tmap = shovel = None
    for s, it in c.world_items_near(c.pos[0], c.pos[1], 1).items():
        if it.get("graphic") in (0x14EB, 0x14EC):
            tmap = s
        if it.get("graphic") in (0x0F39, 0x0F3A):
            shovel = s
    if not log.check(tmap is not None and shovel is not None, "a treasure map and a shovel at the character's feet"):
        return
    for s in (tmap, shovel):
        to_pack(c, PK, s, log)
    log.check(all(c.items.get(s, {}).get("container") == c.backpack() for s in (tmap, shovel)), "the map and the shovel are in the backpack")
    n = len(c.messages)
    c.dclick(tmap)   # decode (level 1 needs Cartography -3)
    c.sleep(2.0)
    c.dclick(tmap)   # open: the map's bounds and its pin
    c.sleep(2.5)
    w.drain()
    det, pins = c.mapdetails.get(tmap), c.mappins.get(tmap)
    log("  map details %s, pins %s; lines %s" % (det, pins, [m.get("text") for m in c.messages[n:]][:4]))
    if not log.check(det is not None and pins, "the map opens with its bounds and a pin"):
        return
    x1, y1, x2, y2, wdt, hgt = det
    px, py = pins[-1]
    spot = (int(round(x1 + px * (x2 - x1) / float(wdt))), int(round(y1 + py * (y2 - y1) / float(hgt))))
    log("  the pin reads as %s on Trammel" % (spot,))
    # get near: by gate and walk when it is near a gate, else staff to 25 tiles off
    near = None
    for dx, dy in ((25, 0), (-25, 0), (0, 25), (0, -25), (18, 18), (-18, -18), (18, -18), (-18, 18)):
        if w.g.ok(spot[0] + dx, spot[1] + dy):
            near = (spot[0] + dx, spot[1] + dy)
            break
    if near:
        move_to(adm, log, name, (near[0], near[1], int(w.g.stand[near])), "Trammel")
        c.sleep(2.5)
        log("  STAFF put the character 25 tiles from the pin, at %s (a player walks or recalls there)" % (c.pos[:3],))
    ok = w.go(spot, 2, what="to the pin")
    # stand beside it, not on it
    if (c.pos[0], c.pos[1]) == spot:
        c.walk(2, 1)
    n = len(c.messages)
    menu = c.context_menu(tmap)
    dug = False
    if menu:
        ent = [e for e in menu["entries"] if e.get("cliloc") in (6148, 3006148)]
        log("  the map's menu: %s" % [(e.get("cliloc"), e.get("text")) for e in menu["entries"]])
        if ent:
            c.pick_context(menu, 6148)   # "Dig For Treasure" (run 14: pick_context takes the cliloc, not the entry)
            if c.wait_target(6):
                c.target_xyz(spot[0], spot[1], int(w.g.stand[spot]) if w.g.ok(*spot) else 0)
                c.sleep(12.0)
                dug = True
    w.drain()
    lines = [m.get("text") for m in c.messages[n:]]
    log("  dig lines: %s" % lines[:8])
    # run 14: the dug chest is 0xA308 here (the newer chest art), with dirt piles 0x914 round it (probe_pin.py)
    chest = [s for s, it in c.world_items_near(spot[0], spot[1], 3).items() if it.get("graphic") in (0x0E40, 0x0E41, 0x0E7C, 0x09AB, 0x0E42, 0x0E43) or 0xA300 <= it.get("graphic", 0) <= 0xA30F]
    log.check(dug and chest != [], "dug: a treasure chest at the pin (%s)" % ([hex(c.items[s]["graphic"]) for s in chest],))
    guards = [m for s, m in c.mobiles.items() if "x" in m and abs(m["x"] - spot[0]) <= 6 and abs(m["y"] - spot[1]) <= 6 and s != c.serial]
    log("  guardians near the chest: %d" % len(guards))


def part_champion(c, w, adm, log, name, altar):
    log("=== a Felucca champion: the altar at %s" % (altar,))
    near = None
    for dx, dy in ((12, 0), (-12, 0), (0, 12), (0, -12), (9, 9), (-9, -9)):
        if w.g.ok(altar[0] + dx, altar[1] + dy):
            near = (altar[0] + dx, altar[1] + dy)
            break
    move_to(adm, log, name, (near[0], near[1], int(w.g.stand[near])), "Felucca")
    c.sleep(3.0)
    log("  STAFF put the character 12 tiles from the altar on Felucca, at %s (facet %s)" % (c.pos[:3], c.facet))
    ok = w.go(altar, 3, what="to the champion's altar")
    c.sleep(2.0)
    items = c.world_items_near(altar[0], altar[1], 4)
    log("  items at the altar: %s" % sorted(set(hex(it.get("graphic", 0)) for it in items.values()))[:30])
    log.check(ok and c.facet == 0 and len(items) > 0, "walked to the champion's altar on Felucca and it is there (%d items)" % len(items))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=2596)
    ap.add_argument("--out", required=True)
    ap.add_argument("--secrets", required=True)
    ap.add_argument("--bot", default=os.path.join(CODE, "tools", "playtest-bot"))
    ap.add_argument("--tiledata", default=r"D:\UO\tool-trials\client-data-copy")
    ap.add_argument("--golem", default="Iron")
    ap.add_argument("--name", default="Iron Islander")
    ap.add_argument("--parts", default="graduate,gates,towns,hatch,boat,treasure,champion")
    ap.add_argument("--altar", default="5511,2360")
    ap.add_argument("--staff", default="owner", help="owner (the private shard's owner) or admin (the Golem's Admin)")
    a = ap.parse_args()
    sys.path.insert(0, a.bot)
    from uobot.client import Client, Cliloc, Transcript
    from uobot import packets as P
    from uobot import golemcheck as GC
    from mapbuild import uofiles
    TC = make_client_class(Client, P)
    global PK, ADM
    PK = P
    os.makedirs(a.out, exist_ok=True)
    log = Log(os.path.join(a.out, "tour-log.txt"))
    tr = Transcript(os.path.join(a.out, "transcript.txt"))
    cl = Cliloc(os.path.join(a.tiledata, "Cliloc.enu"), r"D:\UO\bot-shard\cache")
    _, items = uofiles.read_tiledata(a.tiledata)
    grid = Grid(items)
    if a.staff == "owner":
        s = json.load(open(a.secrets, encoding="utf-8"))
        adm = TC(s["owner"], s["ownerPassword"], tr, cl, label="owner", test_target=(a.host, a.port))
        s = None
        ch = adm.login()
        adm.play(0)
    else:
        # run 15: the owner's account stayed "in use" after a probe; Administrator does every staff step here
        au, ap = GC.account(a.golem, "admin")
        adm = TC(au, ap, tr, cl, label="admin", test_target=(a.host, a.port))
        ap = None
        ch = adm.login()
        adm.play(ch.index(a.golem) if a.golem in ch else 0)
    adm.sleep(2.0)
    ADM = adm
    import threading

    def _keep():   # run 5: the owner sat idle through long walks and the server dropped it; a client pings
        while not adm.closed:
            time.sleep(15)
            try:
                adm.keepalive()
            except Exception:
                break
    threading.Thread(target=_keep, daemon=True).start()
    user, pw = GC.account(a.golem, "player")
    c = TC(user, pw, tr, cl, label="player", test_target=(a.host, a.port))
    pw = None
    chars = c.login()
    if a.name not in chars:
        log("no %s on the account (%s)" % (a.name, chars))
        return 2
    c.play(chars.index(a.name))
    c.sleep(3.0)
    w = Walker(c, grid, log)
    w.drain()
    log("P690 tour: %s in the world at %s, facet %s; parts %s" % (a.name, c.pos[:3], c.facet, a.parts))
    staff(adm, log, '[global set Blessed True where playermobile Name == "%s"' % a.name)
    parts = a.parts.split(",")
    for part in parts:
        try:
            if part == "graduate":
                part_graduate(c, w, adm, log, a.name)
            elif part == "gates":
                part_gates(c, w, adm, log, a.name)
            elif part == "towns":
                part_towns(c, w, adm, log, a.name)
            elif part == "hatch":
                part_hatch(c, w, adm, log, a.name)
            elif part == "boat":
                part_boat(c, w, adm, log, a.name)
            elif part == "blackthorn":
                part_blackthorn(c, w, adm, log, a.name)
            elif part == "treasure":
                part_treasure(c, w, adm, log, a.name)
            elif part == "champion":
                part_champion(c, w, adm, log, a.name, tuple(int(v) for v in a.altar.split(",")))
        except Exception as e:
            log.check(False, "part %s raised %r" % (part, e))
        adm.keepalive()
        c.keepalive()
        if c.closed:
            log("the player's connection closed: %s" % c.closed)
            break
    log("=== %d passed, %d failed: %s" % (log.passes, len(log.fails), log.fails))
    c.close()
    adm.close()
    tr.close()
    return 1 if log.fails else 0


if __name__ == "__main__":
    sys.exit(main())
