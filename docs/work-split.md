# Work split: Claude and Codex

Written 2026-09-06. The split is driven by two hard constraints, not by preference.

## The two constraints

**1. Codex can compile. Claude cannot.**
Verified: the Claude sandbox has Mono (C# 7.3 compiler max, too old for ServUO's syntax)
and .NET SDK 8, but nuget.org is blocked by egress policy and Mono ships no 4.8 reference
assemblies. ServUO targets `net48`. So **anything whose acceptance test is "it builds"
belongs to Codex.**

**2. Codex's context budget is the scarce resource. Claude's is not.**
So **anything whose cost is reading a lot to produce a little belongs to Claude.**

## The consequence: separate "figuring out" from "making it build"

Porting one script has two costs:

- **Research** — what is the ServUO equivalent API, does ServUO already have this, what
  changed in the type, what does the serialization look like. Context-heavy, no compiler
  needed.
- **Verification** — does it actually compile and behave. Cheap in context, needs a build.

Doing both in one agent means paying Codex's scarce tokens for the expensive half. Split
them and Codex's per-file cost drops to reading a prepared diff and running a build.

**The pattern:** Claude writes the port and a short note naming the exact ServUO APIs used
and anything uncertain. Codex builds it, fixes what the compiler complains about, commits.

## Assignments

### Codex owns

| Work | Why |
|---|---|
| **Baseline recovery** (CraftContext members, ResourceInfo wood enums, OutridersGuildmaster) | needs a compile loop to know when it is done. **This is the critical path.** |
| Building and fixing ported scripts | needs `dotnet build` |
| `apply-patches.sh` — make it fail on failed patches | needs to run the container build |
| Docker, entrypoint, compose, deployment | needs the local Docker daemon |
| Anything touching the live shard | needs the machine |
| Running `tools/progress.py` at session end | trivial, keeps the number honest |

### Claude owns

| Work | Why |
|---|---|
| **Port triage** — classify all 111 files by difficulty and produce the port order | read 37,581 lines to produce one table |
| **Pre-written ports** — draft the ServUO version of each script | context-heavy research, no compiler needed |
| **Patch triage research** — for each of the 11 patches, does ServUO already have the behavior | cross-reading two large trees |
| Cross-codebase API lookups | cheap for Claude, expensive for Codex |
| Docs, `AGENTS.md`, decision records, the question queue | no build involved |
| Tooling that does not need compiling (`progress.py`, the accounts exporter) | no build involved |
| Reviewing Codex's work before commit | catches what a build cannot, e.g. the inclusive/exclusive geometry check |

### Shared, with a rule

`shard-migration` is written by both. `docs/` is Claude's. `notes/` is Codex's. Either may
read anything. Commit and push before handing off.

## What this means right now

Codex should not be writing tooling. The three baseline gaps block all 111 content ports,
and nothing else moves until they close. That is Codex's next task and it is the only thing
on the critical path.

Claude should be producing the port triage table and pre-written ports, so that when the
baseline compiles there is a queue of prepared work rather than 111 files of research still
to do.
