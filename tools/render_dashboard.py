#!/usr/bin/env python3
"""
Rewrite the live data sections of dashboard.html from progress.json and
expansion-coverage.json. Called automatically by progress.py.

Only the regions between the DATA markers are touched; the page's design is left alone.
Open dashboard.html in a browser to view. Republishing the hosted artifact is a separate,
manual step.
"""
import json, os, re, sys, html
from pathlib import Path
from datetime import datetime

MIGRATE = Path(os.environ.get("SL_MIGRATE", Path(__file__).resolve().parent.parent))
DASH = MIGRATE / "dashboard.html"

def load(name):
    p = MIGRATE / "tools" / name
    try: return json.loads(p.read_text(encoding="utf-8"))
    except Exception: return None

def esc(s): return html.escape(str(s))

def foundation_html(pg):
    d = pg["setup_defects"]; done = pg["setup_done"]; tot = pg["setup_total"]
    pct = 100*done/tot if tot else 0
    rows = "".join(
        f'<tr><td>{esc(k)}</td><td><span class="pill {"p-ok" if v else "p-no"}">'
        f'{"done" if v else "no"}</span></td></tr>' for k, v in d.items())
    p = pg.get("patches", {})
    return (f'<div class="card"><div class="hero"><span class="big">{done} / {tot}</span>'
            f'<span class="cap"><strong>Foundation defects resolved.</strong> Problems with the '
            f'shard as it runs today. Nothing else starts until these close.</span></div>'
            f'<span class="track"><span class="fill" style="width:{pct:.0f}%"></span></span></div>'
            f'<div class="scroller"><table><thead><tr><th>Foundation item</th><th>Status</th>'
            f'</tr></thead><tbody>{rows}</tbody></table></div>'
            f'<p class="foot"><strong>Patches:</strong> {p.get("total","?")} tracked, '
            f'<strong>{p.get("failing","?")} currently failing to apply</strong>, '
            f'{p.get("triaged",0)} triaged, {p.get("obsolete",0)} found obsolete.</p>')

def expansion_html(ex):
    if not ex: return "<p class='foot'>Expansion data unavailable.</p>"
    rows = "".join(
        f'<tr><td>{esc(r["label"])}</td>'
        f'<td class="n">{r["have"]:,}</td><td class="n">{r["servuo_files"]:,}</td>'
        f'<td class="n">{r["pct"]:.0f}%</td>'
        f'<td class="n">{"+" + str(r["ported_by_us"]) if r["ported_by_us"] else "&mdash;"}</td></tr>'
        for r in ex["rows"])
    t, h, o = ex["total_files"], ex["total_have"], ex.get("ported_by_us", 0)
    return ('<div class="scroller"><table><thead><tr><th>Expansion</th><th class="n">Have</th>'
            '<th class="n">In ServUO</th><th class="n">Coverage</th><th class="n">Ours</th>'
            f'</tr></thead><tbody>{rows}'
            f'<tr><td><strong>Total</strong></td><td class="n"><strong>{h:,}</strong></td>'
            f'<td class="n"><strong>{t:,}</strong></td>'
            f'<td class="n"><strong>{100*h/t:.0f}%</strong></td>'
            f'<td class="n"><strong>+{o}</strong></td></tr></tbody></table></div>')

def content_html(pg):
    cp = pg.get("content_progress") or []
    if not cp: return "<p class='foot'>No content data.</p>"
    d = sum(r["done"] for r in cp); t = sum(r["total"] for r in cp)
    rows = "".join(f'<tr><td>{esc(r["area"])}</td><td class="n">{r["done"]}</td>'
                   f'<td class="n">{r["total"]}</td><td class="n">{r["pct"]:.1f}%</td></tr>'
                   for r in cp)
    return (f'<p><strong>{d:,} of {t:,} candidate files moved over.</strong> Counted by matching '
            f'ServUO file stems against <code>server/customizations</code>, excluding stems stock '
            f'ModernUO already has.</p><div class="scroller"><table><thead><tr><th>Area</th>'
            '<th class="n">Done</th><th class="n">Total</th><th class="n">%</th></tr></thead>'
            f'<tbody>{rows}</tbody></table></div>')

def replace(txt, tag, body):
    s, e = f"<!-- DATA:{tag} -->", f"<!-- /DATA:{tag} -->"
    if s not in txt or e not in txt: return txt, False
    return re.sub(re.escape(s) + r".*?" + re.escape(e),
                  lambda _: s + "\n" + body + "\n" + e, txt, flags=re.S), True

def main():
    if not DASH.exists():
        print(f"  dashboard.html not found at {DASH}", file=sys.stderr); return 1
    pg, ex = load("progress.json"), load("expansion-coverage.json")
    if not pg: print("  progress.json missing; run progress.py first", file=sys.stderr); return 1
    txt = DASH.read_text(encoding="utf-8"); hit = []
    for tag, body in (("FOUNDATION", foundation_html(pg)),
                      ("EXPANSION", expansion_html(ex)),
                      ("CONTENT", content_html(pg))):
        txt, ok = replace(txt, tag, body)
        if ok: hit.append(tag)
    txt = re.sub(r"<!-- DATA:GENERATED -->.*?<!-- /DATA:GENERATED -->",
                 lambda _: f"<!-- DATA:GENERATED -->{datetime.now().astimezone():%Y-%m-%d %H:%M}"
                           "<!-- /DATA:GENERATED -->", txt, flags=re.S)
    DASH.write_text(txt, encoding="utf-8", newline="\n")
    print(f"  dashboard.html updated ({', '.join(hit) if hit else 'no markers found'}).")
    return 0

if __name__ == "__main__":
    sys.exit(main())
