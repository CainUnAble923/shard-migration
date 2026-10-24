# P556: review findings to fix-up drafts, round 4

October 24, 2026. Notes only. These are unnumbered drafts for the overseer to issue, not queued prompts or permission to change a running service.

## Scope and evidence

Read both work-copy AGENTS.md files, docs/README.md, the direction decision, task list, P533's report and its adjacent review, and the P544-P555 files listed below. Checked the relevant canonical implementations and test fixtures against local main. Code HEAD and main were `1c9c5d8bbf9ab4d9a8dd288aace3afff549479dd`; notes HEAD and main were `7529d1c62e8da4da4ea95e1d63f564e64acc32f6`. Both work copies started clean. No fetch or branch change was made.

Pinned ModernUO was read at `d4531cd94b739613155225c234900de9f47d2c88`, matching docker/uo/Dockerfile. The client pin is `3212623f63436be1c0f4e3b308b202b29597c026`. Read its cached-selection code in the existing checkout rooted at `D:/UO/golems/Iron/tazuo-p412/src`, whose HEAD matches that pin. This was read only. Code paths below are relative to the code work copy. `C/` means server/customizations, `T/` server/tests, `U/` the pinned Projects/UOContent tree, and `S/` pinned Projects/Server. `N/` means this notes directory.

Confirmed means the current source supports the failure mechanism. It does not mean a new runtime reproduction. Risk means a possible failure or unsafe shared method with player reachability or live conditions still unverified. Test gap means coverage is missing, not that current behavior is wrong. Design blocker refers to the proposed feature, which is not implemented. Covered means an existing prompt or draft retains ownership, not that its fix is in main.

## Verdict table

P550 has named sections rather than numbered findings. The D labels below map to its four settled-call rows, six numbered corrections, and seven money/timing risk paragraphs, in their original order. Its remaining-question table maps as follows: question 1 to C4; 2 to C5; 3 and 4 to C6; 5 to C7; 6 and 7 to C8; 8 to C11; 9 to C10; and 10 to C9/C12. C13 carries its separate vendor/barkeeper risk.

