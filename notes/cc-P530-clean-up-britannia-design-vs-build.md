# P530: Clean Up Britannia design compared with main

Reviewed October 24, 2026. Notes only. Code HEAD and local main both point to
`f2853e86ca96c89d8f97a6c3a17c9fd2661ad41d`. Notes HEAD and local main both point
to `8a5ee4cf7e1a46313d25f68279569cb9c257f73f`. No remote refresh was attempted.
This report describes source in the supplied work copies. Installed builds,
saved-world contents, NPC placement, and live gameplay remain unverified.

Clean Up Britannia has its character ledger, valuation, barrels, appraisal,
shared store, and Custodian layer. P175 added magic-property value, earned
Fame-based corpse value, pigments, charms, and other rewards. The store still
offers 122 of the ServUO reference's 134 rewards. Main still makes civic waste
bundles and uses them for Civic Contracts. P414 will replace that contract
progress with newly earned points while keeping the rewards. P415 will add
monster-corpse clearing to the trash bag for any player. Neither queued change
is implemented in this snapshot.

## Baseline and table conventions

Read both work-copy AGENTS.md files, the direction decision, tasks, and the
document-governance list. Design inputs are F-3 in `docs/feature-queue.md:214`,
the completed P33 and P175 prompts, and their implementation notes:

- `notes/cc-P33-clean-up-britannia.md`, especially sections 2 through 6 and 10.
- `notes/cc-P175-cont-clean-up-britannia-finish.md`, Parts A through E and its
  deviations. Its completion marker does not mean the reward backlog is empty.
- `D:/UO/cc-prompts/queue/cc-P414-retire-civic-waste-bundles.md`, Chase's
  October 22 bundle-retirement decision, including the replacement contracts.
- `D:/UO/cc-prompts/queue/cc-P415-trash-bag-corpse-claim.md`, Chase's October 22
  corpse-menu decision. Queue presence establishes intent, not implementation.
- `notes/cc-P432-review-clean-up-britannia.md`, checked against the current
  source for unresolved findings. Its P414 safeguard bullet says to remove gold
  payouts. The actual P414 prompt says rewards stay as they are; that prompt
  governs this comparison.

The table follows P515/P528/P529: **Design item / Built or not / Where in code /
Gap / Size**. Built means an implementation and entry path exist in source.
Partial identifies both the present and missing behavior. Queued means requested
but absent here. Sizes judge remaining work: none, S (local change), M (several
interacting paths), or L (subsystem or substantial integration). They are not
measured schedules and should not be added together.

Prefixes: `C/` = `ShatteredLegacy/server/customizations/`, `P/` =
`ShatteredLegacy/server/patches/`, `T/` = `ShatteredLegacy/server/tests/`, and
`D/` = `ShatteredLegacy/docker/uo/`. `U/` = read-only
`D:/UO/ModernUO-pinned/Projects/`, verified at
`d4531cd94b739613155225c234900de9f47d2c88`. Unprefixed notes paths belong to
shard-migration. The generated `server/uo/` tree was not read.

## Points, barrels, and the Custodian layer

