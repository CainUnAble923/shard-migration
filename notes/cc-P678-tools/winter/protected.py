# cc-P678 read only: every tile in SoS Haven that no winter row may use, and why. cc-P266's protected.py with its
# sources moved to the new town (box 3540-3790, 2440-2730):
#   door      pinned Decoration/Trammel haven.cfg and "_haven additions.cfg" doors (the town's stock doors, items on
#             Trammel), each with its swing tile (pinned BaseDoor.GetOffset), and pinned DoorGenerator's scan of the SoS
#             statics (sosbase.generated_doors) with its guessed swing, where no cfg door stands on the tile
#   seeded    every coordinate literal x, y inside the box in any server/customizations .cs file of the code copy but
#             ClusterFWinterDecorLayout.cs (HavenSpots: the arrival tile, the Reset Stone, Rook, the board; the NPC
#             posts; the community art and Halloween rows, the office...). Read fresh on every run, so a seeder another
#             helper moves into the town is seen.
#   home      P678's NPC homes (notes/cc-P678-tools/out/homes.csv), whose seeders may not be written yet
#   spawner   every pinned spawner (shared, uoml and post-uoml) on Trammel in the box, the tile and its 8 neighbours
#   decor     every pinned Decoration cfg item on Trammel in the box (Britannia and Trammel folders)
#   tele      every teleporter end in the box
#   fountain  the Fountain of Youth's 4 x 4 addon (HavenSpots) and a ring of one
#   hatch     the Rootdeep way down on SoS (3619,2620 in the Second Bank, the P678 notes' part 4) and its 8 neighbours
# P266's "P188 way-in path" source is the old map's walk to the old hole; it has no SoS counterpart yet (S2).
import os, re, glob, json, sys, csv
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sosbase as B

CUS = 'D:/UO/golems/Iron/ShatteredLegacy/server/customizations'
PINNED = 'D:/UO/ModernUO-pinned/Distribution/Data'
HOMES = os.path.join(os.path.dirname(HERE), 'out', 'homes.csv')
BOX = B.BOX
def inbox(x, y): return BOX[0] <= x <= BOX[2] and BOX[1] <= y <= BOX[3]
P = {}
def add(x, y, why):
    if inbox(x, y): P.setdefault((x, y), []).append(why)

F = B.facet()

# ---- the decoration cfgs (doors with their facings, and every other item)
CFG_DOORS = set()
LAMPS = {}   # (x, y) -> z of every pinned cfg lamp post (the post rows hang on them)
for folder in ('Britannia', 'Trammel'):
    for f in glob.glob(PINNED + '/Decoration/%s/*.cfg' % folder):
        head = None
        for line in open(f, encoding='latin1'):
            line = line.strip()
            if not line or line.startswith('#'): continue
            m = re.match(r'^(\d+)\s+(\d+)\s+(-?\d+)', line)
            if m and head:
                x, y = int(m.group(1)), int(m.group(2))
                if not inbox(x, y): continue
                add(x, y, 'decor %s (%s)' % (head[0], os.path.basename(f)))
                if head[0].startswith('LampPost'): LAMPS[(x, y)] = int(m.group(3))
                fm = re.search(r'Facing=(\w+)', head[1])
                if ('Door' in head[0] or 'Gate' in head[0]) and fm:
                    CFG_DOORS.add((x, y))
                    add(x, y, 'door %s %s' % (head[0], fm.group(1)))
                    dx, dy = B.SWING[fm.group(1)]
                    add(x + dx, y + dy, 'swing of door %d,%d' % (x, y))
            elif re.match(r'^[A-Za-z]', line):
                parts = line.split(None, 1)
                head = (parts[0], parts[1] if len(parts) > 1 else '')
for (x, y, z, f) in B.generated_doors(F, *BOX):
    if (x, y) in CFG_DOORS: continue
    add(x, y, 'doorgen %s z%d' % (f, z)); dx, dy = B.SWING[f]; add(x + dx, y + dy, 'swing of doorgen %d,%d' % (x, y))

# ---- every seeded literal but the winter table's own
OWN = ('ClusterFWinterDecorLayout.cs',)
for f in glob.glob(CUS + '/**/*.cs', recursive=True):
    if os.path.basename(f) in OWN: continue
    for m in re.finditer(r'\b(3[5-7]\d\d),\s*(2[4-7]\d\d)\b', open(f, encoding='utf-8', errors='replace').read()):
        add(int(m.group(1)), int(m.group(2)), 'seeded %s' % os.path.relpath(f, CUS).replace('\\', '/'))

for r in csv.DictReader(open(HOMES)):
    add(int(r['x']), int(r['y']), 'home %s %s' % (r['kind'], r['name']))

# ---- pinned spawners, all three sets, and their ring
SPAWNERS = set()
for f in glob.glob(PINNED + '/Spawns/**/*.json', recursive=True):
    try: d = json.load(open(f, encoding='utf-8-sig'))
    except Exception: continue
    for e in d if isinstance(d, list) else []:
        loc = e.get('location')
        if e.get('map') != 'Trammel' or not loc: continue
        if not (BOX[0] - 2 <= loc[0] <= BOX[2] + 2 and BOX[1] - 2 <= loc[1] <= BOX[3] + 2): continue
        SPAWNERS.add((loc[0], loc[1]))
        names = '/'.join((x.get('name') or '') for x in (e.get('entries') or []))[:40]
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                add(loc[0] + dx, loc[1] + dy, 'spawner %s at %d,%d (%s)' % (names, loc[0], loc[1], os.path.relpath(f, PINNED).replace('\\', '/')))

for t in json.load(open(PINNED + '/teleporters.json')):
    for end in ('src', 'dst'):
        e = t[end]
        if e['map'] == 'Trammel': add(e['loc'][0], e['loc'][1], 'teleporter %s' % end)

for dx in (-1, 0, 1):
    for dy in (-1, 0, 1):
        add(3619 + dx, 2620 + dy, 'Rootdeep hatch 3619,2620')

# the Fountain of Youth's addon (HavenSpots.FountainOfYouth, pinned StoneFountainAddon offsets -2..+1) and a ring
_fm = re.search(r'FountainOfYouth = new\((\d+), (\d+)', open(CUS + '/Tutorial/HavenSpots.cs').read())
FOUNTAIN = (int(_fm.group(1)), int(_fm.group(2)))
for dx in range(-3, 3):
    for dy in range(-3, 3):
        add(FOUNTAIN[0] + dx, FOUNTAIN[1] + dy, 'Fountain of Youth %d,%d and its ring' % FOUNTAIN)

if __name__ == '__main__':
    kinds = {}
    for v in P.values():
        for w in set(s.split()[0] for s in v): kinds[w] = kinds.get(w, 0) + 1
    print(len(P), 'protected tiles', kinds, 'spawners', len(SPAWNERS))
