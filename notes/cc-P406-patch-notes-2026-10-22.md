# P406: player patch notes for package 2026.10.22.0855

## In plain words

- Wrote `notes/patch-notes-2026-10-22.md`, a player-facing draft with New, Changed, Fixed, Unsure, and Sources sections.
- Kept additions that still need world setup or a player source marked "(coming once placed)". Kept secrets, staff commands, exploits, tests, and Golem tooling out of the player change lists.
- Flagged the missing starting tag, unverified live availability, the known stump-height problem, empty music assignments, and unfinished player access rather than resolving them.

## Scope and release boundary

Read both work-copy AGENTS.md files, migration `docs/direction-decision.md` and `docs/tasks.md`, code `CHANGELOG.md` and `VERSION`, and main's first-parent merge subjects. Both work copies began clean. Main ends at the requested `1ecd9f3`; VERSION is `2026.10.21.24`, distinct from the package timestamp.

No tags exist in the work-copy code repository or the read-only main desk at `D:/ShatteredLegacy`. Neither repository contains a tracked reference to `2026.10.21.0825`. The local release records in `D:/ShatteredLegacy/player-package/dist/` confirm both package stamps but contain no source commit. Consequently the exact tagged baseline is unverified and remains under Unsure.

Used `5d29bfa..1ecd9f3` as the explicitly provisional comparison: `5d29bfa` is main's latest first-parent merge before the older package's 08:25 timestamp. Read P352's notes as boundary evidence; its fog client patch and build already precede that package, whose release record explicitly advertises early fog. P357 only adds changelog text, so fog is not called new. Earlier Appraisal, con colors, satchel icons, climbing boots, New Haven community art, Rootdeep's original opening, and Underworld work precede the provisional baseline and are excluded.

No remote fetch, website access, Haven connection, deployment, image build, account operation, commit, merge, push, or branch switch was performed. No files under docs/ or server/uo/ were edited or used as source.

## Merge and note inventory

The draft's Sources section links every gameplay source and relevant wiki draft. The following inventories all first-parent merges in the provisional interval, including work deliberately omitted from player changes. Notes listed here are under `notes/` in shard-migration.

| Main merge | Prompt notes read | Treatment |
|---|---|---|
| `62c675d` | `cc-P357-cont-fog-of-war-client-half.md` | Changelog only; fog already in prior package record. Also read `cc-P352-cont-fog-of-war-client-half.md`. |
| `53c7829` | `cc-P271-cont-fixup-port-exodus-encounter.md`, `cc-P195-port-exodus-encounter.md` | Exodus, pending placement; crafting uncertainty retained. |
| `b92e08c` | `cc-P355-cont-fixup-accessory-slots.md`, `cc-P262-accessory-slots.md` | Accessories, no secret triggers; extra rings not opened. |
| `98b1d0d` | `cc-P353-cont-golem-questions-install-and-round.md`, `cc-P216-golem-questions-in-console.md` | Omit Golem tooling. |
| `1c39977` | `cc-P285-cont-fixup-levelable-gear-build.md`, `cc-P261-levelable-gear-build.md` | Gear engine qualified by missing Seal source. |
| `9b9bea3` | `cc-P241-achievement-category-icons.md` | Achievement headings and icons. |
| `48191cd` | `cc-P243-league-hall-decor-rewards.md` | Player house decor, distinct from unplaced guild halls. |
| `188cfff` | `cc-P358-cont-fixup-playtest-bot-checks-second.md`, `cc-P224-playtest-bot-checks-second.md` | Omit testing infrastructure. |
| `d62d2a4` | `cc-P157-plain-english-emails.md` | Omit Golem tooling. |
| `e7e5dbd` | `cc-P366-cont-fixup-cont-loot-box-flying-loot.md` | Flying-loot animation. |
| `5fbdee4` | `cc-P367-music-room-console-page.md` | Omit staff music-selection interface. |
| `a67da42` | `cc-P219-tazuo-script-test-harness.md` | Omit test harness. |
| `460f0e2` | `cc-P361-cont-fixup-noted-by-the-system-achievements.md`, `cc-P263-noted-by-the-system-achievements.md` | Generic secret-achievement line, crafted-gear rule, commission wait. |
| `0076ce4` | `cc-P369-cont-fixup-companions-b1-base-and-record.md` | Groundwork only, no playable hiring claim. No standalone P264 note exists in this work copy. |
| `59fb338` | `cc-P275-deployable-traps-build.md` | Craftable traps and pending Rootdeep placement. |
| `6647ef9` | `cc-P356-cont-fixup-golem-questions-in-console.md` | Omit Golem tooling. |
| `484cf7e` | `cc-P276-tutorial-farm-build.md` | Farm, map change, and pet offer qualified by placement. |
| `94eabb0` | `cc-P265-guild-hall-decor-packs.md` | Pending hall decor and startup fix. |
| `47b3eae` | `cc-P280-league-register-build.md` | Register, rank actions, consolidation, backpack limits, repairs. |
| `02c46e8` | `cc-P371-graduation-is-the-first-loop.md` | First recorded loop, travel gate, Young retention; no future leveling claim. |
| `7b11ab4` | `cc-P266-new-haven-winter-decor.md` | Future automatic winter window, placeholder gifts qualified. |
| `2d9fea4` | `cc-P364-league-bestiary-batch-2.md` | Monsters, parts, first-kill entries, pending placement; no job-board claim. |
| `222f0b8` | `cc-P368-added-music-areas-monsters-bosses.md` | Empty track assignments under Unsure; no soundtrack promise. |
| `b240bb4` | `cc-P354-cont-fixup-port-eodon-remainder.md`, `cc-P198-port-eodon-remainder.md` | Eodon gate, population, and vines pending placement. No unspawned creature promises. |
| `1ecd9f3` | `cc-P380-cont-fixup-chopped-tree-stumps.md`, `cc-P359-chopped-tree-stumps.md` | Temporary exhausted-grove marker; known height issue under Unsure. |

