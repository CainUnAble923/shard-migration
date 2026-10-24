# P572: review findings to fix-up drafts, round 5

October 24, 2026. Notes only. This report covers P554 through P563. It creates no queued prompts and authorizes no implementation or publication.

## Result

No new numbered repair draft is needed. P556 already owns P554's Hunter's Satchel defect and P555's deletion-event test gap. The later guides introduce no independently confirmed gameplay defect. Their editorial corrections belong to the queued P478 wiki catch-up. P563 is a design, so its questions appear under For Chase instead of becoming repair prompts.

The urgent existing work stays first: P556 U3 for satchel admission, P533 U4 for retained tutorial service offers, and P452 for requisition eligibility and refresh/configuration fixes. This ordering does not claim that every risk is a reproduced player exploit. P555's correct deletion guard needs coverage under P556 A2/P533 W2, not a gameplay change.

## Evidence and scope

Read AGENTS.md in both supplied work copies, the migration document index, direction decision, task list, all P554-P563 task notes and adjacent Codex reviews listed below, and P556's report and work record. Consulted P533's relevant draft sections, P429's Register/requisition ownership, P451's adjacent review, the P561 cross-check, and the current guide/wiki passages involved in the corrections.

Code HEAD and local main were `1020e36a42d31dde07612544ea2a6f9472911db8`. Notes HEAD and local main were `787040af9608dd55586d310ab338b0c0b7386244`. Both work copies started clean. These are local snapshots, not remote or deployed freshness claims. The code diff since the reviews' `1c9c5d8bbf9ab4d9a8dd288aace3afff549479dd` changes tutorial/account files, patches, tests, version and changelog; it does not change the satchel, level-gear, TutorialPetCare, requisition or wiki files cited here. Tutorial citations below use the current files where lines moved.

Pinned ModernUO is `d4531cd94b739613155225c234900de9f47d2c88`. Read its actual Container capacity, parent-walk and open-drop paths. The client pin file contains `3212623f63436be1c0f4e3b308b202b29597c026`; P563's client analysis is attributed design evidence, not independently repeated client verification by P572.

Paths beginning `C/` mean `server/customizations/` in the code work copy; `T/` means `server/tests/`; `W/` means `docker/wiki/content/pages/uo/`; `N/` means this notes directory. Confirmed means current source supports the mechanism. Coverage gap means a missing regression, not a broken implementation. Covered means an existing prompt or draft owns the work, not that it has shipped.

## Verdict table

