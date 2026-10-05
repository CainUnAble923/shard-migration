# Read-only: count spawner entries per creature name in pinned Distribution/Data/Spawns.
import json, os, collections, sys
root = 'D:/UO/ModernUO-pinned/Distribution/Data/Spawns'
names = sys.argv[1].split(',')
res = {}
for sub in ('post-uoml', 'shared', 'uoml'):
    c = collections.Counter(); files = collections.defaultdict(set)
    for dp, dn, fn in os.walk(os.path.join(root, sub)):
        for f in fn:
            if not f.endswith('.json'): continue
            for sp in json.load(open(os.path.join(dp, f), encoding='utf-8')):
                for e in sp.get('entries', []):
                    n = e['name'].split()[0]
                    if n.lower() in [x.lower() for x in names]:
                        c[n.lower()] += 1; files[n.lower()].add(os.path.relpath(os.path.join(dp, f), root).replace(os.sep, '/'))
    res[sub] = (c, files)
for n in names:
    k = n.lower()
    print(f"{n:22s} post-uoml={res['post-uoml'][0][k]:4d} shared={res['shared'][0][k]:4d} uoml={res['uoml'][0][k]:4d}  ", ','.join(sorted(res['post-uoml'][1][k] | res['shared'][1][k]))[:150])
