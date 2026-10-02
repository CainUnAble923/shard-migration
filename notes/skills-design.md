# Skills design: every skill to the F-12 cap

Started 2026-10-02 by the skills design chat (pass-down: `notes\passdown-skills-design-2026-10-02.md`).
Design only: nothing here is built. Decided groups go to the overseer, who writes the cc-P prompts.

Ground rules (from `notes\f12-levels-loops-caps.md`): skill cap = max level; ladder 50 (loop 0), 100, 125, 150,
175, 200; every skill maxable on one character; stats uncapped (500). A use stops giving gain once the skill's
**Value** reaches that use's `maxSkill` (`UOContent/Skills/SkillCheck.cs:56-61`, pinned 7c9215d97). Ported
behavior stays faithful unless Chase decides otherwise; every change is a deviation to register.

Pinned paths are relative to `D:\UO\ModernUO-pinned\Projects`. "Ours" is `D:\ShatteredLegacy\server`
(code at e092a3d, 2026-10-02 11:19).

## Status

| # | Skill | Group | Status |
|---|---|---|---|
| 56 | Mining | Gathering | **decided** 2026-10-02 |
| 57 | Lumberjacking | Gathering | **decided** 2026-10-02 |
| 58 | Fishing | Gathering | **decided** 2026-10-02 |
| 50 | Blacksmithy | Crafting | **decided** 2026-10-02 (mark flavor open) |
| 54 | Tailoring | Crafting | **decided** 2026-10-02 (leather bonus rows to draft) |
| 55 | Tinkering | Crafting | **decided** 2026-10-02 |
| 52 | Carpentry | Crafting | **decided** 2026-10-02 |
| 51 | Bowcraft/Fletching | Crafting | **decided** 2026-10-02 |
| 53 | Cooking | Crafting | **decided** 2026-10-02 |
| 49 | Alchemy | Crafting | **decided** 2026-10-02 |
| 17 | Inscription | Crafting | not started |
| 23 | Imbuing | Crafting | not started |
| 1-6 | Swords, Macing, Fencing, Archery, Throwing, Wrestling | Combat | not started |
| 7 | Tactics | Combat | not started |
| 8 | Anatomy | Combat | not started |
| 9 | Parry | Combat | not started |
| 10 | Bushido | Combat | not started |
| 11 | Focus | Combat | not started |
| 12 | Arms Lore | Combat | **decided** (F-26, 2026-10-02) |
| 33 | Healing | Combat support | not started |
| 13 | Magery | Magic | not started |
| 14 | Evaluating Intelligence | Magic | not started |
| 15 | Resisting Spells | Magic | not started |
| 16 | Meditation | Magic | not started |
| 18 | Necromancy | Magic | not started |
| 19 | Spirit Speak | Magic | not started |
| 20 | Chivalry | Magic | not started |
| 21 | Spellweaving | Magic | not started |
| 22 | Mysticism | Magic | not started |
| 24 | Ninjitsu | Magic | not started |
| 37 | Animal Taming | Animal | not started |
| 38 | Animal Lore | Animal | not started |
| 34 | Veterinary | Animal | not started |
| 39 | Herding | Animal | not started |
| 40 | Musicianship | Bard | not started |
| 41 | Peacemaking | Bard | not started |
| 42 | Provocation | Bard | not started |
| 43 | Discordance | Bard | not started |
| 25 | Hiding | Thief | not started |
| 26 | Stealth | Thief | not started |
| 27 | Detect Hidden | Thief | not started |
| 28 | Snooping | Thief | not started |
| 29 | Stealing | Thief | not started |
| 30 | Lockpicking | Thief | not started |
| 31 | Remove Trap | Thief | not started |
| 32 | Poisoning | Thief | not started |
| 44 | Tracking | Utility | not started |
| 45 | Item Identification | Utility | not started (F-14 Appraisal) |
| 46 | Taste Identification | Utility | not started |
| 47 | Camping | Utility | not started |
| 48 | Cartography | Utility | not started |
| 35 | Begging | Utility | not started |
| 36 | Forensic Evaluation | Utility | not started |

Numbers are cc-P20's row numbers (`notes\cc-P20-skill-scaling-research.md:322-381`).

## Ready for the overseer

**Gathering and core crafting, decided 2026-10-02:** Mining, Lumberjacking, Fishing, Blacksmithy, Tailoring,
Tinkering, Carpentry, Bowcraft/Fletching, Cooking, Alchemy. Each section's "Decided" block is the spec. Cross-cutting
pieces worth one prompt each:
- **The shared ladder** (ore, ingot, wood, leather, cloth, fish, elixir tiers at 100 / 115 / 130 / 140 / 155 / 170 /
  185 / 200) and **"materials lift the gain window"** (shift = gate - 100) across all crafts.
- **Harvest rewards** (truer veins and groves, richer yields, better finds, prospect and survey, plain-resource
  toggles); permanent groves are already in P37.
- **Thrift, master's durability and the master's mark** across crafts (Hammer of Hephaestus T3/T4 thrift).
- **Feature-queue item (features chat):** the creature variants for leather, silk and meat.
- **Ports:** High Seas fishing and fish pies (ServUO pub57).
- **Defect-sized:** large BOD lock-out, Infused Alchemist's Gem cap.

Still in this group: Inscription and Imbuing.

## Corrections to earlier notes, found while verifying

- **D42 is fixed, not live.** `f12-levels-loops-caps.md` still lists it under "still required"; ours
  `customizations\SmithGuildSalvageBag.cs:113-133` clamps the return at `cost - 1` (cc-P23).
- **The Meditation pattern line moved:** the cap-following gain call is ours `customizations\Meditation.cs:111`
  (`CheckSkill(Meditation, 0.0, Skills[Meditation].Cap)`), not `:92`.

---

## 56. Mining

### Today

- **Harvest (pinned engine, our resource table).** Ours `patches\Mining.cs` replaces pinned's; the table is
  pinned's: Iron (req 0, min 0, max 100) up to Valorite (99 / 59 / 139) (`patches\Mining.cs:113-188`). Our 8
  extended ores are appended at world load, **all req 100**, min 65 to 80, max 140 to 155, Platinum to Celestial
  (`customizations\ClusterFMiningExtension.cs:84-94`), vein weights 8 down to 1 of 1036, permanent veins
  (`:108-131`).
- **The gain call** is the harvest itself: `skillBase >= resource.ReqSkill && CheckSkill(Mining, min, max)`
  (pinned `Engines/Harvest/Core/HarvestSystem.cs:147`). Amount is not skill-based: 1 ore, 2 in Felucca
  (`patches\Mining.cs:97-98`).
