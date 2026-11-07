r"""cc-P813: render the Claude Design gump art (canvas "Shattered Legacy gump art", approved by Chase 11-05) to PNGs.

Part 1: each window's HTML at its true size (from the file name), transparent where the page has no background, with
headless Edge. The PNG is written beside its source (the overseer's folder) and into renders\ here.

Part 2: the pieces the client package ships as gumps. Text is never baked in: each piece is the same page re-rendered
with the text hidden (and, for a window background, its buttons hidden), then cut out by the element's own rectangle,
which the page reports through --dump-dom. Pressed button looks are the design's own colours one step darker (the
store's active tab is the design's own "Gear" tab).

    python -P render_gump_art.py <source dir> <gump out dir>

Writes <gump out dir>\<id>.png for gumps 23211-23222 and prints what it cut. Run with Python 3 and Pillow.
"""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

from PIL import Image

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
HERE = os.path.dirname(os.path.abspath(__file__))

# What each render hides or changes, as CSS added after the design's own.
HIDE_TEXT = "h1,p,span{visibility:hidden!important} button{color:transparent!important}"
HIDE_BUTTONS = "button{visibility:hidden!important}"
STORE_ROWS = 'div[style*="grid-template-columns: 1fr 96px"]'
STORE_TABS = 'button[style*="padding: 0 14px"]'
STORE_TAB_W = 104  # one width for every tab, so one tab gump fits every label

RECT_JS = """<script>
window.addEventListener('load', () => {
  const pick = (sel) => Array.from(document.querySelectorAll(sel)).map(e => {
    const r = e.getBoundingClientRect();
    return [Math.round(r.left), Math.round(r.top), Math.round(r.width), Math.round(r.height)];
  });
  const out = {
    buttons: pick('button'),
    rows: pick('%s'),
    root: pick('body > div'),
  };
  const pre = document.createElement('pre');
  pre.id = 'p813rects';
  pre.textContent = JSON.stringify(out);
  pre.style.display = 'none';
  document.body.appendChild(pre);
});
</script>""" % STORE_ROWS


def size_of(name):
    m = re.search(r"-(\d+)x(\d+)\.html$", name)
    if not m:
        raise SystemExit(f"{name}: no WxH in the file name")
    return int(m.group(1)), int(m.group(2))


def edge(args, profile, wait_file=None):
    """Run headless Edge. It often lingers for half a minute after its work is done, so a screenshot run is stopped
    as soon as the file is written and steady; a --dump-dom run as soon as the page's closing tag is out."""
    cmd = [EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
           "--force-device-scale-factor=1", f"--user-data-dir={profile}"] + args
    out_path = os.path.join(os.path.dirname(profile), "stdout.txt")
    with open(out_path, "w", encoding="utf-8") as out:
        p = subprocess.Popen(cmd, stdout=out, stderr=subprocess.DEVNULL)
        last, steady = -1, 0
        for _ in range(600):
            time.sleep(0.5)
            if p.poll() is not None:
                break
            if wait_file:
                size = os.path.getsize(wait_file) if os.path.exists(wait_file) else -1
                steady = steady + 1 if size > 0 and size == last else 0
                last = size
                if steady >= 2:
                    break
            else:
                with open(out_path, encoding="utf-8", errors="replace") as f:
                    if "</html>" in f.read():
                        break
        if p.poll() is None:
            subprocess.run(["taskkill", "/F", "/T", "/PID", str(p.pid)], capture_output=True)
            p.wait(30)
    with open(out_path, encoding="utf-8", errors="replace") as f:
        return f.read()


def render(html_text, w, h, png, work, profile, extra_css=""):
    page = os.path.join(work, "page.html")
    style = f"<style>{extra_css}</style>" if extra_css else ""
    text = html_text.replace("</head>", style + "</head>", 1)
    with open(page, "w", encoding="utf-8") as f:
        f.write(text)
    if os.path.exists(png):
        os.remove(png)
    edge(["--default-background-color=00000000", f"--window-size={w},{h}", f"--screenshot={png}",
          "file:///" + page.replace("\\", "/")], profile, wait_file=png)
    if not os.path.exists(png):
        raise SystemExit(f"Edge wrote no {png}")
    im = Image.open(png).convert("RGBA")
    if im.size != (w, h):
        raise SystemExit(f"{png}: {im.size}, wanted {(w, h)}")
    return im


