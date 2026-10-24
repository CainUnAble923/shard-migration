# P565: League investigation tokens

Written 2026-10-24. Design only. No code, client files, configuration, or world state changed.

## Recommendation and decision boundary

Sell a single-use, account-bound League Investigation Warrant in the existing League shop. Each warrant names one mini boss and one investigation site. Its owner takes it there, invites nearby party members, and confirms the call. One hostile mini boss appears for that roster. Defeating it gives the boss's existing corpse loot and monster parts. The warrant buys an encounter, not a guaranteed victory.

Chase already chose this feature. The overseer's `D:\UO\overseer\decisions-2026-10-22.md:14` records his 09:26 answer: boss summon tokens are a League reward, a party calls a set mini boss once, using F-24's dive investigation idea, folded into the League and F-30 Events work. The completed P405 prompt contains the research assignment, not a separate answer transcript. Its questions are in the research note at lines 1166-1170. The adjacent 09:35 answer in the overseer's file makes the weak friendly Echo a separate high-rank reward. That belongs to the Tome of Echoes design, not this encounter item.

Everything below labeled proposed is a recommended implementation default, not another recorded answer from Chase. The questions at the end are non-blocking design choices. They do not reopen his choice of a League reward or require this design task to stop for an answer.

This is native custom content inspired by the download, not a ServUO port. The overseer should register the invented feature and its player-guide scope in the fidelity register when implementation is approved. Agents put that proposed register text in notes, not `docs/`.

## Evidence and limits

The requested `notes/cc-P405-servuo-batch-1022-research.md` does not exist in either inspected migration checkout. The completed prompt explicitly names the actual output, `notes/cc-P405-servuo-batch-1022.md`. Its world-boss section, lines 388-447, is the third-party evidence used here. The task explicitly says to work from P405's notes for third-party sources. No downloaded scripts were opened, installed, built, or executed for P565.

P405 reports that Tailean's world-boss-in-a-box crystal spawns an Ancient Wyrm variant at the user's feet, with 9,500-10,000 hits, eight UltraRich loot packs, a 10% mask drop, and a 30% tameable-dragon crystal drop. It reports commented-out backpack/range checks, a missing `TameableRubyDragonCrystal`, and broken mask behavior. Those are reported findings from P405, not independently verified measurements here. Its license was unstated. Borrow the portable encounter trigger, credit Tailean's idea in implementation notes, and copy none of those files, reward drops, names, or numbers.

Inspected code work-copy HEAD and local `main` both resolve to `1c9c5d8bbf9ab4d9a8dd288aace3afff549479dd`. Migration HEAD and local `main` both resolve to `e208e5b697b81397605711080a30484ed459c74d`. No branch was switched or fetched. These are local main snapshots, not a claim about remote main or the running shard. Pinned ModernUO is `d4531cd94b739613155225c234900de9f47d2c88`, matching `docker/uo/Dockerfile:3`.

All shard paths below are relative to the code repo. Engine paths are relative to `D:\UO\ModernUO-pinned\Projects`. Source observations:

