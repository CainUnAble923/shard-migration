# cc-P237 read only: ASCII floor maps (P = protected, # wall, D door, t furniture, . floor) and the north-wall art
# candidates of a room: a floor tile at z whose north neighbour has a wall at that floor and that is not protected.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nhbase as B, protected as PR
F = B.Facet(1)
def north_wall_tiles(x0, y0, x1, y1, fz):
    out = []
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            s = F.top_surface(x, y, fz + 2)
            if s is None or abs(s - fz) > 2 or (x, y) in PR.P or F.blocked(x, y, s): continue
            if F.wall_at(x, y - 1, fz): out.append((x, y, s))
    return out
if __name__ == '__main__':
    x0, y0, x1, y1, fz = map(int, sys.argv[1:6])
    print(B.floormap(F, x0, y0, x1, y1, fz, protected=PR.P))
    print('north-wall art tiles:', north_wall_tiles(x0, y0, x1, y1, fz))
