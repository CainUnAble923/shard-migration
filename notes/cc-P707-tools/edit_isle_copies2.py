"""cc-P707: the copies part on accounts with no tutorial yet (the tutorial is per account: Iron's belongs to Iron
Islander), and each [Tutorial copies report by a freshly logged-in Admin (an idle bot client is dropped after ~55 s)."""
import os

p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'isle.py')
s = open(p).read()


def sub(old, new):
    global s
    assert s.count(old) == 1, old[:70]
    s = s.replace(old, new)


sub('''def copies_report(adm, log, label):
    lines = [m["text"] for m in adm.command("[Tutorial copies", settle=3.0)]''', '''def copies_report(a, tr, cl, log, label):
    from uobot.client import Client
    from uobot import golemcheck as GC
    user, pw = GC.account(a.golem, "admin")
    adm = Client(user, pw, tr, cl, label="admin", test_target=(a.host, a.port))
    chars = adm.login()
    adm.play(chars.index(a.golem) if a.golem in chars else 0)
    pw = None
    lines = [m["text"] for m in adm.command("[Tutorial copies", settle=3.0)]
    adm.close()''')
sub('''def part_copies(a, tr, cl, grid, log, adm):''', '''def part_copies(a, tr, cl, grid, log):''')
sub('''    for golem, name in ((a.golem, "Iron PartyA"), ("Bronze", "Bronze PartyB")):''',
    '''    for golem, name in (("Silver", "Silver PartyA"), ("Gold", "Gold PartyB")):''')
sub('''    cc, chars = account_client(a, tr, cl, "Copper", "Copper")
    nc = "Copper Third"''', '''    cc, chars = account_client(a, tr, cl, "Stone", "Stone")
    nc = "Stone Third"''')
sub('''    ca, chars = account_client(a, tr, cl, a.golem, "PartyA")''', '''    ca, chars = account_client(a, tr, cl, "Silver", "PartyA")''')
s = s.replace('copies_report(adm, log, ', 'copies_report(a, tr, cl, log, ')
sub('''    if "copies" in parts and adm:
        part_copies(a, tr, cl, grid, log, adm)''', '''    if "copies" in parts:
        part_copies(a, tr, cl, grid, log)''')
sub('''        if adm:
            for m in adm.command("[Tutorial copies", settle=3.0):
                log("    admin: %s" % m["text"])''', '''        copies_report(a, tr, cl, log, "after the isle character woke")''')
sub('''    if "seed" in parts or "copies" in parts:
        user, pw = GC.account(a.golem, "admin")''', '''    if "seed" in parts:
        user, pw = GC.account(a.golem, "admin")''')
open(p, 'w').write(s)
print('ok')
