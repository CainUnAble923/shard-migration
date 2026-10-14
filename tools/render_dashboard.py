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
    """cc-P92: the ServUO port list (tools/port-list.json), counted by progress.py. Was "27% of candidate content",
    which divided by every ServUO file ModernUO lacks: a pool the page itself called "not a target"."""
    pl = pg.get("port_list")
    if not pl:
        return "<p class='foot'>No port list data (tools/port-list.json, progress.py).</p>"
    c = pl["counted"]
    pct = c["pct"]
    nxt = (f'<strong>Next to land: {esc(pl["next"])}.</strong>' if pl.get("next")
           else '<strong>Every Port system is in.</strong>')
    return (f'<div class="card"><div class="hero"><span class="big">{c["in"]} / {c["systems"]}</span>'
            f'<span class="cap"><strong>Port list: {c["in"]} of {c["systems"]} systems in. {c["done"]:,} of '
            f'{c["total"]:,} files ({pct:.0f}%).</strong> {nxt}</span></div>'
            f'<span class="track"><span class="fill" style="width:{pct:.0f}%"></span></span></div>'
            f'<p>{esc(PORT_DIRECTION)}</p>'
            f'<p class="foot">"In" means every file of a system is ported. Counted by filename stem against '
            f'<code>server/customizations</code>, not by behavior: a direction of travel, not a promise. The list '
            f'itself is <code>tools/port-list.json</code>, kept by hand.</p>')

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
        f'<td class="foot">{esc(x.get("detail",""))}'
        f'{(" <span class=src>Sources: " + esc("; ".join(x.get("sources", []))) + ".</span>") if x.get("sources") else ""}'
        f'</td><td class="n foot">{esc(x.get("confirmed",""))}</td></tr>' for x in gates)
    return (f'<div class="card"><div class="hero"><span class="big">{met} / {len(gates)}</span>'
            f'<span class="cap"><strong>Playable? {verdict}</strong> "Playable" is a judgement, so '
            f'it is written down as gates rather than felt. Each is something a player would hit.'
            f'</span></div><span class="track"><span class="fill" style="width:{pct:.0f}%"></span>'
            f'</span></div><div class="scroller"><table><thead><tr><th class="n">Met</th>'
            f'<th>Gate</th><th>Where it stands</th><th class="n">Confirmed</th></tr></thead><tbody>{rows}</tbody></table></div>')

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

PORT_DIRECTION = ("A faithful port comes first, our feature customizations after it; work already started or already "
                  "requested is still finished (Chase, 2026-10-13).")
TIER_NAMES = {"ride": "Ride-along", "reward": "Reward pool", "source": "Design source", "later": "Later",
              "drop": "Dropped"}


