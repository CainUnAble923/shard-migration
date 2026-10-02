# Sweep C: engine / core / pets / skills stat formulas above 125

Date: 2026-10-02. Read-only. Authority: pinned ModernUO D:\UO\ModernUO-pinned, commit 7c9215d97
(confirmed with `git log -1`). Paths below are relative to `D:\UO\ModernUO-pinned\Projects` unless
prefixed `SL:` = `D:\ShatteredLegacy\`. Numbers from `sweepC_calc.py` in this folder (rerunnable).

Column key for value tables: s125..s200 = player stat at that value with no item bonus (raw = effective);
e150/e225/e500 = effective stat at the clamp options (pinned CAP 150, F-12 candidate 225, today's 500).
Endgame fixed inputs unless stated: BonusHits 25 (ML cap), BonusStam/BonusMana 0, Human, Meditation 120,
Focus 120, RegenMana 18 (ML cap), RegenStam 24 (ML cap), RegenHits 18 incl. Human +2 (ML cap).

## 0. Ground truth established (all verified)

- Effective vs raw. `Mobile.Str` getter `Math.Clamp(m_Str + GetStatOffset(StatType.Str), 1, 65000)`
  (Server/Mobiles/Mobile.cs:1868); Dex/Int floor 0 (:1926, :1984). Raw setters clamp 1..65000 (:1833 area,
  `value = Math.Clamp(value, 1, 65000)`). Item stat bonuses and buffs arrive as StatMods summed by
  `GetStatOffset` (Mobile.cs:8428-8447). PlayerMobile Str/Int/Dex return `Math.Min(base.X, 150)` when
  `Core.ML && AccessLevel == Player` (UOContent/Mobiles/PlayerMobile.cs:588-630). Shard patch
  SL:server/patches/PlayerMobile-individual-stat-cap.patch replaces 150 with
  `ClusterFStatCaps.IndividualStatCap` (SL:server/customizations/ClusterFStatCaps.cs:103, default 500 from
  setting `clusterf.statCaps.individualCap`, :10/:20-23; falls back to 150 if disabled).
- Total stat cap. `Mobile.StatCap` default 225 (Mobile.cs:7720). Shard sets every player's StatCap to
  `clusterf.statCaps.totalCap` (default 1500) on world load and login (ClusterFStatCaps.cs:24, :82-107).
- Per-stat gain ceiling. `_statMax = stats.statMax` (UOContent/Skills/SkillCheck.cs:23, default 125 under LBR).
  Test shard value 500 is documented at SL:docker/uo/SERVER.md:642 (I did not open the live config file).
- RegenRates replacement: SL:docker/uo/apply-patches.sh:250 `replace_file "$CUSTOMIZATIONS/RegenRates.cs"
  "Projects/UOContent/Misc/RegenRates.cs"`; the additive flat copy at :193-201 explicitly excludes it
  (`! -name 'RegenRates.cs'`, :199). Dockerfile copies server/customizations to /customizations (Dockerfile:40).
  Live hits and stamina regen code is byte-for-byte the same logic as pinned (SL:server/customizations/RegenRates.cs:44-129
  vs UOContent/Misc/RegenRates.cs:44-129). Only mana regen differs (armored meditation above skill 200, :156-165).
- Skill stat influence (Server/Skills.cs:255-277, `RawStr * Info.StrScale + ...`) is DEAD under AOS:
  UOContent/Skills/SkillsInfo.cs:137-140 calls `AOS.DisableStatInfluences()` which zeroes all scales
  (UOContent/Misc/AOS.cs:15-26). No effect at any stat.

## 1. Formula catalogue

### 1.1 Player pools (the biggest felt effects)

F1. HitsMax, UOContent/Mobiles/PlayerMobile.cs:548-577
`strBase = Str; strOffs = BonusHits (ML cap 25 at :559-562); +20 Kitsune/GreyWolf; return strBase / 2 + 50 + strOffs;`
Reads EFFECTIVE Str (clamped at CAP). Own clamp: none on Str; BonusHits capped 25.

| s125 | s140 | s155 | s170 | s185 | s200 | e150 | e225 | e500 |
|---|---|---|---|---|---|---|---|---|
| 137 | 145 | 152 | 160 | 167 | 175 | 150 | 187 | 325 |

Verdict: RUNAWAY (slow, 0.5 HP per Str). OSI ceiling is 150 (effective Str 150 + 25 bonus). At raw 200 +
items under CAP 225: 187 HP (+25% over OSI). At today's CAP 500: 325 HP (more than double). A 200 Str
player survives every fixed-damage spike (EB, FS, special moves, explosion pots, boss AoE with fixed dice)
that kills an OSI-capped one; in PvP the classic "dump" (2-3 spells at ~40-60 each) needs one extra spell.

F2. StamMax, PlayerMobile.cs:581 `base.StamMax + BonusStam`; base = `Dex` (Server/Mobiles/Mobile.cs:2096).
EFFECTIVE Dex. No clamp, and no ML cap on BonusStam in this getter.
Values = Dex: 125/140/155/170/185/200, e150 150, e225 225, e500 500.
Verdict: RUNAWAY in pool size (combat consequences such as swing speed belong to the combat sweep).
In this domain: longer running before fatigue (1 stam per 17 running steps, StaminaSystem.cs:376-386, PM StepsMax 16
at PlayerMobile.cs:218): ~2125 steps at 125 vs ~3400 at 200; harder to drain with stamina-drain attacks that
take fixed amounts (EtherealWarrior.cs:102, Twaulo.cs:89, LordOaks.cs:146, Silvani.cs:66, CrystalLatticeSeeker.cs:116).

F3. ManaMax, PlayerMobile.cs:584-585 `base.ManaMax + BonusMana + (ML && Elf ? 20 : 0)`; base = `Int`
(Mobile.cs:2151). EFFECTIVE Int. Values = Int (+20 elf). Verdict: RUNAWAY in pool (spell-cost economics are the
magic sweep's). See F9 for the side effect on Meditation.

F4. MaxWeight, PlayerMobile.cs:237 `(Core.ML && Race == Race.Human ? 100 : 40) + (int)(3.5 * Str)`. EFFECTIVE Str.
Pinned backpack hard cap: UOContent/Items/Containers/Container.cs:252-262 returns 550 for an ML player's own pack.
Ours: SL:server/customizations/ClusterFBackpack.cs:33-42 replaces that with `m.MaxWeight`; every player pack is swapped
to ClusterFBackpack on connect (SL:server/customizations/ClusterFWeightPatch.cs:19-50).

| | s125 | s140 | s155 | s170 | s185 | s200 | e150 | e225 | e500 |
|---|---|---|---|---|---|---|---|---|---|
| MaxWeight human | 537 | 590 | 642 | 695 | 747 | 800 | 625 | 887 | 1850 |
| MaxWeight elf/garg | 477 | 530 | 582 | 635 | 687 | 740 | 565 | 827 | 1790 |
| pinned pack cap | 537 | 550 | 550 | 550 | 550 | 550 | 550 | 550 | 550 |

Verdict: pinned = PLATEAU at 550 pack contents (own clamp, Container.cs:256-259; MaxWeight above that only
matters for the overweight stamina test). Ours = RUNAWAY: pack capacity tracks MaxWeight with no ceiling.
At 200 Str a human hauls 800 stones of ore/logs/loot per trip vs 550 OSI (+45%); at e500, 1850 (3.4x). Directly
inflates gatherer income per trip and loot-run yield. Overweight stamina loss (StaminaSystem.cs:309-310, :423-436)
uses the same MaxWeight so it moves with it (consistent, no extra effect).

### 1.2 Regeneration (live file = pinned for hits/stam)

F5. Hits regen, SL:server/customizations/RegenRates.cs:44-86 (= pinned UOContent/Misc/RegenRates.cs:44-86).
`TimeSpan.FromSeconds(10.0 / (1 + points))`, points from RegenHits (player cap 18 at :67). No stat input.
Refill 0 to max at HPR 18: 72s / 76 / 80 / 84 / 88 / 92s; e150 79s, e225 98s, e500 171s.
Verdict: FINE (rate does not scale with stats; bigger pool simply takes longer to refill, which partly offsets F1).

F6. Stam regen, RegenRates.cs:88-129 (both files). `1.0 / (0.1 * (2 + points))`, points = Focus/10 + RegenStam (cap 24).
Reads `from.Stam / from.StamMax` only as a Focus gain-check ratio (:95). No stat input.
Refill 0 to max: 33s / 37 / 41 / 45 / 49 / 53s; e150 39s, e225 59s, e500 132s. Verdict: FINE.

F7. Mana regen AOS, ours RegenRates.cs:148-202 (pinned :148-196). `medPoints = from.Int + Meditation*3; medPoints *= 0.0275 (GM)`.
EFFECTIVE Int. Clamp: RegenMana capped 18 (ours :185-188), totalPoints floored (ML). No clamp on Int.

| | s125 | s140 | s155 | s170 | s185 | s200 | e150 | e225 | e500 |
|---|---|---|---|---|---|---|---|---|---|
| mana/s, MR18, not meditating | 3.9 | 3.9 | 4.0 | 4.0 | 4.0 | 4.1 | 4.0 | 4.2 | 4.9 |
| mana/s, meditating | 5.2 | 5.2 | 5.3 | 5.3 | 5.3 | 5.4 | 5.3 | 5.5 | 6.2 |
| empty to full, MR18 | 32s | 36s | 39s | 42s | 46s | 49s | 38s | 54s | 102s |

Verdict: FINE (Int adds ~0.0275 points per Int, about +0.2 mana/s from 125 to 200). Same in pinned and ours for stats.

F8. Pre-AOS mana regen branch (both files, ours :206-223): dead under AOS. Not evaluated.

### 1.3 Skills domain

F9. Meditation entry chance, ours SL:server/customizations/Meditation.cs:83 (= pinned UOContent/Skills/Meditation.cs:76):
`chance = (50.0 + (skillVal - (m.ManaMax - m.Mana)) * 2) / 100`. Reads POOL deficit, so EFFECTIVE Int via ManaMax.
No clamp (negative = never succeeds).

| Med 120 | s125 | s140 | s155 | s170 | s185 | s200 | e150 | e225 | e500 |
|---|---|---|---|---|---|---|---|---|---|
| at 0 mana | 0.40 | 0.10 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| at half mana | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.90 | 1.00 | 0.65 | 0 |

Verdict: BROKEN-ish inversion (cross-domain: skill check fed by a pool). Above Int ~145 a GM meditator cannot
enter meditation from empty; at Int 500 (today) not even from half. The skill becomes worse for higher-Int players.
Not a wrap, but a formula that goes to zero. Flag to the magic sweep too. (Our armored-meditation tweak at :86-87
only multiplies this chance further down.)

F10. Stat gain, UOContent/Skills/SkillCheck.cs.
- Pub45 path is live (`_usePub45StatGain = Core.ML`, :30). Chance per skill gain flat `0.05 * multiplier` (:272);
  75% primary stat (:275-277). Delay 3s per stat (`Core.ML ? 0.05 min`, :26). No term depends on the stat's
  current value: gaining 199 to 200 is as fast as 50 to 51.
- Ceiling: `CanRaise` `from.RawStr < _statMax` (:337-339) and `Math.Min(from.RawStr + 1, _statMax)` (:366, :387, :408).
  Reads RAW stats. Player also blocked when `RawStatTotal >= StatCap` (:327-333).
- Atrophy: `from.RawStatTotal / (double)from.StatCap >= Utility.RandomDouble()` (:473), and forced at the cap (:346).
  Only lowers a stat whose lock is Down and raw > 10 (:313-321).
Verdict: FINE as a formula (it is the clamp). Two facts for the builder: (a) with StatCap 1500 and _statMax 200,
the total is never reached (3 x 200 = 600), so the F-12 total cap (325..550/600) only bites if
`clusterf.statCaps.totalCap` is lowered to match; (b) atrophy probability at raw total 600 vs StatCap 1500 is 0.40
per gain, but it only does anything with a Down lock, so harmless.

F11. PET STAT GAIN, same file. `CanRaise` skips the StatCap check for controlled pets
(`if (!(from is BaseCreature creature && creature.Controlled))`, SkillCheck.cs:326-333) so a pet is limited ONLY by
`_statMax`. Pets run skill checks in combat and `Gain` (:203-282) applies the Pub45 stat roll to any mobile
(only Focus is excluded for creatures, :210-213). Stat locks default to Up (`StatLockType.Up = 0`, Mobile.cs:70-75).
Pet delay 5 min per stat (`stats.petGainDelay`, :27; used :420-430).
Effect: every controlled pet stat below `_statMax` creeps up to it. At 125 most tamables are already near
(OSI behaviour). At 200, a pet's Dex/Int/Str below 200 climbs to 200; at today's test value 500, to 500.
Pet HitsMax = Str only when unseeded (UOContent/Mobiles/BaseCreature.cs:579-580; StamMax :586-587, ManaMax :593-594);
seeded pets (SetHits) keep their HP, but Str/Dex still feed weapon damage and swing speed (combat sweep).
Verdict: RUNAWAY for pets, driven by the same setting as players. A 200 player's 200-Dex, 200-Str pet hits harder
and faster than any OSI tamed pet of the same species. Wild uncontrolled creatures are still blocked by
StatCap 225 default (Mobile.cs:7720).

F12. Skill stat bonus, Server/Skills.cs:255-277 (`Owner.Owner.RawStr * Info.StrScale + ...`). RAW stats.
Dead under AOS (all scales zeroed, AOS.cs:15-26 via SkillsInfo.cs:137-140). Verdict: FINE (zero at every value).
(Side note, only matters if AOS were off: skills.json holds already-divided scales, e.g. Alchemy DexScale 0.05,
and the JsonConstructor divides by 100 again, Server/Skills.cs:407-409, while StatTotal 10 is set unscaled.
Not live; not pursued.)

F13. Anatomy, UOContent/Skills/Anatomy.cs:59-88. `str = targ.Str +/- margin; strMod = str / 10` clamped 0..10.
EFFECTIVE target stats. Own clamp at 100. All columns give strMod 10 ("superhumanly strong").
Verdict: PLATEAU at stat 100 (cosmetic message only; message table is safely clamped).

F14. Animal Lore, UOContent/Skills/AnimalLore.cs:119-134. Displays `c.Hits/HitsMax`, `c.Str` etc as text
(FormatStat :402, FormatAttributes :392). Strings, no width limit. Verdict: FINE.

F15. Animal Taming, UOContent/Skills/AnimalTaming.cs:44-61. `MustBeSubdued: bc.Hits > bc.HitsMax / 10`;
`ScaleStats` multiplies creature raw stats. Creature only. No player stat read; control chance
(BaseCreature.cs:1408 GetControlChance) reads no stat. Verdict: FINE.

F16. Focus: only in RegenRates (F6, F7); value of Focus skill, no stat. FINE.

F17. Character creation, pinned UOContent/Engines/Character Creation/CharacterCreation.cs:399-415 and ours
SL:server/customizations/CharacterCreation.cs:379-394 (same): each stat 10..60, total 80 or 90; staff branch sets 100
(pinned :274-276, ours :254-256). Verdict: FINE (unaffected by the raise).

F18. TestCenter `set str/dex/int`, UOContent/Special Systems/Engines/TestCenter.cs:90, :112, :134
`if (value is < 10 or > 125)`. RAW. Own clamp 125. Verdict: PLATEAU at 125 (test-only command; only matters if
`testCenter.enable` is on, :19, which I did not check on the test shard). Our TestCenterKit only preserves StatCap
(SL:server/customizations/TestCenter/TestCenterKit.cs:160-175).

F19. Resurrection: stat loss `TryGiveStatLoss` (UOContent/Gumps/ResurrectGump.cs:30-58) returns at once when
`Core.AOS` (:32). Dead. Res HP `AOS.Scale(from.HitsMax, 20/40/80)` (:228-230) and `HitsMax * _hitsScalar` (:270),
pet `_pet.HitsMax * _hitsScalar` (PetResurrectGump.cs:85): proportional. Verdict: FINE.

### 1.4 Stamina system (UOContent/Misc/StaminaSystem.cs)

F20. FatigueOnDamage :283-296, called from PlayerMobile.OnDamage (PlayerMobile.cs:2379) BEFORE hits drop
(Mobile.cs:5953 OnDamage precedes :5964-5973). Standard: `damage * (100.0 / m.Hits) * ((double)m.Stam / 100) - 5.0`
= damage * Stam / Hits - 5. POOLS. No clamp except >0.
40 damage at full pools, Str = Dex = s: 31/33/35/37/39/40, e150 35, e225 43, e500 56 stamina lost;
as % of StamMax: 25/24/23/22/21/20%, 23%, 19%, 11%. Verdict: FINE (proportional; high stats lose a smaller share).
Note: Hits == 0 at entry would divide by zero into infinity; not stat-related, pre-existing.

F21. Running costs :349-388: `--from.Stam` per StepsMax+1 running steps and extra `--Stam` when
`Stam / StamMax < 0.10` (:356). Flat costs; pool size from F2. Verdict: FINE (see F2 for the effect).

F22. Overweight :309-345 and :423-436: `5 + overweight / 25` stamina per step, x2 running, /3 mounted. Uses MaxWeight
(F4). Verdict: FINE in itself.

F23. Shove, Server/Mobiles/Mobile.cs:4456-4459 `if (Stam == StamMax) ... Stam -= 10`. POOL. Verdict: FINE.

### 1.5 Packets / client fields (Server/Network/Packets/OutgoingMobilePackets.cs)

F24. 0x11 status, :497-570. Writes `(short)` for Str, Dex, Int (:523-525), Stam, StamMax, Mana, ManaMax (:527-530),
weight `(short)(BodyWeight + TotalWeight)` (:534), MaxWeight (:538), StatCap (:542); HitsMax/Hits via WriteAttribute
as short (:511, :166-195). AttributeMaximum = 100 (:32); normalised value `cur * 100 / max` is int math, max
65000 * 100 = 6.5M, no overflow.
Player values at e500: Str 500, HitsMax 325, StamMax 500(+bonus), MaxWeight 1850, StatCap 1500: all far below 32767.
Overflow only for values > 32767: stats are clamped at 65000 for staff/creatures (Mobile.cs:1868) and creature
HitsMax seed clamps at 65000 (BaseCreature.cs:580), so a creature or GM with > 32767 shows a negative/garbled
number. Players cannot reach it (CAP 500, MaxWeight needs Str ~9300). Verdict: FINE for all F-12 options.

F25. 0xA1/0xA2/0xA3/0x2D, :210-299: same WriteAttribute shorts. FINE.

F26. Guild/party map, UOContent/Network/MapUO.cs:91 `(byte)(m.Hits * 100 / Math.Max(m.HitsMax, 1))`: 0..100, FINE.

### 1.6 Creature formulas that read a PLAYER's stats or pools

| # | file:line | code | reads | verdict |
|---|---|---|---|---|
| F27 | UOContent/Misc/Poison.cs:120-121 | `1 + (int)(_mobile.Hits * _poison._scalar)`, clamp min..max (AOS table UOContent/Misc/PoisonKinds.cs:79-83) | player current Hits | PLATEAU (own clamp). Lethal 48 at s125, 50 from s140 up; as % of HitsMax 35% falls to 29% at s200, 15% at e500. Deadly capped 30 at every column. Players benefit slightly. |
| F28 | UOContent/Mobiles/Abilities/DeathExplosion.cs:43 | `AOS.Damage(defender, ..., defender.HitsMax / 5, true, ...)` | target HitsMax | FINE (proportional 20%): 27/29/30/32/33/35, e150 30, e225 37, e500 65 |
| F29 | Mobiles/Monsters/LBR/Meers/MeerEternal.cs:110 | `(int)(m.Hits * scalar) +/- 5` (0.75/0.5/0.25) | target Hits | FINE (proportional) |
| F30 | Mobiles/Monsters/ML/Special/Meraktus.cs:241, Mobiles/Special/Rikktor.cs:122 | `Math.Clamp((int)(m.Hits * 0.6), 10, 75)` | target Hits | PLATEAU at 75 (reached at Hits 125); 75 in every column, so it hurts high-HP players proportionally less |
| F31 | Mobiles/Monsters/Misc/Melee/PlagueBeast.cs:89 | `IncreaseHits(ceil(corpse.Owner.HitsMax * 0.75))` | dead player's HitsMax | creature only; beast gains 103..132 (s125..s200), 244 at e500 |
| F32 | Mobiles/BaseCreature.cs:2420-2421 | `FightMode.Strongest => Tactics + m.Str`, `Weakest => -m.Hits` | target effective Str / Hits | FINE (target choice only) |
| F33 | Mobiles/Monsters/Misc/Melee/AnimatedWeapon.cs:89, BladeSpirits.cs:61, EnergyVortex.cs:69 | `m.Str / dist`, `(m.Str + Tactics) / dist`, `(m.Int + Magery) / dist` | target effective stat | FINE (target choice; high-stat players attract summons a bit more) |
| F34 | Mobiles/AI/MageAI.cs:389, :569 | `psDamage > c.Hits`; `c.Int < c.Dex` picks Feeblemind/Clumsy | target pools/stats | FINE |
| F35 | Mobiles/AI/ThiefAI.cs:95 | `fleeChance = 10 + Math.Max(0, combatant.Hits - Mobile.Hits)` | target Hits | creature only, FINE |
| F36 | Mobiles/BaseCreature.cs:3617, :5418-5419 | pet heals owner when `owner.Hits < HealOwnerTrigger * owner.HitsMax` | owner pools, ratio | FINE |
| F37 | Mobiles/AI/HealerAI.cs:165-167 | `m.Hits < m.HitsMax - 40 / - 10` | ally pools, absolute | FINE |
| F38 | Mobiles/Animals/Mounts/Kirin.cs:80, Unicorn.cs:78 | `Rider.Hits - damage < 30 / 40` | rider Hits, absolute | FINE (triggers relatively later for high-HP riders) |
| F39 | Mobiles/Abilities/DrainLifeAttack.cs:35, Golem.cs:153-160, EtherealWarrior.cs:102-112, Twaulo.cs:89-90, LordOaks.cs:146-156, Silvani.cs:66-67, CrystalLatticeSeeker.cs:106-126 | fixed-amount drains of target Stam/Mana/Hits | target pools | FINE (fixed amounts; matter less vs larger pools) |
| F40 | Mobiles/Guards/BaseGuard.cs:290, :320 | `target.Damage(target.HitsMax, _owner)` | target HitsMax | FINE (always lethal) |
| F41 | Mobiles/Healers/BaseHealer.cs:119, :144 | `m.Hits = m.HitsMax` | pools | FINE |
| F42 | Engines/Factions/Mobiles/Guards/GuardAI.cs:746-748 | `GetStatMod(combatant, ...)` chooses debuff | target stat MODS, not values | FINE |

Creature only (own stats, brief): BaseCreature.cs:579-594 HitsMax/StamMax/ManaMax seed or stat, clamp 65000;
AIMovement.cs:27-28, :78; BaseAI.cs:623; MeleeAI.cs:144; ThiefAI.cs:93, :146; MageAI.cs:94, :140-163
(`Math.Sqrt(600 - Int)` guarded by `Int >= 500`, :163); AITimer.cs:97 `30000 / _owner.Mobile.Int` (divides by zero
for an Int-0 creature; pre-existing, creature only); GuardAI.cs:117-807 own pools, :237 own Int; MagicalBarrier.cs:22;
FireBreath.cs:209 `source.Hits`; Paragon.cs:62-68, :126-132, :242; JukaMage.cs:131-190 (buffs a Juka lord);
MeerCaptain.cs:123; BogThing.cs:98; HarrowerTentacles.cs:159; DemonKnight.cs:135, Misc/LootPack.cs:94,
Engines/Quests/The Summoning/Objectives.cs:123 (looting rights by the dead creature's HitsMax); DarkWolf.cs:59,
ShadowWisp.cs:92 (familiar +1 stam/mana).

## 2. Searches with no player-felt hit

- Table indexed by a stat value (`[ ... .Str|Dex|Int|Hits|Stam|Mana ... ]`) across Server and UOContent: 0 hits.
- Narrow casts of a stat: only OutgoingMobilePackets.cs:523-542 (short, F24) and MapUO.cs:91 (byte percent, F26).
  Same grep over SL:server/customizations and SL:server/patches: 0 hits.
- Stat as divisor: StaminaSystem.cs:287-288 (Hits, F20), AITimer.cs:97 (creature Int). Nothing else.
- Mount/ethereal Str/Dex checks: grep `\.(Str|Dex|Int|RawStr|RawDex|RawInt|StamMax|HitsMax)\b` in
  UOContent/Mobiles/Animals/Mounts: 0 hits. Mount stamina uses steps (StaminaSystem.cs:391-421), no stat.
- No Misc/WeightOverloading.cs exists at the pinned commit; its role is StaminaSystem.cs (grep of MaxWeight across
  Projects listed every implementation: Container.cs:144/155/161, Mobile.cs:1023, PlayerMobile.cs:237,
  Containers/Container.cs:21/252, StaminaSystem.cs:298, plus readers Ore.cs:333, BaseTalisman.cs:458, Banker.cs:487).
  Ours: ClusterFBackpack.cs:33, ClusterFWeightPatch.cs; other customization DefaultMaxWeight overrides are fixed
  numbers on special containers (ArtificersSatchel 500, PackMuleBackpack 4000, FirstAidBelt 100, two satchels by tier).
- Files checked with nothing player-felt: Server/Items/Item.cs (:2097 is a doc comment), Engines/Spawners/SpawnPropsGump.cs
  (:30-34 property names), PlayerMobile.cs ValidateEquipment :1331-1460 (reads effective Str/Dex/Int vs item requirements;
  higher stats only make equip easier, FINE), PlayerMobile.cs:4166 OnRawStatChange (empty),
  Mobile.cs:8395-8447 StatMod plumbing, Mobile.cs:8895-8940 regen timers (+1 per tick), Mobile.cs:7814-7825 InitStats,
  SL PetMimic*.cs (only show item bonus totals; item side belongs to the item sweep), SL ClusterFStatInspect.cs (display),
  SL ClusterFDevTools.cs:122-127 (resets a test char to 10/10/10).

## 3. Ranked runaways / brokens (worst first)

1. F11 Pet stat gain uncapped except by `stats.statMax` (SkillCheck.cs:326-339). Today's test value 500 lets every
   controlled pet climb each stat to 500; at 200 to 200. Silent, applies to all pets, and it rides on the player change.
2. F1 Player HitsMax (PlayerMobile.cs:548-577): 137 at 125, 175 at 200, 187 at e225, 325 at e500. Largest survivability
   change in this domain.
3. F4 Carry capacity, ours only (ClusterFBackpack.cs:33-42 replacing Container.cs:252-262's 550): 800 at 200,
   887 at e225, 1850 at e500 vs OSI 550. Direct economy inflation.
4. F9 Meditation entry chance goes to 0 as ManaMax grows (Meditation.cs:76 pinned / :83 ours). Above Int ~145 a GM
   cannot meditate from empty; at e500 not from half. Inverted reward. (Magic-sweep overlap.)
5. F2/F3 StamMax and ManaMax 1:1 with effective Dex/Int, unbounded below CAP. Pool size itself; consequences mostly
   in combat and magic sweeps.
Plateaus that hide the raise: F13 Anatomy (100), F18 TestCenter (125), F27 Poison (max dmg), F30 Meraktus/Rikktor (75),
pinned backpack 550, and the pinned effective CAP 150 itself (raw 200 is worth nothing above 150 if CAP stays 150).
No overflow/wrap is reachable by a player at any F-12 option (F24).

## 4. Places a builder would touch

- Per-stat raw ceiling: setting `stats.statMax` read at UOContent/Skills/SkillCheck.cs:23 (test shard 500 per
  SL:docker/uo/SERVER.md:642). Used at :337-339, :366, :387, :408.
- Pet decoupling (needed if pets should stay at OSI 125): UOContent/Skills/SkillCheck.cs:324-340 CanRaise (add a
  separate pet max for `BaseCreature { Controlled: true }`), or a pet-side override. Pinned code.
- Effective clamp: SL:server/patches/PlayerMobile-individual-stat-cap.patch (PlayerMobile.cs:594/609/624) and setting
  `clusterf.statCaps.individualCap` (SL:server/customizations/ClusterFStatCaps.cs:10, :20-23, :103).
- Total cap: `clusterf.statCaps.totalCap` (ClusterFStatCaps.cs:11, :24, applied :107). Must be lowered to the F-12
  total, or 3 x statMax is the real total.
- HitsMax: UOContent/Mobiles/PlayerMobile.cs:556-576 (e.g. cap strBase, or keep and accept).
- Carry weight: SL:server/customizations/ClusterFBackpack.cs:33-42 (cap at a number) and/or PlayerMobile.cs:237.
- Meditation chance: SL:server/customizations/Meditation.cs:83 (pinned Skills/Meditation.cs:76) if pool growth is kept.
- TestCenter limit 125: UOContent/Special Systems/Engines/TestCenter.cs:90, :112, :134 (only if TC is used for testing).
- Nothing to change in packets (OutgoingMobilePackets.cs) or MapUO for any F-12 option.

## 5. Unverified

- The live test-shard config file value of `stats.statMax` (I relied on the brief plus SERVER.md:642) and whether
  `testCenter.enable` is on.
- How many tamable species lack SetHits (seeded HitsMax), i.e. whose HP would grow with pet Str gains (F11). Not counted.
- Whether pets actually reach the Pub45 stat roll often in practice (depends on pet skill gain rate; 5 min delay per stat).
- Effect of F2/F3/F11 on swing speed, weapon damage, spell damage: belongs to other sweeps; not evaluated here.
- F12 double-division of skill stat scales: reasoned from System.Text.Json constructor binding, not run. Dead under AOS anyway.
