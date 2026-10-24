"""cc-P412: chop one real map tree empty on a PRIVATE test shard (proof-shard.ps1, 127.0.0.1:2596) with the playtest
bot's client, and record what the server sent: the stump (0xF3, its Z) and the exhausted-tree message (0xF4 sub 0x05),
then the same list again after a relog.

    python -B chop.py --bot <work copy>\\tools\\playtest-bot --out <folder> [--port 2596]

The tree: Trammel (1300, 1536), a walnut tree, trunk 0x0CE0 and leaves 0x0CE1, both at Z 15 in statics1.mul
(D:\\UO\\tool-trials\\client-data-copy). A client targets a static at its own Z; pinned StaticTarget adds the tile's
height (20), so before P412 the stump sat at Z 35.
"""
import argparse
import json
import os
import struct
import sys
import time

TREE = (1300, 1536, 15)
TRUNK, LEAVES = 0x0CE0, 0x0CE1
STAND = (1301, 1536, 15)


def parse_f4(p):
    if len(p) < 9 or p[0] != 0xF4 or p[3] != 0x05:
        return None
    facet, plen = p[4], struct.unpack_from(">I", p, 5)[0]
    body, o, trees = p[9:9 + plen], 0, []
    while o + 9 <= len(body):
        x, y, secs, n = struct.unpack_from(">HHIB", body, o)
        ids = [struct.unpack_from(">H", body, o + 9 + 2 * i)[0] for i in range(n)]
        trees.append({"facet": facet, "x": x, "y": y, "seconds": secs, "ids": ["0x%04X" % i for i in ids]})
        o += 9 + 2 * n
    return trees


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bot", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--port", type=int, default=2596)
    a = ap.parse_args()
    sys.path.insert(0, a.bot)
    from uobot.client import Client, Cliloc, Transcript
    from uobot import checks, golemcheck

    os.makedirs(a.out, exist_ok=True)
    tr = Transcript(os.path.join(a.out, "transcript.txt"))
    cl = Cliloc(golemcheck.CLILOC if os.path.exists(golemcheck.CLILOC) else None)
    f4 = []

    def enter(role):
        user, pw = golemcheck.account("Iron", role)
        c = Client(user, pw, tr, cl, label="iron-" + role, test_target=("127.0.0.1", a.port))
        orig = c._handle

        def handle(p, c=c, orig=orig):
            if p and p[0] == 0xF4 and len(p) > 3 and p[3] == 0x05:
                f4.append({"who": c.label, "t": round(time.time(), 1), "trees": parse_f4(bytes(p)), "hex": bytes(p).hex()})
                c.log("<- 0xF4 sub 0x05 %s" % parse_f4(bytes(p)))
            return orig(p)

        c._handle = handle
        chars = c.login()
        want = golemcheck.character_name("Iron", role)
        c.play(chars.index(want))
        return c

    result = {}
    admin = enter("admin")
    player = enter("player")
    try:
        checks.staff_target(admin, "[set Map Trammel", player)
        checks.staff_target(admin, "[set Location (%d,%d,%d)" % STAND, player)
        player.wait(lambda: player.pos and player.pos[:2] == STAND[:2], 8)
        result["player_at"] = player.pos
        checks.staff_target(admin, "[SetSkill Lumberjacking 120", player)
        hatchet = checks.give(admin, player, "Hatchet")
        worn, said, _ = checks.try_equip(player, hatchet)
        result["hatchet_worn"] = worn
        admin.command("[go %d %d %d" % (STAND[0] + 1, STAND[1], STAND[2]), 1.0)  # the admin watches from beside

        chops = []
        for k in range(14):
            n = len(player.messages)
            player.dclick(hatchet)
            if not player.wait_target(8):
                chops.append("no target cursor")
                continue
            player.target_xyz(TREE[0], TREE[1], TREE[2], TRUNK)
            player.sleep(4.5)
            texts = player.texts_since(n)
            chops.append(texts)
            if any("not enough wood" in str(t) for t in texts):
                break
        result["chops"] = chops
        stumps = {s: it for s, it in player.items.items()
                  if it.get("world") and 0xE56 <= (it.get("graphic") or 0) <= 0xE59
                  and abs(it.get("x", 0) - TREE[0]) <= 1 and abs(it.get("y", 0) - TREE[1]) <= 1}
        result["stumps"] = [{"serial": "0x%08X" % s, "graphic": "0x%X" % it["graphic"], "at": [it["x"], it["y"], it["z"]]}
                            for s, it in stumps.items()]
        result["f4_while_chopping"] = list(f4)

        # A relog: EnterWorld empties the client's list and the shard resends every live tree.
        player.close()
        time.sleep(2)
        before = len(f4)
        player = enter("player")
        player.sleep(4)
        result["f4_after_relog"] = f4[before:]
    finally:
        for c in (admin, player):
            try:
                c.close()
            except Exception:
                pass
    with open(os.path.join(a.out, "result.json"), "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=1, default=str)
    print(json.dumps(result, indent=1, default=str))


if __name__ == "__main__":
    main()
