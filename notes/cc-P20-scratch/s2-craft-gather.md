# s2: crafting and gathering skills at 120 / 300 / 500 / 1000 (cc-P20)

Skills: Alchemy, Blacksmithy, Bowcraft/Fletching, Carpentry, Cooking, Tailoring, Tinkering, Mining, Lumberjacking, Fishing.
Pinned paths are relative to D:\UO\ModernUO-pinned\Projects. "ours" = D:\ShatteredLegacy\server\customizations (cust\) or \patches.
Read-only audit. Expansion branches evaluated: AOS/SE/ML/SA (Core.AOS true).

## 0. Shared mechanics

### 0.1 Our CraftItem.cs vs pinned CraftItem.cs (full diff done)

cust\CraftItem.cs (1517 lines) REPLACES UOContent/Engines/Craft/Core/CraftItem.cs. `diff -w` shows the math is IDENTICAL to pinned. The only differences:
- m_TypesTable gains 8 extended log/board pairs (ours :71-79).
- ConsumeRes: GetAmount -> GetBestGroupAmount(..., CheckHueGrouping) for UseAllRes (ours :651).
- DevTestingCrystal bypasses: resources (ours :587-590) and skills/success = 1.0 (ours :860-866). Staff/dev only; make sure the crystal can never reach players.
- ClusterFCraftRun (Craft X runs) refusal/after-attempt hooks, no math (ours :921-1013, :1047-1125, :1307-1310, :1325-1386, :1438, :1493).
- Hammer of Hephaestus familiarity + BOD autofill + achievements hooks (ours :1157-1162, :1215-1237). No skill math.

So the formulas below are pinned's, cited at both:
- Success: `chance = minChance + (val - min)/(max - min) * (1 - minChance)` + talisman SuccessBonus. ours :906 / pinned :886. NOT clamped. val = Skills[mainSkill].Value (includes item/HoH mods).
  Only consumers: CheckSkills (`chance > Random`), Craft() gate `chance <= 0`, Enhance `<= 0`, BOD item filters, gump (clamped to 0..1 for display, CraftGumpItem.cs:207,211). So >100% is harmless: it just means "cannot fail".
- Gain call: `from.CheckSkill(craftSkill.SkillToMake, craftSkill.MinSkill, craftSkill.MaxSkill)` for EVERY skill on the recipe, each attempt (ours :893-896 / pinned :875). Gain ceiling per recipe = its MaxSkill. No shard change.
- Exceptional (ours :807-834 / pinned :794): ECA per system:
  - ChanceMinusSixtyToFortyFive (Blacksmithy, Tailoring, Cooking): `chance - clamp(0.60 - (Value-95)*0.03, 0.45, 0.60)` -> offset is 0.45 at Value >= 100.
  - FiftyPercentChanceMinusTenPercent (Fletching): `chance*0.5 - 0.1`.
  - default (Alchemy, Carpentry, Tinkering, Glassblowing, Masonry): `chance - 0.6`.
  - plus talisman ExceptionalBonus if > 0. Not clamped, only compared to Random, so >100% = always exceptional.
- GetChanceAtMin: Alchemy 0, Blacksmithy 0, Fletching 0.5, Carpentry 0.5, Cooking 0, Tailoring 0.5, Tinkering 0 (0.5 for potion keg / faction trap kit), Glassblowing 0 (0.5 HollowPrism), Masonry 0. (Def*.cs:23-47)
- Material (sub-resource) requirement: `Skills[mainSkill].BASE < subResource.RequiredSkill` -> refuse (ours :629 / pinned :616; gump CraftGump.cs:571,589). Materials do NOT change success or exceptional chance in ModernUO; they are a pure Base gate. Item skill mods (HoH +5/+10/+12.5 Value) do not help this gate. Enhance uses VALUE instead (Enhance.cs:349): a Base-290 smith with Reinforced HoH (+10) can Enhance with Celestial but not craft with it (minor inconsistency).
- Maker's mark: exceptional + Base >= 100 (ours :1487). Threshold.
- Exceptional item effects do not read the crafting skill: weapon DI 35 (+ArmsLore/20, capped 50, BaseWeapon.cs:700-711), armor DistributeBonuses(15) + ArmsLore/20 random resist points, UNCAPPED count (BaseArmor.cs:597). So crafting skill past the "always exceptional" point is wasted (clamps). ArmsLore note (not my skill): ArmsLore 300 -> +15 resist points, 1000 -> +50 points on exceptional armor; only the 70 resist cap limits it. ArmsLore gain from crafting CheckSkill(ArmsLore,0,100) (BaseWeapon.cs:709).

