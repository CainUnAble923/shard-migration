# cc-P374: the guild hall decor proof (continues P265): a screenshot per set, the live refusal shown

## In plain words

- All four guild hall decor sets now have in-game screenshots: the Order of the Alembic's vat, tanks, flask bench and
  crystal ball, the Smiths' fire pit and blacksmith, the Artificers' crystal gate, and the five towers with the marble
  railing and ladder. Every piece stands where its template puts it, and the towers' pieces meet without seams.
- The proof found one fault: in our game client none of the new decor moved. The vat did not bubble and the tanks,
  fire pit, crystals and orbs stood still on their first frame. The cause was a small quirk in the client. A fix is
  now in the client's patch list, and with it all of them move (three short animations in the notes show it).
- With the test-shard setting off (as on the live shard), the decor commands refuse and place nothing (shown).
- For you: after merging, rebuild our client (`client\Build-Client.ps1`, which also picks up patches 0005 and 0006
  that the shared client build does not have yet), then build and publish the player package. Players will only see
  the decor once you say where the halls go (F-49).

## Status

Done. The Iron Golem (Opus), branch `golem/Iron/P374` of both repos, not committed (the Golem commits). Image
`sl-modernuo:cc-P374` = `4fddd4cfba64` (main at `995251a`, which holds P265's merge `94eabb0`). `latest` untouched.
Nothing ran against the live shard or the shared Test Shard (2594): every in-game step ran on a private copy of the
bot shard's world on `127.0.0.1:2596`, under the `test-shard` lock, removed afterwards. The shared client build
(`D:\UO\tazuo-sl-build`) was not changed. The package was not built or published.

## 1. The image under test

`docker\uo\build.sh -t sl-modernuo:cc-P374` from this Golem's code copy (current main, so P265 and its start-up fix
`VirtualCheckActivatorFirst.cs` are in), run detached through a script file under the `docker-build` lock, the WSL
page cache dropped first (10 GB free before). **2,380 tests: 2,376 passed, 4 skipped, 0 failed.**

Started on the private copy (part 2): "Loading world done (212362 items, 35229 mobiles) (2.72 seconds)", then
listening on 2596. Five boots in all (three test-on, one live, one for the client fix); no exception in any log.

## 2. The shard

