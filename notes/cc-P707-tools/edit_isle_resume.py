"""cc-P707: isle.py resumes a character mid-route (--from <lesson key>) and the farm follows Wren's own answers."""
import os

p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'isle.py')
s = open(p).read()


def sub(old, new):
    global s
    assert s.count(old) == 1, old[:70]
    s = s.replace(old, new)


start = s.index('def t_farm(pl, log):')
end = s.index('def t_death(pl, log):')
s = s[:start] + '''def find_pet(pl):
    c = pl.c
    for s_, m in list(c.mobiles.items()):
        if s_ != c.serial and "x" in m and m.get("body") in (0xD9, 0xC9) and near((m["x"], m["y"]), pl.pos(), 12):
            return s_
    return None


def farm_pests(pl, log):
    c = pl.c
    walk_to(pl, log, PESTS, 3, "the cabbage rows")
    t0 = time.time()
    targets = 0
    while time.time() - t0 < 240 and not c.find_text(r"You cleared the farm pests", since=0):
        ps = pests_near(pl)
        if not ps:
            c.sleep(3.0)
            pl.drain()
            continue
        p = min(ps, key=lambda s_: abs(c.mobiles[s_]["x"] - pl.pos()[0]) + abs(c.mobiles[s_]["y"] - pl.pos()[1]))
        m = c.mobiles[p]
        pl.go((m["x"], m["y"]), 2)
        if not c.pet_command("all kill", settle=1.0):
            log("  'all kill' gave no target cursor")
            c.sleep(2.0)
            continue
        c.target_obj(p)
        targets += 1
        log("  -> all kill on 0x%08X at %d,%d" % (p, m["x"], m["y"]))
        c.wait(lambda: p not in c.mobiles or c.find_text(r"Farm pests defeated|You cleared", since=len(c.messages) - 1), 25)
        pl.drain()
    log.check(c.find_text(r"You cleared the farm pests", since=0) is not None,
              "the pests are cleared (%.0f s, %d targets)" % (time.time() - t0, targets))


def farm_heal(pl, log, scratched):
    c = pl.c
    pl.open_pack()
    band = c.wait(lambda: pl.in_pack(0x0E21), 5)
    if not log.check(band is not None, "bandages are in the backpack"):
        return
    c.send(P.status_request(c.serial, 4))
    pet = find_pet(pl)
    if pet:
        c.send(P.status_request(pet, 4))
    c.sleep(1.0)
    me, pm = c.mobiles.get(c.serial, {}), c.mobiles.get(pet, {}) if pet else {}
    log("  hits: you %s/%s, pet %s/%s" % (me.get("hits"), me.get("hitsMax"), pm.get("hits"), pm.get("hitsMax")))
    order = [c.serial] if scratched else ([pet] if pet else []) + [c.serial]
    for who in order:
        n = len(c.messages)
        c.sleep(1.2)
        c.dclick(band)
        if not c.wait_target(5):
            log("  the bandage gave no target cursor")
            continue
        c.target_obj(who)
        log("  -> bandage on %s" % ("the pet" if who != c.serial else "yourself"))
        if c.find_text(r"Your bandage restored health", since=n, timeout=14):
            break
        pl.drain()
    pl.drain()
    log.check(c.find_text(r"Your bandage restored health", since=0) is not None, "a bandage really healed (the farm's heal step)")


def t_farm(pl, log):
    """Wren's three steps, by her own answers: the pet window, the pests line, the bandages line."""
    c = pl.c
    walk_to(pl, log, WREN, 3, "Wren at the farm gate")
    wren = pl.mobile_at(WREN, 2, "Wren")
    if not log.check(wren is not None, "Wren the Farmhand stands at %s" % (WREN,)):
        return
    for _ in range(4):
        if c.find_text(r"You finished the farm lessons|finished the farm", since=0):
            return
        pl.go(WREN, 3)
        n, m0 = len(c.gumps), len(c.messages)
        c.sleep(1.2)
        c.dclick(wren)
        c.wait(lambda: len(c.gumps) > n or any((m.get("name") or "").startswith("Wren") for m in c.messages[m0:]), 6)
        c.sleep(0.8)
        pl.drain()
        g = next((g for g in c.gumps[n:] if any("Choose your farm pet" in (t or "") for t in c.gump_text(g))), None)
        said = " ".join(m["text"] or "" for m in c.messages[m0:] if (m.get("name") or "").startswith("Wren"))
        if g is not None:
            log("  pet window: %s" % [t for t in c.gump_text(g) if t])
            c.reply_gump(g, 1)
            c.sleep(2.0)
            pl.drain()
            log.check(pl.wait_text(r"This pet is yours to keep", 4, since=m0) is not None, "the System says the pet is yours")
            c.pet_command("all follow me")
        elif "all kill" in said:
            log.check(True, "Wren explains 'all kill'")
            farm_pests(pl, log)
        elif "bandage" in said.lower():
            scratched = "nipped" in said
            log.check(True, "Wren hands bandages%s" % (" and a scratch to treat" if scratched else ""))
            farm_heal(pl, log, scratched)
        else:
            log("  Wren said: %r" % said)
            return


''' + s[end:]

sub('''def play_isle(pl, log, times):
    c = pl.c
    by_title = {v: k for k, v in TITLES.items()}
    walk_to(pl, log, TAMSIN, 2, "Tamsin")
    since = len(c.gumps)
    if not guide_station(pl, log, "core.movement"):
        return False''', '''def play_isle(pl, log, times, first="core.movement"):
    c = pl.c
    by_title = {v: k for k, v in TITLES.items()}
    walk_to(pl, log, TAMSIN, 2, "Tamsin")
    since = len(c.gumps)
    if not guide_station(pl, log, first):
        return False''')
sub('''    ap.add_argument("--parts", default="seed,isle,skip")''', '''    ap.add_argument("--parts", default="seed,isle,skip")
    ap.add_argument("--from", dest="first", default="core.movement", help="the lesson to start from (resuming)")''')
sub('''        ok = play_isle(pl, log, times)''', '''        ok = play_isle(pl, log, times, a.first)''')
sub('''        log.check(near(pl.pos(), BEACH, 3), "the character wakes on the beach %s (at %s)" % (BEACH, pl.pos()))
        log.check(pl.wait_text(r"You wake on a quiet shore", 3, since=0) is not None, "the System says: you wake on a quiet shore")
        log.check(any(x["active"] and near((x["x"], x["y"]), TAMSIN, 1) for x in pc.arrows), "a quest arrow points to Tamsin")''',
    '''        if a.first == "core.movement":
            log.check(near(pl.pos(), BEACH, 3), "the character wakes on the beach %s (at %s)" % (BEACH, pl.pos()))
            log.check(pl.wait_text(r"You wake on a quiet shore", 3, since=0) is not None, "the System says: you wake on a quiet shore")
            log.check(any(x["active"] and near((x["x"], x["y"]), TAMSIN, 1) for x in pc.arrows), "a quest arrow points to Tamsin")''')
open(p, 'w').write(s)
print('ok')
