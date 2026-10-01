"""cc-P22 red run 2: the four facts the first red run left green, each with a break nothing else masks.

    python mutate2.py apply | restore
"""
import sys
import mutate

mutate.BACK = mutate.os.path.join(mutate.HERE, 'red-backup-2')
mutate.MANIFEST = mutate.os.path.join(mutate.BACK, 'manifest.json')

mutate.M = [
    # F11 2 alone: each material taken as it passes its check (run 1's "bank not searched" refused first).
    (r'server\customizations\GuildResources.cs',
     '''            if (cost != null && cost.Amount > 0 && Count(pm, cost).Total < cost.Amount)
            {
                pm.SendMessage(0x22, ShortMessage(pm, cost));
                return false;
            }''',
     '''            if (cost != null && cost.Amount > 0 && Count(pm, cost).Total < cost.Amount)
            {
                pm.SendMessage(0x22, ShortMessage(pm, cost));
                return false;
            }

            TryConsume(pm, cost); // P22 RED 2: each material taken as it passes''',
     'F11 2: not all or nothing'),
    # F17 3: no stop when full, and every try counted.
    (r'server\customizations\BODCombineContained.cs',
     '''            if (IsFull(deed))
            {
                break;
            }''',
     '''            // P22 RED 2: no stop when full''',
     'F17 3: does not stop'),
    (r'server\customizations\BODCombineContained.cs',
     '''            if (item.Deleted)
            {
                combined++;
            }''',
     '''            combined++; // P22 RED 2: counts every try''',
     'F17 3: says the wrong number'),
    # F17 2: the first item in the container is skipped. F17 4: a large deed takes nothing.
    (r'server\customizations\BODCombineContained.cs',
     '''        var items = new List<Item>();
        foreach (var item in container.Items)
        {
            if (item != deed && (deed is not LargeBOD || item is SmallBOD))''',
     '''        var items = new List<Item>();
        var skipFirst = true; // P22 RED 2
        foreach (var item in container.Items)
        {
            if (skipFirst && item != deed) { skipFirst = false; continue; } // P22 RED 2
            if (item != deed && deed is not LargeBOD) // P22 RED 2: a large deed takes nothing''',
     'F17 2 and 4: items missed'),
]
mutate.PATCH = r'server\customizations\BODCombineContained.cs'  # nothing extra to patch this time


def apply():
    import os, shutil, json
    os.makedirs(mutate.BACK, exist_ok=True)
    files = sorted({f for f, *_ in mutate.M})
    manifest = {}
    for f in files:
        src = os.path.join(mutate.R, f)
        shutil.copy2(src, os.path.join(mutate.BACK, f.replace('\\', '__')))
        manifest[f] = mutate.sha(src)
    json.dump(manifest, open(mutate.MANIFEST, 'w'), indent=1)
    for f, old, new, what in mutate.M:
        p = os.path.join(mutate.R, f)
        s = open(p, newline='').read()
        assert s.count(old) == 1, (f, what)
        open(p, 'w', newline='').write(s.replace(old, new))
        print('applied:', what)


if __name__ == '__main__':
    {'apply': apply, 'restore': mutate.restore}[sys.argv[1]]()
