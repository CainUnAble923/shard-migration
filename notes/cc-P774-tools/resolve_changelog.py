# cc-P774: resolves the CHANGELOG.md and VERSION conflicts of merging golem/Iron/P763 into golem/Iron/P774 (main).
# main's sections stay as they are; P763's section becomes the newest version, 2026.11.02.4 (P715's branch holds .3).
import re, sys
root = r'D:\UO\golems\Iron\ShatteredLegacy'
ver = '2026.11.02.4'
p = root + r'\CHANGELOG.md'
t = open(p, encoding='utf-8', newline='').read()
nl = '\r\n' if '\r\n' in t[:3000] else '\n'
m = re.search(r'<<<<<<< HEAD\r?\n(.*?)\r?\n=======\r?\n(.*?)\r?\n>>>>>>> golem/Iron/P763\r?\n', t, re.S)
if not m: print('no conflict block'); sys.exit(1)
ours, theirs = m.group(1), m.group(2)
if not theirs.startswith('## 2026.11.01.4'): print('unexpected P763 side'); sys.exit(1)
theirs = '## ' + ver + theirs[len('## 2026.11.01.4'):]
t = t[:m.start()] + theirs + nl + nl + ours + nl + t[m.end():]
if '<<<<<<<' in t or '>>>>>>>' in t: print('markers left'); sys.exit(1)
open(p, 'w', encoding='utf-8', newline='').write(t)
v = root + r'\VERSION'
vt = open(v, encoding='utf-8', newline='').read()
open(v, 'w', encoding='utf-8', newline='').write(ver + ('\r\n' if '\r\n' in vt else '\n'))
print('resolved')
