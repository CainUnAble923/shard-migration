# cc-P118: Port list, Bulk orders, all crafts (ServUO 2016 revamp)

2026-10-15. Prompt: `D:\UO\cc-prompts\cc-P118-port-bulk-orders.md`. **Stopped at the prompt's step 3:** the faithful port
changes what a player already sees in the smith system, so it needs Chase's decision first. Nothing was ported and no
repo file was changed. Both repos were clean at the start.

## Headlines

- **The decision in one line.** Turn on OSI's 2016 bulk-order rules for **every** craft, smith and tailor included, as
  this Endless Journey shard would have on OSI (option A, my recommendation)? Or keep smith and tailor turn-ins exactly
  as they are and use the 2016 rules only for the six new crafts (option B)?
- **Why it is a decision and not a port step.** ServUO's revamp switches on with `BulkOrderSystem.NewSystemEnabled =
  Core.TOL`, and this shard runs Endless Journey (TOL on). With it on, a **non-member turning in a smith deed at a
  town Blacksmith** no longer gets "gold and a reward item" (what P56-2 checks as unchanged). Instead they get:
  - gold, plus points banked, then a rewards gump to pick from;
  - a "claim your last reward first" gate;
  - bribes;
  - a different way orders are handed out: up to 3 cached, one per 6 hours, per craft.
  That is the smith system's rewards, which the prompt says not to change without Chase.
- **Society of Smiths members would see no change under either option.** Their payout path (Seals, bank or cash out,
  the Small/Large choice gump, commissions) runs before the stock turn-in, and stays as it is.
- **Commissions:** still the Society's own (`ClusterFSmithCommissions.cs`). F-37 (2026-10-05) decided they move to the
  League board, and that is not built. This port would not touch them.

## What exists today (the inventory)

**1. Pinned ModernUO: the pre-2016 system, smith and tailor only.**
`Projects/UOContent/Engines/Bulk Orders/`, 28 files, 4,407 lines:
- small and large smith and tailor deeds, the accept and deed gumps;
- the bulk order book with its filter and buy gump;
- `Rewards.cs`, the old smith and tailor reward tables.

How it behaves:
- **A turn-in** at a stock vendor pays gold, fame and a reward item into the pack (`Mobiles/Vendors/BaseVendor.cs:1119-1132`,
  "Thank you so much! Here is a reward for your effort.").
- **Offers** come on a per-player timer: `NextSmithBulkOrder` of 6, 2 or 1 hours by skill (`Mobiles/Vendors/NPC/Blacksmith.cs:78-93`).

**2. The shard's changes to those stock files.**
- **Two full replacements:** `server/patches/BulkMaterialType.cs` and `server/patches/LargeSmithBOD.cs`.
- **Six patches:** `BOD-combine-contained`, `BOD-gumps-post-valorite-material`, `LargeBOD-post-valorite-material`,
  `SmallBOD-post-valorite-material`, `SmallSmithBOD-PostValorite` and `SmallSmithBOD-teaching-orders`.
- Together they add the post-Valorite metals, teaching orders and combining deeds inside containers.

**3. The shard's own smith system,** about 4,500 lines in `server/customizations`:

| File | What it does |
|---|---|
| `ClusterFSmithBODSystem.cs` | The Society path. `BlacksmithGuildmaster` and the Smithing Guild Book give and take smith deeds for members (cap-based, 3 small and 1 large, no cooldown); Large needs 70.1 Blacksmithy |
| `ClusterFSmithBODPayout.cs` | A member's turn-in, anywhere, banks Smithing Seals or cashes out, by a per-character setting (cc-P55 Part H). A non-member at a regular smith is paid by pinned's `BaseVendor.OnDragDrop`, OSI's pre-2016 rewards (its own header, lines 44-45) |
| `SmithBulkOrderChoiceGump.cs`, `SmithGuildmasterGump.cs`, `SmithGuildBook.cs` | The Small/Large choice, the guildmaster's pages, the guild book |
| `ClusterFSmithTeaching.cs`, `ClusterFMetalTiers.cs`, `BODCombineContained.cs`, `LargeBODItemFill.cs` | Teaching orders, the metal tiers, combining |
| `ClusterFSmithCommissions.cs`, `SmithCommissionGump.cs` | Commissions (still the Society's; F-37 is not built) |

Its tests, all of which must still pass unchanged: `server/tests/Misc/` `BODCombineContained`,
`GuildmasterBulkOrderChoice`, `LargeBODItemFill`, `PostValoriteBODMaterial`, `RegularSmithBOD`, `SmithBODPaths`,
`SmithBulkOrderChoice`, `SmithCommissionRewards`, `SmithSealCatalog` and `SmithSealPrice`, each `...Verification.cs`.

**4. What ServUO's revamp adds** (`Scripts/Services/BulkOrders/`, 51 files, 11,972 lines):
- **Six new crafts:** small and large deeds for Carpentry, Fletching, Tinkering, Cooking, Alchemy and Inscription.
- **Books and filters** that know all eight crafts (`BODType`).
- **`BulkOrderSystem`,** with per-player, per-craft context and reward points:
  - points are banked, or offered for a choice, through a points mode (Enabled, Disabled or Automatic);
  - `ConfirmBankPointsGump` and `RewardsGump`;
  - eight reward calculators, one per craft;
  - BOD collection rewards: the `Items/` folder, 11 reward items;
  - buying a deed back with a bribe;
  - "Bulk Order Info" offers: up to 3 cached, one per 6 hours (`BulkOrderSystem.cs:30-31`, `:168-195`).
- **Vendor hooks** in ServUO's `BaseVendor` (`:1174-1290`):
  - the turn-in branch under `NewSystemEnabled` (points and the rewards gump, gold to the bank);
  - each craft vendor's `SupportsBulkOrders`, e.g. `Carpenter.cs:64`, `Tinker.cs:56`, `Cook.cs:62`, `Scribe.cs:66`,
    `Bowyer.cs:70`, `Alchemist.cs:28`.

## The plan (either option)

1. **Base: the revamp.** Port `Scripts/Services/BulkOrders/` to `server/customizations/Services/BulkOrders/`, per the
   port recipe.
   - It replaces pinned's `Engines/Bulk Orders/` smith and tailor types, so those become **routed replacements** (the
     way `LargeSmithBOD.cs` already is).
   - **The shard's eight BOD patches and replacements get folded into the ported files,** each change kept and
     commented. The post-Valorite metals stay in smith deeds as the shard has them; teaching orders and combining stay.
2. **Saves:**
   - Existing smith and tailor deeds and bulk order books are in the world, so the ported types keep their serialized
     shape and add new fields through a version bump with a migration. No fresh world.
   - `BulkOrderSystem`'s per-player data saves through a ModernUO generic persistence, not ServUO's hand-written file.
3. **Who gives which deeds.** By the shard's one-owning-guild rule (`docs/feature-queue.md:3243`), plus the town
   vendors that are the stock givers:

   | Craft | Owning guild (gives and takes for members) | Town vendors (stock) |
   |---|---|---|
   | Blacksmithy | Society of Smiths (as today) | Blacksmith, Weaponsmith (pinned's two; our GargoyleWeaponsmith is a Weaponsmith) |
   | Tailoring | Tailors' Circle | Tailor, Weaver |
   | Carpentry, Fletching | Foresters' Union | Carpenter; Bowyer |
   | Tinkering | Tinkers' Union | Tinker |
   | Inscription | Arcane Society | Scribe |
   | Cooking | Maritime Brotherhood | Cook, Baker |
   | Alchemy | Order of the Alembic | Alchemist |

   - Guild masters other than the smiths' would give and take their craft's deeds on the stock rules.
   - Their own payouts (guild currency, a choice gump like the smiths') are F-18, F-20 and F-25 work, after the port, as
     the prompt says.
4. **Rewards.**
   - The revamp's reward tables are ported.
   - Any reward item not yet ported stays a **named placeholder** that says so and is listed in the notes, never
     dropped.
   - Recipe rewards (F-43), non-craft BODs and League commissions are not in this prompt.
5. **Tests and play tests, as the prompt lists:**
   - shard tests for each craft's offer at the right skill, small fill, large combine, turn-in pay, and the book storing
     and filtering;
   - all ten smith test files above unchanged;
   - play-test items with Where, Do and Pass steps, marked for the bot where it can check them.

## The decision needed

**Option A, faithful (recommended).**
- The revamp's turn-in, rewards and offer rules apply at every **town vendor**, for all eight crafts, smith and tailor
  included. That is OSI's behaviour on an Endless Journey shard since 2016, and the fidelity principle's default (port
  unchanged, so players can use UOGuide).
- **What changes for players:** a non-member's smith or tailor turn-in at a town vendor pays gold plus points into a
  rewards gump (or banked) instead of gold plus an item. Offers come up to 3 at a time, one per 6 hours, per craft.
- **What does not change:** everything a Society member sees (Seals, bank or cash out, the choice gump, the guild book,
  commissions); post-Valorite metals; teaching orders; combining.
- **To update:** P56-2's expectation ("gold and an item, as before") becomes "gold and the rewards gump".

**Option B, no visible change for smith and tailor.**
- Smith and tailor deeds at town vendors keep today's pre-2016 turn-in (gold and an item) and today's timer.
- Only the six new crafts use the revamp's points and rewards.
- The book and filter know all eight crafts either way.
- **A recorded deviation from OSI:** two systems side by side, and a UOGuide reader would find smith and tailor
  rewards described differently from what they get.

**Either way,** say whether the other guild masters (Tailors' Circle, Foresters', Tinkers', Arcane, Maritime, Alembic)
should give and take their craft's deeds now, on the stock rules (my plan), or only town vendors until each guild's own
payout is designed (F-18, F-20, F-25).

**To answer:** reply "A" or "B", and "guild masters now" or "town vendors only". The port can then run as one prompt,
probably two, given its size (51 ServUO files, eight patches to fold in, a save migration).

## What was ported

Nothing yet: the prompt's step 3 says to stop here.

## Port-list numbers

Unchanged: Bulk orders 0 of 28 (`tools/port-list.json`; the status page reads "Port list: 1 of 16 systems in").

## Deviations and decisions for Chase

1. The decision above (A or B, and whether guild masters give deeds now).
2. **The prompt's "### Player" heading:** the changelog's player lists are Added, Changed and Fixed. A port would use
   those (as P117 did).
3. **Size:** the revamp is 11,972 lines, three times pinned's BOD engine. I expect the port to need two prompts:
   - one for the core (system, deeds, books, the smith and tailor fold-in, the save migration);
   - one for the six crafts' tables and rewards, the guild givers and the play tests.

## For Chase

Nothing to try in game yet. Answer the decision above (A or B; guild masters now or town vendors only) and the port
will be queued.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`:

```
Repo Result 
---- ------ 
docs dry run
```

code: nothing pending (clean, or the importer only). docs: this note, plus the importer's `testing/` output (machine output).

P118 STOPPED: needs Chase
