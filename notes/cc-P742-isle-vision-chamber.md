# cc-P742: the isle vision moves to a dungeon shrine where the Stranger breaks the Gem

Iron Golem, 2026-10-31. Code copy `D:\UO\golems\Iron\ShatteredLegacy`, docs copy `D:\UO\golems\Iron\shard-migration`,
both on `golem/Iron/P742` (main at the P751 merge). Not committed (the Golem commits). Nothing deployed; the shared
Test Shard was not touched.

## In plain words

- **The vision now takes you to a small dungeon shrine.** When a trainee double-clicks the signpost at the standing
  stones, the screen goes dark and they are carried into a stone room lit by braziers and torches. Inside are broken
  pillars, bones, glowing runes on the floor and the Gem on a white pedestal in the middle. They watch unseen. Pictures:
  `notes\cc-P742-review\tazuo-vision-02-shrine-lit.jpg` and the rest of that folder.
- **The Stranger breaks the Gem in front of you.** He steps out of the dark corner, walks to the pedestal and strikes
  it twice. The Gem bursts into shards on the pedestal and across the floor (`tazuo-vision-05-strike.jpg`,
  `-08-gem-shatters.jpg`, `-09-shards.jpg`). The story lines and the slower timing are as before. Then your echo and
  the hooded figure appear in the same room.
- **You come back exactly where you stood**, free to move, with nothing lost. A disconnect or a server restart in the
  middle also puts you back on that tile; nobody can be left in the room.
- Nothing for you to do. It goes to its build review (the room is new), and it applies cleanly to the isle-only release
  branch for the next release.

## 1. The chamber

**Where.** The empty strip of site A on the player's own lesson map (the Fold, map 32, or their private copy):
- x 6170-6570, y 3752-3760: west of the Wakening Isle (x 6594 and east), north of Blackthorn's Fold dungeon
  (`BlackthornFold.Dungeon`, y 3804 and south).
- It is void land (0x0244, Z 0) on stock Trammel (the release) and on the Siege of Sosaria map (main). Both were read
  from the files: every tile of x 6160-6593, y 3744-3803 is void on both, with no statics.
- Nothing walks there: void is impassable, and FoldRegion, the Fold's default region everywhere, refuses every travel
  spell. So the room needs no door.
- FoldRegion is also what gives the vision its own light (`TutorialVisionScene.AlterLight`), and that works on the
  whole Fold map, chamber included.

**How it is placed.** As scene props, like the vision's figures, not as map statics:
- `TutorialVisionChamber.Build` lays the 114 pieces of `TutorialVisionChamberLayout` when the vision starts and takes
  them away when it ends. They are all `TutorialVisionProp`, which deletes itself if a save ever loads it.
- So there is no map patch, no seeding and nothing on an existing world to upgrade. It also applies to the release
  without its map.
- One room per scene, in slots 28 tiles apart, so no room is in another's view (a client sees 18 tiles):
  - on a private copy, slot 0 always;
  - on the shared Fold, the first free slot (15 slots).
- The pieces' serials go into the save with the scene.

**The room** (`notes\cc-P742-review\placed.md`, `render-chamber.png`; generator `notes\cc-P742-tools\gen_chamber.py`):
- **Walls: OSI's own dungeon brick.** `survey_dungeon.py` counted the statics in OSI's stock dungeons: "dungeon wall"
  0x0242 (9,008 tiles) and 0x0241 (8,260) are the commonest. Its grid of a room at 5122-5146, 680-702 shows the roles:
  - 0x0244 the post;
  - 0x0241 east-west runs, 0x0242 north-south runs;
  - 0x0243 where runs meet.
  Laid by the guide's corner rule (2.2): post NW, 0x0241 along the north row to the NE tile and along the south row,
  0x0242 down the west column to the SW tile and down the east column, 0x0243 at the SE. The cave wall statics
  0x025C-0x0280 were looked at and not used: OSI hardly uses them (its caves draw walls as raised cave land).
- **Floor** at Z 0, inside the box and under the south row and east column (2.2): grey pavers 0x051D/0x0519 on the
  shrine's 5 x 5, and cave floor 0x053B-0x053F round it. Those are the floors OSI's dungeons use most.
