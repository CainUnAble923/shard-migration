import json, os, runpy, sys
R = runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'render.py'), run_name='lib')
s = {int(k): v for k, v in json.load(open('sizes.json')).items()}
c = sorted(g for g, (w, h) in s.items() if 36 <= w <= 120 and 36 <= h <= 120 and 0.7 <= w / h <= 1.4)
CELL, COLS, PER = 128, 12, 96
os.makedirs('sheets', exist_ok=True)
for n in range(0, len(c), PER):
    ids = c[n:n + PER]
    rows = (len(ids) + COLS - 1) // COLS
    cv = R['Canvas'](COLS * CELL, rows * (CELL + 16))
    cv.px = [[(60, 60, 70)] * cv.w for _ in range(cv.h)]
    for i, g in enumerate(ids):
        x, y = (i % COLS) * CELL, (i // COLS) * (CELL + 16)
        w, h, _ = R['art'](g)
        cv.blit(x + (CELL - w) // 2, y + (CELL - h) // 2, g)
        cv.text(x + 4, y + CELL, str(g), (255, 255, 120))
    p = 'sheets/s%02d-%d-%d.png' % (n // PER, ids[0], ids[-1])
    cv.save(p)
    print(p)
