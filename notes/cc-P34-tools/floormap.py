# cc-P34 read only: an ASCII map of one floor. # wall, D door static (rare; doors are items, see the list),
# t furniture, . floor (a Surface static or land within 2 of the floor z), ~ land/outside, space nothing.
import sys
exec(open('tiles.py').read().split("if __name__")[0])
def fmap(x0, y0, x1, y1, fz):
    print('      ' + ''.join(str((x // 10) % 10) if x % 10 == 0 else ' ' for x in range(x0, x1 + 1)))
    for y in range(y0, y1 + 1):
        line = ''
        for x in range(x0, x1 + 1):
            st = statics(x, y)
            w = [s for s, z in st if T.sflags[s] & WALL and fz - 3 <= z <= fz + 3]
            tb = [s for s, z in st if T.sflags[s] & IMP and not T.sflags[s] & WALL and fz - 3 <= z <= fz + 6]
            fl = [s for s, z in st if T.sflags[s] & SURF and fz - 3 <= z + calch(s) <= fz + 3]
            ln = abs(avgz(x, y) - fz) <= 2
            line += '#' if w else ('t' if tb else ('.' if fl else ('~' if ln else ' ')))
        print(y, line)
if __name__ == '__main__':
    x0, y0, x1, y1, fz = [int(v) for v in sys.argv[1:6]]
    fmap(x0, y0, x1, y1, fz)
