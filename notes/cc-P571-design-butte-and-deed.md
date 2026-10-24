# P571: the scoring archery butte and its deed

Design prepared October 24, 2026. No code changed. This is a build specification, not a claim that the scoring butte is installed or that its art has been tested in a client.

## The recommendation

Add a butte that shows the latest arrow or bolt hit, first as optional practice beside the New Haven tutorial yard, then as a craftable house addon. Keep ModernUO's firing, scoring, ammunition and skill checks. Use the reviewed Archaaz hit-display set described in P405, with new registered item IDs. Offer east and south deeds through Carpentry. Do not replace existing stock buttes or the existing Clean Up Britannia reward.

Chase already approved the feature and its two destinations. The remaining recommendations here, including the art selection, craft requirements and yard positions, are proposed defaults for his review. Implementation can be written from this specification after the art inputs and client proof are available. World placement and publication remain separate operator actions.

## Authority and evidence

Paths beginning `C/` refer to this code work copy, `D:/UO/golems/Verite-tower/ShatteredLegacy`. Paths beginning `N/` refer to the notes work copy, `D:/UO/golems/Verite-tower/shard-migration/notes`. `M/` means `D:/UO/ModernUO-pinned/Projects`. The code snapshot is `1020e36a42d31dde07612544ea2a6f9472911db8`, also this checkout's local main. The notes snapshot is `3e07963`. The Docker pin and pinned engine are `d4531cd94b739613155225c234900de9f47d2c88`.

The task's first-read filename, `notes/cc-P405-servuo-batch-1022-research.md`, does not exist. Its completed prompt explicitly names the actual deliverable, [cc-P405-servuo-batch-1022.md](cc-P405-servuo-batch-1022.md). I read that note, its [Codex review](cc-P405-servuo-batch-1022-research-codex-review.md), the completed prompt at `D:/UO/cc-prompts/completed/cc-P405-servuo-batch-1022-research.md`, and the overseer's answers at `D:/UO/overseer/decisions-2026-10-22.md:15-24`.

The recorded October 22 answer is: "after F-8/F-21 prove new item art; New Haven yard plus a craftable or reward deed." It does not select the art pack or settle craft versus reward. P405's original question is at line 1191. The completed prompt is the research assignment, not an additional answer from Chase.

Read both work copies' AGENTS.md, the direction decision, the governing-document list, task list and subsystem policy. The newer Golem rules control commits and the notes-only destination. No `docs/` file is edited. Third-party download contents were not opened, executed or extracted. Their reported behavior and asset inventory below come from P405, as this prompt directs. I also read the ordinary ServUO reference `D:/UO/ServUO-pub57/Scripts/Items/Addons/ArcheryButteAddon.cs`; it is not the third-party modification.

| Evidence read in source | Consequence for this design |
|---|---|
| `M/UOContent/Items/Addons/ArcheryButteAddon.cs:9`, `:34`, `:61`, `:93` | The stock component exists. `FacingEast`, `Gather` and `Fire` are nonvirtual. A hidden property or method in a subclass cannot change the inherited calls. |
| Same file, `:108-144`, `:185-270` | Alignment, distance, skill check, ring selection, split calculation and scores can stay in the engine. The valid distance is 5 or 6 tiles, not the loose "4 to 6" description in P405. |
| Same file, `:42-79`, `:273-293` | Ammo counters persist; score entries and last-use time do not. Gathering resets all shooters' scores. |
| `M/UOContent/Items/Addons/BaseAddonDeed.cs:42-118`; `BaseAddon.cs:84-123`, `:140-202` | Existing deed placement checks the backpack again at target time, requires house ownership and checks fit. Existing chopping requires the house owner and an addon registered to that house. |
| `C/server/customizations/Tutorial/TutorialWingTrials.cs:45-75`, `:145`, `:315-367`, `:412-461`, `:555-578` | The bow lesson lends a bow, 50 normal Arrow items and skill 30. It finishes through three hits on the learner's echo. Loans are tracked by item and returned on finish/cancel. |
| `C/server/customizations/Tutorial/TutorialCorePlacement.cs:16`, `:66-108` | Tutorial placement is explicit, test-world only and preflights before mutation. |
| `C/server/customizations/Services/CleanUpBritannia/CleanUpBritanniaRewards.cs:186` | A stock ArcheryButteDeed already costs 80,000 cleanup points. This feature must not silently replace that reward. |
| `M/UOContent/Engines/Craft/DefCarpentry.cs:528-541`; `Core/CraftSystem.cs:139-192`, `:303` | The Training group, mixed Carpentry/Tailoring recipes, string names and nonexceptional output are supported. |
| `C/server/customizations/Engines/Craft/CarpentryCraftRegistrations.cs:26-60` | An idempotent `EventSink.ServerStarted` registration can append the deeds without a DefCarpentry patch. |
| `C/server/customizations/ShatteredRunestone.cs:39-59`; `ClusterFCommunityArtSeeder.cs:24-77` | Server tiledata already has an additive art-record application route. |
| `C/player-package/payload/app/Build-UoOverrides.ps1:1-49`; `C/scripts/find-free-art.py:1-27` | The package supports PNG item overrides and patched copies of players' tiledata. Free-slot checks cover more than empty tiledata. This is existing code, not proof of this butte's delivery. |

