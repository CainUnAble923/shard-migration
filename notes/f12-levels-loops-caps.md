# F-12 revised: levels, loops and caps (decided 2026-10-01; stats rewritten 2026-10-02)

Written 2026-10-01 by the overseer from Chase's decisions in one sitting, against cc-P20's research
(`notes\cc-P20-skill-scaling-research.md`, 236 KB). **This supersedes the max level 1000 design and the
example loop ladder in the F-12 and F-13 entries of `docs\feature-queue.md`.** Where this doc and the
queue entries disagree, this doc governs until the entries are rewritten.

## Why it changed

cc-P20 read all 58 skills one at a time. Storage allows 1000 (skills are ushort tenths, ceiling 6553.5,
`Server/Skills.cs:89-90`), but the game rules do not: **41 of 58 skills break by 1000, and 20 break at
or below 300**, which is the live cap today. Separately, **39 of 58 skills cannot gain past about 160
by play at all**, because each use carries a fixed `maxSkill` above which the check succeeds with no
gain roll (`UOContent/Skills/SkillCheck.cs:58-61`). So a high cap was buying nothing it could reach.

Chase lowered the ceiling to 200. Counted against P20's per-skill table, that removes all 21 skills
whose only breaks are in the 500 and 1000 columns, and defuses both breaks that can hard-fail: the
Discordance divide by zero in the swing timer (needs a -100 effect, which needs 300) and Parry's 100
percent shield block (needs 380). Feint's guaranteed no-damage needs 237 and is also out of reach.

It also matches what the engine already does: **`CharacterCreation.cs:437` rejects any starting skill
above 50**, which is exactly the loop-0 cap, so no character can ever be created above its own cap.

## The model

- **Individual skill cap = max level.** One number per character.
- **Total skill cap = 58 x max level.** Every skill is maxable on one character; this was already the
  recorded F-12 intent and Chase reconfirmed it 2026-10-01. Character identity comes from stats, loop
  progress and titles, not from choosing which skills to train.
- **Current level** climbs within a loop and resets to 1 on reset.
- **Max level ladder:** 50 at creation, then 100, 125, 150, 175, 200. Six loops, five resets.
- **A reset wipes skills and level.** Max level goes up, current level returns to 1, skills return to
  starting values. The re-climb is the content.
- **Echo XP** on levels the character already reached in an earlier loop, and it **accelerates each
  loop**, so old ground gets progressively cheaper and only the new levels carry weight.
- **Power scrolls raise the level cap, not individual skill caps.** They gate every step above 100.
  Reaching max level 100 is earned; 125, 150, 175 and 200 each need a scroll.
- **At max level, XP banks into a reserve, and the reserve is capped**, so a long stay at cap cannot
  skip the next step the moment a scroll is applied.
- **Scroll drops:** champion spawns, paragons and bosses, with the New Haven dungeon's mini champ as
  the first source. This ties the dungeon into progression rather than leaving it a side trip.

## Loop memory: skill and level gain speed (Chase, 2026-10-02, 11:03)

Live only; the test shard keeps its fast test rates during playtesting.

