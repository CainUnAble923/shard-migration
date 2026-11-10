# cc-P872: fix-up of P858 (real-light lamps and the Festival Peddler's wagon) after its build review P868 said FAIL

## In plain words

- **The fortune teller's wagon by the Festival stall in New Haven has a bare roof now.** The four glowing green
  symbols and the small grey "vent" that sat on the shingles are gone.
- **The black cat is still there, but on the porch** now, sitting on the potion kegs beside the door, where you see it
  as you walk up the steps. It no longer sits on the roof.
- The lamps and the wagon's steps are unchanged, and both still work in game.
- Nothing for you to do. P858's two questions still stand: the release New Haven needs its own spot for the stall and
  wagon, and the prices are placeholders.

Iron Golem, 2026-11-10. Code copy `D:\UO\golems\Iron\ShatteredLegacy` and docs copy, both on `golem/Iron/P872`. Read
first: `notes\guides\building-and-decorating.md`. I also wrote the review P868 this fixes up, so these are my own
findings. All play on the private proof shard (2596) under the test-shard lock. Stock art only.

## Step 1: P858 onto this branch

The prompt says to check out `golem/Iron/P858` and merge main into it; the Golem's hand-off says not to switch
branches or merge. Same result without either: this branch is main, and `git cherry-pick --no-commit
origin/golem/Iron/P858` put P858's change into both working trees, uncommitted, for the Golem to commit.
- shard-migration: clean.
- ShatteredLegacy:
  - `AchievementStore.cs`: P859's Horn of Plenty row and P858's ten lamp rows both kept, the horn first.
  - `CHANGELOG.md` and `VERSION`: P858's **2026.11.10.4** is still free (P869 has .3, P871 .5), so I kept it, above
    main's .2.

## The reviewer's list (P868) and what I did

The wagon's design file (`server/customizations/FestivalWagon/FortuneTellerWagonDesign.cs`) is generated, so the
change is in its generator, `notes/cc-P858-tools/convert858.py` (`ROOF_OUT`, `CAT_MOVE`), and the file was
regenerated. The wagon now has **207 parts** (was 212).

1. **The four rune glyphs on the roof** (0x4862 at 3649,2630,52; 0x4856 at 3649,2635,50; 0x4856 at 3647,2631,56;
   0x4844 at 3647,2635,56): left out of the design.
   - They were the author's hidden "window light" emitters. I gave their light to nothing new: the wagon still
     carries three lights, the porch lantern 0x0A22 (Circle300), the lamp stand 0x4C53 inside (Circle300) and the
     stained glass window 0xA5F8 (Circle150).
   - The night shots (`p872-lamps-night-*.jpg`) show the wagon still lit at its porch.
2. **The vent sculpture 0x2419 on the ridge** (3648,2633,53, "A Vent"): left out.
3. **The black cat 0x4689 on the roof's corner** (3650,2629,47): moved off the roof, its line ("You notice a black
   cat looking down at you") kept. I tried both places my review offered:
   - **The driver's bench at the north end first** (3648,2627,22). The run passed, but its shot showed the cat can't
     be seen there: from the default camera the wagon's own body hides its north end. A cat nobody can see is as good
     as deleted, so I moved it.
   - **The porch, final:** on top of the two potion kegs 0x9E36 (z 21 and 26) on the porch's west side, at
     **3646,2636,31**. It is beside the door, off the walk from the stair (the walk uses x 3647), and in view from
     the default camera as you climb the steps (`main-wagon-cutaway.jpg`, and the shots).

**Test:** `LampsAndWagonVerification` fact 6 now expects 207 parts and checks the roof:
- from the roof's lowest course (z 38) up, only roofing (bark 0x26F8-0x26FA, shingles 0x2C35) and the gable ends
  (0x0443, 0x299B);
- none of the four glyphs or the vent;
- the cat at -1,4,31, on the top keg.

P858's design breaks every one of these checks: 212 parts, the glyphs at z 50-56, the cat at z 47. That is the fact's
red; I did not run a separate red build.

## Proof

- **Renders** (`notes/cc-P858-tools/render858.py`, isorender, hues not drawn), in `notes\cc-P872-review\`:
  - `main-stall-wagon-3647-2632.jpg`: the roof bare;
  - `main-wagon-cutaway.jpg`: the roof off, the cat on the porch kegs.
- **TazUO** (default camera, private 2596 shard, P858's kit repointed into `notes/cc-P872-tools/kit`, `Walk872.py`):
  - the Player-account trainee "Iron Lamps";
  - staff hands only forced the winter festival (which put up the stall and the wagon), moved the trainee, laid the
    lamps, set the night and did one `[Flip`.
  - The run adds two checks to P858's: no rune glyph or vent within 18 tiles of the stall view, and the cat at
    3646,2636,31.
  - The stair walked for real both ways again.
  - Results: see "Final run" below.
- **`placed.md`**: every one of the 207 parts, one line each, with a "What cc-P872 changed" section at the top
  (`notes/cc-P872-tools/placed872.py`, P858's generator repointed).

## Final run

The final gated build and run had the cat on the porch kegs.

- **Gated build** `sl-modernuo:cc-p872` (`notes/cc-P872-tools/gated-build.ps1`, docker-build lock, page cache
  dropped first, `latest` not moved; log UTF-16): **EXIT=0, 3373 passed, 0 failed, 6 skipped**, with the eight lamp
  and wagon facts among them. The first build, with the cat on the bench, was also EXIT=0, 3373 passed.
- **TazUO: all 10 checks PASS** (`walk-log.txt` in the review folder):
  - the stair stands by the stall;
  - **the roof is bare (0 glyphs or vents found)**;
  - **the cat sits on the porch kegs at 3646,2636,31**;
  - walked up the stair and inside (z 0, 0, 2, 7, 12, 17, 21, 21, 19), then back down to the street;
  - eleven lamps laid and all lit by double-click;
  - the dragon lantern turned and stayed lit;
  - the jack-o-lantern goes out on a second double-click.
- **Shots** (`notes\cc-P872-review\shots\`): `p872-stall-and-wagon.jpg` and `p872-porch.jpg` show the bare roof and
  the cat on the kegs beside the door; the rest repeat P858's (stair foot, inside, going down, down again, the lamps
  by day, unlit and lit at night, the lantern turned).
- The first run (cat on the bench) was deleted before the rerun. Its north-end shot showed only the wagon's back with
  no cat in view, which is why the cat moved.

Seen, not ours: the pinned post-UOML skeleton spawners still walk New Haven's square (P858 noted them).

## Files

- `ShatteredLegacy`:
  - P858's change: `Items/Lights/ShardLamps.cs`, `FestivalWagon/` (2 new), `RewardStores/AchievementStore.cs` and
    `FestivalStore.cs`, `server/tests/Items/LampsAndWagonVerification.cs`, `server/tests/Misc/RewardStoreVerification.cs`,
    `CHANGELOG.md`, `VERSION` (2026.11.10.4);
  - on top of it: `FortuneTellerWagonDesign.cs` regenerated (207 parts), fact 6's count and roof checks, and the
    merge with P859's store row.
- `shard-migration`:
  - P858's notes and tools, with `cc-P858-tools/convert858.py` changed (`ROOF_OUT`, `CAT_MOVE`);
  - this file;
  - `notes/cc-P872-tools/` (the kit with `Walk872.py` and `stage872.py`, run872.ps1, gated-build.ps1,
    build-then-run.ps1, placed872.py, the edit script, the build log);
  - `notes/cc-P872-review/` (placed.md, the two renders, the shots, walk-log.txt);
  - `notes/cc-P872-shots/` (the full run).

P872 DONE
