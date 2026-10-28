"""cc-P707: isle.py's "copies" part: a party of two shares one copy, a third trainee gets another, and a copy left empty
resets after the (shortened) hold."""
import os

p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'isle.py')
s = open(p).read()


def sub(old, new):
    global s
    assert s.count(old) == 1, old[:70]
    s = s.replace(old, new)


sub('''def player_client(a, tr, cl):''', '''def party_packet(sub_, serial):
    """0xBF 0x0006: a party message (pinned IncomingExtendedCommandPackets.PartyMessage): 0x01 add (a target cursor
    follows), 0x08 accept (the leader's serial)."""
    import struct
    return struct.pack(">BHHBI", 0xBF, 10, 0x0006, sub_, serial)


def copies_report(adm, log, label):
    lines = [m["text"] for m in adm.command("[Tutorial copies", settle=3.0)]
    log("  [Tutorial copies (%s):" % label)
    for t in lines:
        log("    %s" % t)
    return lines


def copy_of(lines, name):
    """The copy line that names this occupant ("TheFold 3 ... Iron PartyA ..."), or None."""
    for t in lines:
        if name in (t or ""):
            m = re.search(r"(TheFold \\d+|map \\d+|copy \\d+)", t)
            return m.group(1) if m else t
    return None


def account_client(a, tr, cl, golem, label):
    from uobot.client import Client
    from uobot import golemcheck as GC
    user, pw = GC.account(golem, "player")
    c = Client(user, pw, tr, cl, label=label, test_target=(a.host, a.port))
    return c, c.login()


def rook_window(pl, log):
    c = pl.c
    rook = pl.mobile_at((3500, 2572), 3, "Rook")
    if not rook:
        log("  Rook is not near %s" % (pl.pos(),))
        return None
    n = len(c.gumps)
    c.sleep(1.2)
    c.dclick(rook)
    g = c.wait_gump(lambda g: any("Rook Hallowell" in (t or "") for t in c.gump_text(g)), 8, since=n)
    pl.drain()
    return g


def part_copies(a, tr, cl, grid, log, adm):
    """Two friends pick New Haven, party up on the plaza and both restart the tutorial: one copy. A third trainee picks
    the isle at creation: another copy. All log out; after the hold (clusterf.tutorial.copyHoldMinutes) the copies reset
    and a returning trainee is sent to a fresh copy at their next lesson."""
    log("=== copies: a party of two shares a copy, a third trainee gets another, an empty copy resets")
    made = []
    for golem, name in ((a.golem, "Iron PartyA"), ("Bronze", "Bronze PartyB")):
        c, chars = account_client(a, tr, cl, golem, name.split()[1])
        if name in chars:
            c.play(chars.index(name))
        else:
            c.create(name, stats=(45, 35, 10), skills=((0, 30), (17, 30), (40, 30), (43, 30)), city=1)
        pl = base.Player(c, grid, log)
        c.sleep(2.0)
        pl.drain()
        log("  %s starts at %s" % (name, c.pos[:3]))
        made.append((name, c, pl))
    (na, ca, pa), (nb, cb, pb) = made
    # the party: A adds B (a target cursor), B accepts
    ca.send(party_packet(0x01, 0))
    if log.check(ca.wait_target(6) is not None, "adding a party member gives a target cursor"):
        ca.target_obj(cb.serial)
        cb.sleep(1.5)
        cb.send(party_packet(0x08, ca.serial))
        cb.sleep(1.5)
        pa.drain(); pb.drain()
        log.check(cb.find_text(r"joined the party|You have been added to the party", since=0) is not None
                  or ca.find_text(r"joined the party", since=0) is not None, "Bronze PartyB joined Iron PartyA's party")
    for name, c, pl in made:
        g = rook_window(pl, log)
        texts = [t for t in c.gump_text(g) if t] if g else []
        log("  %s: Rook's window: %s" % (name, texts))
        if log.check(g is not None and any("Restart the tutorial" in t for t in texts), "%s: Rook offers to restart the tutorial" % name):
            c.reply_gump(g, 2)
            c.sleep(3.0)
            pl.drain()
            log.check(near(pl.pos(), BEACH, 4), "%s is on an isle beach (%s)" % (name, pl.pos()))
    lines = copies_report(adm, log, "after the party went")
    ka, kb = copy_of(lines, na), copy_of(lines, nb)
    log.check(ka is not None and ka == kb, "the party shares one copy (%s, %s)" % (ka, kb))
    # the third trainee
    cc, chars = account_client(a, tr, cl, "Copper", "Copper")
    nc = "Copper Third"
    if nc in chars:
        cc.play(chars.index(nc))
    else:
        cc.create(nc, stats=(45, 35, 10), skills=((0, 30), (17, 30), (40, 30), (43, 30)), city=0)
    pc_ = base.Player(cc, grid, log)
    cc.sleep(3.0)
    pc_.drain()
    lines = copies_report(adm, log, "after the third trainee")
    kc = copy_of(lines, nc)
    log.check(kc is not None and kc != ka, "the third trainee is on another copy (%s, the party's %s)" % (kc, ka))
    # everyone leaves; the hold runs out
    for c in (ca, cb, cc):
        c.close()
    hold = a.hold_minutes
    log("  all three logged out; waiting %d minutes (the hold is %d) and the minute tick" % (hold + 2, hold))
    time.sleep((hold + 2) * 60)
    lines = copies_report(adm, log, "after the hold")
    log.check(copy_of(lines, na) is None and copy_of(lines, nc) is None, "the copies were freed after the hold")
    ca, chars = account_client(a, tr, cl, a.golem, "PartyA")
    ca.play(chars.index(na))
    pa = base.Player(ca, grid, log)
    ca.sleep(3.0)
    pa.drain()
    log("  %s logs back in at %s" % (na, ca.pos[:3]))
    log.check(near(pa.pos(), BEACH, 4) or near(pa.pos(), TAMSIN, 4), "%s is on a fresh copy at the first lesson (%s)" % (na, pa.pos()))
    copies_report(adm, log, "after the return")
    ca.close()


def player_client(a, tr, cl):''')
sub('''    ap.add_argument("--from", dest="first", default="core.movement", help="the lesson to start from (resuming)")''',
    '''    ap.add_argument("--from", dest="first", default="core.movement", help="the lesson to start from (resuming)")
    ap.add_argument("--hold-minutes", type=int, default=2, help="the world's clusterf.tutorial.copyHoldMinutes")''')
sub('''    if adm:
        adm.close()
    log("=== %d failed check(s): %s" % (len(log.fails), log.fails))''', '''    if "copies" in parts and adm:
        part_copies(a, tr, cl, grid, log, adm)

    if adm:
        adm.close()
    log("=== %d failed check(s): %s" % (len(log.fails), log.fails))''')
sub('''    if "seed" in parts:
        user, pw = GC.account(a.golem, "admin")''', '''    if "seed" in parts or "copies" in parts:
        user, pw = GC.account(a.golem, "admin")''')
sub('''        log("=== seed (the Admin)")
        for cmd in''', '''    if "seed" in parts:
        log("=== seed (the Admin)")
        for cmd in''')
open(p, 'w').write(s)
print('ok')
