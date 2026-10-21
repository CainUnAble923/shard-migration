# cc-P263: the "Noted by the System" hidden achievements (the exploit and barefoot set)

Copper Golem, 2026-10-21. Server only. Branch `golem/Copper/P263` in both repos. Image `sl-modernuo:cc-P263`.
Source list: `cc-prompts/design/f-exploit-achievements-accessory-slots.md`, first section.

## Headlines

- **45 hidden achievements, all in P231's Mischief category.** P231 is in main, so its category is used.
  - **40 are hooked** to real game events.
  - **5 are data only**: hidden, and nothing can award them yet.
  - Each one shows a snarky flavor line, then the plain "(Earned: ...)" line written from its trigger (D73).
- **Nothing duplicates an earlier achievement.**
  - Dressed for the Occasion and Creature of Habit already exist (P82), so they are not added again.
  - Plate Bottoms Only, Iron Soles, Ring Bearer, Fully Accessorized and Smothered belong to P262 and are left to it.
  - The list's "Planned Obsolescence" title is already P231's (100 worn-out tools). The recycle pair here is named
    **Built to Be Recycled** / **Circular Economy** instead. A test checks that every Noted title is unique.
- **Rewards are data** (`NotedRewards.Table`, below, for Chase to approve):
  - 18 rows give a **Dented Box**. It replaces that achievement's usual earn box: a tier 1 roll with one guaranteed
    joke item.
  - 3 rows give a **title**: Larry, the Supervisor, the Brave (citation needed). A title shows in the title picker
    only once it is held.
- **17 joke items are built**, on stock graphics and hues. They have zero stats, are blessed, and are bound to the
  earner's account. 6 more need art or live data (listed below).
- **Fix instead of reward:**
  - **Store-Bought: fixed.** Bulk orders and smith commissions now take only player-crafted items.
  - **Reroll Goblin: fixed.** Commissions exist, and abandoning one was free, so an abandon now holds back the next
    request for 5 minutes.
  - **Sandbagger:** described only, not changed.
- **Found, not fixed (for Chase): P79's boss loot box never fires in play.** See "Finding" below. My own boss checks
  work around it.
- **Tests:** 9 new facts in `server/tests/Misc/NotedBySystemVerification.cs`, one per event family and more.
  - `docker/uo/build.sh -t sl-modernuo:cc-P263` was green: **2,002 tests, 1,998 passed, 0 failed, 4 skipped**. All 8
    new patches applied.
  - Four existing BOD test files now mark their test items as crafted (the Store-Bought rule).
  - The achievement count test moves from 95 to 140.

## What changed

ShatteredLegacy repo:

| File | What |
|---|---|
| `server/customizations/ClusterFNotedBySystem.cs` (new) | The 45 definitions (`RegisterNoted`, a partial of `ClusterFAchievementSystem`). `NotifyNoted` / `NotifyNotedStreak` / `FirstTimeFor` (counters on the account). `NotedReward` and `NotedRewards.Table` (the reward data). The hook class `ClusterFNotedBySystem`: deaths, travel, pets, crafting, mining, steps, boxes, commissions, rewards (`OnEarned` adds a title, `Dent` makes the Dented Box). |
| `server/customizations/LootBoxes/NotedJokeItems.cs` (new) | `LootBox.Dent` (the Dented Box), `INotedJoke`, the 12 deco items (`NotedJokeDeco` base) and the 5 wearables. |
| `server/customizations/ClusterFStoreBought.cs` (new) | The crafted-only rule and its setting `clusterf.bods.craftedOnly` (default true). |
| `server/customizations/ClusterFAchievements.cs` | 32 `TriggerKind`s (27 hooked, 5 data only) and their "(Earned: ...)" wording. `RegisterNoted()` after `RegisterJokes()`. `TryGrant` calls `ClusterFNotedBySystem.OnEarned` (titles). |
| `server/customizations/LootBoxes/ClusterFLootBoxes.cs` | `OnAchievementEarned`: a row with a joke item gives its tier, then dents the box. |
| `server/customizations/LootBoxes/LootBoxItems.cs` | `OnDoubleClick` refusal calls `BoxRefused` (Can't Wait). `Open` calls `BoxOpened` (Superstitious, Edge Lord, Unboxing Video). |
| `server/customizations/LeagueShop/LeagueShop.cs`, `LeagueShopGumps.cs` | `TitleDef.Secret`. The three Noted titles. The picker skips a secret title until held. |
| `server/customizations/ClusterFSmithCommissions.cs` | `IsMatch` / `IsMatchForPieceKey` refuse store-bought items. `Complete` calls `CommissionCompleted` (Pre-Crafted). The abandon cooldown (`AbandonCooldown`, `Abandoned`, `RequestCooldownLeft`, setting `clusterf.commissions.abandonCooldownMinutes`, default 5); `Generate` refuses during it. `IssuedAt` now reads `Core.Now`, the server clock; it was `DateTime.UtcNow`, the same time in play. |
| `server/customizations/SmithCommissionGump.cs` | Request says how long the wait is. Abandon starts the cooldown. |
| `server/customizations/LargeBODItemFill.cs` | A large deed's direct item fill refuses store-bought items. |
| `server/customizations/SmithGuildSalvageBag.cs` | Recycle hook before the item is deleted. |
| `server/customizations/Services/Pet Training/PetTrainingHooks.cs` | `OnTamed` calls `Tamed` (Commitment Issues). |
| `server/patches/Mining.cs` (our full replacement) | `CheckResources` override: a swing refused by an empty vein counts (the swing's own check only, not the timed re-checks). |
| `server/patches/` 8 new | `Recall-arrival-achievement`, `Moongate-arrival-achievement`, `Runebook-full-achievement`, `PetOrders-release-achievement`, `CraftItem-fail-streak-achievement` (4 one-line sites: 2 success, 2 fail, in both CompleteCraft overloads), `Resmelt-recycle-achievement`, `SalvageBag-recycle-achievement`, `SmallBOD-crafted-only`. Each adds one call. Made against the fully patched tree, so they go last. |
| `docker/uo/apply-patches.sh` | The 8 `apply_patch` lines, last, with their reason. |
| `server/tests/Misc/NotedBySystemVerification.cs` (new) | 9 facts. |
| `server/tests/Misc/AchievementEarnedLineVerification.cs` | Counts 95 to 140. |
| `server/tests/Misc/BODCombineContainedVerification.cs`, `PostValoriteBODMaterialVerification.cs`, `LargeBODItemFillVerification.cs`, `server/tests/Services/BulkOrders/BulkOrderSystemVerification.cs` | Their test items are `PlayerConstructed = true` (crafted, as orders now require). |
| `CHANGELOG.md`, `VERSION` | New section 2026.10.21.12 (Added, Changed, Staff). VERSION goes from 2026.10.21.11. |

## The achievements

AP and Renown are small, as P231's are. "Box" means the usual earn box. "Dented" means the Dented Box with the named
item. Hooked = earned in play now.

| Achievement (key `noted.*`) | Earned by | Status | AP / R | Reward |
|---|---|---|---|---|
| Geography Major | killing a melee creature that never damaged you | hooked | 5/1 | box |
| Rock Enthusiast | 50 of those | hooked | 15/2 | Dented: Strategic Boulder |
| Tactical Retreat | arriving by recall or gate under 10% hits while in combat | hooked | 5/1 | box |
| Professional Coward | 25 of those | hooked | 15/2 | Dented: Cloak of Hasty Departure + title "the Brave (citation needed)" |
| Not My Problem | a creature you provoked kills another, no damage from you on it | hooked | 5/1 | box |
| Somebody Else's Problem | 100 of those | hooked | 15/2 | Dented: Bucket of Popcorn |
| Last Hit Larry | a boss's killing blow with under 1% of its damage | hooked | 10/1 | box + title "Larry" |
| Acceptable Losses | your pet dies while you are at full hits | hooked | 5/0 | box |
| Meat Shield Procurement | 10 of those | hooked | 15/1 | Dented: "World's Okayest Owner" nameplate |
| Middle Management | a companion's killing blow on a boss you fought | **data only**: no companions | 10/1 | Dented: Squire's Necktie + title "the Supervisor" |
| Commitment Issues | release a pet and tame it back within 5 minutes | hooked | 5/0 | box |
| It's Complicated | 10 of those | hooked | 15/1 | Dented: Friendship Bracelet |
| Remote Work | your pet kills while you are hidden or 15+ tiles from it | hooked | 5/1 | box |
| Bare Minimum | a boss's killing blow barefoot, in armor | hooked | 10/2 | box |
| Built to Be Recycled | recycling a crafted item within 60 s of its making | hooked | 5/0 | box |
| Circular Economy | 1,000 of those | hooked | 15/2 | box |
| Skill Issue | the same craft failed 10 times in a row | hooked | 5/0 | box |
| Persistence Is Not a Strategy | 25 in a row | hooked | 15/1 | Dented: Participation Trophy (engraved with the streak) |
| Quality Control | recycling an exceptional item within 10 s of crafting it | hooked | 10/1 | box |
| Rock Bottom | 20 swings in a row at an empty vein, same tile | hooked | 5/0 | box |
| Still Nothing | 100 in a row | hooked | 15/1 | Dented: The Rock |
| Any% Speedrun | 10 recalls in 60 s | hooked | 10/1 | Dented: Dizzy Runebook |
| Wrong Turn | dying within 10 s of a recall or gate arrival | hooked | 5/0 | box |
| Directionally Challenged | 10 of those | hooked | 15/1 | Dented: Souvenir Toe Tag |
| Rune Hoarder | filling a runebook (each book counts once) | hooked | 5/1 | box |
| Rune Archivist | 10 books | hooked | 15/2 | box |
| Ambition Exceeds Capacity | 100 steps overweight | hooked | 5/0 | box |
| Beast of Burden | 1,000 steps | hooked | 15/1 | box |
| Mule Train | 3+ pack animals (horse, llama, our pack mule) following, packs 90%+ full | hooked | 10/1 | Dented: Mule's Sunhat |
| Hot Foot | 25 lava or fire tiles barefoot, in armor | hooked | 10/1 | box |
| Frostbitten | 500 snow tiles barefoot, in armor | hooked | 10/1 | box |
| Pantsless Wonder | 1,000 tiles in armor and boots with no leg armor | hooked | 10/1 | box |
| Home Sweet Grave | dying in a house you own or co-own | hooked | 5/0 | box |
| Haunted Property | 5 of those | hooked | 15/1 | Dented: Personalized Tombstone |
| Hoarder | house storage at 100% | hooked | 10/1 | box |
| Superstitious | 5 loot boxes in a row opened from one tile of your house | hooked | 5/0 | box |
| Lucky Spot | 25 in a row | hooked | 15/1 | Dented: Lucky Rug |
| Can't Wait | 10 tries to open a box where it won't open | hooked | 5/0 | Dented: Box-Shaped Box |
| Edge Lord | opening a box within 1 tile of a guard zone's edge | hooked | 5/1 | box |
| Unboxing Video | opening a box with another player within 3 tiles | hooked | 5/1 | Dented: Box of Smaller Boxes |
| Pre-Crafted | a smith commission turned in within 60 s of being issued | hooked | 10/1 | box |
| Deja Vu | regaining a previous loop's skill peak within 24 h of looping | **data only**: no loops | 10/1 | box |
| Procrastinator | 7 days at cap, full experience bar, not looping | **data only**: no levels or loops | 10/1 | Dented: Hourglass of Eventually |
| Cold Feet | starting the League loop and backing out 3 times | **data only**: no League loop process (so no cancel step to check) | 10/0 | box |
| Infamous | letting 5 commissions expire | **data only**: commissions never expire | 5/0 | box |

Also in the table: P82's **Creature of Habit** gives a Dented Box with **Lucky Underwear**. That is the list's
"Lucky Underwear (+0 Luck)", and it is the only change to an existing achievement.

**Skipped from the list:**
- Dressed for the Occasion and Creature of Habit (P82 has them).
- The five accessory and barefoot ones P262 owns.

**Missing hooks for the data-only five:**

| Achievement | Hook it needs | Trigger kind |
|---|---|---|
| Middle Management | a companion's kill event; there is no companion type | `CompanionBossKill` |
| Deja Vu | F-12's loop event and per-loop skill peaks | `PeakRegained` |
| Procrastinator | a daily check of "at cap with a full bar"; there are no levels or experience bar | `ProcrastinatedDays` |
| Cold Feet | the League loop process with a cancel step | `LoopBackedOut` |
| Infamous | commission expiry; `SmithCommissionEntry` has `IssuedAt` but nothing ever expires it | `CommissionsExpired` |

Each needs only `ClusterFAchievementSystem.NotifyNoted(pm, TriggerKind.X)` at its event.

**Names I chose, for Chase to change** (the list gives none):
- The follow-up tiers: Somebody Else's Problem, It's Complicated, Circular Economy, Persistence Is Not a Strategy,
  Still Nothing, Directionally Challenged, Rune Archivist, Beast of Burden, Haunted Property, Lucky Spot.
- The snow variant: "Frostbitten" (the list says it needs a name).
- Built to Be Recycled, used for the recycle base tier because P231 has "Planned Obsolescence".
- All flavor lines.

**Where the follow-up counts come from:** the list writes "Name (xN): do X" (for example "Skill Issue (25 in a row):
fail ... 10 times"). I read X as the base tier and N as the follow-up tier.

**How some list items were interpreted:**
- **"In armor" for the barefoot set** means an armor chest piece is worn. P262's barefoot rule (4+ armor slots, legs
  and chest) is on its own branch, not in main, so this one is simpler. When both are in main, they could share one
  definition.
- **Plate Socks** do not count as bare feet here. They are P262's item.
- **"Your own crafted item"** means `PlayerConstructed`. Pinned records the maker only when the maker's mark is used
  (`Crafter` is a name). Under a minute old in your pack makes it yours in practice.

## The reward table (for Chase to approve)

`NotedRewards.Table` in `ClusterFNotedBySystem.cs`, one row per achievement. A row can give:
- a `JokeItem`: makes the earn box a Dented Box at `BoxTier`, 1 for all rows (tier 1 is the smallest box);
- a `TitleKey`: adds that title when the achievement is earned.

Achievements without a row get the usual earn box from the loot table.

| Achievement | Dented Box joke item | Title |
|---|---|---|
| Creature of Habit (P82) | Lucky Underwear | |
| Rock Enthusiast | Strategic Boulder | |
| Professional Coward | Cloak of Hasty Departure | the Brave (citation needed) |
| Somebody Else's Problem | Bucket of Popcorn | |
| Last Hit Larry | (usual box) | Larry |
| Meat Shield Procurement | "World's Okayest Owner" nameplate | |
| Middle Management (data only) | Squire's Necktie | the Supervisor |
| It's Complicated | Friendship Bracelet | |
| Persistence Is Not a Strategy | Participation Trophy | |
| Still Nothing | The Rock | |
| Any% Speedrun | Dizzy Runebook | |
| Directionally Challenged | Souvenir Toe Tag | |
| Mule Train | Mule's Sunhat | |
| Haunted Property | Personalized Tombstone | |
| Lucky Spot | Lucky Rug | |
| Can't Wait | Box-Shaped Box | |
| Unboxing Video | Box of Smaller Boxes | |
| Procrastinator (data only) | Hourglass of Eventually | |

**How the titles show:** they are League titles with `FreeAtAp -1` and a new `Secret` flag, so they appear in the title
picker only once held. On the character they show after the name: "Chase Larry", "Chase the Supervisor".

**One decision for Chase:** should a Dented Box replace the usual earn box (built this way), or come in addition to it?
Replacing is what "small roll" suggests.

## The joke items

**Built.** All blessed, bound to the account, zero stats, no effect:

| Item | Graphic, hue | Notes |
|---|---|---|
| Lucky Underwear | short pants 0x152E, hue 0x21 | wearable; property line "+0 Luck" (a line only) |
| Strategic Boulder | rock 0x1363 | "It has never once been reached" |
| Cloak of Hasty Departure | cloak, hue 0x496 | wearable |
| Squire's Necktie | body sash, hue 0x26 | wearable |
| Friendship Bracelet | gold bracelet, hue 0x30 | wearable; line "Returnable" (a line only); no attributes, so worn in an extra slot (P262) it adds nothing |
| "World's Okayest Owner" nameplate | brass sign 0x0BD2 | |
| Bucket of Popcorn | bucket 0x14E0, hue 0x35 | |
| Participation Trophy | bronze trophy cup 0xB4D1 | engraved with the earner's name and best fail streak |
| The Rock | rock 0x1368 | |
| Personalized Tombstone | gravestone 0x1165 | "Here lies <name>. Again. At home." |
| Mule's Sunhat | straw hat, hue 0x499 | wearable |
| Lucky Rug | rug tile 0x0AB3 | |
| Souvenir Toe Tag | blank scroll 0x0E34 | engraved with the name |
| Dizzy Runebook | runebook graphic 0x22C5 | deco only, holds no runes |
| Hourglass of Eventually | hourglass 0x1810 | |
| Box-Shaped Box | small box 0x09A8 | deco, not a container |
| Box of Smaller Boxes | wooden box 0x09AA | deco, not a container |

**Binding.** A deco item may stand on a floor or in a chest, for display in the earner's house. Only the earner's
account can lift it, and it never goes into another character's pack. A wearable follows the box cosmetics' rules:
carried only by its account.

**Graphics.** The graphics were checked against the shard client's tiledata. None of them was looked at in game.

**Need art or live data (not built):**
- **Memorial Plaque (lists dead pets):** needs pet names recorded at death. The count exists; the names are not kept.
- **Your Permanent Record (live Infamy):** needs commission expiry and an Infamy value. Neither exists.
- **Barrel Pants:** need a wearable barrel. No stock graphic exists.
- **The Rock and Strategic Boulder as real boulders:** the big boulder art (0x11B6) is a static, so a small rock
  stands in.
- **Plate Socks, Singed Toe Ring, Mood Toe Ring:** P262's items.

## Fix instead of reward

**Store-Bought: fixed.**
- **Before:** pinned's `SmallBOD.EndCombine` (Engines/Bulk Orders/SmallBOD.cs:126-181) checks type, material and
  quality only. So does our large deed's direct item fill (`LargeBODItemFill`, written to match it), and so do our
  commissions (`IsMatch`). An NPC smith's iron stock filled plain iron orders.
- **Pinned already tells crafted from bought:** Resmelt says "store-bought" (cliloc 500418) for an item that is not
  `PlayerConstructed`.
- **Now:** a small deed (`SmallBOD-crafted-only.patch`), a large deed's item fill and a commission (small and large
  pieces) refuse an armor, weapon or clothing item that is not `PlayerConstructed`. The refusal says "System: That was
  bought, not made. Orders take only items crafted by a player."
- **Flag:** loot is not crafted either, so loot no longer fills orders.
  - Set `clusterf.bods.craftedOnly` to false to turn the rule off.
  - Only a vendor-sale stamp would separate loot from bought items, and pinned has none.

**Reroll Goblin: fixed.**
- Commissions exist (`ClusterFSmithCommissions`), and Abandon was free and instant. A player could abandon and request
  again until the best requester and reward came up.
- An abandon now holds back the next small-commission request for 5 minutes (`clusterf.commissions.abandonCooldownMinutes`).
  The Request button says how long is left.
- The wait is kept in memory per character, so a restart clears it. Large commissions are not covered.

**Sandbagger: described only, not changed.**
- Box contents scale with the character's level (`ClusterFLootBoxes.LevelOf`: total Base skill / 10, a stand-in until
  F-12).