| Finding | Verdict and effect | Current evidence | Owner |
|---|---|---|---|
| P544 #1 | Confirmed: the fruit trunk can fail both harvest and foliage filters, leaving the trunk visible or the stump at the leaf elevation. Map examples are P544's observations, not remeasured here. | C/ClusterFLumberStumps.cs:122,135-136 | W1 |
| P544 #2 | Confirmed: the server collects unrelated trunks inside its height window, and the client identity omits Z. Repeated graphics can hide together. | Same file:132-142; client/patches/0006-exhausted-trees.patch:124-155 | W1 |
| P544 #3 | Confirmed by source: a stationary cursor can retain a hidden static through cached selection. Actual rendered behavior was not retested. | Client GameScene.cs:761,780 and GameSceneDrawingSorting.cs:700 in the pinned client checkout; patch only guards StaticView | W1 |
| P544 #4 | Scope risk: resolving only one X,Y does not cover multipart jungle trees. P412 explicitly requested same-tile matching, so this is not an automatic mandate to expand the feature. | C/ClusterFLumberStumps.cs:100; P544's multipart records and pinned client's IsFoliageUnion | C3; W1 covers an explicit scope fixture |
| P545, no new finding | No new entrance repair to draft. Its source checks and historical walk records are not a new pet/mount runtime proof. | N/cc-P545-review-rootdeep-anthill-entrance.md, Evidence and limits | Existing entrance/map owners only |
| P546 #1 | Confirmed economic scenario: discounted 5-gold sandals cost 4 each; 25 pairs cost 100, yield 50 spendable points and refund 100 through Refuse Collection. No positive net gold or live active-town condition was proved. | C/ClusterFWorkOrderSystem.cs:2676,2682; C/Services/PointsSystems/CleanUpBritanniaData.cs:461; U/Mobiles/Vendors/GenericBuy.cs:79; BaseVendor.cs:1353-1361; U/Engines/Factions/Gumps/FinanceGump.cs:10-13 | U1; C1 for tuning choice |
| P546 #2 | Confirmed ordering, compatibility risk: bundle redemption before the old contract's first progress lookup loses those earnings for that contract. First-look initialization was intentional in P414, so changing it needs an explicit compatibility choice. | C/ClusterFWorkOrderSystem.cs:523-527; C/ClusterFCustodianSystem.cs:625-634; T/Services/CivicContractPointsVerification.cs:246-249 | U1; C2 |
| P546 #3 | Test gap: staggered/partial overlaps, reverse completion, three open contracts and persistence after a claim. No overlap accounting bug established. | C/ClusterFWorkOrderSystem.cs:535-567; T/Services/CivicContractPointsVerification.cs:142-159 | U1, coverage only unless a failure is found |
| P547 #1 | Confirmed eligibility gap: bonded pet corpses pass the common predicate. The zero pet base prevents that award, not corpse/content deletion. This does not delete the ghost pet or prevent resurrection. | C/ClusterFCustodianSystem.cs:133-162; U/Items/Misc/Corpses/Corpse.cs:619,631; U/Mobiles/BaseCreature.cs:3482-3495 | A1, extend P476 U2 |
| P547 #2 | Confirmed: the nearby warning callback scans again at the player's new position. Its approval can destroy a different set of corpses and contents. | C/ClusterFCustodianSystem.cs:436,450-461 | A1, extend P476 U2 |
| P547 #3 | Confirmed missing acceptance check, risk: neither warning retains the required bag. Banking, transferring or deleting it can leave the pending action usable. | C/TrashBag.cs:153,192-208; C/ClusterFCustodianSystem.cs:383-392,457-461 | A1, extend P476 U2 |
| P548 #1 | Risk: the shared TurnIn method can pay the same completed quota twice when called directly. Current ledger/Register callers select active entries, so a player replay exploit is unproved. | C/GuildContractLedgerGump.cs:541-554,562-602; C/LeagueRegister/LeagueRegister.cs:283 | W2 |
| P548 #2 | Test gap only: button 82 needs a balance-change case. Current code correctly reads the held vouchers again. | C/MinersCompactLiaisonGump.cs:1068-1083; T/Services/StoneMiningGateVerification.cs:405-437 | W2 |
| P548 #3 | Test gap: the old Ore Refinement Run's 150-iron completion and fresh Dull Copper payout are not exercised. No wrong payout was found. | T/Services/StoneMiningGateVerification.cs:315-350; C/ClusterFWorkOrderSystem.cs, mining definitions and legacy requirement handling | W2 |
| P549 #1 | Confirmed: failed CheckOnly parts can reach list deletion/replacement and return Fresh=True. P549's exclusive-stamp-lock probe was read, not rerun. | player-package/payload/app/Build-UoOverrides.ps1:879-929; Overrides-Launch.ps1:116-118 | U2 |
| P549 #2 | Risk with a demonstrated race window in P549: concurrent Play calls can clear shared staging and start two writers before PID publication. A half-built set reaching TazUO remains unverified. | player-package/payload/app/Overrides-Launch.ps1:113,126-137 | U2 |
| P549 #3 | Confirmed: both initial promotion and post-build swap retries sit outside the timed wait. P549 measured 4.82 seconds with a one-second limit. | Same file:69-76,110,123,165 | U2 |
| P549 #4 | Confirmed missing progress coverage, risk: map parsing/stamping and animation hashes occur before the relevant Start-Step. Slow operations can show the previous step. | player-package/payload/app/Apply-MapOps.ps1:130,162,174; Build-UoOverrides.ps1:425,434 | U2 |
| P549 #5 | Test gap: helper return values do not establish actual game launch, and existing Play sandboxes bypass preparation or disable Play. | player-package/tests/Launch-Overrides.Tests.ps1:70,117,142,230; Launch-Settings.Tests.ps1:430; P549 evidence | U2 |
| P550 D01, native rentals/sublets | Settled scope, not a defect: native leases and sublets stay approved. A rent-first release cannot silently remove sublets. | Chase's October 22 decisions:24-25; N/cc-P409-town-houses-design.md | D1 |
| P550 D02, guarded towns | Design blocker: a missing-parent warning does not fulfill working guard coverage. | N/cc-P409-town-houses-design.md:281-283; U/Regions/GuardedRegion.cs; S/Regions/Region.cs parent lookup | D1, also D14 |
| P550 D03, account house limit | Principal tenancy fits the stock owner table. A room-renter exception to the account's one-house limit is unresolved policy. | U/Multis/Houses/BaseHouse.cs:76-83,3541-3556; N/cc-P409-town-houses-design.md:111-113,325 | D1; C4 |
| P550 D04, inns/halls | Confirmed design contradiction: the inn example conflicts with the exclusion; reserved halls need explicit exclusion too. | N/cc-P409-town-houses-design.md:190-191; Chase's October 22 decisions:25 | D1; settled, do not ask again |
| P550 D05, correction 1 | Design blocker: subclass UpdateRegion cannot assign BaseHouse's private region field. A separate hidden property/region disconnects stock consumers and cleanup. | U/Multis/Houses/BaseHouse.cs:40,439,1645-1658 | D1 |
| P550 D06, correction 2 | Design blocker inferred from source: Resize on an empty multi leaves zero Min/Max, so footprint lookup can miss other sectors. Not a reproduced server failure. | S/Client/MultiData.cs:637-716; S/Maps/Map.cs:775-779; U/Multis/Houses/BaseHouse.cs:1434-1447 | D1 |
| P550 D07, correction 3 | Design blocker: doors/speech alone do not supply room entry, login, lockdown, secure or container rights. Stock nonvirtual checks cannot simply be overridden as proposed. | U/Regions/HouseRegion.cs:33-41,81-185; U/Multis/Houses/BaseHouse.cs:2157-2164,2394-2543,3563-3665 | D1; C6 |
| P550 D08, correction 4 | Design blocker: stock lockdown/secure lists do not record the depositor. Room location alone cannot safely assign belongings; stock addon packing can spill contents. | U/Multis/Houses/BaseHouse.cs:55-57,853-996,1247-1267,3920-3941; U/Items/Addons/BaseAddon.cs:198-202 | D1; C6,C9,C11 |
| P550 D09, correction 5 | Design blocker: permanent site state must survive disposable sign/house deletion; vacant house doors with no house deny access. | U/Multis/Houses/HouseSign.cs:12-23,47-54; U/Multis/Houses/BaseHouse.cs:3386-3397; U/Items/Construction/Doors/HouseDoors.cs:99-105,138-146 | D1 |
| P550 D10, correction 6 | Design blocker: ordinary decay/account deletion can bypass recovery; disabling decay alone leaves abandonment unresolved. | U/Multis/Houses/BaseHouse.cs:110-151,627-673,1303,3400-3455; U/Accounting/Account.cs:331-349 | D1; C10 |
| P550 D11, escrow order | Design loss risk: zero-before-deposit erases debt when a bank refuses or accepts only part. Durable pending payment records are required. | N/cc-P409-town-houses-design.md:247; U/Mobiles/Townfolk/Banker.cs:209-268,316-367 | D1 |
| P550 D12, gold equation | Confirmed design assertion error: unchanged total spendable gold ignores intended rent/fee sinks. Include credit, escrow, pending payments and recorded sinks once each. | N/cc-P409-town-houses-design.md:247 and L2 | D1 |
| P550 D13, downtime | Design blocker: wall-clock dates plus skipping the first sweep do not implement uptime-only grace/rent or prevent restart extension. | N/cc-P409-town-houses-design.md:271-285, L2 | D1; C5 |
| P550 D14, guard recovery | Design safety risk: sign-tile lookup or a financial hold alone cannot guarantee guards across the occupied 3D area. Exclude self-parenting on rebuild. | Same design:281-283; S/Regions/Region.cs:458-475; U/Regions/GuardedRegion.cs:199-233 | D1 |
| P550 D15, state enforcement | Design gap: grace restrictions, stale offers, edited terms, entitlement/payment and staff assignment need acceptance-time enforcement, including storage growth. | N/cc-P409-town-houses-design.md, lease/grace and L1-L3 descriptions; P550 Money section | D1; C7,C8 |
| P550 D16, recovery crates | Design exploit risk: unconditional over-capacity bank delivery could become repeatable remote storage. No implementation or live exploit exists. | N/cc-P409-town-houses-design.md:86-94, open question 5; P550 recovery-crate paragraph | D1; C9 |
| P550 D17, vendors | Policy/design boundary: no placement entry currently implies zero vendor capacity, but make that intentional; barkeep capacity is separate. | U/Multis/Houses/BaseHouse.cs:774-791; U/Items/Misc/PlayerVendorDeed.cs:42-61 | D1; C13 |
| P551, guide and sources | No new defect. Iron Beetle credit, live stock/prices, and runtime are explicitly unverified. P548's gaps keep their existing rows above. | N/cc-P551-guide-mining.md; N/wiki-drafts/mining-changes.md | P561 publication cross-check; W2 for P548 |
| P552, guide and sources | No new defect. The first-look contract instruction and replacement-bag warning describe current limitations. Update after owning fixes, not a second guide task. | N/cc-P552-guide-clean-up-britannia-changes.md; N/wiki-drafts/clean-up-britannia-changes.md | P561; U1 and P476 U2 supply changed behavior |
| P553, guide and sources | No new defect. It correctly qualifies total launch time and tells users to close a stuck launcher before retrying. | N/cc-P553-guide-launcher.md; N/wiki-drafts/launcher-help.md | P561; U2 supplies changed behavior |
| P554 #1 | Confirmed: the open Hunter's Satchel drop route lacks its resource filter; nested ordinary items can receive the Field Satchel item-count allowance. Client reproduction unverified. | C/HuntersSatchel.cs:134-174; C/LeagueRegister/LeagueConsolidation.cs:163-185; S/Items/Container.cs:274,300-308 | U3 |
| P555 #1 | Test gap only: current positive-hits deletion guard is correct. No real deletion test protects it against removal. P427's five reported fixes are present. | C/LevelGear/ClusterFLevelGear.cs:461-478; T/Misc/LevelGearVerification.cs:223-252 | A2, extend P533 W2 |