P405's review identified the missing extension hooks. This design corrects its roughly 60-line subclass estimate. The work includes an engine hook patch, new saved types, matching server/client records, acquisition, placement and behavioral tests. It is a small feature with meaningful integration work, not an ID-swap-only port.

## What players see

The public prop is named "scoring archery butte." The empty target uses the ordinary east or south butte picture. Equip your own bow or crossbow, stand on its marked firing line, and double-click the butte. The projectile animation and score messages are the stock ones. The target changes to an arrow or bolt in the bullseye, inner, middle or outer ring. A miss uses the reviewed frame with the projectile in the frame of the target.

The picture represents the latest shot by anybody, including a miss. It does not accumulate arrows or show an individual player's history. A split uses that ammunition's ordinary hit picture for the selected ring; the stock message and score identify the split. Another player's shot can immediately replace the picture. A nearby sign says this plainly.

Walk within one tile and double-click to gather recoverable ammunition and clear the display. Ammo is shared, as on the stock butte: any nearby user can collect it. Collection also resets everybody's score on that butte. Misses and splits create no recoverable projectile. If a session contains only misses or splits, a close click still clears its picture and score without creating ammo. This close-click reset is a deliberate usability addition on the new type.

Suggested sign text:

> Equip your own bow or crossbow. Stand on the line, 5 or 6 tiles in front, and double-click the target. The picture shows the last shot. Walk up and double-click to gather shared ammunition and clear everyone's score. Finish your tutorial trial before practicing here.

This is optional practice. It adds no tutorial station, completion requirement, account reward, gold, item XP, pet XP, League credit or achievement. Keep the current three-hit echo lesson and its Throwing option. The butte does not teach Throwing or pay combat kill rewards. Players bring their own equipment and ammo for this optional activity.

## Numbers and rules

These firing and scoring values come from the pinned butte, not from new balance choices.

| Rule | Value |
|---|---|
| Delay between accepted shots | 2 seconds per butte, shared by all shooters. A rejected click does not consume ammo or advance the delay. Gathering does not clear this delay. |
| East-facing alignment | Shooter X greater than target X; shooter Y equal to target Y. |
| South-facing alignment | Shooter Y greater than target Y; shooter X equal to target X. |
| Firing distance | Exactly 5 or 6 tiles on the aligned axis. Distance 4 or less, 7 or more, the wrong side and an off-axis tile refuse. |
| Skill window | `CheckSkill(bow.Skill, -25.0, 25.0)`. Inherit the shard's normal skill-gain wrappers. Do not raise the ceiling or add a second gain roll. |
| Ammo cost | One item of the equipped ranged weapon's AmmoType, from the backpack, for each accepted shot, including a miss or split. |
| Recovery | One Arrow or Bolt added to the corresponding stored counter on an ordinary hit; none on a miss or split. The split does not subtract an existing stored projectile. |
| Split chance | Stored arrows plus bolts, before this shot, multiplied by 0.02, compared with a uniform random number. At 50 stored projectiles this is certain. Preserve the engine expression. |
| Gathering/reset distance | Within one tile, same map, reachable through line of sight. |
| Score | Per shooter on that butte until anybody gathers or the process restarts. No leaderboard or score rewards. |

Ring selection occurs after the skill check succeeds:

| Ring | Conditional chance | Ordinary score | Split score |
|---|---:|---:|---:|
| Bullseye | 10% | 50 | 100 |
| Inner | 15% | 10 | 20 |
| Middle | 25% | 5 | 15 |
| Outer | 50% | 2 | 5 |
| Miss, before ring selection | Skill check failure | 0 | Not applicable |

