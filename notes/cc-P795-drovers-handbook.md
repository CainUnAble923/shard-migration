# cc-P795: the Drover's Handbook

## In plain words

- **The Drover's Handbook is built, with your "Stronger" numbers.** Animal Trainers will sell the book for 2,500 gold with Corral in it, plus three
  pages to drop in: Calm 500, Herd 1,000, Lure 1,500. No crook is needed, and using the abilities trains Herding, up to 200 on the hardest animals.
- **At 200 Herding:** Corral makes an animal 25 easier to tame, Calm stops one fighting for 13 seconds, Herd walks up to 10 animals from an 8-tile
  area to a spot you pick, and Lure pulls one animal from 15 tiles away, even out of sight.
- **Seen working in TazUO:** all four worked on wild peacocks on the Trinsic meadow, on the private proof shard. Buying from a trainer in the
  client was not tried; the tests cover the trainer's stock instead.
- **For you:** it reaches players with the next main deploy. Two small things to look at are under "Deviations and decisions for Chase": Herd can
  train faster than the others, and old frames are left in the shots folder.

## State

Iron Golem, 2026-11-04 and 2026-11-05. Code copy `D:\UO\golems\Iron\ShatteredLegacy` and docs copy `D:\UO\golems\Iron\shard-migration`, both on
`golem/Iron/P795`, not committed by me. Main only, not the isle release. Nothing deployed, packaged or published. `latest` was not moved. The only
shard started was the private proof shard on 127.0.0.1:2596, now removed. Gated image: `sl-modernuo:cc-p795`, version 2026.11.05.

## Numbers

Chase chose "Stronger" on 2026-11-05 (`Iron-P795-20261104-132203-75f3`). All are in modernuo.json under `clusterf.drover`, written with these
defaults on first start, and the book's page text reads them.

| Ability | Number | Stamina | Setting names |
|---|---|---|---|
| Corral | Herding / 8 easier (25 at 200), next attempt within 60 s | 5 | `corralDivisor`, `corralSeconds`, `corralAttemptGraceSeconds`, `corralStamina` |
| Calm | 3 + Herding / 20 seconds (13 at 200), same animal again 30 s after a calm that worked | 10 | `calmBase`, `calmDivisor`, `calmCooldownSeconds`, `calmStamina` |
| Herd | radius Herding / 25 (8 at 200), Herding / 20 animals (10 at 200), at least 1 each, to a spot up to 10 tiles off, one roll each | 15 | `herdRadiusDivisor`, `herdCountDivisor`, `range`, `herdStamina` |
| Lure | one animal up to 15 tiles away, no line of sight needed | 10 | `lureRange` (held to 15 at most), `lureStamina` |
| Book and scrolls | 2,500; Calm 500, Herd 1,000, Lure 1,500 | | `bookPrice`, `calmScrollPrice`, `herdScrollPrice`, `lureScrollPrice` |
| All | gains up to the animal's difficulty + 92, cast delay 1 s, target range 10 | | `gainTop`, `castDelaySeconds`, `range` |

## What was built

| Piece | State |
|---|---|
| `DroverSpell` | A `Spell` on Herding: no mana, no reagents, stamina paid once the target is chosen. The cast cannot fizzle or gain. |
| Corral | `CorralSpell.cs`, `DroverCorral`. One corral per tamer, in memory only, as it lasts a minute. |
| Calm | `CalmSpell.cs`. Uses the creature's pacify state, so it stops fighting everyone, as peacemaking does, and hurting it can break the calm. |
| Herd | `HerdSpell.cs`. Animal, then spot. The stamina goes at the spot, so cancelling is free. |
| Lure | `LureSpell.cs`. The animal walks to a free tile beside the drover. |
| Scrolls | `DroverScrolls.cs`: `CalmScroll`, `HerdScroll`, `LureScroll`, stock blank scroll art with hue 0x8A5. No saved fields beyond `SpellScroll`'s. |
| Book | `DroversHandbook : Spellbook`, IDs 693 to 696, art 0x0FEF, blessed as every spellbook is. Double-click opens `DroversHandbookGump`, as the client has no such book. `[Corral`, `[Calm`, `[Herd` and `[Lure` are for macros. |
| Patches | `Spellbook-drover-type`, `AnimalTaming-drover-corral`, `SBAnimalTrainer-drovers-handbook`, all applied at `--fuzz=0` in the gated build. |
| Existing worlds | Nothing to seed: vendors rebuild their stock on load (`BaseVendor.cs:740`), so a trainer in an old world has the rows at once. |

### Decisions

- **Chase's answer gave only the numbers at 200,** so the Herd formulas are mine: Herding / 25 and / 20, as the two numbers that reach 8 and 10 exactly.
- **Herding could not reach 200 on the crook's window.** That window is the animal's difficulty + 30 to 39, and the hardest tame is 108, so it stops
  near 147. `Persuade` adds a gain-only roll past it, up to difficulty + 92. Chase was told this in the question.
- **Herd leaves out an animal over 15 tiles from the spot,** before it rolls. `BaseAI.CheckHerding` drops any walk over 15 tiles, so that animal
  would roll, gain and never move. If none are left, Herd says so and costs nothing.
- **Lure refuses an animal over 15 tiles in a straight line,** for free. A target's range is a square, so 14,14 is "in range" but 19.8 tiles to the
  engine, which would drop the walk silently.