### 0.2 Computed craft chances (success s / exceptional e; display-capped, raw in brackets)

| Item (system, min-max) | 120 | 300 | 500 | 1000 | e reaches 100% at |
|---|---|---|---|---|---|
| Dagger (Smith, -0.4-49.6) | s 241% e 100% | s 601% e 100% | s 1001% e 100% | s 2001% e 100% | 79.7 |
| PlateChest (Smith, 75-125) | s 90% e 45% | s 450% e 100% | s 850% | s 1850% | 147.6 |
| Plate Kabuto (Smith, 90-140) | s 60% e 15% | s 420% e 100% | s 820% | s 1820% | 162.6 |
| Bow (Fletch, 30-70) | s 162% e 71% | s 388% e 100% | 638% | 1262% | 166.1 |
| Yumi (Fletch, 90-130) | s 88% e 34% | s 312% e 100% | 562% | 1188% | 226.1 |
| Shirt (Tailor, 20.7-45.7) | s 249% e 100% | 609% | 1009% | 2009% | 75.8 |
| Gargish cloth chest (Tailor, ours 94-144) | s 76% e 31% | s 256% e 100% | 456% | 956% | 189.1 |
| Scissors (Tinker, 5-55) | s 230% e 100% | 590% | 990% | 1990% | 85.1 |
| Wind chimes (Tinker, 80-130) | s 80% e 20% | s 440% e 100% | 840% | 1840% | 160.1 |
| Quarter staff (Carp, 73.6-98.6) | s 143% e 83% | 503% e 100% | 903% | 1903% | 128.7 |
| Tetsubo (Carp, 80-140.3) | s 83% e 23% | s 232% e 100% | 398% | 813% | 212.7 |
| Bread loaf (Cook, 0-100) | s 120% e 75% | 300% e 100% | 500% | 1000% | 145.1 |
| Green tea (Cook, 80-130) | s 80% e 35% | 440% e 100% | 840% | 1840% | 152.6 |
| Greater heal (Alch, 55-105) | s 130% | 490% | 890% | 1890% | (potions not exceptional) |
| Deadly poison (Alch, 90-140) | s 60% | 420% | 820% | 1820% | - |
| Hollow prism (Glassblowing/Alch, 100-150) | s 70% e 10% | 250% e 100% | 450% | 950% | 210.1 |
| Any extended-ore item (e.g. Celestial PlateChest) | refused below Base 300 (Platinum 100 ... Celestial 300, ClusterFMiningExtension.cs:174-181) | same chances as iron once Base allows | | | |

All of these: clamps (success at item MaxSkill, exceptional at the value in the last column). No craft formula breaks at high skill; the risk is the opposite: everything past ~230 is wasted for crafting proper.

### 0.3 Harvest mechanics (HarvestSystem.cs)
- Gate and gain: `skillBase >= resource.ReqSkill && CheckSkill(def.Skill, resource.MinSkill, resource.MaxSkill)` (HarvestSystem.cs:142-147). Base for the gate, Value for the roll. Gain ceiling per resource = MaxSkill.
- Amount per harvest is NOT skill-based: ConsumedPerHarvest (Fel amount, human racial x1.1 on 10%) (HarvestSystem.cs:167-194). Jacobs Deepdelver/Worldbreaker pickaxes add +1 ore (cust\JacobsDeepdelverPickaxe.cs:20, JacobsWorldbreakerPickaxe.cs:21-22), not skill-based.
- Vein choice is weight-based, not skill-based; fallback to Iron/Log if Value < primary ReqSkill/MinSkill or 50% vein fallback (HarvestSystem.cs:332-351).
- Bonus resources (gems/amber/pearl) need Base >= ReqSkill (100/80), fixed chance (:209-211). Clamp.
- cust\ClusterFSkillGain.cs wraps all four CheckSkill handlers (3 attempts, 5x amount) but calls the base handler, so the min/max early-outs and therefore every ceiling below are unchanged (ClusterFSkillGain.cs:63-112).