| Source | What was read and what it establishes |
|---|---|
| `server/customizations/LeagueShop/LeagueShop.cs:93`, `:139`, `:158` | Stock rows have stable keys, AP thresholds, Renown prices, and buyer-specific factories. Purchase checks again, places all items or none, then spends Renown. |
| `server/customizations/LeagueShop/LeagueShop.cs:268` | `BoxPool` includes any factory row except another loot box when its AP is low enough. Adding an encounter row alone would leak warrants into Silver or Gold boxes depending on its AP. This requires an explicit exclusion. |
| `server/customizations/LeagueShop/LeagueShopGumps.cs:23`, `:185` | The existing shop and confirmation pages supply the purchase path and requirement presentation. A new token also needs its own use confirmation; a purchase confirmation is not consent to spawn a monster. |
| `server/customizations/ClusterFLeagueRanks.cs:228`; `ClusterFAccountData.cs:653`, `:666` | Registration is account-wide, metal rank is stored per character, and spending Renown leaves LifetimeRenown intact. |
| `server/customizations/StaffHub/ClusterFSurge.cs:237`, `:268`, `:417`, `:818`, `:856` | The surge runner is a shard-wide singleton with its own persistence and restart deletion. It is suitable precedent for tracked cleanup, not a concurrent player-investigation runner. |
| `server/customizations/StaffHub/ClusterFSurgeTemplates.cs:90` | Staff templates accept arbitrary constructible creature types. Player warrants must use a separate closed catalog, never the editable staff type field. |
| `server/customizations/ClusterFLeagueBestiary.cs:119`, `:122`, `:139`, `:172`, `:213`, `:220` | The Siegebreaker and Hollow Oak are existing mini bosses. Lookup is by exact type, and the current first-kill hook credits `LastKiller` only. Their natural spawn rows already exist. |
| `server/customizations/Mobiles/Bestiary/BestiaryMiniBosses.cs` | Both boss implementations, including constructor-packed parts and jewels, combat, stats, and generated loot. These are our own custom classes and can receive conditional policy overrides without patching ModernUO. |
| `server/customizations/Tutorial/TutorialCreature.cs:35`, `:37`, `:40` | Existing precedent for participant-only AI, outgoing harmful actions, and incoming damage filtering. The tutorial's no-loot and no-award rules are specific to the tutorial and are not suitable encounter rewards. |
| Engine `Server/Mobiles/Mobile.cs:8333`, `:8367`; `Server/Regions/Region.cs:802` | `CanBeHarmful` asks the attacker's region. A target's region alone cannot prevent a cross-boundary attack. |
| Engine `Server/Items/Item.cs:4172`; `Server/Mobiles/Mobile.cs:4959`, `:5074`; `UOContent/Items/Misc/Corpses/Corpse.cs:397`, `:772`, `:775` | Normal double-click/lift paths check item accessibility through the item's region, including its container ancestry. Carving has a separate path and delegates creature carving to `BaseCreature.OnCarve`. |
| Engine `UOContent/Engines/Party/Party.cs:14`, `:186`, `:325`; `UOContent/Mobiles/BaseCreature.cs:3333` | Party capacity is 10, `Party.Get` and membership queries exist, and `GetMaster` resolves controlled/summoned ownership. |
| `server/tests/Misc/LeagueShopVerification.cs:454` | An existing box test derives its allowed set from the same permissive shop predicate. Updating that predicate in both places is insufficient evidence that boxes cannot contain warrants. Add a direct forbidden-type assertion. |

F-24 in `docs/feature-queue.md:1918` specifies solo or party jobs and temporary investigation mini bosses with parts. The source and P515 comparison agree that the general investigation job framework is not built. P565 therefore supplies its smallest encounter service and a future job seam, not a new contract framework or a second requisition board.

Unverified here: live deployment, client rendering, walking the proposed site tiles, their Z values, current regional overrides, player damage/time-to-kill, and a running save/restart cycle. Source presence is not proof of any of those. The first implementation prompt must verify sites and the final prompt must verify behavior before enabling sales. No art generation or art request is needed for the recommended existing-art version.

## What players see

The League shop gains two rows, both using the same item class:

| Stable row key | Player label | Named encounter |
|---|---|---|
| `investigation.siegebreaker` | Investigation Warrant: The Siegebreaker | The Siegebreaker at the Covetous lake shore site |
| `investigation.hollow-oak` | Investigation Warrant: The Hollow Oak | The Hollow Oak at the Yew woods site |

Proposed shop requirement: 500 AP to open either row, 300 Renown per warrant, no gold or guild-currency price. There is no additional metal-rank gate. This keeps the existing AP-unlocks/Renown-buys model and leaves the high-rank power reward to Echoes. Registration is required to use a warrant; an unregistered buyer sees that requirement on the purchase confirmation and item. Buying does not consume AP, LifetimeRenown, or rank. The two prices are the same until play testing gives a reason to separate them.

The item is a blessed, nonstackable paper warrant, art `0x14F0`, hue `LeagueShop.LeagueHue` (1323), weight 0.1. Those are already used by shard books/shop goods. It is bound to the buying account, usable by that account's characters, and cannot be transferred, sold, stolen, insured for another owner, or used from a bank, pet, ground tile, or another player's container. Blessing is death protection, not the ownership implementation. Use the existing bound-item patterns for the actual ownership checks.

Its tooltip shows the named boss, site and facet, bound account, one use, 24-hour account investigation cooldown, and these plain rules: "Use at the marked site. Solo or with consenting party members. One corpse's loot for the group. A failed investigation spends the warrant. Server interruption restores it."

Double-click away from the site opens directions, not a ground target. Directions show the site name, facet, coordinates, and distance. There is no teleport or travel gate. At the site, the owner starts a 60-second ready check. Nearby party members receive: "Join this investigation? Joining starts your 24-hour investigation cooldown when the boss appears." The owner consents through the same screen. No party is needed for solo use. Invitees must actively accept; silence is not consent. There is no minimum party size or guarantee a solo character can win.