The adjacent P544-P555 Codex reviews all report no findings in the notes themselves. They are not twelve additional implementation reviews or new defects.

## Existing ownership and deduplication

Searched Markdown prompts recursively in `D:/UO/cc-prompts/queue`, `waiting`, `completed`, `claimed`, `merging`, and `held`, including the nested claimed lane folders. Read relevant implementation, fix-up, review and guide prompts, and compared the P429, P476, P477 and P533 draft scopes. The catalog fingerprint is recorded below. Completed review prompts are evidence collection, not an implementation of their findings.

- P476 U2 already owns the Clean Up barrel, bag-replacement preservation, access/LOS/protected-content sweep and store-confirm fixes. A1 extends that draft. It creates no second cleanup prompt. Its Sandals crafting-value policy remains a different question from the discounted vendor loop in P546.
- P412 completed the original stump/client work and the P429 W5 polearm addition. W1 repairs the newly reviewed component identity and cached-selection paths. It does not draft P412 again. Retain P412's prior lower-leaf regression as adjacent coverage rather than a separate task.
- P411 completed the launcher implementation. P543 restored its notes after the merge problem; it is not a new launcher fix. P533 has no launcher-repair draft and explicitly preserves P411's always-start policy. U2 is a follow-up for P549's defects. Earlier unresolved P411 review issues are correctness constraints of the same repair, not extra numbered drafts here.
- P414-P416 are completed implementations. U1 and W2 repair their new findings; they do not restore bundles, remove quotas or redesign gathering. P417's proposed gathering redesign is not current behavior.
- P451 completed the repairs, fee handling and delivery changes. P554 checked those paths without a new defect. U3 is restricted to the Hunter's Satchel admission path. The separate populated Field Satchel capacity finding in P451's adjacent review is not counted or redrafted here. P533 W22 retains Register paging/rank/reset ownership, and P178 retains the wider action catalog.
- P427 completed the five Crystal/P379 fixes. A2 adds only P555's test to P533 W2. P457's separate achievement work is not part of it.
- P409/P542 own the original Town Houses design and its restoration. Neither implements P550's corrections. D1 is one notes-only revision before L0-L5 implementation, not a duplicate housing build. P560 already owns the planned player page, P561 the cross-check, and P562 the glossary. No new guide, publication or glossary prompt is drafted.
- P557 owns the League Register player guide. Its unchanged prompt moved from claimed/Verite to merging during final checking. It is documentation work, not a Hunter's Satchel admission repair, so it does not duplicate U3.
- P545 found nothing new. P533 U7 and C16 retain server-overlay and client-map safety ownership, and P476 U4 retains Vault recovery. Do not reopen entrance geometry or claim unperformed pet/mount travel as a pass.
- P533 W24 already owns progress.py's dry-run write defect. P544-P555 repeat that observation; no new helper-fix draft is needed.
- P533's own adjacent review identifies its duplicated tutorial island-gate/core-window scopes. Those remain P477 T1/T3, not new P556 work. No tutorial draft is copied into this round.