## 1. Blacksmithy

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Craft success/exceptional | ours CraftItem.cs:906, :822-830 | see 0.1/0.2 | scales | clamps (all items 100% s/e by 162.6) | clamps | clamps | 140.0 (Plate kabutos, DefBlacksmithy.cs:251-257); ours adds Gargish items <=135 (cust\Engines\Craft\BlacksmithyCraftRegistrations.cs:91-125) |
| Material gate | ours CraftItem.cs:629; ClusterFMiningExtension.cs:174-181 | Base >= 0..99 vanilla, Platinum 100, Toxic 125, Blaze 150, Frost 175, Obsidian 200, Mythril 225, Adamantium 250, Celestial 300 | Platinum only | all | all | all | - |
| BOD turn-in gain | cust\ClusterFSmithBODSystem.cs:240,426, ranges :351-391 | CheckSkill(min,max) per material; exc +10 | scales | scales | no gain | no gain | 350 (Celestial exc 290-350); practically ~295, see BREAKS B3 |
| Commission gain | cust\ClusterFSmithCommissions.cs:616,687, ranges :772-800 | same idea | scales | scales | no gain | no gain | 335 (Celestial exc 300-335) |
| Large BOD roll | ClusterFSmithBODSystem.cs:95 | (Base-40)/300 > Random | 26.7% | 86.7% | 100% (>=340) | 100% | - | see BREAKS B4 |
| Small BOD exceptional | SmallSmithBOD.cs:126 | (Base+80)/200 | 100% (clamps at 120) | clamps | clamps | clamps | - |
| BOD post-Val material | patches\SmallSmithBOD-PostValorite.patch:27-48, patches\LargeSmithBOD.cs:84-110 | 30%/15% roll, then weights 50%..0.195% (Celestial) gated by Base 105..300 | Platinum/Toxic | all tiers possible | same | same | - |
| Commission material | ClusterFSmithCommissions.cs:429-445 | ladder by Base, 70/30 | Toxic/Platinum | 70% Celestial | same | same | - |
| Commission exceptional | ClusterFSmithCommissions.cs:463,511 | (Base-40)/100 | 80% | 100% (clamps at 140) | clamps | clamps | - |
| Enhance break chance | Enhance.cs:186-189, :314-330 | base 20 - (int)(Value-90)/10, + property; 10% fail per property separate | 17 | -1 (break ~0 for low props) | -21 (break 0) | -71 | - | clamps ~300-400 (break 0, 10% fail floor stays) |
| Repair | Repair.cs:41-75, :247 | weaken = 40 + missing - Value/10; difficulty window (d-25,d+25), d<=100 | scales | weaken only if missing > 10 | weaken only if missing > 10..; at 500 only if missing>10 | weaken only if missing > 60 | 125 (fully broken item) |
| HoH upgrade gates | cust\HammerOfHephaestus.cs:1122,1249 | thresholds | - | - | - | - | - |

recommendation: crafting itself clamps harmlessly; give 150-300+ smiths new outputs (extended-ore recipes with MaxSkill spread to 300+), and fix the gain path (B3) before anything else. Repair: floor weaken chance at e.g. 5% so durability stays a sink.