A miss still counts as a shot in the shooter's total/count message. These percentages are conditional on a successful skill check. They are not absolute hit chances. At effective skill 25 or higher the stock window is no challenge; it succeeds without training from that window (`M/UOContent/Skills/SkillCheck.cs:57-77`). The current shard's `ClusterFSkillGain.TryRow` has no Archery row extending this practice ceiling. The tutorial's lent skill 30 is another reason not to describe the butte as the main bow lesson.

The new component validates a living PlayerMobile, the same map and line of sight before player interaction. Failure leaves ammo, scores, cooldown and artwork untouched. Keep these checks local to the new component's `OnDoubleClick`; the engine patch must not change old buttes' access rules.

Before either firing or resetting, reject a player whose `TutorialWingTrials.Current(player)` is an unfinished trial. Say: "Finish or stop your tutorial trial and return its loans before using this butte." Do not cancel their trial automatically. Also reject use of the tutorial's marked loaner weapon or marked loaner ammo stacks if any remain after an interrupted cleanup. Use the established loaner-prefix constant, not a new copy of its text. A prefix is a supplemental check, not proof of ownership; the active-trial check is the main guard.

This guard closes a concrete interaction: the lesson creates normal Arrow items, while stock `Gather` constructs new normal Arrow/Bolt stacks. Allowing borrowed arrows into the new butte could turn temporary supplies into permanent ones. The public practice target must never mint replacement loaners, supply free arrows, or claim tutorial evidence. This design does not assert that every existing stock butte already prevents that interaction.

## Code shape and engine hooks

All paths below are proposed additions unless called out as existing. Recheck names and aliases in pinned ModernUO and canonical customizations before implementation.

Use `server/customizations/Items/Addons/ScoringArcheryButte.cs` for `ScoringArcheryButte : ArcheryButte`, its addon and east/south deed types. Use `server/customizations/Items/Addons/ScoringArcheryButteArt.cs` for the explicit artwork map and tiledata records. Use generated ModernUO serialization and version 0 for the new saved classes. Leave the old classes, aliases, saved fields and inheritance chains intact.

Add `server/patches/ArcheryButte-practice-display-hooks.patch` against pinned `Projects/UOContent/Items/Addons/ArcheryButteAddon.cs`. Make only these extension changes:

1. Make `FacingEast` virtual. Keep the stock getter and setter unchanged. The new component overrides it using saved orientation, rather than comparing ItemID with an empty target's ID.
2. Add a protected virtual, no-op `OnPracticeShotResolved(Mobile from, Type ammoType, int area, bool split)`. Area is -1 for a miss and 0, 1, 2 or 3 for the rings in stock order. Call it once after the miss has recorded and announced its score, immediately before that branch returns; call it once after the successful shot has updated ammo, score and messages. Never call it on validation failures. Pass the actual ammo type, not an invented projectile item.
3. Add a protected virtual, no-op `OnPracticeGathered(Mobile from)`. Call it after Gather has zeroed both counters and cleared the score dictionary. The derived implementation clears its display state.

`Fire` and `Gather` can remain nonvirtual. The derived component's normal path delegates to `base.OnDoubleClick`; only the empty-counter close-click reset calls the inherited Gather explicitly. The overridable facing property is reached by the existing Fire body. The shot hook receives the actual ring and split outcome from that same body. Do not call Fire twice to infer a result, copy it into a subclass, reroll a hit for the picture, inspect translated score messages, or subtract ammo again in the hook.

For normal Arrow or Bolt ammo the derived shot hook records the display state and sets ItemID through the mapping table. Preserve base handling of any other ranged ammo type, but leave its picture unchanged because this pack has no frame for it. Do not invent a recoverable arrow for an unsupported type. Retain the inherited BaseThrown dispatch and test it; the new pictures do not promise throwing support.

Alternatives considered before authorizing the patch:

| Alternative | Why it is not the recommendation |
|---|---|
| Hide FacingEast/Fire/Gather in a subclass | Existing calls bind to the nonvirtual engine members. The hit ring is local to Fire. This is P405's review finding. |
| Copy the full firing implementation into a new component | Duplicates ammo, gain, split and score behavior and can drift silently on a pin bump. The subsystem policy prefers a patch that fails loudly. |
| Replace all of ArcheryButteAddon.cs | Takes ownership of stock saves and all buttes for a visual addition. |
| Infer a result from counters or overhead messages after calling base | Counters cannot distinguish rings; misses and splits can leave counters unchanged; messages are not a stable extension API. |
| Continue with stock art only | A safe fallback while art proof is pending, but does not deliver Chase's selected hit-display feature. |