| Design item | Built or not | Where in code | Gap | Size |
| --- | --- | --- | --- | --- |
| Fractional Clean Up points per character, saved separately from account guild currency | Built | `C/Services/PointsSystems/PointsSystem.cs:85`, `:119`, `:144`, `:221`; `C/Services/PointsSystems/CleanUpBritanniaData.cs:39` | Awards, deductions, character deletion, and persistence are wired. Both spendable and lifetime totals are saved. Existing serialization tests are source evidence, not a fresh save-load run. | none identified |
| Shared item valuation from the ServUO table and special cases | Built, with remaining table gaps | `C/Services/PointsSystems/CleanUpBritanniaData.cs:112`, `:138`, `:186`, `:261`, `:320` | Runic uses, scrolls, equipment recipes/materials, and other special cases exist. P127 changed maps to the revamp values: levels 0/1 pay 50, 2 pays 250, 3 pays 750, 4 pays 1,000. P33's old map-column gap is obsolete. Some later-ported item values remain commented out; examples below. | S-M table follow-up |
| Extended ingot/board values and proper wood classification | Built | `C/Services/PointsSystems/CleanUpBritanniaData.cs:340`, `:355`; `C/ResourceInfo.cs:1174`; `T/Services/CleanUpPropertyWeightVerification.cs:265` | Extended equipment rates use the same extended-material values. The wood range now reaches Rootwood, so P33's Frostwood cutoff defect is fixed. P36 separately makes Dawnstone, Burrowhide leather, and Rootwood equipment rates zero. | none identified |
| P175: magic properties increase eligible loot's points through the shared imbue catalog | Built, with disclosed deviations | `C/ArtificersImbueGump.cs:134`, `:782`; `C/Services/PointsSystems/CleanUpBritanniaData.cs:279`, `:293`, `:316` | Equipment found in a craft system gets material value plus integer property weight / 30, then the result is truncated. Each supported property weighs 100 at Full rather than ServUO's individual weights; weapon Damage Increase is excluded. PlayerConstructed items get no property premium. Fixed table entries and equipment with no matching recipe do not automatically gain that premium. These are limits of the implementation, not an absent property system. | S-M for exact weight fidelity |
| P33 anti-farm requirement, including salvage; preserve OSI wood/cloth values under P175 | Partial as a universal guarantee | `C/Services/PointsSystems/CleanUpBritanniaData.cs:121`, `:316`, `:333`, `:461`; `T/Services/CleanUpBritanniaPointsVerification.cs:161`, `:188`, `:212`, `:499`; `T/Services/CleanUpPropertyWeightVerification.cs:107`, `:178` | Tests cover material-based equipment, salvage, runic crafting, and imbuing costs. Wood/cloth premiums were deliberately retained by P175. Fixed-price crafted sandals still bypass material valuation, and the measurement excludes table-listed outputs. P432 finding 3 remains relevant. Do not describe the whole system as farm-proof. | S-M sandals/coverage; wood/cloth retained by design |
| Appraise for Cleanup and points from public cleanup barrels, house barrels, and trash chests | Built; bookkeeping defects remain | `C/Services/CleanUpBritannia/CleanUpTrash.cs:42`, `:86`, `:116`, `:138`; `C/Services/CleanUpBritannia/CleanupTrashBarrel.cs:54`; `P/TrashBarrel-clean-up-britannia.patch`; `P/TrashChest-clean-up-britannia.patch`; `D/apply-patches.sh:470` | The custom barrel and chest pay immediately; the house barrel pays on emptying. All offer appraisal. Serial-based cached values and recording after stacking still leave P432 findings 1 and 2 open. Barrel bookkeeping is unsaved, so a restart does not preserve pending credit. | M correctness tests/fix |
| One store, opened by Cleanup Officer and Sanitation Warden, also open to non-members | Built; confirmation edge remains | `C/Services/CleanUpBritannia/TheCleanupOfficer.cs:69`; `C/SanitationWardenGump.cs:176`, `:223`; `C/Services/CleanUpBritannia/CleanUpBritanniaRewards.cs:246`, `:308`, `:436` | Buying checks funds and pack capacity, delivers the item, and deducts the price without lowering lifetime points. Opening through the Warden needs a nearby trader. Purchase confirmation still checks coordinates without checking the trader's map or deletion, as P432 finding 7 records. | S confirmation fix |
| Free owned trash bag, one per character, portable dump and return-all | Built; replacement can destroy contents | `C/TrashBag.cs:32`, `:55`, `:76`, `:95`, `:251`, `:299`; `C/SanitationWarden.cs:76`; `C/SanitationWardenGump.cs:246` | Owner persists; version 0 bags remain ownerless. Only the owner can dump. Replacement deletes old owned bags wherever they are, including their contents. The current Dump context entry checks backpack location, not ownership; ownership is checked later in the gump/dump. Warden issuance and replacement currently require membership. P415's universal access needs that path considered. | S-M replacement/access follow-up |
| Craft X rejects use the crafter's own bag after recovery routes | Built | `C/ClusterFCraftRejects.cs:63`, `:73`; `T/Services/CustodianLayerVerification.cs:358` | The route checks ownership and that the bag is in the crafter's pack, after recovery attempts and before the chosen rejects bag. It stores the reject; dumping remains a separate action. | none identified |
| Member ground cleanup and ten-tile area sweep with a 60-second cooldown | Built; per-item protection gaps remain | `C/ClusterFCustodianSystem.cs:41`, `:73`, `:96`, `:115`, `:290`, `:337` | Commands require Custodian membership even though registered at AccessLevel.Player. Eligible worthless litter is deleted for zero points. Player corpses are refused. The sweep checks eligibility without checking each item's visibility, access, line of sight, or height. P415 cannot safely expose this exact sweep unchanged to everyone. | M shared-path protection |
| P175: corpse value scales with creature Fame and earned kill credit | Built for ground cleanup | `C/Services/CleanUpBritannia/ClusterFCorpseValue.cs:39`, `:49`, `:59`, `:75`, `:83`; `C/ClusterFCustodianSystem.cs:155`, `:163`, `:314`, `:384` | Base is Fame x 0.001 for a qualifying wild creature and a rights holder or their current party member, plus recursively valued contents. Pets, ever-tamed creatures, summons, and fameless creatures pay no base. An unearned or unrecorded corpse still pays contents. Records are not saved. Staff-spawned creatures are not distinguished, so P175's requested staff-spawn exclusion is unfulfilled and disclosed in its note. The old flat 0.10 base is gone. | S-M if addressing staff/restart limits |
| Lifetime rank and retirement of Civic Tokens | Built | `C/Services/PointsSystems/CleanUpBritanniaData.cs:90`; `C/ClusterFCustodianSystem.cs:47`, `:192`, `:214`; `C/ClusterFGuildSystem.cs:1318`; `C/ClusterFDevTools.cs:160` | Ranks are Volunteer 0, Junior 25, Custodian 125, Senior 500, Chief 1,250. Awards from barrels count too; spending does not lower rank. Joining/load synchronize standing; load clears old Custodian currency rather than converting it. Guild reset paths remove cleanup entries. Civic Token retirement is already built and is separate from P414's bundle retirement. | none identified |
| Staff placement, dry run, and repeat-safe Officer/barrel creation | Built; actual placement unverified | `C/Services/CleanUpBritannia/ClusterFCleanUpPlacement.cs:25`, `:48`; `T/Services/CleanUpBritanniaStoreVerification.cs:310` | The command places the Officer on the caller's tile and barrel one east, with proximity and fit checks. There is no automatic world-load placement. Source does not prove where either stands in the saved world. | none for implementation; placement check |
| Cleanup Point Exchange stone | Omitted by explicit P33 decision | `C/Services/PointsSystems/CleanUpBritanniaData.cs:27` | Do not add it to the backlog as a missing feature. P33 deliberately chose character balances without pooling. | none |

