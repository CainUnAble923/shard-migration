"""cc-P803: stamp Walk803.py for one run. python -P make_walk.py <release|main> <phase> <character> <out.py>"""
import sys, re
which, phase, char, out = sys.argv[1:5]
s = open(__file__.replace("make_walk.py", "Walk803.py")).read()
s = s.replace('CHARACTER = "Iron Stock"', 'CHARACTER = "%s"' % char)
s = s.replace("RELEASE = True", "RELEASE = %s" % (which == "release"))
s = s.replace('PHASE = "before"', 'PHASE = "%s"' % phase)
open(out, "w").write(s)
print(out)