This is one targeted UOContent patch, not a Server core patch. The hook contract and both call sites must be listed in the implementation note's pinned-commit bump checklist for overseer promotion. Let `apply-patches.sh` discover and account for the patch normally; it must still fail on a rejected patch. No full-file replacement or migration is required.

## Saved state, facing and redeeding

The new component saves its orientation and a compact, explicitly numbered display enum: Empty, ArrowMiss, ArrowBullseye, ArrowInner, ArrowMiddle, ArrowOuter, BoltMiss, BoltBullseye, BoltInner, BoltMiddle, BoltOuter. This describes 11 logical states, each with east/south artwork. Empty uses stock art; the other 10 states use new art. Inherited ammo counters remain the sole source of recoverable ammo. Never count pixels or the display enum to calculate it.

The addon saves its orientation so its Deed property can return the corresponding `ScoringArcheryButteEastDeed` or `ScoringArcheryButteSouthDeed` even when base chopping has already deleted the components. `BaseAddon.OnChop` deletes before asking for Deed, so do not discover orientation by searching live components in that getter. Each concrete deed constructs the same addon with its fixed orientation and an empty display. Use stock deed graphic 0x14F0 and direct names "scoring archery butte deed (east)" and "scoring archery butte deed (south)". This needs no new cliloc or gump.

Creation initializes addon and component orientation together. If staff change FacingEast, update both values and redraw the current display. If a Flip attribute is provided, use `[Flippable]` with a parameterless `Flip()` that goes through this setter, never the inherited static two-ID list. The existing Flip handler reads attributes on the concrete type without inheritance (`M/UOContent/Items/Misc/FlippableAttribute.cs:34-84`). Player orientation choice is the deed, so a new player rotation menu is unnecessary.

After deserialization, validate enum/orientation, reconcile the addon/component orientation after their references are available, and derive ItemID from that state. Do not infer east from the displayed hit ID. Keep the last picture and recoverable ammo across a normal save/restart; let the inherited score table and cooldown reset, as on stock. An invalid display enum becomes Empty and must never create ammo. A hand-edited ItemID is corrected from state on load. Test entity load order, not just a constructor followed by property assertions.

Player placement uses BaseAddonDeed's existing backpack, target, fit, ownership and house registration path. An invalid or cancelled placement retains the deed and creates no persistent component. Do not patch house rules to make this feature work. A valid house may still be too small for a 5-tile firing lane; the deed description should warn players to leave room. That is not grounds to extend the firing range or allow public-land placement.

For the new addon only, refuse owner chopping while recoverable ammo remains and ask the owner to gather first. Check the same owner/house-addon eligibility before that message, then delegate to the normal chop path once empty. This avoids silently destroying stored ammo. It creates no refund or extra recovery. A successful redeed returns exactly one matching deed and resets picture and scores on the next placement. A second chop or a nonowner's chop grants nothing.

Public yard components use a separate owned addon subtype/tag with no player deed output and an OnChop refusal. It is still the same scoring component and rules. Do not let a player axe the public prop into a free house deed.

## The deed's acquisition

Recommend craftable, rather than a new reward currency. Add two rows to Carpentry's existing Training group 1044297, one for each deed. Put them in a dedicated additive `server/customizations/Engines/Craft/ScoringArcheryButteRecipes.cs`, registered once on ServerStarted. No quest recipe, theme pack, rare drop or vendor purchase is required.

| Proposed recipe value, each facing | Value and reason |
|---|---|
| Carpentry window | 68.4 to 93.4, matching the stock training dummy recipe |
| Tailoring window | 50.0 to 55.0, matching that same recipe |
| Wood | 55 boards or logs through `typeof(Log)` and the existing resource substitution |
| Cloth | 60 Cloth |
| Result | One ordinary, nonexceptional deed; no scoring or skill bonus from quality |
| Recipe scroll | None |
| Sale or redemption payout | None added |

Use AddCraft with literal item names, AddSkill, AddRes and ForceNonExceptional. Stock resource failure, tool use, material consumption and craft-gain behavior remain the craft system's job. Normal wood selection may color a deed/addon according to existing craft behavior; it must not affect scores, chance, ammo recovery or the full-color hit images. Keep the visible scoring component Hue 0 and do not share material hue onto it. The implementation must test this with ordinary and colored wood, including redeeding.

These are new custom recipe defaults, not an assertion that OSI or the third-party script has this craft recipe. Keep the current cleanup reward type and its 80,000-point price. The economy tradeoff is explicit: crafting would offer functionally equivalent target practice more cheaply than that reward, with better visual feedback. If Chase prefers reward-only, substitute new scoring deeds in a separately reviewed acquisition change; do not quietly convert existing reward items or allocate an unapproved League price.

