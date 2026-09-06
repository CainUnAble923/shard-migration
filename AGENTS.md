# Working agreements for agents on this repo

Applies to any agent working here (Codex, Claude, or otherwise). Humans should read it too.

## What this project is

Migrating a live Ultima Online shard from **ModernUO** to **ServUO pub57** so it can carry
post-ML content: High Seas, Time of Legends, Endless Journey. Target scope explicitly
includes naval combat and Eodon.

Read `docs/direction-decision.md` before proposing we do it the other way. That was costed
and rejected with numbers, not vibes.

## Ground rules

1. **Decisions live in `docs/`.** If you make or change a decision, write it there in the
   same change. A decision that exists only in a chat log does not exist.
2. **Do not relitigate the direction.** Going to ServUO costs us .NET 10, source-generated
   serialization and fast saves. That trade was made deliberately for content reach. If you
   have new *evidence* that changes the math, open it as a note in `notes/` with the numbers.
3. **Never commit shard runtime data.** No `Saves/`, no `Accounts/`, no logs. See `.gitignore`.
4. **Never commit client data files.** `.mul`, `.uop` and `.idx` are huge and not ours.
5. **Verify against the source tree, not against documentation.** Neither ServUO nor ModernUO
   documents its content coverage accurately. Every content claim in `docs/` was produced by
   reading and counting files in the actual repos. Hold new claims to the same bar.
6. **State what you could not verify.** An explicit "unverified" is worth more than a
   confident guess. Several findings here carry that label on purpose.

## Two facts that are easy to get wrong

- **ServUO targets `net48`**, on every branch including `p58-wip`. The .NET 10 in its setup
  instructions is the build toolchain, not the target framework. Linux and macOS run Mono.
- **The six-facet client ceiling is an official-client limit only.** ClassicUO reads map
  indices well past 5. Verified in the wild: Immortal Realms ships `map0.mul` through
  `map21.mul`. ServUO's core allocates 256 map slots. Custom facets are a real option.

## Division of labor

Mechanical, high-volume, patterned work is a good fit for an agent: serialization rewrites,
API drift sweeps, the converters in `tools/`. Deep subsystem design is not. Specifically,
grafting the High Seas galleon and cannon subsystem onto a different boat model, or
implementing missing systems like Skill Masteries, needs human judgment and play-testing.
An agent will produce something that compiles and is subtly wrong.

## Conventions

- One commit per ported or rewritten system. A bad port should be one revert.
- Build after each script, not after each batch.
- When re-applying a ServUO override, re-apply it **by hand** against the current stock file.
  Never copy an old file over a new one. That is how a shard ends up running two copies of
  the same system.
