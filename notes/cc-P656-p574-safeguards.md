# cc-P656: the P574 safeguards that need no decision

## In plain words

- **Trash barrels** pay for what is really thrown away. Before, lifting one ingot off a stack of 1,000 in a barrel and throwing it back paid for all 1,000, every time the barrel emptied. Now it pays for the one ingot. Two players whose stacks join in a barrel each get their own share; before, the second got nothing.
- **A new trash bag from the Sanitation Warden** no longer destroys what the old bag held. The things move into the new bag, or your backpack or bank if they do not fit.
- **The Custodians' sweep** (`[cleanupall`), `[cleanup` and the trash bag's "Clear corpses nearby" only take what you could reach yourself: nothing behind a wall, on another floor, or loose in someone else's house. A corpse holding a blessed or quest item, or a filled bag, is left alone. **The Clean Up store** no longer completes a purchase from another facet, another floor or after the trader is gone.
- **For you:** nothing to try. It reaches the shard with the next deploy. The Civic Contract point fix, the old-contract start rule and the unravel shard formula still wait on your answers (P574 F01, F02, F03). They are listed under For Chase.

## What P574 says can proceed

P574 (`notes/cc-P574-questions-for-chase-2.md`) names two kinds of safeguard as independent of the open answers:

- **F01:** "independent corpse and payment safeguards can proceed". These are the Clean Up safeguards that P556 hands to P476 U2 ("P476 U2 separately owns barrel and corpse/bag safety", P556:98), plus P556's A1 addition to it.
- **F03:** "destructive-item protection does not wait" (P533 U2 parts 1 to 3).

Every other Fix scope row (F02, F04, F06, F07) is the blocked change itself, not a safeguard beside it. The Build, Release and Future rows are new features. P574 also says the P533/P556/P572 repair tables "remain with their named repair owners"; P610, P611 and P612 built those.

## The table

| Row | Safeguard | Done or skipped | Why |
|---|---|---|---|
| F01 | P556 A1: bonded-pet corpses, exact corpse approvals, the bag checked again on OK, no second payment | Skipped | Already done by merged P611 (`TrashBagCorpseApprovalVerification`). |
| F01 | P476 U2 #1: the barrel pays by what it deletes | **Done** | See below. Not done by any merged prompt and not queued. The queued `cc-P476` is the Crystal draft-writing task, not a build of its U2 (P611 noted the same). |
| F01 | P476 U2 #2: a new trash bag keeps the old bag's contents | **Done** | Same. |
| F01 | P476 U2 #3: the sweep respects walls, height, houses and loot rights | **Done**, loot-rights part skipped | Line of sight, height, houses and the corpse-contents rule are new. The loot-rights part (`[cleanup` and `[cleanupall` ignoring corpse rights, other players' instanced loot) was already done by P415 (`CanClear`, `LootRightsLapsedFor`). The draft asked for `CheckLoot` in place of `IsCriminalAction`; today's rule is `IsCriminalAction` plus the instanced-loot check, which covers the same cases, so I left it. |
| F01 | P476 U2 #4: the store confirmation checks facet, trader and range | **Done** | See below. |
| F03 | P533 U2 #1-#3: unravel only what was approved, BlessedFor refused, locked ancestors | Skipped | Already done by merged P610 (`UnravelApprovalVerification`). |
| F01 | P556 U1 #5: Civic Contract overlap coverage tests | Not built | Test coverage, not a safeguard, and P556 puts it in the U1 draft that waits on C1/C2. It belongs with U1 when that is issued. |

None of the four built parts was wrong against today's code, apart from the loot-rights part noted in the table.

## What was built

**Barrel** (`server/customizations/Services/CleanUpBritannia/CleanUpTrash.cs`, `server/patches/TrashBarrel-clean-up-britannia.patch`). A record is now a dropper's share of an item, in units: its amount when dropped, or what a merged stack added. A drop snapshots the barrel first, so a stack that merges into another is credited to the right stack. Points are priced when the barrel deletes the item, from the amount it holds then, and split by the records' units. When the records add up to more units than the item holds (a piece was lifted off), each share shrinks to fit. When it holds more (someone stacked onto it by hand), the extra pays no one. A whole item dropped in again replaces its old records. The Clean Up barrel and the trash chest pay at once, as before; their tests are unchanged and pass.

**Trash bag** (`TrashBag.IssueTo`, `SanitationWardenGump`). The new bag is made first. Each old bag's items go into it, or into the backpack, or the bank (the bank is the last resort and always takes them). Then the old bag is deleted. The Warden says where things went when the old bag held anything.