## The New Haven yard

Use `server/customizations/Tutorial/TutorialScoringButtePlacement.cs`, with its own tagged public addon type. Add an Administrator command `[TutorialButtes status|place|clear [dryrun]]`, following the tutorial's test-world gate and the community-art seeder's ownership pattern. Nothing seeds on startup. Reuse existing staff command discovery; no new Shard Console window button is needed. If a later prompt adds one, it must also supply the P187 web twin.

Place two buttes, one per facing, with unobtrusive passable line markers and one sign. Concrete first candidates on Trammel:

| Owned key | Butte XY | Facing | Firing tiles XY |
|---|---|---|---|
| `yard-east` | (3411, 2624) | East | (3416, 2624), (3417, 2624) |
| `yard-south` | (3420, 2618) | South | (3420, 2623), (3420, 2624) |

These coordinates are proposals, not verified clear tiles. The current trial yard is (3411, 2617), its echo is two tiles east and its patient two tiles west. The candidates separate buttes and lanes from those known anchors, but map geometry, farm boundaries, paths, spawners and other props must be checked before committing a placement table. Do not reuse the old Haven stock butte coordinates quoted in P405 as if they describe the current yard.

The placement prompt computes Z from the loaded patched map and writes the verified XYZ values into its owned layout. Preflight both targets, both complete shooting corridors, gather approaches, line markers and the sign as one operation. Require reachable standable firing/gather tiles, reasonable matching elevations, line of sight, no doors/stairs/path obstruction, and no tutorial props, trial spawn locations or existing occupied rows. Allow the proper blocking footprint at the target. A failure refuses the entire placement with a named coordinate. Never force a target into terrain or move unrelated objects. If a candidate is unsuitable, inspect the map, choose and document a corrected table before retrying.

`status` reports missing, moved and duplicate owned keys. `place` is idempotent by saved tag and concrete public type, not by art ID or display name. A moved or duplicate owned target is reported for staff rather than silently copied or moved. Dry run mutates nothing. `clear` removes only the tagged public props, markers and sign, including their components, never a player's house addon or a stock same-art target. If public targets contain recoverable ammo, clear refuses until staff have gathered it. Refusal is all-or-nothing for the owned layout.

Keep the public props out of player houses and without a registered house addon entry. Their public subclass refuses player redeeding regardless. Tutorial hints may mention the optional range after returning the loans, but butte clicks never call `TutorialWingTrials.Hit` or another completion/reward method. Regression tests keep the three echo hits as the bow lesson's completion path.

## Art and client work

P26 and P237 established the general PNG/records route in code. P571 has not demonstrated this particular asset set through an installed player's updater. Treat Chase's prerequisite as two deliverables: valid artwork and matching collision records in the package, then proof that a clean player install/update actually displays them on a test target. A historical "F-8 done" label alone does not satisfy it.

Recommended source is P405's `archery-butte-hits` set by Archaaz, source archive 1340. P405 reports 20 complete target pictures, plus four loose projectile pieces that the script does not use. Use the complete pictures only. That gives 20 new art IDs from this explicit manifest:

| Group | Source frame names as reported in P405 |
|---|---|
| Arrow east | Arrow East Bullseye; Arrow East Inner; Arrow East Middle; Arrow East Outer; Arrow East Total Miss |
| Arrow south | Arrow South Bullseye; Arrow South Inner; Arrow South Middle; Arrow South Outer; Arrow South Total Miss |
| Bolt east | Bolt East Bullseye; Bolt East Inner; Bolt East Middle; Bolt East Outer; Bolt East Total Miss |
| Bolt south | Bolt South Bullseye; Bolt South Inner; Bolt South Middle; Bolt South Outer; Bolt South Total Miss |

P405 reports these as 66 by 81 pixel, 24-bit BMPs with black backgrounds. It also names a sibling `archery-buttes` set with arrow1-14 and bolt1-14. Do not mix these inventories or claim to have recounted them in P571. The asset prompt must locate the actual files, confirm names/dimensions and publish its measured file list. If those source assets are unavailable, pause asset integration with the missing inputs named. Do not manufacture substitute frames from this prose.

Recheck the source's credit/terms before using it. P405 records Archaaz, no license stated, private use only and no reposting of the downloaded pack. Put provenance and credits in the existing art SOURCE.txt/registry format. The actual player-package distribution permission remains an explicit unverified review item; a private source repository does not by itself settle distribution. Use the project's existing art intake decision rather than silently declaring a new license or blocking this design on a legal guess.

