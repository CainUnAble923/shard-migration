# P658: player patch notes for the next test release

Written October 26, 2026. Documentation only.

## Result and boundary

Wrote [the player draft](wiki-drafts/patch-notes-next-test-release.md), grouped by tutorial, skills, mounts, guilds and crafting, fishing, fixes, UI, and early test features. It describes merged behavior pending the next test release, not a deployment. Test-only tutorial content and the seven early experiments are labeled explicitly. Unfinished access routes and material known limits stay visible.

Read AGENTS.md in both work copies first, then the direction decision and task list. No nested AGENTS.md applies to either destination. Both work copies began clean. No skill was needed for these explicitly requested Markdown files.

The actual local release archive is `D:/ShatteredLegacy/player-package/dist/ShatteredLegacy-2026.10.23.1001.zip`. Opened it read-only without extraction. Its `app/VERSION.txt` says:

```text
Shattered Legacy player package 2026.10.23.1001
TazUO 3212623f + 4 patches
built from ShatteredLegacy d58c75e
```

Its `app/tazuo/sl-build.txt` lists client patches 0001 through 0004. `git show d58c75e:VERSION` is `2026.10.23.3`. Used that recorded source commit as the lower boundary, rather than comparing the package's time-based suffix numerically with server changelog suffixes. The sidecar identifies the same package version; this task did not recompute its archive hash or establish what server image ran alongside it.

Upper boundary: code `e4c2dd9f987534cd1775f7471cc2c0d6e3a359d0`, VERSION `2026.10.26.8`; notes `ab307974906efc483be98d863873282fecdc86d2`. Read CHANGELOG.md from `2026.10.23.4` through `2026.10.26.8`, and enumerated `git log --first-parent d58c75e..HEAD`. The changelog contains no literal build-note links in that interval. Matched entries to their implementation notes using merge history and read the related reviews where they qualify availability. Earlier patch-note drafts are context, not the release boundary.

## Changelog coverage and build sources

Links below are relative to this notes directory. Version labels are the current merged changelog headings; several original build notes have pre-integration version numbers that were later renumbered.

