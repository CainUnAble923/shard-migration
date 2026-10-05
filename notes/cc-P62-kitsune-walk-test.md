# cc-P62: Kitsune ears and tail, one-direction walk test (builder, test shard only)

2026-10-05. Agent: Claude Code. Brief: `D:\UO\cc-prompts\cc-P62-kitsune-walk-test.md`. Spec: `docs\feature-queue.md` F-35
("Fox capstone, human form" and the art-route lines under it). Scratch: 
otes\cc-P62-scratch\` (scripts, proof images)
and `D:\UO\cc-p62-work\` (package zips, logs, the doctored client-data folder).

Authorities: pinned ModernUO `D:\UO\ModernUO-pinned` at **`d4531cd94b739613155225c234900de9f47d2c88`** (`git rev-parse
HEAD`); paths below under `PIN\` = `D:\UO\ModernUO-pinned\Projects\`. TazUO: the build we ship, `D:\UO\TazUO\client`,
**26.0909.63, ProductVersion `+3212623f63436be1c0f4e3b308b202b29597c026`** (read from `TazUO.exe` today). Its source
at that commit is checked out at `D:\UO\cc-p40-work\tazuo-3212623f` (`git rev-parse HEAD` = `3212623f...`; two
LegionScripting doc files modified there, not by me, irrelevant). Paths below under `TUO\` = that folder's `src\`.
"Ours" = `D:\ShatteredLegacy\`.

Nothing was placed in any world, nothing was deployed or published, nothing was committed. `sl-modernuo:latest` was
`9349dc9c9826` before and after.

> **Headlines**
>
> 1. **Built end to end, all green.** The route: our frames go in a **seventh anim file that is entirely ours**
>    (`app\sl-anim7.bin` and `app\sl-anim7-idx.bin`, 3,059 + 422,100 bytes). TazUO opens it as `anim7.mul`/`anim7.idx`
>    through the `-uofilesoverride` list P26 built, and **one `Bodyconv.def` line** (added to a copy of the player's
>    own file at launch) sends Animation 4783 there. Nothing of EA's ships. Paperdoll and icon are P26-style PNG
>    overrides.
> 2. **IDs, all registered and gated:** Animation **4783** (0x12AF), female paperdoll gump **64783** (male 54783 checked
>    free, not shipped), item/icon art ID **15420** (0x3C3C). Layer **Earrings (0x12)**.
> 3. **The beard layer would have been a trap.** It draws in the right place, but at every world load pinned's
>    `Cleanup` turns any real item on Hair or FacialHair into virtual hair and deletes it: her ears would have become
>    her beard. Earrings draws after Hair in all eight of TazUO's orders and nothing covers it. The cost: she
>    cannot also wear earrings (section A3).
> 4. **Direction 1 is South, facing the viewer down-left; mirrored, it is East, down-right.** Walk with the mouse or
>    arrows down-left, then down-right (section A4).
> 5. **Overlay proof:** decoded from the encoded file with P59's decoder (not mine), all 10 frames have **exactly the
>    input's pixel positions**. Colours differ by **at most 4 of 255** per channel, because the anim format holds 5 bits
>    a channel; no encoding can match 8-bit PNG colours exactly. The brief said "pixel for pixel"; this is the
>    one deviation, and it is the format's (section C1).
> 6. Shard build **872/872** (869 before, 3 new), image `sl-modernuo:cc-p62` = **`b04ed61adb5a`**. Launcher facts 10/10, cliloc facts 10/10, launch-settings 20/20, package gates 1 to
>    6 green. Every new gate and fact was seen red first (section C3).
> 7. **There is no test channel.** `Publish-PlayerPackage.ps1` has one target, which every player's updater reads.
>    The package is built to scratch only. Deploy options for Chase are in "For Chase".

---

## 0. Before starting

- `git --no-optional-locks status` in `D:\ShatteredLegacy`: clean at `8a7e754` ("Shard work, 2026-10-05 13:27"). P61
  is committed (its notes end `P61 DONE`, in `65aa5bc`), and `design\kitsune-ears-tail\` is committed (503 files,
  last in `8a7e754`). Nothing there was mine or anyone else's in flight.
- shard-migration: `docs\feature-queue.md` was modified before I started (not mine). During the task, other files
  changed there too (`docs\bug-list.md`, `docs\fidelity-principle.md`, two P54 notes, 
otes\f12-decisions-2026-10-05.md`);
  none are mine.
