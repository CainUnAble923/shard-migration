# cc-P844 review folder (for the build reviewer)

The task: fix-up of P721 (the bandage wait on the isle) after P834's build review FAIL. Notes:
`notes\cc-P844-cont-fixup-isle-bandage-healing.md`. Every piece P834 listed is in `placed.md`, **as main has it now**,
not as the old `golem/Iron/P721` branch had it. The one piece this fix-up changed is Pip's bench (0x0B2D to 0x0B2C).

## Renders (isorender: client-correct statics from this branch's map patch, the server's pieces drawn in by `notes\cc-P844-tools\render844.py`)

| Subject | File |
|---|---|
| Farm gate and stop area (field, gate, fence, gate signpost, Wren's corner, farmhouse, healing sign) | `farm-gate-and-stop-isorender.jpg` |
| Farmhouse with the roof off: Pip's bench 0x0B2C, blood, table | `farmhouse-pip-cutaway-isorender.jpg` |
| Clothes and chat stops together | `clothes-and-chat-stops-isorender.jpg` |
| Clothes stop (table 0x0B8F, rack 0x0EC6, lesson sign) | `clothes-stop-isorender.jpg` |
| Chat stop (chat signpost at Signpost -2,-4, lesson sign) | `chat-stop-isorender.jpg` |
| The wooden bench's two runs: 0x0B2D (left) and 0x0B2C (right), each on two tiles in a north-south line | `bench-0B2D-left-0B2C-right.png` |
| One standing signpost 0xA854 (left) and two on diagonal tiles (right): a finding, see the notes | `signpost-one-left-two-diagonal-right.png` |

The vision braziers are in P742's chamber. Their render and shots are P742's (`notes\cc-P742-review\`).

## TazUO shots (default camera, private shard 127.0.0.1:2596, image `sl-modernuo:cc-P844`, this branch's map, Iron the Tester, a Player account)

Before the bench fix (the image built from main, the bot world freshly seeded):
- `tazuo-chat-signpost.jpg`, `tazuo-farm-gate-signpost.jpg`, `tazuo-field-gate-and-fence.jpg`, `tazuo-clothes-table.jpg`
- `before-tazuo-pip-on-bench.jpg`: Pip on the old 0x0B2D pieces.

After the fix, on **the same world saved before it**, restarted on the new image (the upgrade in place), walked on foot:
- `after-tazuo-clothes-table-read.jpg`: the table and rack clicked, their names shown.
- `after-tazuo-chat-signpost-read.jpg`: "Farm signpost: say 'I am ready to learn'" over the post.
- `after-tazuo-farm-gate-signpost-read.jpg`: "Farm signpost: Wren the Farmhand at the gate".
- `tazuo-field-gate-and-fence-walk.jpg`: the gate 0x0843 and fence piece 0x0837 in the field's east fence.
- `after-tazuo-pip-on-bench.jpg`, `after-tazuo-pip-on-bench-named.jpg`: inside the farmhouse, Pip seated on the bench by
  the east wall with blood around him, named "Pip the farm boy, cut on the fence".

## Walk log

`tour-walk.log`: the tour walked with the client's own steps (Pathfind, no teleport). It went from the clothes stop
along the road to the chat stop and up to the farm gate. Then up the farmhouse steps (Z 0, 4, 7), through the door to
Pip and back out. It has 13 PASS lines and no FAIL. On the upgraded world it found one 0x0B2C piece on each bench tile,
6704,3975,7 and 6704,3976,7.
