# cc-P25: stats above 125, research only (F-12)

Written 2026-10-02 by CC. Read only: nothing built, committed, deployed or placed. No D or Q number taken.
Authority: pinned ModernUO `D:\UO\ModernUO-pinned` at `7c9215d97cb25c56b0b5cb35034944ccdaa0a485` (checked with
`git rev-parse HEAD`). Pinned paths are relative to `Projects\`; "ours" paths are relative to `D:\ShatteredLegacy\server\`.

**Chase decided 2026-10-02; see `notes\p25-decisions-2026-10-02.md`:**
- No ceilings of any kind: no per-stat table, no effective clamp, no total cap, no formula soft caps.
- No bandage floor; pets follow players.
- Carry weight uncapped; a reset keeps stats.

The recommendations in Parts 3 to 5 below are kept as the record of what was weighed, but they are declined.

## Headlines

1. **The raw per-stat ceiling is 500 today, not 125.** Live and test configs both set `stats.statMax = 500`
   (`uo\modernuo\Configuration\modernuo.json:160`, `Configuration-test\modernuo.json:165`), a deliberate May 2026
   change recorded only in the shard repo (`D:\ShatteredLegacy\docker\uo\SERVER.md:642`). F-12's "125 to 200" is a
   **cut from 500 to 200**. The F-12 notes, the arch verdict and P20 all assumed 125.
2. **200 holds**, as approved, with three must-fix items. None of them changes the table:
   - Self-bandage speed has no floor. It takes 1.0 s at Dex 200 against OSI's 3.5 s, and is instant from Dex 220.
     Fixing it needs a one-line pinned patch.
   - Controlled pets inherit the global ceiling. They creep to 500 today, and would creep to 200 under F-12. The fix
     goes in our skill-gain wrapper, with no patch.
   - The meditation start chance inverts as the mana pool grows. The fix goes in our own `Meditation.cs`.
3. **The worst runaway is self-bandage** (`UOContent/Items/Skill Items/Misc/Bandage.cs:493`). At max level a
   character heals about 57 HP/s on themselves with no items. It is reachable at raw 200 alone, and at any effective
   cap of 220 or more it is instant. The next two are carry weight, which is ours (800 to 1850 stones against OSI's
   550), and swing speed from stamina, which a Pet Mimic's +150 stamina already floors at OSI stats.
4. **Effective cap: recommend 225, applied per character as "personal ceiling + 25".** It keeps OSI's +25
   headroom at every loop (150 at loop 0, which is exactly OSI), and it is the only option that stops loop-0
   characters from reaching 225 through imbuing. Today's single global 500 lets gear reach 500 at any loop.
5. **Stat offsets on this shard are far above OSI's +25.** Imbuing gives +15 Str/Dex/Int per item on any slot,
   and a Pet Mimic gives +50 to each. A fully geared character carries about +130 to +380 per stat. So the
   effective clamp decides the outcome for geared players, not the raw ceiling.
6. **Two design facts F-12 relies on are untrue in pinned:**
   - Lowering `StatCap` below a character's total never reduces their stats (`SkillCheck.cs:313-321`, `:327-333`).
     A reset must write stats down explicitly.
   - Talisman and quiver stat bonuses are probably never removed on unequip (`UOContent/Misc/AOS.cs:598` vs `:620`).
     That would make the effective clamp the only bound on stacking.

## 0. Before building on the brief: what was checked, and what was wrong

**Builder check.** `D:\ShatteredLegacy`: `git --no-optional-locks status` showed `main`, up to date, clean, at HEAD
`0f4c989`. I did **not** run the test host. P27 is a builder that may start beside this pass, so all work was done by
reading code, plus throwaway Python in `notes\cc-P25-scratch\`.

**P27 started mid-task.** At the end of this pass, `D:\ShatteredLegacy` was dirty with P27's work, none of it mine:
- modified: `ArtificersImbueGump.cs`, `GuildResources.cs`, `SOURCE.txt`;
- new: a Fountain of Fortune seeder and two test files.

Every "ours" line number in these notes is against committed HEAD `0f4c989`. One of them has already moved in the
working tree: the imbue intensity table, `ArtificersImbueGump.cs:1667-1674` at HEAD, is about `:1679` now. The
stat-property lines `:182-195` have not moved.

**Numbering.** No clash. `cc-prompts` holds P25, P27 and P28. P27 and P28 both refer to P25 as this stats research.
P26's notes are committed.

**The brief's five facts.**

| # | brief says | verdict |
|---|---|---|
| 1 | gain stopped by a single global `_statMax` (`SkillCheck.cs:23`, enforced `:337-341`) | **Correct** as a mechanism: `:23`, checked at `:335-341`, clamped again at `:366`, `:387`, `:408`. **Wrong in value**: the brief, `f12-levels-loops-caps.md` ("the global 125 is what governs gain") and the arch verdict ("Gain is still stopped at 125 by `_statMax`") all assume 125. Live and test configs set 500 (headline 1). |
| 2 | `Mobile.StatCap` per mobile, serialized (`Mobile.cs:1731`, `:2365`, `:6332`) | Correct. The default is 225 (`:6357`, `:7720`). Ours overwrites it with 1500 on login and world load (`customizations\ClusterFStatCaps.cs:107`). |
| 3 | max hits plateau about 300 to 345 at 500 Str (`PlayerMobile.cs:548-578`) | **The numbers are right but "plateau" is wrong.** HitsMax is linear in effective Str (`Str/2 + 50 + min(BonusHits, 25)`, `:576`). 325 (345 in Kitsune or Grey Wolf form, `:565-569`) is only where today's 500 clamp stops Str. Nothing in the formula plateaus. |
| 4 | the patch makes the effective clamp 500; `base.Str` includes offsets (`Mobile.cs:1866-1868`) | Correct. The getter is at `Mobile.cs:1868`. The patch hunks are at pinned `PlayerMobile.cs:594`, `:609`, `:624`. `ClusterFStatCaps.IndividualStatCap` is 500 (`:10`, `:103`; live config `:112`). |
| 5 | the stat lock is client-controlled (`IncomingExtendedCommandPackets.cs:301-322`) | Correct: `StatLockChange` at `:301` writes the lock with no check. |

P20 section 1.4.4 also guessed the live `statMax` was probably 125; it is 500.

**Another correction.** The prompt names "Misc/WeightOverloading.cs" by implication. It does not exist at the
pinned commit; weight and stamina live in `UOContent/Misc/StaminaSystem.cs`.

## Part 1: every place a stat is read

**Method.**
- Counted grep of pinned `Projects` for qualified reads of `.Str .Dex .Int .RawStr .RawDex .RawInt .HitsMax .StamMax
  .ManaMax .RawStatTotal`: 382 lines in 93 files (`cc-P25-scratch\pinned-stat-reads.txt`, `pinned-stat-files.txt`).
- Reads of the pools `.Stam .Mana .Hits`, excluding assignments: 170 lines, adding 32 more files
  (`pinned-pool-reads.txt`).
- Unqualified reads inside `Mobile`, `PlayerMobile` and `BaseCreature` were read by hand.
- Ours: 37 files by a first grep (`ours-stat-files.txt`) and 178 by a wider identifier grep (`my-grep.txt`). The
  extra 141 are item definitions setting `Attributes.Bonus*` or requirements, covered in aggregate.
- Four domain sweeps did the reading: `sweep-A-melee-items.md`, `sweep-B-magic.md`, `sweep-C-engine.md` and
  `sweep-D-ours.md`. They hold the full tables, and each has a rerunnable `*_calc.py`.
- I re-read every runaway and broken row below in the source myself before keeping it. One sweep claim was wrong
  and is corrected in 1.2.

**Which value a formula sees.**
- `.Str/.Dex/.Int` on a player is the **effective** value: raw plus every StatMod, then
  `Math.Min(..., IndividualStatCap)`, under ML for AccessLevel Player (`PlayerMobile.cs:588-630` plus our patch).
- `.RawX` is raw.
- No live player-felt formula in pinned reads raw, except Bless and curse magnitudes (`SpellHelper.cs:402-407`).
  The others that read raw run only before AOS (Concussion Blow `BaseAxe.cs:129`, `BasePoleArm.cs:79`; Discordance
  `Discordance.cs:206-231`). So **the effective clamp governs everything**, and the raw ceiling matters only through
  it and through gain.

**Live branches.** The expansion is Endless Journey (`Configuration\expansion.json`, Id 11; AOS, SE, ML, SA, TOL
and EJ all true). Pre-AOS branches are listed as "not live" and not tabled.

**Columns.**
- 125 to 200 is the stat with no offsets.
- e150, e225 and e500 are the effective value at those clamps.
- Where a formula has other inputs, they are fixed as stated in the row: skills at 120, and SSI, DI and SDI at
  their caps.

### 1.1 Pools

| formula | file:line | reads | own clamp | 125 | 140 | 155 | 170 | 185 | 200 | e150 | e225 | e500 | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| HitsMax `Str/2+50+min(BonusHits,25)` (+20 two forms) | `UOContent/Mobiles/PlayerMobile.cs:548-577` | eff Str | BonusHits 25 (`:559-562`); none on Str | 137 | 145 | 152 | 160 | 167 | 175 | 150 | 187 | 325 | runaway (slow) |
| StamMax `Dex + BonusStam` | `PlayerMobile.cs:581`, `Server/Mobiles/Mobile.cs:2096` | eff Dex | none; BonusStam uncapped | 125 | 140 | 155 | 170 | 185 | 200 | 150 | 225 | 500 | runaway (pool; see swing speed) |
| ManaMax `Int + BonusMana (+20 elf)` | `PlayerMobile.cs:584-585`, `Mobile.cs:2151` | eff Int | none; BonusMana uncapped | 125 | 140 | 155 | 170 | 185 | 200 | 150 | 225 | 500 | runaway (pool) |
| Pool setters clamp to max | `Mobile.cs:2011`, `:2067`, `:2112` | | | | | | | | | | | | fine |
| HP regen | ours `customizations\RegenRates.cs:44-86` (live; replaces pinned via `docker\uo\apply-patches.sh:250`) | no stat | RegenHits 18 | no stat term | | | | | | | | | fine |
| Stam regen | ours `RegenRates.cs:88-129` | no stat (Stam/StamMax only as a Focus gain ratio, `:95`) | RegenStam 24 | | | | | | | | | | fine |
| Mana regen `(Int + Med*3) * 0.0275 + ...`, mana/s at Med 120, Focus 120, MR 18 | ours `RegenRates.cs:148-202` (stat term same as pinned `:146-196`) | eff Int | meditating bonus 13, MR 18 | 3.9 | 3.9 | 4.0 | 4.0 | 4.0 | 4.1 | 4.0 | 4.2 | 4.9 | fine (+0.2 mana/s from 125 to 200) |

### 1.2 Melee, healing and items

| formula | file:line | reads | own clamp | 125 | 140 | 155 | 170 | 185 | 200 | e150 | e225 | e500 | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ML swing delay `floor((speed*4 - Stam/30) * 100/(100+SSI))` ticks of 0.25 s; bow 4.25 at SSI 60, Stam = Dex | `UOContent/Items/Weapons/BaseWeapon.cs:1428-1431` | current Stam | SSI 60 (`:1419-1422`); 1.25 s floor (`:1446-1449`) | 2.00 | 2.00 | 1.75 | 1.75 | 1.50 | 1.50 | 1.75 | 1.50 | 1.25 | runaway to the floor |
| same, heavy crossbow 5.0 at SSI 0 | same | | | 4.00 | 4.00 | 3.75 | 3.75 | 3.50 | 3.50 | 3.75 | 3.25 | 1.25 | runaway |
| Str melee damage bonus `GetBonus(Str, 0.3, 100, 5)`; total multiplier with Anat/Tac 120, DI 100 | `BaseWeapon.cs:2556`, `:2502-2512`, sum `:2599-2602` | eff Str | none ("No caps apply", `:2552-2555`) | 3.888 | 3.933 | 3.978 | 4.022 | 4.067 | 4.112 | 3.962 | 4.188 | 5.012 | runaway (mild to 225, +26.5% over OSI at 500) |
| Hit-spell Int bonus `Int/10`, avg Hit Lightning | `BaseWeapon.cs:2265` | eff Int | none | 28.6 | 29.1 | 29.3 | 29.8 | 30.1 | 30.6 | 29.3 | 31.1 | 38.2 | runaway (mild) |
| Hit chance, defense chance | `BaseWeapon.cs:1235-1366` | no stat | HCI/DCI 45 | | | | | | | | | | fine |
| Parry low-Dex penalty | `BaseWeapon.cs:1535-1538`, `:1574-1577` | eff Dex | flat at 80 and above | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | fine |
| Thrown range, Soul Glaive (design max 11) | `UOContent/Items/Weapons/Throwing/BaseThrown.cs:24` | eff Str | none | 10 | 11 | 11 | 12 | 12 | 13 | 11 | 14 | 24 | runaway (past design from Str 164; 24 tiles at 500 exceeds the update range of 18, `Server/Main.cs:150`) |
| Force of Nature bonus | `UOContent/Items/Weapons/Abilities/ForceOfNature.cs:106` | eff Str | 100 | 1.75 | 1.90 | 2.00 | 2.00 | 2.00 | 2.00 | 2.00 | 2.00 | 2.00 | plateau at Str 150 |
| Concussion Blow (SA) | `Abilities/ConcussionBlow.cs:47-58` | defender pool ratios | 20 | | | | | | | | | | fine |
| Throwing dagger hit chance `1 - 0.8*sqrt(Dex/100)` | `UOContent/Items/Weapons/Knives/ThrowingDagger.cs:57` | target eff Dex | none | 10.6% | 5.3% | 0.4% | 0 | 0 | 0 | 2.0% | 0 | 0 | broken (immune from Dex 157); GM-spawn item only |
| **Self bandage delay** `5.0 + 0.5*(120 - Dex)/10` | `UOContent/Items/Skill Items/Misc/Bandage.cs:484`, `:493` | eff Dex | **none** | 4.75 s | 4.00 | 3.25 | 2.50 | 1.75 | **1.00** | 3.50 | **8 ms** | **8 ms** | **runaway, worst** (see 2.1) |
| Bandage on others `3.2 - sin(Dex/130)*2.5` | `Bandage.cs:506-513` | eff Dex | 0.70 s from Dex 204 | 1.15 | 1.00 | 0.88 | 0.79 | 0.73 | 0.70 | 0.91 | 0.70 | 0.70 | plateau at Dex 204 |
| Item stat requirements, equip checks | `BaseWeapon.cs:1049-1061`, `Items/Armor/BaseArmor.cs:826-846`, `:1128-1148`, `Items/Clothing/BaseClothing.cs:484-536`, `Items/Jewels/BaseJewel.cs:211-231`, `PlayerMobile.cs:1331-1460` | eff | thresholds; ours max StrReq 80 (sweep D 2.Q) | | | | | | | | | | fine |
| Item stat bonuses (talisman, quiver, clothing, spellbook) | `UOContent/Misc/AOS.cs:590-625`, `Spellbook.cs:565-585` | summed into StatMods | **no total cap** | | | | | | | | | | the source of offset; see 2.6 for a probable unequip leak |
| Potions: Agility, Strength (flat, x Enhance Potions), Refresh (% of StamMax), Heal | `Items/Skill Items/Magical/Potions/*/Base*Potion.cs:25-32`, `BasePotion.cs:207-218` | pool or flat | | | | | | | | | | | fine (they feed offset) |
| Poison damage `1 + Hits*scalar`, clamped | `UOContent/Misc/Poison.cs:120-121`, `Misc/PoisonKinds.cs:79-83` | victim current Hits | per-level max (Lethal 50) | 48 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | plateau (high HP takes a smaller share) |
| Bleed, Talon Strike, mace and staff stamina drain | `BleedAttack.cs:74`, `TalonStrike.cs:86`, `BaseBashing.cs:24`, `BaseStaff.cs:23` | none | | | | | | | | | | | fine |
| Weapon abilities, Bushido, Ninjitsu, SpecialMove | `WeaponAbility.cs:307`, `:324`; `SpecialMove.cs:103`, `:117`; `SamuraiSpell.cs:53-86`; `NinjaSpell.cs:52-85`; `AnimalForm.cs:133-157`, `:453-473` | mana pool checks only | | | | | | | | | | | fine |
| Fatigue on damage `damage * Stam / Hits - 5` | `UOContent/Misc/StaminaSystem.cs:283-296` (from `PlayerMobile.cs:2379`) | pools | > 0 | | | | | | | | | | fine (proportional) |
| Running and overweight stamina | `StaminaSystem.cs:309-345`, `:349-388`, `:423-436` | MaxWeight, pool | | | | | | | | | | | fine |
| Virtues (Honor, Sacrifice), crafting costs, duels, King of the Hill, Storm's Eye, food, magic fish, Rose of Trinsic, rejuvenation ankh | `Honor.cs:134`, `Sacrifice.cs:108`, `CraftItem.cs:287-299`, `DuelContext.cs:742-744`, `KingOfTheHill.cs:93`, `StormsEye.cs:103-110`, `Food.cs:94-96`, `MagicFish.cs:19`, `RoseOfTrinsic.cs:180`, `RejuvinationAnkhs.cs:23-49` | creature HP, pools, flat | | | | | | | | | | | fine |

**Correction to sweep A.** It read a negative bandage delay as an index exception or a 32-second stall in the timer
wheel. It is neither. The `Timer.Delay` setter (`Server/Timer/Timer.cs:67`) routes through
`RoundTicksToNextPowerOfTwo`, which returns 8 ms for any value at or below 0 (`Server/Timer/Timer.TimerWheel.cs:174-179`).
A negative delay is simply an instant bandage. That is worse for balance and harmless for the server.

### 1.3 Magic

| formula | file:line | reads | own clamp | 125 | 140 | 155 | 170 | 185 | 200 | e150 | e225 | e500 | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Spell damage `Int/10` added to damageBonus; Flame Strike PvP avg at Inscr 120, Eval 120, SDI 15 | `UOContent/Spells/Base/Spell.cs:226-227` (chain `:219-257`; 15 callers across Magery and Mysticism) | eff Int | **none**; the PvP cap of 15 at `:229-237` covers item SDI only | 97 | 98 | 99 | 100 | 101 | 102 | 99 | 104 | 123 | runaway (+5% at 225, +27% at 500) |
| Bless, Strength, Agility, Cunning `RawX * (1 + Eval/10)%`; curses `RawX * (8 + (Eval - Resist)/10)%` | `UOContent/Spells/Base/SpellHelper.cs:380-408`, applied `:303-375` | **target raw** | none on size; the player clamp applies after | +16 | +18 | +20 | +22 | +24 | +26 | | | | fine (proportional); see the note below |
| Mind Blast `min((Magery+Int)/5, 60)` | `UOContent/Spells/Fifth/MindBlast.cs:43` | eff Int | 60 | 49 | 52 | 55 | 58 | 60 | 60 | 54 | 60 | 60 | plateau at Int 180 |
| Eval Int readout | `UOContent/Skills/EvalInt.cs:55-61` | target eff Int | 10 (Int 100) | | | | | | | | | | plateau, message only |
| **Meditation start chance** `(50 + (Med - (ManaMax - Mana))*2)/100`; minimum current mana to have any chance at Med 120 | ours `customizations\Meditation.cs:83` (live; same as pinned `UOContent/Skills/Meditation.cs:76`) | pool deficit (absolute) | none | 0 | 0 | 11 | 26 | 41 | 56 | 6 | 81 | 356 | **inverted**: more Int means you meditate later. Broken in shape, no overflow. |
| Bard difficulty of a player target | `Items/Skill Items/Musical Instruments/BaseInstrument.cs:260-301` | pools | 160 | 83.3 | 84.5 | 85.6 | 86.8 | 87.9 | 89.0 | 85.2 | 90.9 | 112.0 | fine |
| Nether Cyclone, Strangle, Earthquake, Divine Fury, Close Wounds, Noble Sacrifice, Gift of Renewal, Mana Drain or Vampire, Wraith leech, Spirit Speak | `NetherCycloneSpell.cs:83-84`, `Strangle.cs:188`, `Earthquake.cs:58`, `DivineFury.cs:40`, `CloseWounds.cs:48-69`, `NobleSacrifice.cs:100-102`, `GiftOfRenewal.cs:134`, `ManaDrain.cs:41`, `ManaVampire.cs:41-58`, `WraithForm.cs:37-38`, `SpiritSpeak.cs:137-183` | pool ratios or skill | | | | | | | | | | | fine |
| Discordance stat malus, pre-AOS Mind Blast | `Discordance.cs:206-231`, `MindBlast.cs:62-107` | | | | | | | | | | | | not live |

**Note on Bless and curses against a tight clamp.** The clamp is applied after StatMods. At raw 200 with an
effective clamp of 225, Bless gives at most +25, and nothing once items reach the cap. A curse has no felt effect
while raw plus items minus the curse is still at or above the cap. OSI has the same quirk at 150. It is not a reason
to move the clamp.

### 1.4 Engine, skills, packets, pets

| formula | file:line | reads | own clamp | value or effect | verdict |
|---|---|---|---|---|---|
| Stat gain chance (pub45) | `UOContent/Skills/SkillCheck.cs:256-281`, `:30` | none; flat 5% | | does not depend on the current stat, so 199 to 200 is as fast as 50 to 51 | fine |
| Stat gain ceiling | `SkillCheck.cs:23`, `:335-341`, `:366`, `:387`, `:408` | raw | `stats.statMax` (500 live) | the clamp itself | (cap) |
| Total cap and atrophy | `SkillCheck.cs:327-333`, `:346`, `:473`; `CanLower` `:313-321` | raw total vs StatCap | StatCap (1500 ours) | atrophy lowers only stats locked Down. **Lowering StatCap never reduces existing stats.** | fine as a formula; matters for F-12's reset (Part 4) |
| **Pet stat gain** | `SkillCheck.cs:327` skips StatCap for `BaseCreature { Controlled: true }`; the gain roll at `:256-281` applies to any mobile; pet delay 5 min (`:27`, `:420-430`); locks default Up | pet raw | `stats.statMax` only | every controlled-pet stat below 500 creeps to 500 today; under F-12, to 200 | **runaway, live now** |
| Skill stat influence | `Server/Skills.cs:255-277` | raw | zeroed under AOS (`UOContent/Skills/SkillsInfo.cs:137-140`, `UOContent/Misc/AOS.cs:15-26`) | 0 | fine (dead) |
| Anatomy readout | `UOContent/Skills/Anatomy.cs:59-88` | target eff | 10 (stat 100) | message only | plateau |
| Animal Lore, Animal Taming | `AnimalLore.cs:119-134`, `AnimalTaming.cs:44-61` | creature only | | | fine |
| Character creation | pinned `Engines/Character Creation/CharacterCreation.cs:399-415`; ours `customizations\CharacterCreation.cs:379-394` | | 10 to 60 each, total 80 or 90 | unaffected | fine |
| Resurrection stat loss | `UOContent/Gumps/ResurrectGump.cs:30-58` (returns at `:32` under AOS) | | | dead | fine |
| TestCenter `set str/dex/int` | `UOContent/Special Systems/Engines/TestCenter.cs:90`, `:112`, `:134`; StatCap 250 at `:231` | raw | 10 to 125 | test command only | plateau at 125 |
| Status packet 0x11 | `Server/Network/Packets/OutgoingMobilePackets.cs:497-570` (stats as short `:523-525`, pools `:527-530`, weight and max `:534-538`, StatCap `:542`) | | short (32767) | the largest player value at any option is MaxWeight 1850 | fine |
| 0xA1-0xA3, 0x2D | `OutgoingMobilePackets.cs:166-299` | normalized `cur*100/max` as int | | at most 6.5 M, no overflow | fine |
| Party and guild map HP byte | `UOContent/Network/MapUO.cs:91` | percent | 0 to 100 | | fine |
| A table indexed by a stat, a narrow cast, a stat as divisor | grep across `Server`, `UOContent`, ours | | | none, except the shorts above and creature-only `AITimer.cs:97` | fine |
| Mount or ethereal Str checks | `UOContent/Mobiles/Animals/Mounts` | | | no stat read exists | fine |
| Creatures reading a player's pools: Death Explosion `HitsMax/5`, Meer Eternal, Meraktus and Rikktor clamp 10..75, guards, healers, AI target choice, Kirin and Unicorn | `DeathExplosion.cs:43`, `MeerEternal.cs:110`, `Meraktus.cs:241`, `Rikktor.cs:122`, `BaseGuard.cs:290`, `BaseCreature.cs:2420-2421`, `AnimatedWeapon.cs:89`, `BladeSpirits.cs:61`, `EnergyVortex.cs:69`, `MageAI.cs:389`, `:569`, `Kirin.cs:80`, `Unicorn.cs:78` | | | proportional, clamped, or target choice only | fine |
| PlagueBeast gains 75% of a dead player's HitsMax | `Mobiles/Monsters/Misc/Melee/PlagueBeast.cs:89` | | | 103 at 125, 132 at 200, 244 at e500 | creature only |

### 1.5 Ours

| formula | file:line | reads | own clamp | value | verdict |
|---|---|---|---|---|---|
| Effective clamp | `patches\PlayerMobile-individual-stat-cap.patch` (pinned `PlayerMobile.cs:594`, `:609`, `:624`); `customizations\ClusterFStatCaps.cs:10`, `:103`; live config `:112` | | 500 (150 if disabled) | the governing clamp | runaway enabler |
| Total cap writer | `ClusterFStatCaps.cs:11`, `:107` (login `:30-38`, world load `:80-101`) | | 1500 | overwrites any StatCapScroll or veteran raise at every login | must change for F-12 |
| **Carry weight**: own backpack max = `MaxWeight` = `100 + 3.5*Str` (human) instead of pinned's 550 | `customizations\ClusterFBackpack.cs:33-42`, `ClusterFWeightPatch.cs:19-50`; pinned `PlayerMobile.cs:237`, `Items/Containers/Container.cs:252-262` | eff Str | none | 537, 590, 642, 695, 747, **800**; e150 625, e225 887, e500 1850 (OSI 550) | **runaway** (ours; not in `docs\fidelity-principle.md`, grep 2026-10-02) |
| Pet Mimic stat feed | `customizations\PetMimic.cs:1238-1243`, `:1029`, `:1318-1319`; `ClusterFPetMimicSettings.cs:69-80`; `patches\AOS-pet-mimic-attribute-aggregation.patch`; live config `:63-87` | | str/dex/int 50 each (as StatMods); BonusHits 150, capped to 25 at `PlayerMobile.cs:560`; **BonusStam and BonusMana 150 each, uncapped** (`:581`, `:584`) | +50 offset per stat; +150 stamina floors every bow at OSI stats (Part 3 table) | runaway contributor |
| Imbuing stat properties | `customizations\ArtificersImbueGump.cs:182-195`, max by standing `:53-60`, `:1667-1674` | | 8 vanilla, 15 at top guild standing, per property per item, on weapon, armor, jewel or clothing; each property costs one slot, so Str, Dex and Int can share one item | up to about +240 per stat over 16 items | runaway contributor (OSI imbue max is 8 per item) |
| Set bonuses | `customizations\Items\Artifacts\Equipment\Armor\Sets\SetItem.cs:294-379`; `patches\AOS-set-attribute-aggregation.patch` | | flat (Str 12 max) | | fine |
| Fountain of Fortune | `customizations\Items\Addons\FountainOfFortune.cs:107-120` | | +10, 60 min | | fine |
| Medusa clone HP = player's eff Str | `customizations\Mobiles\Bosses\Medusa.cs:641-677`; pinned `BaseCreature.cs:579-580` | eff Str | | e225: clone 225 vs player 187 | runaway (mild, mirror by design) |
| Skill-gain acceleration also multiplies stat rolls | `customizations\ClusterFSkillGain.cs:97-139`; live `:107-109` | | | up to about 15 stat rolls per action while a skill is below cap | fine (rate only; 200 is reached quickly) |
| Crafting, achievements, reset stone, young player, character creation | `CraftItem.cs:296-318`, `ClusterFAchievements.cs`, `ClusterFResetStone.cs`, `ClusterFYoungPlayer.cs`, `CharacterCreation.cs:379-394` | | | no stat term | fine |
| Stat inspect display | `customizations\ClusterFStatInspect.cs:52-57`, `:105-114`, `:246-265` | | | shows uncapped BonusHits ("+150") while the real effect is 25, and omits set bonuses | display bug only |

**Realistic offset per stat on this shard** (sweep D section 5; the inputs are cited there):
- Imbuing: 16 items at 15 gives 240.
- Pet Mimic: 50.
- Set bonus: up to 12.
- Bless at Eval 300 and raw 200: 62. Bless and the Strength and Agility potions share one mod name, so only one
  counts.
- Fountain of Fortune: 10. Rose of Trinsic: 5 (Str only).
- **Total: about +375 per stat. Without imbuing, about +130. OSI's design is +25.**
- Mid guild standing (11 per item) gives about +300.

## Part 2: what breaks, ranked

Ranked like P20: what a player at 200 can do that one at 125 cannot, and how bad that is in play. The "where it
bites" column says whether raw 200 alone is enough, or whether gear is needed above the clamp.

| rank | formula | verdict | where it bites | what a 200 player can do, and how bad |
|---|---|---|---|---|
| 1 | Self bandage, `Bandage.cs:493` | runaway to instant | **raw 200 alone** (1.0 s); instant from effective Dex 220 | Heals 43 to 72 HP (Healing and Anatomy 120, `:387-388`) every 1.0 s against OSI's 3.5 s. That is about 57 HP/s against OSI's 16, making a melee character close to unkillable. At effective 225 or above, every bandage is instant. **Severe.** |
| 2 | Pet stat gain, `SkillCheck.cs:327` | runaway | **live today, at 500** | Every controlled pet with a stat below 500 climbs to 500 at one gain per 5 minutes per stat. Str and Dex feed creature weapon damage and swing speed. Unseeded pets' HP grows with Str (`BaseCreature.cs:579-580`). Under F-12 the climb stops at 200. **Severe and silent**; it rides along with the player change. |
| 3 | Carry weight, ours `ClusterFBackpack.cs:33-42` | runaway | raw 200: 800 stones; e225: 887; e500: 1850 (OSI 550) | Gatherer and loot-run yield per trip +45% at raw 200, and 3.4 times OSI at 500. Economic, not combat. **High**, and it is a Chase decision because the deviation is ours and deliberate (comment at `:9-19`). |
| 4 | ML swing speed from stamina, `BaseWeapon.cs:1428` | runaway to the 1.25 s floor | raw 200: slow weapons 0.25 to 0.5 s faster; **a Pet Mimic's +150 stamina floors a bow at OSI stats today** | Bow at SSI 60: 1.75 s at OSI to 1.50 s at 200 (+17% DPS). With the mimic, 1.25 s at every column. Fast weapons are already floored at 125. **Moderate** from stats. **High** from the mimic, but that is a separate, live, ours issue. |
| 5 | Meditation start, ours `Meditation.cs:83` | inverted | raw 200: needs 56 mana to start; e225: 81; e500: 356 | Higher Int makes active meditation worse. At 500 it is useless below 71% full. **Moderate, and backwards**, which players notice. |
| 6 | HitsMax, `PlayerMobile.cs:576` | runaway (slow) | raw 200: 175; e225: 187; e500: 325 (OSI 150) | Survives one more nuke in a three-spell dump at 225. At 500 it is more than double. **Moderate.** This is the reward stats are meant to give; keep it and bound it with the clamp. |
| 7 | Spell damage, `Spell.cs:226` | runaway | e225: Flame Strike 104 vs 99; e500: 123 | +5% at 225 is noise. +27% at 500 bypasses the PvP SDI 15 cap. **Low at 225, high at 500.** |
| 8 | Thrown range, `BaseThrown.cs:24` | runaway | raw 200: Soul Glaive 13 vs 11; e225: 14; e500: 24 | Gargoyle throwers outrange others by 2 to 3 tiles at 225. Past the 18-tile update range at 500. **Low to moderate at 225.** |
| 9 | Str melee damage, `BaseWeapon.cs:2556` | runaway | e225: multiplier +5.7% over OSI; e500: +26.5% | **Low at 225.** |
| 10 | Mana pool and StamMax, `PlayerMobile.cs:581-585` | runaway (pools) | linear | Bigger pools; mana regen does not keep pace (+0.2/s), which acts as a brake. **Low at 225.** |
| 11 | Hit-spell Int bonus, `BaseWeapon.cs:2265` | runaway (mild) | e225: +6% | **Low.** |
| 12 | Throwing dagger, `ThrowingDagger.cs:57` | broken | target Dex 157 and up is immune | GM-spawn only. **Negligible.** |

**Plateaus, all safe:**
- Force of Nature (Str 150).
- Bandaging others (0.70 s at Dex 204).
- Mind Blast (60 at Int 180 with Magery 120).
- Poison (per-level max).
- Meraktus and Rikktor (75).
- Anatomy and Eval Int messages.
- TestCenter set (125).
- Bard difficulty (160).

**Nothing is broken in storage or packets.** All values fit their fields at every option (1.4).

## Part 3: the effective cap

The comparison is at max level 200 (raw 200). Script: `cc-P25-scratch\p3_clamp_table.py`. The "OSI 150" column is
pinned's own clamp; "raw only 200" is no offset at all.

| formula | OSI 150 | raw only 200 | eff 225 | eff 250 | eff 500 |
|---|---|---|---|---|---|
| HitsMax | 150 | 175 | 187 | 200 | 325 |
| Self-bandage delay | 3.50 s | 1.00 s | 8 ms | 8 ms | 8 ms |
| Bow 4.25 at SSI 60, Stam = Dex | 1.75 s | 1.50 s | 1.50 s | 1.25 s | 1.25 s |
| same with a mimic's +150 Stam | 1.25 s | 1.25 s | 1.25 s | 1.25 s | 1.25 s |
| Heavy crossbow 5.0 at SSI 0 | 3.75 s | 3.50 s | 3.25 s | 3.00 s | 1.25 s |
| Melee damage multiplier | 3.962 | 4.112 | 4.188 | 4.263 | 5.012 |
| Flame Strike PvP avg | 99 | 102 | 104 | 106 | 123 |
| Soul Glaive range (design 11) | 11 | 13 | 14 | 15 | 24 |
| Carry, human | 625 | 800 | 887 | 975 | 1850 |
| Mana pool, no items | 150 | 200 | 225 | 250 | 500 |
| Minimum mana to start meditating (Med 120) | 6 | 56 | 81 | 106 | 356 |
| Mind Blast (Magery 120) | 54 | 60 | 60 | 60 | 60 |

- **225** keeps every combat number within about 6% of the raw-200 value. Only the bandage, already broken at
  raw 200, gets worse.
- **250** adds a full extra floor tick on slow weapons and 2 more tiles of thrown range.
- **500** is a different game: 325 HP, a +27% nuke, every weapon at the floor, 24-tile throws and 1850 stones.

**Recommendation: effective 225, set per character as "personal per-stat ceiling + 25".** It is OSI's own headroom
at every loop, so loop 0 is exactly OSI (125 raw, 150 effective). It is also the only option that bounds a loop-0
character: with a single global clamp, a fresh character's +240 imbue offset reaches 225, or 500 today, at any loop.

**What this costs.** The current patch reads one static, `ClusterFStatCaps.IndividualStatCap` (`ClusterFStatCaps.cs:103`).
Per-character means the three hunks call something like `ClusterFStatCaps.EffectiveCap(this)` instead. That is the
same three lines and the same hunk, so it folds into `patches\PlayerMobile-individual-stat-cap.patch` and adds no new
patch. The arch verdict already asked for any change on this hunk to go into that patch.

Chase decides.

## Part 4: the table, confirmed or amended

**The approved per-stat column, 125 to 200, holds. No amendment.** "Base total + 50 veteran = 3 x per-stat" checks
on all six rows (325+50 = 375 = 3x125, through 550+50 = 600 = 3x200).

The one runaway that makes raw 200 unsafe on its own is the self-bandage (rank 1). It is cheaper to fix in that
formula than to lower the table.

**Self bandage: the options, argued (AGENTS.md: argue every pinned patch first).**
- **(a) Lower the top.** Bandage reaches OSI's 3.5 s only if effective Dex stays at 150, so the top would drop
  from 200 to 125 raw. That throws away the whole stat half of F-12. Rejected.
- **(b) A per-stat effective clamp of 150 for Dex in the existing patch.** No new patch, but raw Dex above 150
  becomes worthless everywhere: stamina, swing speed, bandaging others. Rejected.
- **(c) Leave it.** At 1.0 s, about 57 HP/s of self-heal; instant at 220 and above. Rejected: this is the worst
  thing on the list.
- **(d) Replace the whole of `Bandage.cs` from customizations**, the way `Meditation.cs` and `RegenRates.cs` are
  replaced. It is not a patch, but it freezes about 540 lines of pinned against upstream to change one. Worse than (e).
- **(e) A one-line pinned patch at `UOContent/Items/Skill Items/Misc/Bandage.cs:484` or `:493`.** For example, use
  `Math.Min(dex, 150)` in the self-heal line only, which makes it OSI-identical at every stat. Alternatively, floor
  `seconds` at a number Chase picks if Dex should keep paying. There is no hook: `BandageContext.BeginHeal` is
  static and is called straight from the target. **Recommended.** It is one new patch, against about thirty for
  F-12. It does not fold into an existing patch because it is a different file.

**Pet ceiling: no patch needed.**
- Our `ClusterFSkillGain` replaces all four global skill-check handlers (`customizations\ClusterFSkillGain.cs:37-46`),
  so it sees every pet skill check before pinned's `Gain` runs.
- Before the attempt, for `BaseCreature { Controlled: true }`, set to Locked any stat lock whose raw value is at or
  above a pet ceiling. 125 is OSI's, because pets shared the 125 statMax in pinned's defaults.
- Pet locks are never otherwise touched: the 0x1A handler acts only on `state.Mobile`, the player. Atrophy needs
  Down, so Locked is permanent and safe.
- The alternative is a patch in `SkillCheck.cs:327-341` adding a pet max. That is a new pinned patch with no
  advantage. Rejected.
- Not verified: that no pinned path calls `SkillCheck.Gain` directly on a pet and bypasses the handlers.
- **This is live now at 500 and should not wait for F-12.**

**Meditation: ours, no patch.** In `customizations\Meditation.cs:83`, make the deficit relative to the pool,
e.g. `(ManaMax - Mana) * 125 / ManaMax`. The file is already our full replacement (`apply-patches.sh:243-244`).
This is a deliberate deviation, recorded as one.

**Carry weight: ours, no patch. Chase's call.** Cap `ClusterFBackpack.DefaultMaxWeight` (`:33-42`) at a number,
for example the value at Str 150 (625). Alternatively, keep it and register it in `docs\fidelity-principle.md`;
it is a live deviation that is not registered today.

**Leave unchanged at 225:** HitsMax, spell damage, Str melee damage, the hit-spell Int bonus, pools and regen.
These are the stat reward. **If Chase picks 250 or keeps 500, thrown range and swing speed need soft caps** at
`BaseThrown.cs:24` and `BaseWeapon.cs:1428`. Both are new pinned patches, and Chase should weigh them against
simply choosing 225.

**Not F-12 work but adjacent, for the overseer:**
- The Pet Mimic's uncapped +150 stamina floors bows today (`ClusterFPetMimicSettings.cs:78`, config only).
- Imbuing's stat properties go to 15 per item against OSI's 8 (`ArtificersImbueGump.cs:182-195`).
- Neither needs a patch.

**Design facts F-12 must absorb.**
1. **A reset that only lowers StatCap does not lower stats.**
   - `CanRaise` blocks gain at `RawStatTotal >= StatCap` (`SkillCheck.cs:327-333`).
   - Forced atrophy (`:346`) only lowers a stat locked Down (`CanLower`, `:313-321`).
   - So "total stat cap rises with current level" leaves a freshly reset character at their full old stats.
   - The F-12 notes say this cap "is what makes a reset feel like a reset". For that to be true, the reset must write
     raw stats down, for example to the loop's starting values.
   - That is a design decision for Chase, not a build detail.
2. **`ClusterFStatCaps.Apply` writes 1500 on every login and world load** (`:105-108`). The per-character total
   (325 to 550, plus 50 veteran) has to be computed there, or every StatCapScroll and veteran raise is overwritten.
3. **Cutting `stats.statMax` from 500 to 200 does not lower anyone already above 200.** `CanRaise` only stops
   gain. The F-12 notes say the old live world is retired, so this may be moot. I did not count characters above
   125 or 200 (saves not read).
4. **On the arch verdict's stat lock** (not re-argued, two additions):
   - The same `ClusterFSkillGain` wrapper is a second, server-side enforcement point. It can lock a player's stat at
     their personal ceiling immediately before every gain roll, so a client that flips the arrow back to Up gains
     nothing even if the 0x1A handler were missed.
   - The 0x1A handler is still wanted, so the UI does not lie.
   - The wrapper only sees checks that go through the four handlers (see Not verified).

## Part 5: the cheap list for the F-12 builder

**Places to touch (stats only):**

| # | where | what |
|---|---|---|
| 1 | config `stats.statMax` (live `modernuo.json:160`, test `:165`); read at pinned `SkillCheck.cs:23` | 500 to 200, the absolute raw ceiling |
| 2 | ours `ClusterFStatCaps.cs:10`, `:103` and `patches\PlayerMobile-individual-stat-cap.patch` (pinned `PlayerMobile.cs:594`, `:609`, `:624`) | the effective clamp becomes per character: personal ceiling + 25 (Part 3), in the same hunk |
| 3 | ours `ClusterFStatCaps.cs:11`, `:105-108`; config `totalCap` (live `:113`, test `:118`) | the total from the F-12 table by level, plus veteran; stop writing 1500 |
| 4 | the 0x1A re-registration (arch verdict) and, optionally, the `ClusterFSkillGain.cs:97-139` pre-gain lock | the personal per-stat ceiling |
| 5 | ours `ClusterFSkillGain.cs` (handlers `:37-46`, `RunBoostedCheck` `:97`) | the pet ceiling of 125 by lock, **live now** |
| 6 | **new pinned patch**, `UOContent/Items/Skill Items/Misc/Bandage.cs:484` or `:493` | the self-bandage floor or Dex clamp |
| 7 | ours `customizations\Meditation.cs:83` | relative mana deficit |
| 8 | ours `customizations\ClusterFBackpack.cs:33-42` | a carry cap, or register the deviation (Chase) |
| 9 | the reset path (F-12, not yet written) | write raw stats down on reset, if Chase wants a reset to cost stats |
| 10 | ours `TestCenter\TestCenterKit.cs:160-175`; pinned `TestCenter.cs:90`, `:112`, `:134` (10 to 125) and `:231` (StatCap 250) | only if test characters must be set above 125 by the TC command; otherwise leave it |
| 11 | pinned `StatCapScroll.cs:99`, `:119-123` (from the F-12 notes) | retune or drop. Ours never references it (grep, 0 hits). |

**Tests.** One fact per finding. Each is stated so that it fails today, which lets you watch it red.

| finding | test |
|---|---|
| Effective clamp | A player with personal ceiling 140, raw Str 140 and +100 Str from StatMods reads `Str == 165`. **Red today: 240.** |
| Effective clamp, loop 0 | A player at ceiling 125 with +240 Str offset reads `Str == 150`. **Red today: 365.** |
| Self bandage | A player with effective Dex 200 bandaging themselves gets a `BandageContext` delay of at least 3.5 s (or the chosen floor). **Red today: 1.0 s.** At Dex 225 the delay is above 8 ms. **Red today.** |
| Pet ceiling | A controlled pet with RawDex 124 and `statMax` 200, after 1000 forced `GainStat` calls with the pet delay reset, has RawDex at most 125. **Red today: it climbs to 200 (or 500).** |
| Meditation | ManaMax 225, Mana 0, Meditation 120: the computed start chance is above 0. **Red today: negative.** |
| Total cap | After `ClusterFStatCaps.Apply`, a character at max level 100 without the veteran reward has `StatCap == 370`. **Red today: 1500.** |
| Reset (characterization; green today) | Setting StatCap to 325 on a character with raw total 550 leaves raw total 550 after N gain rolls with all locks Up. Pins the fact the reset design must not rely on. |
| Talisman leak (pinned defect; green if I am wrong) | Equip and unequip a talisman with `BonusStr 10` three times. Raw Str is unchanged and `GetStatOffset(Str) == 0` at the end. **Expected red** by reading `AOS.cs:598` vs `:620`. |
| Carry (if capped) | A human with effective Str 225 has a backpack `MaxWeight` at or below the chosen cap. **Red today: 887.** |

**Plateau and characterization facts.** These are green today; they pin the plateaus so nobody "fixes" them by
accident:
- Mind Blast damage at Int 200 with Magery 120 is 60.
- Force of Nature's bonus at Str 200 equals its value at 150.
- HitsMax at effective 225 with BonusHits 30 is 187, because BonusHits is capped at 25.
- Status packet 0x11 round-trips Str 225 and MaxWeight 887.

**Already covered by P20's skill list (not repeated here):**
- Packet fields for skills.
- The `StatCapScroll` and `PowerScroll` plumbing (P20 section 1.5 and section 4).
- Skill-driven parts of the same formulas: Eval and Inscription in spell damage, Healing and Anatomy in bandage
  amount, Meditation and Focus in regen.
- At a skill cap of 200, Eval moves spell damage and Bless size more than Int does (`Spell.cs:250-252`,
  `SpellHelper.cs:383-385`). That belongs to P20's rank 7 soft-curve work.

## 2.6 The talisman and quiver stat-bonus leak (pinned defect, found in passing)

This is filed here because it decides how much the effective clamp has to carry.
- `AosAttributes.AddStatBonuses` names its StatMods `$"{GetHashCode()}Str"` (`UOContent/Misc/AOS.cs:598-611`).
- `RemoveStatBonuses` removes `$"{Owner.Serial}Str"` (`:618-625`). `Serial.ToString()` is hex `0x...`
  (`Server/Serial.cs:122-129`).
- `BaseAttributes` has no `GetHashCode` override in source (`AOS.cs:1347-1380`). The serialization generator
  package (`ModernUO.Serialization.Generator` 2.14.3) contains no emitted `GetHashCode` text: 0 UTF-16 literals,
  and its single ASCII hit is a metadata reference. So the add name is the object's default hash in decimal, and
  the remove name never matches.
- `AddStatMod` appends without replacing a same-name mod (`Server/Mobiles/Mobile.cs:8388-8401`).
- StatMods are not saved (`Mobile.cs:6419`).
- **By reading:** each unequip and re-equip of a talisman (`BaseTalisman.cs:356`, `:379`) or quiver
  (`BaseQuiver.cs:206`, `:214`) with Bonus Str, Dex or Int stacks another full copy until the next restart. Only
  the effective clamp bounds it, and that is 500 today.
- Clothing and spellbooks use their own paths and were not traced.
- **Not runtime-verified.** The test above settles it.

## Not verified

- **The talisman and quiver leak (2.6)** is from reading code, not from running it.
- **Whether a pet's stat gain always passes through the four `Mobile.SkillCheck*Handler` delegates.** A pinned
  path calling `SkillCheck.Gain` directly on a pet would bypass the wrapper fix. Not traced.
- **How many existing characters hold raw stats above 125 or 200**, and how many pets above 125. Saves not read.
- **Whether the bind-mounted `Configuration\modernuo.json` is exactly what the running containers load.** Mounts are
  read from `docker\uo\docker-compose.yml:18` and `docker-compose.test.yml:39`, but nothing was checked inside a
  container.
- **The offset estimate**: the count of 16 simultaneously equippable imbuable items (19 theoretical), and whether
  top guild standing (15 per item) is reachable in practice.
- **Weapon speed values** (2.0 to 5.0, Bow and Halberd at 4.25, Heavy Crossbow at 5.0) come from sweep A's reading
  of `MlSpeed` overrides. I did not recount them.
- **Pet HP growth** applies only to species with an unseeded HitsMax (`BaseCreature.cs:579-580`). I did not count
  how many tamables lack `SetHits`.
- **`testCenter.enable` on the test shard** was not checked.
- **OSI behavior** was not consulted. Every claim here is pinned behavior, cited.