- Read F-35 (`docs\feature-queue.md:2786-2821`), 
otes\cc-P26-animated-runestone.md`, 
otes\cc-P59-evo-pet-body-sheet.md`
  and 
otes\cc-P59-scratch\p59anim.py`.
- **My one mistake, repaired:** a .NET `WriteAllText('.gitattributes')` with a relative path resolved against the
  process directory and appended `*.bin binary` to **shard-migration's** `.gitattributes` instead of ShatteredLegacy's.
  The diff was that one line; I restored the file with `git checkout -- .gitattributes` (it was clean before) and
  wrote the right file by absolute path. `git status` shows shard-migration's `.gitattributes` unmodified.

## Part A: the route

### A0. How a worn item reaches the body and the paperdoll (confirmed in TazUO's source)

- **Body:** `TUO\ClassicUO.Client\Game\GameObjects\Views\MobileView.cs:361-441`: for each layer in
  `LayerOrder.UsedLayers[layerDir, i]`, an item with `ItemData.AnimID != 0` is drawn with `graphic = AnimID` (after
  `Equipconv.def`, `:400-412`) in the **wearer's** animation group and frame (`animGroup`, `animIndex`), `isEquip`
  true. `DrawInternal` (`:743-826`) refuses `id >= MaxAnimationCount` (`:768`; 8192, `TUO\ClassicUO.Renderer\Animations\Animation.cs:10`, `:45`).
- **Only Human or Equipment typed bodies draw as equipment:** `Animation.cs:284-289`.
- **Paperdoll:** `TUO\ClassicUO.Client\Game\UI\Controls\PaperDollInteractable.cs:509-563` (`GetAnimID`): offset
  `FEMALE_GUMP_OFFSET` 60000 or `MALE_GUMP_OFFSET` 50000 (`TUO\ClassicUO.Client\Game\Constants.cs:90-91`), after an
  `Equipconv.def` swap and a `tileart.uop` appearance swap; `IsAnimExistsInGump` (`:566-583`) falls back to the other
  sex's gump and refuses anything above `MAX_GUMP_DATA_INDEX_COUNT` 0x10000 (`TUO\ClassicUO.Assets\GumpsLoader.cs:14`).
  So **60000 + N** for her, **50000 + N** for him. Confirmed.

### A1. How to ship a new equipment animation (question 1)

Options checked:

| Option | Verdict | Evidence |
|---|---|---|
| ExternalImages for animations | **does not exist.** TazUO's external images cover gumps and art only | `TUO\ClassicUO.Assets\ExternalImageLoader.cs:14` (`IMAGES_FOLDER`, `"gumps"`, `"art"`), `:275-320` (`Load` reads only those two folders) |
| patched copy of `anim.mul`/`anim.idx` | works, but `anim.mul` is **194,950,053 bytes**; a copy per player and a 195 MB rewrite on every EA patch | sizes from `D:\UO\UltimaOnlineVanilla` |
| UOP `AnimationFrame` entry | needs a `mobtypes.txt` line flagged `UseUopAnimation` for N (the UOP path is taken only then, `AnimationsLoader.cs:306-349`), our own UOP container in the AMOU format, and the client's `AnimationFrame5.uop` slot is free today but EA's to take | |
| **an anim file EA does not have, plus one `Bodyconv.def` line** | **chosen** | below |

Why it works, all at the shipped commit:
- TazUO opens `anim.mul` and `anim2.mul` to **`anim10.mul`** (`_files = new UOFileMul[10]`, `TUO\ClassicUO.Assets\AnimationsLoader.cs:47`)
  **by name through `FileManager.GetUOFilePath`** (`:75-81`, `:83-100`), which consults the `-uofilesoverride` map first
  (`TUO\ClassicUO.Assets\UOFileManager.cs:103-107`; the map loads before anything else, `:144`). A map entry may name
  any path (`TUO\ClassicUO.IO\UOFilesOverrideMap.cs:16-55`), including a file name EA's folder lacks.
- EA's 7.0.114.40 and 7.0.117.0 folders hold `anim.mul` and `anim2` to `anim6` only. **`anim7` is free.**
- `Bodyconv.def` column i sends body N to `_files[i]`, so column 6 is `anim7.mul` (`AnimationsLoader.cs:541-645`).
  Only columns 1 and 2 are gated by expansion flags (`:567-580`); a missing file skips the column (`:629-632`).
  `ProcessBodyConvDef` runs on login (`TUO\ClassicUO.Client\Network\PacketHandlers\EnableLockedFeatures.cs:40`,
  `Animation.cs:435`).
- `GetIndices` (`AnimationsLoader.cs:351-362`) then reads slot S of anim7. **S must be 400 or more**: an anim7 slot
  is typed by `CalculateTypeByGraphic(S, 6)` (`:924-945`; 400 and up is Human), and only Human or Equipment draws as
  equipment (`Animation.cs:284-289`). The people layout puts slot S at index entries `35000 + (S - 400) x 175`
  (`:915`), 35 actions x 5 directions. **S = 400**, so the idx is 35,175 entries (422,100 bytes), all empty but one.
- `Body.def` replacement is skipped for a body whose file index is not 0 (`Animation.cs:252`), so nothing redraws it.
- The frame format is `anim.mul`'s, as P59 documents: `ReadMULAnimationFrames` (`AnimationsLoader.cs:1406-1459`) and
  `ReadSpriteData` (`:1461-1532`). A run pixel lands at image column `x + centerX`, row `y + centerY + height`
  (`:1510-1511`), and `DrawInternal` places the image at the anchor minus `(centerX, height + centerY)`
  (`MobileView.cs:817-826`), so every pixel lands at anchor + its own run (x, y), the same rule as the body's frames.

This is P26's pattern: the shipped files are ours alone; the one EA file touched (`Bodyconv.def`) is copied from the
player's own install at launch, our lines appended, by `Build-UoOverrides.ps1`, and named in the same override list.

### A2. A free Animation number (question 2)

`scripts\find-free-art.py --anim` (new; tests in its docstring). A number N is free only when: 400 <= N <= 5535 (people
layout; `60000 + N` below 0x10000); no line of `mobtypes.txt`, `Body.def`, `Corpse.def`, `Bodyconv.def` names it and
`Equipconv.def` does not use it as body, graphic or new graphic; its people slot in `anim.idx` holds no frames; no
`AnimationFrame*.uop` entry `build/animationlegacyframe/<N>/<00-79>.bin` and no `AnimationSequence.uop` record; no
static's tiledata animId is N; no `tileart.uop` appearance maps to it; the number is in no code (pinned `Projects\`,
`Distribution\`, our `server\`, and the TazUO source we ship), hex or decimal; it is not registered; and **both** gumps
50000 + N and 60000 + N are free (no `gumpartLegacyMUL.uop` entry, not in `gump.def` or `Equipconv.def`, no
`ExternalImages\gumps` PNG we ship, not in code, not registered).

Result: **86 free numbers** on the shard's 7.0.114.40 data and **the same 86** on 7.0.117.0 (list in the command's
output; 2335 to 5375). I took **4783**; 4784 and 4785 are free too, room for more tails later. `--explain-anim
4783` is FREE on both; gumps 64783 and 54783 FREE. Spot checks that the tests bite: 401 fails on mobtypes, Body.def,
Corpse.def, Equipconv.def, anim.mul, code and TazUO; 470 on a tiledata animId and a gumpart entry; 1423 (a UOP-only
body) on `AnimationFrame3.uop`.

The **item art ID** is the next placeholder slot after the runestone block: **15420 (0x3C3C)**, `--explain` FREE
("art placeholder") on both data sets. The art test now also refuses an ID that `tileart.uop` gives appearances to
(they swap a worn item's paperdoll gump, `PaperDollInteractable.cs:546-557`); 0x3C3C has none.

Registered in `player-package\vendor\shattered-legacy-art\registry.csv`, which now has a **`kind` column** (art, anim,
gump; the 44 runestone rows are art): `15420 art`, `4783 anim`, `64783 gump`. 50000 + 4783 is not registered (nothing
ships there), but `--check-registry` re-tests it through the anim row.

### A3. The layer (question 3)

The ears and tail are one item on **Layer.Earrings (0x12)**; one layer does both, so nothing was split.

- **Body draw order:** `TUO\ClassicUO.Client\Game\Data\LayerOrder.cs:7-64`, indexed by the **server** direction
  before mirroring (`MobileView.cs:152`, `byte layerDir = dir`). In all eight orders Earrings comes after Hair (and
  after Beard, Waist, Robe and everything worn on the body), and before OneHanded, Helmet, TwoHanded and (in seven
  orders) Cloak. Walking in direction 1 uses orders 4 (South) and 2 (East), which are identical:
  `... Robe, Neck, Hair, Waist, Beard, Earrings, OneHanded, Cloak, Helmet, TwoHanded` (`LayerOrder.cs:24-28`, `:38-42`).
  So **the ears draw over her hair, and her hair cannot hide the tail**. A hat or cloak drawn later can cover them,
  which looks right.
- **Nothing hides it:** `MobileView.IsCovered` (`:1305` on) has cases for Shoes, Pants, Tunic, Torso, Arms, Helmet and
  Hair, none for Earrings.
- **Paperdoll:** `PaperDollInteractable.cs:20-44`: Earrings after Hair and after Robe and Cloak; ears over the hair.
- **Why not the beard layer**, which is female-free and also after Hair everywhere: pinned `PIN\UOContent\Misc\Cleanup.cs:79-94`
  collects every item on `Layer.Hair` or `Layer.FacialHair` worn by a mobile at world load, and
  `PIN\Server\Mobiles\Mobile.cs:6551-6566` (`ConvertHair`) makes its ItemID the mobile's `FacialHairItemID` and deletes
  it. Her ears would have become her beard at the first restart.
- **Why not** Cloak (drawn first, under the body, in order 3: `LayerOrder.cs:32`), Waist (before Hair in order 3:
  `:33-34`), Helmet, OneHanded, TwoHanded (hats and weapons).
- Server side, pinned has no special handling of Layer.Earrings (only `Earrings.cs:8` and `EarringsOfProtection.cs:32`
  use it). `Item.CanEquip` needs the layer empty (`PIN\Server\Items\Item.cs:2251`). **The cost:** a woman wearing the
  ears cannot also wear earrings. For F-35's kitsune (a pet) that costs nothing; for a player it would.

### A4. Which screen direction animation direction 1 is

- `TUO\ClassicUO.Renderer\Animations\Animation.cs:78-113` (`GetAnimDirection`): server directions 2 and 4 both draw
  animation direction 1, mirrored for 2 (`:82-87`).
- `TUO\ClassicUO.Client\Game\Data\Direction.cs:10-20`: East = 2, South = 4. The client's own arrow-key mapping
  (`:156-168`): **down + left is South (4)**, **down + right is East (2)**, straight down is Down (3).
- So: **walking down-left on screen (South), she faces the viewer three-quarter to the left: direction 1 as drawn.
  Walking down-right (East) draws the same frames mirrored.** The art chat's "in dir1 she faces the viewer" is right;
  P59 called it south too. Mirrored, the tail moves to her other hip, as a mirror image.

## Part B: what was built

### B1. Encoding (`scripts\build-equip-anims.py`, new)

- Inputs: `vendor\shattered-legacy-art\anim-src\4783\a00_d1_f00.png` to `_f09.png`, byte-identical copies of
  `design\kitsune-ears-tail\stage3-final\walk_dir1\walk_dir1_f00-09.png` (SHA-256 compared); `records.json`
  `"equipAnims": [{ "anim": 4783, "slot": 400 }]`.
- Output: `sl-anim7.bin` (3,059 bytes: one block, action 0 (`PeopleAnimationGroup.WalkUnarmed`,
  `AnimationsLoader.cs:1665`), direction 1, 10 frames) and `sl-anim7-idx.bin` (35,175 entries; every one but entry
  35001 is position -1, which TazUO treats as empty, `Animation.cs:312`). Every other action and direction is empty.
- Palette and runs as P59 documents: 256 colours (16 used), run headers length/y/x in 12/10/10 bits, 0x7FFF7FFF end.
- Colour: the 16 PNG colours are 8-bit and none is exactly a 5-bit level, so each becomes the 15-bit colour whose
  expansion through TazUO's table (`TUO\ClassicUO.Utility\HuesHelper.cs:10-20`) is nearest: at most 4 of 255 off.
  No pure black, so the MUL path's "palette 0 is drawn opaque" (`AnimationsLoader.cs:1520-1527`, `alphaCheck` false)
  does not matter. Only alpha 0 and 255 occur in the art (checked).
- `--check` rebuilds in memory, fails unless the committed files are byte-identical, and decodes them back against
  the PNGs.

### B2. Gump and icon, the P26 way

- `vendor\shattered-legacy-art\gumps\64783.png` (= `stage2-final\paperdoll_260x237.png`, byte for byte) ships to
  `app\tazuo\ExternalImages\gumps\`, beside Fiddle-Me-This's 170. TazUO reads an external gump before EA's
  (`TUO\ClassicUO.Renderer\Gumps\Gump.cs:22-36`); the slot array has `max(count, 65535) + 0x4000` entries
  (`TUO\ClassicUO.IO\UOFileUop.cs`, `FillEntries`), so 64783 is inside it.
- `vendor\shattered-legacy-art\art\15420.png` (= `icon_44.png`) ships to `ExternalImages\art\` like the runestone frames.
- `records.json` tiledata record for 15420: flags `0x00400002` (Wearable, and 0x2 = Weapon, which nothing reads), weight 1, layer 18 (0x12),
  animId 4783, height 1, name "fox ears and tail": OSI's earrings 0x1087 have flags 0x400002, weight 1, layer 0x12,
  height 1 (read from the shard's tiledata.mul today; animId 496 there).

### B3. Launcher (`payload\app\Build-UoOverrides.ps1`)

- **Art part:** tiledata records with no animdata of their own (our icon) are now written too, after the same slot
  tests (tiledata free, not another animation's frame).
- **New worn-item part** (`Build-EquipAnim`), run only when the art part produced its copies (the tiledata copy is
  what names 4783): refuses if the player's folder has its own `anim7.mul` or `anim7.idx`; skips, with a yellow line,
  an N that the player's `Bodyconv.def` or `mobtypes.txt` already names (mobtypes would send N to the UOP files);
  writes the player's `Bodyconv.def` byte for byte plus a comment and `4783 -1 -1 -1 -1 -1 400` to
  `app\uo-overrides\Bodyconv.def`; adds `bodyconv.def=`, `anim7.mul=<app>\sl-anim7.bin`, `anim7.idx=<app>\sl-anim7-idx.bin`
  to `files-override.txt`. Stamp `equip-stamp.txt`: the two EA files' size and time, the records' and both anim
  files' SHA-256. Any failure is one yellow line and that part is left out; the art and text parts still ship.
- On the shard's real client data: rebuild 1.7 s and skip 1.0 s, both **including a PowerShell start**. Read back
  independently with Python: **120 bytes changed in tiledata, in exactly 5 records** (the 4 stones and ours, which
  reads `(0x400002, weight 1, layer 18, count 0, anim 4783, hue 0, light 0, height 1, "fox ears and tail")`); the
  Bodyconv copy is the player's file as a prefix plus 150 bytes.

### B4. Server

- `server\customizations\KitsuneEarsTail.cs` (new): `[SerializationGenerator(0, false)]`, `: Item`, `[Constructible]`,
  ItemID 0x3C3C, `Layer = Layer.Earrings`, hue 0, name "fox ears and tail". `OnEquip` refuses a wearer who is not
  Female with cliloc **1010388** "Only females can wear this." (pinned's own message for female-only armour,
  `PIN\UOContent\Items\Armor\BaseArmor.cs:1072-1076`), so the item does not go on (`PIN\Server\Mobiles\Mobile.cs:7800-7820`).
  Staff are not exempt. Staff-spawned only: nothing places it.
- `ApplyTileData` writes the record into `TileData.ItemTable` (`PIN\Server\TileData.cs:46` constructor, `:289` table),
  called from `ShatteredLegacyArt.Apply` in `ShatteredRunestone.cs`, so the server and a patched client agree.
- `server\tests\Items\KitsuneEarsTailVerification.cs` (new, 3 facts): round trip (0x3C3C, Earrings, hue 0, name); a
  woman equips it (on Earrings), a man does not (EquipItem false, still in his pack); the server's tiledata row.

### B5. Package (`Build-PlayerPackage.ps1`)

- The registry's `kind` splits the counts: art rows = PNGs in `art\`, gump rows = PNGs in `gumps\`, anim rows =
  `equipAnims` entries.
- Staging refuses a `gumps\` file the registry does not list, a count mismatch, and a gump named like a
  Fiddle-Me-This one; copies the gumps and the two anim files (byte-checked in gate 3).
- **Equipment-animation gate** (`Test-EquipAnims`), run on vendor\ before staging and on the zip in gate 4: every
  `equipAnims` anim is registered and every registered anim has one entry; slots 400 and up; idx whole entries; every
  non-empty idx entry is in a named slot and inside `sl-anim7.bin`; idx long enough for each slot.
- Gate 4: gumps PNG count 170 + registered gumps; each registered gump present; anim files present iff `equipAnims`.
- Gate 4's "nothing of EA's" still holds: our files are `.bin`, not `.mul`/`.idx`, and EA has no file by those names.
  The player's own `Bodyconv.def` copy lives in `app\uo-overrides\`, which never ships.
- `.gitattributes`: `*.bin binary` (the two files would have been detected as binary anyway by their NUL bytes; now
  it is said).
- Built to scratch: `D:\UO\cc-p62-work\pkg\ShatteredLegacy-2026.10.05.1356.zip`, 76 MB, 740 client files (983 zip
  entries), gates 1 to 6 green; `-CheckZip` gates 4, 5, 6 green. It holds `app/sl-anim7.bin` (3,059),
  `app/sl-anim7-idx.bin` (422,100), `ExternalImages/art/15420.png`, `ExternalImages/gumps/64783.png`.
  **Final build, from the final files:** `D:\UO\cc-p62-work\pkg\ShatteredLegacy-2026.10.05.1419.zip`, 76 MB, gates 1 to 6
  green; `-CheckZip` gates 4, 5, 6 green. It records "uncommitted player-package changes": a test build, not for publishing.

No `CHANGELOG.md` line and no `VERSION` bump, per the brief.

## Part C: checks

### C1. Overlay proof (
otes\cc-P62-scratch\overlay_proof.py`)

