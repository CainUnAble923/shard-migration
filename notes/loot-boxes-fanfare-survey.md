# Loot boxes and fanfare: Step 0 survey (cc-P79, F-40 and F-41 phase 1)

Written 2026-10-13, before any code. A research subagent did the reading; its citations are kept as given. I re-read
`ClusterFAchievements.cs` (the grant functions and `TryGrant`) and pinned's `Effects.cs` and `GetLootingRights`
myself.

Short names:
- **C** = `D:\ShatteredLegacy\server\customizations`.
- **P** = `D:\UO\ModernUO-pinned\Projects`, at `d4531cd94b739613155225c234900de9f47d2c88`.

## 1. The achievement system (`C\ClusterFAchievements.cs`)

**Definitions.**
- `AchievementDef` (:159-241) has these fields: `Key`, `Title`, `Description`, `FlavorText`, `Category`, `AP`,
  `Renown`, `ItemGumpId`, `Hidden`, `PrerequisiteKey`, `RewardItems`, `ProgressCounter`, `Trigger`, `Retired`.
  **There is no difficulty field.**
- **Flavor text** is `FlavorText`.
- **The plain-text parenthetical** is generated from the trigger: `EarnedLine => $"(Earned: {Trigger.Describe()})"`
  (:213; `Describe` :95-139).
- **The table** is `RegisterAll()` (:288-1019), with `Reg(...)` calls into `_defs` (:264). It holds **74
  achievements, 6 retired, 68 live**.
- **Categories:** Combat, Skills, Exploration, Mining, Crafting, Legacy, Discovery, Collection, League (:144-155).

**How they fire.**
- `GrantCounted`, `GrantEvent` and `GrantSkills` all call `TryGrant(IAccount, key)` (:1111-1133).
- **The callers:**
  - login (:1233);
  - player death (:1272);
  - creature death (`[OnEvent(CreatureEvents.CreatureDeathEvent)]`, :1279, `NotifyKill` :1163);
  - mining, maps, crafting and smelting notifiers (:1323-1404);
  - the League (`ClusterFLeagueSystem.cs` :106, :122, :139, :207).
- **What a grant does:** it adds AP, grants Renown (`RenownSource.Achievement`), spawns reward items, and shows
  `AchievementEarnedGump` to the first online character (`NotifyOnlinePlayer` :1430-1440). It plays no sound, no
  effect and no broadcast.

**Where earned achievements are stored: per account only**, `_earned[username]` (:267-269), persisted by
`ClusterFAchievementPersistence` (:1567-1647). **There is no per-character or per-loop record.** `TryGrant` takes
the account, not the character.

**Gumps.**
- `AchievementEarnedGump` (:1656-1711): the earn popup.
- `AchievementsGump` (:1727 on): the page, opened by `[achievements` (:1475-1482).

## 2. Hooks that exist and do not

| Source | Exists? | Where, or what is missing |
|---|---|---|
| Player levels, level-up | **No** | no player level in code; F-12 is notes only (`notes/f12-levels-loops-caps.md`) |
| Loops, loop completion | **No** | "until loops exist" (`ClusterFGuildStarterPath.cs:13-14`) |
| Loop scroll item | **No** | no `LoopScroll` type |
| League ranks, rank-up | **Yes** | `ClusterFLeagueRanks.TryPromote` (:344-385); the rank is set at :376 (`...Rank = report.To`). Staff path `SetRank` (:208-219). Per character (`CharacterLeagueData.Rank`). 17 ranks, Iron to Celestial |
| League trial chapters | **No completion** | `TrialsDone` is only read by `Evaluate` (:297); all six chapters are waived by setting |
| Boss kills | **Partly** | no `IBoss`. The de facto list is `ClusterFRareSelfRepair.IsHighEndSource` (:57-60): paragon, `BaseChampion`, `Harrower`, `BasePeerless` (ours, with `BaseSABoss`), `DespiseBoss`, `ShameGuardian`, `NavreyNightEyes`, `IRareSelfRepairSource`. Death event: `CreatureEvents.CreatureDeathEvent`; looting rights `BaseCreature.GetLootingRights` (P `BaseCreature.cs:3344`) |
| Dungeon or floor clears | **No** | no clear tracking |
| Reaching 200 | **No hook** | the skill cap is 200 (`ClusterFSkillCaps.cs:11`); "skills.master" is checked only at login. The fanfare lines read as **level** 200 (an F-12 end state), which does not exist |

## 3. Hue ladders (all in our replacement `C\ResourceInfo.cs`; `CraftResources.GetHue` :1222-1227)

**Metal:**

| Metal | Hue | Metal | Hue |
|---|---|---|---|
| Iron | 0 | Platinum | 0x481 |
| Dull Copper | 0x973 | Toxic | 0x4F6 |
| Shadow Iron | 0x966 | Blaze | 0x026 |
| Copper | 0x96D | Frost | 0x76D |
| Bronze | 0x972 | Obsidian | 0x455 |
| Gold | 0x8A5 | Mythril | 0x22C |
| Agapite | 0x979 | Adamantium | 0x413 |
| Verite | 0x89F | **Celestial** | **0x8AF** |
| Valorite | 0x8AB | | |

