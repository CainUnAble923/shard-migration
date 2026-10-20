# cc-P172: pets learn faster with the owner's loops, taming skill and Outriders rank

Copper Golem, 2026-10-20, branch `golem/Copper/P172` (both repos). Chase, 2026-10-18 14:43, test shard, training a pet
Giant Spider: "pet skills do not increase rate... that should be something that increases in speed after
loops/skill/outriders rank".

## Headlines

- **A player's pet now rolls its skill gains at up to 3x pinned's chance.** The multiplier is
  `1 + loops x 0.1 + 0.004 x (Animal Taming above 100 + Animal Lore above 100, each counted to 200) + Outriders rung x 0.1`.
  It is never below 1 and capped at 3.0. The hook sits inside pinned's own controlled-creature branch
  (`SkillCheck.cs:140-143`, d4531cd9, the `gc *= 2`). That makes the roll likelier but never a free gain. It covers every
  pet skill, including Focus while training (cc-P130), and an uncontrolled creature never reaches it.
- **Defaults:** a fresh tamer's pet stays at x1.0. 120/120 is x1.16 and 200/200 is x1.8. A 200/200 Legendary Outrider
  with no loops is x2.4, and 6 loops brings it to the cap: **x3.0, three times a fresh tamer's**.
- **Loops are still F-12's stub.** They are read through the same source as evo pets, `EvoPet.OwnerLoopsSource`, which
  returns 0 until F-12 sets it. An evo pet reads its own `OwnerLoops`, which is that source or staff's `[EvoPet loops`
  stand-in. Until F-12 lands, a real master tops out at **x2.4**.
- **The owner sees it** on the Animal Lore gump's three skill pages (Combat Ratings and both Lore & Knowledge pages): a
  "Learns x2.4" at the right of the heading, shown for any pet a player controls.
- **Tests:** 28 new cases in `PetGainSpeedVerification`, each seen red first (a stub, then a mutation of the hook). Full
  build: `Built sl-modernuo:cc-P172 with patches applied and 1573 shard test(s) passing` (0 failed, 4 skipped).

## What changed

`D:\ShatteredLegacy`:

| File | Change |
|---|---|
| `server/customizations/ClusterFPetGainSpeed.cs` (new) | the rule and its four settings. `Configure` `:36-42`, `OwnerSkillBonus` `:45-46`, `Multiplier(loops, taming, lore, rank)` `:49-54` (clamped to [1, max]), `Multiplier(Mobile)` `:57-65` (1 unless `Controlled` with a `PlayerMobile` `ControlMaster`; skills read as `Value`), `OwnerLoops` `:68-69` (an evo pet's `OwnerLoops`, else `EvoPet.OwnerLoopsSource`), `OutridersRank` `:75-100`, `Describe` `:103` |
| `server/patches/SkillCheck-pet-gain-speed.patch` (new) | one hunk at pinned `SkillCheck.cs:140-143`: after `gc *= 2;` in the `BaseCreature { Controlled: true }` branch, `gc *= ClusterFPetGainSpeed.Multiplier(from);` |
| `docker/uo/apply-patches.sh:686-691` | the patch applied after `SkillCheck-pet-focus-gain.patch` (same file, the other hunk), with the reason it is a patch |
| `server/customizations/Services/Pet Training/Gumps.cs:267, :287, :307, :517-524` | `AddGainSpeed` on pages 5, 6 and 7 of `NewAnimalLoreGump` (the skill pages): `<div align=right>Learns x…</div>` at (160, 74, 120, 18), only for a pet a player controls |
| `server/tests/Skills/PetGainSpeedVerification.cs` (new) | the facts below |
| `server/tests/Services/PetTraining/PetTrainingVerification.cs:202, :204, :216` | `WireGump`, `Inflate`, `OnTheWire` changed from private to internal so the new gump fact can decode the gump on the wire. No behavior change |
| `CHANGELOG.md`, `VERSION` | `## 2026.10.20.3`: one Changed line and one Staff line (the settings). VERSION goes from 2026.10.20.2 to 2026.10.20.3; .2 was already committed |

`D:\UO\shard-migration`: this note; `testing\playtest-steps.json` (P172-1); `testing\bot-triage.md` (`### P172`).

### Why a patch, and why there

`gc` is a local of the static `SkillCheck.CheckSkill` (pinned `:108-159`), so no event or virtual reaches it. The shard's
`ClusterFSkillGain` wrapper only boosts players (`ShouldBoost` requires `from.Player`) and adds extra attempts. It can't
scale a creature's chance, and a second attempt would be "more rolls" rather than "a likelier roll". Placing the hook in
the controlled branch means:
- an uncontrolled creature is untouched by construction;
- the floor (`gc < 0.01`, `:135-138`) and the "Base below 10 gains regardless" rule (`:120-123`) stay pinned's;
- Focus for a pet in training goes through the same `CheckSkill`, so it is covered too.

### The rank

The Rangers' League key is `rangers`. Its ladder is the seven-rung one (`ClusterFGuildSystem.RankThresholds`: 0, 1,000,
5,000, 15,000, 40,000, 80,000, 150,000), running Wanderer, Scout, Outrider, Trailblazer, Beastmaster, Warden of the
Wild, Legendary Outrider. I used the rung (0 to 6), not `GuildRankIndex`, because that folds both Beastmaster and Warden
into 4. That way every Outriders rank counts. The rung only counts while the owner is a member (`IsJoined`). The
Apprentice task's bump counts as Scout, the same bump `GetRankName` shows.

