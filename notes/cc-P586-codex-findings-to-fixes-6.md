# P586: review findings to fix-up drafts, round 6

October 25, 2026. Notes only. These are unnumbered drafts for the overseer, not queued work or authorization to implement or publish.

## Result

Six new follow-up drafts cover the remaining findings in P573, P580, P581, P582, P583 and P585. U1 comes first because failed tutorial delivery spends a limited allowance and an orphaned active record prevents progress. W1 fixes two achievement ground-classification defects. W2 corrects misleading Artificers text. W3-W5 strengthen coverage of working death, smith and hatchling paths; W5 also corrects a fidelity claim. A coverage gap is not a reproduced gameplay defect.

P574's existing questions, P576's pending play-test plans, P577's refreshed guide, P578's release draft and P579's Appraiser recommendations do not need replacement prompts. P584 has no note in this checkout and is still claimed in the prompts repo. Its review remains pending; there is no P584 verdict to infer or repair to draft.

## Evidence and scope

Read both work-copy AGENTS.md files, the governing document index, direction decision and task list. Code HEAD is `6b7437172d2d87af5f7ad2b4daa6048ed6f20efe`; notes HEAD is `c5c0389716b29bda57c23f2bbf011aa72f5139a2`. Both started clean. These are local snapshots, not claims about deployed freshness. Read the P572 report and work record for the requested shape and the P429/P476 ownership rules, then the available P573-P585 notes and adjacent reviews listed below.

Confirmed the relevant current implementations and assertions in the canonical code tree. Tutorial paths cited by P573 have no changes from its reviewed `1020e36` to current HEAD. The smith, death-hook, Noted by the System implementations and cited tests have no changes from the reviews' `608d0b4` to current HEAD. The Artificers review already uses current HEAD. Read the current hatchling hook, real-tame test, taming patch and Staff changelog as well.

Read-only references: ModernUO `d4531cd94b739613155225c234900de9f47d2c88` and ServUO pub57 `d76bf4443cf76d081ddaf8f57c87ff33749256af`. Read the actual backpack-delivery, movement and taming implementations. Nothing under server/uo/ was used.

Paths below use C for `server/customizations/`, T for `server/tests/`, P for `server/patches/`, and N for this notes directory. Code paths are relative to the supplied ShatteredLegacy work copy. Confirmed means source and call-path inspection supports the finding. No new runtime reproduction or mutation run was performed.

## Verdict table

