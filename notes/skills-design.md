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
| 57 | Lumberjacking | Gathering | not started |
| 58 | Fishing | Gathering | not started |
| 50 | Blacksmithy | Crafting | in discussion |
| 54 | Tailoring | Crafting | not started |
| 55 | Tinkering | Crafting | not started |
| 52 | Carpentry | Crafting | not started |
| 51 | Bowcraft/Fletching | Crafting | not started |
| 53 | Cooking | Crafting | not started |
| 49 | Alchemy | Crafting | not started |
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