def rects(html_text, w, h, work, profile, extra_css=""):
    page = os.path.join(work, "rects.html")
    style = f"<style>{extra_css}</style>" if extra_css else ""
    text = html_text.replace("</head>", style + "</head>", 1).replace("</body>", RECT_JS + "</body>", 1)
    with open(page, "w", encoding="utf-8") as f:
        f.write(text)
    res = edge([f"--window-size={w},{h}", "--virtual-time-budget=3000", "--dump-dom",
                "file:///" + page.replace("\\", "/")], profile)
    m = re.search(r'<pre id="p813rects"[^>]*>(.*?)</pre>', res, re.S)
    if not m:
        raise SystemExit("no rectangles in the dumped page")
    return json.loads(m.group(1).replace("&quot;", '"'))


def cut(im, r):
    x, y, w, h = r
    return im.crop((x, y, x + w, y + h))


def main():
    src, gumps = sys.argv[1], sys.argv[2]
    renders = os.path.join(HERE, "renders")
    os.makedirs(renders, exist_ok=True)
    os.makedirs(gumps, exist_ok=True)
    work = tempfile.mkdtemp(prefix="p813-")
    profile = os.path.join(work, "edge-profile")
    pieces = {}

    def html(name):
        with open(os.path.join(src, name), encoding="utf-8-sig") as f:
            return f.read()

    # Part 1: the three windows as designed.
    for name in sorted(os.listdir(src)):
        if not name.endswith(".html"):
            continue
        w, h = size_of(name)
        png = os.path.join(work, "full.png")
        im = render(html(name), w, h, png, work, profile)
        base = name[:-5] + ".png"
        im.save(os.path.join(src, base))
        im.save(os.path.join(renders, base))
        print(f"rendered {name} -> {base} {im.size}")

    # Part 2a: the pet choice scroll. Background without text or tiles; each tile (icon, no word) and its pressed look.
    name = "pet-choice-scroll-340x280.html"
    w, h = size_of(name)
    t = html(name)
    pieces[23211] = render(t, w, h, os.path.join(work, "a.png"), work, profile, HIDE_TEXT + HIDE_BUTTONS)
    r = rects(t, w, h, work, profile)
    up = render(t, w, h, os.path.join(work, "b.png"), work, profile, HIDE_TEXT)
    down = render(t, w, h, os.path.join(work, "c.png"), work, profile,
                  HIDE_TEXT + "button{background:#ddcfa6!important;border-color:#5c4110!important}")
    pieces[23212], pieces[23213] = cut(up, r["buttons"][0]), cut(down, r["buttons"][0])
    pieces[23214], pieces[23215] = cut(up, r["buttons"][1]), cut(down, r["buttons"][1])
    print("pet tiles at", r["buttons"])

    # Part 2b: the skip achievement popup: the panel only.
    name = "skip-achievement-popup-400x136.html"
    w, h = size_of(name)
    pieces[23216] = render(html(name), w, h, os.path.join(work, "d.png"), work, profile, HIDE_TEXT)

    # Part 2c: the reward store. Background: panel, border and header rule (no tabs, rows or text: the server draws
    # them); a 1 px row rule to tile; a tab, inactive and active, one width; the Buy button and its pressed look.
    name = "reward-store-window-560x420.html"
    w, h = size_of(name)
    t = html(name)
    tabs = f"{STORE_TABS}{{width:{STORE_TAB_W}px!important;padding:0!important}}"
    pieces[23217] = render(t, w, h, os.path.join(work, "e.png"), work, profile,
                           HIDE_TEXT + HIDE_BUTTONS + f"{STORE_ROWS}{{visibility:hidden!important}}")
    r = rects(t, w, h, work, profile, tabs)
    up = render(t, w, h, os.path.join(work, "f.png"), work, profile, HIDE_TEXT + tabs)
    down = render(t, w, h, os.path.join(work, "g.png"), work, profile,
                  HIDE_TEXT + tabs + f"{STORE_ROWS} button{{background:#2a2317!important}}")
    row = r["rows"][0]
    rule = up.crop((row[0], row[1] + row[3] - 1, row[0] + 8, row[1] + row[3]))
    pieces[23218] = rule
    tab_btns = [b for b in r["buttons"] if b[3] == 32]
    buy_btns = [b for b in r["buttons"] if b[3] == 28]
    pieces[23219] = cut(up, tab_btns[1])   # an inactive tab ("Companions")
    pieces[23220] = cut(up, tab_btns[0])   # the active tab ("Gear")
    pieces[23221] = cut(up, buy_btns[0])
    pieces[23222] = cut(down, buy_btns[0])
    print("store tabs at", tab_btns, "buy at", buy_btns[0], "rows at", r["rows"])

    for gid, im in sorted(pieces.items()):
        out = os.path.join(gumps, f"{gid}.png")
        im.save(out)
        print(f"gump {gid} (0x{gid:04X}) {im.size[0]}x{im.size[1]} -> {out}")
    shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
