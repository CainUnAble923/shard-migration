# P461: Review of the Sorcerer's Dungeon Halloween port

Reviewed October 23, 2026. Notes only; no code changes.

Code checkout: `4c2af575317a96153369b1dadd19892b549eb7ea`.
Notes checkout: `fbebe834311bd1f29932ef0d81fdc2b37bc724f6`.
References: read-only ModernUO `d4531cd94b739613155225c234900de9f47d2c88` and ServUO pub57 `d76bf4443cf76d081ddaf8f57c87ff33749256af`.

Read both working agreements, the direction decision, the task list, `cc-P408-sorcerers-dungeon-halloween.md`, and `cc-P408-sorcerers-dungeon-halloween-codex-review.md` first. The earlier review's three findings are excluded here.

## Findings

Event file paths in this section are relative to `server/customizations/Services/Seasonal Events/TreasuresOfSorceresDungeon/`; other paths start at the code repository root.

1. **bug**, `server/customizations/Gumps/BaseRewardGump.cs:186`, `server/customizations/Gumps/BaseRewardGump.cs:203`, and `SorcerersDungeonRewards.cs:56`: A player with 50 points can queue multiple ring purchase confirmations while still eligible, then accept them all because confirmation gives the reward without checking the current balance and ignores a failed deduction after the first purchase (an inherited shared reward-gump defect). Recheck and successfully debit points before delivering each reward, refund on delivery failure, and test two pending purchases against one purchase's balance.