Dawnstone (0xA5B) is off the ladder.

**Leather (AOS table):** Normal 0, Spined 0x8AC, Horned 0x845, Barbed 0x851. Burrowhide (0x71D) is a starter
leather, not a tier above Barbed. **No leather tier above Barbed exists.**

**Wood:**

| Wood | Hue | Wood | Hue |
|---|---|---|---|
| Oak | 0x7DA | Ghostwood | 0x47E |
| Ash | 0x4A7 | Emberbark | 0x058 |
| Yew | 0x4A8 | Frostbark | 0x76E |
| Heartwood | 0x4A9 | Shadowbark | 0x544 |
| Bloodwood | 0x4AA | Runewood | 0x060 |
| Frostwood | 0x47F | Voidwood | 0x22E |
| Ironwood | 0x966 | Starwood | 0x4EC |

Rootwood is a starter wood.

## 4. Guarded region and house access (pinned)

- **Guarded:** `m.Region.GetRegion<GuardedRegion>() is { } g && !g.IsDisabled()`. `GuardedRegion.IsDisabled` is at
  P `UOContent\Regions\GuardedRegion.cs:50`; `Region.GetRegion<T>` at P `Server\Regions\Region.cs:458`; the same test
  is used at `Moongate.cs:196`.
- **House:** `BaseHouse.FindHouseAt(Mobile)` (P `BaseHouse.cs:1421`). `IsOwner` (:3559) includes GameMaster and, under
  AOS, the same account; `IsCoOwner` (:3563) includes the owner; `IsFriend` (:3612) includes co-owners. So
  `house.IsFriend(m)` alone covers owner, co-owner and friend.

## 5. Account-bound items

**None on the shard.** The closest pinned model is `Item.Nontransferable` (P `Item.cs:569`, true for quest items).
It refuses:
- a world drop (`OnDroppedToWorld` :3743);
- a drop onto a mobile (`OnDroppedToMobile` :3632);
- a drop into any container but the dropper's own backpack (`OnDroppedInto` :3649, which also covers trade windows,
  banks and sub-bags);
- a drop onto an item (`OnDroppedOnto` :3665).

Other virtuals: `AllowSecureTrade` (:1884), `VerifyMove` (:2277). Nothing pinned binds an item to an *account*, so
the box needs its own owner-account field checked in those virtuals.

## 6. Delivery and Renown

- **Pack, else bank:** `ClusterFGuildPromotion.Deliver(pm, item)` (cc-P78): `Backpack.TryDropItem`, else
  `BankBox.DropItem`, with a message saying where.
- **Renown:** `ClusterFAccountData.GrantRenown(int, RenownSource)` (:539-547).

## 7. Effects and messages (pinned)

- **The FireworksWand** (P `Items\Weapons\Maces\FireworksWand.cs`):
  - launch: moving effect 0x36E4;
  - burst: `SendLocationEffect` 0x373A + 0x10 * (0 to 3), sounds 0x11B to 0x11E;
  - hues 0x66D, 0x482, 0x47E, 0x480, 0x47F.
- **Location effects:** `Effects.SendLocationEffect(p, map, itemID, duration, speed, hue, renderMode)`
  (P `Server\Effects.cs:130`) builds `OutgoingEffectPackets.CreateLocationHuedEffect` and sends it to the area.
  For one player only, the same packet can go to that player's `NetState` alone.
- **Private sound:** `Mobile.SendSound`.
- **Shard-wide message:** `World.Broadcast(hue, ascii, text)` (P `World.cs:130`).
- **Overhead text:** `PublicOverheadMessage` and `PrivateOverheadMessage` (P `Mobile.Messages.cs:119`, :150).

## 8. Character level, Fiddle-Me-This

- **No character level in code.**
- **No Fiddle-Me-This gump replacement** in our code or pinned. It is a client-side art pack that replaces gump art
  3500 to 3508 (the brief's note).

## 9. Settings and storage

- **Settings:** `ServerConfiguration.GetOrUpdateSetting(key, bool)`.
- **Player commands:** `[ShardCommand(CommandCategory.Player)]` (`ClusterFSelfResurrect.cs:9-30`).
- **Per-character data** lives in `ClusterFAccountData` (hand-serialized, version 17 since cc-P78), keyed by
  character serial: `CharacterGuildData`, `CharacterLeagueData`, `GuildStarterRecord`. There is no mute flag
  anywhere yet.

## What this means for the build (decisions taken; details in cc-P79-loot-boxes-fanfare.md)

- **Achievements are per account.** A box fires on the account's first earn (`TryGrant` returning true) and goes to
  the account's online character, the same one the earn popup goes to. Per-character, per-loop records are kept
  anyway, so that when loops (F-12) let achievements be earned again, repeats find their count. A second character on
  the same account gets no box for an achievement the account already holds, because the account system never fires
  for it. Decision for Chase.
- **Hooks left for the missing sources:** level-up, loop completion, dungeon or floor clear, League trial chapter,
  reaching 200, the loop scroll combine.
- **Hooked now:** achievements, League rank-up (`TryPromote`), boss first kills (`CreatureDeathEvent`).
