# cc-P81: Siege of Sosaria paperdoll art in the Shattered Legacy client

Run 2026-10-13 by Claude Code (autopilot hand-off after P80). Builder (client art and package). Test shard only.
Nothing deployed, committed or uploaded; no server image needed beyond a tests-only build (`sl-modernuo:cc-p81`, 1116
tests passing, for the changelog); `latest` unchanged.

**Sources:**
- The kit: `D:\ShatteredLegacy\design\paperdoll-sos\kit\UO Paperdoll Project (Siege of Sosaria) Builder's Kit\`
  (v3.1, Zigholtul). Terms: none stated; credit him (`D:\UO\third-party\paperdoll-siege-of-sosaria\SOURCE.txt`).
- Our TazUO: source `D:\UO\cc-p40-work\tazuo-3212623f` (commit 3212623f, v26.0909.63). The package ships TazUO's
  **release build** (`D:\UO\TazUO\client`); we do not build TazUO from source.

**I could not play the client.** Everything below is from files and offline renders; the in-game checks are under
"For Chase".

## Report summary

| Item | Result |
|---|---|
| Route | TazUO's gump override folder, `app\tazuo\ExternalImages\gumps\<id>.png`: the route Fiddle-Me-This and our own gump 64783 already use. No UOP or MUL patching |
| Gump IDs installed | **1,575** SFW PNGs: 1,372 default gumps, 121 spell icons, 68 DLC, 14 DLC templates (grayscale) |
| Collisions | **0** with our own gumps (64783). **27** with Fiddle-Me-This: 62000-62026, kept as FMT's (below). 9001, the kit's login splash, left out |
| JSON | not adopted: our TazUO never reads it, and the kit's button positions overrun FMT's paperdoll frame (diff below) |
| Faces | no paperdoll gump exists for the stock face items in our client data; nothing draws, before or after (below) |
| Out of scope found | 18 animation VDs, the kit's Equipconv.def (238 differing lines), the MUL files (below) |
| Package | built: `player-package\dist\ShatteredLegacy-2026.10.13.0118.zip`, **83 MB** (was 80.2 MB), all gates passed; not uploaded |
| Server version | `VERSION` 2026.10.13.4, patch note in `CHANGELOG.md` |
| NSFW | kept out of the package by a build gate (proved red twice); a local-only switch in our launcher for Chase's machine |

## 1. The delivery route

TazUO's `ExternalImageLoader.Load` (`ClassicUO.Assets/ExternalImageLoader.cs:275-320`) works like this:
- it reads every `*.png` and `*.bmp` under `<TazUO>\ExternalImages\gumps\`, **subfolders included**;
- each file is keyed by its decimal or `0x` hex name (`TryParseId`, :428-433);
- `LoadGumpTexture` serves that PNG in place of the gump from the client's files.

Our package already ships this way:
- **Fiddle-Me-This**'s 170 gumps (`player-package\vendor\fiddle-me-this\`);
- **our own gump 64783** (`vendor\shattered-legacy-art\gumps\`);
- both copied into `app\tazuo\ExternalImages\gumps\` by `Build-PlayerPackage.ps1`.

**Chosen:** the same route. A new vendor folder, `player-package\vendor\paperdoll-sos\`:
- `ExternalImages\gumps\<id>.png`: the 1,575 SFW PNGs;
- `bodies-sfw\<id>.png`: the six SFW bodies, also shipped as `app\paperdoll-sfw\` for the launcher;
- `nsfw-sha256.txt`: 57 hashes, no art;
- `SOURCE.txt`.

**Made only by `design\paperdoll-sos\tools\select.py`** from the kit, never by hand. EA's files and the kit's MUL and
UOP files are never shipped.

## 2. Collision check (`design\paperdoll-sos\tools\ids.py`)

**The kit's PNGs:**

| Folder | IDs | Notes |
|---|---|---|
| `#01 Default Gumps` | 1,372 | includes the six body gumps, **byte-identical** to the SFW swaps |
| `#02 Player Mobile Swaps\#01 Default Versions` | 6 | 12, 13, 14, 15, 665, 666 |
| `#03 Spell Icon Upgrades` | 121 | |
| `DLC` | 110 IDs in 174 files | 96 at the top level; `Paperdoll Templates` in Default, Topless and Nude variants, each Grayscale and Hued |