## Reward coverage and the remaining store work

Counted the actual rows in these two files, rather than their headers:

- `C/Services/CleanUpBritannia/CleanUpBritanniaRewards.cs:86`: 122 active
  reference rewards and 12 commented omissions. Its separate supplies array at
  `:224` adds three offers: 100 bandages for 15 points, five refresh potions for
  3, and three greater heal potions for 5.
- Read-only `D:/UO/ServUO-pub57/Scripts/Services/CleanUpBritannia/CleanUpBritanniaRewards.cs`:
  134 `Rewards.Add` entries. Every active local reference reward matched a
  reference type and price, accounting for `ScrollOfAlacrity` being spelled
  `ScrollofAlacrity` in ModernUO. No current live OSI catalog check was made.

Active rows by point price are: 1,000: 5; 5,000: 7; 10,000: 37; 15,000: 3;
20,000: 10; 50,000: 22; 75,000: 2; 80,000: 2; 150,000: 4; 250,000: 24;
300,000: 6. These sum to 122. The full active item list is the array at
`:89` through `:220`; the complete omitted list is named in the table below.
P175's 73 marked additions remain present. The 250,000 and 300,000 tiers are
built; P33's claim that the store ends at 150,000 is historical.

| Design item | Built or not | Where in code | Gap | Size |
| --- | --- | --- | --- | --- |
| P175 decor, robes, boots, instruments, tile/addon rewards, pigments, and charms | Built catalog and item types | `C/Services/CleanUpBritannia/CleanUpBritanniaRewards.cs:89`; `C/Services/CleanUpBritannia/CleanUpRewardItems.cs`; `C/Services/CleanUpBritannia/CleanUpPigments.cs`; `C/Services/CleanUpBritannia/CleanUpRewardAddons.cs`; `T/Services/CleanUpBritanniaStoreVerification.cs:210` | Store supports creation, purchase, and sorting by price, with the three custom supplies afterward. P175's purchase/serialization fixture exists. Visuals, item-use fidelity, and current client presentation were not revalidated. P175 discloses the beehive's omitted bee overlay. | none for catalog; runtime/item-use checks |
| Mailbox, 1,000 points | Not offered | `C/Services/CleanUpBritannia/CleanUpBritanniaRewards.cs:88` | No implementation definition found in canonical or pinned source. P175 left this as a small self-contained port, rather than an unavailable engine capability. Port and register, with purchase/save tests. | S-M |
| VollemHeldInCrystal, 500,000 points | Not offered | `C/Services/CleanUpBritannia/CleanUpBritanniaRewards.cs:221` | No Vollem/crystal implementation definition found in those trees. P175 identifies the creature and its imprisoned-mobile wrapper as the work. The missing top tier is still real. | M |
| Human FishermansHat, FishermansTrousers, FishermansVest, FishermansEelskinGloves, 50,000 points each | Items and fishing hook built later; cleanup offers missing | `C/Services/CleanUpBritannia/CleanUpBritanniaRewards.cs:159`; `C/Services/Expansions/High Seas/Items/Sets/FishermansSet.cs:19`, `:26`, `:57`, `:95`, `:132`; `C/Services/Expansions/High Seas/Items/Fish/FishInfo.cs:392`; `C/Services/Expansions/High Seas/Mobiles/Charybdis.cs:111` | P193 added these pieces, their IFishingAttire contract, and its consumer, and names them in Charybdis's reward array. P175's absent-hook explanation is obsolete for these pieces. They are still commented out of this store. Adding their store rows and purchase/save coverage is separate from porting them again. | S store registration |
| Gargish FishermansChestguard, FishermansKilt, FishermansArms, FishermansEarrings, 50,000 points each | Not offered; no implementation definitions found | `C/Services/CleanUpBritannia/CleanUpBritanniaRewards.cs:163`; `C/Services/Expansions/High Seas/Items/Sets/FishermansSet.cs:4` | P193 ported only the human pieces. Recheck the gargish parents and set behavior against current source before a port; its old header is not proof the same dependency blockers still apply. IFishingAttire itself is now available. | M |
| RefinementAmalgamator and StewardDeed, 10,000 points each | Not offered; dependencies remain unverified in detail | `C/Services/CleanUpBritannia/CleanUpBritanniaRewards.cs:102`, `:112`; P175 Part C remaining-reward table | No implementations found by type/file searches in canonical or pinned source. P175 ties these to Armor Refinement and Mannequin/Steward systems, respectively. Those dependency walks and old line estimates were not repeated here. Do not treat them as two missing catalog lines or silently choose stand-ins. | M-L, subject to dependency sizing |
| Later ports receive their reference turn-in values | Partial | `C/Services/PointsSystems/CleanUpBritanniaData.cs:905`, `:914`; `C/Items/Consumables/TastyTreat.cs:19`; `C/Services/Monster Stealing/Items/BalmOfSwiftness.cs:10` | TastyTreat and BalmOfSwiftness now exist but their 100-point table rows remain comments. This confirms P175's loose-end warning with concrete examples. It is a valuation-registration gap, distinct from the reward catalog. No full current census of unresolved valuation rows was made. | S examples; M full table audit |