## Urgent drafts and additions

### A1. Extend P476 U2 with bonded-pet protection and exact corpse approvals

This is an addition to `N/cc-P476-crystal-codex-findings-round-2.md`, U2. Attach it before that draft is issued, or carry it in the same repair's follow-up if implementation has begun. Keep the existing barrel, replacement bag, sweep access and store fixes in that owner.

1. Reject bonded pet corpses in the shared eligibility rule used by commands and both bag menu actions. Determine which persisted corpse/owner identity survives load; use a narrowly versioned field only if current identity is insufficient. Preserve the ghost pet and its resurrection path. A zero base award is not a deletion safeguard.
2. The nearby warning must retain the previewed corpse serials and source map. Acceptance can clear only approved corpses still in range and still permitted by current rights and shared safety rules. Do not rescan and silently add fresh, newly eligible or different-hunt corpses. If an expanded selection is offered, require a new preview/approval. A location or facet change must never turn the old confirmation into approval for another hunt.
3. Both warning paths retain the originating bag and recheck its existence, ownership and presence in that character's backpack on acceptance. Cancel/refusal deletes nothing, awards nothing and starts no successful-sweep cooldown. Replayed replies cannot pay again.
4. Exercise actual context-menu clicks, single targeting and WarningGump responses, not direct helper calls with `confirmed: true`. Red-first cases: empty and filled bonded corpses, expired rights, reload with a surviving pet/corpse; movement/facet change; new corpse while open; bag banked/transferred/deleted; cancel; ordinary authorized monster clearing and one award. Preserve normal single/batch ranges, cooldown and instanced-loot checks.
5. Keep P476 U2's existing build gate and notes. This adds P547 #1-#3 evidence; it does not repeat the older access/loot-rights findings or claim that pet resurrection is currently destroyed.

### U1. Civic Contracts cannot reimburse discounted vendor points for free

```text
# CC task P??: Civic Contract follow-up: final vendor prices, old baselines and overlap coverage
**Model:** Opus
**Touches:** server
**Agent:** Codex OK
**Summary:** P546 found a zero-net-cost point loop under faction discounts and an old-contract baseline ordering risk. This follows completed P414. P476 U2 separately owns barrel and corpse/bag safety.

1. Read P546 and P556 C1/C2 before choosing changed defaults. Reproduce the final transaction price through pinned vendor/tax/rounding behavior, including the 5-to-4-gold sandals case. Measure every supported lower-price path in the relevant vendor pricing flow rather than using fresh SBInfo list prices as final quotes. Publish the inspected vendor/item file list and the limiting rows.
2. Under C1's recommended policy, preserve contract gold rewards and ordinary Clean Up valuation, and raise only the affected Civic Contract point requirements enough that the cheapest reachable purchases still leave a positive net gold cost for the retained store points. Calculate the amounts from the measured minimum, with an explicit rounding margin. Do not change the broader crafted-Sandals valuation policy or consume spendable points. If source prices require a different correction, document the alternatives for Chase instead of silently tuning unrelated rewards.
3. Define the behavior of already accepted affected entries explicitly. Keep them finishable and avoid leaving the same repeatable loop through a legacy path; no retroactive debit or real-account compensation. Record any balance deviation for overseer promotion, without editing docs/.
4. Under C2's recommended compatibility policy, initialize null old civic baselines after the relevant point/contract data are available and before the first new award, including old-bundle redemption before opening the ledger. Preserve explicit saved baselines and avoid counting historical pre-upgrade earnings. Centralize the award boundary if that is the safe order; do not initialize against unloaded point totals. Keep bundle type and one-time redemption intact.
5. Red-first regressions: actual discounted purchase/dump/contract arithmetic; an old saved contract redeeming bundles before its first Active view; awards through the common path; reload with initialized baselines. Add staggered acceptance, partial overlap, reverse completion and three open contracts, followed by real turn-ins and reload after a claim. The overlap coverage is not a prior demonstrated bug: prove sensitivity with a temporary mutation if it already passes.
6. New tests must be seen failing before the correction or with an explicit temporary mutation for existing correct behavior, then passing after restoration. Run docker/uo/build.sh -t sl-modernuo:cc-P?? in an isolated test setup. Keep P414's gold rewards, retired-bundle rule and lifetime/spendable separation. Note changed guide statements for P561, update the owned wiki draft if appropriate, and do not publish it.
7. Done means the price evidence, saved-entry policy, regression/build results and limits are recorded in notes/cc-P??-civic-final-prices-and-baselines.md. No live tax changes, account edits or deployment. End P?? DONE.
```

C1/C2 are recommended scope choices, not approvals obtained by this notes task. Resolve them when issuing this draft; their answers do not block the independent safeguards.

### U2. Launcher checks preserve fallback and share one bounded preparation operation

