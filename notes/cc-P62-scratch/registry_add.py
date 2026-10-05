# P62: add the kind column to registry.csv (every existing row is art) and the three new rows. Run once.
p = r'D:\ShatteredLegacy\player-package\vendor\shattered-legacy-art\registry.csv'
lines = open(p, encoding='ascii').read().split('\n')
assert not any(l.startswith('id,') and l.endswith(',kind') for l in lines), 'already done'
out = []
for l in lines:
    if not l:
        continue
    if l.startswith('#'):
        out.append(l)
    elif l.startswith('id,'):
        out.append('# kind (cc-P62): art = an art/item ID, one PNG in art\\; anim = an Animation number (a worn item\'s')
        out.append('# tiledata animId), its frames in sl-anim7.bin; gump = a gump ID, one PNG in gumps\\.')
        out.append(l + ',kind')
    else:
        out.append(l + ',art')
src = '"Shattered Legacy art chat for Chase, 2026-10-05: design\\kitsune-ears-tail\\%s"'
out.append('15420,0x3C3C,fox ears and tail: item icon (the item ID; tiledata record: Earrings layer 0x12; Animation 4783),'
           + src % 'icon_44.png' + ',ours,art')
out.append('4783,0x12AF,fox ears and tail on the female human body 401 (anim7 slot 400; walk direction 1 only so far),'
           + src % 'stage3-final\\walk_dir1\\walk_dir1_f00-f09.png' + ',ours,anim')
out.append('64783,0xFD0F,fox ears and tail: female paperdoll gump (60000 + Animation 4783),'
           + src % 'stage2-final\\paperdoll_260x237.png' + ',ours,gump')
open(p, 'w', encoding='ascii', newline='\n').write('\n'.join(out) + '\n')

import csv
r = list(csv.DictReader(l for l in open(p) if not l.startswith('#')))
print(len(r), {k: sum(1 for x in r if x['kind'] == k) for k in ('art', 'anim', 'gump')})
