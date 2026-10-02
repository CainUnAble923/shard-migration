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
| 17 | Inscription | Crafting | **decided** 2026-10-02 |
| 23 | Imbuing | Crafting | **decided** 2026-10-02 |
| 1-6 | Swords, Macing, Fencing, Archery, Throwing, Wrestling | Combat | **decided** 2026-10-02 |
| 7 | Tactics | Combat | **decided** 2026-10-02 |
| 8 | Anatomy | Combat | **decided** 2026-10-02 |
| 9 | Parry | Combat | **decided** 2026-10-02 |
| 10 | Bushido | Combat | **decided** 2026-10-02 |
| 11 | Focus | Combat | **decided** 2026-10-02 |
| 12 | Arms Lore | Combat | **decided** (F-26, 2026-10-02) |
| 33 | Healing | Combat support | **decided** 2026-10-02 |
| 13 | Magery | Magic | **decided** 2026-10-02 |
| 14 | Evaluating Intelligence | Magic | **decided** 2026-10-02 |
| 15 | Resisting Spells | Magic | **decided** 2026-10-02 |
| 16 | Meditation | Magic | **decided** 2026-10-02 |
| 18 | Necromancy | Magic | **decided** 2026-10-02 |
| 19 | Spirit Speak | Magic | **decided** 2026-10-02 |
| 20 | Chivalry | Magic | **decided** 2026-10-02 |
| 21 | Spellweaving | Magic | **decided** 2026-10-02 |
| 22 | Mysticism | Magic | **decided** 2026-10-02 |
| 24 | Ninjitsu | Magic | **decided** 2026-10-02 |
| 37 | Animal Taming | Animal | **decided** 2026-10-02 |
| 38 | Animal Lore | Animal | **decided** 2026-10-02 |
| 34 | Veterinary | Animal | **decided** 2026-10-02 |
| 39 | Herding | Animal | **decided** 2026-10-02 |
| 40 | Musicianship | Bard | **decided** 2026-10-02 |
| 41 | Peacemaking | Bard | **decided** 2026-10-02 |
| 42 | Provocation | Bard | **decided** 2026-10-02 |
| 43 | Discordance | Bard | **decided** 2026-10-02 |
| 25 | Hiding | Thief | **decided** 2026-10-02 |
| 26 | Stealth | Thief | **decided** 2026-10-02 |
| 27 | Detect Hidden | Thief | **decided** 2026-10-02 |
| 28 | Snooping | Thief | **decided** 2026-10-02 |
| 29 | Stealing | Thief | **decided** 2026-10-02 |
| 30 | Lockpicking | Thief | **decided** 2026-10-02 |
| 31 | Remove Trap | Thief | **decided** 2026-10-02 |
| 32 | Poisoning | Thief | **decided** 2026-10-02 |
| 44 | Tracking | Utility | **decided** 2026-10-02 |
| 45 | Item Identification | Utility | **decided** 2026-10-02 |
| 46 | Taste Identification | Utility | **decided** 2026-10-02 |
| 47 | Camping | Utility | **decided** 2026-10-02 |
| 48 | Cartography | Utility | **decided** 2026-10-02 |
| 35 | Begging | Utility | **decided** 2026-10-02 |
| 36 | Forensic Evaluation | Utility | **decided** 2026-10-02 |

Numbers are cc-P20's row numbers (`notes\cc-P20-skill-scaling-research.md:322-381`).

## Ready for the overseer

**Gathering and crafting, decided 2026-10-02:** Mining, Lumberjacking, Fishing, Blacksmithy, Tailoring,
Tinkering, Carpentry, Bowcraft/Fletching, Cooking, Alchemy, Inscription, Imbuing. Each section's "Decided" block is the spec. Cross-cutting
pieces worth one prompt each:
- **The shared ladder** (ore, ingot, wood, leather, cloth, fish, elixir tiers at 100 / 115 / 130 / 140 / 155 / 170 /
  185 / 200) and **"materials lift the gain window"** (shift = gate - 100) across all crafts.
- **Harvest rewards** (truer veins and groves, richer yields, better finds, prospect and survey, plain-resource
  toggles); permanent groves are already in P37.
- **Thrift, master's durability and the master's mark** across crafts (Hammer of Hephaestus T3/T4 thrift).
- **Feature-queue item (features chat):** the creature variants for leather, silk and meat.
- **Ports:** High Seas fishing and fish pies (ServUO pub57).
- **Defect-sized:** large BOD lock-out, Infused Alchemist's Gem cap.

Inscription and Imbuing decided 2026-10-02 (15:44): **the crafting and gathering group is complete.**

**Combat, decided 2026-10-02 (16:03):** weapon skills, Tactics, Anatomy, Parry, Bushido, Focus, Healing. Prompt-sized
pieces: the gain fixes (skill-only weapon gain roll, Bushido/Focus/bandage windows to the cap); block rework (shields
read Parry only, shield curve doubled past 120, cap 75 / 90 with Evasion); bandage HP scaling at half; Throwing and
Wrestling in the special-move mana discount.

**Magic, decided 2026-10-02 (16:11):** Magery, Eval Int, Resisting Spells, Meditation, Necromancy, Spirit Speak, Chivalry,
Spellweaving, Mysticism, Ninjitsu. Pieces: gain to the cap for the seven stuck schools; school mastery (mana -20 percent
at 200, after and outside LMC); heal spells at full HP scaling with their clamps scaled; **port** the missing Mysticism
and Spellweaving spells (ServUO pub57); Mysticism casts gain Imbuing/Focus.

**Animal, decided 2026-10-02 (16:30):** Taming, Animal Lore, Veterinary, Herding. Pieces: **port** the 25 missing
tamable creatures and **OSI Pet Training** (ServUO pub57); tamable variants on the ladder (with the variant feature
item); Lore pet-growth bonus and breeding handoff; Vet removes resurrection skill loss; the **Drover's Handbook**
(Corral, Calm, Herd, Lure); **Beastcraft** (Taming craft system); stable slots from max level (F-12).

**Bard, decided 2026-10-02 (16:47):** Musicianship, Peacemaking, Provocation, Discordance. Pieces: gain to the cap (our
above-160 creatures carry bard difficulty from their level); success capped 90 percent (85 vs bosses and champions);
Discordance effect 28 at 120 to 40 at 200; bard range capped at 18; durations double by 200; Fire Horn unchanged.

**Thief, decided 2026-10-02 (16:53):** Hiding, Stealth, Detect Hidden, Snooping, Stealing, Lockpicking, Remove Trap,
Poisoning. Pieces: gain to the cap (Meditation pattern for five; Stealing on creature level; Lockpicking on ladder
locks); fixes (Hiding combat range floor 8, Stealing 5 percent caught floor, DH range 18 plus guard floor, the pinned
`Poison.IncreaseLevel` bug); mastery rewards; **higher poisons** Virulent / Baneful / Plague with Alchemy antidotes.