Reads `sl-anim7-idx.bin` entry 35001 (slot 400, action 0, direction 1) the client's way, decodes the block with
**P59's `decode_runs`** (written for EA's anim.mul, independent of my encoder), and compares with the PNGs:

```
idx entry 35001 -> 3059 bytes at 0; 10 frames; 1 non-empty index entries in all
f00: 124 px, positions identical, largest colour difference 4
...  (every frame the same)
f09: 148 px, positions identical, largest colour difference 4
frames with different positions: 0; largest colour difference over all: 4
```

Strips (body 401's walk direction 1 from the client's anim.mul, our decoded frames on top, 3x):

otes\cc-P62-scratch\overlay-proof-3x.png` and the mirrored one `overlay-proof-mirrored-3x.png`. Before encoding, the
same composite from the input PNGs (`input-overlay-3x.png`, `input-overlay-zoom.png`, `overlay_check.py`) confirmed
the brief's alignment: the ears sit on the crown and the tail on the hip in every frame, at (x - 67, y - 98).

**Deviation:** "pixel for pixel" holds for positions, not colours: 5 bits a channel is the format's limit (the body
itself is drawn that way). Largest difference 4 of 255.

### C2. Collision gate (`find-free-art.py --check-registry`, extended)

Re-tests every registered row in its own space (art, anim with both gumps, gump), plus: each anim has one of its
gumps registered, each gump belongs to a registered anim. A hit in our own `server\` code is the ID's expected use;
pinned and TazUO hits never are. Green: **0 of 47** no longer free, on both the shard's data and 7.0.117.0.

**Seen failing first** (`D:\UO\cc-p62-work\red-data\`: hard links to the shard's client data, with doctored copies of
`tiledata.mul` and `Bodyconv.def`, 
otes\cc-P62-scratch\red_registry.py`; plus a planted
`fiddle-me-this\[Custom]\ExternalImages\gumps\64783.png`):

