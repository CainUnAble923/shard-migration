# cc-P92: the status page tracks the ServUO port list (2026-10-13)

## Headlines

- The status page headline is now the port list, not "candidate content":
  "Port list: 1 of 16 systems in. 283 of 983 files (29%)." Next to land: Bulk orders, all crafts.
- Chase's decisions are recorded. Pet Training moved to the Port tier, right after Creatures, which makes
  16 systems. No Decide tier is left; the page still renders one if a row is ever marked decide. The
  direction line sits under the headline and in tools/README.md: "A faithful port comes first, our
  feature customizations after it; work already started or already requested is still finished."
- tools/port-list.json is the list progress.py reads. It is a copy of notes/port-list-2026-10-13.json,
  which now carries the decision and a "Decided 2026-10-13" line in its .md twin.
  tools/port-triage.json moved to tools/obsolete/ along with the script that wrote it.
- 8 new tests in tools/tests/test_port_list.py. Each behavior was broken on its own first and its test
  was seen failing.

## Numbers versus expected, and why they differ

The port-list note (written earlier today) expected Port 222 of 905 files and 2,753 candidates. Today's
trees count Port 283 of 983 files and 2,850 candidates, with 0 unassigned. The whole difference is in
three rows:

| Row | Noted | Counted now | Difference |
|---|---|---|---|
| Base items (Port) | 106 of 220 | 167 of 298 | +78 files, +61 done |
| Reward pool | 708 | 717 | +9 files |
| Ride-along | 351 | 361 | +10 files |

- In the Port tier, 983 - 905 = 78 files and 283 - 222 = 61 done, exactly the Base items row.
- In candidates, 78 + 9 + 10 = 97 = 2,850 - 2,753.
- The Base items gap is almost all Items/Equipment (Armor, Suits, Weapons, Jewelry), most of it
  already ported.
- I could not reproduce the noted numbers from the trees, so the page shows what the counter finds
  (AGENTS.md: counts follow the source, never the document). Every other row matches the note.
- Per row today:
  - Bulk orders 0/28, Treasure maps 0/2, Monster stealing 0/14.
  - Despise and Shame 15/15 (in).
  - Blackthorn 3/147, Covetous 2/29, Wrong 2/26, Exodus 1/38, Underworld 3/27.
  - Creatures 80/193, Pet Training 0/11, Eodon 6/19, High Seas 4/59.
  - Crafting gaps 0/33, Food 0/44, Base items 167/298.
  - Not counted: Ride-along 11/361, Reward pool 288/717, Design source 3/178, Later 12/307, Dropped 5/304.

## What moved on the page

- Headline. Before: "27% of candidate content ported. 551 of 2045 ServUO files that ModernUO does not
  already ship."
  After: the hero is "1 / 16", followed by the Port list line and Next to land, the direction line,
  and a caveat (counted by filename stem, not behavior; the list is kept by hand in tools/port-list.json).
- The "Moved over" section is now "Port list: ServUO content still worth porting".
  - It has one row per Port system with done, files, a bar and what it feeds, then a Port tier total row.
  - Each uncounted tier (Ride-along, Reward pool, Design source, Later, Dropped) is a collapsed
    details block showing its file count, how many are in, what it means and its systems.
  - The old by-area table is kept, collapsed, as "Every ServUO file ModernUO lacks, by area (scale, not
    a target)".
- The "Content backlog" and "Deferred" sections are retired. Expansion, Maintenance and the Correction
  log stay.
- The section dates in tools/progress-state.json now read foundation and portlist 2026-10-13.
- The README progress block has the same headline, Next to land, direction line, the Port-tier table and a
  "Not counted" line. The old area breakdown is renamed "Every ServUO file ModernUO lacks, by area (not a
  target)".
- progress.json gains a port_list object: systems, tiers, counted, next, unassigned and decided.

## Proof

- Before and after text dumps of the HEADLINE and CONTENT blocks were taken from dashboard.html (summarized
  above). Before, the "Content backlog" and "Deferred" sections were present; after, both are absent.
- progress.py was run twice in a row. The second run changed only the time: "Last updated" in
  dashboard.html and "generated" in progress.json. README.md had no diff.
- dashboard.html renders on its own from file:/// in headless Edge, with the shared menu, the Port list
  headline, Next to land and the collapsed tiers.
- Red proof. Each break was applied to progress.py alone, the port-list tests were run, and the file was
  restored byte-identical:
  - First match removed: 3 tests failed.
  - Exclude ignored: 1 failed.
  - Unassigned files dropped silently: 1 failed.
  - Decide and reward counted in the headline: 1 failed.
  - Next to land ignoring "in": 1 failed.
- Green: test_port_list, test_status_dashboard and test_feature_ideas, 34 tests, OK.
- CHANGELOG (D:\ShatteredLegacy): 2026.10.13.12 was already committed with P91, so a new section
  2026.10.13.13 holds the Staff line "Status page tracks the ServUO port list instead of every ServUO file."
  VERSION is 2026.10.13.13. The wiki was not published.

## Deviations and decisions for Chase

- Count drift: 283 of 983 instead of the noted 222 of 905, explained above. If the note's numbers came
  from a different rule (for example, Equipment counted elsewhere), say so and I will move those prefixes
  in tools/port-list.json. Until then the page shows the counter.
- docs/port-triage.md line 85 still points at tools/port-triage.json. Agents do not edit docs/; the file
  now lives at tools/obsolete/port-triage.json.
- The hand-off asked for a task list Chase can follow. This session has no task-list tool, only
  scheduled tasks, so progress was given step by step in chat instead.
- testing/SUMMARY.md and testing/play-tests.json were already modified when P92 started. They come from
  the play-test importer, not from this task, and are left as found; the preflight will include them.
- The README Port-tier table uses the same block-character bars progress.py already drew in that
  progress block (the old "Content" bar line had them too). So README.md gains non-ASCII bars, as it
  always has. Every file this task wrote by hand is plain ASCII.
- The prompt called this a Staff change in D:\ShatteredLegacy, so that repo's CHANGELOG and VERSION are
  touched even though the code change is in shard-migration.

## For Chase

Notes on the port list file, tools/port-list.json:

- Each system has an id, a tier (port, ride, reward, source, later, drop, or decide to put it on hold
  with you), a title, feeds, why, path prefixes and an optional exclude regex.
- A ServUO file belongs to the first system, in file order, whose prefix matches and whose exclude does
  not. Order matters: put narrow prefixes above wide ones.
- Only the port tier counts toward the headline. Next to land is the first port row that is not fully in,
  so reordering port rows changes what the page says comes next.
- After an edit, run python tools/progress.py. Any file no system claims is listed under "unassigned" on
  the page and in progress.json, never dropped.

## Preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`

```
Repo Result
---- ------
code dry run
docs dry run
```

P92 DONE