| Input | Verdict and current evidence | Disposition |
|---|---|---|
| P573 #1 | Confirmed delivery defect. C/Tutorial/TutorialFarm.cs:294 increments BandagesIssued before unchecked AddToBackpack at :295. Pinned Projects/Server/Mobiles/Mobile.cs:7584 provides PlaceInBackpack; AddToBackpack at :7594 drops failed delivery at :7605. T/Tutorial/TutorialFarmVerification.cs:445 tests the cap without a full pack. | U1. Preserve the cap; make delivery and allowance consumption agree. |
| P573 #2 | Confirmed active-record recovery defect. C/Tutorial/ClusterFTutorial.cs:71 permits a missing/deleted/off-account owner for the page, but :64 still requires an exact serial for participation. TryEnter at :112 only accepts NotStarted; StartRemedial at :225 only accepts Skipped. T/Misc/TutorialVerification.cs:596 deletes an owner only after skipping. | U1. Recover active ownership at a defined entry point without resetting progress or entitlements. |
| P574 | Existing question collection, not implementation. Its adjacent review has no findings. Recommendations remain proposals; its existing reconciliation already protects accepted decisions. | Keep its stable question IDs and recommendations. Refer to it under For Chase; do not produce another question sweep or builder task. |
| P575 | Summary with an explicit Saturday cutoff, not evidence of the whole weekend or installation. Its adjacent review has no findings. Tutorial and satchel warnings refer to existing reviews. | No repair draft. Use its testing priorities with their original owners. |
| P576 | Pending plans, not executed tests or new independently established defects. Its adjacent review has no findings. Its deleted-owner plan 28 uses Skipped and does not cover P573's active states. | Keep the plans. U1 adds active-state and failed-delivery regressions; other repeated findings retain existing owners below. |
| P577 | Refreshed tutorial draft explicitly retains P573's remaining limits and planned island status. No new gameplay finding. | Existing P478 integration input; U1 owns the two tutorial defects. |
| P578 | Release prose retains known corpse, satchel and tutorial limits and separates proposals from merged code. Its adjacent review has no findings. | No repair draft. Preserve the pending-update and availability labels. |
| P579 | Research/design input for existing P452. The exceptional armor counterpart is already within P452's explicit crafting-bonus scope. The source report's empty-P452 observation is historical: that brief is now populated. | A1 below, with explicit policy conflicts. No second Appraiser task. |
| P580 #1 | Confirmed coverage gap. T/Misc/NotedBySystemVerification.cs:848,856 use the book and are stopped by C/SmithGuildBook.cs:678. The direct call at :850 tests Generate, not GenerateLarge. The actual large-generator guard remains correct at C/ClusterFSmithCommissions.cs:578. | W4. Add direct generator coverage after both abandon sizes; preserve the accepted shared wait. |
| P581 #1 | Confirmed coverage gap. T/Misc/DeathHooksVerification.cs:126 checks only the source record at :137. C/LootBoxes/ClusterFLootBoxes.cs:110-111 separately creates and delivers the box; :180 deduplicates eligible players. No mixed-credit or delivered-box assertion exists in that fact. | W3. Assert actual source-specific delivery and same-loop nonduplication through real kills. |
| P581 #2 | Confirmed coverage gap. The AlwaysZero random stub at T/Misc/DeathHooksVerification.cs:114 makes the first roll succeed; the already-enchanted item would then skip a second roll. C/ClusterFRareSelfRepair.cs:92 makes the probability call only for an eligible item. | W3. Use a first-miss, second-hit counting stub through a real death. No present double-roll defect is asserted. |
| P582 #1 | Confirmed classifier defect. C/ClusterFNotedBySystem.cs:907 examines world items only for FireFieldItem. Ordinary immovable surfaces never enter its floor candidates. Pinned Projects/UOContent/Engines/Pathing/Movement.cs:384-395 accepts qualifying item surfaces. | W1. Cover a placed world floor over snow, not only a map-static seam. |
| P582 #2 | Confirmed classifier defect. The static loop at C/ClusterFNotedBySystem.cs:927 accepts any surface below the feet; :952 always prefers it to land. It never compares the supporting land height. Pinned movement at :261,353,437-463 compares land and surface candidates. | W1. Elevated snow above a buried floor must classify as snow. World occurrence is unverified. |
| P582 #3 | Confirmed coverage gap. T/Misc/NotedBySystemVerification.cs:511 creates an old crafted item without recording its crafter; it fails identity validation before the age limits. The fresh positive at :516 does record the crafter. | W1. Separate own-craft age boundaries from provenance rejection. Do not redraft P457's previously reported missing-loot exception. |
| P583 #1 | Confirmed fidelity-description risk, not a P458 production regression. T/Services/TimeOfLegends/EodonRemainderVerification.cs:701 expects unchanged re-tamed skills and CHANGELOG.md:57 says taming back takes nothing more. Pinned taming scales only on first tame; ServUO Scripts/Skills/AnimalTaming.cs:432-435 also scales subsequent tames by 0.90. | W5 corrects the attribution. C1 below handles whether to retain or change the inherited behavior. Keep the extra hatchling cut first-tame-only. |
| P583 #2 | Confirmed coverage gap. C/Services/Expansions/Time Of Legends/Mobiles/DragonTurtleHatchling.cs:74 assigns SkillsCap before its extra cut. Its real-tame fact checks skill bases and per-skill caps at :679-684 but not the total cap. | W5. Protect the independent fixed-point total with a mutation-sensitive assertion. |
| P584 | No matching note exists in this checkout. The claimed Verite prompt requests a review of P459; it is not a result. | Pending input. Reconcile its eventual findings separately. No code review was invented to fill the missing number. |
| P585 #1 | Confirmed misleading text. C/ArtificersGuildmasterGump.cs:129 says imbuing earns Shards; C/ArtificersImbueGump.cs:1880 spends them and :1898 awards Standing. | W2. Distinguish currency sources from imbuing's Standing reward. |
| P585 #2 | Confirmed misleading default eligibility. C/ArtificersGuildmasterGump.cs:155 promises skill bonuses on robes/cloaks; C/ArtificersImbueGump.cs:499,538 uses configured crafter gear, default HalfApron/FullApron in C/Imbuing/ImbuingTable.cs:136. | W2. Describe general clothing attributes and default apron skill eligibility accurately. |
| P585 #3 | Confirmed wording risk. Joining Requirements at C/ArtificersGuildmasterGump.cs:176-181 puts the task before Join. C/ClusterFGuildSystem.cs:313 and :397 separate free entry from the Apprentice task. | W2. Explicitly separate joining from the optional next task. No new entry requirement. |
| P585 #4 | Confirmed unsupported availability promise in the checked sources. C/ArtificersGuildmasterGump.cs:212-215 advertises a trial and advanced acquisition routes without planned labels. C/ClusterFGuildPromotion.cs:34,79 defaults to waived trials. P585's knowledge-write audit found book/staff entry points, not those normal advanced reward callers. | W2. Label future acquisition routes and current trial defaults; do not implement rewards from this text correction. |