- **Lure aims beside the drover,** not at the drover's tile: an animal aimed at an occupied tile stays herded, pushing against the drover.
- **Calm refuses an animal already calm or still in its wait,** for free. A failed Calm costs stamina and leaves no wait.
- **Corral and the other abilities roll like the crook,** so a low-Herding drover can fail on a hard animal and still pays the stamina.
- **The taming patch keeps its pinned line.** `SkillGainRowKeysVerification` reads `var minSkill = ...` literally, so Corral is a new line after it.
- **The anger chance still uses the animal's own difficulty,** so Corral helps the taming and not the anger.
- **A corral is used at the roll, not at the start,** so an interrupted attempt does not spend it.
- **Reading a scroll** casts once without a book, as any spell scroll does, and uses the scroll up.
- **Rules check.** Nothing grants skill or stat points, power scrolls, bless deeds or property artifacts: the only gain is the normal skill roll. The
  book and scrolls round-trip through save and load (D40).

## Tests

`server/tests/Drover/DroversHandbookVerification.cs`, 29 cases. Final gated build: 3082 tests, **3076 passed**, 0 failed, the rest skipped;
`notes\cc-P795-tools\gated-build-final.log`, EXIT=0. `gated-build.log` is the run before the gump row fix, same count.

**Watched red** (`mutants.txt`): 11 mutants in a throwaway builder container. 10 went red. The eleventh, removing `bc.Combatant = null` in Calm,
stayed green because `Warmode = false` already clears the fight, which a further mutant proved. I removed that line rather than keep it.

Fact-writing traps:

- Ter Mur is 1280 wide, so the old spot 1802,1183 was off that map and range lookups found nothing. The facts moved to Ilshenar.
- There the animals' AI runs during the clock's seconds, so they wander: the facts set `CantWalk`.
- The same seconds refill stamina, so costs are read across the target answer alone.

The first gated build failed: `Spellbook-drover-type.patch` had no tab after its path, which has spaces, so `patch` could not find the file. Fixed in
`p795patches.py`.

## TazUO proof

`notes\cc-P795-shots\`, real TazUO on the private proof shard, a copy of the bot world, so an existing world. Script `Shots795.py`, rig copied from
P793. On the final image all 11 checks in `walk.log` pass, and `shard.log` has no exceptions. The final run's files are dated 08:21 or later.

- `1-book-and-scrolls-in-pack.jpg`: the book in the backpack, last slot of the third row, and the three gold scrolls on the row below.
- `2-gump-corral-only.jpg`: Corral lit, the other three pages grey.
- `3-gump-all-four-pages.jpg`: after dropping the scrolls in.
- `4-corral.jpg`, `5-calm.jpg`: cast on a wild peacock.
- `6-herd-a.jpg`, `6-herd-b.jpg`: the bird stood exactly on the spot chosen (1991,2245).
- `7-lure-a.jpg`, `7-lure-b.jpg`: the bird came from 10 tiles to 1, and stands beside the character.

The first TazUO run found a clipped Herd line in the gump, so the rows are taller now. The first two runs also stopped or failed on my script: a wrong
property name, then standing 16 tiles off, past Lure's range. The blue skill lines are the proof shard's test-center mode.

**Not proved:**

- Buying from an Animal Trainer in the client. The facts prove the rows, their prices, and that each row makes its item.
- Lure with a wall in the way, in the client. The fact proves the target does not check line of sight.
- A real save and restart. The round-trip facts cover the book and scrolls.
- The fight stopping in the client: the peacock was not attacking. The fact proves it.

## Deviations and decisions for Chase

- **A step was denied and not done.** While the run was unattended, a compound command was denied. It included `rm -rf ../cc-P795-shots` from
  `notes\cc-P795-tools`, to clear the first proof run's shots before the rerun. The denial named no step, so that delete is my best guess at the
  cause; I did not retry it, and ran the other steps separately. **Result:** `frame-004.jpg` to `frame-024.jpg` in `notes\cc-P795-shots\` are stale
  timed frames from the first run (dated 08:03 to 08:13), showing the older gump layout or a stalled script. They prove nothing and can be deleted.
- **Herd may train fast.** It rolls once per animal, as you approved, so a full herd is up to 10 rolls for 15 stamina. It is worth a look if players
  reach 200 too quickly. Lowering `herdCountDivisor`'s reach would mean raising that setting; there is no separate limit on gains per cast.
- **Corral rolling** (a failed Corral costs stamina) was my reading of the design. Chase can say otherwise.
- **Main moved.** This branch sits on `b72f964`; main has P794 merged since. P794 touches none of the three patched files, and the integrator's merge
  will run the gate. VERSION here is 2026.11.05, later than main's 2026.11.04.3.

## Credits

Book, gump, registry and base-spell structure after Hammerhand's druid-spell-system pack, as reference only, no code taken. Credited in the CHANGELOG.

## Files

- **ShatteredLegacy:** new `server/customizations/Drover/` (7 files), `server/tests/Drover/DroversHandbookVerification.cs`, the 3 patches; changed
  `docker/uo/apply-patches.sh`, `CHANGELOG.md`, `VERSION`.
- **shard-migration:** this file, `notes\cc-P795-tools\`, `notes\cc-P795-shots\`.

P795 DONE