def portlist_html(pg):
    """cc-P92: the port list section. Port rows with bars and their feeds; any Decide rows, marked as waiting on Chase;
    then one collapsed line per not-counted tier; then the old every-file area table, collapsed, as scale only."""
    pl = pg.get("port_list")
    if not pl:
        return "<p class='foot'>No port list data.</p>"
    counted = [r for r in pl["systems"] if r["tier"] == "port"]
    decide = [r for r in pl["systems"] if r["tier"] == "decide"]

    def row(r, extra=""):
        state = ('<span class="pill p-ok">in</span>' if r["complete"] else "")
        return (f'<tr><td>{esc(r["title"])} {state}{extra}</td><td class="n">{r["done"]}</td>'
                f'<td class="n">{r["candidates"]}</td><td class="bar">{minibar(r["done"], r["candidates"])}</td>'
                f'<td class="foot">{esc(r["feeds"])}</td></tr>')

    rows = "".join(row(r) for r in counted)
    rows += "".join(row(r, ' <span class="pill p-todo">waiting on Chase</span>') for r in decide)
    c = pl["counted"]
    rows += (f'<tr><td><strong>Port tier</strong></td><td class="n"><strong>{c["done"]:,}</strong></td>'
             f'<td class="n"><strong>{c["total"]:,}</strong></td><td class="bar">{minibar(c["done"], c["total"])}</td>'
             f'<td class="foot">{c["in"]} of {c["systems"]} systems in</td></tr>')
    tiers = ""
    for t, v in pl["tiers"].items():
        if t in ("port", "decide"):
            continue
        items = "".join(f"<li>{esc(x)}</li>" for x in v["titles"])
        tiers += (f'<details><summary><strong>{esc(TIER_NAMES.get(t, t))}</strong>: {v["files"]:,} files '
                  f'({v["done"]:,} in). {esc(v.get("meaning", "") or "Not counted.")}</summary><ul>{items}</ul></details>')
    un = ""
    if pl.get("unassigned"):
        un = (f'<p class="flag"><strong>{pl["unassigned"]} ServUO files belong to no system</strong>, the first: '
              + ", ".join(f"<code>{esc(x)}</code>" for x in pl.get("unassigned_first", [])[:20]) + ".</p>")
    return ('<div class="scroller"><table><thead><tr><th>System</th><th class="n">Done</th><th class="n">Files</th>'
            f'<th></th><th>Feeds</th></tr></thead><tbody>{rows}</tbody></table></div>{un}{tiers}'
            f'<p class="foot">{pl["candidates"]:,} ServUO files under Services, Items and Mobiles that stock ModernUO '
            'lacks; each belongs to the first system in the list whose path prefix matches. "Next to land" is the first '
            'Port row, in the list&#x27;s order, that is not in.</p>'
            '<details><summary>Every ServUO file ModernUO lacks, by area (scale, not a target)</summary>'
            + content_html(pg) + '</details>')


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
        f'<td class="foot">{esc(t.get("note",""))}</td><td class="n foot">{esc(t.get("confirmed",""))}</td></tr>' for t in tk)
    pct = 100*nd/len(tk)
    return (f'<div class="card"><div class="hero"><span class="big">{nd} / {len(tk)}</span>'
            '<span class="cap"><strong>Tasks done.</strong> The open work the overseer tracks by hand; '
            'the prompt queue below is read from disk.</span></div>'
            f'<span class="track"><span class="fill" style="width:{pct:.0f}%"></span></span></div>'
            f'<p><strong>{nd} of {len(tk)} tasks done.</strong> Status in <code>tools/progress-state.json</code>; '
            f'<code>python tools/judge.py</code> updates one row and stamps its date.</p>'
            '<div class="scroller"><table><thead><tr><th class="n">ID</th><th>Task</th>'
            '<th>Status</th><th>Notes</th><th class="n">Confirmed</th></tr></thead><tbody>'
            f'{rows}</tbody></table></div>')

# --- cc-P85: freshness, the direction note, the queue and the play tests ------------------------------------------

LAN_HOST = "192.168.1.58"   # the Windows box (docker/test-queue/docker-compose.yml); used only when opened as a file

def today_str():
    return datetime.now().astimezone().strftime("%Y-%m-%d")

def days_old(date_str, now=None):
    """Whole days from a YYYY-MM-DD date to now (local); None for a missing or bad date."""
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        return None
    return ((now or datetime.now()).date() - d).days

def asof_html(date_str, header_date):
    """A section's own as-of line, only when it differs from the header's date."""
    if not date_str or date_str == header_date:
        return ""
    old = days_old(date_str)
    age = f" ({old} days ago)" if old and old > 0 else ""
    return f'<span class="eyebrow asof">As of {esc(date_str)}{age}</span>'

def reviewed_html(pg):
    dv = pg.get("derived") or {}
    rev = dv.get("reviewed") or ""
    stale_days = dv.get("stale_days") or 7
    old = days_old(rev)
    stale = old is None or old > stale_days
    cls = "reviewed stale" if stale else "reviewed"
    tip = (f"The hand-written judgment (gates, tasks, status) was last confirmed {rev}. It turns amber after "
           f"{stale_days} days; tools/README.md says how to update it.")
    return (f'<span class="{cls}" data-reviewed="{esc(rev)}" data-stale-days="{stale_days}" title="{esc(tip)}">'
            f'Judgment reviewed {esc(rev or "never")}</span>')

