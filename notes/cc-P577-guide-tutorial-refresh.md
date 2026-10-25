# P577: tutorial guide refresh

October 24, 2026. Refreshed the P525 tutorial draft for the merged P480, P290, P291, and P453 changes.

## Work completed

Read AGENTS.md in both work copies, the direction decision, and the task list. Read the existing P525 guide and work notes, P480, P290, P291, and P453 implementation notes, the P453 review notes, and P481's queued design prompt. Checked the relevant behavior in the canonical source.

Updated [the tutorial draft](wiki-drafts/new-player-tutorial.md) for the merged changes:

- Retained the P480 core order, bright practice props, replacement supplies, and pet recovery instructions. Added the pet picker's pictures and descriptions.
- Clarified P290 combat controls, spell targets, the Close Wounds distance, and the requirement to restore health in the bandage lesson.
- Clarified P291 craft identification actions, temporary skill loans, ordered tour stops, and restarting unfinished lessons.
- Added P453's recorded-character restrictions, one tutorial pet per account across remedial training, saved pending graduation choice, Farmhand route, default bandage allowance, actual healing requirement, and refusal of outsiders' attacks.
- Kept P481's secluded island and related proposals explicitly planned. Added P453 and this refresh note to the guide's sources.

## Source evidence

Paths are relative to the ShatteredLegacy work copy.

| Claim | Source |
|---|---|
| Test-world gate, tutorial ownership, remedial behavior | `server/customizations/Tutorial/ClusterFTutorial.cs:44`, `:60`, `:71`, `:223`; `server/customizations/Tutorial/TutorialGumps.cs:40` |
| Core order, hints, bright practice items, replacements | `server/customizations/Tutorial/TutorialStations.cs`, core rows; `server/customizations/Tutorial/TutorialCoreTrials.cs:48`, `:62`, `:75` |
| Optional wings open after core or during remedial training | `server/customizations/Tutorial/TutorialGumps.cs:43` |
| Combat and magic actions, targets, loans and cleanup | `server/customizations/Tutorial/TutorialWingTrials.cs:59`, `:150`, `:424`, `:447` |
| Trades, craft identification actions, goat lesson, ordered tours | `server/customizations/Tutorial/TutorialTradeTrials.cs:76`, `Trades` rows and tour stops |
| Farm pet claim, pest credit, bandage defaults and actual heal | `server/customizations/Tutorial/TutorialFarm.cs:74`, `:75`, `:222`, `:258`, `:282`, `:301`; `server/patches/Bandage-tutorial-real-heal.patch` |
| Outsiders' harmful actions refused | `server/patches/Notoriety-tutorial-creature-outsiders.patch`; `server/customizations/Tutorial/TutorialCreature.cs`, `Engages` |
| Pending pet choice, claim checks, graduation reward | `server/customizations/Tutorial/ClusterFTutorial.cs:245`, `:248`, `:271`, `:289`, `GraduationRewards` |
| Pet claim, pending choice and bandage count are saved | `server/customizations/ClusterFAccountData.cs:1280`, `:1283`, `:1286`, `:1309`, `:1334` |

P481 was checked at `D:/UO/cc-prompts/queue/cc-P481-new-player-start-area-design.md`. It requests design only, with implementation following a separate choice. No new island availability is claimed.

P573's review identifies remaining full-backpack bandage-delivery and deleted-trainee recovery gaps. This draft does not claim that bandage delivery succeeds with a full backpack or that another character can resume an orphaned active tutorial. No code fixes are in scope.

## Validation and limits

Reviewed the final prose against the canonical source, including the loan cleanup and ordered tour behavior. Relative links in both deliverables resolve, both files contain no em dashes, and both are below 5 MB. The guide uses plain American English. `git diff --check` passed after editing the guide. Both work copies were clean at entry; the code work copy remains clean. Only the requested guide and this task note have been edited.

No lane tests were requested. No tests or gates were added, so no red/green cycle applies. No build, client playthrough, live inspection, deployment, Haven connection, commit, or branch change was performed. Running placements and behavior remain unverified by this task.

Ran `python tools/progress.py --dry-run` with `SL_SHARD` and `SL_MIGRATE` pointing to these work copies. It exited 0 and recognized shard version `2026.10.24.15`. This guide does not certify the reporter's project-wide status claims or use its content counts. The reporter still writes `tools/progress.json` before returning in dry-run mode (`tools/progress.py:722`, `:732`, `:737`), so its pre-run bytes were preserved and restored in a finally block. Byte-for-byte restoration was verified. README and progress files are unchanged. The checks ran under Windows PowerShell 5.1.

## Pause and resumption

The Golem requested a budget pause after the draft-edit step. Its stop-file reason was: "the Golem has used 417% of the week (codexMaxPctPerWindow 400)". The draft and evidence were saved. The user then authorized resumption with the stop file removed; the remaining review and progress-report checks were completed.

Final whitespace, style, size, link, and status checks passed. The code work copy is clean, and the docs work copy contains only the requested guide edit and this note. No work remains for P577.

P577 DONE
