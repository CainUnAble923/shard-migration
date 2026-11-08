# cc-P820: fix-up for P801 (the New Haven jail) after its build review (P815) said FAIL

## In plain words

- **The New Haven jail's corner, torches and crate are fixed.** The stub of wall sticking out at the jail's front-left
  corner is gone. No torch hangs on a window any more. A standing candelabra by the warden's table now lights the hall.
  The marked crate the lesson sends you to now stands in the middle of the hall beside the bench, where you can see it
  (it was hidden behind the front wall).
- **The orange patches on the jail's roof are gone.** They were the two wall torches showing through the low edge of
  the roof. The street-side shots on both versions now show a clean roof.
- **A world that already has the jail fixes itself when the shard starts.** The old corner piece and torches are
  removed, and the crate moves to its new spot (the same crate).
- **For you:** the overseer applies `notes\cc-P820-tools\p820-release-isle-20261028.diff` to the release branch. It
  carries P801's whole jail with these fixes and replaces P801's own release diff. Nothing to decide.

## State

Iron Golem, 2026-11-08, on `golem/Iron/P820` in both work copies, not committed by me. Release copy:
`D:\UO\golems\Iron\p820-isle`, a detached worktree at `56f98af` (update 12, the release tip, with P799/P806/P814) with
the whole change staged; mine to remove after the merge. Nothing went to the release branch, nothing was deployed,
`latest` did not move, and all play was on the private proof shard, 127.0.0.1:2596.

**How P801's work got onto this branch.** The prompt says to check out `golem/Iron/P801` and merge `main` into it. The
Golem's hand-off says to stay on `golem/Iron/P820` and not merge or switch branches. I did what P814 did in the same
spot: I applied P801's whole change (`git diff main...origin/golem/Iron/P801`, `git apply -3`) to the working tree of
both copies, on top of main, and fixed it there. The Golem's commit carries P801 and the fixes together; P801's own
commit is not an ancestor of this branch. Merging P820 lands P801 too.

The apply conflicted with P802 (merged after P801 was built), all in the lesson tables. How I resolved them:

- P802's mark-and-recall travel lesson stays.
- The jail replaces the old three-stop Name Colors tour.
- The jail joins P802's switches: where the lesson points, which props it sets up, the per-tick hook, and the finish
  line. At the finish the jail still keeps the System line quiet, and P802's `Refresh` redraws its window.
- In the tours fact, the `travel.wing` and `reputation.wing` rows are both gone, because neither lesson is a stop tour
  any more.

**The last step, merging `main` again:** code `main` has not moved since I started (`a7a7a4b`). Docs `main` has gained
two commits, the P824 review notes, which touch nothing here. Per the hand-off I did not merge; the integrator's merge
brings them in.

## The four review items (P815, `review-P801.json`)

1. **The south-west corner stub (0x0034).** `notes\cc-P801-tools\gen_jail.py` now starts the south row at x = 1
   (`range(1, W)`, still skipping the door). The south-west tile keeps only the "east" piece 0x0035 (guide 2.2, 11.1),
   and `TutorialJailLayout.cs` is regenerated. On an older world the stub goes at load (see below).
2. **The torch on the west window (0x0A07 at (1,6)).** Removed rather than moved. The reviewer offered (1,7) instead,
   but item 3 called for taking the west-wall torches away and lighting the hall from a source away from the eave, so
   both west torches went.
