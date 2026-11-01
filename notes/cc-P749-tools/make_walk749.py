"""cc-P749: IsleWalk749.py from P740's IsleWalk740.py (itself from P733's stock-land walk) for the isle-only release:
P741's turned-round farm (the field 18 west with its gate on the east side, the farmhouse 12 east with Pip, the table's
bandages and the door), a check that the farm-then-farmhouse leg never doubles back west, and the bank and the League
lodge walked into and shot. The wake and the bandage steps are P740's as they are.
Usage: python -P make_walk749.py <IsleWalk740.py> <out IsleWalk749.py> <character name>"""
import sys

src, dst, character = sys.argv[1], sys.argv[2], sys.argv[3]
s = open(src, encoding="utf-8", newline="").read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:80])
    s = s.replace(a, b)


rep("# cc-P740 (P733's, with P740's wake and bandages): a real character plays",
    "# cc-P749 (P740's, with P741's farm; the isle-only release): a real character plays")
rep("p740-proof", "p749-proof", 2)
rep('API.SysMsg("P740: " + text)', 'API.SysMsg("P749: " + text)')
rep('API.SysMsg("P740: not %s, the walk does not run" % CHARACTER)', 'API.SysMsg("P749: not %s, the walk does not run" % CHARACTER)')
a = s.index('CHARACTER = "')
b = s.index("\n", a)
s = s[:a] + 'CHARACTER = "%s"   # the brand-new character TazUO creates (ui.ps1); any other character: do nothing' % character + s[b:]

# -- P741's farm: the field west (gate on its east fence), the farmhouse east beside the gate ------------------------
rep("WREN, BELOW_WREN, PESTS = (6714, 3978), (6714, 3979), (6702, 3978)",
    "WREN, BELOW_WREN, PESTS = (6696, 3978), (6696, 3979), (6684, 3978)   # cc-P741: TutorialFarm.FarmhandSpot, gate 6695,3979")
rep("PIP = (6692, 3975)", "PIP = (6704, 3975)   # cc-P741: TutorialFarm.PipBench")
rep("STEPS = (6690, 3980)", "STEPS = (6702, 3980)   # cc-P741: below the farmhouse door 6702,3978")
rep("TABLE_BANDAGES = (6690, 3975)", "TABLE_BANDAGES = (6702, 3975)   # cc-P741: TutorialFarm.TableBandagesSpot")

# -- the route's order: chat sign, Wren, the farmhouse, then on east; never back west past the gate -----------------
rep('''go(SIGN, 2, "the signpost")
shot("path-chat-sign", 0.5, clear=True)''',
'''go(SIGN, 2, "the signpost")
shot("path-chat-sign", 0.5, clear=True)
ROUTE = [("chat sign", where())]''')
rep('''go(WREN, 3, "Wren at the farm gate")
shot("path-farm", 0.5, clear=True)''',
'''go(WREN, 3, "Wren at the farm gate")
shot("path-farm", 0.5, clear=True)
ROUTE.append(("Wren at the gate", where()))''')
rep('''pip = mobiles_near(PIP, 0, name="Pip")
check(len(pip) > 0''',
'''ROUTE.append(("in the farmhouse", where()))
pip = mobiles_near(PIP, 0, name="Pip")
check(len(pip) > 0''')
rep('''check(abs(API.Player.X - STEPS[0]) <= 1 and abs(API.Player.Y - STEPS[1]) <= 1, "back out of the farmhouse (at %s)" % (where(),))''',
'''check(abs(API.Player.X - STEPS[0]) <= 1 and abs(API.Player.Y - STEPS[1]) <= 1, "back out of the farmhouse (at %s)" % (where(),))
go((6720, 3990), 1, "the road east of the farm")
ROUTE.append(("the road east", where()))
say("route: " + ", ".join("%s %s" % (n, p[:2]) for n, p in ROUTE))
xs = [p[0] for _, p in ROUTE]
check(all(xs[i] <= xs[i + 1] + 1 for i in range(len(xs) - 1)),
      "chat sign, farm gate, farmhouse, road: each stop east of the last, no doubling back (x %s)" % xs)
shot("farm-from-road", 0.5, clear=True)''')

# -- the League lodge, after the bank ----------------------------------------------------------------------------------
rep('''go((6762, 3990), 0, "back to the road")
for wp in ((6790, 3992), (6806, 3991)):''',
'''go((6762, 3990), 0, "back to the road")
shot("bank-front", 0.5, clear=True)
go((6782, 3991), 0, "the road at the League lodge's walk")
shot("lodge-front", 0.5, clear=True)
go((6782, 3997), 0, "inside the League lodge, through its door (6782,3995)")
check(where()[1] >= 3996, "walked into the League lodge (at %s)" % (where(),))
shot("lodge-inside", 1.0, clear=True)
go((6782, 3991), 0, "back out to the road")
check(where()[1] <= 3992, "walked back out of the lodge (at %s)" % (where(),))
for wp in ((6790, 3992), (6806, 3991)):''')

open(dst, "w", encoding="utf-8", newline="").write(s)
print("wrote", dst)
