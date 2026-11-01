# cc-P742 build review: the isle vision's dungeon shrine

For the reviewer (guide section 8). Everything here is stock art, placed per scene by the server; no map patch.

| File | What it shows |
|---|---|
| `placed.md` | Every piece, x, y, z, the wall or place it belongs to; the scene's spots and the tiles kept clear. |
| `render-chamber.png` | isorender of the room as the client draws it (default camera), on the void it stands on, the Gem on the pedestal. Read the four corners: post NW, east-west pieces on the north and south rows (the NE tile takes one), north-south pieces on the west and east columns (the SW tile takes one), corner SE. |
| `render-chamber-shards.png` | The same after the Gem breaks: shards on the pedestal and round it, the broken sword. |
| `tazuo-vision-00-at-the-stones.jpg` | The trainee (made by the bot's client minutes before) at the standing stones, before. |
| `tazuo-vision-01-dark.jpg` to `-16-back.jpg` | Each beat from the trainee's own TazUO, default camera: dark, the shrine lit, the Stranger walks, faces the Gem, strikes, the hit, the second blow, the Gem shatters, the shards, the fold, the echo, the hooded figure, what you keep, the gate, and back at the stones. |
| `before-vision-in-place-p707.jpg` | Before: the vision as it played where the player stood (P707's shot). |

Walk logs: none needed (nobody walks in the room; the player is frozen and every figure is moved by the server). The
return was checked by the client: `notes\cc-P742-tools\runs\vision\vision.log` (in the chamber at 6176,3758 during
the scene, back on 6792,3984 after, seen again, the lesson finished).

Windows: none (a dungeon room). Doors: none (sealed; the void round it cannot be walked, and FoldRegion refuses every
travel type). Sign: none (no one ever walks up to it).