| Changelog entry | Build sources | Treatment in player draft |
| --- | --- | --- |
| 2026.10.23.4 | [P480](cc-P480-tutorial-first-play-fixes.md) | Test tutorial presentation, pet choice and care; general elixir vendor additions. |
| 2026.10.23.5 | [P290](cc-P290-tutorial-wing-trials-combat-magic.md) | Test tutorial combat, healing and magic lessons. |
| 2026.10.23.6 | [P291](cc-P291-tutorial-wing-trials-trades.md) | Test tutorial trades, animal, bard, thief and walking lessons. |
| 2026.10.23.8 | [P362](cc-P362-ui-skins-player-options.md) | Personal container and scroll appearance choices; updated client required. |
| 2026.10.23.9 | [P365](cc-P365-reward-mounts-and-evo-stages.md), [P521 review](cc-P521-review-reward-mounts-evo-stages.md) | Mount routes, new evo lines and package requirement; no automatic reward for prior achievement earners. |
| 2026.10.24 | P370 merge `f2853e8` | Omitted Golem operation, retries, notifications and prompt queue management. |
| 2026.10.24.1 | P373 merge `70df7c5` | Omitted Golem operation and console routing. |
| 2026.10.24.2 | [P411](cc-P411-launcher-always-starts.md), [review](cc-P411-launcher-always-starts-codex-review.md) | Launcher progress, fallback and test target, with later P611 fixes incorporated. |
| 2026.10.24.3 | [P412](cc-P412-chopped-tree-visuals.md), [review](cc-P412-chopped-tree-visuals-codex-review.md) | Stump placement, client tree hiding and polearm message; floating-leaf limit retained. |
| 2026.10.24.4 | [P413](cc-P413-rootdeep-anthill-entrance.md) | Wider Rootdeep entrance and safe exit, with map and setup dependency. |
| 2026.10.24.6 | [P414](cc-P414-retire-civic-waste-bundles.md) | Civic Contract point counting and old bundle redemption. |
| 2026.10.24.7 | [P415](cc-P415-trash-bag-corpse-claim.md) | Corpse clearing, destruction warning and loot protection, updated with P611 safeguards. |
| 2026.10.24.8 | [P416](cc-P416-stone-mining-gate.md), [P551 guide evidence](cc-P551-guide-mining.md) | Stone learning, ore quotas, grandfathered contracts and voucher shortfall payment. |
| 2026.10.24.9 | [P427](cc-P427-fixes-from-crystal-p379.md) | Pet XP exclusion, crafted-only deeds and nonspecific hidden-achievement correction. |
| 2026.10.24.10 | [P451](cc-P451-league-register-fixups.md) | Register purchases, repair scope, Field Satchel rules and nested order turn-in. |
| 2026.10.24.11 | [P453](cc-P453-tutorial-fixups.md) | One tutorial pet, saved pending choice, trainee ownership, bounded bandages and real healing; later P613 recovery included. |
| 2026.10.24.12 | [P454](cc-P454-commission-reroll-cooldown.md) | Shared commission abandonment wait; hidden achievement details omitted. |
| 2026.10.24.14 | [P455](cc-P455-death-hooks.md) | Boss loot boxes and bestiary credit; also included its merged Self Repair and Butcher's Eye fixes missing from the short changelog. |
| 2026.10.24.15 | [P457](cc-P457-noted-fixups-2.md) | Hidden achievement fixes without revealing conditions. |
| 2026.10.24.16 | [P458](cc-P458-eodon-fixups.md) | Vine refusal, wildlife proportions pending reseeding, and staff-supplied hatchling correction. |
| 2026.10.24.17 | [P459](cc-P459-hall-decor-seeder.md) | Omitted staff decor placement checks and tower doors; no newly opened player hall promised. |
| 2026.10.24.18 | [P168](cc-P168-hammer-t3-craft-order.md), [P372 fix-up](cc-P372-cont-fixup-hammer-t3-craft-order.md), [P587 hammer review](cc-P587-review-hammer-t3.md), [P460](cc-P460-artificers-text.md) | Hammer T3, Craft This Order, deed payouts and Artificers' wording; known hammer limits retained. |
| 2026.10.25 | [P269](cc-P269-high-seas-fishing-second-half.md), [P587 fishing fix-up](cc-P587-cont-fixup-high-seas-fishing-second-half.md), [P598 review](cc-P598-review-high-seas-second-half.md) | Fishing additions with normal reward access, cancellation, ingredient and encounter limits. |
| 2026.10.25.2 | [P374](cc-P374-cont-guild-hall-decor-proof.md) | Omitted unused guild decor animation as a player feature: the client fix is merged, but the changelog says no decor is placed. |
| 2026.10.25.3 | [P609](cc-P609-apply-tutorial-text.md) | Clearer tutorial hints and windows. |
| 2026.10.25.5 | [P610](cc-P610-fix-drafts-from-p533.md) | Companion, unravel, tutorial loan and payment, Exodus, Void Pool, Rootdeep, jewelry, puzzle and mini champion fixes. Omitted staff play-test decisions page. |
| 2026.10.25.6 | [P611](cc-P611-fix-drafts-from-p556.md) | Hunter's Satchel, protected corpses, exact clearing approval and launcher repairs. |
| 2026.10.25.7 | [P613](cc-P613-fix-drafts-from-p586.md) | Full-pack bandage retry and orphaned tutorial recovery. |
| 2026.10.25.8 | [P624](cc-P624-build-pumpkin-king.md) | Event cleanup, bounded pumpkins and no pet artifact credit. No new reward pool or purchase safeguards claimed. |
| 2026.10.25.10 | [P436](cc-P436-guild-league-gump-look.md) | Stone and bronze menus with updated client; no change claimed for other clients. |
| 2026.10.25.11 | [P625](cc-P625-build-tracking-ping.md) | Tracking Ping, skill thresholds, costs and current limitations. |
| 2026.10.25.13 | [P626](cc-P626-build-social-skill.md) | Persuasion rename, charity and courier training. No new skill points or courier gold promised. |
| 2026.10.25.14 | [P627](cc-P627-build-item-identification.md), [P628](cc-P628-build-guard-patrols-pilot.md), [P635 fix-up](cc-P635-cont-fixup-build-guard-patrols-pilot.md) | Staff-enabled test identification and observation-only Cove guard pilot. |
| 2026.10.26 | [P629](cc-P629-build-league-warrants.md) | Test warrant directions, not playable investigations or a shop. |
| 2026.10.26.3 | [P630](cc-P630-build-echo-summon.md) | Staff-run test Echo, not an obtainable player reward. |
| 2026.10.26.4 | [P631](cc-P631-build-townsfolk-rest.md) | Staff-enabled and placed conversations; no inn rest. |
| 2026.10.26.5 | [P633](cc-P633-build-procs-milestone.md) | Test weapon milestone, including pending player-level and imbuing work. |
| 2026.10.26.7 | [P634](cc-P634-build-town-houses.md) | Free staff-assigned test leases; no rent, sublets, player leasing or belongings packing. |
| 2026.10.26.8 | [P647](cc-P647-fix-weekend-review-findings.md), [review](cc-P647-fix-weekend-review-findings-codex-review.md) | Tracking and Persuasion repairs folded into their sections; experimental safeguards reflected without claiming all review defects are closed. |

