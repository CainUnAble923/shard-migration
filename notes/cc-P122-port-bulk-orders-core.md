# cc-P122: Bulk orders part 1, the 2016 core (smith and tailor, option A)

2026-10-15. Prompt: `D:\UO\cc-prompts\cc-P122-port-bulk-orders-core.md` (handed by the Golem after P121). Both repos were
clean at the start apart from the play-test importer's `testing\` output. Built on Chase's answers to P118: option A
(OSI's 2016 rules at every town vendor, smith and tailor included) and "guild masters now".

## Headlines

- **OSI's 2016 bulk-order rules now run for smith and tailor deeds at the town vendors** (Blacksmith, Weaponsmith and
  their subclasses; Tailor, Weaver): up to 3 offers per craft (one more every 6 hours), a turn-in pays gold to the bank
  plus reward points spent in a rewards gump or banked (2% small, 20% large), the points mode (ask, always claim, always
  bank) set from the deed gump, the "claim your last reward first" gate, and bribes.
- **The Tailors' Circle guild master** gives and takes tailor deeds for members on the same rules (answer 2).
- **The Society of Smiths is exactly as it was.** Its guild master, the guild book, Seals, bank or cash out, commissions
  and the members' turn-in at a regular smith all run before the 2016 code is reached. The one shared piece, the regular
  smiths' Small/Large choice gump, now takes its offers from the 2016 rule instead of the old 1/2/6-hour timer.
- **Architecture: pinned's deed and book types are kept, and the 2016 system is built around them.** So every deed and
  book in the world keeps its exact saved shape, **no migration was needed**, and the shard's eight BOD patches and
  replacements did not have to be folded into anything: they apply unchanged. That departs from the prompt's "routed
  replacements of pinned's Engines/Bulk Orders/ types"; argued below.
