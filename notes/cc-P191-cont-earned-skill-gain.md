# cc-P191: skill gain that feels earned (retune the shard's base rate)

Written 2026-10-19 by the Bronze Golem (Fable), on branch golem/Bronze/P191 of both repos. Chase, 15:00: "We need to
drop the 5x gain/3 tries in base shard to a more level where things feel earned (without crystal)". Pinned paths are
relative to `D:\UO\ModernUO-pinned\Projects` (d4531cd9); "ours" is `server\customizations` and `server\tests`.

## Headlines

1. **Recommendation: `clusterf.skillGain.chanceAttempts` 2 and `clusterf.skillGain.amountMultiplier` 1** (today 3 and 5).
   Every gain is pinned's own 0.1 point and comes about twice as often as on a stock server. Measured with the real gain
   code: a combat skill reaches 100 in about 0.8 h of steady fighting and 200 in about 2 h; a craft or gathering skill
   in 1.4 h and 3.3 h; Magery and Imbuing reach their ceilings (120 and 140) in 1.7 h and 3.5 h. Today's rate does the
   same climbs in 8 to 30 minutes. Table in section 1.
2. **"Stock 1 and 1" on this shard is already about three times OSI's speed**, so it is not the OSI-slow end of the
   curve. Pinned's gain chance halves as the character's skill total nears the total cap (`SkillCheck.cs:126`); OSI's
   700 cap drives that term to zero, while the shard's total of 58 x 200 (`ClusterFSkillCaps.TotalSkillCap`) keeps it
   near 0.94 for any character. The recommendation doubles stock; it does not need the attempts and amount both up.
3. **The rate is the same at every range; no range rule and no code for a curve.** Pinned's per-skill headroom term
   (`SkillCheck.cs:127`) already makes the last 50 points cost about twice the uses of the first 50, and F-12's ladder
   (50, 100, then +5 per loop) gates everything above 100 five points at a time, so the climb past 100 is paced by loops,
   not by the gain rate. `pastStockCeiling` stays on: it is what lets sixteen skills reach the 200 cap at all (cc-P66
   hook G) and has nothing to do with speed.