| Input | Verdict and evidence | Disposition |
|---|---|---|
| P554 #1 | Confirmed by current source. HuntersSatchel restricts TryDropItem and OnDragDrop at C/HuntersSatchel.cs:134,155, but has no CheckHold or OnDragDropInto override. Pinned Container.cs:300 calls CheckHold then AddItem; its parent walk at :274 reaches C/LeagueRegister/LeagueConsolidation.cs:163, whose :178 discounts incoming item totals. Ordinary contents can receive the nested allowance. No new client reproduction. | Already P556 U3. Do not draft another satchel task. |
| P554 repair/deed, worn repair, fee and delivery checks | No additional finding in the requested P451 repair paths. The reviewed source files are unchanged since P554. | Keep P451 completed. Its separate populated-Field-Satchel return finding remains separate from Hunter's Satchel admission. |
| P555 #1 | Coverage gap only. C/LevelGear/ClusterFLevelGear.cs:464 still correctly requires Hits <= 0. T/Misc/LevelGearVerification.cs:223 onward covers real wild, controlled and summoned deaths, but not deleting a damaged living wild creature. | Already P556 A2, extending P533 W2. Preserve the guard and add the mutation-sensitive regression through that owner. |
| P556 | Its adjacent review reports no findings. Its report already carries both overlapping findings above, plus the other P544-P555 repair/design owners. | Retain its ownership. Do not reissue U1/U2/U3/W1/W2/D1 or its additions. |
| P557 | No new Register defect. Its old-page repair-scope discrepancy is corroborated, but P561 R2 provides the more current distinction between the stale notes draft and corrected code wiki. Loaded return, admission and UI-fit limits remain disclosed. | P478 editorial handoff below; P556 U3 for admission; P533 W22 for Register paging/rank/reset. Client fit remains unverified. |
| P558 | No new requisition defect. The four changing-soon items are existing P422/P452 findings. C/Requisitions/RequisitionItems.cs:316 still refuses blessed items and RequisitionSystem.cs:127 still compares days for equality. | Keep P452 ownership. P478 must retain the warnings until actual changes are verified. Accepted Lead/standing rules are not questions to reopen. |
| P559 | No new independently established defect. The retained vet offer still lacks vet proximity validation at C/Tutorial/TutorialPetCare.cs:136, already covered by P533 U4. The guide's availability and unconditional town-vet wording need editorial correction. | P533 U4 for service validation; P478 for P561 F1-F4. An elixir's lack of an explicit ControlMaster check alone does not establish an unintended ownership rule. No new elixir repair draft. |
| P560 | Planned player guide exists at N/wiki-drafts/town-houses.md. It preserves native rentals/sublets, guarded towns, the account house limit and the inn/hall exclusions. No new repair finding. | P478 for integration; P556 D1 for the already identified housing design revision. Do not draft another player guide or housing implementation. |
| P561 | Its cross-check supplies editorial corrections, plus corroboration of existing launcher, requisition, satchel and housing findings. Its statements that no Town Houses player draft exists are now stale: P560's draft is present. | Map every labeled row below; route editorial work to P478 and retain existing code/design owners. |
| P562 | No new finding in its adjacent review. Glossary terms distinguish planned systems from implemented defaults. Repeated progress dry-run writes are an existing tool defect. | Keep the updated glossary as P478 input. P533 W24 owns progress.py; no duplicate helper-fix draft. Quest-marker integration and start-area design retain their existing owners. |
| P563 | Design only; adjacent review reports no findings. Proposed tuning, floor volumes, protocol and map overlays are not implemented guarantees. | Questions C1-C7 below. No repair or builder prompt drafted. |

Every adjacent P554-P563 `-codex-review.md` says no findings in the reviewed notes change. P554 and P555's substantive implementation findings are in their main review notes, not in those adjacent reviews.

## Existing ownership and deduplication

Searched Markdown prompts recursively in `D:/UO/cc-prompts/queue`, `waiting`, `completed`, `claimed`, `merging` and `held`, including nested lane folders. Read the relevant P476, P478, P556, P554-P563 and P563 design briefs, and compared P533/P556's actual report sections. No prompt files were changed.

- P556 is completed as a synthesis task. Its U3 is an unnumbered repair draft, not a completed satchel fix. Its A2 explicitly extends P533 W2 with P555's deletion regression. Those are the existing draft owners even though their parent synthesis prompts are completed.
- P478 is queued. Its work item 1 requires every file in notes/wiki-drafts, item 3 merges drafts into the right existing pages, item 5 retains test-shard availability limits, and item 8 records open questions. The correction checklist below is input to that existing work, not a competing wiki prompt.
- P452 is present under waiting, but the current local file is zero bytes. Its full current instructions could not be reread. P429 U2, P558's detailed P452 map and P561 Q1 establish the existing intended ownership; the empty file is not evidence that the fix is finished or abandoned. The overseer should recover/check its authoritative brief before execution rather than issue a second requisition task here. Its current precise wording and execution state remain unverified.
- P451 and P427 are completed implementations. P554/P555 are reviews of their remaining behavior, not permission to redo their original fixes. P451's adjacent review separately owns the evidence for loaded Field Satchel reinsertion; this batch does not rediscover or redraft that excluded finding.
- P533 U4 already specifies local, living-owner vet confirmation, exact fee/no-loss refusal and safe elixir purchase delivery. P559 adds no new service owner. P533 W24 already specifies a truly read-only progress dry run.
- P556 U2 owns launcher check/promotion/deadline/progress and real Play-stub coverage. P561 L1/L2 do not justify another launcher task. P556 D1 owns housing design corrections; P560's guide does not approve those proposed answers.
- P562's planned quest-marker entry is not a new implementation request. P520 is in merging as the quest-marker continuation, and P481 remains queued for the new start-area design. Neither is replaced here.