The available adjacent P574-P576, P578-P583 and P585 Codex reviews all report no findings in their notes changes. That verdict does not erase the implementation findings in their main review reports. No adjacent P573 or P577 review file is present in this checkout.

## Deduplication and existing owners

Searched Markdown prompts recursively in `D:/UO/cc-prompts/queue`, `waiting`, `completed`, `claimed`, `merging` and `held`. Read the relevant P429/P476/P478, P452-P455, P457/P458/P460, P572 and P584 briefs. Compared the actual P429, P476, P533, P556 and P572 synthesis sections. Queue hits are candidates until the brief's scope is read; a completed review or original implementation is not a completed follow-up fix.

Catalog SHA-256 at inspection: `f1cbeaa726f5118514f667f049289846b3f8ff0c5371414b71805b916df915e4`. Method: use the folder order above, recursively sort Markdown paths within each folder using Python WindowsPath ordering, join relative POSIX path plus one space plus lowercase content SHA-256 with LF and no terminal LF, then hash the UTF-8 result. This records the inspected catalog, not remote state.

| Existing owner | Keep there |
|---|---|
| Completed P453 and P533 A2 | Original one-pet entitlement, pending picker, living-alt restrictions, cap and successful-heal work. U1 concerns failed delivery and active orphan recovery remaining after that implementation. Do not rebuild those completed features. |
| P533 U4 | Paid elixir delivery, retained vet-service validation and tutorial exit gating. U1 changes Farmhand bandages and active record adoption only; coordinate shared ownership helpers if both drafts are issued. |
| Completed P454; P476 W10 | Shared commission cooldown and Pre-Crafted implementation; separate dragon-armor small-pool correction. W4 adds the missing direct large-generator assertion, not another cooldown or pool rewrite. |
| Completed P455 | Working earlier death hooks, bestiary master credit and killed-pet effect exclusion. W3 adds the delivery/multiplicity regressions P581 identified. |
| Completed P457; P533 A4 | Earlier destination/height changes, provenance rule, and separately retained missing-loot and optional action-route follow-ups. W1 repairs the new supporting-floor cases and age-test masking only. |
| Completed P458 | First-tame hook, spawner weights and held-vine refusal. W5 protects SkillsCap and corrects the re-tame attribution. C1 is not permission for a global taming change. |
| Completed P460 | Its three original reward/learned-tier texts. W2 addresses the four surrounding passages P585 found, without redoing their correct changes. |
| Queued P452 | Exceptional crafting payouts, ordinary blessed books, monotonic refresh and config-null publication. Use P579 as research with A1's conflicts resolved by the overseer. |
| Queued P478 | P577 guide refresh plus P572's existing editorial checklist. No new wiki catch-up or guide-writing draft. |
| P556 U1/U2/U3/W1/W2; P476 U2 | Repeated Civic pricing/baselines, launcher preparation, Hunter's Satchel admission, tree identity, mining shared validation and destructive corpse approvals. P575/P576/P578 do not create second owners. |
| P451 and P413 adjacent reviews, carried into P576 | Existing populated Field Satchel return, Rootdeep footprint and clean-baseline map-builder findings. P576 proposes pending checks for those original findings, not new code evidence or a new repair owner. Keep the original handoffs separate from U1 and W1-W5. |
| P533 W24 | All repeated progress.py dry-run writes. No seventh repair draft for the reporting helper. |
| P481; P574 | Planned start-area design and existing decision collection. No island builder or repeat question sweep. |