## What P414 and P415 will change

| Design item | Built or not | Where in code | Gap | Size |
| --- | --- | --- | --- | --- |
| P414: cleanup stops making civic waste bundles | Queued; old production still built | `C/ClusterFCustodianSystem.cs:397`, `:405`; `C/TrashBag.cs:283`; `C/CleanedDebris.cs:16` | Both area sweep and bag dump call GiveBundles. It pays floor(valued top-level items / 5) per batch, not per point or stack unit. Single-item cleanup does not call it. Remove both producers and bundle messages while preserving cleanup point awards. | S producers; M with contract conversion |
| P414: Civic Contracts count points earned after acceptance, per character, while keeping current rewards | Queued; bundle turn-ins still built | `C/ClusterFWorkOrderSystem.cs:2408`; `C/Services/PointsSystems/CleanUpBritanniaData.cs:39`, `:90` | Contracts still require 5 / 15 / 40 / 80 / 200 bundles, gate at 0 / 25 / 125 / 500 / 1,250 standing, and pay 100 / 300 / 750 / 1,500 / 4,000 gold with no standing or vouchers. P414 needs acceptance baselines on the existing point record, progress from later earnings, and explicit sizing from the old five-valued-items-per-bundle effort. A preexisting balance or spending points must not manufacture progress. | M |
| P414: existing bundles redeem once for points; existing accepted contracts have a safe transition | Queued; no bundle-to-points redemption found | `C/CleanedDebris.cs:16`; `C/SanitationWarden.cs:23`; `C/ClusterFWorkOrderSystem.cs:2418`, `:2435`, `:2452`, `:2469`, `:2486` | Keep the saved item type; choose and document a fair conversion rate, delete redeemed bundles, and convert accepted contracts or cancel without penalty. No new rate is settled in the prompt. Test old backpack bundles loading, one-time redemption, and old-contract handling. P414 does not delete the contracts or their gold payouts. | M |
| P414: explain the new contracts and check cheap-vendor profit | Queued; current instructions still describe bundles | `C/SanitationWardenGump.cs:132`; `C/ClusterFWorkOrderSystem.cs:2416`, `:2433`; `notes/wiki-drafts/rangers-custodians-healers.md`; `notes/cc-P386-guide-rangers-custodians-healers.md` | Replace bundle instructions with points earned after acceptance and old-bundle redemption. Show sizing and whether bottles/lockpicks can fill contracts profitably, including whatever actually limits repeated payouts. Removing bundles alone does not prove the replacement economy safe. No conversion rate or cap is assumed here. | S text; M economy/progress checks |
| P415: owner/backpack menu entries, Clear a corpse and Clear corpses nearby, usable by any player | Queued; neither entry built | `C/TrashBag.cs:95`; `C/SanitationWardenGump.cs:246`; `C/ClusterFCustodianSystem.cs:73`, `:85`, `:96` | The bag currently adds only DumpEntry. Add the two corpse targets through a shared cleanup path without the commands' membership gate. Show them only for the owner with the bag in their pack and recheck at use. Establish how non-members obtain an owned bag; current Warden issuance is member-only. Do not make everyone join just to clear corpses. | M |
| P415: corpse-only nearby clearing, no player corpses, protect others' live loot rights, warn that contents are destroyed | Queued; only the basic corpse/value helpers exist | `C/ClusterFCustodianSystem.cs:115`, `:163`, `:331`, `:367`; `C/Services/CleanUpBritannia/ClusterFCorpseValue.cs:83`; `U/UOContent/Items/Misc/Corpses/Corpse.cs:303`, `:321`, `:465`, `:750` | Existing eligibility accepts monster corpses without checking the actor's deletion rights. Earned-base credit is a payment check, not permission to destroy someone else's loot. P415 must choose and document a rights-expiry rule from pinned behavior, preserve instanced/protected belongings, show a contents warning before destruction, and filter nearby results to eligible corpses only. Existing sweep reach is ten tiles; its 60-second cooldown is current command behavior, not proof a future menu implements it. | M |
| P415: same corpse points/messages, real recursive deletion, and no bundles regardless of merge order | Queued; reusable pieces built | `C/ClusterFCustodianSystem.cs:155`, `:163`, `:176`, `:314`, `:384`, `:405`; `C/TrashBag.cs:170`, `:269`, `:283` | The ground path passes the actor for earned Fame credit. Existing bag preview/dump calls omit it. New corpse targets must pass the actor consistently, award once including contents, delete once, and bypass bundle production even if P414 has not landed. Report measured corpse/item removal counts from an example, rather than inventing a typical number now. | M shared path and evidence |

