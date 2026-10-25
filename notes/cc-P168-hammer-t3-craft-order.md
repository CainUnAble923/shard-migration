# cc-P168: Hammer of Hephaestus T3: crafts a whole bulk order for you, and wastes fewer ingots

2026-10-21, the Copper Golem (Opus), branch golem/Copper/P168 of both repos. Prompt: `cc-P168-hammer-t3-craft-order.md`.
Not committed (the Golem commits after DONE). Both repos were clean at the start, and neither held earlier P168 work
(Chase's 10:07 answer was about the Silver attempt, whose work is not on this branch, so this is a full build of P168 on
Copper, gated build and tests included). Nothing was run against any world, nothing was deployed, and the player package
was not built or published.

## In plain words

The Hammer of Hephaestus has a third tier now, the Masterwork Hammer. It wastes fewer ingots on metals you know well, and
it can craft a whole smith bulk order for you, one normal craft at a time, until the order is full. Bulk order deeds now
also tell guild members exactly what turning them in will pay.

## Headlines

- **The T3 hammer, `MasterworkHammerOfHephaestus`** (the name in T1/T2's style; rename freely): 800 uses (T2 400), one
  regenerated every 10 minutes (T2 15), +15 Blacksmithy held only (T2 +10), familiarity cap 5,000 a metal (T2 2,500).
  Same held-only SkillMod rules as P52, manual versioned serialization in T2's shape, `MergeFamiliarity` ready for T4.
- **T3 bonus, resource efficiency:** a successful craft gives back `ingots used x familiarity / 5,000 x 25%` of the craft's
  metal: the whole part always, the fraction as a roll. 0 familiarity saves nothing; at the cap a quarter.
- **The upgrade:** T2 -> T3 at the Society guildmaster's Hammer page, exactly as T1 -> T2 works: Master rank (15,000
  standing), 100 Blacksmithy, 60 Seals, 25,000 gold, 1,000 iron and 250 Valorite (pack and bank), familiarity carried
  over. T4 stays a stub (the page says "T4 is not available yet").
- **Craft This Order:** the T3 held, its menu's **Craft This Order**, then target a smith deed in the backpack. Every item
  is a real `CraftSystem.CreateItem` (skill roll and gains, ingots, one hammer use, familiarity, the T3 saving) at normal
  craft speed, put into the deed by the deed's own `EndCombine`. It is a Craft X run carrying the deed, so it stops on
  everything Craft X stops on, plus the deed full, damage, the hammer out of hand, and the deed leaving the backpack.
- **Deeds show guild members their pay** (gump and tooltip): a Society member sees the Seals or cash-out gold and the
  standing by their Completed orders setting; a Tailors' Circle (or other 2016 guild) member sees the gold their
  guildmaster banks. **The gold behind every deed payout is a +-10% roll**, so each deed now has one quote, rolled once,
  that the display and the turn-in both read: shown always equals paid.
- **Patches:** two new one-call patches (`BOD-properties-guild-pay.patch`, the tooltip; `PlayerMobile-craft-order-hurt.patch`,
  the damage stop) and two lines added to `CraftItem-shard-hooks.patch`. Alternatives argued below.
- **Tests:** 23 new shard test cases (13 order/hammer, 10 guild pay), every one seen failing under a deliberate break;
  the gated build is green at **2,044 of 2,044** shard tests and the runtime image `sl-modernuo:cc-P168` is built.

## 1. The T3 hammer

All in `server/customizations/HammerOfHephaestus.cs`.

