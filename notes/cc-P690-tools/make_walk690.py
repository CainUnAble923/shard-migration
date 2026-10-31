"""cc-P690: IsleWalk690.py from P740's IsleWalk740.py: only the name and the paths change (tazuo-pkg.ps1 fills
__CHARACTER__ and __OUT__). Usage: python -P make_walk690.py"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
s = open(os.path.join(HERE, "p740", "IsleWalk740.py"), encoding="utf-8", newline="").read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a)
    s = s.replace(a, b)


rep("# cc-P740 (P733's, with P740's wake and bandages): a real character plays",
    "# cc-P690: P740's IsleWalk740.py, run by TazUO FROM THE BUILT PACKAGE (tazuo-pkg.ps1) on a fresh world, for a\n"
    "# brand-new account; only the name and the paths change (the runner fills __CHARACTER__ and __OUT__).\n"
    "# cc-P740 (P733's, with P740's wake and bandages): a real character plays")
rep(r'LOG = r"D:\UO\golems\Iron\p740-proof\walk.log"', r'LOG = r"__OUT__\walk.log"')
rep(r'SIG = r"D:\UO\golems\Iron\p740-proof\shots.sig"', r'SIG = r"__OUT__\shots.sig"')
rep('API.SysMsg("P740: " + text)', 'API.SysMsg("P690: " + text)')
rep('CHARACTER = "Iron Dunes"', 'CHARACTER = "__CHARACTER__"')
open(os.path.join(HERE, "IsleWalk690.py"), "w", encoding="utf-8", newline="").write(s)
print("wrote IsleWalk690.py")
