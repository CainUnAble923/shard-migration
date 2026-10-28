"""cc-P728: P727's isle.py taught P728's isle: the trainee lies on the sand until it moves (a step gets it up), no window
comes while it lies, the cloak is taken from a chest that appears, the farm's fight starts with the pitchfork and war
mode before the pet's commands, and the cleared rows give the next step (the lesson window's "Now:" line, the arrow to
Wren), with Wren never saying "0 more". Usage: python -P make_isle_bot.py <P727 isle.py> <out isle.py>."""
import sys

src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8", newline="").read()


def sub(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:120])
    s = s.replace(a, b)


sub('"""cc-P727: P722\'s isle.py with New Haven on main\'s land again (P678).\n',
    '"""cc-P728: P727\'s isle.py taught P728\'s isle: the first arrival lies on the sand until it moves (the bot waits for\n'
    '"Move to get up.", checks that no window came while it lay, and steps to get up), the cloak comes in a chest that\n'
    'appears (opened, the cloak dragged to the paperdoll, the chest gone), Wren\'s fight starts with the pitchfork and war\n'
    'mode before the pet\'s commands, and the cleared rows say the next step in the lesson window with the arrow on Wren.\n'
    '\n'
    'cc-P727: P722\'s isle.py with New Haven on main\'s land again (P678).\n')

sub("TABLE = (6664, 3990)                       # cc-P718: TutorialCorePlacement.ClothesTable\n",
    "TABLE = (6664, 3990)                       # cc-P718: TutorialCorePlacement.ClothesTable\n"
    "CHEST_IDS = (0x0E43, 0x0E42)               # cc-P728: TutorialCloakChest, a wooden chest\n"
    "CLEARED = r\"The cabbage rows are clear\"     # cc-P728: TutorialFarm.EchoPestsLine\n")

# -- the cloak, from its chest
sub('''def t_paperdoll(pl, log):
    c = pl.c
    walk_to(pl, log, TABLE, 2, "the clothes table")
    cloak = c.wait(lambda: pl.item_at(TABLE, 0x1515, 0) or pl.item_at(TABLE, 0x1516, 0), 5)
    if not log.check(cloak is not None, "the cloak of the Wakening Isle lies on the clothes table"):
        return
    if pl.lift(cloak):
        c.send(P.equip(cloak, 0x14, c.serial))
        log("  -> dragged the cloak from the table onto the paperdoll")
''', '''def t_paperdoll(pl, log):
    """cc-P728: a chest appears by the clothes rack; open it, drag the cloak onto the paperdoll; the chest goes."""
    c = pl.c
    walk_to(pl, log, TABLE, 2, "the clothes table")
    chest = c.wait(lambda: next((s_ for s_, it in list(c.items.items()) if it.get("world") and it.get("graphic") in CHEST_IDS
                                 and it.get("hue") == SUPPLY and near((it["x"], it["y"]), TABLE, 2)), None), 6)
    if not log.check(chest is not None, "a chest appears by the clothes rack (at %s)" % ((c.items[chest]["x"], c.items[chest]["y"]) if chest else None,)):
        return
    c.sleep(0.6)
    c.dclick(chest)
    cloak = c.wait(lambda: next((s_ for s_, it in list(c.items.items()) if it.get("container") == chest
                                 and it.get("graphic") in (0x1515, 0x1516)), None), 6)
    if not log.check(cloak is not None, "double-clicking the chest shows the cloak of the Wakening Isle inside"):
        return
    if pl.lift(cloak):
        c.send(P.equip(cloak, 0x14, c.serial))
        log("  -> dragged the cloak from the chest onto the paperdoll")
    gone = c.wait(lambda: chest not in c.items or not c.items[chest].get("world"), 6)
    log.check(gone is not None, "the chest vanishes once the cloak is taken")
''')

# -- the farm's fight: pitchfork, war mode, then the commands
sub('''def pet_commands(pl, log, since):
    """cc-P718: Wren's pet commands: follow, then guard (speech; the pet's menu sets the same orders)."""
    c = pl.c
    c.pet_command("all follow me")
    log.check(pl.wait_text(r"Your pet follows you", 5, since=since) is not None, "'all follow me' counts")
    c.sleep(1.0)
    c.pet_command("all guard me")
    log.check(pl.wait_text(r"Your pet guards you", 5, since=since) is not None, "'all guard me' counts")
    # cc-P721: hold the pitchfork Wren put in the pack, then war mode (Tab sends the same packet).
    c.sleep(1.0)
    pl.open_pack()''', '''def pet_commands(pl, log, since):
    """cc-P728: Wren's fight in order: hold the pitchfork, war mode, then the pet's commands (follow, then guard)."""
    c = pl.c
    log.check(pl.wait_text(r"Before the pests, a weapon", 5, since=since) is not None, "Wren hands the pitchfork first")
    # cc-P721: hold the pitchfork Wren put in the pack, then war mode (Tab sends the same packet).
    c.sleep(1.0)
    pl.open_pack()''')