- **Base rate on live: "fast but not crazy fast".** Not test-center speed (today's test shard runs the Test Center
  x5 multiplier plus ClusterF's 3 attempts and x5 amount). The number is set by **playtesting what feels good**.
- **Loop memory: below a skill's previous peak, gain is faster, and the speed-up grows each loop.** "You remember what
  you learned." Above the previous peak, gain is the plain live base rate ("just fast").
- **The growth is capped.** Chase liked a ceiling over pure exponential: by the last loop the memory multiplier stops
  at a set top, so late re-climbs are quick but never instant. Overseer example to playtest against: +50 percent per
  loop compounding (about 7.6x by loop 5), or a hand table.
- **Levels use the same rule.** This answers the shape of echo XP above: levels already reached in an earlier loop
  re-climb at the loop-memory rate, new levels at the base rate. The echo multipliers stay placeholders until the
  playtest sets them, together with the skill multipliers.
- **Shown somewhere, not on every gain** (Chase, 11:03): the player can look it up on the paperdoll or another stat
  display (Chase, 11:04; overseer adds a line at reset), but skill-gain messages stay as they are.
- Does not fix the cc-P20 limit: 39 of 58 skills cannot gain past about 160 by use (fixed `maxSkill`,
  `SkillCheck.cs:58-61`). F-12 still needs a gain path for those (as F-26 plans for Arms Lore).

## Stats (rewritten 2026-10-02: no ceilings)

**Superseded:** the 2026-10-01 table (per-stat 125 to 200 by max level, total 325 to 550, veteran +50) and the
stat-lock plan are withdrawn. cc-P25 surveyed stats past 125 (`notes\cc-P25-stats-above-125-research.md`) and
Chase decided on its findings (`notes\p25-decisions-2026-10-02.md`). Register row: D-101 and D-102.

- **No ceilings of any kind.** No per-stat table, no effective clamp, no total cap, no soft caps inside formulas.
  Reason (Chase): players will face world bosses and champion spawns solo or in small parties.
- **Raw stats gain to the one global `stats.statMax`, which is 500 in both configs** and has been since May 2026
  (`docker\uo\SERVER.md:642`). Every note before cc-P25, this one included, assumed 125.
- **Effective stats are not clamped.** F-12 removes the `Math.Min` in `patches\PlayerMobile-individual-stat-cap.patch`
  (or sets `clusterf.statCaps.individualCap` very high). `Mobile.cs:1868`'s 65000 is the only bound left.
- **A reset keeps stats.** Pinned already never lowers raw stats when `StatCap` drops (`SkillCheck.cs:313-333`).
- **Carry weight stays uncapped** (`100 + 3.5 x Str`, `customizations\ClusterFBackpack.cs:33-42`).
- **Self-bandage keeps pinned's formula** (1.0 s at Dex 200, instant from effective Dex 220). **Pets gain to the same
  cap as players.**

**What this removes from the F-12 build:** the 0x1A stat-lock handler (`arch-f12-stat-lock-verdict-2026-10-01.md`),
the per-level total in `ClusterFStatCaps.Apply`, the `StatCapScroll` retune and the veteran +50.

**Still to do, because they are defects, not ceilings:**
- **D44**, the talisman and quiver stat-bonus leak (`AOS.cs:598` vs `:620`), now unbounded. Fact first, fix if red.
- **D45**, meditation's start chance inverts as Int rises (ours `Meditation.cs:83`).

**Consequences accepted:** stock bosses and champions were balanced for OSI players (about 150 effective, 150 HP)
and will be much easier. F-14's level field on our own creatures is where bosses scale to these players. Thrown
range passes the 18-tile update range from effective Str about 300 (cc-P25 decisions, fact 3).

## What each counter gates

Three counters, and putting a thing on the wrong one is how loop systems turn frustrating.

**Current level** resets every loop, so it gates what should be re-earned:
- ~~Total stat cap~~ **withdrawn 2026-10-02** (no stat ceilings; stats carry through a reset). A reset now
  costs skills and level only, so a reset character keeps full stats. Whether that is enough of a reset is
  Chase's call once loops are played; current level still needs a job of its own (Still open, item 2).
- **Level requirements on our gear only**, never on OSI items (the standing F-12 fidelity rule).
  **Exception, Chase 2026-10-01: the newbie dungeon's Tier 1 set carries no level requirement**, so it
  is wearable the moment a character resets. With the set blessed, no-trade and re-obtainable from the
  repeatable quest, Tier 1 is the guaranteed floor of every loop.
- Dungeon floor depth, so the dungeon is loop content rather than cleared once.

**Max level** only ever rises, so it gates permanent capability:
- Individual skill cap, and the total skill cap at 58 x max level.
- **Pet and stable slots (Chase, 2026-10-01).** Deliberately not current level: stabled pets would be
  stranded behind a shrinking slot count on every reset.
- Bank space (F-19's base of 1,000), extended ore access, housing and vendor slots.

**Loop count** only ever rises, so it gates prestige and identity: titles, cosmetic hues, the Legacy
Awakening history, the echo multiplier, and account-wide unlocks for newly created characters.

**Outside the loop entirely.** Collections are identity, not power, and must survive a reset:
P13's grove ledger above all, since it was specified as a long-term collection that eventually grants
teleportation to found groves, plus achievements, renown, guild membership and learned recipes.

### Pet and stable slots: what it costs

- **Follower slots are free.** `Mobile.FollowersMax` is per-mobile and serialized
  (`Server/Mobiles/Mobile.cs:844`, written `:2342`) and we already write it elsewhere
  (`customizations\Mobiles\Bosses\DespiseBosses.cs:50`).
- **Stable slots need a small patch.** `AnimalTrainer.GetMaxStabled` is a static method in a pinned file
  with no hook (`Mobiles/Vendors/NPC/AnimalTrainer.cs:58`), and we override nothing today.
- **It needs doing regardless.** The formula takes a 2 to 5 base from the summed Taming, Animal Lore and
  Veterinary, then adds `(skill - 90) / 10` for each of the three above 100. Verified by the overseer
  2026-10-01: that is 68 slots at 300 in all three, confirming cc-P20's figure, and still **38 at the
  new 200 cap**. OSI's own ceiling is 14.

## Placeholder numbers for Chase to react to

Every number here is a first proposal, not a decision.

- **Reserve cap: the XP for 5 levels.** Enough that a player hunting a scroll is never wasting play,
  small enough that a 25-level step still has to be played.
- **Echo multiplier: x2 on loop 1, rising by x1 per loop to x6 on loop 5.**
- **Step size +25** above 100. Four scrolls to go 100 to 200. OSI's +5 would need twenty.

cc-P20's XP curve (`XP(L) = 40 x L^1.5`) was modeled against the old 13-loop ladder to 1000 and needs
re-running against this six-loop ladder with the new echo rule. The script is already written at
`notes\cc-P20-scratch\xp_curve.py`.

## What this costs, from cc-P20's ranked list

**Deleted or shrunk:**
- Rank 11, the bespoke Legacy Scroll line (M): deleted. Power scrolls do the job, and pinned's
  `SpecialScroll` and `PowerScroll` plumbing, including the confirmation gump and consumption, is
  reused rather than patched out.
- Rank 10 inverts from "stop scrolls raising caps" to "point scrolls at level", which is simpler.
- Rank 6, grandfathering: gone. Chase ruled no grandfathering 2026-10-01, and the old live world is
  retired, so there is nobody to grandfather.
- Rank 7, the soft-curve work across about 25 pinned files (L): shrinks a long way, because a 200
  ceiling leaves most runaway magnitudes inflated rather than inverted.
- Rank 9, gain paths (L): shrinks the most. At a 200 cap the six weapon skills (ceiling about 220),
  Focus (200), Parry with a shield (380) and Mining sand (400) already reach it with no new content.
  The other 39 skills need a lift of about 40 points, not 840.

**Still required, unchanged:**
- **Rank 4** (M, about 8 pinned files): the chance-based exploits all sit below 160 and survive the
  lower ceiling. Hiding works in combat from 118; Stealing is never caught from 150; bard skills are a
  certain success from about 150, with Musicianship's uncapped difficulty reduction as the root cause;
  guards cannot reveal anyone hiding at 121+; Tinkering trap damage is uncapped from 120.
- **D42**, the salvage bag ingot dupe, starts at Mining 143 and is live now.
- **Rank 5** is the implementation: a per-character record in `ClusterFAccountData` keyed by serial
  (the `CharacterGuildData` pattern from P18), and `ClusterFSkillCaps.Apply` writing `cap = maxLevel`
  instead of a flat 300. `Apply` is a single chokepoint hooked to `WorldLoad` and `OnLogin`, so this
  is small.

## Rescaling the 200 ceiling forces

- `ClusterFSkillCaps`: individual cap 300 and the total, now both derived from max level.
- `ClusterFStatCaps`: the individual cap of 500 is live (it feeds the effective-stat patch), not dead config.
  Under the 2026-10-02 decision the effective clamp goes; the total of 1500 never binds and can go with it.
- The `skills.grandmaster` and `skills.triple_grandmaster` achievements are keyed to 300
  (`ClusterFAchievements.cs:950, :984-993`) and become unreachable.
- `ClusterFMiningExtension.cs:148-181`: the smithing ingot gates run 100 to 300, so everything above
  200 strands content, Celestial included.
- The Smith Seal catalog sells Blacksmithing scrolls at 305 to 320 (D43). Under this design those
  become level scrolls or they go.
- Pinned's `StatCapScroll` raises a total cap that no longer exists. Drop it from loot, or leave it inert.
- Two stale comments: `ClusterFMiningExtension.cs:148-150` still says scrolls raise the cap to 500, and
  `roadmap.md:457-500` claims Mining progression uses the full 0-300 range.

## A content consequence worth keeping

A 50 cap in loop 0 puts the whole extended resource system out of reach, because all 8 extended ores
require GM Mining at 100. That is not a problem, it is pacing, and the dungeon decision already covers
it: the four New Haven resources (Dawnstone, Burrowhide, Gloomsilk, Rootwood) are specified as a
**starter tier, low skill**, so they are the loop-0 resource game and the extended ores become the
reward for pushing max level to 100.

## Still open

1. The reserve cap, echo multipliers and step size above (placeholders).
2. What **current level** gates besides earning the next reset: stat and renown rewards, content
   access, titles. The cap comes from max level, so current level needs a job of its own.
3. Re-running the XP curve against the six-loop ladder.
4. **F-14's creature scale: answered 2026-10-01 (Chase). Everything above 160 is a custom creature we
   create.** So Bard difficulty (`BaseInstrument.GetBaseDifficulty`, hard cap 160, 68 creatures sitting
   on it including every boss) stays as the scale for ported creatures, and our own creatures carry
   their own level field above it. F-14 does not need a new scale for stock content, only a field on
   ours.
5. **A gain path for every skill, one skill at a time (Chase, 2026-10-02).** cc-P20 found 39 of 58 skills cannot gain
   past about 160 by use, because each use carries a fixed `maxSkill` (`SkillCheck.cs:58-61`). Each needs a use whose
   ceiling follows the cap, as our `Meditation.cs:92` already does (P20 recommendation 3, `cc-P20-skill-scaling-research.md:87`). Start from P20's per-skill
   tables (every gain call and its ceiling, with file:line). Shape: a notes-only pass that proposes a gain path per
   skill, then builder batches by skill group. Only needed once the F-12 cap goes above 160.
