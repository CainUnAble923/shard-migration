"""cc-P690: tour.py run 13: measure the sail by the server's location (the bot does not read a ship's move packet,
0xF6) and try each ship's key in the pack on a locked plank. python -P edit_tour_sail.py"""
import os

p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tour.py")
s = open(p, encoding="utf-8").read()


def rep(a, b):
    global s
    assert s.count(a) == 1, a[:80]
    s = s.replace(a, b)


rep('''PK = None   # uobot.packets, set in main''', r'''PK = None   # uobot.packets, set in main
ADM = None  # the owner's client, set in main


def server_loc(name):
    """The server's own location for a character (staff [global get), for when the client's is stale: the bot does
    not read a ship's move packet (0xF6), so its position stays where it boarded (run 13)."""
    out = ADM.command('[global get Location where playermobile Name == "%s"' % name, settle=2.0)
    for m in out:
        r = re.search(r"Location = \((-?\d+), (-?\d+), (-?\d+)\)", m.get("text") or "")
        if r:
            return tuple(int(v) for v in r.groups())
    return None''')
rep('''        start = c.pos[:3]
        n = len(c.messages)
        # run 11''', '''        start = server_loc(name)
        n = len(c.messages)
        # run 11''')
rep('''        moved = (c.pos[0], c.pos[1]) != (start[0], start[1])
        log.check(moved, "the ship sails ('back', then 'stop'): from %s to %s; the tillerman: %s" % (
            start, c.pos[:3],''', '''        end = server_loc(name)
        moved = start is not None and end is not None and (end[0], end[1]) != (start[0], start[1])
        log.check(moved, "the ship sails ('back', then 'stop'): the server has the character from %s to %s; the tillerman: %s" % (
            start, end,''')
rep('''    global PK
    PK = P''', '''    global PK, ADM
    PK = P''')
rep('''    adm.play(0)
    adm.sleep(2.0)
    import threading''', '''    adm.play(0)
    adm.sleep(2.0)
    ADM = adm
    import threading''')
# every key in the pack, until one unlocks the plank
rep('''    key = None
    bp = c.backpack()''', '''    keys = []
    bp = c.backpack()''')
rep('''        if it.get("container") == c.backpack() and it.get("graphic") in (0x100E, 0x100F, 0x1010, 0x1013):
            key = s
    for s in planks[:1]:''', '''        if it.get("container") == c.backpack() and it.get("graphic") in (0x100E, 0x100F, 0x1010, 0x1013):
            keys.append(s)
    for s in planks[:1]:''')
rep('''        if key and any("locked" in (t or "").lower() for t in msgs):
            n = len(c.messages)
            c.dclick(key)
            if c.wait_target(6):
                c.target_obj(s)
                c.sleep(1.5)
            w.drain()
            log("  the key on the plank: %s" % [m.get("text") for m in c.messages[n:]][:3])
            c.dclick(s)      # opens it''', '''        if keys and any("locked" in (t or "").lower() for t in msgs):
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
            c.dclick(s)      # opens it''')
open(p, "w", encoding="utf-8").write(s)
print("ok")