Other first-parent code merges in the interval:

- P479, `8b0ccb8`: omitted staff Docker disk maintenance.
- P456, `f15bec8`: read [music saves and fallbacks](cc-P456-music-room-saves-and-fallbacks.md). Omitted staff Music Room saves and future custom-track fallback behavior. The note makes the player changes conditional on tracks shipping; no new soundtrack release is claimed.
- P632, `313d94d`: read [scoring butte stage one](cc-P632-build-scoring-buttes.md). This imports unused display art only. No scoring target, crafting recipe, deed, tutorial range, or player package release exists in this stage, so none is announced.

Read the previous [P513](cc-P513-patch-notes-for-10-23.md), [P541](cc-P541-patch-notes-10-24.md), [P578](cc-P578-patch-notes-2026-10-24b.md), [P594](cc-P594-patch-notes-2026-10-25.md), and [P604](cc-P604-patch-notes-2026-10-25b.md) evidence or drafts. These explain older known limits; P611 and P613 supersede the old corpse-clearing and tutorial-delivery warnings. P604 corrects the earlier fishing reward claims. Unpublished wiki guides, story chapters, designs, reviews and play-test plans are not announced as new gameplay or published pages.

## Source checks and unclear points

Source paths here are relative to the code work copy. These are source checks, not runtime tests.

