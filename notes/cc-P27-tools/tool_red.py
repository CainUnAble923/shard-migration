# cc-P27 Part C: each fact watched red, the tool's own way (reachability-audit section 9): a copy of the tool with
# one rule reverted, the full suite run against it. Writes only into a scratch dir. Usage:
#   python tool_red.py <scratch dir> <export's server/customizations>
import os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, '..', '..'))
scratch, ours = sys.argv[1], sys.argv[2]

REVERTS = {
    # fix 1: pinned read unpatched again (and, as before cc-P27 without the added-lines pass, no patch read at all)
    'patched pinned': ('built, scratch = pinned_as_built(pinned, patches, script)',
                       'built, scratch = {}, tempfile.mkdtemp()'),
    # fix 2: every typeof in an AddCraft is a product again
    'addcraft resource': ("if site == 'AddCraft' and not first_typeof_in_call(code, s):", 'if False:'),
    # the moved fact (commented-out pinned code, now on Ilhenir)
    'pinned comments': ('for pos, text in comments:', 'for pos, text in []:'),
    # the rewritten fact (static access): every live type acts
    'acting rule': ("if t not in acting and (r[1] in REACHING or r[1] == 'base' or not self.is_content(t)):",
                    'if t not in acting:'),
}

src = open(os.path.join(REPO, 'tools', 'content_index.py'), encoding='utf-8').read()
for name, (old, new) in [('none', ('', ''))] + list(REVERTS.items()):
    d = os.path.join(scratch, 'red-' + name.replace(' ', '-'))
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(os.path.join(d, 'tools'))
    os.makedirs(os.path.join(d, 'notes'))
    shutil.copy(os.path.join(REPO, 'tools', 'test_content_index.py'), os.path.join(d, 'tools'))
    shutil.copy(os.path.join(REPO, 'notes', 's9-backlog-remeasure.md'), os.path.join(d, 'notes'))
    if old:
        assert src.count(old) == 1, (name, src.count(old))
    open(os.path.join(d, 'tools', 'content_index.py'), 'w', encoding='utf-8').write(src.replace(old, new) if old else src)
    run = subprocess.run([sys.executable, '-m', 'unittest', 'tools/test_content_index.py'], cwd=d, capture_output=True,
                         text=True, env=dict(os.environ, CONTENT_INDEX_OURS=ours))
    out = run.stderr.splitlines()
    tail = next((l for l in reversed(out) if l.startswith(('OK', 'FAILED'))), '?')
    bad = sorted({l.split(' ')[1] for l in out if l.startswith(('FAIL:', 'ERROR:'))})
    print(f'{name:18} -> {tail:30} {", ".join(bad)}')
