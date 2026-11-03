# cc-P792: assess druid spells, spellcrafting, the lich staff and voodoo dolls (third-party intake, 11-03)

Iron Golem, 2026-11-03. Docs copy `D:\UO\golems\Iron\shard-migration`, branch `golem/Iron/P792`. Assessment only: nothing
was built or run, and nothing from `D:\UO\third-party` was compiled or copied into the shard. No code changed.

## In plain words

- **The druid spell pack is the most useful of the four, as a pattern.** Your skills design already decided on a
  Drover's Handbook (four Herding spells cast from a book), and it is not built yet. The druid pack shows how to add a
  whole new spellbook, which is exactly the plumbing that book needs. A full druid school on Animal Lore is a bigger,
  separate decision for you.
- **Spellcrafting would compete with Imbuing.** It adds stats and properties to any gear, artifacts included, from
  jewels. Imbuing (the Artificers' guild) already does that job. Skip it.
- **The lich staff** (collect two broken halves and a gem, combine them) is a nice collecting idea, but the staff itself
  is far too strong. **Voodoo dolls** let a player hurt another player from anywhere in the world with a pin. Skip.
- **For you:** say whether the Drover's Handbook prompt (rank 1 below) goes in the queue, and whether a druid school is
  wanted at all. Nothing else to do.

## Sources and method

- Read every `.cs` in the four folders under `D:\UO\third-party\code\` (outside `_zips`), the spellcrafting readme and
  config XML, and each `SOURCE.txt`.
- Shard state: `D:\UO\golems\Iron\ShatteredLegacy` (branch `golem/Iron/P792`) and `D:\UO\ModernUO-pinned` at d4531cd9.
  Design: `notes\skills-design.md` (every skill to the F-12 cap; the Animal section and Chase's 2026-10-02 16:24 decision
  on the Drover's Handbook), `notes\f12-levels-loops-caps.md` (the loop ladder: cap 50 at creation, 100 after the first
  reset, +5 a loop to 200; every skill maxable on one character), `notes\cc-P535-skills-design-vs-build.md` (Drover's
  Handbook: not built).
- "Ser" is the number of hand-written `Serialize` methods. Line counts include any copies of core files the pack ships.
- Art: all four use stock art only (druid book 0xEFA and book gump 0x89B-0x89E, 0x903, 0x93A; spellcraft jewels 0x1EA7;
  lich gem 0x1EA7 on a wild staff; voodoo doll 0x13CA, pins 0x1027). Our 7.0.117 client has all of it. No new spell
  icons are drawn anywhere; the druid book gump lists spells by name.
- Terms: druid, lich staff and voodoo dolls say "none stated" (credit Hammerhand; Tukaram; tass23 and Tru). Spellcrafting
  carries Xanthos's readme term: "use or modify this system in any way you desire" if the original headers stay.

## Part 1: each item

| # | Folder | What it does | Size | Fit and overlap |
|---|---|---|---|---|
| 1 | `druid-spell-system` (Hammerhand, v2.0) | **A new spell school of 20 druid spells** in a Druidic spellbook, cast on **Animal Lore** (damage and resist on **Animal Taming**), skill 1 to 94, 10 to 75 mana, six new reagents (fen moss, pumice, petrified wood, spring water, destroying angel, fertile earth). Spells: summons (fireflies, forest kin, pack of beasts, treefellow, swarm of insects), area damage (hurricane, volcanic eruption), roots and spores (paralyze, poison), Hibernate (puts a target into a sleeping body), Bark Skin (resist), Hollow Reed (+Str and Dex), Spring of Life (heal), Mana Spring and Enchanted Grove (regen fields), Mushroom Gateway (a gate), Lure Stone (draws creatures), Restorative Soil (a resurrection field). Six familiars. Arch Druid, Druid and Evil Druid (Lord) NPCs drop scrolls, the book, a cloak and a staff; a druid vendor sells reagents. | 79 .cs, 12,035 lines, 58 Ser. **Replaces five core files** with full copies: `Initializer.cs` (all spell registrations), `Spellbook.cs` (1,375 lines; adds `SpellbookType.Druidic`), `SpellRegistry.cs`, `Reagent.cs`, `SpellHelper.cs` (1,686 lines). Spell IDs 301-320. | **No druid on the shard.** On pinned, IDs 301-320 are free inside the 700-slot registry, but `SpellbookType` is a closed enum (`Items/Skill Items/Magical/Spellbook.cs:16-26`), so any new book still needs a patch. **The skills design decided a Drover's Handbook** (Corral, Calm, Herd, Lure: Herding abilities cast from a book, existing book and gump art) that P535 found unbuilt; this pack's book, gump, registry and scroll plumbing is the closest reference, and its Lure Stone spell is that book's Lure. Animal Lore past 120 is already promised to pet growth and breeding (decided 16:17), so a whole school on Lore is new design. |
| 2 | `spellcrafting` (LimpBizquick; Xanthos and TheOutkastDev v3.0) | **Add properties to gear.** A Book of Spellcrafts holds up to 50 crafts; each craft (str/dex/int bonus, hit points, stamina, mana, five resists, regen, cast speed and recovery, mana and reagent cost, spell damage, spell channeling, hit spells and areas, leeches, slayer, luck, durability and more) costs magic jewels and applies 2-10 points scaled by Inscription + Alchemy (both 50+). Up to 5 properties per item; artifacts allowed by default; 35% chance of an explosion that hurts the crafter, and of that 35% to destroy the item. Jewels and books drop from a Guardian of the Magics. | 108 .cs, 6,036 lines, 55 Ser. No core edit; reads a config XML. | **Overlaps Imbuing** (our Artificers' guild, decided in the skills design), which is the shard's one route for adding properties to gear. Two routes would double the power budget and undercut the Artificers. |
| 3 | `lich-staff` (Tukaram) | **A three-piece collectible**: two broken staff halves and a lich gem drop (the author put them on the Lich); double-click the gem holding all three to get the Lich Staff: a wild staff hitting 45-55 (pinned's wild staff hits 10-12, `Items/Weapons/ML Weapons/WildStaff.cs:17-18`), silver slayer, +10 Int, +10 mana, 10% lower mana and reagent cost, spell channeling, use best skill, night sight. | 4 .cs, 259 lines, 3 Ser, plus notes. No core edit. | Our loot side already has slayers and spell-channeling staves. The **collect-the-pieces** loop is new on the shard and works well with any reward. |
| 4 | `voodoo-dolls` (tass23, after Tru) | **Make a doll of a real player and poke it.** Carve a player's corpse for their head (needs edited `Corpse.cs` and `Head.cs`), cook it into a doll, then poke the doll with pins (Harm, Heal, Cure, Poison) to affect that player **wherever they are**, if they are online; Magery and Necromancy 50+, 10 pokes per doll. A doll can be animated into a summon. | 7 .cs, 2,551 lines (1,592 of them the two edited core files), 8 Ser. | Nothing like it on the shard. It is player-on-player harm at any range with no aggression or region checks. |

## Part 2: rules check

The rules: nothing that grants skill or stat points, power scrolls, bless deeds or property artifacts; usable now and
mostly helpful. The prompt also asks about power and the reset loop.

| # | Folder | Grants a banned thing? | Power and the reset loop | Verdict |
|---|---|---|---|---|
| 1 | druid-spell-system | **Yes, in its drops:** the Arch Druid Cloak gives **+15 Animal Lore, Herding and Tracking and +15 Int**; the Arch Druid Staff is a **Blessed** property artifact (hit lightning, harm, leech, 200 luck, 10 cast speed, 20 physical resist bonus) | The spells gate on 1-94 skill, so they all open inside loop 1 (cap 100) and give nothing to train toward on later loops (to 200). A new school needs its own numbers past 100, like every skill in the design. Summons and a resurrection field are strong but within OSI's range | The spells pass as ideas; the gear and core-file copies fail |
| 2 | spellcrafting | **Yes, it makes them:** stat bonuses (+Str/Dex/Int, hit points) on any item, artifacts included | Scales on Inscription + Alchemy with a hard 100 ceiling (`MaximumSkillValue`), so it ignores the loop ladder | **Fails** |
| 3 | lich-staff | **Yes:** the staff is a property artifact (+10 Int, 45-55 damage) | Not loop-aware | Fails as written; the collecting loop passes as an idea |
| 4 | voodoo-dolls | No banned item | Remote harm to any online player; trains Magery, Necromancy and Poisoning off another player | **Fails** "mostly helpful" |

## Part 3: recommendations, ranked

| Rank | Item | Call | Why |
|---|---|---|---|
| 1 | **Druid spell system** (1), as the pattern for the **Drover's Handbook** | **Rebuild as ours (the Handbook only); the druid school is idea only** | The Handbook is decided and unbuilt; this pack shows every piece it needs (book item, book gump, registry IDs in a free range, scrolls, a base spell class on a non-Magery skill). A full druid school on Animal Lore is a design question for Chase, with loop-aware numbers, and none of the drops. |
| 2 | Lich staff (3) | **Idea only** | The "collect two halves and a gem, combine" loop is a good fit for boss loot or the League shop, with a cosmetic or ordinary reward. Not this staff. |
| 3 | Spellcrafting (2) | **Skip** | A second property-adding route next to Imbuing, with stat bonuses, artifact edits and a skill ceiling of 100. |
| 4 | Voodoo dolls (4) | **Skip** | Player-on-player harm at any range; two core edits. |

### Prompt sketch for rank 1

**Drover's Handbook.** "Build the Drover's Handbook as decided in `notes\skills-design.md` (Animal, Chase 2026-10-02
16:24): a book (stock book art) holding four Herding abilities, Corral (the target's tame difficulty drops by Herding / 8,
25 at 200, for your next attempt within 60 s), Calm, Herd and Lure, cast from the book on Herding with gain windows on the
target's taming difficulty so Herding trains to 200; a patch adding the book type to `SpellbookType` and the abilities to
free registry IDs; scrolls or a vendor to fill it. Take the structure from the druid pack (book, gump, registry, base
spell on a non-Magery skill) as reference only; draft Calm, Herd and Lure numbers for Chase. Facts per ability and a save
and load; a proof shot of the book." Size: medium, about 6-8 files (~800 lines), one patch, 2-3 test files.

## CODE-INTAKE

`D:\UO\third-party\CODE-INTAKE.md` had no rows for these four. I added one row each, dated 11-03, with the Overseer column
set to `assess (P792)`.

P792 DONE
