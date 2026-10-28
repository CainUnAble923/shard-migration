# cc-P716: TazUO pictures of the server on the SoS map (continues P675, SoS swap S2)

Iron Golem, 2026-10-28, second session (the first stopped at 05:38 for the overnight bot and low memory; Chase's answer
`Iron-P716-20261028-053858-d4f0`: retry after P717 and P718, private shard only, keep the TazUO windows off-screen).
Docs copy `D:\UO\golems\Iron\shard-migration` on `golem/Iron/P716`. Nothing in the code copy changed. Not committed,
nothing deployed, Haven not touched.

## In plain words

- **The pictures are taken, and they show the server on Zigholtul's Siege of Sosaria map.** Valunstead looks the
  same on Trammel, Felucca and the Fold, and the hall's inside is his. They are in `notes\art\sos-s2-shots\`.
- **The "send them home" corner works as P675 meant.** A player put on the Wakening Isle's beach on Trammel woke in
  town (the author's Haven). Staff on Felucca stayed on the beach. Down in his Passage of Lost Souls cave a player is
  left alone, on Trammel and on Felucca.
- **One oddity, seen once and not explained:** in the first run the player's cave picture showed the town instead,
  right after the beach scene had sent him home. Run again on its own on a fresh shard, the player stayed in the cave,
  and the server confirmed where he stood. Worth a glance on the swap's go-live day.
- **For you:** nothing to do. The game windows were opened off the screen, so nothing popped up on the tower.

## What was done

1. **Overlay.** `cc-P675-tools\overlay-run.ps1 -Scratch <scratchpad>\p716` built it on SoS, and its three refusal checks
   still refuse (the red lines in its output are those checks). `rebase.py` rebuilt the edited map: today's patch on
   SoS, drifted 0, missing 0. `overlay_check.py` (`cc-P716-tools\out-overlay-check.txt`): land identical to SoS + patch
   **True**, statics blocks differing **0**, 504,384 `0003@15`, 6638,3993 `0073@0`.
2. **Private shard.** No `uobot.run` process and no bot container. Took `test-shard` and ran `cc-P675-tools\proof-shard.ps1`
   on 127.0.0.1:2596 from `sl-modernuo:cc-P675` with that overlay. Never 2594.
3. **Shots.** `cc-P716-tools\shots.ps1` is P675's script plus `-OffScreen`, which opens both TazUO windows at x -4000
   (Chase's ask). PrintWindow still captures them (`make_shots.py` writes it from P675's). The client is
   `D:\UO\golems\Iron\tazuo-p670\client`, its overrides built on the SoS base with today's `trammel.mapops`. Spec:
   `cc-P675-tools\scenes.json`. Every picture was looked at. The login windows (patch notes, paperdoll, achievement
   pop-ups) cover the upper left of each, but the land around them is clear.
4. **Down.** `proof-shard.ps1 -Down` and the lock released, twice (the recheck below). No container of mine is
   running.

## The pictures (`notes\art\sos-s2-shots\`)

| Scene | Player window | Admin window |
|---|---|---|
| 1 Valunstead, 504,384 | Trammel: his blue-tiled plaza, the green-roofed hall, a lamppost. The pop-up says "set foot in Trammel" | Felucca, same spot: the same plaza, hall and lamppost. The pop-up says "set foot in Felucca" |
| 2 | The Fold (map 32) at Valunstead: the same land as Trammel | Trammel, the hall floor 479,388,20: his interior (green walls, teal floor, bookcases, candelabras) |
| 3 The isle's beach 6638,3993 | Trammel: **sent home**. He woke in the author's Haven (a stone tower, a fountain, a lamppost), not on the beach | Felucca: **stays** on the isle's beach (sand, grass, the road) |
| 4 Passage of Lost Souls 2, 6202,2116 | First run: showed the Haven town (see below). **Recheck: in the cave**, pop-up "set foot in Trammel" (`recheck\4-...-player.jpg`) | Felucca: in the cave's rock |

**Scene 4's first player picture.** It ran right after scene 3, where the same Player had just been sent home. The
setup's answers were all "Property has been set", yet the picture showed the Haven town. I ran scene 4 again on its
own, on a freshly started shard, and then asked the server
(`recheck\proof-log.txt`): `Location = (6202, 2116, -9)`, `Map = Internal` (logged out there), and the picture shows
him in the cave. So the region leaves the cave alone, as P675's facts say. Why the first run differed is not explained.
My guess, unverified: the Player was still lingering in the world after scene 3's logout when the moves were typed. The
two first-run pictures are kept beside the recheck so the overseer can compare.

## State

- No lock held, no container of mine running, nothing committed.
- Files: this note, `notes\cc-P716-tools\` (`out-overlay-check.txt`, `make_shots.py`, `shots.ps1`,
  `scene4-recheck.json`), `notes\art\sos-s2-shots\` (8 pictures, `proof-log.txt`, `recheck\` with 4 pictures and
  its log; 1.6 MB). P675's notes already link here.

P716 DONE