Prompt-catalog SHA-256 at the deduplication pass: `5ee609c394fe57f267d09b27018777889fda38c96ea4c39f46500e9727e3034c`. Method: in the folder order above, sort Markdown paths recursively within each folder using Python WindowsPath ordering, concatenate each relative POSIX path, one space and its lowercase content SHA-256, joined by LF without a final LF, then hash that UTF-8 text. This records the inspected catalog without treating a keyword hit count as coverage.

Final catalog SHA-256 was `71e4d299ae7c377011faf74f6bc987ac64ea8bff4c5bea0f2306c3a581b8aa73`. The only change was the unchanged P571 butte/deed design prompt moving from merging to completed. Read its full brief and the prompt repo's move history; restoring that path in memory reproduces the initial fingerprint exactly. It adds no repair ownership conflict. Both work-copy HEADs remained unchanged.

## New drafts and additions

There are no new numbered drafts. The existing urgent repairs above retain their scopes and red-first/build requirements. Use the following concrete addendum when the overseer hands off P478; it creates no second publishing or implementation task.

### A1. P478: incorporate P561's corrections and the completed P560/P562 inputs

Read N/wiki-drafts/cross-check-2026-10-24b.md beside the actual current implementation and player drafts. Apply the checklist below to P478's existing page conversion/merge work. Update affected Markdown prose if needed to prevent contradictory inputs, and record the chosen canonical page in P478's output table. Do not edit historical review notes to make their snapshot claims appear current.

| P561 row | Required treatment in P478 |
|---|---|
| M1 | Preserve the new mining guide's source defaults: 100 base Mining to read the stone book, effective skill for quota eligibility, actual Iron/Dull Copper quota definitions and saved legacy exceptions. Buying the Compact book does not itself require GM Mining. Do not invent quotas for every metal. |
| M2 | Correct W/professions/mining.txt:57,59,66 and W/guilds/miners_compact.txt:68,72. Replace planned book/gate/quota labels and blanket material-delivery wording with implemented quotas and the legacy exception. Describe enabling ore and stone together; granite is an occasional result. |
| C1 | Preserve bundle redemption, post-acceptance point progress and separate spendable balance. Keep first-look compatibility and replacement-bag caveats while their existing repair owners remain open. Bag corpse actions and member-only commands have different access rules. |
| C2 | Correct W/systems/clean_up_britannia.txt:28 and W/guilds/custodians.txt:37. New bundles are retired; old bundles can be redeemed. Civic Contracts use earned-point progress rather than consuming bundles. Keep package-dependent menu-label and availability qualifications. |
| L1 | In N/wiki-drafts/launcher-help.md, replace the unmeasured few-seconds assertion with: "The launcher shows the current step and elapsed time. Preparation time depends on your computer and the files that need rebuilding." Keep the default one-minute rebuild wait distinct from total launch time and attribute designed fallback behavior honestly. |
| L2 | Retain the close-stuck-launcher instruction, skip-art shortcut, advice to decline an update during recovery, and actual log paths. Skip-art bypasses art preparation only. Do not claim a downloaded package, SmartScreen screen or updater flow was tested by this prose task. |
| R1 | Preserve P451's equipped-only free Blaze repair, the Remote Repair Deed's worn/backpack/bank scope, defaults, and current combined-turn-in behavior. Ask each time currently follows the banked-Seals branch in the combined action. |
| R2 | Fix N/wiki-drafts/pages/uo/systems/league_register.txt's old Blaze scope, deed equivalence, satchel placement and family rules. W/systems/league_register.txt already corrects Blaze and has no deed/Blaze equivalence; do not claim otherwise. Make direct-backpack discount, sequential upgrades and safe delivery explicit, preserving the loaded-return caveat until repaired. |
| Q1 | Keep P452 changing-soon warnings until the merged behavior is checked. Do not promise ordinary blessed-book turn-ins now or blessed-book Appraiser sales after a turn-in fix. Keep exceptional-craft eligibility, backward-day refresh and invalid-config publication under P452. |
| Q2 | Preserve accepted rules: lower of guild rank/League gate, live Leads survive refresh, immediate requisition standing for nonmembers, qualifying area/group/Fame kills, the guarantee by qualifying kill 40 since the last drop, and repeat drops until expiry or turn-in. |
| Q3 | Correct W/systems/requisitions.txt's tier table: total property count is separate from the requested property's intensity. Include Slayer/AnyMagic exceptions, the current blessed-book caveat and the exact 40th-qualifying-kill wording. Appraiser eligibility does not require that no request wants the item. NPC posts/settings are source defaults, not verified world placement. |
| F1 | Add an explicit test-world qualifier to N/wiki-drafts/first-companion.md. Current C/Tutorial/ClusterFTutorial.cs:51 gates enablement on testCenter.enable; TutorialCorePlacement.cs:68 refuses seeding elsewhere. This is stronger than merely saying placement was not checked. |
| F2 | Replace the unconditional town tutorial-vet sentence. C/Tutorial/TutorialCorePlacement.cs:82 adds that vet only when FindTownVet at :120 finds none; any existing stock Veterinarian can suppress it. Suggested text: "Tobin is the tutorial farm's resurrection vet. A tutorial vet is added near New Haven's stables only when the town has no existing vet. Use Tobin if a town vet offers no resurrection." Retain actual-placement uncertainty. |
| F3 | Keep current starter choices, bonding, slot, fees, corpse wait and health details. Add: "If the elixir says the pet cannot be resurrected there, move its ghost to a clear nearby tile and try again." C/Items/Consumables/ElixirOfRebirth.cs:70 requires CanFit. |
| F4 | In W/drafts/companions.txt:48, replace the vague NPC healer promise with the tutorial-vet and elixir routes, distinct from player Veterinary and stock NPC vets. Reconcile the older Markdown companion guide with P480/P559. The defined dog capstone is great grey wolf or windrunner (C/Mobiles/Evo/EvoPetData.cs:106); later forms still depend on unbuilt progression and are not unlocked by this editorial change. |
| H1 | Use the already completed N/wiki-drafts/town-houses.md from P560. P561's absence statements describe an older snapshot. Preserve planned status, native rentals/sublets, guard coverage as a requirement, the account's one-house rule and inn/hall exclusions. Do not write another Town Houses guide or imply approved sale/room exceptions. |
| H2 | Retain P550's region, bounds, permissions, payment, downtime, door/decay and recovery concerns under P556 D1. Do not turn a proposed solution or lossless-recovery promise into delivered player instructions. No housing builder prompt is authorized by this checklist. |

