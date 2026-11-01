# cc-P758 (P742's VisionShots742.py, paths only): a brand-new trainee (made by the bot's client minutes before, stopped at the standing stones with every lesson
# before the vision done, isle.py --stop-at core.loop) is logged in by TazUO; this script double-clicks the vision's
# signpost and asks the runner (isle-shots742.ps1, its "sig" file) for a shot at each beat, checks the trainee is moved
# into the chamber strip and back onto the very tile it stood on, and logs every step to LOG. Started by TazUO itself
# (Data\lscript.json), so every action is the client's own.
import API
import time

LOG = r"D:\UO\golems\Iron\p758-proof\vision.log"
SIG = r"D:\UO\golems\Iron\p758-proof\vision-signal.txt"
CHARACTER = "Iron Visionary"
LOOP_SIGN = (6794, 3981)            # TutorialCorePlacement.SignPoint("core.loop")
STRIP = (6170, 3752, 6570, 3760)    # TutorialVisionChamber.Strip: x 6170 to 6570, y 3752 to 3760 (inclusive)
FAILS = []


def say(text):
    with open(LOG, "a") as f:
        f.write(text + "\n")
    API.SysMsg("P758: " + text)


def signal(text):
    with open(SIG, "a") as f:
        f.write(text + "\n")


def check(ok, what):
    say(("PASS " if ok else "FAIL ") + what)
    if not ok:
        FAILS.append(what)
    return ok


def where():
    p = API.Player
    return (int(p.X), int(p.Y), int(p.Z))


def hidden():
    # TazUO's Legion API: the player's hidden flag, if this build has it (shots show it either way)
    for name in ("IsHidden", "Hidden"):
        v = getattr(API.Player, name, None)
        if v is not None:
            return bool(v)
    return None


def in_strip(p):
    return STRIP[0] <= p[0] <= STRIP[2] and STRIP[1] <= p[1] <= STRIP[3]


def clear():
    for _ in range(6):
        API.CloseGump()
        API.Pause(0.3)
    for g in API.GetAllGumps():
        try:
            g.Dispose()
        except Exception:
            pass


if API.Player.Name != CHARACTER:
    API.SysMsg("P758: not %s, the script does not run" % CHARACTER)
else:
    API.Pause(6)
    for _ in range(3):
        clear()
        API.Pause(2)
    # cc-P758: VisionBack758.py's free-to-move check can leave the trainee a tile south, out of the signpost's reach
    # (3 tiles); walk north back onto 6792,3984 first (the first step may only turn)
    for _ in range(4):
        if where()[1] <= 3984:
            break
        API.Walk("north")
        API.Pause(0.8)
    start = where()
    say("start %s at %s, hidden %s" % (CHARACTER, start, hidden()))
    signal("SHOT vision-00-at-the-stones")
    API.Pause(3)
    sign = None
    for it in API.GetItemsOnGround(6, 0xA854):
        if (int(it.X), int(it.Y)) == LOOP_SIGN:
            sign = it
    if check(sign is not None, "the vision's signpost stands at %s" % (LOOP_SIGN,)):
        API.ClearJournal()
        # run 1: after a relog the lesson starts again first ("You have found Watch a loop vision"), so a second
        # double-click starts the vision, as a player would do; the vision starts when the trainee is moved
        t0 = None
        for attempt in range(3):
            API.UseObject(sign.Serial)
            t1 = time.time()
            while time.time() - t1 < 4 and not in_strip(where()):
                API.Pause(0.1)
            if in_strip(where()):
                t0 = time.time() - 0.2
                say("the vision started on double-click %d" % (attempt + 1))
                break
            say("double-click %d: no vision yet (at %s)" % (attempt + 1, where()))
            clear()
            API.Pause(1.0)
        if t0 is None:
            t0 = time.time()
        # beats (TutorialVisionScene.Beats): 0 dark, 2 lit, 4 and 6 the walk, 7 faces, 8 strike, 9 burst, 11 second blow,
        # 16 the Gem shatters (flash), 17 shards, 23 flash, 24 folds, 28 echo, 30 echo speaks, 41 hooded, 42 speaks,
        # 47 what you keep, 52 fade out, 57 the gate, 61 back
        shots = [(1.0, "vision-01-dark"), (3.0, "vision-02-shrine-lit"), (5.0, "vision-03-stranger-walks"),
                 (7.5, "vision-04-faces-the-gem"), (8.3, "vision-05-strike"), (9.3, "vision-06-hit"),
                 (11.4, "vision-07-second-blow"), (16.2, "vision-08-gem-shatters"), (17.5, "vision-09-shards"),
                 (23.2, "vision-10-flash"), (29.0, "vision-11-echo"), (31.0, "vision-12-echo-speaks"),
                 (43.0, "vision-13-hooded-figure"), (48.0, "vision-14-what-you-keep"), (58.0, "vision-15-the-gate"),
                 (64.0, "vision-16-back")]
        inside = None
        for at, name in shots:
            while time.time() - t0 < at:
                API.Pause(0.1)
            p = where()
            say("%5.1f s %s at %s, hidden %s" % (time.time() - t0, name, p, hidden()))
            if name == "vision-02-shrine-lit":
                inside = p
            signal("SHOT " + name)
        check(inside is not None and in_strip(inside), "during the vision the trainee stands in the chamber (%s)" % (inside,))
        API.Pause(2)
        back = where()
        check(back == start, "after it, back on the very tile (%s, was %s)" % (back, start))
        check(hidden() in (False, None), "and seen again (hidden flag: %s)" % (hidden(),))
        check(API.InJournal("Lesson finished") or API.InJournal("finished"), "the vision lesson is finished")
        # free to move: one step west and back
        API.Walk("south")
        API.Pause(0.8)
        moved = where()
        API.Walk("north")
        API.Pause(0.8)
        check(moved != back, "free to move again (stepped to %s)" % (moved,))
    say("END %d failed: %s" % (len(FAILS), FAILS))
    signal("DONE")