| What | Where |
|---|---|
| `MasterworkHammerOfHephaestus` (uses, regen, held +15, serialization v0, registry key `legacy.masterwork_hammer_of_hephaestus`) | :934 on |
| `RecordFamiliarity(..., CraftItem, CraftSystem)`: the saving (from the familiarity before this craft's roll), then the familiarity roll | :1087 |
| `MetalUsed`, `SavedIngots`, `RollSaved`, `RefundIngots` | :1103-1137 |
| `MergeFamiliarity` (T3+T3 -> T4, still a stub) | after `LoadFamiliaritySnapshot` |
| `HammerCraftOrderEntry` (the menu entry, held only) | :1360 |
| Metal Familiarity panel: T3 title, cap, uses, the efficiency line and each metal's saving % | :1398 on |
| `HammerRestoreGump`: T3 status and restore, `MasterworkRequirements`, the T2 -> T3 section (button 30), `HandleMasterwork` | :1642, :1851 |
| `HammerFamiliarityEntry` accepts the T3 | `OnClick` |
| `SmithGuildmasterGump.cs`: the Hammer button reads "(T3)" | :346 |
| `CraftItem-shard-hooks.patch`: the T3's `RecordFamiliarity` call, and the auto-fill's tool test names the T3 | hunk at 1423 |
| `ShardClilocs.CraftThisOrder` = 1,900,011, "Craft This Order"; `entries.json`, `registry.csv`, and the package fact's map in `Cliloc-Overrides.Tests.ps1:254` | |

**The numbers proposed** (T1 / T2 / **T3**): uses 150 / 400 / **800**; regen one per 30 / 15 / **10** minutes; held
Blacksmithy +5 / +10 (+ up to 2.5 familiarity) / **+15**; familiarity cap 1,000 / 2,500 / **5,000** a metal; bonus refund
up to 20% / skill up to +2.5 / **ingots back up to 25%**. Upgrade T1 -> T2 / **T2 -> T3**: Journeyman 5,000 / **Master
15,000**; Blacksmithy 80 / **100**; Seals 25 / **60**; gold 10,000 / **25,000**; iron 500 / **1,000**; Valorite 100 /
**250**.

**The efficiency rule:** after a successful Blacksmithy craft with the T3, `saved = used x min(1, familiarity / 5,000) x
0.25`, where `used` is the craft's ingots of its metal kind (the `CraftRes` entries whose type is the craft's resource
type, as `CraftItem.ConsumeRes` swaps them); the whole part of `saved` is given back as that metal's ingots, and the
fraction is the chance of one more (`Utility.RandomDouble`). The familiarity read is the metal's before this craft's own
gain roll. Not refunded: a failed craft (it already uses half, `CraftItem.ConsumeRes`), non-metal resources, and anything
while the Dev Testing Crystal is active (nothing was consumed). Example: a plate chest (25 ingots) at full Verite
familiarity gives back 6, and a seventh one time in four.

## 2. Craft This Order

`server/customizations/ClusterFCraftOrder.cs` (new) and the order hooks in `ClusterFCraftRun.cs`.

- **Start** (`Begin`, :42; `CanStart`): alive; the T3 in hand, not exhausted, uses left; a `SmallSmithBOD` or
  `LargeSmithBOD` (any other deed: "Only a smith's bulk order can be crafted this way."); in the backpack (so never the
  bank, never another player's); not complete; an anvil and a forge within 2 (`DefBlacksmithy.CheckAnvilAndForge`).
- **The craft:** `ClusterFCraftRun.Begin(..., order: deed)`: the item the deed needs, in the deed's metal (iron for an
  iron deed: `ResourceType`, the metal's first `CraftResourceInfo.ResourceTypes`), count = what the deed still needs.
- **The fill** (`TryFill`, :269, called first thing in `HammerBODAutoFill.TryAutoFill`, which the CraftItem patch calls
  after `AddToBackpack`): the item goes through the deed's own `EndCombine` (pinned `SmallBOD.EndCombine`, our
  `LargeSmithBOD.EndCombine` -> `LargeBODItemFill.Fill`), so the checks and their messages are exactly a hand combine's.
  The combine's own gump and new combine cursor are closed. An item the deed refuses goes on through the Hammer's normal
  auto-fill (a Society member's other deeds), else stays in the pack, as for a hand-made craft.
- **Large deeds, exactly:** at the start, every complete `SmallSmithBOD` lying directly in the backpack is offered to the
  large deed through its own `EndCombine` (pinned `LargeBOD.EndCombine`, as "Combine this deed with contained items"
  does); then the open lines are crafted one after another in the deed's order, each finished item going into its line
  through the large deed's item fill (cc-P42 H). The prompt says "crafts the missing parts of each line into the
  backpack, then fills from small deeds": it is the same result with the small deeds taken first, so none is wasted by
  crafting a line a small deed in the pack would have filled.
- **Stops** (`CheckStop`, :303, before the common Craft X stops, `ClusterFCraftRun.cs:231`): order gone from the backpack;
  order full (done); Stop pressed; hurt (`MakeXRun.Hurt`, set by `OnHurt`, :91, which `PlayerMobile.OnDamage` calls once
  damage has landed); the hammer not in hand or exhausted; 500 attempts. Then Craft X's own: died, moved (any step; so also away from the anvil and forge),
  hammer out of uses, pack full, overloaded; and every refusal (out of ingots, skill, anvil) through `Refused`.
- **Progress:** one line before each attempt, "Crafting 7 of 20: Plate Gorget ...", the progress gump titled "Order" with
  "7 of 20 in the order", and the summary: "Craft order done. Made 10 (0 failed, 10 exceptional), 10 into the order (now
  10 of 10)." A stop says why: "Craft order stopped: you were hurt." and so on.