sub('''    c.send(P.war_mode(True))
    log("  -> war mode on")
    log.check(pl.wait_text(r"You are in war mode", 5, since=since) is not None, "war mode counts, and Wren opens the gate")
''', '''    c.send(P.war_mode(True))
    log("  -> war mode on")
    log.check(pl.wait_text(r"You are in war mode", 5, since=since) is not None, "war mode counts, then the pet's commands")
    # cc-P718: the pet commands (speech; the pet's menu sets the same orders), now after the weapon (cc-P728)
    c.sleep(1.0)
    c.pet_command("all follow me")
    log.check(pl.wait_text(r"Your pet follows you", 5, since=since) is not None, "'all follow me' counts")
    c.sleep(1.0)
    c.pet_command("all guard me")
    log.check(pl.wait_text(r"Your pet guards you\\. I opened the field gate", 5, since=since) is not None,
              "'all guard me' counts, and Wren opens the gate")
''')

sub('''        elif "obeys spoken commands" in said:
            pet_commands(pl, log, m0)''', '''        elif "0 more" in said:
            log.check(False, "Wren never says '0 more' (she said %r)" % said)
            return
        elif "Before the pests, a weapon" in said or "obeys spoken commands" in said or "You hold the pitchfork" in said:
            pet_commands(pl, log, m0)''')

# the cleared rows
sub('''    while time.time() - t0 < 240 and not c.find_text(r"You cleared the farm pests", since=0):''',
    '''    while time.time() - t0 < 240 and not c.find_text(CLEARED, since=0):''')
sub('''        c.wait(lambda: p not in c.mobiles or c.find_text(r"Farm pests defeated|You cleared", since=len(c.messages) - 1), 25)''',
    '''        c.wait(lambda: p not in c.mobiles or c.find_text(r"Farm pests defeated|" + CLEARED, since=len(c.messages) - 1), 25)''')
sub('''    log.check(c.find_text(r"You cleared the farm pests", since=0) is not None,
              "the pests are cleared (%.0f s, %d targets)" % (time.time() - t0, targets))
''', '''    log.check(c.find_text(CLEARED, since=0) is not None,
              "the pests are cleared (%.0f s, %d targets)" % (time.time() - t0, targets))
    # cc-P728 item 6: the next step at once, in the lesson window and with the arrow on Wren
    c.sleep(1.0)
    pl.drain()
    log.check(any("Now: The cabbage rows are clear" in (t or "") for g in c.gumps for t in c.gump_text(g)),
              "the lesson window says: Now: the cabbage rows are clear, go back to Wren")
    log.check(any(x["active"] and near((x["x"], x["y"]), WREN, 1) for x in c.arrows), "the arrow points at Wren")
''')

# -- the wake-up: down until a move
sub('''        pl = base.Player(pc, grid, log)
        pc.sleep(7.0)  # cc-P721: the first arrival lies on the sand for 5 s
        log.check(pc.find_text(r"You wake on cold sand", since=0) is not None, "the System says: you wake on cold sand")
        pl.drain()''', '''        pl = base.Player(pc, grid, log)
        g0 = len(pc.gumps)
        log.check(pc.find_text(r"You wake on cold sand", since=0, timeout=8) is not None, "the System says: you wake on cold sand")
        # cc-P728: down until the first move; "Move to get up." after 8 s; no window while lying
        log.check(pc.find_text(r"Move to get up\\.", since=0, timeout=14) is not None, "the System says: move to get up")
        log.check(pc.find_text(r"You wake on a quiet shore", since=0) is None, "still lying: the first lesson's lines wait")
        log.check(len(pc.gumps) == g0, "no window opened while lying (%d)" % (len(pc.gumps) - g0))
        took = pc.walk(2, 1)
        log.check(took == 0, "the first step is spent getting up (refused: %d)" % took)
        pc.sleep(3.0)
        pl.drain()''')

open(dst, "w", encoding="utf-8", newline="").write(s)
print("ok")
