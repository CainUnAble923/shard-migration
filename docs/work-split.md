# Work split: Claude and Codex

> **SUPERSEDED 2026-09-07.** Describes a two-agent split from the project's first day.
> **`how-this-works.md` is the current description** of who does what and why the line falls
> where it does.

Updated 2026-09-06 for the current direction: **the shard stays on ModernUO** and ServUO
content is pulled in selectively.

## The two constraints

**1. Codex can build. Claude cannot.**
Verified: Claude's sandbox has Mono (C# 7.3 max) and .NET SDK 8, but nuget.org is blocked by
egress policy. It cannot compile ModernUO or ServUO. So **anything whose acceptance test is
"it builds" belongs to Codex.**

**2. Codex's context budget is the scarce resource. Claude's is not.**
So **anything whose cost is reading a lot to produce a little belongs to Claude.**

## The pattern

Adding one piece of ServUO content has two costs:

- **Research** — find it in ServUO, work out its dependencies, check whether ModernUO already
  has it, check for name collisions, convert ServUO's hand-written `Serialize`/`Deserialize`
  to ModernUO's `[SerializationGenerator]` form. Context-heavy, no compiler needed.
- **Verification** — does it build and behave. Cheap in context, needs a build.

Claude does the first and hands over a draft plus a note naming the exact APIs used and
anything uncertain. Codex builds it, fixes what the compiler says, commits.

## Assignments

### Codex owns

- **The three setup defects** (recover `CraftContext` members, wood enum members,
  `OutridersGuildmaster`; make `server/customizations` compile standalone). **Critical path.**
- Making `apply-patches.sh` fail on a failed patch, then triaging the seven that fail
- Removing the stale `customizations/migrations` subfolder
- Building and fixing every ported piece
- Docker, entrypoint, compose, deployment, anything touching the live shard
- Running `tools/progress.py` at session end

### Claude owns

- **Surveying ServUO for content worth pulling**, with dependency cost per candidate
- **Drafting ports**: ServUO source rewritten into ModernUO conventions
- Checking each candidate for name collisions against ModernUO before any work starts
- Cross-codebase API lookups
- Docs, `AGENTS.md`, decision records, answering the question queue
- Reviewing Codex's work before commit

Review earns its place: it caught an inclusive-versus-exclusive geometry bug that would have
compiled fine and silently shifted every spawn area by one tile.

### Shared

`docs/` is Claude's, `notes/` is Codex's, either may read anything. Commit and push before
handing off.

## Standing rule

**Never set a Goal in Codex for this project.** A Goal runs autonomously and does not accept
steering mid-run. On 2026-09-06 that produced seven commits rewriting live ModernUO
customization files into ServUO style while the direction was being reversed. All seven were
unpushed and reverted, but the shard's own source was modified. One scoped task per chat,
with `AGENTS.md` carrying the standing context.

---

## Update: three roles, not two

Claude Code running on Chase's machine can compile, which removes the drafting/building
handoff for implementation work.

| Role | Does | Cannot |
|---|---|---|
| **Claude (chat)** | cross-codebase research, drafts, review, `docs/`, decisions, answering the question queue | compile anything |
| **Claude Code** | implementation: write, build, fix, verify, commit | decide scope; deploy to the live shard |
| **Codex** | Foundation items F1-F5 | (same boundaries) |

Do not run Claude Code and Codex in the same working tree at the same time. On 2026-09-06 a
single agent working from a stale direction produced seven commits rewriting live
customization files; two agents overlapping would be worse and harder to unpick.

The single task list for every agent is `tasks.md`.
