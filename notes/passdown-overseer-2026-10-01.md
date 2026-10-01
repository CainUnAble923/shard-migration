# Overseer pass-down, 2026-10-01

For the chat taking over the overseer role. Read `claude/shattered-legacy-state.md` in the project for
the stable picture (machines, Haven, the web stack, diagnostics, preferences). **That doc is from
2026-09-29 and its numbering and task sections are stale**; this one corrects them.

## Corrections to the 2026-09-29 state doc

- "Next free there is D30" is wrong. **bug-list's highest is D43, so next free is D44.**
- "CC tasks P1 to P3" is wrong. **P1 through P24 exist.** P4 is long done.
- Q-066 is used. Re-derive the next free numbers rather than trusting any written figure:
  `grep -rhoE "\b[DQ]-[0-9]+\b" notes docs | sort -u | tail`.
- The doc says D26 and D28 were fixed. **They were, but both rows still sit in bug-list section 1
  (Open).** Verified 2026-10-01: `BestialArms` now derives from `BaseSetArmor` with `base(0x4052)`
  rather than `GargishLeatherArms`, which was D28's cause. We also carry our own
  `customizations\CharacterCreation.cs`, which is where D26's fix would live. **Confirm both and move
  the rows to section 2.** This is a 1b-class documentation defect: a wrong note costs as much as a
  wrong line.

## Where the queue stands

| Prompt | State |
|---|---|
| P19 registrar office decor | done, committed `f49e693` |
| P20 skills past 120 research | done, 236 KB of notes, debriefed |
| P21 console world commands | done, committed. T-034's console incongruity came out of it and is back with CC separately |
| P22 small features 1 (F-16, F-19, pit thief, F-11, F-17, F-15) | **queued on disk, unblocked**, its gate (P19 and P20 done, P19 committed) is satisfied |
| P23 live defect sweep (D42, D43, D41, D13) | **running** |
| P24 New Haven dungeon research | **running**, read only, owns its own chat |
| P25 stats above 125 research | **not written, not started.** Notes only when it is; it gates the F-12 stat numbers Chase has already approved in shape |

**The concurrency rule: one builder at a time in `D:\ShatteredLegacy`.** Notes-only prompts run freely
alongside. P22 and P23 cannot overlap: they share `ClusterFGuildSystem.cs` (1,097 lines, F-11 reworks
its consume paths while D41 reads its guild key list), they share the only `QuestArrow` use in the tree
(`ClusterFGuildStarterPath.cs`, which holds "Show me the way" that D41 is rewriting and P22's pit thief
is specified to reuse), and concurrent `build.sh` runs race on `server/uo/` at `--fuzz=0`.

**So P22 runs after P23 commits**, and its thief then inherits the fixed arrow instead of needing a
follow-up.

## What cc-P20 found, in short

Storage allows skills to 1000, the game rules do not: 41 of 58 skills break by 1000 and 20 break at or
below the live cap of 300. Separately **39 of 58 skills cannot gain past about 160 by play at all**,
because each use carries a fixed `maxSkill` (`UOContent/Skills/SkillCheck.cs:58-61`). It also found two
live exploits, now filed and in P23:

- **D42**, an ingot dupe. `customizations\SmithGuildSalvageBag.cs:139-148` dropped pinned's Mining
  clamp. The return crosses the input at Mining about 143 and returns 51 ingots for a 25-ingot item at
  300.
- **D43**, the Smith Seal catalog sells Blacksmithing power scrolls up to 10,000 seals whose cap
  `ClusterFSkillCaps.Apply` wipes at the next login.

## F-12 is redesigned and recorded

`notes\f12-levels-loops-caps.md`, also in the project as `claude/f12-levels-loops-caps.md`. It
supersedes the max level 1000 design and the loop ladder in the feature queue, and the F-12 and F-13
entries carry pointers to it. Max level 200, individual skill cap equals max level, total skill cap
58 x max level, loops at 50/100/125/150/175/200, power scrolls raise the level cap, stats 125 to 200
per stat with the total scaling on current level.

**Three numbers are still placeholders and the F-12 build cannot start without Chase settling them:**
the reserve cap, the echo multipliers, and the step size above 100.

**One assumption is unverified:** nobody has surveyed stats above 125. That is what P25 is for.

## Open and owned

- **Chase:** the three F-12 numbers above. Q-009, the compose mount, still the oldest item on the
  project.
- **Unwritten:** P25, the stats-above-125 research pass. It is the one unverified assumption in the
  approved F-12 stat table, and it is notes only, so it can run alongside anything.
- **Features chat:** the League of Extraordinary Citizens pointer, a design gap under F-9, not a defect.
- **Dungeon chat (P24):** everything downstream of the dungeon research. Its gating question is whether
  TazUO can read Trammel map files out of the player package. Until that is answered the dungeon cannot
  be built, because Route 2 (real map edits) is the whole premise.
- **Still open tests:** T-039, T-041, T-042, T-044 through T-048. T-020 was closed 2026-10-01 (the phone
  requirement dropped). **T-021, the updater replace path, is waiting on a package build and publish,
  not on code**, and becomes testable on the first package after P22's F-15 adds VERSION and
  CHANGELOG.md.
- **Chase's reasoning reset, 2026-09-30, still not written into `fidelity-principle.md`:** "We will TRY
  and be as faithful to OSI as possible but we will have a lot of systems that build on OSI so in the
  end we may just have one amazing and detailed wiki." That supersedes the principle's premise that
  external wikis do our documentation.

## How this chat works

Chase does not paste CC's output. He says "P23 done" and the overseer reads
`D:\UO\shard-migration\notes\cc-P23-*.md` off disk through `device_bash`.

The repeated failure in this project is **asserting from memory or from a prompt's text instead of
reading the code.** It has produced a wrong shard diagnosis, a wrong D40 hypothesis, three wrong facts
in a brief that P13 had to correct, a claim that F-1 still needed building when P18 had shipped it, and
the D26/D28 error above. Verify before asserting, and cite file:line.
