# What upstream ModernUO is actually working on

**Observed 2026-09-07 from the ModernUO Discord `#code-updates` channel, which mirrors the
GitHub activity feed. Every item below is a commit, PR or branch name from that feed.**

> **This is a hypothesis file, not an evidence file.** Per `AGENTS.md` ground rule 4, nothing
> here justifies a decision on its own. Branch names and PR titles say what someone *intends*.
> Verify anything you act on in `D:\UO\ModernUO-pinned`, or in the upstream repo at the commit
> you would actually bump to, and cite file and line.

## The headline: nobody upstream is doing content

Every PR and branch active on 2026-09-06, the day before this was read:

| Work | What it is |
|---|---|
| Delta Saves, project #7, PRs #2608 #2609 #2610 | skip clean entities during the save freeze |
| #2612 world save failure handling | no partial snapshots, staged publication |
| #2615 OPL revision hash collisions | `AddHash` XOR was commutative and self-inverse |
| #2611 `BaseCreature` to the SerializationGenerator | **merged to main** as `392c4e1` |
| #2613 pet release, summon master, horse breeder | **merged to main** as `ab738d9` |
| #2614 pet orders resolve in one place | open |
| #2592 `SpeedClass` + ControlMaster/SummonMaster collapse | open, behaviour changes |

**Not one line of expansion content.** It is all engine correctness and save performance.

**This is the strongest evidence yet that the project's direction is right.** Nobody is going to
build Eodon, Pet Training abilities, armour set bonuses or High Seas for us. Porting content
ourselves is not duplicating someone else's effort, it is the only path to that content, and it
is complementary: they maintain an engine that keeps getting better, we bring the content.

It also means the missing subsystems in `docs/subsystem-policy.md` are **not** "not built yet
but coming". Treat them as permanently ours to build or decline.

## The risk: `BaseCreature` is being rewritten right now

Every creature we port derives from `BaseCreature`, and our pinned commit is `7c9215d97`.

- **`BaseCreature` moved to the SerializationGenerator and is already on `main`.** A future bump
  crosses that.
- **`SpeedClass` is an open behaviour change** in #2592, alongside a commit titled "collapse the
  move-speed properties". **This is the subject of our Q-008**, where we decided ported creatures
  take ModernUO's `Medium` fallback. That decision rests on how `SpeedClass` and
  `Data/npc-speeds.json` behave today. **Re-verify Q-008 before and after any bump.**
- `ControlMaster`/`SummonMaster` collapse into one reference: matters for anything we port that
  is tameable or summoned.
- The OPL revision hash fix touches property-list hashing. **S1 adds set-bonus property lines to
  armour**, so it is worth confirming our lines still hash as expected after a bump.

## What this means for bumping `MODERNUO_COMMIT`

Upstream is committing daily and is mid-refactor on the exact class our content sits on. So:

1. **Do not bump casually, and never as a side effect of another task.** A bump is its own task
   with its own verification.
2. **`notes/s1-armour-sets.md` section 3 is the checklist** for the three patches. Read it first.
   The core patch into `Mobile.ComputeResistances` is the highest-risk item.
3. **Run `docker/uo/build.sh`.** The S4 test route exists precisely so a bump that leaves patches
   applying but behaviour broken gets caught.
4. **Re-check Q-008** specifically, per the `SpeedClass` work above.
5. Waiting for the delta-saves project and the `BaseCreature` refactor to settle is a defensible
   reason to stay on `7c9215d97` for now. Nothing we want is in those changes.

## Worth reporting upstream, unrelated to any of this

The ModernUO `SetPassword` bug found during P1 and verified three ways. Under SHA1 or SHA2 a
brand-new account's hash is stored with the wrong phrase, because `_passwordAlgorithm` is still
the enum default at the first `SetPassword`, so `CheckPassword` can never match. Full write-up in
`notes/cc1-p1-runtime-validation.md` and Q-007. It does not affect us any more, since the SHA2
entrypoint block is reverted, but it is a real upstream defect and cheap to hand over.
