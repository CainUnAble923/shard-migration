"""cc-P726: P728's isle.py taught P726's isle: Wren's farm is the pitchfork, war mode and the pests (the trainee fights
them itself: no pet yet), then the pet as thanks and its commands; bandaging is its own lesson after the farm, at Pip on
his bench inside the farmhouse. Usage: python -P make_isle_bot.py <P728 isle.py> <out isle.py>."""
import sys

src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8", newline="").read()


def sub(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:120])
    s = s.replace(a, b)


def between(start, end, new):
    """Replaces the text from start up to (not including) end."""
    global s
    i = s.index(start)
    j = s.index(end, i)
    s = s[:i] + new + s[j:]


sub('"""cc-P728: P727\'s isle.py taught P728\'s isle:',
    '"""cc-P726: P728\'s isle.py taught P726\'s isle: the farm is the pitchfork, war mode and the pests (fought by the trainee\n'
    'alone), then the pet as Wren\'s thanks and its commands; bandaging is its own lesson after the farm, at Pip on his bench\n'
    'in the farmhouse.\n\ncc-P728: P727\'s isle.py taught P728\'s isle:')

sub('''CORE = ["core.movement", "core.backpack", "core.paperdoll", "core.chat", "core.farm", "core.death", "core.banking",''',
    '''CORE = ["core.movement", "core.backpack", "core.paperdoll", "core.chat", "core.farm", "core.healing", "core.death", "core.banking",''')
sub('''          "core.farm": "The farm: your pet, pests and bandages", "core.death": "Death and resurrection",''',
    '''          "core.farm": "The farm: pests, then your pet", "core.healing": "Healing: bandage Pip",
          "core.death": "Death and resurrection",''')
sub('''CLEARED = r"The cabbage rows are clear"     # cc-P728: TutorialFarm.EchoPestsLine
''', '''CLEARED = r"The cabbage rows are clear"     # cc-P728: TutorialFarm.EchoPestsLine
PIP, BESIDE_PIP = (6692, 3975), (6691, 3976)  # cc-P726: TutorialFarm.PipBench, and the floor beside his bench
''')

# the pests: fought by the trainee alone
between("def farm_pests(pl, log):", "    log.check(c.find_text(CLEARED, since=0) is not None,", '''def farm_pests(pl, log):
    """cc-P726: the trainee fights the pests itself with the pitchfork, in war mode (no pet yet)."""
    c = pl.c
    walk_to(pl, log, BELOW_WREN, 0, "the field gate")
    open_field_gate(pl, log)
    walk_to(pl, log, PESTS, 3, "the cabbage rows")
    t0 = time.time()
    targets = 0
    while time.time() - t0 < 240 and not c.find_text(CLEARED, since=0):
        ps = pests_near(pl)
        if not ps:
            c.sleep(3.0)
            pl.drain()
            continue
        p = min(ps, key=lambda s_: abs(c.mobiles[s_]["x"] - pl.pos()[0]) + abs(c.mobiles[s_]["y"] - pl.pos()[1]))
        m = c.mobiles[p]
        pl.go((m["x"], m["y"]), 1)
        c.send(P.war_mode(True))
        c.send(P.attack(p))  # a double-click in war mode
        targets += 1
        log("  -> attack 0x%08X at %d,%d" % (p, m["x"], m["y"]))
        t1 = time.time()
        while time.time() - t1 < 25 and p in c.mobiles and not c.find_text(CLEARED, since=0):
            if p in c.mobiles and "x" in c.mobiles[p] and not near((c.mobiles[p]["x"], c.mobiles[p]["y"]), pl.pos(), 1):
                pl.go((c.mobiles[p]["x"], c.mobiles[p]["y"]), 1)
                c.send(P.attack(p))
            c.sleep(1.0)
            pl.drain()
''')

# the fight, then the pet, then its commands
between("def pet_commands(pl, log, since):", "def t_farm(pl, log):", '''def fight(pl, log, since):
    """cc-P726: Wren's fight: hold the pitchfork, war mode (she opens the gate), then the pests."""
    c = pl.c
    log.check(pl.wait_text(r"Before the pests, a weapon", 5, since=since) is not None, "Wren hands the pitchfork first")
    c.sleep(1.0)
    pl.open_pack()
    fork = c.wait(lambda: pl.in_pack(0x0E87) or pl.in_pack(0x0E88), 5)
    # a new character already holds its starting weapon: into the backpack first, as Wren says
    for s_, it in list(c.items.items()):
        if it.get("parent") == c.serial and it.get("layer") in (0x01, 0x02) and s_ != fork and pl.lift(s_):
            c.send(P.drop(s_, 60, 60, 0, c.backpack()))
            log("  -> put the held 0x%04X into the backpack" % it.get("graphic", 0))
            c.sleep(0.8)
    if log.check(fork is not None, "Wren's pitchfork is in the backpack") and pl.lift(fork):
        c.send(P.equip(fork, 0x02, c.serial))
        log("  -> dragged the pitchfork onto the paperdoll's hand")
    log.check(pl.wait_text(r"You hold the pitchfork", 5, since=since) is not None, "holding the pitchfork counts")
    c.sleep(0.8)
    c.send(P.war_mode(True))
    log("  -> war mode on")
    log.check(pl.wait_text(r"You are in war mode.*I opened the field gate", 5, since=since) is not None,
              "war mode counts, and Wren opens the gate")
    log.check(c.find_text(r"Choose your farm pet|This pet is yours", since=0) is None, "no pet before the pests")
    farm_pests(pl, log)


def pet_commands(pl, log, since):
    """cc-P718: the pet's commands, follow then guard (speech; the pet's menu sets the same orders), after the pet (cc-P726)."""
    c = pl.c
    log.check(pl.wait_text(r"Pet Info", 4, since=since) is not None, "the System says how to see the pet's Pet Info")
    c.sleep(1.0)
    c.pet_command("all follow me")
    log.check(pl.wait_text(r"Your pet follows you", 5, since=since) is not None, "'all follow me' counts")
    c.sleep(1.0)
    c.pet_command("all guard me")
    log.check(pl.wait_text(r"Your pet guards you", 5, since=since) is not None, "'all guard me' counts")
    log.check(pl.wait_text(r"Lesson finished: The farm", 5, since=since) is not None, "the farm lesson is finished")


''')

