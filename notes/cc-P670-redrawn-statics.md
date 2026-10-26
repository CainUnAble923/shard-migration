# cc-P670: Zigholtul's redrawn statics as an opt-in look in our client

Iron Golem, 2026-10-26. Branch `golem/Iron/P670` in both work copies.

## In plain words

- Players can now switch on Zigholtul's redrawn world art: fuller trees, crisper beds, armoires, chests and crystals.
  It is a tick box in the game's Options, Interface, Appearance tab, called "Redrawn world art (Zigholtul)". It is off
  for everyone until they tick it, it changes at once with no restart, and only that player sees it. Before and after
  shots from the game are in `notes\art\redrawn-statics\` (`*-off.jpg` and `*-on.jpg`).
- 787 of his 1,019 pictures ship. I left out the ones that would not sit where the stock picture sits: shop signs that
  hang lower, vines and branches drawn in other places, moongates, ankhs, and water, which came out a different blue so
  the sea looked like a patchwork. Trees ship only as whole sets, so no tree is half redrawn.
- The player download grows by about 6 MB, to 152 MB.
- **For you:** the package README now says "No EA game file is included" instead of "Nothing from EA is included". His
  own description says a few pictures were taken from EA's Enhanced Client. You okayed shipping them inside the
  package, but say if you would rather leave the whole pack out. Before the next package publish, rebuild the client
  (`client\Build-Client.ps1`); the package build will tell you to.

## 1. The PNGs, vendored

`player-package\vendor\zigholtul-redrawn-statics\` holds three things:
- `art\<id>.png`: 787 PNGs, byte for byte from the download.
- `manifest.csv`: all 1,019 files, each with its verdict, the reason, and a SHA-256 for every shipped file.
- `SOURCE.txt`: the terms, the credit, and the flag about the Enhanced Client.

`notes\cc-P670-tools\vendor.py` made these from `fit.py`'s verdicts. It reads the download as data and runs nothing
from `D:\UO\third-party`.

**Skipped by name: 11 files.** They are not named by a plain decimal art ID: `3308 vines.png` to `3313 vines.png` (6),
`3318 fallen log.png`, `3319 fallen log.png`, `3332 water plants.png`, `3333 reeds.png` and `3708 metal chest.png`.
TazUO's own loader would not take them either: `TryParseId` accepts a plain or 0x number, so "3308 vines" fails to
parse. `3708 metal chest.png` is an alternate beside the numbered `3708.png`.

| Of 1,008 numbered PNGs | Count |
|---|---|
| Ship (`ok`) | **787**: 530 small pieces, 121 tree trunks, 98 tree crowns, 38 structural (walls, doors, cave walls) |
| Left out: do not stand where stock does (`shifted`) | 181 |
| Left out: water statics | 34 |
| Left out: a tree set covered only in part (3315-3322; its log is only "3318 fallen log.png") | 6 |

All 1,008 have stock art to replace. None is one of our registered art IDs or a UI skin's ID (`Redrawn-Art.Tests.ps1`).

## 2. The setting (client patch 0008)

`client\patches\0008-redrawn-world-art.patch`, on top of 0001 to 0007:
- **The box.** Options > Interface > Appearance gets a "World" group with one checkbox, **Redrawn world art
  (Zigholtul)**. It is offered as working only when the client has the art installed; without it, the tooltip says
  "Not installed".
- **Off by default.** `Profile.SlRedrawnArt` is a bool with no initializer, so a new or existing profile starts false.
  It is saved as `sl_redrawn_art`.
- **Off is stock, exactly.** The PNGs go to `ExternalImages\sl-redrawn-art\`. TazUO's own loader scans only
  `ExternalImages\gumps` and `ExternalImages\art`, so it never sees them. With the box unticked, the redrawn table
  (`ExternalImageLoader.SetArtRedrawn`) is empty and every lookup is what it was.
- **On.** Each covered item ID is drawn from its PNG. Order of precedence: a UI skin's remap first (0005's scroll skin
  still wins), then the redrawn art, then the ID's own `ExternalImages\art` PNG.
- **No restart.** Switching calls `Art.Invalidate` on every changed ID, so the next frame redraws. The in-game shots
  show both states. When a sprite reloads, `Art.Get` recomputes the click picker and the real bounds from the new
  pixels, so clicking and tree transparency follow the redrawn shapes; a bigger redrawn tree has a bigger click area.
- **One cost.** As with 0005's skins, the old atlas space is not reclaimed, so each switch re-adds what is on screen to
  the texture atlas. Flipping it many times in one session grows memory a little; a relog clears it.
- **Applied at login** beside the skins (`World.CreatePlayer`). New file `Game\Managers\SlRedrawnArt.cs`, plus hooks
  in `ExternalImageLoader.cs`, `Profile.cs`, `AppearanceTab.cs` and `World.cs`.

**Tests, seen failing first.** `SlRedrawnArtTests`, 4 facts. I ran them against stubs with the same public names and
no behaviour: 3 failed and 1 passed. The one that passed is the skin-precedence guard, which already held because
0005's remap exists.
- **The real code:** 4 of 4 pass, and the whole client suite passes, 1,322 of 1,322.
- **A fresh `Build-Client.ps1` into `D:\UO\golems\Iron\tazuo-p670`:** applied 0001 to 0008, passed all 1,322 tests,
  and published. `sl-build.txt` names 0008 with SHA-256 `2377b5f8...`.

## 3. Fit, and tiledata

`notes\cc-P670-tools\fit.py` measures where each picture stands, using the client's anchor rule. The client draws a
static centred on its tile, standing on the tile's foot. Each picture's lowest row and its base (left, right and centre
of the bottom four rows) are compared with the stock picture's. Sizes: 674 of 1,008 are the same size as stock, 208
are larger and 126 smaller. The rules, set from renders of the real map (`preview.py`, three panels: stock, every
redraw, only those that fit):

| Kind | Rule | Why |
|---|---|---|
| Structural (wall, door, window, arch, stair, floor, roof, post, pillar, column) | bottom and base within 1 px | a wall off by one shows; all 38 pass |
| Tree sets (a run of trunks, then the crowns after them) | the whole set ships when every piece with stock art is in the pack, else none of it | the redraws are fuller trees, about 1.7 times the size, with trunk, columns and crown drawn to fit each other, not stock. Judged piece by piece, the first pass kept redrawn trunks and dropped their crowns: bare trees (orchard) and half-redrawn big trees (Yew). As sets, they all stand on their tiles. Two blank PNGs in set 3438-3455 (3449, 3455) are the author hiding stock columns his fuller tree covers, and ship with their set |
| Water | never | another blue than stock water land; the sea drew as a patchwork of squares |
| Everything else | bottom within 2 px, base centre within 4 px | the contact sheets of the 181 left out show them truly off: shop signs 5 to 16 px lower and a different shape, vines and branches drawn in other places, ankhs 3 to 4 px off |

Evidence in `notes\cc-P670-tools\out\`: `fit.csv` (every ID: sizes, offsets, kind, set, verdict),
`preview-{yew-forest,yew-trees,jungle,orchard,waterfall,yew-house,crystal-cave}.jpg`, and `sheet-shifted-*.jpg`
(stock beside the redraw on the same tile diamond). Re-checked on the vendored folder itself: 787 of 787 ok.

**Tiledata.** Only pictures change. Tiledata (height, flags, light), animdata and light.mul are the stock files, and
the patch touches no tiledata code.
- **Animated statics.** 14 ship: 13 waterfall frames and 1 stew. Every frame of each animation is in the pack, so
  nothing flips between styles. The 14 moongate frames are among the shifted ones and stay out.
- **Light sources.** 3 lamp posts ship; their light comes from tiledata and light.mul, unchanged.

## 4. The package

`Build-PlayerPackage.ps1` (its header notes the new vendor folder):
- **Before staging,** the vendor folder must hold exactly `manifest.csv`'s shipped files, byte for byte, or the build
  stops.
- **Staging:** into `app\tazuo\ExternalImages\sl-redrawn-art\`.
- **Gate 4,** on the finished zip: exactly those files there, each with the manifest's SHA-256. I proved it on a copy
  of the real zip with one redrawn PNG changed by a byte: `-CheckZip` failed with "...sl-redrawn-art/12252.png is not
  the vendored redrawn PNG (SHA-256 differs from manifest.csv)".

**The real build** ran under the `package` lock, with `-TazUO D:\UO\golems\Iron\tazuo-p670\client` (0001 to 0008) and
`-UoData D:\UO\UltimaOnlineVanilla`. Every gate passed: paperdoll fit, animation encode, gate 6, and `-CheckZip`'s
gates 4, 5 and 6. Result: `ShatteredLegacy-2026.10.26.1754.zip` in `dist\` (git-ignored), **152,476,726 bytes**,
4,053 entries, "TazUO 3212623f + 8 patches".

**Size before and after.** The 787 redrawn entries are 6,250,792 bytes raw and 6,240,391 compressed. So the package is
about **146.2 MB before and 152.5 MB after**, about 6 MB more. The "before" figure is derived (the zip less those
entries), not a second build; 0008's own code adds a few KB to the client.

**Package tests.**
- `Redrawn-Art.Tests.ps1`: 6 facts. Red first: 5 passed and 1 failed (the build did not stage the folder yet). After
  the build change, 6 of 6 pass.
- `Ui-Skins.Tests.ps1` 4 of 4 and `Paperdoll-Bodies.Tests.ps1` 9 of 9 pass.
- `Package-Client.Tests.ps1` fails 6 of 9 here, on this desk: its child builds look for EA client data under
  `ShatteredLegacy\client-data\classic-client`, which this work copy does not have ("No EA client data in
  ...\client-data\classic-client (-UoData)"). The failures come from that, not from this change; I did not run it on
  another desk.

## 5. The in-game shots

These are in `notes\art\redrawn-statics\`, with `shots-log.txt`:
- `1-forest-yew-off.jpg` / `-on.jpg`
- `2-house-interior-yew-off.jpg` / `-on.jpg`
- `3-dungeon-crystal-cave-off.jpg` / `-on.jpg`

How they were taken:
- **Shard.** A private shard (P661's `proof-shard.ps1`, `sl-modernuo:latest`, a copy of the bot world, 127.0.0.1:2596)
  under the `test-shard` lock. The shared Test Shard on 2594 was not touched. The shard was removed and the lock
  released afterwards.
- **Client.** Our client from 0001 to 0008, with the 787 PNGs in `ExternalImages\sl-redrawn-art`, run by
  `notes\cc-P670-tools\shots.ps1` with `scenes.json`.
- **Each scene.** Iron (Admin) moves Iron the Tester to the spot and makes him Blessed. The Tester then logs in twice
  from the same client folder, with `sl_redrawn_art` false and then true.

| Scene | Spot | What changes |
|---|---|---|
| Forest | Trammel 524,1036 (Yew) | the trees: fuller and lighter, each on its trunk's tile |
| House interior | Trammel 664,824 (Yew) | beds, armoires and chests inside (server-placed furniture items too, since items use the same art) and the trees outside |
| Dungeon | Trammel 6536,186 (a crystal cave) | the crystals; the cave is dark at that hour, so this pair shows the least |

Two failed attempts, both redone:
1. The first run wrote the profile key as `SlRedrawnArt`. The client's key is `sl_redrawn_art` (snake case, like
   `sl_skins`), so both shots were stock. Fixed in `shots.ps1`.
2. The second run's Tester had died in the forest in run 1, so its shots were a grey ghost's view. Run 3 used a fresh
   world copy and a Blessed Tester.

The patch-notes gump and the paperdoll sit over the top left of every shot; the world shows round them.

## 6. Credits and CHANGELOG

- **CHANGELOG:** 2026.10.26.13, one Added player line. `VERSION` bumped to match.
- **Credits:** the package README (`player-package\payload\README.txt`, "What is in here") credits Zigholtul's UO Art
  Static Replacements for TazUO and says where the files are. Its line "Nothing from EA is included" now reads "No EA
  game file is included", because his description says a few pictures came from EA's Enhanced Client. That is your
  call to keep (question above).
- **`client\README.md`:** a row for 0008.

## Not verified

- A player's machine through the launcher. The client and package were built and gate-checked here, and the shots ran
  this build, but the zip was not installed and run from `Play.ps1`.
- Switching live in a running game by clicking the box. The shots switch by profile between logins. The unit tests
  prove the live path (the table switches and names every changed ID), and the redraw is the same `Art.Invalidate`
  path 0005's skins use live.
- Which of the 787 came from EA's Enhanced Client. The download does not say.

## For the overseer

- After the merge, rebuild the shared client with `D:\ShatteredLegacy\client\Build-Client.ps1` before the next package
  build. `D:\UO\tazuo-sl-build\client` has 0001 to 0007 only, and the client gate will call it stale.
- `D:\UO\golems\Iron\tazuo-p670\` is this prompt's client build and worktree (outside both repos); it can be deleted.

## Commit preflight

- Code (`D:\UO\golems\Iron\ShatteredLegacy`), changed: `CHANGELOG.md`, `VERSION`, `client\README.md`,
  `player-package\Build-PlayerPackage.ps1`, `player-package\payload\README.txt`.
- Code, new: `client\patches\0008-redrawn-world-art.patch`, `player-package\tests\Redrawn-Art.Tests.ps1`,
  `player-package\vendor\zigholtul-redrawn-statics\` (787 PNGs, the largest 77 KB; `manifest.csv`; `SOURCE.txt`).
- Docs: this file; `notes\cc-P670-tools\` (scripts and `out\`, 3.5 MB); `notes\art\redrawn-statics\` (6 shots and the
  log, 1.4 MB). No file over 5 MB. `docs\` untouched. Not committed (the Golem commits).
- Locks: `package` and `test-shard`, each taken and released. Haven was not touched. Nothing asked of Chase through
  Ask-Chase.

P670 DONE
