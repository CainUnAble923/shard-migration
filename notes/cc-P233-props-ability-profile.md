# cc-P233: a creature's AbilityProfile opens from [props

2026-10-20. Server only (`D:\ShatteredLegacy`, read and changed in the Bronze work copy, branch `golem/Bronze/P233`).
Staff tool, not player-facing. Ported system (Pet Training), ours in the staff view.

## Headlines

- **Cause.** Pinned's props gump draws a row's gold open arrow only when the property can be modified, and it reads
  that as "the attribute is not read-only, the viewer has the write level, and the property has a setter **or** its
  attribute says `canModify`" (`UOContent\Gumps\Props\PropsGump.cs:141`, re-read on d4531cd94). The press is refused by
  the same test (`:210-213`) before the `[PropertyObject]` branch that would open the object (`:316-321`). Our
  `BaseCreature.AbilityProfile` and `TrainingProfile` are get-only with a plain `[CommandProperty(AccessLevel.GameMaster)]`
  (`Services\Pet Training\BaseCreature.PetTraining.cs:31-32`, `:54-55` before the change), so staff saw the profile's
  `ToString()` ("...", `AbilityProfile.cs:711`) and no arrow. `[PropertyObject]` was already on both types
  (`AbilityProfile.cs:30`, `TrainingProfile.cs:23`); that alone is not what the gump checks.