```
art 15420 ...: tiledata: flags 0x2
anim 4783 ...: defs: named in Bodyconv.def:975; tiledata: animId of 0x1087; female gump 64783: overrides: ...\64783.png
gump 64783 ...: overrides: ...\fiddle-me-this\[Custom]\ExternalImages\gumps\64783.png
3 of 47 registered IDs are no longer free        (exit 1)
```

Plant removed (`git status` clean for `vendor\fiddle-me-this`), then **0 of 47, exit 0**.

### C3. Every other new gate, red then green

| Run | Break | Result |
|---|---|---|
| gate 4, `-CheckZip` on doctored copies of the real zip (`red_zip.py`) | r1 gump PNG removed; r2 equipAnims names 4784; r3 idx block in entry 100; r4 `sl-anim7.bin` removed; r5 idx block past the file's end; r6 equipAnims removed, files kept | **all 6 red**, each with its own line ("170 PNGs ... expected 170 + 1", "no ...64783.png", "equipAnims 4784, which registry.csv does not list", "entry 100 holds a block outside the slots", "...is missing", "entry 35005 points outside", "shipped with no equipAnims") |
| staging | an unregistered `gumps\64784.png` | "vendor\shattered-legacy-art\gumps holds files registry.csv does not list: 64784.png. Not building." |
| `build-equip-anims.py --check` | one byte of `sl-anim7.bin` flipped | red (file differs; frame 0 pixel decodes wrong); restored, SHA-256 equal, green |
| launcher facts (`mutate_player.py`, in place, restored, SHA-256 checked) | p1 Bodyconv skip off; p2 line break not added; p3 anim7 not checked; p4 icon record not written; p5 C# Animation 4784 | **each red in exactly its fact** (9/10), restored (`53ec0b31e398`, `5db1ff0030d1`) |
| server facts (`mutate_server.py`, `build.sh --tests-only`, restored, SHA-256 `3611b936f61e`) | s1 female check off, s2 layer Helm, s3 server record Animation 4784 | **all 3 new facts red, 869 passed** ("Expected: Earrings / Actual: Helm", "Expected: 4783 / Actual: 4784"). s2 masked s1 in fact 2, so **s1 alone**: only "a man does not" red ("Expected: False / Actual: True"), 871 passed. Two earlier attempts did not compile (pinned's enum says `Helm`, not `Helmet`) and are not counted |
| launcher cross-check, by value | p6: C# flags Wearable or Background | red ("expected [4194306] but got [4194305]"), restored |

### C4. Tests and build

- Launcher (`player-package\tests\Build-UoOverrides.Tests.ps1`): **10/10** (8 before; 2 new; facts 1 and 6 updated for
  the new record: 120 changed bytes, 47 registry rows, the C# copy of the kitsune record). The two sandbox facts ran
  `Play.ps1` against the test shard's port.
- `Cliloc-Overrides.Tests.ps1` **10/10**: one fact needed the builder pointed at the vendor anim files and a
  `Bodyconv.def` in its synthetic folder (it asserts exactly one yellow line, and the folder had none).
- `Launch-Settings.Tests.ps1` **20/20**.
- **Found while testing, fixed:** with tiledata missing, the worn-item part still listed its overrides, which mean
  nothing without the tiledata record that names 4783. It now runs only when the art part did (old facts 5 and 8
  caught it).
- Shard: `build.sh -t sl-modernuo:cc-p62` **872 passed, 0 failed**, image `b04ed61adb5a`. `sl-modernuo:latest` not moved (`9349dc9c9826`).
- **The first full build was red, for a real reason:** server fact 3 found the C# record flagged Wearable | **Background**
  (0x400001) while records.json says 0x400002. Bit 0x2 is **Weapon** (pinned `Server/TileData.cs:219-220`; TazUO's
  `TAEFlag` agrees). I had misread OSI's earrings flags. Fixed to `Wearable | Weapon`, OSI's exact value, which
  neither side reads (pinned never uses `TileFlag.Weapon`; TazUO's only `IsWeapon` use, `MobileView.cs:414`, is
  commented out). The launcher cross-check passed through the mistake because it compared my flag *names* with my
  own wrong label; it now compares values (p6 above).

## Deviations and decisions for Chase

1. **Colours are 15-bit in game** (C1). Up to 4/255 per channel off the PNGs; positions exact. The format's limit.
2. **Earrings layer**: a woman wearing the ears cannot wear earrings. Fine for the kitsune pet; worth knowing if
   players ever get the item. The beard layer is not an option (A3).
3. **No test channel exists** for the package (`D:\UO\haven-migration\Publish-PlayerPackage.ps1` has one target).
   Publishing this package reaches every player. That is harmless (only `[add KitsuneEarsTail` makes anything use the
   art, and no live server has the item), but it is a publish. The alternative is to test from an unzipped copy of
   the scratch build (For Chase, option A).
4. **Staff are not exempt** from the female-only rule (pinned's armour exempts GameMasters in one path,
   `BaseArmor.cs:917`; the brief said a male wearer does not equip it).
5. **One tiny TazUO quirk, not ours to fix, unverified in a client:** a body reached through `Bodyconv.def` has
   `BodyConvInfo.Hue = INVALID_HUE` (0xFF, `AnimationsLoader.cs:1785-1787`), which `GetIndices` hands back
   (`:353`) on the first lazy load only. The very first draw of an unhued item on such a body may be hued 0xFF for
   one frame. It applies to every EA creature in anim2 to anim6 too. If Chase sees a one-frame flash, that is it.
6. **Mirroring is the client's.** Walking East shows direction 1 flipped, tail on the other hip. Directions 0, 2, 3, 4
   and East's true art come with the remaining 95 frames.
7. **Registry format changed**: `registry.csv` has a `kind` column. Anything else that reads it must filter on
   `kind = art` for art IDs (the package build and the scanner do).
8. **Hands empty, not in war mode:** the frames are action 0 (walk unarmed). Holding a weapon or in war mode, the body
   walks in action 1 or 15 and the ears and tail draw nothing.

## Files (`D:\ShatteredLegacy`)

```
.gitattributes                                              *.bin binary
scripts/find-free-art.py                                    --anim, --explain-anim, --explain-gump; tileart test; kinds in --check-registry
scripts/build-equip-anims.py                                NEW  PNG frames -> sl-anim7.bin / -idx.bin; --check
player-package/Build-PlayerPackage.ps1                      registry kinds; our gumps and anim files; equipment-animation gate; gate 4
player-package/payload/app/Build-UoOverrides.ps1            icon tiledata record; Build-EquipAnim (Bodyconv.def copy, anim7 overrides)
player-package/tests/Build-UoOverrides.Tests.ps1            2 new facts; facts 1, 6 and the Play sandbox updated
player-package/tests/Cliloc-Overrides.Tests.ps1             builder given the anim files; a Bodyconv.def in one fixture
player-package/vendor/shattered-legacy-art/registry.csv     kind column; 15420 art, 4783 anim, 64783 gump
player-package/vendor/shattered-legacy-art/records.json     icon tiledata record; equipAnims
player-package/vendor/shattered-legacy-art/SOURCE.txt       the new files and the fox ears and tail
player-package/vendor/shattered-legacy-art/art/15420.png    NEW  icon
player-package/vendor/shattered-legacy-art/gumps/64783.png  NEW  female paperdoll gump
player-package/vendor/shattered-legacy-art/anim-src/4783/   NEW  10 walk frames (source)
player-package/vendor/shattered-legacy-art/sl-anim7.bin     NEW  encoded frames
player-package/vendor/shattered-legacy-art/sl-anim7-idx.bin NEW  its index
server/customizations/KitsuneEarsTail.cs                    NEW  the item and its server tiledata record
server/customizations/ShatteredRunestone.cs                 ShatteredLegacyArt.Apply also writes the kitsune record
server/tests/Items/KitsuneEarsTailVerification.cs           NEW  3 facts
```

All text files ASCII and LF (checked by script). `design\` untouched; nothing written into the EA folders or
`D:\UO\third-party\`.

## For Chase

Package first, then the server, then the client check.

1. Commit (`D:\UO\Commit-ShardWork.ps1`).
2. Build the package from the commit: `D:\ShatteredLegacy\player-package\Build-PlayerPackage.ps1` (gates 1 to 6 must
   pass), then `-CheckZip <the new zip>`.
3. Get it onto your PC, one of:
   - **A (nothing published):** unzip the new zip to a scratch folder and run its `Play TEST Shard.bat`. It sets up
     its own `app\uo-overrides\` from your EA install. Your published install is untouched.
   - **B (publish):** `D:\UO\haven-migration\Publish-PlayerPackage.ps1`, then `Play TEST Shard.bat` from your install
     and accept the update. This reaches every player (harmless; see decision 3).
4. Put `sl-modernuo:cc-p62` (`b04ed61adb5a`, 872 tests green) on the test shard your usual way. Not live.

In-game checklist (test shard):

- [ ] Log in a **female** character. `[add KitsuneEarsTail`, equip it (drag onto the paperdoll). Empty hands, out of
      war mode.
- [ ] Paperdoll: ears on her head above the hair, tail behind the hip.
- [ ] Walk **down-left on screen** (mouse or arrows down + left: South, animation direction 1 as drawn): ears and tail
      move with her, frame for frame.
- [ ] Walk **down-right on screen** (down + right: East, the same frames mirrored, `Animation.cs:82-85`): they move with
      her, tail on her other hip.
- [ ] Other directions, standing and running show nothing yet; that is expected.
- [ ] Stand next to another character at normal zoom: does it read as fox ears and a tail?
- [ ] A male character: equipping it says "Only females can wear this." and it does not go on.
- [ ] Restart the test shard and look again: still worn (the layer survives world load; A3).

P62 DONE
