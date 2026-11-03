# cc-P778: gathering and crafting side activities, assessed

Iron Golem, 2026-11-02. Assessment only, no code. I read the seven packages in `D:\UO\third-party\code\` (reference
only: nothing there was built, run or copied). Three read-only helpers surveyed the larger packages and our own systems,
and I spot-checked their sharpest claims in the code myself (the cooking set's +10 skill foods and +1 elixirs, the
camping +8 stat buff and bank stash, the grave node made at the player's feet). Docs copy
`D:\UO\golems\Iron\shard-migration` on `golem/Iron/P778`, not committed.

## In plain words

- **Seven downloaded add-ons looked at:** gold panning, grave digging, camping outposts, a huge cooking set,
  chocolate making, a "farm" minigame and crafting totems. They were assessed as things to do between fights, next
  to our guilds, New Haven lessons and the planned herbalism.
- **Worth bringing in, rewritten our way (best first):** gold panning in rivers and shallows, grave digging in
  cemeteries, beekeeping (honey and wax for candles) from the cooking set, and chocolate making for the recipes we
  already half have. Each is one Golem task; beekeeping may be two.
- **Not worth it:** the farm minigame (a lottery with bless deeds and a million-gold jackpot), the crafting totems
  (+20 skill talismans that can come blessed), and most of the cooking set (84,000 lines, real beer brands, edits to
  the creature core). Camping outposts are an idea only: a free teleport and a bank in the woods are not for us.
- **For you:** pick which of the four ports you want queued, and in what order. Nothing else to do.

## 1. Each item

Sizes are the downloaded .cs files. "Ser" counts classes with a hand-written Serialize (each is a D40 conversion).
Terms come from each `SOURCE.txt`. None of the packages has a license, so all are community work: credit the
author, ship only inside the player package or the private repo, and do not repost.

### Gold Panning (manwitch; by Hammerhand and Milva)

- **What it does:** a gold pan (50 uses) is a harvest tool on Mining. The player targets water within 2 tiles:
  land water 0xA8-0xAB and 0x136-0x137, and some static water ranges (`GoldPanningSystem.cs`). Not while mounted.
  - Banks are 8x8 tiles holding 5-10 pans each, refilling in 10-20 minutes.
  - Small nuggets need Mining 75, medium 90, large 105.
  - The ML bonus table gives nine gems at 2% each: blue diamond, fire ruby, white pearl and others.
- **The trader** ("Harry Johnson, an old dude gold panner", frozen, invulnerable) swaps by drag and drop:
  - 10 small for 1 medium, 5 medium for 1 large, 3 large for 1 gold brick.
  - 2 bricks for a 10,000 gold bank check.
  - That makes a small nugget worth about 33 gold.
  - His idle lines include "tell me your wife's number" and "that's what she said".
- **Size:** 4 .cs, 633 lines, 3 Ser. It uses the stock HarvestSystem with no core edits. The trader must have exactly
  the stack size; a bigger stack is refused.
- **Fit and overlap:** nothing like it is built. It gives Mining a second, quieter loop by water, and it suits the
  Miners' Compact (its contracts and the proposed gathering orders, `notes/cc-P417-gathering-orders-design.md`). It
  shares water tiles with fishing but uses its own tool, so there is no clash. The gems feed jewelry, imbuing and
  the existing crafts.

### Grave Digging (Massapequa)

- **What it does:** a mining tool on a grave static (0xED3, 0xEDF, 0xEE0-0xEE2, 0xEE8; `HarvestTarget.cs:36`), anywhere
  in the world, with no cemetery check.
  - Each dig rolls Forensics, so Forensics gains normally.
  - The finds depend on Forensics:
    - Under 50: bones.
    - Over 50: fertile dirt or bones.
    - Over 75: grave dust, nox crystal, bat wing, daemon blood, pig iron, bone, fertile dirt.
    - Over 80: sometimes doubled.
  - Each success has a 12.5% bonus roll:
    - human bones (which chop into bones);
    - a random weapon, armor or jewel with 0 to Forensics/20 properties at 1-100% intensity, luck-scaled;
    - a Magery or Necromancy scroll up to 8th circle;
    - a treasure map (level 1 at 50, up to 3 at 70, up to 6 at 90);
    - at Grandmaster only, an "unearthed bones" container (0-999 gold and 1-5 magic items of 1-6 properties) or a
      jewelry box (1-10 magic jewels);
    - coffin, grave and gravestone deeds (house decor).
- **Size:** 9 .cs, 1,713 lines, 16 Ser. It **replaces the stock `HarvestTarget.cs`** to catch the grave tiles inside
  the mining branch.
- **Bugs:**
  - The node holding 40 digs is made at the *player's* spot when none is within 4 tiles, so stepping away gives a
    fresh one: digs are endless.
  - New nodes are not added to the node list.
  - Jewelry in the bones container gets no properties (a duplicated shield branch).
  - The gravestone deed copies the house banner's messages.
- **Fit and overlap:** nothing like it is built. It gives Forensics a real use and makes necromancy reagents a
  gathering trade. Fertile dirt feeds the planned herbalism (F-51; the stock plant engine already uses it,
  `notes/cc-P519-herbalism-vs-build.md`). Treasure maps link to the SOS and treasure revamp. It overlaps the loot
  boxes and treasure chests as a source of magic gear, and that part is too generous as written.

### Advanced Camping and Outpost System (Massapequa)

- **What it does:**
  - **The campfire:**
    - Lasts 220 s instead of about 100.
    - Becomes secure faster with Camping.
    - At Camping 50 the owner gets a gump. "Upgrade" has no skill check, though the readme says 70.
    - An upgraded fire gives everyone within 7 tiles +1 hit and +1 mana a second, and a one-time **+8 Str, Dex and Int
      for 10 minutes** (`Campfire.cs:210-227`).
  - **The camping map:** holds 9 saved spots, with a "travel" button that teleports after 3 s. There are no combat,
    criminal, region or facet checks (`CampingMapGump.cs:116-124`), and nothing in the package makes the map.
  - **Outposts:** staff place them. Camping 50 lights one for 60 minutes, then campers add a tent and bedroll (70), an
    anvil and forge (70), an ankh (90), and a stash at 100 that **opens the player's bank box** (`CampStash.cs:29`).
- **Size:** 13 .cs, 2,168 lines, 11 Ser. It **replaces the stock `Campfire.cs` and `Kindling.cs`**.
- **Bugs:**
  - The gump button IDs overlap: remove is i+20, and rename and travel are 2+2i up to 19.
  - The list is captured when the gump is built.
  - Anyone at Camping 50 can upgrade another player's fire.
  - The first map entry is dropped.
  - Outposts do not save their state.
- **Fit and overlap:** Camping is in the Rangers' list (`ClusterFGuildStarterPath.cs`). The tutorial already tells
  players to light a campfire (`TutorialTradeTrials.cs:69`). Our tents are NPC decor only (`notes/cc-P16-mine-camp-tents.md`).
  A field camp fits League field work and P776's road encounters. The teleport overlaps runes and moongates, and the
  stash overlaps banks: both undercut travel and risk.

### Cooking Expansion Set 13 (Shafev)

- **What it does:** 748 .cs files, about 84,500 lines, 708 Ser, in eight systems:
  - foods: 376 files, 19.5k lines;
  - farming crops: 136 files, 28.7k lines;
  - beverages, with brewing, juicing and wine: 60 files, 10.1k lines;
  - mobiles: 55 files, 8.8k lines;
  - a ranch (raise and feed farm animals): 23 files, 5.9k lines;
  - apiculture (beekeeping, honey, raw wax, wax pots, candles, wax masks): 36 files, 3.5k lines;
  - eight custom craft systems (six on Cooking, two on Alchemy);
  - fireplaces, utensils, seed boxes and recipe scrolls.
- **Core edits** (its own Docs folder):
  - BaseCreature: meat types, the carve switch, the diet arrays, and an AI_WildAnimal case.
  - BaseAI: the AIType enum.
  - PlayerMobile: a RanchersGuild NpcGuild.
  - LootPack: a 5% recipe scroll in every pack.
  - SBBaker: recipe sales.
  - It ships parallel copies of Food.cs and Beverage.cs instead of editing them.
- **Buffs:**
  - Every food rolls a random stat boost when made. It is +1 to +6, mostly +1 or +2, through **XmlSpawner2
    attachments** that ModernUO lacks (`Foods/Core/BaseFood.cs`).
  - 22 "skill foods" give **+10 to a skill for 60 s, ignoring the cap** (`ObeyCap = false`), e.g.
    `Foods/Witchcraft/Skill Food/BowyerBerry.cs:24-26`.
  - Three elixirs add a +1 Str, Dex or Int StatMod **with no expiry** (`Foods/Witchcraft/Elixirs.cs:20`). It is
    cleared only when mods are cleared.
- **Out of setting:** long-neck bottles of "BudLight", "BudWiser", "Corna", "MilleLite", "MGD", "Wild Turkey" and
  more, which are real brands. There is also a steam-powered beverage maker, hot dogs, tacos and clown masks. Some
  art needs an HS/TOL-era client (IDs to 0x9A97).
- **Fit and overlap:**
  - **Apiculture fills a gap.** We have only the Clean Up Britannia beehive decor (`CleanUpRewardAddons.cs:453`) and
    stock jars of honey. Beekeeping is modelled on the plant system, which herbalism builds on.
  - **Farming crops overlap** the stock plant system, raised garden beds (P128) and the tutorial farm, and herbalism
    (F-51) is meant to own planting.
  - **Brewing and wine** have nothing of ours to overlap, but they are 10k lines tied to the parallel food types.
  - **The ranch needs creature-core edits.**

### Chocolatiering Adventure (Carlos_ar; guardian house by Juzzver)

- **What it does:**
  - **The craft:** a chocolatiering bowl, a Cooking craft at an oven (`DefChocolatiering.cs`):
    - cocoa butter and cocoa liquor from cocoa pulp;
    - dark, milk and white chocolate at 15, 32.5 and 52.5;
    - sweet cocoa butter;
    - foil-wrapped figures (nutcracker, orc, beetle, bunny, solen, unicorn) from molds and gold foil.
  - **Unwrapping a figure:** a 20% chance of one of ten tarot cards, which only show a picture.
  - **The Candy Shack**, a guardian house that staff place:
    - Using the door spawns 3-10 "Oompa" and "Loompa" mobs (800 hits, flee, tunnel away).
    - The chest spawns the "Evil Chocolatier" (about 450 hits, Magery 200).
    - The chest is trapped, needs lockpicking 70-100, and holds 1,000 gold and three FilthyRich loot packs.
    - The house removes itself 30 minutes after it is emptied.
- **Size:** 26 .cs, about 3.2k lines, 33 Ser. No stock file is replaced. The readme's optional step edits DefTinkering
  for the bowl.
- **Bugs:**
  - The drop tables are off by one: the unicorn mold and gold foil never drop from the chest or the chocolatier, and
    the beetle never drops from the Oompas.
  - The door only ever spawns Oompas.
  - A double-click can roll the tarot card twice.
- **Out of setting:** the Oompa-Loompas and the "candy man" are Willy Wonka's, and tarot cards are not our setting.
  The art for the tarot cards, molds and chests needs a newer client (0x9C14, 0xA305 and up).
- **Fit and overlap:** we already have the ingredients and the end items in part:
  - cocoa pulp from the stock plants;
  - `GoldFoil.cs`, `Nutcrackers.cs` and `ValentineChocolate.cs`.
  
  Our cooking registrations say the chocolate nutcracker recipes were left out *because sweet cocoa butter is in
  neither tree* (`CookingCraftRegistrations.cs` header). This package's recipes are exactly that missing step.

### The Farm Minigame (DragnMaw)

- **What it does:** it is not a farm. Weak random-bodied mobs ("FarmMob") give a damage-weighted 5% chance of a
  cursed Farm Ticket. Opening it inside your house always gives 1,000 gold to the bank, then rolls:
  - 1 in 2 of 50 valorite, barbed leather or heartwood;
  - 1% a **clothing bless deed**;
  - 1% powder of fortification;
  - 50% 5 Sovereigns (ServUO's store currency);
  - 1% **1,000,000 gold**;
  - 1% 1,000 Sovereigns.
  
  The big wins are broadcast to the world.
- **Size:** 4 .cs, 459 lines, 4 Ser. It depends on ServUO Sovereigns.
- **Fit and overlap:** none as a gathering activity. The damage-weighted award is something we already have:
  P776's toll box goes to the top damager through `ClusterFLootBoxes.Award`.

### Crafting Totems (kfritz411)

- **What it does:** seven talismans, one each for smithing, tailoring, carpentry, cooking, fletching, alchemy and
  tinkering. Each has:
  - **+5 or (1 in 4) +20** to its craft skill;
  - a random craft success bonus;
  - a random chance to come **Blessed** (`GetRandomBlessed`);
  - random slayer protection;
  - a summon (fire beetle or earth elemental for the smith).
- **Size:** 8 .cs, 1,182 lines, 8 Ser. It **replaces `TalismanSummons.cs`**. It uses OWLTR hues and resources
  (`CraftResource.Platinum`), which we do not have, and newer-client art (0x9E2A).
- **Fit and overlap:** we already have the library talismans with craft bonuses
  (`CollectionsBritLibraryTalismans.cs`). Under D-113 (`ClusterFSkillBonusAboveCap.cs`), item skill bonuses count
  above the cap here, so a +20 craft talisman is worth more on this shard than on OSI.

## 2. Rules check

The rules for this task: nothing that grants skill or stat points, power scrolls, bless deeds or property artifacts,
and items usable now and mostly helpful. Normal skill gain from using a skill (panning on Mining, digging on Forensics)
is not a grant. Short buffs are read as allowed only when they are as modest as a spell's.

| Item | Skill or stat points | Power scrolls | Bless deeds, blessed items | Artifacts, magic gear | Usable now, helpful | Verdict |
|---|---|---|---|---|---|---|
| Gold panning | none | none | none | none; ML gems are crafting resources | yes | **passes** |
| Grave digging | none (Forensics gains by use) | none | gravestone decor is blessed (house decor, fine) | **random magic gear up to 5 props at 100%, GM containers of 1-5 magic items, maps up to 6**: too rich, must go | yes, once trimmed | passes after rework |
| Camping outposts | **+8 Str/Dex/Int for 10 min** to anyone at the fire; too big for a campfire | none | none | none | the teleport and bank stash are not "helpful items", they bypass travel and risk | fails as written |
| Cooking expansion | **+10 skill for 60 s above the cap; a +1 stat mod with no expiry; random stat buffs on every food** | none | GardenDeed and beer bottles blessed | none | much is decor or junk | fails as written; apiculture alone passes (no buffs) |
| Chocolatiering | none | none | none | Candy Shack chest: FilthyRich packs (stock loot) | the craft is usable now; the tarot cards do nothing | craft **passes**; Candy Shack fails on setting |
| Farm minigame | none | none | **clothing bless deed (1%)** | none, but a 1,000,000 gold jackpot | no | **fails** |
| Crafting totems | **+20 craft skill item bonus** (above the cap here) | none | **random Blessed** | they are property items | yes, but too strong | **fails** |

None of the seven grants power scrolls or permanent skill or stat points.

## 3. Recommendations

| Item | Call | Why |
|---|---|---|
| Gold panning | **port** (small) | Clean, small, harvest-system native, a calm Mining loop by water that rewards repetition with modest gold and gems. Rewrite the trader and his lines. |
| Grave digging | **port** (medium, rebuilt) | Gives Forensics a use and makes reagents and fertile dirt a trade that feeds necromancy and herbalism. Rebuild rather than copy: our own spade tool (no HarvestTarget replacement), cemetery regions only, nodes on the grave, and bonus finds through our loot tables. |
| Camping outposts | **idea only** | The good part is small: a tended fire that helps a party rest. The teleport, the bank stash, the +8 buff and the stock replacements all have to go, which leaves too little to port. Rebuild it as a few lines of our own when the Rangers' League work wants it. |
| Cooking expansion | **port apiculture only** (medium); **skip the rest** | Beekeeping is self-contained, fits the plant and herbalism direction, and fills a gap (honey, wax, candles). The other 81k lines bring core edits, XmlSpawner buffs, real brands, and overlap with herbalism's planting. Brewing is an idea only, for later. |
| Chocolatiering | **port the recipes only** (small); **skip the Candy Shack** | Finishes our half-built chocolate (sweet cocoa butter is the missing step for the nutcracker recipes) and suits Valentine's and the festival calendar. The Candy Shack is Wonka's, buggy and out of setting. |
| Farm minigame | **skip** | A lottery with a bless deed and a million-gold jackpot; nothing to do with farming. The damage-weighted award is already ours. |
| Crafting totems | **skip** | +20 skill talismans (worth more here under D-113), random blessed, OWLTR resources, and a stock file replaced. Our library talismans already cover craft bonuses. |

### Ranked ports, with prompt sketches

1. **Gold panning** (about one small Golem task; roughly 500 lines ours plus facts).
   - Sketch: "Port gold panning as our own harvest: a prospector's pan (sold by Compact provisioners), Mining 60+ on
     shallow river and lake water only (no ocean), small, medium and large nuggets and the ML gems at a low rate, sold
     to a Miners' Compact assayer for gold or Compact standing. Our voice, no trader jokes. Tests for tile, skill
     gates, bank depletion and price."
   - First because it is the smallest, cleanest and most "between fights", and it gives the Compact a second loop.
2. **Grave digging, rebuilt** (one medium Golem task; roughly 900 lines plus facts).
   - Sketch: "Build grave digging from Massapequa's idea: a gravedigger's spade, Forensics on grave statics inside
     cemetery regions only, a node per grave (not per player), bones, fertile dirt and necro reagents by skill, and a
     small bonus roll through our loot tables (human bones, a low treasure map, grave decor deeds). No magic gear
     generation, no stock HarvestTarget replacement, a karma or criminal touch if Chase wants it. Tests for the
     region gate, node depletion, the tiers and the bonus odds."
   - Second because it opens Forensics and feeds necromancy and herbalism, but needs more rework.
3. **Apiculture (beekeeping) from the cooking set** (one large Golem task, maybe two; the source is 3.5k lines plus
   the wax craft).
   - Sketch: "Port the Cooking Expansion Set's apiculture alone: placeable hive (house or garden), hive care like
     the plant system, honey and raw wax, a wax pot and a candle-making step on Alchemy or Tinkering, our art only, no
     food buffs, no XmlSpawner. Decide whether wild hives exist. D40 serialization for the hive."
   - Third because it is the biggest, and it should line up with herbalism's plots (F-51) so the two do not fight
     over garden space.
4. **Chocolatiering recipes** (one small Golem task; roughly 400 lines plus facts).
   - Sketch: "Add the chocolatiering recipes to Cooking (no separate bowl unless needed): cocoa butter and liquor
     from cocoa pulp, the three chocolates, sweet cocoa butter, and then turn on our nutcracker recipes; figures only
     where our client has the art; no tarot, no Candy Shack; molds from a provisioner. Tests for each recipe and the
     unlocked nutcrackers."
   - Fourth only because it is seasonal and narrow; it could go anywhere in the queue, for example before Valentine's.

Idea only, not ranked: a campfire rest (an upgraded, tended campfire gives a short regen to a resting party and a
safe logout, no stat buff, no teleport, no bank), and brewing (ale, cider, mead) as a later cooking guild loop.

## Notes for the record

- `D:\UO\third-party\CODE-INTAKE.md`: no row existed for any of the seven. I added seven rows after the 11-02
  token-system row, each with Overseer `assess (P778)` and the call above. A copy of the file from before the edit is
  in this session's scratchpad. The project copy (`claude/servuo-code-intake.md`) is not in this docs copy; the scout
  re-syncs it.
- The cooking set's Ranch is the only part that touches creature AI. If a ranch is ever wanted, build it fresh; the
  edits to BaseCreature and BaseAI would be a pinned-file patch.
- Credits to keep if ported: Hammerhand, Milva and manwitch (gold panning); Massapequa (grave digging and the
  campfire idea); Shafev (apiculture); Carlos_ar (chocolatiering recipes).
- Not verified: whether our client has every art ID the four ports would use. Each port prompt should check its art
  with the art tools first.

P778 DONE