## The table (defaults, printed by `TheTable`)

| Owner | Multiplier |
|---|---|
| fresh (100 / 100, no loops, not an Outrider) | x1.00 |
| 120 / 120 | x1.16 |
| 150 / 150 | x1.40 |
| 200 / 200 | x1.80 |
| Outriders rung 0 Wanderer (100 / 100) | x1.00 |
| Outriders rung 1 Scout | x1.10 |
| Outriders rung 2 Outrider | x1.20 |
| Outriders rung 3 Trailblazer | x1.30 |
| Outriders rung 4 Beastmaster | x1.40 |
| Outriders rung 5 Warden of the Wild | x1.50 |
| Outriders rung 6 Legendary Outrider | x1.60 |
| 1 / 2 / 3 / 4 / 5 loops (100 / 100) | x1.10 / x1.20 / x1.30 / x1.40 / x1.50 |
| 6 / 7 / 8 / 9 / 10 loops (100 / 100) | x1.60 / x1.70 / x1.80 / x1.90 / x2.00 |
| 200 / 200, Legendary Outrider, 0 loops | x2.40 |
| … 1 / 2 / 3 / 4 / 5 loops | x2.50 / x2.60 / x2.70 / x2.80 / x2.90 |
| 200 / 200, Legendary Outrider, 6 loops | **x3.00 (the cap)** |

The inputs add, so they can be mixed: for example 160 Taming, 140 Lore, Trailblazer and 2 loops is x1.9 (a test case).
On top of this is pinned's own x2 for any controlled creature, which applies to fresh and master alike.

What it means in a roll: a Grey Wolf at Wrestling 90 / 100 has a pinned chance of about 0.43 per failed check (the test
prints 0.426). At x3 that is above 1, so every such check gains. Lower in the skill, where pinned's chance is already
high, the cap is reached sooner; near a skill's cap the chance is small and x3 matters most.

## Tests

`server/tests/Skills/PetGainSpeedVerification.cs`, 28 cases:

1. `TheMultiplierForEachInputAndTheCap` (14 cases): fresh, below 100, 120/120, Taming alone, Lore alone, 200/200,
   above 200 (counts as 200), rung 1, rung 6, 1 loop, 5 loops, the cap exactly (6 loops at 200/200 Legendary), past the
   cap (20 loops), negative inputs (never below 1).
2. `TheFourSettingsAreRead`: `clusterf.petGain.perLoop`, `perSkillPoint`, `perRank`, `maxMultiplier`, through
   `Configure`; the cap applies, and a cap below 1 is 1.
3. `TheOutridersRungFollowsTheLadder` (8 cases, every threshold and 999) and `ARealOwnersInputsReachThePet`: a real
   owner's skills, rung and loops (through `EvoPet.OwnerLoopsSource`) reach `Multiplier(pet)`. Standing without
   membership counts nothing, and the Apprentice bump counts as Scout.
4. `AnUncontrolledCreatureIsUnchanged`: multiplier 1 for a wild wolf, even with a 200/200, 20-loop Legendary Outrider
   standing next to it. A player is not a pet either. With a fixed random, pinned's uncontrolled roll misses just above
   pinned's chance and gains just below it.
5. `APetsGainChanceRisesWithTheMultiplier`: a fixed random roll at 1.5x pinned's controlled chance. The fresh tamer's
   pet misses it and the master's pet (x3.0) gains. With the cap at 1.2, the same roll above the raised chance gains
   nothing, while a roll at 1.15x still gains.
6. `TheTable`: the table above.
7. `TheLoreGumpShowsTheGainSpeed`: the gump decoded off the wire has "Learns x3.0" exactly three times, once per skill
   page.

**Seen red first:**
- **Stub** (`ClusterFPetGainSpeed` returned 0 from both `Multiplier`s and -1 from `OwnerLoops` and `OutridersRank`; the
  patch in place): **27 failed, all PetGainSpeed, nothing else** (1546 passed). Every fact went red: the gump showed
  "Learns x0.0", and the uncontrolled multiplier was 0 against 1. `TheTable` only prints, so it was never meant to be
  red.
- **Mutation** (the real class, with the hook made a no-op: `gc *= 1.0 + 0.0 * Multiplier(from)`): **1 failed**,
  `APetsGainChanceRisesWithTheMultiplier` at `RollOnce(masterPet, roll)` (`:315`). That is pinned's behavior: the
  master's pet missed the roll. This is the fact that proves the patch itself.
- **Restored after each:** both the class and the patch were copied back from the scratchpad, `cmp` confirmed them,
  and `grep RED STUB / MUTATION` finds nothing.