**Against what we ship:**
- **Our own gumps:** none overlap (we have one, 64783).
- **Fiddle-Me-This:** 27 overlap, **62000 to 62026**, all in FMT's `[Custom]` set.
  - FMT uses those numbers for its own UI art (62000 is a 250x482 panel its XML gumps draw); the kit uses them for
    female wearable items (62000 is a small female headband).
  - **Kept FMT's.** The kit's 62000-62026 are left out, so FMT's XML gumps keep working. The kit's 62027 (no FMT
    file) ships.
  - The female versions of those 27 wearables then show FMT's panel art if worn. These are DLC items (52000-52027
    male, 62000-62027 female) whose item art is not in stock; check whether any item we ship uses animation numbers
    2000-2026 (decision 2).
- **9001** (0x2329, TazUO's login screen picture, `LoginGump.cs:53`): the kit's own splash. Left out, so ours stays.
- **The DLC templates:** the Default Grayscale set (14) ships; the pre-hued copies, which duplicate those IDs, do not.
  - Seven of them (55528-55534, the male templates) are **byte-identical** to the "topless" versions: a man in a
    loincloth, the same as the SFW body.
  - The NSFW hash list leaves out any hash an SFW file shares.

**Against EA's own paperdoll gumps** (read from this machine's `gumpartLegacyMUL.uop`; 5,524 gumps, 1,274 of them
50000 and up):
- **The kit redraws 1,191** of the 1,274.
- **It adds 256 IDs EA's files do not have.** These are DLC items such as 52000-52027 and the templates; inert unless
  an item uses them.
- **83 stock paperdoll gumps keep EA's look** next to the new art (style mismatch, listed for Chase):
  50432, 50475, 50585-50603 (odd), 50609, 50663, 50704-50706, 50713-50715, 50718, 50804-50808, 51056, 51058, 51060,
  51573, 51640, 51647-51650, 59972-59986 (even), 59988-59999, 60679-60683, 60704-60706, 60709, 60711, 60713-60715,
  61059, 61061, 61415, 61647-61650, 69971-69985 (odd).

## 3. Installed

**1,575 gump PNGs**, 6.3 MB, the largest 92 KB, as `app\tazuo\ExternalImages\gumps\<id>.png`:

| Source | Count |
|---|---|
| default gumps | 1,372 |
| spell icons | 121 |
| DLC top level, less 9001 and 62000-62026 | 68 |
| DLC templates, Default Grayscale | 14 |

