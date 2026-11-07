"""cc-P814: isorenders of the moved signs on each land. python -u -P -W ignore notes/cc-P814-tools/render_signs.py"""
import os, sys
sys.path.insert(0, 'notes/cc-P708-tools/p281sos')
import hallbase as H
for client, x, y, z, out in (('D:/UO/tool-trials/client-data-copy', 3471, 2588, 10, 'render-stop1-sign.jpg'),
                             ('D:/UO/golems/Iron/p708-work/sosclient', 3609, 2614, 0, 'render-main-stables-sign.jpg')):
    H.CLIENT = H.uofiles.CLIENT = client
    H.uofiles._TD.clear() if hasattr(H.uofiles, '_TD') else None
    F = H.Facet(1)
    H.render(F, x - 10, y - 10, x + 10, y + 10, extra=[(0xA854, x, y, z)], grid=0, out='notes/cc-P814-review/' + out)