## 2. Tailoring

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Craft s/e | ours CraftItem.cs:906 | 0.5 at min, ECA 45-60 | scales | clamps (100% s/e by 189.1) | clamps | clamps | 144.0 (ours Gargish cloth chest, cust\Engines\Craft\TailoringCraftRegistrations.cs:91-98); pinned max 121 (BoneChest, DefTailoring.cs:651) |
| Leather material gate | DefTailoring.cs:662-665 | Base >= 0/65/80/99 | all | all | all | all | - |
| ArcaneGem charges | Items/Misc/ArcaneGem.cs:35 | clamp(Value/5, 16, 24) | 24 | clamps at 120 | clamps | clamps | - |
| Tailor BOD exceptional/material | SmallTailorBOD.cs:72+ (unmodified) | like smith | clamps | clamps | clamps | clamps | (pinned BOD reward, no gain call) |
| Repair (cloth) | Repair.cs:391-434 | as smith | | | | | 125 |

recommendation: let it scale (harmless); add 150-300 content (recipes, extended leathers) or gains stop at 144.

## 3. Tinkering

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Craft s/e | ours CraftItem.cs:906 | 0 at min, -0.6 | scales | clamps (by 160.1) | clamps | clamps | 130.0 (WindChimes, DefTinkering.cs:363); ours <=125 (TinkeringCraftRegistrations.cs:79-107) |
| Trap craft level | DefTinkering.cs:663-668 | level = (int)(Value/10); TrapPower = level*9 | L12, P108 | L30, P270 | L50, P450 | L100, P900 | - |
| Explosion trap dmg | TrappableContainer.ExecuteTrap.cs:63-72 | Random(10,30)*level, 100% fire | 120-360 | 300-900 | 500-1500 | 1000-3000 | BREAKS (B5) |
| Dart trap dmg | ExecuteTrap.cs:104-106 | Random(5,15)*level, physical | 60-180 | 150-450 | 250-750 | 500-1500 | BREAKS |
| Poison trap | ExecuteTrap.cs:128 | Poison level min(4, level-1) | Lethal | clamps at 50 | clamps | clamps | - |
| Remove Trap vs our trap | Skills/RemoveTrap.cs:61 | CheckTargetSkill(RemoveTrap, P, P+30) | needs RT 108 | needs RT 270 | needs RT 450 | needs RT 900 (untrappable) | - |
| Lockable container | Items/Containers/LockableContainer.cs:30-37 | level=0.8*Value; lock/req min(..., 95) | clamps ~136 | clamps | clamps | clamps | - |
| Golem repair | Repair.cs:183-203 | heal min(dmg, Value*0.3)+30 | 66 | 120 | 180 | 330 (limited by golem max hits) | 100 (CheckSkill 0-100) |
| Clockwork golem scalar | Items/Misc/ClockworkAssembly.cs:53-71 | step to 1.0 at 100 | clamps | clamps | clamps | clamps | - |
| Faction trap removal | RemoveTrap.cs:96-97 | CheckTargetSkill(Tinkering,80,100) | - | - | - | - | 100 |
| Weapon engraving | WeaponEngravingTool.cs:148 | Value/100 | 100% | clamps | | | - |

recommendation: cap trap level at 10 (vanilla GM) or soft-cap `level = 10 + sqrt(Value-100)/2`; then let craft scale and add new tinker content past 130.

## 4. Carpentry (incl. Masonry, which uses Carpentry)

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Craft s/e | ours CraftItem.cs:906 | 0.5 at min, -0.6 | scales | clamps (by 212.7) | clamps | clamps | 140.3 (Tetsubo, DefCarpentry.cs:322); Masonry 132 (DefMasonry.cs:107-110); ours <=128.9 (CarpentryCraftRegistrations.cs:57) |
| Wood material gate | DefCarpentry.cs:601-607; ClusterFLumberjackingExtension.cs:274-281 | vanilla 0-100; ALL 8 extended boards = 100.0 | all | all | all | all | - |
| Extended wood properties | cust\ResourceInfo.cs (Ironwood..Starwood CraftAttributeInfo empty) | none | - | - | - | - | - |
| Log->board | Items/Skill Items/Lumberjack/Log.cs:92-93 | Carpentry or LJ Value >= wood req | threshold | | | | - |
| Taxidermy / Masonry book | TaxidermyKit.cs:39,88; MasonryBook.cs:24 | Base thresholds 90/100 | - | | | | - |