Plus the six SFW bodies as `app\paperdoll-sfw\`. The built zip holds 1,746 gump PNGs: 170 FMT + 1 ours + 1,575 kit.

## 4. The paperdoll layout JSON (`design\paperdoll-sos\tools\json_diff.py`)

**Our TazUO never reads a `PaperDollGump.json`.** Its layout is the static class `PaperDollGump.Settings`
(`ClassicUO.Client/Game/UI/Gumps/PaperdollGump.cs:1025` on), with built-in values and no loader anywhere in the source
(searched). The kit's file matches that class key for key (86 keys, presumably for a TazUO build that loads it).

**The diff:** 70 values the same, 16 different, no key on either side only.

| Key | TazUO | Kit |
|---|---|---|
| `Position_X_` Options, Logout, Journal, Quest, Skills, Guild, WarMode, Status | 185 | 197 |
| `Position_X_Durability` | 12 | 0 |
| `Position_Y_Durability` | 33 | 40 |
| `Position_Y_LeftSlots` | 67 | 75 |
| `Position_X_RightSlots` | 166 | 178 |
| `Position_Y_RightSlots` | 67 | 75 |
| `Position_X_CombatBook` | 150 | 178 |
| `Position_Y_CombatBook` | 198 | 200 |
| `Position_X_MinimizeButton` | 228 | 240 |

**Not adopted.**
- **The kit does not redraw the paperdoll background (2000, 2001) or its buttons.** In our package those are
  Fiddle-Me-This's.
- **Rendered on FMT's background:**
  - TazUO's positions sit centered in the button column (`test\background-tazuo-positions.png`);
  - the kit's x 197 runs the buttons to the frame's edge (`test\background-kit-positions.png`).
- **The kit's art does not need it to line up:** item and body gumps are drawn at the doll's origin, which these
  values do not move.

## 5. Faces

- **Our client data has no paperdoll gump for the stock face items.** Face items 0x3B44 to 0x3B57 and 0x5679 to 0x567E
  have tiledata animation numbers 1000 to 1025, but gumps 51000-51025 and 61000-61025 do not exist in our
  `gumpartLegacyMUL.uop` (checked by hash).
- **So a face draws nothing on the paperdoll,** before and after this change (`test\*.png`, the "stock face item"
  column).
- **One possibility not checked:** TazUO can map an item through `tileart.uop` appearances (`PaperDollInteractable.cs`,
  `GetAnimID`, `TryGetAppearance`). Whether it finds a face gump that way was not verified offline (**unverified**;
  the in-game check below).
- **No style mismatch is possible** while nothing draws. Face handling is unchanged, as the brief says.

## 6. The package

| Change | Where |
|---|---|
| Copies the paperdoll PNGs beside FMT's and ours, and the six SFW bodies to `app\paperdoll-sfw\` | `Build-PlayerPackage.ps1`, staging |
| Refuses a non-ID file name, a clash with FMT or ours, and a bodies folder that is not exactly the six | staging |
| Gate 4 expects 170 + 1 + 1,575 gump PNGs and the six SFW bodies | zip gate |
| **THE NSFW GATE** | staging and zip gate (next section) |
| Players install nothing by hand: the art arrives with the next package update | |

- **Package build:** `ShatteredLegacy-2026.10.13.0118.zip`, 83 MB, gates 1 to 6 passed, and `-CheckZip` on it passes.
- **Server `VERSION`:** 2026.10.13.4. The patch note says new paperdoll art and credits Zigholtul. It says nothing
  about the local switch.
- **Not uploaded:** publishing the zip is Chase's.

**The 83 MB.** Every update downloads the whole zip (cc-P76). The paperdoll adds about 3 MB compressed.

## 7. NSFW: the gate, and the local-only switch

**Git.**
- `.gitignore` gains `design/paperdoll-sos/kit/` and `client-addons/` (beside the overseer's `.git\info\exclude`
  lines).
- Proved with `git check-ignore -v`:
  - `.gitignore:84 design/paperdoll-sos/kit/` (a Nude body path);
  - `.gitignore:85 client-addons/` (`client-addons/paperdoll-nsfw/nude/12.png`).
- **Tracked from `design\paperdoll-sos\` is only `tools\` (24 KB) and `test\` (536 KB of renders).**

**The gate** (`Build-PlayerPackage.ps1`):
- **What it reads:** `vendor\paperdoll-sos\nsfw-sha256.txt` (every Topless and Nude file in the kit, both body sets
  and both template sets, minus any hash an SFW file shares: 57 hashes), plus, on a machine that has it, every file
  under `client-addons\` (minus SFW hashes).
- **Before staging,** any vendored paperdoll file with one of those hashes stops the build.
- **In the finished zip,** every file is hashed and any match fails gate 4. So does any path naming topless, nude,
  client-addons or paperdoll-nsfw.
- **Proved red twice:**
  1. a Topless 12.png planted in `vendor\paperdoll-sos\ExternalImages\gumps\`: the build stopped ("NSFW GATE:
     vendor\paperdoll-sos holds Topless or Nude art ... Not building.");
  2. a copy of the built zip with its 665.png swapped for the Nude one: `-CheckZip` failed ("NSFW GATE:
     app/tazuo/ExternalImages/gumps/665.png is a Topless or Nude file from the paperdoll kit").
- **Both restored.** The real zip passes `-CheckZip`.

**The local switch.**
- **Where Chase's copy is:** the kit's two folders' six bodies each, in
  `D:\ShatteredLegacy\client-addons\paperdoll-nsfw\topless\` and `...\nude\` (git ignored, never packaged).
- **Where the switch lives: our launcher, not TazUO's code.** The brief asked for a setting "in our TazUO build", but
  we ship TazUO's upstream release binaries and do not build it. A launcher setting is the client-side equivalent
  that needs no client fork (decision 1).
  - `app\Paperdoll-Bodies.ps1` (new, dot-sourced by `Play.ps1`).
  - `<install>\paperdoll-bodies.txt` (outside `app\`, so updates never touch it): `mode=sfw|topless|nude` and an
    optional `folder=`. The add-on folder is `<install>\client-addons\paperdoll-nsfw\` unless named.
  - Set by `Play.ps1 -PaperdollBodies sfw|topless|nude [-PaperdollFolder <path>]`, for example
    `Play TEST Shard.bat -PaperdollBodies topless -PaperdollFolder D:\ShatteredLegacy\client-addons\paperdoll-nsfw`.
- **Before every start,** `Sync-PaperdollBodies` copies the chosen set over the six body PNGs in
  `app\tazuo\ExternalImages\gumps\`, when that set's folder holds all six. Otherwise it copies the shipped SFW six back
  from `app\paperdoll-sfw\`.
- **What it guarantees:**
  - **A fresh install** has no setting and no add-on: always SFW.
  - **Without the add-on** the switch refuses ("No local paperdoll add-on ... stays SFW") and changes nothing. It is
    not mentioned in the player README; that is the "hidden" option.
  - **Back to SFW** is restored at the next start, no reinstall.
  - **Purely client-side:** no server flag, no packet; others see nothing different.
  - **An update** puts the SFW six back in `app\`, and the next start re-applies the local choice.
- **Why it swaps files in place:** TazUO scans the gump folder's subfolders too, so a second copy of 12.png in an
  "overlay" subfolder would win or lose at random.
- **One local caveat:** `Update.ps1` backs up `app\` before an update, so on Chase's machine that local backup can
  hold the swapped bodies. It never leaves the machine.
- **Tests:** `player-package\tests\Paperdoll-Bodies.Tests.ps1`, 5 facts, all pass:
  - a fresh install stays SFW;
  - no add-on, no switch;
  - the add-on swaps in, and sfw restores;
  - a removed add-on falls back with a line;
  - a named folder elsewhere works.
  - **Red:** a sync that ignores the choice failed fact 3; restored.

## 8. Renders (`D:\ShatteredLegacy\design\paperdoll-sos\test\`)

Made by `tools\render.py`:
- **Layering as the shipped client sees it:** the kit's PNG, else Fiddle-Me-This's, else EA's own gump from this
  machine's `gumpartLegacyMUL.uop`.
- **Decoding EA's gumps** needed TazUO's BWT step for compression flag 3; it is ported from `BwtDecompress.cs`,
  BSD 2-Clause.
- **Items** are layered in ClassicUO's paperdoll order, with no hues.

**The files:**
- `human-male.png`, `human-female.png`, `elf-male.png`, `elf-female.png`: naked; robe, wide-brim hat and cloak; full
  plate and heater shield; a stock face item (draws nothing).
- `gargoyle-male.png`, `gargoyle-female.png`: naked; gargish robe; a stock face item.
- `background-tazuo-positions.png`, `background-kit-positions.png`: the layout comparison (section 4).
- `spell-icons-kit-top-stock-bottom.png`: the first 16 upgraded icons (2240-2255), kit above stock.
- `render-report.txt`: which source each layer came from. Every body and test item came from the kit; the background
  from FMT.

**Our custom items:**
- Our art (`ExternalImages\art\`) and our gump 64783 are untouched: no ID overlap.
- The satchels are container art, not paperdoll gumps.
- The kitsune ears and tail are worn-item animations (anim7), outside the gump IDs the kit covers.

## 9. Out of scope (found, not applied)

- **Animation VDs: 18 files, not 19** (the brief said 19). New worn animations:

  | File | Item |
  |---|---|
  | anim3_913 | Cape with Hood |
  | anim3_914 | Black Heater Shield |
  | anim3_915 | Hood |
  | anim3_916 | Infantry Shield |
  | anim3_917 | Elven Shield |
  | anim3_918 | Wooden Kitten Shield |
  | anim3_919 | Paladin Shield |
  | anim3_920 | Jewel Shield |
  | anim4_637 to 646 | Drums, Lute, Harp, Flower, Bottle, Mug, Angel Wings, Puff-Sleeved Blouse, Umbrella, Shovel (equips) |

  They would add animation slots, through our anim7 route or a new one, plus tiledata for the matching items.
- **The kit's Equipconv.def** (`PNGs\Equipconv.def`) against ours: 238 differing lines.
  - It **drops** the PUB39 male-to-female conversions for the Helm of Swiftness and the Dragon pieces (human and elf
    females), and five "3D client only" elf lines.
  - It **adds** a long block of new conversions, starting with fishing poles for every body. It would change which
    gump each item shows per body.
- **"Dragon Desktop" interface:** not found by that name anywhere in the extracted kit. The only "Dragon" pieces are
  item gumps (Dragon arms, chest, gloves, helm, legs; Dragon Turtle pieces), already among the PNGs. If it means the
  kit's full gumpart MUL, that is never shipped.
- **MUL Files** (Gumpart.mul, Gumpidx.mul, gumpartLegacyMUL.uop): modified EA data, never shipped (hard rule 2).
- **BMPs and Gimp Files:** source art; the PNGs are what ships.

## For Chase (in-game, test shard, after installing the 2026.10.13.0118 package locally)

1. **Paperdolls:** human male and female, elf male and female, gargoyle male and female. For each, naked and in a robe,
   plate set, cloak, hat and shield. Compare with `test\*.png`, and check skin hues tint the new bodies naturally.
2. **A stock face item** (0x3B44 and up) on each race: nothing should draw, as before. If something draws, tell me
   whether it sits right on the new bodies.
3. **Spell icons** in a spellbook (Magery, Necromancy, Chivalry, Bushido, Ninjitsu, Mysticism).
4. **Our custom items:** the kitsune ears and tail, satchels, and anything with our art still look right. The paperdoll
   buttons and frame are FMT's, as before.
5. **Wearables using the 83 gumps the kit does not redraw** (section 2) show EA's style next to the new art. Say
   whether any of those matter.
6. **The local switch, on your machine only:**
   `Play TEST Shard.bat -PaperdollBodies topless -PaperdollFolder D:\ShatteredLegacy\client-addons\paperdoll-nsfw`,
   then `-PaperdollBodies sfw` to return. A restart applies each.

## Decisions for Chase

1. **The local NSFW switch is in our launcher (`Play.ps1` and `Paperdoll-Bodies.ps1`), not in TazUO's code,** because we
   ship TazUO's release build. OK, or should we fork and build TazUO to put it in its options?
2. **62000-62026:** kept as Fiddle-Me-This's, so the kit's female versions of those 27 DLC wearables are not shipped.
   Fine while no item we ship uses animation numbers 2000-2026; renumber if one ever does.
3. **The JSON layout:** not adopted (our TazUO cannot load it, and it misaligns on FMT's frame).
4. **The DLC templates:** the grayscale (hueable) set shipped, not the pre-hued one.
5. **Optional later:** the 18 animation VDs and the kit's Equipconv.def changes, as their own prompt.

## Commit preflight

`Commit-ShardWork.ps1 -DryRun`, run 2026-10-13 before DONE:

```
Repo Result
---- ------
code dry run
docs dry run
```

- **Code, about 1,600 files:**
  - `.gitignore`, `CHANGELOG.md`, `VERSION`, `Build-PlayerPackage.ps1`, `Play.ps1`, `Paperdoll-Bodies.ps1`, the new
    test;
  - `design/paperdoll-sos/tools/` and `test/`;
  - the vendored 1,575 + 6 PNGs, `nsfw-sha256.txt` and `SOURCE.txt`.
- **Never in it:** the kit (`design/paperdoll-sos/kit/`) and `client-addons/`, both ignored.
- **Docs, 1 file:** this note.
- **Sizes:** no file over 5 MB (the largest is a 92 KB PNG); nothing BLOCKED.

P81 DONE
