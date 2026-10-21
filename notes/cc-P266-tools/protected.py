# cc-P266 read only: every tile in New Haven that no winter row may use, and why. cc-P237's sources
# (notes/cc-P237-tools/protected.py), with this task's own generated table left out and P237's own table put IN:
#   door      ClusterFNewHavenServicesSeeder.Decoration doors (ServUO NewHaven.cfg) and pinned DoorGenerator's scan
#             (nhbase.generated_doors), each with its swing tile (pinned BaseDoor.GetOffset, BaseDoor.cs:13-28)
#   seeded    every coordinate literal x, y inside the box in any server/customizations .cs file but
#             ClusterFWinterDecorLayout.cs (NPC posts, the board, the arrival tile, the Reset Stone, the office, the
#             guild halls, the quest givers, P237's community art rows, P267's Halloween bank rows...): a tile some
#             other seeder names is never used. The winter table's own rows are checked against each other by
#             validate.py (one row per tile and z).
#   spawner   every pinned spawner (shared and post-uoml) on Trammel in the box, the tile and its 8 neighbours
#   decor     every pinned Decoration cfg item on Trammel in the box (Britannia and Trammel folders)
#   tele      every teleporter end in the box
#   path      P188's walk from New Haven's east edge to the Rootdeep hole (notes/cc-P188-tools/walk-report.json)
import os, re, glob, json, sys
HERE = os.path.dirname(os.path.abspath(__file__))
P237 = os.path.join(HERE, '..', 'cc-P237-tools')
sys.path.append(P237)   # after this folder: P237 has an art_src.py of its own
import nhbase as B

CUS = 'D:/UO/golems/Bronze/ShatteredLegacy/server/customizations'
BOX = (3400, 2460, 3660, 2660)
def inbox(x, y): return BOX[0] <= x <= BOX[2] and BOX[1] <= y <= BOX[3]
P = {}
def add(x, y, why):
    if inbox(x, y): P.setdefault((x, y), []).append(why)

F = B.Facet(1)
src = open(CUS + '/ClusterFNewHavenServicesSeeder.cs', encoding='utf-8').read()
SEEDED_DOORS = set()
for m in re.finditer(r'new\("(\w+) 0x[0-9A-F]+ \(Facing=(\w+)\)", (\d+), (\d+), (-?\d+)\)', src):
    t, f, x, y = m.group(1), m.group(2), int(m.group(3)), int(m.group(4))
    if 'Door' in t:
        SEEDED_DOORS.add((x, y))
        add(x, y, 'door %s %s' % (t, f)); dx, dy = B.SWING[f]; add(x + dx, y + dy, 'swing of door %d,%d' % (x, y))
# pinned DoorGenerator's scan guesses a facing from the frames; where the shard's own seeder places a door on that
# tile, the seeded door (and its swing, above) is the real one, and the scan's guess is left out (P266: the scan put
# the inn's front door swing on 3510,2519, where P34 hung the mistletoe knowing the seeded door swings to 3509,2517).
for (x, y, z, f) in B.generated_doors(F, *BOX):
    if (x, y) in SEEDED_DOORS: continue
    add(x, y, 'doorgen %s z%d' % (f, z)); dx, dy = B.SWING[f]; add(x + dx, y + dy, 'swing of doorgen %d,%d' % (x, y))
OWN = ('ClusterFWinterDecorLayout.cs',)   # this task's own generated table is not a protection source
for f in glob.glob(CUS + '/**/*.cs', recursive=True):
    if os.path.basename(f) in OWN: continue
    for m in re.finditer(r'\b(3[4-6]\d\d),\s*(2[4-6]\d\d)\b', open(f, encoding='utf-8', errors='replace').read()):
        add(int(m.group(1)), int(m.group(2)), 'seeded %s' % os.path.relpath(f, CUS).replace('\\', '/'))
for (mp, x, y, z, hr, names, fn) in B.spawns_in('Trammel', BOX[0] - 2, BOX[1] - 2, BOX[2] + 2, BOX[3] + 2):
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            add(x + dx, y + dy, 'spawner %s at %d,%d home %d (%s)' % ('/'.join(n for n in names if n)[:40], x, y, hr, fn))
for (x, y, z, t, i, fn) in B.decoration_in(1, *BOX):
    add(x, y, 'decor %s %s (%s)' % (t, i, fn))
for (x, y, z, end) in B.teleporters_in('Trammel', *BOX):
    add(x, y, 'teleporter %s' % end)
_walk = json.load(open(os.path.join(HERE, '..', 'cc-P188-tools', 'walk-report.json')))
PATH = [tuple(p) for p in _walk['after']['path']]
for (x, y) in PATH: add(x, y, 'P188 way-in path')

if __name__ == '__main__':
    kinds = {}
    for v in P.values():
        for w in set(s.split()[0] for s in v): kinds[w] = kinds.get(w, 0) + 1
    print(len(P), 'protected tiles', kinds, 'path', len(PATH))
    print('P237 community art rows protected:', sum(1 for v in P.values() if any('ClusterFCommunityArtLayout' in s for s in v)))