```text
# CC task P??: launcher follow-up: read-only checks, one staging owner and bounded promotion
**Model:** Opus
**Touches:** client-package
**Agent:** Codex OK
**Summary:** Repair P549 #1-#5 after P411/P543. Honor P411: on timeout or failure, Play reaches the game with the last complete set or none on a first install.

1. Make every CheckOnly branch read-only for generated overrides and the current list. A failed part check must return an explicit unsuccessful/unknown result, never Fresh=True with a reduced or missing list. Cover outer exceptions too. A locked stamp, invalid input and an otherwise fresh set must leave existing list bytes/existence and generated assets unchanged. Do not publish a ready marker from a check.
2. Give each install one interprocess staging/promotion owner. Acquire it across discovery, generation allocation, child start/PID publication and promotion decisions; use distinct staging generations so a second Play cannot delete a live writer's files. Never promote a generation until its owner has exited successfully and its complete marker is valid. A contender must honor its remaining launch budget rather than wait indefinitely for the lock. Test stale ownership and owner termination without killing unrelated processes.
3. Start one deadline before lock acquisition, promotion and freshness work. Include swap retries and recovery in that budget; place potentially blocking checks under the bounded child mechanism. Preserve a recoverable last-good directory/list if the budget runs out during a rename. Restore or retain .old when live is missing, rather than deleting the only fallback on next launch. Keep promotion atomic from the game's perspective and leave no launched game reading a half-written set.
4. Begin named progress/timing steps before map patch reading/parsing/stamping and animation hashing, with map parser counts. Emit a durable active-step trace before work, plus its completion time. Verify progress during a forced slow map parse/hash as well as art.targets. Do not equate one step's count with overall completion.
5. Add real Play and updater-to-Play sandboxes using the actual override helper and a harmless local game stub recording launch time and arguments. Stub connection/update checks before any real network or game operation. Cover a good prior set, first install, a locked/failed check, short-limit locked promotion, concurrent Play calls and a timed-out updater handoff that does not wait again in Play. Assert fallback list bytes and the actual stub invocation, not only Invoke-UoOverrides's return.
6. Every new regression fails first against the current code, or through a documented temporary mutation for already-correct behavior, then passes. Run all PowerShell scripts/tests in powershell.exe 5.1. Run relevant override/launcher/map tests and the player-package build gates in an isolated setup. Do not run existing suites unmodified if their Play fixtures contact the shard. Do not publish a package or start a real client.
7. Keep test-shard routing, player settings and P411's fallback policy. P533 C16 separately owns missing-client-map policy; no new client hard stop here. Earlier P411 adjacent-review defects in bounded checks, active traces, backup recovery and double updater waits are constraints of this repair, not separate replacement launcher tasks.
8. Done means an actual recorded game-stub start under each timeout path, no concurrent staging corruption or check-only mutation, passing package gates and notes/cc-P??-launcher-checks-and-promotion.md with exact timings/limits. Update changed player guidance or hand it to P561. End P?? DONE.
```

### U3. A nested Hunter's Satchel admits only its intended resources

```text
# CC task P??: Hunter's Satchel follow-up: enforce admission on open-container and parent checks
**Model:** Opus
**Touches:** server
**Agent:** Codex OK
**Summary:** P554 found that OnDragDropInto bypasses the Hunter's Satchel filters and admits ordinary items under the Field Satchel item-count allowance. P451's repair/deed/fee/delivery fixes are already present.

1. Enforce the shared Accepts policy from CheckHold, including checks reached by a parent walk from any existing child container. Preserve intended hides/leather conversion, resource types, weight reduction and tier capacity. Ensure open-container drops cannot skip the conversion or create duplicate resource stacks.
2. Through actual OnDragDropInto while the Hunter's Satchel is nested in a Field Satchel in the owner's backpack, reject gold, weapons and bags; accept intended resources. Seed an existing child bag using test setup only and verify new ordinary contents are refused through the parent walk. Test the same admission policy outside the Field Satchel.
3. Watch the regressions fail first, then pass. On refusal, item serial, location, amount, parent, backpack item/weight totals and currency remain unchanged. Successful legal resources retain the designed Field Satchel allowance and normal weight checks. No confiscation or deletion of existing illegal contents is authorized; allow safe removal and record any repair policy needed.
4. Run docker/uo/build.sh -t sl-modernuo:cc-P?? with the relevant satchel/Register regressions. Do not rework paging/reset (P533 W22), the broader action catalog (P178), or the distinct populated-Field-Satchel reinsertion finding. Coordinate shared capacity code with that finding's owner.
5. Done means the resource policy holds on every tested admission route without disabling legitimate nested resources. Notes: notes/cc-P??-hunters-satchel-admission.md, including unchanged P451 repair/fee/delivery behavior and runtime limits. End P?? DONE.
```

## Other drafts and additions

### W1. Exhausted-tree identity includes the actual components and elevations

```text
# CC task P??: chopped-tree follow-up: fruit trunks, stacked components and cached selection
**Model:** Opus
**Touches:** server, client, client-package
**Agent:** Codex OK
**Summary:** P544 #1-#3 remain after P412. Fix tree component identity and the stationary-cursor selection path. P544 #4's multipart expansion is a separate scope choice in P556 C3.

1. Resolve associated trunk/foliage art independently of whether each part is itself harvestable. Use the targeted static and actual component relationships, not every harvestable trunk within a broad Z window. Recheck P544's fruit examples at Trammel (1126,2285) and (1420,1425) from available local data; retain the earlier P412 lower-leaf example at (525,816). Synthetic fixtures must cover equal, higher and lower foliage/trunk elevations.
2. Identify hidden components with facet, position, graphic and Z. Distinguish stacked unrelated trunks and repeated graphics, including P544's (587,1636) and (5363,3149) records. Update server encoding, client validation/storage/drawing/selection and packet tests together. Define compatibility with the existing no-Z packet so mismatched versions do not misparse or hide unrelated statics; use versioning/capability handling rather than silently reinterpreting the old payload.
3. Reject hidden statics in cached world-selection validation and invalidate selection when exhaustion/reset/expiry changes visibility. A stationary-cursor test must exercise GameScene's actual cached route; fresh CheckMouseSelection or manager lookups alone are insufficient.
4. Include a multipart jungle-tree fixture that states the supported limit. Default to C3's recommended same-tile scope unless multipart expansion is expressly approved. Do not claim all canopy pieces disappear. If expanded, encode each component's position and prove adjacent unrelated trees remain visible; do not infer a whole tree from an arbitrary radius scan.
5. Keep shared observer/login hiding, final-target-only stumps, bank/reset/expiry lifetime and the existing polearm message. Do not narrow visibility to the chopper or redo P412's original feature. No new art is required.
6. Observe each new regression failing first, then passing. Run docker/uo/build.sh -t sl-modernuo:cc-P??, apply/build the client patch against client/TAZUO_COMMIT and run client tests plus relevant package gates. Use isolated world/client fixtures only. Record any unavailable visual or real-map verification explicitly rather than claiming a rendered pass.
7. Done means a fruit tree resolves to its trunk, unrelated stacked graphics remain selectable/visible, and hidden cached statics cannot remain selected, with protocol compatibility documented. Notes: notes/cc-P??-tree-components-and-selection.md. End P?? DONE.
```

