# cc-P64: In-game patch history page, wrapped lines, no wiki button

Builder in `D:\ShatteredLegacy`, 2026-10-05. Brief: `D:\UO\cc-prompts\cc-P64-patch-history-gump.md`.
Not committed, not deployed, `sl-modernuo:latest` not moved, wiki not published.

## Headlines

- **`[version` now opens a Patch History gump**: every version in `CHANGELOG.md`, newest first, paged with
  Previous / Next and "Page N of M". Each version has its heading ("Shattered Legacy 2026.10.05.3"), its date on the
  right ("October 5, 2026"), and its Added / Changed / Fixed lists. The version the server runs is gold with a green
  "(you are here)" beside it.
- **No line is cut any more (D87).** Every patch line, in the history and in the login bulletin, is its own HTML block
  as tall as its words wrap to, measured with the client's font widths (`ClusterFGumpText`, the cc-P57 table). The
  D87 line takes 4 rows in the history and 5 in the bulletin.
- **The bulletin's wiki button is gone.** "Full notes (opens the wiki in your browser)" is now **"All patch notes"**,
  which opens the history; "... and N more in the full notes." is now "... and N more (All patch notes)". Opening the
  history from the bulletin marks the notes seen, as every bulletin button already did.
- **Staff see the `### Staff` list** in the history, in lavender under "Staff (players do not see this list)". Players
  never see it; the bulletin and the wiki page still leave it out.
- Build: `sl-modernuo:cc-p64`, **876 shard tests passing** (872 before plus 4 new facts). Red was watched for all four
  new facts (details below).

## What changed

`D:\ShatteredLegacy`:

- `server/customizations/PatchHistoryGump.cs` (new, 277 lines): the gump. Rows built at `:161`, pages at `:212`, item
  height at `:156`, staff check at `:55`, Previous / Next at `:259`.
- `server/customizations/ShardVersion.cs`: `PatchNoteVersion.Staff` (`:47`) and `Date` (`:50`); the parser fills Staff
  from `### Staff` (`:134`), which it used to drop. `Sections()` is unchanged (Added, Changed, Fixed), so the bulletin,
  the wiki page and status.json are unchanged. `[version` says the version as before and then opens the history
  (`:349`), also when the current version has no notes. Header comment updated.
- `server/customizations/ClusterFBulletin.cs` (`BulletinGump`): `FullNotesButton` is `AllNotesButton` (same ID 2,
  `:378`); note lines are measured blocks (`:414`, `NoteHeight` `:516`) shown whole while they fit in 180 pixels
  (`MaxNotesHeight`, `:379`); the rest are counted in "... and N more (All patch notes)" (`:464`); the button label
  (`:469`); `OnResponse` opens the history instead of `LaunchBrowser` (`:528`).
- **Where the wiki URL lives for launch:** `PatchNotes.WikiBase`, `PatchNotes.WikiPage` and `PatchNotes.NotesUrl` in
  `ShardVersion.cs` (comment at `:68`), unchanged. The comment in `BulletinGump.OnResponse` (`ClusterFBulletin.cs:528`)
  gives the one line that brings the browser button back. The server still writes `patch_notes.txt` at start for
  `scripts/Publish-PatchNotes.ps1`; nothing was published.
- `server/tests/Misc/PatchHistoryVerification.cs` (new): facts H1 to H4.
- `server/tests/Misc/PatchNotesVerification.cs`: fact 2 now presses All patch notes and asserts the history opens and
  the wiki address is **not** sent; fact 4 expects the history gump from `[version`.
- `CHANGELOG.md`: new section 2026.10.05.3 (one Added, one Changed line), and one line in the top comment saying what a
  `### Staff` list is (players never see it; staff see it in `[version`). `VERSION`: 2026.10.05.3.

## Layout (no screenshot)

Patch History gump, 600 x 500 at (50, 50): frame 9270, solid tile 2624 over (10, 10, 580, 480), no alpha region (the
Staff Hub / achievements look, D67 and cc-P57 F; hues are `StaffHubGump`'s).

- y 14: "Shattered Legacy patch notes" (gold). y 34: "You are on 2026.10.05.3. Newest first." (grey). Rule at y 58.
- List from y 66 to y 440 (374 pixels). Rows: a version heading 24 high (title at x 20, "(you are here)" after it,
  the date right-aligned to x 570); a list heading 20 high at x 30 (gold; Staff in lavender); each item an HTML block at
  x 40, 536 wide, `lines x 18 + 4` high (wrapped 8 pixels short of the width, as the achievements gump does) plus a
  2-pixel gap. One row of text is 18 pixels, so a page holds about 18 to 20 text rows.
- Pages hold whole rows. A heading is never left at the bottom of a page: it moves on with the row under it. A page
  that starts inside a version repeats "Shattered Legacy X (continued)", and inside a list, "Changed (continued)".
- Footer rule at y 448; at y 462: "Previous" (left arrow, page 2 onward), "Page N of M" centered, "Next" (right arrow,
  not on the last page), "Close".
- With today's real `CHANGELOG.md` (7 versions, 81 player lines; counted by a Python mirror of the parser and pager,
  not by the server): **12 pages for a player, 14 for staff**. Longest line: 4 rows.

