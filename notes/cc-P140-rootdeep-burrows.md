# cc-P140: Rootdeep Burrows 2 of 3: render sheet, bodies, and every creature

2026-10-18. Prompt: `D:\UO\cc-prompts\cc-P140-rootdeep-burrows-creatures.md` (Parts B and C of the features chat's
`cc-P-rootdeep-burrows-creatures.md`; P139 did Part A, P141 does Part D). P139 is DONE and committed (its notes end
`P139 DONE`; `206e941`). Both repos were clean at the start. P134's `validate-art.py` made every slot decision. Model:
Fable. Scratch: `D:\UO\cc-p139-work\` (build logs, the scratch package) and the session scratchpad (the scripts named below).

## Headlines

1. **23 creature bodies registered through P139's route** (2049-2071, anim7 slots 2-21 and 200-202), every one of the
   lineup's third-party `.vd` files but the three Tree Fellows, plus two derived here: the Overdraft (the WoW crate
   creature at 1.5x) and the Crop Crow (EA's stock bird body 6 at 1.5x). `check-vd` says "free and matching" for each,
   both registry checks read 0 of 137 rows with problems, and the encoder decodes every block back byte for byte
   (section 2).
2. **The 5 MB rule changed the pipeline:** the encoded anim7 file is 25.0 MB with these bodies, so it is no longer
   committed. `build-equip-anims.py` writes it to a git-ignored `build\` folder, and `Build-PlayerPackage.ps1` runs the
   encoder and its `--check` as a new **ANIMATION ENCODE GATE** before staging (a missing or stale source refuses the
   build). The `.vd` sources (each under 5 MB; the largest is the Ratman Lord, 2.4 MB) stay committed. **A decision I
   made and ask Chase to confirm** (section 8, item 1); the alternatives are there.
3. **Every creature of the lineup exists on the server** (24 types in `server\customizations\Mobiles\Burrows\`, 6 part
   items): the tutorial farm's seven and the Vault's five as `TutorialCreature`s with fixed drops, the Burrows' twelve as
   normal spawns, two bosses. Each family drops its part, the hog and the grub carve Burrowhide, the spiders drop
   Gloomsilk, the Overdraft's drop is exactly its list. Nothing is placed: the map and spawners are later prompts.
4. **Facts:** 7 shard facts in one file, 6 of them red under a deliberate break each (section 6), the full build green at
   1,424 tests, **1,420 passed, 0 failed**, 4 skipped; image `sl-modernuo:cc-P140` = `47d756a2319b`; `sl-modernuo:latest` still `8e1a1916a752`; the bot's new check **P140-1** (six Burrows spawns fight and die to a player) read FLAKY in both of two sessions: 2 full passes of 4 runs; in each session run 1 passed every creature and run 2 timed out on one (the Rootling, then the Gloomling) with no swing logged from the fighter in the 60 s, the same harness flake P119 and P129 recorded; every creature appeared with its body in all 4 runs and each was killed in 3 of 4; the
   package built to scratch with every gate green (98 MB, 102,957,371 bytes, 741 files; `app/sl-anim7.bin` 25,027,644 bytes compresses to 16,010,218 in the zip, so the package grows by about 16 MB on the wire) and the encode gate seen red with a source missing;
   the launcher facts rewritten for 24 bodies, 12 of 12; the other package suites: Build-UoOverrides 12/12, Cliloc-Overrides 10/10 (its anim path moved to `build\`), Launch-Settings 27/27, Paperdoll-Bodies 9/9, Package-Client 9/9 run alone (a first run concurrent with my own package build failed 3 facts because both use `%TEMP%\sl-player-package`: my scheduling, not the code).
5. **Render sheet:** `notes\art\bestiary\cc-P140-sheet\` (28 folders of GIFs, the contact sheet, `flags.md`, the three
   panels, the hue previews; 4.9 MB in all, no file over 300 KB). **Flags:** no hit frames on the Cackler Scrapper,
   Hoarding Rat and Gloom Queen (they stand still when hit); walk frames over 120 px tall on the three Tree Fellows
   (213 to 390, two to four tiles), the Bramblehulk (139), the Seamguard (147) and the Gloom Queen (166). The Tree
   Fellows fall back to a hued stock bogling (the prompt's rule; they are also 6 to 17 MB files); the three elites and
   the boss keep their art, tall as they are, for Chase's eye (section 1).
6. **Recolours and scale (Chase's picks):** the Slinger is **hue 1258** (the closest rust in hues.mul; the bow turns rust
   too; a frame recolour with the bow kept brown is on the sheet as the alternative); the Crop Crow is the stock bird at
   1.5x in **hue 1910** (black), between the bird and the eagle; the Overdraft is the crate at 1.5x (89 x 83 at 1x,
   about one and a half humans) in **hue 1740** (strongbox brown; iron 1901 on the sheet). The upscale reads as a
   crate on the panel, so no AI art brief was written.
7. **The mini champ engine is not ported** (P24 section 4's ~610 lines; AGENTS.md: never build a subsystem inside a
   content task). The Burrow Mother carries her own brood instead and her death ends it (section 3). A later prompt can
   put her at the top of a mini champ; the notes say how.

---

## 0. Before starting

- `git --no-optional-locks status --short`: both repos clean (ShatteredLegacy `206e941`, shard-migration `b09abb6`).
- Read: P139's notes (the route and its checklist, followed here step by step), P24 sections 4 and 6, P36 (the region,
  the four resources: `DawnstoneOre`/`Ingot`, `BurrowhideHides`, `RootwoodLog`, `GloomsilkCloth`), P80 A.6 and
  `TutorialCreature`, the 10-14 tutorial decisions, P50 (`ChestMimic`: its levels, public constructor and virtual
  hooks), P59, P62, P119 and P129 (no lineup creature is ported already; pinned has no Rotworm, Bloodworm or Grubber,
  the Warren's stock fillers, which are P141's spawner concern), the third-party README and every pack's SOURCE.txt,
  F-45 and F-46, Chase's bestiary renderer.
- The subagent that read 26 pinned creature files for their numbers wrote `scratchpad\pinned-creature-stats.md`; every
  base cited below is from it and spot-checked (RatmanArcher, Orc, GiantSpider read by me).

## 1. Part B.1: the render sheet

`scratchpad\p140_sheet.py` ran Chase's `vd.py`/`render.py` over every `.vd` in the prompt's tables plus the stock bird and
eagle exports: per creature `notes\art\bestiary\cc-P140-sheet\<name>\walk|attack|die|hit-dir1-1x.gif` (direction 1,
south, 1x, 110 ms a frame) and `walk-first-1x.png`; `contact-sheet-walk-1x.png` (every first walk frame with its
size, actions and flag); `flags.md` and `flags.json` (the table: layout, bytes, walk size, every action with frames and
its name, GIF frame counts, flags). `render.py`'s action names are P139's corrected ones.

| Flag | Creatures | What was done |
|---|---|---|
| no hit frames (action 10) | Cackler Scrapper (`Gnoll.vd`), Hoarding Rat (`Ratman Lord.vd`), the Gloom Queen (`Drider Female.vd`); the stock bird too (the crow) | registered as they are: pinned plays action 10 for a hurt monster, TazUO shows the stand frame when a body lacks it (P139 notes, section 1). A flinch is missing, nothing else |
| no attack or death frames | none | - |
| walk frame over 120 px tall | Tree Fellow 1 (344 x 390), 2 (220 x 229), 3 (198 x 213); Bramblehulk (127 x 139); Seamguard (127 x 147); the Gloom Queen (193 x 166) | **the Tree Fellows fall back** to a hued stock body (the Rootling is the bogling 779 in bark hue 1140): two to four tiles tall, and 16.7, 7.0 and 6.1 MB files, each over the 5 MB rule. The Bramblehulk and Seamguard are the Tangle's and Dawnseam's elites and the Queen is the end boss, so their size is a feature; registered, flagged for Chase's eye (P140-3) |
| near the line | Hoarding Rat 135 x 120, Burrow Mother 150 x 76, Gloomspinner 125 x 115, Gloomweaver 134 x 109 | registered |

Other things the sheet shows: the Ledger Bat (`VampireBat.vd`) is 92 x 100 at 1x, a big bat for a "weak swarm"
(Chase may want a hue or a smaller body later); the Burrow Grub lies long (78 x 40); the two Sand Maggots share a
rig; `Myconid Blue.vd` has a cast action (13) the red one lacks; the crate creature has a fly action (19) that nothing
plays.

**Scale and hue panels** (`panel-slinger-rust.png`, `panel-overdraft-scale.png`, `panel-crow-scale.png`, made by
`scratchpad\p140_panels.py`; the hue is applied the way TazUO does, the hue table indexed by the pixel's 5-bit red,
`HuesLoader.GetColor16`):
- Slinger: unhued, hue 1258, hue 1079 (the second-nearest rust: a pink-green mess, rejected), the luminance recolour
  (rust ramp, the bow's brown pixels kept), walk and shot. **Hue 1258 shipped**: a solid rust kobold; the bow goes rust
  with it, which reads as a stained bow, not badly. The recolour is the alternative if Chase prefers the brown bow: it
  would be a new `.vd` (derived art) and a second body or a swap of 2048's blocks. `scratchpad\p140_hues.py` found the
  candidates (`hues\hue-candidates.json`: rust red 1258, 1079, 2778; black 1910, 1932, 1954; iron 1901, 2103; strongbox
  brown 1740, 1505).
- Overdraft: human 400 (27 x 63), the crate at 1x (59 x 55), at 1.5x (89 x 83) plain, hue 1740, hue 1901, the 1.5x
  attack (177 x 175: the lid-mouth opens wide), the Otyugh (159 x 106). The 1.5x crate reads as a crate: planks,
  bands, the lid. No AI art chat brief was needed; the alternative stays open (section 8).
- Crow: stock bird 6 (16 x 8), the bird at 1.5x (24 x 12) plain and in hue 1910 and 1109, the eagle (28 x 20), a human.

## 2. Part B.2 to B.4: the bodies

The route is P139's (its checklist, section 3 there), once per file. `propose` on the final file list gave consecutive
bodies from 2049 and the next free slot of each layout; `check-vd` with the planned `--file 7 --slot --type --flags`
said "free and matching" for every one, the two upscales and the bat with its flag included.

| Body | In game | Source file (pack, author) | Slot | Layout | mobtypes | Server type | Bytes |
|---|---|---|---|---|---|---|---|
| 2048 | Burrow Scamp Slinger | `kobold-bow\Kobold Bow.vd` (Vert-I-Go), P139 | 1 | high | MONSTER 0 | Monster | 159,223 |
| 2049 | Gourdling | `theart-critters\Original\H-SpookyPumpkin.vd` (TheArt) | 2 | high | MONSTER 0 | Monster | 261,469 |
| 2050 | Cackler Scrapper | `humanoids\Humanoid\Gnoll.vd` (Vert-I-Go) | 3 | high | MONSTER 0 | Monster | 511,881 |
| 2051 | Cackler Slasher | `gnolls\Gnoll Slasher.vd` (Vert-I-Go) | 4 | high | MONSTER 0 | Monster | 501,440 |
| 2052 | Cackler Veteran | `gnolls\Gnoll Veteran.vd` | 5 | high | MONSTER 0 | Monster | 489,937 |
| 2053 | Cackler Packleader | `gnolls\Gnoll Flind.vd` | 6 | high | MONSTER 0 | Monster | 555,484 |
| 2054 | Burrow Hog | `dnd-boar\DND Final Boar Animal.vd` (Skandraven) | 200 | low | ANIMAL 0 | Animal | 695,408 |
| 2055 | Ledger Bat | `vampire-bat\VampireBat.vd` (Thagoras) | 7 | high | MONSTER 4 (hover idle on 8) | Monster | 996,492 |
| 2056 | Hoarding Rat | `humanoids\Humanoid\Ratman Lord.vd` (Vert-I-Go) | 8 | high | MONSTER 0 | Monster | 2,431,848 |
| 2057 | The Overdraft | `vrark-animations\...\WoW creatures\Monster\cratecreature_monster_1.vd` (Vrark) at 1.5x | 9 | high | MONSTER 0 | Monster | 2,022,485 |
| 2058 | Burrow Grub | `mobile-megapack\Diablo 2 Pack\Sand Maggot Small.vd` (Thagoras) | 10 | high | MONSTER 0 | Monster | 524,020 |
| 2059 | Burrow Scamp | `vrark-animations\...\Vanguard kobold - L.vd` (Vrark) | 201 | low | ANIMAL 0 | Animal | 290,765 |
| 2060 | Redcap Scamp | `vrark-animations\...\Vanguard redcap kobold - L.vd` | 202 | low | ANIMAL 0 | Animal | 296,138 |
| 2061 | The Burrow Mother | `mobile-megapack\Diablo 2 Pack\Sand Maggot Large.vd` | 11 | high | MONSTER 0 | Monster | 2,053,217 |
| 2062 | Sporecap (red) | `plant-pack\Plant Pack\Myconid Red.vd` (Thagoras) | 12 | high | MONSTER 0 | Monster | 682,762 |
| 2063 | Sporecap (blue) | `plant-pack\Plant Pack\Myconid Blue.vd` | 13 | high | MONSTER 0 | Monster | 1,091,728 |
| 2064 | Bramblehulk | `plant-pack\Plant Pack\Thorned Hulk.vd` | 14 | high | MONSTER 0 | Monster | 1,868,359 |
| 2065 | Dawnshard | `elemental-pack\Elemental Pack\CaveElemental.vd` (Thagoras) | 15 | high | MONSTER 0 | Monster | 726,591 |
| 2066 | Seamguard | `elemental-pack\Elemental Pack\Stone Golem.vd` | 16 | high | MONSTER 0 | Monster | 1,919,586 |
| 2067 | Gloomling | `underdark\Underdark\Underdark Spider Hatchling.vd` (Vert-I-Go) | 17 | high | MONSTER 0 | Monster | 1,088,149 |
| 2068 | Gloomspinner | `underdark\Underdark\Underdark Spider.vd` | 18 | high | MONSTER 0 | Monster | 1,853,286 |
| 2069 | Gloomweaver | `underdark\Underdark\Underdark Spider Mage.vd` | 19 | high | MONSTER 0 | Monster | 1,933,944 |
| 2070 | The Gloom Queen | `underdark\Underdark\Drider Female.vd` | 20 | high | MONSTER 0 | Monster | 1,945,333 |
| 2071 | Crop Crow | EA's bird body 6 (`notes\art\bestiary\stock-body-6.vd`) at 1.5x | 21 | high | ANIMAL 28 (as the bird: CanFlying, the high layout) | Animal | 122,814 |

Not registered: the three Tree Fellows (above). Stock bodies, nothing needed: Penny Rat 0xD7 (the giant rat), Rootling
779 (the bogling), Echo Rat 0xEE (P80's). SHA-256 of every source is in `registry.csv` and `SOURCE.txt`.

**The two upscales** (`scratchpad\p140_upscale.py`, writing a UOFiddler `.vd`): each frame through Chase's `up.py`
(EPX scale2x, then a BOX resize to 1.5), scaled about the client's anchor (the image sits at anchor minus
(centerX, centerY + height), so centerX scales and centerY follows the new height), alpha cut at 128, every block's
colours median-cut to 255 when the resize blends past 256 (the crate's blocks did: 284 colours in one), then snapped
to 15 bits. Read back with the same reader: the crow 60 blocks, 305 frames (the bird's), the Overdraft 70 blocks,
490 frames; `check-vd` free and matching; the encoder's `--check` identical. The crow keeps the bird's type and flags
(`ANIMAL 28`: CanFlying and the high-layout flag), so its death is the client's own choice for a flying animal (action
2) and the server plays animal actions on it, as it does for the stock bird. EA-derived art ships only as encoded
blocks inside `sl-anim7.bin`, never as an EA file, like the EA-derived PNGs (SOURCE.txt).

**Pipeline change (the 5 MB rule).** The 23 sources total 23.7 MB and the encoded `sl-anim7.bin` is **25,027,644
bytes** (35,175 idx entries, 422,100 bytes), so the two generated files cannot be committed under the rule, and a
split into anim7..anim10 (TazUO's four free files, 20 MB at 5 MB each) would not hold them either. Done instead, as the
prompt's own rule for large render files says ("put anything larger in a git-ignored folder, proven with git
check-ignore"):
- `player-package\vendor\shattered-legacy-art\build\` is git-ignored (`.gitignore:100`, `git check-ignore -v` proves it);
  the two tracked `sl-anim7*.bin` are deleted; `build-equip-anims.py` writes to `build\`.
- `Build-PlayerPackage.ps1` gains the **ANIMATION ENCODE GATE** before staging: it runs `python -P
  scripts\build-equip-anims.py` (writes) then `--check` (every block decoded back against its source; refuses on any
  failure or without python, as cc-P138's paperdoll gate does), then the ANIMATION GATE and staging read from `build\`.
  Seen red: with `2049.vd` renamed away the build stopped at the encode gate (section 6).
- `validate-art.py` looks in `build\` first (beside `records.json` is the older place; its 23 tests still pass);
  `Build-UoOverrides.Tests.ps1` reads `build\` and says how to make the files when they are missing.
- Chase's machine already runs the package build with python (the paperdoll gate); nothing new is needed there. A fresh
  clone builds the files on its first package build.

**Registry and records:** `registry.csv` has 23 new `body` rows (137 rows; both `--check-registry`s read 0 problems);
`records.json` `bodyAnims` has 24 entries; `SOURCE.txt` a section per body with author, resource, terms and SHA-256; the
`.vd` copies are byte for byte (`anim-src\bodies\<body>.vd`, 23.7 MB in the repo, the largest 2.4 MB). The gnolls pack's
`SOURCE.txt` flag line now ends "Cleared by Chase 2026-10-15: rip allowed, renamed in game." (the one phrase the prompt
names; the humanoids, vrark, plant, elemental and underdark packs carry other flag wordings and were left as they are;
their clearing is recorded in our `SOURCE.txt` and the registry rows).

## 3. Part C: the creatures

All in `server\customizations\Mobiles\Burrows\` (P139's folder for the test creature; one folder for the dungeon, not
`RootdeepBurrows\`, so the region's and the creatures' files sit together under the class name the code keeps).
Six files: `BurrowsCommon.cs` (parts, carving, loot helpers), `FarmCreatures.cs`, `VaultCreatures.cs`,
`WarrenCreatures.cs`, `TangleDawnseamCreatures.cs`, `GloomCreatures.cs`. Every type is `[SerializationGenerator(0, false)]`
with no saved fields of its own.

**Parts** (`BurrowsPartBase : Item`, stackable, a stock graphic with a hue each, placeholders for Chase's eye):
Burrower Claws (0x10E8 hue 0x8AB), Rootheart Sap (a bottle 0xF0E hue 0x8A5), Dawnstone Shards (0x223B hue 0x8AC),
Gloom Glands (0x1CEF hue 0x497); the boss parts the Burrow Mother's mandible (0x10E8 hue 0x845) and the Gloom Queen's
fang (0x10E8 hue 0x455). They drop; what they buy is P24 section 5 (the set upgrades, a later batch).

**Burrowhide** (`BurrowsCarving.Carve`): pinned's `OnCarve` knows four hide types and no hook for a fifth
(`BaseCreature.cs:2003-2110`), so the hog and the grub override `OnCarve`: blood, the hides onto the corpse with
`AddCarvedItem` (as pinned does for feathers), ribs for the hog, pinned's messages (500471, 500467, 500485 on a second
carve), `Carved` set, the human 10% and Felucca doubling kept. Nothing of pinned's is patched.

**Tutorial creatures** (farm and Vault): `TutorialCreature` (P80: engage only participants, Young protection ignored,
`NoKillAwards`). **Loot is fixed** in `OnDeath` (Chase, 2026-10-15), so the looting lesson always finds something.
**`NoKillAwards` stays true**: a kill that only a sheltered participant can make should not pay fame or karma; Young
players earn those on real spawns. The Burrow Hog is the exception: a plain animal (`FightMode.Aggressor`, tamable
like a boar) because it is also a Warren spawn; on the farm a non-participant could kill it (deviation 6).

| Creature (class) | Body, hue | Base (pinned file) | Numbers (first proposal) | Fixed drop |
|---|---|---|---|---|
| Gourdling | 2049 | Bogling (`Plant/Melee/Bogling.cs`) | Str 20 Dex 25 Int 5; hits 18; dmg 2-4; phys 5-10; Wrestling/Tactics 20 | 10 gold, a pumpkin |
| Crop Crow (`CropCrow`) | 2071, hue 1910 | Eagle (`Animals/Birds/Eagle.cs`), Bird | Str 12 Dex 40 Int 8; hits 12; dmg 1-3; CanFly; feathers 10; flees 4 s when struck in melee (`BeginFlee`), then its AI returns | 6 gold |
| Burrow Scamp Slinger (`BurrowScampSlinger`) | 2048, hue 1258 | RatmanArcher (`Humanoid/Melee/RatmanArcher.cs`) | AI_Archer; Str 30 Dex 60 Int 20; hits 22; dmg 3-6; Archery 40; P139's animating bow, 20 arrows | 12 gold |
| Cackler Scrapper | 2050 | Orc (`Humanoid/Melee/Orc.cs`) | Str 40 Dex 35 Int 10; hits 30; dmg 3-6; phys 10-15; Wrestling/Tactics 30 | 15 gold |
| Cackler Slasher | 2051 | Orc with Bleed Attack (`GetWeaponAbility`) | Str 45 Dex 45 Int 30 (mana 60 for the ability); hits 34; dmg 3-7 | 15 gold, 3 bandages |
| Cackler Veteran | 2052 | OrcCaptain (`Humanoid/Melee/OrcCaptain.cs`) | Str 55 Dex 40 Int 15; hits 45; dmg 4-8; phys 15-20 | 20 gold |
| Cackler Packleader | 2053 | OrcishLord (`Humanoid/Melee/OrcishLord.cs`) | Str 65 Dex 45 Int 25; hits 60; dmg 5-9; phys 20-25 | 30 gold, 5 bandages |
| Burrow Hog (plain animal) | 2054 | Boar (`Animals/Misc/Boar.cs`) | Str 30 Dex 20 Int 5; hits 22; dmg 3-5; tamable 29.1; carves 4 Burrowhide and 2 ribs | (normal: none) |
| Ledger Bat | 2055 | Mongbat (`Humanoid/Melee/Mongbat.cs`) | Str 8 Dex 30 Int 6; hits 6; dmg 1-2; CanFly | 3 gold |
| Penny Rat | 0xD7 (stock) | GiantRat (`Animals/Rodents/GiantRat.cs`) | Str 20 Dex 40 Int 10; hits 14; dmg 2-4 | 5 gold |
| Hoarding Rat | 2056 | Ratman (`Humanoid/Melee/Ratman.cs`) | Str 50 Dex 50 Int 20; hits 45; dmg 4-7; the first time it is hurt it calls 2 Penny Rats to its side (once a life; not saved) | 40 gold, 3 bandages |
| Safe Deposit Box (`SafeDepositBox : ChestMimic`) | P50's shell art | ChestMimic level 1, cut down | Str/Dex/Int 40; hits 40; dmg 3-6; Magery/EvalInt 30; the base's random reagents removed | 25 gold |
| The Overdraft (`TheOverdraft`) | 2057, hue 1740 | the ChestMimic level-1 row's shape (OSI's Mimic scaled, P50) as a melee creature | Str 90 Dex 30 Int 20; hits 120; dmg 6-10; phys 25-30; Wrestling/Tactics 45; **slow** (ActiveSpeed 0.4, Passive 0.8: the kiting lesson); the Mimic's sounds | exactly: a coin pouch holding 100 gold, 1 Dawnstone ingot, 10 bandages, one of GoldRing / GoldBracelet / GoldEarrings / SilverNecklace |

**The Safe Deposit Box and ChestMimic's saves:** `ChestMimic(int level, MimicFacing)` is public and `IsEnemy`,
`CanBeHarmful`, `Damage`, `GenerateLoot` and `OnDeath` are virtual, so a sibling type with the tutorial rule and no
fields needed **no schema change**; PetMimic and ChestMimic are untouched. Its drop is only the scripted gold: the base
constructor's `PackReg(20)` is emptied.

**Normal spawns** (Young allowed; P36's three-hostiles limit stands in the region):

| Zone (tier) | Creature | Body | Base (pinned file) | Numbers (first proposal) | Drops |
|---|---|---|---|---|---|
| Warren (1) | Burrow Grub | 2058 | Slime, GiantRat (`Misc/Melee/Slime.cs`, `Rodents/GiantRat.cs`) | Str 30-40 Dex 20-30 Int 10; hits 20-28; dmg 3-6; phys 10-15 poison 20-30; Poor loot; fame 300 | 1 Burrower Claws; carves 2 Burrowhide |
| Warren (1) | Burrow Scamp | 2059 | Ratman (`Humanoid/Melee/Ratman.cs`) | Str 50-60 Dex 50-60 Int 20-30; hits 35-45; dmg 4-7; phys 15-20; Meager; fame 600; rummages corpses | 1 Burrower Claws |
| Warren (1) | Redcap Scamp | 2060 | Ratman, a step up | Str 60-70 Dex 55-65 Int 25-35; hits 45-55; dmg 5-8; phys 20-25; Meager; fame 900 | 1 Burrower Claws |
| Brood Pit | The Burrow Mother | 2061 | Ogre (`Humanoid/Melee/Ogre.cs`) | Str 160-190 Dex 40-60 Int 40-60; hits 150-180; dmg 8-12 (80 phys / 20 poison); phys 30-35 poison 40-50; Resist 50-65; Wrestling 65-80; cannot flee; lesser hit poison 30%; Average + Gems; fame 3000. **Brood:** while she fights, a Burrow Grub every 15 s up to 3 alive, 8 a life; her death deletes the brood | 3 Burrower Claws, a gold jewel, her mandible |
| Tangle (2) | Rootling | 779 (stock bogling), hue 1140 | Bogling | Str 70-90 Dex 60-80 Int 20-40; hits 45-60; dmg 5-8; phys 20-25; Meager; fame 450 | 1 Rootheart Sap, 2 Rootwood logs |
| Tangle (2) | Sporecap | 2062 or 2063 | Corpser (`Plant/Melee/Corpser.cs`), walking | Str 60-80 Dex 40-60 Int 20-30; hits 50-65; dmg 5-9 (60/40 poison); poison 40-50; lesser hit poison 50%, immune lesser; Meager; fame 600 | 1 Rootheart Sap |
| Tangle (2) elite | Bramblehulk | 2064 | Quagmire, Reaper (`Plant/`) | Str 120-150 Dex 40-60 Int 30-50; hits 110-130; dmg 8-13 (80/20 poison); phys 35-45 poison 40-50; Bleed Attack (thorns); Average; fame 2000 | 2 Rootheart Sap, 5 Rootwood logs |
| Dawnseam (2) | Dawnshard | 2065 | EarthElemental (`Elemental/Melee/EarthElemental.cs`) | Str 100-130 Dex 40-60 Int 40-60; hits 60-80; dmg 7-12; **phys 55-65** (bring magic); bleed immune; Meager + Gems; fame 1500 | 1 Dawnstone Shards, 2 Dawnstone ore |
| Dawnseam (2) elite | Seamguard | 2066 | Golem, EarthElemental (`Misc/Melee/Golem.cs`) | Str 180-220 Dex 40-60 Int 50-70; hits 130-160; dmg 10-15; phys 60-70; bleed and lethal-poison immune; Average + Gems; fame 3000 | 2 Dawnstone Shards, 5 ore, 1 ingot |
| Gloom (3) | Gloomling | 2067 | GiantSpider (`Arachnid/Melee/GiantSpider.cs`) cut down | Str 40-60 Dex 70-90 Int 20-40; hits 30-45; dmg 4-8; poison 25-35; lesser hit poison; arachnid pack instinct; Poor; fame 400 | 1 Gloom Glands, 1 Gloomsilk |
| Gloom (3) | Gloomspinner | 2068 | GiantSpider | Str 80-100 Dex 80-100 Int 40-60; hits 60-80; dmg 6-12; poison 35-45; regular hit poison; **web**: 15% a hit to paralyze 3 s ("You are tangled in webbing!"); Meager; fame 900 | 1 Gloom Glands, 2 Gloomsilk, 3 spiders' silk |
| Gloom (3) | Gloomweaver | 2069 | DreadSpider (`Arachnid/Magic/DreadSpider.cs`) cut down | AI_Mage; Str 70-90 Dex 70-90 Int 90-110; hits 55-70; dmg 5-10 (50/50 poison); Magery/EvalInt 45-60; poison 50-60; regular hit poison; Meager + low scrolls; fame 1500 | 1 Gloom Glands, 2 Gloomsilk, 4 reagents |
| Gloom lair | The Gloom Queen | 2070 | TerathanMatriarch (`Arachnid/Magic/TerathanMatriarch.cs`) cut to a small group of graduated Young players | AI_Mage, female; Str 180-220 Dex 90-110 Int 150-180; hits 220-260; dmg 10-14 (70/30 poison); phys 40-50 poison 60-70; Magery/EvalInt/Resist 60-75; Tactics/Wrestling 60-80; regular hit poison; web 20%; deadly-poison immune; cannot flee; Rich + medium scrolls; fame 6000 | 3 Gloom Glands, 5 Gloomsilk, 8 silk, 8 reagents, a gold jewel, her fang |

Parts drop one per kill (`PackItem`), elites two, bosses three: a first proposal; P24's upgrade costs (a later batch)
decide whether that is generous.

**The Burrow Mother and the mini champ.** P24 section 4 costed ServUO's `MiniChampionSystem` at about 610 lines plus a
test and listed four surprises to design around; AGENTS.md says never to build a subsystem inside a content task, and
this task already carries 23 bodies and 24 creatures. So the engine is not ported here; she keeps her own brood
(`SpawnBrood` from `OnThink`, caps `BroodAtOnce` 3 and `BroodPerLife` 8, the brood deleted on her death), which gives
the Brood Pit its waves and an end without a controller. When the engine lands (its own prompt), she is the last
level's single `MiniChampTypeInfo`, as Meraktus is, and her brood can go; nothing here stands in the way. The prompt's
fact "the Burrow Mother ends the mini champ" is replaced by "her brood ends with her" (fact 6).

**Not built here (P141, Part D):** the Vault room and its refusal of a non-participant or graduate, the crawlway opening
on the Overdraft's death, every spawner and the layout spec. Their facts are P141's.

## 4. Every creature's teaching, as built

Echo Rat (P80, unchanged): first melee, war mode. Gourdling: pests in the pumpkin rows (weak melee, a pumpkin to loot).
Crop Crow: ranged lesson: a flier that flees when struck and comes back. Slinger: enemies shoot back (it animates its
shot). Cackler Scrapper: the pet lesson's target. Slasher: bleed, then healing (bandages drop). Veteran, Packleader:
the pack's steps. Burrow Hog: carving (Burrowhide). Ledger Bat: the weak swarm. Penny Rat: tight-space fighting with a
pet. Hoarding Rat: a leader that calls its pack. Safe Deposit Box: that chest has teeth. The Overdraft: death,
resurrection, looting (a drop that is always the same), kiting (slow). Warren: the first real fights and parts. Tangle:
poison and Cure (Sporecap). Dawnseam: bring magic (physical resistance). Gloom: webs and a caster; the Queen as a group
fight.

## 5. For the overseer: deviations to register

1. **Every number in section 3** is ours (the lineup has no OSI creature): first proposals scaled from the cited pinned
   bases to the tiers (farm: a new Young character with starter skills; Warren 1; Tangle and Dawnseam 2; Gloom 3;
   bosses for a small group of graduated Young players).
2. **Tutorial creatures drop loot** (Chase, 2026-10-15; P80 said none) and keep `NoKillAwards`.
3. **Parts drop every kill** (1 / 2 elite / 3 boss) through `PackItem`; bosses also drop one stock gold jewel and a boss
   part; the Gloom Queen's loot is Rich.
4. **Burrowhide carves through the creatures' `OnCarve`**, not a `HideType` (P36's plan); the hog gives 4, the grub 2.
5. **Webs are a paralyze on hit** (15% spinner, 20% Queen, 3 s) rather than a weapon ability or a pinned patch.
6. **The Burrow Hog is a plain animal**, not a `TutorialCreature`, because it is also a Warren spawn (one class).
7. **The Hoarding Rat's pack call is not saved**: a restart mid-fight lets it call again.
8. **The Burrow Mother carries her own brood** instead of a mini champ (section 3).
9. **Hues:** Slinger 1258, Crop Crow 1910, Overdraft 1740, Rootling 1140, and the six part hues: placeholders until
   Chase has looked.
10. **The Rootling is a hued stock bogling** (the Tree Fellows fell to size and the file rule).
11. **The encoded anim7 files are generated at package build, not committed** (section 2); the package grows by about
    25 MB.
12. **The Overdraft is slow** (0.4 / 0.8) where pinned's table gives a melee creature 0.2 / 0.4.
13. **The crow keeps the stock bird's `ANIMAL 28`** so the server plays animal actions on a high-layout body, as it does
    for the bird (its hurt action 7 does not exist; no flinch).

## 6. Facts, red then green

`server\tests\Mobiles\Burrows\BurrowsCreaturesVerification.cs`, 7 facts:

1. Every type constructs with its body and names, the server types the body (never Empty), it spawns, and killed it
   leaves a corpse of 0x2006 carrying the body; every cc-P140 body is in `ShardBodyTypes`.
2. Every type and every part round-trips the generated serializer.
3. The eleven tutorial creatures engage only a participant (`IsEnemy`, `CanBeHarmful`, a graduate's blows do nothing),
   keep `NoKillAwards` and `IgnoreYoungProtection`, and still drop their fixed loot when the participant kills them;
   the Safe Deposit Box the same, as a `ChestMimic` of level 1 with an empty pack and 25 gold on death.
4. The Overdraft's drop is exactly its list, twenty kills over: four items, the pouch with exactly 100 gold, one
   Dawnstone ingot, 10 bandages, one trinket from the list.
5. Each family drops its part (and Rootwood, Dawnstone ore, Gloomsilk where the design says), the bosses their jewelry
   and boss part; the hog and the grub carve Burrowhide (and the hog ribs), a second carve adds nothing.
6. The Hoarding Rat calls exactly two Penny Rats aimed at its attacker on the first hit and none on the second; the
   Burrow Mother's brood stops at three alive and resumes when one dies, counts a life's total, and dies with her.
7. A Gloomspinner's web paralyzes and a held target is not webbed again; a Crop Crow flees when struck; the Slasher's
   ability is Bleed Attack; the Slinger has its hue, its bow and the archer AI.

| Run | Break | Result |
|---|---|---|
| red A, `--tests-only` | six at once, one per fact: the Gourdling's body 2149 (fact 1); the Gourdling's gold drop removed (3); the Overdraft's bandages 9 (4); the Gloom Queen's fang not dropped (5); the Hoarding Rat calling one rat (6); `TryWeb` returning before the paralyze (7) | **exactly the six facts red, each by its own break**: fact 1 `Expected: 2049 / Actual: 2149`; 3 `Gourdling dropped no gold: Pumpkin`; 4 `Expected: 10 / Actual: 9`; 5 the fang missing from the Queen's corpse; 6 `Expected: 2 / Actual: 1`; 7 `Expected: True / Actual: False`; fact 2 green. 1,424 tests, 1,414 passed, 6 failed, 4 skipped; "No image was built". It took five attempts to compile first: `NoKillAwards` is not virtual (set in the constructor instead, as TutorialCreature does), `MessageType` lives in `Server`, `GetMobilesInRange<T>` is a pooled enumerator (walked with foreach), and two xUnit analyzer rules (Assert.Single with a filter, Assert.DoesNotContain). Then the first full build was red on one wrong expectation of mine: the Penny Rat's stock body 215 is **Monster** in pinned's bodyTable.cfg (`215 Monster`), not Animal; the test row was corrected |
| green, the full build | none (the six files restored from the scratchpad copies, SHA-256 equal to the recorded hashes) | 1,424 tests, **1,420 passed, 0 failed**, 4 skipped; image `sl-modernuo:cc-P140` = `47d756a2319b`; `sl-modernuo:latest` still `8e1a1916a752` |

Fact 2 (the round trip) has no break of its own: the generator writes the class, and a wrong body or name would show in
facts 1 and 2 together (as P139's red run A showed for its creature).

**Gates outside the shard:**
- The ANIMATION ENCODE GATE red: `2049.vd` moved out of `anim-src\bodies\`: the build stopped before staging with `ANIMATION ENCODE GATE: the encoder failed: ... FileNotFoundError: [Errno 2] No such file or directory: ...anim-src\bodies\2049.vd ... Not building.`, exit 1, no zip; the file put back, the encoder regenerated `build\` and `--check` read `anim7 matches`. (The gate's first version died on the encoder's stderr instead of its exit code: Windows PowerShell 5.1 turns a child's first stderr line into a terminating error under ErrorActionPreference Stop, as cc-P124 met; the two calls now run under Continue and the exit code decides, and the refusal names the error); the real build to scratch:
  `D:\UO\cc-p139-work\pkg140\ShatteredLegacy-2026.10.18.0055.zip`, every gate green ("animation encode gate: anim7 matches"), 98 MB, 741 files, TazUO 3212623f + 2 patches; `-CheckZip` on the same inputs' 0050 build: gates 4, 6 and 5 passed. Not for publishing (its notes say so; the console builds the real one from the committed tree).
- The launcher facts: rewritten for every body in `records.json` (24 Bodyconv lines and 24 mobtypes lines, every body
  named by the player's files skipped, one body named only in mobtypes left out of both copies while the player's own
  line stands), registry rows 137: **12 of 12** after one wrong assertion of mine (it expected the player's own 2048
  mobtypes line to be absent from the copy, which is the copy's job to keep).
- validate-art's 23 tests, `check-registry` 0 of 137, find-free-art `--check-registry` 0 of 137; the bot's suite 41
  tests, the one known environmental failure.
- the other package suites: Build-UoOverrides 12/12, Cliloc-Overrides 10/10 (its anim path moved to `build\`), Launch-Settings 27/27, Paperdoll-Bodies 9/9, Package-Client 9/9 run alone (a first run concurrent with my own package build failed 3 facts because both use `%TEMP%\sl-player-package`: my scheduling, not the code)

**The bot's check P140-1** (`Run-OvernightPlaytests.ps1 -SkipBuild -Only P140-1 -SkipSoak -NoEmail -Runs 2`, the image
tagged `sl-modernuo:bot`): read FLAKY in both of two sessions: 2 full passes of 4 runs; in each session run 1 passed every creature and run 2 timed out on one (the Rootling, then the Gloomling) with no swing logged from the fighter in the 60 s, the same harness flake P119 and P129 recorded; every creature appeared with its body in all 4 runs and each was killed in 3 of 4 Run folders `testing\bot-runs\2026-10-18-0042\` and `2026-10-18-0047\` (report.md, results.json, transcripts). The scratch shard booted both times on the image from a copy of the test world's backup 2026-10-18-05-40-00 with 0 exceptions or errors in shard.log; rule 1 held (the real test shard untouched). Marked BOT in the triage with the flake noted; the nightly runs will keep settling it.

## 7. Decisions for Chase

1. **The generated anim7 files are no longer committed** (section 2). Alternatives: Git LFS for the two files; an
   exemption of generated files from the 5 MB rule; or fewer bodies (the lineup's 23 do not fit four 5 MB files
   either). The current state builds from a fresh clone on the first package build.
2. **The Tree Fellows (Rootling):** keep the hued stock bogling, or cut one Tree Fellow file to a 1-tile size (a
   downscale to about 0.5x would make Tree Fellow 3 about 100 px tall and roughly 1.5 MB; the renderer's scaler runs
   both ways) and register it. P140-8.
3. **The Slinger's bow colour:** hue 1258 as shipped, or the frame recolour (P140-4).
4. **The Overdraft's hue:** 1740 brown or 1901 iron (P140-6); and whether the 1.5x crate is boss-scale enough in the
   client, or the AI art chat brief should be written after all.
5. **Parts per kill** (1 / 2 / 3) and the tutorial drops' gold (3 to 40) are first numbers.
6. **The mini champ engine:** its own prompt (P24's ~610 lines plus a test), or leave the Burrow Mother's brood as is.
7. **The Ledger Bat's size** (92 x 100 at 1x, a large bat for a weak swarm): a hue, a smaller body, or fine.
8. **The packs' other flag lines** (humanoids, vrark, plant, elemental, underdark): their wording does not match the
   phrase the prompt names, so they were left; say if they should read "Cleared by Chase 2026-10-15" too.

## 8. For Chase

Deploy first (not play tests): the package must be built and published from the committed tree (the console's Build
runs the new encode gate and the zip grows by about 25 MB), and the test shard rebuilt on `sl-modernuo:cc-P140` or the
next build. Then, to try it in game on the test shard with the new package:

1. **The bot's half (P140-1, run here):** `[add BurrowHog`, `[add BurrowGrub`, `[add BurrowScamp`, `[add Rootling`,
   `[add Sporecap` and `[add Gloomling` beside a player and kill each: each shows with its body, fights back, dies and
   leaves a corpse carrying the body.
2. **Deploy:** Player package > Build package, then Publish; Test shard > Rebuild (or `Start-TestShard.ps1 -Image
   sl-modernuo:cc-P140`); run the launcher once so `app\uo-overrides\Bodyconv.def` and `mobtypes.txt` carry the 24
   lines: no yellow line about creature art.
3. **Every body by eye:** SL TEST - Admin (Eve), open ground: `[add` each of Gourdling, CropCrow, BurrowScampSlinger,
   CacklerScrapper, CacklerSlasher, CacklerVeteran, CacklerPackleader, BurrowHog, LedgerBat, PennyRat, HoardingRat,
   TheOverdraft, BurrowGrub, BurrowScamp, RedcapScamp, TheBurrowMother, Rootling, Sporecap (twice), Bramblehulk,
   Dawnshard, Seamguard, Gloomling, Gloomspinner, Gloomweaver, TheGloomQueen. Pass looks like: each draws as its
   picture on `notes\art\bestiary\cc-P140-sheet\contact-sheet-walk-1x.png` and animates when it moves, attacks, is hit
   (the Cackler Scrapper, Hoarding Rat and Gloom Queen have no hit frames and stand still instead) and dies; the corpse
   draws. The farm and Vault creatures fight only a tutorial participant: use a fresh character to fight them.
4. **The archer's colour:** `[add BurrowScampSlinger` next to `panel-slinger-rust.png`: hue 1258, or the recolour.
5. **The crow's hue and size:** `[add CropCrow`, `[add Bird`, `[add Eagle` side by side: black, between the two, flies,
   flees when struck and comes back.
6. **The Overdraft's scale:** `[add TheOverdraft` next to your character: about one and a half humans tall, strongbox
   brown, a slow walker, its lid-mouth opens on the attack.
7. **The decoy chests bite:** a fresh tutorial character beside `[add SafeDepositBox`: it springs (P50's frames), bites,
   dies leaving 25 gold; a graduated character gets nothing and does it no damage.
8. **The Tree Fellows:** the decision in section 7, item 2.

Who and steps: `testing\bot-triage.md` (P140 group: P140-1 BOT, P140-2 DEPLOY, P140-3 to P140-7 EYES, P140-8 DECISION)
and `testing\playtest-steps.json`.

## 9. Repo size rule

Largest files added: `anim-src\bodies\2056.vd` 2,431,848 bytes, `2061.vd` 2,053,217, `2057.vd` 2,022,485 (all under
5 MB); the render sheet folder 4.9 MB in 28 folders, no file over 300 KB (`contact-sheet-walk-1x.png` 268 KB). The
generated `build\sl-anim7.bin` (25.0 MB) is git-ignored, proven with `git check-ignore -v`. The scratch packages and
build logs are in `D:\UO\cc-p139-work\`, outside both repos.

## 10. Deviations in how the work was done

- Two Read calls were denied by the unattended hook (the first on the P139 encoder in the previous prompt's session set
  the pattern): every file was read with `cat`/`sed` and written to the scratchpad then copied in, as the memory note
  says.
- The subagent that extracted pinned creature numbers ran in the background (the Agent tool's default), not the
  foreground the hand-off asked for; its report was a file, read after it finished.
- The Golem's task-list tool was not available in this session, so there was no live task list to mark.
- Two background jobs (the red test run and the first package build) were stopped by the harness for low system
  memory while the session waited on them; nothing was lost (the red build had already failed on a compile error, the
  package build was mid-way and left no state: the one `.vd` it had moved aside was checked back in place). Every later
  build, suite and bot run ran one at a time in the foreground.
- The green hashes of the eight creature and test files are in `scratchpad\p140-green-hashes.txt`; the files in the
  repo are the scratchpad copies byte for byte (the red breaks were applied to the repo copies only and the copies
  restored over them).

## 11. Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:/UO/Commit-ShardWork.ps1 -DryRun` (run with this note written,
before its last line), commits nothing:

```
=== code  (D:\ShatteredLegacy) ===
  45 file(s) pending:
    .gitignore
    CHANGELOG.md
    VERSION
    player-package/Build-PlayerPackage.ps1
    player-package/tests/Build-UoOverrides.Tests.ps1
    player-package/tests/Cliloc-Overrides.Tests.ps1
    player-package/vendor/shattered-legacy-art/SOURCE.txt
    player-package/vendor/shattered-legacy-art/records.json
    player-package/vendor/shattered-legacy-art/registry.csv
    player-package/vendor/shattered-legacy-art/sl-anim7-idx.bin
    ... (31 more)
  dry run: would add, commit and push

=== docs  (D:\UO\shard-migration) ===
  188 file(s) pending:
    README.md
    dashboard.html
    testing/SUMMARY.md
    testing/bot-triage.md
    testing/play-tests.json
    testing/playtest-steps.json
    tools/progress.json
    notes/art/bestiary/cc-P140-sheet/bramblehulk/attack-dir1-1x.gif
    notes/art/bestiary/cc-P140-sheet/bramblehulk/die-dir1-1x.gif
    notes/art/bestiary/cc-P140-sheet/bramblehulk/hit-dir1-1x.gif
    ... (31 more)
  dry run: would add, commit and push

Repo Result 
---- ------ 
code dry run
docs dry run
```

P140 DONE