The final screen lists the boss, accepted roster, existing loot rules, expiry, and "Call the investigation" / "Cancel". Unaccepted members remain spectators. Refusals name the cause: wrong owner, warrant not in backpack, site disabled, too far, cooldown remaining, another run, busy site, or no safe spawn tile. All final checks run again on the server. Canceling, timing out a ready check, or failing validation takes nothing and starts no cooldown.

On successful spawn: "The League's investigation begins. Defeat The Hollow Oak within 15 minutes." A short System flavor line may accompany that plain sentence. On completion: "Investigation complete. The party has one corpse to loot." On an ordinary failure: "The investigation has ended. The warrant was spent." Give a one-minute expiry warning. Use plain boss/site names in all critical messages; flavor must not hide costs or conditions.

## Numbers and encounter catalog

All values in this section are proposed defaults. Put them in one validated settings/catalog layer, not scattered in gumps.

| Setting | Default and boundary |
|---|---|
| Sales/use switch | Disabled until validation; staff can inspect/dry-run while disabled |
| AP and price | 500 AP; 300 Renown; both nonnegative |
| Cooldown | 24 real UTC hours from successful spawn, common to both warrants and every accepted participant account |
| Roster | Caller plus accepted party members, maximum `Party.Capacity` (10), at most one character per account |
| Acceptance/start range | Alive, online, same facet, within 12 tiles of the site at acceptance and final start; caller within 4 |
| Ready check | 60 seconds; final confirmation uses the frozen accepted roster and revalidates it |
| Active limits | One run per participant account; one per site; four shard-wide; GM surge does not consume these slots |
| Initial engagement | At least one allowed player/pet damages the boss within 120 seconds, otherwise ordinary failure |
| Empty party timeout | No alive, online roster member within 24 tiles for 120 continuous seconds ends the run; reentry before expiry resets this timer |
| Hard lifetime | 15 minutes from spawn, including engagement time; never extended by healing or combat |
| Boss leash | Eight tiles from site center; a breach resets the boss to center at full health and clears combat/damage, without extending timers |
| Policy area | Radius 32 around center, parent region preserved; it governs tracked encounter interactions, not ordinary nearby combat |
| Spawn attempts | Up to 20 safe tiles within four tiles of center; no unsafe fallback to center |
| Completion corpse | Existing corpse loot, protected to the roster; ordinary corpse decay after completion |

Cooldowns and active eligibility apply to every accepted account, not just the person paying. Alts and a rotation of party leaders cannot bypass them. Only the caller needs 500 AP and League registration; invited friends can help without League membership or that AP. Each must still pass ownership-independent eligibility, including cooldown. An accepted member who becomes ineligible makes final confirmation fail without spending anything; refresh the ready check rather than silently removing someone.

Roster membership is a frozen list of character serials and account identities. Joining the party after spawn does not add a participant. Leaving/disbanding the party does not remove an accepted participant. A different character on the same account cannot take over. Pets and ordinary summons count through the accepted character who currently owns them, using `GetMaster`; transferring a pet outside the roster removes its access. No new follower slots are granted. The boss is hostile, untameable, and not `Summoned` or `Controlled`.

Initial site candidates are source-backed starting points, not tiles certified by this note:

| Site key | Facet, candidate X/Y | Evidence and verification required |
|---|---|---|
| `covetous-shore` | Trammel, 5440/2023 | `ClusterFLeagueBestiary.Spawners` calls this lake shore, based on stock spider spawns. It is away from the natural Siegebreaker at 5577/2006. Verify dry land, walls, spawn clearance, and the complete policy area on the actual test map. |
| `yew-investigation` | Trammel, 1059/1166 | Existing Yew woods Moonmaw spawn row, away from the natural Hollow Oak at 1010/1250. Verify guards, housing, tree collision, and access on the actual test map. |

The site prompt records exact validated X/Y/Z and the walkable area in the catalog. Do not seed an enabled marker or accept money based only on these candidate coordinates. If a tile fails, find a nearby valid tile in that same named home and record its evidence; do not move the feature to New Haven or the tutorial. Defaulting Z to zero is not validation. No new map edits are expected. Any necessary map work needs its own correctly locked map prompt.

Add a fixed, immovable League investigation marker using the same existing rune graphic `0x1F14` as the shop's recall rune. A marker opens directions and the warrant-use screen; it cannot spawn without a valid carried warrant. Its seeder is idempotent and explicit, with a dry run. No automatic placement on a live world.