- **The shrine:**
  - the pedestal 0x1223 in the middle (the Gem 0x1EA7, Celestial hue, on top at the pedestal's height 9);
  - four glowing floor runes round it (0x0E5D, 0x0E60, 0x0E63, 0x0E66);
  - two lit braziers 0x0E31 (light Circle300) on its north-east and south-west.
- **Light on the walls the camera shows** (guide 3): torches 0x0A0C on the north wall and 0x0A07 on the west wall, on
  the floor tile in front, Z 13.
- **A forgotten shrine:**
  - broken pillars 0x45B5 and 0x45B4 in the north-east and south-west corners;
  - bones 0x0ECB, 0x0ECE and 0x0ED1 by the walls;
  - stalagmites 0x08E1 and 0x08E4.
  These are from the guide's Shrine and Dungeon lists. They are not the virtue shrine's holy dressing, since this is
  where the Gem is broken.
- **Every facing piece was rendered alone before use** (11.2): the pieces sheet, the cave-wall strip and OSI's room.
  Nothing was turned from its art.
- **Kept clear of everything but floor:** the Stranger's walk (1,1), (2,2) and (3,3), the onlooker's tile (6,6), and
  (5,5), the line of sight and the echo's tile. The generator refuses a layout that puts anything there, and fact 1
  checks it.

## 2. Into the vision

At the vision's first beat (`Beats.Start`):
- the screen fades and the light goes black, as before;
- the room is built in the scene's slot;
- the player is hidden, moved to the onlooker's tile (6,6), two tiles south-east of the pedestal, and turned toward it.
  They stay frozen for the scene, as before.
- Hidden means no one else sees them, and they see themselves as a ghostly onlooker. Their earlier hidden state is kept
  and restored.
- The windows over the middle of the screen close, as before (P721).

## 3. The Stranger breaks the Gem

The beats keep P721's and P733's timing (61 s) and P665's lines. Only the places changed:
- **2 s:** the light comes up. The Gem sparkles on its pedestal, and the Stranger stands in the north-west corner,
  facing it.
- **4 s and 6 s:** he walks to the pedestal, a step every two seconds (slower than P721's tile a second).
- **7 s:** he faces the Gem: south-east, so the onlooker sees him face on.
- **8 s:** the strike: the one-handed slash, the sword's hit, the bolt. "The sword strikes the Gem. The shards fly."
- **9 s:** the burst. **11 s:** the second blow.
- **16 s:** **the Gem shatters**:
  - a light flash (the screen effect, and the light at 0 for that second);
  - a burst on the Gem;
  - shards fly out (moving effects) and lie on the pedestal and on five floor tiles round it, all in the Gem's hue;
  - the broken sword and its point fall beside it.
  "The blade breaks with it." At 17 s the braziers' light is back.
- **23 s onward, as before**, in the same room: the fold, the player's echo (at 5,5, facing them), the hooded figure
  (at 2,2) and the broken sword, then "What you keep", the fade and the gate's line.

## 4. Back, and safe

- **At the end:** the room is taken away, and the player is put back on **the exact tile they stood on**. They are
  unfrozen, hidden as they were before, with the light restored and the subtitles closed. The lesson finishes as
  before. Nothing is taken or given.
- **A disconnect, death, a move off the map or a cancelled lesson** mid-scene ends it at once the same way (the scene's
  timer sees it within a second).
- **A server restart mid-scene:**
  - the save's `TutorialVisionStore` is now **version 1**. It keeps each player's spot and hidden flag, beside the
    serials of everything the scene placed, the room's 114 pieces included;
  - after the world loads, recovery puts the player back on their spot (or sets their logout spot) and deletes the
    pieces;
  - a version 0 save still reads, and sends its players to the stones as before.
- **And a last net:** at login, a player found inside the chamber strip with no scene playing (a crash between saves,
  a lost record) goes to the stones of that map, seen and free (`TutorialVisionScene.SendOutOfChamber`). Staff are left
  alone.

## Tests

**New facts** (`server/tests/Tutorial/TutorialVisionChamberVerification.cs`, 9). Each was seen failing on a mutant
that undoes its own fix and nothing else (`mutate742.py`, `run-mutants.sh`, `mutants.txt`, logs in `mutant-logs\`):

| Fact | Mutant | Fails |
|---|---|---|
| 1. the room whole, the scene tiles clear, the strip where nobody walks | `corner`: the corner piece at the NW | 1 |
| 2. into the shrine hidden and frozen, the room round them, the Gem on the pedestal | `noenter`: no move | 2 (and 3, 5, 6, 8) |
| 3. the walk, the facing, the strike, the shatter with its flash, shards on the pedestal | `noflash` | 3 |
| 4. back on the exact tile, free, hidden as before (both ways) | `oldreturn`: P665's return to the stones; `keeproom` | 4 |
| 5. a disconnect: straight back, the room gone | `oldreturn`, `keeproom` | 5 |
| 6. a restart: back on the saved spot, nothing left | `nospot`: the save forgets the spot | 6 |
| 6b. a version 0 save still reads (to the stones) | `v0`: read as version 1 | 6b (see below) |
| 7. a login in the chamber with no scene goes to the stones | `nologin` | 7 |
| 8. two scenes on one map, two slots out of each other's view | `oneslot` | 8 |

- `v0` first passed: the fact wrote one scene, so a misread only read zeros past its end. The fact now writes two
  scenes, and the mutant fails it (`mutant-logs\v0-2.log`); the green run is `probe-v0-green.txt`.
- **Changed fact:** P721's `TheVisionIsLitWalksUpStrikesTheGemAndRunsLonger` measured the Stranger from the player's
  tile and counted the braziers among the scene's props. It now reads the chamber's braziers and measures him against
  the pedestal. It still checks the same things (lit, two braziers, at a distance, then beside the Gem facing it, the
  strike, 61 s).
- **P665's seven vision facts pass unchanged** (the disconnect, death and restart ones still find the player within 4
  of the stones, since they stood there).
- **The vision facts on the builder image** (`probe.sh` on `sl-uo-builder:cc-P735`): **17 of 17** (`green-probe.txt`).
  The first run (`red-probe-1-my-mistakes.txt`) failed 3 of mine:
  - slots 24 apart put a neighbour's wall at exactly 18 tiles; now 28;
  - the test host has no tiledata, so the pedestal read 0 high; now it falls back to its height, 9;
  - one fact asked too much.
- **Gated build** (`docker/uo/build.sh -t sl-modernuo:cc-P742`, `docker-build` lock taken and released): **EXIT=0**,
  2,854 tests: 2,848 passed, 6 skipped, 0 failed (`green-gated-build.txt`).

## Live, on a private shard (127.0.0.1:2596, `test-shard` lock taken and released, container down)

- **Setup:** `proof-shard.ps1` on a fresh copy of the bot world each time, image `sl-modernuo:cc-P742`. The map overlay
  is main's patch on the SoS base (`D:\UO\golems\Iron\p735-work\patched`, built by the test shard's own
  `Build-MapOverlay.ps1`).
- **A brand-new trainee in TazUO:**
  - the bot's client made **Iron Visionary** and played every lesson before the vision, then stopped at the standing
    stones (`isle.py --stop-at core.loop`, `runs\stopat\`). The one "failed" check there is the route's last check
    (Rook), which a stopped run never reaches;
  - TazUO logged that character in, and `VisionShots742.py` played the vision with the client's own double-clicks
    (`isle-shots742.ps1`, `vision742.json`);
  - **result** (`runs\vision\vision.log`): in the chamber at 6176,3758 (slot 0, the onlooker's tile) and hidden from
    the first second; back on its very tile 6792,3984 after 64 s, seen again; the lesson finished;
  - shots of every beat: `notes\cc-P742-review\tazuo-vision-00` to `-16`.
  - **Run 1** (`runs\vision\vision-run1.log`) did not start the vision. The bot's logout had cancelled the lesson, so
    the first double-click opened the lesson again ("You have found Watch a loop vision"), as it would for a player.
    The script now double-clicks again when nothing happens, as a player would.
  - The script's last check, a step south and back, "failed" because the first step only turned the character (they
    faced north-west from the chamber). Free movement afterward is shown by the bot instead (below) and by fact 4.
- **The bot plays the whole isle green:** **85 checks, 0 failed** (`runs-run1-console.txt`, `runs\run1\`):
  - "core.loop done" after 62 s;
  - it then walked from the stones to the dock moongate, and the gate took it beside Rook.
  The route is P741's `isle.py` (main's newest), with P740's two wake-timing lines (`../cc-P749-tools/make_isle749.py`).

**My look at the shots** (default camera):
- the room's corners are whole;
- the torches hang on the north and west walls;
- the Stranger stands in the corner at the light (02), then beside the pedestal facing the onlooker (04), and the bolt
  of the strike falls on the Gem (05);
- the burst (06), the blue cloud of the second blow (07);
- the Gem gone, shards on the pedestal and the floor (08, 09);
- the echo named for the trainee at 5,5 (11);
- the hooded figure by the north wall saying its line (13);
- back at the stones with "Lesson finished" and "Next: Getting around" (16).

## The isle-only release

- **Applies cleanly:** `git apply --check` of this whole change onto `release/isle-20261028` (`9c31000`, after P749), in a
  throwaway index: all five files apply (`release-apply-check.txt`). That covers TutorialVisionScene.cs, the two new
  chamber files and the two test files.
- **The only conflict will be `CHANGELOG.md` and `VERSION`**, as for every release pick (not in the check: added after
  it).
- **Nothing depends on the swap:**
  - the strip is void on stock Trammel too;
  - the release's FoldRegion has the same light hook;
  - the fact names Blackthorn's edge as a number (y 3804), since the release has no Blackthorn on the Fold.

## CHANGELOG

- `2026.10.31.6`, Changed: the vision takes you into a small dungeon shrine, you watch unseen as the Stranger breaks the
  Gem into shards, and you are back where you stood. VERSION `2026.10.31.6` (P735's branch uses 2026.10.31.5; the
  integrator keeps both sections).

## Deviations and decisions for Chase

- **"Build a small vision chamber somewhere players can't walk to"** is a room placed per scene, not map statics. It is
  in a void strip no one reaches, so it needs no sealing walls of land or a map patch, and it reaches the isle-only
  release without a new map.
- **"Fade to dark":** the vision's own light goes black and the screen fade is sent. TazUO draws no screen effect
  (P665's note), so in TazUO the dark is the light level. The same holds for the flash when the Gem breaks: the light
  jumps to full for a second and the burst plays, but TazUO draws no white screen.
- **Hidden, not a ghost.** The prompt allowed either. Hidden keeps their body as it is and shows them to themselves as
  the translucent onlooker; a ghost would change their body and the client's death screen.
- **The Read tool was not used on the code copy** (it was denied in the last task's unattended run). Every edit of an
  existing code file went through a small Python script that checks each replacement (`edit_scene.py`,
  `edit_tests.py`, `edit_fix1.py`). The new files were written whole.
- **The build review** (the guide's step for a new room) comes after this, from a second Golem. `notes\cc-P742-review\`
  holds what it reads.

## Files

- **Code copy:**
  - `server/customizations/Tutorial/TutorialVisionChamber.cs` (new);
  - `server/customizations/Tutorial/TutorialVisionChamberLayout.cs` (new, generated);
  - `server/customizations/Tutorial/TutorialVisionScene.cs`;
  - `server/tests/Tutorial/TutorialVisionChamberVerification.cs` (new);
  - `server/tests/Tutorial/TutorialIsleBandageWaitVerification.cs` (P721's fact);
  - `CHANGELOG.md`, `VERSION`.
- **Docs copy:**
  - `notes/cc-P742-review/`: `README.md`, `placed.md`, two renders, 17 TazUO shots and the before shot;
  - `notes/cc-P742-tools/`:
    - the room: `survey_cave.py`, `survey_dungeon.py`, `gen_chamber.py`, `render_chamber.py`, `sheet742.py`;
    - the edits: `edit_scene.py`, `edit_tests.py`, `edit_fix1.py`;
    - the tests: `probe.sh`, `mutate742.py`, `run-mutants.sh`, `mutants.txt`, `mutant-logs/`, the probe outputs,
      `gated-build.ps1`, `gated-build.log`, `green-gated-build.txt`;
    - the release check: `release-apply-check.txt`;
    - the live runs: `proof-shard.ps1`, `isle.py`, `isle-shots742.ps1`, `vision742.json`, `VisionShots742.py`,
      `Clear741.py`, `seed-on-load.txt`, `runs/` (run1, stopat, vision) and their consoles;
  - `notes/guides/building-and-decorating.md` (section 10: the chamber under "Already on our shard");
  - this note.
- **Outside the repos:** `D:\UO\golems\Iron\p742-proof\` (the shard copy, the clients, full-size shots) can be deleted.

P742 DONE
