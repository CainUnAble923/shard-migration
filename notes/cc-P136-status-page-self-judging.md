# cc-P136: The status page keeps its own judgments current, and lists what still needs the overseer

Prompt: `D:\UO\cc-prompts\cc-P136-status-page-self-judging.md`. Both repos were clean at the start. Not committed (the
Golem commits after DONE).

## Headlines

- **The page now opens with "Needs overseer review".** It lists only what the machinery cannot judge. Each line says what
  to check and gives the exact `judge.py` command that settles it. When nothing is owed it reads "Nothing owed". If
  working the box out fails, it says so instead of reading as empty.
  - Today it holds **one line**: the direction was confirmed 2026-10-13, but `notes/decisions-2026-10-14.md` is newer.
    The fix is `python tools/judge.py confirm direction`, after reading the note.
- **Four judgments are derived on every refresh and never stored.** Systems that are in, tasks covered by the port list,
  STOPPED prompts never counting, and next to land. They are listed below.
- **C2, C3, C4, C5, C7 and S7 are retired** with `judge.py retire-task`, each stamped 2026-10-17 with a reason (C6 was
  already retired by P85). The task list goes from 1 of 13 to **1 of 7**. The port list's `covers` field now names the
  system behind each retired row, so a re-added row would show as covered, not counted twice.
- **Never decides for Chase.** `judge.py gate|task ... --needs-confirm "..."` puts an item in the box until a person
  decides. `confirm all`, a detail edit or a refresh never clears it, and `progress.py` never writes
  `progress-state.json`.
- **The refresh still never blocks a commit.** A derived step that fails prints one line and the rest refreshes. A crash
  of `progress.py` as a whole prints one line and exits 1. The commit script now shows that line as the reason and
  commits anyway.
- **Tests:** 17 new in `tools/tests/test_self_judging.py`, all seen failing first (17 of 17 red before the code). Then 12
  deliberate breaks, one per rule, were each caught. Dashboard, port-list and new tests: 52 of 52 pass with
  test_feature_ideas.

## The derived rules

Computed in `tools/progress.py` on every run (the comment block at `tools/progress.py:310-321` lists them):

1. **A port-list system whose candidate files are all ported is "in".**
   - `port_list()`, the `complete` flag, as P92 built it.
   - New: the system's `covers` list is carried to the page (`tools/progress.py:122`).
2. **A task covered by a port-list system is shown as covered by it, not counted twice.**
   - `split_tasks()` (`tools/progress.py:334`). A task whose id appears in a system's `covers` list
     (`tools/port-list.json`) goes under the task table as "Covered by the port list", with the systems' summed done and
     files. It is marked "in" when every covering system is in, and it is left out of the task totals.
   - `progress.json` now carries `tasks` (the own rows) and `tasks_covered`.
3. **A prompt that ended STOPPED never counts as progress.**
   - `queue_state()` adds `done_total`, DONE only (`tools/progress.py:276`). The page and README say "N prompts done; M
     more stopped early, never counted as progress". Before, they said "N prompts finished", with stopped ones included.
   - `latest_done` already skipped STOPPED.
   - In the review box, only a DONE prompt can make a task row owe a review.
4. **"Next to land" follows the port list.** It is the first Port row, in `port-list.json` order, that is not in
   (`port_list()`, as P92 built it). The rule is now pinned by a test here as well as test_port_list's.

And the review box (`review_owed()`, `tools/progress.py:376`). A line is owed when:

- a **gate or task carries `needs_confirm`** (set only by `judge.py --needs-confirm`). Its commands are
  `judge.py gate "<name>" --done yes|no --detail "..."` or `judge.py confirm gate "<name>"`; for a task,
  `judge.py task <id> --status ... --note "..."` or `judge.py confirm task <id>`;
- a **gate** was last confirmed **more than 7 days** ago (`REVIEW_DAYS = STALE_DAYS`, the page's amber rule). The
  commands are `confirm gate`, or `gate ... --done`;
- a **task row** was last confirmed more than 7 days ago, and a prompt it names finished DONE after that date. A task
  names a prompt with `P80`, `P65-P84` or `P65-84` in its title or note, or with an optional `prompts` list. Its commands
  are `judge.py task <id> --status ...` or `confirm task <id>`;
- the **shard status** was last confirmed more than 7 days ago. Its commands are `judge.py status "..."` or
  `confirm status`;
- the **direction** was confirmed before the newest `notes/*decision*.md`, dated by the YYYY-MM-DD in its name, else
  its file date. The fix is to edit `direction` in `progress-state.json` if it moved, then
  `python tools/judge.py confirm direction`.

## Rows retired

All six were retired with `python tools/judge.py retire-task <id> --why "..."` on 2026-10-17. Each is kept in
`tasks_retired` with `"retired": "2026-10-17"` and the reason. The mapping is P92's ("For the overseer" in
`notes/port-list-2026-10-13.md`), now also recorded as `covers` in `tools/port-list.json`:

