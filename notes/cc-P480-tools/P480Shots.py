# P480Shots.py (cc-P480): the Legion side of shots.ps1, started by itself when the character enters the world. ASCII only.
#
# It does what a player does (walks to Rook, double-clicks him, presses a button) and, at each moment worth a picture,
# writes status.json {"state": "shot", "name": ...} into RUN_DIR and waits for the harness's "ack-<name>" file (the
# harness captures the window first). Modes (RUN_DIR\mode.txt):
#   companion  a graduate whose companion is waiting: Rook's page with "Choose your companion", then the pick.
#   core       a character just entered into the core: Rook's core-only page, the first lesson's page, the tiles.
import API
import json
import os
import time

RUN_DIR = r"@RUN_DIR@"


def path(name):
    return os.path.join(RUN_DIR, name)


def status(obj):
    tmp = path("status.json.tmp")
    with open(tmp, "w") as f:
        f.write(json.dumps(obj))
    if os.path.exists(path("status.json")):
        os.remove(path("status.json"))
    os.rename(tmp, path("status.json"))


def log(text):
    with open(path("runner.log"), "a") as f:
        f.write(time.strftime("%H:%M:%S") + " " + text + "\n")


def shot(name):
    log("shot " + name)
    status({"state": "shot", "name": name})
    t0 = time.time()
    while not os.path.exists(path("ack-" + name)) and time.time() - t0 < 60:
        API.Pause(0.5)


def rook():
    for m in API.GetAllMobiles(None, 20) or []:
        if m.Name and "Rook" in m.Name:
            return m
    return None


def to_rook():
    r = rook()
    if r is None:
        log("no Rook in sight")
        return None
    API.PathfindEntity(r.Serial, 2, True, 15)
    API.Pause(1.0)
    return r


def main():
    status({"state": "inworld"})
    mode = open(path("mode.txt")).read().strip()
    log("mode " + mode)
    API.Pause(6.0)          # the login's lines and pages arrive
    shot("0-login")
    API.CloseGumps()
    API.Pause(1.0)
    r = to_rook()
    if r is None:
        status({"state": "done", "why": "no Rook"})
        return
    API.UseObject(r.Serial)
    API.Pause(2.5)
    if mode == "companion":
        shot("1-rook-companion")
        API.ReplyGump(4)        # TutorialRecruiterGump.BtnCompanion
        API.Pause(2.5)
        shot("2-companion-pick")
    else:
        shot("1-rook-core-menu")
        API.ReplyGump(100)      # the first core lesson
        API.Pause(3.0)
        shot("2-lesson-and-tiles")
        API.CloseGumps()
        API.Pathfind(3497, 2569, 14, 0, True, 10)   # two tiles north-west: the tiles in open view, below the windows
        API.Pause(2.2)          # a sparkle every two seconds
        shot("3-tiles")
        API.Pathfind(3499, 2571, 14, 0, True, 10)
        API.Pause(2.0)
        shot("4-on-the-blue-tile")
    status({"state": "done"})


try:
    main()
except Exception as e:
    log("error: " + str(e))
    status({"state": "done", "why": str(e)})
