# cc-P715: the CHANGELOG ops line (a Staff list in a new version section) and VERSION, in Iron's code copy.
import sys

root = r'D:\UO\golems\Iron\ShatteredLegacy'
cl = root + r'\CHANGELOG.md'
ver = '2026.11.02.3'
line = ("- A Golem's question to Chase now stays open on the Golem card until it is answered, retried, cleared or the prompt "
        "moves on. Before, a stopped session that woke once more for its own background task (a watcher ending) looked "
        "like Chase answering, so the question closed before he saw it and his answer was refused.")
t = open(cl, encoding='utf-8', newline='').read()
if line in t:
    print('already there'); sys.exit(0)
nl = '\r\n' if '\r\n' in t[:3000] else '\n'
anchor = nl + '## 2026.11.02.2' + nl
i = t.index(anchor)
t = t[:i] + nl + '## ' + ver + nl + nl + '### Staff' + nl + line + nl + t[i:]
open(cl, 'w', encoding='utf-8', newline='').write(t)
v = root + r'\VERSION'
old = open(v, encoding='utf-8', newline='').read()
vnl = '\r\n' if old.endswith('\r\n') else '\n'
open(v, 'w', encoding='utf-8', newline='').write(ver + vnl)
print('added')