At start, reject houses, guarded/safe/tutorial regions, Internal or wrong facets, overlapping runs/surge footprints, unsafe spawn tiles, and an occupied boss spawn space. Check the boss leash area and policy footprint, not just the caller's tile. Ordinary world creatures/spawners stay in place and keep their rules. Do not pause natural spawners or remove their creatures. A new spawn point must not overlap either natural mini-boss's home range. If the policy area overlaps an incompatible special region, disable that site.

## Bosses, participation, and rewards

Reuse the existing exact boss types. Do not clone their stat blocks, replace their parents, or change natural versions. The shared runner owns a dictionary from boss serial to run. Conditional overrides added to our two classes consult that dictionary; an untracked natural boss takes the existing path. The run store, rather than new fields in those existing classes, saves ownership. This preserves exact-type bestiary lookup and the bosses' existing serialization ancestry.

| Existing type | Current combat numbers retained | Current corpse contents retained |
|---|---|---|
| `TheSiegebreaker` | 320-380 hits, 16-24 damage, Crushing Blow, existing skills/resistances | Three `SiegebreakerTusk`, one `BurrowsLoot.RandomJewel()`, Rich plus Average plus two Gems packs; existing carvable meat |
| `TheHollowOak` | 300-350 hits, 14-22 damage, Paralyzing Blow, Regular poison at 30%, existing skills/resistances | Three `HollowOakHeartwood`, one random jewel, 20 logs, Rich plus Average packs |

These values were read in `BestiaryMiniBosses.cs`, not copied from the world-boss download. Existing bestiary level bands are 70-110 for both. This note does not infer that a character must be level 70 or that the encounter is balanced for a full party. No HP scaling, extra adds, alternate difficulty, mask, tameable crystal, guaranteed artifact, automatic Renown refund, or return warrant drops in the first release. Changing combat numbers later requires play-test evidence and its own review.

One purchase creates one boss and one normal set of corpse loot. No per-member copies of the parts or jewel. No additional flat Renown, AP, XP, gold grant, or guild standing is attached to warrant completion. Normal creature-death rewards still run once through existing hooks, with the same source type and no new multiplier. The future F-24 job framework can consume one completion event and pay its own explicitly accepted objectives; it must not reinterpret the warrant itself as a job acceptance or pay every party member just for standing there.

For a tracked encounter, credit the first-kill bestiary entry to roster members who are alive, online, on the same facet and within 24 tiles when the boss dies, and who dealt damage, had an owned pet/summon deal damage, or successfully healed/resurrected an accepted participant during the run. Keep this contribution set through healing/damage-entry expiry. Merely accepting the ready check does not earn credit. Ordinary natural-boss credit remains unchanged. Hook through an explicit tracked-run branch in `ClusterFLeagueBestiary.OnCreatureDeath` so event callback ordering cannot double-process the run. The account's existing first-kill set remains the deduplication authority.

The boss's `IsEnemy`, outgoing `CanBeHarmful`, and incoming `Damage` must consult the run roster, including pet ownership and leash. Keep normal base checks after eligibility. Block outsiders' hostile and beneficial interactions with the tracked boss through the encounter region. Outsider healing of participating characters inside the active footprint is also refused during the run; accepted healing counts as contribution. Ordinary player combat, resurrection outside the footprint, and all interactions unrelated to a run keep their existing rules.

The region must retain the underlying parent and its town/dungeon/travel restrictions. It is a combat-policy area, not an invisible wall or private facet. Spectators can see and pass through; the boss does not acquire them. Participants can leave. This is party-owned combat and credit, not visual instancing.

Cross-boundary protection is a required acceptance case: the boss stays within eight tiles, leaving at least 24 tiles to the 32-tile policy boundary, and incoming damage is roster-filtered wherever its source stands. Verify the actual ranged attacks, spells, fields, poison, reflection, and harmful-status paths available on this shard against that geometry. Reject unowned environmental damage on tracked bosses unless it is an explicitly attributed allowed effect. Do not declare the region alone sufficient. If a reachable harmful/beneficial route bypasses these controls, keep the site disabled and fix that demonstrated route before enabling sales. Any proposed upstream patch must first record alternatives in notes and pass the normal build gate.

Protect the encounter corpse from non-roster looting and carving for its normal lifetime. Freeze the same character/account roster for that check, including after party disband and restart. Add an entry for the corpse serial in the investigation store, and let the encounter region's `CheckAccessibility` enforce it while also retaining normal corpse rights for participants. `Item.IsAccessibleTo` resolves container ancestry and asks the item's region, so this also covers a lift from an already open corpse window and a looter outside the boundary. Keep the region registered until its protected corpse is gone, even though the site's active-run slot has been released; a later run at that site shares the site's policy region and checks each tracked entity's own roster.