**Pinned's path for each item:** `CraftSystem.CreateItem` -> `CraftItem.Craft` -> the craft timer -> `CompleteCraft`, as a
hand craft (Craft X's design, cc-P18). Nothing in pinned's craft code changed for this beyond the two patch lines.

## 3. Deeds show what they pay a guild member

`server/customizations/Services/BulkOrders/BulkOrderGuildPay.cs` (new), `BulkOrderDeedGumpLines.cs`,
`ClusterFSmithBODPayout.cs`, `BulkOrderVendors.cs`, and `server/patches/BOD-properties-guild-pay.patch`.

| Viewer (the player whose pack holds the deed) | Gump | Tooltip |
|---|---|---|
| Society member, smith deed, **Always bank** | "Society pays you: +S standing, N Smithing Seals" / "Completed orders: Always bank" | the same two lines |
| Society member, smith deed, **Always cash out** | "Society pays you: +S standing, G gold (cash out)" / the setting | the same |
| Society member, smith deed, **Ask each time** | "... +S standing, N Seals or G gold" / the setting | the same |
| Member of the deed's 2016 guild (Tailors' Circle, Foresters', Tinkers', Maritime, Alembic, Arcane) | the points line, "<Guild> pays you: G gold to the bank (no guild currency or standing yet)", the points-mode button | the gold line |
| Non-member, **or a member of a different guild only** (a Society member holding a tailor deed) | the 2016 points line and button, as before | nothing new |

A large smith deed for a member under the Society's large-order skill adds "(large orders need more Blacksmithy)".