def version_html(pg):
    v = (pg.get("derived") or {}).get("version")
    return f'<span>Version {esc(v)}</span>' if v else ""

def direction_html(pg):
    d = pg.get("direction")
    if not d:
        return ""
    body = "".join(f"<p>{x}</p>" for x in d.get("body", []))   # the state file holds trusted, hand-written HTML here
    return (f'<div class="note"><span class="eyebrow">{esc(d.get("eyebrow", "Direction"))}'
            f' &middot; confirmed {esc(d.get("confirmed", "?"))}</span>'
            f'<h3>{esc(d.get("title", ""))}</h3>{body}</div>')

def queue_html(pg):
    q = (pg.get("derived") or {}).get("queue")
    if not q:
        return "<p class='foot'>No queue data.</p>"
    cls = {"running": "p-next", "queued": "p-todo", "done": "p-ok", "stopped": "p-no"}
    rows = ([q["running"]] if q.get("running") else []) + q.get("queued", []) + q.get("finished", [])
    trs = "".join(
        f'<tr><td class="n">P{r["n"]}</td><td>{esc(r["slug"].replace("-", " "))}</td>'
        f'<td><span class="pill {cls.get(r["state"], "p-todo")}">{esc(r["state"])}</span></td>'
        f'<td class="foot">{esc(r.get("since") or r.get("date") or "")}'
        f'{(" &middot; " + esc(r["why"])) if r.get("why") else ""}</td></tr>' for r in rows)
    run = q.get("running")
    lead = (f'P{run["n"]} running' if run else "nothing running") + f', {len(q.get("queued", []))} queued'
    ld = q.get("latest_done")
    return (f'<div class="card"><div class="hero"><span class="big">{esc(lead)}</span>'
            f'<span class="cap"><strong>Golem {esc(q.get("autopilot"))}.</strong> {q.get("finished_total", 0)} '
            f'prompts finished, {q.get("stopped_total", 0)} stopped early'
            + (f'; latest done P{ld["n"]}.' if ld else '.') +
            ' Read from <code>D:\\UO\\cc-prompts\\queue</code>, the Golem\'s <code>state.json</code> and each '
            'prompt\'s notes, every run.</span></div></div>'
            '<div class="scroller"><table><thead><tr><th class="n">Prompt</th><th>Task</th><th>State</th>'
            f'<th>When</th></tr></thead><tbody>{trs}</tbody></table></div>'
            '<p class="foot">The ten most recently numbered finished prompts are shown.</p>')

def playtests_html(pg):
    pt = (pg.get("derived") or {}).get("playtests")
    if not pt:
        return "<p class='foot'>No play-test data (testing/play-tests.json).</p>"
    unlogged = pt.get("unloggedFails") or 0
    return (f'<div class="card"><div class="hero"><span class="big">{pt.get("open", 0)} open</span>'
            f'<span class="cap"><strong>{pt.get("failed", 0)} failed, {pt.get("passed", 0)} passed</strong>, '
            f'{pt.get("later", 0)} later, {pt.get("blocked", 0)} blocked, {pt.get("total", 0)} in all.'
            + (f' <strong>{unlogged} failure(s) not yet in the bug list.</strong>' if unlogged else '') +
            '</span></div></div>'
            '<p class="foot">From <code>testing/play-tests.json</code> (the play-test page writes it). '
            '<a class="lan" data-port="8093" data-path="/" href="http://' + LAN_HOST + ':8093/">Open the play-test page</a>.</p>')

# cc-P88: the shared menu's one source, in the shard repo beside the play-test page that serves it.
NAV_JS = Path(os.environ.get("SL_SHARD", r"D:\ShatteredLegacy")) / "docker" / "test-queue" / "html" / "nav.js"