**Utility, decided 2026-10-02 (17:00):** Tracking (con color and health on the arrow, stealth footsteps at 150,
variants at 200), Appraisal (loot hints 150, weakest resist 200), Taste ID (connoisseur), Camping (regen aura,
dungeon camps at 150, private party camp plots at 175), Cartography (treasure maps 7 and 8, Cartography widens the dig
and gives warmer/colder, extents clamped), **Begging renamed Persuasion** (temporary vendor discounts while training,
permanent 30 percent at 200, guild stores included), Forensics (bigger carves, rare parts).

**All 58 skills are decided.**

## Corrections to earlier notes, found while verifying

- **D42 is fixed, not live.** `f12-levels-loops-caps.md` still lists it under "still required"; ours
  `customizations\SmithGuildSalvageBag.cs:113-133` clamps the return at `cost - 1` (cc-P23).
- **cc-P20's Raptor is not in our tree.** P20 cites `customizations\Mobiles\Normal\Raptor.cs:50` (MTS 107.1); no
  `class Raptor` exists anywhere under `D:\ShatteredLegacy\server` today (grep 2026-10-02). It is a ServUO creature still
  to port (below, Animal section).
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

---

## 17. Inscription

### Today

- **Crafting gain:** recipe windows; top is the Mystic spellbook at 50-150 (`Engines/Craft/DefInscription.cs`, cc-P20).
  **Ceiling 150.** Scroll success clamps at 100 percent; no material tiers (blank scrolls only).
- **Spell damage bonus** for every caster: `(fixed + 1000 x (fixed / 1000)) / 200` percent (pinned
  `Spells/Base/Spell.cs:222-224`): +10 at 100, +11 at 120, **+20 at 200** (integer step at each 100). Same for weapon
  hit spells (cc-P20).
- **Reactive Armor, Magic Reflect, Protection** read it: Reflect's physical malus `-25 + Insc / 20`
  (`Spells/Fifth/MagicReflect.cs:86`) and Protection's `-15 + Insc / 20`, `-35 + Insc / 20`
  (`Spells/Second/Protection.cs:138-139`) are still maluses at 200 (-15, -5, -25). They flip at 300 and 500, so
  **nothing breaks at 200.**
- Runebook charges `min(5 + quality + Insc / 30, 10)` clamp at 10.
- **Crafted spellbook properties read Magery, not Inscription:** count by Magery tier up to "legend" at 120
  (`Items/Skill Items/Magical/Spellbook.cs:168-209`).
- Guild: the Arcane Society; F-20 ports Inscription BODs there.

### Relevance and synergies

Every caster wants it (spell damage), scribes sell scrolls and spellbooks. Pairs with Magery, Necromancy,
Mysticism, Spellweaving (books), and now Tailoring's leather ladder (below).

### Proposal

1. **Vellum on the shared ladder.** Hides from the leather ladder (Stonehide to Starhide) are scraped into vellum
   for spellbooks and scrolls. Materials lift the gain window (gate - 100), so scribes climb to 200 by working the
   ladder, and **spellbooks on vellum carry the leather's caster line** (normal and exceptional, F-29 gap).
2. **Spellbook properties past 120:** keep Magery setting the property count (more tiers at 150 and 200), and let
   **Inscription set the intensity**, so the best books need a mage and a scribe (or one character who is both).
