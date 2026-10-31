"""cc-P740: IsleWalk740.py from P733's IsleWalk733.py: the wake checked as P740 has it (lying shots in the lighter dusk,
"You lie on the wet sand..." and "Move to get up." over the head, a turn starts the slow get-up, shot as a frame burst,
then the dawn, and no window or first line before then), and the healing lesson's bandages again (the lesson's own set
down, Wren's hint, Wren hands more, then the table's picked up beside Pip, and Pip healed with them).
Usage: python -I make_walk740.py <IsleWalk733.py> <out IsleWalk740.py> <character name>"""
import sys

src, dst, character = sys.argv[1], sys.argv[2], sys.argv[3]
s = open(src, encoding="utf-8", newline="").read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:80])
    s = s.replace(a, b)


rep("# cc-P733 (P731's, with P732's wake and P724/P725's shots): a real character plays",
    "# cc-P740 (P733's, with P740's wake and bandages): a real character plays")
rep("p733-proof", "p740-proof", 2)
rep('API.SysMsg("P733: " + text)', 'API.SysMsg("P740: " + text)')
rep('CHARACTER = "Iron Tide"', 'CHARACTER = "%s"' % character)
rep('API.SysMsg("P733: not %s, the walk does not run" % CHARACTER)', 'API.SysMsg("P740: not %s, the walk does not run" % CHARACTER)')

# -- the wake ---------------------------------------------------------------------------------------------------------
a = s.index("import time\nT0 = time.time()")
b = s.index("# -- 1. movement")
wake = '''import time
T0 = time.time()
UP = "You wake on a quiet shore"
for t, name in ((2, "lying-02"), (5, "lying-05"), (10, "lying-10")):
    while time.time() - T0 < t:
        API.Pause(0.25)
    say("%s: at %s, %d server windows, up: %s" % (name, where(), len(gumps()), API.InJournal(UP)))
    shot(name, 0.1)
check(not API.InJournal(UP), "still down 10 s in, without moving")
say("over the head: You lie on the wet sand... (TazUO keeps an overhead line off the journal: see the lying-02 shot)")
check(API.InJournal("Move to get up"), "Move to get up. (by %d s)" % int(time.time() - T0))
check(len([1 for _, t in gumps() if t]) == 0, "no server window while lying")
start = where()
t1 = time.time()
API.Turn("south")
with open(SIG, "a") as f:
    f.write("BURST getting-up 14 400\\n")
up_after, first_gump = None, None
while time.time() - t1 < 15:
    if first_gump is None and len([1 for _, t in gumps() if t]) > 0:   # run 1: the quest arrow is a gump without text
        first_gump = time.time() - t1
    if up_after is None and API.InJournal(UP):
        up_after = time.time() - t1
    if up_after is not None and first_gump is not None:
        break
    API.Pause(0.2)
say("after the turn: first lines at %s s, first server window at %s s" % (
    None if up_after is None else round(up_after, 1), None if first_gump is None else round(first_gump, 1)))
check(up_after is not None and 3.5 <= up_after <= 9, "the first lines come after the get-up and the dawn (%s s after the turn)" % (None if up_after is None else round(up_after, 1)))
check(first_gump is not None and up_after is not None and first_gump >= up_after + 1.5, "no window before they are up and the light is back; the windows %s s after the lines" % (None if first_gump is None or up_after is None else round(first_gump - up_after, 1)))
check(where()[:2] == start[:2], "they stay on their tile (%s, was %s)" % (where(), start))
shot("up-day", 0.5)
API.Pause(2.0)
log_gumps("stood up")
shot("up-wreck-beach", 0.5, clear=True)

'''
s = s[:a] + wake + s[b:]

# -- the healing lesson: the bandages again ----------------------------------------------------------------------------
rep('''check(wait_journal("sits hurt on the bench", 6), "the healing lesson points at Pip in the farmhouse")
go(STEPS, 0, "the farmhouse steps")''',
'''check(wait_journal("sits hurt on the bench", 6), "the healing lesson points at Pip in the farmhouse")
TABLE_BANDAGES = (6690, 3975)


def set_down_bandages():
    # run 1: the first set-down, right after the lesson's click, was refused (the item-move pace); retry, paced
    for _ in range(4):
        b = API.FindType(0x0E21, API.Backpack)
        if b is None:
            return True
        API.Pause(1.5)
        API.MoveItemOffset(b.Serial, 0, 1, 0)
        API.Pause(1.5)
    return API.FindType(0x0E21, API.Backpack) is None


check(API.FindType(0x0E21, API.Backpack) is not None, "the lesson's bandages are in the backpack")
check(set_down_bandages(), "set down: no bandages in the backpack now")
check(wait_journal("No bandages?", 40), "Wren says where to get bandages (over her head)")
shot("wren-hint", 0.1)
wren = mobiles_near(WREN, 2, name="Wren")
if wren:
    go(BELOW_WREN, 1, "back to Wren")
    API.UseObject(wren[0].Serial)
    check(wait_journal("Here are more bandages", 6), "double-clicked, Wren hands more")
    check(API.FindType(0x0E21, API.Backpack) is not None, "Wren's bandages are in the backpack")
check(set_down_bandages(), "set down again, for the table: no bandages in the backpack")
go(STEPS, 0, "the farmhouse steps")''')
rep('''shot("pip", 1.0, clear=True)
band = API.FindType(0x0E21, API.Backpack)''',
'''shot("pip", 1.0, clear=True)
table = [it for it in API.GetItemsOnGround(4, 0x0E21) if (it.X, it.Y) == TABLE_BANDAGES]
if check(len(table) > 0, "bandages lie on the table beside Pip (%s)" % ((table[0].X, table[0].Y, table[0].Z) if table else None,)):
    shot("table-bandages", 0.5)
    API.ClearJournal()
    API.MoveItem(table[0].Serial, API.Backpack)   # pick them up
    if not wait_journal("You take some bandages from the table", 6):
        say("the drag gave none; double-click")
        API.Pause(1.0)
        API.UseObject(table[0].Serial)
        wait_journal("You take some bandages from the table", 6)
    check(API.InJournal("You take some bandages from the table"), "the table's bandages: a stack of the trainee's own")
    API.Pause(1.0)
    still = [it for it in API.GetItemsOnGround(4, 0x0E21) if (it.X, it.Y) == TABLE_BANDAGES]
    check(len(still) > 0, "and the table's stack stays on the table")
band = API.FindType(0x0E21, API.Backpack)''')

open(dst, "w", encoding="utf-8", newline="").write(s)
print("wrote", dst)