Carving is a separate route: add a conditional `OnCarve(Mobile from, Corpse corpse, Item with)` override to each owned boss class, consulting the protected-corpse record before calling base. That signature is present in pinned `BaseCreature.cs:2003`. On reload a missing corpse owner already prevents normal creature carving; do not reconstruct a dead boss just to make it carvable. Verify opening, item lift, drag/drop and carving paths, including from outside the policy boundary. Natural corpses remain untouched. A demonstrated additional direct access path needs a narrow documented fix before release, not a promise that standard party loot rights cover strangers forever.

## State, cancellation, and restart

Use one new versioned `GenericPersistence` store, `LeagueInvestigations`, with account cooldown records, active run records, and protected corpse records. Follow the structure of `ClusterFSurge.WriteTo/ReadFrom/CleanUpAfterRestart`, but not its reward policy. Unknown versions fail loudly. Account identities use the same canonical account-name convention as existing bound goods. Do not bump `ClusterFAccountData` just to store these cooldowns.

A generated-serialization `LeagueInvestigationWarrant` item saves its bound account, catalog key, unique receipt ID, and ready/reserved state. A generated marker item saves only its stable site key. A run saves its ID, owner/receipt, immutable catalog revision, site/coordinates, participant character/account pairs, boss serial, prior and new cooldown timestamps, start/deadline, phase, and cancellation reason. Save/load must tolerate a removed catalog key by refusing use and preserving the paid warrant for staff exchange.

State flow is `Ready -> Reserved -> Active -> Completed | Failed | ServerCanceled`. Ready checks are transient and create no run record. Serialize state on the game thread; timer callbacks and gump responses use that same authority.

1. Final confirmation validates the exact carried receipt, roster, cooldowns, site slot, and safe point again. Reserve the receipt and run slot before creating the boss. Repeated confirmation of that receipt can only find that reservation, not create another run.
2. Move the same paid warrant into internal escrow owned by the run, not a public ground container. Create and register the boss, set its home/leash, and make it visible only after policy registration. Commit `Active` and the accepted accounts' cooldowns together on the game thread. On construction/placement failure, delete the partial boss, clear reservations and return the same ready receipt; no cooldown is charged.
3. Ordinary no-engagement, absence, leash-related eventual expiry, wipe, owner cancellation, or hard timeout becomes `Failed`. Delete the living boss and its carried items, without calling its kill path. Destroy the escrowed receipt. Keep cooldowns. Do not award progress, loot or parts on cleanup.
4. Allowed boss death settles `Completed` exactly once through its tracked death path. Preserve its ordinary corpse and normal death hooks, protect that corpse, publish the completion/contribution result, and destroy the escrowed receipt. A repeated death/event callback cannot spawn another corpse, replace the warrant, or pay future job credit twice. Process terminal state on the game thread before a save can capture the run as active again.
5. World load cancels every saved nonterminal run before players can act: delete only its recorded living encounter boss, release site/account locks, restore the same escrowed ready warrant, and restore prior cooldown values only where the current value still matches that run's reservation. Never kill the boss to clean it up. If the backpack is missing/full or the owner is offline, leave that same receipt in internal claim custody, visible to the owner through the Registrar's shop. Claim checks space and transfers that receipt once. It never mints a second item.
6. A GM's explicit server-cancel action has the same refund path as restart. Completed or ordinary failed runs are terminal and never refundable. Deleting a tracked living boss through staff tools is a server cancellation; a valid player kill is completion. Repeating cancellation/claim or restarting during claim must remain idempotent. Log run ID, site, account identities, serials and reason, never credentials.

This uses the shard's normal world-save boundary. A crash can roll all state back to the last save; do not claim transaction durability beyond ModernUO's save. No external payment or live-account repair is part of this feature. Test old-save reconciliation, dangling serials, missing escrow items, and unknown keys. A missing receipt is a staff-visible inconsistency, not permission to repeatedly generate replacements. Cleanup must never delete an unrelated entity just because its serial was in a bad record; check expected type, site, and ownership evidence.

For protected completed corpses, reload protection until that corpse decays, then remove the record. Do not delete a completed corpse during active-run cleanup or refund its consumed warrant. Retain a bounded terminal-run summary for staff diagnostics; prune successful/failed run records after corpse/receipt cleanup and seven days, while preserving any outstanding claim and unexpired cooldown.