| Row | Was | Covered by |
|---|---|---|
| C2 | Revamped Dungeons | Despise and Shame, Blackthorn, Covetous, Wrong, Exodus, Underworld (Port rows) |
| C3 | High Seas, cheap half | High Seas, fishing half (Port row) |
| C4 | Creatures and NPCs | Creatures (Port row); NPCs ride along with the systems that use them |
| C5 | Decoration, housing, crafting | Crafting gaps, Base items (Port rows); decoration and housing in the Reward pool tier |
| C7 | High Seas naval, proposal only | Later tier |
| S7 | Services/PointsSystems | Design source tier (P33 built ours); Vice vs Virtue and City Loyalty are Dropped |
| C6 | Artifacts and equipment | already retired by P85 on 2026-10-13; nothing to do |

The row notes said "unchanged, no prompt has taken it" (C3, C5), "do not start" (C7) and "partly superseded" (S7).
Nothing in them is lost: the port list rows carry the same work with live counts.

## What changed

- `tools/progress.py`
  - `:122`: `port_list()` carries `covers`.
  - `:274-276`: `queue_state()` adds `done_total`.
  - `:310-458`: rules comment, `safely()`, `split_tasks()`, `prompt_refs()`, `newest_decisions_note()`, `review_label()`
    and `review_owed()`.
  - `:465-478`: `build()` computes both steps through `safely()`, and the README block opens with the review list.
  - The task table counts only the task's own rows and lists the covered ones under it. The Queue heading counts
    done only. `progress.json` gains `tasks_covered` and `review`.
  - `:701-706`: `main()` turns a crash into one line and exit 1.
- `tools/render_dashboard.py`
  - `:229`: `covered_html()`.
  - `:240`: `review_html()`, which has three states: owed, nothing owed, and could not be worked out.
  - `:323`: the queue counts done only.
  - `:402`: the REVIEW marker.
- `dashboard.html:287-292`: a new first section, "Start here / Needs overseer review", with a `DATA:REVIEW` marker.
- `tools/judge.py`
  - `:62`: `mark()`.
  - `--needs-confirm` on `gate` and `task`.
  - `confirm gate|task` clears the mark; `confirm all` does not.
  - `retire-task --why` appends `{id, title, retired, why}` to `tasks_retired`. Before, the row was dropped with no
    record.
  - `list` shows marks.
  - The docstring describes all of this.
- `tools/port-list.json`: `covers` on 13 systems, and a top-level `covers` comment. The note's twin
  `notes/port-list-2026-10-13.json` was left as it was: it is the dated decision record, and `tools/` is the live copy.
- `tools/progress-state.json`: six rows moved to `tasks_retired`, and `sections.tasks-reviewed` is 2026-10-17
  (`retire-task` already stamped that). A backup of the file before this task is in the session scratchpad.
- `D:\UO\Commit-ShardWork.ps1:109-126` (backed up first to `D:\UO\Commit-ShardWork.ps1.bak-P136`)
  - Each output record of `progress.py` is turned into plain text, so PowerShell 5.1's NativeCommandError wrapping never
    becomes the reason.
  - Any "not worked out" lines are shown.
  - A failed run prints `dashboard refresh failed (<code>: <last line>); committing anyway`.
  - It is still skipped on `-DryRun`, and still in try/catch. The script is ASCII, and its parse check is clean.
- `tools/README.md:114-148`: the new judge.py lines, and a section on the derived rules and the box.
- `tools/tests/test_self_judging.py`: new.
- `D:\ShatteredLegacy\CHANGELOG.md`: a new section, 2026.10.17.6, with one `### Staff` line. `VERSION` is 2026.10.17.6.
  The wiki page was not published.
- Regenerated by the refresh: `README.md`, `dashboard.html`, `tools/progress.json`.

## Tests

`python -m unittest tools/tests/test_self_judging.py`, 17 tests:

- **Derived rules:**
  - a system is in exactly when every file is ported, next to land is the first Port row not in, and covers reaches
    the page;
  - covered tasks are listed apart and not counted, case-insensitive ids, "in" only when every covering system is in,
    and no port list means nothing is covered;
  - a STOPPED prompt is not in done_total, and the page never adds it to the done count.
- **Review box:**
  - nothing owed renders "Nothing owed" with no lines;
  - a needs_confirm gate is owed with both commands, and stays not done;
  - a gate at 8 days is owed, at 7 days it is not; a stale status is owed;
  - a task row is owed when a named prompt (in a P65-P84 range) finished DONE after its date, and not for a STOPPED
    prompt or a freshly confirmed row;
  - a prompt that finished before the row's date owes nothing;
  - the direction is owed when it is older than the newest decisions note;
  - box lines are HTML-escaped and their commands shown;
  - a failed review reads as "could not be worked out", never as empty.
- **Refresh:**
  - a failing step writes one line and returns its fallback;
  - the commit script still says "committing anyway" and gives the reason.
- **judge.py:**
  - needs_confirm survives `confirm all` and a detail edit, and clears on `confirm gate`;
  - `retire-task --why` keeps a dated record.
