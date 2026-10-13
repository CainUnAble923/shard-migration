# cc-P79: F-40 loot boxes and F-41 fanfare, phase 1

Run 2026-10-13 by Claude Code (autopilot hand-off after P78). Builder. The brief's `docs\` targets live here; agents
never edit `docs\`.

Sources:
- The Step 0 survey, written before any code: **`notes/loot-boxes-fanfare-survey.md`**.
- Pinned `D:\UO\ModernUO-pinned` at `d4531cd94b739613155225c234900de9f47d2c88`.
- Code repo `D:\ShatteredLegacy`, built as `sl-modernuo:cc-p79`. Not deployed, not committed, `latest` unchanged
  (8863156884f8).

Phase 1 is server side only: stock UO effects and sounds, overhead and System text for the voice, no client data.

## What was built

All new code is in `server/customizations/LootBoxes/`.

| File | What |
|---|---|
| `ClusterFLootTable.cs` | All box numbers in **`Configuration/loot-boxes.json`**: slots, gold, Renown, pool weights, rarity names and hues, the metal, leather and wood ladders, tier by source, achievement category to theme, abandoned-box days. A missing file is written with the defaults; a bad file is refused whole and the table in force is kept (cc-P48's League ladder pattern) |
| `ClusterFFanfare.cs` | The fanfare service; the line pools in **`Configuration/fanfare-lines.json`** (Chase's approved pools as defaults; a bad file, for example an unknown `[placeholder]`, is refused whole); `[FanfareMute` (player command); the phase 2 `VoiceHook` |
| `LootBoxItems.cs` | `LootBox`, account binding, `LootBoxRevealGump`, and the reward items (table below) |
| `LootBoxRoller.cs` | Names and hues, the theme slot, the currency slot, the general pool, scaling |
| `ClusterFLootBoxes.cs` | The award rule; the live sources (achievements, bosses, League ranks); hooks for the missing sources; the abandoned-box cleanup; `[LootBox` and `[Fanfare` (staff, test shard) |

**Changed:**
- `ClusterFAchievements.cs`: `TryGrant` calls `OnAchievementEarned` after a new earn; the achievement page adds
  "Earned on loops 1, 3, 7 (3 times)" once a character on the account has earned it on more than one loop.
- `ClusterFLeagueRanks.cs`: `TryPromote` calls `OnLeagueRank` after the rank is set.
- `ClusterFAccountData.cs`: account record **v18** adds a `CharacterLootRecord` per character (source key to the
  loops it was earned on, and the fanfare mute), with its own version (D40 rule).
- The serializer test's version asserts went from 17 to 18.

### F-40, the rules as built

**Sources.**
- **Achievements:** `ach:<key>`, on the account's first earn.
- **Bosses:** `boss:<type>`, the first kill. Every player with looting rights, plus the last killer, counts. A boss is
  `ClusterFRareSelfRepair.IsHighEndSource` without paragons: champions, the Harrower, peerless and SA bosses, the
  Despise and Shame bosses, Navrey, and `IRareSelfRepairSource`.
- **League ranks:** `league:<rank>`.
- **Dungeon clears:** `clear:<dungeon>` (hook).
- **Loops:** `loop:<n>`, where each loop number is a new first (hook).

**First and repeat.**
- The first earn of a source on a loop records it.
- The first ever gives a box.
- A later loop gives no box. It plays a repeat line from the pool with `[count]` and `[loop]` filled, and the page
  shows the loops.
- The same loop again does nothing.

**Tiers.**

| Source | Tier |
|---|---|
| Achievement | by AP: up to 10 is tier 1, 25 tier 2, 50 tier 3, 100 tier 4, 250 tier 5, above that tier 6. Per-key overrides go in the file |
| Boss | 4 by default; champions and peerless 5; the Harrower 6 (by type or base class name) |
| League rank | 1-1-1-2-2-2-3-3-3-4-4-4-5-5-5-6-6 (Iron to Celestial) |
| Dungeon clear | 3 |
| Loop | 6 |

- **Slots:** 2, 3, 3, 4, 5, 6 for tiers 1 to 6.
- **Achievement themes by category:** Combat is Hunter; Skills and Collection are Scholar; Exploration and Discovery
  are Explorer; Mining is Miner; Crafting and Legacy are Artisan; League is League.

**Names and hues.**
- **Resource themes** use their ladder by tier:
  - Miner's (metal): Dull Copper, Bronze, Verite, Valorite, Mythril, Celestial.
  - Woodsman's (wood): Oak, Yew, Heartwood, Frostwood, Runewood, Celestial.
  - Hunter's (leather): Leather, Spined, Horned, Barbed, Barbed, Celestial.
  - Artisan's: by its craft's ladder.
- Hues come from `CraftResources.GetHue`. "Celestial" is the Celestial metal hue, 0x8AF.
- **The other themes use rarity:** Common gray 0x386, Uncommon green 0x44, Rare blue 0x59, Epic purple 0x13,
  Legendary orange 0x2B, Celestial 0x8AF.
- A box is named "<step> Box" (for example "Valorite Box"). Its tooltip gives the theme, tier and what earned it.

**The roll** happens when the box is earned. The contents go to the internal map inside the box, and the gold and
Renown are stored on it. Opening hands over exactly those items: a red run that re-rolled at opening failed.
- **One theme slot**, by related skill (the skill sets the resource tier through the metal, wood and leather skill
  ladders, `ClusterFMetalTiers` / `ClusterFWoodTiers` up to Celestial and Starwood):
  - Miner's: ore and gems, sometimes a satchel upgrade.
  - Woodsman's: logs, sometimes a grove ledger page.
  - Artisan's: the craft's resources plus a pattern book, or at tier 5 and up a Band V scroll (F-43).
  - Hunter's: hides plus a slayer weapon.
  - Explorer's: a treasure map of the tier's level plus a blank map.
  - Tamer's: a companion item.
  - Scholar's: reagents plus a spell scroll whose circle scales with tier.
  - Boss: a trophy.
  - Loop: a scroll fragment plus a bound loop cosmetic.
  - League: extra Renown plus a discount token.
- **One currency slot:** gold at every tier (250, 750, 2,000, 5,000, 12,000, 30,000), plus Renown from tier 2 (25, 50,
  100, 200, 400).
- **The rest from the general pool**, weighted by tier exactly as the brief's placeholder table.

**Scaling.**
- The level sets potion strength and magic gear intensity.
- **No level exists yet** (F-12), so `LevelOf` stands in with total Base skill / 10, clamped 1 to 200.

**Gear.**
- Plain quality, never exceptional.
- 1 to 4 properties (1 + tier / 2) at an intensity of 20 + level / 4, at most 60 percent (pinned
  `BaseRunicTool.ApplyAttributesTo`).
- Nothing on the shard is levelable, so box gear is not either.
- **Unverified:** whether this is always below an exceptional crafted piece of the same material. It is plain iron
  quality with modest properties, but no test compares the two.

**Opening.**
- **Where:** a guarded region with its guards on, or a house where the opener is owner, co-owner or friend
  (`house.IsFriend`, which includes both). Elsewhere it refuses with a System line.
- **Gold and Renown** are paid out; every item goes to the pack, else the bank (`ClusterFGuildPromotion.Deliver`, the
  shard's convention).
- **The reveal gump** lists everything, a System line follows, and the fanfare plays for the box's tier:
  - minor below tier 4, major from 4;
  - the rare line if a rare-pool item came out, the box-in-a-box line for a box.
- **Then the box deletes itself.**
- **The safety cleanup:** an hourly timer, from world load, deletes any box opened and still there after
  `abandonedBoxDays` (7). `[LootBox cleanup` runs it by hand.

**Binding.**
- **A box** refuses a secure trade, a drop on the ground, a drop onto anyone but its owner, a drop into or onto
  anything not carried by a character of its account (another player's pack, a house chest), and a lift by another
  account. Into the owner's own bags is fine.
- **Cosmetics** (`BoundCosmeticSash`) are bound the same way. The unique title and unique hue placeholders are also
  bound.
- **Everything else** in a box trades normally.

### F-41, the fanfare as built

| Level | Who sees it | What plays |
|---|---|---|
| Minor | the player only | one burst sent to that client alone (pinned's hued location effect packet), a private sound, the line overhead (private) |
| Major | nearby players | three bursts with area sound, sparkles (0x376A), the line overhead (public) |
| Capstone | the whole shard | six bursts and bigger sparkles, plus a shard-wide `World.Broadcast` naming the player |

- **Hues** are the rarity colors by tier. The bursts are pinned's firework family (0x373A + 0x10 x 0 to 3,
  sounds 0x11B to 0x11E).
- **Merge:** fanfares on one player within 2.5 seconds play once, at the highest level asked, with all lines stacked.
- **Mute:** `[FanfareMute` toggles `CharacterLootRecord.FanfareMuted`. A muted player gets no effects and no overhead
  lines; the chat lines still arrive, and **a capstone always broadcasts**.
- **Lines** rotate at random. Placeholders: `[Player]`, `[level]`, `[loop]`, `[count]`, `[tier]`.
- **Phase 2 hook:** `ClusterFFanfare.VoiceHook(player, key)`. Keys are "achievement", "box:<box name>" (for "You have
  received a" + tier + "Box!"), "levelup", "loop", "trial", "reached200". It is null in phase 1; no custom sound plays.
- **Who calls it now:** achievements (minor below tier 4, major from 4), box awards and openings, repeats, first boss
  kills (major), League ranks (through the box award), and the hooks below.

## Placeholder items (each says so in its name)

| Item | Stands for | Where it drops |
|---|---|---|
| `LootBoxPlaceholder("Ore Satchel Upgrade")` | a satchel upgrade | Miner's theme |
| `LootBoxPlaceholder("Grove Ledger Page")` | a grove ledger page | Woodsman's theme |
| `LootBoxPlaceholder("Companion Treat")` | a pet or companion item | Tamer's theme |
| `LootBoxPlaceholder("Trophy of <boss>")` | a boss-themed drop | Boss theme |
| `LootBoxPlaceholder("League Shop Discount Token")` | the League shop discount | League theme |
| `LootBoxPlaceholder("Unique Title")` (bound) | a unique title | rare pool |
| `LootBoxPlaceholder("Unique Hue")` (bound) | a unique hue | rare pool |
| `LootBoxPlaceholder("Companion Item")` | a companion item | rare pool |

Real new items, not placeholders:
- `LoopScrollFragment` (stackable; five make a loop scroll, a hook).
- `EpicComponent`, the new component category. It shows "Epic component" and the System line "Something,
  somewhere, calls for this. You have not found the recipe yet." No recipe uses one (F-42).
- `BoundCosmeticSash` (a wearable sash in a unique hue, bound; also the loop-only cosmetic "Loop N").
- `LootBox` itself.

**Recipes come through F-43's hook.**
- The Schematics/recipes pool calls `ClusterFRecipeRewards.CreateFromTable("bandV", LootBox)`, else a stock ML
  `RecipeScroll`.
- The Artisan's slot gives the craft's pattern book or Band V scroll.
- A mule module schematic in the rare pool is an `AccountRecipeScroll` for `recipe:<9000 + module * 10 + tier>`.

## Hooks left for sources that do not exist

Public methods in `ClusterFLootBoxes`; nothing calls them yet.

| Hook | Missing source | What it does when called |
|---|---|---|
| `OnLevelUp(pm, level)` | F-12 levels | minor fanfare from the level-up pool |
| `OnLoopCompleted(pm, loop)` | F-12 loops | capstone (broadcast) plus a tier 6 Loop box per loop number |
| `OnDungeonCleared(pm, key)` | no clear tracking exists | a tier 3 Explorer's box per dungeon or floor |
| `OnTrialChapter(pm, chapter)` | League trials are waived and nothing completes them | capstone broadcast |
| `OnReached200(pm)` | F-12's level 200 (the lines read as level, not skill) | capstone from the "reaching 200" pool |
| `CombineLoopScroll(from, fragments)` | no loop scroll item exists | says so; consumes nothing |
| `LoopProvider` | F-12 | the loop number; 1 for everyone now |
| `LevelOf` | F-12 | the level; the skill-total stand-in now |

## Tests (red then green)

New: `server/tests/Misc/LootBoxFanfareVerification.cs`, 8 facts.
1. **First, same loop, later loop:** a box; nothing; a repeat line with count 2 and loop 3, and "Earned on loops 1, 3
   (2 times)".
2. **Roll at earn:** contents fixed at earn (on the internal map). After the skill changes, opening hands over exactly
   those items, the box is gone, and the reveal gump lists the items plus the gold and Renown.
3. **Guarded regions:** refused in the wild; allowed in a guarded region; refused when its guards are off.
4. **Houses:** owner, co-owner and friend may open; a stranger in the house may not (a floor-only test house, as the
   wipe test builds).
5. **Binding:** the box refuses trade, ground, another player, another account's pack and another account's lift;
   the owner's own bag is fine. The cosmetic sash is bound too; gear and gold trade.
6. **Fanfare:** two fanfares merge into one major with 2 lines, and the second flush is empty. Muted: no effects, the
   line still there. A loop capstone on a muted player still broadcasts, naming the player and the loop.
7. **Data files:** the loot table round-trips; a file with a 1-slot tier is refused and the defaults kept; a line
   file with an unknown placeholder is refused.
8. **Saves:** the account record v18 keeps a character's loot loops and mute.

The **reveal gump** is checked by its contents (`Shown`). Its layout and the items' property lists were not read off
the wire: **unverified** in a client. The gump uses background 9270, not the 3500 to 3508 gump art that Fiddle-Me-This
replaces, so that art pack does not change it.

| Run | Result |
|---|---|
| Builds 1 to 3 | compile fixes: the generator's own `Contents` property; a missing `using`; an unassigned local; the analyzer refusing a `stackalloc` in a loop, now moved into a helper |
| Green, tests only | **1110 passed** |
| Red 1 | 8 breaks at once (every award a first; re-roll at opening; guards-off counted as guarded; owner only; the box trades; no merge; a 1-slot tier accepted; the mute not read back): **all 8 new facts failed** |
| Red 2 | an emptied box stays; mute ignored; the cosmetic trades: 5 failed (the house and guard facts also check the box deletes) |
| Red 3 | no broadcast when muted: 1 failed (the fanfare fact) |
| Restore | backups copied back, `cmp` byte-identical after each round |
| Green, full | **1110 passed**; "Built sl-modernuo:cc-p79 with patches applied and 1110 shard test(s) passing." |

**Patch notes:** 2026.10.13.2. `VERSION` bumped.

## Decisions for Chase

1. **Achievements are per account**, so a box fires once per account (on the first earn) and goes to the online
   character. A second character on the account gets no box for achievements its account already holds. Per-character
   records are kept so loops can change this. Should achievements become per character (a larger change to the
   achievement system)?
2. **The level stand-in** until F-12: total Base skill / 10.
3. **Tier rules:** achievements by AP (10/25/50/100/250), boss 4/5/6, League ranks in threes, clears 3, loops 6. All
   in the file.
4. **The leather ladder** has no tier past Barbed: tier 5 repeats "Barbed" and tier 6 is "Celestial" in the metal hue.
   Name a fifth leather?
5. **Box gear strength:** 1 to 4 properties at up to 60 percent intensity, plain quality. Confirm that sits below
   exceptional crafted gear, or lower it.
6. **Placeholders** to replace with real items: satchel upgrade, grove ledger page, companion items, boss trophy,
   League discount token, unique title, unique hue (table above).
7. **Repeat counts on the achievement page** show only when earned on 2 or more loops, so the page is unchanged until
   loops exist.
8. **Fanfare level for achievements:** minor below tier 4, major from 4. Capstones are only loops, reaching 200 and
   trial chapters.
9. **Trial chapters, loops, levels, clears** are hooks with no caller. Wire them as those systems land.

## Commit preflight

`Commit-ShardWork.ps1 -DryRun`, run 2026-10-13 before DONE:

```
Repo Result
---- ------
code dry run
docs dry run
```

- **Code, 12 files:** CHANGELOG.md, VERSION, ClusterFAccountData.cs, ClusterFAchievements.cs, ClusterFLeagueRanks.cs,
  AccountDataSerializerVerification.cs, the 5 files in LootBoxes/, and LootBoxFanfareVerification.cs.
- **Docs, 2 files:** this note and the Step 0 survey.
- No file is near 5 MB; nothing BLOCKED.

P79 DONE
