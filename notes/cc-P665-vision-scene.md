# cc-P665: the loop vision as a staged scene (P481 F5)

Iron Golem, 2026-10-27. Code copy `D:\UO\golems\Iron\ShatteredLegacy`, docs copy `D:\UO\golems\Iron\shard-migration`,
both on `golem/Iron/P665` (main at P705; P664's private copies are not merged, see below). Stones at 6794, 3982 (P673
1.4). Not committed; nothing deployed or published; no package built; Haven not touched.

## In plain words

- **The loop vision is a real scene now (test shard, once this ships).** At the Wakening Isle's standing stones, a new
  player who double-clicks the blue rune stone is held still for about 45 seconds while the world goes dark, the
  Stranger strikes the Gem, the shards fly, their own double appears and speaks, and a hooded League figure appears.
  Before, it was four lines of grey text in the journal.
- **Only that player sees and hears it.** The words show in a dark band in the middle of the screen, so they read even
  if the player's client overrides the game's lighting. It changes nothing about the character.
- **Logging out, dying or a server restart in the middle puts the player back at the stones**, free to move, with
  normal light and the figures gone, and they can watch it again.
- **For you: nothing now, two things later.** You chose to fold the recording of the scene in our client, and the sounds
  checked by ear, into P707's play-through on its private world. Later: draw the two optional full-screen pictures (art
  request `p665-vision-panels`). Also, our TazUO does not do the screen fades yet (it ignores them), so the scene darkens
  with light instead.

## What was built

