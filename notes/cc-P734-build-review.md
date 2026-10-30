# cc-P734: a building and decorating guide, and a render review before build work merges

Iron Golem, 2026-10-29.

## In plain words

- **A building guide every build task reads.** `notes\guides\building-and-decorating.md` turns your isle corrections
  (roofless boxes, doors outside walls, the too-high bridge, stepped shores, rune markers, Pip never placed) into
  rules, adds how real UO houses are put together (read from OSI's own house files: which corner gets the post, which
  way each stair climbs, where the roof sits) and what human decorators do, and lists which art fits a farm, beach,
  dock, bank, guild hall, market, shrine, garden, dungeon entrance or tropical isle.
- **A second Golem checks build work before it merges.** When a task places buildings, decoration or map pieces, the
  merge Golem now holds it and queues a short review for Gold or Copper (never the Golem that built it). The reviewer
  looks at the pictures and either passes it or sends a numbered list of fixes back as a fix-up. You will see review
  tasks (`cc-P<n>-review-build-...`) in the queue. A review left unanswered for 8 hours stops holding the merge.
- **Six practice buildings, built by the guide and reviewed.** A farmhouse, a bank, a League lodge, a bridge and
  pier on a lake, a market corner and a two-story house stood on a private test shard (The Fold: Green Acres, and a
  lake at 1550,612), each walked with a real character and passed by the reviewer on its third round.
  The gallery is `notes\cc-P734-practice\gallery.md`. Any of them can be placed again with `[PlaceBuild practice-bank`
  (and the others) on a test shard.
- **For you:** nothing to decide for the step to start working; it is live in the Golem kit now. Two things to
  look at when you can:
  - **The CHANGELOG line could not be written.** The unattended run would not let me read `CHANGELOG.md`; the line
    is under "Deviations" below, ready to paste.
  - **The review found three things the isle itself may have wrong:**
    - the chairs (0x0B4E/0x0B4F, by the art they face east and south);
    - the bank's sign arm 0x0B97, which lies along the wall instead of sticking out;
    - the lodge's west-wall bookcases 0x0A97, which face south and stand edge-on.

    Worth a glance in your next isle walk; they are listed for a follow-up prompt.

## What changed

### 1. The guide (`notes\guides\building-and-decorating.md`)

Sections: a short checklist; buildings (whole multis at one Z, walls and corners, roofs, doors, windows, signs,
furnishing, nothing stray); facing; heights (walkable joins, stairs, docks); land; markers and props; lessons and the
existing world; proof (tools and what a build prompt leaves); learned from human builders (with links and 15 example
layouts); What to use where (ten kinds of place); lessons from the practice builds.

Sources:

- **Chase's corrections:** P718, P720, P721 (its notes from `golem/Iron/P721`, commit 5bc43a8), P724, P725, P726,
  P728 and P732 prompts and notes, and `D:\UO\overseer\decisions-2026-10-23.md` (10-27 and 10-28). A subagent read
  them and wrote a 27-item digest; every rule in the guide names its correction.