## Common instructions for the drafts

Each draft below is ready for numbering after the overseer's duplicate check against the then-current queue. Substitute the assigned number for P??, including the note filename and final marker. They all use Model Opus, following the current server-lane briefs' tool-access choice.

Read both work-copy AGENTS.md files before implementation. Change only canonical customizations/tests and necessary metadata or prose. No Haven connection, deployment, live-account work, save repair, commit, push, merge or branch switch is authorized by these drafts. Build server changes through `docker/uo/build.sh -t sl-modernuo:cc-P??`, using its test gate and a disposable local test world where needed. Every PowerShell script/test runs under Windows PowerShell 5.1.

For defect fixes, first watch the new regression fail against the existing implementation, then fix and watch it pass. For coverage of correct code, first apply the named temporary mutation, watch the new regression fail, restore production code and watch it pass. Record the exact case, mutation and result. Restore every mutation before the final build. A passing old test, a source assertion or a direct event-handler call does not replace the requested real action. Only appropriate existing checks are required; no new framework or unrelated coverage campaign.

## Urgent draft

### U1. Tutorial supply delivery and recovery of an orphaned active record

```text
# CC task P??: tutorial follow-up: keep failed bandage issues and recover active trainees

**Model:** Opus
**Touches:** server
**Golem:** any
**Summary:** P573 found that failed Farmhand delivery spends a limited allowance and that deleting an active trainee leaves the replacement character unable to continue. Original P453 pet and ownership safeguards remain in force.

Read P573, P453 and the P533 A2 ownership addendum; coordinate with P533 U4 if it is being implemented.

1. In TutorialFarm.GiveBandages, use PlaceInBackpack or equivalent checked delivery without a world-drop fallback. Delete an undelivered stack, leave BandagesIssued unchanged and tell the trainee to make room. Return a distinct failure result if the current enum cannot express this truthfully. The Farmhand must not report a successful gift or an exhausted allowance for a capacity failure. Increment only after successful placement. Preserve current defaults, account cap and existing-bandage check.
2. Add one deliberate recovery entry point, such as login or opening Rook's page. An ordinary same-account character may adopt an active record only when its old owner is absent, deleted or no longer belongs to that account. Store the replacement CharacterSerial before exposing actions. Use the same ownership result for the page, participant checks, lessons, farm and completion paths; avoid side effects in arbitrary eligibility getters.
3. Preserve State, completed lessons, StartedAt/FinishedAt where applicable, WasSkipped, PetClaimed, PetClaimPending and BandagesIssued. Do not replay rewards, replace a living same-account trainee, clear progress or grant another pet. Existing skipped-remedial and graduated-pending behavior must remain valid.
4. Red-first regressions: full pack by item count and separately by weight, no backpack, repeated refused conversations, no new ground stack, allowance unchanged, then free space and retry through the Farmhand for exactly one counted gift. Verify successful issues still stop at the saved account cap after banking and remedial training.
5. Red-first recovery cases for InCore, InWings and Remedial: remove the recorded owner, enter through the chosen public path as another character, then successfully perform a lesson/farm action appropriate to the preserved state. Cover missing serial, deleted owner and off-account owner. Keep a living-owner negative through rendered buttons and retained replies. Round-trip the adopted record with its progress and claims and a trailing sentinel, then verify a further same-account character cannot take over while the adopted owner remains valid.
6. Run the tutorial suites and normal build gate. Add plain player-facing Fixed lines without exploit instructions. Give P478 the corrected final guide wording only after behavior is verified. Notes: notes/cc-P??-tutorial-delivery-recovery.md, with red/green evidence and unverified client checks. End P?? DONE.

**Done means:** delivery failure consumes nothing and creates no world gift; each orphaned active state becomes usable through the replacement character while progress, account limits and valid-owner restrictions survive.
```