**The quote** (`DeedQuote`, `Quote`, BulkOrderGuildPay.cs:38, :80). Every deed payout's gold is a roll: pinned
`SmithRewardCalculator.ComputeGold` returns `Utility.RandomMinMax(gold * 9 / 10, gold * 10 / 9)` (Rewards.cs:474-500),
P123's six calculators `Vary` the same way, and the Society's Seals are worked out from that gold
(`ClusterFSmithBODSystem.cs` `GoldEquivalentForSeals`). So "shown = paid" cannot hold if each rolls on its own. Each deed
gets one quote (kept in a `ConditionalWeakTable`, so it dies with the deed), each part rolled when first read by the very
call the turn-in made before: `ComputeGuildReward` (Seals, standing, skill checks), `ClusterFSmithBODPayout.CashOutGold`
(the deed's `ComputeGold` x 0.5, which `GetRewards` used to roll), `BulkOrderSystem.ComputeGold` (the 2016 bank gold).
The display reads it, and so do `ClusterFSmithBODPayout.Pay` (:170), its `CashOut` (:226), its choice gump (:278) and
`BulkOrderVendors.TurnIn` (:330). A quote is re-rolled when the deed's terms change (a bribe raises its amount or metal)
and after a restart (it is not saved); either way display and payout read the same one. Parts are rolled only when read,
so a stock turn-in that never showed anything rolls exactly what it rolled before.

The tooltip is the item's one property list, built for whoever holds it. It is refreshed when the deed changes and when
the member changes their Completed orders setting (`SetMode` -> `BulkOrderGuildPay.Refresh`); joining or leaving a guild
refreshes it on the deed's next change.

**The tooltip patch, alternatives argued:** the line has to come from `GetProperties`. (a) An override on each deed type:
pinned's `SmallSmithBOD`, `SmallTailorBOD`, `LargeTailorBOD` are pinned files (three patches instead of one) and P123's
twelve deeds would need twelve copies; (b) a partial class per type: the same twelve, and a pinned type gaining
`GetProperties` upstream would then collide; (c) an `OnEvent`: pinned raises none for property lists. One call at the end
of `SmallBOD.GetProperties` and `LargeBOD.GetProperties` (no deed type overrides either) covers all eight crafts. The
patch is made against the tree every other patch leaves and applies last (`apply-patches.sh`, the cc-P168 block).

**The hurt patch, alternatives argued** (`PlayerMobile-craft-order-hurt.patch`, one call after `Confidence.StopRegenerating`
in `PlayerMobile.OnDamage`, PlayerMobile.cs:2406, beside the bandage slip). The first version compared hit points and
the damage entries between attempts, with no patch, and its own test showed why that fails: a 10-point hit was back to
full before the attempt ended (hits 100 -> 90 -> 100 in the test world), and the Hits setter clears every damage entry at
full (pinned Mobile.cs:2032-2043), so both signals were gone. Rejected: (a) polling hit points on a fast timer: the same
regeneration can win inside one tick; (b) `Mobile.Aggressors`: only attacks by a mobile, not a fire field or a trap;
(c) an event: pinned raises none for damage. `OnDamage` runs only after the region and blessed checks let the damage
through (Mobile.cs:5970-6023), so it is exactly "took damage". The patch applies last, after every PlayerMobile patch.

**The CraftItem patch lines:** the T3's `RecordFamiliarity` needs the craft's item and system for the ingot count; the
existing hook is the only place that sees both after a success, so it gains an `else if` beside T1's and T2's (it was
already ours). The auto-fill's tool test names the T3. No other way reaches `CompleteCraft`.

## Tests

New: `server/tests/Engines/Craft/HammerCraftOrderVerification.cs` (13) and
`server/tests/Services/BulkOrders/BulkOrderGuildPayVerification.cs` (10 cases). Every craft runs the real timer chain at
an anvil and forge; random numbers are pinned where a fact needs them (0.0: every craft succeeds exceptional; 0.7 at 100
Blacksmithy: a gorget succeeds but is not exceptional). The guild-pay facts run on the live random source on purpose:
the gold is a roll, and the quote is what makes shown and paid one roll.

| Fact | Red (the break that made it fail) | Green |
|---|---|---|
| A 10-item small deed is crafted to full: 10 attempts, 10 uses, deed 10/10, 409 of 500 iron left (100 used, 9 given back by the growing familiarity) | B1 (the deed never offered the item) | yes |
| Stops at no ingots (35 ingots: deed 3, Materials) | B1 | yes |
| Stops at no uses (4 uses: deed 4, Tool) | B1 | yes |
| Stops on moving away (deed 2: the attempt in hand is refused at its end, no anvil in reach) | B1 | yes |
| Stops when hurt, even when regeneration has them back to full before the attempt ends (deed 3, Damaged) | B2 (the hurt hook ignored); before the patch it failed for real (above) | yes |
| Stop button (deed 2, Stopped) | B1 | yes |
| Exceptional-only deed: three normal gorgets stay in the pack, deed 0; then three exceptional ones go in | B1 | yes |
| Familiarity still rolls (iron 30 after 10 exceptional crafts) | B5 (the T3 never rolls) | yes |
| Large deed: the finished small deed goes in, then only the 2 missing gorgets are crafted, deed complete | B4 (no small deeds taken), B1 | yes |
| Refused: a tailor deed, a deed in the bank, the hammer not in hand | B3 (any deed, anywhere) | yes |
| Efficiency: iron at the cap, 10 used and 3 back (2.5, the fraction rolled 0.0); dull copper at 0, none back | B6 (the saving ignores familiarity) | yes |
| T2 -> T3 at the guildmaster carries familiarity (2,500 iron, 1,234 verite) and takes the costs | B7 (snapshot not loaded) | yes |
| T3 save and load: uses and familiarity | B8 (familiarity not written) | yes |
| Society bank, small and large: lines = the quote; Seals and standing paid = shown | B9 (no shared quote), B11 (no tooltip) | yes |
| Society cash out, small and large: gold and standing paid = shown | B9 | yes |
| Ask shows Seals or gold | B9 | yes |
| Non-member, small and large: the points line only, 48 high, no tooltip line; bank gold = the quote; points banked = shown | large: B9; small (its 2016 gold is the fixed buy price, no roll): B12 (everyone a member) | yes |
| Tailors' Circle member: the points line and the gold line; bank gold at the guildmaster = shown | B13 (no gold line for 2016 guild members) | yes |
| A Society member holding a tailor deed sees the non-member view | B10 (any guild counts), B12 | yes |
| The tooltip carries the member's line (read from the item's property list) | B11, B12 | yes |

