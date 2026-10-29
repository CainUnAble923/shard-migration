"""cc-P733: IsleWalk733.py from P731's IsleWalk731.py: P732's wake check in place of P731's (shots while lying, then a
turn alone must get them up at once on the same tile), and shots of what P724 and P725 added: the wreck and the beach
after getting up, the shore and plants at each stop, the fountain on the bank's square (walked round to the bank door
and back), the lighthouse from the dock's road, and the moongate frame from the landing.
Usage: python -I make_walk733.py <IsleWalk731.py> <out IsleWalk733.py>"""
import re
import sys

src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8", newline="").read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:80])
    s = s.replace(a, b)


rep("# cc-P731: a real character plays", "# cc-P733 (P731's, with P732's wake and P724/P725's shots): a real character plays")
rep("p731-proof", "p733-proof", 2)
rep('API.SysMsg("P731: " + text)', 'API.SysMsg("P733: " + text)')
rep('CHARACTER = "Iron Dawn"', 'CHARACTER = "Iron Tide"')
rep('API.SysMsg("P731: not %s, the walk does not run" % CHARACTER)', 'API.SysMsg("P733: not %s, the walk does not run" % CHARACTER)')

# the wake: P732's check (lying shots, no window, "Move to get up", a turn gets them up at once on their tile)
a = s.index("API.Pause(3)\nlog_gumps(\"at login\")")
b = s.index("# -- 1. movement")
wake = '''import time
T0 = time.time()
UP = "You wake on a quiet shore"
for t, name in ((2, "lying-02"), (6, "lying-06"), (12, "lying-12"), (25, "lying-25")):
    while time.time() - T0 < t:
        API.Pause(0.25)
    say("%s: at %s, %d server windows, up: %s" % (name, where(), len(gumps()), API.InJournal(UP)))
    shot(name, 0.1)
check(not API.InJournal(UP), "still down 25 s in, without moving")
check(API.InJournal("Move to get up"), "the System said: Move to get up.")
check(len(gumps()) == 0, "no server window while lying")
start = where()
t1 = time.time()
API.Turn("south")
API.Pause(0.4)
shot("getting-up", 0.0)
up_after = None
while time.time() - t1 < 8:
    if API.InJournal(UP):
        up_after = time.time() - t1
        break
    API.Pause(0.2)
check(up_after is not None and up_after < 5, "the first move, a turn, got them up (%s s after it, shots included)" % (None if up_after is None else round(up_after, 1)))
check(where()[:2] == start[:2], "and they stay on their tile (%s, was %s)" % (where(), start))
API.Pause(4.0)
log_gumps("stood up")
shot("up-wreck-beach", 0.5, clear=True)

'''
s = s[:a] + wake + s[b:]

# P725's shore and plants along the lesson path; P724's wreck seen again from Tamsin's spot
rep('go(BLUE_TILE, 0, "the blue tile")', 'shot("path-tamsin", 0.5, clear=True)\ngo(BLUE_TILE, 0, "the blue tile")')
rep('go(CAMP, 2, "the camp")\n', 'go(CAMP, 2, "the camp")\nshot("path-camp", 0.5, clear=True)\n')
rep('go(SIGN, 2, "the signpost")\n', 'go(SIGN, 2, "the signpost")\nshot("path-chat-sign", 0.5, clear=True)\n')
rep('go(WREN, 3, "Wren at the farm gate")\n', 'go(WREN, 3, "Wren at the farm gate")\nshot("path-farm", 0.5, clear=True)\n')

# the fountain on the bank's square: walk to it, round it to the bank's door and back to the road
rep('for wp in ((6720, 3990), (6750, 3992), (6790, 3992), (6812, 3991)):\n    go(wp, 1, "the road")\n',
    '''for wp in ((6720, 3990), (6750, 3992), (6762, 3990)):
    go(wp, 1, "the road")
shot("fountain-square", 0.5, clear=True)
go((6766, 3986), 0, "beside the fountain (6768,3984)")
shot("fountain", 0.5, clear=True)
go((6762, 3981), 0, "the bank door (6762,3980), past the fountain and the signpost")
check(where()[1] <= 3981, "the fountain blocks no way to the bank door (at %s)" % (where(),))
go((6762, 3990), 0, "back to the road")
for wp in ((6790, 3992), (6806, 3991)):
    go(wp, 1, "the road")
shot("lighthouse", 0.5, clear=True)
go((6812, 3991), 1, "the road")
''')
rep('shot("dock-landing", 1.0, clear=True)', 'shot("dock-landing-frame", 1.0, clear=True)')
open(dst, "w", encoding="utf-8", newline="").write(s)
print("wrote", dst)