- **Fallback:** a colored vein gives its fallback (iron) half the time regardless of skill (`ChanceToFallback`
  0.5, `HarvestSystem.cs:339`; elves +20 percent toward primary), and always when Value is below the ore's req
  or min (`:346`).
- **Gems:** 0.1 percent each of six gems at Base 100, fixed (`patches\Mining.cs:208-216`, gate
  `HarvestSystem.cs:211`).
- **Smelting** (pinned `Items/Resources/Blacksmithing/Ore.cs:176-205`): window difficulty +/- 25, OSI ores 65
  to 99. **Our 8 ores fall to the default 50** (`:186`), so any miner smelts Celestial and the window is 25 to
  75. Our satchel's Smelt All uses 100 for all 8 and no gain (`customizations\ReinforcedOreSatchel.cs:53-70`).
- **Sand** (needs Base 100 and the Sand Mining book): req 100, min 70, **max 400**
  (`patches\Mining.cs:254`, gate `:334-335`). Granite: Base 100, the Stone Mining book and the toggle, 10
  percent (`:284-285`).
- **Guild:** the Miners' Compact (vouchers and standing, `customizations\MinersCompactLiaison*.cs`), Jacob's
  pickaxes (+5 to +25 Mining **Value**, `customizations\Jacobs*Pickaxe.cs`), ore satchels.
- **Achievements:** `skills.mining_gm` 100, `mining_elite` 200, `mining_legend` 300
  (`customizations\ClusterFAchievements.cs:998-1001`). Legend becomes unreachable at the 200 cap.

### Gain path to 200

| Use | Ceiling | Reachable by play at the 200 cap? |
|---|---|---|
| Iron | 100 | stops at 100 |
| OSI colored ores | 105 to 139 | stops at 139 |
| Our 8 ores | 140 to 155 | stops at 155 |
| Smelting | 124 (Valorite); our ores 75 | stops at 124 |
| Sand | 400 | **yes, the only path from 155 to 200** |

So Mining reaches 200 today only by digging sand, which is a glassblowing input, not mining.

**Pickaxe trap:** the gain check reads Value, so a +25 Worldbreaker stops Base gains 25 points early (Celestial
gains end at Base 130 while it is equipped). OSI behaves the same (faithful), but it matters more here because
our pickaxes are the guild's reward line.

**Base vs Value mismatch:** the vein choice reads Value (`HarvestSystem.cs:346`), the harvest gate reads Base
(`:147`). A +25 pickaxe at Base 90 picks the Platinum vein, then fails the gate with "you loosen some rocks"
instead of falling back to iron. Small, ours to fix or leave.

### What breaks above 120

Nothing in Mining itself now that D42 is fixed. Gem and fallback odds clamp. Felucca double yield is fixed.

### Loop by loop (today's numbers)

- **Loop 0 (cap 50):** iron and Dawnstone (45 / 5 / 85, dungeon decision 9) only. Dull Copper needs Base 65.
  That is pacing, not a problem: Dawnstone is the loop-0 metal.
- **Loop 1 (cap 100):** all OSI ores. Our ores need Base 100, so they open at the very top of loop 1.
- **Loops 2 to 5 (125 to 200):** our ores gain to 155, then nothing but sand.

### Relevance

Mining is the root of the metal economy: every smith item, the Smith BODs and commissions, the Miners' Compact,
and the extended-ore ladder that F-28 mirrors for wood. Today a miner past 100 gets **access** (which ores) and
nothing else: no extra yield, no better odds on the vein, no better gems.

### Synergies

- **Blacksmithy:** the ingot gates (`ClusterFMiningExtension.cs:174-181`, 100 to 300) must match the ore ladder.
- **Carpentry (Masonry)** through granite, **Alchemy (Glassblowing)** through sand.
- **Arms Lore (F-26)** no direct link. **Tinkering** makes the shovels and pickaxes.
- **The ore logbook** (`customizations\OreDiscoveryEntry.cs`) is the mining twin of the grove ledger.

### Proposal

1. **One ladder for ore, ingot and wood.** Rescale our 8 ores to the F-28 wood ladder: Platinum 100, Toxic 115,
   Blaze 130, Frost 140, Obsidian 155, Mythril 170, Adamantium 185, Celestial 200, used for the **mining req,
   the smelt difficulty and the smithing ingot gate** (Blacksmithy section confirms the smith side).
2. **Each ore trains to about 45 above its own req**, so the ladder itself is the gain path: Platinum
   (req 100, min 60, max 145) up to Celestial (200, 160, 245). Obsidian and up carry a miner to 200 with no
   sand needed. A pickaxe bonus no longer strands anyone, because the top windows run past 200.
