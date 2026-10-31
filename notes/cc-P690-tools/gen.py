"""cc-P690: the fresh world's generation, rehearsed in the order proposed for swap day (notes cc-P690 "go-live
checklist"), typed by the private shard's OWNER through the play-test bot's client (the packets a real client sends).

    python -P gen.py --port 2596 --out <folder> --secrets <secrets.json> [--bot <tools/playtest-bot>] [--only n,m]

The owner's account is the one answer_owner.py made at first boot; its password stays in the secrets file outside the
repos. The owner makes a staff character ("P690 Owner", New Haven) on first run, and logs the start-city list the
server offers (both start choices). Every command's replies go to <out>/gen-log.txt. Test ports only."""
import argparse
import json
import os
import sys
import time

STEPS = [
    # (command, settle seconds, why)
    ("[SeedGolemAccounts", 6, "test only: Iron's Admin and Player accounts for the clients (golem-accounts.json)"),
    ("[MoonGen", 8, "P679: the public moongates, PMList re-placed on SoS"),
    ("[TelGen", 15, "P679: teleporters-sos.json"),
    ("[Decorate", 90, "P680 stock decoration graded on SoS; P683 the author's dungeon lines"),
    ("[GenerateSpawners Data/Spawns/shared/**/*.json", 180, "SERVER.md:355; P681's moves apply on import"),
    ("[GenerateSpawners Data/Spawns/post-uoml/**/*.json", 90, "SERVER.md:356"),
    ("[GenerateSpawners Data/Spawns/uoml/**/*.json", 60, "SERVER.md:357"),
    ("[GenerateSpawners Data/Spawns/sos/**/*.json", 60, "P682: the author's new towns, keeps and wild"),
    ("[GenerateNewShame", 30, "reachability audit 5; Shame revamped"),
    ("[SetupDespise", 30, "reachability audit 5; P677 re-placed"),
    ("[GenChamps", 20, "P685: Felucca's champions on SoS"),
    ("[GenBlackthorn", 30, "P691: the dungeon on the Fold, the hatch in the castle"),
    ("[GenEodon", 30, "first boot said: Eodon moongate MISSING (run [GenEodon)"),
    ("[save", 30, "SERVER.md:360"),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=2596)
    ap.add_argument("--out", required=True)
    ap.add_argument("--secrets", required=True)
    ap.add_argument("--bot", default=r"D:\UO\golems\Iron\ShatteredLegacy\tools\playtest-bot")
    ap.add_argument("--cliloc", default=r"D:\UO\tool-trials\client-data-copy\Cliloc.enu")
    ap.add_argument("--only", default="")
    ap.add_argument("--extra", action="append", default=[], help="an extra command to type (repeatable), run after --only")
    a = ap.parse_args()
    sys.path.insert(0, a.bot)
    from uobot.client import Client, Cliloc, Transcript
    os.makedirs(a.out, exist_ok=True)
    logf = open(os.path.join(a.out, "gen-log.txt"), "a", encoding="ascii", errors="replace")
    t0 = time.time()

    def log(s):
        line = "[%7.1f] %s" % (time.time() - t0, s)
        print(line, flush=True)
        logf.write(line + "\n")
        logf.flush()

    s = json.load(open(a.secrets, encoding="utf-8"))
    tr = Transcript(os.path.join(a.out, "gen-transcript.txt"))
    cl = Cliloc(a.cliloc, r"D:\UO\bot-shard\cache")
    c = Client(s["owner"], s["ownerPassword"], tr, cl, label="owner", test_target=(a.host, a.port))
    s = None
    chars = c.login()
    log("owner's characters: %s" % [x for x in chars if x])
    log("start cities offered: %s" % (c.cities,))
    if "P690 Owner" in chars:
        c.play(chars.index("P690 Owner"))
    else:
        c.create("P690 Owner", stats=(60, 10, 10), city=1)
    c.sleep(3.0)
    log("owner in the world at %s map %s" % (c.pos, getattr(c, "map", None)))
    steps = STEPS
    if a.only == "none":   # an empty --only once ran every step again (run 3); "none" runs only --extra
        steps = []
    elif a.only:
        idx = [int(x) for x in a.only.split(",") if x != ""]
        steps = [STEPS[i] for i in idx]
    steps = list(steps) + [(x, 10, "extra") for x in a.extra]
    for cmd, settle, why in steps:
        log("=== %s   (%s)" % (cmd, why))
        n = len(c.messages)
        c.say(cmd)
        end = time.time() + settle
        last = n
        while time.time() < end:
            c.sleep(1.0)
            if int(time.time()) % 20 == 0:
                c.keepalive()   # run 1: a 3-minute import passed the server's inactivity limit
            if len(c.messages) != last:
                last = len(c.messages)
                end = max(end, time.time() + 5)   # keep reading while replies still come
        for m in c.messages[n:]:
            log("    %s: %s" % (m.get("name") or "-", m.get("text")))
        if c.closed:
            log("connection closed: %s" % c.closed)
            break
    c.close()
    log("done")


if __name__ == "__main__":
    main()
