# cc-P860: a live ridable polar bear (the ice bloodline source)

## In plain words

- **Ridable polar bears now live on Dagger Isle's snow** (north-east of Minoc, Trammel). There are two dens, with two
  bears each, and they come back 20 to 40 minutes after one is tamed or killed. They appear on the live world by
  themselves after the next restart.
- **Tame one with Animal Taming 59.1 and ride it.** It looks like a polar bear and fights like one. The leash shrinks
  it to the polar bear figurine. Its tooltip says it follows Milva's ridable polar bear.
- It is the ice line's first mount for pet breeding, made from art every player already has: no new art and no
  client update.
- **For you:** the download's numbers were a horse's (tame 29.1). I set a tame of **59.1** and **1 control slot**,
  because a mount that starts a bloodline should take some taming. Say if you want them higher, for example the
  nightmare's 95.1 and 2 slots. It is not trainable yet: our pet training table is kept exactly ServUO's, as for the
  Peacock.

Iron Golem, 2026-11-10. Code copy `D:\UO\golems\Iron\ShatteredLegacy` and docs copy on `golem/Iron/P860`. Main only;
nothing on the isle branch. The download `D:\UO\third-party\code\ridable-polar-bear\` (Milva, servuo.dev 2013) was read
as reference; nothing built, run or copied from it.
- Read first: P853's assessment (item 2), `design/systems/pet_progression_breeding.md` (the code copy's), and the
  Peacock (cc-P793) as our own mount and spawn pattern.
- The claude.ai project doc `claude/pet-breeding-design-notes.md` is not on this disk (P853 found the same). I worked
  from the prompt's summary of it.

## What was built

- **`server/customizations/Mobiles/Mounts/RidablePolarBear.cs`** (new, ours): a `BaseMount` on stock art, body 213
  (the polar bear, typed Animal in pinned's `bodyTable.cfg`) and mount item 0x3EC5 (the ethereal polar bear's, pinned
  `Ethereals.cs`).
  - **Numbers:** the polar bear's fighting numbers (pinned `PolarBear.cs` and the download agree): strength
    116-140, hits 70-84, damage 7-12, cold resist 60-80, and so on. Also its food (fish, fruit, meat), its pack
    instinct, 2 meat and 16 hides.
  - **Three changes from the download:**
    - an animal's AI that only fights back, as pinned's polar bear (the download's attacked the nearest thing);
    - a tame of **59.1** (the download's 29.1 is a horse's, below a plain polar bear's 35.1);
    - one control slot, as both have.
  - **Credit:** the tooltip says "After Milva's ridable polar bear", and `Credit = "Milva"`.
  - Serialization is generated.
- **`server/customizations/Mobiles/Mounts/RidablePolarBearDens.cs`** (new; the Peacock's `PeacockSystem` shape):
  - **Dens:** two on Trammel, each a spawner of two bears, home range 10, every 20 to 40 minutes: **Dagger Isle,
    north snowfield 4090,325,0** and **west snowfield 3963,508,0**.
  - **Why there:** the SoS land keeps Dagger Isle's snow where Britannia has it, and pinned's own polar bear spawns
    sit at these spots (`Data/Spawns/shared/trammel/Outdoors.json`). Both spots are flat snow with no static within
    10 tiles (read from the SoS land and statics), and clear of every SoS fence (the north-east snow isles' fence
    starts at x 4224).
  - **Existing worlds:** on the tick after every world load, each den gets its spawner if it has none, so a live
    world has the bears after its next start and a second load adds nothing. Staff can check it with
    `[PolarBearDens status | seed [dryrun]`.
- **`CHANGELOG.md`** and **`VERSION`: 2026.11.10.6**. Main is at .2; P869, P872 and P871 hold .3, .4 and .5.
- **Pet training:** no row. I first gave it the polar bear's row in `PetTrainingHelper`, and the gate's
  `PetTrainingVerification.TheTablesAreServUOs` (the table stays exactly ServUO's 137 rows) failed
  (`gated-build-1-training-row.log`). I took the row out. It is untrainable, as our Peacock and every other mount of
  ours that ServUO does not list.

Nothing grants skill or stat points: the bear carries nothing, drops no loot and has no treasure map level.

## Tests

`server/tests/Mobiles/Mounts/RidablePolarBearVerification.cs`, eight facts:

1. Body 213 (Animal, opens no doors), mount item 0x3EC5, its name, the polar bear's numbers, tame 59.1 (above the
   plain bear's), one slot, the polar bear's food and pack instinct, untrainable (no row), Milva credited.
2. A real tame (Animal Taming's own target and timer, a 120 tamer) makes it the tamer's.
3. Its owner rides it (the worn mount item is 0x3EC5) and dismounts; a stranger cannot ride it.
4. It round-trips the generated serializer, tamed and while ridden.
5. The leash shrinks it to the polar bear's figurine 0x20E1, and it comes back.
6. A dry run places nothing; the seed gives each den one spawner of ridable polar bears on Trammel (count, home range,
   delays); a second seed adds nothing.
7. Every den is on Dagger Isle, and no den's home range touches an SoS fence.
8. It carries nothing and grants nothing.

**Watched red, then green** (`notes/cc-P860-tools/red-all.txt`; `red-all.sh`, one container on `sl-uo-builder:bot`):
- **The code before the change** (`red/stub.cs`: only the names the facts use, all inert): **6 of 8 failed**. Facts 7
  and 8 pass there vacuously (no dens, an empty bear), so each has a mutant:
  - `m-fence-dens` (a den moved under the snow isles' fence): fact 7 red;
  - `m-loot-bear` (gold in its pack and a treasure map level): fact 8 red (and fact 5).
- **Green:** 8 of 8 on the real code.

**Gated build** (`notes/cc-P860-tools/gated-build.ps1`: docker-build lock, page cache dropped first, `latest` not
moved; log UTF-16): `sl-modernuo:cc-p860` **EXIT=0, 3373 passed, 0 failed, 6 skipped**, the eight bear facts among
them (`gated-build.log`). The first build (`gated-build-1-training-row.log`) was the training-row failure above.

## In game (TazUO, `notes\cc-P860-shots\main\`)

Private proof shard (2596) only, under the test-shard lock, on a fresh copy of the bot world on `sl-modernuo:cc-p860`
(`run860.ps1`, kit in `notes/cc-P860-tools/kit`, P859's repointed, with `Walk860.py`).
- The trainee "Iron Frost" is on a Player account.
- Staff hands (`stage860.py`) only did this: blessed the trainee, moved them to the den, set Animal Taming and Animal
  Lore to 100 (and read the skill back: `AnimalTaming : 100 (Base: 100)`), handed over a leash, and ran
  `[PolarBearDens status`.
- Everything else is the trainee's own client.

**Every check PASS** (`walk.txt`):
- The dens were seeded by themselves on this world copy: both spawners there, four bears (`stage-out.txt`).
- A wild ridable polar bear stands at the den; its tooltip reads "a ridable polar bear | After Milva's ridable polar
  bear".
- Animal Taming tames it.
- **Riding: the mount layer is 0x3EC5.**
- Dismounted, it is back on the snow.
- The leash makes the polar bear figurine 0x20E1.

Shots:
- `p860-1-wild-bear.jpg`: the den with wild bears.
- `p860-2-tamed.jpg`, `p860-3-following-*.jpg`: the tamed bear following.
- **`p860-4-ridden.jpg`** and **`p860-5-ridden-walking-*.jpg`**: the trainee riding the polar bear across the snow
  (the rider sits on the bear's body as it walks).
- `p860-6-dismounted.jpg`, `p860-7-figurine.jpg`.

**Run 1** (`cc-P860-shots/run1-no-skill/`, kept) failed the tame with "You have no chance of taming this creature."
- The skills had been set before the trainee was moved off the Wakening Isle, and leaving the isle resets a new
  character's skills.
- Run 2 sets them on Dagger Isle and reads them back; everything passed.
- Run 1 already showed the dens seeded by themselves and the wild bears drawn.

## Deviations and decisions for Chase

- **Tame 59.1, 1 slot** (the prompt gave no numbers; P853 said the download's were a starter animal's). They are
  constants in `RidablePolarBear.cs`; say if the ice line's source should ask for more.
- **Untrainable for now:** pet training keeps ServUO's table exactly (a gate). Making it trainable means changing
  that rule.
- **Free memory** read 2.8 GB when the second gated build started, a little under the prompt's 3 GB. The build drops
  the page cache first and finished green; I did not wait the 30 minutes.

## Files

- `ShatteredLegacy`: `server/customizations/Mobiles/Mounts/RidablePolarBear.cs` and `RidablePolarBearDens.cs` (new),
  `server/tests/Mobiles/Mounts/RidablePolarBearVerification.cs` (new), `CHANGELOG.md`, `VERSION`.
- `shard-migration`:
  - this file;
  - `notes/cc-P860-tools/` (red stub and mutants, red-all.sh and its results, gated-build.ps1 and both logs,
    build-then-run.ps1, run860.ps1, the kit);
  - `notes/cc-P860-shots/` (`main\` and `run1-no-skill\`).

P860 DONE