**Build record** (the gated build script, `-t sl-modernuo:cc-P168`, all under the docker-build lock, released after; logs
`build*.log` in the session scratchpad):

| Run | Result |
|---|---|
| 1 | compile error: `CloseGump` needs `using Server.Gumps` (fixed) |
| 2 | 2,042 of 2,044: the large non-member deed's gold went to the bank as a check (the test counted gold piles only; test fixed), and the hurt stop (above) |
| 3, 4 | diagnosing the hurt stop: hits 100 -> 90 -> 100 inside one craft. Also one unrelated failure, `WispOrbPossessionVerification` (ForestNymph vs Phantom), which passed in every other run |
| 5 | **2,044 of 2,044** with the hurt patch |
| red 1 | breaks B1-B11 (`breaks.py` in the scratchpad): 21 failed, every one a new case; the other 2 are red 2's |
| red 2 | breaks B12, B13: the 5 expected failures |
| green | breaks reverted (no `BREAK` left in the tree, checked): **2,044 of 2,044**, the 23 new cases among them |
| image | first try 2,043: `CreatureLevelsVerification.BelowPinnedsCapTheUncappedDifficultyIsPinnedsExactly` ("TheButcher: uncapped 158.2 under pinned's cap 160"), unrelated random creature stats, green in all 8 other runs; rerun **2,044 of 2,044**, "Built sl-modernuo:cc-P168" |

**Player package:** its cliloc test (`player-package/tests/Cliloc-Overrides.Tests.ps1`) compiles inline C# with
`Add-Type -TypeDefinition` (its line 291), which this machine's SentinelOne rule forbids me to run, so it was not run.
The three-way agreement it checks was checked with a Python script instead: entries.json 12 rows, registry.csv 12, no
duplicates, every number in the block, every text equal, and `ShardClilocs.CraftThisOrder` = 1,900,011 = "Craft This
Order". The test's own map gained the entry (`:254`). Run it on a PC where it is allowed.

**Two flaky shard tests seen, not mine:** `WispOrbPossessionVerification` (run 3) and `CreatureLevelsVerification`
(image run 1), each once in ten runs.

## Deviations and decisions for Chase

1. **"Double-click then target the deed":** double-clicking the hammer stays the craft menu (near a forge) and Metal
   Familiarity (away from one), since players need both. Craft This Order is on the hammer's single-click menu, and
   choosing it gives the target cursor for the deed. If you want a double-click route as well, say which of the two
   current double-click results it should replace.
2. **The menu entry's name is a new shard cliloc** (1,900,011 "Craft This Order"), so it needs the next player package;
   until then the row is blank and cannot be clicked (as Metal Familiarity was). The craft itself needs nothing new.
3. **Shown = paid made the payout quote-based.** The deed gold is a +-10% roll, so a deed now keeps its roll from when it
   is first shown (or turned in) until it is paid. Players see the same totals as before on average; they simply cannot
   re-roll by looking. A bribe re-quotes the deed; a restart re-quotes it (the quote is not saved).
4. **The other order-giving guilds pay no currency or standing yet** (their payouts are F-18, F-20, F-25), so their
   members' line is the bank gold and says "(no guild currency or standing yet)". Members keep the points line, because
   those turn-ins do pay points.
5. **A Society member's deed gump loses the 2016 points-mode button**: the Society pays no points, so the button did
   nothing for them. The Completed orders setting is shown in its place (changed at the guildmaster, as before).
6. **T3 replaces T2's familiarity SkillMod** (one bonus per tier, as T2 replaced T1's refund): +15 flat against T2's
   +10 + up to 2.5.
7. **Damage stop** is checked between items (after each attempt), as every Craft X stop is; the attempt in hand finishes.
8. **Large deeds take the small deeds first**, then craft (see part 2): the prompt's order reversed, same end.
9. **Not refunded:** the T3 saving applies to successful crafts only.

## For Chase

**Setup:** rebuild the test shard from this branch (`sl-modernuo:cc-P168`), and build the player package and update a
test client for the menu entry's name ("Craft This Order" is our cliloc 1,900,011; an old client shows an empty, unclickable
row there, as Metal Familiarity did). Then the play tests in order, each in P115's shape:

