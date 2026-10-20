# cc-P220: Crystal refreshes the status page's hand-written judgments

2026-10-20. Prompt: `shattered-legacy-prompts/claimed/Crystal/cc-P220-crystal-status-page-judgments.md` (claimed from
`queue/` at 21:25 UTC). Golem: Crystal, a Claude Code cloud session (machine `CLOUD`), GitHub only. Branch
`golem/Crystal/P220` in `shard-migration`, cut from `origin/main` (`73791eb`). Code repo read at `main` `7049a69`
(version 2026.10.20.4); nothing changed there.

## Headlines

1. **Every hand-written row was re-judged and re-dated 2026-10-20 through `judge.py`**: the shard status, the
   direction, the 11 playable gates, the 6 live tasks (and 1 retired), and the port-list section. **No gate changed
   its yes or no**: 2 of 11 stay met. What changed is the evidence under each, which was a week old and in four
   places wrong about the code (the skill-gain rate, the creature batches, the tutorial's decisions, the live shard).
2. **Three rows now carry `--needs-confirm` for Chase**, because the cloud cannot see the game PC: which build the
   test shard runs (gate "What is built is seen in a client" and task DEPLOY), and which player package is published
   (gate "The player package installs on a clean PC"). The page's "Needs overseer review" box lists them with the one
   command each that settles it.
3. **The direction text was stale by a decision**: it said the work had moved from porting to building our own
   systems; Chase's 2026-10-13 rule is the other way round (faithful port first, our systems after). The body was
   edited by hand, as the README's own review line says to, then `judge.py confirm direction`.
4. **The counted numbers were not touched.** `progress.py` ran only with `--dry-run` (it wrote nothing to the README;
   the `progress.json` it still writes on a dry run was reverted with `git checkout`, and its cloud numbers, "Golem
   off, 0 queued", are wrong exactly as the prompt warned). The home PCs' commit hook refreshes the counts after the
   merge.
5. **The tool's own tests pass before and after**: `python3 -m unittest tools/tests/test_status_dashboard.py
   tools/tests/test_self_judging.py`, 34 tests, OK (1 skipped), on Python 3.13 in the cloud.

## 1. Row by row: old judgment, new judgment, evidence

"Old" is `tools/progress-state.json` at `73791eb` (every row confirmed 2026-10-13, except the sections). "New" is the
row as `judge.py` wrote it; the full detail text is in the file. Code paths are in `shattered-legacy-infrastructure`
at `7049a69`; CHANGELOG versions are that repo's `CHANGELOG.md` sections.

| Row | Old judgment | New judgment | Evidence |
|---|---|---|---|
| shard status | test shard only, image 2026.10.10; no live until the wipe; 2026-10-05 package; P65-P84 not deployed | test shard only; live retired and deleted 10-14 until the 1.0 world; main 2026.10.20.4 with Shadow Iron merging every 10 minutes, each branch built green first; the deployed build and the published package are not visible from the repos | CHANGELOG 2026.10.14.14 (live retired); `notes/passdown-overseer-2026-10-14.md` ("live deleted"); `notes/cc-P208-cont-shadow-iron-merger.md` headlines; `VERSION` at `7049a69` |
| direction | "the work moved from porting ServUO content to building Shattered Legacy's own systems" | faithful port first (Chase 2026-10-13), our own systems after; the port list's state; several Golems and Shadow Iron | `notes/port-list-2026-10-13.md` ("Direction, same day"); `notes/decisions-2026-10-14.md`; the README's port list block (3 of 16 in); CHANGELOG 2026.10.19.4, 2026.10.20.4 |
| gate: The shard runs and holds a world | **yes**; 1,133 tests at P82; image 2026.10.10 | **yes**; 1,430 tests, 1,426 passed at P208; live deleted; the running image not visible from the repos | `notes/cc-P208-cont-shadow-iron-merger.md` (test line); CHANGELOG 2026.10.14.14 |
| gate: The player package installs on a clean PC | **yes**; T-049, T-020, T-021; the 2026.10.13.0118 zip not uploaded | **yes**, same passes; three later package changes (our TazUO build, the scripts updater, the Achievements button) have no recorded clean-PC pass; **needs confirm** which package is published | `testing/play-tests.json` T-049, T-020, T-021; CHANGELOG 2026.10.15.9, 2026.10.18.4, 2026.10.18.7 |
| gate: A new character can train without hitting a wall | **no**; "ClusterFSkillGain still runs 3 attempts and a 5x gain amount" | **no**; the rate is 2 attempts and 1x since P191/P202/P204; hook G, the material ladders and Pet Training are in; the casting schools are still excluded; no in-client pass | `ClusterFSkillGain.cs:24, :39-40, :322-403`; `ClusterFMetalTiers.cs:70-81`; `ClusterFWoodTiers.cs:54-65`; `notes/cc-P191-cont-earned-skill-gain.md` section 6; CHANGELOG 2026.10.19.5, 2026.10.16.4 |
| gate: A new character's first hour | **no**; "8 decisions wait on Chase"; "nothing points a player to the League" | **no**; the 8 decisions were answered 10-14; the recruiter, the League station and the Guild Directory point at the League; stations still placeholders; the Vault has no map | `Tutorial/ClusterFTutorial.cs:1-15, :33`; `Tutorial/TutorialStations.cs:59-75`; `Tutorial/TutorialRecruiter.cs:25`; `notes/decisions-2026-10-14.md` Tutorial 1-10; CHANGELOG 2026.10.13.3, 2026.10.18.2 |
| gate: Levels and loops work end to end | **no**; CompleteLoop a hook | **no**, unchanged; parked after the port | `Tutorial/ClusterFLoops.cs:1-11`; `LootBoxes/ClusterFLootBoxes.cs:12, :19`; `notes/decisions-2026-10-14.md` Tutorial 7 |
| gate: What is built is seen in a client, not only compiled | **no**; "P65 to P84 are committed but not on the deployed image" | **no**; 418 play-test items: 362 open, 43 passed, 4 failed, 8 later, 1 blocked; last result 2026-10-18; **needs confirm** which build the test shard runs | `testing/play-tests.json` (counted 2026-10-20 with a 6-line Python read: `status` and `resultAt`) |
| gate: Somewhere to go | **no**; Despise verified, Shame unseen, Burrows checks open, extra facets research | **no**; the Burrows' rules and creatures are in, the map is not; Wrong and Covetous claimed by Bronze; four dungeons queued; 3 of 16 port systems in | `Regions/OldHavenBurrowsRegion.cs:1-11`; CHANGELOG 2026.10.18.2; prompts repo `claimed/Bronze/cc-P194-*`, `queue/cc-P195-*` to `cc-P198-*` (2026-10-20); README port list |
| gate: Things to fight | **no**; "No creature batch since CC6 batch 8 (2026-09-21)" | **no**; three batches since (P119, P129, P140), Creatures row 138 of 193; only Drelgor placed; spawn orphans unrecounted (needs the pinned tree) | CHANGELOG 2026.10.15.5, 2026.10.16.3, 2026.10.18; README port list; `tools/spawn-orphans.txt` (2026-09-21) |
| gate: Set mechanics actually fire | **no**; unchanged since 09-19 | **no**; still no caller for EpiphanyHelper or BeastialSetHelper outside their set files | `grep -rn 'EpiphanyHelper\.\|BeastialSetHelper\.' server/customizations` at `7049a69`: hits only in `Sets/Epiphany/VillainousEpiphany.cs:8-32` |
| gate: No live gap a player would call a bug | **no**; 60 rows, 34 say fixed | **no**; 65 rows, 41 mention fixed or built; highest D95; four moves still owed from 10-14 | `docs/bug-list.md` section 1 (`awk` between "## 1." and "## 1b", 65 rows starting `| **D`); `notes/passdown-overseer-2026-10-14.md` Record-keeping owed |
| gate: The fresh-world wipe is ready | **no**; D50 live timeout, the tutorial would greet old characters | **no**; live deleted so D50 is moot; accounts wiped at the tutorial update; Young ends at the first loop; D34, T-006, T-010, F-4 and P73 still scattered | `notes/passdown-overseer-2026-10-14.md`; `notes/decisions-2026-10-14.md` Tutorial 1; `Tutorial/ClusterFLoops.cs:5-7`; CHANGELOG 2026.10.12 |
| task DEPLOY | todo; "Deploy P65-P84"; image 2026.10.10, VERSION 2026.10.13.6 | todo; retitled "Deploy main to the test shard and run its play tests"; main 2026.10.20.4; **needs confirm** which build is on the test shard | `VERSION`; `testing/play-tests.json` (362 open) |
| task TUTORIAL | todo; 8 decisions for Chase | todo; decisions answered 10-14; stations still placeholders; Vault map missing | `notes/decisions-2026-10-14.md`; CHANGELOG 2026.10.13.3, 2026.10.18.2 |
| task WIPE | todo; gather D34, D50, T-006, T-010, F-4, the tutorial greeting | todo; live deleted; accounts wiped at the tutorial update; gather D34, T-006, T-010, F-4, P73 | as the wipe gate |
| task BUGS | todo; 60 rows, 34 say fixed | todo; 65 rows, 41 mention fixed or built; D94, D50, D89, D93 moves owed | `docs/bug-list.md`; `notes/passdown-overseer-2026-10-14.md` |
| task P83-DEPLOY | done 2026-10-13 | **retired** (done; the Websites tab can now move the page to Haven) | CHANGELOG 2026.10.14.13; `judge.py retire-task` also stamps `sections.tasks-reviewed` 2026-10-20 |
| task F-12 | todo; after the port | todo; after the port; the loop placeholders parked with it | `notes/decisions-2026-10-14.md` Tutorial 7; `Tutorial/ClusterFLoops.cs` |
| task F-37 | todo; after the port; nothing spends Renown | todo; after the port; F-47's requisitions (P150) now pay Renown and standing; nothing spends Renown yet | CHANGELOG 2026.10.20.3; `Requisitions/RequisitionSystem.cs:8-11`; `notes/cc-P75-league-rewards-rethink.md` A.1 |
| section portlist | 2026-10-13 | confirmed 2026-10-20: the list's rows still match the queue (bulk orders, pet training, treasure maps, monster stealing, creatures, consumables and crafting gaps landed by P118-P142; P193-P198 cover the rest) | the README's port list block; prompts repo `queue/`, `claimed/`, `merging/` on 2026-10-20 |
| sections foundation, corrections | 2026-10-13, 2026-09-19 | **not re-confirmed**: the setup defects and the patch risk register were not re-read for this prompt; their dates stand | n/a |

Counts: 21 rows judged (1 status, 1 direction, 11 gates, 7 tasks, 1 section); 3 marked needs-confirm; 1 task retired;
2 sections left as they were.

## 2. What the dry run showed

`SL_SHARD=<code clone> python3 tools/progress.py --dry-run` rendered the block with "Judgment reviewed 2026-10-20",
the four review lines (the three confirmations above plus the standing "play tests not sorted" line, which is derived
and not this prompt's) and every gate's new text. Its counted line read "Shard version 2026.10.20.5. Golem off, 0
queued", both wrong here: the version because the local clone sat on P217's branch, the Golem and queue because the
cloud has no `D:\UO\golem`. That is the wrong-numbers case the prompt forbids writing, and nothing was written: the
README is byte-identical to `73791eb`, and `tools/progress.json` was restored.

## 3. What I could not check from GitHub alone

- **Which image the test shard runs**, and so whether any post-10-13 work has been in a client. Hence the two
  needs-confirm gates and the DEPLOY task.
- **Which player package is published** on `get.shatteredlegacyuo.com`. A fetch of the download site would say; the
  cloud's network policy was not tried for it.
- **The spawn orphans** (`tools/spawn_orphans.py` needs `D:\UO\ModernUO-pinned`), so the "Things to fight" gate keeps
  the 2026-09-21 count with a note that it is stale.
- **ServUO comparisons**: none were needed for these rows, so the public pub57 repository was not consulted.
- **The Haven mirror of the play tests**: `testing/play-tests.json` in the repo is what the last commit carried; results
  marked on Haven since then would not be in it.

## 4. Working as a cloud Golem, this prompt

Docs-only prompts over a JSON file and a Python tool are a good fit: `judge.py` and its tests ran unchanged on the
cloud's Python 3.13, and every judgment's evidence was in the repos. Two things to know for the next status prompt:
`progress.py --dry-run` still writes `tools/progress.json` (worth a one-line fix so a dry run is a dry run), and the
claim and status steps go through the GitHub API tool, as in P217 and P218, because `git push` to the prompts repo's
`main` is refused here.

P220 DONE