recommendation: harmless; spread extended board gates 100..300 and give them attributes if Carpentry is meant to grow past 140.

## 5. Bowcraft/Fletching

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Craft s/e | ours CraftItem.cs:906, :824 | 0.5 at min, e = 0.5*s - 0.1 | scales | clamps (by 226.1) | clamps | clamps | 130.0 (Yumi / RepeatingCrossbow, DefBowFletching.cs:123,128) |
| Wood gate | ClusterFLumberjackingExtension.cs:302-309 | all extended logs 100.0 | all | all | all | all | - |
| JukaBow modify | Items/Weapons/Ranged/JukaBow.cs:35,62 | Base >= 100 | threshold | | | | - |

recommendation: same as Carpentry.

## 6. Cooking

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Craft s/e | ours CraftItem.cs:906 | 0 at min, ECA 45-60 | scales | clamps (by 152.6) | clamps | clamps | 130.0 (GreenTea, DefCooking.cs:143); WhiteChocolate 127.5 |
| Other reads | none in pinned or ours (grep) | - | | | | | - |

recommendation: harmless; no content past 130.

## 7. Alchemy (incl. Glassblowing)

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Craft success | ours CraftItem.cs:906 | 0 at min | scales | clamps | clamps | clamps | 140.0 potions (DeadlyPoison, DefAlchemy.cs:194-199); 150.0 Glassblowing HollowPrism (DefGlassblowing.cs:123) |
| EnhancePotions skill part | Items/Skill Items/Magical/Potions/BasePotion.cs:207-218 | EP = item EP (cap 50) + (int)(Value*10/33), UNCAPPED | +36% | +90% | +151% | +303% | - |
| Greater Heal | Heal Potions/BaseHealPotion.cs:19-20, GreaterHealPotion.cs:13-14 | 20-25 * (1+EP) | 27-34 | 38-47 | 50-62 | 80-100 (90-113 w/ 50 EP), every 10 s | scales to 500; strong at 1000 |
| Greater Explosion (direct) | Explosion Potions/BaseExplosionPotion.cs:151-155, :180-189 | Scale(20..40) + Value/5 fire | 51-78 | 98-136 | 150-200 | 280-361 (70 fire resist: 84-108) | BREAKS at 500/1000, strong at 300 |
| Greater Conflagration tick | Conflagration Potions/BaseConflagrationPotion.cs:237-241, :258,:312 | (4..8 + F/125 + F/250) * (1+EP), F = Value*10; per second, 10 s field, 30 s reuse | 23-28/s | 76-83/s | 160-170/s | 499-515/s (70 resist: ~150/s) | BREAKS at 300+ |
| Cure chance | Cure Potions/BaseCurePotion.cs:39 | base chance * (1+EP) | Deadly 0.75->100% at ~112 | Lethal 0.25 -> 47% (60% w/ EP 50) | 63% | 100% lethal cure (~990) | clamps then trivialises lethal |
| Str/Agi offset | Strength/Agility potions :25, BasePotion.cs:242 | 20 * (1+EP) and duration *(1+EP) | +27 | +38 | +50 | +80 STR/DEX, 4x duration | soft-cap |
| Refresh | Refresh Potions/BaseRefreshPotion.cs:32 | Scale(Refresh*StamMax) | clamps at StamMax | | | | - |
| Glassblowing gate | DefGlassblowing.cs:38 | Base >= 100 + book | threshold | | | | - |
| InfusedAlchemistsGem | cust\Items\Artifacts\Consumables\InfusedAlchemistsGem.cs:28 | Skills.Alchemy.Base += 1, no cap check (Skill.BaseFixedPoint clamps only at 6553.5, Server/Skills.cs:179) | - | - | - | - | BREAKS (B7): bypasses individual cap and total cap |

recommendation: soft-cap the skill part of EnhancePotions: e.g. `skillEP = 30 * (1 - exp(-(Value)/100)) * ...` or simply `min(Value,120)*10/33` plus diminishing `sqrt(Value-120)`; cap explosion alchemyBonus and conflag bonus at their 120 values; then give alchemists new effects (potion duration, new potion types) past 120.

