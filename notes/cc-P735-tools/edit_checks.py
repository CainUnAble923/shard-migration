"""cc-P735: T-039 and P64-1 (and so P64-2, which reads P64-1's run) make their character with creation's New Haven
city: on an isle-ready world city 0 wakes on the isle's beach, where neither New Haven's board nor the first-login
bulletin (held until the trainee stands, cc-P728) is there to check. They now test a character whose account has
finished or skipped the tutorial.
Usage: python -P edit_checks.py <code copy>"""
import sys

p = sys.argv[1] + "/tools/playtest-bot/uobot/checks.py"
s = open(p, encoding="utf-8", newline="").read()


def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:90])
    s = s.replace(a, b)


rep('''    unused = [a for a in ctx.pool_rest if a not in ctx.first_logins]
    if not unused:
        raise RuntimeError("no pool account left for a first login")
    c = ctx.fresh(race="human", female=False, label="fresh")
''', '''    unused = [a for a in ctx.pool_rest if a not in ctx.first_logins]
    if not unused:
        raise RuntimeError("no pool account left for a first login")
    # cc-P735: New Haven's start (creation's city 1). On an isle-ready world city 0 wakes on the isle, where the bulletin
    # waits until the trainee stands up (cc-P728), so this checks a character whose account skipped the tutorial.
    c = ctx.fresh(race="human", female=False, label="fresh", city=HAVEN_CITY, first_login=True)
''')

rep('''    race, female = RACES[SHARED.setdefault("t039", 0) % len(RACES)]
    SHARED["t039"] += 1
    c = ctx.fresh(race=race, female=female)
''', '''    race, female = RACES[SHARED.setdefault("t039", 0) % len(RACES)]
    SHARED["t039"] += 1
    # cc-P735: New Haven's start (creation's city 1), a character whose account skipped the tutorial; city 0 wakes on the
    # isle once the isle is ready (cc-P688 found it on the bot's world).
    c = ctx.fresh(race=race, female=female, city=HAVEN_CITY)
''')

# the constant, beside the module's other imports
a = s.index("\nimport ")
b = s.index("\n\n", a)
s = s[:b] + "\n\nHAVEN_CITY = 1   # cc-P735: creation's New Haven entry (uobot.run.HAVEN_CITY; TutorialStart.Cities)" + s[b:]
open(p, "w", encoding="utf-8", newline="").write(s)
print("edited", p)