## Other drafts

### W1. Achievement footing uses the supporting surface; age tests reach the age check

```text
# CC task P??: Noted follow-up: world floors, elevated land and independent recycling age tests

**Model:** Opus
**Touches:** server
**Golem:** any
**Summary:** P582 found two remaining GroundAt errors and a recycling negative masked by missing crafter identity. Existing P457 fixes and the accepted own-craft-or-loot rule retain their separate ownership.

1. Read P582 and compare GroundAt with pinned Movement.cs, including GetAverageZ, static/multi surfaces, immovable world-item surfaces, CalcHeight and bridge behavior. Classify the support at the player's feet. A floor below higher supporting land cannot override it. A qualifying world floor over snow must mask that snow just as a map floor does. Keep the existing near-feet fire/overlay behavior and mounted, footwear and armor filters.
2. Red-first cases: snow land at Z 0, an immovable world floor using a seeded passable graphic such as 0x0491 at Z 20, and feet at its calculated top returns Other; snow land at Z 20, a buried ordinary static floor at Z 0, and feet at the land height returns Snow. Include land height in any expanded test seam. A coordinate-only fake that always supplies land Z 0 cannot prove the second case. Cover equivalent static/multi/world support and irrelevant movable or overhead items where the implementation needs those distinctions.
3. Drive representative cases through a real completed player step and assert the correct counter delta, retaining floor-over-snow and upstairs-field controls. Keep terrain reading behind the existing equipment filters. Prefer a narrow supporting-surface helper over copying the whole movement engine or patching upstream; document alternatives before any upstream patch if one proves necessary.
4. Repair the old-item negative by recording the recycler as crafter through CraftAttempt before Recycled. Use separate fixtures/counters to test exceptional own-crafts just outside ten seconds and just outside one minute, with positive controls inside each window. Preserve identity/protection checks. Independently remove each relevant age condition temporarily and watch its new assertion fail, then restore it. Do not implement the separately reported missing-loot exception as incidental scope.
5. Run focused Noted suites and the normal build gate. Public changelog wording stays generic, with no hidden conditions or rewards. Notes: notes/cc-P??-noted-footing-age.md. Record the source/movement comparison, red/green cases and world-occurrence limits. End P?? DONE.

**Done means:** the two concrete floor regressions fail before correction and pass afterward; each age negative independently detects loss of its time guard.
```

### W2. Artificers pages state currency, clothing, entry and availability accurately

```text
# CC task P??: Artificers text follow-up: currency sources, apron skills and planned rewards

**Model:** Opus
**Touches:** server
**Golem:** any
**Summary:** P585 found two incorrect claims and two ambiguous promises around P460's corrected passages. Match the current implementation without changing guild mechanics or creating future rewards.

1. About: say Essence Shards come from disenchanting, extraction, work orders and the Apprentice task after checking those reward callers. Successful imbuing spends Shards and earns Standing. Keep these separate in player language.
2. What We Enhance: describe general attribute bonuses on clothing. Crafting and gathering skill bonuses use configured crafter gear, defaulting to aprons. Do not promise robe/cloak skill eligibility or imply jewelry's skill groups are the same. Qualify defaults rather than hiding server configuration.
3. Joining Requirements: explicitly say no skill or tribute is required to join. Label Imbuing 20.0 or three Diamonds as the optional next Apprentice task after entry, using the current task description. Keep the rewards attached to completing that task.
4. Rewards: identify the currently waived trial requirement under defaults and mark advanced 140+ acquisition through quests, commissions, boxes or bosses as planned until real reward callers exist. Preserve the actual learned-tier, account knowledge and soul-forge rules. Match effective trial configuration where the page makes a current-state claim, or state the default clearly.
5. Extend the existing ArtificersTextVerification page assertions for those four semantic distinctions, seeing each fail on the current text first. Assert meaning without pinning unrelated formatting. Retain P460's already correct tests. Run the existing guild/imbuing checks appropriate to the change and the normal build gate; a C# text edit still has to compile. Client rendering remains a separate check unless actually performed.
6. Add a plain Fixed changelog line for corrected guidance. Give P478 final text to reconcile with artificers-order.md; do not change historical review notes or advertise new acquisition routes. Notes: notes/cc-P??-artificers-guidance.md. End P?? DONE.

**Done means:** the four pages agree with current defaults and clearly label planned content, with no mechanics, eligibility or reward-table changes.
```

