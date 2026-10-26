# P632: scoring archery buttes and deeds, stage 1

Written 2026-10-26 by the Iron Golem (Claude Code). Builds stage 1 of [cc-P571-design-butte-and-deed.md](cc-P571-design-butte-and-deed.md), its first ordered prompt "BUTTE-A: integrate the reviewed hit artwork". Chase's decision (10-25 evening) took the design's defaults: the reviewed hit-display art once client proof passes, craftable deeds, optional tutorial practice, no score rewards. BUTTE-A is the art and its records only: no world items, recipe rows or scoring component yet, as the design orders. Those are stages 2 and 3, drafted at the end. The client proof is stage 4.

## In plain words

- Players will not notice anything yet. The 20 new archery butte pictures (an arrow or a bolt in each ring, or stuck in the frame on a miss, in both facings) are now in our art package. Nothing in game uses them, and no new package has been published.
- Each picture is the ordinary archery butte with one projectile added, so it sits exactly where the stock target does and blocks the same tile.
- The pictures are Archaaz's, credited and shipped the same way as his chest mimic: only inside our player package, as our own new picture numbers.
- Nothing for you to do. The scoring butte that shows these pictures, the house deeds and the New Haven practice range are the next stages (drafted at the end).

## Status

Done. The Iron Golem (Opus), branch `golem/Iron/P632` of both repos, not committed (the Golem commits). The gated build is green (section 4). No shard started, no world command, no package built for players or published, nothing deployed, no Haven contact. The `package` lock was taken once, for the package test suite's own build into `%TEMP%` (section 3).

## 1. The source and its manifest

