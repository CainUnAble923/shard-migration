# P525: new player tutorial guide draft

Written October 24, 2026 by the Golem's Codex lane.

## Deliverable

Added [the player guide draft](wiki-drafts/new-player-tutorial.md) in plain American English, with no em dashes. It covers starting, skipping and remedial training, every core lesson in its current order, the optional wings, graduation, the pet choice and reopening it, and dead pet recovery. P481's secluded start area and related proposals are explicitly planned.

Only this note and the requested guide were added. No code, configuration, map, existing guide, or docs/ file was changed. No service was contacted or deployed. No commits or branch changes were made.

## Evidence checked

Paths below are relative to the ShatteredLegacy work copy. The source was read, not inferred from station names or older guide drafts.

| Player claim | Source |
|---|---|
| Tutorial requires the test-world setting; account entry and login resumption | `server/customizations/Tutorial/ClusterFTutorial.cs:44`, `:69`, `:96` |
| Core order and station membership | `server/customizations/Tutorial/TutorialStations.cs`, `All` and `Core` |
| Exact actions, hints, practice supplies, replacement, logout behavior | `server/customizations/Tutorial/TutorialCoreTrials.cs`, `Hint`, `Resupply`, `Start`, `Tick`, `Cancel`, and `TutorialTrialGump` |
| Core prop locations, real death confirmation, Sera's ghost interaction, tutorial moongate | `server/customizations/Tutorial/TutorialCorePlacement.cs`, spot declarations, `TutorialDeathGump`, `TutorialHealer`, `TutorialResurrectionGump`, and `TutorialTravelGate` |
| Core-only menu until done; remedial wings; return to Rook to graduate | `server/customizations/Tutorial/TutorialGumps.cs:39`, `:195` |
| Skip twice, current default waiver, remedial reset and rewards | `server/customizations/Tutorial/TutorialGumps.cs:228`; `ClusterFTutorial.cs:39`, `:179`, `:211`, `:279` |
| Combat and magic actions, yard, skill loans and return rules | `server/customizations/Tutorial/TutorialWingTrials.cs:59`, `:120`, `:150`, `:447`, plus its trial page |
| Gathering, nine crafts and products, goat, bard, thief and four walking tours | `server/customizations/Tutorial/TutorialTradeTrials.cs:43`, `:76`, `:530`; its `Trades` rows were read individually |
| Farmhand's separate route and graduation pet exclusion | `server/customizations/Tutorial/TutorialFarm.cs`, `Talk`, `ChoosePet`, pest and healing hooks; `ClusterFTutorial.cs:313` |
| Graduation's first loop changes no skills, stats, level or XP and leaves Young running | `server/customizations/Tutorial/ClusterFLoops.cs`, `Graduate`, `CompleteLoop`, and empty `ResetLevelAndSkillsForF12` |
| Graduation box, elixir, pet pending state, four choices and follower-slot refusal | `server/customizations/Tutorial/ClusterFTutorial.cs:262`, `:279`, `:313`; `TutorialGumps.cs:351` |
| Bonded animal, one slot, color pick recovery | `server/customizations/Mobiles/Evo/EvoPet.cs`, constructor, `GivePet`, `OnDoubleClick` |
| Vet location and fee, Young exemption, corpse wait and skill loss | `server/customizations/Tutorial/TutorialPetCare.cs:43`, `:136`; `TutorialCorePlacement.cs`, `Seed` |
| Elixir use, backpack requirement, two-tile distance, alive user and consumed item | `server/customizations/Items/Consumables/ElixirOfRebirth.cs`, `OnDoubleClick` and `TryResurrect` |
| Animal Trainer sales, 500 gold | `server/patches/AnimalTrainer-elixir-of-rebirth.patch`; `server/customizations/Tutorial/TutorialPetCare.cs:189` |
| Haven exit restriction already exists separately from P481's proposed new island | `server/customizations/Tutorial/TutorialIslandGate.cs`, `NeedsGraduation`, `CanMove` |

Historical notes read: P289, P475, P480, P290, and P291, with the current code taking precedence. P481's queued prompt was read at `D:\UO\cc-prompts\queue\cc-P481-new-player-start-area-design.md`. It explicitly calls for design only, no code or map changes, with the build to follow a separate choice. No P481 completion note exists in this work copy. The guide does not present the character creation choice, new facet, private visibility, or staged scene as available.

The existing companions guide was read for related context and linked for evolution details. Its earlier tutorial and pet recovery descriptions were not used as evidence over P480's current implementation.

## Validation and limits

No lane tests were requested. No tests or new gates were added, so no red/green cycle applies. No server build or client playthrough was run for this prose-only change. Claims were checked against the canonical source and prior task evidence. Running shard deployment, current saved placements and client behavior remain unverified by this task. The guide identifies its test-world scope rather than claiming a live rollout.

Ran `tools/progress.py --dry-run` with `SL_SHARD` and `SL_MIGRATE` pointing to these work copies: exit 0. Its summary reports shard version 2026.10.24, with review items still pending. This guide does not certify those project-wide status claims or use its filename-based content counts.

The final diff caught an existing tool defect: `progress.py` writes `tools/progress.json` inside `build()` before `main()` checks `--dry-run`. Its claimed print-only mode changed the timestamp and queue snapshot. That file was clean at entry; restored its exact HEAD bytes after reading the diff, keeping this task within its two requested Markdown files. This is our reporting tool's defect, confirmed by its source and the resulting diff, and was not repaired in this docs-only task.

Reviewed the prose against the source, including the distinction between the existing Haven exit restriction and P481's planned new start island. All relative links in both added files resolve, neither contains an em dash, and both are far below 5 MB. Whitespace review passed. Final status shows a clean code work copy and only the two requested new notes files in the docs work copy. No work remains for P525.

P525 DONE
