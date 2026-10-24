# P513: patch notes for October 23

## In plain words

- Wrote `notes/cc-P513-patch-notes-2026-10-23.md`, with short player lines grouped under Pets and Player guides.
- Included the new elixir vendor sources and described the wiki revisions as coming with its next update.
- Left out test-only tutorial lessons, tutorial fixes and rewards, guild hall placement, and staff tooling.

## Scope and sources

Read both work-copy AGENTS.md files, the direction decision and task list, P406's work notes and player draft, the code CHANGELOG.md and VERSION, and the October 23 first-parent merge log. Both work copies started clean. The code snapshot ends at `bd95351`, version `2026.10.23.6`. This covers October 23 merges present in that snapshot, using America/Chicago dates, rather than a player-package interval.

P406 supplied the plain-language draft and separate evidence-note pattern. This task's shorter format groups player lines by area; verification details stay here.

| October 23 main merge | Treatment |
| --- | --- |
| `e445668`, P281 | Omitted guild halls, which are test-only. |
| `72f410f`, P287 | Omitted Golem scheduling and idle checks. |
| `4c2af57`, P288 | Omitted staff console package-note autofill. It changes the staff workflow, not the player client. |
| `0f1871f`, P475/P289 | Omitted tutorial fixes and core trials, since live tutorial entry is disabled. |
| `d58c75e`, P478 | Included player guide revisions, explicitly pending the next wiki update. Omitted draft pages for unavailable systems. |
| `7c085f7`, P480 | Included animal trainer elixirs and Rangers' League member sales. Omitted tutorial presentation, graduation rewards, companion selection, and seeded vets. |
| `579ad58`, P290 | Omitted test-only combat and magic tutorial lessons. |
| `bd95351`, P291 | Omitted test-only trade and other tutorial lessons. |

Source checks in the canonical code tree:

- `server/customizations/Tutorial/ClusterFTutorial.cs:48`: tutorial enablement requires `testCenter.enable`. New lessons in CHANGELOG sections 2026.10.23.5 and .6 do not establish live availability.
- `server/customizations/Tutorial/TutorialCorePlacement.cs:68` and `TutorialFarm.cs:333`: placement restrictions. A new farm or town vet is not promised to players.
- `server/patches/AnimalTrainer-elixir-of-rebirth.patch`, applied by `docker/uo/apply-patches.sh:876`: trainers register the new vendor stock without a tutorial or test-world gate.
- `server/customizations/Tutorial/TutorialPetCare.cs:187`: vendor stock includes the elixir.
- `server/customizations/OutridersGuildmasterGump.cs:267` and `:365`: discounted member price and membership check for the purchase.
- `server/customizations/Items/Consumables/ElixirOfRebirth.cs`: existing resurrection behavior requires a dead bonded pet, its corpse gone, proximity, and an elixir in the user's backpack. The note announces new purchase sources, not a newly invented potion.
- `docker/wiki/content/pages/uo/guilds/`: checked the individual guild page filenames against the draft's names. `docker/wiki/README.md` says the seed is separate from the live wiki.
- [P478 work notes](cc-P478-wiki-catch-up-3.md) explicitly say nothing was published. Wiki additions therefore use future wording; draft-only tutorial, loops, companions, halls, Rootdeep, levelable gear, and red dragon pages are omitted.
- [P480 work notes](cc-P480-tutorial-first-play-fixes.md) confirm vendor additions are separate from tutorial changes and report no deployment.

## Limits and validation

Live deployment and publication were not verified. No Haven connection or remote request was made. The draft describes merged player changes, with the wiki publication dependency stated explicitly. It makes no claim that test-only systems have opened. October 22's Halloween encounter release is outside this day's merge boundary; only its new guide is included.

Docs-only task; lane tests are none. No tests or gates were added, so a red-first test cycle does not apply. No code, changelog, VERSION, or docs/ file was changed. No commit, merge, push, branch switch, deployment, build, or account operation was performed.

- One-time document review: short player lines grouped by area, plain American English, no em dashes, no staff commands, and no tutorial or other unavailable system announcements. Wiki changes are explicitly pending publication.
- `git diff --check` passed in both work copies. `git diff --no-index --check` found no whitespace errors in either new note.
- Both files are below 5 MB. Final scope is only these two new notes; the code work copy is unchanged.
- Windows PowerShell reports `5.1.26100.9711`. No PowerShell 7 script or test ran.
- Ran `tools/progress.py --dry-run` with `SL_SHARD` and `SL_MIGRATE` pointing to these work copies: exit 0. Its status text explicitly says the deployed shard build and published package cannot be determined from the repositories. Its older main-version text is not release evidence for this draft.
- As P406 already documented, the progress tool writes `tools/progress.json` even with `--dry-run`. Preserved its original bytes before the run and restored them afterward; byte equality and final git status confirmed no generated change remains.
- Checked the stop-request path between research, drafting, and validation steps; it was absent.

P513 DONE