- **First compile** failed on a missing `using Server.Gumps` (the `SendGump` extension), my own mistake, and was fixed.
- **Final:** `bash docker/uo/build.sh -t sl-modernuo:cc-P172` gave **1573 passed, 0 failed, 4 skipped**, and the image
  was built. The table and gump strings come from a separate filtered `dotnet test` with detailed logging in the built
  `sl-uo-builder:cc-P172`.

## Play-test items added

One, P172-1, under **For Chase** below. Sorted **BOT** in `testing\bot-triage.md` (`### P172`): the "Learns x" line is
gump text and Wrestling is a skill value the server sends. It has steps and a check line in
`testing\playtest-steps.json`.

## Deviations and decisions for Chase

1. **"About 3 times as fast" needs loops.** With F-12 still stubbed (loops read 0), the best a real player reaches
   today is **x2.4** (200/200, Legendary Outrider). The defaults reach exactly x3.0 at 6 loops. If you want x3 now,
   raise `perRank` to 0.2 (Legendary alone gives +1.2) or `perSkillPoint` to 0.006, and the cap still holds at 3.
2. **The 3x is relative to a fresh tamer's pet, on top of pinned's x2 for any pet.** A master's pet rolls at up to 6x
   a wild creature's chance. A chance above 1 is simply a certain gain on that check; the amount per gain is pinned's
   (0.1, or 0.1-0.4 below 10).
3. **Rank uses the 7-rung Outriders ladder, not `GuildRankIndex`** (which merges Beastmaster and Warden into 4), so
   every Outriders rank adds. Non-members get 0 even with standing.
4. **Owner skills read as `Value`** (worn bonuses count), as cc-P171 and pinned's taming checks do, and each is capped
   at 200.
5. **Never below x1**, even if someone sets `maxMultiplier` under 1, so the settings can't make pets slower than pinned.
6. **Where it shows:** the Animal Lore gump's skill pages, not the pet's properties line. BaseCreature's
   `GetProperties` is pinned's and a partial class can't override it, so a property line would need another patch.
   The gump line is checked on the wire, but not by eye: the text box (160-280) overlaps the heading's box (47-207). The
   right-aligned text sits at about x 210-280 and the headings end before 160, so they should not collide. Say if it
   looks wrong in game.
7. **Stats are unchanged.** Pinned's pet stat gain (`stats.petGainDelay`) is a separate path and was not asked for.
8. **`tools/progress.py` was not run.** On this laptop it refuses: "cannot see ServUO scripts at D:\UO\ServUO-pub57
   (set SL_SERVUO)". So `README.md`, `dashboard.html` and `tools\progress.json` were not refreshed; the integrator's PC
   can do it.
9. **No task-list tool exists in this session**, so per-step progress went into the chat instead.
10. **Not deployed:** I did not rebuild or restart the test shard. The image `sl-modernuo:cc-P172` (and
    `sl-uo-builder:cc-P172`) exists on this laptop (Copper); `latest` was not moved.

## For Chase

Rebuild the test shard from HEAD after the merge.

**The four settings** go in the test shard's `modernuo.json`, written with the defaults on first start
(`GetOrUpdateSetting`) and read at start, so restart after a change:

| Setting | Default | What it does |
|---|---|---|
| `clusterf.petGain.perLoop` | 0.1 | added per owner loop (loops are 0 until F-12) |
| `clusterf.petGain.perSkillPoint` | 0.004 | added per point of Animal Taming and of Animal Lore above 100 (to 200), so +0.4 per skill at 200 |
| `clusterf.petGain.perRank` | 0.1 | added per Outriders rung (Scout 1 to Legendary Outrider 6), members only |
| `clusterf.petGain.maxMultiplier` | 3.0 | the cap; 1.0 turns the whole feature off (pinned's behavior) |

To try it in game:

1. **Compare a fresh tamer's pet with a master's:** two characters, each with a freshly tamed Grey Wolf: a fresh tamer
   (Taming and Lore at 100 or less, not in the Rangers' League) and a master (200.0 Taming and Lore, joined the
   Rangers' League, then `[GuildStanding rangers 150000` on them). Use Animal Lore on each wolf and open the Combat
   Ratings page; `[set` both wolves' Wrestling to 50 and let each fight the same weak creatures for 10 minutes; lore
   them again. **Pass:** the fresh tamer's wolf shows "Learns x1.0" and the master's "Learns x2.4" (x3.0 once loops
   exist). After the same fights, the master's wolf has gained clearly more Wrestling, about two to three times as
   much.

## Repo size rule

No file over 5 MB in either repo. The new files are source; the largest, `PetGainSpeedVerification.cs`, is about 15 KB.
Build logs, the stub and mutation copies, and the pinned SkillCheck extract stayed in the session scratchpad, outside
both repos.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`:

```
Repo Result
---- ------
code dry run
docs dry run
```

Code: the 8 files in the table under What changed. Docs: this note, `testing\bot-triage.md` and
`testing\playtest-steps.json`. Nothing BLOCKED.

P172 DONE
