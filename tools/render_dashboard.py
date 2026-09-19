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

def minibar(done, total):
    """Inline proportion bar for a table cell. A nonzero value always paints at
    least a sliver, so "barely started" never looks identical to "not started"."""
    if not total:
        return '<span class="mini zero"><i style="width:0"></i></span>'
    pct = 100 * done / total
    w = max(pct, 1.5) if done else 0
    z = "" if done else " zero"
    return (f'<span class="mini{z}" role="img" aria-label="{pct:.0f} percent">'
            f'<i style="width:{w:.1f}%"></i></span>')

def headline_html(pg):
    """Overall percentage plus the playable verdict. The caveat rides with the number."""
    cp = pg.get("content_progress") or []
    done = sum(r["done"] for r in cp); total = sum(r["total"] for r in cp)
    pct = 100*done/total if total else 0
    return (f'<div class="card"><div class="hero"><span class="big">{pct:.0f}%</span>'
            f'<span class="cap"><strong>of candidate content ported.</strong> {done} of {total} '
            f'ServUO files that ModernUO does not already ship.</span></div>'
            f'<span class="track"><span class="fill" style="width:{pct:.0f}%"></span></span></div>'
            f'<p class="foot"><strong>Read that denominator with suspicion.</strong> "Candidate" is '
            f'ServUO filtered against the names ModernUO already declares, and every count on this '
            f'project has moved once someone read the files: CC9 went 455 &rarr; 437, Despise was '
            f'"4 files" and was 14. A direction of travel, not a promise.</p>')

def playable_html(pg):
    g = pg.get("playable_gates")
    if not g:
        return ""
    gates = g.get("gates", [])
    met = sum(1 for x in gates if x.get("done"))
    blockers = [x for x in gates if not x.get("done")]
    pct = 100*met/len(gates) if gates else 0
    verdict = (f'Not yet. Next to fall: <em>{esc(blockers[0]["name"])}</em>.'
               if blockers else "Yes, every gate met.")
    rows = "".join(
        f'<tr><td><span class="pill {"p-ok" if x.get("done") else "p-todo"}">'
        f'{"yes" if x.get("done") else "no"}</span></td><td>{esc(x["name"])}</td>'
        f'<td class="foot">{esc(x.get("detail",""))}</td></tr>' for x in gates)
    return (f'<div class="card"><div class="hero"><span class="big">{met} / {len(gates)}</span>'
            f'<span class="cap"><strong>Playable? {verdict}</strong> "Playable" is a judgement, so '
            f'it is written down as gates rather than felt. Each is something a player would hit.'
            f'</span></div><span class="track"><span class="fill" style="width:{pct:.0f}%"></span>'
            f'</span></div><div class="scroller"><table><thead><tr><th class="n">Met</th>'
            f'<th>Gate</th><th>Where it stands</th></tr></thead><tbody>{rows}</tbody></table></div>')

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
        f'<td class="bar">{minibar(r["have"], r["servuo_files"])}</td>'
        f'<td class="n">{r["pct"]:.0f}%</td>'
        f'<td class="n">{"+" + str(r["ported_by_us"]) if r["ported_by_us"] else "&mdash;"}</td></tr>'
        for r in ex["rows"])
    t, h, o = ex["total_files"], ex["total_have"], ex.get("ported_by_us", 0)
    return ('<div class="scroller"><table><thead><tr><th>Expansion</th><th class="n">Have</th>'
            '<th class="n">In ServUO</th><th></th><th class="n">Coverage</th><th class="n">Ours</th>'
            f'</tr></thead><tbody>{rows}'
            f'<tr><td><strong>Total</strong></td><td class="n"><strong>{h:,}</strong></td>'
            f'<td class="n"><strong>{t:,}</strong></td>'
            f'<td class="bar">{minibar(h, t)}</td>'
            f'<td class="n"><strong>{100*h/t:.0f}%</strong></td>'
            f'<td class="n"><strong>+{o}</strong></td></tr></tbody></table></div>')

