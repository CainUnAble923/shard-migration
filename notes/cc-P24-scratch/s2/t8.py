import xml.etree.ElementTree as ET, json
C={'A':(5128,1120,5255,1271),'B':(5520,1416,5623,1527),'C':(6152,1816,6647,2303),'D':(6488,1544,6807,1799),'E':(6664,768,7159,1151)}
root=ET.parse('D:/UO/ServUO-pub57/Data/Regions.xml').getroot()
def ov(r,c): return not (r[2]<c[0] or r[0]>c[2] or r[3]<c[1] or r[1]>c[3])
for facet in root.findall('Facet'):
    fn=facet.get('name')
    for reg in facet.iter('region'):
        for rect in reg.findall('rect'):
            g=rect.get
            if g('x') is not None and g('width') is not None:
                x,y=int(g('x')),int(g('y')); r=(x,y,x+int(g('width'))-1,y+int(g('height'))-1)
            elif g('x1') is not None or g('x') is not None:
                x1=g('x1') or g('x'); y1=g('y1') or g('y')
                r=(int(x1),int(y1),int(g('x2') or g('width')),int(g('y2') or g('height')))
            else: continue
            for k,c in C.items():
                cc=(c[0]-20,c[1]-20,c[2]+20,c[3]+20)
                if ov(r,cc): print('ServUO',fn,k,reg.get('name'),reg.get('type'),r)
# pinned other facets
for r in json.load(open('D:/UO/ModernUO-pinned/Distribution/Data/regions.json')):
    for a in r.get('Area',[]):
        rr=(a['x1'],a['y1'],a['x2'],a['y2'])
        for k,c in C.items():
            if ov(rr,(c[0]-20,c[1]-20,c[2]+20,c[3]+20)): print('pinned',r.get('Map'),k,r.get('Name'),r.get('$type'),rr)
