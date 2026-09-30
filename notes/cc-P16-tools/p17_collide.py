# cc-P16 (read only): do any of P17's 125 New Haven decoration entries, or its Healer spawner, fall on or
# near a mine-camp component tile or NPC destination? Parses ClusterFNewHavenServicesSeeder.cs.
import re, json
src = open(r'D:/ShatteredLegacy/server/customizations/ClusterFNewHavenServicesSeeder.cs').read()
ents = [(h, int(x), int(y), int(z)) for h, x, y, z in re.findall(r'new\("([^"]+)",\s*(-?\d+),\s*(-?\d+),\s*(-?\d+)\)', src)]
L = json.load(open(r'D:/ShatteredLegacy/design/mine-camp-tents/layout.json'))
tiles = {(c['x'], c['y']) for a in L['addons'] for c in a['components']} | {tuple(n['to'][:2]) for n in L['npcs']}
print('decoration entries parsed:', len(ents))
best = min(((max(abs(x - tx), abs(y - ty)), h, x, y, z, tx, ty) for h, x, y, z in ents for tx, ty in tiles))
print('exact collisions:', [e for e in ents if (e[1], e[2]) in tiles])
print('nearest entry to any camp tile (Chebyshev tiles, entry, camp tile):', best)
print('max y of any entry:', max(e[2] for e in ents), '; camp tiles y range:', min(t[1] for t in tiles), '-', max(t[1] for t in tiles))
m = re.search(r'Point3D\((\d+),\s*(\d+),\s*(\d+)\)', src[src.find('Healer'):])
print('first Point3D after "Healer" in the file (the Healer spawner tile):', m.groups() if m else None)
