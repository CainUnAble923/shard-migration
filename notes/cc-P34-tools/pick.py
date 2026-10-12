# cc-P34 read only: candidate tiles. floor(cx, cy, r, z): free tiles near a point; wallart(box, z): tiles whose north or
# west neighbour is a wall at that floor (north wall: art faces south; west wall: art faces east, the visible faces).
exec(open('tiles.py').read().split("if __name__")[0])
exec(open('protected.py').read().split("if __name__")[0])
def wall_at(x, y, z): return any(T.sflags[s] & WALL and z - 3 <= sz <= z + 3 for s, sz in statics(x, y))
def free(x, y, z, allow_walkway=False):
    s = top_surface(x, y, z + 2)
    if s is None or abs(s - z) > 2: return False, 'no surface at z'
    if blocked(x, y, z): return False, 'blocked ' + blocked(x, y, z)
    if (x, y) in P: return False, 'protected ' + '; '.join(P[(x, y)])
    if not allow_walkway and walkway(x, y, z): return False, 'walkway ' + walkway(x, y, z)
    return True, ''
def floor(cx, cy, r, z, allow_walkway=False, n=12):
    out = []
    for y in range(cy - r, cy + r + 1):
        for x in range(cx - r, cx + r + 1):
            ok, why = free(x, y, z, allow_walkway)
            if ok: out.append(((x - cx) ** 2 + (y - cy) ** 2, x, y, top_surface(x, y, z + 2)))
    return sorted(out)[:n]
def wallart(x0, y0, x1, y1, z):
    out = []
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            s = top_surface(x, y, z + 2)
            if s is None or abs(s - z) > 2 or (x, y) in P: continue
            if wall_at(x, y - 1, z): out.append((x, y, s, 'north'))
            if wall_at(x - 1, y, z): out.append((x, y, s, 'west'))
    return out
