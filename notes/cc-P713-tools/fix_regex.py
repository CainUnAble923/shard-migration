"""cc-P713: the README regex line, written with raw strings (shell quoting halved its backslashes)."""
import sys

p = sys.argv[1]
s = open(p, 'rb').read().decode('ascii')
lines = s.split('\n')
idx = [i for i, l in enumerate(lines) if l.lstrip().startswith('$rmRx = [regex]')]
assert len(idx) == 1, idx
lines[idx[0]] = r"""    $rmRx = [regex]'(?m)^  app\\map\\ [^\r\n]*\r?\n(?: {15}[^\r\n]*\r?\n)*'"""
open(p, 'wb').write('\n'.join(lines).encode('ascii'))
print(lines[idx[0]])