**Sweep** (`ClusterFCustodianSystem`). There is a new rule, `ReachRefusal`. The item must be on the sweeper's facet, within 8 Z of them and in their line of sight. If it is in a house, the sweeper must be its owner, a co-owner or a friend. `[cleanupall`, `[cleanup`, "Clear a corpse" and "Clear corpses nearby" (including the approved-list recheck) all ask it. `[cleanup` says why it refuses. `IsEligible` now refuses a corpse that holds, at any depth, a blessed or quest item or a container with something in it. Each of those is refused on the ground already. `[cleanup` gives its own message for that case.

**Store** (`ConfirmCleanUpRewardGump.Confirm`). The trader must exist and be on the buyer's facet, within 5 tiles and within 16 Z (one storey is 20).

## Tests

New file `server/tests/Services/CleanUpSafeguardsVerification.cs`, 5 facts. It was probed on builder image `sl-uo-builder:cc-P647` (this branch's base) with the files bind-mounted:

- **Red on the old code, 5 of 5:**
  - The barrel paid 100 for the one ingot thrown back.
  - With merged stacks, the first dropper got 10 and the second 0.
  - The banked bag's ingot was destroyed.
  - The corpse behind the wall was in the "nearby" list.
  - The store sold with the trader on another facet.
- The sweep fact stops at its first failure, so I ran a log-only copy of it against the old sweep code. The old code swept all six of the new cases:
  - the ingot behind the wall
  - the ingot 20 Z up
  - the ingot loose in the neighbour's house (by `[cleanupall`, and by `[cleanup`)
  - the corpse holding a blessed candle
  - the corpse holding a filled bag
  - the corpse behind the wall (also in the "nearby" list)
- **Green on the new code:** 5 of 5. In a wider probe, 97 of 98 Clean Up, TrashBag, Custodian, CorpseValue, Sanitation and CivicContract facts passed. The one failure was the new sweep fact, before I registered `[cleanupall` in it (the test host runs no `Configure`). It then passed.

**Gated build:** I took the `docker-build` lock and released it afterwards. Before the build, Windows had 11.2 GB available and the Docker VM's cache was small (827 MB), so I did not drop it. The build ran detached, with its log in the session scratchpad (`build-P656.log`). `docker/uo/build.sh -t sl-modernuo:cc-P656` finished with EXIT=0: "Built sl-modernuo:cc-P656 with patches applied and 2638 shard test(s) passing". That is 2,638 passed, 4 skipped (the real-map-data facts, as always) and 0 failed, including the 5 new facts and the existing barrel, store, trash bag and custodian suites.

## Deviations and decisions for Chase

- **Houses: friend, not access.** The draft said "a house the sweeper has access to". `BaseHouse.HasAccess` lets everyone into a public house, so a stranger could still sweep the loose things on its floor. I used owner, co-owner or friend (`IsFriend`). This is stricter, and it matches the changelog's "only what you could pick up yourself" more closely for public houses.
- **Heights:** the sweep reaches 8 Z, as the draft said. The store allows 16 Z, my number for "within 5 tiles in 3D": under one storey (20), with room for steps.
- **Corpse contents:** corpses holding blessed or quest items or filled containers are now left alone. That narrows P415's "the contents go with the corpse" for those cases only. Such corpses still decay on their own.
- **The 20-Z case** is refused by the reach rule as a whole. I did not prove whether line of sight or the height limit does it in the test host.
- **A tool step was denied:** the Grep tool on `D:/UO/golems/Iron/ShatteredLegacy/docker/uo` (looking for `mirror_cs_tree` and `dotnet test`, to learn where the build puts the test files). Before that, a Bash grep of the same folder was refused by the lock hook because its text named the build script. I found the layout from inside the builder image with `find` instead.
- **CHANGELOG:** a new section `2026.10.26.9` with four Fixed lines, and `VERSION` bumped to match. If another branch takes `.9` first, the integrator renumbers.

## For Chase

These stay out of this prompt. Each waits on an open P574 row:

- **F01 / P556 C1:** raising the Civic Contract point requirements so discounted vendor items cannot repay themselves (the P556 U1 economy fix).
- **F02 / P556 C2:** when an old Civic Contract with no saved starting point begins counting.
- **F03 / P533 C4:** the bounded unravel shard recovery formula (P533 U2 part 4).
- **F04:** rechecking the ankh shrine when a kept resurrection offer is accepted.
- **F05:** the missing or outdated client map safeguard (it needs an isolated client repro first).
- **F06:** the +15 Focus gain boundary.
- **P532 S054 / S055** (P476's own "not in this prompt"): whether crafted Sandals pay Clean Up points by material, and whether the blessed trash bag should accept only Clean Up items. The bag fix here keeps the contents and does not restrict them.

P656 DONE