4. **Applied in code and the changelog, not in the test config.** The code defaults now match (`ClusterFSkillGain.cs:39-40`)
   and `CHANGELOG.md` carries the player note. The test and live config files live in `D:\ShatteredLegacy\server\uo\`,
   which this Golem may not touch (hand-off rule), so the two edits are written for Chase in "For Chase" (section 6).
5. **Facts, each red first:** the configured rate is what the gain code uses (five pairs), the simulation is seeded,
   GainFactor (the Test Crystal's lever, cc-P190) still multiplies the chance, and the accelerated skill (New Haven,
   cc-P189's apprentice boost) still multiplies each gain. Built as `sl-modernuo:cc-P191`; all 1,554 shard tests green.

## 0. Read first, and today's settings

Read in full: `notes\cc-P20-skill-scaling-research.md` (sections 0, 3 and the per-skill rows cited below),
`notes\skills-design.md` (status, magic and crafting sections), `notes\passdown-skills-design-2026-10-02.md`,
`notes\f12-levels-loops-caps.md`, `notes\f12-decisions-2026-10-05.md`, `notes\cc-P54-f12-xp-and-gain-paths.md` Part C,
`notes\cc-P66-clamps-and-hook-g.md`, `notes\cc-P67-craft-ceilings.md`, `notes\cc-P171-taming-anger-scales.md`, and the
prompts P172, P189 and P190 (all three are still in `D:\UO\cc-prompts\queue\`, not built; see section 5).

Today, both configs (the prompt's lines; the files themselves are outside this Golem's desk): `clusterf.skillGain.enabled`
True, `amountMultiplier` 5, `chanceAttempts` 3, and on test `pastStockCeiling` True and `testCenter.skillGainMultiplier`
5.0. The code: `ClusterFSkillGain.cs` wraps pinned's four handlers (`Skills/SkillCheck.cs:33-40`); after the first
attempt (pinned's own handler) it re-rolls pinned's `SkillCheck.CheckSkill` (`:108`) up to `chanceAttempts` times
(`MoreAttempts`), and after any gain calls pinned's `Gain` (`:236`) up to `amountMultiplier` times (`ApplyAmountBonus`).
Pinned's gain chance (`SkillCheck.cs:126-137`): `((Cap - Total) / Cap + (skill.Cap - Base) / skill.Cap) / 2`, plus
`(1 - chance) x 0.5` on a successful use, halved, times `GainFactor`, floor 0.01. Below Base 10 every use gains (`:120`).

Every other thing that adds gain on top, checked by reading the code:

| Source | What it does | Reads the rate? |
|---|---|---|
| New Haven training quests (pinned `GainSkillObjective`, `SkillCheck.cs:273-276`) | `AcceleratedSkill` while `AcceleratedStart` is ahead: each gain's amount x 2 to 5 | Multiplies each of the amount multiplier's repeated gains too, so under today's 5x a New Haven gain was 1.0 to 2.5 points |
| cc-P189 Old Haven apprentice boost (queued) | ServUO's `ApprenticeRegion` is only the buff icon for the ML quest's `ApprenticeObjective` (`Services/MondainsLegacyQuests/ApprenticeRegion.cs`); the gain is the same `AcceleratedSkill` path | Same as above |
| cc-P190 Test Crystal (queued) | A per-character factor at the one `GainFactor` read, `SkillCheck.cs:133` | Multiplies the chance of every attempt; fact R3 |
| `testCenter.skillGainMultiplier` (test shard, until P190) | Scales every skill's `GainFactor` (`TestCenterSkillGain.cs`) | Same lever as the crystal |
| Loop memory / echo (F-12, not built) | Decided as an amount multiplier with a per-use cap (`f12-decisions-2026-10-05.md`, item 14) | Will sit on the amount; another reason to keep the base amount at 1 |
| Pets (cc-P172, queued; pinned `SkillCheck.cs:140-143` controlled x2 chance) | A pet's own rolls; `ShouldBoost` is players only | No |
| Young (ours `ClusterFYoungPlayer.cs`) | Protection and duration only; no gain term | No |
| Guild orders (`ClusterFSmithTeaching.cs`), commissions, craft ceilings (`ClusterFCraftGain.cs`) | Pick items and windows that still teach; the roll is pinned's `CheckSkill` | No extra gain, only a window |
| Achievements (`ClusterFAchievements.cs:1142, :1155`) | Thresholds on `Base`; nothing timed | No |
| Hook G (`ClusterFSkillGain.Roll`) | A gain-only roll past a stock ceiling, re-rolled `chanceAttempts` times | Yes, the same attempts |

## 1. Measure

### Method

`server\tests\Skills\SkillGainRateVerification.cs` (fact S1). A `PlayerMobile` in the test host with the shard's hook
installed over pinned's handlers exactly as the server installs it (`ClusterFSkillGain.Initialize` over
`SkillCheck.Mobile_SkillCheck*`), the 200 cap on every skill, the shard's total cap (58 x 200), six other skills at 100
(so the total-cap term reads about 0.94, as a real character's does), stats locked, anti-macro off (the pinned default,
`AntiMacroSystem.cs:96`; the live value is inside the container and unread). `BuiltInRng.Generator` is `new Random(seed)`
for seeds 1 to 5; the table is the mean. Each use calls `Mobile.CheckSkill` with the window (or direct chance) a real
use passes, so the chance, the gain roll, the amount and the clamps are all the real code. Nothing is re-implemented.

The play model is the test's own (what each use rolls, and seconds per use); it is the only assumption in the numbers:

| Skill | Each use rolls | Seconds per use (uses an hour) | Ceiling today |
|---|---|---|---|
| Swordsmanship | the hit chance of `BaseWeapon.cs:1296-1340` against a creature of equal skill up to 120 (50 percent, rising to about 80 at 200) | 3 (1,200): a fast weapon against a stream of targets, P54's figure | cap |
| Tactics | (0, cap) on every hit, `BaseWeapon.cs:2524` | 3 (1,200), passively with the weapon | cap |
| Blacksmithy | an item or Society order at 50 percent: window (v - 20, v + 20), `CraftItem.cs:891-894`; shard metals carry the window to 200 (`ClusterFCraftGain`) | 5 (720): a craft macro with ingots on hand, P54's figure | cap |
| Mining | the richest vein the miner can work (`HarvestSystem.cs:147`, each ore's own window: pinned `Mining.cs:115-187`, ours `ClusterFMiningExtension.Ore`, tier +/- 40) | 5 (720): the swing plus moving between banks | cap (iron alone stops at 100) |
| Magery | the highest circle at 37.5 percent or better (`Spell.cs:627`, `MagerySpell.cs:30-44`, window min + 40) | 5 (720): cast, recovery and mana | 120 (8th circle window 80 to 120; casting schools are not hook G, `f12-decisions-2026-10-05.md` 8b) |
| Imbuing | a property at 50 percent, window (difficulty - 20, difficulty + 20), `ArtificersImbueGump.cs:1854`, difficulty 40 to 120 (`:121`) | 10 (360): the gump, shards and gold per try | 140 (`SkillDifficulty` tops at 120) |

Seconds per use are the slow end of a focused session: a player who also loots, heals, walks or waits for mana takes
longer, and hours scale with it. An hour of play is therefore 1,200 swings, 720 crafts, digs or casts, or 360 imbues.

### Uses and hours to each milestone (seeds 1 to 5, mean; a dash is past the skill's ceiling today)

Settings are written amount and attempts, as the prompt does: "2 and 1" is `amountMultiplier` 2, `chanceAttempts` 1.

Swordsmanship (3 s per use):

| setting | uses to 50 | 80 | 100 | 120 | 150 | 200 | h to 50 | 80 | 100 | 120 | 150 | 200 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| stock 1 and 1 | 840 | 1471 | 1916 | 2392 | 3173 | 4733 | 0.70 | 1.23 | 1.60 | 1.99 | 2.64 | 3.94 |
| **1 and 2 (recommended)** | 420 | 736 | 958 | 1196 | 1587 | 2367 | 0.35 | 0.61 | 0.80 | 1.00 | 1.32 | 1.97 |
| 2 and 1 | 412 | 726 | 959 | 1196 | 1589 | 2357 | 0.34 | 0.61 | 0.80 | 1.00 | 1.32 | 1.96 |
| 2 and 2 | 206 | 363 | 480 | 599 | 795 | 1179 | 0.17 | 0.30 | 0.40 | 0.50 | 0.66 | 0.98 |
| 3 and 1 | 275 | 493 | 647 | 806 | 1070 | 1596 | 0.23 | 0.41 | 0.54 | 0.67 | 0.89 | 1.33 |
| today 5 and 3 | 55 | 99 | 129 | 164 | 218 | 321 | 0.05 | 0.08 | 0.11 | 0.14 | 0.18 | 0.27 |

Tactics (3 s per use):

| setting | uses to 50 | 80 | 100 | 120 | 150 | 200 | h to 50 | 80 | 100 | 120 | 150 | 200 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| stock 1 and 1 | 889 | 1534 | 1987 | 2466 | 3272 | 5020 | 0.74 | 1.28 | 1.66 | 2.05 | 2.73 | 4.18 |
| **1 and 2 (recommended)** | 445 | 768 | 994 | 1233 | 1636 | 2510 | 0.37 | 0.64 | 0.83 | 1.03 | 1.36 | 2.09 |
| 2 and 1 | 430 | 758 | 988 | 1230 | 1644 | 2504 | 0.36 | 0.63 | 0.82 | 1.03 | 1.37 | 2.09 |
| 2 and 2 | 216 | 380 | 494 | 615 | 822 | 1252 | 0.18 | 0.32 | 0.41 | 0.51 | 0.69 | 1.04 |
| 3 and 1 | 293 | 511 | 665 | 832 | 1107 | 1712 | 0.24 | 0.43 | 0.55 | 0.69 | 0.92 | 1.43 |
| today 5 and 3 | 60 | 101 | 133 | 167 | 220 | 334 | 0.05 | 0.08 | 0.11 | 0.14 | 0.18 | 0.28 |

Blacksmithy (5 s per use):

| setting | uses to 50 | 80 | 100 | 120 | 150 | 200 | h to 50 | 80 | 100 | 120 | 150 | 200 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| stock 1 and 1 | 845 | 1491 | 1947 | 2433 | 3232 | 4794 | 1.17 | 2.07 | 2.70 | 3.38 | 4.49 | 6.66 |
| **1 and 2 (recommended)** | 423 | 746 | 974 | 1217 | 1616 | 2399 | 0.59 | 1.04 | 1.35 | 1.69 | 2.25 | 3.33 |
| 2 and 1 | 416 | 739 | 974 | 1218 | 1622 | 2379 | 0.58 | 1.03 | 1.35 | 1.69 | 2.25 | 3.30 |
| 2 and 2 | 208 | 370 | 487 | 609 | 811 | 1189 | 0.29 | 0.51 | 0.68 | 0.85 | 1.13 | 1.65 |
| 3 and 1 | 281 | 498 | 656 | 818 | 1100 | 1621 | 0.39 | 0.69 | 0.91 | 1.14 | 1.53 | 2.25 |
| today 5 and 3 | 56 | 100 | 132 | 167 | 221 | 327 | 0.08 | 0.14 | 0.18 | 0.23 | 0.31 | 0.45 |

Mining (5 s per use):

| setting | uses to 50 | 80 | 100 | 120 | 150 | 200 | h to 50 | 80 | 100 | 120 | 150 | 200 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| stock 1 and 1 | 869 | 1530 | 1983 | 2473 | 3285 | 4869 | 1.21 | 2.13 | 2.75 | 3.43 | 4.56 | 6.76 |
| **1 and 2 (recommended)** | 435 | 765 | 992 | 1237 | 1643 | 2435 | 0.60 | 1.06 | 1.38 | 1.72 | 2.28 | 3.38 |
| 2 and 1 | 431 | 758 | 996 | 1246 | 1661 | 2417 | 0.60 | 1.05 | 1.38 | 1.73 | 2.31 | 3.36 |
| 2 and 2 | 216 | 379 | 498 | 623 | 831 | 1209 | 0.30 | 0.53 | 0.69 | 0.87 | 1.15 | 1.68 |
| 3 and 1 | 289 | 507 | 663 | 833 | 1119 | 1648 | 0.40 | 0.70 | 0.92 | 1.16 | 1.55 | 2.29 |
| today 5 and 3 | 57 | 101 | 135 | 168 | 222 | 328 | 0.08 | 0.14 | 0.19 | 0.23 | 0.31 | 0.46 |

Magery (5 s per use; stops at 120 today):

| setting | uses to 50 | 80 | 100 | 120 | h to 50 | 80 | 100 | 120 |
|---|---|---|---|---|---|---|---|---|
| stock 1 and 1 | 864 | 1526 | 1987 | 2505 | 1.20 | 2.12 | 2.76 | 3.48 |
| **1 and 2 (recommended)** | 432 | 763 | 994 | 1253 | 0.60 | 1.06 | 1.38 | 1.74 |
| 2 and 1 | 420 | 751 | 996 | 1269 | 0.58 | 1.04 | 1.38 | 1.76 |
| 2 and 2 | 210 | 376 | 498 | 635 | 0.29 | 0.52 | 0.69 | 0.88 |
| 3 and 1 | 286 | 508 | 666 | 846 | 0.40 | 0.71 | 0.93 | 1.18 |
| today 5 and 3 | 58 | 101 | 134 | 170 | 0.08 | 0.14 | 0.19 | 0.24 |

Imbuing (10 s per use; stops at 140 today):

| setting | uses to 50 | 80 | 100 | 120 | h to 50 | 80 | 100 | 120 |
|---|---|---|---|---|---|---|---|---|
| stock 1 and 1 | 894 | 1561 | 2018 | 2527 | 2.48 | 4.34 | 5.61 | 7.02 |
| **1 and 2 (recommended)** | 447 | 781 | 1010 | 1264 | 1.24 | 2.17 | 2.80 | 3.51 |
| 2 and 1 | 447 | 775 | 1019 | 1270 | 1.24 | 2.15 | 2.83 | 3.53 |
| 2 and 2 | 224 | 388 | 510 | 635 | 0.62 | 1.08 | 1.42 | 1.76 |
| 3 and 1 | 296 | 514 | 669 | 841 | 0.82 | 1.43 | 1.86 | 2.34 |
| today 5 and 3 | 59 | 105 | 139 | 173 | 0.16 | 0.29 | 0.39 | 0.48 |

Loop 0, where the cap is 50 (Swordsmanship; the per-skill headroom term reads against 50, so the same 50 points cost
more):

| setting | uses to 50 | h to 50 |
|---|---|---|
| stock 1 and 1 | 1122 | 0.94 |
| **1 and 2 (recommended)** | 562 | 0.47 |
| 2 and 1 | 547 | 0.46 |
| 2 and 2 | 274 | 0.23 |
| 3 and 1 | 371 | 0.31 |
| today 5 and 3 | 75 | 0.06 |

### What the numbers say

- **Uses are nearly the same for every skill.** Pinned's formula is relative to the cap (cc-P20 section 3.3), the use's
  own chance only enters as a bonus of at most 0.25 on a success, and every model here has a use whose window is above
  the skill. The hours differ only by seconds per use. So one setting fits all skills; nothing needs a per-skill rate.
- **Attempts and amount are the same dial at this scale.** Two attempts halve the uses as exactly as a 2x amount does,
  because the gain chance per roll sits around 0.4 to 0.5 for the whole climb (0.49 at 100 on a (0, 200) window, 0.24 at
  the cap), so a second roll is nearly a second gain. The difference is the feel: amount 2 gives 0.2 jumps, attempts 2
  gives stock 0.1 jumps twice as often.
- **Stock here is about three times OSI.** cc-P20 3.4 put OSI's chance at 0.11 at 90 and 0.07 at 100 on a 700 total
  (0.1 per gain); this shard's stock column rolls about 0.45 at the same place because the total-cap term never falls.
  cc-P54 Part C's "plain 1x" figures (4,903 uses to 200) match this table's stock column (4,733 to 5,020).
- **The curve already slows at the top.** Stock: 840 uses for 0 to 50, 1,560 for 150 to 200, from the headroom term
  alone. The loop ladder then meters everything past 100 five points per loop.

## 2. Recommend

**`chanceAttempts` 2, `amountMultiplier` 1, `pastStockCeiling` on, `enabled` on** (set to true even though "1 and 1" is
also reachable by `enabled` false: the hook's worn-bonus rule and hook G run either way, but keeping the rate on makes
the config say what it means).

Where each option lands, in a player's evening (3 hours of play), taking the combat and crafting rows:

| Option | A GM (100) in | 200 in | What it feels like |
|---|---|---|---|
| today 5 and 3 | 7 to 11 min | 16 to 27 min | The crystal's job. Loop 0's cap of 50 falls in 4 minutes; the 26 New Haven quests lock out (50) before the trainer is found (`NewHavenQuestBoard.cs:12-16`). |
| 2 and 2 | 24 to 41 min | 1 to 1.7 h | One evening caps two or three skills to 200 if the ladder allowed it; the climb is a session, not a goal. |
| 3 and 1 | 33 to 55 min | 1.3 to 2.3 h | Close to 2 and 2 with 0.3 jumps; every stacked multiplier (apprentice x2 to 5, echo) rides on a tripled gain. |
| **1 and 2** | **48 min to 1.4 h** | **2 to 3.4 h** | A GM is an evening's work in one skill, or an hour of fighting for the combat set that gains together. 200 is a few sessions, and above 100 the ladder is the real clock. Gains are stock-sized and frequent. |
| 2 and 1 | same hours | same hours | Same speed, 0.2 jumps half as often; stacked multipliers double on top (a New Haven gain is 0.4 to 1.0). |
| stock 1 and 1 | 1.6 to 2.8 h | 4 to 7 h | A GM is a day's play per skill. Already three times OSI, but with 58 skills to max and a reset every loop it reads as a grind (cc-P54 Part C: a 200 re-climb at 1x with no echo is 16 to 44 minutes per skill at best, and the echo is not built). |

Why 1 and 2 over 2 and 1 at the same speed: every multiplier the shard stacks on top is an amount multiplier (the
accelerated skill x2 to 5 per gain, the decided echo, the recommended per-use cap on echoed gain), and a 0.1 base keeps
each of them meaning what its author measured. Hook G and the craft ceilings re-roll attempts, so a second attempt also
helps the sixteen hook-G skills past their stock ceilings in the same proportion.

Why not a range rule (faster early, slower past 100, or slower past the stock ceiling): the headroom term already does
the first two (the last 50 points cost about twice the first 50), the ladder gates +5 per loop past 100, and the stock
ceilings are where the skill would otherwise stop dead; slowing hook G past them would turn the sixteen skills' only
path into a second grind. Also Chase's decision 17 (2026-10-05) was to start live at plain x1 and tune up in playtesting;
the retune is "earned, not OSI-slow", and x2 stock is the smallest step that is clearly past OSI-slow.

Why `pastStockCeiling` stays on: it is not a rate. Off, Hiding stops at 100, Healing at 120 and so on (cc-P66 B).

**The Test Crystal (P190) and `testCenter.skillGainMultiplier` are unaffected by this.** The crystal's factor multiplies
the chance of each of the 2 attempts (fact R3), so a 5x crystal on the new base is about 5 times faster than the new base,
not the old 5x3 (which was about 10 times stock).

## 3. What changed, with file:line

Only the shard repo; no patch, no saved type, no config file (section 5, deviation 1).

- `server\customizations\ClusterFSkillGain.cs:39-40`: `DefaultChanceAttempts` 3 -> 2, `DefaultAmountMultiplier` 5 -> 1.
  These are the values a config without the keys gets (`GetOrUpdateSetting`, `:89-93`); every existing config already
  holds its own values, so this changes nothing until the config lines are set. Header comment `:7-10` records cc-P191.
- `server\customizations\Engines\ML Quests\Items\NewHavenQuestBoard.cs:13-16`: the comment that said "3 attempts and 5x
  gain ... arrives in minutes" now says what the board was for and what it is under the new rate (about half an hour to
  the 50-point lockout). Comment only.
- `server\tests\Skills\SkillGainRateVerification.cs` (new, 460 lines): facts R1 to R4 and the simulation S1 (section 4).
  `RecommendedAttempts` 2 and `RecommendedAmount` 1 at `:39-40` are what R3 and R4 run under.
- `CHANGELOG.md`: new section 2026.10.19.5 (a Changed line for players, a Staff line); `VERSION` 2026.10.19.5.

Things that assumed 5 and 3, checked (list only; docs are not edited by agents):

| Where | What it says | Action |
|---|---|---|
| `server\tests\Skills\SkillGainPastStockCeilingVerification.cs:81-83` | its own hook sets 3 and 5 for its facts | Nothing: it tests hook G under an explicit rate, not the config |
| `server\tests\Engines\Craft\CraftCeilingsVerification.cs:86-88` | sets 1 and 1 for its facts | Nothing |
| `server\tests\Misc\TestCenterVerification.cs` Part C | `testCenter.skillGainMultiplier` on GainFactor | Nothing; the lever is unchanged |
| `tools\playtest-bot\uobot\checks.py:285-295` (P66-7) | matches `\d+x gain amount` in `[ClusterFSkillGain` | Nothing: "1x gain amount" matches |
| `tools\playtest-bot\uobot\report.py:44` | prints `clusterf.skillGain.amountMultiplier` for T-002 and T-031 | Nothing; it reports the value |
| `testing\play-tests.json` T-002 (New character training) and T-031 (the multiplier compounds) | T-002's text says ClusterFSkillGain runs 5x; T-031 expects "extra gains still happen on top" | Machine output from the importer; T-031 still holds (2 attempts on top of the multiplier), T-002's caveat text is stale |
| `docker\uo\SERVER.md:54, :607, :1028-1050` | "3 chance attempts, 5x successful player gain amount" and the Proxmox-era install notes | Doc, for the overseer: the two numbers are now 2 and 1 |
| `docs\community-scripts-wishlist.md:95, :116, :149` | "We run ClusterFSkillGain at 3 attempts and 5x gain" and the 26-quest lock-out argument | Doc: the argument weakens (half an hour to 50, not minutes); the board still removes the trainer hunt |
| `docs\feature-queue.md:623, :2763` | "at our gain rate" | Doc; the rate is now this note's |
| `notes\f12-levels-loops-caps.md` "Loop memory" | "today's test shard runs the Test Center x5 plus ClusterF's 3 attempts and x5" | Historical; superseded by this note |
| `design\phases\phase_4_smiths_guild_extended_crafting.md:758` | "no tuning needed, natural slowdown past 200" | Historical (cc-P20 3.3 already refuted it) |
| The Crafter script | There is none: `D:\UO\sl-scripts` holds SL_Combat, SL_Loot, SL_Lumberjack, SL_Mining and `server\razor-scripts` the taming trainer and radars; none waits on a gain rate (grep "gain" in all of them: SL_Mining's only hits are vein and Tinkering skill checks) | Nothing |
| Achievements | `ClusterFAchievements.cs:1142, :1155` are thresholds on `Base`; nothing is timed | Nothing |
| Website | `website\` holds only `.gitkeep` | Nothing |

## 4. Tests

All in `server\tests\Skills\SkillGainRateVerification.cs`. Seen red first in build cycle 1 (log
`build-red.log` in the session scratchpad; 1,558 tests, 8 failed, all eight this file's), then green in cycles 2 and 3
(1,554 passed, 4 skipped, 0 failed; cycle 3 built the image `sl-modernuo:cc-P191`).

| Fact | What it checks | How it was made red | Red | Green |
|---|---|---|---|---|
| R1 (theory, 5 pairs) | `SetSetting` the two keys, `Configure()`, the properties read them; then one use at Base 50 on (0, 200) with every roll held at 0 raises Base by attempts x amount x 0.1 | `Configure` read the key `chanceAttemptz` (a one-letter break in `ClusterFSkillGain.cs`) | 4 of 5 pairs: "Expected: 1 Actual: 3" (the (3, 5) pair passed because the default is 3; a fact that only tested the default would not have caught this) | 50.2, 50.2, 50.4, 50.3, 51.5 |
| R2 | the same seed gives the same six use counts twice, another seed differs, every milestone is reached | the simulation used an unseeded `Random` and a use limit of 10 | "Collections are equal", all -1 | seed 7: 416, 781, 1015, 1256, 1635, 2481 twice; seed 8: 414, 767, 1021, 1246, 1635, 2518 |
| R3 | at Base 100 on (0, 200) with every roll held at 0.5 (the use passes, the gain chance is 0.485): GainFactor 1 gains nothing, GainFactor 3 gains, under the recommended rate | the fact's own expectation flipped (expected factor 1 to gain). Honest note: the lever is pinned's `SkillCheck.cs:133`, which the shard does not patch, so there is nothing of ours to break; the red proves the fact can fail, not that it guards a shard line | "RED: factor 1 expected to gain" | factor 1: 100.0; factor 3: 100.2 |
| R4 | one use with every roll held at 0: plain +0.2 (2 attempts x 1 x 0.1), with `AcceleratedSkill` set +0.4 (`RandomMinMax(2, 5)` reads 2 at roll 0, `SkillCheck.cs:273-276`) | expectation flipped (expected accelerated == plain) | "Expected 0.2 Actual 0.4", which is itself the evidence that the accelerated skill doubles on top | plain +0.2, accelerated +0.4 |
| S1 | the table; asserts every skill reaches 50 under every setting | use limit 10 | "never reached 50" | the tables above (316 ms) |

The simulation's output is `ITestOutputHelper`, which `build.sh`'s `console;verbosity=normal` prints only for failed
tests; the table was read by running this one class on the builder image with `verbosity=detailed`, the test route
`notes\s4-test-route.md` documents (the gate itself ran through `build.sh`). The command, for the next retune:

```
MSYS_NO_PATHCONV=1 docker run --rm --network=none --security-opt seccomp=unconfined -w /build/modernuo sl-uo-builder:cc-P191 dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore --filter "FullyQualifiedName~SkillGainRateVerification" --logger "console;verbosity=detailed"
```

## 5. Deviations and decisions for Chase

1. **The test config was not set.** The prompt says to set the recommendation in `Configuration-test\modernuo.json`,
   which lives in `D:\ShatteredLegacy\server\uo\` (gitignored, bind-mounted into the test shard). The Golem hand-off
   forbids this Golem any read or write under `D:\ShatteredLegacy`, and `server\uo\` does not exist in the Bronze work
   copy. The exact edit is in "For Chase" below, test and live alike. The code defaults were changed instead, so a config
   that ever lacks the keys gets the new rate; existing configs keep their stored 3 and 5 until edited.
2. **P189 and P190 are not built** (both still in `D:\UO\cc-prompts\queue\`), so "P190's crystal still multiplies on
   top" and "P189's apprentice boost still applies" are proven against the mechanisms those prompts name: the
   `GainFactor` read (`SkillCheck.cs:133`, where P190 puts the per-character factor per its own text) and pinned's
   `AcceleratedSkill` (what OSI's and ServUO's apprentice training actually drives; ServUO's `ApprenticeRegion` only
   shows the buff). When P189 and P190 land, their own facts should run under this rate; R3 and R4 are the shape.
3. **The play test "train one skill for 15 minutes on the test shard with the crystal off" is written for Chase**, not
   run: no test shard was started (the config could not be set, and there is no crystal to turn off yet).
4. **Reading `docker\uo\build.sh` through the Read tool was auto-denied** (unattended run); it was read with `cat` once
   the docker-build lock was held, as the hook requires. No other denial.
5. **No task list.** The hand-off asks for one task per main step in the task list; this session has no task tool
   (`TodoWrite` and the Task tools are not in its tool set), so progress went to the chat instead.
6. **The red for R3 and R4 is an expectation flip**, said plainly in section 4: both facts sit on pinned lines the shard
   does not patch.
7. **Chase's decision 17 (2026-10-05, "start live at plain stock speed (x1) and tune up")** is superseded by his
   2026-10-19 ask and this recommendation (x2 stock by attempts). Said here so the decisions file can be updated.
8. **The patch note is in `CHANGELOG.md` 2026.10.19.5** as the prompt's patch-notes section requires. It describes the
   live rate as changed. If this build is deployed before the live config line is set, the note is early by one deploy;
   set the line in the same deploy.

## 6. For Chase

**The table (hours), recommendation "1 and 2":**

| Skill (seconds per use) | h to 50 | h to 100 | h to 150 | h to 200 | today 5 and 3, h to 200 |
|---|---|---|---|---|---|
| Swordsmanship (3) | 0.35 | 0.80 | 1.32 | 1.97 | 0.27 |
| Tactics (3) | 0.37 | 0.83 | 1.36 | 2.09 | 0.28 |
| Blacksmithy (5) | 0.59 | 1.35 | 2.25 | 3.33 | 0.45 |
| Mining (5) | 0.60 | 1.38 | 2.28 | 3.38 | 0.46 |
| Magery (5) | 0.60 | 1.38 | stops at 120 (1.74) | - | 0.24 to 120 |
| Imbuing (10) | 1.24 | 2.80 | stops at 140 (3.51 to 120) | - | 0.48 to 120 |

Loop 0 (cap 50): 0.47 h of fighting per combat skill. Full tables with every option in section 1.

**The live config line** (`D:\ShatteredLegacy\server\uo\modernuo\Configuration\modernuo.json`, the `settings` block,
values are strings; today's lines 107-109):

```
"clusterf.skillGain.amountMultiplier": "1",
"clusterf.skillGain.chanceAttempts": "2",
```

`clusterf.skillGain.enabled` stays `"True"`. The server reads the keys at start (`ClusterFSkillGain.Configure`), so it
is a restart, and `[ClusterFSkillGain` in game should then say "rate enabled, 2 chance attempt(s), 1x gain amount; past
stock ceilings on". Existing characters keep their skills: nothing here touches a saved value.

**The test config**, the same two lines in `Configuration-test\modernuo.json` (today's lines 117-120; `pastStockCeiling`
stays `"True"`). From PowerShell 5.1, both files at once, after a backup:

```
$files = 'D:\ShatteredLegacy\server\uo\modernuo\Configuration\modernuo.json', 'D:\ShatteredLegacy\server\uo\modernuo\Configuration-test\modernuo.json'
foreach ($f in $files) { Copy-Item $f "$f.bak-P191"; $t = Get-Content $f -Raw; $t = $t -replace '"clusterf.skillGain.amountMultiplier": "5"', '"clusterf.skillGain.amountMultiplier": "1"' -replace '"clusterf.skillGain.chanceAttempts": "3"', '"clusterf.skillGain.chanceAttempts": "2"'; Set-Content $f $t -Encoding utf8 -NoNewline; Select-String -Path $f -Pattern 'clusterf.skillGain' }
```

Dry run first: the same with the `Set-Content` removed shows what would match. Leave `testCenter.skillGainMultiplier` at
5.0 on test until P190's crystal replaces it, or set it to 1.0 for the play test below.

**The patch note** (already in `CHANGELOG.md` 2026.10.19.5, Changed):

> Skills now rise at a rate meant to feel earned: every gain is the normal 0.1 and comes about twice as often as on a
> stock server, instead of the old five-point-per-gain, three-tries-per-use sprint. A skill reaches 100 in roughly an hour
> of steady fighting or an hour and a half of crafting; the Test Crystal, New Haven and Old Haven training, loop memory
> and pet training still speed things up on top. Existing characters keep every point they have.

**Play test (15 minutes, test shard, `sl-modernuo:cc-P191`, the two lines set, `testCenter.skillGainMultiplier` 1.0 or
the crystal off once P190 lands):** a fresh character, Swordsmanship 50 from creation, fights at the New Haven dungeon
or Old Haven skeletons for 15 minutes. Expect about 300 swings and Swordsmanship from 50 to about 70 (uses 420 to 736
cover 50 to 80 in the table; Tactics, Anatomy and Healing climb alongside). Then 15 minutes at a forge at 50 percent
success items: about 180 crafts, Blacksmithy from 50 to about 65. The question to answer: does a point every 15 to 20
seconds feel earned, or still handed out. If it feels slow, "2 and 2" (one line: `chanceAttempts` 2, `amountMultiplier`
2) halves the hours again; if it feels fast, "stock 1 and 1" (`enabled` false, or 1 and 1) doubles them. The table is
the map; no rebuild is needed for any of these, only the two lines and a restart.

## Commit preflight

Run 2026-10-19 against the Bronze work copies (the script defaults to the main checkouts, where another Golem's P186
work is pending; with -CodeRepo and -DocsRepo pointed at D:\UO\golems\Bronze it reads only this branch's files). Neither
repo is BLOCKED. Image: sl-modernuo:cc-P191 (label sl.commit=453735e, sl.dirty=1, since the branch is uncommitted until
the Golem commits). The docker-build lock was taken for the three build cycles and released; no test-shard, package or
haven lock was needed.

```
=== code  (D:\UO\golems\Bronze\ShatteredLegacy) ===
  5 file(s) pending:
    CHANGELOG.md
    VERSION
    server/customizations/ClusterFSkillGain.cs
    server/customizations/Engines/ML Quests/Items/NewHavenQuestBoard.cs
    server/tests/Skills/SkillGainRateVerification.cs
  dry run: would add, commit and push

=== docs  (D:\UO\golems\Bronze\shard-migration) ===
  1 file(s) pending:
    notes/cc-P191-cont-earned-skill-gain.md
  dry run: would add, commit and push

Repo Result
---- ------
code dry run
docs dry run
```

No file over 5 MB in either repo (find -size +5M: none).

P191 DONE
