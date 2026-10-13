# cc-P93: port assessment for the servuo.dev code downloads (2026-10-13)

## Headlines

- The full assessment is written to `D:\UO\third-party\code\PORT-ASSESSMENT.md`, with an identical copy at
  `notes\servuo-code-port-assessment.md` (the project copy; see the deviations below).
- **Vita-Nex: do not port Core.** It is 147,294 lines in 582 files (counted). Its value sits in packet rewriting and
  custom gump entries, exactly what ModernUO changed most. The release has only token ModernUO support (`#if MUO` in
  2 files). A full port is months; even the subset Power Hour needs is 3-5 weeks (guess). Power Hour itself is a
  2-4 day native rebuild. The Vault Pass is not worth buying for porting.
- **Top 5, in order:**
  1. Building Duplicator, adapted to write our layout JSON (S, staff tool, can run now).
  2. Visual Builder with recorded erase and wipe (S, staff tool).
  3. Animal Lore dashboard on the ported Pet Training (M, after the Pet Training port).
  4. Specimen star rating, rebuilt (S, after 3).
  5. League hunts on Apex Hunt's skeleton (M, after F-14 and F-24's hunt design).
- Draft prompts P94 to P98 are inside the assessment, **not** saved to `cc-prompts\queue\`, as the prompt says,
  until Chase reads it and says go.
- **Skip or idea only:**
  - Craft from bank: skip, because F-34 already has our own engine in `GuildResources.cs`.
  - Virtual storage: idea only, because of three High exploit findings.
  - Invasions: idea only (GPL-3.0, restart and wrong-map guard bugs).
  - UORespawn: idea only, because it would fight stock spawns.
  - Level System Extreme: idea only, as F-12 already ruled.
  - Runebook reordering: idea only.
  - Seagull and butterfly art: skip, it is ripped.
  - Power Hour: idea only, if wanted.
- **No client plugins** in any download.
- **Nothing is blocking.**

## How it was done

- Both repos were clean at the start (`git status --short --no-optional-locks`).
- I read the context:
  - the P92 prompt (`cc-prompts\completed\`) and `notes\port-list-2026-10-13.md`;
  - the feature queue handoff and the F-11, F-12, F-19 and F-34 entries;
  - the third-party README, `download-queue.md`, `servuo-ideas.md` and every module's SOURCE.txt.
- `servuo-ideas.md` has one row since the prompt was written: a small-character animation discussion, idea only, no code.
- Five read-only reviews ran in parallel, one per module group. I spot-checked each group's key claims myself:
  - Vita-Nex line count 147,294 and the 2 `#if MUO` files.
  - The UORespawn MUO zip on disk holds 77 .cs.
  - `using ShrinkSystem;` and the GPL-3.0 header in the Animal Lore dashboard.
  - 193 `Register("` hits, of which 2 are commands.
  - The virtual storage ADD target and withdraw code.
  - Every shard path cited in the drafts exists.
- Nothing under `D:\UO\third-party` was built, run, installed or extracted. The UORespawn zip contents were listed by
  name only.
- `D:\ShatteredLegacy` and the ModernUO trees were only read.

## Deviations and decisions for Chase

- **Project copy.** The prompt asks for the assessment "to the project as `claude/servuo-code-port-assessment.md`".
  There is no `claude\` folder on disk. Agents do not write `docs\`, which is where project docs are mirrored. So the
  copy is `notes\servuo-code-port-assessment.md`, for Chase to add to the Claude project.
- **Engine commit.** The shard runs `d4531cd94`, so citations are from that commit, not the older `7c9215d97` some
  notes mention.
- **Third-party records.** `D:\UO\third-party` is not in either repo, so `PORT-ASSESSMENT.md` there is not committed
  by autopilot. The notes copy is.
- **SOURCE.txt corrections, not made.** I found errors in several SOURCE.txt files (UORespawn's server source,
  runebook's Vita-Nex use, the bestiary count, the dashboard's GPL header, the duplicator's duplicate file, Power
  Hour's hooks). They are listed at the end of the assessment for the features overseer. I did not edit those files,
  since the prompt is read and report.
- **Vault module IPL.** It is an installer, patcher and launcher (download queue row 94), not a server module, so it
  needs no port.
- **Task list.** The hand-off asked for one task per step for Chase to follow. This session has no task-list tool, so
  progress was posted in chat.
- **No Finishing section in the prompt.** I followed the hand-off's finishing rule (this file's last line) and ran
  the commit preflight anyway.

## For Chase

The decisions the assessment needs from you are its "Open questions" section:
- go on drafts P94 to P98;
- the Vault Pass (my answer: no);
- whether virtual storage is wanted at all;
- Power Hour;
- the GPL-3.0 header on the Animal Lore dashboard;
- the bestiary bonus size against slayers;
- whether to unzip UORespawn's ModernUO scripts for a closer read;
- adding the project copy.

None of these blocks anything now: the staff tools can start whenever you say go, and the rest wait on the port
list anyway.

## Preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`

```
Repo Result
---- ------
code clean
docs dry run
```

P93 DONE
