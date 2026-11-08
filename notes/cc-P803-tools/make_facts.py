"""cc-P803: writes server/tests/Misc/LeagueOfficeDecorVerification.cs into one copy from the template, with that town's
walls, windows and board.   python -P notes/cc-P803-tools/make_facts.py <release|main> <root>
Walls and windows from the map (office_statics.py on client-data-copy for the release, p735-work/patched for main)."""
import sys, os
which, root = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(os.path.join(here, "LeagueOfficeDecorVerification.cs.template")).read()
FOREIGN = open(os.path.join(here, "foreign-fact.cs.part")).read()
P = lambda pts: ", ".join("new(%d, %d)" % p for p in pts)
if which == "release":
    v = dict(BRANCH="the isle release", TOWN="the ML New Haven house, walls x3453-3462, y2596-2603, floor z18",
             FLOORZ="18", BOARD="3458, 2598, 18", BOARDART="0x1E5E",
             WINDOWS=P([(3456, 2597), (3460, 2597), (3454, 2598), (3461, 2598), (3461, 2602), (3456, 2602), (3460, 2602), (3454, 2602)]),
             ROOMS="(3457, 2596, 3458, 2597, 3461, 2602), (3453, 2596, 3454, 2597, 3456, 2602)",
             OLDSPOTS="    [InlineData(3459, 2596, 18)]\n", FOREIGN=FOREIGN)
else:
    v = dict(BRANCH="main", TOWN="SoS Haven's hall, walls x3658-3674, y2547-2562, floor z0",
             FLOORZ="0", BOARD="3662, 2548, 0", BOARDART="0x1E5F",
             WINDOWS=P([(3661, 2561), (3662, 2561), (3664, 2561), (3665, 2561), (3670, 2561), (3673, 2561)]),
             ROOMS="(3658, 2547, 3659, 2548, 3673, 2561)",
             OLDSPOTS="    [InlineData(3459, 2596, 18)]\n    [InlineData(3662, 2547, 0)]\n", FOREIGN="")
for k, val in v.items():
    s = s.replace("@@%s@@" % k, val)
assert "@@" not in s
out = root + "/server/tests/Misc/LeagueOfficeDecorVerification.cs"
open(out, "w", newline="\n").write(s)
print(out)