Reserve IDs with `scripts/find-free-art.py` against the current approved client data, pinned source and this checkout's registry. Use its `--data`, `--pinned` and `--registry` arguments to avoid another checkout's defaults. Inspect any code/static/map hits and run `--check-registry` after registration. Do not take the download's 0x7898 through 0x78AB IDs on trust. P405 checked only selected slots, and no free range has been reserved by P571. Prefer a consecutive block if the scanner proves one, but bind code through an explicit state/facing table, not assumptions about filename order.

Append the 20 rows to `player-package/vendor/shattered-legacy-art/registry.csv` before placing PNGs. Add converted frames under its `art/<id>.png`, the provenance under SOURCE.txt, and one tiledata record for every new ID under records.json. Preserve geometry and anchor through `scripts/anchor-art-frames.py`; review conversion of pure black to transparency because black details in the target must remain legible. Keep a matching contact sheet for manual review in proven ignored scratch. No animation timer or animdata sequence is needed: server shot results select static images.

Read the actual approved client's stock 0x100A and 0x100B tiledata and copy each facing's full relevant collision/height properties to its hit pictures. P405 verified Impassable for 0x100A, but did not supply every field needed here. Do not guess the height or copy flags from an unrelated decoration. Match client records to `ScoringArcheryButteArt.Apply()` in the server's in-memory table, called from existing `ShatteredLegacyArt.Apply`. The silhouette must stay in the same place when empty art changes to a hit frame. Every display state must block the same footprint on server and client.

The existing package already ships registered PNGs into TazUO's ExternalImages/art and builds local tiledata overrides. Extend its existing registry/record tests and validate its current packaging rules instead of introducing a new art installer, TazUO source patch, protocol packet, map patch or redistributed EA data file. Test a records change invalidating the existing override stamp and an occupied EA slot refusing safely. Use a working copy of client data for tests.

No newly drawn art is required by the recommended reuse option, so there is no art for Chase to generate and no new-art request in P571. If Chase chooses original replacement art instead, the asset prompt must file it through `scripts/art/New-ArtRequest.ps1` under an authorized writable art-store run, not leave only a brief in notes. Never generate it unattended.

## Tests and acceptance

P571 adds no test or lane-test requirement. The following tests belong to implementation. Every new test must first show its intended failing assertion against the unchanged behavior, then pass after the change. A new-type compile failure does not prove the behavior failed; use a minimal callable stub where needed, then implement. Record both results. Use Windows PowerShell 5.1, `powershell.exe`, for every PowerShell test.

| Test area | Required observable proof |
|---|---|
| Engine hooks | Exercise actual Fire/OnDoubleClick with a recording subclass: exactly one resolved callback for miss, ordinary hit and split; correct ring/ammo; one callback after Gather reset; no callback or mutation on refusal. Run a stock butte alongside it and verify original scores, ammo, alignment and messages. |
| Facing and repeated fire | East and south each still accept a second shot after any hit/miss art change. Reject wrong side, off-axis, distances 4 and 7; accept 5 and 6. Test both shots with the real firing path, not just the artwork lookup. |
| RNG and scoring | Use the test host's controllable randomness/skill handlers where available, restore globals in finally, and check values on either side of ring cutoffs 0.10, 0.25 and 0.50. If an RNG seam is missing, argue the smallest seam before adding it. Never use a probabilistic test or a wall-clock sleep. Split/no-split with known stored counts and a guaranteed split at 50 must exercise the engine result and its displayed frame. |
| Ammo/reset | Arrow and Bolt hits, misses and splits; mixed stored ammo; no-ammo refusal; repeated gather produces no extra ammo; empty-counter close-click clears without creating ammo; two shooters share stock gathering/reset semantics but have separate scores. Unsupported ammo never becomes a displayed/recovered Arrow or Bolt. |
| Access/tutorial loans | Dead/wrong-map/blocked-LOS use has no effect; an active bow or other wing trial is refused; marked remaining loans are refused; finish/cancel returns loans normally; the butte cannot turn 50 lent arrows into permanent stacks or increment tutorial evidence. Ordinary owned ammo still works afterward. |
| Skill/progression | One accepted shot reaches the normal skill handler once with its original window. Refusals do not invoke it. Preserve the wrapper's behavior and no-challenge ceiling, and make no direct XP, milestone, achievement or League award. |
| Saves and lifecycle | Save/load both orientations with all logical display states, stored mixed ammo and attached component references. Confirm picture/collision, orientation and ammo survive; volatile scores/cooldown reset. Invalid display resets safely. Existing stock save chains have no new fields. Test real entity references/load ordering as well as direct round trips. |
| House and redeed | Correct facing from both deeds; moved/deleted deed at target time; backpack/ownership/fit failures; owner-only chop; ammo blocks chop without loss; empty chop returns one matching deed; repeated chop yields no duplicate; public subtype never yields a deed. Material hues cannot tint the visible component or alter behavior. |
| Craft acquisition | Register twice yields one row per facing; each skill/resource row is correct; insufficient resources fail without output; a real successful craft consumes the requested resources and makes the right deed. Output is nonexceptional. Existing 80,000-point cleanup reward remains its stock type and price. |
| Public placement | Test gate, dry run, all-or-nothing preflight, repeated place, moved/duplicate tags, occupied lanes, clear with stored ammo, repeated clear, and unrelated/house/stock lookalikes preserved. Map checks use actual patched data during acceptance, not only fake Fits predicates. |
| Package and records | Every manifest frame has exactly one registered ID, PNG and matching server/client tiledata; mappings cover both facings without collisions. Deleting one PNG, changing one record or breaking one mapping makes the relevant new check fail, then restoring it makes the check pass. No EA file is modified in place. |