2. **bug**, `Creatures/JackThePumpkinKing.cs:217` and `Spawner.cs:151`: Jack's hatched undead never enter the spawner's cleanup list, and outstanding pumpkins keep their hatch timers through `off` or `remove`, so creatures survive or appear after shutdown even without a room change (inherited from ServUO, separate from the earlier review's rotated-room finding). Persist ownership of pumpkins and their children separately from room kill counts, remove them and cancel pending spawns at shutdown, and cover shutdown before and after hatching across a save/reload.

3. **risk**, `Creatures/JackThePumpkinKing.cs:98` and `Creatures/JackThePumpkinKing.cs:107`: The delayed callback reads the attacker's current map and position without checking the dungeon, the boss, or event state, so an attacker moved outside during the delay becomes the placement target there, including on another facet (inherited from ServUO; normal player travel timing is unverified). Require a still-active encounter and a target inside the Ilshenar dungeon, validate each placement, and test moving the target before the callback runs.

4. **bug**, `EnchantedOriginArtifacts.cs:88`: The two-argument equipment roll drops ServUO's Stygian Abyss selection, which is chosen half the time in this non-Tokuno, non-ML dungeon, so Enchanted Origin artifacts can never be boomerangs or other SA-only equipment; P408's recorded property-roll deviation does not disclose this separate pool change. Add an explicit SA-aware selector using verified available types and test its branches, or record the omitted equipment pool as an intentional deviation.

5. **risk**, `Items/EscapingAndSterlingRewards.cs:172`: The ring checks for an existing skill bonus only when first double-clicked, so two queued skill confirmations can apply different choices in sequence and overwrite the advertised one-time selection (the missing final check is inherited from ServUO). Recheck that the selected bonus slot is unset when confirming and test two pending selections against the same ring.

6. **risk**, `server/tests/Services/Seasonal Events/TreasuresOfSorceresDungeon/SorcerersDungeonVerification.cs:853` and `server/tests/Services/Seasonal Events/TreasuresOfSorceresDungeon/SorcerersDungeonVerification.cs:930`: The toy and heart assertions check only their starting art, and the pumpkin round-trip deletes both copies before hatching, so these tests still pass if the delayed effects never run. Advance `ShardTestClock` to assert the toy's 9-second opening and 5-second reset, the heart's blood ticks and stop without damage, and the restored pumpkin's single hatch and deletion.

## Evidence and limits

- Reward purchases: the shared gump checks affordability at selection (`server/customizations/Gumps/BaseRewardGump.cs:167`), but its confirmation checks only distance and the reward row (`:254`); `PointsSystem.DeductPoints` refuses overdrafts (`server/customizations/Services/PointsSystems/PointsSystem.cs:119`), and the event discards that result. Pinned `Projects/UOContent/Gumps/Base/BaseGump.cs:43` defaults `Singleton` to false, and `NetStateGumps.cs:79` retains multiple confirmations; reopening the researcher's reward list does not close them. ServUO's `Scripts/Gumps/BaseRewardGump.cs:173` has the same delivery-before-payment ordering.
- Pumpkins: the callback places an ordinary `UnholyPumpkin`; its hatch creates an ordinary mobile, moves it to the pumpkin, and deletes only the pumpkin. Neither path registers encounter ownership or checks `Enabled`; the same paths exist in ServUO's event `Creatures/JackThePumpkinKing.cs:83` and `:265`.
- Artifact pool: ServUO event `SorcerersDungeonData.cs:72` passes `LootPackEntry.IsStygian(bc)`; `Scripts/Misc/LootPack.cs:578` supplies the random half, and `Scripts/Misc/Loot.cs:783` selects the SA tables. Pinned `Projects/UOContent/Misc/Loot.cs:668` has no SA branch in this combined selector, although its SA weapon and ranged tables exist at `:9` and `:15`; the shard's `Loot-hat-types-orc-tribal-mask.patch` only extends the hat table.
- Ring: confirmation checks possession and deletion, then writes slot zero without checking its current value. ServUO's `Scripts/Gumps/ApplySkillBonusGump.cs` has the same missing final guard; this is a retained risk, not a newly introduced fidelity change.
- Missing tests: all 11 facts are in the verification file listed below, and none calls `ShardTestClock.Advance`, drives a reward purchase confirmation, or drives the ring's confirmation callback. The existing ring test writes `SkillBonuses` directly at `:841`.

No additional unexpected permanent event-item defect was found. ServUO deliberately leaves the researcher and entrance decorations after the season, and its artifacts, points, purchased rewards, and bag oddities have no seasonal expiration; P408 documents that behavior. The bag's October-only use and saved daily cooldown match its source.

This was a source review, including normalized comparison of the nine bosses' constructor values with ServUO and inspection of the relevant base classes and patches. Runtime exploit sequences, client behavior, actual travel timing, live configuration, and live world cleanup remain unverified; no builds or lane tests were requested or run, and no new tests were added. No connection to Haven, deployment, or shared-world action was made.

The required progress check completed against these work copies with output writes suppressed in memory: `progress.py --dry-run` still attempts to write `tools/progress.json`, so that write was discarded to keep this task notes-only. Repository checks confirmed no code changes and only this new notes file.

## Files reviewed

All 19 event files under `server/customizations/Services/Seasonal Events/TreasuresOfSorceresDungeon/`:

```text
Generate.cs
Spawner.cs
SorcerersDungeonData.cs
EnchantedOriginArtifacts.cs
SorcerersDungeonResearcher.cs
SorcerersDungeonRewards.cs
Creatures/AbominableSnowman.cs
Creatures/GarishGingerman.cs
Creatures/HeadlessElf.cs
Creatures/JackInTheBox.cs
Creatures/JackThePumpkinKing.cs
Creatures/NightmareFairy.cs
Creatures/RabidReindeer.cs
Creatures/StockingSerpent.cs
Creatures/TwistedHolidayTree.cs
Items/EscapingAndSterlingRewards.cs
Items/JackInTheBox.cs
Items/JacksBagOfTricks.cs
Items/ShackledHeartOfThePumpkinKing.cs
```

Tests and supporting shard files:

```text
server/tests/Services/Seasonal Events/TreasuresOfSorceresDungeon/SorcerersDungeonVerification.cs
server/tests/Route/ShardTestClock.cs
server/customizations/ClusterFSeasonalSwitch.cs
server/customizations/Services/PointsSystems/PointsSystem.cs
server/customizations/Services/Revamped Dungeons/BlackthornDungeon/Items/MinaxArtifacts.cs
server/customizations/Mobiles/NPCs/BaseTurnInMobile.cs
server/customizations/Gumps/BaseRewardGump.cs
server/customizations/Items/Containers/RewardBackpack.cs
server/patches/Loot-hat-types-orc-tribal-mask.patch
server/patches/PlayerMobile-fountain-luck-bonus.patch
```

P461 DONE
