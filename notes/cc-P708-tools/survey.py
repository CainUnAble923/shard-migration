"""cc-P708: P281's pick.propose (the main floor, doors, a travel stop outside the main door, guildmaster candidates and a
floor map) for any rectangle on the SoS land, through the P708 copy of the hall tools (p281sos: today's patch, our
decoration and SoS spawners).
    python -P survey.py name x1 y1 x2 y2 [z] [doorx,doory]   -> out/survey-<name>.txt, and the head on stdout
Read only.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'p281sos'))
os.chdir(os.path.join(HERE, 'p281sos'))
import pick  # noqa: E402

name = sys.argv[1]
rect = tuple(int(v) for v in sys.argv[2:6])
z = int(sys.argv[6]) if len(sys.argv) > 6 and sys.argv[6] != '-' else None
door = tuple(int(v) for v in sys.argv[7].split(',')) if len(sys.argv) > 7 else None
t = pick.propose(name, 1, rect, 'reuse', z=z, door=door)
os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
open(os.path.join(HERE, 'out', 'survey-%s.txt' % name), 'w').write(t + '\n')
print(t)
