# Architecture chat pass-down, 2026-10-01

For a new chat owning the architecture of Shattered Legacy. Read `claude/shattered-legacy-state.md` in
the project for the stable picture of machines, repos and standing constraints; its numbering and task
sections are from 2026-09-29 and are stale, and `notes\passdown-overseer-2026-10-01.md` corrects them.

**Do your own reading.** Everything below is a pointer, not a summary to inherit. The repeated failure
on this project is asserting from memory or from a brief instead of reading the code, and it has
produced a wrong shard diagnosis, a wrong save-corruption hypothesis, three wrong facts in a brief that
cc-P13 had to correct, and a claim that a feature still needed building when cc-P18 had shipped it.
Cite file:line.

## The boundary

**You own:** the instruments and their reliability (D39, D33, D24, D20, `tools/content_index.py`); the
test host's truths (D27, D15, D16); `docs\subsystem-policy.md` and `docs\patch-backlog.md`; whether a
proposed patch to pinned is the right call; the deviation register, all 91 of them; build cost and the
runtime image (D4, D6).

**You do not own:** the prompt queue, prompt numbering, bug triage, or client test results. Those stay
with the overseer chat. **You produce findings and verdicts; the overseer schedules them.** That keeps
you out of the one-builder-at-a-time contention for `D:\ShatteredLegacy` entirely.

**Numbering:** do not claim a `cc-PNN` number yourself. Two tasks were both called P21 once already.
Ask the overseer for a number, because the commit script's archiver matches prompt files to notes files
by exact name.

## Your first job

Decide whether we build a reachability instrument that checks preconditions, and if so, spec it.

Read `notes\reachability-audit.md` and `notes\cc-P12-audit-correction.md` first. The state to
understand, and the distinction matters:

- **The orphan count is exact and trustworthy.** 340 of 570 ported content files, 60 percent, are in no
  player's reach at HEAD (`reachability-audit.md` sections 1 and 3). The earlier figure of 219 of 768
  was superseded: the 219 were confirmed 219 of 219 with **zero false orphans**, and 121 more were
  found. Nothing here is in doubt.
- **The remediation estimates are not.** D39: of 27 gates, 292 predicted files became 227 on
  restatement, of which **70 were actually delivered**. The headline planning figure "gates 1 to 5:
  117 files, 31 percent" was really 65 files, 17 percent. Nine gates have been built or attempted, not
  the four the original row claimed.
- **The cause is one sentence, and cc-P12 wrote it:** the instrument finds the code site that would put
  a type in the world and stops there, never asking whether that site's own preconditions are met.
  Gate 5 and blacksmithy hit their numbers exactly because their sources are terminal. Gate 11 looks
  like the cheapest remaining unit and is the shape that has already failed three times.

So the standing advice, "port no more content except decoration", rests on the **solid** number. What
is unreliable is every estimate of what it would cost to make the existing 340 reachable, and that is
what scoping keeps being done against. P2 proposed `content_index.py reach` as the instrument
(`notes\backlog-remeasure-2026-09-28.md` section 6.1, about 60 lines).

The question for you is whether that instrument is worth building, what it must check to be worth
trusting, and how we would know it is right this time. A gate-by-gate verdict with no instrument is
also an acceptable answer if you can argue it.

## Why this is about to matter more

cc-P20 (`notes\cc-P20-skill-scaling-research.md`, 236 KB) surveyed all 58 skills and the revised F-12
design (`notes\f12-levels-loops-caps.md`) came out of it. The F-12 build will be the largest on this
project, and it lands on your territory:

- **Rank 4**, about 8 pinned files of patches, closing chance-based exploits that are live today.
- **Rank 7**, patches across about 25 pinned files, routing runaway magnitudes through a soft curve.
- Serialization versioning on `ClusterFAccountData` (already at v15 from cc-P18's per-character guild
  data), for the new per-character max level record.
- A proposed way to avoid patching `SkillCheck.cs` at all for per-stat ceilings, using stat locks
  rather than the global `_statMax`. **That trick wants your verdict before anyone builds on it.**

Every one of those patches is applied by `docker/uo/apply-patches.sh` at `--fuzz=0`, so a patch whose
context drifts by one line fails the build. Thirty-odd new patches is a step change in how exposed we
are to pinned moving, and nobody has written down what we do when it does.

## The other thing nobody owns

**D27: every item built in a shard test reads tiledata row 0**, so every piece of armor is
`Layer.Invalid` and goes to the backpack instead of being worn. That means the test suite cannot catch
equipment layer bugs. It is very likely why D26 and D28 sat in the open section of `bug-list.md` while
their fixes were already in the tree, found only on 2026-10-01 because the state doc and the bug list
disagreed. Fixing D27 makes the build gate able to catch a class of bug it is currently blind to.

## Standing constraints that bind you

- `D:\UO\ModernUO-pinned` (7c9215d97) is the only authority on engine behavior. ServUO pub57 is a
  content source and **never** an authority on engine behavior. That confusion has withdrawn seven
  deviation entries; `bug-list.md` section 1b is the standing record.
- Agents never edit `docs\`. Findings go in `notes\`.
- Agents never deploy. Chase owns every deploy decision and runs every commit and push.
- A patch to a pinned file needs its alternatives argued in `notes\` first, per AGENTS.md, and an
  `apply_patch` line in `docker/uo/apply-patches.sh`.
- ASCII only, no em dashes. American spellings.