### W3. Death-hook tests prove box delivery and one probability attempt per item

```text
# CC task P??: death-hook coverage follow-up: delivered boss boxes and one Self Repair attempt

**Model:** Opus
**Touches:** server tests
**Golem:** any
**Summary:** P581 found missing assertions, not a remaining event-order or duplicate-roll bug. Strengthen DeathHooksVerification around the working P455 implementation.

1. Kill a real eligible boss through mixed damage from a player and their pet or summon plus another eligible player. Ensure each actually has ordinary looting rights. Assert exactly one boss-source LootBox is present in each eligible player's pack or bank, with the source record, then kill another boss of that type in the same loop and assert no additional boss-source boxes. Include controlled and summoned damage coverage without crediting the helper as a recipient.
2. Filter by LootBox.Theme, EarnedFor and BoundAccount in LootBoxItems.cs, matching the actual OnBossKilled label, rather than assuming a stored source-key property; achievement boxes can also arrive during this kill. Test the normal backpack route and a full-backpack fixture reaching the existing bank fallback. Do not count every LootBox as a boss award or infer delivery solely from RecordOf.
3. In a real high-end death, use a scoped counting random stub whose first relevant Next(500) misses and whose second would hit. Arrange known eligible corpse items and isolate unrelated RNG consumers. Assert one probability call per eligible item and no Self Repair after its first miss. Keep the existing positive-roll and ordinary-source negatives. Restore global RNG in a finally block.
4. Red-first mutation proof: suppress delivery while retaining source recording, and watch the new delivery assertion fail. Separately add a temporary second corpse traversal and watch the first-miss/count assertion fail. Restore both and run the focused suites and normal build gate. Avoid production edits unless a new reproducible defect emerges, and explain any such scope change before fixing it.
5. No gameplay-fix changelog claim for added coverage alone. Notes: notes/cc-P??-death-hook-coverage.md, recording source-specific outcomes, mutations, restoration and runtime limits. End P?? DONE.

**Done means:** tests fail when recorded boxes are not delivered and when an eligible item receives a second probability attempt; correct production code passes after all mutations are restored.
```

### W4. Direct large-commission requests independently obey the shared cooldown

```text
# CC task P??: smith cooldown coverage follow-up: direct large generator after either abandon

**Model:** Opus
**Touches:** server tests
**Golem:** any
**Summary:** P580 found that the book-level refusal masks the guard in GenerateLarge. The accepted shared cooldown is already implemented correctly.

1. Extend LargeCommissionsShareTheAbandonCooldown or a focused companion fact. After a real book abandon of a large commission, assert the large slot is empty and direct SmithCommissionSystem.GenerateLarge(pm) returns null during the wait. Repeat after a real small abandon, again with an empty large slot. Keep the direct small-generator and book assertions.
2. Advance the deterministic clock past the configured shared wait in each independent branch. Assert a direct large request succeeds and creates exactly one active large entry. Arrange fresh or cleared fixtures so a maximum-active check cannot masquerade as the cooldown. Failed requests must add no entries or alter the recorded abandon time.
3. Temporarily remove only GenerateLarge's RequestCooldownLeft guard. Watch the new direct assertion fail while the book's guard remains intact. Restore it and run the focused Noted/smith suites plus the normal build gate. Keep production cooldown, Pre-Crafted and pool behavior unchanged unless a separate regression proves a defect.
4. Notes: notes/cc-P??-smith-direct-cooldown-coverage.md, with mutation/red/green evidence. No gameplay-fix changelog claim for coverage alone. End P?? DONE.

**Done means:** both abandon sizes protect the direct large-generator entry point, and removing only its guard makes the new regression red.
```

### W5. Protect the hatchling total cap and correct the re-tame attribution

