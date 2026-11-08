# cc-P851: build review of P849 (the League requisitions board turned to the art that hangs flat on its wall)

## In plain words

- **P849 passes its build review, so it can merge.** The League notice board in New Haven's League office now hangs
  flat on its wall in both towns. Before, it stuck out of the wall edge-on, like a partition.
- **Testers' New Haven (the isle release):** the board is flat on the office's inside dividing wall, south of the desk.
  **Main's New Haven:** it is flat on the hall's north wall, beside the bookcases.
- **One small slip to fix later, not blocking:** a notes page for builders (`notes\map-building-playbook.md`) still has
  the two board pictures the wrong way round. The main building guide is right.
- Nothing for you to do.

Gold Golem, 2026-11-08. Reviewed `origin/golem/Iron/P849` (docs `d6f551ed`, code `23af0c3`) without changing
branch. Docs-only: no build, no shard.

## What I looked at

- The guide `notes\guides\building-and-decorating.md`, read in full (sections 2.2, 2.4, 2.5, 3, 6 and 11.2, 11.12 are
  the ones that apply here).
- `notes/cc-P849-review/placed.md`, the notes `notes/cc-P849-fixup.md` (the prompt names
  `cc-P849-fixup-league-boards.md`; the branch has it as `cc-P849-fixup.md`), its Codex review, and the P836 review
  whose FAIL list P849 answers.
- The code: `OfficeBoardItemID` is **0x1E5E** in main's `Appraiser.cs` (board 3663,2548,0) and **0x1E5F** in the
  release diff (3458,2602,18). The load-time retag turns a board already on its spot.
- Every image: `board-sprites.png`, `board-arts-on-walls.jpg`, the two isorender before/after sheets and their zooms,
  the two TazUO before/after sheets, and the TazUO shots in `shots-main-after\` and `shots-release-after-run1\`
  (board from the room, inside the office or hall, the west wall or north wall, outside).

## Check, one by one

| Check | Result |
|---|---|
| Which art hangs on which wall (P836 item 3) | `board-sprites.png`: 0x1E5E's frame runs like the east-west wall piece 0x0034, 0x1E5F's like the north-south 0x0035. `board-arts-on-walls.jpg`: 0x1E5E flat on the north wall, edge-on at the west; 0x1E5F the opposite. Matches guide section 3 (south facing on a north wall, east facing on a west wall). **Pass** |
| Release board 0x1E5F, 3458,2602,18, west (dividing) wall x3457 (P836 item 1) | Isorender after: frame lies along x3457, on the tile's west edge, clear of the desk's south end and the hide at 3458,2597. TazUO check line "art is 0x1E5F, the one for its west wall" PASS. **Pass** |
| Main board 0x1E5E, 3663,2548,0, north wall y2547 (P836 item 2) | Isorender and TazUO (`after849-board-from-the-room.jpg`, `after849-inside-hall-north-wall.jpg`): flat on the north wall, in line with the bookcases 0x0A98/0x0A97, free tiles 3662 and 3664 each side. **Pass** |
| Guide rows (Bank, Guild hall, section 10) | Corrected to 0x1E5E north wall, 0x1E5F west wall, with the render cited. **Pass** |
| Walls, corners, doors, roofs | No wall, door or roof piece placed or changed; both buildings are the map's own. Nothing new on a roof. **Pass** |
| Wall-mounted items, signs | The board is the only change. Release signpost 0xA854 at 3460,2591,20 and main sign arm 0x0B98 + board 0x0BCF at 3671,2563 are unchanged from P827, which P836 passed; the shots still show them. **Pass** |
| Stairs, shores, bridges, docks, foliage | None in this build. |
| Better piece on disk (section 10) | The board is the shard's own `RequisitionsBoard` on stock bulletin-board art; no better stock or pack piece for a usable notice board. **Pass** |
| Existing worlds (checklist 7) | A board on its spot with the old art is turned on load (fact `ABoardWithTheEdgeOnArtIsTurnedOnLoadOnceAndStaysTheSameItem`); a board on the first old spots moves (both `shard.log`s). **Pass** |

BUILD REVIEW P849: PASS

## Not blocking (for the overseer's list)

1. **`notes/map-building-playbook.md`, section 7, second row** (added by P827's merge, carried in P849) still says
   "Bulletin board: 0x1E5E hangs on a west wall, 0x1E5F on a north wall" and cites P803's `board-facings.png`. That is
   the swap P849 fixed; the guide and the renders say the opposite. Swap the two IDs and point the row at
   `notes/cc-P849-review/board-arts-on-walls.jpg`. Codex flagged the same line. It is a docs line, not a placed piece,
   so it does not hold the merge.
2. **P803's and P827's in-between board spots** (main 3662,2548,0; release 3458,2598,18) are not in
   `OldOfficeBoardSpots`, so a world seeded by P803 or P827 alone would keep its board there (Codex's other flag).
   Neither P803 nor P827 merged or shipped, so only proof shards ever held those spots; worth adding with the next
   change to this seeder.

P851 DONE
