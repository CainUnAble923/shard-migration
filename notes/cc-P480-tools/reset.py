"""cc-P480: the one staff step between the two screenshot sessions. The character logs in (the bot's client), Iron's
Admin runs [Tutorial reset on it (TutorialRecord cleared), and both log out; the character's next login enters the core.
Test ports only (safety.check_test_target). Passwords from Get-GolemTestAccount.ps1, never written. ASCII only.

    python -P reset.py --port 2596 --name "Iron Arrival" --tiledata D:\\UO\\UltimaOnlineVanilla --out <folder>
"""
import argparse, os, sys


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=2596)
    ap.add_argument("--name", required=True)
    ap.add_argument("--tiledata", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--bot", default=r"D:\UO\golems\Iron\ShatteredLegacy\tools\playtest-bot")
    ap.add_argument("--golem", default="Iron")
    a = ap.parse_args(argv)
    sys.path.insert(0, a.bot)
    from uobot.client import Client, Cliloc, Transcript
    from uobot import golemcheck as GC
    os.makedirs(a.out, exist_ok=True)
    tr = Transcript(os.path.join(a.out, "reset-transcript.txt"))
    cl = Cliloc(os.path.join(a.tiledata, "Cliloc.enu"), r"D:\UO\bot-shard\cache")
    user, pw = GC.account(a.golem, "player")
    pc = Client(user, pw, tr, cl, label="player", test_target=(a.host, a.port))
    chars = pc.login()
    pw = None
    pc.play(chars.index(a.name))
    pc.sleep(3.0)
    x, y = pc.pos[0], pc.pos[1]
    user, pw = GC.account(a.golem, "admin")
    adm = Client(user, pw, tr, cl, label="admin", test_target=(a.host, a.port))
    chars = adm.login()
    pw = None
    adm.play(chars.index(a.golem) if a.golem in chars else 0)
    adm.sleep(2.0)
    adm.command("[go %d %d 14" % (x, y - 2), settle=2.0)
    n = len(adm.messages)
    adm.say("[Tutorial reset")
    if adm.wait_target(6):
        adm.target_obj(pc.serial)
    adm.sleep(2.0)
    replies = [m["text"] for m in adm.messages[n:]]
    print("admin: %s" % replies)
    for c in (pc, adm):
        try:
            c.close()
        except Exception:
            pass
    tr.close()
    return 0 if any("cleared" in (t or "") for t in replies) else 1


if __name__ == "__main__":
    sys.exit(main())
