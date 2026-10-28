"""cc-P677: a copy of notes/cc-P16-tools/gen_layout.py that reads and writes this Golem's work copy (the original names
the main checkout, another desk). Writes notes/cc-P677-tools/gen_layout.py."""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, '..', 'cc-P16-tools', 'gen_layout.py'), encoding='utf-8').read()
new, n = re.subn(r"^ROOT = r'[^']*'", "ROOT = r'D:/UO/golems/Iron/ShatteredLegacy'  # cc-P677: this Golem's work copy",
                 src, count=1, flags=re.M)
assert n == 1
open(os.path.join(HERE, 'gen_layout.py'), 'w', encoding='utf-8', newline='\n').write(new)
print('ok')