- **P168-1, the T3 by command.** Where: test shard, a staff character beside an anvil and forge. Do: `[add
  MasterworkHammerOfHephaestus`, equip it, single-click it, open Metal Familiarity. Pass looks like: "[800/800 uses - T3
  +15 BS]", Blacksmithy +15 while held and back when unequipped, the panel titled "Masterwork Hammer of Hephaestus /
  Metal Familiarity - T3" with "Active Bonus - Resource Efficiency (Tier 3)" and a % per metal.
- **P168-2, the upgrade.** Where: a player in the Society of Smiths with a Reinforced Hammer (T2) in the pack. Do: give
  15,000 smithing standing, 100 Blacksmithy, 60 Seals, 25,000 gold, 1,000 iron, 250 Valorite; Society guildmaster, Hammer
  of Hephaestus Upgrades, "Upgrade to Masterwork Hammer of Hephaestus". Pass looks like: the T2 is gone, a T3 is in the
  pack with the T2's familiarity per metal (the panel), the costs taken; the page then shows the T3 and "T4 is not
  available yet."
- **P168-3, Craft This Order.** Where: the T3 held at an anvil and forge. Do: a small iron smith deed (`[add
  SmallSmithBOD`, or from the guildmaster) and ingots from `[TCFill`; the hammer's menu, Craft This Order, target the
  deed. Pass looks like: one "Crafting n of N: ..." line per item at normal craft speed, the progress gump titled
  "Order", the deed filling, "Craft order done. Made ... into the order (now N of N)." at the end.
- **P168-4, the stops.** Same setup, four runs: start with too few ingots; step one tile mid-run; take a hit
  mid-run (a monster, or stand in a fire field); press Stop on the progress gump. Pass looks like: "Craft order stopped: out of
  materials." / "you moved." / "you were hurt." / "Craft order stopped.", the deed keeping what was made.
- **P168-5, exceptional only.** An exceptional-only deed with a low-skill character (about 85 Blacksmithy). Pass looks
  like: normal pieces stay in the pack ("The item must be exceptional."), exceptional ones go into the deed.
- **P168-6, a large deed.** A large smith deed and a finished small deed for one of its lines in the pack. Pass looks
  like: "1 small order from your pack went into the large order.", then only the other lines' missing pieces are crafted.
- **P168-7, the saving.** With a T3 at high familiarity in one metal (`[props` won't reach it; grow it, or upgrade a T2 that
  has some), craft that metal: "Your familiarity with <metal> saved n ingots." and the ingot count agrees; a metal at 0
  familiarity says nothing.
- **P168-8, the deed lines.** A Society member: open a smith deed and hover it, once on each Completed orders setting
  (Smith guildmaster's toggle). Pass looks like: the "Society pays you" line with Seals (bank) or gold (cash out) and the
  setting line; turn the deed in and the journal's Seals/gold/standing are the numbers shown. A Tailors' Circle member
  with a tailor deed sees the points line and "Tailors' Circle pays you: n gold to the bank ...", and the bank grows by
  that n at the tailor guildmaster. A non-member sees the points line only.

**Numbers to change if wanted:** all in `HammerOfHephaestus.cs`: `MasterworkHammerOfHephaestus.MaxUses`, `RegenMinutes`,
`FamCap`, `BaseSkillBonus`, `MaxSaving`; the upgrade's `Masterwork*` constants in `HammerRestoreGump`.

## Patch notes

`CHANGELOG.md` 2026.10.21.16 (the 2026.10.21.15 section was already committed), `VERSION` bumped: four `### Added` lines
(the T3, its saving, Craft This Order, the deed pay lines) and one `### Staff` line. Wiki page not published.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`. Code: 20 files pending (14
changed; new `ClusterFCraftOrder.cs`, `BulkOrderGuildPay.cs`, the two patches, the two test files). Docs: this note.
Neither repo BLOCKED; no file over 5 MB; scratch (pinned source copy, logs, `breaks.py`) is in the session scratchpad, outside
both repos. (One comment line in `apply-patches.sh` was corrected after the dry run; it changes no file count.)

```
Repo Result
---- ------
code dry run
docs dry run
```

P168 DONE