## Where the implementation lives

All new source is additive under `server/customizations/LeagueInvestigations/`, mirrored by the existing `apply-patches.sh` subdirectory route. Proposed files and ownership:

| File | Responsibility |
|---|---|
| `LeagueInvestigationCatalog.cs` | Closed encounter/site keys, factories for the exact existing boss types, prices, timers, feature switches and validation. No player-supplied type names. |
| `LeagueInvestigationWarrant.cs` | Bound item, saved receipt identity, item properties, marker item, backpack/use checks. |
| `LeagueInvestigationGumps.cs` | Directions, ready check, use confirmation, claim presentation. Reuse `RequirementList` and the existing shop's wording/colors. |
| `LeagueInvestigations.cs` | Reservation/start/settlement service, roster and pet resolution, timers, contribution and future job completion event. |
| `LeagueInvestigationStore.cs` | Versioned persistence, cooldowns, run/escrow/corpse records, world-load reconciliation and pruning. |
| `LeagueInvestigationRegion.cs` | Parented interaction policy, tracked-corpse protection, boundary and leash helpers. |
| `LeagueInvestigationSeeder.cs` | Explicit idempotent marker placement and dry run at verified sites. |

Existing edit points are `LeagueShop/LeagueShop.cs` for the two rows and a new `LeagueShopKind.Investigation` excluded from `BoxPool`; `LeagueShop/LeagueShopGumps.cs` for clear purchase rules and the owner-only pending-claim path; `Mobiles/Bestiary/BestiaryMiniBosses.cs` for conditional run-policy/death overrides; and `ClusterFLeagueBestiary.cs` for tracked encounter credit. Existing natural encounters and shop rows must keep their behavior. There is no upstream override or full-file replacement in the recommended design.

F-30 integration goes in `StaffHub/StaffHubGump.cs`, calling the same `LeagueInvestigations` service. Add an Investigations subpage under Events: run ID, caller, site, roster count, boss health, time left, escrow/claim status, and terminal reason. GM actions are Inspect, dry run, Go to site, and Cancel as server interruption, each gated server-side. Keep a clear separate action for ending the GM surge; it must not end investigations. Surge and investigation overlap checks are symmetric regardless of which starts first. Staff dry runs cannot grant loot, consume a warrant or modify cooldowns.

No Shard Console window buttons, web-service changes, Haven calls, or new services are required. These are in-game Staff Hub controls. If a later prompt adds a Shard Console button, it must add its web twin and Golem catalog entry under P187; this design does not authorize a separate implementation of the action.

## Art and client needs

Use existing paper/rune item art and existing gump frames. The bosses already use body 2084 (Siegebreaker) and 2085 (Hollow Oak). Both are represented in `player-package/vendor/shattered-legacy-art/registry.csv` and `records.json`; P364's source/credit record is `player-package/vendor/shattered-legacy-art/SOURCE.txt`. Verify those mappings in the package used for the test. This note does not claim that a player's installed package includes them.

There is no new bitmap, body, animation slot, hue, custom cliloc, launcher behavior, or client code change. No art request is owed for this version because Chase need not make any art. A future custom warrant illustration is optional separate work through `New-ArtRequest.ps1`; it cannot gate or silently enlarge this build. Do not use the download's unverified `0x9CBB` crystal, `0xA1C7` mask, or tameable dragon.

Client checks cover the warrant/marker names and tooltip, shop row fit, ready-check consent and expiry, refusal text, boss movement/attacks/death on the installed package, corpse access, and clear cooldown/claim messages. Capture checks on the approved loopback test route, without contacting Haven or publishing a package.

## Tests and release evidence

P565 adds no tests because it changes only this note. Each implementation prompt adds meaningful subsystem facts under `server/tests/Misc/LeagueInvestigationVerification.cs` and the existing appropriate shop, bestiary, and Staff Hub fixtures. Every new fact must be observed failing against the behavior before its change, then passing. For new APIs, establish the smallest buildable seam first and demonstrate behavioral red before adding the implementation; a missing-type compiler error is not the intended assertion. If a new safety gate is added, deliberately break its guarded behavior and record red/green evidence too.

Required cases, split with the prompts below:

- Purchase: 499/500 AP, 299/300 Renown, exact spend, full backpack, forged/stale responses, correct bound owner and catalog key, and unchanged LifetimeRenown/rank. Assert directly that no Bronze, Silver or Gold box pool contains a warrant, independent of the production eligibility predicate. Check both factory output and repeated box contents. Preserve all previous shop goods.
- Start: wrong account, alt, traded/ground/bank/pet-contained receipt, wrong facet/range, unregistered caller, accepted vs silent member, ready timeout, duplicate account, departed/new party member, changed pet owner, exact cooldown boundary, occupied/unsafe/disabled site, slot cap and both orders of surge overlap. Every refusal leaves receipt, balances and cooldowns unchanged. Replayed confirmation creates one boss.
- Party combat: eligible player and pet damage, healer credit, spectator acquisition/damage/healing/status effects, boundary shots/fields/poison/reflection, owner logout, party disband, member death and reentry, leash reset, and natural boss regression. Demonstrate the caller-only-region defect with an outsider attack test before adding protection. Verify all actual maximum-range attack routes that can reach the site.
- Reward/cleanup: constructor-packed parts/jewel appear exactly once, one generated loot sequence, correct corpse rights including carving, no loot or corpse on deletion, no flat completion currency, one bestiary credit per qualifying account, pet/support attribution, one future completion notification, and no credit on failure/staff abort. Prove an outsider cannot lift after party disband or restart, or from outside the area.
- Time/state: use `ShardTestClock` for 120-second engagement/absence boundaries, 15-minute expiry and 24-hour cooldown; no real sleeps. Verify failure consumes once, ordinary wipe is not a refund, and the site slot is freed once.
- Persistence: round-trip active run/receipt/cooldowns/corpse protection; restart before/after spawn and death; repeated reconciliation; offline/full-pack claim; cancellation during claim; missing boss/item/account; unknown version/key; unrelated serial protection; and bounded pruning without dropping a claim. Compare natural boss serialization and behavior before/after the conditional overrides.
- Staff: player access refused; GM inspect/dry-run has no mutations; cancel affects only the selected investigation; concurrent GM surge is left intact; all subpage responses use the shared service and current run identity.

Run the relevant facts first, then `docker/uo/build.sh` through its normal gated route in a throwaway loopback-only environment with scratch saves. Never use direct `docker build` as the verification gate. Any PowerShell verification runs under `powershell.exe` 5.1, not `pwsh`. Record assertions actually observed, not only planned test names. No tests or builds were run for this docs-only task.

## Ordered Golem prompts

These are prompt drafts, not assigned P numbers or queue writes. Every prompt writes its own notes, leaves files below 5 MB, checks its stop-request file, and lets the Golem commit. All start from current canonical source, reread the agreements, and never deploy or connect to Haven. Scope is server only unless stated. M means a feature spread over several paths; it is an estimate, not measured elapsed time.

1. **Investigation catalog, verified sites, and guarded item skeleton.** Size M.

   **Touches:** server

   Read P565 and confirm Chase's answers. Add the catalog/settings, warrant and marker types with generated serialization, closed keys, feature switch off, and safe-site validation. Verify the candidate coordinates against the actual local map and regions and record exact X/Y/Z, clearance, access and parent regions. Add the explicit dry-run/idempotent seeder, but do not execute placement on a running shard. Add ownership/backpack/catalog/site rejection facts, observed red then green. Deliver site evidence and any failed candidate explanation. Shop sales are still absent.

2. **Party investigation runner, combat policy, and durable settlement.** Size L.

   **Touches:** server

   Depends on 1. Build the roster-ready protocol's service, reservations, escrow, timers, serial tracking, parented region, contribution ledger, protected corpse policy, versioned store and restart/claim behavior. Add the conditional policy/death overrides to the existing exact mini-boss types and the explicit bestiary branch. Demonstrate outsider damage/loot failures before closing them. Prove all ordinary failure/refund boundaries and save/restart cases above. Preserve natural boss loot/behavior and parent classes. Keep the feature disabled and sales absent. If this exceeds one prompt's budget, split combat/runtime and persistence into separately gated server prompts before adding purchases; do not ship a partial runner to players.

3. **League shop warrants and player consent flow.** Size M.

   **Touches:** server

   Depends on 2 passing, including persistence and corpse protection. Add the two rows, `Investigation` kind and explicit loot-box exclusion; update stock expectations without weakening existing reward guardrails. Complete directions, ready-check/final-use gumps, purchase rules, marker interaction, cooldown display and one-time claim delivery through the shop. Prove box exclusion with an independent forbidden-type test. Gate visibility/purchase/use on the feature switch. AP remains the existing row gate; do not add a rank gate or a second currency. Leave the switch off pending final checks.