3. **Master's scrolls:** a scroll scribed at 150+ has a chance not to be used up when cast from, 0 at 150 to
   25 percent at 200 (the scribe's thrift lives in the product).
4. **Runebooks:** charge cap rises with Inscription, 10 at 100 to 20 at 200.
5. Spell damage bonus stays pinned's (uncapped, +20 at 200). Thrift on blank scrolls and reagents, and the mark,
   as for other crafts.

---

## 23. Imbuing (ours: the Artificers' guild)

### Today

- **Imbue success:** `CheckSkill(Imbuing, diff - 20, diff + 20)` with difficulty 40 to 100-120 by property and
  guild standing (ours `customizations\ArtificersImbueGump.cs:1405`, difficulty `:84-93`). Disenchant and essence
  crafting gain only to 80 (`:1483`, `:1545`). **Ceiling 140.**
- **Power comes from guild standing, not skill:** intensity cap 100 to 200 percent and 5 to 8 property slots by
  standing (`:1686-1700`). Past 140 the skill does nothing for imbuing.
- **Mysticism damage reads the higher of Imbuing and Focus** (pinned `Spells/Mysticism/MysticSpell.cs:42-44`), so
  the points do count there.

### Proposal

1. **Materials lift the imbue window:** imbuing an item made of a ladder material adds (gate - 100) to the
   difficulty, so working on Celestial, Starwood or Starhide gear trains Imbuing to 200. Standing still sets the
   ceilings.
2. **Skill earns on top of standing:** +1 property slot at 150 and +2 at 200, and essence-shard thrift (up to 25
   percent fewer shards at 200). Standing stays the main gate; skill rewards the master.
3. Mysticism's read stays as is.

### Open questions for Chase

1. Inscription: vellum from the leather ladder, spellbooks carrying the leather's caster line: yes?
2. Spellbooks: Magery sets count, Inscription sets intensity: yes?
3. Master's scrolls (chance not consumed) and runebook charges to 20: yes?
4. Imbuing: material-lifted difficulty, and +1/+2 slots from skill on top of standing: yes?

### Decided (Chase, 2026-10-02, 15:44)

All four approved: **vellum from the leather ladder** (spellbooks carry the leather's caster line); **spellbooks:
Magery sets count (new tiers at 150 and 200), Inscription sets intensity**; **master's scrolls** (0 to 25 percent not
consumed, 150 to 200) and **runebooks to 20 charges** at 200; **Imbuing: material-lifted difficulty, +1 slot at 150
and +2 at 200, shard thrift to 25 percent.** Thrift and the mark for Inscription as for other crafts.

---

## Combat: weapon skills, Tactics, Anatomy, Parry, Bushido, Focus, Healing

Numbers at the 200 cap, with Str 500 where it matters (stats are uncapped, D-101/D-102). Pinned formulas verified
2026-10-02; the per-use tables are cc-P20 section 2.1 and the Healing table at 2.3.

### Today: gain ceilings

| Skill | Gain call | Reaches 200 by play? |
|---|---|---|
| Swords, Macing, Fencing, Archery, Throwing, Wrestling | `CheckSkill(skill, hitChance)` (`Items/Weapons/BaseWeapon.cs:1365`); hit chance `(atk+20)(100+HCI) / 2(def+20)(100+DCI)` | Yes vs targets of skill 90+ (ceiling `2 x def + 20`), **but HCI lowers it**: with 45 HCI the ceiling vs a 100-skill monster is about 145 |
| Tactics, Anatomy | `CheckSkill(x, 0, Cap)` on every hit (`:2540, :2543`) | Yes, follows the cap |
| Parry | direct chance on block (`:1540, :1581`) | Yes with a shield (ceiling 380) |
| Bushido | moves: `req - 12.5 .. req + 37.5` (`Spells/Base/SamuraiMove.cs:9`), Momentum Strike `70..120` (`Spells/Bushido/MomentumStrike.cs:67`) | **No, stops at 120** |
| Focus | bonus-skill chance with `v = sqrt(Focus x 0.005)` (ours `customizations\RegenRates.cs:36`) | **Barely:** v reaches 1.0 at 200, so the gain chance falls to zero just as it gets there |
| Healing (and Anatomy on bandages) | `CheckSkill(x, 0, 120)` per bandage (`Items/Skill Items/Misc/Bandage.cs:444-445`) | **No, stops at 120** |

### What 200 does (all uncapped, in line with "no caps")

- **Damage:** Tactics +131 percent, Anatomy +105, Str +155, plus 100 item DI: about **x5.9** a hit (cc-P20 2.1;
  "no caps apply", `BaseWeapon.cs:2552-2602`). F-14's creature levels are where monsters keep up.
- **Being hit:** a 100-skill monster hits a 200 fighter 27 percent of the time (no DCI). Fine.
- **Bushido at 200:** Confidence about 21 HP/s, Honorable Execution heals about 103 per kill, Lightning Strike ignores
  armor 56 percent, Momentum Strike +100 percent, Evasion 10 s on a 20 s cooldown. All fine at our HP.
- **Focus at 200:** about 2.2 stamina/s and 10 mana regen points. Fine.
- **Healing 200 / Anatomy 200:** 69-117 per bandage (avg about 93), about 29 percent of a 325 HP bar; self-bandage is
  instant from Dex 220 (P25 decision 4).

### The one break inside 200: Parry + Bushido + Evasion

- With no shield, block chance is `Parry x Bushido / 48000 + 0.05` (one-handed, `BaseWeapon.cs:1550-1552`): **88 percent
  at 200 / 200** (OSI 120/120: 35 percent).
- Evasion multiplies it by `1.16 + (Bushido - 60) x 0.004` (cc-P20, `Spells/Bushido/Evasion.cs:175-204`): x1.72 at 200,
  so **100 percent block for 10 s of every 20**. While Evasion is up, a block also stops single-target spells and fire
  breath. Every enemy swing also triggers Confidence's heal on block.
- With a shield, Parry 200 alone is 55 percent: fine.

### Proposal

1. **Gain fixes, so every combat skill trains to the cap by fighting:**
   a. Weapon skills: the gain roll uses the **skill-only** hit chance (no HCI or DCI), so gear never stalls training.
      The actual hit still uses the full chance.
   b. Bushido: move gain windows run to the player's cap (the Meditation pattern), Momentum Strike included.
   c. Focus: clamp v at 0.95 so the gain chance never hits zero.
   d. Healing and the bandage Anatomy check: windows run to the cap.
2. **Damage, Bushido effects, Focus and Healing amounts stay pinned's, uncapped.**
3. **Block chance gets a ceiling:** final block chance capped at **85 percent**, Evasion included. The one place a
   chance passes 100 percent and becomes immunity; everything else stays open.
4. **Throwing and Wrestling join the special-move mana discount** (`Items/Weapons/Abilities/WeaponAbility.cs:182-191`
   lists the other weapon skills but not these two). A gap fix.
5. **Healing:** keep pinned's amount (about 93 at 200, instant self-bandage from Dex 220). Scaling it by HitsMax like
   potions would make it about 200 a bandage, and with instant self-bandages that is close to unkillable.

### Open questions for Chase

1. Gain fixes a to d: yes?
2. Block chance capped at 85 percent (Evasion included), or a different number, or no cap?
3. Healing: keep pinned's numbers (proposal 5), or scale them like potions despite instant self-bandages?
4. Throwing and Wrestling in the special-move mana discount: yes?

### Answers (Chase, 2026-10-02, 15:59)

1. **Gain fixes a to d: yes.**
2. **Block cap: Chase asked for a proposal.** Overseer proposal, to confirm:
   - **Block chance capped at 75 percent normally, and 90 percent while Evasion is up.** At 200/200 with no shield
     that is 75 percent all the time and 90 percent in the Evasion window (instead of 88 and 100); a shield at Parry
     200 (55 percent) is untouched. Evasion keeps a real job (the burst window), nothing is ever immune, and since
     Evasion's spell dodge uses the same roll, single-target spells get through at least 10 percent of the time.
   - For scale, OSI's best (Parry and Bushido 120, no shield) is 35 percent, about 49 percent with Evasion.
3. **Healing: scale like potions, but less.** Overseer proposal, to confirm: **half the potion scaling**, multiplier
   `1 + (target HitsMax / 150 - 1) / 2` (never below 1). At 325 HP that is x1.58: Healing 200 / Anatomy 200 heals about
   109-185 a bandage (avg about 147, about 45 percent of the bar), against a Greater Heal potion's 91-114 every 10 s.
   Same rule for Veterinary on pets (their HitsMax). Note: with self-bandages instant from Dex 220 (P25), the **rate**
   is the lever if playtests show unkillable self-healers, not the amount.
4. **Throwing and Wrestling in the special-move mana discount: yes.**

**Parry and Bushido together (Chase asked, 16:01).** Pinned `CheckParry` (`BaseWeapon.cs:1503-1585`), Dex 80+:

| Setup | 120/120 (OSI) | 200 Parry / 100 Bushido | 200 / 200 | 200 / 200 with Evasion |
|---|---|---|---|---|
| Shield | 5 percent (Bushido subtracts) | 30 | **5** | 9 |
| No shield, one-handed | 35 | 47 | 88 | 100+ |
| No shield, two-handed | 40 | 54 | **100+ even without Evasion** | 100+ |
| Shield, Parry 200, Bushido 0 | (55 at 200) | | | (no Evasion without Bushido) |

- **With a shield, Bushido subtracts:** `(Parry - Bushido) / 400 + 0.05` (`:1520`). OSI's rule, faithful, but on a shard where
  every character ends with every skill at 200, **a maxed character's shield blocks 5 percent**, so shields die as a
  choice for everyone in the late loops.
- **Two-handed at 200/200 passes 100 percent without Evasion** (divisor 41140, `:1550`).

**Revised overseer proposal, to confirm:**
- **Shields read Parry only on our shard** (drop the Bushido subtraction; a deviation, because every character
  maxes everything). Shield at Parry 200: 55 percent, with Evasion about 95.
- **One cap for every path: 75 percent normally, 90 percent while Evasion is up.** So at 200/200: shield 55 (90 with
  Evasion), no shield 75 (90 with Evasion), two-handed 75 (90). Shield, one-hand and two-hand all stay real choices.

### Decided (Chase, 2026-10-02, 16:03)

- **Block:** shields read Parry only (no Bushido subtraction); **cap 75 percent normally, 90 percent during Evasion**,
  every path.
- **Shield block boosted past 120** (Chase: "might boost base parry with shield as the skill is 200 vs 100").
  Overseer default: **OSI's curve to 120, then twice as steep:** `Parry/400 + 0.05` up to 120 (35 percent, faithful),
  then `+ (Parry - 120) / 200`, so 55 percent at 160 and **75 percent (the cap) at 200**. A maxed shield user sits at
  the cap without needing Bushido; Evasion lifts it to 90.
- **Bandage healing: half the potion scaling** (`1 + (HitsMax / 150 - 1) / 2`), Veterinary on pets the same.
- Gain fixes a to d, uncapped damage and Bushido effects, Throwing and Wrestling in the mana discount, as answered.

---

## Magic: Magery, Eval Int, Resisting Spells, Meditation, Necromancy, Spirit Speak, Chivalry, Spellweaving, Mysticism, Ninjitsu

Per-spell tables are cc-P20 section 2.2 (cited there); numbers below recomputed at the 200 cap with Int up to 500.

### Gain ceilings

| Skill | Ceiling | Why |
|---|---|---|
| Eval Int, Spirit Speak | cap | the damage skill gains on every cast up to its cap (`Spells/Base/Spell.cs:623-626`) |
| Meditation | cap (active, ours `Meditation.cs:111`) | passive regen check stalls at 200 like Focus (`RegenRates.cs:36`) |
| **Magery** | **120** | 8th circle window 80-120 (`Spells/Base/MagerySpell.cs:15-17`) |
| **Resisting Spells** | **130** | gains only while below a per-circle limit (`MagerySpell.cs:77-83`) |
| **Necromancy** | **120** | req + 40 (`NecromancerSpell.cs:37-41`) |
| **Chivalry** | **115** | req + 50; the High Seas Divine Fury tier needs 120 and **cannot be earned** (`DivineFury.cs:46`) |
| **Spellweaving** | **117.5** | req + 37.5 |
| **Mysticism** | **120.5** | req + 37.5; casting gains Eval Int, not Imbuing/Focus (cc-P20 quirk) |
| **Ninjitsu** | **137.5** | Animal Form Ki-rin and Unicorn |

### What 200 does (nothing breaks inside 200)

- **Spell damage** (Eval 200, Inscription 200, Int 500): about **x3.6** OSI's base, Energy Bolt about 153 before
  resists (46 through 70). In line with uncapped damage; F-14 scales monsters.
- **Resisting Spells 200 vs a 200 caster:** about 62 percent on an 8th-circle check, 74 on Poison. Not immune (that needed
  300). Resist floor 60 on all five resists.
- **Meditation 200, Int 500:** about 3 mana/s passive. Fine against 500+ mana pools.
- **Spirit Speak 200:** Strangle about 370 over 65 s, Wraith leech 35 percent, Revenant resists in the 70s. Fine.
- **Ninjitsu 200:** Feint cuts the target's damage 84 percent for 6 s (100 percent needs 237); Dog/Cat form regen about
  6.7 HP/s outside the item cap. Strong, not broken.
- **The heals are the weak spot again,** like potions: Greater Heal 81-90, Heal 17-20, Close Wounds **clamped at 39**,
  Noble Sacrifice and Holy Light **clamped at 24** (OSI constants), Spirit Speak 51-55, Cleansing Winds 100 single target,
  Gift of Renewal about 7 per 2 s. Against a 325 HP bar, all small.

### Missing spells (port source found)

Pinned has **only 9 of Mysticism's 16 spells** (`Spells/Mysticism/`): missing Nether Bolt, Healing Stone, Purge Magic,
Enchant, Sleep, Mass Sleep, Spell Trigger, Rising Colossus (plus Mystic Transformation). Spellweaving lacks **Wildfire,
Arcane Empowerment and Dryad Allure**. ServUO pub57 has all of them (`Scripts\Spells\Mysticism\SpellDefinitions\`,
`Scripts\Spells\Spellweaving\`). OSI content, so a faithful port.

### Proposal

1. **Gain to the cap for all seven stuck skills (the Meditation pattern):** each school's highest-circle window runs to
   the caster's cap (Magery, Necromancy, Chivalry, Spellweaving, Mysticism, Ninjitsu); Resisting Spells gains on every
   resist check up to the cap; Focus and Meditation passive checks get the 0.95 clamp (combat fix c). Chivalry's Divine
   Fury tier becomes earnable.
2. **School mastery past 120 (one rule for every school):** each point past 120 in a casting skill lowers that school's
   mana cost 0.25 percent (**-20 percent at 200**, stacking with LMC) and lifts that school's OSI clamps in proportion
   (Close Wounds, Holy Light, Consecrate Weapon and the like scale on past 120 instead of stopping). Gives every school a
   reason to reach 200 beyond success rate.
3. **Heal spells scale with the target's HitsMax, half the potion rule** (same as bandages, `1 + (HitsMax / 150 - 1) / 2`):
   Heal, Greater Heal, Close Wounds, Noble Sacrifice, Spirit Speak, Cleansing Winds, Gift of Renewal, Healing Stone. Greater
   Heal at Magery 200 on a 325 HP target: about 128-142.
4. **Port the missing Mysticism and Spellweaving spells** from ServUO pub57.
5. **Fix the Mysticism quirk:** casting gains Imbuing or Focus (whichever the damage reads), not Eval Int.
6. Damage, curses, durations, Feint and the rest stay pinned's (uncapped; nothing crosses into immunity below 200).

### Open questions for Chase

1. Gain to the cap for the seven stuck skills: yes?
2. School mastery (mana cost -20 percent at 200, OSI clamps lifted past 120): yes, or a different reward?
3. Heal spells at half the potion scaling, like bandages: yes?
4. Port the missing Mysticism and Spellweaving spells: yes?

### Decided (Chase, 2026-10-02, 16:11)

1. **All seven stuck skills train to the cap** (Meditation pattern; Divine Fury's tier earnable). Yes.
2. **School mastery = just mana, 20 percent cheaper at 200** (0.25 percent per point past 120). Chase asked whether gear
   makes it moot: it would if it were added to LMC, which is capped at 40 for players (`Spells/Base/Spell.cs:642-647`).
   So it is **its own multiplier applied after LMC, outside that cap**: cost x (1 - LMC) x (1 - mastery). With 40 LMC at
   200: 0.6 x 0.8 = **52 percent cheaper**, never moot. The "lift OSI clamps" half is dropped.
3. **Heal spells: "make heal spells great again"** (Chase): **full potion scaling**, not half. Multiplier
   `max(1, target HitsMax / 150)`, and the OSI clamps on heals (Close Wounds 39, Noble Sacrifice 24) scale by the same
   multiplier. Greater Heal at Magery 200 on 325 HP: about 176-195 (over half the bar). Applies to Heal, Greater Heal,
   Close Wounds, Noble Sacrifice, Spirit Speak, Cleansing Winds, Gift of Renewal, Healing Stone. (Bandages stay at half,
   decided 16:03; spells cost mana and cast time, bandages are instant from Dex 220.)
4. **Port the missing Mysticism and Spellweaving spells** from ServUO pub57. Yes.
5. Mysticism casting gains Imbuing or Focus (proposal 5) and damage stays uncapped (proposal 6), not objected.

---

## Animal: Taming, Animal Lore, Veterinary, Herding

Context: pets gain to the same cap as players; **pet and stable slots are tied to max level** (F-12, Chase
2026-10-01); companions share `FollowersMax` (`claude/companions-squire-evo-research.md`).

### Today

- **Taming:** gate `Value >= MinTameSkill` (`Skills/AnimalTaming.cs:185`); roll and gain
  `CheckTargetSkill(Taming, MTS + 6 x owners - 25 .. + 25)` (`:397-407`). Hardest tame is our Raptor at 107.1
  (cc-P20), so **gain stops at about 157** (181 on a four-owner Raptor). Control clamps at 99 percent.
- **Animal Lore:** `CheckTargetSkill(Lore, 0, 120)` on use and while taming (`Skills/AnimalLore.cs:59`,
  `AnimalTaming.cs:373, :394`), and as the Vet bandage secondary. **Ceiling 120.**
- **Veterinary:** bandages on pets, `CheckSkill(0, 120)` (`Bandage.cs:444-445`). **Ceiling 120**; combat fix d
  (decided) already moves bandage checks to the cap, and pets heal at half potion scaling (decided 16:03).
- **Herding:** the shepherd's crook, `CheckTargetSkill(Herding, MTS - 30, MTS + 30 + 0..9)`
  (`Items/Weapons/Staves/ShepherdsCrook.cs:146`). **Ceiling about 146.** Its only use is moving an animal.
- **Stable slots:** a base plus `(skill - 90) / 10` for each of Taming, Lore, Vet past 100
  (`Mobiles/Vendors/NPC/AnimalTrainer.cs:58-100`): 38 at 200 (OSI 14). F-12 already says this moves to max level.

### What 200 does

Nothing breaks: taming and control clamp, Lore and Herding have no scaling reads, Vet is covered by the bandage
decision. The problem is reach (Taming 157, Lore 120, Herding 146) and that past about 120 none of them do anything.

### Proposal

1. **Tamable creature variants on the shared ladder.** Some of the new variants (the beast families: hell hounds,
   drakes, nightmares, wyrms, ki-rin and so on) are tamable, with MinTameSkill on the ladder (100 / 115 / ... / 200)
   and their variant look and slightly better stats. Taming trains to about 225 on them (window MTS +/- 25), and
   tamers get pets nobody else has. Our above-160 creatures (F-14) can join the ladder the same way.
2. **Animal Lore follows the creature:** the Lore use and the taming-time Lore check use the creature's MTS window
   (as Taming does), so studying ladder creatures trains Lore to 200. **Past 120, Lore raises your pets:** pet skill
   and stat gain up to x1.5 at 200 (on top of loop memory), so a lore-master's pets grow faster.
3. **Veterinary:** covered (bandage gain to the cap, half potion scaling on pets). Add: Vet past 120 cuts the skill
   loss a pet takes on resurrection, to none at 200.
4. **Herding gets a job: Corral.** Herding a wild creature with the crook makes it easier for you to tame for a short
   time: its tame difficulty drops by Herding / 20 (10 at 200) for your next attempt. Crook windows on ladder
   creatures train Herding to 200. Optional later: herding a group (radius) of animals at once.
5. **Stable slots come from max level** (F-12's pending item), not skill, so they stop growing with these skills.

### Open questions for Chase

1. Tamable variants on the ladder (some variant families tamable, with better stats): yes?
2. Lore past 120 speeds your pets' growth (to x1.5): yes, or a different reward?
3. Vet past 120 removes pet resurrection skill loss: yes?
4. Herding's Corral (lowers tame difficulty for your next attempt): yes?

### Decided (Chase, 2026-10-02, 16:17)

1. **Tamable variants on the ladder: yes.** Chase asked for candidates among creatures still to port. Found
   2026-10-02: **tamable creatures in ServUO pub57 with no class in pinned or ours** (grep of `class <Name>`), by
   MinTameSkill: Paralithode 47.1, Stone Slith 65.1, Gargoyle Pet 65.1, Iron Beetle 71.1, Blood Fox 72, Ossein Ram 72,
   Slith 80.7, Crimson / Platinum / Stygian Drake 85, Ice Hound 85.5, Wild Tiger 95.1, Lion 96, Cold Drake 96, Dragon
   Wolf 102, Frost Mite 102, Gallusaurus 102, Sabertoothed Tiger 102, Triceratops 102, Dragon Turtle Hatchling 104.7,
   Frost Dragon 105, Bane Dragon 107.1, Raptor 107.1, Dread Warhorse 108 (plus mounts and statuettes). OSI content, so
   porting them is faithful; they fill 47 to 108 and push the plain taming ceiling to about 158. **Our variants then
   carry the ladder from 100 to 200.** Port list to the features chat (with the variant item).
2. **Lore past 120: pet growth up to x1.5 at 200, and a breeding bonus** (Chase). Breeding is its own chat; handoff:
   the breeder's Animal Lore improves inheritance (for example a better chance the heir takes the stronger parent's
   stat or skill line, and better odds on rare traits), scaled 120 to 200.
3. **Vet past 120 removes pet resurrection skill loss** (none at 200). Yes.
4. **Corral: yes, bigger bonus, and usable without a crook** (Chase: a backpack item, or "a skill in a book like a
   spell"). Overseer proposal, to confirm:
   - **A Drover's Handbook** (a skill book like Bushido's and Chivalry's) holding Herding abilities, cast from the book
     or a macro with a small stamina cost, no crook needed. The crook keeps working as OSI's command item.
   - **Corral:** tame difficulty of the target drops by **Herding / 8** (25 at 200) for your next tame attempt within
     60 s. Gain window on the target's MTS, so Herding trains to 200 on ladder creatures.
   - Room for more pages later: **Calm** (a wild animal stops attacking you for a few seconds), **Herd** (move a group
     in a radius), **Lure** (pull a creature out of its spawn toward you).

### Decided (Chase, 2026-10-02, 16:24)

- **Port the candidate creatures and build the variants** (feature-queue item, with the leather/silk/meat variants).
- **Drover's Handbook with four Herding spells:** Corral (tame difficulty - Herding / 8 for 60 s, 25 at 200), Calm,
  Herd, Lure. Corral numbers stand. Art: existing book and ability gump art stands in; custom icons are optional and
  go through the F-8 art pipeline when the build prompt is written.
- **Taming gets a crafting element: pet potions, which should allow shrinking and similar.** Searched ServUO pub57
  2026-10-02:
  - **OSI Pet Training is in ServUO and not in pinned:** `Scripts\Services\Pet Training\` (11 files, about 8,700 lines:
    `PetTrainingHelper`, `TrainingProfile`, `AbilityProfile`, `SpecialAbility`, `AreaEffects`, training points per skill
    to 200 at `PetTrainingHelper.cs:854-862`, the Ethologist title deed). It is OSI's 2017 animal training: tamers spend
    training points to give pets skills, special moves, magical abilities and area effects. **The biggest single
    reason to train Taming and Lore past 120, and faithful.** Strong port candidate.
  - **Pet Bonding Potion** (`Scripts\Items\Tools\PetBondingPotion.cs`, OSI item, instant bond) and **ShrinkTable**
    (`Scripts\Misc\ShrinkTable.cs`, body to figurine art) exist. No shrink potion item in ServUO.
  - **We already have shrinking:** ours `customizations\ShrunkPet.cs`, a figurine made by the Outrider's Crook's
    "Shrink Pet" option (Rangers system).
  - **Overseer proposal, to confirm: Beastcraft,** a small craft system with **Animal Taming as the main skill** (a
  tamer's kit as the tool), so tamers craft and train Taming by it:
    - Pet Bonding Potion (OSI item), **Shrink Potion** (makes the same `ShrunkPet` figurine, no crook needed), pet
      tonics (heal over time, cure), **growth elixirs** (stack with Lore's growth bonus), and **training draughts**
      (extra Pet Training points, if Pet Training is ported).
    - Ingredients from the gathering ladders and the variant creatures; **materials lift the gain window**, so Taming
      also climbs to 200 at the kit, not only by taming.
    - Animal Lore as a secondary skill on the stronger recipes.

**Approved (Chase, 16:30): port OSI Pet Training from ServUO pub57, and Beastcraft as proposed** (Animal Taming main
skill, tamer's kit; bonding potion, shrink potion, pet tonics, growth elixirs, training draughts; ladder materials lift
the gain window; Lore secondary on the stronger recipes). **The animal group is complete.**

---

## Bard: Musicianship, Peacemaking, Provocation, Discordance

The bard skills are where the real breaks sit **inside** 200. Per-use tables: cc-P20 2.4; recomputed here at 200.

### Today

- **Gains:** Musicianship `CheckSkill(0, 120)` on every bard use (`Items/Skill Items/Musical Instruments/BaseInstrument.cs:528`);
  Peacemaking area `CheckSkill(0, 120)` (`Skills/Peacemaking.cs:83`); targeted peace, provoke and discord
  `CheckTargetSkill(diff - 25, diff + 25)` (`Peacemaking.cs:171`, `Provocation.cs:154`, `Discordance.cs:168`) where
  diff comes from the creature's bard difficulty, **capped at 160 for every ported creature**, minus
  `(Musicianship - 100) x 0.5` (`Discordance.cs:159` and the same in the other two). **Musicianship and area peace stop
  at 120; the targeted skills stop around 150** because Musicianship keeps shrinking the difficulty.
- **Range:** `8 + skill / 15` (`BaseInstrument.cs:212`): 21 tiles at 200, past the 18-tile client view.
- **Discordance effect:** `-20 + (skill - 100) / -2.5` above 100 (`Discordance.cs:183`): **-60 at 200** (bosses with
  difficulty 160+ get half). Applied to resists, every skill, and the creature's melee damage (twice the effect).

### What breaks at 200

1. **Every bard skill always succeeds against every creature.** Musicianship 200 takes 50 off the difficulty, so a
   difficulty-160 boss becomes 100, and a 200 skill passes 100 percent at 150. Bosses included (unless flagged immune).
2. **Discordance zeroes a creature's melee damage:** -60 effect is -120 percent damage, so any non-boss discorded
   creature hits for nothing. Its resists also drop 60 and its skills to 40 percent.
3. **Area peace reaches 21 tiles**, so it resets fights the bard cannot see.
4. Fire Horn at four skills 200: about 190-230 fire per blast to monsters (radius 2, every 6 s, 4 sulfurous ash), about
   126-155 to players before resists. Strong, a magnitude, not a break.

### Proposal

1. **Gain to the cap:** Musicianship and area peace windows run to the cap (Meditation pattern). Targeted skills keep
   training on difficulty, and **our own creatures above 160 (F-14) carry a bard difficulty above 160** (from their level),
   so bards climb to 200 on them.
2. **Success never certain: final bard success capped at 90 percent** (every skill, every target), and **85 percent
   against bosses and champions**. The same idea as the block cap: power, but never immunity.
3. **Discordance grows to 40, not 60:** OSI's 28 at 120 rising to 40 at 200 (half against bosses). A discorded creature
   still hits for 20 percent of its damage, resists -40, skills -40 percent.
4. **Bard range capped at the 18-tile view** (reached at skill 150).
5. **Fire Horn stays pinned's** (uncapped magnitude).
6. **Mastery past 120 (the reward):** longer effects instead of certainty: peace and provoke durations and discord's
   maintain time grow to double at 200.

### Open questions for Chase

1. Gain to the cap, with our above-160 creatures as the bard ladder: yes?
2. Success capped at 90 percent (85 against bosses): yes, or other numbers?
3. Discordance effect capped at 40 at 200 (so creatures still do some damage): yes?
4. Range capped at 18 tiles: yes?
5. Durations doubling by 200 as the reward: yes?

### Decided (Chase, 2026-10-02, 16:47)

All five approved as proposed: gain to the cap with our above-160 creatures as the ladder; success capped at 90 percent
(85 against bosses and champions); Discordance effect 40 at 200 (half against bosses); range capped at 18 tiles;
peace, provoke and discord durations double by 200. Fire Horn unchanged.

---

## Thief: Hiding, Stealth, Detect Hidden, Snooping, Stealing, Lockpicking, Remove Trap, Poisoning

Per-use tables: cc-P20 2.3. Nothing of ours changes these handlers (P20 grep); key lines re-checked 2026-10-02.

### Gain ceilings today

| Skill | Ceiling | Where |
|---|---|---|
| Hiding | 100 | `Skills/Hiding.cs:73` |
| Stealth | 60 unarmored, 142 max (armor term) | `Skills/Stealth.cs:96-100` |
| Detect Hidden | 100 | `Skills/DetectHidden.cs:151, :175` |
| Snooping | 100 | `Skills/Snooping.cs:84` |
| Stealing | 127.5 (a 10-stone item) | `Skills/Stealing.cs:316` |
| Lockpicking | 140 (treasure map level 5, paragon chests) | `Items/Containers/TreasureMapChest.cs:190` |
| Remove Trap | trap power + 30: about 180 on world chests, about 210 on a Tinkering-200 trap (decided power keeps scaling) | `Skills/RemoveTrap.cs:61` |
| Poisoning | 100 | `Skills/Poisoning.cs:124` |

### What breaks inside 200

1. **Hiding works in melee from 118:** the "someone is fighting you" range is `(100 - Hiding) / 2 + 8` (`Hiding.cs:53`),
   which hits 0 at 116 and goes negative, so nobody can stop the hide.
2. **Stealing is never caught from 150** (`caught = Stealing < Random(150)`, `Stealing.cs:337`). Piles up to 20 stones or
   3,000 gold a try at 200.
3. **Detect Hidden scans 20 tiles at 200** (`range = DH / 10`, `DetectHidden.cs:145`), past the screen. And **guards (DH 100)
   can never reveal a hider at 121+** (cc-P20).
4. **Poisoning's Infectious Strike bug (pinned):** `Poison.IncreaseLevel` takes the next list entry, not the next level of the
   same family (`Server/Poison.cs:51`, used at `Items/Weapons/Abilities/InfectiousStrike.cs:67`), so at Poisoning 100+ every
   Infectious Strike turns Lethal into Lesser Darkglow and Darkglow into Parasitic. A defect at any cap.

Stealth (40 steps at 200), Snooping, Lockpicking and Remove Trap scale harmlessly.

### Proposal

1. **Gain to the cap.** Meditation pattern (window to the cap) for Hiding, Stealth (armor term kept below it), Detect
   Hidden, Snooping and Poisoning. Content-driven for the rest: **Stealing** trains against the target's level (F-14),
   so stealing from tougher creatures trains it; **Lockpicking** gets lock levels on the shared ladder (dungeon and
   higher-tier chests, treasure maps above level 5); **Remove Trap** already climbs on tinker traps and ladder chests.
2. **The breaks become caps, the same "never immune" rule as block and bard:**
   - Hiding's combat range never drops below 8 tiles (OSI's GM value).
   - Stealing keeps a 5 percent caught floor.
   - Detect Hidden range capped at 18; guards and our NPC detectors get BaseAI's floor (at least DH / 10 percent to reveal).
   - Fix the IncreaseLevel bug (a pinned patch: next level in the same family).
3. **Rewards past 100 (the thief's mastery):**
   - Hiding: taking damage has a chance not to reveal you, up to 50 percent at 200.
   - Stealth: more steps (pinned already gives 40 at 200) and running costs 1 step instead of 2 at 200.
   - Detect Hidden: reveals stealth footsteps for a few seconds after a scan.
   - Snooping: see into nested containers.
   - Stealing: piles grow as pinned (20 stones at 200).
   - Lockpicking: lockpicks stop breaking at 200, picks get faster.
   - Remove Trap: a disarmed trap can be salvaged into a trap kit (for tinkers).
   - Poisoning: extra charges per dose, up to +4 at 200.

### Open questions for Chase

1. Gain to the cap (Meditation pattern for five, content-driven for Stealing and Lockpicking): yes?
2. The four fixes (Hiding range floor 8, Stealing 5 percent caught floor, DH range 18 plus guard floor, poison bug): yes?
3. The mastery rewards: keep, cut or change any?

### Decided (Chase, 2026-10-02, 16:51)

Gain to the cap as proposed, the four fixes, and every mastery reward: **yes.** Chase added: **Poisoning and Alchemy
synergy, higher poisons.** Draft below; Poisoning stays "in discussion" until it is answered.

### Higher poisons (draft, Poisoning x Alchemy)

**Why poison falls behind too.** AOS poisons tick a share of current HP, but each level has a hard per-tick ceiling
(pinned `Misc/PoisonKinds.cs:80-84`, `PoisonImpl(name, id, level, min, max, percent, ...)`): Lethal is 35 percent of current
HP, **min 20, max 50 per tick**. Against a 325 HP player or our above-160 creatures, the 50 ceiling makes Lethal small.
Levels stop at 4 in every family.

**Proposal: three poisons above Lethal on the shared ladder** (regular family; numbers are placeholders for playtest):

| Gate (Alchemy to brew / Poisoning to apply) | Poison | Level | Per tick (share of current HP, min-max) | Ticks |
|---|---|---|---|---|
| 140 | **Virulent** | 5 | 40 percent, 30-90 | 20 |
| 170 | **Baneful** | 6 | 45 percent, 40-140 | 20 |
| 200 | **Plague** | 7 | 50 percent, 50-200 | 20 |

- **Brewed by Alchemy** on the shared ladder (window gate to gate + 45, so alchemists also train on them), ingredients
  from the gathering ladders and **variant creature venom** (Etherhide-tier serpents and spiders and up).
- **Applied with Poisoning** (window gate to gate + 45, so Poisoning trains to 200 on them), to weapons and arrows as
  today. Infectious Strike can raise up to Plague once the IncreaseLevel bug is fixed.
- **Cures keep up:** Alchemy gets matching **antidotes** at each tier (a Virulent antidote, and so on), and the existing
  cure formulas (spell, bandage, potion) treat levels 5-7 with their usual `- (level + 1)` penalty, so high poisons
  are hard to cure without the matching antidote or high skill.
- **Immunity:** 58 pinned creatures are immune to Lethal (`PoisonImmune => Poison.Lethal`). Overseer default: **a creature
  immune to Lethal is immune to every higher poison too** (no change to ported bosses); our own creatures (F-14) set
  their own immunity per level.

Open questions for Chase:
1. Three higher poisons (Virulent, Baneful, Plague) at 140 / 170 / 200: yes? Names?
2. Matching antidotes from Alchemy: yes?
3. Lethal-immune creatures stay immune to all higher poisons: yes, or let the new tiers pierce it?

### Decided (Chase, 2026-10-02, 16:53)

**Higher poisons approved:** Virulent 140, Baneful 170, Plague 200 (names and placeholder numbers as drafted), brewed by
Alchemy and applied with Poisoning on the ladder; **matching antidotes** from Alchemy; **Lethal-immune creatures stay
immune to all higher poisons.**

---

## Utility: Tracking, Item ID (Appraisal), Taste ID, Camping, Cartography, Begging, Forensics

These need the most invention: every one of them stops gaining at or near 100 and does nothing past it. Per-use
tables: cc-P20 2.3 and 2.4.

### Today

| Skill | Gain ceiling | What it does past 100 |
|---|---|---|
| Tracking | 100 (`Skills/Tracking/Tracking.cs:129, :163`) | search range `10 + (skill / 10) x 10`: 210 tiles at 200 (`:166-168`), a stalking bonus for Ninjitsu |
| Item ID | 100 (`Skills/ItemIdentification.cs:44`) | nothing; **F-14 repurposes it as Appraisal** (decided: con colors free, skill steps to a stat card at 90) |
| Taste ID | 100 (`Skills/TasteID.cs:37`) | nothing |
| Camping | 100 (`Items/Skill Items/Camping/Kindling.cs:38`) | nothing |
| Cartography | 130 (treasure map level 5-6 decode, `Items/Maps/TreasureMap.cs:371-417`) | map extents grow past the facet edge (cosmetic break) |
| Begging | 100 (`Skills/Begging.cs:111`) | nothing (gold has no skill term) |
| Forensics | 100 (`Skills/ForensicEval.cs:36, :54`) | nothing |

### Proposal, skill by skill (each a new job; every one is a deviation to register)

1. **Tracking: the hunter's sense.** Gains on tracking creatures by their level (F-14), to the cap. Past 100: the
   tracking arrow also shows the target's **con color and health**; from 150 it **shows the footsteps of stealthed
   players and creatures** for a few seconds; at 200, **track variant creatures** (the rare spawns) from double range.
   Search range kept as pinned.
2. **Appraisal (Item ID):** F-14's steps stand (to the stat card at 90). Gains on appraising creatures and items by
   their level, to the cap. Past 120: **150 shows what a creature carries** (loot hints, including variant materials);
   **200 shows its weakest resist** (feeds F-26's Expose Weakness, where Appraisal already sets the duration).
3. **Taste ID: the connoisseur.** Gains on tasting dishes, potions and elixirs by their ladder tier, to the cap. Past 100:
   **food and elixir buffs you consume last longer**, up to +50 percent at 200; identifies poison level on food, drink and
   weapons, higher poisons included; names unknown potions and elixirs.
4. **Camping: the camp is a rest point.** Gains on lighting fires with ladder kindling (woods by tier), to the cap. Past
   100: a lit campfire gives the party a **regen aura** (hits, stamina, mana up to +10 points at 200); from 150 you can
   **make a secure camp inside dungeons** (safe logout during dives, F-24); campfires burn longer with skill.
5. **Cartography: higher treasure.** Gains on decoding maps by level, to the cap. **Treasure map levels 7 and 8 on the
   ladder** (decode at about 150 and 190), with chests whose locks and traps sit on the Lockpicking and Remove Trap ladders
   (decided there). Fishing's maps (up to level 3, decided) and the dungeon feed it. **Map extents clamped at the 100 value**
   (fixes the cosmetic break).
6. **Begging becomes Persuasion** (renamed for everyone through the updater, like Appraisal). Gains on haggling with NPC
   vendors, to the cap. Past 100: **vendor buy prices down** to 20 percent at 200, and **better League quest rewards** (a
   share more gold or renown). (Chase turned down better sale prices for Arms Lore; this is buying, and it is Persuasion's
   whole job.)
7. **Forensics: the field dresser.** Gains on examining corpses by the creature's level, to the cap. Past 100: **more from
   every carve** (hides, meat, venom, parts), up to +50 percent at 200, and a **chance at a rare part** from variant
   creatures; keeps its OSI job (who killed it, who looted it, thieves).

### Open questions for Chase

1. Tracking: con color and health on the arrow, stealth footsteps at 150, variants at 200: yes?
2. Appraisal: loot hints at 150, weakest resist at 200: yes?
3. Taste ID as the connoisseur (longer food and elixir buffs, poison and potion ID): yes?
4. Camping: party regen aura, dungeon camps at 150: yes?
5. Cartography: treasure map levels 7 and 8, extents clamped: yes?
6. Begging renamed **Persuasion**, vendor discounts and better quest rewards: yes? Name?
7. Forensics as the field dresser (bigger carves, rare parts): yes?

### Decided (Chase, 2026-10-02, 16:57)

1. **Tracking: approved as proposed** ("great start, no notes").
2. **Appraisal: approved as proposed** ("great start, no notes").

### Decided (Chase, 2026-10-02, 17:00)

3. **Taste ID: approved as proposed.**
4. **Camping: approved, plus a temporary "instanced" camp site** (Chase). Overseer default: at Camping 175, pitching a
   tent opens a **private camp for the party**, 30 minutes, entered through the tent: the regen aura, a cooking fire,
   safe logout, and you step back out where you pitched it. ModernUO has no true instancing, so "instanced" means a set
   of **reserved camp plots** in an unused map area, one handed to each party while in use (the cc-P16 tent addons are a
   starting point for the plot art). Check first: a free area for the plots and how many are needed at once.
5. **Cartography: approved, plus an easier way to find the X** (Chase). Today the dig tolerance comes from **Mining**, 1 to
   4 tiles (pinned `Items/Maps/TreasureMap.cs:585-593`). Overseer default: **Cartography adds to it**, +1 tile at 150 and
   +2 at 200, and from 100 each missed dig says **warmer or colder** (and roughly which way at 150).
6. **Persuasion: approved, scaled up** (Chase): **a successful haggle gives a temporary discount with that vendor while
   training, and at 200 the discount is permanent.** Overseer numbers: temporary discount of skill / 10 percent (10 at 100,
   up to 20 at 199) for 10 minutes with that vendor; **at 200, a permanent 30 percent** with every vendor. **Includes guild
   stores when used on guildmasters** (Chase): seal, voucher and other guild-currency prices drop by the same share.
7. **Forensics: approved as proposed.**

**The utility group is complete, and with it all 58 skills.**
