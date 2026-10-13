# Open play tests, sorted for the overnight bot (cc-P91)

Every open item in `testing/play-tests.json` on 2026-10-13 (164: 163 open, 1 blocked), in exactly one bucket. The bot
(`D:\ShatteredLegacy\tools\playtest-bot`) is a headless UO protocol client on a SCRATCH copy of the test world
(127.0.0.1:2595, client 7.0.117.0), with an admin and player accounts of its own. **It never marks a result**: a check
is evidence, and Chase marks on the play-test page.

- **BOT**: the pass condition is something the server sends (a message, a gump's text or buttons, an item in a pack, a
  skill value, a mobile at a place, a refusal, staying connected).
- **BOT-PARTIAL**: the bot can settle the mechanics, but part of the pass condition is how it looks. The reason says
  which half is left for Chase.
- **EYES**: art, hues, rendering, paperdolls, animation, "reads right", "feels fast enough".
- **DEPLOY**: needs live, the player package, Windows Sandbox, the website, the Shard Console, the web pages, or
  anything rule 1 forbids.
- **DECISION**: Chase picks something.

Where a check depends on a context-menu label, a tooltip line or a gump colour, the bot sees the server's cliloc number,
property text or layout code, not what the client draws, so those items are BOT-PARTIAL.

**Code under test on 2026-10-13: commit 36c7ae9 (P81), not HEAD**, because HEAD (with P82) crashes at boot. Items
from P82 on cannot be checked until that is fixed.

## Counts

| Bucket | Items |
|---|---|
| BOT | 76 |
| BOT-PARTIAL | 15 |
| EYES | 8 |
| DEPLOY | 55 |
| DECISION | 10 |
| **All** | **164** |

## Checks built (cc-P91)

18 play-test ids, plus two of the bot's own:
- `CREATE`: character creation for every race and sex, through the real packet;
- `D41`: the Guild Directory regression.

Ids with a check: P56-4, P56-6, P58-0, P61-3, P61-5, P62-1, P62-7, P64-1, P64-2, P64-3, P64-4, P64-5, P64-6, P66-7, P71-7, T-039, T-046, T-047.
The other BOT and BOT-PARTIAL items are the backlog for the next nights: the sketches at the end say how each could be
checked.

## Items by prompt group


### client-test-queue

