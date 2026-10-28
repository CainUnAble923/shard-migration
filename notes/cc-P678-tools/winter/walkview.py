r"""cc-P678 read only: soswalk's standing Z as characters. python -P walkview.py x1 y1 x2 y2
'#' blocked, '.' reachable on foot from the start, 'o' standable but not reachable; a second block gives z mod 10."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import soswalk
a = [int(v) for v in sys.argv[1:5]]
w = soswalk.Walk((3540, 2440, 3790, 2730))
fl = w.flood((3634, 2586))
for y in range(a[1], a[3] + 1):
    print('%4d ' % y + ''.join('#' if w.stand.get((x, y)) is None else ('.' if (x, y) in fl else 'o') for x in range(a[0], a[2] + 1))
          + '  ' + ''.join('#' if w.stand.get((x, y)) is None else str(w.stand[(x, y)] // 10 % 10) for x in range(a[0], a[2] + 1)))
