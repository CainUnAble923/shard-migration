# cc-P877 review (fix-up of P861 after P876): what is placed in the world

**Nothing permanent is placed.** P861 and this fix-up add no seeder, map static, mapop, decoration file or permanent
addon to any shipped world. The change is the NPC name lists, the town name rule and the staff tool `[VBuild statify`
(with its Visual Builder undo). Everything below was placed by staff hands on the **private proof shard (2596) only**,
on a throwaway copy of the bot world, to show the tool working. The copy is thrown away after the run.

## Proof placements (Trammel, main's New Haven square, town region "Haven")

| Piece | Item ID(s) | Location (origin) | Facing | What happened to it |
|---|---|---|---|---|
| Fountain of Youth (`FountainOfYouthAddon`, fixed) | 0x1731-0x173F, 0x1741 (middle 0x173A) | 3651,2600,0 | none (round, one variant) | `[VBuild statify` **refused** it (a seeder places and keeps it); it stayed an addon on Trammel. P876 item 2. |
| Stone fountain (`StoneFountainAddon`) | 0x1731-0x173F, 0x1741 (middle 0x173A) | 3655,2605,0 | none (round, one variant) | Frozen into 16 plain statics where its parts stood (same art and height), then `[VBuild undo` put the addon back. P861's proof, redone. |
| Provisioner named Mara (female) | body 0x191 | 3660,2601,0 | n/a (NPC, CantWalk) | The older of two Maras; the town rule renamed her. |
| Mara, the town steward (`ClusterFTownsfolk plaza`) | body 0x191 | 3661,2601,0 | n/a (NPC, CantWalk) | Kept her name (a fixed identity). |

Both fountains use pinned's stone fountain pieces and offsets: 0x1731 at -2,1; 0x1732 -1,1; 0x1733 0,1; 0x1734 1,1;
0x1735 1,0; 0x1736 1,-1; 0x1737 1,-2; 0x1738 0,-2; 0x1739 0,-1; 0x173A 0,0; 0x173B -1,0; 0x173C -2,0; 0x173D -2,-1;
0x173E -1,-1; 0x173F -1,-2; 0x1741 -2,-2; all at z 0 on paving whose land z is 0 (every tile checked by
`cc-P877-tools/render877.py`). The Fountain of Youth's footprint is x 3649-3652, y 2598-2601; the stone fountain's
x 3653-3656, y 2603-2606. They do not touch each other, a wall, a door or a road edge piece.

## Files here

- `main-square-fountains-3651-2600.jpg`: isorender of the square (x 3640-3668, y 2588-2614) with both fountains as
  staged (upper: Fountain of Youth; lower: stone fountain). Hues are not drawn.
- `shots/`: the TazUO shots of the proof walk (`p877-1` to `p877-7`) and `walk.txt`.
  - Before, refused: `p877-1-youth-before.jpg`, `p877-2-youth-refused.jpg`.
  - Before, after, undo: `p877-3-fountain-addon.jpg`, `p877-4-fountain-statics.jpg`, `p877-5-fountain-back.jpg`.
  - Names: `p877-6-maras-before.jpg`, `p877-7-maras-after.jpg`.
- `p861-shots/`: P861's own three fountain shots (before, after, undo at 3655,2605,0), copied as P876 asked.
