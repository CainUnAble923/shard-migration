# Sweep D (ours): where player stats become numbers in Shattered Legacy's own code

Date: 2026-10-02. Read-only sweep. Ours = paths relative to D:\ShatteredLegacy\server.
Pinned = paths relative to D:\UO\ModernUO-pinned\Projects (7c9215d97).
Scratch calc: notes/cc-P25-scratch/sweepD_calc.py (all numbers below come from it or are hand arithmetic shown inline).

## 0. Corrections to the brief (verified)

1. LIVE config also has `stats.statMax = 500`, not only test. uo/modernuo/Configuration/modernuo.json:160
   (test: Configuration-test/modernuo.json:165). Pinned reads it at UOContent/Skills/SkillCheck.cs:23 and
   raw gain stops at it (SkillCheck.cs:337-339, 366, 387, 408). With StatCap 1500 (ClusterFStatCaps.cs:107),
   live players can ALREADY gain raw 500/500/500. F-12 "raise 125 -> 200" is, on this config, a LOWERING
   of the raw ceiling from 500 to 200. How many live characters hold raw > 125 or > 200 is UNVERIFIED
   (saves not read).
2. The ours-stat-files.txt list (37 files) is not the same set as a grep for the brief's identifiers.
   My grep (`\b(Str|Dex|Int|RawStr|...|StatType)\b` over customizations + patches) hits 178 files
   (notes/cc-P25-scratch/my-grep.txt). The extra ~140 are almost all item definitions that set
   `Attributes.Bonus*` / `StrRequirement`; they are covered in aggregate in section 3. Five files in the
   37-list do not match the brief's identifiers at all (ArtificerWorkOrderSystem.cs, CraftItem.cs,
   VirtuousEpiphany.cs, VillainousEpiphany.cs, KepetchAmbusher.cs, TrapdoorSpider.cs match only on
   Hits/Mana/Stam/Weight words). All 37 were read for this sweep.
3. Brief said PetMimic BonusHits 150 might bypass the ML 25 cap. It does NOT (section 2.F).

## 1. How our replacements reach the build

