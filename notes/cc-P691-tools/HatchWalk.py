# cc-P691: a real character walks onto the cellar hatch in Blackthorn Castle (the client's own steps, the server's own
# checks) and so goes down to the dungeon's landing on the Fold, then walks east up the landing's stairs and so comes
# back beside the hatch. Started by TazUO in the world (Data\lscript.json). Each step's position goes to the journal and
# to D:\UO\golems\Iron\p691-proof\hatch-walk.log. The shot's commands put the character on the landing tile, 1521,1437,15, two east of the hatch.
import API

LOG = r"D:\UO\golems\Iron\p691-proof\hatch-walk.log"


def say(text):
    API.SysMsg("HatchWalk: " + text)
    with open(LOG, "a") as f:
        f.write(text + "\n")


def where():
    p = API.Player
    return (p.X, p.Y, p.Z)


API.Pause(8)
say("start %s" % (where(),))
for direction, done, limit in (("west", lambda p: p[0] > 6000, 10), ("east", lambda p: p[0] < 2000, 20)):
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