- **Fix: one attribute argument on each property**, `canModify: true`, which is exactly what pinned does for its own
  get-only `[PropertyObject]` members (`Engines\ConPVP\Arena.cs:26, :478`, `TournamentController.cs:26`,
  `Ladder.cs:23`; the shard's `BaseSetArmor.cs:23` does the same). No command was added, so nothing changes for
  `CommandDeclarationVerification`. No patch, no new file in `customizations`.
- **Opening writes nothing for a stock creature.** The open path is pinned's `prop.GetValue` (`PropsGump.cs:216`), the
  same call `[props` already makes to draw the row's value (`:145`), so it creates the same in-memory profile P121
  chose to create on look (so a stock dragon's row shows its breath) and nothing more: `IsEmpty` stays true and
  `AbilityProfileStore.Serialize` skips it (`AbilityProfileStore.cs:80-84`). The fact below proves the save count is
  unchanged and a save-and-load drops the entry. For `TrainingProfile` the getter passes `create: false`, so an
  untrained creature's press creates no training record; pinned's null branch re-sends the creature's own page
  (`PropsGump.cs:320`).
- **Tests: 4 facts, all seen red first** (section Tests): red A on the unchanged customization (4 of 4 failed: no arrow,
  press refused), red B with a deliberate break that makes the open path store a regeneration bonus (the
  "writes nothing" fact failed), then green. Full gate `docker\uo\build.sh -t sl-modernuo:cc-P233`: **1,628 tests,
  1,624 passed, 4 skipped** (P232's 1,620 plus these 4), image built, 2 min 7 s.

## What changed, file:line

| File | Change |
|---|---|
| `server\customizations\Services\Pet Training\BaseCreature.PetTraining.cs:27-35` | `AbilityProfile`: `[CommandProperty(AccessLevel.GameMaster, canModify: true)]` at `:34`, and three doc lines (`:30-32`) saying why |
| same file, `:61-66` | `TrainingProfile`: the same attribute argument at `:65` and a doc line |
| `server\tests\Services\PetTraining\PropsAbilityProfileVerification.cs` (new) | 4 facts, below |
| `CHANGELOG.md`, `VERSION` | `## 2026.10.20.12`, one `### Staff` line; VERSION `2026.10.20.12` (the branch's base is `.11`; the merger renumbers if P232's `.12` lands first, P213's rule) |

Nothing else: no command, no gump, no patch, no store change.

## 3. The other Pet Training objects

- **`TrainingProfile`** (`BaseCreature.TrainingProfile`, `[PropertyObject]` at `TrainingProfile.cs:23`, 18 command
  properties): the same one-line treatment, done. Null until the lore gump begins training, so on an untrained
  creature the arrow re-sends the creature's own page; on a trained one it opens the profile.
- **`PlanningProfile`** (`TrainingProfile.PlanningProfile`, `TrainingProfile.cs:93`): not done. The property has no
  `[CommandProperty]`, the type has no `[PropertyObject]` and no command properties (`PlanningProfile.cs:12`), and its
  getter creates the plan on read (`_plan ??= new PlanningProfile(Creature)`), so giving it an arrow is three changes
  and a design question (what staff would edit in a plan), not one line. Left as is; the plan is reachable through the
  training gumps.
- **`AbilityProfile.Creature`** and `TrainingProfile.Creature` (get-only `BaseCreature`, `[CommandProperty]`): entity
  rows; pinned's entity branch (`PropsGump.cs:219`) would offer a set gump, which is not wanted on a back-reference.
  Left read-only.
- `PetTrainingRecord` (the store's row: `SlotsLowered`, `CurrentTameSkill`, `Training`) has no command surface and is
  read through `ControlSlotsMin`, `ControlSlotsMax` and `CurrentTameSkill` on the creature already. Nothing to do.

## Tests

`server\tests\Services\PetTraining\PropsAbilityProfileVerification.cs`, 4 facts, driven the way pinned's own
`UOContent.Tests\Tests\Gumps\PropsGumpTextDefinitionTests.cs` drives the props gump: a GameMaster `PlayerMobile` with
`PacketTestUtilities.CreateTestNetState()`, a `PropertiesGump` subclass that exposes the protected row list, the gump
built on the row's page, and `OnResponse` with that row's button id (`index on page + 3`, `PropsGump.cs:126-150`).

1. **TheAbilityProfileRowCanBeOpened**: the attribute the gump reads says `canModify` (or the property has a setter),
   the type carries `[PropertyObject]`, and the real gump built on a stock Dragon's page has a `GumpButton` with that
   row's id.
2. **PressingTheArrowOpensTheCreaturesProfile**: pressing the row sends a `PropertiesGump` whose object (the protected
   `m_Object`, read by reflection) is the Dragon's own `AbilityProfile`, the same reference
   `PetTrainingHelper.GetAbilityProfile(dragon)` returns, and its names include DragonBreath.
3. **OpeningAStockCreaturesProfileWritesNothing**: a fresh Dragon has no stored profile; after the press the entry
   `[props` makes is `IsEmpty`, the store's serialized live count is unchanged, and `Serialize` then `Deserialize`
   drops it (`TryGet` false).
4. **TheTrainingProfileRowCanBeOpenedAndMakesNoRecord**: the same attribute and arrow checks for `TrainingProfile`;
   pressing it on an untrained Dragon re-sends the Dragon's own page (opened object is the Dragon) and
   `PetTrainingStore` has no record and no more rows than before.

**Seen failing first.** Each run is the builder stage built from the work copy, then the class alone in that image
(`dotnet test ... --filter FullyQualifiedName~PropsAbilityProfileVerification`), detached, with the `docker-build`
lock held.

- **Red A** (facts present, customization unchanged; first attempt was a compile error in the fact, `ReadEncodedInt`
  is an `IGenericReader` member, fixed): **4 of 4 failed**, each at its intended line: 1 and 4 at "has no setter and
  its attribute does not say canModify", 2 and 3 at "the press opened nothing" (`Assert.NotNull` on the opened gump).
- **Red B** (fix applied, plus a deliberate break: the getter sets `RegenHits = 1` on every read, so the open path
  stores something): **1 of 4 failed**, fact 3 at "opening the profile stored something on a stock creature"; facts 1,
  2 and 4 passed, which is the fix proving itself. The break was then reverted (`grep -c "P233 BREAK"` is 0).
- **Green**: the full `docker\uo\build.sh -t sl-modernuo:cc-P233` on the finished tree, all three gates:
  `Total tests: 1628, Passed: 1624, Skipped: 4`, the four new facts listed as Passed (33, 32, 4 and 5 ms),
  `Built sl-modernuo:cc-P233 with patches applied and 1624 shard test(s) passing.` START 2026-10-21T00:13:08Z, END
  00:15:15Z (UTC; 19:13 local). Free memory was 1,265 MB at launch; the Docker VM's page cache (13.2 GB) was dropped
  during the run and Windows read 6,607 MB after; the detached build was unaffected.

## Deviations and decisions for Chase

- **The Read and Edit tools are denied on the code repo in this unattended session** (it is outside the working
  directory), so every edit there was made by a small Python script run with `-I` from the session scratchpad (the
  attribute change, the deliberate break and its reversal, the patch note), and the test file was written to the
  scratchpad and copied in. Each edit asserts its anchor text and the diffs are quoted above.
- **No `[abilities` command.** The prompt's second option was for the case where pinned only opens objects with a
  setter; it does not (`canModify` exists for exactly this), so the command would have been a second way to the same
  gump.
- **`[props` still makes an in-memory profile on look** (P121's choice, kept): the open path adds nothing to that.
  If Chase would rather `[props` show "-null-" for a creature with nothing stored, that is a one-word change
  (`create: false`) and loses the natural-abilities view P121 wanted.
- `PlanningProfile` left without an arrow (section 3).

## For Chase

On the test shard (image `sl-modernuo:cc-P233`), `[props` a wild dragon: the AbilityProfile row shows "..." with a
gold arrow; the arrow opens a page with `AbilityNames` (Magery, Dragon Breath), `MagicalAbility`, the regeneration
numbers and `Creature`. `TrainingProfile` on a wild creature shows "-null-" with an arrow that re-opens the same
page; on a pet that has begun training it opens the training numbers. `[version` shows 2026.10.20.12.

## Repo size rule

Largest changed file: `CHANGELOG.md` (about 84 KB). The new test is 11 KB. Scratch (run scripts and logs) is in the
session scratchpad under `%LOCALAPPDATA%\Temp\claude\`, outside both repos.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun -CodeRepo D:\UO\golems\Bronze\ShatteredLegacy -DocsRepo D:\UO\golems\Bronze\shard-migration`
(the work copies; the script skips the mirror and dashboard refresh for them by its cc-P184 rule; it commits nothing):

```
=== code  (D:/UO/golems/Bronze/ShatteredLegacy) ===
  4 file(s) pending:
    CHANGELOG.md
    VERSION
    server/customizations/Services/Pet Training/BaseCreature.PetTraining.cs
    server/tests/Services/PetTraining/PropsAbilityProfileVerification.cs
  dry run: would add, commit and push

=== docs  (D:/UO/golems/Bronze/shard-migration) ===
  1 file(s) pending:
    notes/cc-P233-props-ability-profile.md
  dry run: would add, commit and push

Repo Result
---- ------
code dry run
docs dry run
```

Neither repo is BLOCKED. Changed-file sizes: `CHANGELOG.md` 83,564 bytes, the customization 11,576, the test 11,326,
`VERSION` 14. The docker-build lock was released after the gate; the image `sl-modernuo:cc-P233` (1.29 GB) is on the
game PC for the test shard.

P233 DONE