- **OSI's house multis**, read from `MultiCollection.uop` in `D:\UO\tool-trials\client-data-copy` by scripts in
  `notes\cc-P734-tools\` (outputs beside them):
  - `stair_survey.py` -> `stair-survey.txt`: in every classic house the **post stands at the north-west** corner and
    the **L corner at the south-east**; the "south" piece runs the north and south rows, the "east" piece the west and
    east columns. This contradicts the brief's guess ("corner at the NW") and agrees with RunUO's names `SECorner` and
    `NWCornerPost` and with `notes\uo-wall-orientation.md`. A step named for a direction **climbs toward** it (every
    "north" step has the next one 5 higher to its north).
  - `roof_survey.py` -> `roof-survey.txt`: in all 8 small houses the lowest roof course is at **wall Z + 20** over
    **x0+1..x1+1, y0+1..y1+1**, and the floor lies under the **south row and east column** only.
  - `window_survey.py` -> `window-survey.txt`: which window piece stands in an east-west wall and which in a
    north-south one, per material.
  - Tiledata (read with `scripts\mapbuild\uofiles.py`): steps 5 high, blocks 10, walls 20, roofs 3.
- **Human builders (part 1b):** a subagent researched with WebSearch and WebFetch only. **Stratics did not answer**:
  uo.stratics.com, uo2.stratics.com, community.stratics.com, forum.uo.com, forums.uo.com, uoex.net and MassivelyOP all
  returned 403, and the Wayback Machine was refused; their threads appear only as search snippets, marked [snippet].
  The precise material came from the data the in-game house tool uses (ServUO `Data/Components/walls|stairs|roof|
  floors.txt`), RunUO's wall scripts and OSI town decoration files, uo.com's decorating articles, UOGuide, uotavern and
  a player blog. Every claim in section 9 carries its link; no images were copied.
- **Art library (part 1c):** a subagent read `D:\UO\third-party\ART-LIBRARY.md` and 139 of the pack folders (read
  only), tagging each pack "server addon from stock art (usable now)" (37: `.cs`, `.uoa` or multi `.txt` only) or
  "needs new client art", with each pack's terms from its `SOURCE.txt`, and a "do not use here" list per place (for
  the tropical isle: the savanna, autumn and temperate trees, snow and Christmas packs, purple grass, hallow-trees).
  Terms needing care are listed there (`drc1k-uoassets`, packs with no `SOURCE.txt`, art ripped from other games).

### 2. The review step (Golem kit, `D:\UO\golem`)

`Golems.ps1` (cc-P734 section after `New-FixupPrompt`), wired into `Invoke-Integrate`:

- **Which tickets:** the prompt Touches `map`, or the branch changes a path that is placement work: `.mapops`,
  `server/data/Decoration/` (and so the saved builds), anything named addon, decor, statics or mapops,
  `scripts/mapbuild/`, or an isle or tutorial seed, place, build or spawn file. Notes, testing output, server tests and
  client art files are not (`Test-BuildReviewFiles`).
- **Queue:** the first time such a ticket comes up, the integrator writes `queue\cc-P<n>-review-build-<slug>.md`
  (Touches docs-only, Model Opus) with `**Golem:** Gold, Copper` (settings `buildReviewFirst`), never the builder; if
  neither can take it, every other enabled Claude Golem that may take docs-only. It records
  `merge-queue\review-P<nn>.json` and holds the ticket (result `review` on the merge card).
- **The review prompt** tells the reviewer to read the guide, fetch the branch without switching (`git fetch`,
  `git archive ... notes/cc-P<nn>-review | tar -x`), read `placed.md`, the renders, shots and diff, check every wall,
  corner, door, stair, wall-mounted item, roof, sign, height and piece choice one by one, in 45 minutes, and write
  `BUILD REVIEW P<nn>: PASS` or `FAIL` and a numbered list in its notes. A missing review folder is a FAIL.
- **Verdict:** when the review's own branch is ticketed, the integrator reads that line from the review's notes on
  the branch (`git show`), records it, and merges the review's notes. Review tickets go first in a round, so a PASS
  merges the build in the same round.
- **FAIL** becomes a fix-up for the builder (`New-FixupPrompt -Review`: the reviewer's list, read the guide, fix each
  item, new shots and placed list, one more review), exactly like a merge conflict: the head is marked handled, the
  ticket removed, and a fix-up's own FAIL goes to Chase (NEEDS YOU), as a fix-up's conflict does. A Codex lane's FAIL
  is Chase's too.
- **Kept light:** one review per prompt; after `buildReviewWidenMinutes` (60) unclaimed the review is opened to every
  other Claude Golem; after `buildReviewHours` (8) with no verdict the ticket merges and the log says so.
- **Skip:** `Skip-BuildReview.ps1 -Prompt <nn> [-Reason ...]` (new, writes `merge-queue\review-skip-P<nn>`), or a
  `**Build review:** skip` line in the prompt; `settings.json` `buildReview: false` turns the step off.
- **Golem lines with several names:** `Test-PromptForGolem` lets `**Golem:** Gold, Copper` mean either; the claim and
  the marathon queue count use it (`Golems.ps1` `Get-ClaimCandidate`, `golem.ps1` queue-low count).

### 3. Templates

There is no prompt template file (searched `D:\UO\overseer`, `D:\UO\cc-prompts` and the overseer's memory): the text
every session gets is the Golem's hand-off, and the integrator's fix-up text. Both now name the guide:

- `golem.ps1` `Get-BuildHandOffText`: a prompt that Touches map, or speaks of decoration, addons, mapops or statics,
  is told to read the guide and its What to use where section first and to leave renders, off-screen shots and
  `placed.md` in `notes\cc-P<nn>-review\`.
- `New-FixupPrompt`: a fix-up of map work (Touches map, or a review's FAIL) carries a **Read first** line for the guide.

### 4. Practice builds

- **The placer:** `server\customizations\Builds\PlaceBuild.cs` (new): `[PlaceBuild <name> [x y z] [dryrun]`,
  `[ClearBuild <name> x y z [dryrun]`, `[ListBuilds`. A build is a decoration file in pinned's own `[Decorate` format
  with coordinates relative to its north-west corner, placed through pinned's `DecorationList` (doors link, names and
  facings work, placing again skips what is there). The six builds are
  `server\data\Decoration\Builds\practice-{farmhouse,bank,lodge,dock,market,twostory}.cfg`. They ship inside the
  `Decoration` folder the image already copies (the Dockerfile could not be read in this unattended run, see below);
  `[Decorate` reads only its facet subfolders there, so it never places them. `tools\tests\test_sos_fences.py` skips
  `Builds` (relative coordinates) in its glob of every decoration file.
- **The builds:** `notes\cc-P734-tools\gen_builds.py` lays them by the guide's rules, reading every wall, window, roof
  and gable piece from an OSI multi of that material (the light wood cottage 0x006E, the stone shop 0x00A0, the brick
  house 0x0074, the plaster house 0x006C); it writes the `.cfg`, `notes\cc-P734-review\placed-<build>.md` and the
  isorender previews and cut-aways. First renders caught two wrong kits (the stone shop's front row is arches; 0x0074
  and 0x0076 pitch their roofs along x), fixed before anything was placed.
- **The plot:** The Fold (map 32, Trammel's files, its own items), Green Acres, x 5700-5779, y 1170-1224: flat grass
  at Z 0 with no statics on this branch's SoS overlay (`plot_scan.py`). The dock is on a real lake on The Fold at
  1550,612 (round 1 tried a pond of water statics on the plot; they block nothing).
- **In game:** `sl-modernuo:cc-P734` on a private shard (port 2596, `proof-shard.ps1`, the bot world copied, this
  branch's map overlay). The Admin placed all six (`place.json`: 147, 188, 251, 177, 162 and 219 pieces).
- **Walked, shot, reviewed until PASS:**
  - A real character (TazUO, the client's own steps) walked every door, the gate, the stair, the bridge and the pier
    both ways: logs in `notes\cc-P734-review\walks\`. Stair Z 2, 7, 12, 17 and 20 at the landing, and back down.
    Bridge Z 1 → 2 → 1 both ways. Pier Z 6 → 6 both ways.
  - 19 TazUO shots from the default camera are in `notes\cc-P734-review\shots\`; renders and cut-aways are beside
    them.
  - Three review rounds by a fresh second Claude each time, all six PASS in round 3. The rounds' files are
    `review-round-1/2/3.md`, and the gallery has the table.
- **Fixes the reviews drove:** one wall rule bug (the south-west corner), facings read from the art (chairs, carpet
  edges and corners, sign arm, west-wall bookcase, the fence's L corner), hearths moved out from under low roof and
  floor, windows cleared of furniture. The dock moved from a fake pond to a real lake (water statics on grass blocked
  nothing), and its bridge start moved onto flat bank (the edge tile is a steep slope the walker could not cross).
- **Not re-walked after round 3's re-placement:** the bank and lodge doors (their door tiles did not change; the
  reviewer took the round-2 logs as still valid); the farmhouse was walked again.
- **The image** `sl-modernuo:cc-P734` holds the round-1 build files. The private shard read the final ones from a
  mounted folder (setting `clusterf.builds.folder`), byte-identical to the repo's. The final files need no new build:
  no fact parses them.

## Tests

- **Golem facts (new, six, `D:\UO\golem\tests\Golem.Tests.ps1`, `-Only P734`):** the review rules (a Golem line
  with several names; Gold and Copper first, never the builder, no Codex lane, script or console-only Golem; which
  paths need a review; the verdict line and its numbered list); a map prompt waits for its review and merges on PASS in
  the same round as the review's own branch, and no second review is queued while it waits; a FAIL becomes a fix-up
  for the builder carrying the list, reading the guide, nothing on main, the head handled; the overseer's skip (the
  marker, `Skip-BuildReview.ps1`, the prompt line) and the 8-hour time-out; an unclaimed review opened to every other
  Claude Golem after an hour, and `buildReview: false`; a map prompt's hand-off names the guide and the review folder,
  another prompt's does not.
  - **Red first:** against the live kit before the change, 1 check passed and 13 failed
    (`notes\cc-P734-tools\red-golem-p734.txt`).
  - **Green:** against the scratch kit, then against the installed live kit: 31 checks, 0 failed
    (`notes\cc-P734-tools\green-golem-p734-live.txt`).
- **The whole Golem suite on the changed kit** (`notes\cc-P734-tools\golem-suites-summary.txt`): Golem.Tests 1634
  passed, 5 failed; Lane 65/0; Codex 161/0; Tinker 199/0; RemoteAgent 90/0; GolemPower 133/0; Assign, CommitShardWork,
  GolemDays, LegionScript, UoFiles all green. **The 5 Golem failures are the same 5 on the unchanged live kit**
  (P184's Touches-guessing and overlap facts, run with `-Only P184` against `D:\UO\golem\golem.ps1` before install:
  102 passed, the same 5 failed), so they predate this prompt. GolemPaths (1), Join (4), GolemTestAccounts and
  Move-ToGolem ran against the live kit's own files, which this prompt does not change; their failures are this PC's
  state (Docker was down when they ran, the overseer folder layout, `golem` account ownership), not this change.
- **Server facts (new, `server\tests\Misc\PlaceBuildVerification.cs`, 3):** Shift moves only coordinate lines; placing
  puts each piece at origin + offset (a named signpost, a WestCCW door with closed art 0x06A9) and placing again places
  nothing; ClearBuild removes exactly the build's pieces and leaves a movable item on the tile.
  - **Red first:** the gated build with `PlaceBuild.cs` moved aside failed to compile the facts
    (`notes\cc-P734-tools\red-placebuild-test.txt`, CS0103 `PlaceBuild` does not exist).
  - **Green:** `docker\uo\build.sh -t sl-modernuo:cc-P734`: 2821 shard tests passing, including the three facts and
    `CommandDeclarationVerification` (the three new commands declare their kind, dry run and re-run)
    (`notes\cc-P734-tools\green-gated-build.txt`). Free memory before the build: about 1.2 GB available on Windows,
    14 GB free in the Docker VM; it ran detached under the docker-build lock.
- **Python tests:** `tools\tests\test_sos_fences.py` changed (skips `Decoration\Builds`); it is skipped on this PC
  without `SL_SOS_MAP`, as before, so the change is untested here.

## Deviations and decisions for Chase

- **CHANGELOG line not written.** The unattended run denied reading `D:\UO\golems\Iron\ShatteredLegacy\CHANGELOG.md`
  (the Edit tool needs a read first), and I did not work round it. The line I wanted under `## 2026.10.29`, in a new
  `### Staff` list:
  `- Building work now gets a second look before it reaches the shard: every task that places buildings, decoration or map pieces follows one building and decorating guide, and a second Golem checks its pictures (walls, corners, doors, stairs and what hangs on walls) and passes it or sends back a numbered list of fixes before it is merged. [PlaceBuild <name> places a saved build anywhere (six practice builds ship: farmhouse, bank, lodge, dock, market, two-story house); [ClearBuild removes one; [ListBuilds lists them.`
- **Dockerfile not read.** Reading `docker\uo\Dockerfile` was denied the same way. I wanted to add
  `COPY server/data/Builds/ .../Data/ShatteredLegacy/Builds/`; instead the builds live in `server/data/Decoration/Builds`,
  which the existing `COPY server/data/Decoration/` line already ships (the green build placed them from there).
- **Low memory:** Claude Code stopped four of my idle wait loops for low memory (only waits, no work); the shot,
  walk and build runs were detached and finished. I did not restart the stopped waits.
- **Follow-ups (not done here):**
  - Check the isle's chairs, bank sign arm 0x0B97 and lodge west bookcases 0x0A97 against the review's art findings
    (guide 2.5 and 3).
  - Optionally add the guide's carpet and facing corrections to P720's isle layout.
  - Client-art ideas for the practice places are in the gallery.
- **Shots read from the repo copy.** Reading a shot in `D:\UO\golems\Iron\p734-proof\shots` was denied; the shots are
  copied into `notes\cc-P734-review\shots\` (where the reviewer reads them anyway) and read there.
- **Docker Desktop was not running** on this PC when the practice started (no process; the Tinker's log shows only the
  laptops' Docker failures). I started it (`Docker Desktop.exe`). Memory was tight all session: about 0.7 to 1.2 GB
  available of 32 GB, 76 GB committed, with the Docker VM itself mostly free; builds ran detached.
- **This branch will itself be held for a build review** once the new kit is live: it adds `server/data/Decoration/
  Builds` and an addon-free placer. Its review folder is `notes\cc-P734-review\` (placed lists, renders, shots, walks
  and the practice reviews), so a reviewer has what it needs; or skip it with `Skip-BuildReview.ps1 -Prompt 734`.

P734 DONE