### W2. Shared work-order turn-in validates the entry, with mining compatibility coverage

```text
# CC task P??: mining follow-up: one work-order payout and real confirmation/legacy tests
**Model:** Opus
**Touches:** server
**Agent:** Codex OK
**Summary:** P548 identified a shared-method replay risk and two test gaps. Current ledger/Register UI paths choose active entries; do not advertise a demonstrated player double-pay exploit.

1. In GuildContractLedgerGump.TurnIn, before requirements, consumption, progress adjustment or reward, validate that the entry is uncompleted, belongs to this character's actual active list, and matches the requested guild and its definition. Do not trust an arbitrary CharacterGuildData object supplied by a caller. Refuse absent, completed, foreign-character and mismatched-guild entries without side effects.
2. Red-first a completed mining quota passed to TurnIn twice, plus foreign/absent/mismatched entries. Compare standing, vouchers, gold, history count/order, mining progress and materials after refusal. Exercise normal ledger and combined Register turn-ins so legitimate completed requirements still pay exactly once.
3. Open the real RestoreWithGold confirmation with one voucher, then gain at least four before pressing button 82. Exactly four vouchers, ordinary ingots and 1,000 base gold pay for one Reinforced Pickaxe, with no stale surcharge or second restoration on repeat. The current handler is correct; prove the new test detects a temporary mutation to stale-price use, then restore it.
4. Deserialize a version-2 mining.ore_refinement_s entry and finish with 150 iron and no Dull Copper discovery. Separately finish a fresh 50-Dull-Copper quota. Both pay 350 standing, 16 vouchers and 400 gold once; only the legacy unmet-quota path consumes iron. Prove test sensitivity to the respective compatibility/payout mutations if these paths already pass.
5. Keep the StoneMining book/gates, Journeyman offer, exact-metal quota hook, held Stone Contracts and gold-for-missing-vouchers policy. P551/P561 own publication checks; Iron Beetle credit remains unverified unless actually exercised, not an invented new defect.
6. Every new test is seen failing first against the unfixed path or a documented temporary mutation, then passing after restoration. Run docker/uo/build.sh -t sl-modernuo:cc-P??. Notes: notes/cc-P??-work-order-entry-guards.md with the shared-method reachability limit. End P?? DONE.
```

### A2. Add P555's deletion regression to P533 W2

Keep `N/cc-P533-codex-findings-to-fixes-3.md`, W2 as the existing level-gear repair owner. Add one real-event test in LevelGearVerification: equip XP-eligible gear, damage a wild creature without killing it, assert its remaining hits are positive, call Delete(), and assert unchanged gear XP. Ensure the fixture would yield nonzero rounded XP if incorrectly paid, so a zero pool cannot make the test vacuous. Temporarily remove only the Hits <= 0 guard, observe that new test fail, restore it and observe it pass with the existing ordinary-wild, controlled and summoned death cases. Run the existing owner's build gate. Do not remove the correct guard, reopen P427's five completed fixes or number a second level-gear prompt.

### D1. Revise the Town Houses design before any implementation prompts

