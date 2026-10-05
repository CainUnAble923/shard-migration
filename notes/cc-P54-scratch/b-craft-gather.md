# cc-P54 scratch b: CRAFT AND GATHER gain ceilings at the 200 cap

Read-only research. Engine: `D:\UO\ModernUO-pinned` at `d4531cd94b739613155225c234900de9f47d2c88` (checked with
`git rev-parse HEAD`); pinned paths are relative to `Projects\`. `C\` = `D:\ShatteredLegacy\server\customizations`,
`P\` = `D:\ShatteredLegacy\server\patches`. Shard as cc-P53 left it (working tree). Nothing edited or built.

## 0. Mechanics that decide every ceiling (verified on d4531cd94)

- `UOContent\Skills\SkillCheck.cs:58-67` (CheckLocation) and `:180-189` (CheckTarget): `value = skill.Value`;
  `value < min` returns false with no gain; `value >= max || min >= max` returns true with no gain roll. Direct-chance
  forms: `chance >= 1.0` no roll (`:100`, `:220`). Gain needs `skill.Base < skill.Cap` (`:248`). Gain probability
  floor 0.01 (`:135-138`).
- **Value, not Base, is tested against max.** Since cc-P53 Part C (D-113, `P\PlayerMobile-skill-bonus-above-cap.patch`)
  item and temporary bonuses count above the cap. So a window that tops out at M stops gaining at Base = M - bonus.
  This bites any "max = Cap" (Meditation-pattern) proposal: `C\Meditation.cs:115` passes
  `m.Skills[SkillName.Meditation].Cap` (the brief's ":92" is out of date), so a +15 item stops Meditation gain at
  Base 185. Any pattern-(a) change should pass `Cap + max(0, Value - Base)` (or test Base), not Cap.
- `C\ClusterFSkillGain.cs:63-112` wraps all four handlers (3 attempts, 5x amount) and calls the base handler with the
  same min/max/chance; `ShouldBoost` reads Base < Cap (`:141-147`). Ceilings unchanged.
- **Craft gain**: pinned `Engines\Craft\Core\CraftItem.cs:871-894` rolls `from.CheckSkill(craftSkill.SkillToMake,
  minSkill, maxSkill)` for every skill on the recipe (`:893`), each completed attempt. Success chance `:902-904`
  (`minChance + (val-min)/(max-min)*(1-minChance)`), exceptional `:812-839`. `P\CraftItem-shard-hooks.patch` adds
  extended-lumber type pairs, the DevTestingCrystal bypass, Craft-X refusal hooks and `GetBestGroupAmount`; it
  changes **no** skill math (grep of the patch for skill/chance: only the dev bypass). `C\CraftItem.cs` (P20's
  replacement) no longer exists.
- **Material does not move the craft window.** `typeRes` is used only by the Base gate
  (`CraftItem.cs:630`, `Base < subResource.RequiredSkill` refuses) and resource consumption; `GetSuccessChance` never
  reads it. So crafting in Celestial or Starwood has the same success, exceptional and gain window as iron or plain wood.
  Note `typeRes` is the selected material even for recipes that do not consume it: mutation happens only when a
  resource equals the system's `ResType` (`CraftItem.cs:620-628`). Any material-scaled hook must test that.
- **Harvest gain**: `Engines\Harvest\Core\HarvestSystem.cs:147` `skillBase >= resource.ReqSkill &&
  CheckSkill(def.Skill, resource.MinSkill, resource.MaxSkill)`; resource chosen first (`:138-140`, `MutateResource
  :332-351`, falls back if `Value < primary.ReqSkill || Value < primary.MinSkill` `:346`, or on the vein's 50% fallback
  `:339`). One roll decides both yield and gain.
- **Repair** (Smith, Tailor, Carpentry, Tinker, Fletching): `Engines\Craft\Core\Repair.cs:47-48` difficulty max 100.0,
  window `difficulty +-25` (`:75`): ceiling 125 for all five.

## (i) Per-skill table

| Skill | Gain calls (file:line, pinned/ours, min/max) | Ceiling now | P20 ceiling (confirmed/corrected) | Reaches 200? |
|---|---|---|---|---|
| Alchemy | Craft top: Glassblowing HollowPrism 100-150 (pinned `DefGlassblowing.cs:123`; needs Base 100 + Glassblowing book, `:38`); DeadlyPoison 90-140 (pinned `DefAlchemy.cs:199-204`, values `:203-204`); SmokeBomb 90-120 (`:260`). No other Alchemy CheckSkill in pinned, C\ or P\. `C\Items\Artifacts\Consumables\InfusedAlchemistsGem.cs:28` sets `Base += 1` with no cap check (not a roll; no drop source found in C\ or pinned, staff-add only) | **150.0** | 150: confirmed | No: STALLED at 150 |
| Blacksmithy | Craft top: Plate kabutos 90-140 (pinned `DefBlacksmithy.cs:251-257`); ours <=135 (`C\Engines\Craft\BlacksmithyCraftRegistrations.cs:91,92,117,122,125`). Repair 125 (pinned `Repair.cs:75`). BOD turn-in (ours, `C\ClusterFSmithBODSystem.cs:277-281`, window `:400-441`): post-Val = requirement -20/+20 (`:424-428`), exceptional +10/+10 (`:432-437`): Mythril 155-195 / exc 165-205, Adamantium 167.5-207.5 / exc 177.5-217.5, Celestial 180-220 / exc 190-230. 1 check per small, 2 per large (3 from tier 5) (`:362-389`, called from `C\ClusterFSmithBODPayout.cs:185`). Commission (ours, `C\ClusterFSmithCommissions.cs:658` large, `:729` small; window `:825-850`): requirement -10/+20, exc +10/+10: Mythril exc 175-205, Adamantium 177.5-207.5 / exc 187.5-217.5, Celestial exc 200-230 | **200 (cap)**, via commission Adamantium exceptional (max 217.5) | ~295 (300-era): **corrected** to 200 by P53's tables. Craft 140 confirmed | **Yes.** Commission: at Base 187.5-199.9 the offer is 70% Adamantium / 30% Mythril (`ClusterFSmithCommissions.cs:483`), exceptional chance `(Base-40)/100` is 1.0 above 140 (`:504`, `:551`), so nearly every order is exc Adamantium (187.5-217.5) or exc Mythril (175-205). No cooldown, abandon allowed. BOD route also reaches but post-Val Mythril/Adamantium smalls are 0.3 x 1.56% / 0.78% of orders (`P\SmallSmithBOD-PostValorite.patch:15-16, :28-34`). Caveat: a smith with +30 or more Blacksmithy bonus reads Value >= 217.5 at Base 187.5 and stops short |
| Bowcraft/Fletching | Craft top: Yumi, RepeatingCrossbow 90-130 (pinned `DefBowFletching.cs:123,128`); elven bows 75-125 (`:223-243`). Repair 125. No other | **130.0** | 130: confirmed | No: STALLED |
| Carpentry | Craft top: Tetsubo 80-140.3 (pinned `DefCarpentry.cs:322`); PhantomStaff 90-130 (`:330`); Masonry (Carpentry main) SmallUrn/SmallTowerSculpture 82-132 (`DefMasonry.cs:107, :115`); ours GargishGnarledStaff 78.9-128.9 (`C\Engines\Craft\CarpentryCraftRegistrations.cs:57`), Incubator 90-115 (`C\Engines\Craft\IncubatorCarpentryRecipe.cs:60`), Kings Collection <=105. Repair 125 | **140.3** | 140.3: confirmed | No: STALLED |
| Cooking | Craft top: GreenTea 80-130 (pinned `DefCooking.cs:143-148`, values `:147-148`); WhiteChocolate 52.5-127.5 (`:416`). No other Cooking CheckSkill anywhere | **130.0** | 130: confirmed | No: STALLED |
| Tailoring | Craft top: ours Gargish cloth chest 94-144 (`C\Engines\Craft\TailoringCraftRegistrations.cs:93, :97`), legs 141.2 (`:94, :98`); pinned BoneChest 96-121 (`DefTailoring.cs:651`). Leathers gate only, max 99 (`DefTailoring.cs:662-665`); no shard leathers exist (`C\ResourceInfo.cs` enum: Regular/Spined/Horned/Barbed only). Tailor BODs pinned, no turn-in gain. Repair 125 | **144.0** | 144: confirmed | No: STALLED |
| Tinkering | Craft top: WindChimes, FancyWindChimes 80-130 (pinned `DefTinkering.cs:363, :366`); Pendant/Essence/Bracer 100-125 (`:529-565`); ours <=125 (`C\Engines\Craft\TinkeringCraftRegistrations.cs:79-107`). Golem repair 0-100 (`Repair.cs:203`); faction trap removal 80-100 (`Skills\RemoveTrap.cs:97`); key 0-75 (`Items\Misc\Key.cs:313`); lockable -5-15 (`Items\Containers\LockableContainer.cs:22`). Repair 125. Sub-res: 9 OSI metals only, max 99 (`DefTinkering.cs:585-597`); our extended metals are added to Blacksmithy only (`C\ClusterFMiningExtension.cs:173-180`) | **130.0** | 130: confirmed | No: STALLED |
| Mining | Ore: vanilla Iron 0-100 ... Valorite 59-139 (`P\Mining.cs:115-187`, full replacement, diff vs pinned = `partial` only); extended Platinum 65-140 ... Celestial 80-155, all ReqSkill 100 (`C\ClusterFMiningExtension.cs:98-105`). **Sand 70-400**, ReqSkill 100 (`P\Mining.cs:254`), needs Base >= 100 and SandMining (`:334-336`; book sold by the Glassblower, pinned `Mobiles\Vendors\SBInfo\SBGlassblower.cs:41`, spawned in Ilshenar `Distribution\Data\Spawns\shared\ilshenar\Vendors.json`). Smelt: pinned `Items\Resources\Blacksmithing\Ore.cs:167-181`, window difficulty +-25, Valorite 74-124, extended ores default 50 -> 25-75 (`:177`), roll `:197`; satchel smelting goes through this step (`P\Ore-smelt-at-forge.patch`). Guild salvage bag, `C\ReinforcedOreSatchel.cs`, work orders: no CheckSkill | **200 (cap)** via sand (window to 400); ore 155; smelt 124 | 155 ore / 400 sand: confirmed | **Yes**, sand only (Base 100 + SandMining book). Ore stalls at 155 |
| Lumberjacking | Harvest: vanilla Log 0-100 ... Frostwood 60-140 (pinned `Engines\Harvest\Lumberjacking.cs:71-77`); extended Ironwood 60-140 ... Voidwood/Starwood 68-148, ReqSkill 100 (`C\ClusterFLumberjackingExtension.cs:230-237`). Axe combat `CheckSkill(Lumberjacking, 0, 100)` (pinned `Items\Weapons\BaseWeapon.cs:2532` AOS, `:2605` pre-AOS). Work orders (20 Foresters/LJ) no CheckSkill | **148.0** | 148: confirmed | No: STALLED |
| Fishing | Harvest: Fish 0-100, only resource (pinned `Engines\Harvest\Fishing.cs:100`). Mutate table (`:13-31`, roll `:181-185`) uses Value for rare chance, no gain. No shard Fishing code | **100.0** | 100: confirmed | No: STALLED |

Count: **2 reach 200 (Blacksmithy, Mining), 8 stalled** (Alchemy 150, Fletching 130, Carpentry 140.3, Cooking 130,
Tailoring 144, Tinkering 130, Lumberjacking 148, Fishing 100).

Top items checked by script over every `AddCraft` in the nine pinned Def files (counts: Alchemy 25, Blacksmithy 146,
Fletching 24, Carpentry 154, Cooking 46, Tailoring 126, Tinkering 96, Glassblowing 14, Masonry 13; the few with an
integer min, e.g. AcidProofRope 80-130, read by hand). Secondary-skill `AddSkill` windows in pinned top out at 85
(Tailoring 65-85), in ours at 55: none raises a ceiling.

## (ii) Proposals for the stalled skills

### Shared piece for Carpentry, Fletching, Tinkering: a material-shifted gain window (option b)

One hook in pinned `CraftItem.GetSuccessChance` (`CraftItem.cs:891-894`, through `P\CraftItem-shard-hooks.patch`)
calling a new `C\ClusterFCraftGainWindow.cs`: for the **gain roll of the main skill only**, when the recipe really
consumes the system's sub-resource (some `Resources[i].ItemType == resCol.ResType`, the same test as `:620-622`) and
the selected sub-resource's `RequiredSkill` R is above 100, roll `CheckSkill(main, itemMin + S, itemMax + S)` with
S = R - 100. Success chance, exceptional chance, the `allRequiredSkills` test and every secondary-skill roll keep the
item's own numbers (use separate locals; `minMainSkill`/`maxMainSkill` must not change).

Why shift and not the commission's fixed (R-10, R+20): the shift keeps item difficulty meaningful and is safe on
zero-width recipes. Carpentry's Board recipe is 0-0 from `typeof(Log)` (pinned `DefCarpentry.cs:95`) and Log is
Carpentry's ResType (`DefCarpentry.cs:597`), so a fixed window would let a player cut Starwood logs into Starwood
boards 1:1, losing nothing, and roll gains to 220. Shifted, 0-0 stays `min >= max` = no roll.

Every OSI material has R <= 100 (metals 65-99, woods to 100, leathers to 99), so S = 0 and nothing OSI changes.
Decide one thing: whether the hook also covers Blacksmithy. Our metals already sit at 112.5-200, so smiths would gain
to 200 by crafting (Adamantium kabuto 177.5-227.5) as well as by commission. That changes the smith design (orders as
the route past 140). The default should be to limit it to Carpentry, Fletching and Tinkering and ask Chase.

### Carpentry (b): F-28's wood re-gate plus the shared hook

Today all eight boards gate at 100 (`C\ClusterFLumberjackingExtension.cs:294-301`), so S = 0 and the hook alone does
nothing. F-28 Q3 is already approved (Chase 2026-10-02): Ironwood 100, Ghostwood 115, Emberbark 130, Frostbark 140,
Shadowbark 155, Runewood 170, Voidwood 185, Starwood 200. Tetsubo (80-140.3) windows: Frostbark 120-180.3 (usable from
Base 140), Shadowbark 135-195.3, Runewood 150-210.3, Voidwood 165-225.3. That is continuous from 140.3 to the cap:
**reaches 200**. (Starwood needs Base 200 and so never trains anyone; it is the reward tier.)
- Skipped (a): Carpentry items succeed every time past their max (Tetsubo by 140.3), so a window to the cap would have
  no difficulty behind it. Exceptional stays uncertain until 212.7, but stretching the window on that basis would also
  reach sub-100 items (fidelity) and invites macroing the cheapest hard item.
- Files: `P\CraftItem-shard-hooks.patch` (pinned CraftItem.cs), new `C\ClusterFCraftGainWindow.cs`,
  `C\ClusterFLumberjackingExtension.cs:294-301` (8 numbers).
- Fidelity: none below 100 or 120. Only shard woods move. The re-gate means Ghostwood and the woods above it need more
  than 100 Base (F-28's change, already approved).
- Exploit check: no listed exploit uses Carpentry. New between 160 and 200: none. Craft output does not read
  Carpentry beyond success and exceptional, which is clamped. Material consumption paces the gain, with Voidwood at
  vein weight 2 and Starwood at 1 (`:258`).

### Bowcraft/Fletching (b): same hook, same F-28 re-gate

Logs gate at 100 today (`C\ClusterFLumberjackingExtension.cs:322-329`). With the ladder, Yumi (90-130) windows run:
Emberbark 120-160 (from Base 130), Frostbark 130-170, Shadowbark 145-185, Runewood 160-200 (gains until 199.9, so it
reaches 200), Voidwood 175-215. **Reaches 200.** Skipped (a) for the same reason (Yumi succeeds every time past 130).
- Files: as Carpentry, plus `:322-329`.
- Fidelity: none below 100 or 120.
- Exploit check: none listed. Bows read no Fletching value at use time. At 200, exceptional on Yumi is 0.5 x 3.75 - 0.1
  (capped) and certain from 226.1, harmless. F-28 wood bonuses read the material, not the skill.

### Tinkering (b): our extended metals as Tinkering materials, the shared hook, and a trap cap (required)

Add the eight extended ingots to Tinkering's sub-resources, with the same `ClusterFMetalTiers` requirements, next to
the Blacksmithy block (`C\ClusterFMiningExtension.cs:173-180`). WindChimes (80-130, made from IronIngot, which is the
ResType) windows: Toxic 105-155 (from Base 125), Blaze 117.5-167.5, Frost 130-180, Obsidian 142.5-192.5, Mythril
155-205, Adamantium 167.5-217.5. Continuous from 130: **reaches 200.**
- Skipped (a): tinker items succeed every time past 130, so a window to the cap would have no difficulty behind it.
  Skipped (c) F-20 Tinker BODs: that is a large port, and its turn-in windows would need these same extended metals
  anyway.
- **Trap cap, required in the same batch.** Trap level = `(int)(Tinkering.Value / 10)`, uncapped (pinned
  `DefTinkering.cs:678-682`). Explosion damage `RandomMinMax(10,30) * level`, 100% fire
  (`TrappableContainer.ExecuteTrap.cs:65`); dart `RandomMinMax(5,15) * level` (`:107`); TrapPower = level x 9, and
  Remove Trap rolls `(TrapPower, TrapPower+30)` (`Skills\RemoveTrap.cs:61`). At today's ceiling of 130: level 13,
  130-390 fire. At 200: level 20, 200-600 fire, dart 100-300, TrapPower 180, so Remove Trap needs 180 just to try and
  is 67% at 200. **The proposal would make this exploit reachable and worse (level 13 to 20).** Cap level at 12 (what
  OSI's 120 power-scroll maximum gives). That changes nothing for Value <= 129.9 and only trims today's 130 tinkers
  from 13 to 12. Item bonuses (D-113) also raise Value above the cap, so the cap protects that path too.
- Files: `C\ClusterFMiningExtension.cs` (also touched by cc-P53), `P\CraftItem-shard-hooks.patch`,
  `C\ClusterFCraftGainWindow.cs`, a new `P\DefTinkering-trap-level-cap.patch` (pinned `DefTinkering.cs:678`), or a
  ResType check in the hook if a C\ route exists (unverified that one does).
- Fidelity: OSI metals are untouched. The cap changes nothing at or below 120.
- Side effects to check (unverified): which tinker products take the ingot's `Resource` and so pick up the extended
  metal's `CraftAttributeInfo` (tool-weapons such as pickaxe and hatchet, cleaver, butcher knife). That would be a second
  route to Celestial-property gear, and a new sink for extended ingots.

### Lumberjacking (b): raise the extended woods' harvest maxSkill (ours, numbers only)

Keep ReqSkill 100 and each MinSkill. Set MaxSkill to max(current, F-28 requirement + 20): Ironwood 140, Ghostwood
142, Emberbark 150, Frostbark 160, Shadowbark 175, Runewood 190, Voidwood 205, Starwood 220
(`C\ClusterFLumberjackingExtension.cs:230-237`). That is continuous from 148: **reaches 200** on Voidwood or Starwood
trees.
- Skipped (a): the axe-combat roll (`BaseWeapon.cs:2532`) has no difficulty: any swing counts. A window to the cap
  there (the way pinned already does Tactics and Anatomy at `:2524, :2527`) would train Lumberjacking by fighting, and
  it is pinned code.
- Cost: one roll decides yield and gain (`HarvestSystem.cs:147`), so a lower success rate also means fewer logs. At
  Value 100 Voidwood drops from 40% to 23%, and Starwood from 40% to 21%. At 148, Voidwood drops from 100% to 59%.
  These are shard-only trees, but players will feel it. Chase should accept that or ask for a gain-only roll, which
  would be a larger change in our extension.
- Fidelity: none below 100. Only extended woods change, and they need Base 100.
- Exploit check, **new break 160-200, and the proposal reaches it:** the axe bonus `GetBonus(LJ.Value, 0.2, 100, 10)`
  (`BaseWeapon.cs:2543-2545`, formula `:2486-2496`) is added outside the 100% damage-increase cap ("No caps apply",
  `:2537-2539`). That is +30% at GM, +39.6% at today's 148, +42% at 160 and +50% at 200. Recommend a cap at the GM
  value (+30%), which changes nothing at or below 100. It needs a pinned patch on `BaseWeapon.cs:2543`. Ship it with
  this batch or before it.

### Alchemy (c): new top recipes (content)

- (a) skipped: potions succeed every time past 140, prisms past 150. Potions are never exceptional, so nothing gets
  harder past 150.
- (b) impossible: Alchemy and Glassblowing have no sub-resources.
- (c) F-20 Alchemy BODs (Arcane Society) do not suffice alone. With no material or exceptional tier, a turn-in window
  can only follow item difficulty, which tops out at 140. Smallest working option: 2-4 new shard recipes with windows
  reaching about 200-210, gated by a min around 150, using scarce inputs. These would go in a new
  `C\Engines\Craft\AlchemyCraftRegistrations.cs` (the existing Registrations pattern). This needs Chase's design (which
  items). Size M.
- Fidelity: none if every min is 150 or more.
- **New break 160-200 if Alchemy passes 150:** EnhancePotions skill part `(int)(Value*10/33)` uncapped (pinned
  `Items\Skill Items\Magical\Potions\BasePotion.cs:210`): +30% at 100, +45% at 150, +60% at 200. Explosion potion
  bonus is Value/5 (`Explosion Potions\BaseExplosionPotion.cs:154`): 20 at 100, 40 at 200. Conflagration reads
  `Alchemy.Fixed` (`Conflagration Potions\BaseConflagrationPotion.cs:237`). Cap the skill part at its 120 value before
  any Alchemy route opens. The InfusedAlchemistsGem `Base += 1` (`:28`) ignores the cap. It has no drop source today,
  but the gem should clamp to Cap.

### Cooking (c): new top recipes (content)

- (a) skipped: GreenTea succeeds every time past 130 and is certain exceptional at 152.6.
- (b) impossible: Cooking has no materials.
- (c) F-20 Cooking BODs (Maritime Brotherhood) have the same limit as Alchemy's: windows top out at 130. Smallest
  working option: new shard recipes reaching 200, in a new `C\Engines\Craft\CookingCraftRegistrations.cs`, with
  Chase's design. Size M.
- Fidelity: none if every min is 150 or more.
- Exploit check: nothing reads Cooking outside crafting (pinned and C\ grep), so 200 breaks nothing.

### Tailoring (c): new top recipes, or shard leathers (content)

- (a) skipped: the cloth chest succeeds every time past 144. Exceptional is certain at 189.1, which is under 200 anyway.
- (b) impossible today: no shard leathers exist (`C\ResourceInfo.cs:29-32`, pinned leathers top at 99). With extended
  leathers, the shared hook would carry Tailoring to 200 exactly as it does woods. That means new hides, skinning
  sources, `CraftAttributeInfo` rows and F-29 numbers: size L.
- (c) The F-18 remainder (tailoring into the guild seal system) inherits leather-tier windows, at most about 99 + 30,
  so it does not reach 200 alone. Smallest: new recipes reaching 200 in the existing
  `C\Engines\Craft\TailoringCraftRegistrations.cs` (size M), or extended leathers (L). Chase's design.
- Fidelity: none if every min is 150 or more.
- Exploit check: nothing reads Tailoring at use time except ArcaneGem charges, which clamp at 120 (P20). No new break.

### Fishing (c): extended deep-water veins (content)

- (a) skipped: Fish 0-100 is the only roll, and it decides yield too. Raising its max lowers every fisher's success
  below 100 (an OSI-visible change), and catching a plain fish has no difficulty past 100.
- (b) impossible: there are no materials.
- (c) Smallest working option: a `C\ClusterFFishingExtension.cs` modeled on
  `ClusterFLumberjackingExtension.ApplyExtendedVeins`. It would add rare-fish HarvestResources (ReqSkill 100, min about
  60-70, max stepping to about 200-220) as low-weight veins with Fish as fallback, so OSI water and yields stay as
  they are. This needs new fish items, so it is a design question (Maritime Brotherhood, F-9/F-20). Size M-L.
- Fidelity: none below 100 (ReqSkill 100 and fallback to Fish).
- **New break 160-200 if Fishing passes 100:** each deep-water rare is `(Value-80)/4000` (`Fishing.cs:15-18`, roll
  `:183`). That is 0.5% each at 100, 2% at 160 and 3% at 200: about 11.5% of deep-water casts give a net, big fish,
  map or bottle at 200, versus about 2% at 100, and each net, map or bottle comes with its serpent spawn. Cap the
  Value used there at its 120 reading before any route opens.

### No proposal: Blacksmithy and Mining (both reach 200)

- Blacksmithy: the gain route to 200 is P53's commission table. BOD route works but is rare. Exploit list: none
  involve Blacksmithy. Note the edge at the top: Celestial commissions offered at Base 200 (exc 200-230) can never
  gain, which is fine because 200 is the cap.
- Mining: the gain route is sand (70-400). **D42 is not live**: the ingot return is clamped to `cost - 1`
  (`C\SmithGuildSalvageBag.cs:128-129`), and `D:\UO\shard-migration\docs\bug-list.md:252` records it fixed by cc-P23
  (`70f01e3`), client-verified 2026-10-02 (24 of 25 at Mining 150). Salvage resmelt difficulty is 112.5-200
  (`:55-69`), with no gain roll. Between 160 and 200 nothing new reads Mining: gems are a fixed Base 100 threshold,
  salvage returns `cost - 1` from about 143, and treasure dig range clamps. Leftover design gap (P20, still live):
  extended ores smelt at default difficulty 50 (`Ore.cs:177`), so any Mining of 25 or more smelts Celestial ore. No
  proposal here touches Mining; Tinkering (b) only adds a sink for extended ingots.

### Fidelity summary

No proposal changes anything for an OSI player at or below 100. Only shard materials or shard trees with ReqSkill 100
or more move. The two caps (trap level 12, axe bonus at its GM value) change nothing at or below 120 and 100.
Nothing changes gain below 100.

### Exploit summary (cc-P20 rank 4)

| Exploit | Touched by a proposal here? |
|---|---|
| Hiding in combat 118, Stealing never caught 150, bard certain ~150, guards cannot reveal 121 | No (other skills) |
| Tinkering trap damage uncapped from 120 | **Yes: Tinkering (b) makes it reachable to level 20 (200-600 fire).** Ship the level-12 cap with it |
| D42 salvage dupe from Mining 143 | Dead (clamped, fixed cc-P23). No Mining proposal |
| New 160-200: LJ axe damage | **Yes: LJ (b) reaches +50%.** Cap at +30% |
| New 160-200: Alchemy EP, fishing rares | Only if their (c) content ships. Cap first |
| Exceptional past certain | Harmless: clamped, and success and exceptional ignore the hook |

## (iii) P20 file:lines that moved (P20 was on pinned 7c9215d97; now d4531cd94 and the current shard)

| P20 cite | Now | Status |
|---|---|---|
| pinned CraftItem.cs:875 (gain), :886 (chance), :794 (exc), :616 (material gate) | `:893`, `:904`, `:812`, `:630` | moved |
| ours `C\CraftItem.cs` :893-896, :906, :629 | file removed; replaced by `P\CraftItem-shard-hooks.patch` (no math change) | gone |
| DefAlchemy.cs:194-199 (DeadlyPoison) | `:199-204` | moved |
| DefBlacksmithy.cs:251-257, DefBowFletching.cs:123/128, DefCarpentry.cs:322, DefCooking.cs:143, DefTailoring.cs:651, :662-665, DefTinkering.cs:363, DefGlassblowing.cs:123, :38, DefMasonry.cs:107-110 | same | confirmed |
| `C\...\TailoringCraftRegistrations.cs:91-98` | rows `:92-99` (144 at `:93`, `:97`) | moved by 1 |
| `C\...\BlacksmithyCraftRegistrations.cs:91-125`, `CarpentryCraftRegistrations.cs:57`, `TinkeringCraftRegistrations.cs:79-107` | same | confirmed |
| HarvestSystem.cs:142-147, :209-211, :332-351 | `:147`, `:211`, `:332-351` | confirmed |
| `P\Mining.cs` :113-188, sand :252-255, :334-336 | `:113-188`, `:254`, `:334-336` | confirmed |
| `C\ClusterFMiningExtension.cs:84-94` (ore), `:93` (Celestial 155), `:174-181` (sub-res) | `:98-105`, `:105`, `:173-180` | moved |
| Ore.cs:176-205, :189-190 | table `:167-178`, window `:180-181`, gate `:183`, roll `:197` | moved |
| Lumberjacking.cs:71-77 | same | confirmed |
| `C\ClusterFLumberjackingExtension.cs:219-229` (`:228`), `:274-281`, `:302-309` | `:230-237` (`:237`), `:294-301`, `:322-329` | moved |
| BaseWeapon.cs:2545-2549 (LJ roll), :2559-2561 (axe bonus), :2599-2602 | `:2529-2533`, `:2543-2545`, `:2602-2606` | moved |
| `C\ClusterFSmithBODSystem.cs:240, :426`, ranges `:351-391`, large roll `:95` | roll `:281`, ranges `:400-441`, large roll `:105` | moved |
| `C\ClusterFSmithCommissions.cs:616, :687`, ranges `:772-800`, material `:429-445`, exc `:463, :511` | `:729`, `:658`, `:825-850`, `:459-484`, `:504`, `:551` | moved |
| Repair.cs:41-75, :183-203 | same (`:203` golem) | confirmed |
| DefTinkering.cs:663-668 (trap level) | `:678-682` | moved |
| TrappableContainer.ExecuteTrap.cs:63-72, :104-106 | `:65`, `:107` | moved |
| RemoveTrap.cs:61, :96-97 | same | confirmed |
| BasePotion.cs:207-218 (:210) | `:208-219` (`:210`) | confirmed |
| BaseExplosionPotion.cs:151-155 | `:154` | confirmed |
| BaseConflagrationPotion.cs:237 | same | confirmed |
| Fishing.cs:15-18, :19-30, :100, :181-185 | same | confirmed |
| `C\SmithGuildSalvageBag.cs:145-148` (unclamped) | `:128-129`, clamped to cost - 1 | moved and fixed |
| `C\...\InfusedAlchemistsGem.cs:28` | same | confirmed |
| `C\Meditation.cs` ~:92 (brief) | `:115` | moved |

## (iv) Batch sizing

| Batch | Skills | Size | Files | Overlaps |
|---|---|---|---|---|
| A: material-shifted gain window + F-28 wood re-gate | Carpentry, Fletching | S-M | `P\CraftItem-shard-hooks.patch` (pinned `CraftItem.cs:891-894`), new `C\ClusterFCraftGainWindow.cs`, `C\ClusterFLumberjackingExtension.cs:294-301, :322-329` | **F-28** (the re-gate is F-28 Q3; ship together or after), F-29 (reads materials, separate code). cc-P53 did not touch these lines |
| B: Tinkering metals + trap cap | Tinkering | S-M | `C\ClusterFMiningExtension.cs` (**cc-P53 touched it**, `:173-180` block and a comment), new `P\DefTinkering-trap-level-cap.patch`, hook from A | F-20 (Tinker BODs later reuse the metals), F-29 (extended-metal tinker items get x1.5 if exceptional) |
| C: LJ wood maxSkill + axe bonus cap | Lumberjacking | S | `C\ClusterFLumberjackingExtension.cs:230-237`, new `P\BaseWeapon-lumberjack-bonus-cap.patch` (`BaseWeapon.cs:2543-2545`; `P\BaseWeapon-talisman-durability.patch` already patches this file, so check context) | F-28 numbers (keep the ladder in one table) |
| D: content | Alchemy, Cooking, Tailoring, Fishing | M each (Tailoring L with leathers) | new `C\Engines\Craft\AlchemyCraftRegistrations.cs` / `CookingCraftRegistrations.cs`, existing `TailoringCraftRegistrations.cs`, new `C\ClusterFFishingExtension.cs`; caps first: `BasePotion.cs:210`, `Fishing.cs:183`, gem `:28` | F-18 remainder (Tailoring), F-20 (Alchemy/Cooking/Tinker BODs), F-9 (Maritime) |

Facts a builder needs:
- `GetSuccessChance` is called with `gainSkills` true only from `CheckSkills`; the gain loop and the chance share
  `minSkill`/`maxSkill` locals, so use new locals for the shifted roll.
- Test that the recipe consumes the ResType: `typeRes` is the selected material even for recipes that do not use it
  (`CraftItem.cs:620-628`).
- `CraftSubResCol.SearchFor(typeRes)` gives `RequiredSkill`. Carpentry's ResType is Log (`DefCarpentry.cs:597`), and
  our Carpentry sub-resources are Board types, matched through the type pairs the CraftItem patch adds.
- Harvest uses Value against MaxSkill, and its gate uses Base.
- Every window stops at Base = max - (Value - Base) under D-113.
- Red-then-green facts to write: an iron/OSI-material craft rolls the item's own window; a Voidwood Tetsubo rolls
  165-225.3; a Starwood Board rolls nothing; a 130 Tinker's trap is level 12; a 200 lumberjack's axe bonus is 30%.

Unverified: the Ilshenar Glassblower spawn is live on the shard (the sand route depends on it); which Tinkering
products carry the extended metal's properties; any Tinkering or Lumberjacking skill bonus items that would raise
Value past the caps; Magic Untrap against trap power 108-180.