`D:\UO\third-party\code\archery-butte-hits\` (P405's download; `SOURCE.txt` there). I measured every file myself:

| Group | Files (66x81, 24-bit BMP unless noted) |
|---|---|
| Arrow east | Arrow East Bullseye, Inner, Middle, Outer, Total Miss |
| Arrow south | Arrow South Bullseye, Inner, Middle, Outer, Total Miss |
| Bolt east | Bolt East Bullseye, Inner, Middle, Outer, Total Miss |
| Bolt south | Bolt South Bullseye, Inner, Middle, Outer, Total Miss |
| Not used | East Arrow and South Arrow (44x33), East Bolt and South Bolt (44x32): loose pieces the script never draws |

That makes 24 BMPs: 20 complete pictures, which are used, and 4 loose pieces, which are not. The script `ArcheryButteAddon.cs` is not used (stage 2 writes our own component).

**Terms.** None stated; credit Archaaz; private repo only; do not repost; EA-derived. The project already ships two Archaaz sets under exactly these terms: the animated mimic (cc-P50) and the partial-hue chests. Both are listed in `D:\UO\third-party\README.md` as "none stated; built from EA ... art, ship as our patch records only". The P571 design says to follow the existing intake decision rather than declare a new one, and Chase chose this set on 10-25. So it ships the same way: as our PNGs over free IDs, only inside the player package, credited in `SOURCE.txt` and the registry, with no EA file touched. Whether distribution is permitted stays the open review item the design names.

**Comparison with the stock butte**, decoded from the approved 7.0.117 client's `artLegacyMUL.uop` (vseUOAware `render_art_tile`; 0x100A and 0x100B are both 66x81):

- Every east picture is closest to 0x100A and every south picture to 0x100B.
- In 5-bit colour, each picture differs from its stock target only inside one box of at most 14 x 14 pixels (the projectile). No stock pixel is removed; at most 14 pixels are added, where a shaft sticks out of the canvas silhouette.
- So `--keep-geometry` is right: the canvas is the stock one and each picture stands where the stock target stands.
- Every pure-black (0,0,0) pixel is background reachable from the canvas edge (a flood fill found none enclosed), so making black transparent loses nothing inside the target.

## 2. What was added

| Where | What |
|---|---|
| IDs | **46690-46709 (0xB662-0xB675)**, four blocks of five (bullseye, inner, middle, outer, miss): arrow east 46690-46694, arrow south 46695-46699, bolt east 46700-46704, bolt south 46705-46709. Found with `scripts/find-free-art.py --run 20` against the approved client (art, art.def, tiledata, animdata, maps, multis, tileart), pinned and our code, and the registry. It reported 76 runs of 20 or more free IDs; 0xB662 starts a run of 1,310, right after the reward mounts' 46672-46689. Before using them I checked every pushed branch (143) for registry rows in 46690-46709: none. The download's IDs (0x7898-0x78AB) were not used. |
| `player-package/vendor/shattered-legacy-art/art/46690.png` to `46709.png` | Made by `scripts/anchor-art-frames.py --files <the 20 in ID order> --black-transparent --keep-geometry --first-id 46690`, which re-reads each PNG and checks it against its source. 66x81 each, about 80 KB in all. A contact sheet of all 20 beside the two stock targets is in the session scratchpad (`butte-contact-sheet.png`); I looked at it, and every ring and miss is where its name says, in both facings. SHA-256 prefixes: 46690 `5930db299779` to 46709 `2014e5dbab7d` (all 20 in the scratch log). |
| `registry.csv` | 20 `art` rows: what (facing, stock ID, ammo, ring), source (the resource name, number and the BMP's path), license "none stated; see SOURCE.txt". |
| `records.json` | 20 tiledata records after the mount items, each the stock butte's own record: "archery butte", flags `0x00008040` (ArticleAn 0x8000 \| Impassable 0x40), weight 255, height 10, layer, count, animId, hue and light 0. No animdata: the server will pick each still. Read from the approved client's `tiledata.mul` (SHA-256 `44f48a45...`, the hash recorded for the original 7.0.117 folder). The reader was checked against two records the repo already knows: wooden chest 0xE43 `0x204040` height 4, and earrings 0x1087 `0x400002` layer 18 anim 496. |
| `SOURCE.txt` | A section as the chest mimic's: author, resource, download, terms, what was used, the comparison, the ID map, how the IDs were chosen, what was done to the pixels, the records. |
| `server/customizations/Items/Addons/ScoringArcheryButteArt.cs` (new) | `ButteDisplay`, the design's explicitly numbered states (Empty 0, ArrowMiss 1, ArrowBullseye 2 ... BoltOuter 10), for stage 2 to save. `ScoringArcheryButteArt.ItemId(display, east)`: an explicit state and facing table, with Empty or an unknown value giving the stock target (0x100A or 0x100B). `Records`: the 20 records above. `Apply()` writes them into the server's `TileData.ItemTable`. |
| `server/customizations/ShatteredRunestone.cs` | `ShatteredLegacyArt.Apply` also calls `ScoringArcheryButteArt.Apply()`, beside the other art tables, so every picture blocks on the server as on the client. |

## 3. Tests: red first, then green

**Server**, `server/tests/Items/ScoringArcheryButteArtVerification.cs`, 3 facts:

1. `TheDisplayStatesKeepTheirSavedNumbers`: 0 to 10 in the design's order.
2. `EveryShotHasItsOwnPictureInEachFacing`: 20 distinct IDs, exactly 46690-46709; east states in east blocks and south in south; a few fixed points; Empty and an unknown value give 0x100A or 0x100B.
3. `EveryPictureHasTheStockButtesRecord`: after `ShatteredLegacyArt.Apply()`, each ID reads "archery butte", ArticleAn \| Impassable, impassable, weight 255, height 10; 20 records.

Run on builder image `sl-uo-builder:cc-P631` with the art file, `ShatteredRunestone.cs` and the fact file bind-mounted, filtered to the class.
- **Red**: a stub with the same names, where every state is the stock target, there are no records and `Apply` does nothing. Facts 2 and 3 failed ("Expected: 20, Actual: 2"; "Expected: archery butte, Actual: null"). Fact 1 passed there, because the enum is the seam itself.
- **Mutant**: `ArrowMiss = 11` turned fact 1 red.
- **Green**: the real table, 3 of 3.

**Package**, `player-package/tests/Build-UoOverrides.Tests.ps1`, under Windows PowerShell 5.1 (`powershell.exe`):
- New fact `TheScoringButteRecordsAreTheServersTableAndEveryPictureIsThere`. It reads the C# constants (first and last ID, flags by value, name, weight, height) and requires `records.json` to hold exactly those 20 IDs in order with those values, no animation and no animdata. It also requires 20 registry rows, each `art`, Archaaz's, "none stated", with a 66x81 PNG.
- The existing summary fact `TheServersCopyOfTheRecordsIsRecordsJsonAndEveryIdIsRegistered` now leaves 46690-46709 to the new fact and counts 801 registry rows and 672 art rows (was 781 and 652).
- **Baseline** before any change: exit 0.
- **Red**, with the PNGs present but no rows or records, exit 3. The summary fact failed on "expected [801] but got [781]" and the new fact on "expected [20] but got [0]". The existing winter fact also failed, on "expected [652] but got [672] PNG count equals the registry art rows", which is a further guard that each PNG must be registered.
- **Green**: exit 0, 26 facts passing.
- **Mutations the design asks for**, each applied to the repo files from a scratch backup and restored byte-for-byte (hashes compared) before the final green run:
  - PNG 46700 deleted: the new fact failed on "PNG for 46700" and the winter fact on its count, exit 2.
  - Record 46703's height set to 9: "expected [10] but got [9]", exit 1.
  - C# `TileWeight` set to 254: "expected [254] but got [255]", exit 1.

**Registry checks:**
- `python -P scripts/find-free-art.py --check-registry` (against the same approved client folder): "0 of 801 registered IDs are no longer free". Every new ID is "still free" apart from being ours.
- `python -P scripts/validate-art.py --data <same> check-registry`: "0 of 801 rows have problems", each new row "ok".

The approved client folder for both scans was assembled as hard links in my work copy's git-ignored `client-data/classic-client`, from `D:\UO\tool-trials\client-data-copy`. Its `artLegacyMUL.uop`, `map1`, `statics1` and `staidx1` hashes equal those recorded for the original 7.0.117 folder in `D:\UO\tool-trials\hashes-original-after.txt`. `tiledata.mul` was copied from `D:\UO\UOAlive\UOAlive 7.0.116.0`, which hashes to the original's `44f48a45...`; the tool-trial copy's own tiledata was modified by a tool trial. I did not read `D:\ShatteredLegacy\client-data` (another desk). I removed the links afterwards; the originals are untouched.

**`player-package/tests/Package-Client.Tests.ps1`**, run under the `package` lock because one fact does a real package build into `%TEMP%`: 6 passed, 3 failed. The 3 all stop at the build's client gate: "CLIENT GATE: STALE CLIENT BUILD in ...\client". The local TazUO build that suite copies (`D:\UO\tazuo-sl-build\client`) is older than the TazUO patches. The gate runs before anything is staged, so the art is never reached. This is an environment problem outside this prompt, and I did not change that suite. I did not re-run it on an unchanged tree; the cause is in the message.

## 4. Build gate

`docker\uo\build.sh -t sl-modernuo:cc-P632`, under the Golem's `docker-build` lock (taken, then released), with the Docker VM's page cache dropped and the build started detached. First run: **green**, exit 0: "Built sl-modernuo:cc-P632 with patches applied and 2553 shard test(s) passing". 2,557 tests: 2,553 passed, 4 skipped (the real-map facts), 0 failed; the 3 art facts are among those passed. Image `6866990f9ecd`.

## 5. CHANGELOG

No entry, and `VERSION` unchanged. Players see nothing: no item uses the pictures and no package is published. A staff line would also have nothing to point at, because there is nothing to `[add` yet. Stage 2 (the scoring butte) brings the first changelog line.

## 6. Deviations and decisions for Chase

- **Distribution terms** are handled as the earlier Archaaz sets were (section 1). This is the open item the design names and leaves to the intake decision; not a new license claim.
- **No client proof yet.** Chase's condition was "once client proof passes". This stage makes the art ready to inspect; the proof (a clean package install showing all 20 pictures) is the design's last prompt, drafted below as Draft C. Nothing here makes the pictures appear for players.
- **`Package-Client.Tests.ps1`'s stale TazUO build** (section 3): an environment fix for whoever next rebuilds the local client; nothing in this change.
- The Read tool stayed off for work-copy files in this unattended run. Edits to existing files went through an exact-replacement script that refuses unless each old text occurs exactly once. New files were written whole.

## 7. Remaining stages, ready to number

Each prompt writes its own notes, keeps files under 5 MB, checks its stop-request file, lets the Golem commit, starts from current canonical source, rereads the agreements, P571 and this note, and never deploys or contacts Haven. Do not run two of them at once against the art registry.

### Draft A: the scoring archery butte and its house deeds (P571 BUTTE-B)

**Touches:** server

Depends on P632 (IDs 46690-46709, `ButteDisplay`, `ScoringArcheryButteArt.ItemId`). Chase's choices (10-25): craftable deeds, optional tutorial practice, no score rewards.

1. `server/patches/ArcheryButte-practice-display-hooks.patch` against pinned `Projects/UOContent/Items/Addons/ArcheryButteAddon.cs`, registered with `apply-patches.sh`. Make `FacingEast` virtual. Add protected virtual no-op `OnPracticeShotResolved(Mobile from, Type ammoType, int area, bool split)`, called once after a miss is recorded and once after a hit is fully applied, never on a refusal. Add `OnPracticeGathered(Mobile from)`, called after `Gather` clears the counters and scores. List both call sites in the pinned-commit bump checklist.
2. `server/customizations/Items/Addons/ScoringArcheryButte.cs`: `ScoringArcheryButte : ArcheryButte` saving orientation and `ButteDisplay` (generated serialization v0), with ItemID always derived from state through `ScoringArcheryButteArt.ItemId`. Hit and miss pictures only for Arrow and Bolt. Local checks before fire or reset: a living player, same map, line of sight; no unfinished tutorial trial (`TutorialWingTrials.Current`); no marked loaner bow or arrows (the existing loaner-prefix constant). A close double-click with empty counters clears the picture and scores. The addon, plus `ScoringArcheryButteEastDeed` and `ScoringArcheryButteSouthDeed` (art 0x14F0, names "scoring archery butte deed (east)" / "(south)"). Owner chopping is refused while ammo is stored. A public subtype never yields a deed. Hue 0 on the scoring component.
3. Red-then-green facts in `server/tests/Items/Addons/ScoringArcheryButteVerification.cs`: hook delivery (one callback for a miss, a hit and a split; none on refusal; a stock butte alongside unchanged); repeated fire in both facings after an art change; distances 4/5/6/7, wrong side, off-axis; ring cutoffs with the host's controllable randomness, and a certain split at 50 stored; ammo and reset cases; tutorial loan refusal; save/load of every state in both facings (an invalid state becomes Empty); house placement, chop and redeed; the public subtype. No probabilistic tests, no sleeps.
4. `docker\uo\build.sh -t sl-modernuo:cc-P<nn>` green. Items are staff-constructible only (no recipe yet). CHANGELOG Staff line. Notes; `P<nn> DONE`.

### Draft B: butte crafting and the New Haven practice yard (P571 BUTTE-C)

**Touches:** server

Depends on Draft A.

1. `server/customizations/Engines/Craft/ScoringArcheryButteRecipes.cs`: two Carpentry rows in the Training group (1044297), registered once on ServerStarted. Carpentry 68.4-93.4, Tailoring 50.0-55.0, 55 boards or logs (`typeof(Log)`), 60 cloth, non-exceptional, no recipe scroll. The Clean Up Britannia `ArcheryButteDeed` at 80,000 points stays unchanged.
2. `server/customizations/Tutorial/TutorialScoringButtePlacement.cs`: `[TutorialButtes status|place|clear [dryrun]]`, Administrator and test world only, declared with `[ShardCommand]`. Check the candidates (yard-east 3411,2624 firing from 3416-3417,2624; yard-south 3420,2618 firing from 3420,2623-2624) on hash-verified map data: reachable firing and gather tiles, line of sight, no doors, stairs, tutorial props or trial spawns. Record verified XYZ, or corrected points with evidence. Placement is all-or-nothing, with the passable line markers and the sign (the design's text). Clear refuses while ammo is stored and removes only tagged props.
3. Red-then-green facts: idempotent recipe registration, a real craft consuming resources and making the right deed, insufficient resources; placement gate, dry run, all-or-nothing, rerun, moved or duplicate tags, clear with ammo. The bow lesson's three echo hits stay its completion path.
4. Build gate green. Seed nothing on a shared world. CHANGELOG Staff line (the recipes become player lines only when released). Notes; `P<nn> DONE`.

### Draft C: prove the package update and the butte end to end (P571 BUTTE-D)

**Touches:** server, client

Depends on Drafts A and B. Under the `package` and `test-shard` locks, on a throwaway loopback-only container with scratch saves and an isolated local player install:

1. Rebuild the local TazUO client first if `Package-Client.Tests.ps1` still reports STALE CLIENT BUILD (P632 section 3), then build the package with its checks.
2. Show an update from a package without 46690-46709 to one with them. All 20 pictures and both empty targets must appear, through real shots or documented deterministic staff setups. Also check repeated shots in each facing, gather and reset, arrows and bolts, split messages, anchors, readable scores and collision from every side.
3. Both house deeds placed, the public yard placed with `[TutorialButtes place`, then a save and restart.
4. Record the package version and hash and what was seen, and name honestly any visual check left for Chase. No Haven, no publishing, no shared-world restart. Notes; `P<nn> DONE`.

After Draft C's proof the overseer prepares Chase's release: the client package first, then the recipes and the yard placement, as the design orders.

P632 DONE
