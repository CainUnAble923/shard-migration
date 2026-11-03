# cc-P791: assess bounties, goals and quest chains (third-party intake, 11-03)

Iron Golem, 2026-11-03. Docs copy `D:\UO\golems\Iron\shard-migration`, branch `golem/Iron/P791`. Assessment only: nothing
was built or run, and nothing from `D:\UO\third-party` was compiled or copied into the shard. No code changed.

## In plain words

- **One of the five is worth building as our own: a community goal stone.** Players chip in gold toward a shared goal
  that staff set (say, "open the winter Festival early"), see the total climb, and get named on the stone. It gives the
  shard a gold sink, which it does not have yet.
- **Reagent harvesting is an idea for the herbalism build**, not something to take: it gives every reagent, including
  necromancy ones, from any tree with an axe, using Magery.
- **The Holy Grail quest has one good puzzle** (pick the true grail among four, the wrong one kills you) but needs tools
  we do not run and rewards gear far past the rules. **The bounty board** is for player killers, and **the Zelda quest**
  is Nintendo's characters with absurd gear. Skip those.
- **For you:** pick whether the goal stone prompt (rank 1 below) goes in the queue. Nothing else to do.

## Sources and method

- Read every `.cs` (and the two `.bak` core files, the readme and the spawn XML headers) in the five folders under
  `D:\UO\third-party\code\`, and each `SOURCE.txt`.
- Shard state: `D:\UO\golems\Iron\ShatteredLegacy` (branch `golem/Iron/P791`, main as of P789) and
  `D:\UO\ModernUO-pinned` at d4531cd9. Related notes: P780 (daily League hunts), P629 (League investigation warrants),
  P519 (herbalism against what is built; the master design `f-herbalism-reagents.md` is summarised there), P532 (open
  questions, PvP).
- Art: every item, mobile and addon in these packs uses stock art. The grail's castle and caves (4,392 components) top
  out at item 0x3F1A; the bounty head is 0x1DA0, the goal stone 0xED4. Our client (7.0.117 data) has all of it.
- "Ser" is the number of hand-written `Serialize` methods (saved types to convert to the serialization generator).
- Terms: all five say "none stated". Treat as community work: credit the author, ship only inside the player package or
  the private repo. The Zelda pack also carries Nintendo names (SOURCE.txt: rename everything). A rebuild "as ours"
  takes the idea, not the code.

## Part 1: each item

| # | Folder | What it does | Size | Art | Fit and overlap |
|---|---|---|---|---|---|
| 1 | `fs-bountyhunting` (demented; RunUO FS Bounty System) | **Player-killer bounties.** When a player reports a murderer, a gump lets them post gold from their bank as a bounty (30 days). Carving a player's corpse yields a `BountyHead`; the killer hands it to a Bounty Officer NPC for a bank check. A board lists the wanted. Bounties live in their own `Saves/FS Systems/FSBounty` files. | 7 .cs, 896 lines, plus **two edited core files** shipped as `.bak`: `Corpse.cs` (1,304 lines; carving makes a `BountyHead`) and `ReportMurdererGump` (199 lines; opens the bounty gump). 4 Ser plus a custom save file. | Stock (head 0x1DA0, board, NPC). | **No fit.** Our goal loops are PvM: daily League hunts (P780) post kill goals on the Requisitions board, and League warrants (P629) send groups after named mini-bosses. PvP is not part of the League loop, and new PvP features stay off by default (P532, S057). |
| 2 | `goal-stone` (Abracadabra2.0) | **Community goal stone.** Staff name a stone and set a gold goal; players double-click, target gold or a bank check, and the stone takes up to what is left. The gump shows contributed and goal. Meant as a gold sink and to let players vote on development with gold. | 2 .cs, 186 lines, 1 Ser, plus a `.docx` readme. No core edit. | Stock (0xED4). | **Nothing like it on the shard** (no fund, treasury or gold-sink feature in customizations). The code has three bugs: `Serialize` writes only a version, so goal and total are lost on restart (despite the "v1.1 serialized" note); the target takes **any** gold it can see, not just the giver's own; and there is no record of who gave what. |
| 3 | `holy-grail-quest` (Karmageddon) | **A long story quest** on the classic `QuestSystem` (pinned has it): King Arthur sends you after the grail via a cartographer, alchemist, tinker and Lancelot; a sand dragon and a wyrm guard map pieces; a cave with saw traps, death tiles and a bridge; a final chamber where you **choose one of four grails** (the wrong one kills you). Reward: 1,500-2,000 gold and one random piece of Excalibur or the King's set. | 49 .cs, about 14.3k lines (7,302 of them the King's castle addon), 68 Ser. Needs **XmlSpawner** (`Grail.xml`, 908 lines) and **Custom Regions in a Box**, neither of which we run. Fixed places on Malas 1076,1229, Ilshenar and Trammel 4550,3171; staff must decorate and place teleporters by hand. | Stock (addons up to 0x3F1A). | Overlaps nothing directly. Our story work is the League (chapters, investigations); the classic quest engine is not used by our own content. |
| 4 | `zelda-quest` (Falkor; RunUO, Vladamere) | **A hand-in chain**: bosses (Agahnim, Deku, Ganon, the Great Fairy, Kokiri) drop items; giving one to the Zelda NPC returns the next tool or weapon (magic hammer, Megaton hammer, Biggoron sword, green and red tunics, Master Sword). A "crushing target" wall blocks Ganon until hammered; a boomerang paralyzes. | 20 .cs, about 2.0k lines, 19 Ser. No core edit. No per-player state: whoever holds a drop can hand it in. | Stock. | No fit. Nintendo names and characters throughout. |
| 5 | `reagent-harvesting` (demented; Lord Greywolf) | A harvest system and a "Reagent Gathering Axe" (100 uses): chop any tree for one of 13 reagents (the five plant reagents, spider's silk, and seven necromancy reagents), 0-4 per 2x2 bank, 20-30 minute respawn, skill **Magery** with every resource at 100.0. | 1 .cs, 305 lines, 1 Ser. Scraped from the resource page (no file was attached): it has stray `[B]` tags and will not compile as is. The axe uses item 0x13E4. | Stock. | Lines up with one unbuilt row of the herbalism design (P519 row: "wild biome patches, respawn, forage checks" **not built**). Herbalism is still unbuilt as a skill. |

## Part 2: rules check

The rules: nothing that grants skill or stat points, power scrolls, bless deeds or property artifacts; usable now and
mostly helpful.

| # | Folder | Grants a banned thing? | Usable now and helpful? | Verdict |
|---|---|---|---|---|
| 1 | fs-bountyhunting | No | Needs two core-file edits; rewards player killing; a PvP feature on a PvM loop | **Fails** "mostly helpful" for this shard |
| 2 | goal-stone | No | Small and helpful once the three bugs are fixed | **Passes** (as a rebuild) |
| 3 | holy-grail-quest | **Yes:** Excalibur (50-70% damage, 80-100 hit life leech, 70-90 hit lightning), the King's crown, arms, tunics, shield (+4-8 Str/Dex/Int, 20-40 hit and defense chance) are property artifacts | Needs XmlSpawner and a region kit we do not run; instant-kill traps | **Fails** |
| 4 | zelda-quest | **Yes:** Master Sword (+20 Str, Dex and Int, 25 hit point regen, 150% damage, five 100% area hits), Great Fairy sword (+40 Str and Dex), Megaton hammer, Mirror shield (50 hit and defense chance) | Boomerang paralyzes any target, players included, for 10 s; IP | **Fails** |
| 5 | reagent-harvesting | No banned item. It would flood necromancy reagents and train Magery off trees | Does not compile as saved; wrong skill for our herbalism design | Fails as written, the idea passes |

## Part 3: recommendations, ranked

| Rank | Item | Call | Why |
|---|---|---|---|
| 1 | **Goal stone** (2) | **Rebuild as ours** | A shared gold sink with a visible goal, which the shard lacks. Tiny, no core edit, no banned rewards. |
| 2 | Reagent harvesting (5) | **Idea only** | Fold "forage reagents from the wild" into the herbalism build when it comes (P519's unbuilt wild-patches row), on Herbalism, plant reagents only, from bushes and herb patches rather than any tree. |
| 3 | Holy Grail quest (3) | **Idea only** | Keep the "choose the true grail" chamber and the step-by-step errand chain as ideas for a League story trial, with cosmetic or League-shop rewards. Nothing from the code. |
| 4 | Bounty system (1) | **Skip** | Player-killer bounties with two core edits; our repeatable goals are PvM and already built (P780 hunts, P629 warrants). |
| 5 | Zelda quest (4) | **Skip** | Nintendo IP, gear far past the rules, a player-paralyzing boomerang. |

### Prompt sketch for rank 1

**Goal stone.** "Add a League goal stone as ours: a staff-placed stone with a name, a gold goal and a description of what
finishing it does; players double-click to give gold or a bank check from their own backpack (refuse anything else),
capped at what is left; it records each giver and total, shows progress and the top givers in a gump, broadcasts when
complete, and stays complete (staff reset it for the next goal). Optional: a once-per-character achievement for giving.
Generator serialization; facts for give, cap, own-pack-only, completion, save and load." Size: small, 1 file (~250
lines), 1 saved type, 1 test file. What finishing unlocks stays a staff action or an existing switch; the stone does not
hand out items. Credit Abracadabra2.0 for the idea.

## CODE-INTAKE

`D:\UO\third-party\CODE-INTAKE.md` had no rows for these five. I added one row each, dated 11-03, with the Overseer
column set to `assess (P791)`.

P791 DONE
