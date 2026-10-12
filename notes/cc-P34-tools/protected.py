# cc-P34 read only: every tile no decor row may use, from the sources that put something there.
#   doors     ClusterFNewHavenServicesSeeder.Decoration (ServUO NewHaven.cfg), each door tile and its swing tile
#             (the tile + pinned BaseDoor.GetOffset(facing), UOContent/Items/Construction/Doors/BaseDoor.cs:13-28, :240)
#   npc       ClusterFNewHavenSeeder.Entries and ClusterFInstitutionSeeder (their x, y), the healer spawner tile
#   spawner   every pinned Distribution/Data/Spawns entry on Trammel inside New Haven's box
#   fixed     the quest board 3502,2573, the arrival tile 3503,2574, the Reset Stone 3501,2575
#   office    ClusterFRegistrarOfficeLayout components (cc-P19/P31)
import re, json, glob, os
CUS = r'D:/ShatteredLegacy/server/customizations'
OFF = {'WestCW': (-1, 1), 'EastCCW': (1, 1), 'WestCCW': (-1, 0), 'EastCW': (1, -1), 'SouthCW': (1, 1),
       'NorthCCW': (1, -1), 'SouthCCW': (0, 0), 'NorthCW': (0, -1)}
BOX = (3400, 2460, 3560, 2660)
def inbox(x, y): return BOX[0] <= x <= BOX[2] and BOX[1] <= y <= BOX[3]
P = {}
def add(x, y, why): P.setdefault((x, y), []).append(why)
src = open(CUS + '/ClusterFNewHavenServicesSeeder.cs').read()
for m in re.finditer(r'new\("(\w+) 0x[0-9A-F]+ \(Facing=(\w+)\)", (\d+), (\d+), (-?\d+)\)', src):
    t, f, x, y, z = m.group(1), m.group(2), int(m.group(3)), int(m.group(4)), int(m.group(5))
    if 'Door' in t:
        add(x, y, 'door %s %s z%d' % (t, f, z)); dx, dy = OFF[f]; add(x + dx, y + dy, 'swing of door %d,%d %s' % (x, y, f))
for m in re.finditer(r'typeof\((\w+)\).*?(\d{4}), (\d{4}), Direction\.', open(CUS + '/ClusterFNewHavenSeeder.cs').read()):
    add(int(m.group(2)), int(m.group(3)), 'npc %s' % m.group(1))
for m in re.finditer(r'(\d{4}),\s*(\d{4}),\s*Z=(\d+)', open(CUS + '/ClusterFInstitutionSeeder.cs').read()):
    add(int(m.group(1)), int(m.group(2)), 'npc institution')
add(3462, 2559, 'spawner healer (ClusterFNewHavenServicesSeeder.HealerSpawnerLocation)')
for f in glob.glob(r'D:/UO/ModernUO-pinned/Distribution/Data/Spawns/**/*.json', recursive=True):
    try: d = json.load(open(f))
    except Exception: continue
    for e in d if isinstance(d, list) else []:
        loc = e.get('location')
        if e.get('map') == 'Trammel' and loc and inbox(loc[0], loc[1]):
            add(loc[0], loc[1], 'spawner %s (%s)' % (e.get('name'), os.path.relpath(f, r'D:/UO/ModernUO-pinned/Distribution/Data')))
add(3502, 2573, 'quest board'); add(3503, 2574, 'arrival tile (Sir Helper)'); add(3501, 2575, 'Reset Stone')
for m in re.finditer(r'new\("(\w+)", 0x[0-9A-F]+, "([^"]+)", (\d+), (\d+), (-?\d+)\)', open(CUS + '/ClusterFRegistrarOfficeLayout.cs').read()):
    add(int(m.group(3)), int(m.group(4)), 'office %s %s' % (m.group(1), m.group(2)))
if __name__ == '__main__':
    kinds = {}
    for k, v in P.items():
        for w in v: kinds[w.split()[0]] = kinds.get(w.split()[0], 0) + 1
    print(len(P), 'tiles', kinds)
