import os, subprocess
S = r'C:\Users\ckfle\AppData\Local\Temp\claude\D--UO-shard-migration\04262ca5-d41c-48c4-a651-b1de824239a3\scratchpad\bodpatch'
D = r'Projects\UOContent\Engines\Bulk Orders'


def edit(name, pairs):
    p = os.path.join(S, 'b', D, name)
    s = open(p, newline='').read()
    for old, new in pairs:
        assert s.count(old) == 1, (name, old[:60])
        s = s.replace(old, new)
    open(p, 'w', newline='').write(s)


edit('SmallBODGump.cs', [
    ('''            builder.AddBackground(50, 10, 455, 260, 5054);
            builder.AddImageTiled(58, 20, 438, 241, 2624);
            builder.AddAlphaRegion(58, 20, 438, 241);''',
     '''            // Shattered Legacy (F-17): one row taller for "Combine this deed with contained items".
            builder.AddBackground(50, 10, 455, 284, 5054);
            builder.AddImageTiled(58, 20, 438, 265, 2624);
            builder.AddAlphaRegion(58, 20, 438, 265);'''),
    ('''            builder.AddImage(45, 245, 10460);
            builder.AddImage(480, 245, 10460);''',
     '''            builder.AddImage(45, 269, 10460);
            builder.AddImage(480, 269, 10460);'''),
    ('''            builder.AddButton(125, 216, 4005, 4007, 1);
            builder.AddHtmlLocalized(160, 216, 120, 20, 1011441, 0x7FFF); // EXIT''',
     '''            builder.AddButton(125, 216, 4005, 4007, BODCombineContained.ButtonID);
            builder.AddHtmlLocalized(160, 216, 300, 20, BODCombineContained.Cliloc, 0x7FFF); // Combine this deed with contained items.

            builder.AddButton(125, 240, 4005, 4007, 1);
            builder.AddHtmlLocalized(160, 240, 120, 20, 1011441, 0x7FFF); // EXIT'''),
    ('''                from.SendGump(new SmallBODGump(_deed));
                _deed.BeginCombine(from);
            }''',
     '''                from.SendGump(new SmallBODGump(_deed));
                _deed.BeginCombine(from);
            }
            else if (info.ButtonID == BODCombineContained.ButtonID) // Combine with contained items (F-17)
            {
                from.SendGump(new SmallBODGump(_deed));
                BODCombineContained.Begin(from, _deed);
            }'''),
])

edit('LargeBODGump.cs', [
    ('''            builder.AddBackground(50, 10, 455, 236 + entries.Length * 24, 5054);

            builder.AddImageTiled(58, 20, 438, 217 + entries.Length * 24, 2624);
            builder.AddAlphaRegion(58, 20, 438, 217 + entries.Length * 24);''',
     '''            // Shattered Legacy (F-17): one row taller for "Combine this deed with contained items".
            builder.AddBackground(50, 10, 455, 260 + entries.Length * 24, 5054);

            builder.AddImageTiled(58, 20, 438, 241 + entries.Length * 24, 2624);
            builder.AddAlphaRegion(58, 20, 438, 241 + entries.Length * 24);'''),
    ('''            builder.AddImage(45, 221 + entries.Length * 24, 10460);
            builder.AddImage(480, 221 + entries.Length * 24, 10460);''',
     '''            builder.AddImage(45, 245 + entries.Length * 24, 10460);
            builder.AddImage(480, 245 + entries.Length * 24, 10460);'''),
    ('''            builder.AddButton(125, 192 + entries.Length * 24, 4005, 4007, 1);
            builder.AddHtmlLocalized(160, 192 + entries.Length * 24, 120, 20, 1011441, 0x7FFF); // EXIT''',
     '''            builder.AddButton(125, 192 + entries.Length * 24, 4005, 4007, BODCombineContained.ButtonID);
            builder.AddHtmlLocalized(
                160,
                192 + entries.Length * 24,
                300,
                20,
                BODCombineContained.Cliloc, // Combine this deed with contained items.
                0x7FFF
            );

            builder.AddButton(125, 216 + entries.Length * 24, 4005, 4007, 1);
            builder.AddHtmlLocalized(160, 216 + entries.Length * 24, 120, 20, 1011441, 0x7FFF); // EXIT'''),
    ('''                sender.SendGump(new LargeBODGump(_deed));
                _deed.BeginCombine(from);
            }''',
     '''                sender.SendGump(new LargeBODGump(_deed));
                _deed.BeginCombine(from);
            }
            else if (info.ButtonID == BODCombineContained.ButtonID) // Combine with contained small deeds (F-17)
            {
                sender.SendGump(new LargeBODGump(_deed));
                BODCombineContained.Begin(from, _deed);
            }'''),
])

out = []
for name in ['SmallBODGump.cs', 'LargeBODGump.cs']:
    r = subprocess.run(['diff', '-u', f'a/Projects/UOContent/Engines/Bulk Orders/{name}', f'b/Projects/UOContent/Engines/Bulk Orders/{name}'],
                       cwd=S, capture_output=True, text=True)
    lines = r.stdout.splitlines(keepends=True)
    # Quote the paths as the repo's other Bulk Orders patch does (a path with a space).
    for i in (0, 1):
        tag, rest = lines[i][:4], lines[i][4:]
        path, _, stamp = rest.partition('\t')
        lines[i] = f'{tag}"{path}"\t{stamp}'
    out.extend(lines)

open(r'D:\ShatteredLegacy\server\patches\BOD-combine-contained.patch', 'w', newline='').write(''.join(out))
print(''.join(out))