3. **The orange patches on the roof.** They were the two wall torches. A torch is 15 high (tiledata) and hung at floor
   + 13, so its flame reached floor + 28, while the roof's west eave sits at floor + 19 on that column. The flame drew
   over the roof tiles north-west of it (guide 11.3). The hall is now lit by a standing candelabra 0x0B26 at (2,4),
   north of the warden's table and out of the camera's way. It is 15 high on the floor, under the roof's floor + 22
   there. The new street-side shots on both builds (`1-outside-door-and-sign.jpg`, `1b-at-the-door.jpg`,
   `8-outside-after.jpg` in `shots-main\` and `shots-isle\`) show no patch on the roof. P801's shots of the same view,
   with the patches, are kept in `notes\cc-P801-review\shots-main\` and `shots-isle\`.
4. **The hidden crate.** `TutorialJail.CrateSpot` is now layout (7,4), beside the bench: main 3709,2638,21, release
   3476,2601,11. That is off every window's floor tile, off the door line (x 5) and off every person's tile, as the
   reviewer suggested. In `2-hall-window-open.jpg` and `4-crate-gray-name.jpg` on both builds it stands whole in the
   hall. The walk scripts now go to (7,5) to reach it.

**An already seeded world** (`TutorialJail.Seed`, every world load, after the load):

- A `Retired` list takes away the three cc-P801 pieces the layout no longer has: 0x0034 on the south-west tile (only
  that ID; its 0x0035 stays) and the two 0x0A07 torches.
- A `TutorialJailCrate` on the old spot (9,7) moves to the new one, the same item. If a crate already stands on the new
  spot, the old one is deleted.
- A second load changes nothing.
- The load line now reads, for example, "placed 0 pieces, removed 3 old ones, moved 1 crates (cc-P820)".

The facts below prove this on an older jail. The proof shard's world (a copy of the bot world) never had the jail, so
the client runs show a fresh seed ("placed 272 pieces, removed 0 old ones, moved 0 crates" in both `shard.log`s), not
an upgrade.

## Facts

New in `server/tests/Tutorial/TutorialJailVerification.cs` (section 9):

- `TheSouthWestCornerTakesTheEastPieceOnly`.
- `NoTorchHangsOnAWindowAndNoneComesThroughTheEave`: no wall torch at all, no furnishing on any of the four window floor
  tiles, and the candelabra at (2,4).
- `TheMarkedCrateStandsInViewInTheHall`.
- `AnOlderJailIsPutRightOnLoad`: the stub, both torches and the crate on its old spot are all put right, the crate is
  the same item, and a second load changes nothing.
- `ACrateOnBothSpotsLeavesOne`.

- **Red first**, by mutants of the new code (`notes\cc-P820-tools\red\`, run by `probe-all.sh` through `probe.sh` and
  `probe-inner.sh` on `sl-uo-builder:bot`, main's latest builder):
  - P801's layout put back turns the corner, torch and load facts red (`red-old-layout.txt`).
  - The crate back in the corner turns the crate fact and both load facts red (`red-crate-in-corner.txt`).
  - No removal turns the load fact red (`red-no-retire.txt`).
  - A new crate instead of a moved one turns the load fact red too (`red-new-crate.txt`).

  P801's own code does not compile against the new facts (it has no `Retired` or `OldCrateSpot`), so the mutants are
  the real red.
- **Green:** `probe-clean.txt`, 68 of 68 (the jail, tutorial and trade-trial facts on main's builder).
- **Gated builds** (the docker\uo build script via `both-builds.ps1` and `isle-build.ps1`, under the `docker-build`
  lock):
  - Main `sl-modernuo:cc-p820`: **EXIT=0, 3318 shard tests passing** (`gated-build.log`).
  - Release `sl-modernuo:cc-p820-isle`: **EXIT=0, 2996 passing** (`gated-build-isle.log`), built from `56f98af` with
    the diff.
  - The first release build failed (`gated-build-isle.run1.log`). P801's old release diff, written before update 12,
    added `PlayerMobile-private-mobile.patch` and its `IPrivateMobile` interface. Update 12 already has both (from
    P799), so the patch was applied twice and the interface defined twice. Both duplicates are dropped; the release's
    `TutorialJail.cs` is now the same file as main's.

## The release diff

`notes\cc-P820-tools\p820-release-isle-20261028.diff` (13 files) carries P801's jail with these fixes, made against
update 12 (`56f98af`). `git apply --check` passes on the release branch's own checkout. **It replaces
`notes\cc-P801-tools\p801-release-isle-20261028.diff`,** which no longer applies cleanly to update 12: it conflicts in
the lesson tables and duplicates the private-mobile patch. P801's changelog line had also landed inside the
changelog's comment block on the release. Both copies now have one entry, `2026.11.08.1`, with the jail line and a
Fixed line for these items. `VERSION` is 2026.11.08.1 in both.

## Proof in TazUO

Both builds were walked by a fresh Player-account character, each on a fresh copy of the bot world on the private
proof shard (`run820.ps1`). The walk kit is P801's, copied to `notes\cc-P820-tools\` with the crate leg moved. The
character walked in through the real door, met the five people, took from the crate and put the pouch back, read the
ledger, called the guards and walked out. `walk-main.log` and `walk-isle.log`: **23 PASS, 0 FAIL each.**

What is in `notes\cc-P820-review\`:

- `shots-main\` and `shots-isle\`: the shots from both walks.
- `sheet-main.jpg` and `sheet-isle.jpg`: contact sheets.
- `sw-corner-before-after-main.jpg`: P801's hall shot beside the new one, at the south-west corner.
- `render-sos-after*.jpg` and `render-stock-after*.jpg`: the isorenders, roof on and off, with the crate and ledger
  drawn in at their server spots.
- `placed.md`: every piece on both plots, plus what an older world loses at load.

Seen in the shots, not part of this fix: after the walk attacks Mirren (to show she takes no harm), TazUO leaves its
own "This may flag you criminal" box open in the later shots. That is the client's own warning, and it was there in
P801's run too.

## Files

- Code copy: P801's 13 files (merged with main as above). From this task: `TutorialJail.cs` (CrateSpot, OldCrateSpot,
  Retired, the load pass), `TutorialJailLayout.cs` (regenerated), `TutorialJailVerification.cs` (section 9),
  `CHANGELOG.md` and `VERSION`.
- Release copy `D:\UO\golems\Iron\p820-isle`: the same, against update 12.
- Docs copy:
  - P801's notes, review folder and tools, applied as above.
  - `notes\cc-P801-tools\gen_jail.py`: the fix, plus the crate and ledger drawn into the mock.
  - `notes\cc-P820-review\`.
  - `notes\cc-P820-tools\`: probes, mutants, build scripts and logs, the walk kit and its logs, `make_placed.py`, and
    the release diff.
  - This file.

P820 DONE
