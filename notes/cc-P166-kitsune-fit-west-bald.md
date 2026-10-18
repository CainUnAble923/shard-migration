# cc-P166: Kitsune ears and tail: west-facing tail and ears on a bald head

2026-10-18. Prompt: `D:\UO\cc-prompts\cc-P166-cont-kitsune-fit-west-bald.md`. Both repos were clean at the start.
Read first: cc-P138 (render path, `fit-*-sfw.png`, per-direction frames) and cc-P81. Scratch:
`notes\cc-P166-scratch\` (the scripts, the two cc-P138 gumps kept as input, `proof\`); the full render sheets stayed
in the session scratchpad. "Ours" = `D:\ShatteredLegacy`.

## Headlines

1. **Found, from Chase's own screenshots.** `screenshot_2026-10-18_11-28-01.png` is Eve standing **West** and
   `11-26-45` / `11-27-05` standing **East**; my renders of the package's encoded frames match both
   (`proof\before-stand-8dirs-vs-chase-screenshots-11-26-E-11-28-W.png`), so the render path is the client's.
2. **The West tail: the art, not an offset or a missing frame.** West is drawn direction 3 unmirrored (North is the
   same frames mirrored; `Animation.GetAnimDirection`). The frames are present for walk, run and stand and line up
   with the body; the mirror maths (`MobileView.cs:817-826`) is the same for body and item. The fault was the
   stage-4 generator's direction-3 tail path (`design\kitsune-ears-tail\build_stage4_walk_remaining.py`
   `tail_points`, direction 3): root at the lower back and the tip only 4-5 px to the side, so the tail lay inside
   her leg silhouette and read as a stripe painted down the back of her thigh. Facing up-left, her back is toward the
   viewer's lower right; the tail now leaves the lower back and sweeps out past the hip on that side down to knee
   height, the profile's S-curve foreshortened. Same palette, widths, tip, sway and bob. Neighbours: South-West
   (drawn 2) and North-West (drawn 4) were right and are unchanged except the ears.
3. **The ears sat a little high on a bald head, in both places.** Paperdoll: the ears piece has a band across the
   crown, and on the bald bodies there were 3 rows (female 13, elf 15, elf 14) or 2 rows (male 12) of air between
   the band and the scalp; the kit's hair fills exactly that. In the world, hair adds one row over the skull's top.
   The client draws one gump and one animation per item (by sex, never by hair), so **one height for both**: the
   paperdoll ears down 3 rows (64783) and 2 rows (54783), the world ears down 1 row in all 105 frames. With hair they
   still rise out of it (they draw over the hair). Before and after for bald and haired: section 2.
4. **The fit gate learned it.** `check-paperdoll-fit.py` now refuses ears with more than a row of air above a bald
   scalp over the head's middle (seen red on the committed art: 4 failures), tests the face by the ears' pixels rather
   than their bounding box, and allows the ears' bottom to crown + 8 (was + 6). Deviation 1.
5. **A package build is required** (both gumps and `sl-anim7.bin` changed). Built here from the working tree:
   `player-package\dist\ShatteredLegacy-2026.10.18.1709.zip`, 98 MB, every gate passed including the paperdoll fit
   and animation encode gates; the zip's `sl-anim7.bin`, `64783.png` and `54783.png` are byte-identical to the
   sources. Not published (Chase's Build after the commit is the one to publish). No server change, no client patch.

## 1. Renders, every direction (prompt step 1)

`notes\cc-P166-scratch\render_dirs.py` composes body, hair and our Animation 4783 from the client data and our
`build\sl-anim7.bin` through `validate-art.py`'s reader (P134), at one anchor, as `MobileView.DrawInternal` places
and mirrors them, for all eight server directions x walk, run, stand. Run for bodies 401 (female), 400 (male),
606 (female elf), 605 (male elf), each bald, short hair (0x203B) and long hair (0x203C): 12 sheets before (the
anim-src PNGs at HEAD, `--src`) and 12 after (the re-encoded file), in the session scratchpad; the representative ones
are in `proof\`:

- `before-dirs-401-bald.png`, `after-dirs-401-bald.png`: all 24 cells, female bald.
- `world-female-bald-SW-W-NW-before-top-after-bottom.png`: South-West, West, North-West; walk, run, stand; before
  (top three rows) and after (bottom three).
- `world-after-male-bald-top-elf-long-bottom-N-SW-W-NW.png`: the fix on the male body bald and the male elf with long
  hair, North (the mirror of West) included.

Which frames were wrong: West and North, all three actions (walk 10, run 10, stand 1 frames of drawn direction 3).
Not mirrored-wrong, not offset, not missing.

## 2. The fixes (step 2), with file:line, before and after

**West tail.** `notes\cc-P166-scratch\build_west.py` loads cc-P138's `build_stand_run.py` (which drives the stage-4
generator), replaces `tail_points` for direction 3 only, and regenerates `a00_d3_*`, `a02_d3_*`, `a04_d3_f00`. First
checked: with the old path the generator reproduces every committed d0/d2/d3/d4 frame of walk, run and stand with 0
differing pixels, so only the path changes. Design source files under `design\` were not edited.

**Ears, world.** The same script moves every frame's ear pixels (canvas rows above 58, cc-P138's split) down 1 row.
`measure_ears.py` (per ear column, rows of air down to the head or hair): every body, hair and direction moved by
exactly one row, e.g. female bald direction 0 tightest column -1 -> -2, female long hair -2 -> -3.
`proof\world-heads-bald-short-long-8dirs-before-top-after-bottom-8x.png`: rows bald, short, long; eight directions
standing; before above the yellow line, after below.

**Ears, paperdoll.** `notes\cc-P166-scratch\lower_paperdoll_ears.py` (input: `old-64783-p138.png`,
`old-54783-p138.png`, kept beside it) moves the rows above 45 down: 3 rows in 64783, 2 in 54783; 2,535 opaque
pixels before and after in each. Options shown to choose from:
`proof\paperdoll-ears-options-down-0-2-3-4-4x.png` (top female, bottom male; each pair bald | kit hair).
Chosen: `proof\paperdoll-ears-bald-hair-before-left-after-right-4x.png` (left before, right after; both cells carry
the label "down 0" because the script labels the shift it applies on top of the file it is given).

Files in `D:\ShatteredLegacy`:

| File | What |
|---|---|
| `player-package/vendor/shattered-legacy-art/anim-src/4783/*.png` (105) | d3 tails redrawn; all ears 1 row down |
| `player-package/vendor/shattered-legacy-art/gumps/64783.png`, `54783.png` | ears 3 and 2 rows down |
| `scripts/check-paperdoll-fit.py:22-23` | doc: crown + 8, the bald-scalp rule |
| `scripts/check-paperdoll-fit.py:46-51` | `EARS_SIT` (-1, 8); `EARS_REST` 1, `EARS_REST_COLS` 5 |
| `scripts/check-paperdoll-fit.py:220-237` | face test by pixels; air above the bald scalp |
| `scripts/tests/test_check_paperdoll_fit.py:88-95`, `:103-111` | too-low test +5 (was +8); new bald-scalp test |
| `player-package/vendor/shattered-legacy-art/SOURCE.txt:156-159`, `:171-173` | the fox section |
| `player-package/vendor/shattered-legacy-art/registry.csv:53-55` | the three fox rows' descriptions |
| `CHANGELOG.md:32-41`, `VERSION` | 2026.10.18.11 |

`build\sl-anim7.bin` (git-ignored, generated) was rebuilt: 25,028,054 bytes, idx 422,100.

## 3. Rebuild (step 3)

- `python scripts/build-equip-anims.py`, then `--check`: "anim7 matches" (every block decodes back to its PNG).
- `python scripts/check-paperdoll-fit.py`: "2 gumps, 0 failures", the Topless and Nude add-on sets present on this
  machine checked too.
- `Build-PlayerPackage.ps1`: built `ShatteredLegacy-2026.10.18.1709.zip` (98 MB, 744 files, TazUO 3212623f + 3
  patches), exit 0; paperdoll fit gate and animation encode gate passed. `dist\` is git-ignored (`.gitignore:66`).
- **A package build and publish are required** for players to see this. No shard rebuild is needed for the art (the
  server only sends the item); the shard image only carries the new patch notes.

## Tests

- **New: `test_ears_with_air_under_them_on_a_bald_head_fail`** (the cc-P138 placement, 3 rows up, must fail with "rows
  of air between the ears and the bald scalp"). **Seen red first** in the other direction that matters: with the rule
  in and the art not yet moved, the committed-art test failed with exactly the four bald-scalp failures (3, 3, 2, 3
  rows on bodies 13, 15, 12, 14). Then the art moved and all passed.
- **Face test by pixels:** with the ears moved, the bounding-box version failed on 64783 (box row 40 touching the
  face box's top row 40) and on 54783 at 3 rows (box row 37 on its top row 37), with no ear pixel inside either
  face box (the outer base corners are at columns 75-80 and 104-108, outside the face's 82-103). The committed-art
  test pins the pixel version; the too-low test, now +5 (8 more rows takes the ears past `EARS_BELOW` so they stop
  counting as ears), still fails with "cross the face box".
- `python -m unittest discover -s scripts/tests`: **36 of 36** (13 paperdoll fit, 23 validate-art).
- `Paperdoll-Bodies.Tests.ps1`: 9 of 9.
- `Build-UoOverrides.Tests.ps1`: **11 of 12; the one failure is not this task's** and is red at HEAD:
  `TheServersCopyOfTheRecordsIsRecordsJsonAndEveryIdIsRegistered` pins 137 registry rows and 2 gump rows, and cc-P147
  added three gump rows (22456-22458, the Achievements button) without updating the pins (140 rows, 5 gump rows).
  This task added no rows. Deviation 3.
- No world-frame unit test was added: the frames are art, checked by `build-equip-anims.py --check` (encoding) and
  by the renders and `measure_ears.py` numbers above.
- Play-test Who tests: `python -m unittest tools/tests/test_play_who.py tools/tests/test_playsessions.py
  tools/tests/test_playtests_reopen.py`: 33 of 35; the two failures name open items M-001, P163-0 and P164-0 with no
  Who, from earlier work, not P166's.

## Play-test items added

Two, under **For Chase** below, sorted in `testing\bot-triage.md` (`### P166`, both EYES) with steps in
`testing\playtest-steps.json` (after P138-7). P138-6's pass text there now describes the new West/North look.

## Deviations and decisions for Chase

1. **The fit gate changed in two ways besides the new rule:** the ears may now end at crown + 8 (was + 6), because
   lowered ears' outer base corners hang beside the skull, below the crown; and "ears out of the face" is tested on the
   ears' pixels, not their bounding box, which had started refusing ears with no pixel in the face. Neither lets the
   P62 placement or the cc-P138 failure cases through (all 13 tests, including the "too low", "floating" and
   "off-centre" ones, still fail as they should).
2. **One height for bald and hair, not per hair.** Neither the paperdoll gump nor the world animation can follow hair
   in the client (both are picked by the item's animation number and the wearer's sex). The server could swap the item
   to a second "bald" version when the wearer has no hair, but that needs a second item ID, gumps and frames and has to
   follow every haircut; not done. The chosen heights: bald, the ears rest on the scalp; hair, they rise out of the hair
   a little lower than before (`paperdoll-ears-options-down-0-2-3-4-4x.png` shows 0, 2, 3 and 4 rows down if you want
   another).
3. **`Build-UoOverrides.Tests.ps1` is red at HEAD** from cc-P147's three registry rows (above). Not fixed here: it
   is cc-P147's pin, and P165 is still working on that button. The fix is the two numbers (140 rows, 5 gump rows).
4. **Also seen, not changed: standing East and South (drawn direction 1) the tail hangs a few pixels clear of her
   leg**, at knee height, so it looks detached; that is your 11:26 screenshot (`proof\before-stand-8dirs-vs-chase-
   screenshots-11-26-E-11-28-W.png`, top row, the third (East) and fifth (South) figures from the left). It is the
   cc-P138 stand frame moved from the walk art; walking and running there look joined. Say if you want it pulled in to
   the hip; it is a small follow-up of the same kind.
5. **North changed with West** (they are one set of frames, mirrored). You only reported West; North had the same
   flat-on-the-legs look.
6. **No task-list tool exists in this session,** so the step-by-step progress was not posted there; the sections above
   follow the prompt's steps in order.
7. **Read was used on my scratchpad copies** of your screenshots; nothing was skipped.

## For Chase

Build and publish the package after the commit (Shard Console > Player package > Build package, then Publish). No
shard rebuild is needed for the art. Then set **P138-6 back to open** on the play-test page (I did not change its
recorded result).

In game on the test shard with the new package:

1. **West and North:** a female character with the ears and tail on, hands empty: stand facing west (up-left on
   screen) and north (up-right), then walk and run that way, then all eight directions (this is P138-6 again). The tail
   leaves the small of her back and sweeps out behind her past the hip, not flat down her legs; the other six
   directions look as before (`notes/cc-P166-scratch/proof/world-female-bald-SW-W-NW-before-top-after-bottom.png`).
2. **Bald and haired side by side:** two characters wearing the ears and tail, one bald and one with hair, in the
   world and on their paperdolls. Bald: the ears sit on the scalp with no gap under them. Hair: they still rise out of
   the hair (`notes/cc-P166-scratch/proof/paperdoll-ears-bald-hair-before-left-after-right-4x.png`).

## Patch notes

`CHANGELOG.md` has a new section **2026.10.18.11** (2026.10.18.10 was committed with P165): two Fixed lines (the west
and north tail; the ears on the head) and one Staff line (the fit check). `VERSION` is 2026.10.18.11. The wiki page
was not published.

## Repo size rule

No file over 5 MB in either repo. Largest new or changed: the proof images, 18-101 KB each; `notes\cc-P166-scratch\` is
about 0.5 MB in all. The 98 MB zip is in `player-package\dist\` (`git check-ignore -v`: `.gitignore:66:player-package/dist/`)
and the 25 MB `sl-anim7.bin` in `vendor\shattered-legacy-art\build\` (`.gitignore:100`). Python caches are ignored by
`.gitignore:20:__pycache__/` (checked for both scratch folders). The full render sheets stayed in the session scratchpad.

## Files

`D:\UO\shard-migration`: this note; `notes\cc-P166-scratch\` (`render_dirs.py`, `measure_ears.py`, `heads.py`,
`zoom.py`, `pd_ears.py`, `build_west.py`, `lower_paperdoll_ears.py`, the two cc-P138 gumps, `proof\` 8 images);
`testing\bot-triage.md`, `testing\playtest-steps.json`; `README.md`, `dashboard.html`, `tools\progress.json` from
`tools\progress.py`. Agents never edit `docs\`; nothing there was touched.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`:

```
Repo    Result
----    ------
code    dry run
docs    dry run
scripts clean
```

P166 DONE