def nav_html():
    """nav.js, inline, so the page has the same menu served at :8093/status and opened from disk. None when the file
    cannot be read: the block is then left as it is, never emptied."""
    try:
        js = NAV_JS.read_text(encoding="utf-8")
    except OSError as e:
        print(f"  nav.js not read ({e}); the menu block is left as it was", file=sys.stderr)
        return None
    if "</script" in js.lower():
        print("  nav.js contains </script; not inlined, the menu block is left as it was", file=sys.stderr)
        return None
    return '<script data-sl-page="status">\n' + js.rstrip("\n") + '\n</script>'

def replace(txt, tag, body):
    s, e = f"<!-- DATA:{tag} -->", f"<!-- /DATA:{tag} -->"
    if s not in txt or e not in txt: return txt, False
    return re.sub(re.escape(s) + r".*?" + re.escape(e),
                  lambda _: s + "\n" + body + "\n" + e, txt, flags=re.S), True

def replace_inline(txt, tag, body):
    """As replace(), with no line breaks around the body (for markers inside a line)."""
    s, e = f"<!-- DATA:{tag} -->", f"<!-- /DATA:{tag} -->"
    if s not in txt or e not in txt: return txt, False
    return re.sub(re.escape(s) + r".*?" + re.escape(e), lambda _: s + body + e, txt, flags=re.S), True

def main():
    if not DASH.exists():
        print(f"  dashboard.html not found at {DASH}", file=sys.stderr); return 1
    pg, ex = load("progress.json"), load("expansion-coverage.json")
    if not pg: print("  progress.json missing; run progress.py first", file=sys.stderr); return 1
    txt = DASH.read_text(encoding="utf-8"); hit = []
    gen = datetime.now().astimezone()
    hdate = gen.strftime("%Y-%m-%d")
    secs = pg.get("sections") or {}
    gates = (pg.get("playable_gates") or {}).get("gates", [])
    tdates = [t.get("confirmed", "") for t in (pg.get("tasks") or [])]
    pt = (pg.get("derived") or {}).get("playtests") or {}
    asof = {
        "PLAYABLE": max([g.get("confirmed", "") for g in gates] or [""]),
        "TASKS": max(tdates or [""]),
        "FOUNDATION": secs.get("foundation", ""),
        "PATCHES": (pg.get("upstream_patches") or {}).get("confirmed", ""),
        "PLAYTESTS": str(pt.get("generatedAt") or "")[:10],
        "CORRECTIONS": secs.get("corrections", ""), "PORTLIST": secs.get("portlist", ""),
    }
    for tag, d in asof.items():
        txt, _ = replace_inline(txt, "ASOF-" + tag, asof_html(d, hdate))
    for tag, body in (("REVIEWED", reviewed_html(pg)), ("VERSION", version_html(pg))):
        txt, ok = replace_inline(txt, tag, body)
        if ok: hit.append(tag)
    nav = nav_html()
    if nav is not None:
        txt, ok = replace(txt, "NAV", nav)
        if ok: hit.append("NAV")
    for tag, body in (("DIRECTION", direction_html(pg)),
                      ("QUEUE", queue_html(pg)),
                      ("PLAYTESTS", playtests_html(pg)),
                      ("HEADLINE", headline_html(pg)),
                      ("PLAYABLE", playable_html(pg)),
                      ("FOUNDATION", foundation_html(pg)),
                      ("EXPANSION", expansion_html(ex)),
                      ("CONTENT", portlist_html(pg)),
                      ("TASKS", tasks_html(pg)),
                      ("PATCHES", patches_html(pg))):
        txt, ok = replace(txt, tag, body)
        if ok: hit.append(tag)
    txt = re.sub(r"<!-- DATA:GENERATED -->.*?<!-- /DATA:GENERATED -->",
                 lambda _: f"<!-- DATA:GENERATED -->{gen:%Y-%m-%d %H:%M}"
                           "<!-- /DATA:GENERATED -->", txt, flags=re.S)
    DASH.write_text(txt, encoding="utf-8", newline="\n")
    print(f"  dashboard.html updated ({', '.join(hit) if hit else 'no markers found'}).")
    return 0

if __name__ == "__main__":
    sys.exit(main())