`notes\cc-P374-tools\proof-shard.ps1` (P281's script with a `-Live` switch): copies `D:\UO\bot-shard`'s Configuration
and world (read only; the nightly bot was not running, 11:47 to 12:31), `listeners` 0.0.0.0:2596 published on
127.0.0.1 only, `serverListing.serverName` "Shattered Legacy TEST", `testCenter.enable` True (False with `-Live`),
autosave off, container `sl-p374-proof`. It refuses 2593 and 2594. The bot shard's save is from main, so it loaded
with no type prompts. The Golem's accounts were made at start (`[GolemAccounts]`). Iron's Admin typed the commands
(P219's `uobot.legionsetup`, `safety.py` already allows 2595-2599) and TazUO logged in "Iron the Tester".

## 3. Seed and shoot

`notes\cc-P374-tools\shots.py` writes the shot list for P265's `notes\cc-P265-tools\proof.ps1`. Each shot sends the
Admin to Trammel and the anchor (`[go x y z`), seeds with `place here` (or `place <group> here`), reads `status`,
then puts the Player on a free tile (`LogoutMap`, `LogoutLocation`, `Map`, `Location`, Point3D without spaces). Only
three empty spots exist near P265's (no other 26-tile square, none of 42 tiles), so the structure set went on the
Alembic and Smiths spots after those sets were shot and cleared.

Every place answered with no refusal (the full answers are in `notes\cc-P374-tools\proof-log-shots.txt`):

| Shot (`notes\art\cc-P374\`) | Seeded at (Trammel, z 0) | Server's answer |
|---|---|---|
| `1-alembic.jpg` | 1135,1791 | placed 51 item(s) of vat, tanks-north, tanks-west, bench, scrying; 0 already there |
| `2-smiths.jpg` | 1199,1823 | placed 5 item(s) of forge |
| `3-artificers.jpg` | 1231,1889 | placed 8 item(s) of gate |
| `4-structure-towers-and-balustrade.jpg` | 1131,1788 (Alembic cleared first: "removed 51 item(s)") | tower-large 29, tower-medium 14, balustrade 10 |
| `5-structure-small-and-white-towers.jpg` | 1182,1838 (Smiths cleared first: "removed 5 item(s)") | tower-small 5, tower-white-brick 24, tower-white-column 34; status "116 item(s) from 2 placement(s)" |
| `6-structure-white-column-tower.jpg` | (same placement, closer) | |

What each shot shows (checked against P265's renders, `notes\cc-P265-tools\preview-*.png`):
- **Alembic:** the vat in the middle, four tanks on stands along each wall (fish, frog, hamster and lobster north;
  scorpion, snake, tarantula and turtle west), the eight-counter bench with a flask on each, the crystal ball on its
  cloth. Laid out exactly as the render. The vat and flasks show the art's own silver-grey and white: every template
  row has hue 0, so nothing tints them (a choice for F-49, not a fault).
- **Smiths:** the lit fire pit, the cold pit, the stock forge and anvil, the blacksmith at the anvil.
- **Artificers:** the arc orb gate between the green and purple floating crystals, its field before it, two pillars
  each with a small orb.
- **Structure:** the large and medium brick towers with their conical turrets seated on the wall tops; the small
  crenellated tower; the white brick tower with its gold-ribbed dome; the two-storey white column tower with its dome;
  the L of marble balustrade and the marble ladder. No seams or gaps between the wall pieces, no turret or dome
  floating or sunk.

The first run's camera put the sets under the patch-notes and paperdoll gumps that a first login opens (the small
tower was hidden entirely). The shots were retaken from a fresh world copy with the Player about 12 tiles of screen
west of each set's middle; the kept shots are that run. The gumps still show at the top left and cover no decor.

**Templates:** no piece was out of place, so `design\guild-hall-decor\templates.json` is unchanged.

### The animation check, and the fault it found

A still cannot show animation, so `proof.ps1` gained `-Frames`/`-FrameMs` (a burst of captures after the shot) and
`notes\cc-P374-tools\framediff.py` counts the pixels that change between them. With our shared client build
(`D:\UO\tazuo-sl-build\client`, TazUO 3212623f + patches 0001-0004), **nothing in any decor shot changed** across 6
frames: only the direction cursor. A control burst beside the Britain moongate (`8-control-moongate.jpg`, a stock
animated item) did change, so the capture sees animation; our pieces do not animate.

The records are right: the override `tiledata.mul` has the Animation flag on 0x6D70 etc., and `animdata.mul` has the
vat's 4 frames at interval 3. The fault is in the client. TazUO's `AnimatedStaticsManager` keeps each animated
static's current frame on its art index entry (`Arts.File.Entries[id + 0x4000].AnimOffset`), but the item, static and
sorting views read it back through `GetValidRefEntry`, which returns the shared `UOFileIndex.Invalid` entry (offset
always 0) when the entry has no data in `artLegacyMUL.uop`. P265's IDs (0x6D70-0x6E86) lie past the stock art table:
their art is only an `ExternalImages\art` PNG, so their entries are empty and they always draw frame 0.

**Only P265's IDs are affected.** A check of `artLegacyMUL.uop` by hash shows that every earlier animated add-on piece
(winter decor 13192+, shattered runestones 15376+, the chest mimic, the New Haven lanterns, the flying loot) uses an ID
with stock data, so those animated already. The flying loot also goes through effects, not this path.

**The fix: client patch `client\patches\0007-animated-external-art.patch`** (code repo, listed in `client\README.md`).
A new `UOFile.GetAnimOffset(index)` reads the entry itself; `ItemView`, `View.DrawStatic` and
`GameSceneDrawingSorting` use it instead of `GetValidRefEntry(...).AnimOffset`. Stock art animates as before. Plus 3
unit tests (`tests\ClassicUO.UnitTests\IO\AnimOffsetTests.cs`).

- `client\Build-Client.ps1 -Out D:\UO\golems\Iron\tazuo-p374` (the guard refuses an output path containing
  "shard-migration", which the session scratchpad's does): every patch 0001-0007 applied with no fuzz, **1,318 client
  unit tests passed, 0 failed**, published with `sl-build.txt` naming 0007 (sha256 `fc161906...`).
- Red: `GetAnimOffset` changed back to the old read (`GetValidRefEntry(index).AnimOffset`): 1 failed,
  `AnArtIdWithNoFileEntryStillReportsItsAnimationFrame`, "Expected ... to be 2y, but found 0y". Restored by SHA-256
  (`6142cb33...`), then 3 of 3 passed.
- In game with that build (`proof.ps1 -ClientSource D:\UO\golems\Iron\tazuo-p374\client -Frames 8 -FrameMs 400`):
  the vat changes on every frame except the one that comes back to frame 0, the crystal ball flickers, the north
  tanks' creatures move, the fire pit and blacksmith move (761 changed pixels), and the gate, field, crystals and
  orbs move (6,389). The west tanks' creatures are subtle by design: 12 to 28 pixels a frame, and the scorpion and
  turtle hold for four or five frames before one twitch. They fall under the change threshold in this short burst.
  The three animations are `anim-alembic-vat-tanks-ball.gif`, `anim-smiths-firepit-blacksmith.gif`,
  `anim-artificers-gate-crystals.gif` (cropped, 8 frames, 400 ms).
- A first confirmation used a hand-patched copy of the shared client's source in the session scratch (same change);
  its frames were replaced by the official build's.

## 4. The live refusal

The copy restarted with `-Live` (`testCenter.enable` False, read back from the copy's `modernuo.json`), Admin at the
Artificers' spot (`notes\cc-P374-tools\proof-log-refusal.txt`):

```
[DecorArtificersHall place here
    Refused: the guild hall decor seeders run on the test shard only (testCenter.enable is false here). Nothing was placed or removed.
[DecorArtificersHall clear all
    Refused: the guild hall decor seeders run on the test shard only (testCenter.enable is false here). Nothing was placed or removed.
[DecorArtificersHall status
    [DecorArtificersHall] Artificers' Order: 8 items in 1 group(s). In the world: 0 item(s) from 0 placement(s).
```

`7-refusal-live.jpg`: the Player on the empty spot. Before the restart, on the test-on copy, `clear all` removed every
set: the dry run "would remove 51 item(s)", then 51, 5, 8 (the structure had been cleared with its world copy), and
each `status` read "In the world: 0 item(s)". Each world copy was deleted after its run, so no save with the decor
types reached any other shard.

## Tests

| Run | Result |
|---|---|
| Server gate, `build.sh -t sl-modernuo:cc-P374` | 2,380 tests: 2,376 passed, 4 skipped, 0 failed; image `4fddd4cfba64` |
| Client, `Build-Client.ps1` with 0001-0007 | 1,318 passed, 0 failed |
| Client red, the old read in `GetAnimOffset` | 1 failed (the ExternalImages fact), 2 passed |
| Client green again, `--filter AnimOffsetTests` | 3 of 3 passed |
| Server gate after the CHANGELOG line, `--tests-only` | 2,380 tests: 2,376 passed, 4 skipped, 0 failed |
| In game | above: every place answered, every shot taken, the refusal shown, the fix seen animating |

## Deviations and decisions for Chase

1. **A client patch, outside the prompt's "Touches"** (server, docs). The prompt says to build nothing unless the
   proof finds a fault; it found one, and the fix belongs in our TazUO patches. Without it the decor ships still.
2. **The shared client build is behind main** already: `D:\UO\tazuo-sl-build\client\sl-build.txt` lists 0001-0004,
   main has 0005 and 0006. The package's client gate refuses it until `Build-Client.ps1` runs again; 0007 adds one
   more reason. I did not rebuild the shared client (other Golems' proofs use it).
3. **`D:\UO\golems\Iron\tazuo-p374`** holds the verified build (client and its worktree `src`, registered in
   `D:\UO\cc-p40-work\tazuo-3212623f`). It can be deleted (`git -C D:\UO\cc-p40-work\tazuo-3212623f worktree remove
   --force D:\UO\golems\Iron\tazuo-p374\src`) once the shared build has 0007.
4. **P265's `proof.ps1` changed** (it is a docs tool): `-Frames`/`-FrameMs` and `-ClientSource`, defaults as before.
5. **The structure set was shot in three pictures from two anchors**, not from one placement: no 40-tile empty
   square exists in the area. The groups were placed one by one, as the prompt allows.
6. **Hue:** the vat and flasks are placed unhued (hue 0 in every template row). If you want a tint, F-49 sets it.
7. **CHANGELOG:** a Staff line under a new 2026.10.25.2 (VERSION too), since players see no decor yet.

## Files changed

`ShatteredLegacy`: `client\patches\0007-animated-external-art.patch` (new), `client\README.md` (the 0007 row),
`CHANGELOG.md`, `VERSION` (2026.10.25.2).

`shard-migration`: this note; `notes\art\cc-P374\` (8 JPEGs, 3 GIFs, 2.0 MB); `notes\cc-P374-tools\` (`shots.py`,
`proof-shard.ps1`, `framediff.py`, `tazuo-animoffset.patch` (the same change against the shared build's source, for
reference), four `proof-log-*.txt`); `notes\cc-P265-tools\proof.ps1` (two options); P265's note (a pointer here).

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun -NoRefresh -NoArchive -CodeRepo
D:\UO\golems\Iron\ShatteredLegacy -DocsRepo D:\UO\golems\Iron\shard-migration -Branch golem/Iron/P374`. Code: 4 files
pending (the patch, the README row, CHANGELOG, VERSION). Docs: 22 (this note, the 11 pictures, the tools and logs,
P265's note and `proof.ps1`). Neither is BLOCKED. Largest new file: `anim-artificers-gate-crystals.gif`, 445 KB.

```
Repo Result
---- ------
code dry run
docs dry run
```

Clean-up: the proof container is removed and every world copy deleted; the `test-shard` and `docker-build` locks are
released. Left on disk on purpose: `D:\UO\golems\Iron\tazuo-p374` (deviation 3).

P374 DONE
