# cc-P237 read only: the road to the Rootdeep way in, P188's walk (yellow) and spawner boxes (orange marks).
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rend, protected as PR, nhbase as B
F = rend.F
x0, y0, x1, y1 = 3545, 2570, 3625, 2640
marks = [('', x, y, F.top_surface(x, y) or 0, (255, 255, 0, 255)) for (x, y) in PR.PATH if x0 <= x <= x1 and y0 <= y <= y1]
for s in B.spawns_in('Trammel', x0 - 20, y0 - 20, x1 + 20, y1 + 20):
    if s[4] < 50:
        marks.append(('spawn %s hr%d' % (s[5][0], s[4]), s[1], s[2], s[3], (255, 128, 0, 255)))
print(B.render(F, x0, y0, x1, y1, marks=marks, grid=5, out=os.path.join(rend.HERE, 'preview-camp-road.png'), scale=0.6))
