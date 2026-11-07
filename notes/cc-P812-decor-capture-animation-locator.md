# cc-P812: staff tools: decor capture and animation locator

## In plain words

- **Staff can now save what they decorate.** Decorate a corner in game, type `[VBuild capture <name>` and click two corners. The pieces are written to a decoration file a Golem can seed or place again with `[PlaceBuild`. Each piece keeps its art, place, hue and name, and doors keep their facing. In the proof run, a small corner (a bookcase, a bench, a door and a lantern) came out as a nine-line file.
- **Staff can now see each animation of a body.** `[AnimLocate` lists our bodies. Pick one and a frozen copy stands beside you, playing every action in turn with its number over its head. `[AnimLocate target` does the same on any creature, and `[AnimLocate stop` ends it.
- **Both are staff only and change nothing for players.** The numbers (box size, pace, actions per kind of body) are in `Configuration/staff-build-tools.json`.
- **For you:** nothing is required. To see which number is the attack or the death of one of our creatures, try `[AnimLocate` on the test shard.

## What was built

All of this is in `D:\UO\golems\Iron\ShatteredLegacy`.

| File | What it is |
|---|---|
| `server/customizations/StaffBuildTools/StaffBuildToolsSettings.cs` | `Configuration/staff-build-tools.json`: written with the defaults on first start, and refused whole when wrong |
| `server/customizations/StaffBuildTools/DecorCapture.cs` | The capture: collecting the pieces, writing the `[Decorate` text, and the two-corner targeting |
| `server/customizations/ClusterFVisualBuilder.cs` | `[VBuild capture <name> [build\|world]`, one new subcommand, plus its usage and description |
| `server/customizations/StaffBuildTools/AnimLocator.cs` | `[AnimLocate`, its gump of our bodies, and the stand `AnimLocatorStand` (saved type) |
| `server/tests/Misc/StaffBuildToolsVerification.cs` | 10 facts |
| `CHANGELOG.md`, `VERSION` | `2026.11.07.6`: two Staff lines |

There is no engine change and no `.patch` file.

### Decor capture (`[VBuild capture`)

- **The format is the shard's own decoration data:** pinned's `[Decorate` text, the format of `server/data/Decoration/<Facet>/` and of P734's builds. It is one type line per kind of piece, then one `x y z` line per piece. For example:

  ```
  # p812-demo: captured by [VBuild capture on Trammel from 1987,2244 to 1992,2248 by Iron Tools at ...
  # Build form: 0 0 0 is 1987 2244 0. Put it in server/data/Decoration/Builds and use [PlaceBuild p812-demo.
  DarkWoodDoor (Facing=WestCCW)
  4 1 0
  Lantern 0x0A25
  3 3 0
  Static 0x0A99
  1 1 0
  ```

  That is the real file from the proof run, shortened here (`notes\cc-P812-shots\p812-demo.cfg`).
- **Two forms:**
  - **build** (the default): coordinates relative to the box's north-west corner, at the lower of the two targeted heights. The file goes into `server/data/Decoration/Builds` and `[PlaceBuild <name>` puts it anywhere.
  - **world**: the map's own coordinates, for a facet folder and `[Decorate` or a seeder.
- **Each piece keeps:**
  - its item ID, place, hue (`Hue=0x...`) and name (`Name=...`);
  - a door's facing. It is found by trying each facing on a probe of the same door type, and an open door is written closed where it hangs.
- **How each piece is written:**
  - an item that can be made without arguments is written as its own type (a lantern stays a lantern);
  - anything else, and every addon part, is written as a plain `Static` of the same art. The look is kept but not the behaviour, and the capture reports how many.
- **Left out:** the map's own statics (`CaptureMapStatics` false), and corpses, houses and boats, spawners, moongates and the locator's stand (`CaptureSkipTypes`).
- **Limits:** a box is at most 64 x 64 and a capture at most 4,096 pieces. Both are refused before anything is written. The name follows `[CaptureLayout`'s rule, so it can't escape the folder.
- **Where files go:** `<world folder>/decor-captures/<name>.cfg`, beside Saves, never in a repo.
- **It changes nothing in the world.** It places and deletes nothing.
- **Beside P98's `[CaptureLayout`:** that one writes the layout JSON the design generators read. This one writes what the seeders and `[PlaceBuild` read. P798 didn't mention that `[CaptureLayout` existed. I left it as it is and reused its name rule.
- **Credit:** Hammerhand's AddonGenerator through High Seas (after CEO's YAAAG) and Addon2Static (third-party, reference only). The ideas taken were capturing a box into something that can be placed again, and breaking addons into statics. No code was taken. It writes data, not generated C#.
- **Not built:** P798's sketch also had `[VBuild statify` (break a staff-placed addon into separate statics). The prompt asked only for the capture, and the capture already writes addon parts as statics, so I left `statify` out.

### Animation locator (`[AnimLocate`)

- **Commands:**

  | Command | What it does |
  |---|---|
  | `[AnimLocate` | A gump of our bodies, a page at a time (`ShardBodyTypes.Entries`: 7 pages) |
  | `[AnimLocate <body> [from]` | A stand of that body appears 2 tiles south-east of you, frozen, blessed and unable to walk |
  | `[AnimLocate target [from]` | Plays the actions on any mobile you target. Nothing is made, and it is left as it was |
  | `[AnimLocate stop` | Stops the run, and the stand goes |