3. **Smelting our ores gets real windows** (difficulty = the ore's req, +/- 25, as pinned does for OSI ores),
   so smelting is a second gain path to 200 and nobody smelts Celestial at Mining 30. The satchel's Smelt All
   uses the same numbers.
4. **What skill buys past 100 (pick any):**
   a. **Truer veins:** the 50 percent fallback to iron falls with skill, to 25 percent at 200.
   b. **Richer strikes:** a chance for +1 ore per swing, 0 at 100 rising to 50 percent at 200.
   c. **Better gems:** gem odds rise with skill above 100 (0.6 percent total today, about 1.5 percent at 200).
   d. **Prospecting:** use Mining on a rock to learn the vein's ore without digging; feeds the ore logbook.
5. **Achievements:** `mining_legend` moves to 200; `mining_elite` to 150.

### Open questions for Chase

1. Proposal 1: one shared ladder (ore, ingot, wood), with Celestial and Starwood at exactly 200, so they are
   the final-loop reward?
2. Proposal 2: gains come from the ore ladder (content driven), or a simpler rule where every ore trains to the
   player's cap (the Meditation pattern)?
3. Proposal 4: which of a to d? Overseer-style lean: **a and b**, since they make a 200 miner visibly better
   at the job.
4. Sand stays at 400 (a free path to the cap for anyone with the book), or does it come down to 200 like
   everything else?

### Decided (Chase, 2026-10-02, 11:58)

1. **One shared ladder** for ore, ingot and wood: Platinum/Ironwood 100, Toxic/Ghostwood 115, Blaze/Emberbark 130,
   Frost/Frostbark 140, Obsidian/Shadowbark 155, Mythril/Runewood 170, Adamantium/Voidwood 185,
   Celestial/Starwood 200. Same number for the mining req, smelt difficulty and smithing ingot gate. Celestial and
   Starwood are the final-loop reward.
2. **Gains come from the ore ladder:** each ore trains to about req + 45 (Platinum 100/60/145 up to Celestial
   200/160/245).
3. **Smelting our ores gets real windows** (difficulty = req, +/- 25), satchel Smelt All matching. (Approved with
   the ladder.)
4. **All four skill rewards, approved:**
   a. **Truer veins:** fallback to iron falls from 50 percent at 100 to 25 percent at 200 (linear).
      **Plus an iron-only toggle** (Chase): when on, every swing yields iron, for bulk iron needs. Overseer
      default: a context-menu toggle on the pickaxe and shovel, saved per character, the way pinned's stone
      toggle works (`patches\Mining.cs:284`); richer strikes (b) still apply to iron.
   b. **Richer strikes:** chance of +1 ore per swing, 0 at 100 to 50 percent at 200 (linear).
   c. **Better gems:** total gem odds from 0.6 percent at 100 to about 1.5 percent at 200 (linear).
   d. **Prospecting:** use a pickaxe or shovel on a rock (context menu) to learn the vein's ore without digging;
      the find goes into the ore logbook. Overseer default: no skill gain from prospecting (it would be a free
      macro), a short cooldown, and it needs Mining 100.
5. **Achievements:** `mining_elite` to 150, `mining_legend` to 200. (Proposal 5, not objected.)
6. **Sand stays at 400** ("no one's going to want to do it"). It remains an alternate path to the cap.

Deviations to register: the ore ladder rescale, the extended windows, extended-ore smelt difficulties,
truer veins, iron-only toggle, richer strikes, gem odds, prospecting.

---

## 50. Blacksmithy

### Today

- **Crafting gain** is passive and separate from success: every attempt calls `CheckSkill(skill, recipe min,
  recipe max)` for each skill on the recipe (ours `customizations\CraftItem.cs:893-896`); success is computed
  after, from the main skill (`:904-906`). **The material does not change the gain window.** Pinned's highest
  smith recipe ceiling is 140 (plate kabutos, `Engines/Craft/DefBlacksmithy.cs`); our Gargish items stop at 135.
- **Material gate** reads Base (ours `CraftItem.cs:629`); **Enhance** reads Value (pinned
  `Engines/Craft/Core/Enhance.cs:349`), so a Hammer of Hephaestus helps Enhance but not crafting.
- **Hammer of Hephaestus:** +5 / +10 (and a variable) Blacksmithy as a skill mod
  (`customizations\HammerOfHephaestus.cs:234, :599, :649`). Same effect as the pickaxes: it lowers the Base at
  which each window stops giving gain.
- **Guild paths (Society of Smiths)**, both ours:
  - BOD turn-in: skill checks in a window by material (`customizations\ClusterFSmithBODSystem.cs:362-405`, called
    at `:249-251` and `:436-438`).
  - Commissions: same idea, own windows (`customizations\ClusterFSmithCommissions.cs:767-797`).
- **Four different ladders for the same 8 metals** (found 2026-10-02):

| Metal | Ingot gate (`ClusterFMiningExtension.cs:174-181`) | BOD offered at (`patches\SmallSmithBOD-PostValorite.patch:31-48`) | Commission tier from (`ClusterFSmithCommissions.cs:438-445`) | Salvage resmelt (`SmithGuildSalvageBag.cs:56-75`) |
|---|---|---|---|---|
| Platinum | 100 | 105 | 105 | 105 |
| Toxic | 125 | 115 | 115 | 115 |
| Blaze | 150 | 130 | 130 | 130 |
| Frost | 175 | 150 | 150 | 150 |
| Obsidian | 200 | 175 | 175 | 175 |
| Mythril | 225 | 200 | 200 | 200 |
| Adamantium | 250 | 250 | 250 | 250 |
| Celestial | 300 | 300 | 300 | 300 |

  So a smith at 115 is offered Toxic orders and commissions he cannot craft until 125, and so on up the ladder.

### Gain path to 200

| Use | Ceiling today |
|---|---|
| Crafting | 140 (any material) |
| BOD turn-in | Valorite 105 (115 exc); Platinum 115 ... Obsidian 205 ... Celestial 340 (+10 exc) |
| Commission | Platinum 125 ... Obsidian 200 ... Celestial 325 (+10 exc) |
| Repair | 125 (pinned) |

At a 200 cap, BODs and commissions already reach 200, but only through Obsidian and Mythril orders that the
offer ladder (175, 200) hands out late, and crafting itself stops at 140.

### What breaks or plateaus

- Nothing breaks: success and exceptional clamp at 100 percent (cc-P20 0.2: every smith item is always
  exceptional by about 163). **Past about 160 crafting gets nothing better**, only metal access.
- **Large BOD lock-out (cc-P20 B4) is still in code:** `ClusterFSmithBODSystem.cs:98-107` rolls a large at
  `(Base - 40) / 300` and, if one is already held, refuses the request outright instead of giving a small.
  At 200 that is 53 percent of requests refused. A defect for the overseer, not a design question.
- Achievements `smith_elite` 200 and `smith_legend` 300 (`ClusterFAchievements.cs:1005-1007`).

### Relevance

The core crafter: weapons and armor for everyone, the Society of Smiths' seals and standing, BODs (F-18, F-25),
commissions, salvage, and under F-29 the exceptional gap that lets crafted gear beat found artifacts. Under F-28
and the Mining decision, the metal ladder is the spine of loop progression for crafters.

### Synergies

- **Mining** feeds it (shared ladder, decided). **Arms Lore** (F-26) sets exceptional damage and armor bonus,
  and lowers max-durability loss on repair. **Tinkering** makes the tongs and hammers.
- **Imbuing** and runic hammers sit on top of smith output (later sections).

### Proposal

1. **One ladder everywhere.** Ingot gate, BOD offer, commission tier and salvage resmelt all use the decided
   ladder (100 / 115 / 130 / 140 / 155 / 170 / 185 / 200). Commissions keep their 70/30 current/previous mix.
2. **Materials lift the crafting gain window.** When crafting with one of our 8 metals, the gain check's window
   shifts up by (metal's gate - 100): a plate kabuto (90-140) in Obsidian trains at 145-195, in Celestial at
   190-240. Success and exceptional chances are unchanged (recipe based). So a smith can climb to 200 at the forge
   by working up the ladder, and the BODs become a faster path, not the only one.
3. **BOD and commission windows re-fit to the ladder**, each about gate - 10 to gate + 40 (Celestial 190-240),
   exceptional +10 as today, so they top out just past 200.
4. **What skill buys past 100 (pick any):**
   a. **Thrift:** chance to refund the ingots on a successful craft, 0 at 100 to 25 percent at 200.
   b. **Master's durability:** crafted items get more max durability, up to +50 percent at 200 (stacks with
      F-26's slower wear).
   c. **Enhance follows skill:** keep pinned's falling break chance (already gets better to 200); no change.
   d. **Master's mark:** at 200, the maker's mark reads "Master" (cosmetic, a loop-5 bragging right).
5. **Achievements:** `smith_elite` to 150, `smith_legend` to 200 (same as Mining).
6. **Overseer item:** fix the large BOD lock-out (fall back to a small order). May already be in P32 Part B or
   F-25; check before writing a new prompt.

### Open questions for Chase

1. Proposal 2 (materials lift the gain window at the forge): yes, or keep crafting capped at 140 and leave BODs
   and commissions as the only climb past it?
2. Proposal 4: which of a, b, d? Lean **a and b**: thrift mirrors the miner's richer strikes, and durability
   pays off for every player who wears the gear.
3. Should Tailoring (next) get the same pattern (one leather ladder, materials lift the window, thrift)?

### Decided (Chase, 2026-10-02, 12:17)

1. **One ladder everywhere** (ingot gate, BOD offer, commission tier, salvage resmelt). Yes.
2. **Materials lift the crafting gain window** (shift = metal's gate - 100). Yes: smiths climb to 200 by crafting.
3. **BOD and commission windows re-fit** to about gate - 10 to gate + 40, exceptional +10. Yes.
4. a. **Thrift: yes, and built into the Hammer of Hephaestus "the more they use that metal".** It already has
      the hook: per-metal familiarity is recorded on every forge strike (`customizations\HammerOfHephaestus.cs:254-262`),
      and its **T3 bonus, "familiar metals waste fewer ingots", is a stub** (`:24`). Overseer default: skill thrift
      0 at 100 to 25 percent at 200 for everyone; a T3+ hammer adds up to +10 percent more for a metal as its
      familiarity for that metal reaches the tier's cap (T4 the same, its cap higher). Thrift refunds the ingots
      only, never more than the item cost (the D42 lesson).
   b. **Master's durability: yes**, up to +50 percent max durability at 200.
   d. **Master's mark: yes, with more flavor.** Proposal below, to confirm.
5. **Achievements** to 150 and 200. Yes.
6. **Overseer item** (not a question): the large BOD lock-out at `ClusterFSmithBODSystem.cs:98-107`.

**Master's mark flavor (overseer proposal, open):** the maker's mark records the smith's standing at the moment
of crafting, so old gear tells a story:
- Mark by skill: "Crafted by X" (pinned) below 150, "Expert smith X" at 150, "Master smith X" at 200.
- Plus the loop the smith was on ("Master smith X, of the Fifth Loop"), since loop count is the prestige counter.
- Plus the metal's own epithet on Celestial work ("Starforged by X"); one epithet per metal of ours.
- The hammer tier can add a line ("Struck with the Hammer of Hephaestus").

Deviations to register: ladder unification, material-lifted gain windows, refit BOD/commission windows, thrift,
hammer T3/T4 thrift, master's durability, mark text.

---

## 54. Tailoring

Chase, 2026-10-02 12:17: **same pattern as Blacksmithy** (one leather ladder, better leather trains higher,
thrift). This section works out what that needs.

### Today

- **Crafting gain** uses the same passive recipe-window call as smithing (ours `CraftItem.cs:893-896`).
  Pinned's highest tailoring recipe stops at **121** (`Engines/Craft/DefTailoring.cs`, top windows 95-120 and
  96-121). Ours adds Gargish cloth armor to **144** (`customizations\Engines\Craft\TailoringCraftRegistrations.cs:92-99`),
  but only gargoyles wear it.
- **Leather ladder is OSI's four:** Regular 0, Spined 65, Horned 80, Barbed 99 (`DefTailoring.cs:662-665`).
  **We have no extended leathers.** Hides come only from carving creatures by their `HideType`
  (`Mobiles/BaseCreature.cs:113-119`, drop `:1732-1767`); Barbed comes from dragons, wyrms, nightmares and a few
  others (11 files).
- **Cloth has no ladder** (no sub-resource with bonuses). Gloomsilk is cosmetic (dungeon decision 8); Burrowhide
  is the dungeon's carved starter leather, not built yet (cc-P36).
- **Guild:** the Tailors' Circle exists (join at Tailoring 50, `customizations\ClusterFGuildSystem.cs:126-131`).
  **Tailor BODs are still vanilla** (no guild turn-in, no skill check); F-18 moves them into the same system as
  smithing (approved, batched with smithing).
- **Repair** gains to 125 like smithing (pinned `Engines/Craft/Core/Repair.cs`).

### Gain path to 200

Crafting 121 (144 for Gargish cloth), repair 125. **Nothing past 144 at all.** Tailoring cannot pass about 121
by play for a non-gargoyle.

### What breaks or plateaus

Nothing breaks (cc-P20: clamps; every item always exceptional by about 189). Past 121 there is no recipe, no
leather and no reason.

### Relevance

Leather and cloth armor (the mage and archer layer), clothing, bags, and the Tailors' Circle. Under F-29, crafted
leather armor can outclass found pieces. Today the skill tops out at the loop-1 cap.

### Synergies

- **Carving** (any blade) and **creature content**: hides are a hunter's drop, so a leather ladder makes hunters
  and tailors trade, the way miners and smiths do.
- **Arms Lore** (F-26) on exceptional leather armor. **Imbuing** later.

### Proposal

1. **Eight extended leathers on the shared ladder** (100 / 115 / 130 / 140 / 155 / 170 / 185 / 200), one theme each
   to match its ore and wood partner. Working names, to change freely:

| Gate | Leather | Theme (ore / wood partner) | Comes from (overseer default) |
|---|---|---|---|
| 100 | Stonehide | sturdy (Platinum / Ironwood) | hulking beasts: ettins, trolls, ogre lords |
| 115 | Etherhide ("ethereal") | unseen, otherworldly (Toxic / Ghostwood) | fey and spirit beasts: bake kitsune, ki-rin, unicorns |
| 130 | Cinderhide | fire (Blaze / Emberbark) | hell hounds, hell cats, fire beetles, drakes (red) |
| 140 | Rimehide | cold (Frost / Frostbark) | frost trolls, white wyrms, frost spiders |
| 155 | Shadehide | assassin (Obsidian / Shadowbark) | nightmares, shadow wyrms, dread horns |
| 170 | Runehide | arcane (Mythril / Runewood) | ancient magic beasts: greater dragons, hiryu, serpentine dragons |
| 185 | Voidhide | hunger (Adamantium / Voidwood) | abyssal creatures, the deeper dungeon floors |
| 200 | Starhide | pinnacle (Celestial / Starwood) | champions, bosses and our own above-160 creatures (F-14) |

   The **drop is a roll on carving**: a creature that already gives hides has a small chance its pile is the
   extended leather of its family, higher for paragons. Exact creature lists go into the build prompt.
2. **Leather bonuses** follow F-28's pattern: normal = the theme line, exceptional = theme plus damage/secondary
   line (armor version: resists and a secondary), with F-29's exceptional gap.
3. **Materials lift the gain window** (shift = leather's gate - 100), same rule as smithing. A Barbed-tier recipe
   in Starhide trains to about 221.
4. **Thrift, master's durability and the mark** as decided for smithing (thrift refunds leather or cloth only).
5. **Tailor BODs** (F-18) use the leather ladder for offers and turn-in windows, the same refit as smithing.
6. **Cloth stays without a ladder.** Cloth items (robes, clothing) stay cosmetic and utility; leather is the
   armor ladder.

### Open questions for Chase

1. Eight new leathers on the shared ladder: yes? Names and themes as above, or your own?
1a. (12:24) Chase: Wraithhide and Shadehide read as the same leather. Chase chose **ethereal** for 115 (working name Etherhide,
   fey and spirit beasts) and **Shade** for 155 (shadow/assassin). Runehide's sources moved to dragons to avoid overlap.
1b. (12:25) **Source decided in principle: the extended hides come from new versions of creatures** (Chase: "possibly
   new versions of creatures"), not from stock ones. So stock creatures keep OSI's hides (faithful), and each
   leather has its own creature variants, ours, carrying F-14's level field. The family column in proposal 1 becomes
   the list of creatures to make variants of (for example a Cinder Hell Hound, a Rime Troll). Feature-sized: the
   creature work belongs in the features chat's queue, not here. (12:26) Chase decided: **for now, existing spawners
   produce a rare variant** (paragon-style roll) until the variants get their own locations; variants are
   **tougher than stock and look different** (hue and name prefix). (12:28) **Every variant always drops its
   leather** (Chase: yes).
2. Source: carved from creature families by theme (above), or one simpler rule (any hide creature, tier set by
   the creature's difficulty)?
3. Cloth: (12:28) Chase: **"let's play with a ladder and what it should look like, it might be a short ladder."**
   Draft below.

### Cloth ladder (draft, in play)

**What cloth is for.** Leather and metal are armor. Cloth makes the pieces **armor never covers**: cloak, robe,
sash or apron, shoes, shirt, pants, skirt or kilt, surcoat, plus the Gargish cloth armor. A fighter in full plate
still wears four or five cloth pieces. So the cloth ladder is the **utility layer** on top of any armor, and
leaves resists to leather and metal. Pinned clothing already carries `Attributes` and `Resistances`
(`Items/Clothing/BaseClothing.cs:35-74`), all zero on crafted pieces today.

**Short ladder: four silks** on every other rung of the shared ladder, plus the starter:

| Gate | Cloth | Theme | Normal | Exceptional adds |
|---|---|---|---|---|
| 45 | Gloomsilk (dungeon starter) | cosmetic, as decided | hue only | hue only |
| 100 | Moonsilk | calm, the caster's cloth | mana regen +1 | lower reagent cost 5 |
| 140 | Wardsilk | warding | one resist +2 (by dye: fire, cold, poison, energy) | defense chance +2 |
| 170 | Runesilk | arcane | spell damage +2 | faster cast recovery 1 (cloak and robe only) |
| 200 | Starsilk | pinnacle | luck +40, stamina regen +1 | hit point regen +1, one random extra from the three above |

**Watch the stacking.** Five or six cloth pieces stack, so per-piece numbers stay small; a full Starsilk outfit at
exceptional is about +200 luck and +5 or 6 to each regen. A per-outfit cap (for example "material bonuses from
cloth count on at most four pieces") is the alternative if that is too much.

**Where silk comes from.** Same rule as the leathers: rare, tougher, re-hued **spider variants** from existing
spawners (giant and dread spiders, the dungeon's spiders) drop **raw silk** of their tier, always. Spun at a
spinning wheel and woven on a loom like flax and cotton, so the cloth chain stays OSI's. The variants are part of
the same feature-queue item as the leather creatures.

**Gain.** Materials lift the gain window (gate - 100), as for metal and leather. A 121-ceiling cloth recipe in
Starsilk trains to about 221.

### Decided (Chase, 2026-10-02, 12:17 to 12:37)

- **Same pattern as smithing:** shared ladder, materials lift the gain window, thrift, master's durability, mark,
  tailor BODs on the ladder (F-18).
- **Eight extended leathers:** Stonehide 100, Etherhide 115, Cinderhide 130, Rimehide 140, Shadehide 155,
  Runehide 170, Voidhide 185, Starhide 200.
- **Source: new creature variants**, rare, from existing spawners for now (paragon-style), tougher than stock, own
  hue and name prefix, **always drop their leather**. Stock creatures keep OSI's hides.
- **Cloth ladder: four silks** (Moonsilk 100, Wardsilk 140, Runesilk 170, Starsilk 200) plus Gloomsilk, **themes and
  numbers as drafted**, **no stacking cap**, and **Gargish cloth armor takes the silk bonus** (12:37). Silk from
  spider variants under the same rule.
- Still to draft (overseer or the build prompt): the leather bonus rows (normal / exceptional adds), following
  F-28's wood table and F-29's gap.
- **Feature-queue item for the features chat:** the creature variants (leather families and spiders): rare
  variant roll on existing spawners, tougher, re-hued, name prefix, F-14 level field, guaranteed material drop.

---

## 55. Tinkering

### Today

- **Crafting gain** is the same passive recipe-window call (ours `CraftItem.cs:893-896`). Pinned's top window is
  80-130 (`Engines/Craft/DefTinkering.cs`); ours adds gem jewelry at 75-125 and Gargish jewelry to 115
  (`customizations\Engines\Craft\TinkeringCraftRegistrations.cs:60-107`). **Ceiling 130.**
- **Metals:** OSI ingots only, Iron 0 to Valorite 99 (`DefTinkering.cs:574-582`), and they change **only the hue**
  (jewelry `Items/Jewels/BaseJewel.cs:130-141`). Our 8 metals are not registered for Tinkering at all.
- **Tools:** exceptional tools get double uses (`Items/Skill Items/Tools/BaseTool.cs:73-80, :103`). Skill does
  nothing past exceptional.
- **Traps:** trap level = `(int)(Tinkering Value / 10)`, power = level x 9, **uncapped** (`DefTinkering.cs:663-668`).
  Explosion damage = 10-30 x level (`Items/Containers/TrappableContainer.ExecuteTrap.cs:65`), dart 5-15 x level
  (`:107`). At 200: level 20, explosion **200-600 fire**, dart 100-300. OSI's GM is level 10 (100-300).
- **Remove Trap trains on tinker traps:** `CheckTargetSkill(RemoveTrap, trap, TrapPower, TrapPower + 30)`
  (`Skills/RemoveTrap.cs:61`). So **a tinker's trap power is Remove Trap's main gain path**: power 90 (GM) trains
  Remove Trap to 120; power 180 (Tinkering 200) to 210.
- **Clockwork golems:** need Tinkering 60, strength scalar 0.6 to 1.0, flat from 100
  (`Items/Misc/ClockworkAssembly.cs:53-71`). Golem repair gains to 100.
- **Guild:** the Tinkers' Union (join at 50, `customizations\ClusterFGuildSystem.cs:136-141`). F-20 ports Tinkering
  BODs (Carpentry and Tinkering first, approved).

### Gain path to 200

Crafting 130, golem repair 100. **Nothing past 130.**

### What breaks

- **Trap damage at 200** (above): a trapped box one-shots most players. cc-P20 B5.
- Everything else clamps at 100 (golems) or exceptional (tools).

### Relevance

The tool maker for every crafter and gatherer, jewelry, traps (and through them Remove Trap), golems, and the
Tinkers' Union. Past 130 it has no recipes and its only scaling effect (traps) is the one that breaks.

### Synergies

- **Remove Trap** (traps train it), **Lockpicking** (tinkers make locks and lockpicks), **Mining and
  Blacksmithy** (the metal ladder), **every gatherer and crafter** (tools), **Animal Taming / companions**
  (golems are followers).

### Proposal

1. **Our 8 metals join Tinkering on the shared ladder**, and **materials lift the gain window** (gate - 100), same
   rule as smithing and tailoring. Tinkers climb to 200 by working the ladder.
2. **Jewelry becomes the metal's utility layer** (like cloth for leather): rings, bracelets and earrings take a
   small per-metal bonus from our metals, normal and exceptional lines with F-29's gap. OSI metals stay hue only
   (faithful). Rows drafted in the build prompt, themed to each metal.
3. **Traps split power from damage.** Trap power keeps scaling with Tinkering to 200 (so Remove Trap can train
   to about 210 on them); **damage caps at the GM value** (level 10: explosion 100-300, dart 50-150).
4. **Tools last longer with skill:** exceptional tools x2 uses (pinned), rising to x3 at 200.
5. **Golems scale past 100:** the scalar keeps climbing, 1.0 at 100 to 1.5 at 200, so a master tinker's golem is a
   real companion. (Pairs with the planned squire/mercenary companion system; check that design first.)
6. Thrift, master's durability (jewelry and tools) and the mark, as for smithing.

### Open questions for Chase

1. Jewelry as the metal's utility layer (proposal 2): yes? Or keep jewelry plain and give metals to tools only?
2. Trap damage capped at GM while power keeps scaling (proposal 3)?
3. Golems scaling to 1.5 at 200, or leave golems as OSI has them and let companions be a separate system?

### Decided (Chase, 2026-10-02, 12:41)

1. **Jewelry is the metal's utility layer** (proposal 2). Our 8 metals join Tinkering on the shared ladder, and
   materials lift the gain window (proposal 1, with it).
2. **Traps: overseer suggestion approved (Chase, 12:50).**
   - **Damage caps at OSI's GM value** (level 10: explosion 100-300 fire, dart 50-150, poison Lethal as today).
     Player hit points stay roughly OSI-sized even with uncapped stats (about 300 at 500 Str, cc-P20 1.4), so
     anything past GM is a one-shot box, mostly used on other players.
   - **Power keeps scaling with Tinkering to 200** (power 180), so a master's trap is much harder to disarm and
     trains Remove Trap to about 210. The skill shows up as "hard to beat", not "kills you".
   - **Noted for later (Chase, 12:50): new non-lethal trap types at 150 and 200**, for example an alarm trap (tells the owner who
     tripped it and where) and a binding trap (paralyzes for a few seconds). Gives high tinkers new tools for
     their homes and loot boxes without raising damage.
3. **Golems scale up:** strength scalar 1.0 at 100 to 1.5 at 200 (proposal 5).
4. Proposals 4 (tool uses x3 at 200) and 6 (thrift, durability, mark) stand as written (not objected).

---

## 57 / 52 / 51. The wood group: Lumberjacking, Carpentry, Bowcraft/Fletching

Done together: F-28 already decided the wood bonuses and the craft-gate ladder (Ironwood 100 ... Starwood 200 in
Carpentry and Fletching), and the Mining, Blacksmithy and Tailoring decisions set the pattern.

### Today

**Lumberjacking**
- Harvest: OSI woods Log (0/0/100) to Frostwood (100/60/140) (pinned `Engines/Harvest/Lumberjacking.cs:71-77`); our 8
  woods all **req 100**, windows 60-140 to 68-148 (ours `customizations\ClusterFLumberjackingExtension.cs:219-228`).
  10 logs a chop, 20 in Felucca (`Lumberjacking.cs:53-54`); fallback to plain logs 50 percent
  (`ClusterFLumberjackingExtension.cs:242-249`). Bonus finds (bark, fungi, switch, parasitic plant, amber) at 100,
  fixed odds (`Lumberjacking.cs:93-101`).
- Wood discovery gate: an unreported extended log comes out as a plain log until reported at the Foresters'
  guildmaster (`ClusterFLumberjackingExtension.cs:19-22`). The Foresters' Union gives a logbook and satchel
  (`customizations\ClusterFGuildSystem.cs:226, :468-473`).
- Axe combat: gains only to 100 (`Items/Weapons/BaseWeapon.cs:2547-2548`); damage bonus 0.2 percent per point plus 10 at
  GM, outside the 100 percent damage cap (`:2559-2560`): **+30 percent at 100, +50 percent at 200.**
- **Gain ceiling 148.**

**Carpentry:** recipes to 140.3 (tetsubo), Masonry 132, ours to 128.9; OSI wood gates 0/65/80/95/100
(`Engines/Craft/DefCarpentry.cs:601-607`); our 8 boards flat 100 (`ClusterFLumberjackingExtension.cs:274-281`).
**Ceiling 140.3.**

**Fletching:** recipes to 130 (yumi, repeating crossbow); same gates (`DefBowFletching.cs:264-270`, ours `:302-309`).
**Ceiling 130.**

### Two harvest findings (source read, not probed; for the overseer)

1. **Groves are not permanent.** Lumberjacking keeps pinned's `RandomizeVeins = Core.ML` (true); only Mining turns it
   off (`ClusterFMiningExtension.cs:131`). Each time a grove's bank respawns it re-rolls its wood
   (`Engines/Harvest/Core/HarvestBank.cs:61-64`). **That breaks the planned grove ledger teleport**, which assumes a
   recorded grove still holds the same wood (P13 decision, 2026-09-30).
2. **A fresh grove can never be one of our 8 woods.** With randomize on, a new bank picks from `Random(1000)`
   (`HarvestDefinition.cs:136-139`), but our woods sit at weights 1001-1036. They appear only after a bank has been
   cut down and respawned (`HarvestBank.cs:63` uses the full 1036). Mining avoided this by turning randomize off.
   Fix for both: turn randomize off for lumber, as Mining does (the seed already spans 1036).

### What breaks

Nothing in Carpentry or Fletching (they clamp). Lumberjacking's axe bonus reaches +50 percent at 200, outside the
damage cap (+70 percent at 300, cc-P20 B2); inflated, not broken.

### Relevance and synergies

The wood economy: Carpentry (furniture, staves, shields, house add-ons, Masonry through Mining's granite),
Fletching (bows, arrows and F-28's wood bonuses), the Foresters' Union, the grove ledger. Lumberjacking is also a
fighter skill through axes, which pairs it with Swords and Tactics.

### Proposal (the same pattern, applied)

1. **Lumberjacking on the shared ladder:** each of our 8 woods gets the ladder req (Ironwood 100 ... Starwood 200)
   and trains to about req + 45 (Ironwood 100/60/145 ... Starwood 200/160/245), as decided for ore.
2. **Lumberjacking rewards past 100,** mirroring Mining:
   a. Truer groves: fallback from 50 percent at 100 to 25 percent at 200, plus a **plain-log toggle** for bulk logs.
   b. Richer chops: up to +50 percent logs per chop at 200 (10 logs a chop makes "+1" meaningless).
   c. Better finds: bonus-find odds (bark, amber and the rest) rise to about double at 200.
   d. Survey: use the axe on a tree (context menu, Lumberjacking 100) to learn its wood without chopping; it goes
      into the grove ledger. No skill gain, short cooldown.
3. **Carpentry and Fletching:** materials lift the gain window (gate - 100), thrift, master's durability, mark, as
   for smithing. **Fletching's thrift is extra arrows and bolts** (up to +25 percent per craft at 200).
4. **Turn off grove re-rolling** (findings 1 and 2).
5. **Axe bonus:** keep pinned's formula (+50 percent at 200, a lumberjack-fighter perk), or cap it at GM's +30.

### Open questions for Chase

1. Proposals 1 to 3: the same pattern for all three? (Expected yes.)
2. Lumberjacking rewards a to d, and the plain-log toggle?
3. Axe bonus: keep +50 percent at 200, or cap at +30?

### Decided (Chase, 2026-10-02, 12:54)

- **Groves are permanent** (Chase). **Going into P37** (Chase, 13:33). Turn off lumber vein re-rolling, as Mining does; this also lets fresh groves
  hold our 8 woods. A defect-sized fix for the overseer, needed by the grove ledger teleport.
- **Same pattern for all three** (proposals 1 and 3): ladder windows for our woods, materials lift the gain window,
  thrift (Fletching: extra arrows and bolts), master's durability, mark.
- **Lumberjacking rewards a to d and the plain-log toggle:** yes.
- **Axe bonus: do not cap.** Pinned's formula stays (+50 percent at 200, outside the damage cap). Recorded as a
  deliberate choice, not an oversight.

---

## 58 / 53. Fishing and Cooking

Done together: fish are Cooking's natural ladder, the way ore is smithing's.

### Today

**Fishing (pinned, nothing of ours changes it)**
- One resource: Fish (0 / 0 / 100) (`Engines/Harvest/Fishing.cs:98-101`). **Gain ceiling 100. It cannot pass GM by
  play at all.**
- Deep-water specials, each `(Value - 80) / 4000` and checked in order: special net, big fish, treasure map,
  message in a bottle (`:15-18`, roll `:170-190`). About 3 percent each at 200. Magic fish and shoes stop at 125
  and 105 (`:19-29`).
- Treasure maps from fishing are always level 1 (0 for Young on Haven) (`:215-228`). White pearls at 80, 0.6 percent
  (`:113-116`).
- Guild: a fishers' guild exists (join at Fishing 30, `customizations\ClusterFGuildSystem.cs:208-212`).

**Cooking:** recipes to 130 (green tea, `Engines/Craft/DefCooking.cs`). **Nothing in pinned or ours reads Cooking**
outside its recipes: food only fills hunger. Ceiling 130, and no reason to train it.

**Port source found:** ServUO pub57 has OSI's **High Seas fishing** (`Scripts\Services\Expansions\High Seas\Items\Fish\`):
- 16 rare and 19 legendary fish by region, skill 82 to 120 (`FishInfo.cs:18-54`; for example Lava Fish in the Abyss
  at 110, Winter Dragonfish in the Ice at 120).
- Bait, hooks, lobster and crab traps, trophies.
- Fish raises to 120 (`Scripts\Services\Harvest\Fishing.cs:88`).
- **Fish pies:** each rare fish cooks into a pie with a 5-minute buff (`FishPies.cs:30-160`). That is Cooking's
  OSI job, and pinned lacks it.

### Proposal

**Fishing**
1. **Port High Seas fishing** (OSI content, faithful): rare and legendary fish by region, bait, hooks, traps,
   trophies. Fishing then trains to 120 by OSI's own rules.
2. **Above 120, our own fish on the shared ladder:** eight deep fish, gates 100 / 115 / 130 / 140 / 155 / 170 / 185 / 200,
   each found in one kind of water (lava, ice, swamp, deep sea, dungeon lakes including New Haven's), windows to
   gate + 45. Themed to match their ore, wood and leather partners.
3. **Rewards past 100:** treasure maps from fishing rise in level with skill (level 1 at 100, up to level 3 at
   200); special-catch odds keep their pinned formula; plus a plain-fish toggle like iron-only.

**Cooking**
4. **Port the fish pies** with High Seas: Cooking's first real use.
5. **Our dishes on the ladder:** our eight fish, plus **meat from the creature variants** (a Cinder Hell Hound gives
   cinder meat as well as Cinderhide), cook into dishes with buffs. Materials lift the gain window (gate - 100), so
   Cooking climbs to 200 by cooking the ladder.
6. **One food buff at a time** (as OSI's pies work), with duration rising with the cook's skill (5 minutes at 100, up to
   15 at 200). Exceptional dishes get a stronger line (F-29's gap).
7. Thrift (a chance for an extra serving) and the mark ("Master chef X") as for the other crafts.

### Open questions for Chase

1. Port High Seas fishing (and its fish pies) as the base: yes?
2. Our eight fish above 120 on the shared ladder: yes? Any water types or places you want in it?
3. Cooking dishes from our fish and the variant creatures' meat, one buff at a time: yes? (Fits the cultivation
   feel: meals as power, the way Alchemy could do pills.)
4. Treasure map level rising with Fishing skill: yes?

### Decided (Chase, 2026-10-02, 13:33)

All four approved: **port High Seas fishing** (rare and legendary fish, bait, hooks, traps, trophies, fish pies);
**our eight fish above 120** on the shared ladder, by water type; **Cooking dishes** from our fish and the variant
creatures' meat, materials lifting the gain window, **one food buff at a time**, duration 5 to 15 minutes by skill,
exceptional stronger; **treasure map level rises with Fishing** (1 at 100 to 3 at 200). The plain-fish toggle,
thrift (extra serving) and the mark stand as proposed. Fish names, water types and dish buffs to draft in the
build prompt. Variant meat joins the creature-variant feature-queue item.

---

## 49. Alchemy (with Glassblowing)

### Today

- **Crafting gain** is the recipe-window call. Potions top out at 140 (deadly poison, `Engines/Craft/DefAlchemy.cs`),
  Glassblowing at 150 (hollow prism, needs Alchemy 100 and the book, cc-P20 2.5). **Ceiling 150.**
- **Potion strength reads Alchemy:** `EnhancePotions = item EP (capped 50) + (int)(Alchemy Value x 10 / 33)`, the
  skill part **uncapped** (pinned `Items/Skill Items/Magical/Potions/BasePotion.cs:206-217`). Skill part: +36 percent
  at 120, **+60 percent at 200**. With 50 item EP at 200: Greater Heal about 42-52 per drink, Greater Conflagration
  about 60 fire per second, explosion bonus +40 fire, Greater Cure much more likely on Lethal. Inflated, not broken
  at 200 (cc-P20's breaks are at 300+).
- **Infused Alchemist's Gem** (ours): `Alchemy.Base += 1` with no cap check
  (`customizations\Items\Artifacts\Consumables\InfusedAlchemistsGem.cs:28`). No drop source references it
  (grep 2026-10-02), so staff-only today. Defect-sized: should obey the cap.
- **Guild:** the Arcane Society (`customizations\ClusterFGuildSystem.cs:116`) per F-20's homes for Alchemy and
  Inscription.

### Relevance

Potions for everyone, poisons for Poisoning, and (per Chase's vision) **the natural home of cultivation**: pills and
elixirs are the genre's core progression item. Today there is nothing past 150 and no reason past about 120 except
potion strength.

### Synergies

Mining (sand for glass, and the gems from decision c), Lumberjacking's bonus finds (amber, fungi, parasitic plant),
Fishing and the creature variants (rare parts), Poisoning, Healing (potions back it up), Cooking (food buff and
elixir buff are separate slots).

### Proposal

1. **Elixirs on the shared ladder: eight cultivation-style elixirs** (gates 100 / 115 / 130 / 140 / 155 / 170 /
   185 / 200), each needing a glass flask (Glassblowing, so sand finally matters) and ingredients from the gathering
   ladders: gems, grove finds, rare fish, variant creature parts. Gain windows to gate + 45, so Alchemy climbs to 200
   by brewing them.
2. **What elixirs do (one elixir buff at a time, separate from food):** long timed buffs, 30 to 60 minutes, themed by
   tier. The upper tiers carry the cultivation hook: **"breakthrough" elixirs** that raise skill or level gain for
   their duration (stacking with loop memory), so an alchemist sells the thing every grinder wants.
3. **Potion strength: keep pinned's formula** (+60 percent at 200), in line with "no caps" for stats and the axe;
   or cap the skill part at its 120 value (+36 percent).
4. **Glassblowing on the ladder too:** flask quality by skill (better flasks = longer elixirs), so Glassblowing
   trains past 150 with the elixir tiers.
5. **Thrift:** chance to keep the reagents on a successful brew, 0 at 100 to 25 percent at 200.
6. **Overseer item:** the Infused Alchemist's Gem obeys the cap (or goes).

### Open questions for Chase

1. Cultivation elixirs as Alchemy's ladder: yes? Breakthrough elixirs that speed skill and level gain: yes, or too
   close to selling progression?
2. Potion strength: uncapped (+60 percent at 200) or capped at the 120 value?
3. Elixir and food as two separate buff slots, or one shared slot?

### Answers (Chase, 2026-10-02, 14:12)

1. **Cultivation elixirs: yes**, breakthrough elixirs included. **And "make Alchemy great again": the healing
   numbers are pitiful once stats get high.**
2. **Potion strength uncapped** (pinned formula stays).
3. **One shared buff slot** for food and elixirs ("no separate slots").

### Making potions keep up (overseer proposal, open)

**Why they fall behind.** Heal potions heal flat numbers: Lesser 6-8, Heal 13-16, Greater 20-25, times
`1 + EnhancePotions` (`Heal Potions/*.cs:13-15`, `BasePotion.cs:242`). Player hit points grow with Str:
`Str / 2 + 50 + bonus hits (25 max)` (pinned `Mobiles/PlayerMobile.cs:548-576`). OSI balanced the potion against
about 150 HP: a Greater Heal at GM is about 27-34, roughly a fifth of a bar. Here a 500 Str character has about
325 HP (more with effective Str above 500), and the same potion at Alchemy 200 with 50 item EP heals 42-52, about
an eighth. Stat potions have the same problem: Greater Strength is a flat +20 (`GreaterStrengthPotion.cs:14`),
which is nothing at 500 Str.

**Proposal: potions scale with the drinker, so they feel like OSI's at any stat level.**
1. **Heal potions heal OSI's share of the bar:** the base numbers are multiplied by `HitsMax / 150` (never below 1),
   then by `1 + EnhancePotions` as today. At 325 HP that is x2.17: a Greater Heal at Alchemy 200 with 50 EP heals
   about 91-114. A 150 HP character sees exactly OSI's numbers.
2. **Stat potions scale the same way:** the offset is multiplied by `raw stat / 100` (never below 1). A 500 Str
   character's Greater Strength gives +100 before EP, about +210 at Alchemy 200 with 50 EP.
3. **Refresh and Cure are already proportional or chance-based** (refresh restores a share of stamina), no change.
4. **Explosion and conflagration** stay on pinned's formula (uncapped, per answer 2); monster HP is F-14's job.
5. **Heal-over-time elixirs** fill the gap between potions: a tier of elixirs (decision 1) restores a share of max HP
   every few seconds for their duration, so an alchemist's supply carries a long fight.

6. **An emergency tier** (Chase, 14:13: "potions need to be emergency items again or a valid way to heal"): a
   Supreme Heal elixir that restores about half the bar at once, on its own long cooldown (for example 2 minutes)
   separate from the 10 s heal-potion timer, so it is the "oh no" button and ordinary heal potions stay the
   steady way to heal.

**Approved (Chase, 14:14): 1 to 6**, the `/150` and `/100` anchors included.
