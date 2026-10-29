"""cc-P679: walk the dungeon entrances SoS rebuilt, on a PRIVATE test shard, with the playtest bot's client.

    python -P walk_entrances.py --code <code copy> --port 2596 [--golem Iron] [--walks walks.json] [--out <dir>]

For each walk (walkplan.py): the Golem's Admin moves the Player ("<Golem> the Tester") onto the start tile on Trammel,
the Player steps once onto the entrance, and the server's answer says where he stands. A walk passes when he lands
within 1 tile of the far end. --prep lines are typed by the Admin first (e.g. to set a re-placed teleporter's Z in a
world [TelGen has not been run on). Prints one line per walk and a JSON summary; the transcript goes to --out.
"""
import argparse
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--code', required=True)
    ap.add_argument('--host', default='127.0.0.1')
    ap.add_argument('--port', type=int, required=True)
    ap.add_argument('--golem', default='Iron')
    ap.add_argument('--walks', default=os.path.join(HERE, 'walks.json'))
    ap.add_argument('--prep', default='')
    ap.add_argument('--out', default=HERE)
    ap.add_argument('--steps', type=int, default=2)
    a = ap.parse_args()
    if not 2595 <= a.port <= 2599:
        sys.exit('private shards only (2595-2599)')
    sys.path.insert(0, os.path.join(a.code, 'tools', 'playtest-bot'))
    from uobot.client import Cliloc, Transcript
    from uobot.golemcheck import CLILOC, enter

    walks = json.load(open(a.walks))
    prep = json.load(open(a.prep)) if a.prep else []
    tr = Transcript(os.path.join(a.out, 'walk-transcript.txt'))
    cl = Cliloc(CLILOC)
    admin, _, _ = enter(a.golem, 'admin', a.host, a.port, tr, cl)
    player, _, pname = enter(a.golem, 'player', a.host, a.port, tr, cl)
    results = []
    try:
        for line in prep:
            replies = [str(m.get('text', '')) for m in admin.command(line, settle=1.5)]
            print('prep', line, '->', replies)
        for w in walks:
            if not w['start']:
                results.append(dict(w, ok=False, why='no start tile'))
                continue
            x, y, z = w['start']
            for cmd in ('[global set Map 1 where playermobile Name == "%s"' % pname,
                        '[global set Location (%d,%d,%d) where playermobile Name == "%s"' % (x, y, z, pname)):
                admin.command(cmd, settle=1.0)
            player.sleep(1.5)
            before = player.pos
            steps = player.walk(w['dir'], a.steps, pause=0.6)  # the first step may only turn
            player.sleep(2.5)
            after = player.pos
            dx, dy = w['dst'][0], w['dst'][1]
            ok = bool(after) and abs(after[0] - dx) <= 1 and abs(after[1] - dy) <= 1
            r = dict(w, before=list(before[:3]) if before else None, after=list(after[:3]) if after else None,
                     steps=steps, ok=ok)
            results.append(r)
            print('%s src %s dst %s: from %s stepped %d, now %s' % ('PASS' if ok else 'FAIL', w['src'], w['dst'],
                                                                    r['before'], steps, r['after']))
    finally:
        player.close()
        admin.close()
    json.dump(results, open(os.path.join(a.out, 'walk-results.json'), 'w'), indent=1)
    print(json.dumps({'walks': len(results), 'passed': sum(r['ok'] for r in results)}))


if __name__ == '__main__':
    main()