- So a player can put off easy achievements until a high level and get a bigger box for the same deed.
- The list's fix is to scale by the achievement's tier, with level as a smaller modifier. The tier already comes from AP
  (`LootTable.TierForAchievement`), so the change would be in `LootBoxRoller.Roll`'s use of level. Not touched here, as
  the prompt says.

## Finding (for Chase): the boss loot box never fires in play

- **The cause:** pinned's `Mobile.OnDeath` deletes an NPC (`if (!m_Player) Delete()`) before `BaseCreature.OnDeath`
  raises `CreatureDeathEvent`.
- **The effect:** by that event the creature reads `Deleted`, so `ClusterFLootBoxes.IsBoss` is false for every boss.
  `IsBoss` calls `ClusterFRareSelfRepair.IsHighEndSource`, which wants `Deleted: false`. So P79's first-kill boss box
  (`ClusterFLootBoxes.OnCreatureDeath`) never awards.
- **Any other `CreatureDeathEvent` handler** that reads a pet's master, or an `IsHighEndSource` check, has the same
  problem.
- **What this prompt does:** my handlers use `CreatureDeletedEvent` instead. It fires from `BaseCreature.OnDelete`,
  first, with the master, the damage entries and `LastKiller` still there. A creature deleted there with no hits left
  is dying. A bonded pet, which is not deleted, keeps `CreatureDeathEvent`.