Proposed test homes: `server/tests/Items/Addons/ScoringArcheryButteVerification.cs`, `server/tests/Tutorial/TutorialScoringButtePlacementVerification.cs`, and additions to `player-package/tests/Build-UoOverrides.Tests.ps1` and `Package-Client.Tests.ps1`. Use the existing sequential shard fixture and restore altered clocks, skill handlers, RNG and world items after each case.

Run `docker/uo/build.sh` with the prompt's own image tag and required build lock. Let its normal patch, nonzero-test and full shard test gates run. Do not substitute direct docker build/compose build. Package tests run in Windows PowerShell 5.1; tests that require a server must use an explicitly authorized throwaway loopback-only shard and scratch saves, never a live service.

Manual acceptance must show all 20 hit frames plus both empty targets, repeated shots in each facing, gather/reset, both ammo kinds, split messages, correct anchors, readable scores, and collision from all sides. Show both house deed placements and a save/restart. Install/update a clean local player package and record its version/hash plus what was actually seen. A screenshot of an asset contact sheet is not updater proof. None of these client/world checks was performed by P571.

## Ordered Golem prompts

These are proposed prompt briefs with dependency order, not assigned P numbers or edits to the prompts repo. Each writes its own notes and finishing marker. Every build stays on ModernUO and follows the no-deploy/no-Haven rules. Do not start parallel edits to the shared art registry or records.

### BUTTE-A: integrate the reviewed hit artwork

**Touches:** server, client

Depends on Chase's pack choice and access to the actual assets. Read P405 and this design. Verify the manifest and provenance, scan/reserve IDs, convert the 20 complete pictures, append registry/provenance/records, and add ScoringArcheryButteArt plus its existing ShatteredLegacyArt application call. No world items, recipe rows or scoring component yet. Reuse the package's existing override route. Add the specific new record/package checks, show them fail before their data/code change, then pass. Run registry/art validation, PowerShell package checks and build.sh because server code changes. Notes include the exact source file list, assigned IDs, copied stock tiledata values, hashes and remaining client checks. Art is ready to inspect, not published.

### BUTTE-B: add the scoring component and house deeds

**Touches:** server

Depends on A's measured manifest and assigned IDs. First capture failing behavioral tests for hook delivery and repeated-fire facing. Implement the narrow hook patch, generated new types, logical display map, local player/loan guards, close-click reset and owner redeed rules. No full Fire copy, stock save conversion, reward replacement or automatic spawn. Test ammo/scoring parity, real firing paths, saved state, house lifecycle, public no-deed subtype and tutorial loan refusal. Run build.sh and record the hook sites in the bump checklist. New items are staff-constructible but have no player acquisition yet.

### BUTTE-C: add crafting and the explicit tutorial-yard layout

**Touches:** server

Depends on B and Chase's acquisition choice. Add the two idempotent recipe rows at the stated requirements, preserving the cleanup reward. Inspect patched map data and finalize the owned yard layout, including complete lanes and approach tiles. Add the test-only dry-run/place/status/clear command, owned public props and concise instructions after loan return. Keep the echo tutorial unchanged. Show new acquisition and placement tests failing first, then passing; run build.sh. Deliver verified coordinate tables and a staff walkthrough. Do not seed a shared world during this build prompt.

### BUTTE-D: prove the player update and local end-to-end behavior

**Touches:** server, client