- **Mount prices and access:** `server/customizations/Mobiles/Mounts/RewardMounts.cs:57`, `:59`, `:150`, and `:167` distinguish the 1,750 AP unlock from the Renown prices. `LeagueShop/LeagueShop.cs` confirms AP unlocks and Renown pays. The changelog's shorthand is ambiguous; the draft names both. Read the entire definition list, common placeholder stats, and the statuette's `OnDoubleClick` in `RewardMountStatuette.cs`; redemption consumes the statuette only after summoning succeeds. The earlier-achievement reward gap in P521 is still a limit, so there is no retroactive mount promise. Read `Mobiles/Evo/EvoPetData.cs` Horse and Lizard stages and their owner-loop/BondTrial prerequisites. `Tutorial/ClusterFTutorial.cs:265` excludes those lines from starter choices, and the other normal `EvoPet.GivePet` caller is the staff command in `Mobiles/Evo/EvoPetCommands.cs`. The draft labels them staff-supplied tests. Initial alternate foal and hatchling appearances also remain unavailable through the normal owner picker; the draft promises neither those choices nor a completed Bond Trial/loop path.
- **Fishing access:** read `server/customizations/Services/Expansions/High Seas/Quests/ProfessionFishQuest/ProfessionalFisherQuest.cs` order construction and response menus, `PlayerFishingEntry.cs:GetPointsAwarded`, and `FishQuestHelper.cs:GetTier` and its reward table in that same directory. Available orders are one line capped at 20 fish and at most three points each, below tier two's 100-point threshold. The tier-one table has no hooks or Oracle. Read the InProgress menu, which offers Close only. Therefore the draft does not tell players to destroy a crate to cancel or earn higher rewards by repeating jobs. The broader item-handling and delivery issues reported in P598 are not fixed by P647.
- **Hammer:** read `SmithGuildmasterGump.cs` upgrade routing and the P168/P372/P587 evidence. P587's last-charge, charge-regeneration, whole-small-deed and stale-tooltip issues are not repaired by later scoped fix-ups. The draft includes the partial-deed warning, avoids a regeneration timing promise, and asks players to reopen traded deeds for a current quote.
- **Test gating:** `Tutorial/ClusterFTutorial.cs:54` requires `testCenter.enable`. `ClusterFItemKnowledge.cs:165` and `LevelGear/LevelGearProcs.cs:47` also require the test-shard predicate. The seven early features follow the availability labels in the changelog and build notes. **Do not generalize the changelog's config-gate claim to every feature:** `LeagueEchoes/LeagueEchoSettings.cs:30` still reads its enable config without a test-shard check. `LeagueEchoSystem.cs` restricts its staff command instead, as P647's Limits section admits. No normal player Tome or Registrar path exists. The player draft calls this a staff-run test and does not claim a universal config safeguard.
- **Guard pilot:** P647's review still reports a medium defect where separate owner crimes in the same server frame can be suppressed as pet forwarding. The draft says the recorder is experimental and guard behavior is unchanged; it does not advertise complete crime recording or physical patrols.
- **Placement and client requirements:** fish mongers, the widened Rootdeep entrance, Eodon spawn proportions and townsfolk need setup or reseeding. The guild frame needs the server and updated client art together. New mounts need their animation package. No setup or release publication was verified. The draft's opening and relevant bullets preserve these dependencies.
- **No deployment inference:** P647's casual reference to live player fixes is not proof of a deployed server image. This task inspected local sources and one local release archive only. Shared test-shard state, live configuration, published download contents, current wiki publication and real client appearance remain unverified.
- **No spoilers:** hidden achievement changes stay nonspecific, even where implementation notes explain their conditions. The baseline already contains the October 23 wiki catch-up, so it is not announced a second time.

## Validation and limits

Documentation-only task; lane tests are none. No tests or gates were added, so a red-first test cycle does not apply. Historical build/test reports above belong to their original tasks and were not rerun or claimed as P658 verification. No new runtime, client rendering, or gameplay validation was performed.

- Ran the required `tools/progress.py --dry-run` with `SL_SHARD` and `SL_MIGRATE` pointing at these work copies: exit 0, version `2026.10.26.8`. Its unrelated project counts are not player-release evidence and are not repeated here. The script writes `tools/progress.json` despite dry-run; preserved its original bytes, restored them afterward, and verified byte equality. No generated reporting change remains.
- Compared all 39 real changelog headings above the baseline with the coverage table after stripping the changelog's HTML example comment: 39 table rows, no uncovered or extra versions. The table is the full version list beside this count. Checked the first-parent merge inventory for additional work without a player changelog entry, including P456 and P632.
- Local Markdown links resolve. Both new files contain no em dashes or trailing whitespace and are below 5 MB. Read through the player draft for short American English wording, pending-release language, unavailable features, and hidden-achievement spoilers.
- `git diff --check` passed in both work copies. New-file whitespace checks with `git diff --no-index --check -- NUL <file>` produced no diagnostics; exit 1 means the new files differ from NUL.
- Shell reports Windows PowerShell `5.1.26100.9711`. No PowerShell 7 script or test ran.
- Final scope is only the two requested Markdown files under `notes/`. The code work copy remains clean. No code, CHANGELOG.md, VERSION, docs/ file, service, save, account, or installed tool was changed. No build, deployment, Haven connection, commit, merge, push, or branch switch occurred.
- Checked the stop-request file between research, drafting, and validation steps; it was absent. No work remains for P658.

P658 DONE
