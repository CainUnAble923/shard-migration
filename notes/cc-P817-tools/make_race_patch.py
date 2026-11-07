r"""cc-P817: client patch 0012 (humans only on the creation screen), made from the appearance gump as our TazUO build has
it (upstream at TAZUO_COMMIT plus patches 0001-0011, D:\UO\tazuo-sl-build\src, read only here), with git diff (3 lines
of context, so git apply takes it with no fuzz, as Build-Client.ps1 applies every patch).

    python -P make_race_patch.py <patched CreateCharAppearanceGump.cs> <out .patch> <scratch folder>
"""
import os
import shutil
import subprocess
import sys

src, out, scratch = sys.argv[1:4]
REL = 'src/ClassicUO.Client/Game/UI/Gumps/CharCreation/CreateCharAppearanceGump.cs'
text = open(src, encoding='utf-8-sig', newline='').read()
nl = '\r\n' if '\r\n' in text else '\n'

start = text.index('            Add' + nl + '            (' + nl + '                _elfRadio = new Button(')
end = text.index('            // Prev/Next')
block = text[start:end]
assert '_gargoyleRadio = new Button' in block and 'Buttons.GargoyleButton, 0x07D3' in block, 'not the elf and gargoyle buttons'
new = (
    '            // Shattered Legacy patch (cc-P817, Chase 2026-11-07: "I still want Gargoyle and Elf removed from selection page"):' + nl +
    '            // Human is the only race on the creation screen, and selected (below). The Elf and Gargoyle buttons are not added,' + nl +
    '            // so _elfRadio and _gargoyleRadio stay null: the Human button\'s handler already checks them for null, and their own' + nl +
    '            // handlers are only reached from those buttons. The server makes any other race Human as well' + nl +
    '            // (NewCharacterRules.RaceFor, newCharacters.races).' + nl + nl
)
edited = text[:start] + new + text[end:]

a = os.path.join(scratch, 'a', *REL.split('/'))
b = os.path.join(scratch, 'b', *REL.split('/'))
for p in (a, b):
    os.makedirs(os.path.dirname(p), exist_ok=True)
shutil.copyfile(src, a)
with open(b, 'w', encoding='utf-8', newline='') as f:
    # keep a BOM if the original had one
    raw = open(src, 'rb').read()
    if raw.startswith(b'\xef\xbb\xbf'):
        f.write('\ufeff')
    f.write(edited)

r = subprocess.run(['git', 'diff', '--no-index', '--no-color', '-U3', 'a/' + REL, 'b/' + REL],
                   cwd=scratch, capture_output=True)
diff = r.stdout.decode('utf-8')
assert diff.startswith('diff --git'), r.stderr
# git diff --no-index names the files as given; the index line carries blob ids of these copies, as 0010's does.
head = (
    'From 0000000000000000000000000000000000000000 Mon Sep 17 00:00:00 2001\n'
    'From: Chase Fleming <ckfleming@gmail.com>\n'
    'Date: Sat, 7 Nov 2026 12:00:00 -0600\n'
    'Subject: [PATCH] Character creation: Human is the only race (Shattered Legacy\n'
    ' cc-P817)\n'
    '\n'
    'Chase, 2026-11-07: "I still want Gargoyle and Elf removed from selection page". The appearance screen adds only the\n'
    'Human race button; Human was already the default selection. The server makes any other race Human anyway.\n'
    '---\n'
)
diff = diff.replace('a/a/', 'a/').replace('b/b/', 'b/')
open(out, 'w', encoding='utf-8', newline='\n').write(head + diff)
print('wrote', out, len(diff), 'bytes of diff')
