# cc-P414: retire civic waste bundles; Civic Contracts count Clean Up points instead

**Golem:** Iron. **Date:** 2026-10-24. **Branch:** `golem/Iron/P414` in both work copies. **Image:**
`sl-modernuo:cc-P414`.

## In plain words

- Cleaning up no longer hands out civic waste bundles. A sweep, a trash bag dump or a single cleanup pays Clean Up points
  and nothing else.
- The Sanitation Warden's Civic Contracts (the directory's Contracts page) now ask for Clean Up points earned after you
  take one: 50, 150, 400, 800 or 2,000 by tier. They pay the same gold as before (100 to 4,000). Turning one in does not
  spend your points, and the same points never fill two contracts.
- Anyone still holding bundles can drag them onto the Sanitation Warden. Each bundle becomes 10 Clean Up points, and the
  Warden takes it. Contracts taken before this change carry on and count points from now.
- For you, after the overseer deploys: in game, take the Refuse Collection contract from the Warden's directory, clean
  up until the ledger shows 50 of 50 "Clean Up points earned since taken", and turn it in for 100 gold. Then drag a
  bundle (`[add CleanedDebris` as staff) onto the Warden and check that you gain 10 points. Nothing to decide.

## What changed

### 1. No new bundles

- `ClusterFCustodianSystem.GiveBundles` is gone. `[cleanupall` and the trash bag's Dump Now (`TrashBag.cs`) pay Clean Up
  points and say only that ("+12.5 Clean Up points."). Single `[cleanup` never gave bundles.
- Nothing else in the code makes a `CleanedDebris` (grep: no `new CleanedDebris` outside the facts).

### 2. Civic Contracts count points (`ClusterFWorkOrderSystem.cs`, `GuildContractLedgerGump.cs`)

- **The requirement.** A new `WorkOrderCleanUpRequirement` carries the points. A contract counts the character's
  lifetime Clean Up points (the existing Clean Up record, `CleanUpBritanniaData.GetLifetimePoints`) above the
  `CleanUpBaseline` stored on its `WorkOrderEntry`.
  - The baseline is set when the contract is taken (`ClusterFWorkOrderSystem.Accept`, which the ledger now calls).
  - Points earned before taking it never count.
  - `WorkOrderEntry` serialization goes to version 2 (a bool and a double). Versions 0 and 1 still load.
- **Every source of Clean Up points counts:** the Custodian commands, the trash bag, trash barrels and turned-in
  bundles. Lifetime is the one record that spending never lowers.
- **Nothing is taken at turn-in.** The points stay spendable in the Clean Up store. This keeps the old economics, where
  bundles came on top of the points.
- **Points are claimed.** When a contract is turned in, the points it counted are taken out of the count of every other
  open Civic Contract that also counted them (`ClaimCleanUpPoints`). So one sweep cannot fill three contracts. Before,
  each contract consumed its own bundles.
- **Rewards are unchanged:** 100, 300, 750, 1,500 and 4,000 gold, with no standing and no scrip. The gates are
  unchanged: 0, 25, 125, 500 and 1,250 standing.
- **What players see:**
  - Ledger requirement line: `* Clean Up points earned since taken: 12.5/50`.
  - Ledger, when not met: "Clean up litter to earn the remaining Clean Up points."
  - Accepting: "Accepted: ... Clean Up points you earn from now count toward it; return to turn it in."
  - Refused turn-in: "You have not yet earned the Clean Up points this contract asks for."
  - The first two contract descriptions now say points.
  - The Warden's gump says: "Civic Contracts count the Clean Up points you earn after taking one. Old civic waste
    bundles: hand them to me for Clean Up points."

### Sizing (measured)

A bundle was 1 per 5 items with Clean Up value, cleaned in one batch. A corpse counted as one item and paid its contents
plus its creature's fame base.

To price an item, I rolled each of pinned's loot packs 300 times in the test host. That is what monster corpses carry,
and what Custodians clear or players drop. The probe is fact 8, `SizingProbeLootPointsPerValuedItem`; gold is left out,
because Custodians never clean gold.

| Loot pack | Valued items in 300 rolls | Points per valued item | Points per corpse load with value |
|---|---|---|---|
| Poor | 1 | 1 | 1 |
| Meager | 73 | 2.30 | 2.40 |
| Average | 185 | 2.81 | 3.44 |
| Rich | 490 | 2.76 | 5.03 |
| FilthyRich | 600 | 3.31 | 6.95 |

The corpse loads come before the fame base, which is 0.001 a point of fame, so 1 to 5 more for typical monsters.

**Rate chosen:** 2 points per valued item, which is under every measured average. That makes **10 points a bundle**,
so no contract is harder than it was:

| Contract | Bundles before | Points now | Gold (unchanged) | Gold per point |
|---|---|---|---|---|
| Refuse Collection | 5 | 50 | 100 | 2.0 |
| Sanitation Detail | 15 | 150 | 300 | 2.0 |
| District Cleanup | 40 | 400 | 750 | 1.875 |
| Ward Sanitation Contract | 80 | 800 | 1,500 | 1.875 |
| Grand Sanitation Commission | 200 | 2,000 | 4,000 | 2.0 |

My first draft took P33's "an iron weapon is about 1 point" as the rate, which gave 5 points a bundle. The farm fact
(below) showed that this lets vendor sandals fill a contract at a profit, and the probe showed it undervalued real loot
two to three times. So I measured instead.

### 3. Bundles already in the world

- **The type stays.** `CleanedDebris` is unchanged apart from its comment (still `[SerializationGenerator(0, false)]`),
  so saves that hold bundles load.
- **Turning them in.** Dragging a bundle stack onto the Sanitation Warden (`SanitationWarden.OnDragDrop`) calls
  `ClusterFCustodianSystem.RedeemBundles`.
  - It pays **10 Clean Up points per bundle** (`PointsPerBundle`, the sizing rate) and deletes the stack, so each bundle
    is redeemed once.
  - The Warden answers: "3 civic waste bundles? We count Clean Up points now. That is 30 to your name."
  - One new ambient line tells players about it.
- **Only the Warden takes them.** The prompt allowed "the Sanitation Warden (or a Custodian)". There is one Warden per
  chapter, and that is enough.
- **Open contracts that asked for bundles are finished with points, not cancelled.** Their entries are version 1, with no
  baseline. The first time the ledger, a turn-in or the League Register looks at one, it starts counting from the
  character's lifetime points at that moment. The definition keys are unchanged, so the old entries pick up the new
  point requirements. A player who held bundles for such a contract hands them to the Warden; those points are earned
  after the first look, so they count, at the same 10-a-bundle rate.

### 4. The farm P33 flagged

The farm was buying cheap vendor goods with Clean Up value, cleaning them, and turning the result into contract gold.

Fact 7 (`NoVendorItemFillsACivicContractForProfit`) walks every vendor buy list in the shard:

- 86 vendor lists, 231 items sold with Clean Up value.
- Each item is priced at its base price (the vendor's markup is on top), against the most gold any Civic Contract pays
  per point.

**Result:**

- The cheapest points a vendor sells are **sandals: 5 gp for 2 points, 2.5 gp a point.** Next are hats and cloaks at 7
  to 8 gp a point. Bottles are 20 gp a point (5 gp for 0.25) and lockpicks over 100.
- **The most a contract pays is 2.0 gp a point.** So no vendor item fills a contract at a profit, and the fact fails
  the moment one would. A future price cut, a new cheap vendor item, or a richer contract would trip it.
- With bundles, a contract counted items, not points: any 25 valued items filled the first one, however little they
  were worth. That is the opening P33 flagged. Points close it, because a cheap item now counts only for what it is
  worth.

The margin is not large: 2.5 against 2.0.

**What else caps it:** one active copy per contract, at most 3 Custodian contracts at once, claimed points, and vendor
stock per restock.

**Not this task's, but worth a look in the F-18/F-25 economy pass:** the same 2.5 gp a point lets anyone buy Clean Up
**store** goods with gold through sandals. That is ServUO's Clean Up valuation and store, unchanged here, and it was
true before P414.

### 5. Docs and wiki drafts

**Updated here** (wiki drafts, which agents may edit):

- `notes/wiki-drafts/rangers-custodians-healers.md`: the Civic Contracts paragraph, plus a new paragraph saying bundles
  are retired.
- `notes/wiki-drafts/glossary.md`: the "Civic Contracts" and "Civic waste bundle" rows.
- `notes/wiki-drafts/guilds.md`: the Custodians row, "Civic Contracts pay gold for Clean Up points earned after taking
  one."

**For the overseer** (agents do not edit `docs\`, or other prompts' notes):

- `docs/implementation-status.md:31` lists `CleanedDebris.cs` as "Ported, uncommitted". It is now a retired item kept
  only for saves: say so, or drop the row.
- `docs/port-triage.md:68` names `CleanedDebris.cs` as done. Add "(retired by cc-P414)".
- `notes/cc-P386-guide-rangers-custodians-healers.md`:
  - line 94 "Bundles only for valued items in one sweep or dump, one per five" is no longer true;
  - line 95 "Civic Contracts pay gold only" is still true, but they now ask for points (`ClusterFWorkOrderSystem.cs`,
    the Custodians section).
  - That note is P386's record; the wiki page it fed is the draft updated above.
- `notes/cc-P33-clean-up-britannia.md` open item 2 (the bundle farm) is answered by this note's section 4.
- `docs/feature-queue.md:132` and `:1638` ("turn-in checks 1 per 5 items") are about F-18's tailoring seals, not
  bundles. Nothing to change.
- The published wiki pages (`uo:guilds:custodians`, `uo:systems:clean_up_britannia`, per P478) still describe bundles
  until the drafts are published.

### Player notes

`CHANGELOG.md` has a new section, 2026.10.24.5, with two Changed lines. `VERSION` is 2026.10.24.5. This branch starts
from main at .3; P413's branch already took .4, so .5 keeps the headings apart when both merge.

## Tests

Built and tested only through `docker/uo/build.sh`, under the docker-build lock.
`server/tests/Services/CivicContractPointsVerification.cs` (new):

1. `CleaningDropsNoBundles`: a dump of ten longswords pays points and puts no bundle in the pack. `GiveBundles` no
   longer exists.
2. `AContractFillsFromPointsEarnedAfterItWasTakenAndNotBefore`: 40 points before taking it count for nothing. 49.5
   after is not enough; 50 is. The turn-in pays 100 gold and leaves points and lifetime as they were.
3. `TheSamePointsNeverFillTwoContracts`: with 150 points both the 50 and the 150 contract are met. After the 50 is
   turned in the 150 reads 100, and 50 more fill it.
4. `AnOldBundleTurnsInOnceForPointsAndIsDeleted`: three bundles dropped on the Warden pay 30 points and are deleted. The
   same stack pays nothing again.
5. `ASaveWithBundlesInABackpackLoads`: a stack of 7 in a backpack round-trips through the generated serializer whole
   (amount, name, stackable, not deleted).
6. `AContractTakenBeforeTheChangeIsFinishedWithPointsFromTheFirstLook`: a version 1 entry, written byte for byte as
   the old build wrote it, loads with no baseline. 60 points earned before do not fill it; 50 after the first look do.
   A version 2 entry keeps its baseline through a save.
7. `NoVendorItemFillsACivicContractForProfit`: section 4.
8. `SizingProbeLootPointsPerValuedItem`: the measurement above. It asserts only that loot with value was generated.

**Red first:** one build with six breaks in the production files, restored from pristine copies afterwards
(`red414.py` in the session scratchpad):

- the trash bag drops a bundle again;
- points from before the contract count;
- nothing is claimed at turn-in;
- redeemed bundles are not deleted;
- a loaded bundle deletes itself;
- the first contract is sized at 5 points (the bundle count).

Result: **facts 1 to 7 all failed**, 2,270 others passed. The reasons:

- fact 1: a CleanedDebris in the pack;
- fact 2: "Expected 25, Actual 5", the sizing break, hit first;
- fact 3: "Expected 50, Actual 75";
- fact 4: the stack not deleted;
- fact 5: the loaded copy deleted;
- fact 6: met before any new points;
- fact 7: "Sandals from SBCobbler: 5 gp for 2 points beats a Civic Contract's 20 gp a point".

Fact 8 is a measurement, not a rule, and was not run red.

The facts' numbers were then moved to the measured sizing (50 for the first tier instead of 25, 10 a bundle instead of
5). The breaks above fail them the same way.

**Green:** `Built sl-modernuo:cc-P414 with patches applied and 2278 shard test(s) passing.` 2,282 in all, 0 failed,
4 skipped.

The two extra builds in between were a compile fix to fact 1's gold count and a run that made the probe print its
numbers.

**Not run:** a live check on a test shard. Every path is server code covered by the facts above, so the in-game check is
yours after deploy.

## Deviations and decisions for Chase

1. **10 points a bundle, measured**, not the 5 that P33's rough reading gives: section 2's table. A contract now takes
   at most the cleaning it took before. Say if you want it harder; the numbers are five constants in
   `ClusterFWorkOrderSystem.cs` and `PointsPerBundle`.
2. **Same points, one contract:** a turn-in claims its points from the other open Civic Contracts. The prompt did not
   ask for this, but without it one sweep would pay up to three contracts, and the vendor margin above would no longer
   hold.
3. **Open bundle contracts are finished with points from the first look**, not cancelled. Bundles held for them
   redeem at the Warden at the same rate.
4. **Only the Sanitation Warden takes bundles**, not every Custodian.
5. **The Clean Up store can still be bought into at 2.5 gp a point via vendor sandals.** That is outside this task (the
   store and ServUO's valuation are unchanged); flagged for the economy pass.
6. **Code edits were made with small Python scripts** that assert each replaced block is present exactly once. The Read
   tool has been denied on this desk's server files in unattended runs (P412, P413).

P414 DONE