The bulletin keeps its 480-wide layout; note lines are 440-wide blocks at x 20, up to 180 pixels of them (about 10 text
rows), then the "... and N more" line, then the All patch notes button.

## Facts and build

`PatchHistoryVerification` uses a 14-version sample: the real D87 line, a 160-pixel-plus word with no spaces, a
version with only a Staff list, and three Staff items in all.

- **H1** No line is cut: on every page for a player and for a GM, and in the bulletin, every HTML block is at least
  as tall as its wrapped lines (`GumpTextWidth`, the test's own copy of the font table), ends inside the frame, has no
  scrollbar, and no two rows overlap; every label ends inside the frame; the D87 line appears whole in both.
- **H2** Every version appears, in order, with its date; every Added / Changed / Fixed item appears for both viewers;
  no Staff item and no "Staff" text reaches a player; a GM sees all three Staff items; the wiki markup and the
  bulletin lines still leave Staff out.
- **H3** `[version` opens page 1 (no Previous); Next walks to "Page N of N", which shows the oldest version and has no
  Next; Previous walks back to page 1. "(you are here)" sits on the current version's heading. Opaque: no alpha
  region, the 2624 tile under the frame.
- **H4** The bulletin has no "wiki" and no "full notes" text; button 2 is labeled "All patch notes"; pressing it opens
  the history, sends no URL, and the notes count as seen. 20 long lines show some whole and count the rest in
  "... and N more (All patch notes)".

**Red, then green.** I wrote the tests after the code, so red came from breaking the code on purpose:

1. Run 1 (`--tests-only`) with four planted breaks (item height one row, staff shown to everyone, Next staying on the
   same page, the wiki label back): all four facts failed. H1: "Player page 1/7: ... needs 4 lines, its block is 18
   high". H2: the Shard Console Staff line found in the player's text. H4: "wiki" found. H3 failed too, **but for a
   test bug, not the planted break**: the full build that followed failed H3 the same way with nothing planted.
   Calling `OnResponse` directly leaves the old gump on the open list, so `FindGump` returned page 1 again. The real
   server removes the gump first (pinned `GumpSystem.IncomingPackets.cs:157`, then `OnResponse` at `:166`); the test's
   `Press` now does the same.
2. Run 2, Next break only: H3 failed ("Expected: 1, Actual: 0"). The message matches the test bug, so this run alone
   proves nothing. Run 4 is what separates the two.
3. Run 3, Next restored and only the bulletin's line height planted at one row (run 1 had hidden it, since H1 failed
   on the history first): H1 failed on the bulletin with the D87 line, "needs 5 lines, its block is 16 high", and H4
   failed on the crowded bulletin. H3 passed.
4. Run 4, nothing planted, full build: `Built sl-modernuo:cc-p64 with patches applied and 876 shard test(s) passing.`
   No compiler warnings in the log. The image holds `VERSION` 2026.10.05.3 and the new changelog section (read back
   from the image).

Every touched file is ASCII (byte count, 0 non-ASCII in all seven).

## Deviations and decisions for Chase

- **New version 2026.10.05.3, not an addition to .2.** The 2026.10.05.2 section is already committed, so per the
  changelog's own rule I started the next one and bumped `VERSION`. P63's uncommitted Staff line is still under .2;
  I left it there.
- **Staff list:** shown to staff (AccessLevel above Player), lavender (hue 1645, the bulletin's Personal Notice
  color), heading "Staff (players do not see this list)". A version with only Staff lines shows players "- Nothing
  players see changed in this version." so every version still appears.
- **The date comes from the version string** ("2026.10.05.3" gives October 5, 2026). The changelog has no other date.
- **The bulletin itself is still see-through** (its `AddAlphaRegion` is unchanged), and League Dispatch entries still
  use their fixed 40-pixel block. Neither was in the brief. If you want the bulletin opaque like the history, it is a
  two-line change.
- **The history opens at page 1**, the newest version, which is always the one the server runs.
- Pages are rebuilt from `ShardVersion.All` (parsed once at server start) each time a page is drawn; no file is read.

## For Chase

Deploy (after you commit; Windows PowerShell, `;` between commands):

```
cd D:\ShatteredLegacy; git status --short
docker tag sl-modernuo:cc-p64 sl-modernuo:latest
```

Then restart the test shard the usual way (or rebuild with `docker/uo/build.sh` after committing, as normal).
The server log should say `[ShardVersion] Shattered Legacy 2026.10.05.3 (7 version(s) in the changelog)`.

In-game checklist:

1. Log in on an account that has not seen 2026.10.05.3: the bulletin shows "Shattered Legacy 2026.10.05.3", the two
   new lines, an **"All patch notes"** button, and **no** wiki button.
2. Press All patch notes: the history opens; log out and back in, and the bulletin does not show again.
3. `[version` on a player: "Shattered Legacy 2026.10.05.3", then the history. Page 1 shows 2026.10.05.3 gold with
   "(you are here)".
4. Next through to the last page ("Page 12 of 12" on a player today): it ends with 2026.10.01, the oldest version;
   Previous comes back.
5. On 2026.10.05.2, "Crafting in Platinum to Celestial now raises Blacksmithy past the item's own limit, ..." wraps
   onto four rows and ends "The chance to make the item is unchanged."
6. As staff, `[version`: lavender "Staff (players do not see this list)" lists appear; as a player they do not.

P64 DONE