Use the updated P562 glossary as the current terminology input. Its planned quest markers, Town Houses, new facet and island must remain planned. Do not restore superseded League questions, hidden-achievement spoilers, later story spoilers, or the old Remote Repair Deed comparison.

P478 acceptance: its output table names the affected page for each correction above, explains any intentional no-change decision with current source, and retains explicit unresolved availability/package/client checks. Recheck after any owning code fix merges so temporary warnings do not become permanent misinformation. Keep the wiki work local and unpublished; no Haven access or code changes are part of this addendum. No product test is needed for prose; perform source, links, DokuWiki rendering/syntax, whitespace and size checks appropriate to P478's actual deliverables.

## For Chase: P563 design questions

These are P563's seven questions and recommended answers, not answers obtained by P572. Listing them completes this task; no Ask-Chase exchange or decision is needed now. Chase's existing direction already requires many refreshed contacts on the mini map. A smaller release would require an explicit scope change.

| ID | P563 question | Recommended answer |
|---|---|---|
| C1 | Build the full moving radar or accept a smaller release? | Choose C, refreshed radar plus companion world-map overlay and fallback. A is the first internal text/selection milestone, not feature completion. P563 estimates A at 2 prompts, B at 3-4 total and C at 5-6 total; these are unmeasured cumulative alternatives, not additive budgets. A snapshot-only B needs explicit acceptance of reduced scope. |
| C2 | Where should access start and how strong should it become? | Use trained Base Tracking: 90/100/120/150/200 give creature radii 18/24/28/34/44 tiles and lifetimes 6/6/6/8/10 seconds. Recommend 15 stamina, a one-second cancelable focus and a fixed 30-second cooldown, no mana or Ping skill gain. Gear does not buy unlocks. Tune after playtesting without lifting ordinary Tracking's existing range clamp. |
| C3 | Should Ping find players? | Yes from 120 Base, only living visible players within 12 tiles and current line of sight, with a watched warning and real notoriety flags. Apply the same anti-proxy restrictions to nonparty player-owned pets, including hidden-owner exclusion. If Chase chooses creature-only sensing, remove the player branch deliberately; retain the other privacy restrictions. |
| C4 | Should 150 or 200 Tracking defeat Hiding? | No precise hidden contacts at any Ping tier. Hiding, hidden Stealth and magical invisibility beat Ping. Keep the separately approved 150 historical-footstep reward for its own approximate-trail design; Detect Hidden remains the reveal skill. |
| C5 | Should walls block it, and which dungeons launch first? | Allow through-wall PvE sensing only within authored, unambiguous same-floor volumes. Select one launch dungeon and an outdoor/vertical-structure fixture when issuing the builder work; P563 does not choose a dungeon name. Reject unmapped or ambiguous dungeon floors without stamina or cooldown cost rather than scan every floor. Expand coverage separately. |
| C6 | Does the Rangers' League own the unlock? | Let the existing League teacher explain/practice it, but unlock automatically for any character at 90 Base. No membership, rank, currency or saved unlock gate in the first version. |
| C7 | Does Ping grant extra information or party sharing? | Personal results with relative creature threat only. No exact HP, resist, loot or player-strength disclosures and no automatic party broadcast. Keep ordinary Tracking health/con, double variant range and historical footsteps as separate approved rewards, not silently removed or treated as implemented by Ping. |