- **Two of the ten smith test files' facts had to change, not one.** The prompt allowed only P56-2's expectation to
  change. `RegularSmithBODVerification` H3 asserts the old 1/2/6-hour timer and H4 asserts gold in the pack: both are
  exactly the old rules option A replaces (H4 is P56-2's own shard-test form). I changed those two facts' expectations
  and nothing else in the ten files; the other eight files and the other facts of that file pass unchanged. P118 missed
  them; flagged for Chase below.
- **Gates:** 16 new facts (`BulkOrderSystemVerification`), every one seen failing under deliberate breaks; gated build
  green at 1,250 shard facts; full server suite green; the test world booted, its pre-change smith deeds loaded (3, the
  census line), the new save file written and read back.

## What was ported (ServUO -> ours)

All under `server/customizations/Services/BulkOrders/` unless stated.

| ServUO | Ours | What |
|---|---|---|
| `BulkOrderSystem.cs` (944) | `BulkOrderSystem.cs` (839) | contexts, offers, points, bribe rules, buy prices, the save file (`BulkOrderStore`), the census line |
| `Mobiles/NPCs/BaseVendor.cs` :132-308, :1174-1291, :1350-1460 | `BulkOrderVendors.cs` (373) | Bulk Order Info offer, Bribe and Claim Rewards entries, the turn-in branch, the bribe; `TailorGuildmaster` partial |
| `Rewards/Rewards.cs` smith and tailor (:315-361, :667-698, constructors) | `BODRewardCollections.cs` (227) | the 2016 reward lists, 40 smith and 25 tailor, ServUO's order, clilocs, hues and prices |
| `Gumps/BaseRewardGump.cs`, `Rewards/RewardsGump.cs`, `Rewards/ConfirmBankPointsGump.cs`, `Gumps/ConfirmCallbackGump.cs` | `BODRewardsGump.cs` (322) | the rewards list, its confirm step, the bank-or-claim choice |
| `SmallBODs/SmallBODGump.cs` :82-96 (and Large) | `BulkOrderDeedGumpLines.cs` (73) | the deed gump's points line and points-mode button |
| `Items/RockHammer.cs` | `Items/RockHammer.cs` | reward, 500 points |
| `Items/MasterCraftsmanTalisman.cs` | `Items/MasterCraftsmanTalisman.cs` | reward (smith 10/25/50 charges, tailor the same) |
| `Books/BODType.cs` | `BODType-all-crafts.patch` | the six 2016 crafts appended |

Points use pinned's own calculators: their `ComputePoints` is ServUO's line for line (checked, `Rewards.cs` both trees).

**Left, with the reason:**
- **The six other crafts' deeds, calculators and reward lists, their vendors and guild masters:** P123. The context
  already carries all eight crafts (saved), and `BODType` has them.
- **The deed and book types themselves** (ServUO's `SmallBOD`, `LargeBOD`, the smith and tailor deeds, the book and its
  entries and filter gump): kept as pinned's. Pinned's book already sorts and filters smith and tailor deeds by craft
  (`BOBGump.CheckFilter`, Material 1 and 2), and has a per-player filter (`UseOwnFilter`), which ServUO keeps in the
  context instead; the filter gump learns the six new crafts' materials in P123.
- **Three reward kinds, kept as named placeholders** (13 entries): `BODRewardTitleDeed` (5: no reward-title system in
  pinned or ours), `SmeltersTalisman` (4: no smelting-bonus talisman), `HarvestMap` (4: no harvest maps). The gump lists
  each at its price with "not on the shard yet" and has no button for it, so no player spends points on nothing.
- **City Loyalty's turn-in hook** (`CityLoyaltySystem.OnBODTurnIn`): no City Loyalty on this shard.
- **Recipe rewards (F-43), non-craft BODs, League commissions (F-37):** out of scope by the prompt.

## Why not routed replacements (the prompt's shape)

The prompt asked for ServUO's types as routed replacements of pinned's `Engines/Bulk Orders/` (as `LargeSmithBOD.cs`).
I kept pinned's types and built around them:
- **Saves.** ServUO's deed classes write a different shape (hand-written, ServUO field order) from pinned's generated one.
  Replacing them means a migration for every deed and book in the world. Keeping pinned's means none; the prompt's own
  rule ("keep their serialized shape") is met by construction.
- **Drift.** AGENTS.md: a replacement hides upstream drift (`CraftItem` went from replacement to patch for this reason).
  Four new files' worth of logic plus three small patches is less exposed than replacing 28 pinned files.
- **The shard's eight BOD changes** stay exactly where they are, as patches that still apply; nothing to fold.
- **Cost:** the 2016 code adapts to pinned's types (`BaseBOD` for ServUO's `IBOD`, `GetBODType` from the deed's class).

## Upstream files patched

Applied after the P121 patches, each with its own line and comment in `docker/uo/apply-patches.sh`. Generated against
the fully patched builder tree of `sl-uo-builder:cc-p121`; all apply at `--fuzz=0`.

| Patch | File | Hunks | What | Meets |
|---|---|---|---|---|
| `BODType-all-crafts.patch` | Engines/Bulk Orders/Books/BODType.cs | 1 | Alchemy, Inscription, Tinkering, Fletching, Carpentry, Cooking appended (Smith 0, Tailor 1 stay) | none |
| `BaseVendor-bulk-orders-2016.patch` | Mobiles/Vendors/BaseVendor.cs | 3 | `BulkOrderVendors.TryTurnIn` at the top of the BOD turn-in; `AddContextEntries` after Bulk Order Info; `TryOffer` in Bulk Order Info's click | none of the shard's patches touch BaseVendor |
| `BOD-gumps-points-mode.patch` | SmallBODGump.cs, LargeBODGump.cs | 6 | two rows below EXIT (points worth, points-mode button 5), the background two rows taller, the button's response | after `BOD-combine-contained` (button 3) and `BOD-gumps-post-valorite-material`; their rows stay where they were, which `BODCombineContainedVerification` pins |

Plus our replacement `server/patches/BulkMaterialType.cs`: ServUO's six woods appended as 20..25. **ServUO numbers them
12..17, which the shard's post-Valorite metals already hold in saved deeds**, so they follow Celestial (19). P123 uses them.

**Alternatives argued (before patching):**
- *Partial-class overrides on each vendor instead of the BaseVendor patch.* Possible for the turn-in on Tailor, Weaver and
  the guild master, and already done by the Society on Blacksmith and Weaponsmith; but pinned's Blacksmith, Weaponsmith,
  Tailor and Weaver each declare `CreateBulkOrder`/`GetNextBulkOrder`, which a partial cannot override, and the stock Bulk
  Order Info entry is private to BaseVendor. Three one-call hunks in BaseVendor cover every vendor, and P123's six crafts.
- *Replacing the stock Bulk Order Info entry from each vendor's partial* (as the Society does for smiths). Would need a
  partial per vendor class and per future craft vendor; the BaseVendor hook needs none.
- *Patching each vendor's `CreateBulkOrder` to the 2016 rule.* Not done on purpose: ServUO keeps the vendors' old
  `CreateBulkOrder` and its per-player timer for the offer that can follow a sale to the vendor (`BaseVendor.cs:2228`),
  and so does this port. Faithful, and recorded below.
- *Drawing the deed-gump rows above the combine buttons* (ServUO's place). Moves rows `BODCombineContainedVerification`
  pins, one of the ten files that must pass unchanged; below EXIT instead.

## What changed, file:line

- `customizations/Services/BulkOrders/BulkOrderSystem.cs`: offers `CanGetBulkOrder` :103, `HasBulkOrder`, `CreateBulkOrder`;
  points `ComputePoints`; gold `ComputeGold` :259 (half the shop price for a small deed, pinned's table otherwise);
  `BuyPrices` (every shop list, lowest price); bribes `CanExchangeBOD`, `MutateBOD` :394, `GetBribe`, vendor states;
  `Census` :526; `BODContext`, `BODEntry`, `VendorBribeState`; `BulkOrderStore` :758.
- `BulkOrderVendors.cs`: `TryOffer` :46, `AddContextEntries` :91, `ClaimRewards`, `TryBribe`/`OfferBribe`/`DoBribe`,
  `TryTurnIn` :246, delete handlers; `TailorGuildmaster` partial :361.
- `customizations/ClusterFSmithBODPayout.cs`: `ClusterFRegularSmithBODs.CreateChosen` takes a 2016 offer at a regular smith;
  `Offer` says when the next comes; the choice gump's last line reads "Each order uses one offer: up to 3, one more every
  6 hours." (was "Either choice starts your wait for the next order.").
- `server/tests/Misc/RegularSmithBODVerification.cs`: H3 and H4, as above; header lines for both.
- `server/tests/Services/BulkOrders/BulkOrderSystemVerification.cs`: new.
- `shard-migration/notes/cc-P56-smith-economy-and-labels.md` item 5 (P56-2): its expectation updated, marked cc-P122.

## Tests

`BulkOrderSystemVerification`, 16 facts:
1. three offers at once, the fourth waits ~6 h, one back after 6 h, smith and tailor apart;
2. Bulk Order Info at a Tailor: three accept gumps, then the wait;
3. no large offer at 70.0 (0 of 200), some at 120 (59 of 200); no skill, no offer entry;
4. a small deed fills from ten swords and a large deed combines a small one;
5. a non-member's turn-in at a Blacksmith and at a Tailor: gold to the bank equal to half the shop price (275 for a
   10-Longsword deed, 60 for 10 shirts), points pending, the bank-or-claim gump; a second turn-in waits;
6. half the shop price, pinned to the shop list (Longsword 55, `SBBlacksmith.cs:68`), and a large deed paid from the table;
7. 800 points for a small 20 exceptional Valorite deed, 16 banked; spending banked points; a placeholder not sold;
8. Disabled mode: claim one reward, pending cleared;
9. Automatic banks at once; the deed gump's button cycles Automatic -> Enabled -> Disabled -> Automatic;
10. a bribe priced at worth x multiplier (300), paid from the bank on handing the deed over, the deed improved, the
    multiplier up one; a started deed refused;
11. the book stores both crafts and its craft filter picks the tailor deed;
12. the Tailors' Circle guild master: no offers for a non-member, offers and turn-in for a member, no smith deeds;
13. offers, points, pending, mode and a vendor's bribe state round-trip through the save file;
14. a save folder without the file (a pre-cc-P122 world) loads nothing;
15. the reward lists: 40 and 25 entries, 13 placeholders named, every real reward builds, prices rise.

**Seen failing first**, three break sets on a copy of the build tree (`p122/breaks.py`, scratchpad), each a fast run:
- **A, the hooks off** (no vendor runs 2016 rules, no deed-gump lines): 12 failed, including H3 and H4.
- **B, the rules wrong** (four offers, small banking at 20%, bribes at 1x, the save writing nothing, gold from the table,
  placeholders sold, the guild master serving everyone, started deeds accepted for bribes): 13 failed.
- **C, the rest** (large at 70.0, shop prices +1, a file-less load that clears, pinned's fill and craft filter broken):
  4 failed; the price fact then survived C because it read the price from the table under test, so it now pins Longsword
  at 55 from the shop list, and failed under C on rerun.
- A fact checking a deed's same-build save round trip was dropped: it could only fail by breaking pinned's serializer
  generator, so it proved nothing. The real proof is the test-world boot below.

Found on the way, in my own setup: the test host builds no craft systems (deed generation reads them) and configures no
book-entry serials; both are set up in the class's constructor.

**Gated build** (`docker/uo/build.sh -t sl-modernuo:cc-p122`): **1,250 shard facts, 1,250 passed** (P121's 1,234 + 16),
image built; the final build after the changelog is in "Final build" below.

**Full server suite, unfiltered**, in the builder: `Server.Tests.dll` 910 total, **893 passed, 0 failed**, 17 skipped;
`UOContent.Tests.dll` 2,437 total, **2,346 passed, 0 failed**, 91 skipped.

**The test shard boots clean, and a pre-change world's deeds load.** `sl-modernuo:cc-p122` on a copy of the test world's
newest automatic backup (`2026-10-15-17-35-00`, saved by the P121 build, no BulkOrderSystem file):
- boot 1: `Loading world done (206946 items, 35051 mobiles)`, then
  `[BulkOrders] 2016 rules on: 3 smith and 0 tailor deeds, 0 books holding 0 deeds, 0 players' offers on file.`;
  stopped (SaveOnShutdown): `Saving world done`, `BulkOrderSystem/BulkOrderSystem.bin` written;
- boot 2 on that save: the same census line, no error.
- **Narrow sample:** the test world holds 3 smith deeds, no tailor deeds and no books. The live world's save is not on
  this machine's disk (not under `server/lib/uo/modernuo`), so its deeds and books were not loaded here. Their types are
  pinned's, unchanged, so their shape cannot have moved; the census line will show the counts at the live server's next
  start.

## Port-list numbers

`tools/progress.py --dry-run`, before (HEAD, after P121) and after:

| | before | after |
|---|---|---|
| Bulk orders, all crafts | 0 / 28 | **3 / 28** (stem proxy: BulkOrderSystem, RockHammer, MasterCraftsmanTalisman) |
| Port list, counted | 318 / 983 | **321 / 983** |

The proxy undercounts this port: the rewards, gumps and the vendor code sit in files whose names differ from ServUO's,
and pinned's deed and book types are used as they are rather than ported.

## Play-test items added

Through the For Chase list below; Who and steps by hand in `testing/bot-triage.md` (P122 group) and
`testing/playtest-steps.json`. P122-1 BOT-PARTIAL (offers, turn-in), P122-2 BOT-PARTIAL (Society unchanged), P122-3
BOT-PARTIAL (tailor and the Tailors' Circle), P122-4 BOT (bribe). **P56-2's expectation is updated** in its source note
(`cc-P56`, item 5), its steps entry and its triage row: a non-member's town-smith turn-in now gives gold to the bank and
the rewards gump.

## Deviations and decisions for Chase

1. **Two smith test facts changed, not one** (above): H3 (offers by the 2016 rule, not the 1/2/6-hour timer) and H4
   (gold to the bank and the points gump, not gold in the pack). Both are option A itself; H4 is P56-2.
2. **Pinned's types kept instead of routed replacements** (above). No migration, the BOD patches untouched.
3. **A sale can still bring an offer on the old timer.** ServUO keeps it (`BaseVendor.cs:2228`): selling items to a smith
   or tailor can offer a deed on the vendor's old per-player timer, beside the 2016 offers. Ported as ServUO has it. If
   OSI does not do this, it is one line to turn off; say so.
4. **Bribes do not raise the shard's post-Valorite metals**, and a bribe never steps past Celestial (it would land on a
   wood). ServUO's material step stops at Valorite, Barbed and Frostwood; Celestial is added as the top of our metal line.
   Post-Valorite deeds earn iron's points, as they already do today (cc-P56: "OSI pays iron's rewards for them").
5. **Shop prices:** ServUO's table is filled by whichever vendor was built last; here it is built once from every shop
   list, the lowest price for each item. In pinned the prices agree where two shops sell the same item (Longsword 55 at
   both smiths).
6. **The Master Craftsman Talisman's failure protection is not carried** (nothing in pinned spends those charges), and
   its tooltip line is left off rather than promise it. Its craft success and exceptional bonuses do work (pinned's
   `CraftItem` reads them).
7. **Turn-in pause** is ServUO's 2 seconds at a 2016 vendor (pinned's was 10).
8. **Points-mode rows sit below EXIT** on the deed gumps, not above the combine buttons as on OSI, to keep the existing
   rows where the shard's combine patch and its test put them.

## For Chase

Try a non-member first, then a Society member, to see that nothing changed for the Society.

**Rebuild the test shard** (console, Test shard, Rebuild) before trying these.

In game on the test shard:

1. **2016 offers and turn-in:** on a character not in the Society, with Blacksmithy 80, ask a town Blacksmith for Bulk Order Info three times (Small each time): three offers, then "an offer may be available in about 360 minutes". Fill a small deed and hand it in: gold goes to your bank and you are asked to bank the points or claim a reward; claiming shows the rewards list.
2. **The Society, unchanged:** as a Society of Smiths member, hand a completed deed to the Society guildmaster and another to a town Blacksmith: both pay Seals (or cash out, by your setting) as before, and no rewards list appears.
3. **Tailors:** with Tailoring 60, ask a town Tailor for offers; set a deed's points button to Automatic and hand it in (the points bank without asking); as a Tailors' Circle member, ask the Tailors' Circle guild master for an offer (a non-member gets none).
4. **A bribe:** with gold in your bank and an unfilled smith deed, choose Bribe on a town Blacksmith's menu and target the deed, then hand the deed over: the gold leaves your bank and the deed comes back better.

## Repo size rule

No pending file in either repo is over 5 MB; the largest new one is `BulkOrderSystem.cs`, 839 lines. Build logs, the
scratch worlds, the patch generator and the break scripts stayed in my session scratchpad, outside both repos.

## Final build

After the changelog and VERSION: `docker/uo/build.sh -t sl-modernuo:cc-p122`, **1,250 of 1,250**, image built. Booted on
the same scratch world: `[ShardVersion] Shattered Legacy 2026.10.15.7 (59 version(s) in the changelog)`,
`Loading world done (208836 items, 35215 mobiles)`, the same census line, saved on stop, no error.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`, after the notes were written:

```
Repo Result
---- ------
code dry run
docs dry run
```

code: `Services/BulkOrders/` (5 files and 2 items), three patches, `BulkMaterialType.cs`, `apply-patches.sh`,
`ClusterFSmithBODPayout.cs`, the new test file, `RegularSmithBODVerification.cs`, CHANGELOG and VERSION. docs: this note,
the cc-P56 note's item 5, the triage and steps files, and progress.py's output.

P122 DONE
