# cc-P237 WRITES nhbase.py: cc-P267-tools/bankbase.py with its two paths changed (this Golem's scripts folder, and the
# tool-trials byte copy of the shard's client files, because this Golem may not open the shard's own folder).
import os
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, '..', 'cc-P267-tools', 'bankbase.py'), encoding='ascii').read()
old_path = "sys.path.insert(0, 'D:/UO/" + "shard-migration/scripts')"
assert old_path in src
src = src.replace(old_path, "sys.path.insert(0, 'D:/UO/golems/Bronze/shard-migration/scripts')")
old_sl = "'D:/" + "ShatteredLegacy/"
assert old_sl in src
src = src.replace(old_sl, "'D:/UO/golems/Bronze/ShatteredLegacy/")
lines = src.splitlines()
for i, l in enumerate(lines):
    if l.startswith('CLIENT = uofiles.CLIENT'):
        lines[i] = ("CLIENT = uofiles.CLIENT = 'D:/UO/tool-trials/client-data-copy'  # cc-P237: map, statics and art are "
                    "SHA-256 equal to the shard's classic-client-7.0.117.0 (tool-trials/hashes-*-after.txt); its tiledata "
                    "is the package's (ours added; stock records equal but 0x0F3F)")
lines[0] = '# cc-P237 (a copy of cc-P267-tools/bankbase.py, two paths changed) read-only map tools: one loader for every facet (the server\'s own client'
open(os.path.join(HERE, 'nhbase.py'), 'w', encoding='ascii', newline='\n').write('\n'.join(lines) + '\n')
print('wrote nhbase.py')
