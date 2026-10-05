# cc-P53: the 200 skill cap pass

Builder task, 2026-10-05. Brief: `D:\UO\cc-prompts\cc-P53-two-hundred-cap.md`. Engine authority: `D:\UO\ModernUO-pinned`
at `d4531cd94b739613155225c234900de9f47d2c88` (`git rev-parse HEAD`); every pinned file:line below is against it.
`C\` = `D:\ShatteredLegacy\server\customizations`, `P\` = `server\patches`, `T\` = `server\tests`.

## Headlines

1. **All six parts done. Final build `docker\uo\build.sh -t sl-modernuo:cc-p53`: 44/44 patches (42 plus 2 new),
   686/686 shard facts (671 plus 15 new), image `sl-modernuo:cc-p53` = `a1158037d0d0`.** Shard-Console facts
   **95/95** (Part F; was 94/95 at HEAD). `sl-modernuo:latest` not moved, nothing deployed, no shard restarted, nothing
   committed by me.
2. **Your commit script committed this work mid-task.** `a8cf0e5` ("Shard work, 2026-10-05 06:03") holds P53 as it stood
   at build 3: it compiles, but two of my new facts were still wrong in it (684/686). The working tree on top of it is
   the green state: four files (`T\Misc\TwoHundredCapVerification.cs`, `T\Engines\Craft\CraftCategoryPagingVerification.cs`,
   a comment in `C\ClusterFMiningExtension.cs`, and one comment dash made ASCII in `C\Meditation.cs:69`, the only
   change after the final build). Commit those with this note.
3. **Part A: no config line for you to change.** Both config files hold `clusterf.skillCaps.individualCap: "300"`, written
   by the old code default. The code now defaults to 200 and rewrites a stored value of exactly 300 to 200 once, then
   records `clusterf.skillCaps.rescaledTo200: True` so it never runs again. A value you set by hand (anything but 300,
   or anything after that first boot) is never touched. **No player can lose skill:** pinned's Cap setter never touches
   Base. New total cap: 58 x 200 = **11,600** (was 17,400).
4. **Part B: one table, `C\ClusterFMetalTiers.cs`, now feeds every post-Valorite number.** Before, six places each had
   their own copy of a 300-era table, and two of those copies did not match the craft requirement they gated. Full
   before/after table below. **The brief's `ClusterFSmithBODSystem.cs:99` (`/ 300.0`) is stock OSI and is left alone:**
   pinned has the same line in `Blacksmith.cs:96`, `Weaponsmith.cs:68`, `Tailor.cs:44` and `Weaver.cs:50`.
5. **Part C: one hook covers every source.** `PlayerMobile.AddSkillMod` (a new override, `P\PlayerMobile-skill-bonus-above-cap.patch`)
   clears `ObeyCap` on every mod a player gets. Counted: 27 SkillMod constructions in all (pinned 20, ours 7). Only 3 set
   ObeyCap (item `Skill +X`, and Animal Form's Stealth and Stealing bonuses); everything else, ours included, already went
   above the cap. Skill gain is unchanged: it reads Base, never Value.
6. **Part E: the panel holds 10 categories; blacksmithy has 12 and inscription 11.** Both drew over NOTICES; the craft gump
   now pages categories past ten, nine to a page. Inscription's overflow was not in the brief: its groups are computed
   (spell circles), so a grep of `AddCraft` arguments counts 1; the fact measured 11. Every other system has 10 or fewer.
7. **For Chase, decisions:** (a) the skill achievements keyed to 250 and 300 are now unreachable. I left them alone; the
   options are in Part B. (b) Armored meditation moved from Meditation 200 to 150. That is my scaling choice, not an
   approved number; say if you want another.
8. **Found, not mine:** the Mining extension's doc comment had both message clilocs wrong. 1044036 is "Ingots" (the
   generic name), and the refusal is 1044268, "You cannot work this strange and unusual metal." I fixed the comment.

## Part A: the per-skill cap is 200 (D64)

**Cause.** `C\ClusterFSkillCaps.cs:10` defaulted to 300, and `Configure` read it through
`ServerConfiguration.GetOrUpdateSetting`. That call stores a missing key once and returns the stored value from then on
(pinned `Server\Configuration\ServerConfiguration.cs:186-200`). Both files hold "300" (`Configuration\modernuo.json:105`,
`Configuration-test\modernuo.json:110`), so changing only the code default would have changed nothing on either shard.

**Choice: migrate the stored value, once, and only if it is the old default.** The 300 in both files was not chosen by
you; the code wrote it. Telling you to hand-edit two files repeats D-numbers this project has paid for (a config value
nobody remembers changing). The migration (`ClusterFSkillCaps.RescaleStoredLegacyCap`, `:88-112`):
- runs once per config file, then sets the marker `clusterf.skillCaps.rescaledTo200 = True`;
- rewrites only a stored value of exactly 300, and logs one line ("was the old default 300; now 200 (cc-P53)");
- leaves any other value alone, and leaves even 300 alone if it is set again after the marker.
`SetSetting` saves the file itself (pinned `ServerConfiguration.cs:213-217`, `Save` at `:328`), so this happens at the
first boot of the new image. No config file was edited by hand.

**Characters already above 200 (staff test characters at 300).** Pinned `Skill.CapFixedPoint` sets the cap and nothing
else (`Server\Skills.cs:205-219`). Base is untouched, and `Value` starts from Base with no clamp on Base itself
(`:250-331`). So a 300 character keeps Base 300 and Value 300; **no skill is lost.** It cannot gain: `SkillCheck.Gain` needs
`Base < Cap` (`UOContent\Skills\SkillCheck.cs:248`), and the gain is capped at `CapFixedPoint` (`:280`). Two side effects,
both stock behaviour for anyone over the total cap: a character whose Base total exceeds 11,600 gains nothing in any
skill until the total drops (`:278`), and each gain attempt lowers a skill the player locked Down (`:259-270`). No other
code in pinned clamps Base to Cap (searched for every `Base > Cap` / `Cap < Base` / `Base = Cap` form). Players: unverified
whether any live player has a skill above 200. The live shard is down and saves were not read; by the F-12 counts only
the six weapon skills, Focus, Parry and Mining can gain past about 160. Acceptable: nothing is taken away.

**Total cap:** rule unchanged (`TotalSkillCap = skills x individual`, `:126-127`): 58 x 200 = 11,600. The Staff Hub reads
it at runtime (`C\StaffHub\ClusterFStaffHub.cs:394`), so it will show "of 11600".

**Facts** (`T\Misc\TwoHundredCapVerification.cs`): A1 the default is 200; a stored 300 is rewritten once and the marker
stops a second run; a hand-set 250 is kept; applied, every skill's cap is 200 and the total is 11,600. A2: a character
at 300 keeps Base and Value 300 when the cap drops to 200, and does not gain. A2 tests pinned's behaviour, not our change,
so it passes in the red tree too. That is expected.

## Part B: metal tiers to 200 and every 300-era number (D64)

**Search.** I grepped all 808 `.cs` files in `C\` for 300/275/250/225/17400/500.0, every decimal from 200 to 500,
`Skills.*.Base/Value` comparisons, `CheckSkill`, `AddSubRes`, `HarvestResource`, `minSkill`, `Cap` and `PowerScroll`, and
did the same in `P\`. Each hit was read. Results:

| Where | What | Before | After |
|---|---|---|---|
| `C\ClusterFSkillCaps.cs:11` | individual cap | 300 | 200 (Part A) |
| `C\ClusterFMiningExtension.cs:173-180` | Blacksmithy requirement, Pt / Tox / Bl / Fr / Ob / My / Ad / Ce | 100 / 125 / 150 / 175 / 200 / 225 / 250 / 300 | **112.5 / 125 / 137.5 / 150 / 162.5 / 175 / 187.5 / 200** (Chase-approved; from `ClusterFMetalTiers`) |
| `C\ClusterFSmithCommissions.cs:476-484` | commission offer brackets (metal offered when skill below) | Val <105, Pt <115, Tox <130, Bl <150, Fr <175, Ob <200, My <250, Ad <300, Ce above | Val <112.5, Pt <125, Tox <137.5, Bl <150, Fr <162.5, Ob <175, My <187.5, Ad <200, Ce at 200: each bracket opens at its metal's requirement |
| `C\ClusterFSmithCommissions.cs:841-844` | commission skill-gain range | Pt 95-125, Tox 105-135, Bl 120-155, Fr 140-175, Ob 165-200, My 190-225, Ad 240-275, Ce 290-325 | requirement -10 to +20: Pt 102.5-132.5, Tox 115-145, Bl 127.5-157.5, Fr 140-170, Ob 152.5-182.5, My 165-195, Ad 177.5-207.5, Ce 190-220 (exceptional +10 both ends, as before) |
| `C\ClusterFSmithBODSystem.cs:422-425` | BOD turn-in skill-gain range | Pt 85-115, Tox 95-130, Bl 110-150, Fr 130-175, Ob 155-205, My 180-235, Ad 230-285, Ce 280-340 | requirement -20 to +20: Pt 92.5-132.5, Tox 105-145, Bl 117.5-157.5, Fr 130-170, Ob 142.5-182.5, My 155-195, Ad 167.5-207.5, Ce 180-220 |
| `C\SmithGuildSalvageBag.cs:65-69` | salvage resmelt difficulty (Mining) | 105 / 115 / 130 / 150 / 175 / 200 / 250 / 300 | the requirement: 112.5 .. 200 |
| `P\SmallSmithBOD-PostValorite.patch:32`, comments `:10-17` | small BOD post-Valorite material gate | 105 / 115 / 130 / 150 / 175 / 200 / 250 / 300 | the requirement |
| `P\LargeSmithBOD.cs:124-125` | large BOD post-Valorite material gate | same as small | the requirement |
| `C\Meditation.cs:13, :75`, `C\RegenRates.cs:161` | armored meditation (armor no longer blocks; reduced regen) | Meditation > 200 | > **150** (`Meditation.ArmoredMeditationSkill`) |
| `C\TestCenter\TestCenterKit.cs:142`, `T\Misc\TestCenterVerification.cs:225-242` | comment, and the fact's "our caps" | 300 | 200 |

Why each changed. The commission and BOD offers, and the BOD gates, are there so a smith is only asked for metal they can
work. Raising Platinum to 112.5 made the old brackets offer Platinum at 105-112.4, which the smith cannot work; on the
old tables Toxic was already offered at 115 against a requirement of 125, and Mythril at 200 against 225. All three now
open at the requirement. The skill-gain ranges matter because `CheckSkill(min, max)` never gains below min, so Adamantium
and Celestial orders (min 230-290) could never train anyone at 200. The salvage difficulty put Adamantium and Celestial
out of reach at 200. Armored meditation tested `> 200`, which can never pass at a cap of 200. Mapping the old 300 range
linearly onto the new one (100..300 to 100..200) puts it at 150. I kept the commission and BOD range shapes
(commission requirement -10/+20; BOD min requirement -20, max now +20 throughout where it used to widen). The
commissions table may be reworked in another chat: the only things I changed there are the two tables above, both forced.

**Checked and left (not tuned to 300):** mining ore harvest (`C\ClusterFMiningExtension.cs:98-105`, required 100 and max
155), wood harvest (`C\ClusterFLumberjackingExtension.cs:230-237`, max 148), carpentry and fletching extended woods (all
100.0, `:294-301`, `:322-329`), satchel smelting (`C\ReinforcedOreSatchel.cs:53-72`, all 100), the large-BOD roll (`/ 300.0`,
stock, see headline 4), commission exceptional chance (`(skill-40)/100`), every work-order `minSkill` (0-100, 118 values in
`C\ClusterFWorkOrderSystem.cs`), imbuing difficulty (peaks 120), guild task minimums (0-50), the hammer and pickaxe
upgrade requirements (75-100), `SmithSealScrollCensus.CatalogScrollMinimum` 305 (identifies old catalog scrolls, still
right), and the Survey Archivist and Seal catalog 250/300 values (Standing, Vouchers, Seal prices, not skill). Tailoring
leathers, alchemy, inscription, cooking and fishing have no customization above 100. The Seal reward multipliers
(`C\ClusterFSmithBODSystem.cs:320-330`) are unchanged, per your 2026-10-04 decision.

**Left for you: the skill achievements.** `C\ClusterFAchievements.cs:945-950, :976-1013` and their text at
`:218-245, :398-416, :445-509` are keyed to a 300 cap: Paragon 250, Grandmaster 300, Triple Grandmaster (3 skills at 300),
and Mining, Smith and Magery Legend (300). At 200 those six are unreachable. I did not rescale them. A rescale either puts
two achievements on the same number (Legend 300 to 200 is where Elite already is; Triple Grandmaster lands on Triple
Master), or remaps the whole ladder. A remap rewrites the reward thresholds and the text ("150. The old standard GM cap
was 100...") and hands players already between thresholds AP and renown they had not earned. That is a design call, not
a forced number. Options: **(1)** map the whole ladder linearly (above 100: 150 to 125, 200 to 150, 250 to 175, 300 to 200)
and rewrite the numbers in the text; **(2)** retire the six (leave them registered, unreachable, or hide them); **(3)** leave
them until F-12 brings back caps above 200. My recommendation is (3): F-12's level ladder is the real cap system, and
it is not built yet.

**Facts** (`T\Misc\TwoHundredCapVerification.cs`): B1 each metal's requirement in the live craft menu is the approved
step; B2 (two cases) a 200 smith can work Celestial and a 187.4 smith cannot, through pinned's own `CraftItem.ConsumeRes`
(refused with the sub-resource's own message 1044268), and can still work Mythril; B3 every rescaled table above
(commission and BOD ranges, salvage difficulty, armored meditation); B4 commissions offer only metal the smith can
work, and offer Celestial at 200 (400 draws at each of ten skills, including both sides of 112.5 and 187.5).

## Part C: item and temporary bonuses above the cap (deviation D-113)

**Stats already do.** `StatCap` is only ever compared against raw stats: pinned `SkillCheck.cs:357, :374, :501`,
`StatCapScroll.cs:99-123`, `RewardSystem.cs:592`, `TestCenter.cs:96-140`. Mods and items are never limited by it. The
shard's per-stat limit is a different thing: `P\PlayerMobile-individual-stat-cap.patch` swaps pinned's ML clamp of 150 on
effective Str/Dex/Int (`PlayerMobile.cs:583-623`) for `ClusterFStatCaps.IndividualStatCap`, default 500. That one does
clamp effective stats, items included. F-12 (2026-10-02) plans to drop it. I left it alone: the brief's claim that stats
already go above the cap is true of `StatCap`, and true of the 500 limit up to 500.

**Every SkillMod source (counted).** 27 constructions: pinned 20, customizations 7, patches 0. `EquippedSkillMod`: 0.
`ObeyCap` defaults to false; no constructor sets it (pinned `Server\Mobiles\Mods\SkillMod.cs:24-58`).

| Source | File:line | ObeyCap before | Kind | Now |
|---|---|---|---|---|
| Item "Skill +X" (`AosSkillBonuses.AddTo`): all equipment, talismans (`BaseTalisman.cs:344, :628`), our set bonuses (`C\...\Sets\SetItem.cs:304`), the Jacob pickaxes (`P\JacobsPickaxe.cs:39` and the four upgrades) | `Misc\AOS.cs:1357-1358` | **true** | item | above cap |
| Animal Form Stealth +20 | `Spells\Ninjitsu\AnimalForm.cs:237` | **true** | temporary | above cap |
| Animal Form Stealing +10 | `AnimalForm.cs:245` | **true** | temporary | above cap |
| Gloves of Mining | `GlovesOfMining.cs:133, :151, :179` | false | item | unchanged (already above) |
| Ancient Smithy Hammer | `AncientSmithyHammer.cs:41, :62, :90` | false | item | unchanged |
| Weapon accuracy | `BaseWeapon.cs:306, :1078, :3558` | false | item | unchanged |
| Mage Weapon (Magery penalty) | `BaseWeapon.cs:1086, :3565` | false | item penalty | unchanged |
| Protection, Evil Omen (absolute), Honorable Execution, faction skill loss, Discordance, Satyr (timed) | `Protection.cs:141`, `EvilOmen.cs:57`, `HonorableExecution.cs:69`, `Faction.cs:1380`, `Discordance.cs:239`, `Satyr.cs:113` | false | temporary penalty | unchanged |
| Hammer of Hephaestus T1 +5, T2 +10, familiarity +2.5 | `C\HammerOfHephaestus.cs:254, :634, :685` | false | item | unchanged |
| Outrider crooks (+5/+10/+15) | `C\OutridersCrook.cs:82, :83, :85` | false | item | unchanged |
| Pet Mimic | `C\PetMimic.cs:1059` | false | item | unchanged |

Not SkillMods: the Human racial bonus is a floor of 20, not an addition, and ignores the cap (`PlayerMobile.cs:261-272`,
`Skills.cs:238-243`). Elves and gargoyles have no skill bonus. Under AOS the stat offset is zeroed
(`AOS.DisableStatInfluences`). Scrolls of Transcendence and our Infused Alchemist's Gem raise Base itself, which is not a
bonus layer. No potions build a SkillMod in either tree.

**Change, one hook.** Pinned `Mobile.AddSkillMod` is virtual (`Server\Mobiles\Mobile.cs:3500`) and PlayerMobile does not
override it. `P\PlayerMobile-skill-bonus-above-cap.patch` adds the override (8 lines after `RacialSkillBonus`, pinned
`PlayerMobile.cs:271`), which calls `C\ClusterFSkillBonusAboveCap.Admit(mod)` to clear `ObeyCap` and then calls the base.
It covers the three cap-obeying sources above, and any added later. Players only; creatures keep pinned's behaviour. Off
switch: `clusterf.skillCaps.bonusAboveCap` (default True).

Alternatives argued before patching:
- Patch `Skills.cs` to ignore ObeyCap. Rejected: it is a core project, it changes every mobile, and it changes what the
  flag means.
- Patch the 3 sites in `AOS.cs` and `AnimalForm.cs`. Rejected: two files, and the next source added upstream would clamp
  silently.
- Customizations only. Rejected: no event fires on AddSkillMod, so the only way would be to poll equip events.

**Gain is unchanged, shown:** `SkillCheck.Gain` gates on `skill.Base < skill.Cap` and clamps at `CapFixedPoint`
(`SkillCheck.cs:248, :280`). `ClusterFSkillGain.ShouldBoost` gates on Base too (`C\ClusterFSkillGain.cs:141-147`). The
success roll uses Value (`SkillCheck.cs:58, :180`), so a bonus makes success likelier, as stock. Material requirements
read Base (`CraftItem.cs:625`; the craft gump's picker, `CraftGump.cs:571, :589`), so a +15 item does not unlock a higher
metal. One knock-on: armored meditation reads Value, so a 140 meditator with a +15 item now qualifies (see Part B).

**Facts** (`T\Misc\SkillBonusAboveCapVerification.cs`): C1 a +15 Blacksmithy ring on a capped 200 skill reads 215, and
200 again once it is in the pack; C2 Animal Form's exact construction (Stealth +20, ObeyCap set) reads 220 and 200 after
removal, and a timed +10 likewise; C3 50 gain attempts at the cap with the ring worn leave Base at 200, and from 199.9 a
gain stops at 200 with Value 215; C4 with the switch off, pinned's clamp returns (200 at Base 200 and at Base 190). C4 is
the control, so it passes in the red tree too.

**Register line for you (D-113):**

| D-113 | **Ours (cc-P53 C, Chase 2026-10-04).** Item skill bonuses ("Skill +X" on equipment, talismans, set bonuses) and temporary skill effects count above the skill's cap: a +15 item on a capped skill reads cap + 15. Skill gain still stops at the cap, and material requirements still read the unmodified skill. OSI clamps item and Animal Form bonuses at the cap | gear matters at the cap | `visible` | `cc-P53` C |

## Part D: stock material names in Title Case (D62, deviation D-114)

**Cause.** Pinned names its stock sub-resources by cliloc. Those clilocs are upper case and carry the amount
("IRON (~1_AMT~)", 1044022). Ours are strings. Texts were read from the client's `Cliloc.enu` (ClassicUO copy; the
shard's `client-data` copy is in the newer compressed format and was not decoded).

**Change.** `C\Engines\Craft\CraftMaterialNames.cs` runs at ServerStarted, after every `Def*.Initialize`. It replaces each
stock entry in place with the same sub-resource under a string name: same type, required skill, generic name and message,
at the same index. `CraftSubRes.Name` has no setter, but `CraftSubResCol` is a `List`, so no pinned file or client cliloc
is edited. The gump then draws "Iron (12)" in the list and "Iron (12 Available)" on the selected-material line, the same
as "Platinum" has always drawn (`CraftGump.cs:155, :288`). Nothing else in pinned reads these names (searched every
`CraftSubRes` consumer, including the T2A menus); everything uses `ItemType`.

| System | Changed (list name, then entries) |
|---|---|
| Blacksmithy | Iron; Iron, Dull Copper, Shadow Iron, Copper, Bronze, Gold, Agapite, Verite, Valorite |
| Blacksmithy scales | Red Scales; Red, Yellow, Black, Green, White, Blue Scales |
| Tinkering | Iron; the same nine metals |
| Carpentry | Wood; Wood, Oak, Ash, Yew, Heartwood, Bloodwood, Frostwood |
| Bowcraft/Fletching | Wood; the same seven |
| Tailoring | Leather/Hides; Leather/Hides, Spined Hides, Horned Hides, Barbed Hides |
| Masonry | Normal; Normal, then the eight metal granites (Dull Copper .. Valorite) |
| Alchemy, Inscription, Cooking, Cartography, Glassblowing | none (no sub-resources) |

Not changed: types, required skills, refusal messages, what any craft makes or consumes.

**Facts** (`T\Engines\Craft\CraftCategoryPagingVerification.cs`): D1 every system's list name and every entry above is the
exact Title Case string, with no cliloc, its type and required skill unchanged, and ours still last; D2 the material
picker and the main gump draw none of the 27 clilocs, and show "Dull Copper (50)" and "Iron (0)", then
"Dull Copper (50 Available)" and "Red Scales (0 Available)"; picking Dull Copper sets the index whose type is
`DullCopperIngot`, and a real `ConsumeRes` with it consumes Dull Copper ingots.

**Register line for you (D-114):**

| D-114 | **Ours (cc-P53 D, Chase 2026-10-04).** Craft menu material names read in Title Case ("Iron", "Dull Copper", "Red Scales", "Leather/Hides") instead of the client's upper-case labels ("IRON", "DULL COPPER"), so they match the shard's own metals and woods. Cosmetic; what each material does is unchanged | consistent craft menus | `visible` | `cc-P53` D |

## Part E: the category list overflowing into NOTICES (D63)

**Cause.** Pinned `CraftGump.CreateGroupList` (`Engines\Craft\Core\CraftGump.cs:398-420`) draws LAST TEN at y 60 and each
group at `80 + i * 20`, with no paging. The categories panel is the tile at y 37, 250 tall (`:51`), so it ends at 287;
NOTICES begins at 292 (`:48`, label `:66` at 302). Under LAST TEN it holds ten group rows (the last at y 260, its button
ending at 282). An eleventh row's button runs to 302, over the notices box, and a twelfth row's label sits at 303, on the
NOTICES label. ServUO's `CraftGump.CreateGroupList` (`Scripts\Services\Craft\Core\CraftGump.cs:446-466`) is identical,
so this is a defect in both. The brief's "about 12" is ten groups plus LAST TEN.

**Counts** (measured by the fact, printed to the build log as `[P53 categories]`, final build): Alchemy 9, **Blacksmithy
12 (2 pages)**, Bowcraft/Fletching 3, Carpentry 10, Cartography 1, Cooking 5, Glassblowing 1, **Inscription 11 (2 pages)**,
Masonry 3, Tailoring 10, Tinkering 9. Carpentry and Tailoring sit exactly at the limit and draw as pinned. Blacksmithy is
pinned's 11 plus ServUO's Miscellaneous (1011173, kept by `C\Engines\Craft\BlacksmithyCraftRegistrations.cs`). Pinned's
own 11 already pushed "Throwing" onto the notices box border.

**Choice: page the list.** `P\CraftGump-category-pages.patch`:
- Ten groups or fewer draw exactly as pinned.
- Past ten, nine show per page, and the tenth row holds a previous arrow (4014, x 15), "Page x of y", and a next arrow
  (4005, x 175).
- The page shown is the one holding the selected group, unless a paging button asked for another.
- Paging re-sends the gump, through a new optional constructor argument; every existing call compiles unchanged. It does
  not use client pages, because the item list already uses those, and the category list is drawn on page 0.
- The arrows are buttons (6, 9) and (6, 10), indexes the misc switch did not use.

Rejected: a tighter row pitch (buttons are 22 tall at a 20 pitch already, so they would overlap and mis-click); folding a
category (it moves ServUO content, and pinned's own list alone is 11); a second column (the panel is 200 wide).

**Facts** (same file): E1 for all 11 systems, on every category page and with every group (and LAST TEN) selected, no
button, label or HTML in the category column reaches below y 287, the selected group is on the page shown, and every
group can be clicked on some page; E2 blacksmithy needs more than one page, page 1 draws next and not previous, pressing
next sends page 2 with the tenth group first, a previous arrow and "Page 2 of 2", and paging selects nothing.

## Part F: Shard-Console red-list fact (P52 headline 7)

**Cause, two commands.**
- `[ClusterFDespiseStockCleanup` (cc-P42 J) declares `Rerun = DeletesAgain` and a summary starting "DELETES"
  (`C\ClusterFDespiseStockSpawns.cs:77`). Its plain run deletes, so by the fact's rule it is red. Its dry-run row is not
  red. **The list was out of date: added to it.**
- `[SL` (cc-P51) is a dev tool (`[ShardCommand(CommandCategory.DevTool, ...)]`, `C\StaffHub\ClusterFStaffHub.cs:45`). It
  showed as red only because the console could not read its registration. `CommandSystem.Register(CommandName, Access,
  SL_OnCommand)` passes its access level as a constant, and the console's reader accepted only a literal
  `AccessLevel.X`, so it filed the command as unclassified. **Fixed the reader, not the list.**
  `scripts\Shard-Console.ps1:1493` now also accepts an identifier there, and `:1517-1524` resolves
  `const AccessLevel X = AccessLevel.Y` in the same file, the way it already resolved a constant name. If it cannot, it
  says so as a problem and never drops the command. `[SL` now reads `GameMaster`, `dev-tool`, `Any`, with no problems,
  and leaves the world tab, as dev tools always have.

**Change:** the fact's expected list gains `[ClusterFDespiseStockCleanup` (`scripts\tests\Shard-Console.Tests.ps1:740`).
**Red, then green:** red at HEAD (94/95, the P52 finding); 95/95 after. The ASCII/no-BOM fact passes over both files.

## Facts, red then green

The red tree (`D:\UO\cc-p53-work\make-red.py`, built with `build.sh -t sl-modernuo:cc-p53-red --tests-only`, log
`D:\UO\cc-p53-work\red.log`) copies the final tree and undoes each behaviour while keeping every API the facts call.
Thirteen edits:
- the default cap back to 300, and the stored-300 rewrite turned off;
- the seven changed tiers back to 100 / 150 / 175 / 200 / 225 / 250 / 300 (Toxic was 125 both before and after);
- armored meditation back to 200;
- `Admit` a no-op;
- `CraftMaterialNames.Apply` renaming nothing;
- `GroupRowsWithoutPaging` set to 100.

Result: 44/44 patches, **686 tests, 13 failed, 673 passed**. Every new fact failed except the two that cannot fail there
by design: A2 (pinned's Base-above-Cap behaviour) and C4 (the off-switch control).

| Fact | Red reason seen |
|---|---|
| A1 TheDefaultCapIs200... | expected 200, got 300 |
| B1 EachMetalsRequiredSkill... | expected 112.5, got 100 ("Platinum: 100") |
| B2 (200, Celestial) | `ConsumeRes` false: Celestial needs 300 |
| B2 (187.4, Mythril) | Mythril needs 225 |
| B3 EveryRescaledTable... | commission range expected (102.5, 132.5), got (90, 120) |
| B4 CommissionsOffer... | Celestial not offered at 200 (offered: Obsidian, Frost) |
| C1 APlusFifteenItem... | expected 215, got 200 |
| C2 ATemporaryEffect... | expected 220, got 200 |
| C3 SkillGainAtTheCap... | expected Value 215, got 200 |
| D1 EverySystemsMaterial... | expected Number 0, got 1044022 |
| D2 TheGumpDrawsNoMaterial... | layout contains " 1044022 " on the selected-material line |
| E1 NoCategoryRow... | "Blacksmithy (selected -1, page 0): button at y 280 reaches 302, past 287" (12 categories, 1 page) |
| E2 ThePagingButtons... | "blacksmithy needs more than one page" |

## Builds

| Build | Command | Result |
|---|---|---|
| 1 | `build.sh -t sl-modernuo:cc-p53` | 44/44 patches; CS0407, the ServerStarted handler returned int (fixed: `() => Apply()`) |
| 2 | same | two compile errors in my new test (namespace of `ClusterFLumberjackingExtension`; `NetStateGumps` is not LINQ-able, used `Find<T>`) |
| 3 | same | 686 tests, 2 failed, both my facts' expectations: the refusal message is 1044268, not 1044036, and `Base = 187.4` truncates to 187.3 (fact now sets `BaseFixedPoint`); the E1 fact filled one test NetState's send buffer (now one crafter per view). **This is the state in `a8cf0e5`.** |
| 4 | same | 685/686: my fact again; 187.4 is below Adamantium (187.5) too, so "a lower metal still works" now checks Mythril |
| red | `build.sh -t sl-modernuo:cc-p53-red --tests-only` in the red tree | 13 failed, 673 passed (table above) |
| 5 | same as 1 | 44/44, **686/686**, image built |
| final | same as 1, after the count line and comment fix | **44/44 patches, 686/686**, image `sl-modernuo:cc-p53` = `a1158037d0d0`; `sl-modernuo:latest` still `88b7983f2d29` (P52) |

## For Chase

1. Commit the four working-tree files with this note (headline 2). Then `build.sh` (not `-t`) when you want `latest`.
2. Deploy to the test shard first. In its log at boot, look for this line:
   `[ClusterFSkillCaps] clusterf.skillCaps.individualCap was the old default 300; now 200 (cc-P53).` Then open
   `Configuration-test\modernuo.json`: `clusterf.skillCaps.individualCap` is `200` and `clusterf.skillCaps.rescaledTo200`
   is `True`. Restart once more: the line does not appear again.
3. Log in a player character and type `[props`, then pick yourself, then Skills: any skill's Cap reads 200. `[SL`,
   Player tab, on yourself: "skills x of 11600".
4. On a staff character at 300 Blacksmithy: after login, Base still reads 300 and Cap reads 200 (nothing lost).
5. `[SetSkill Blacksmith 200` and target a test smith, with Celestial ingots and a smith hammer near an anvil and forge.
   Open the craft menu, then the material button: Celestial is selectable and a dagger in Celestial crafts. Then
   `[SetSkill Blacksmith 187.4`: choosing Celestial says "You cannot work this strange and unusual metal."
   Adamantium needs 187.5, Mythril 175.
6. Same menu: the material list reads "Iron (n)", "Dull Copper (n)" ... "Valorite (n)", "Platinum (n)" ... all in the same
   style, and the line beside the material button reads "Iron (n Available)". The scales button reads "Red Scales (n
   Available)". Check a carpenter's (Wood, Oak ...), a tailor's (Leather/Hides, Spined Hides ...) and a tinker's menu.
7. Blacksmithy categories: page 1 lists LAST TEN and nine categories, then a row reading "Page 1 of 2" with an arrow on the
   right. Nothing touches NOTICES. The arrow shows page 2: "Throwing"/"Miscellaneous" and the rest, a left arrow, and
   "Page 2 of 2". Pick "Miscellaneous", craft something, and the menu comes back on page 2. Then a scribe's pen
   (Inscription): the same two pages.
8. Item bonus: on a smith at Blacksmithy 200 (cap 200), `[add GoldRing` then `[props` it, SkillBonuses, Skill 1 Blacksmith,
   value 15, and wear it. Skills gump: Blacksmithy shows 215. Take it off: 200. Crafting at 215 does not raise Base.
9. Decide: the achievements (Part B, options 1-3; I recommend 3), and whether armored meditation at 150 is right.
10. Promote D-113 and D-114 (above) to `docs\fidelity-principle.md`, and close D62, D63, D64 in `docs\bug-list.md`.