## 8. Mining

Our patches\Mining.cs replaces pinned Engines/Harvest/Mining.cs; diff = only `partial` (adds hooks in cust\ClusterFMiningExtension.cs and cust\CompactOreSatchelRoutingHook.cs:51). Resource table identical to pinned (patches\Mining.cs:113-188).

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Ore harvest (vanilla) | patches\Mining.cs:115-187 | Iron (0,0,100) ... Valorite (99,59,139): chance (V-min)/(max-min) | Iron 100%, Valorite 76% | 100% all | clamps | clamps | 139 |
| Ore harvest (extended) | cust\ClusterFMiningExtension.cs:84-94 | all ReqSkill 100 (Base); Platinum (65,140) ... Celestial (80,155) | Plat 73%, Celestial 53% | 100% | clamps | clamps | 155.0 (Celestial) |
| Vein weights | ClusterFMiningExtension.cs:108-118 | 8..1 of 1036, not skill-based; RandomizeVeins=false (:131) | - | - | - | - | - |
| Sand | patches\Mining.cs:252-255, :334-336 | ReqSkill 100 Base + SandMining; (70, 400) | 15% | 70% | 100% | 100% | 400.0 |
| Stone (granite) | patches\Mining.cs:284-288 | Base >= 100, 10% | threshold | | | | - |
| Smelt ore (pinned) | Items/Resources/Blacksmithing/Ore.cs:176-205 | diff+-25; vanilla 65..99; EXTENDED ores fall to default 50 -> (25,75), no skill gate (diff>50 check fails) | trivial | | | | 124 (Valorite) |
| Satchel smelt | cust\ReinforcedOreSatchel.cs:126-146 | Value >= difficulty, guaranteed, no gain | threshold | | | | none |
| Guild salvage resmelt | cust\SmithGuildSalvageBag.cs:145-148 | ingots = ((4+Value)*N - 4)*0.0068, NO 100 cap (pinned SalvageBag.cs:94-98 caps at 100) | 21 of 25 (84%) | 51 of 25 (206%) | 85 of 25 | 170 of 25 | BREAKS (B1) |
| Guild salvage difficulty | SmithGuildSalvageBag.cs:60-76,154 | Platinum 105 ... Celestial 300 | | | | | - |
| Treasure dig range | Items/Maps/TreasureMap.cs:585-593 | 4 at >=100 | clamps | | | | - |
| Jacobs pickaxes | cust\Jacobs*Pickaxe.cs (SkillBonuses +5..+25 Mining Value; upgrade gates 75/80/90/100 Value) | Value-only, so they raise roll chance but not Base gates | - | | | | - |
| Pinned salvage bag | Items/Containers/SalvageBag.cs:94-100 | capped 100 | clamps | | | | - |

recommendation: restore `Math.Min(Value,100)` (or a gentle cap that never exceeds ~95% return) in SmithGuildSalvageBag; give extended ores real smelt difficulties (e.g. 100..300 matching the ingot gates) in Ore.cs or a BaseOre override; past 155, give miners something (yield, rare-vein find chance) if Mining is to scale.

## 9. Lumberjacking

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Log harvest (vanilla) | Engines/Harvest/Lumberjacking.cs:71-77 | Log (0,0,100) ... Frostwood (100,60,140) | Frostwood 75% | 100% | clamps | clamps | 140 |
| Log harvest (extended) | cust\ClusterFLumberjackingExtension.cs:219-229 | ReqSkill 100; Ironwood (60,140) ... Starwood (68,148) | Starwood 65% | 100% | clamps | clamps | 148.0 |
| Discovery gate | ClusterFLumberjackingExtension.cs Give() | unreported extended log -> regular Log | - | | | | - |
| Amount | Lumberjacking.cs:53-54 | 10 (20 Fel), not skill | - | | | | - |
| Axe damage (AOS) | Items/Weapons/BaseWeapon.cs:2559-2561, :2599-2602 | lumberBonus = Value*0.2% + 10% at >=100; NOT inside the 100% DI cap ("No caps apply") | +34% | +70% | +110% | +210% | BREAKS (B2) |
| Axe passive gain | BaseWeapon.cs:2545-2549 | CheckSkill(LJ, 0, 100) | no gain | | | | 100 |
| Log->board | Log.cs:92-93 | threshold | | | | | - |

