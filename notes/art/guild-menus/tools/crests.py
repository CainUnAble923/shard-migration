"""cc-P177: every guild's crest and accent, read from GuildMenuGump.cs's theme table. Usage: crests.py OUT.png"""
import os, re, runpy, sys
HERE = os.path.dirname(os.path.abspath(__file__))
R2 = runpy.run_path(os.path.join(HERE, 'render2.py'), run_name='lib')
R = R2['R']
src = open(r'D:\ShatteredLegacy\server\customizations\GuildMenuGump.cs', encoding='utf-8').read()
rows = re.findall(r'new\((?:"(\w+)"|LeagueKey), "([^"]+)",(?: /\*[^*]*\*/)? (0x[0-9A-F]+), (\d+), (0x[0-9A-F]+)\),?\s*//\s*(.*)', src)
COLS, CW, CH = 2, 400, 78
c = R['Canvas'](COLS * CW + 20, (len(rows) + 1) // 2 * CH + 20)
c.blit(0, 0, 2624, tw=c.w, th=c.h)
for i, (key, name, hue, crest, item, note) in enumerate(rows):
    x, y = 10 + (i % COLS) * CW, 10 + (i // COLS) * CH
    hue, crest, item = int(hue, 16), int(crest), int(item, 16)
    if crest:
        c.blit(x, y + 4, crest)
    else:
        c.background(x, y + 4, 60, 60, 9270)
        R2['blit_item'](c, x + 12, y + 16, item)
    c.text(x + 72, y + 8, name, R['label_rgb'](hue))
    c.text(x + 72, y + 28, '%s  crest %s  accent 0x%X' % (key or 'league', crest or 'none (placeholder)', hue), (172, 172, 172))
    c.text(x + 72, y + 46, note.strip()[:44], (120, 120, 120))
c.save(sys.argv[1])
print(len(rows))