## Source checks and editorial choices

- Checked canonical code alongside notes: `LeagueRegister/LeagueRegisterSettings.cs` for issue/action ranks, `Accessories/ClusterFAccessories.cs` for bracelet and locked ring defaults, `Tutorial/ClusterFLoops.cs` for saved loops and the empty reset hook, and `Tutorial/TutorialFarm.cs` for live-placement restrictions.
- Checked `ClusterFStoreBought.cs` and commission call sites for the crafted-gear rule and small-request wait. Described the new requirement without discussing the exploit it closes.
- Checked `Items/Traps/Deployable/DeployableTraps.cs` and `ClusterFRootdeepSeeder.cs` for default target/presence rules and pending floor traps. Avoided the stale wiki instruction to start by targeting a kit with Remove Trap; no step-by-step setting instructions are included.
- Checked `ClusterFLeagueBestiary.cs` for placement and named mini-bosses. Did not use the prompt's approximate creature count or imply that the League job board is built.
- Checked `Music/ShardMusicTracks.cs` and `Music/ShardMusicTable.cs`: both collections are empty. No custom soundtrack is claimed.
- Checked `VirtualCheckActivatorFirst.cs` for the startup fix and `ClusterFLumberStumps.cs` for marker creation/refill removal. P380's confirmed but unfixed map-tree height problem remains explicitly unresolved; no claim that the tree itself is replaced.
- Wiki drafts read: `new-haven-start.md`, `levels-loops-and-scrolls.md`, `league.md`, `crafting-changes.md`, `dungeons.md`, `thieves-den.md`, `achievements-and-loot-boxes.md`, `companions-and-evo-pets.md`; pages `uo/systems/league_register.txt`, `league_shop.txt`, `accessories.txt`, `uo/professions/traps.txt`, and `uo/drafts/levelable_gear.txt`; plus `cross-check-2026-10-22.md`. These are secondary context. Their availability and future-system claims were not promoted to facts.
- No claim of new player levels, XP resets, extra ring access, companion hiring, approved music tracks, selected Seal acquisition, fixed stump height, live spawn placement, or exact holiday gifts.

## Validation

Docs-only task; lane tests are none. No tests or gates were added, so no red-first test cycle applies.

- One-time document review passed: required section order, no em dashes, no trailing whitespace, all relative source links resolve, no staff commands in the draft, both files below 5 MB, and every main merge in the provisional interval appears in the inventory above.
- `git diff --check` in both work copies and `git diff --no-index --check` against each new file reported no whitespace errors.
- Windows PowerShell reports version 5.1.26100.9444. No PowerShell 7 scripts or tests ran.
- Ran `tools/progress.py --dry-run` with `SL_SHARD` and `SL_MIGRATE` pointing to these work copies: exit 0, shard version `2026.10.21.24`. It reports existing project review items, including unconfirmed clean-PC installation/client checks, test-shard deployment state, and unassigned play-test work. These are outside P406.
- Found an existing tool defect: `--dry-run` still writes `tools/progress.json`. `build()` writes it at `tools/progress.py:722`, before `main()` checks the flag at line 737. The final status check caught the changed timestamp and newly queued P407 entry. Since that file was clean before this run, restored it byte-for-byte from HEAD and verified equality. No generated changes remain. This is our tooling to fix in a separate task, not a player patch-note item.
- Final scope: only `notes/patch-notes-2026-10-22.md` and this work note are new. Code repository unchanged; no docs/ changes. Release baseline and live availability remain explicitly unverified.
- Checked the stop-request path between research, drafting, and validation steps; it was absent.

P406 DONE
