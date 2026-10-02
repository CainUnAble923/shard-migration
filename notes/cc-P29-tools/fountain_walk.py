# cc-P29 Part D: which tiles within coin range of the fountain a walking player reaches from the Underworld's
# entrances, under pinned's movement rules (walk.py), in the server's data and in EA's 7.0.117 data.
import sys
sys.path.insert(0, r'D:/UO/shard-migration/notes/cc-P29-tools')
from walk import *

FX, FY = 1121, 957
COMP = [(FX + dx, FY + dy) for dx in range(-2, 2) for dy in range(-2, 2)]  # FountainOfFortune.cs:33-60 offsets


def near(x, y):
    return min(max(abs(x - cx), abs(y - cy)) for cx, cy in COMP)


def report(label, w, starts, srcs):
    seen = walk(w, starts, srcs)
    inrange = sorted((near(x, y), x, y, seen[(x, y)][0]) for (x, y) in seen if near(x, y) <= 3)
    close = sorted((near(x, y), x, y, seen[(x, y)][0]) for (x, y) in seen if near(x, y) <= 8)
    print(f'{label}: {len(seen)} tiles reached; within 3 of a component: {[(x, y, z) for _, x, y, z in inrange]}')
    print(f'  nearest reached (distance, x, y, z): {close[:10]}')
    return seen, inrange


if __name__ == '__main__':
    entries, srcs = teleporters()
    print('entries into the Underworld box (teleporters.json):')
    for e in entries:
        print('  ', e)
    print('teleporters inside the box:', len(srcs))
    starts = sorted(set(e[2] for e in entries))
    for label, cd in (('server 7.0.114.40', SERVER), ('EA 7.0.117.0', EA)):
        seen, inrange = report(label, World(cd), starts, srcs)
        if inrange:
            d, x, y, z = inrange[0]
            print('  path tail:', path(seen, x, y)[-15:])