- **Real files:** C2-C7 and S7 are out of `tasks` and in `tasks_retired` (the six dated today, with "port list" in the
  reason), and every one of them is in some system's `covers`.

**Red first.** Before any code: `Ran 17 tests ... FAILED (failures=3, errors=14)`. Every new test was red. Three more
failures after the first code were in the tests themselves (`assertIn` on a list instead of its joined text) and were
fixed in the tests.

**Breaks, one at a time.** Each break was applied to the code alone, then the three dashboard test files were run, then
the file was restored byte-identical (checked; `__pycache__` cleared each time):

| Break | Caught by |
|---|---|
| rule 1: a system is in with one file missing | 3 failures (this file and two in test_port_list) |
| rule 2: covered tasks still counted | 1 |
| rule 3: stopped counted in done_total | 1 |
| rule 3: a stopped prompt owes a task review | 1 |
| rule 4: next to land ignores "in" | 2 |
| review: gate stale at 7 days instead of 8 | 1 |
| review: needs_confirm ignored | 1 |
| review: direction never owed | 1 |
| render: a failed review reads as empty | 1 |
| judge: confirm all clears needs_confirm | 1 |
| judge: retire without a dated record | 1 |
| refresh: a failing step raises | 1 error |

Baseline and after restore: OK.

**Green.**
- test_self_judging 17, test_status_dashboard 15, test_port_list 8 and test_feature_ideas 12: all OK.
- The rest of `tools/tests`: bot_tonight, bug_reports, haven_h1, opsmirror and playtests_reopen pass.
- **test_play_who fails 2 tests, the same 2 with this task's changes stashed.** They check the real
  `testing/play-tests.json`: 40 open items have no "Who", and P122-2 has a step missing its check or do half. That is
  the Haven mirror's data, not this task's.

**Commit script failure path.** A scratch copy of the new block was run against a fake `progress.py` that prints a
"not worked out" line and a failure line and exits 1. It printed:

```
  review box not worked out (KeyError: x); the rest of the page is refreshed
  dashboard refresh failed (1: progress.py failed: ValueError: bad state; the page was left as it was); committing anyway
carried on after the refresh
```

**Real refresh.**
- `python tools/progress.py` exits 0. It updated README and dashboard.html with the REVIEW marker among those hit.
- README opens with "### Needs overseer review (1)" and the direction line.
- Tasks read 1 of 7. The queue reads "85 prompts done; 3 more stopped early, never counted as progress".
- The dashboard opened in headless Edge from `file:///D:/UO/shard-migration/dashboard.html`. The red-bordered box sits
  first under the header, with the one direction line and its command in code; Overall and Playable follow unchanged.

## Deviations and decisions for Chase

1. **No task-list tool in this session.** The hand-off asked for one task per step. Only scheduled tasks exist here, so
   progress went step by step in chat, as P92 noted too.
2. **Two owed rules beyond the prompt's three examples:**
   - a gate older than 7 days, the page's existing amber rule, now with a command;
   - the shard status older than 7 days. The status text still says "P65-P84 are committed, not deployed" (confirmed
     2026-10-13), so it will appear in the box on 2026-10-21 unless someone re-confirms or rewrites it.
3. **"Gates that need confirmation" is a mark, not a guess.** No rule can tell that a gate is met, so the box shows
   only what a person marked with `--needs-confirm`, plus stale dates. A port-list "in" never flips a gate.
4. **A task names its prompts by Pnn in its title or note,** or a `prompts` list. A row that names no prompt never owes
   the "related prompts finished" line. It still turns stale under the 7-day amber date of the whole judgment.
5. **C5 includes the Reward pool tier,** for decoration and housing. That tier is never counted, so a re-added C5 could
   never read "in". That is accurate: decoration is ported when a reward table asks.
6. **`notes/port-list-2026-10-13.json` was not given `covers`.** `tools/port-list.json` is the live copy that
   `progress.py` reads.
7. **`Judgment reviewed` stays 2026-10-13.** Retiring rows stamps `sections.tasks-reviewed`, which is not a `confirmed`
   date, so the header does not claim a review nobody did. The one owed line, the direction, is left for the overseer:
   reading `decisions-2026-10-14.md` and deciding whether the direction moved is the overseer's job.
8. **testing/SUMMARY.md and testing/play-tests.json** were changed by the dry run's Haven mirror (machine output). They
   are left as found.

## For Chase

The status page now keeps itself current; the "Needs overseer review" box is what a new overseer checks first.

## Patch notes

`D:\ShatteredLegacy\CHANGELOG.md` 2026.10.17.6 `### Staff`: "The shard status page keeps its own judgments current and
opens with a "Needs overseer review" box listing what only the overseer or Chase can settle, each with the one command
that settles it." `VERSION` 2026.10.17.6. Not published.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`:

```
Repo Result
---- ------
code dry run
docs dry run
```

No file over 5 MB is pending. The one large file in the tree, `notes/cc-P34-tools/town.png`, is older than this task
and ignored: `git check-ignore -v` gives `.gitignore:25:notes/cc-P*-tools/*.png`.

P136 DONE