P414's required regression evidence covers no new bundles, post-acceptance
earnings, old-bundle redemption, and saved bundles loading. P415's covers menu
ownership/location, actual corpse clearing and payout, player-corpse refusal,
another player's live rights, and nearby clearing that touches nothing else.
Those are future acceptance requirements, not tests run or added by P530.

## Existing review findings still affect the comparison

P432's seven findings remain supported by the inspected code: stale stack value
in barrels (`CleanUpTrash.cs:78`, `:109`); credit lost when recording after a
stack merge (the barrel patch and `CleanUpBritanniaData.cs:114`); crafted sandals
using the fixed table (`:121`, `:461`); replacement bags deleting their contents
(`TrashBag.cs:85`); sweeps lacking per-item access/visibility checks
(`ClusterFCustodianSystem.cs:367`); corpse contents bypassing descendant
protection (`:130`, `:167`); and cross-facet purchase confirmation
(`CleanUpBritanniaRewards.cs:438`). P432 contains the reproduction reasoning and
suggested tests. These were checked by source inspection here, not reproduced
in a running shard. P414/P415 do not by themselves promise to fix every finding.

The existing source fixtures inspected were
`T/Services/CleanUpBritanniaPointsVerification.cs`,
`T/Services/CleanUpBritanniaBarrelVerification.cs`,
`T/Services/CleanUpBritanniaStoreVerification.cs`,
`T/Services/CustodianLayerVerification.cs`,
`T/Services/CleanUpPropertyWeightVerification.cs`, and
`T/Services/ClusterFCorpseValueVerification.cs`. They cover core valuation,
ledger/persistence, store purchase and reward round-trips, ownership, token
retirement, rank, craft rejects, and corpse-value helpers. Their presence does
not establish command-level protection, the queued contract transition, or
actual client behavior. Historical P33/P175 green builds were not rerun.

