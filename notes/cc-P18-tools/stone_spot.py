# Candidate tiles for the Reset Stone around the New Haven town square, checked with cc-P15's fit.py
# (port of pinned Map.CanFit / GetAverageZ over the client map, statics and pinned's New Haven decoration).
# Prints, per tile, the z's a mobile can stand at, and what static or decoration items sit on the tile.
import os
os.chdir(r'D:/UO/shard-migration/notes/cc-P15-tools')
exec(open('fit.py').read())

ARRIVAL = (3503, 2574, 14)   # CharacterCreation New Haven start; Sir Helper
BOARD = (3502, 2573, 14)     # NewHavenQuestBoard.HomeLocation

for y in range(2570, 2579):
    row = []
    for x in range(3498, 3509):
        s = surfaces(x, y)
        tiles = [(sid, sz) for (sid, sx, sy, sz, hue) in M.statics(x >> 3, y >> 3) if (x & 7, y & 7) == (sx, sy)]
        tiles += DECO.get((x, y), [])
        mark = 'A' if (x, y) == ARRIVAL[:2] else 'B' if (x, y) == BOARD[:2] else ' '
        row.append(f'{x},{y}{mark} z{s} {"+" + str(len(tiles)) if tiles else ""}')
    print(' | '.join(row))

print()
for x, y in [(3504, 2573), (3505, 2573), (3504, 2572), (3501, 2573), (3505, 2574), (3504, 2575), (3501, 2575)]:
    tiles = [(hex(sid), T.sname[sid], sz) for (sid, sx, sy, sz, hue) in M.statics(x >> 3, y >> 3) if (x & 7, y & 7) == (sx, sy)]
    print((x, y), 'stand at', surfaces(x, y), 'canfit z14', canfit(x, y, 14, why=True), 'statics', tiles, 'deco', DECO.get((x, y), []))