4. **F-30 oversight, integration checks, and player guide draft.** Size M.

   **Touches:** server

   Depends on 3. Add the in-game Events subpage using the same runner, GM permissions, dry run and selected server cancellation. Prove simultaneous nonoverlapping surge/investigation behavior and symmetric overlap refusal. Run the full shard build gate and a scratch save/restart exercise. Verify both sites and the complete player flow in the approved local test client, including bodies 2084/2085 and outsider corpse attempts. Write a guide draft and the invented-feature register proposal in notes, not `docs/` or Haven. Report time-to-kill/party composition and any imbalance without changing stats unreviewed. Recommend enabling only when all required checks pass; Chase controls running-shard activation and publishing. If client access is unavailable, label it unverified and leave sales off rather than declaring the release ready.

The source change is larger than P405's small idea estimate because the product now includes player spending, consent, cooldowns, party ownership and interrupted-run refunds. It still avoids a new general jobs backend, arbitrary staff templates exposed to players, an upstream fork, and a separate event engine with waves/prizes. The service's explicit completion event is the reuse point for F-24 investigations when those jobs are built.

## P565 verification record

Read both work copies' agreements, direction/task guidance, actual P405 output and completed prompt, Chase's recorded 10-22 answers, current League/shop/surge/bestiary/tutorial source, relevant tests, and pinned engine paths cited above. Local main/HEAD equality was checked. Registry rows 629-630 and body records 412-413 confirm the package source mappings for 2084/2085; their rendering remains unverified. The final source review added the explicit carving guard and preserved the corpse policy region after encounter completion.

Ran `python tools/progress.py --dry-run` successfully with `SL_SHARD` and `SL_MIGRATE` pointing at these work copies. Its existing review reminders concern package publication, client checks, deployment status, direction freshness and unsorted play tests; they are outside P565 and were not changed. The required generated `tools/progress.json` snapshot is also refreshed. Its diff updates the generation time and observed prompt queue; no manual task-status decisions were changed.

Source-confirmed tooling finding, ours to fix separately: despite its documented print-only flag, `tools/progress.py:722` writes `progress.json` inside `build()`, before `main()` checks `--dry-run` at line 737. The final status check exposed that write. The generated snapshot is retained under the standing end-of-session progress rule. README/dashboard regeneration did not run. P565 does not change the tool or add a test for this unrelated defect.

No code or `docs/` file was edited, no test was added, no build/deploy/remote action ran, and no branch/commit operation was performed. This note is the only new file; the other changed file is the required generated progress snapshot. Both are below 5 MB. The note contains no em dashes or trailing whitespace, and all ordered prompt drafts include a Touches line. No lane tests apply to this design-only task. Future runtime/client checks remain explicit implementation requirements, not claimed passes.

## Questions for Chase

These concern proposed defaults only. His League reward choice and the separate Echo reward are already settled.

1. **Should entry follow the existing AP shop or also require a League metal rank?** Recommend 500 AP and 300 Renown, with League registration required to call and no extra metal rank. Friends can join without the AP or membership. Alternative: require Bronze to buy/use, which needs explicit character-aware shop gating and additional tests.
2. **Which bosses should launch?** Recommend the existing Siegebreaker and Hollow Oak with their present numbers/loot, each tied to its verified home site. Alternative: launch just one while the other site's checks remain incomplete. A new Ruby Dragon or another boss needs a separate combat and reward proposal.
3. **Who shares the cooldown?** Recommend every consenting participant account, 24 hours shared across both warrants. Alternative: buyer-only cooldown, which deliberately allows friends to rotate callers and chain encounters. The recommended ready check makes each participant's cost explicit.
4. **What is the payoff?** Recommend one normal corpse and parts for the group, ordinary death hooks only, and no extra Renown/AP/job payout. Alternative: an additional completion reward only after a separate economy proposal. Do not multiply constructor-packed parts or jewels by party size.
5. **What counts as a refund?** Recommend restoration of the same warrant for server restart, staff server-cancel, or a failed spawn; no restoration for wipes, timeouts, no engagement or player abandonment. Alternative: consume on every successful spawn even if interrupted by the server, which is simpler but makes maintenance cost players their purchase.
6. **Is visible party-owned combat acceptable?** Recommend spectators can watch/pass through, with combat, contribution and corpse access restricted to the frozen roster. Alternative: a private instance, which should wait for separately designed map/instance allocation rather than silently expanding this feature.
7. **Can the first release use existing art?** Recommend paper/rune graphics and the already registered boss bodies, with client validation before activation. Alternative: commission a new warrant graphic through the art-request workflow as later optional work.

P565 DONE