def content_html(pg):
    cp = pg.get("content_progress") or []
    if not cp: return "<p class='foot'>No content data.</p>"
    d = sum(r["done"] for r in cp); t = sum(r["total"] for r in cp)
    rows = "".join(f'<tr><td>{esc(r["area"])}</td><td class="n">{r["done"]}</td>'
                   f'<td class="n">{r["total"]}</td>'
                   f'<td class="bar">{minibar(r["done"], r["total"])}</td>'
                   f'<td class="n">{r["pct"]:.1f}%</td></tr>'
                   for r in cp)
    return (f'<div class="card"><div class="hero"><span class="big">{d:,}</span>'
            f'<span class="cap"><strong>files moved over, out of {t:,} candidates.</strong> '
            'The candidate pool is what exists in ServUO, not a target. This backlog has no '
            'completion date by design, so read the bar as scale, not as progress toward '
            'finishing.</span></div>'
            f'<span class="track"><span class="fill" '
            f'style="width:{max(100*d/t, 0.6) if (t and d) else 0:.2f}%"></span></span></div>'
            f'<p class="foot">Counted by matching '
            'ServUO file stems against <code>server/customizations</code>, excluding stems stock '
            'ModernUO already has.</p><div class="scroller"><table><thead><tr><th>Area</th>'
            '<th class="n">Done</th><th class="n">Total</th><th></th><th class="n">%</th>'
            f'</tr></thead><tbody>{rows}</tbody></table></div>')

def patches_html(pg):
    up = pg.get("upstream_patches") or {}
    if not up: return "<p class='foot'>No patch inventory.</p>"
    ps, rp = up.get("patches", []), up.get("replacements", [])
    cls = {"high": "p-no", "medium": "p-next", "low": "p-todo"}
    order = {"high": 0, "medium": 1, "low": 2}
    rows = "".join(
        f'<tr><td><code>{esc(x["file"])}</code></td><td class="foot">{esc(x["patch"])}</td>'
        f'<td class="n">{esc(x["d"])}</td>'
        f'<td><span class="pill {cls.get(x.get("risk"),"p-todo")}">{esc(x.get("risk",""))}</span></td>'
        f'<td class="foot">{esc(x["breaks"])}</td></tr>'
        for x in sorted(ps, key=lambda v: order.get(v.get("risk"), 3)))
    return (f'<div class="card"><div class="hero"><span class="big">{len(ps)}</span>'
            f'<span class="cap"><strong>patches into upstream files</strong>, plus {len(rp)} full-file '
            'replacements. This is what a pinned-commit bump has to reconcile, and nothing else '
            'tracks it.</span></div></div>'
            f'<p class="foot">{esc(up.get("note",""))}</p>'
            '<div class="scroller"><table><thead><tr><th>Upstream file</th><th>Patch</th>'
            '<th class="n">Diff</th><th>Risk</th><th>Breaks when</th></tr></thead>'
            f'<tbody>{rows}</tbody></table></div>'
            f'<div class="flag"><span class="eyebrow">Silent on a bump</span>'
            f'<p>These {len(rp)} full-file replacements <strong>always apply</strong>. They never fail, '
            'they just quietly discard whatever upstream changed in that file, so they must be diffed '
            'by hand: '
            + ", ".join(f"<code>{esc(x['file'])}</code>" for x in rp) + ".</p></div>")

def tasks_html(pg):
    tk = pg.get("tasks") or []
    if not tk: return "<p class='foot'>No task data.</p>"
    cls = {"done":"p-ok","in-progress":"p-next","blocked":"p-no","todo":"p-todo"}
    lab = {"done":"done","in-progress":"in progress","blocked":"blocked","todo":"todo"}
    nd = sum(1 for t in tk if t["status"]=="done")
    rows = "".join(
        f'<tr><td class="n">{esc(t["id"])}</td><td>{esc(t["title"])}</td>'
        f'<td><span class="pill {cls[t["status"]]}">{lab[t["status"]]}</span></td>'
        f'<td class="foot">{esc(t.get("note",""))}</td></tr>' for t in tk)
    pct = 100*nd/len(tk)
    return (f'<div class="card"><div class="hero"><span class="big">{nd} / {len(tk)}</span>'
            '<span class="cap"><strong>Tasks done.</strong> Foundation and the port pipeline. '
            'The content backlog below it is open-ended.</span></div>'
            f'<span class="track"><span class="fill" style="width:{pct:.0f}%"></span></span></div>'
            f'<p><strong>{nd} of {len(tk)} tasks done.</strong> Detail and acceptance criteria '
            f'in <code>docs/tasks.md</code>; status in <code>tools/progress-state.json</code>.</p>'
            '<div class="scroller"><table><thead><tr><th class="n">ID</th><th>Task</th>'
            '<th>Status</th><th>Notes</th></tr></thead><tbody>'
            f'{rows}</tbody></table></div>')

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
    for tag, body in (("HEADLINE", headline_html(pg)),
                      ("PLAYABLE", playable_html(pg)),
                      ("FOUNDATION", foundation_html(pg)),
                      ("EXPANSION", expansion_html(ex)),
                      ("CONTENT", content_html(pg)),
                      ("TASKS", tasks_html(pg)),
                      ("PATCHES", patches_html(pg))):
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
