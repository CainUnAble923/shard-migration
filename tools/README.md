# Migration tools

## `spawner-json-to-xmlspawner`

`spawner_json_to_xmlspawner.py` converts the JSON produced by ModernUO's
`ExportSpawners` command into the native DataSet XML consumed by ServUO pub57's
XmlSpawner loader:

```console
python tools/spawner_json_to_xmlspawner.py modernuo-spawns.json servuo-spawns.xml
```

The default is deliberately strict. Unsupported spawner types or behavior stop the
conversion without writing output. `--skip-unsupported` writes only verified rows and
prints every skipped spawner. `--allow-z-loss` explicitly accepts that XmlSpawner cannot
preserve ModernUO's bounds/region Z-selection behavior; both options are intentionally
lossy.

Currently source-verified mappings: ordinary `Spawner`, `RegionSpawner`, legacy home
range, total and per-entry counts, whole-second delays, team, walking/home range,
map/location, XY bounds, and region name.
Not verified and therefore rejected: `ProximitySpawner`, per-entry probability other
than 100, entry constructor parameters/properties, non-default position optimization,
and non-default maximum spawn attempts. Exact Z-selection parity
remains unverified and cannot be represented directly by XmlSpawner.

Run its tests with:

```console
python -m unittest tools/test_spawner_json_to_xmlspawner.py
```

## `muo-accounts-to-servuo-xml`

`modernuo/ExportServUOAccounts.cs` is a temporary owner-only ModernUO command that walks
the live account collection and atomically emits a ServUO-shaped
`Export/ServUO/accounts.xml`:

1. Copy it into `Projects/UOContent/Commands/` in the pinned ModernUO build tree.
2. Rebuild and restart ModernUO.
3. Run `[ExportServUOAccounts` as an Owner.

The command refuses to write anything unless every account has a valid SHA2 hash. The
output contains password hashes, login IPs, comments, tags, email addresses, and character
serials; handle it as a secret and never commit it.

Key detail: the SHA512 digests are byte-identical between the engines, but ServUO stores
`BitConverter.ToString` output (hyphenated hex, `A1-B2-C3`) and ModernUO stores unseparated
hex (`A1B2C3`). Insert a hyphen every two characters on the way out.

The exporter writes stock ServUO's `totalCurrency` value and also preserves ModernUO's
exact gold, platinum, and email values in `modernUO*` extension elements. Stock ServUO
ignores those extension elements. `servuo/Account-modernuo-email.patch` loads the email
extension and makes subsequent ServUO saves retain it. Exact high-balance currency
preservation remains unresolved because ServUO's in-memory account model uses `double`.

Compilation was verified against ModernUO `7c9215d97` (the pin until cc-P38) and is not re-verified against `d4531cd94`; executing it against live accounts
and loading the result in ServUO remain unverified.

## `content_index.py` (D20, 2026-09-27)

The S3/S9 content index, kept as a tool instead of rebuilt and thrown away. Read-only against all three trees.
`--legacy` is S9's method and reproduces S9's artifacts row file for file; the default adds the D20 fixes (alias strings
count as declarations, every secondary type of a discarded file is reported) and splits S9's `upstream` bucket into
`upstream` (a patch), `extract` (a type inside a discarded file) and `unknown` (read it). See `notes/index-blindspots.md`.

```console
python tools/content_index.py row artifacts             # candidates bucketed; also cc4, cc7, cc7extra, cc5
python tools/content_index.py hidden artifacts          # secondary types of discarded files, classified. NOT a backlog
python tools/content_index.py filter                    # step 1 alone
python tools/content_index.py compare-s9 artifacts --ours <tree>   # legacy vs S9's appendix, then S9 -> fixed
python -m unittest tools/test_content_index.py          # regression, ~8 s
```

`hidden` output is classified mechanically; `unresolved` means read it. Never quote its total as content.

## `save_instance_check.py`

The re-parenting window check (`docs/gap-register.md`) as a script: does any save artefact on this machine hold
an instance of the named types? Reads every `SerializedTypes.db` under the live save, `Saves-test`, each
`Backups/Automatic` snapshot and the two newest archives of each kind (needs `pip install --user zstandard`), with
`Server.Items.Dagger` as a positive control on each. Read-only.

```console
python tools/save_instance_check.py SpiritualityHelm ValorGauntlets
```

## The status dashboard: `progress.py`, `render_dashboard.py`, `judge.py` (cc-P85)

`dashboard.html` ("Shard status") and the progress block in `README.md` are rebuilt by `python tools/progress.py`.
`D:\UO\Commit-ShardWork.ps1` runs it before every commit, so the counts are never older than the last commit.
On the home network the page is at `http://192.168.1.58:8093/status` (served by `sl-play-tests`, docker/test-queue).

What a person keeps and what the script derives:

| Kept by hand in `progress-state.json`, each with a `confirmed` date | Derived by `progress.py` on every run |
|---|---|
| shard status line, direction note, playable gates (with sources), tasks, setup defects, the static sections' as-of dates; and the port list itself, `port-list.json` (cc-P92) | file and test counts, the port list's per-system counts and next to land, content and expansion coverage, the CC prompt queue (queued, running, done, stopped), play-test counts, VERSION, the latest DONE prompt, "Judgment reviewed" (the newest `confirmed` date) |

The page header shows "Last updated" (when the counts ran) and "Judgment reviewed". The review date turns amber
when it is more than 7 days old (`STALE_DAYS` in progress.py). A section whose own date differs from the header's
says "As of <date>".

### Updating one item (the overseer)

Re-read the item's sources, then one line:

```console
python tools/judge.py list                                        # everything, with its date
python tools/judge.py gate "Things to fight" --done no --detail "..." --source "notes/cc-P90-....md"
python tools/judge.py confirm gate "Things to fight"              # still true: only the date moves
python tools/judge.py task DEPLOY --status done --note "deployed 2026-10-14"
python tools/judge.py add-task F-44 --title "..." --note "..."
python tools/judge.py retire-task C3 --why "..."                 # kept in tasks_retired with today's date
python tools/judge.py gate "Things to fight" --needs-confirm "Chase: ..."   # owed on the review box until decided
python tools/judge.py status "the test shard ..."
python tools/judge.py confirm all                                 # after a full review
python tools/progress.py                                          # redraw the page (or just commit)
```

A gate is named exactly or by a unique start. Every write stamps today's date, so "Judgment reviewed" moves only when
someone actually confirmed something. Tests: `python -m unittest tools/tests/test_status_dashboard.py`.

### What the page judges for itself, and the "Needs overseer review" box (cc-P136)

`progress.py` works these out on every run; nobody stores them:

1. A port-list system whose candidate files are all ported is **in**.
2. A task whose id a port-list system lists under `covers` (in `port-list.json`) is **covered by** that system: shown
   under the task table with the system's counts, and left out of the task totals.
3. A prompt whose notes end `STOPPED` is **never progress**: not in the done count, never "latest done", and it never
   makes a task row owe a review.
4. **Next to land** is the first Port row, in `port-list.json` order, that is not in.

The page opens with **Needs overseer review**: what it cannot judge for itself, one line per item with the
`judge.py` command that settles it. A new overseer checks it first. A line is owed when:

- a gate or task carries `needs_confirm` (Chase's or the overseer's call). Nothing sets it from the facts; only a
  decision clears it (`gate --done`, `task --status`, `confirm gate` or `confirm task` on that item). `confirm all`
  and detail or note edits keep it;
- a gate or the shard status was last confirmed more than 7 days ago;
- a task row was last confirmed more than 7 days ago and a prompt it names (`P80`, `P65-P84`, or a `prompts` list)
  finished DONE after that date;
- the direction was confirmed before the newest `notes/*decision*.md` (dated by its file name).

An empty box says "Nothing owed". If working the box out fails, the page says so rather than showing it empty, and
the rest still refreshes: each step that fails prints one line, and the commit script shows that line and commits
anyway. Tests: `python -m unittest tools/tests/test_self_judging.py`.

### The port list: `port-list.json` (cc-P92)

The page's headline is the **ServUO port list**: ServUO content still worth porting given the shard's direction, in
tiers. **Direction (Chase, 2026-10-13): a faithful port comes first, our feature customizations after it; work already
started or already requested is still finished.**

- **`tools/port-list.json` is hand-kept judgment**, like `progress-state.json`: the overseer edits it, and `progress.py`
  only reads it. Each system has an `id`, a `tier`, a `title`, what it `feeds`, the `prefixes` it claims under
  ServUO's `Scripts/`, and an optional `exclude` regex. The decision and its reasons are
  `notes/port-list-2026-10-13.md`.
- **Tiers:** `port` counts toward the headline. `decide` is shown as waiting on Chase and counts once moved to
  `port`. `ride`, `reward`, `source`, `later` and `drop` are shown, never counted.
- **How `progress.py` counts it** (`port_list()`):
  - Every `.cs` under `Scripts/Services`, `Items` and `Mobiles` whose lowercased stem is not in
    `modernuo-stems.txt` is a candidate.
  - It is done when the stem exists under `server/customizations`: filename stems, not behavior.
  - Each candidate belongs to the **first** system, in file order, whose prefix matches and whose `exclude` does not.
  - Candidates no system claims are listed on the page (count and the first 20), so a new ServUO file shows up
    instead of vanishing.
- **To change it:**
  - Move a system between tiers by editing its `tier`.
  - Reorder the `port` rows to change **"Next to land"**, which is the first `port` row, in file order, that is not
    complete.
  - Then `python tools/progress.py` redraws the page and README (a commit does it too).
  - Order also decides which system claims a file, so put a narrow prefix before a wide one.
- Tests: `python -m unittest tools/tests/test_port_list.py`.
- `tools/obsolete/port-triage.json` (moved there by cc-P92) is the 2026-09-06 triage of our own customizations for
  the migrate-to-ServUO plan that was not taken. Nothing reads it.