recommendation: soft-cap the axe bonus at its GM value (30%) or `30 + 10*ln(1 + (Value-100)/100)`; give extended logs attributes or spread their gates 100..300 if LJ is meant to grow.

## 10. Fishing

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Fish harvest | Engines/Harvest/Fishing.cs:100 | Fish (0,0,100) | 100% | 100% | 100% | 100% | 100.0 (only gain source) |
| Deep-water rares (net, big fish, T-map, MIB) | Fishing.cs:15-18, :181-185 | each (Value-80)/4000, checked in order; ReqSkill Base 80/80/90/100 | 1% each, ~3.9% total | 5.5% each, ~20% of casts | 10.5% each, ~36% | 23% each, ~65% of casts | BREAKS economy at 1000 (B6) |
| Serpent spawn | Fishing.cs:324-366 | every net/map/MIB spawns a sea serpent (25% deep sea) | ~3% casts | ~15% | ~26% | ~47% | - |
| Magic fish | Fishing.cs:19-28 | (V-125)/(-2375) | 0.2% | 0 (clamps at 125) | 0 | 0 | - |
| Shoes | Fishing.cs:29 | (V-105)/(-525) | 0 | 0 | 0 | 0 | - |
| Null catch (fail) | Fishing.cs:30 | (V-200)/(-400) | 20% | 0 | 0 | 0 | - |
| White pearl | Fishing.cs:115-116 | Base >= 80, 0.6% | clamps | | | | - |
| T-map level | Fishing.cs:215-228 | always level 1 (0 on Haven young) | - | | | | - |
| SOS chest level | Fishing.cs:304 | min(4, sos.Level) | - | | | | - |
| Aquarium net | Items/Aquarium/AquariumFishingNet.cs:77-84 | Value/100 chance, species max Value/5 cap 20 | clamps at 100 | | | | - |

recommendation: Fishing cannot be gained past 100 at all today; if it should, add a resource with MaxSkill > 100. Cap the four rare mutate chances at their ~150 values (or diminishing returns) before 1000 is allowed.

## 11. BREAKS findings

- B1 SmithGuildSalvageBag ingot dupe (Mining): cust\SmithGuildSalvageBag.cs:145-148 removed pinned's `if (mining > 100) mining = 100` (pinned Items/Containers/SalvageBag.cs:94-98). For a 25-ingot item: 21 ingots at 120, 25 (100%) at 147.1, 51 at 300 (LIVE), 85 at 500, 170 at 1000. Craft iron plate (Smith >= 125 = 100% success) -> salvage -> net +26 iron per cycle at 300, plus guild seals per item. Works for every extended metal too once gates are met.
- B2 Lumberjacking axe damage: BaseWeapon.cs:2559-2561 adds Value*0.2% (+10% at GM) to totalBonus outside the 100% DI cap: +70% at 300 (live), +110% at 500, +210% at 1000.
- B3 Blacksmithy progression wall (gains): crafting gains stop at 140; above that only BOD/commission turn-ins gain. Adamantium windows top out at 285 (commission exc) / 295 (BOD exc, but a post-Val Adamantium BOD is 0.3*0.78% = 0.23% of BODs). Celestial windows (280-350 BOD, 290-335 commission) are only offered at Base >= 300 (patches\SmallSmithBOD-PostValorite.patch:40-44, ClusterFSmithCommissions.cs:445) and Celestial needs Base 300 to craft (ClusterFMiningExtension.cs:181). So Base 295-300 has no gain source and Celestial crafting is unreachable by play. HoH Value mods make it worse (window max is checked against Value). Also Celestial BOD odds 0.06%.
- B4 Large BOD lock-out: ClusterFSmithBODSystem.cs:95 `(Base-40)/300` -> 86.7% at 300, 100% at >=340. When the 1-large cap is reached (:98-104) the request returns null instead of falling back to a small BOD, so at 300 87% of requests are refused, and at >=340 every request is refused until the large is done.
- B5 Tinker traps: DefTinkering.cs:663-668 trap level = Value/10 uncapped. Explosion trap 300-900 fire at 300, 1000-3000 at 1000; dart 150-450 at 300; TrapPower 270/900 needs Remove Trap 270/900 to disarm (RemoveTrap.cs:61). Already 120-360 at 120 (vanilla GM 100-300).
- B6 Fishing rares at high skill: (Value-80)/4000 per rare; at 1000 ~65% of deep-water casts are net/big fish/map/MIB and ~47% spawn a serpent. Not reachable today (Fishing gain ceiling 100) but breaks once 1000 is granted.
- B7 InfusedAlchemistsGem: Base += 1 with no cap check (cust\...\InfusedAlchemistsGem.cs:28); can push Alchemy past the 300 individual cap and the total cap. Severity depends on drop rate (unverified).
- B8 Alchemy potion power: EnhancePotions skill part uncapped (BasePotion.cs:210). Greater Conflagration 76-83 fire/s at 300 (vanilla ~20-26), 499-515/s at 1000; Greater Explosion 98-136 at 300, 280-361 at 1000; Greater Cure becomes a guaranteed lethal cure near 1000.