Depends on A through C. Use only a new throwaway loopback-only container with scratch saves and an isolated local player-package install; obtain the normal local resource locks. Run the package build and its required checks, inspect every state through real shots or documented staff setup of deterministic scenarios, demonstrate an update from a package without these frames, restart the scratch world, and complete the house/public acceptance list. Save evidence in proven ignored scratch and summarize version/hash, results and any unverified parts in notes. No Haven, publication, shared-world restart or account changes. If local client interaction needs Chase, finish all automated proof and name the exact remaining visual checks honestly.

Only after D's recorded proof should the overseer prepare Chase's separately authorized release: client package available before scoring targets/recipes become player-facing, followed by a deliberate yard placement and walk. This respects the existing art prerequisite. Release is not implicit in any of these prompt briefs.

## Failure handling and implementation handoff

If artwork fails its slot, permission or package check, leave existing stock buttes and cleanup rewards usable and do not expose the new acquisition/world props. Do not let a partially filled manifest select an arbitrary item ID. During development it may fall back to the corresponding stock empty art, with an explicit diagnostic, while scoring remains stock. Such a fallback does not count as feature acceptance.

After the new types enter saves, retain their classes, inheritance and registered art IDs. Reversing a release must not mean deleting their source or reusing their IDs. A forward rollback can suppress hit pictures to stock empty art, stop offering new deeds and clear only owned public props after gathering ammo. It must preserve existing house addons, recoverable ammo and redeed support. Do not load saves containing new classes in an older image that cannot read them.

For overseer promotion, this is custom training-yard content. Proposed differences from the stock butte are its display, safer local interaction checks, active-loan refusal, zero-ammo close-click reset, ammo-before-chop check, new craft source and explicit public layout. Record the accepted choices and any required fidelity-register entry through the overseer; this task does not write `docs/`. Do not label the invented recipe as an unchanged OSI port.

## Verification performed for P571

Read-only source and notes review, with line references above. No lane tests were added or run, as requested for this design-only task. No art was generated, imported or requested for drawing. No server, client or package build was run; no world, account, service or client installation was contacted or changed. No Haven connection, commit, merge, push or branch switch was made.

Unverified: actual third-party frame bytes and distribution terms; free slots in the currently approved client; every stock tiledata field; proposed map positions, elevations, paths and current world occupancy; this set in a clean installed/upgraded player package; runtime/save behavior of the proposed implementation. These are explicit inputs or acceptance work in A through D, not hidden implementation claims.

Document checks passed: valid UTF-8, no em dashes, no replacement characters or trailing whitespace, and well below 5 MB. Both repositories passed `git diff --check`; the code work copy is unchanged and this note is the only added file in the notes work copy. Local Markdown links resolve. Windows PowerShell reports version 5.1.26100.9711. Ran `tools/progress.py --dry-run` with `SL_SHARD` and `SL_MIGRATE` pointing at these work copies; exit 0. The reporter writes tools/progress.json even in dry-run mode, so its original bytes were captured and restored in finally, with SHA-256 equality confirmed. Its printed inventory is a filename/source census, not evidence that this proposed feature works. Stop-request checks between steps found no request.

## Questions for Chase

1. **Which pictures should ship?** Recommended: the complete hit-display set reviewed in P405, both facings, rather than the sibling arrow1-14/bolt1-14 set. It has a direct ring/ammo manifest and needs no new drawing. Confirm its intake/distribution treatment before packaging; choose original art through the existing request process if that set cannot be used.
2. **Crafted deed or reward deed?** Recommended: craftable east/south deeds with the proposed training-dummy requirements, while the existing 80,000-point cleanup reward stays stock. This accepts that the new craft provides equivalent practice more cheaply. If preserving that reward's exclusivity matters more, choose reward-only before C; do not invent a League currency price.
3. **Should this replace the bow tutorial?** Recommended: no. Keep three echo hits and the current loan cleanup. Add the buttes as optional practice with owned ammo after the trial, and refuse use during an active loaner trial.
4. **Should a miss-only session have a close-click reset, and must ammo be gathered before redeeding?** Recommended: yes to both on the new type. A picture should be clearable even with no recoverable ammo, and an owner should not lose stored ammo by chopping.
5. **Where should the first public range go?** Recommended: two targets beside the current New Haven tutorial yard, using the candidate lanes above only after patched-map preflight and a client walk. Leave existing town buttes unchanged.
6. **What should scores earn?** Recommended: nothing. Keep stock scores as informal shared practice, without repeatable tutorial credit, XP awards, prizes or a leaderboard.

P571 DONE
