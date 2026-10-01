# F-12 revised: levels, loops and caps (decided 2026-10-01)

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

## Stats (approved 2026-10-01)

**Per-stat ceiling rises with max level. Total stat cap rises with current level inside the loop.**
Both counters get a job.

| max level | per-stat | total base | with veteran |
|---|---|---|---|
| 50 | 125 | 325 | 375 |
| 100 | 140 | 370 | 420 |
| 125 | 155 | 415 | 465 |
| 150 | 170 | 460 | 510 |
| 175 | 185 | 505 | 555 |
| 200 | 200 | 550 | 600 |

The structure Chase set at the first row holds at every row: **base total + 50 veteran = 3 x the
per-stat ceiling.** So maxing all three stats is always the final achievement of a tier rather than
something a character drifts into, and specialization pressure never disappears. Everything tops out
together at 200: max level 200, skill cap 200, per-stat 200.

**Why per-stat had to move.** A per-stat ceiling of 125 caps the total at 375 no matter what, because
3 x 125 = 375. Raising only the total would have bought nothing but unusable headroom.

**Implementation.** Totals are free: `Mobile.StatCap` is per-mobile and serialized
(`Server/Mobiles/Mobile.cs:1731`, written `:2365`, read `:6332`), so our code writes it on login and on
level-up. The per-stat ceiling is the awkward one, because `_statMax` is a single global static
(`UOContent/Skills/SkillCheck.cs:23`, enforced `:337-341`). **Do it without patching pinned:** set the
global `stats.statMax` to the absolute ceiling of 200, then stop each character at their own ceiling
with **stat locks**. `CanRaise` already requires the lock to be `Up`, so locking a stat at the personal
max halts gain exactly, needs no patch, and reads correctly to the player because a locked stat visibly
says "not yet" instead of silently refusing.

`ClusterFStatCaps` already carries `DefaultIndividualStatCap = 500`, so per-stat above 125 was intended
once; it was simply never wired to anything that works.

**Open: nobody has surveyed stats above 125.** cc-P20 covered all 58 skills past 120 exhaustively but
spent about five lines on stats (its section 1.4). The two things it did find are encouraging: stats fit
the status packet, and max hits plateau around 300 to 345 even at 500 Str
(`Mobiles/PlayerMobile.cs:548-578`). But stats feed damage, hit chance, mana, stamina, carry weight and
regen at once, and 125 is the value every OSI formula is balanced around. The numbers in the table above
are approved in shape; the ceiling of 200 should be confirmed by a research pass before it ships.

## What each counter gates

Three counters, and putting a thing on the wrong one is how loop systems turn frustrating.

**Current level** resets every loop, so it gates what should be re-earned:
- **Total stat cap**, scaling toward the tier's base as current level approaches max level. This is what
  makes a reset feel like a reset: skills come back fast because gain is relative to the cap, so without
  this a freshly reset character would be weak in name only.
- **Level requirements on our gear only**, never on OSI items (the standing F-12 fidelity rule).
  **Exception, Chase 2026-10-01: the newbie dungeon's Tier 1 set carries no level requirement**, so it
  is wearable the moment a character resets. With the set blessed, no-trade and re-obtainable from the
  repeatable quest, Tier 1 is the guaranteed floor of every loop.
- Dungeon floor depth, so the dungeon is loop content rather than cleared once.

**Max level** only ever rises, so it gates permanent capability:
- Individual skill cap, and the total skill cap at 58 x max level.
- Per-stat ceiling (table above).
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
- `ClusterFStatCaps`: `DefaultIndividualStatCap = 500` and `DefaultTotalStatCap = 1500` are both wrong.
  The 500 looks like dead config, since the global 125 is what governs gain; CC should confirm and
  remove it rather than leave a second number that does nothing.
- The `skills.grandmaster` and `skills.triple_grandmaster` achievements are keyed to 300
  (`ClusterFAchievements.cs:950, :984-993`) and become unreachable.
- `ClusterFMiningExtension.cs:148-181`: the smithing ingot gates run 100 to 300, so everything above
  200 strands content, Celestial included.
- The Smith Seal catalog sells Blacksmithing scrolls at 305 to 320 (D43). Under this design those
  become level scrolls or they go.
- Pinned's `StatCapScroll` is built around OSI's base of 225 and defaults to 230, so it displays wrong
  against a base of 325. Retune or drop it, now that the veteran reward is the mechanism.
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
