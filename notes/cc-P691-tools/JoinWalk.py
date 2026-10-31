# cc-P691: a real character walks north up the dungeon's corridor across the join into the invasion block's cave
# mouth room (the join teleporters, the cut between the two pieces), then south back through the wall's gap to the
# corridor. Started by TazUO in the world (Data\lscript.json). Positions go to the journal and to
# D:\UO\golems\Iron\p691-proof\join-walk.log. The shot's commands put the character at 6399,3842,0, under the cave side's
# west gap (x 7015) after the crossing.
import API

LOG = r"D:\UO\golems\Iron\p691-proof\join-walk.log"


def say(text):
    API.SysMsg("JoinWalk: " + text)
    with open(LOG, "a") as f:
        f.write(text + "\n")


def where():
    p = API.Player
    return (p.X, p.Y, p.Z)


API.Pause(8)
say("start %s" % (where(),))
for direction, done, limit in (("north", lambda p: p[0] > 6900, 12), ("south", lambda p: p[0] < 6600, 8)):
    for i in range(limit):
        API.Walk(direction)
        API.Pause(0.7)
        now = where()
        say("%s step %d: %s" % (direction, i, now))
        if done(now):
            say("%s: crossed to %s" % (direction, now))
            break
    else:
        say("%s: DID NOT CROSS, at %s" % (direction, where()))
    API.Pause(3)
say("end %s" % (where(),))