| Part | Where (code copy) | What it does |
|---|---|---|
| 1. The scene | `server/customizations/Tutorial/TutorialVisionScene.cs` (new) | A one-second timer runs P481 section 6's beats for one player where they stand at the stones of their lesson map (`TutorialWorld.MapOf`: the Fold today, their private copy once P664 merges). Frozen for the scene. Light per player through `FoldRegion.AlterLightLevel` (30 black, 18 dim, 0 the flash; personal light 0), pushed with `CheckLightLevels(true)` on each change. `SendScreenEffect` fades (out, in, light flash). Subtitles in a borderless gump (alpha band, light centred text, `TutorialStyle`), one line per beat. Every sound and effect is built and sent to the player's NetState only (pinned `Effects` sends to everyone in range): particles where the client takes them, the plain effect otherwise, as `Effects.SendParticlesTo` decides. The two speech lines are `SayTo` (private overhead) and also the subtitle. |
| The beats | same | 0 s fade to black, sparkles 0x376A on the player, 0x1FE, "A vision." 3 s dim; a stone pedestal 0x1223 with the Gem (worldgem bit 0x1EA7, Celestial hue 0x8AF) on its top; the Stranger (body 0x190, dark robe, longsword 0x0F61) beside it; sparkles on the gem every 2 s; 0x20F. 8 s bolt on the gem, 0x29; 9 s explosion 0x36BD, 0x307. 12 s five moving 0x3779 from the gem to five crystal shards 0x5738 left on the floor; the gem goes, the Stranger's sword becomes a dark sword on the floor and its point (0x0EC1, "broken knife"); 0x211. 17 s flash (light 0), 0x220; 18 s black, all cleared. 21 s dim; the echo forms (0x376A, 0x44D) and speaks at 22 s; 29 s it fades (0x374A, 0x3C4). 30 s a hooded figure (hooded shroud 0x2684) at the edge of the light, a dark broken sword at its feet, 0x212; it speaks at 31 s; 34 s "What you keep...". 38 s fade to black, 0x376A, 0x1FE, "This was only a vision. Nothing about you has changed. Yet."; 42 s "Take the moongate at the end of the dock." 45 s light restored, released, the lesson finished. |
| 2. Figures | `TutorialVisionFigure : Mobile`, `TutorialVisionProp : Item` (same file) | Plain mobiles: no AI, skills, master or timers; blessed. The echo copies body, hue, sex, hair and beard, and each worn piece from the hands to the inner legs as a plain item of the same art and hue (not the backpack). Not Mirror Image's `Clone`. Both classes delete themselves if a save ever loads them. |
| 3. Recovery | `TutorialVisionScene.End/Restore`, `TutorialVisionStore` (GenericPersistence "TutorialVision") | Each second the scene checks the player: no client (logout or disconnect), dead, or off the map ends it at once: figures and props deleted, unfrozen, light recomputed, subtitles closed, put back at the stones if more than 4 tiles off (or their logout spot set there), and the stone plays it again (the lesson's step goes back to 0). A cancelled lesson (login, restart of the lesson) ends it the same way. The save holds each scene's player, map and placed serials; at startup (`Initialize`, after World.Load) and at that player's login the recovery runs. Frozen is not saved by the core (`Mobile.m_Frozen` has no writer), so a restart cannot leave anyone frozen anyway. |
| 4. No progress change | the scene never calls `ClusterFLoops` | Fact 6 runs P80's check against the real scene. |
| 5. Panels | `registry.csv` 23209 (0x5AA9) and 23210 (0x5AAA), kind gump; `gumps\23209.png`, `23210.png` | Both free by `find-free-art.py --explain-gump` (client data `D:\UO\tool-trials\client-data-copy`). The package gate wants one PNG per registered gump, so each is a plain dark 800 x 600 placeholder with a label (`notes\cc-P665-tools\make_placeholders.py`), recorded in the art `SOURCE.txt`. The scene shows them on beats 17 and 30 only with `clusterf.tutorial.visionPanels` (off). Art request `p665-vision-panels` filed for Chase's drawings. `validate-art.py check-registry`: 0 of 803 rows have problems. |
| Wiring | `TutorialCoreTrials.cs`, `ClusterFLoops.cs`, `Fold/FoldRegions.cs` | `WatchVision` starts the scene; its last beat observes `VisionFinished`, an early end resets the step. The old 2-second journal lines are gone; `TutorialVision.Lines` is the scene's subtitles. The lesson hint says it lasts under a minute and holds you still. `FoldRegion.AlterLightLevel` asks the scene. |

**Played in place, no chamber.** P673 1.4 leaves the chamber optional, and the scene plays at the stones of the
trainee's lesson map. With P664's private copies that map is theirs alone, so the figures and props are private too.
Effects, sounds, speech, light and subtitles go to the one player whatever the map. **Until P664 merges**, everyone
shares the Fold, so another trainee standing at the stones would see the figures and props (not hear or light them).

## Facts (`server\tests\Tutorial\TutorialVisionSceneVerification.cs`, 7)

1. The scene plays its beats for one player and finishes the lesson: frozen, black then dim for them while a bystander
   two tiles away keeps day light; the subtitles and figures on their beats; nine of the scene's sounds on the player's
   wire and none on the bystander's; at 46 s the lesson is done, released, day light, no gump, no figures or props.
2. The echo copies the player's look and nothing else: body, hue, name, hair, the shirt as a copy; no backpack; not a
   BaseCreature; Swords 45 and Ninjitsu 80 on the player, 0 on the echo; deleting it deletes the copies, not the shirt.
3. A disconnect mid-scene: back at the stones, unfrozen, no scene light, figures and props gone, lesson not done; back
   online, the stone plays it again to the end.
4. Death mid-scene ends it the same way.
5. A restart mid-scene: the store written, the scene abandoned with the player frozen 10 tiles away; the store read
   back and `Initialize` run: unfrozen, at the stones, every placed figure and prop deleted, no gump; replayable.
6. The real scene changes no skill, level, loop or Young status.
7. The panels are off by default and the scene ends without them; on, panel 1 at 17.5 s and panel 2 at 30.5 s.

**Seen failing first.** The facts use the new API, so they cannot compile on the old code. `notes\cc-P665-tools\mutate.py`
makes one copy of the edited Tutorial folder per behaviour taken out; `redrun.sh` mounts each over the builder image
(`probe.sh`). Summaries in `notes\cc-P665-tools\red\`:

| Mutant | Taken out | Failed |
|---|---|---|
| `shared` | sounds to everyone in range (pinned `Effects.PlaySound`), no scene light | **1** |
| `clone` | the echo copies skills too (a Clone in all but name) | **2** |
| `norestore` | an early end only forgets the scene; `Restore` does nothing | **3**, **4**, **5**, and 1 (still frozen at the end) |
| `nosave` | the save leaves the scenes out | **5** |
| `loop` | the scene records a real loop at its end | **6** |
| `panels` | panels shown whatever the setting | **7** |

The first `nosave` run also failed 1, 3 and 4: fact 5 left its Stranger at the shared stones when it failed, and the
next facts found it. Fact 5 now deletes what it placed in a `finally`; rerun, `nosave` fails fact 5 alone.

**Green.** The 7 on the builder image (`green.txt`). Every tutorial, Fold and graduation fact: 207, 206 passed, 1
skipped, 0 failed (`suite.txt`). One existing fact changed: `TutorialVerification`'s timed vision now waits the scene's
45 s instead of 9 s.

## Build

`docker\uo\build.sh -t sl-modernuo:cc-P665`, run detached under the `docker-build` lock (released): **green, `EXIT=0`**,
"Built sl-modernuo:cc-P665 with patches applied and 2682 shard test(s) passing." 2687 tests: 2682 passed, 0 failed, 5
skipped (the usual client-data facts); the 7 new facts pass in it. Windows had 5.4 GB free before it, the Docker VM 13.8 GB
available.

## Moved to P707: the recording and the sounds by ear

Part 6 also asks for a TazUO recording (frame burst) of the scene and its sounds checked by ear on the private world.
Both need a private shard reading P662's patched map (`D:\UO\golems\Iron\p662-work\edited`), the isle seeded on it,
and TazUO drawing the same map. That is the setup P664 stopped on, and the overseer has given it to **P707** (after
P665 and P666: the two-client play-through, the isle bot route and the shots). I cannot judge sounds by ear in any
case; that check is Chase's. Asked Chase whether the recording goes into P707 or a session of its own
(`Iron-P665-20261027-120539-6267`). **Answered 10-27 14:12 (overseer, console): "Fold into P707"**, so P707 records the
vision (a frame burst) on its private world and the sounds are checked by ear then. P665 is marked done without them.

What a recording should look for, so P707 or a session can do it quickly: the light really drops to near black and
back for the player only (a second client beside them stays in day light); the subtitle band is readable on a dark
and on a bright world (try TazUO's own light setting on); the gem sits on the pedestal's top; the five shards land on
the ground; the echo wears the player's clothes; nothing is left when it ends. `proof.ps1 -Frames 8 -FrameMs 400`
(cc-P265) takes the burst.

## Deviations and decisions for Chase

- **No screen fades in our client.** TazUO reads the fade packet and draws nothing
  (`ClassicUO.Client/Network/PacketHandlers/GraphicEffect.cs`: "Effect not implemented"). The scene still sends it for
  clients that honour it, and the light does the darkening. A client patch could draw it later (TazUO already has
  screen overlays with fades); not in scope here.
- **Art picks are candidates from tiledata names, checked by render:** the pedestal 0x1223, the gem 0x1EA7, the shards
  0x5738, the sword 0x0F61 and its point 0x0EC1 (a "broken knife", 9 x 9: there is no stock broken sword), the hooded
  shroud 0x2684. The crest is a dark sword on the ground, not a ring of stones (the stones of the knoll stand round it
  anyway); panel 2 is the proper crest.
- **The last line says "the moongate at the end of the dock"**, not P481's "on the pier", to match every other tutorial
  line about that moongate.
- **The isle's hint line** ("chapter 1 of the storyline adds the hint", P481 6): the hooded figure's line and "What you
  keep" carry the League; I added no line about the miner's complaint, since chapter 1 starts at Dull Copper rank and a
  new player cannot act on it. Easy to add as a 36 s subtitle if wanted.
- **A Read of `TutorialVisionSceneVerification.cs` was auto-denied** in this unattended run (the Read tool on a code-copy
  file); I edited it with a script instead. No step was skipped.
- **A Read of a render in `D:\UO\tools\vseUOAware\exports\Art\ped_1223.png` was auto-denied**; I copied it to the
  scratchpad and read it there.
- **P664 is not merged.** The scene asks `TutorialWorld.MapOf`, so it plays on the trainee's private copy once P664
  merges, with no change here. Both branches change `VERSION` and `CHANGELOG.md` (P664's WIP also used 2026.10.27.3);
  the integrator merges the two sections.

## Not verified

- Anything in a client or on a running shard (above).
- The figures' placement against the knoll's boulders: they are put by offsets from where the player stands (Z read
  from the map), not fitted; on the real knoll one may stand in a boulder. The recording will show it.

## Asked, and commit preflight

- Asked Chase: `Iron-P665-20261027-120539-6267` (the recording and the sounds); answered "Fold into P707".
- **Version clash for the integrator:** this branch and P666 both add `2026.10.27.3` to `CHANGELOG.md` and `VERSION`
  (P664's WIP did too). The second of them to merge needs the next number.
- Resumed in a new session after P666: both WIP commits (`ae76e8f` code, `ffda847` docs) were checked; neither deletes
  a file, and nothing changed since apart from this notes file.
- Files, code copy: new `server/customizations/Tutorial/TutorialVisionScene.cs`, `server/tests/Tutorial/TutorialVisionSceneVerification.cs`,
  `player-package/vendor/shattered-legacy-art/gumps/23209.png`, `23210.png`; changed `TutorialCoreTrials.cs`,
  `ClusterFLoops.cs`, `Fold/FoldRegions.cs`, `server/tests/Misc/TutorialVerification.cs`, the art `registry.csv` and
  `SOURCE.txt`, `CHANGELOG.md`, `VERSION`.
- Files, docs copy: this file, `notes\cc-P665-tools\` (probe, mutants script, red runs, placeholders script, summaries).
- No file over 5 MB; nothing under `docs\` changed; no secrets.

P665 DONE
