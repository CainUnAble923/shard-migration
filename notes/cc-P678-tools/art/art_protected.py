# cc-P678 read only: cc-P237-tools/protected.py on SoS Haven: every tile no community-art row may use, and why.
# P237's sources, each read for the new town:
#   door      pinned DoorGenerator's scan on the SoS statics (sosbase.generated_doors) and SoS statics flagged Door,
#             each with its swing tile (BaseDoor.GetOffset). (P237's other door source, ClusterFNewHavenServicesSeeder's
#             ServUO NewHaven.cfg doors, is the old plaza's and lies outside this box.)
#   seeded    every coordinate literal x, y inside the box in any Iron server/customizations .cs file, but this task's
#             own table (the Halloween rows, HavenSpots, our seeders...)
#   spawner   every pinned spawner on Trammel in the box, every folder (uoml too: SoS Haven is OSI's pre-UOML Haven),
#             the tile and its 8 neighbours
#   decor     every pinned Decoration cfg item on Trammel in the box (Britannia and Trammel folders)
#   tele      every teleporter end in the box
#   kept      p678_extra.kept_clear(): every HavenSpots spot, every homes.csv NPC tile, the Rootdeep hatch (8 round each)
#   path      the way in: soswalk's walk from New Haven's start (3634,2586) to the Rootdeep hatch in the Second Bank
#             (3619,2620). It stands for P188's walk from New Haven to the old Rootdeep hole, which SoS has no more.
import os, re, glob, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import sosbase as B
import p678_extra as X

CUS = 'D:/UO/golems/Iron/ShatteredLegacy/server/customizations'
BOX = (3520, 2440, 3790, 2720)
def inbox(x, y): return BOX[0] <= x <= BOX[2] and BOX[1] <= y <= BOX[3]
P = {}
def add(x, y, why):
    if inbox(x, y): P.setdefault((x, y), []).append(why)

F = B.sos()
for (x, y, z, f) in B.generated_doors(F, *BOX):
    add(x, y, 'doorgen %s z%d' % (f, z)); dx, dy = B.SWING[f]; add(x + dx, y + dy, 'swing of doorgen %d,%d' % (x, y))
for (x, y, z, sid) in B.static_doors(F, *BOX):
    add(x, y, 'door static 0x%04X' % sid)
OWN = ('ClusterFCommunityArtLayout.cs',)
for f in glob.glob(CUS + '/**/*.cs', recursive=True):
    if os.path.basename(f) in OWN: continue
    for m in re.finditer(r'\b(3[3-7]\d\d),\s*(2[3-7]\d\d)\b', open(f, encoding='utf-8', errors='replace').read()):
        add(int(m.group(1)), int(m.group(2)), 'seeded %s' % os.path.relpath(f, CUS).replace('\\', '/'))
for (mp, x, y, z, hr, wr, names, fn) in B.spawns_all():
    if not inbox(x, y): continue
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            add(x + dx, y + dy, 'spawner %s at %d,%d home %d (%s)' % ('/'.join(n for n in names if n)[:40], x, y, hr, fn))
for (x, y, z, t, i, fn) in B.decoration_in(1, *BOX):
    add(x, y, 'decor %s %s (%s)' % (t, i, fn))
for (x, y, z, end) in B.teleporters_in('Trammel', *BOX):
    add(x, y, 'teleporter %s' % end)
for (x, y), whys in X.kept_clear().items():
    for w in sorted(set(whys)): add(x, y, w)
PATH = X.walk().path(X.START, X.HATCH) or []
assert PATH, 'no walk from the start to the hatch'
for (x, y) in PATH: add(x, y, 'the way in (start to the Rootdeep hatch)')

if __name__ == '__main__':
    kinds = {}
    for v in P.values():
        for w in set(s.split()[0] for s in v): kinds[w] = kinds.get(w, 0) + 1
    print(len(P), 'protected tiles', kinds, 'path', len(PATH))