```text
# CC task P??: hatchling follow-up: assert the total skill cap and explain inherited re-tame behavior

**Model:** Opus
**Touches:** server tests and prose
**Golem:** any
**Summary:** P583 found an untested SkillsCap assignment and a misleading source-fidelity claim. P458 correctly applies the hatchling's extra skill cut only on first tame.

1. Extend the existing real-tame fact. Before taming, capture every relevant wild skill in fixed-point units and derive the total after the ordinary un-paralyzed 90% tame scaling, using pinned rounding and all skills, before the extra hatchling cut. Assert this independently computed total equals SkillsCap after the first tame. Per-skill Cap == 100 is a different assertion and stays.
2. Release and successfully re-tame through AnimalTaming. Assert the same original SkillsCap remains; do not recompute it from reduced or subsequently trained current skills. Preserve stats and the first-tame-only extra 55% reduction. Keep the currently expected inherited skill-base behavior until C1's policy-dependent change is separately chosen.
3. Temporarily remove only DragonTurtleHatchling's SkillsCap assignment. Watch the new cap assertion fail with a controlled fixture whose constructor total differs from the expected post-tame total. Restore it and watch the real-tame test and normal build gate pass. Do not replace the actual tame with a direct OnAfterTame call.
4. Correct the Staff changelog description and test comments so they distinguish the faithful first-tame hatchling cut from ModernUO's inherited no-further-loss re-tame behavior. ServUO applies an ordinary 10% skill reduction on subsequent successful tames, including the same owner. Describe the checked behavior as a known fidelity difference, not original behavior. Put a proposed deviation-register entry in notes for the overseer; do not edit docs/.
5. C1 concerns an optional production change to this inherited behavior. Do not change all pets' taming pipeline or introduce another hatchling cut within this coverage/prose task. If the overseer explicitly includes the source-style re-tame correction, settle its narrow scope first and add separate red-first same-owner/new-owner cases.
6. Notes: notes/cc-P??-hatchling-total-cap.md, with fixed-point calculations, mutation proof, fidelity text and remaining runtime checks. End P?? DONE.

**Done means:** loss of the total-cap assignment is caught, re-taming preserves the saved total cap, and prose no longer equates inherited re-tame behavior with ServUO's.
```

## Additions to existing work

### A1. P452 uses P579 as research, with its policy differences made explicit

P452 is now a populated queued brief, not the empty file seen by P579 or the waiting placeholder seen by P572. Read its actual current instructions before implementation. It already includes exceptional armor, blessed books, refresh-hour rollback and null configuration. P579 does not replace any of those criteria.

Carry its useful concrete calculations and regressions into that owner: actual ordinary crafting at Arms Lore 0/100/200, exceptional ranged weapons, separately priced real magic, armor crafting bonuses, exact Spellbook/NecromancerSpellbook types with constructor blessing, real Lead delivery and turn-in, independently effective cap/rounding assertions, protected items and quote-time versus sale-time changes. Keep raw combat properties and Imbuing's own catalogue intact.

Two recommendations conflict with the current brief and remain proposed. First, P579 preserves raw board matching and removes quality bonuses only from payment, while P452 asks for exclusions in board magic/count paths and an explicit matching decision. Second, P579 recommends Appraiser sales of magical ordinary blessed books, while P452 defaults to no if that sale permission is uncertain. Before issuing implementation, the overseer should resolve these within P452 rather than silently substitute P579. Recommended scope: a separate adjusted magic summary shared by eligibility and price, preserving explicitly intended non-magic requests; permit exact ordinary magical books only if that Appraiser extension is accepted. Keep the normal zero-magic book refusal and explicit personal protections.

P579's conservative residual DI rule and exclusion of exceptional armor resist rows are useful proposals, not established provenance or approved balance. They can undervalue real enchantments and need the stated decision and tests. If narrower scope is chosen, name the residual armor or genuine-magic valuation tradeoff instead of claiming every crafting payout is closed. No new P586 Appraiser draft is needed.

### A2. P478 receives the latest guide input; P576 remains a pending plan list

Use N/wiki-drafts/new-player-tutorial.md from P577 with P572's existing editorial checklist. Keep test-world availability and planned P481 island labels. After U1 merges, update the exact failed-delivery and deleted-owner caveats against verified behavior. Until then, retain the caveats already carried in P573/P578 and do not promise active-record recovery. P585's source-backed guide distinctions are inputs for W2 and the same P478 integration.

