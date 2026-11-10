# cc-P876: build review of P861 (extra NPC name lists and [VBuild statify)

## In plain words

- The build review of P861 (new NPC names and the staff command that turns a placed fountain or forge into plain
  scenery) did not pass, so P861 waits and goes back to the Iron Golem for a fix-up.
- The main reason is paperwork: P861 left none of the review files a decoration change must leave (no
  `cc-P861-review` folder, no list of what was placed). Its in-game shots look right: the test fountain looks the same
  before, after freezing and after undo.
- One real catch: the freeze command does not refuse the Fountain of Youth. Freezing it would leave a dead copy of the
  fountain where it stood, and the real one would come back by itself on its weekly move (or, in New Haven, players
  would be left with no fountain to drink from).
- Nothing for you to do.

Iron Golem, 2026-11-10, review only (no build, nothing changed in P861's files). P861 at
`origin/golem/Iron/P861`: docs `53d258c2`, code `fedfd3b1`.

## What was looked at

1. The guide `notes\guides\building-and-decorating.md`, with its section 8 (what a build leaves for the reviewer).
2. `git ls-tree -r --name-only origin/golem/Iron/P861 -- notes/cc-P861-review`: **empty**. The branch has no
   `notes/cc-P861-review/` folder and no `placed.md` anywhere. It has `notes/cc-P861-shots/` (main, run1) and
   `notes/cc-P861-tools/` instead.
3. The notes `notes/cc-P861-names-and-statify.md`, the Codex review beside them, and the code diff
   (`git diff main...origin/golem/Iron/P861`, 11 files). No seeder, map static, mapop or permanent addon is added: the
   change is the name lists and the staff tool `[VBuild statify` (`AddonStatify.cs`) plus its Visual Builder undo hooks.
4. Every shot in `cc-P861-shots/main`: `p861-3-fountain-addon`, `p861-4-fountain-statics` and `p861-5-fountain-back`
   show the stone fountain (middle part 0x173A, 3655,2605,0, main's New Haven, private proof shard 2596) the same in all
   three: frozen statics sit exactly where the addon parts stood, same art and height, nothing shifted or left over.
   The undo shot is clean (no doubled pieces). `walk.txt` PASSes match. The twin-name shots are not a build.
5. No walls, doors, stairs, roofs, signs, shores, bridges, docks or foliage were placed, so those checks have nothing
   to look at.

## Verdict

BUILD REVIEW P861: FAIL

1. No renders or placed list left for review. `notes/cc-P861-review/` and its `placed.md` are missing on
   `golem/Iron/P861` (guide section 8 and this review's rule 4). Fix: add `notes/cc-P861-review/placed.md` that says what
   was placed and where: the test stone fountain (StoneFountainAddon, middle 0x173A, 3655,2605,0, Trammel, main's New
   Haven) on the private proof-shard copy only, frozen into 16 statics, then undone. It should also say plainly that
   nothing permanent is placed in any shipped world, seeder or map file. Copy the three fountain shots
   (`p861-3-fountain-addon.jpg`, `p861-4-fountain-statics.jpg`, `p861-5-fountain-back.jpg`) into that folder as the
   before, after and undo shots.
2. FountainOfYouthAddon (`server/customizations/FountainOfYouth/FountainOfYouth.cs`, fixed in New Haven or roaming
   between pool spots) is not refused by `AddonStatify.WhyNot`/`SeededTypes` (`AddonStatify.cs:31`). It is a seeded
   piece that the guide's "nothing stray" rule (2.6) and P861's own rule ("an addon our seeders place and keep") should
   cover. Freezing it parks the live addon on the internal map while it is still in `_fountains`:
   - for a roaming fountain, `CheckMoveDue` calls `Move`, which `MoveToWorld`s the parked addon to a new spot and
     leaves the frozen static copy behind as a second, dead fountain;
   - for the fixed one, `Seed` sees the parked one as "already placed", so New Haven keeps a dead static fountain with
     no drinkable one.

   Fix: add `typeof(FountainOfYouthAddon)` to `SeededTypes` (or a refusal naming it), with a fact that
   `[VBuild statify` refuses it and leaves it in the world. This is the same as Codex's first P2 finding on P861.

Not part of this verdict (code, not build): Codex's second P2 is that the name sweep can rename a fixed-identity NPC
whose name is also in a list, such as Mara. It is in the P861 Codex review and on the overseer's list. The fix-up may take it
too.

P876 DONE