```text
# CC task P??: Town Houses design follow-up: workable engine hooks, safe tenancy and durable settlement
**Model:** Opus
**Touches:** docs-only
**Agent:** Codex OK
**Lane tests:** none
**Summary:** Resolve P550's design blockers in a successor notes design before issuing P409's L0-L5 build prompts. No Town Houses implementation exists to repair in a running world.

1. Read P409, P542, P550, P556 and Chase's October 22 calls. Write notes/cc-P??-town-houses-revised-design.md with source citations and a replacement L0-L5 plan. Keep native rentals and sublets, guarded-town support, account one-house accounting, and explicit exclusion of F-44 inns and F-49 halls. Do not implement Knive's download or treat P532's defer recommendation as Chase's answer.
2. Specify a narrow region factory used by BaseHouse.UpdateRegion, plus parent/3D region construction, so BaseHouse.Region remains the registered authoritative region. Specify real instance Min/Max bounds and sector registration for invisible multis, not empty Resize alone. Compare patch alternatives and require cross-sector/height/offset/reload proof in L1. State precisely which patch belongs in each later prompt; do not label L2/L3 custom-code-only before checking their hooks.
3. Map each room permission to an actual engine entry point: movement, login, item/container use, lockdown, secure/release, addon placement, targets and gump responses. Do not temporarily grant household owner/co-owner status. Specify common street-to-room access, nonoverlap, door/stair/exit protection, stock combat and guard behavior, and the chosen account entitlement reservation across placement/deeds/transfers/claims and alts.
4. Give registered lockdowns, secures and addons an explicit responsible account and room/lease record with transfer rules. Protect renter property from landlord/co-owner taking or release. Choose a separate loose-item rule rather than assigning ownership by current room location. Pack room property first, then principal property, preserving filled addon containers and strongboxes; never sweep town fixtures, corpses or mobile inventories into recovery.
5. Make the permanent site/recovery/payment state independent of the disposable house/sign. Keep town doors usable while vacant; swap only on activation, with exact originals, links, facing and lock state restored on every end or rollback. Make ordinary house decay unable to bypass lease termination. Route eviction, voluntary/staff ending, account deletion and unexpected sign/house deletion through settlement before destructive base cleanup. Specify holds/orphans and abandonment without indefinite free occupancy.
6. Specify durable pending payouts and an idempotent settlement state machine. Reduce debt only by actually delivered funds, retaining full-bank/partial/missing-bank balances over restart. Use starting gold = remaining spendable gold + prepaid credit + room escrow + pending payments + recorded rent/fee sinks, including initial held balances. Count account gold, gold stacks and checks once. Bound rent/credit/term arithmetic and rounding; a staff test assignment creates no refundable paid credit.
7. Resolve uptime versus wall-clock deadlines explicitly. Under P550's recommendation, persist uptime-based paid/grace budgets, carry deadlines from the prior paid period, define arrears and payment extensions, and prevent restarts from resetting grace. Specify acceptance-time state/terms/payment checks, grace storage-growth restrictions that still allow recovery, nondepositable/nontradeable withdrawal-only recovery storage and a rule against repeated over-capacity banking.
8. Carry C4-C13 into a decision table with recommended answers and proposed defaults clearly labeled. Keep sublets in the accepted plan while identifying the entitlement/refund/abandonment choices still awaiting Chase. Keep vendors explicitly off initially and decide barkeep capacity separately. Prices, supply, quotas and actual site geometry remain proposals pending survey, not verified gameplay.
9. Replace each later build prompt's Done means with concrete red-first acceptance cases from P550: region/guards/self-parenting; multis across sectors and two isolated footprints; renter login and property boundaries; both directions of housing entitlement; full/missing bank and repeated settlement/restart; long downtime and repeated restarts; every termination path; filled addon/strongbox recovery; vacant doors; decay; recovery storage abuse. No new tests or code are added by this design task. A later build must demonstrate each test failing before fixing or with a temporary mutation for already-correct behavior, then passing.
10. Coordinate the corrected planned claims with existing P560 and P561; do not draft another player page. Do not edit docs/, survey/place sites on a live world, connect to Haven or deploy. Done means every P550 correction/risk and remaining question has a concrete disposition, source path, future acceptance proof and owner in the revised notes. End P?? DONE.
```

## For Chase

These are recommended answers, not answers recorded as accepted here. No question blocks completion of P556. C1/C2 affect issuing U1, C3 controls optional expansion of W1, and C4-C13 belong in D1 before the corresponding housing build. Existing approved calls are not questions to ask again.

| ID | Decision and source | Recommended answer |
|---|---|---|
| C1 | Discounted vendor items can reimburse their full cost while leaving spendable points, P546 #1. | Close the zero-cost point loop. Keep current gold rewards and normal Clean Up valuation; raise only affected civic requirements using actual minimum final prices and a rounding margin. Measure first and state saved-entry behavior. Do not use this as approval to retune crafted Sandals or all OSI item values. |
| C2 | When does an old civic contract begin tracking after upgrade, P546 #2? | Initialize its missing baseline after point/contract data load and before the next award, including bundle redemption. Preserve already saved baselines, avoid historical credit, and remove the need to inspect Active first. This deliberately improves P414's disclosed first-look behavior; no retroactive player debit or compensation pass. |
| C3 | Must chopped-tree hiding expand to neighboring-tile jungle components, P544 #4? | Keep the specified same-tile scope for this fix and document/test it honestly. Fix fruit/stacked/cached-selection defects now. Approve multipart expansion separately only with exact component positions and unrelated-tree protection. Do not change shared observer visibility, which P412 deliberately chose. |
| C4 | Does a rented room consume the account's house entitlement, P550 question 1/D03? | Yes, unless Chase explicitly grants an exception. Use a saved account reservation enforced in both directions through every stock housing acquisition route, including alts and pending offers. The principal tenancy already counts; the room exception was only a proposal. |
| C5 | Rent or sale, prices, term/grace and downtime, P550 question 2 plus D13 and P409's open terms? | Weekly rent first with sublets still in scope. Keep staff-set prices, up to four prepaid weeks and seven days of grace as provisional design defaults, not tested balance. Use persisted uptime for rent/grace so downtime does not consume either budget; define overdue payment coverage precisely. Defer outright sales until a separate abandonment policy exists. |
| C6 | Site access and landlord power, P550 questions 3/4 and D04/D07/D08? | Require an approved building list excluding inns, halls, services and public travel routes, revalidated at lease activation. Permit management entry only under disclosed terms; never taking/releasing a renter's registered property or bypassing paid access with bans, doors or blocked common paths. Loose visitor items do not become renter property by location. |
| C7 | What happens to rooms when the principal enters grace, P550 question 5? | Warn renters, stop room renewals/new offers, preserve access for recovery, and settle rooms if the principal lease ends. Never sell a term beyond the guaranteed building lease without an explicit backed refund guarantee. |
| C8 | Early-end refunds and midterm changes, P550 questions 6/7? | Refund unearned room rent when landlord, staff or principal eviction ends it, with one deterministic prorating/rounding rule. Charge town fees only on earned rent. Keep a renter-forfeiture rule only if shown before payment. No paid-term price/storage change; require explicit acceptance at renewal and reserve each promised storage share. |
| C9 | Recovery delivery and over-limit crates, P550 D16 and question 10? | Preserve registered property in account-bound, withdrawal-only, nontradeable recovery storage. Reject deposits, count nested contents and retain ordinary total-item accounting. Block another tenancy until prior recovery storage is cleared. Never use a broad area sweep or allow repeated leases to become unlimited remote bank storage. |
| C10 | Abandoned leases and holds, P550 question 9/D10? | One settlement path for default, warned inactivity and staff ending. Use the stock 180-day inactivity threshold as a proposed lease trigger, subject to Chase's confirmation. Show age-sorted holds/orphans for staff, with no silent permanent rent-free state. Keep ordinary house decay disabled for leaseholds. |
| C11 | Friends' items and deleted character/account recovery, P550 question 8? | Record account entitlement for agreed principal/shared property and each renter's registered property separately. Deliver to a surviving same-account character; if the account itself is deleted, keep a staff recovery record under an explicit retention policy. Do not promise a forever bank after that bank/account is gone. |
| C12 | Supply, facets, initial prices and storage, P550 question 10 and P409 open settings? | Survey and pilot Britain first within the accepted town scope, with a small approved site list rather than every empty building. Keep prices provisional and define capacity through real AOS overrides, with nested room shares inside the total. Broader town/facet supply, eligibility/private-public defaults and price amounts remain the existing P409 decision list, not new settled answers. |
| C13 | Vendors and barkeepers, P550 D17? | Explicitly disable player vendors and barkeepers for the first release. Treat any later vendor support as a separate inventory/rental-settlement design. Zero vendor capacity by incidental missing placement data is insufficient specification. |
| C14 | Publish P551-P553/P560 now, or claim live prices/packages and Iron Beetle behavior? | Keep the completed guide drafts and route accuracy/rollout checks to P561. Keep Town Houses labeled planned. Confirm actual rollout, configurable prices, client/package behavior and pet-mined quota credit only in an authorized environment; do not turn these unverified observations into extra bug or guide prompts. |