P576 is already a structured list of pending plans. Do not write another list, import it, mark results, or authorize fixture setup in this synthesis. When U1 is implemented, attach full-pack failure/retry and InCore/InWings/Remedial recovery checks to its existing tutorial testing handoff; plan 28's skipped-remedial scenario is insufficient for that new coverage. Keep P575/P578's snapshot/update boundaries and source-default wording intact.

## For Chase

These are recommendations for later handoff, not answers requested during this unattended synthesis.

| ID | Question and recommendation | Consequence |
|---|---|---|
| C1 | Retain ModernUO's inherited hatchling re-tame behavior or add ServUO's ordinary 10% skill loss on later successful tames? Recommend retain the working ModernUO behavior for now and explicitly record the deviation; the extra hatchling 55% cut must remain first-tame-only either way. | W5's cap regression and factual correction can proceed without a mechanics decision. A later source-style change needs narrow hatchling scope, same-owner and different-owner real-tame tests, saved-cap preservation and review of existing tame hooks. This is not an instruction to penalize every pet. |
| C2 | P452's board-matching and blessed-book Appraiser policies differ from P579's proposals. Recommend resolving both in the existing P452 brief before execution, with the intended eligibility and price paths stated together as A1 describes. | Policy-dependent P452 behavior waits for its owner to reconcile the brief. Its independent refresh/config safeguards need no new decision. |

P574 remains the existing collection for the earlier progression, housing, Tracking, warrant, Echo, proc, gate, townsfolk and butte questions. Its recommendations remain proposals and its reconciliation of settled answers remains binding evidence for avoiding repeated questions. P575's request to choose the P436 visual direction and P481's later preview choice do not create new fix tasks. No second copy of P574's decision rows is needed here.

## Verification and limits

Lane tests: none. This task adds no executable test or gate, so no P586 red/green cycle applies. Drafted regressions and mutation instructions are future work, not test results. No server build, client session, gameplay reproduction, world save/load, actual taming, real recycling, boss kill, packet-render check, deployed-config inspection or live-account survey was run. Earlier reported tests are attributed history only. Source-confirmed mechanisms do not establish current world prevalence or player impact.

Only this report and [the wrapper work record](cc-P586-codex-findings-to-fix-drafts-6.md) are deliverables. Final scope, editorial checks, progress-reporter handling and stop-request checkpoints are recorded there. No code, guide, prompt, service or file under docs/ was changed; no Haven connection or deployment occurred.

## Input inventory

Available P573-P585 files read, relative to notes/:

```text
cc-P573-review-tutorial-fixes-p453.md
cc-P574-questions-for-chase-2.md
cc-P574-questions-for-chase-round-2-codex-review.md
cc-P574-questions-for-chase-round-2.md
cc-P575-weekend-summary-for-chase-codex-review.md
cc-P575-weekend-summary-for-chase.md
cc-P575-weekend-summary.md
cc-P576-playtest-plans-10-24b-codex-review.md
cc-P576-playtest-plans-10-24b.md
cc-P577-guide-tutorial-refresh.md
cc-P578-patch-notes-10-24b-codex-review.md
cc-P578-patch-notes-10-24b.md
cc-P578-patch-notes-2026-10-24b.md
cc-P579-design-requisitions-appraiser-numbers-codex-review.md
cc-P579-design-requisitions-appraiser-numbers.md
cc-P579-requisitions-appraiser-numbers.md
cc-P580-review-smith-commission-fixes-codex-review.md
cc-P580-review-smith-commission-fixes.md
cc-P581-review-death-hooks-codex-review.md
cc-P581-review-death-hooks.md
cc-P582-review-noted-by-system-2-codex-review.md
cc-P582-review-noted-by-system-2.md
cc-P583-review-eodon-fixes-codex-review.md
cc-P583-review-eodon-fixes.md
cc-P585-review-artificers-text-codex-review.md
cc-P585-review-artificers-text.md
```

P584 is explicitly pending, as described above. All available inputs have been reconciled, all six drafts and existing-owner additions are complete, and final editorial, catalog and scope checks passed as recorded in the work record. No P586 work remains.

P586 DONE