Design gaps (not "breaks" by the formula test, but they matter):
- Extended ore smelting has no skill gate: Ore.cs:176-186 default difficulty 50 -> any Mining >= 25 smelts Celestial ore (only the guild bag and satchel gate it).
- Extended woods all gate at 100 with empty CraftAttributeInfo (cust\ResourceInfo.cs extended lumber block), so they give nothing past 100 to Carpentry/Fletching.
- Material gate uses Base, Enhance gate uses Value (Enhance.cs:349 vs ours CraftItem.cs:629).
- Repair weaken chance reaches 0 for normal damage past ~400 (Repair.cs:41-42): durability sink disappears.
- The ore "0-300" ladder only exists on the smithing side (ingot gates 100-300); the mining side tops at 155 (harvest) and the design doc (D:\ShatteredLegacy\design\systems\extended_resources.md) specifies tiers and facets, not skill numbers.

## 12. Gain ceilings (summary)

| Skill | Gain ceiling (highest MaxSkill) | Source | Notes |
|---|---|---|---|
| Alchemy | 150.0 | Glassblowing HollowPrism (DefGlassblowing.cs:123); potions 140 | nothing past 150; gem bypass B7 |
| Blacksmithy | 140 craft; 335 commission; 350 BOD | DefBlacksmithy.cs:251-257; ClusterFSmithCommissions.cs:797; ClusterFSmithBODSystem.cs:381 | practically ~295, dead zone to 300 (B3); repair 125 |
| Fletching | 130.0 | DefBowFletching.cs:123,128 | |
| Carpentry | 140.3 | DefCarpentry.cs:322 (Masonry 132) | |
| Cooking | 130.0 | DefCooking.cs:143 | |
| Tailoring | 144.0 | ours TailoringCraftRegistrations.cs:93 | pinned only 121 |
| Tinkering | 130.0 | DefTinkering.cs:363 | golem repair 100 |
| Mining | 400.0 (sand); 155 ore; 124 smelt | patches\Mining.cs:254; ClusterFMiningExtension.cs:93; Ore.cs:189-190 | sand needs Base 100 + SandMining book |
| Lumberjacking | 148.0 | ClusterFLumberjackingExtension.cs:228 | axe combat 100 |
| Fishing | 100.0 | Fishing.cs:100 | no gain past GM at all |

Unverified: Magic Untrap spell interaction with TrapPower 270-900; InfusedAlchemistsGem drop sources; whether any other gain source (scrolls) exists outside these files (grep for Transcendence/Alacrity in customizations found only a boss file, not checked).