Before issuing any later builder prompts, retain P563's common requirements: identical server filtering for counts and contacts; fixed pulse origin with refreshed eligibility; private-interior/instance/staff exclusions; guarded quarry selection and arrow lifetime; an independently acknowledged Ping capability; bounded atomic snapshots with short expiry; no fake mobiles or persistent marker files; fog and ordinary-dot handling; and actual maximum-radius/moving-contact client acceptance. Its proposed floor resolver, exact protocol allocation, dense-spawn ceiling, runtime hostility classification and visual fit still require implementation evidence. They are constraints for future work, not newly discovered defects or extra approved tasks.

## Verification and limits

No lane tests apply. No new test or gate was added, so no failing/passing test cycle applies. Current source corroboration is not a new gameplay reproduction. No server/client build, runtime transaction, pet resurrection, launcher timing probe, package download, floor survey, save/reload or client playthrough was performed. Active settings, deployment, player harm and published wiki/package state remain unverified. Prior tasks' test/build results are attributed history only.

No code, wiki draft, prompt file, configuration or file under docs/ changed. No Haven connection, service/account/save action, deployment, commit, merge, push or branch switch occurred. Only this report and its wrapper work record are deliverables. Final editorial, progress-reporter and scope results are recorded in [the work record](cc-P572-codex-findings-to-fix-drafts-5.md).

## Input file inventory

All paths below are in notes/. Companion wrapper notes are retained as separate artifacts rather than counted as additional findings.

```text
cc-P554-review-league-register-fixes-codex-review.md
cc-P554-review-league-register-fixes.md
cc-P555-review-crystal-p379-fixes-codex-review.md
cc-P555-review-crystal-p379-fixes.md
cc-P556-codex-findings-to-fix-drafts-4-codex-review.md
cc-P556-codex-findings-to-fix-drafts-4.md
cc-P556-codex-findings-to-fixes-4.md
cc-P557-guide-league-register-codex-review.md
cc-P557-guide-league-register.md
cc-P558-guide-requisitions-and-leads-codex-review.md
cc-P558-guide-requisitions-and-leads.md
cc-P558-guide-requisitions.md
cc-P559-guide-first-companion.md
cc-P559-guide-pets-and-companions-new-player-codex-review.md
cc-P559-guide-pets-and-companions-new-player.md
cc-P560-guide-town-houses-planned-codex-review.md
cc-P560-guide-town-houses-planned.md
cc-P560-guide-town-houses.md
cc-P561-wiki-cross-check-3.md
cc-P561-wiki-drafts-cross-check-3-codex-review.md
cc-P561-wiki-drafts-cross-check-3.md
cc-P562-glossary-update-2-codex-review.md
cc-P562-glossary-update-2.md
cc-P563-tracking-ping-design-codex-review.md
cc-P563-tracking-ping-design.md
```

All requested work and final editorial/scope checks are complete. No P572 work remains.

P572 DONE
