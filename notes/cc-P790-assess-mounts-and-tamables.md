# cc-P790: assess mounts and tamable creatures (third-party intake, 11-03)

Iron Golem, 2026-11-03. Docs copy `D:\UO\golems\Iron\shard-migration`, branch `golem/Iron/P790`. Assessment only: nothing
was built or run, and nothing from `D:\UO\third-party` was compiled or copied into the shard. No code changed.

## In plain words

- **Two of the twelve downloads are worth building as our own:** a rideable **peacock** that tamers can tame
  (the client already has its art), and a set of **new ethereal mount looks** (windrunner, lasher, tiger, ancient
  hellhound, boura, peacock) to hand out as earned rewards and for companions to ride.
- **Most of the rest we already have, or would break the rules.** The iron beetle, tigers, boura and the Eodon
  dinosaurs are already on the shard in better versions. The turtle boss drops power scrolls, the dinosaur pack drops
  aprons with +10 Taming, and the "tameable ancient wyrm" can be tamed by anyone for one follower slot.
- **The tarantula mount has no walking art** in the client we ship, so it stays an idea until someone checks it in game.
- **For you:** pick whether the two "rebuild" prompts (ranked 1 and 2 below) go in the queue. Nothing else to do.

## Sources and method

- Read every `.cs` in the twelve folders under `D:\UO\third-party\code\` (outside `_zips`), and each `SOURCE.txt`.
- Shard state: `D:\UO\golems\Iron\ShatteredLegacy` (main at 54106ef) and `D:\UO\ModernUO-pinned` at d4531cd9 (the
  Dockerfile's `MODERNUO_COMMIT`). ServUO stock for comparison: `D:\UO\ServUO-work\Scripts`.
- Client art: P59's renderer and scan (`notes\cc-P59-scratch\p59anim.py`, `scan.json`), which read EA 7.0.117 data,
  the data the player package launches. I ran `p59anim.actions_present()` for 1401, 1440, 1410, 1407 and 1069.
  Item names from `tiledata.mul` in `D:\UO\tool-trials\client-data-copy` (a small reader in the session scratchpad).
- "Ser" below is the number of hand-written `Serialize` overrides (each one a saved type to convert to the
  serialization generator). None of the twelve uses Vita-Nex in code, whatever `SOURCE.txt` says.
- Terms: all twelve say "none stated". Treat as community work: credit the author, ship only inside the player package
  or the private repo. A rebuild "as ours" takes ideas and client art IDs, not their code.

## Part 1: each item

| # | Folder | What it does | Size | Art it needs, and do we have it | Fit and overlap |
|---|---|---|---|---|---|
| 1 | `pack-drake` (Neshoba) | A drake (body 60/61, random hue 1-2100) with a pack, fire breath and an auto-loot: every 1-2 s it lifts up to 3 movable stackable items within 2 tiles into its pack. 2 slots, tame 100.9. Strong (Str 400+, Dex 433-552, 241-258 hits, 21-37 damage, resists to 90). | 1 file, 241 lines, 1 Ser. Uses `BackpackOfReduction`, which neither pinned nor our customizations define. No core edit. | Stock drake bodies 60/61, in the client. | Overlaps the **Compact Mule** (P69, the shard's pack animal with modules) and the reward **Riding Drake** (P365). The auto-loot takes anyone's drops and gold from the floor near it. |
| 2 | `iron-beetle` (Kilra Yan) | Iron beetle (body 714) that mines by voice ("mine", "take break") with a shovel in its pack, and turns ore dropped on it into **2 ingots per ore** with no smelt check. Drops a 1,000-use shovel, Lucky Coin. 4 slots, tame 71.1. | 2 files, 403 lines, 2 Ser. Uses `QLPoints` (ServUO only). | Body 714, in the client. | **Already on the shard**: `server/customizations/Mobiles/Normal/IronBeetle.cs` (cc-P129) is a port of ServUO's stock beetle, mining by context menu, with a timer fix. |
| 3 | `peacock-mount` (WiKKiD) | Rideable peacock on ostard numbers: 71-88 hits, 5-11 damage, 1 slot, tame 29.1, eats fruit and grain. | 1 file, 85 lines, 1 Ser. No core edit. | Body **1440** (`Bird_Peacock_Mount`, AnimationFrame4.uop, walk, stand, attack and more present), mount item **0x3ECF**, shrink art **0xA0C0** (`Bird_Peacock_Mount` in tiledata). Body 1440 has **no `bodyTable.cfg` row** (P59 section 6: no idle or feed animations, and it could open doors until one is added). | New look. P59 picked 1440 for the evo bird line "built as a mount"; nothing on the shard uses it yet. Fits the low-skill tamer and the P764 leash (it would shrink to 0xA0C0 only if `ShrinkTable` knows it). |
| 4 | `tarantula-mount` (Shazzy) | Rideable tarantula: 450-575 hits, 20-30 damage (80% poison), Lethal poison, bleed, 10% chance per hit of -15% physical resist for 5 s. 3 slots, tame 115.1, angers on tame. FilthyRich x4 and Gems x4 loot. | 1 file, 147 lines, 1 Ser. No core edit. | Body **1401** (`Turanchula_Mount`): the client has **only actions 29-31** for it, no walk, stand or attack. Mount item 0x3ECA. **Not usable as a walking creature** on our data without a client check. | New look, but over-tuned (Lethal poison on a pet, 115 tame on a shard whose top dinos sit at 102). |
| 5 | `tarantula-lasher-ethys` (Neshoba, after Shazzy and Vorspire) | Two ethereal mounts: tarantula and lasher. | 1 file, 84 lines, 2 Ser. **Serialization bug:** writes the version with `WriteEncodedInt`, reads it with `ReadInt`. The tarantula statuette uses item 0x579 (`stone roof`), not the statuette 0x9DD6. | Lasher: body 1407 (`Horse_Unicorn_RB`, full action set), mount item 0x3ECB, statuette 0x9E35. Tarantula: see row 4. | ServUO stock already has both (`Ethereals.cs:1193`, `:1243`) with correct IDs; pinned has neither. P119 left ServUO's `Lasher` and `Windrunner` creatures unported (store statuettes, "no donations"). |
| 6 | `windrunner-ethereal` (Shazzy) | One ethereal: the windrunner (solid, not translucent). | 1 file, 48 lines, 1 Ser. | Body 1410 (`Canine_Windrunner`, full action set), mount item 0x3ECC, statuette 0x9ED5 (`windrunner_south`). Body 1410 is typed Equipment in pinned's `bodyTable.cfg` (P59), so as a creature it lacks idle animations; as an ethereal that does not matter. | The evo dog line already uses the windrunner as a last-stage choice (`Mobiles/Evo/EvoPetData.cs`, P365). An ethereal is a different thing: an item, no slots. |
| 7 | `ethereal-boura-hellhound` (Yvan Major) | **A full replacement of the core `Ethereals.cs`** (the base `EtherealMount` and 15 stock mounts) plus solid Tiger, Ancient Hellhound and Boura ethereals. | 1 file, 1,015 lines, 18 Ser. Replacing a pinned file: a core edit. | Tiger 1254/1255 and mount items 0x3EC7/0x3EC8 (our `WildTiger` already rides on 16071, 0x3EC7); hellhound body 1069 (full action set), mount item 0x3EC9, statuette 0x3FFD; boura mount item 0x3EC6, statuettes 0x46F8/0x46F9. | Only the three new classes matter, and ServUO stock has them too (`Ethereals.cs:1080`, `:1116`, `:1152`). Boura and wild tigers already exist on the shard as tamable creatures. |
| 8 | `tameable-dragon` (TwilightRaven) | A dragon that does not anger on taming; flies (`CanFly`). 3 slots, tame 93.9. | 1 file, 161 lines, 1 Ser. | Stock bodies 12/59. | **Pinned's `Dragon` is already tamable** at 93.9 and 3 slots (`Mobiles/Monsters/Reptile/Magic/Dragon.cs:41-43`); the only change is no anger. The shard also has the Rideable Red Dragon rewards (P277). |
| 9 | `tameable-ancient-wyrm` (TwilightRaven) | Ancient wyrm (body 46) with `Tamable = true`, no anger. **Sets neither `MinTameSkill` nor `ControlSlots`**, so it takes the defaults: 1 slot and no skill floor. 1,096-1,185 Str, 29-35 damage, Magery 80-100. | 1 file, 169 lines, 1 Ser. | Stock body 46. | A 1-slot ancient wyrm anyone can tame. No overlap worth keeping. |
| 10 | `tol-dinos` (LimpBizquick; EA Time of Legends) | Eight Eodon dinosaurs and Myrmidex as generic 7,000-10,500-hit mobs; a Dragon Turtle and baby; `TEggs`, an egg that hatches a **bonded** Dragon Turtle with no follower-slot check; six "battle" pets (five elemental chicken lizards, a cold battle scorpion; 2 slots, tame 100) and "EnormiousDragon" (body 826, 4 slots, tame 104.7); drops: 13 half aprons, 7 cinctures, bunny slippers, a Blessed dragon turtle cloak and robe, six Eodon stealables. | 45 files, 3,017 lines, 50 Ser. No core edit. | Bodies 1285-1294 all in the client (AnimationFrame3.uop). 716, 717 and 826 present. | **Mostly already on the shard** with EA values: Allosaurus, Archaeosaurus, Dimetrosaur, Najasaurus, Saurosaurus (`Mobiles/Normal`), Anchisaur, Gallusaurus, DragonTurtleHatchling (`Services/Expansions/Time Of Legends/Mobiles`), `BattleChickenLizard`, `DragonTurtleHatchlingNet`. Myrmidex is the only body here we do not use. |
| 11 | `turtle-mob` (Neshoba) | Turtle Queen boss (body 1288, 85-95k hits, 102-109 damage, teleports), Turtle Spirit (drains pets and players), and five Blessed gear drops. **Not tamable**; not a mount. | 7 files, 1,079 lines, 7 Ser. | Bodies 1288, 1294, in the client. | Not companions or mounts. A field boss idea at most; the shard has its own boss work (P786 witch, the champion pack). |
| 12 | `elemental-slimes` (clark71822) | A slime (body 51) that rolls one of five elements; 30-42k hits, 80-115 damage; spell hits split off up to 10 plain slimes; drops one of five elemental daggers. **Not tamable.** | 2 files, 458 lines, 6 Ser. | Stock body 51. | Not companions or mounts. The daggers are 23-28 damage at speed 56 (a stock dagger is 10-11). |

## Part 2: rules check

The rules: nothing that grants skill or stat points, power scrolls, bless deeds or property artifacts; usable now and
mostly helpful.

| # | Folder | Grants a banned thing? | Usable now? | Verdict |
|---|---|---|---|---|
| 1 | pack-drake | No | Breaks: missing `BackpackOfReduction`; the auto-loot lets a pet pick up other players' drops | Fails "mostly helpful" as written |
| 2 | iron-beetle | No banned item; **2 ingots per ore with no smelt check** doubles metal supply | We have a better one | Fails (economy) and redundant |
| 3 | peacock-mount | No | Yes, with a `bodyTable.cfg` row | **Passes** |
| 4 | tarantula-mount | No | **No walking art**; over-tuned | Fails "usable now" |
| 5 | tarantula-lasher-ethys | No | Lasher yes; tarantula statuette wrong and its ride unproven; saves break on reload | Lasher passes as an idea, code fails |
| 6 | windrunner-ethereal | No | Yes | **Passes** |
| 7 | ethereal-boura-hellhound | No | Yes for the three looks; the core-file replacement is not acceptable | Looks pass, code fails |
| 8 | tameable-dragon | No | Yes, but pinned already does it | Passes, redundant |
| 9 | tameable-ancient-wyrm | No banned item; **1-slot, no-skill ancient wyrm** | Breaks taming balance and control slots | **Fails** |
| 10 | tol-dinos | **Yes:** Tamer's half apron +10 Animal Taming and +10 Animal Lore; PVP half +5 Str/Dex/Int; bunny slippers +5 Dex/Int, +10 Stealth, 620 luck, 54 defense chance; Blessed dragon turtle cloak and robe; `TEggs` gives a bonded pet past the slot cap | n/a | **Fails** |
| 11 | turtle-mob | **Yes:** the Queen drops power scrolls (20 skills); Blessed cloak, robe, gloves, boots and shield with +15 stats each | n/a | **Fails** |
| 12 | elemental-slimes | No banned item; the daggers are 2.5x a dagger | n/a | Fails "mostly helpful" as written |

## Part 3: recommendations, ranked

| Rank | Item | Call | Why |
|---|---|---|---|
| 1 | **Peacock mount** (3) | **Rebuild as ours** | Real new look, art in the client, low-tier mount for new tamers (1 slot, ostard numbers). Smallest useful job. |
| 2 | **Ethereal looks** (5, 6, 7: windrunner, lasher, tiger, ancient hellhound, boura; add the peacock) | **Rebuild as ours** | New looks that cost no follower slots, which is what the companion plan wants for companions riding (`docs\companions\companions-squire-evo-research.md`, Mounts: "ethereal mounts are the better fit"). Earned, never sold (store mounts are in the Dropped tier, P119). Subclass pinned's `EtherealMount`; no core edit. |
| 3 | Tarantula mount and ethereal (4, 5) | **Idea only** | Body 1401 has only actions 29-31 in our client data. Check one ride in game first (does 0x3ECA draw under a rider?). If it does, it can join rank 2 as an ethereal; a tamable walking tarantula cannot. |
| 4 | Pack drake (1) | **Idea only** | A "drake" mule look or module for the Compact Mule, if Chase wants one. No auto-loot. |
| 5 | Myrmidex body from tol-dinos (10) | **Idea only** | The one Eodon body (1293) no shard class uses. The shard has Myrmidex items and `Quests/Eodon/MyrmidexThreat` but no Myrmidex creature; that is where it would fit. Not a pet. |
| 6 | Elemental slimes (12) | **Idea only** | A low-level slime that rolls an element is a nice spawn; normal slime numbers, no dagger. |
| 7 | Tameable dragon (8) | **Skip** | Pinned's dragon is already tamable at the same skill and slots. |
| 8 | Iron beetle (2) | **Skip** | Already ported (cc-P129); this version doubles ingots. |
| 9 | tol-dinos (10, rest) | **Skip** | We have the dinos with EA values; the drops break the rules. |
| 10 | Turtle mob (11) | **Skip** | Power scrolls and blessed stat gear; not a pet or mount. |
| 11 | Tameable ancient wyrm (9) | **Skip** | A 1-slot, no-skill ancient wyrm. |

### Prompt sketches for the two rebuilds

**Rank 1, peacock mount.** "Add a tamable Peacock mount as ours: `BaseMount`, body 1440, mount item 0x3ECF, ostard
numbers (1 slot, tame 29.1, fruit and grain), spawn it in a temperate meadow or two; add a `bodyTable.cfg` row for 1440
(Animal) through the shard's data route so it idles and cannot open doors; add 1440 to the leash's shrink art (0xA0C0)
if `ShrinkTable` lacks it; one fact (tame, ride, dismount, save and load) and a proof shot of it walking and ridden."
Size: small, 1 new file (~80 lines), 1 data row, 1 test file. Check first how body 1440 is typed in pinned's
`bodyTable.cfg` and that 0x3ECF draws under a rider (P59 left attack and hit animations unverified).

**Rank 2, ethereal looks.** "Add earned ethereal mounts as ours: subclasses of pinned's `EtherealMount` for the
windrunner (0x9ED5 / 0x3ECC), lasher (0x9E35 / 0x3ECB), tiger (0x9844 / 0x3EC7, light and dark), ancient hellhound
(0x3FFD / 0x3EC9), boura (0x46F8 / 0x3EC6) and peacock (0xA0C0 / 0x3ECF), solid hue by default; routes as League shop or
achievement rewards (proposal table for Chase, no store sale); and confirm a companion can ride one, per the companion
research note. Facts: each mounts and dismounts, saves and loads; proof shot of each ridden." Size: small to medium, 1
file (~150 lines, 6 saved types), reward-table rows, 1 test file. IDs from ServUO stock `Ethereals.cs`, not from the
downloads (row 5's file has a serialization bug and a wrong statuette ID; row 7's replaces a core file).

## CODE-INTAKE

`D:\UO\third-party\CODE-INTAKE.md` had no rows for these twelve (the scout's 11-03 run had not added them). I added one
row each, dated 11-03, with the Overseer column set to `assess (P790)`.

P790 DONE