# Wren's answers
sub('''        if c.find_text(r"You finished the farm lessons|finished the farm", since=0):''',
    '''        if c.find_text(r"Lesson finished: The farm", since=0):''')
sub('''            log.check(pl.wait_text(r"This pet is yours to keep", 4, since=m0) is not None, "the System says the pet is yours")
            pet_commands(pl, log, m0)''',
    '''            log.check(c.find_text(CLEARED, since=0) is not None, "the pet window comes after the cleared rows")
            log.check(pl.wait_text(r"This pet is yours to keep", 4, since=m0) is not None, "the System says the pet is yours")
            pet_commands(pl, log, m0)''')
sub('''        elif "Before the pests, a weapon" in said or "obeys spoken commands" in said or "You hold the pitchfork" in said:
            pet_commands(pl, log, m0)
        elif "all kill" in said:
            log.check(True, "Wren explains 'all kill'")
            farm_pests(pl, log)
        elif "bandage" in said.lower():
            scratched = "nipped" in said
            log.check(True, "Wren hands bandages%s" % (" and a scratch to treat" if scratched else ""))
            farm_heal(pl, log, scratched)''',
    '''        elif "Before the pests, a weapon" in said or "You hold the pitchfork" in said:
            fight(pl, log, m0)
        elif "obeys spoken commands" in said:
            pet_commands(pl, log, m0)
        elif "cabbage rows" in said:
            farm_pests(pl, log)''')

# the healing lesson: Pip on his bench
sub('''    pip = pl.mobile_at((6715, 3981), 0)  # cc-P721: the heal step's patient, who stays hurt (Pip, by his spot)
    if pip:
        walk_to(pl, log, (6716, 3981), 1, "Pip, the hurt farm boy")
        who = pip''',
    '''    pip = pl.mobile_at(PIP, 0)  # cc-P726: on his bench inside the farmhouse
    if pip:
        into_farmhouse(pl, log)
        who = pip''')
sub('''def t_death(pl, log):''', '''def into_farmhouse(pl, log):
    """cc-P726: the walk grid has no floor inside the farmhouse (its floor and steps are server items at Z 7), so walk to
    the steps, open the door, and step in as a player does: north up the steps, through the door, then beside the bench."""
    c = pl.c
    if in_field(pl.pos()):
        # out through the field gate first, step by step (an open gate leaves the walk grid no way through)
        pl.go(INSIDE_GATE, 0)
        open_field_gate(pl, log, INSIDE_GATE)
        for d in (2, 2):
            pl.step(d)
            c.sleep(0.3)
        pl.drain()
    walk_to(pl, log, (6690, 3980), 0, "the farmhouse steps")
    door = pl.door_at((6690, 3978))
    if door:
        c.dclick(door)
        log("  -> opened the farmhouse door 0x%08X" % door)
        c.sleep(1.0)
    for d in (0, 0, 0, 1):  # north, north, north, north-east
        pl.step(d)
        c.sleep(0.3)
    pl.drain()
    log.check(near(pl.pos(), BESIDE_PIP, 1), "walked into the farmhouse, beside Pip's bench (at %s)" % (pl.pos(),))


def t_healing(pl, log):
    """cc-P726: the healing lesson: its bandages, Pip on his bench, a bandage that heals him."""
    c = pl.c
    log.check(c.find_text(r"Pip, the farm boy, cut his arm on the fence and sits hurt on the bench", since=0) is not None,
              "the lesson hands bandages and points at Pip in the farmhouse")
    log.check(pl.mobile_at(PIP, 0) is not None, "Pip sits on his bench at %s" % (PIP,))
    farm_heal(pl, log, False)
    # and back out the same way (the walk grid has no floor in there): south-west, through the door, down the steps
    pl.step(5)
    c.sleep(0.3)
    door = pl.door_at((6690, 3978))
    if door:
        c.dclick(door)
        c.sleep(1.0)
    for d in (4, 4, 4):
        pl.step(d)
        c.sleep(0.3)
    pl.drain()
    log.check(near(pl.pos(), (6690, 3980), 1), "walked back out of the farmhouse (at %s)" % (pl.pos(),))


def t_death(pl, log):''')
sub('''          "core.chat": (t_chat, 10), "core.farm": (t_farm, 20), "core.death": (t_death, 15),''',
    '''          "core.chat": (t_chat, 10), "core.farm": (t_farm, 20), "core.healing": (t_healing, 15), "core.death": (t_death, 15),''')

open(dst, "w", encoding="utf-8", newline="").write(s)
print("ok")