- docker/uo/apply-patches.sh:193-201 copies top-level customizations/*.cs into Projects/UOContent/Misc/
  EXCEPT CharacterCreation, CraftContext, CraftItem, HammerOfHephaestus, Meditation, RegenRates, ResourceInfo.
- Those are routed as full-file replacements: CharacterCreation.cs -> Engines/Character Creation/ (:235-236),
  CraftItem.cs -> Engines/Craft/Core/ (:237-238), Meditation.cs -> Skills/Meditation.cs (:243-244),
  RegenRates.cs -> Misc/RegenRates.cs (:250).
- Subdirectories mirror into Projects/UOContent/<same path> (:212).
- Stat-relevant .patch files applied: PlayerMobile-individual-stat-cap.patch (:257),
  AOS-pet-mimic-attribute-aggregation.patch (:260), AOS-set-attribute-aggregation.patch (:270).

## 2. Formulas and stat touch points (each with verdict)

Value grid: raw 125/140/155/170/185/200, effective 150/225/250/500.
Effective clamp today = 500 (patch). OSI = 150.

### A. Effective-stat clamp (THE clamp). patches/PlayerMobile-individual-stat-cap.patch:7-8, 16-17, 25-26
Code: `return Math.Min(base.Str, ClusterFStatCaps.IndividualStatCap);` (same for Int, Dex), replacing pinned
`Math.Min(base.X, 150)` at pinned UOContent/Mobiles/PlayerMobile.cs:594, 609, 624. Only when Core.ML and
AccessLevel == Player. IndividualStatCap = 500 from config, or 150 when clusterf.statCaps.enabled is false
(customizations/ClusterFStatCaps.cs:103; default const :10; config read :20-23; live value 500 at
Configuration/modernuo.json:112).
Computes: effective Str/Dex/Int = min(raw + all StatMod offsets, 500). base.Str itself is
Math.Clamp(raw+offset, 1, 65000) (pinned Server/Mobiles/Mobile.cs:1868).
Stat: effective. Own clamp: 500.
Values: passes 125..200 raw and 150/225/250 effective unchanged; 500 is the ceiling.
Verdict: runaway (it is the reason everything downstream can reach 500; at raw 200 plus the offsets in
section 3, effective reaches the 500 clamp for a fully geared player, see section 5).

### B. Total stat cap writer. customizations/ClusterFStatCaps.cs:107
Code: `player.StatCap = Math.Max(0, _totalStatCap);` on login (:30-38, CallPriority 100), world load
(:26, :80-101) and [ClusterFStatCaps command (:43-78). _totalStatCap default 1500 (:11), config :24
(live 1500, Configuration/modernuo.json:113).
Effect: overwrites any StatCap a StatCapScroll or vet reward set; pinned CanRaise blocks gain when
RawStatTotal >= StatCap (pinned UOContent/Skills/SkillCheck.cs:326-331).
Verdict: plateau (a cap; at F-12 totals 325..550 this must be changed or it keeps 1500).

### C. HP pool, reached through our clamp. pinned UOContent/Mobiles/PlayerMobile.cs:555-576 (not our file,
but its range is set by A)
`strBase = Str; strOffs = min(BonusHits, 25 under ML); return strBase/2 + 50 + strOffs` (:558, :560, :576).
Values HitsMax (with +25): raw125 137, 140 145, 155 152, 170 160, 185 167, 200 175; eff150 150, 225 187,
250 200, 500 325.
Verdict: fine (slope 1/2, BonusHits capped at 25; bigger only because A allows bigger Str).

### D. Mana regen. customizations/RegenRates.cs:148-150, 167, 187, 199, 202
Code: `medPoints = from.Int + Meditation*3; medPoints *= Med < 100 ? 0.025 : 0.0275;`
`total = focus*0.05 + medPoints + (meditating ? min(medPoints,13) : 0) + min(RegenMana,18); floor; rate = 1/(0.1*(2+total))`.
Stat: effective Int (via A). Clamp: none on Int term (13 cap only on the meditating doubling; 18 on MR).
Int contribution to points at Med>=100: 0.0275*Int = 3.44 (125), 3.85 (140), 4.26 (155), 4.67 (170),
5.09 (185), 5.5 (200); 4.12 (150), 6.19 (225), 6.88 (250), 13.75 (500).
Mana/s, Med120 Focus120 MR0, not meditating / meditating: 125 2.1/3.4; 140 2.1/3.4; 155 2.2/3.5; 170 2.2/3.5;
185 2.2/3.5; 200 2.3/3.6; eff150 2.2/3.5; 225 2.4/3.7; 250 2.4/3.7; 500 3.1/4.4.
Med300 Focus300 (our skill cap 300, Configuration/modernuo.json:105): 125 4.5/5.8 ... 200 4.7/6.0, 500 5.5/6.8.
Verdict: fine (Int is a minor linear term; skill dominates; at raw 200 +0.2 mana/s vs 125).
Our deviation vs pinned: only :156-165 (armored meditation >200 skill); no stat term changed.
HP regen (:44-86) and stam regen (:88-129) have NO stat term: fine.

### E. Active Meditation success. customizations/Meditation.cs:83 (same formula as pinned)
`chance = (50 + (skill - (ManaMax - Mana)) * 2) / 100`.
Stat: ManaMax pool (Int + BonusMana + elf 20; pinned PlayerMobile.cs:584).
Only possible when the mana deficit < skill + 25 (an absolute window). As a share of the pool with mimic
+150 mana: Med120: Int125 53%, 140 50%, 155 48%, 170 45%, 185 43%, 200 41%; eff150 48%, 225 39%, 250 36%,
500 22%. Med300: 100% up to Int 170, 93% at 200, 87% at 225, 50% at 500.
Verdict: plateau (fixed absolute window; larger pools can only start meditating near the top).

### F. PetMimic stat feed. customizations/PetMimic.cs:1238-1243, 862-870, 1025-1033, 1316-1323;
patches/AOS-pet-mimic-attribute-aggregation.patch:7-15; settings customizations/ClusterFPetMimicSettings.cs:69-80
- Feeding an item adds its BonusStr/Dex/Int/Hits/Stam/Mana to accumulators, each Math.Min'd to the
  setting (PetMimic.cs:1238-1243). Live: str/dex/int 50, bonusHits/Stam/Mana 150
  (Configuration/modernuo.json:63-65, 68, 73, 87).
- RebuildAosAttributes copies accumulators into the mimic's AosAttributes (:862-870).
- Str/Dex/Int reach the player as StatMods: OnAdded calls `_aosAttributes?.AddStatBonuses(m)` (:1029),
  re-applied after feeding (:1318-1319). Pinned AddStatBonuses = UOContent/Misc/AOS.cs:589-611.
  => up to +50 Str, +50 Dex, +50 Int of offset, then clamped by A.
- Hits/Stam/Mana reach the player through AosAttributes.GetValue, which the patch extends to PetMimic.
  HitsMax: GetValue(BonusHits) is then capped to 25 at pinned PlayerMobile.cs:560 for players under ML.
  So BonusHits 150 does NOT bypass the cap; mimic and all items share the one 25.
  StamMax (pinned PlayerMobile.cs:581) and ManaMax (:584) have NO cap: mimic gives a full +150 stam and
  +150 mana on top of Dex/Int.
- The mimic occupies the Talisman layer or the absorbed form's layer (PetMimic.cs:461, 953-956), i.e. it
  costs one equipment slot.
Verdict: runaway for Stam/Mana pools (+150 each uncapped; OSI design has no stamina/mana increase cap
either, but item values are single digits). Str/Dex/Int +50 each: runaway contributor to offset (OSI
total design offset is +25).

### G. Set bonuses. customizations/Items/Artifacts/Equipment/Armor/Sets/SetItem.cs:296-302, 357-379;
patches/AOS-set-attribute-aggregation.patch:9-21
Str/Dex/Int set bonus applied once (only the LastEquipped piece, :294-302) as StatMods (:365, :370, :375).
Hits/Stam/Mana set bonus via GetValue (patch). Largest set values in our tree: Str 12 (Grizzle), Dex 12
(Assassin), Int 10 (Mage, "Mage" folder = Leafweave), Mana 15 (Aloron, Darden), Hits 6 (Knights).
Verdict: fine (small, flat).

### H. Fountain of Fortune. customizations/Items/Addons/FountainOfFortune.cs:107-120
+10 Str OR Dex OR Int (distinct mod names FoF_Str/FoF_Dex/FoF_Int), 60 min, one per roll.
Verdict: fine (flat +10; repeated uses can hold all three).

### I. Backpack carry limit. customizations/ClusterFBackpack.cs:33-42 (+ migration ClusterFWeightPatch.cs:23-48)
`DefaultMaxWeight => m.MaxWeight` for the player's own pack, replacing pinned Backpack's 550 under ML
(pinned UOContent/Items/Containers/Container.cs:252-261). m.MaxWeight = (ML human 100 else 40) + 3.5*Str
(pinned PlayerMobile.cs:237). Stat: effective Str. Clamp: only A.
Values human/other: raw125 537/477, 140 590/530, 155 642/582, 170 695/635, 185 747/687, 200 800/740;
eff150 625/565, 225 887/827, 250 975/915, 500 1850/1790.
Verdict: runaway (linear, no cap of its own; at raw 200 + realistic offsets the pack holds 887-1850 stones
vs OSI 550). The comment block (:9-19) documents it as intended; whether it is in docs/fidelity-principle.md
is UNVERIFIED.

### J. Medusa clone. customizations/Mobiles/Bosses/Medusa.cs:641-677 (callers :308, :742)
Copies the PLAYER's effective Str/Dex/Int (:651-653), sets Hits = player HitsMax (:655), copies skill
Base and Cap (:672-676). BaseCreature HitsMax = Str when HitsMaxSeed <= 0 (pinned
UOContent/Mobiles/BaseCreature.cs:579-580), so clone max HP = player's effective Str.
Clone HP vs player HitsMax: eff150 150 vs 150; 225 225 vs 187; 250 250 vs 200; 500 500 vs 325.
Verdict: runaway (mild, mirror-by-design; above 150 the clone out-HPs the player it copies).

### K. Imbuing stat properties. customizations/ArtificersImbueGump.cs:182-195, 53-60, 1667-1682
Bonus Strength / Dexterity / Intelligence: MaxVanilla 8, MaxGuild 15, on Weapon|Armor|Jewel|Clothing.
Max by standing: raw = 8 + 7*(pct-100)/100 with pct 100/120/150/175/200 (:1667-1674) -> 8, 9, 11, 13, 15.
Property slots per item 5/6/7/8 (:1676-1682); a stat property costs one slot (:51).
No Hit Point / Stamina / Mana Increase is imbuable (grep of the file: no BonusHits/Stam/Mana).
No artifact exclusion: any Weapon/Armor/Jewel/Clothing in the pack (:1610-1622).
Verdict: runaway contributor (15 per stat per item, no per-character total; OSI imbuing max is 8 per item).

### L. Artificer work orders. customizations/ArtificerWorkOrderSystem.cs:269-302
Requirement checks only (Bonus Strength 6 etc., checked at :183-193). Verdict: fine.

### M. Character creation. customizations/CharacterCreation.cs:379-394 (unchanged from pinned for stats)
Each stat 10..60, sum 80 (or 90 new client) (:381, :387); staff get 100/100/100 (:254-256).
Verdict: fine (F-12 does not need to touch it).

### N. Stat-gain acceleration (indirect). customizations/ClusterFSkillGain.cs:97-139
Up to 3 attempts (:106) and up to 4 extra SkillCheck.Gain calls per real gain (:129-138) while the skill is
below cap (:141-147). Pinned Gain rolls a pub45 stat gain on every call (SkillCheck.cs:256-281, 5% per call).
So stat gain runs up to ~15 rolls per action instead of 1. Live: 3 attempts, x5
(Configuration/modernuo.json:107-109). No stat value formula. Verdict: fine (rate only; means a 200
ceiling is reached quickly, and stops once skills cap).

### O. Dev/test writers.
- customizations/ClusterFDevTools.cs:120-128: reset sets RawStr/Dex/Int = 10 and refills pools. Fine.
- customizations/TestCenter/TestCenterKit.cs:160-175: keeps the higher StatCap across pinned's fill, which
  sets 250 (pinned UOContent/Special Systems/Engines/TestCenter.cs:231). Fine, but a StatCap writer.
- Pinned TestCenter "set str/dex/int" accepts 10..125 only (pinned TestCenter.cs:90, 112, 134); not ours.

### P. Display only.
- customizations/ClusterFStatInspect.cs:52-57, 105-114, 246-265: sums item Attributes incl. PetMimic but
  NOT set bonuses, and shows uncapped BonusHits ("+150 bonus") while the real effect is 25. Display bug, fine.
- customizations/PetMimicFeedGump.cs:127-132, PetMimicStatusGump.cs:28, 143-145: display. Fine.

### Q. Inert or non-player.
- Epiphany (EpiphanyHelper.cs:58 Hooked=false; :109 OnHit has no caller): karma-scaled (:97, :104), clamps to
  HitsMax (:161-168). No stat term. Fine (inert).
- BeastialSetHelper.cs:39-42: ratio Hits vs HitsMax/2, no caller (D-14 comment :38). Fine (inert).
- JadeWarAxe.cs:62-72 and GargishBattleAxe.cs Concussion -(RawInt/2): guarded by `!Core.AOS`, dead on EJ. Fine.
- EvilOrcHelm.cs:29-38: compares RawInt vs RawDex to pick which -10 applies; +10 Str (:22). Fine.
- DespiseCreature.cs:395-425: creature's own stats. Despise{Good,Evil}Creatures.cs:258/263: heal-threshold
  ratio. DespiseRevamped/Region.cs:166: karma uses the dead creature's HitsMax. Fine.
- Shame Creatures.cs:768-769: flat 30-40 mana sap. Fine (plateau-ish: smaller share of bigger pools).
- BloodWorm.cs:72,100; Niporailem.cs:123; KepetchAmbusher.cs:144; TrapdoorSpider.cs:94; BasePeerless.cs:76,174;
  BaseSABosses.cs:196; ClockworkScorpion.cs:5 (comment); SlasherOfVeils.cs:124 (commented out): own stats only.
  No creature in our code deals percent-of-player-HitsMax damage. Fine.
- StrRequirement values in our items max 80 (VirtuososArmbands.cs:15); GargishBattleAxe AosStrengthReq 35.
  Fine.
- CraftItem.cs:296-318: fixed Hits/Mana/Stam costs; diff vs pinned (169 changed lines) has no stat term.
  No stat in craft success/quality/exceptional. Fine.
- ClusterFAchievements.cs, ClusterFResetStone.cs, ClusterFYoungPlayer.cs, PetMimicPurgePotion.cs: 0 hits for
  RawStr/RawDex/RawInt/RawStatTotal/.Str/.Dex/.Int/StatCap/HitsMax/ManaMax/StamMax. No stat achievements,
  no stat writes.

## 3. Patches: which touch stats (33 files in patches/, counted)
Touch stats: PlayerMobile-individual-stat-cap.patch (the clamp), AOS-pet-mimic-attribute-aggregation.patch
(BonusHits/Stam/Mana via GetValue), AOS-set-attribute-aggregation.patch (same for set attrs).
PlayerMobile-fountain-luck-bonus.patch touches Luck only. The other 29 (incl. whole-file Mining.cs,
BaseGuildmaster.cs, JacobsPickaxe.cs, LargeSmithBOD.cs, BulkMaterialType.cs) have no stat identifiers in
added lines (counted per file with grep on '^+').

## 4. Item stat values set in our own item code (aggregate, counted)
`Attributes.BonusX = N` across customizations (excluding SetAttributes): Str max 10 (7 items at 10, e.g.
PillarOfStrength.cs:12, CowlOfTheMaceAndShield.cs:15, EvilOrcHelm.cs:22, CollectionsBritLibraryGlasses.cs:14),
Dex max 5, Int max 10 (Tangle1.cs:20, DespiseArtifacts.cs:15, glasses), Hits max 15 (glasses :62, :85),
Stam max 12 (BritchesOfWarding.cs:27), Mana max 15 (TheScholarsHalo.cs:12, MagesHoodOfScholarlyInsight.cs:15).
Imbuing (2.K) can overwrite any of these to 15 Str/Dex/Int.

## 5. Max OFFSET per stat (fully geared, top guild standing)
Equippable item layers that take Weapon/Armor/Jewel/Clothing: OneHanded, TwoHanded, Shoes, Pants, Shirt,
Helm, Gloves, Ring, Neck, Waist, InnerTorso, Bracelet, MiddleTorso, Earrings, Arms, Cloak, OuterTorso,
OuterLegs, InnerLegs = 19 (pinned Server/Items/Layer.cs:36-151; Talisman excluded, not imbuable, used by
mimic). Exact co-equip conflicts UNVERIFIED; I use 16 as "realistic full kit".

Str: imbue 16 x 15 = 240 (2.K) + mimic 50 (2.F) + set 12 (2.G) + magic buff max(Bless at EvalInt 300 =
31% of raw = 62 at raw 200, pinned SpellHelper.cs:382-407; Greater Strength potion 20 x (100+EP)/100 with
EP 50 cap + Alchemy 300*10/33 = 48, pinned BasePotion.cs:207-218, 242; same mod name "[Magic] Str Buff" so
they do not stack, SpellHelper.cs:303-327) 62 + FoF 10 + Rose of Trinsic 5 (pinned RoseOfTrinsic.cs:180)
= about 379.
Dex: 240 + 50 + 12 + 62 (Bless) or 48 (Greater Agility) + 10 = about 374.
Int: 240 + 50 + 10 + 62 (Bless/Cunning) + 10 = about 372.
Mid standing (5000: max 11/item, 7 slots): 16 x 11 = 176 item part, total about 300.
No item at all (mimic + set + buff + FoF): about 130.
Racial: no Str/Dex/Int offset; Elf +20 ManaMax (pinned PlayerMobile.cs:584-585), Human +60 MaxWeight
(PlayerMobile.cs:237). Vet/StatCapScroll: our login write (2.B) overrides StatCap.
Pools: BonusHits all sources capped 25. BonusStam: mimic 150 + items (12, 8, ...) about 170+. BonusMana:
mimic 150 + set 15 + items 15+15+... about 200+.
Conclusion: OSI design offset is +25. Ours is roughly +130 (no gear) to +380 (full imbue). Any raw value
from 125 up therefore reaches the 500 clamp for a top-geared player (125 + 379 = 504). The raw ceiling
barely matters for them; the EFFECTIVE clamp (2.A) and the imbue cap (2.K) decide the outcome.

## (a) Ranked runaways / brokens, worst first
1. Imbue stat properties (ArtificersImbueGump.cs:182-195): +15 Str/Dex/Int per item on ~16-19 items, no
   per-character total. At raw 200 this alone pushes effective past 400. Effect at 200: effective 500 (clamp).
2. Effective clamp 500 (PlayerMobile-individual-stat-cap.patch:8,17,26 via ClusterFStatCaps.cs:103): lets
   all of the above through. Effect at raw 200 + full kit: Str 500 -> HitsMax 325, MaxWeight 1850, etc.
3. PetMimic (PetMimic.cs:1238-1243 + AOS-pet-mimic patch): +50 per stat (StatMods) and uncapped +150
   StamMax / +150 ManaMax. Effect at 200: Dex 200 -> StamMax 350+; Int 200 -> ManaMax 350+.
4. ClusterFBackpack (ClusterFBackpack.cs:33-42): carry limit 100+3.5*Str with no cap of its own. At raw 200
   no gear: 800; at effective 500: 1850 stones (OSI 550).
5. Medusa clone HP = player effective Str (Medusa.cs:651, pinned BaseCreature.cs:579-580): at 225 the clone
   has 225 HP vs the player's 187; at 500, 500 vs 325. Mild.
No "broken" verdicts in our code. Meditation start window (Meditation.cs:83) is a plateau that gets worse
with pool size (22% of pool usable at Int 500 / Med 120).

## (b) Exact places an F-12 builder must touch in OUR code
1. customizations/ClusterFStatCaps.cs:10 (DefaultIndividualStatCap 500 = the effective clamp), :11
   (DefaultTotalStatCap 1500), :103 (fallback 150 when disabled), :107 (StatCap write on login/world load).
   Note it overwrites any StatCapScroll/vet raise; per-character total (325..550 + 50 vet) needs to be
   computed here, not a constant, if scrolls are to matter.
2. Config: uo/modernuo/Configuration/modernuo.json:112-113 (individualCap, totalCap) and :160
   (stats.statMax = 500, the RAW ceiling, read by pinned SkillCheck.cs:23); same keys in
   Configuration-test/modernuo.json:117-118, :165. Lowering statMax to 200 strands any live raw > 200
   (pinned CanRaise only blocks gain; it does not reduce existing raw) - decide a migration.
3. patches/PlayerMobile-individual-stat-cap.patch:8, 17, 26 (getter clamp; already parameterised by item 1).
4. customizations/TestCenter/TestCenterKit.cs:160-175 (StatCap preservation around pinned fill). Pinned
   TestCenter.cs:90, 112, 134 hard-code 10..125 for "set str/dex/int" and :231 sets StatCap 250: needs a
   patch if the test shard should set stats to 200.
5. customizations/ArtificersImbueGump.cs:182-195 (MaxVanilla 8 / MaxGuild 15 for stat props): the real
   lever on offset; nothing else in our code bounds total item stat offset.
6. customizations/ClusterFPetMimicSettings.cs:69-80 and live config modernuo.json:63-65, 68, 73, 87
   (mimic +50 stats, +150 hits/stam/mana).
7. customizations/ClusterFBackpack.cs:33-42 if carry weight should not scale past OSI.
8. Not needing changes: CharacterCreation.cs:379-394 (10..60, sum 80/90), ClusterFAchievements.cs (no stat
   achievements), ClusterFResetStone.cs / ClusterFYoungPlayer.cs (no stat writes), ClusterFSkillGain.cs
   (rate only), CraftItem.cs (no stat term). Stat lock and StatCapScroll are pinned-only; our code never
   references StatLock/StrLock/StatCapScroll (grep: 0 hits).

## (c) Max offset estimate per stat (detail in section 5)
Str ~379 = imbue 240 (16 items x 15) + mimic 50 + set 12 + Bless 62 (EvalInt 300, raw 200) + FoF 10 + Rose 5.
Dex ~374 = 240 + 50 + 12 + 62 + 10. Int ~372 = 240 + 50 + 10 + 62 + 10.
Without imbuing: ~130. OSI: +25. Effective result = min(raw + offset, 500).

## (d) Unverified
- Whether Configuration/modernuo.json is what the live container actually loads (I may only read these
  two files); and how many live characters already have raw > 125 / > 200.
- Exact number of simultaneously equippable imbuable items (layer conflicts, e.g. robe vs chest, kilt vs
  leg armour); used 16 as realistic, 19 theoretical.
- Whether imbuing an equipped item refreshes StatMods immediately (does not change the max).
- Whether any guild standing >= 40000 is reachable in practice (15/item); 11-13 at mid ranks.
- Pinned consumers of the large effective stats (swing speed from Stam, damage bonus from Str, etc.) are
  out of scope here (pinned sweep).
- Whether ClusterFBackpack's deviation is recorded in docs/fidelity-principle.md.
