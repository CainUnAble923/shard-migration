# cc-P741 review folder (for the build reviewer)

The task: Chase's 10-30 notes on the Wakening Isle: the coast, the wreck, the signs, the farm, the bank and the League
lodge. Notes: `notes\cc-P741-isle-coast-and-wreck.md`. Every piece placed: `placed.md` (one line a piece).

## Renders (isorender, client-correct statics; the server's farm, signs and addons drawn in)

| Subject | Before | After |
|---|---|---|
| Whole isle | `before-whole-isle.jpg` | `after-whole-isle.jpg` |
| West tip and wreck | `before-wreck.jpg` | `after-wreck.jpg` |
| North coast | `before-coast-north.jpg` | `after-coast-north.jpg` |
| South coast by the yard | `before-coast-south.jpg` | `after-coast-south.jpg` |
| Farm (field, gate, farmhouse) | `before-farm.jpg` | `after-farm.jpg` |
| Farmhouse, roof off | | `after-farmhouse-inside.jpg` |
| Bank and its ground | `before-bank.jpg` | `after-bank.jpg` |
| Bank, roof off | `before-bank-inside.jpg` | `after-bank-inside.jpg` |
| Lodge, roof off | `before-lodge-inside.jpg` | `after-lodge-inside.jpg` |
| Dock end and the travel sign | | `after-dock-travel-sign.jpg` |

The renders draw the farm addon, the signposts and P724's addons but not the moongate frame, NPCs or doors (server
items); the TazUO shots show everything.

## TazUO shots (`shots\`, the default camera, private shard 127.0.0.1:2596, this branch's image and map)

- `tazuo-coast-*.jpg`: wreck, west, south-west, north, north-east, the yard's south, east, dock. (In `coast-north` the
  Tester was put on a sea tile by my shot list; the shore beside him is what to look at.)
- `tazuo-sign-1-movement`, `-4-chat`, `-6-death`, `-11-travel`: the signs north of their paths.
- `tazuo-farm`, `tazuo-farm-gate`, `tazuo-farmhouse-inside`; `tazuo-bank-front`, `-inside`; `tazuo-lodge-front`,
  `-inside`.
- `walk-*.jpg` and `walk2-*.jpg`: frames of the real beach walk (walk2 with the client's windows closed).

## Walk log

`beach-walk.log`: Iron the Tester walked the west beach in TazUO with the client's own steps (no teleport): north from
6629,4003 past the wreck to 6629,3985, east to 6650,3985, back west and south to 6631,4002. Every leg reached its end,
no step stuck, no step changed Z by more than 3 (Z -5 on the wet sand to 0 on the grass).

## What to check (guide section 1)

- Shore: surf along every coast; the near (west, south) coasts smooth; the far (north, east) coasts still step a tile
  at a time along the sand, with surf along them (stated in the notes, not hidden).
- Wreck: both halves, broken open toward each other, one in the shallows, one up the beach.
- Signs: each north of its path, its board (0xA854) facing the path.
- Farm: field west, gate east, farmhouse by the gate, door to the road; furrowed beds, sparse short crops.
- Bank: the sign on the 0x0B98 hanger two east of the door; counter, vault, carpet, torches on plain wall pieces.
- Lodge: one floor tile; bookcases 0x0A98 north / 0x0A99 west, none before a window; banners between the east windows.
