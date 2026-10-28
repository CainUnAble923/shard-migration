"""cc-P707: isle.py --account <golem> (whose Player account the isle character is made on) and --stop-at <lesson key>
(stop when that lesson's page opens, logged out there: the vision shot's trainee stands at the stones)."""
import os

p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'isle.py')
s = open(p).read()


def sub(old, new):
    global s
    assert s.count(old) == 1, old[:70]
    s = s.replace(old, new)


sub('''def play_isle(pl, log, times, first="core.movement"):''', '''def play_isle(pl, log, times, first="core.movement", stop_at=None):''')
sub('''        key = next(by_title[t] for t in c.gump_text(lesson) if (t or "") in by_title)
        log("--- %s" % key)''', '''        key = next(by_title[t] for t in c.gump_text(lesson) if (t or "") in by_title)
        log("--- %s" % key)
        if key == stop_at:
            log("  stopping at %s, as asked (--stop-at), at %s" % (key, pl.pos()))
            if key == "core.loop":
                walk_to(pl, log, STONES, 2, "the standing stones")
            return True''')
sub('''def player_client(a, tr, cl):
    from uobot.client import Client
    from uobot import golemcheck as GC
    user, pw = GC.account(a.golem, "player")''', '''def player_client(a, tr, cl):
    from uobot.client import Client
    from uobot import golemcheck as GC
    user, pw = GC.account(a.account or a.golem, "player")''')
sub('''    ap.add_argument("--hold-minutes", type=int, default=2, help="the world's clusterf.tutorial.copyHoldMinutes")''',
    '''    ap.add_argument("--hold-minutes", type=int, default=2, help="the world's clusterf.tutorial.copyHoldMinutes")
    ap.add_argument("--account", default="", help="the Golem whose Player account makes the isle and skip characters")
    ap.add_argument("--stop-at", default=None, help="stop when this lesson's page opens (the shots' trainee)")''')
sub('''        ok = play_isle(pl, log, times, a.first)''', '''        ok = play_isle(pl, log, times, a.first, a.stop_at)''')
open(p, 'w').write(s)
print('ok')