- **The fix for P79** would be the same move. I did not make it, because it is outside this prompt.

## Tests

`server/tests/Misc/NotedBySystemVerification.cs`, 9 facts. Each one drives the game's own path where the test host
can: real kills, a moongate, runebook drops, Mining's resource check on an emptied vein, loot box double-clicks, deaths
in a test house, and commission turn-ins.

Two things cannot be driven in the test host, so the facts call the hook the patch calls:
- a craft's success roll is random;
- a recycle needs a forge.

| # | Family | Shows |
|---|---|---|
| 1 | combat | Geography Major from a real kill. An orc that hit you, or a mage, does not count. Hidden before, listed with [Secret] and its Earned line after. A second kill adds no AP. |
| 2 | bosses | One killing blow on Barracoon earns both Last Hit Larry (and its title) and Bare Minimum. A shod, full-damage kill earns neither. Earned once. |
| 3 | pets, provocation | Not My Problem (not when you hit the victim too). Acceptable Losses (not when hurt). Remote Work (not when near and visible). Commitment Issues within 5 minutes, not after 6. |
| 4 | travel, steps | Tactical Retreat through a real moongate (not at full hits). Wrong Turn from a death 3 s later. Any% at exactly the 10th recall. Rune Hoarder at the 16th rune (the same book again does not count). Overweight steps; lava barefoot; pantsless in boots (not with leg armor). A turn in place is not a step. |
| 5 | crafting, mining | Skill Issue's streak resets on a success or a different item. Fresh crafted recycling counts; old or bought does not. Quality Control. Rock Bottom on an emptied vein at the 20th swing (timed re-checks do not count). |
| 6 | housing | Home Sweet Grave. Hoarder at full storage, not before. Superstitious (a step aside starts over). Lucky Spot's earn box is a tier 1 Dented Box holding a Lucky Rug bound to the account. |
| 7 | boxes | Can't Wait at the 10th refusal, and its earn box is a Dented Box with a bound Box-Shaped Box in a rare slot. Edge Lord at a guard edge, not in the middle of town. Unboxing Video with another player nearby. |
| 8 | commissions, orders | A bought item does not match a commission; a crafted one does. Pre-Crafted at 20 s, not at 90 s. A small deed refuses a bought sword and takes a crafted one. The abandon cooldown holds back Generate until it passes. |
| 9 | data only, secrets | The 5 unreachable ones are hidden. All 45 are hidden, in Mischief, and have a flavor line; every title is unique. Every reward row names a real achievement. Every joke item is blessed and statless. Larry is not in the title picker until held. |

