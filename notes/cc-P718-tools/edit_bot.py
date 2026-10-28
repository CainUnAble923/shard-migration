p = r"D:\UO\golems\Iron\shard-migration\notes\cc-P718-tools\isle.py"
s = open(p, encoding="utf-8").read()


def rep(old, new):
    global s
    assert s.count(old) == 1, old[:70]
    s = s.replace(old, new)


rep('''"""cc-P707: the Wakening Isle play-through''', '''"""cc-P718: P707's isle.py, changed for P718's lessons: the backpack lesson opens the character window first (a
double-click on yourself), the cloak is taken from the clothes table, Wren's pet commands ("all follow me", then "all
guard me") come before the pests, and the field gate is opened if it has swung shut. Everything else is P707's.

cc-P707: the Wakening Isle play-through''')
rep('''sys.path.insert(0, os.path.join(HERE, "..", "cc-P480-tools"))''', '''sys.path.insert(0, os.path.join(HERE, "..", "cc-P480-tools"))
sys.path.insert(0, os.path.join(HERE, "..", "cc-P707-tools"))''')
rep('''GATE = (6832, 3991)''', '''GATE = (6832, 3991)
TABLE = (6664, 3990)                       # cc-P718: TutorialCorePlacement.ClothesTable
FIELD_GATE = ((6713, 3978), (6713, 3979))  # cc-P718: TutorialFarm.FieldGateSpots
GATE_CLOSED = (0x0841, 0x0843)             # LightWoodGate SouthCW and NorthCCW, closed''')
rep('''    walk_to(pl, log, CAMP, 2, "the camp")
    pl.open_pack()''', '''    walk_to(pl, log, CAMP, 2, "the camp")
    n = len(c.messages)
    c.dclick(c.serial | 0x80000000)  # cc-P718: open the character window first, as a player double-clicks themselves
    log.check(pl.wait_text(r"That is your character window", 5, since=n) is not None, "the character window counts first")
    pl.open_pack()''')
rep('''    walk_to(pl, log, RACK, 2, "the clothes rack")
    pl.open_pack()
    cloak = c.wait(lambda: pl.in_pack(0x1515, SUPPLY) or pl.in_pack(0x1516, SUPPLY), 5)
    if not log.check(cloak is not None, "a practice cloak is in the backpack"):
        return
    if pl.lift(cloak):
        c.send(P.equip(cloak, 0x14, c.serial))
        log("  -> dropped the practice cloak on the paperdoll")''', '''    walk_to(pl, log, TABLE, 2, "the clothes table")
    cloak = c.wait(lambda: pl.item_at(TABLE, 0x1515, 0) or pl.item_at(TABLE, 0x1516, 0), 5)
    if not log.check(cloak is not None, "the cloak of the Wakening Isle lies on the clothes table"):
        return
    if pl.lift(cloak):
        c.send(P.equip(cloak, 0x14, c.serial))
        log("  -> dragged the cloak from the table onto the paperdoll")''')
rep('''def farm_pests(pl, log):
    c = pl.c
    walk_to(pl, log, PESTS, 3, "the cabbage rows")''', '''def open_field_gate(pl, log):
    """cc-P718: Wren opens the field gate; if it has swung shut, double-click each closed half."""
    c = pl.c
    for spot in FIELD_GATE:
        for gid in GATE_CLOSED:
            g = pl.item_at(spot, gid, 0)
            if g:
                pl.go(spot, 1)
                c.sleep(0.6)
                c.dclick(g)
                log("  -> opened the field gate at %d,%d" % spot)
                c.sleep(0.6)


def farm_pests(pl, log):
    c = pl.c
    walk_to(pl, log, WREN, 2, "the field gate")
    open_field_gate(pl, log)
    walk_to(pl, log, PESTS, 3, "the cabbage rows")''')
rep('''            log.check(pl.wait_text(r"This pet is yours to keep", 4, since=m0) is not None, "the System says the pet is yours")
            c.pet_command("all follow me")''', '''            log.check(pl.wait_text(r"This pet is yours to keep", 4, since=m0) is not None, "the System says the pet is yours")
            pet_commands(pl, log, m0)''')
rep('''        elif "all kill" in said:''', '''        elif "obeys spoken commands" in said:
            pet_commands(pl, log, m0)
        elif "all kill" in said:''')
rep('''def t_farm(pl, log):''', '''def pet_commands(pl, log, since):
    """cc-P718: Wren's pet commands: follow, then guard (speech; the pet's menu sets the same orders)."""
    c = pl.c
    c.pet_command("all follow me")
    log.check(pl.wait_text(r"Your pet follows you", 5, since=since) is not None, "'all follow me' counts")
    c.sleep(1.0)
    c.pet_command("all guard me")
    log.check(pl.wait_text(r"Your pet guards you", 5, since=since) is not None, "'all guard me' counts, and Wren opens the gate")


def t_farm(pl, log):''')
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