## Scope and verification

Only this report and the companion lane note
[cc-P530-design-vs-build-clean-up-britannia.md](cc-P530-design-vs-build-clean-up-britannia.md)
are deliverables. No code or docs/ content changed. No tests were added or run;
P530 specifies no lane tests, and this comparison required no build. No Haven
connection, deployment, account action, commit, merge, push, or branch switch.
Shell commands ran under Windows PowerShell 5.1.

Ran `tools/progress.py --dry-run` with SL_SHARD and SL_MIGRATE pointing at the
two work copies. It completed successfully. Its progress.json write was
suppressed in memory, and that file remained byte-identical. Its global counts
are not used as a measure of cleanup behavior or completeness.

Current deployment, saved ledgers and old bundles, NPC locations, client
rendering and reward use, actual cleanup rates, and live exploit reproduction
remain unverified. The queued prompts' future sizing, redemption rate,
rights-expiry choice, and runtime results are also unverified.

Final document checks passed: cited paths and line bounds resolve, local links
resolve, tables have consistent columns, and both notes are ASCII without em
dashes or trailing whitespace. Both files are below 5 MB. Whitespace checks
passed in both repositories. The code work copy is clean; only the two new P530
notes appear in the migration work copy.

Both HEADs still match the measured local main refs. No stop-request file was
present at the final check. No P530 work remains.

P530 DONE