## Source inventory and verification limits

Primary review/guide evidence read:

```text
cc-P544-review-chopped-tree-visuals.md
cc-P545-review-rootdeep-anthill-entrance.md
cc-P546-review-retire-civic-waste-bundles.md
cc-P547-review-trash-bag-corpse-clearing.md
cc-P548-review-stone-mining-gate.md
cc-P549-review-launcher-always-starts.md
cc-P550-review-town-houses-design.md
cc-P551-guide-mining-changes.md
cc-P551-guide-mining.md
cc-P552-guide-clean-up-britannia-changes.md
cc-P552-guide-clean-up.md
cc-P553-guide-launcher-troubleshooting.md
cc-P553-guide-launcher.md
cc-P554-review-league-register-fixes.md
cc-P555-review-crystal-p379-fixes.md
```

Also read each P544-P555 adjacent `-codex-review.md`, the P551-P553 wiki drafts, P533's report/work record/adjacent review, P429/P476/P477 draft ownership, P409's design, and the P411/P412/P451 adjacent implementation reviews. Read Chase's Town Houses calls directly from `D:/UO/overseer/decisions-2026-10-22.md:24-25`. No external tool, service, decision inbox or prompt queue was modified.

Prompt-catalog fingerprint at the deduplication pass: SHA-256 `2933aec441f11c9a371a8b46a4133cea61bd0b76b9de4f3c7f7c9ca2eb35fdb8`. Computation: sort Markdown paths within queue, waiting, completed, claimed, merging and held in that order; hash each file; concatenate relative POSIX path, one space and lowercase content SHA-256, separated by LF with no final LF; hash the UTF-8 concatenation. The scans included nested claimed lanes. Relevant existing owners and exclusions are listed above rather than treating keyword-hit counts as coverage.

Final catalog fingerprint: `9191956de8f063154ab411457caa7acb5ef74b224ab1497745a2261d71fe5bd4`. Read the prompts repo's latest status/log and P557's full prompt: the only delta was the unchanged P557 guide moving from claimed/Verite to merging. Reconstructing its earlier path reproduced the initial fingerprint exactly. No new fix scope appeared. Both work-copy/main refs remained at the hashes recorded above.

Current source was checked at the failure branches cited in the table, including vendor final-price arithmetic, null baseline initialization and claim overlap, corpse eligibility and real warning callbacks, shared turn-in and voucher recalculation, check-only list writing and launch staging/retries, Hunter's Satchel admission and parent checks, the real gear deletion guard, tree encoding and client cached-selection validation. Housing engine checks covered region ownership, multi bounds/sector lookup, private login checks, managed property lists, sign/door deletion, decay and bank delivery. These corroborate the design analysis; proposed hooks and recovery designs were not implemented or runtime-proved.

No build, gameplay test, new test/gate, client session, save/reload experiment, price transaction, launcher probe, package build or live connection ran for P556. P544's map records and P549's lock/race/timing probes are attributed historical evidence. Their source mechanisms were checked; those probes were not rerun. Runtime impact, current faction tax/ownership, actual player harm, visual appearance, live entrance travel, site geometry, crash recovery and published package state remain unverified. No Haven connection, deployment, account change, code change, docs/ edit, commit, merge, push or branch switch occurred.

Ran `tools/progress.py --dry-run` against the supplied work copies with SL_SHARD and SL_MIGRATE overrides. It completed with its known unconditional progress.json write suppressed by a process-local Path.write_text guard. The file's original bytes stayed unchanged. P533 W24 remains the fix owner; this reporting guard is not a code change or a claimed test of that fix.

Final editorial verification and scope results are recorded in the companion [work record](cc-P556-codex-findings-to-fix-drafts-4.md).

P556 DONE
