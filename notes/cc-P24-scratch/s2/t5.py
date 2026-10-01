import json, numpy as np, glob, os, re
P='D:/UO/ModernUO-pinned/Distribution/Data/'
regs=json.load(open(P+'regions.json'))
H,W=4096,7168
regmask=np.zeros((H,W),bool)
tram=[]
def walk(r, parent=None):
    if r.get('Map')=='Trammel' or (parent and parent.get('Map')=='Trammel'):
        for a in r.get('Area',[]):
            tram.append((r.get('Name','?'), r.get('$type','?'), a['x1'],a['y1'],a['x2'],a['y2']))
            regmask[max(0,a['y1']):min(H,a['y2']+1), max(0,a['x1']):min(W,a['x2']+1)]=True
    for c in r.get('Children',[]) or []:
        if 'Map' not in c: c['Map']=r.get('Map')
        walk(c, r)
for r in regs: walk(r)
print('trammel region rects', len(tram), 'region names', len(set(t[0] for t in tram)))
json.dump(tram, open('tram_regions.json','w'))
# teleporters / spawns / decoration points on Trammel
pts=[]
for t in json.load(open(P+'teleporters.json')):
    for k in ('src','dst'):
        if t[k]['map']=='Trammel': pts.append(('tele',t[k]['loc'][0],t[k]['loc'][1]))
# spawns: json files with map + location
for f in glob.glob(P+'Spawns/**/*.json', recursive=True):
    try: d=json.load(open(f, encoding='utf-8-sig'))
    except Exception as e: continue
    for s in d if isinstance(d,list) else []:
        if s.get('map')=='Trammel' and 'location' in s:
            l=s['location']; pts.append(('spawn:'+os.path.basename(f), l[0], l[1]))
# decoration: text cfg files lines "x y z" under Trammel/ and Britannia/
for f in glob.glob(P+'Decoration/Trammel/*')+glob.glob(P+'Decoration/Britannia/*'):
    for line in open(f, errors='ignore'):
        m=re.match(r'^\s*(\d+)\s+(\d+)\s+(-?\d+)', line)
        if m: pts.append(('deco:'+os.path.basename(f), int(m.group(1)), int(m.group(2))))
print('points', len(pts))
json.dump(pts, open('tram_points.json','w'))
ptmask=np.zeros((H,W),bool)
for _,x,y in pts:
    if 0<=x<W and 0<=y<H: ptmask[y,x]=True
np.save('regmask.npy',regmask); np.save('ptmask.npy',ptmask)