Runs:
- **First runs:** 40 failures, all from four existing BOD test files whose items are not crafted (the Store-Bought
  rule). Those test items are now `PlayerConstructed`.
- **My own facts** failed on the way for real reasons, each fixed:
  - the death event order (Finding above);
  - `IssuedAt` on the wall clock;
  - a dog placed 31 tiles away;
  - Larry's damage share in the test.
- **Two runs** failed `CreatureLevelsVerification.BelowPinnedsCapTheUncappedDifficultyIsPinnedsExactly`. That is the
  known flake fixed in P355, which is not in main yet. It is not touched here.
- **Final:** `--tests-only` and the full build both passed: 2,002 tests, 1,998 passed, 0 failed, 4 skipped. "Built
  sl-modernuo:cc-P263 with patches applied and 1998 shard test(s) passing."

## For the merge

P262 (accessory slots) is still on its branch and touches some of the same places:
- the achievement counts in `AchievementEarnedLineVerification` (95 to 100 there, 95 to 140 here; merged, it is 145);
- `LeagueShop.cs` and `LeagueShopGumps.cs` (different lines);
- `CHANGELOG.md` and `VERSION`.

Expect conflicts there; both sides survive.

## Not hooked (could be)

- **Sacred Journey** (Chivalry's recall): the recall patch covers Magery's Recall and runebook recalls only.
- **Tailoring cuts and other recycles:** the recycle hooks cover smelting, pinned's salvage bag and the Smith Guild
  salvage bag, not scissors on clothing.
- **Rock Bottom on other harvest systems:** counts mining (ore and sand) only, not lumberjacking.

P263 DONE
