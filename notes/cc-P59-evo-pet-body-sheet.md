# cc-P59: Evo pet body sheet (dog, cat, fox and bird lines)

2026-10-05. Notes only. Nothing was built, nothing in `D:\ShatteredLegacy` was edited (it was only grepped, read-only,
while P57 builds there), nothing was deployed or committed. Images and scripts are in `notes\cc-P59-scratch\`.

## Headlines

1. **13 of the brief's 20 candidate IDs are recolors, not separate creatures.** They have no art of their own. The
   client draws them as another body plus a hue through `Body.def`:
   - 23, 25, 27, 34, 37 and 98 (Dire, Grey, White wolves and Hell Hound) are all **225 Timber Wolf**.
   - 63, 64, 65 and 127 (Cougar, Snow Leopards, Predator Hellcat) are all **214 Panther**.
   - The brief's "Cat, also Hellcat", "Eagle, also Phoenix" and Lesser Hiryu/Hiryu are also one body per pair.
   Under Chase's "not a recolor" rule, the brief's list has **10 distinct bodies**, not 20.
2. **The client has far more dogs, cats and birds than pinned uses.** I found **25 unused body IDs** in the
   7.0.117.0 data. That is 23 distinct models, because 1254/1255 and 1553/1573 are pairs:
   - eight dogs: Malamute, Great Dane, Saint Bernard, Newfoundland, Rottweiler, Black Russian Terrier, Windrunner and
     Ancient Hellhound;
   - Orc Hellhound, Leather Wolf and Dragon Wolf;
   - Baby Tiger, Tiger (two textures), Lion, Sabertooth, Undead Tiger, and Manticore (two sizes);
   - **a second fox, 1423 "Fox_Small"**;
   - Parrot, Crow, Phoenix Bird, Peacock and Uber Turkey.
   All are listed and rendered below.
3. **The fox line is still the thin one.** Counting the third-party L_Fox, it has 3 real fox bodies (1423, L_Fox.vd,
   246 Bake Kitsune). Two of them are the same size, and there is nothing between about 35 and 87 pixels. So the
   proposal is **3 stages for the fox**.
4. **Dog and cat can each fill 5 distinct stages from EA art alone**, avoiding every common wild body. **The bird line
   needs the third-party birds** to reach 5. EA's small birds either lack combat animations (Parrot, Crow, Parrot
   Bird) or are everywhere in the wild (Bird, Eagle).
5. **Two pitfalls if an unused body is chosen:**
   - pinned's `bodyTable.cfg` types several of them as Equipment, or not at all (section 6);
   - all the new bodies use the UOP-era action numbering.

## Client data and tools

**Client data**
- I read `D:\UO\UltimaOnlineVanilla`, where `client.exe` is **7.0.117.0**. That is EA's current data, the install the
  player package's `Setup.ps1` finds and launches (`notes\player-package.md` Part C).
- The package accepts 7.0.114.40 or newer. The server's own copy (`D:\ShatteredLegacy\client-data\classic-client`) is
  7.0.114.40 and was not used.
- Any player on current EA data sees what these sheets show.

**Engine authority**
- `D:\UO\ModernUO-pinned` at `d4531cd94b739613155225c234900de9f47d2c88` (`git rev-parse HEAD`).
- Every pinned citation below is at that commit.

**Renderer:** `cc-P59-scratch\p59anim.py`. It extends P49's `uopanim.py`, reusing its UOP hash and AMOU decoder. It
resolves a body the way the classic client does, in this order:
1. `AnimationFrame*.uop` (`build/animationlegacyframe/{body:06d}/{action:02d}.bin`). Frames are split into 5
   directions the way ClassicUO does it: padded to 50, then divided by 5.
2. `Bodyconv.def`, which sends the body to anim2 to anim6 `.mul`.
3. `anim.mul`.
4. `Body.def`, which redraws the body as another body with a hue. The hue is applied from `hues.mul` and is
   approximate.

**Layouts**
- MUL layouts follow ClassicUO's `AnimationsLoader`: monster 22 actions, animal 13, people 35.
- Stand and walk actions:
  - monster: stand 1, walk 0;
  - animal: stand 2, walk 0;
  - **bodies flagged `0x10000` in `mobtypes.txt` and stored in UOP: stand 25, walk 22.**
- My first pass missed that flag. It rendered the new bodies in non-standing poses and gave four of them no walk
  frame. The sheets were re-rendered after the fix. The thumbnail scan pages (`scan\page*.png`) were made before the
  fix, so their poses for UOP bodies can be wrong. They were only used to find bodies by eye.

**Direction:** file direction 1, which the client shows as south (the three-quarter view facing down-left).
Direction 0 faces the viewer, and 4 faces away.

**Decode errors:** 130 frames out of the whole-client scan overran their UOP entry and were skipped. None belongs to
any body in this note.

**Other scripts (read-only)**
- `bodyuse.py` indexes `Body =` and mount `base(...)` body arguments in a source tree.
- `spawns.py` counts spawner entries in pinned's `Distribution\Data\Spawns`.
- `sheets.py` renders the sheets.

## Third-party .vd format (UOFiddler animation export)

Read from the bytes of all six files, and it decodes cleanly in every one:

- `int16` file tag, always `6`.
- `int16` type: `0` high/monster (22 actions), `1` low/animal (13 actions), `2` people (35 actions).
- `actions x 5` index entries of `(int32 offset, int32 length, int32 extra)`. Offsets are absolute in the file, so for
  a low body the first block starts at `4 + 65*12 = 784`.
- Each block is an `anim.mul` animation block:
  - a 256-entry `ushort` palette (1555 color);
  - `int32` frame count;
  - `int32` frame offsets, relative to the end of the palette;
  - then each frame: `int16 centerX, int16 centerY, uint16 w, uint16 h`, then run headers
    (`len = h & 0xFFF`, `y = (h>>12)&0x3FF` signed, `x = (h>>22)&0x3FF` signed), ending at `0x7FFF7FFF`.

So I decoded every file directly. The preview `.gif`/`.jpg` files were not needed.

## Part A: the candidates

How to read the table:
- **Type** is the client animation layout.
- **Stand px** is the stand frame's bounding box at 1x.
- **Frames** is all actions and directions summed.
- **Wild** is the number of spawner entries naming the class in pinned's `post-uoml` plus `shared` spawn sets, which
  is what a post-UOML world generates. `uoml` figures are in brackets where they are non-zero.
- **Our seeders place none of these classes.** Grepping `D:\ShatteredLegacy\server\customizations` found only
  comments, item names (`PhoenixHelm`, `FerretImprisonedInCrystal`) and work-order text, no spawn placements.
- A wild count against a recolored ID also applies to the art it borrows. For example, players meet the **225 art**
  in 26+463 Timber Wolf, 14+389 Grey Wolf, 0+55 White Wolf, 2+137 Dire Wolf and 2+58 Hell Hound entries.

| ID | Name (pinned class, file:line) | Art source | Type | Stand px | Frames | Wild |
|---|---|---|---|---|---|---|
| 217 0xD9 | Dog (`UOContent/Mobiles/Animals/Town Critters/Dog.cs:11`) | anim.mul 217 | animal | 27x26 | 258 | 1+96 (4) |
| 225 | Timber Wolf (`.../Animals/Canines/TimberWolf.cs:12`; also `InjuredWolf.cs:12`) | anim.mul 225 | animal | 36x35 | 258 | 26+463 (14) |
| 25, 27 | Grey Wolf (`.../Canines/GreyWolf.cs:12`) | **Body.def:7/:8 = 225, hue 946/947** | animal | 36x35 | (225) | 14+389 (14) |
| 34, 37 | White Wolf (`.../Canines/WhiteWolf.cs:12`) | **Body.def:9/:10 = 225, hue 2301/1154** | animal | 36x35 | (225) | 0+55 |
| 23 | Dire Wolf (`.../Canines/DireWolf.cs:12`) | **Body.def:6 = 225, hue 2305** | animal | 36x35 | (225) | 2+137 (2) |
| 98 | Hell Hound (`.../Monsters/Mammal/Melee/HellHound.cs:12`) | **Body.def:44 = 225, hue 1643** | animal | 36x35 | (225) | 2+58 |
| 277 | Cu Sidhe (`.../Monsters/ML/Animal/CuSidhe.cs:10`) | Bodyconv.def:328 to anim5.mul 205 | animal | 69x78 | 300 | 0+3 |
| 201 0xC9 | Cat (`.../Town Critters/Cat.cs:12`), Hellcat (`.../Felines/HellCat.cs:12`) | anim.mul 201 | animal | 22x19 | 258 | Cat 2+87 (4), HellCat 1+35 |
| 63 | Cougar (`.../Felines/Cougar.cs:11`) | **Body.def:18 = 214, hue 0** | animal | 50x40 | (214) | 14+406 (14) |
| 214 0xD6 | Panther (`.../Felines/Panther.cs:11`, Hue 0x901 at :12) | anim.mul 214 | animal | 50x40 | 258 | 14+374 (14) |
| 64, 65 | Snow Leopard (`.../Felines/SnowLeopard.cs:12`) | **Body.def:19/:20 = 214, hue 2301 both** | animal | 50x40 | (214) | 0+48 (5) |
| 127 | Predator Hellcat (`.../Felines/PredatorHellCat.cs:12`) | **Body.def:74 = 214, hue 1652** | animal | 50x40 | (214) | 0 |
| 6 | Bird, Tropical Bird (`.../Town Critters/Bird.cs:29`, `:70`) | anim.mul 6 | monster layout | 15x9 | 305 | Bird 60+641 (20), Tropical 0+33 |
| 5 | Eagle (`.../Animals/Birds/Eagle.cs:11`), Phoenix (`.../Birds/Phoenix.cs:11`, Hue 0x674), Enraged Eagle (`.../LBR/Meers/EnragedCreatures.cs:68`) | anim.mul 5 | monster layout | 26x15 | 265 | Eagle 15+350 (15), Phoenix 0+1 |
| 254 | Crane (`.../Animals/Birds/Crane.cs:11`) | Bodyconv.def:207 to anim4.mul 204 | animal | 25x39 | 300 | 0+57 (Tokuno only) |
| 243 | Lesser Hiryu (`.../Mounts/LesserHiryu.cs:13`), Hiryu (`.../Mounts/Hiryu.cs:13`) | Bodyconv.def:204 to anim4.mul 201 | animal | 129x71 | 300 | Lesser 0+9, Hiryu 0+3 (Tokuno) |
| 246 | Bake Kitsune (`.../Monsters/SE/BakeKitsune.cs:16`) | Bodyconv.def:205 to anim4.mul 202 | animal | 87x86 | 300 | 0+10 (Tokuno) |

All `...` paths are under `D:\UO\ModernUO-pinned\Projects\UOContent\Mobiles\`. Each ID and name in the brief matched
the pinned class at the cited line. No ID in the brief was wrong.

**Third-party animations** (all read-only from `D:\UO\third-party\`). Each one is a **low (animal) type**, so it needs
an animal slot: **200 to 399** in an anim*.mul (directly, or by a `Bodyconv.def` line from a new body ID), or a UOP
legacy-frame entry.

Groups use ClassicUO's low-group names: 0 walk, 1 run, 2 stand, 3 eat, 4 alert, 5 and 6 attack, 7 hit, 8 die, 9 and
10 idle, 11 lie down, 12 die 2.

| File | Frames | Groups present (frames) | Stand / largest frame |
|---|---|---|---|
| `kr-wolf\Wolf.vd` | 570 | walk 50, run 50, stand 50, eat 105, alert 15, attack 35+35, hit 40, die 50, idle 55+35, die2 50 (no lie down) | 86x110 / 152x136 |
| `cerberus\Cerberus.vd` | 285 | walk 25, run 25, stand 5, eat 25, attack 25+25, hit 25, die 30, idle 25+15, lie down 30, die2 30 (no alert) | 67x68 / 98x79 |
| `Mobile Pack\L_Fox.vd` | 295 | walk 45, run 30, stand 5, attack 30+30, hit 30, die 45, idle 50+30 (no eat, alert, lie down, die2) | 35x26 / 49x37 |
| `Mobile Pack\L_Bird 01.vd` | 360 | all 13: walk 25, run 25, stand 30, eat 30, alert 30, attack 25+25, hit 25, die 30, idle 25+30, lie down 30, die2 30 | 79x99 / 121x123 |
| `Mobile Pack\L_Bird 02.vd` | 360 | same as L_Bird 01 | 79x99 / 121x123 |
| `Mobile Pack\L_Griffin.vd` | 360 | same counts as L_Bird | 75x90 / 264x168 |

Every file has stand, walk, attack, hit and die, so all six would work as a pet.

**Two notes on these files:**
- KR Wolf's author built it as a mount (`SOURCE.txt`).
- Shipping any of them means getting the art into every player's client, as a patched anim*.mul slot or a UOP
  entry. Today the player package deliberately ships no art.

## Part B.1: duplicates

**Body.def redirects (same art, hue only).** Body.def lines are cited in the Part A table.
- 23, 25, 27, 34, 37 and 98 are 225.
- 63, 64, 65 and 127 are 214.

**Pixel-identical pairs** (same frames and same hue):
- **64 and 65** (both 214 with hue 2301).
- **63 and 214**: Cougar is 214 with hue 0, so the client draws it as the bare panther art. In game they still
  differ, because `Panther.cs:12` sets Hue 0x901 server-side.

**One body shared by two pinned classes:**
- 201 (Cat, Hellcat);
- 5 (Eagle, Phoenix, Enraged Eagle);
- 6 (Bird, Tropical Bird);
- 243 (Hiryu, Lesser Hiryu);
- 246 (Bake Kitsune, Summoned Bake Kitsune).

**Same model among the unused bodies**, found by eye and frame sizes (my shape hashes differ because the pixels
differ):
- **1553 Manticore and 1573 Manticore_L** are the same model, drawn at 86x60 and at 140x98. Use one.
- **1254 Tiger and 1255 "Tiger Ethereal"** are the same rig and the same 78x53 frame, with a darker texture on 1255.
  ServUO's `WildTiger.cs:27` picks one at random, so treat them as one creature.
- **1426 Lion** shares the tiger rig (78x53) with a different texture and a mane. It reads as a different animal.

**Third-party:** **L_Bird 01 and L_Bird 02 are a recolor pair.** All 360 frames have identical pixel positions; only
the palette differs. L_Griffin has the same frame counts but different shapes, so it is its own model.

**Checks that came back clean**
- I compared the stand-frame pixels of the 41 distinct EA bodies with art in this note, pairwise. No other two are identical
  or share a shape.
- The whole-client scan found 13 groups of pixel-identical bodies (`scan_dupes.json`). None of them is a dog, cat,
  fox or bird.
- No `Bodyconv.def` line sends two of the candidates to the same slot.

## Part B.2: unused dog, cat, fox and bird bodies

**Method**
- I resolved every body 1 to 4095 through the renderer: 1,264 have art (318 UOP, 837 MUL, 109 Body.def).
- I rendered all 392 non-equipment, non-human ones as thumbnails (376 after dropping identical ones):
  `scan\page00.png` to `page06.png`. I also checked the equipment and human-typed set (`scan\page_equip.png`, 173
  bodies; all gear, no creatures).
- I identified the bodies by eye, and also grepped the names in `mobtypes.txt` and pinned's `bodyTable.cfg` for fox,
  wolf, dog, hound, jackal, hyena, cat, lion, tiger, leopard, bird, eagle, hawk, owl, raven, crow, parrot, phoenix,
  peacock, crane, chicken, turkey, griffin, manticore and kitsune.
- "Unused" means no pinned class sets that Body. I checked `Body =` and mount `base(...)` arguments in decimal and
  hex across `ModernUO-pinned\Projects`. The only hits on these numbers were hues and stats.
- Our customizations do not use any of them either.
- None has a pinned class, so **every wild-spawn count below is 0** (pinned spawns, and our seeders).
- **Name sources:** the client's `mobtypes.txt` line, and the ServUO class that uses the body where one exists. A
  ServUO class is a possible port source, read-only.

| ID | Name | mobtypes.txt | ServUO class | Art | Stand px | pinned bodyTable.cfg |
|---|---|---|---|---|---|---|
| 1069 | Ancient Hellhound | :1200 | none | UOP 2 | 74x81 | :1110 Animal |
| 1410 | Windrunner (canine) | :1270 | `Mobiles/Normal/Windrunner.cs:55` (mount) | UOP 3 | 102x93 | :590 **Equipment** |
| 1546 | Newfoundland | :1399 | none | UOP 3 | 65x63 | :638 **Equipment** |
| 1547 | Alaskan Malamute | :1400 | none | UOP 3 | 62x62 | **missing** |
| 1548 | Great Dane | :1401 | none | UOP 3 | 62x60 | :639 **Equipment** |
| 1549 | Saint Bernard | :1402 | none | UOP 3 | 66x62 | :640 **Equipment** |
| 1551 | Black Russian Terrier | :1404 | none | UOP 3 | 64x64 | **missing** |
| 1552 | Rottweiler | :1405 | none | UOP 3 | 61x61 | **missing** |
| 1576 | Orc Hellhound | :1429 | none | UOP 6 | 44x47 | **missing** |
| 739 | Leather Wolf | :1034 | `Mobiles/Normal/LeatherWolf.cs:23` | UOP 4 | 48x44 | :980 Monster |
| 719 | Dragon Wolf (upright, scaled) | :1015 | `Mobiles/Normal/DragonWolf.cs:13` | UOP 3 | 49x88 | :961 Monster |
| 1309 | Baby Tiger | :1259 | `Quests/Eodon/Valley of One Quest/Creatures.cs:565` (TigerCub) | UOP 3 | 40x27 | **missing** |
| 1254 | Tiger | :1218 | `Mobiles/Normal/WildTiger.cs:27` | UOP 1 | 78x53 | :1117 Animal |
| 1255 | Tiger, darker texture | :1219 | `WildTiger.cs:27` | UOP 1 | 78x53 | :1120 **Equipment** |
| 1416 | Sabertooth Tiger | :1276 | `Mobiles/Normal/SabertoothedTiger.cs:16` | UOP 3 | 95x68 | :596 **Equipment** |
| 1426 | Lion | :1286 | `Mobiles/Normal/Lion.cs:16` | UOP 3 | 78x53 | **missing** |
| 1441 | Undead (skeletal) Tiger | :1301 | `Mobiles/Normal/SkeletalCat.cs:55` (mount) | UOP 2 | 70x56 | **missing** |
| 1553 | Manticore (winged white lion) | :1406 | none | UOP 6 | 86x60 | **missing** |
| 1573 | Manticore_L (same, large) | :1426 | none | UOP 6 | 140x98 | **missing** |
| **1423** | **Fox_Small** | :1283 | `Mobiles/Normal/BloodFox.cs:13` | UOP 3 | 28x27 | **missing** |
| 282 | Parrot | :954 | `Items/Addons/PetParrot.cs:22` | Bodyconv:331 to anim5 208 | 21x27 | :937 Animal |
| 283 | Crow | :955 | none | Bodyconv:332 to anim5 209 | 24x13 | :242 **Equipment** |
| 832 | Phoenix Bird | :1047 | `Mobiles/Normal/Phoenix.cs:13` and `Time Of Legends/Mobiles/GreaterPhoenix.cs:15` | UOP 4 | 73x55 | :993 Monster |
| 1026 | Uber Turkey | :1161 | `Mobiles/Normal/GiantTurkey.cs:14` | UOP 1 | 113x66 | :1109 Monster |
| 1440 | Peacock (mount) | :1300 | `Mobiles/Normal/Eowmu.cs:55` | UOP 4 | 106x76 | **missing** |

**Remarks on the table**
- **ServUO's Phoenix uses body 832 (0x340). Pinned's Phoenix uses 5 (the eagle) with hue 0x674**
  (`Birds/Phoenix.cs:11-12`). Pinned compares Body against 0x340 and 0x402 in `PlayerBarkeeper.cs:186` and
  `BarkeeperGump.cs:15`, but never assigns them to a creature. ServUO paths are under `D:\UO\ServUO-pub57\Scripts\`.
- **Parrot 282 and Crow 283** have only 4 actions (walk, stand, two idles; 70 frames). They have **no attack, hit or
  die**, which is poor for a fighting pet. **831 Parrot Bird** (pinned's 3D-only `Parrot.cs:11`) is flight frames
  only.
- **Checked and rejected**
  - 278 Squirrel and 279 Ferret: used by pinned, and not foxes (279 is on the fox sheet for scale only).
  - 1070 Werewolf: an upright monster.
  - 793: the skeletal horse.
  - 95 Turkey: `Bodyconv.def:444` points it at anim3.mul slot 95, which is **empty in 7.0.117.0**, so it has no art.
  - 30 Harpy: 2+211 wild; half human.
  - 1542 Rabbit_Doom_Baby, 39 Mongbat and 317 Vampire Bat: not canine, feline or bird.

## Part C: the sheets

Every sheet shows each distinct body once at the same scale (2x), sorted small to large by pixel count. The top row
is stand, the bottom row walk, direction south. Unused and third-party bodies are labeled.

- `notes\cc-P59-scratch\sheet-dog.png`: 16 bodies (14 EA, 2 third-party).
- `notes\cc-P59-scratch\sheet-cat.png`: 10 bodies.
- `notes\cc-P59-scratch\sheet-fox.png`: 4 bodies (Ferret for scale).
- `notes\cc-P59-scratch\sheet-bird.png`: 15 bodies.
- `notes\cc-P59-scratch\partA-candidates-1x.png`: every Part A candidate at true scale, including the recolors with
  their Body.def hue applied (approximate) and the six third-party files.

## Proposed stages

Stages run small to large and plain to grand. I avoided art players meet as a common wild spawn: the 225 wolf family,
the 214 panther family, Bird 6 and Eagle 5. Stand sizes are 1x.

### Dog line, 5 stages

| Stage | Pick | Alternate |
|---|---|---|
| 1 | **217 Dog** (27x26). A town critter (97 entries), but it is the obvious puppy | 225 Timber Wolf (36x35, but the most common wild art in the game) |
| 2 | **739 Leather Wolf** (48x44, unused) | 1576 Orc Hellhound (44x47, unused) |
| 3 | **1547 Alaskan Malamute** (62x62, unused) | any one of 1546, 1548, 1549, 1551, 1552 (all about 62x62) |
| 4 | **277 Cu Sidhe** (69x78, 3 wild entries, Twisted Weald only) | KR Wolf.vd (86x110, needs shipped art) |
| 5 | **1410 Windrunner** (102x93, unused) | 1069 Ancient Hellhound (74x81, unused) or Cerberus.vd |

**What the dog line lacks**
- The six dog breeds are all one size (about 62x62), so only one can be a stage. The others could be cosmetic
  variants of stage 3.
- Nothing is missing for 5 stages from EA art.

### Cat line, 5 stages

| Stage | Pick | Alternate |
|---|---|---|
| 1 | **201 Cat** (22x19). A town critter, and Hellcat shares it | none distinct; 201 is the only small cat |
| 2 | **1309 Baby Tiger** (40x27, unused) | 214 Panther (50x40; its art is in 856 wild entries: Cougar 420, Panther 388, Snow Leopard 48) |
| 3 | **1254 Tiger** (78x53, unused) | 1426 Lion (78x53, unused) |
| 4 | **1416 Sabertooth** (95x68, unused) | 1441 Undead Tiger (70x56, unused) |
| 5 | **1573 Manticore_L** (140x98, unused) | 1553 Manticore (the same model, smaller) |

**What the cat line lacks**
- Its stage 1 has no alternate.
- A clean mid-size domestic or wild cat (about 30 to 40 pixels) that is not the hellcat art.
- Nothing else.

### Fox line, 3 stages

| Stage | Pick | Alternate |
|---|---|---|
| 1 | **1423 Fox_Small** (28x27, unused; ServUO's Blood Fox) | L_Fox.vd (35x26, third-party) |
| 2 | **L_Fox.vd** (35x26, needs shipped art). Barely larger than stage 1, but clearly a different animal (bright orange, longer) | none |
| 3 | **246 Bake Kitsune** (87x86, 10 wild entries, Tokuno only) | none |

**What the fox line lacks:** two pieces of new art.
- **A mid fox, about 50 to 65 pixels.** For example a two- or three-tailed fox between the small foxes and the
  kitsune.
- **A grand top fox above 100 pixels.** For example a nine-tailed or celestial kitsune.

With those two, the line reaches 5. Without them, a third option is 2 stages (1423, then 246), which keeps the line
EA-only.

### Bird line, 5 stages

| Stage | Pick | Alternate |
|---|---|---|
| 1 | **254 Crane** (25x39; 57 wild entries, all in Tokuno; full 13-group set) | 282 Parrot (21x27, unused, but no attack, hit or die animations) |
| 2 | **1440 Peacock** (106x76, unused; built as a mount) | 832 Phoenix Bird (73x55, unused) |
| 3 | **L_Bird 01.vd** (79x99, needs shipped art) | L_Bird 02.vd (the same model, another palette) |
| 4 | **L_Griffin.vd** (75x90, needs shipped art) | 832 Phoenix Bird |
| 5 | **243 Lesser Hiryu** (129x71; 12 wild entries, Tokuno; also pinned's tamable mount) | 1026 Uber Turkey (113x66, unused), a poor fit for "grand" |

**What the bird line lacks**
- A **small-to-mid songbird or raptor with full combat animations, about 30 to 60 pixels**. Every EA bird under 70
  pixels is tiny, missing combat animations, or common in the wild.
- A **grand phoenix above 100 pixels**. 832 is only 73x55.
- Its sizes do not climb cleanly: Peacock, L_Bird and L_Griffin are all about 75 to 106 pixels wide.
- An EA-only bird line is 3 stages: 254, then 1440, then 243.

## 6. Server-side note for any unused body

**What `bodyTable.cfg` controls.** Pinned's `Distribution\Data\bodyTable.cfg` sets each body's `BodyType`
(`Server/Mobiles/Body.cs:42-65`; an unlisted body is `Empty`). `BaseCreature` uses it to:
- pick idle, feed and anger animations (`BaseCreature.cs:1762-1769`, `:2987-3010`, `:4583-4590`);
- decide `CanOpenDoors => !Body.IsAnimal` (`:1053`).

**What that means for the picks:** 1410, 1416, 1546, 1548, 1549, 1255 and 283 are typed Equipment, and 1547, 1551,
1552, 1576, 1309, 1426, 1441, 1553, 1573, 1423 and 1440 are missing. A pet on any of those:
- would get no idle, feed or anger animations;
- **could open doors.**

**The fix** would be a `bodyTable.cfg` entry per body. That is shard data and needs a build-side route; it is not
done here.

**Also unverified:** all the new bodies use the UOP-era action set (walk 22, stand 25). I have not checked how
pinned's `Animate` calls for attack and hit look on them, because that needs a client. **Unverified, needs a client
check.**

## Decisions for Chase

1. **Count recolors as the same creature?** The brief's 25, 27, 34, 37, 23, 98, 63, 64, 65 and 127 are recolors.
   **Recommended: yes, so none of them is a stage.**
2. **Use third-party art at all?** It means shipping custom client art (an animal slot 200 to 399, or a UOP entry)
   to every player, which the package does not do today. **Recommended:** yes for the fox (L_Fox) and the bird line
   (L_Bird 01, L_Griffin) once a delivery route exists. KR Wolf and Cerberus stay as dog alternates only, since the
   EA dogs already fill 5 stages.
3. **Fox line length.** **Recommended: 3 stages now** (1423, L_Fox, 246) and commission or source two new foxes (mid
   about 55 pixels, grand above 100) to reach 5 later. If no third-party art is allowed: 2 stages.
4. **Dog line.** **Recommended:** 217, 739, 1547, 277, 1410. The other dog breeds can be cosmetic variants of
   stage 3 if wanted.
5. **Cat line.** **Recommended:** 201, 1309, 1254, 1416, 1573.
6. **Bird line.** **Recommended:** 254, 1440, L_Bird 01, L_Griffin, 243. **If third-party art is declined:** 3
   stages (254, 1440, 243).
7. **Starter-stage bodies that players see everywhere.** Dog 217 and Cat 201 are town critters (97 and 89 spawner
   entries). **Recommended: accept it for stage 1**, since a puppy and a kitten are meant to look ordinary, and the
   later stages are rare or unused.
8. **Body table entries.** Every chosen unused body needs a correct `bodyTable.cfg` type (Animal) through the shard's
   build route, or the pet can open doors and loses its idle and feed animations. **Recommended: include them in the
   F-35 build task.**

P59 DONE