| id | bucket | reason |
|---|---|---|
| T-001 | BOT-PARTIAL | Bot: the craft gump layout carries the MAKE X entry text/cliloc; Chase: the text is actually visible in the client (the original bug was a drawing one) |
| T-002 | BOT | Quest gump, skill updates and the quest-complete message are all server-sent; note the 5x test multiplier caveat |
| T-003 | BOT | Craft gargish plate (Blacksmithy) and cloth (Tailoring) on a gargoyle, equip: item in pack then worn layer. Row is BLOCKED; bot result says whether it still is |
| T-004 | BOT | Walk the four craft gumps, read each new entry's required skill from the detail page; assert not 0 and not 120 |
| T-005 | BOT | Scan every craft gump page for WoodPulp / WorkableGlass entries; assert none |
| T-006 | BOT | Admin runs [GenerateSpawners, [go to Ter Mur, Abyss, Underworld; count mobiles in range |
| T-007 | BOT | Run the two generators, visit both, count distinct mobile names/bodies seen against 41 and 37 |
| T-008 | DECISION | Pass condition is "decides whether Q-064's lines get written"; bot can [go 719 1863 40 and list what is there |
| T-010 | BOT | Find the gargoyle alchemist, save, restart the scratch shard, re-read its name/title and [props type |
| T-011 | DEPLOY | Website panel |
| T-012 | EYES | Paperdoll rendering of a petrified clone |
| T-013 | BOT-PARTIAL | Bot: the chest is locked and trapped (lock/trap messages, trap fires); Chase: it renders as a chest |
| T-023 | BOT | Thief character steals LightInTheVoid; item lands in pack or the refusal text says why (weight) |
| T-024 | BOT | [go Labyrinth, find a Miasma mobile near the spawner, kill it, corpse appears |
| T-025 | BOT | Same as T-024 for Lady Lissith in Twisted Weald |
| T-026 | BOT | [GenStealArties, wait 15 min, [go TerMur 1134 1204 7, see HalfEatenSupperArtifact item, steal succeeds |
| T-027 | BOT | [add TreasureMapChest 5 several times, list contents; count orc/tribal masks and read their properties |
| T-028 | DEPLOY | Live deploy, console Stop/Start, docker logs |
| T-031 | BOT | Measure skill gain per use with and without the multiplier; ClusterFSkillGain bonus gains still appear |
| T-032 | DEPLOY | Config edit on the live port and reading the server log; not a protocol check |
| T-039 | BOT-PARTIAL | Bot: first-login message names the board and the board item is within range of the start point; Chase: a new player can actually find it by eye |
| T-041 | BOT | Join a guild, list pack: the creation items for the guild skills are there; Smiths join keeps ingots |
| T-042 | BOT | Ask for the starter item twice: item once, quest marked done, second ask gives nothing |
| T-044 | BOT | Gargoyle Tailoring gump lists the 8 gargish cloth armor pieces and they craft; garments absent |
| T-045 | BOT | Second character on a joined account: guild gump says not a member; joining hands its own items |
| T-046 | BOT | Reset stone and [ResetMyAccount open the same gump (same text/buttons); each scope clears what it says |
| T-047 | BOT | Young countdown message text (days and hours vs 336 h); "I want to grow up!" brings the confirm gump |
| T-048 | BOT-PARTIAL | Bot: Liaison and Survey Archivist positions and the tent pieces' coordinates; Chase: two tents look right and the NPCs stand at the openings |
| T-014 | DEPLOY | Website panel |
| T-015 | DEPLOY | Website heartbeat |

### P56

| id | bucket | reason |
|---|---|---|
| P56-1 | BOT | Hand in a deed as a member; system message "Society of Smiths: +n standing, +52 Smithing Seals banked." and balance grows |
| P56-2 | BOT | Non-member hands a deed to a town Blacksmith; gold and a reward item land in pack |
| P56-3 | BOT | Ask mode: the hand-in gump's Bank button text carries the new Seal figure |
| P56-4 | BOT | Smelt Platinum at 112.4: refusal message, ore stays; at 112.5 smelts about half the time |
| P56-5 | BOT | Satchel smelt at 112.4: "left unsmelted"; at 112.5 ingots appear in the satchel |
| P56-6 | BOT | Valorite refused at 98.9, smelts at 99; iron smelts at any skill |
| P56-7 | BOT-PARTIAL | Bot: context menu entries' cliloc ids and that each opens its gump / breeding target prompt; Chase: the labels show as words in the client (custom clilocs, D79) |

### P57

| id | bucket | reason |
|---|---|---|
| P57-1 | BOT | Seal catalog gump text: Sturdy Shovel 150, Mining Gloves +5 1,800, Salvage Bag 750, Valorite runic 45,000; deed still +52 |
| P57-2 | BOT | Celestial exceptional 20 deed banks about 1,466 Seals (message) |
| P57-3 | BOT | Mine a Platinum vein at 112.4 (iron only) and 112.5 (Platinum about half), count ore types in pack |
| P57-4 | BOT-PARTIAL | Bot: Bulk Order Info opens the Small/Large gump with the "Completed orders" line; Chase: opaque and the line fits |
| P57-5 | BOT-PARTIAL | Bot: context menu cliloc ids for Breed, Smelt Ore, Metal Familiarity and the panel opens; Chase: labels read in the client, and the un-updated TazUO.exe blank-row check (real client launch) |
| P57-6 | EYES | No row overlaps, tabs on two rows, opaque, line breaks: layout |
| P57-7 | BOT | Steal from a 150-ingot pile at Stealing 150; amount moved to pack at most 100 |

### P58

| id | bucket | reason |
|---|---|---|
| P58-0 | BOT-PARTIAL | Bot: [version history on a player has the 2026.10.02 to 10.05 sections and no Staff lines; Chase: the patch-note wording reads right |

### P59

| id | bucket | reason |
|---|---|---|
| P59-0 | DECISION | Evo pet body sheet: pick bodies per stage ("Decisions for Chase") |

### P60

| id | bucket | reason |
|---|---|---|
| P60-1 | DEPLOY | Shard Console Commit tab |
| P60-2 | DEPLOY | Console Preview commit |
| P60-3 | DEPLOY | Console DRY RUN commit dialog |
| P60-4 | DEPLOY | Console commit wait list |
| P60-5 | DEPLOY | Real commit and push |
| P60-6 | DEPLOY | SYSTEM remote shell refusal of the commit script |

### P61

| id | bucket | reason |
|---|---|---|
| P61-1 | BOT | Craft in Frost/Obsidian/Valorite at the given skills; read Blacksmithy base updates and success counts |
| P61-2 | BOT | At 150 with "Orders that still teach me", Frost deeds name any armor piece, not only plate tunics |
| P61-3 | BOT | Achievements gump text: "Oh Look, It's Dead" has its Earned line and no "Progress: 9/1"; unearned ones show progress |
| P61-4 | BOT-PARTIAL | Bot: deed gump text "All items must be made with Frost ingots." and the same OPL line, large deed too; Chase: the un-updated TazUO.exe blank-line check (real client launch) |
| P61-5 | BOT | [version history holds 2026.10.05.2 with its four lines (current version is newer, assert the history page) |

### P62

| id | bucket | reason |
|---|---|---|
| P62-1 | BOT | Female character: [add KitsuneEarsTail, equip; the item shows on her worn layer |
| P62-2 | EYES | Paperdoll placement of ears and tail |
| P62-3 | EYES | Walk animation down-left |
| P62-4 | EYES | Walk animation down-right |
| P62-5 | EYES | Other directions show nothing (visual expectation) |
| P62-6 | EYES | Does it read as fox ears and a tail |
| P62-7 | BOT | Male equips it: message "Only females can wear this." (cliloc 1010388), item stays in pack |
| P62-8 | BOT | Restart the scratch shard, the female still has the item on its layer |

### P63

| id | bucket | reason |
|---|---|---|
| P63-1 | DEPLOY | Console Player package tab |
| P63-2 | DEPLOY | Player package build |
| P63-3 | DEPLOY | Publish player package |
| P63-4 | DEPLOY | Console window prompt visibility |
| P63-5 | DEPLOY | Deploy built image to the test shard |
| P63-6 | DEPLOY | Console refuses the current image |

### P64

| id | bucket | reason |
|---|---|---|
| P64-1 | BOT | Fresh account login: bulletin gump title is the current version, has the new lines, an "All patch notes" button and no wiki button (version is newer than 2026.10.05.3 now) |
| P64-2 | BOT | Press All patch notes: history gump arrives; relog, no bulletin gump |
| P64-3 | BOT-PARTIAL | Bot: [version text and "(you are here)" on page 1; Chase: the entry shows gold |
| P64-4 | BOT | Page with Next to "Page N of N", last page ends with 2026.10.01; Previous returns |
| P64-5 | BOT-PARTIAL | Bot: the 2026.10.05.2 line ends "The chance to make the item is unchanged."; Chase: it wraps onto four rows |
| P64-6 | BOT-PARTIAL | Bot: "Staff (players do not see this list)" present for admin, absent for player; Chase: shown lavender |

### P65

| id | bucket | reason |
|---|---|---|
| P65-0 | BOT-PARTIAL | Bot: [EvoPet give/xp/loops/bond/info walk (Echo lines, pick gump, body id changes), reset stone, stable/claim, death and res, doors; Chase: the swing/hit/death/idle animation table, plus the section 9 decisions |

### P66

| id | bucket | reason |
|---|---|---|
| P66-1 | BOT | Hide 5 tiles from a fight: "You can't seem to hide right now."; at 9+ works; Hiding base passes 100 |
| P66-2 | BOT | Detect Hidden: no gain on empty spot, reveals a hidden second character, "[trapped]" on a trapped chest, 15-tile hider not found |
| P66-3 | BOT | Repeated steals from a monster at 127.5 with +20: caught roughly 1 in 5 (caught message count) |
| P66-4 | BOT | Peacemaking success rate at 200 vs 120 the same; Musicianship base rises past 120 |
| P66-5 | BOT-PARTIAL | Bot: share of incoming swings that cost HP at Parry 200 vs 120; Chase: blocks as seen (parry has no server message) |
| P66-6 | BOT | Tactics base rises toward 200 with a +15 item worn |
| P66-7 | BOT | [ClusterFSkillGain output text includes the rate and "past stock ceilings on" |

### P67

| id | bucket | reason |
|---|---|---|
| P67-1 | BOT | Carpentry gains in Frostbark, stops at 155, Shadowbark gains; at 99.9 Ironwood says "You cannot work this strange and unusual wood." |
| P67-2 | BOT | Fletching 150 Frostbark bows gain, kindling never |
| P67-3 | BOT | Tinkering gump material list Platinum..Celestial; scissors gain at 150, stop at 162.5 |
| P67-4 | BOT | Blacksmithy 180 plus a +10 item: base caps at 187.5 |
| P67-5 | BOT | Orders at 150 with the toggle on are all Frost post-Valorite; off: Platinum, Toxic, Blaze reappear |
| P67-6 | BOT | Explosion trap HP loss at Tinkering 200 vs 120; Remove Trap failure rate |
| P67-7 | BOT | Axe damage at Lumberjacking 148 vs 100 (target HP via [props), statistical |

### P68

| id | bucket | reason |
|---|---|---|
| P68-1 | DEPLOY | Console commit countdown and Force |
| P68-2 | DEPLOY | Console Check selected package |

### P69

| id | bucket | reason |
|---|---|---|
| P69-1 | BOT | Registrar errand: refused at Iron, 49 ore refused, 50 ore + 25 ingots accepted, bonded Compact mule (hue number), "You have your mule", "Replace my mule" |
| P69-2 | BOT-PARTIAL | Bot: upgrade to Bronzeback, name, hue number, hits, pack size, contents and bond kept; Chase: each tier's hue looks right on the body |
| P69-3 | BOT | Breed two mules, restart scratch shard (or [props DeliverAt), foal deed arrives in bank |
| P69-4 | BOT | Foal deed OPL lines: sex, tier 1, generation, family line, qualities, bloodline |
| P69-5 | BOT | Trade a foal deed between the bot's two characters; the receiver's mule is theirs with the foal's genes ([props) |
| P69-6 | BOT | Existing mules on the copied world: Shadowhide, 1 slot, owner's follower count |

### P70

| id | bucket | reason |
|---|---|---|
| P70-1 | BOT | Tinkers' Union hall gump: buy Clockwork Load Harness I schematic with scrip and vouchers |
| P70-2 | BOT | Mule Modules group: crafts with materials, gump refuses without |
| P70-3 | BOT | Drop module on mule (OPL lists it), Options > Remove returns it to pack as tier I |
| P70-4 | BOT | [add MuleModule TimberRack 3 on a tier 1 mule: refused, still in pack |
| P70-5 | BOT | Tier II craft consumes the tier I only on success |
| P70-6 | BOT | Trailwise Tack III: status follower count drops by one, returns on removal |
| P70-7 | BOT | Trailwise II homing: after a gate the mule appears beside the bot within seconds; "all come" works |
| P70-8 | BOT | Soul Tether II: corpse empty, pack still on the ghost ([props), resurrect |
| P70-9 | BOT | Ore Hopper fitted: mule pack weight drops ([props or container weight) |
| P70-10 | BOT | Survey II: Options lists the map, quest arrow packet points at it; III: "Dig here" spawns chest and guardians |
| P70-11 | BOT | Trader's Ledger III: bank opens in town, refused in a dungeon, while criminal, after a fight |

### P71

| id | bucket | reason |
|---|---|---|
| P71-1 | BOT | Twenty Nerve Strikes at Bushido 200 vs 120; count paralyze messages |
| P71-2 | BOT | Stable 23 pets at 200 taming/lore/vet, the 24th refused |
| P71-3 | BOT | Fire Horn damage at 200 vs 120 (target HP via [props), about +10% |
| P71-4 | BOT | Count steps until "revealed" at Stealth 200 (about 34) and 120 (about 24) |
| P71-5 | BOT | Bandage heal amounts at 200 within 54 to 90 |
| P71-6 | BOT | Harness edits the scratch copy's stepsAt200 to 30 and restarts; steps become 30 (scratch config only) |
| P71-7 | BOT | [version history holds 2026.10.10 with five lines (current version is newer) |

### P72

| id | bucket | reason |
|---|---|---|
| P72-0 | DECISION | Leveling gear research; "Decisions for Chase" |

### P73

| id | bucket | reason |
|---|---|---|
| P73-1 | DEPLOY | Console run as Chase |
| P73-2 | DEPLOY | Real test shard on the P73 image |
| P73-3 | DEPLOY | Console wipe test accounts |
| P73-4 | DEPLOY | Console wipe dialog |
| P73-5 | DEPLOY | Console wipe confirmation |
| P73-6 | DEPLOY | Wipe window, real test shard saves |
| P73-7 | DEPLOY | Log in after the real test shard wipe, TazUO profiles |

### P74

| id | bucket | reason |
|---|---|---|
| P74-1 | DEPLOY | Console launch |
| P74-2 | DEPLOY | Console Autopilot tab |
| P74-3 | DEPLOY | Test email |

### P75 to P82

| id | bucket | reason |
|---|---|---|
| P75-0 | DECISION | League rewards proposal; open questions for Chase |
| P76-0 | DECISION | Extra facets research; B.6 decisions |
| P77-0 | DECISION | Alembic guild: rank names, currency, guildmaster, world step; bot can run [ClusterFSeedAlembicHall on scratch and read the 18-row directory |
| P78-0 | DECISION | Recipe gating: 12 decisions with defaults taken; bot can gather [RecipeGating and [Recipes output |
| P79-0 | DECISION | Loot boxes and fanfare: 9 decisions; bot can gather [LootBox / [Fanfare output |
| P80-0 | DECISION | Tutorial: 8 decisions (veterans, recruiter, voice); bot can run [Tutorial status on scratch |
| P81-0 | EYES | Paperdoll bodies, spell icons, custom art, local NSFW switch |
| P82-0 | BOT | **Could not run: the code with P82 does not boot** (ImbueCatalogue's static initializer reads SkillInfo.Table before SkillsInfo.Configure fills it; cc-P91 notes). Otherwise server-side: imbue rows at the table, read a formula book, Overcharged at an ArtificersSoulForge, custom property OPL line; rank-4 rung and mule socket are separate decisions |

### P83

| id | bucket | reason |
|---|---|---|
| P83-1 | DEPLOY | Play-test page |
| P83-2 | DEPLOY | Play-test page cards |
| P83-3 | DEPLOY | Play-test page buttons |
| P83-4 | DEPLOY | Play-test page Failed view and console tile |
| P83-5 | DEPLOY | Play-test page manual items |
| P83-6 | DEPLOY | Play-test page picks up new notes |
| P83-7 | DEPLOY | Console PLAY TESTS tile |

### P84

| id | bucket | reason |
|---|---|---|
| P84-1 | DEPLOY | Console Look setting |
| P84-2 | DEPLOY | Console separate windows |
| P84-3 | DEPLOY | Console output pane |
| P84-4 | DEPLOY | Console gump art cache |
| P84-5 | DEPLOY | Console tooltips |

### P85

| id | bucket | reason |
|---|---|---|
| P85-1 | DEPLOY | Homepage services.yaml entry |
| P85-2 | DEPLOY | judge.py and the Shard status header; not a shard check |

### P86

| id | bucket | reason |
|---|---|---|
| P86-0 | DEPLOY | Console VPN disconnect with Proton, DNS tile, sl-ddns |

### P87

| id | bucket | reason |
|---|---|---|
| P87-1 | DEPLOY | Console screenshots and window narrowing |
| P87-2 | DEPLOY | Autopilot commit script quoting fix (cc-autopilot.ps1) |
| P87-3 | DEPLOY | Docs repo commit contents |

### P88

| id | bucket | reason |
|---|---|---|
| P88-1 | DEPLOY | Restart sl-play-tests service |
| P88-2 | DEPLOY | Homepage reload |
| P88-3 | DEPLOY | Shared menu on three web pages, phone |
| P88-4 | DEPLOY | Play-test page notice and Homepage bar |

### P89

| id | bucket | reason |
|---|---|---|
| P89-0 | DECISION | Haven move plan (plan only); Chase's decisions and his own Cloudflare/Tailscale steps; no shard check |

### P90

| id | bucket | reason |
|---|---|---|
| P90-1 | DEPLOY | Play-test page Ideas |
| P90-2 | DEPLOY | Play-test page Similar line and queue |
| P90-3 | DEPLOY | Play-test page Copy new ideas |
| P90-4 | DEPLOY | Play-test page Became F-NN / Declined |

Count check: 164 ids listed, 164 unique, against 164 in `open-items.txt`.

## Not built yet: how each BOT item could be checked


Setup shorthand: "admin" = the admin character; "player" = a fresh player character; all on the scratch shard.
Assert exact strings where quoted; numbers are from the notes.

- **T-001** admin [add tinker tools/hammer, open each craft gump; assert a MAKE X entry/cliloc is in the layout text. Chase checks it draws.
- **T-002** player: take a New Haven training quest, use the skill; assert skill update packets raise the skill and the quest-complete message arrives. Run once with testCenter.skillGainMultiplier off if the harness can.
- **T-003** gargoyle player, [SetSkill Blacksmith/Tailoring 100, ingots/cloth; craft gargish plate and cloth; assert items in pack and equip succeeds (worn-item packet on the gargoyle).
- **T-004** admin [SetSkill all four to 120; open each gump, walk categories, read each new entry's detail page; assert required skill not 0 and not 120.
- **T-005** same walk as T-004; assert no entry text contains "WoodPulp" or "WorkableGlass".
- **T-006** admin [GenerateSpawners per the ten files; [go Ter Mur, Abyss, Underworld; assert mobile count near the bot > 0 in each.
- **T-007** admin [GenerateNewShame, [SetupDespise, tour both; assert distinct mobile types reach 41 and 37.
- **T-010** admin [go Royal City, find the gargoyle alchemist, [props type; [save, restart scratch, relog; assert the same type/title "alchemist".
- **T-013** admin [add the hybrid treasure chest; double-click: locked message; [set Locked false, open: trap fires (HP drop / message). Chase checks the graphic.
- **T-023** admin [go to a LightInTheVoid spawn; thief player at Stealing 120; steal; assert the item reaches the pack, or record the refusal text (weight).
- **T-024** admin [go Labyrinth (Malas); assert a mobile named Miasma near its spawner; [kill; assert a corpse.
- **T-025** admin [go Twisted Weald; assert Lady Lissith; [kill; assert a corpse.
- **T-026** admin [GenStealArties; wait 15 min; [go 1134 1204 7 TerMur; assert HalfEatenSupperArtifact item; thief steals it into pack.
- **T-027** admin [add TreasureMapChest 5 x5; open; list contents; assert about one orc or tribal mask per chest with properties ([props / OPL).
- **T-031** player: raise a skill from 0 with the multiplier on and off; assert gains per use differ by about the multiplier and ClusterFSkillGain bonus gains still occur.
- **T-039** new player: assert the first-login message names the board's place and the board item is in the visible item list from the start point. Chase checks findability.
- **T-041** player joins the Smiths with ingots in pack; assert creation tools for the guild skills arrive and the ingot count is unchanged.
- **T-042** player takes the starter item twice; assert one item, the quest marked done, the second ask gives nothing.
- **T-044** gargoyle player opens Tailoring; assert the 8 gargish cloth armor entries and that one crafts; robe/sash/half apron absent.
- **T-045** account with a joined character makes a second character; assert guild gump says not a member; join gives its own items.
- **T-046** stone and [ResetMyAccount; assert identical gump text/buttons; each scope clears joined guilds as stated.
- **T-047** Young player; assert countdown text like "13 days and 23 hours of play time"; say "I want to grow up!"; assert the confirm gump.
- **T-048** [go New Haven mine camp; assert Liaison and Survey Archivist positions and two tent pieces west of the existing one. Chase checks the look.
- **P56-1** member with known Seals; [add SmallSmithBOD until iron 10 regular, fill, hand in; assert "Society of Smiths: +n standing, +52 Smithing Seals banked." and balance +52.
- **P56-2** non-member hands the same deed to a town Blacksmith; assert gold and an item in pack.
- **P56-3** set "Completed orders" to "Ask each time"; hand in; assert the Bank button's text shows the Seal figure.
- **P56-4** [SetSkill Mining 112.4, [add PlatinumOre 10, target a forge; assert "You have no idea how to smelt this strange ore!" and ore remains; at 112.5 assert ingots about half the time.
- **P56-5** [add ReinforcedOreSatchel with the ore; Smelt at 112.4: assert "left unsmelted"; at 112.5 assert ingots in the satchel.
- **P56-6** [add ValoriteOre 10 at 98.9: assert refusal; at 99 smelts; iron smelts at 0.
- **P56-7** [add TrashBag, PetMimic, PackMule (tame); request context menus; assert entries for "Clean Up Britannia", "Eat"/"Status", "Use" and that each opens its gump or "Target the ... pack mule". Chase checks the labels draw.
- **P57-1** open the Seal catalog; assert "150", "1,800", "750", "45,000" on the named rows; deed still +52.
- **P57-2** [SetSkill Blacksmith 200, Celestial exceptional 20 deed, bank; assert about 1,466 Seals.
- **P57-3** [go a Platinum vein; mine at 112.4 (iron only) and 112.5 (Platinum about half); count ore in pack.
- **P57-4** Bulk Order Info on the guildmaster; assert Small/Large gump and the "Completed orders" line. Chase: opaque, fits.
- **P57-5** context menus on mule, satchel, Hammer of Hephaestus; assert Breed, Smelt Ore, Metal Familiarity entries and the panel gump. Chase: client labels and the TazUO.exe blank row.
- **P57-7** thief [SetSkill Stealing 150, 150 iron ingots in a pack on the ground; steal; assert at most 100 moved.
- **P58-0** player [version, page through; assert 2026.10.02 to 2026.10.05 sections present, no Staff lines. Chase: wording.
- **P61-1** [SetSkill Blacksmith 150, Frost ingots; craft; assert occasional gains; at 162.5 none in Frost, gains in Obsidian; Valorite at 140 none.
- **P61-2** at 150 with "Orders that still teach me" on, ask until Frost deeds; assert item names vary beyond plate tunics.
- **P61-3** [achievements Combat; assert "Oh Look, It's Dead" Earned line and no "Progress: 9/1".
- **P61-4** [add SmallSmithBOD until Platinum..Celestial; assert gump and OPL text "All items must be made with Frost ingots." (or metal); large too. Chase: TazUO.exe blank check.
- **P61-5** [version history; assert 2026.10.05.2 with four lines.
- **P62-1** female player, [add KitsuneEarsTail, equip; assert it is worn.
- **P62-7** male player equips it; assert "Only females can wear this." and item stays in pack.
- **P62-8** restart scratch; assert the female still wears it.
- **P64-1** fresh account; assert bulletin gump title "Shattered Legacy <current version>", an "All patch notes" button and no wiki button.
- **P64-2** press All patch notes; assert history gump; relog; assert no bulletin gump.
- **P64-3** player [version; assert current version first with "(you are here)". Chase: gold.
- **P64-4** Next to the last page; assert "Page N of N" and 2026.10.01 last; Previous goes back.
- **P64-5** assert the 2026.10.05.2 line ends "The chance to make the item is unchanged." Chase: four-row wrap.
- **P64-6** admin [version: "Staff (players do not see this list)" present; player: absent. Chase: lavender.
- **P65-0** [EvoPet give dog, pick a hue, close and reopen via double-click, [EvoPet xp 500 / 2500 / 10000, [EvoPet loops 1, [EvoPet xp 40000, loops 5, bond on, [EvoPet info; assert body ids 217 > 739 > pick > 277 > 1410 and the Echo lines; reset stone keeps stage, hue, pick, bond; stable/claim; die/res; door stays shut. Chase: the animation table.
- **P66-1** [SetSkill Hiding 150; attack, step 5 tiles, hide: assert "You can't seem to hide right now."; at 9+ hides; Hiding base passes 100.
- **P66-2** Detect Hidden 150: empty spot no gain; player hides nearby, reveal; trapped chest: assert "[trapped]"; hider at 15 tiles not found.
- **P66-3** thief 127.5 with Shadow Dancer Leggings; steal from a monster x50; assert caught about 1 in 5.
- **P66-4** peacemaking success at Musicianship 200 vs 120 the same; playing raises Musicianship past 120.
- **P66-5** Parry 200, Bushido 120, Evasion, two-hander; take 100 swings; compare damaging hits vs Parry 120. Chase: blocks as seen.
- **P66-6** Tactics 185 + a +15 item; fight; assert base Tactics rises.
- **P66-7** [ClusterFSkillGain; assert output includes the rate and "past stock ceilings on".
- **P67-1** [SetSkill Carpentry 150, Frostbark boards, stools gain; at 155 none; Shadowbark gains; at 99.9 assert "You cannot work this strange and unusual wood.".
- **P67-2** Fletching 150 Frostbark logs: bows gain, kindling never.
- **P67-3** Tinkering gump materials include Platinum..Celestial; scissors gain at 150, stop at 162.5.
- **P67-4** Blacksmithy 180 + a +10 item, Mythril plate; assert base stops at 187.5.
- **P67-5** Blacksmithy 150, toggle on: orders post-Valorite all Frost; off: Platinum, Toxic, Blaze.
- **P67-6** explosion trap at Tinkering 200 vs 120; compare HP loss; Remove Trap failure rate.
- **P67-7** axe damage at Lumberjacking 148 vs 100 on a dummy ([props Hits before/after).
- **P69-1** fresh player registers; "The Compact's Mule" refused at Iron; set Dull Copper rank; 49 ore refused, 50 ore + 25 ingots accepted; assert a bonded Compact mule, 1 slot; "You have your mule"; release: "Replace my mule".
- **P69-2** grant currencies and 25,000 gold; Civic Mule Exchange; assert Bronzeback name, hue number, higher hits, bigger pack, contents/name/bond kept. Chase: hue on body.
- **P69-3** two mules of each sex, Breed; [save, restart scratch (or [props DeliverAt); assert foal deed in bank.
- **P69-4** read the foal deed's OPL; assert sex, tier 1, generation, family line, qualities, bloodline.
- **P69-5** trade the deed to the other character; use it; assert their mule with the foal's genes.
- **P69-6** [props on an existing mule; assert Shadowhide, 1 slot, owner's follower count.
- **P70-1** join Tinkers' Union, Apprentice, 20 scrip, 5 Mining Vouchers; buy Clockwork Load Harness I schematic.
- **P70-2** craft it from Mule Modules with 15 ingots, 2 gears, 10 bone; without them assert refusal.
- **P70-3** drop on mule; OPL lists it; Options > Remove; assert back in pack, tier I.
- **P70-4** [add MuleModule TimberRack 3 on a tier 1 mule; assert refusal, still in pack.
- **P70-5** craft tier II with a tier I in pack; assert tier I gone only on success.
- **P70-6** Trailwise Tack III on a tier 3 mule; assert followers -1, back on removal.
- **P70-7** Trailwise II; gate away; assert mule beside the bot within seconds; "all come" from afar.
- **P70-8** Soul Tether II; kill full mule; assert empty corpse, pack on ghost; resurrect.
- **P70-9** 100 iron ingots in mule pack; fit Ore Hopper; assert pack weight drops.
- **P70-10** decoded map in mule pack, Survey II: Options lists it and a quest arrow packet points at it; III at the spot: "Dig here", chest and guardians appear.
- **P70-11** Trader's Ledger III: "Open your bank box" works in town; refused in a dungeon, while criminal, after a fight.
- **P71-1** Bushido 200, Nerve Strike x20; about 1 non-paralyze; at 120 about 2.
- **P71-2** Taming/Lore/Vet 200; stable 23 pets; assert the 24th refused.
- **P71-3** four bard skills 200, Fire Horn on a dummy; damage about +10% over 120.
- **P71-4** Stealth 200 hidden; count steps until revealed (about 34); 120 about 24.
- **P71-5** Healing/Anatomy 200; bandage a hurt character; heals 54 to 90.
- **P71-6** harness sets scratch clusterf.skillScaling.stealth.stepsAt200 = 30, restarts; assert about 30 steps.
- **P71-7** [version history; assert 2026.10.10 with five lines.
- **P82-0** imbue a few rows at the table, read a formula book, place an ArtificersSoulForge and try Overcharged, read the custom property's OPL line.
- **D41 regression (extra)** player double-clicks the New Haven board: Guild Directory gump; assert each guild name appears once (Artificers' Order once), 18 rows across 3 pages of 8 now that the Alembic is registered (P23 said 17 before P77); League Registrar's Guild Referrals lists the same rows.