- **How a run plays:** the stand plays action 0, 1, 2 and so on, one every 3 seconds. Each action's number shows over its head (`action 2`), and the staff member is told `Body 739: action 2 of 12.` When it ends, the stand goes.
- **How many actions:** this depends on the body's type, in config: Monster 22, Animal 13, Sea 13, Human and Equipment 35, Empty 22.
- **Nothing is left behind.** A stand left in a save deletes itself after load.
- **Credit:** Father Time's Freeze Frame and zerodowned's Animation Locator (third-party, reference only). The idea taken was stepping through actions on a mobile live. No code was taken.

### Rules check

- **Nothing grants anything.** These are staff tools with nothing for players.
- **All numbers are in** `staff-build-tools.json`.
- **It reaches an existing world by itself:** the commands and config arrive with the build. There is nothing to seed.
- **No engine change.**
- **Serialization (D40):** `AnimLocatorStand` uses the generator at version 0 and never outlives a load. The capture saves nothing in the world.

## Tests

- **Facts:** 10, in `StaffBuildToolsVerification`, alongside the existing Visual Builder and PlaceBuild facts (20 in all, all passing).
  - The round-trip fact writes a capture, deletes the originals, places the file elsewhere with `[PlaceBuild`'s own `Place`, and finds every piece back: the door with the same closed art, the hue and name, and the lantern as a lantern.
  - The command fact answers `[VBuild capture`'s two targets with real target objects and checks the file.
- **Red:** I wrote the facts beside the code, so to see each one fail I broke the code on purpose: 26 breaks (`mutate812.py`, results in `mutants-1.txt` and `mutants.txt`). Every fact went red at least once.
  - Three breaks went unseen at first, and each was sorted out:
    - **`noflatten`:** the explicit addon check was hidden behind the no-bare-constructor check. A test-only addon part that *can* be made bare now proves it.
    - **`lastcut` / `nolastend`:** the "end after the last action" branch was redundant (the timer's next tick ends the run at the same moment), so I removed it. I then tightened the fact to check that the last action is still playing before the stand goes; `lastcut` turns it red.
    - **`nonamecheck`:** the fact's bad-name capture used an empty box, so it failed for the wrong reason. Now the box has a piece in it.
  - One break first failed to compile and was rewritten.
- **Gated build:** `sl-modernuo:cc-p812`, 198 patches applied, **3,251 shard tests passing, `EXIT=0`**. It ran twice: green both times, the second on the final code after I added the target-driving fact. `latest` was not moved.

## Proof shots (TazUO, private proof shard 127.0.0.1:2596)

These are in `notes\cc-P812-shots\`, with the captured file `p812-demo.cfg` copied out of the proof shard's world folder.

1. `1-decorated-corner.jpg`: a bookcase (0x0A99), a bench, a dark wood door and a lantern placed with `[add` on the meadow by Britain's south road.
2. `2-captured.jpg`: `[VBuild capture p812-demo`, two corners, then "Captured 4 piece(s) (0 as plain statics) to /var/lib/uo/modernuo/decor-captures/p812-demo.cfg."
3. `3-animlocate-bodies.jpg`: the locator's gump: page 1 of 7 of our bodies, with numbers and names.
4. `4-wolf-action-0-frame-*.jpg` and `5-wolf-action-2-frame-*.jpg`: frame bursts of the leather wolf (body 739) playing actions 0 and 2, with "action 2" over its head. The journal reads "Body 739: action 0 of 12", then 1, then 2.
5. `6-stopped.jpg`: after `[AnimLocate stop`.

Every check in `walk.log` passed, except that the first two runs failed the capture. Each `[add` and capture cursor in my script was answered before the server's new cursor arrived, so only the first piece was placed and the second corner was lost. The code was fine: the new fact drives the same two targets and gets the file. Cancelling the old cursor and waiting for the new one fixed the script; the third run passed. Run 1's log is overwritten.

**Two things the shots don't show:**
- **The hue and name on a captured piece.** The script's `[set Hue … Name …` on the bookcase did not take, so the demo file has no `Hue=` line. The facts prove hue and name both ways.
- **Bodies that are ours alone (2049 and up).** They don't draw in this proof client, which starts without our custom animation file (`sl-anim7.bin is missing`, from P808's run too). The first run's shots of body 2049 show only the "action N" label. So the shots use the leather wolf, body 739: one of our listed bodies, drawn from the client's own art. The locator plays any body the same way.

## Deviations and decisions for Chase

- **The capture writes files on the shard's disk, not into a repo.** A Golem or staff member copies them into `server/data/Decoration/...`. That keeps an in-game action from touching git.
- **I didn't build `[VBuild statify`** (P798's extra), as above.
- **The proof client can't draw our own bodies** without `sl-anim7.bin`. That isn't new, but worth knowing for future animation proofs.

## Tools

These are in `notes\cc-P812-tools\`:

- `run-facts.sh`: quick fact runs.
- `mutate812.py` and `run-mutants*.sh`: the deliberate breaks.
- `gated-build.ps1`: the gated build.
- `shots.ps1`, `Shots812.py` and the TazUO rig copied from P804's.

Both locks have been released.

P812 DONE
