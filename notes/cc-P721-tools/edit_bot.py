p = r"D:\UO\golems\Iron\shard-migration\notes\cc-P721-tools\isle.py"
s = open(p, encoding="utf-8").read()


def rep(old, new):
    global s
    assert s.count(old) == 1, old[:80]
    s = s.replace(old, new)


rep('''"""cc-P718: P707's isle.py, changed for P718's lessons''', '''"""cc-P721: P718's isle.py, changed for P721's lessons: after the pet commands the bot holds Wren's pitchfork, switches
to war mode and attacks a pest itself before "all kill"; the heal step bandages Pip, the hurt farm boy; the first arrival
lies on the sand for a few seconds before the arrow to Tamsin.

cc-P718: P707's isle.py, changed for P718's lessons''')
rep('''    log.check(pl.wait_text(r"Your pet guards you", 5, since=since) is not None, "'all guard me' counts, and Wren opens the gate")''',
    '''    log.check(pl.wait_text(r"Your pet guards you", 5, since=since) is not None, "'all guard me' counts")
    # cc-P721: hold the pitchfork Wren put in the pack, then war mode (Tab sends the same packet).
    c.sleep(1.0)
    pl.open_pack()
    fork = c.wait(lambda: pl.in_pack(0x0E87) or pl.in_pack(0x0E88), 5)
    if log.check(fork is not None, "Wren's pitchfork is in the backpack") and pl.lift(fork):
        c.send(P.equip(fork, 0x02, c.serial))
        log("  -> dragged the pitchfork onto the paperdoll's hand")
    log.check(pl.wait_text(r"You hold the pitchfork", 5, since=since) is not None, "holding the pitchfork counts")
    c.sleep(0.8)
    c.send(P.war_mode(True))
    log("  -> war mode on")
    log.check(pl.wait_text(r"You are in war mode", 5, since=since) is not None, "war mode counts, and Wren opens the gate")''')
rep('''        if not c.pet_command("all kill", settle=1.0):''', '''        if targets == 0:
            c.send(P.war_mode(True))
            c.send(P.attack(p))  # cc-P721: the trainee attacks one itself (a double-click in war mode)
            log("  -> attack 0x%08X" % p)
            c.sleep(2.0)
        if not c.pet_command("all kill", settle=1.0):''')
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
