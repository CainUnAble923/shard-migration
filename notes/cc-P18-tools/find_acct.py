"""For each `GetOrCreate(<acct>)` that is not already followed by a guild/starter accessor, print
the nearest line above it that defines <acct> (assignment, pattern, or parameter)."""
import re
import sys

SITE = re.compile(r'ClusterFAccountPersistence\.GetOrCreate\(([^()]*(?:\([^()]*\))?[^()]*)\)(?!\.GetOrCreate)')

for f in sys.argv[1:]:
    lines = open(f, encoding='utf-8').read().split('\n')
    for i, line in enumerate(lines):
        for m in SITE.finditer(line):
            arg = m.group(1).strip()
            name = re.sub(r'[^A-Za-z_].*$', '', arg.split(')')[-1]) or arg
            defn = None
            for j in range(i, max(-1, i - 80), -1):
                l = lines[j]
                if re.search(r'\b' + re.escape(name) + r'\b\s*=[^=]', l) or \
                   re.search(r'IAccount\??\s+' + re.escape(name) + r'\b', l) or \
                   re.search(r'is\s+(not\s+)?IAccount\s+' + re.escape(name) + r'\b', l):
                    defn = (j + 1, l.strip())
                    break
            print(f'{f}:{i + 1}: [{arg}]  <-  {defn}')
