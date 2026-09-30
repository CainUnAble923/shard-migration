# cc-P21: the console learns every world command, and stops needing to be told

2026-09-30. **I took the whole repo**, not the split: the backfill and the gate first, then the console work. Built with
`docker/uo/build.sh -t sl-modernuo:cc-p21-commands`. **`sl-modernuo:latest` was not moved** (section 9). **Not committed.**
`docs\` untouched. Nothing was run in game.

## 0. What changed, in one paragraph

Every command we register now carries `[ShardCommand(...)]` on its handler, beside `[Usage]`: category, and for the ones
that change a world, re-run behaviour, shard, dry run and a one-line summary. A new test fails the build for any command
registered without one. The console's World setup tab no longer holds a list of our commands. It reads every
`CommandSystem.Register(` in `server\customizations`, reads the declaration beside each handler, and groups what it
finds. Order is one explicit list of sequences, each cited to the runbook that states it.

Files (all in `D:\ShatteredLegacy`):

```
server/customizations/ShardCommandAttribute.cs              NEW. The attribute and three enums. Declares types only.
server/customizations/<32 files>                            +1 line per handler, 58 lines, nothing else (section 3)
server/tests/Misc/CommandDeclarationVerification.cs          NEW. The gate: 5 facts.
scripts/Shard-Console.ps1                                   discovery, grouping, the tab, -WorldCommands
scripts/tests/Shard-Console.Tests.ps1                       13 world-command facts (one replaces the old checklist fact): 71 -> 83
```

---

## 1. The brief's count: 58, not 57

Counted from the source, and separately from the compiled IL (the gate's fact 1 requires the two to agree, and they do):
**58 `CommandSystem.Register(` calls in 33 files.** A comment in `TestCenter/TestCenterKitEntries.cs:4` names the call and
is not a registration. `TCFill` registers through a constant (`TestCenterFillCommand.Command`) and only when
`TestCenter.Enabled` (`TestCenter/TestCenterFillCommand.cs:24-28`).

The list, by category, is in section 3, counted from the discovered tree: world-setup 12, world-generation 2,
world-removal 3, dev-tool 19, grant 8, diagnostic 6, player 8. The brief's eleven world changers are all world-setup.
The twelfth is `PlaceNewHavenQuestBoard`, which the brief did not name. An earlier draft of this note said "fourteen"
without counting, and it was wrong.

## 2. The decision: an attribute, and three refinements to the brief's categories

**Form: a C# attribute, `[ShardCommand(...)]`, in namespace `Server`** (the same namespace as pinned's `UsageAttribute`,
`Server/Attributes.cs:118`, so no file needed a new `using`). A structured comment was the other option. I chose the
attribute because the compiler checks it and the test can read it by reflection. The console reads the same text with a
regex, so the attribute doc asks for plain literals: no constants, no concatenation.

```csharp
[Usage("ClusterFSeedMineCamp [status|dryrun]")]
[Description("...")]
[ShardCommand(CommandCategory.WorldSetup, Rerun = CommandRerun.Skips, Shard = CommandShard.TestFirst, DryRun = "dryrun", Summary = "Places the two mine camp tents if they are not on Trammel. Moves and deletes nothing.")]
private static void OnSeedCommand(CommandEventArgs e)
```

No name collides with pinned: `ShardCommand`, `CommandCategory`, `CommandRerun`, `CommandShard` and `ShardTarget` all
grep empty in `ModernUO-pinned\Projects`. I avoided `CommandInfo`, which pinned already declares as a record
(`Server/Commands.cs:132`).

**Categories: the brief's six, plus `world-removal`.** `DeleteShame`, `DeleteDespise` and `ClearRoyalCityVendors` each
undo what another command placed. As `world-setup` they would sit in a group that says "safe right now". They are never
part of a run sequence, and none of the three has a dry run. So they get their own group and no Copy-group button.

**`CommandRerun`: `Skips`, `Replaces`, `Duplicates`, `Refuses`, `DeletesAgain`, `Unverified`.**
- `DeletesAgain` is the refinement. For `ClusterFOldHavenCleanup` and the removals, "does re-running duplicate?" has the
  honest answer "no, it deletes again whatever matches", and none of the other values says that.
- Rerun describes the plain form, with no argument. Where a mode behaves differently (`replace` deletes), the Summary
  says so.

**`CommandShard`: `Any`, `TestFirst`, `TestOnly`, `Unverified`.** There is no "fresh world" value. Freshness is what the
`world-generation` category says, and the live shard can legitimately get `[SetupDespise` once
(`docs/client-check-backlog.md:242`). **`Unverified` is used wherever no note or source states a shard.** Eight world
commands carry it (section 3: five world-setup and the three removals), and the tab shows "shard: not stated" for them rather than a guess.

**`player` is exactly the Player-access commands, and the gate enforces it.** The 8 are `achievements`, `cleanup`,
`cleanupall`, `guild`, `ResetMyAccount`, `SelfRes`, `stats` and `TCFill`.
- `ResetMyAccount` also declares `Shard = TestOnly` (`ClusterFDevTools.cs:38`: "TEST-SHARD TOOL").
- The player wiki should filter on that shard.
- `stats` is declared `player`, but it is dead (section 6).

## 3. The backfill: 58 declarations

One inserted line per handler, above the method signature, below the existing attributes. `git diff` over
`server/customizations` shows **58 added lines, all `[ShardCommand(`, and no other changed line**. Nothing a command does
changed. The backfill was scripted: it matched each `Register` call to its handler, refused to run unless the 58 names in
the source and the 58 in its table matched exactly, and required each handler to be declared exactly once in its file.

### World commands, with where each fact came from

"P15" and the like are `notes/cc-P15-*.md` and so on. Line numbers are in the file named. Everything here I read or
re-read myself; the sweep was done with a research agent and I re-checked every item marked (v).

| Command | Category | Rerun (plain form) | Dry run | Shard | Evidence |
|---|---|---|---|---|---|
| `GenerateNewShame` | generation | Skips | none | Any | Generate.cs:150-168, :83-86; notes/shard-console.md:593-594 |
| `SetupDespise` | generation | Refuses | none | Any | Setup.cs:58-61; client-check-backlog.md:242 |
| `ClusterFSeedGuildHalls` | setup | Skips | `dryrun` | TestFirst | GuildHallSeeder.cs:50-57 (v); P15:511 |
| `ClusterFSeedNewHaven` | setup | Skips | `dryrun` | TestFirst | NewHavenSeeder.cs:96-99 (v), :145-161; P17:624 |
| `ClusterFSeedOldHaven` | setup | Skips | `dryrun` | Unverified | OldHavenSeeder.cs:115-116, :204-238; no note |
| `ClusterFSeedInstitutions` | setup | Skips | none | Any | InstitutionSeeder.cs:25, :121-133 |
| `ClusterFSeedNewHavenServices` | setup | Skips | `dryrun` | TestFirst | NewHavenServicesSeeder.cs:218-224; P17:624, :629 |
| `ClusterFSeedResetStone` | setup | Skips | `dryrun` | **TestOnly** | ResetStone.cs:3-5, :70-76; P18:199-201 |
| `ClusterFSeedMineCamp` | setup | Skips | `dryrun` | TestFirst | MineCampSeeder.cs:70-76, :129-135; P16:331 |
| `ClusterFMoveMineCampNpcs` | setup | Skips | `dryrun` | TestFirst | MineCampSeeder.cs:88-94, :203-209; P16:331, :338 |
| `ClusterFSouthMineDecor` | setup | Skips | `dryrun` | Unverified | SouthMineDecor.cs:27-29 (v), :51-52; no note |
| `ClusterFOldHavenCleanup` | setup | DeletesAgain | `dryrun` | Unverified | OldHavenCleanup.cs:121-122 (v), :150-160 (v); P17:61 "has not run on the test world" |
| `SeedRoyalCity` | setup | Skips | none | Unverified | RoyalCitySeeder.cs:151-158, :169-195 (v); no note |
| `PlaceNewHavenQuestBoard` | setup | Skips | none | Unverified | NewHavenQuestBoard.cs:357-402; new-haven-quest-board.md:320-321 |
| `ClearRoyalCityVendors` | removal | DeletesAgain | none | Unverified | RoyalCitySeeder.cs:226-251 |
| `DeleteShame` | removal | DeletesAgain | none | Unverified | Generate.cs:59-64 |
| `DeleteDespise` | removal | DeletesAgain | none | Unverified | Setup.cs:41-46 |

Where the note and the code disagreed, **the declaration follows the code**, and the disagreement is reported in section 7.
`SeedRoyalCity` is declared `Skips` because a second run places nothing twice. Its Summary leads with the fact that
matters more: it **DELETES** human vendors in Royal City on every run.

### Everything else

- **dev-tool (19):** `ClusterFReset`, `ClusterFDeleteChar`, `TestingReset`, `TestingZeroSkills`, `CompactExhaust`,
  `CompactClearActive`, `CompactWipeLogbook`, `CompactSeedDiscoveries`, `ClearCommissions`, `ResetGuild`,
  `IncreaseStage`, `addclone`, `GiveDevCrystal`, `RestorationRevoke`, `RestorationClear`, `ClusterFSkillCaps`,
  `ClusterFStatCaps`, `ClusterFAchievement`, `ClusterFBulletin`.
  - `ClusterFBulletin` edits the login bulletins. It is staff content management, not world setup, so it stays out of the
    tab.
  - `ClusterFAchievement` mixes grant, revoke and info. I classified it by its most consequential use.
- **grant (8):** `CompactStanding`, `CompactVouchers` (both "inspect or set"), `CompactUnlockPickaxe`,
  `CompactGivePickaxe`, `CompactGiveReinforcedPickaxe`, `CompactGiveSatchel`, `CompactGiveLogbook`, `RestorationUnlock`.
- **diagnostic (6):** `CompactOreInfo`, `ClusterFAreaScan` (writes a file under `/tmp`, changes nothing in game),
  `CompactRank`, `RestorationList`, `ClusterFSkillGain`, `ClusterFHealerPolicy`.
- **player (8):** as in section 2.

Total: 2 + 12 + 3 + 19 + 8 + 6 + 8 = 58, counted by the console's own discovery (`Group-Object Category` over the tree).

**`GiveDevCrystal` follows the brief and is a dev-tool, not a grant.** It is a testing item.

## 4. The gate: `server/tests/Misc/CommandDeclarationVerification.cs`

**How it finds "a command we register":** from the compiled code, not a grep.
- It scans the IL of every method in `UOContent.dll` whose source document, per `UOContent.pdb`, is a file
  `apply-patches.sh` installed from `server/customizations`. That is the same rule as `TypeIdentityVerification`, applied
  per method, so a partial class of a pinned type still counts.
- At each call to `CommandSystem.Register(string, AccessLevel, CommandEventHandler)` it takes the name (`ldstr`), the
  access (`ldc.i4`) and the handler (`ldftn`).

Five facts:

1. **The IL finds exactly the registrations a plain count of the source finds.** It counts `CommandSystem.Register(`
   lines under `/customizations` with comment lines skipped, and asserts every registration has a resolved handler.
   Either side missing one fails it.
2. **Every registration has `[ShardCommand]` on its handler. This fact is THE GATE.** Its failure message names each
   command and its handler.
3. A world command declares Rerun and Shard, exactly one of `DryRun` or `NoDryRun`, and a Summary.
4. **A declared `DryRun` passes two checks, or the fact fails:**
   - It is a word of that command's own `[Usage]`.
   - It is a string that some method of the command's class loads (`ldstr`). That catches a flag the Usage lists and the
     code never compares against.
5. Player access and the `Player` category name exactly the same commands.

**Watched red first:**
- The attribute and the test were built before the backfill: `build.sh --tests-only`, 328 tests, **327 passed and 1
  failed**.
- The failure was `EveryCommandWeRegisterDeclaresACategory`, listing all 58 as `NO [ShardCommand]: <name> (handler ...)`.
- Fact 1 already passed on that run, so the IL scan and the source count agreed at 58 before any declaration existed.

**Green after:** section 9.

### The day someone adds a command with no `[Usage]`

Nothing breaks, and nothing is hidden. The gate asks for `[ShardCommand]`, not `[Usage]`, and eight of today's 58 have no
`[Usage]`: `SeedRoyalCity`, `ClearRoyalCityVendors`, `GenerateNewShame`, `DeleteShame`, `SetupDespise`,
`DeleteDespise`, `IncreaseStage` and `addclone`. The console takes the name from the `Register` call and shows the command
with no usage.

A command with no `[Usage]` cannot declare a dry run. Fact 4 fails the build, and the console refuses to render one, since
there is no usage to check it against. A dry-run flag nobody can check never reaches the tab.

### What slips past the gate, and what the console does

- **An edited tree that has not been through `build.sh`.** The console lists an undeclared command under **"Registered but
  new, unclassified"**, in red, with its file and line, and no Copy-group button. It never vanishes.
- **A handler the console cannot find in the same file, or a registration shape it cannot read** (a lambda, a computed
  name). It is listed as unclassified with the reason ("handler X is not in <file>", "could not read this registration").
  It is never dropped. The console facts cover both cases with literal sources.
- **A registration through a wrapper** (`void Reg(string n, ...) => CommandSystem.Register(n, ...)`). The IL at that call
  has no `ldstr`, so fact 1's "every registration has a handler" fails the build. That is loud, which is the intent.
- **A declaration that is wrong but well-formed** (says `Skips` when it duplicates). Nothing but a reader catches that.
  The declaration is only as good as the person writing it at the moment they know the answer, which is the premise of
  the brief.

## 5. The console

- **Discovery** (`ConvertFrom-CommandSources`, core, pure). It reads every `Register` call, resolves a constant name in the
  same file, finds the handler's declaration, and reads the attribute block above it (`[Usage]`, `[Description]`,
  `[ShardCommand]`). The shell's `Get-CommandSourceFiles` reads the `.cs` files, read-only. The console discovers and
  renders. It decides nothing about a command.
- **Stock commands are the one exception.** `[GenerateSpawners` and `[save` are pinned's commands, and pinned's source
  cannot carry our declaration. So they stay as cited stock steps inside the fresh-world sequence, exactly as before.
- **Order.** `$script:WorldSetupOrder` is one explicit list of three sequences, each with its source:
  1. **Fresh world, once:** the 12 `[GenerateSpawners` files, `[GenerateNewShame`, `[SetupDespise`, `[save`. Sources:
     notes/shard-console.md section 8, reachability-audit.md section 5, client-test-queue.md:49.
  2. **New Haven:** `[ClusterFSeedNewHavenServices dryrun`, `[ClusterFSeedNewHavenServices`,
     `[ClusterFSeedNewHaven dryrun`, `[ClusterFSeedNewHaven repair`, `[ClusterFSeedGuildHalls repair`. This is P17's
     table verbatim (P17:624-632). On a fresh world P17 puts the first two after the spawn files (:634-637).
  3. **Mine camp:** `[ClusterFSeedMineCamp dryrun`, `[ClusterFSeedMineCamp`, `[ClusterFMoveMineCampNpcs dryrun`,
     `[ClusterFMoveMineCampNpcs` (P16:321-324, :331-338).
- **What is not ordered, and why.** No runbook orders the sequences against each other. P16:343 suggests listing the mine
  camp "next to" NewHavenServices, which is a placement suggestion, not a dependency. So they are separate groups, and
  nothing says which comes first.
  - Seven world commands are in no sequence: `ClusterFOldHavenCleanup`, `ClusterFSeedInstitutions`,
    `ClusterFSeedOldHaven`, `ClusterFSeedResetStone`, `ClusterFSouthMineDecor`, `PlaceNewHavenQuestBoard` and
    `SeedRoyalCity`.
  - They go in **"Existing world: no order established between these"**, with Copy and Copy dry run per line and no
    Copy-group button, because copying them as a group would imply an order.
- **Groups, in the order shown:** the three sequences (each with **Copy group**), no order established, removal, and new
  unclassified.
  - Player, dev-tool, grant and diagnostic commands never appear. A fact checks the 8 player commands are absent.
  - **Copy group** puts the whole group on the clipboard, one command per line, in order. The caption says it is for a
    text file beside the client, since the client takes one command at a time.
- **Each line** gives the access level, the shard ("test first, then live", "either shard", "shard: not stated"), the
  re-run behaviour, "DRY RUN: reports and changes nothing" or "no dry run", and the Summary. Declared problems are
  appended in brackets.
  - Red means test only, unclassified, not registered, or a plain run that deletes.
  - Red covers exactly 6 commands today: `ClearRoyalCityVendors`, `ClusterFOldHavenCleanup`, `ClusterFSeedResetStone`,
    `DeleteDespise`, `DeleteShame`, `SeedRoyalCity`. A fact pins the list.
  - The first cut matched `DELETES` with `-match`, which is case-insensitive in PowerShell and turned "moves and deletes
    nothing" red. It is now a flag on the entry.
- **The honesty stays.** The caption says the console cannot run these and cannot see whether a world has had them.
  Nothing executes anything in game.
- **`-WorldCommands`** prints the tab to the terminal and exits, read-only. It is how I checked it, and it is the quickest
  way to see what P19 adds.

**Facts: 83, all green** under Windows PowerShell 5.1. There were 71 before. There are 13 world-command facts now, one of which replaces the old checklist fact, so the net gain is 12.
They were watched red first: the facts ran before the console functions existed and stopped at `Get-CommandSourceFiles`.
One fact then failed on my own guess ("at least 10 dry runs"). The tree has **nine**, so the fact now names the nine
instead of guessing a number.

The form was built off-screen with `-DryRun` and the tab rendered to an image. It has 3 Copy-group buttons (15, 5 and 4
lines), 34 Copy buttons and 4 Copy-dry-run buttons, which matches the groups. I did not click through the live form.

## 6. Name collisions with pinned (2.2b). Report only; nothing renamed

**Method:**
- I collected every name pinned registers: `Register("...")` literals, `Commands = new[] {...}` and `Accessors` on
  `BaseCommand` implementors, and `[Aliases(...)]`. That is 242 names.
- I compared them case-insensitively with our 58, because `CommandSystem.Entries` is
  `Dictionary<string, CommandEntry>(StringComparer.OrdinalIgnoreCase)` (`Server/Commands.cs:156`).
- Then I grepped pinned for each of our 58 names as a quoted string, case-insensitive, to catch any registration shape
  the collection missed.

**1. Which of ours pinned also registers: one, `stats`.**
- Pinned: `Register("Stats", AccessLevel.Counselor, Stats_OnCommand)` in `Handlers.Configure`
  (`UOContent/Commands/Handlers.cs:20`, `:42`).
- Ours: `CommandSystem.Register("stats", AccessLevel.Player, OnStats)` in `ClusterFStatInspect.Configure`
  (`customizations/ClusterFStatInspect.cs:16-18`).
- None of `guild`, `achievements`, `cleanup`, `cleanupall`, `addclone`, `SelfRes`, or any other of the 58 appears in
  pinned as a string at all. (`GuildProps` exists; it is a different name.)

**2. What `Register` does with a duplicate: it refuses, keeps the first, and logs a warning.**
- `DoRegister` (`Server/Commands.cs:240-254`): if the name exists with a different handler or access, it logs
  `Command {Command} already registered to {Handler}.` at Warning and returns.
- It does not throw and does not overwrite, so a collision is visible only in the startup log.

**Which one registers first is not stated by any source file.**
- Both are `Configure()` with no `[CallPriority]`.
- `AssemblyHandler.Invoke` collects them in `GetTypes()` order and sorts with `List.Sort` (`Server/AssemblyHandler.cs:132-148`),
  which is not a stable sort. So I measured it.

**3. Measured: pinned's wins on both shards, and ours has never been reachable.**
- `docker logs sl-modernuo-test` has `WRN] Command stats already registered to Stats_OnCommand. <s:Server.CommandSystem>`
  at 15:31:36 and 16:39:09.
- `docker logs sl-modernuo` (live) has the same line at 14:16:07.
- `Stats_OnCommand` is pinned's handler. Ours is named `OnStats`.
- So **a player typing `[stats` reaches pinned's Counselor-level command and is refused for access**. Staff at Counselor
  and above get pinned's output: open connections, mobile count and item count (`Handlers.cs:739-745`).
- **Our character stat gump (`ClusterFStatInspectGump`) is unreachable by that command.**
- We did not replace the stock command. Ours silently lost.

**Kind: ours to fix.** Whether to rename ours or not is Chase's call, as the brief says. Two other options exist:
- give ours a `[CallPriority]`, which would take `[stats` from staff instead;
- keep both under different names.

I changed nothing. The declaration says `player` because that is what the command is written to be.

## 7. Defects found while walking the registrations. Report only; none fixed

For the overseer to number. Each has what proved it.

1. **`[stats` never registers** (section 6). Ours to fix.

2. **`[ClusterFOldHavenCleanup` reaches into New Haven.** Ours to fix. I verified every part of this myself.
   - Its spawner scan box is X 3520-3760, Y 2420-2760 (`ClusterFOldHavenCleanup.cs:105-107`). New Haven is X 3416-3545
     (`ClusterFNewHavenServicesSeeder.cs:194`), so X 3520-3545 belongs to both.
   - Pinned `Data/Spawns/post-uoml/trammel/Vendors.json` has a `BlacksmithGuildmaster` spawner at 3526,2536,20.
     `BlacksmithGuildmaster` is on the cleanup's delete list (`:93`).
   - So on any world that has had `[GenerateSpawners ... trammel/Vendors.json`, the plain command deletes New Haven's
     Blacksmith Guildmaster spawner.
   - The other pinned spawners in that strip (Noble, AnimalTrainer, Fisherman, IronWorker, Miner, BaseEscortable,
     reagents) are not on its list.
   - Two more problems:
     - **Any argument other than `dryrun` runs the real delete** (`:121-122`), so a typo such as `dyrrun` deletes.
     - **P17:60-61 says it deletes spawners only.** It also deletes NPCs within 8 tiles of each listed coordinate
       (`:150-160`).
   - The P15 note says the directory rows for Smiths depend on pinned's vendor spawns (P15:521-523). That is how this one
     would be noticed.
   - It is declared `Unverified` shard and shows in red.

3. **`[ClusterFSeedGuildHalls dryrun` does not report moves.** Ours to fix.
   - `Seed(dryRun: mode == "dryrun", repair: mode == "repair")` (`ClusterFGuildHallSeeder.cs:56`) passes `repair: false`
     on a dry run.
   - P15:515 says the dry run "lists what would be placed or moved". It lists placements, and only notes an Artificers'
     Guildmaster still on its old tile.
   - The New Haven sequence runs `[ClusterFSeedGuildHalls repair` with no dry run of its own, as P17 wrote it. So nothing
     previews that move.

4. **`[SeedRoyalCity` deletes on every run, and its header says it is idempotent.** Ours to fix, or to accept and write
   down.
   - It deletes every human-bodied `BaseVendor`, `BaseGuildmaster` or `TownCrier` in the Royal City bounds before placing
     (`ClusterFRoyalCitySeeder.cs:169-195`).
   - The header says "safe to re-run" and "idempotent" (`:20`, `:24`). That holds for placement only.
   - **Unverified:** the Ter Mur `ArtificersGuildmaster` the institution seeder places at 797,3431,-10
     (`ClusterFInstitutionSeeder.cs:99-106`) is a `BaseGuildmaster` (`ArtificersGuildmaster.cs:19`) inside those bounds.
     If its body is human, every `[SeedRoyalCity` deletes it, and the next world load recreates it. I did not check the
     body.
   - It also auto-seeds at world load when no GargoyleAlchemist is on Ter Mur (`:110-115`).

5. **Usage strings that do not match the code.** Ours; documentation-only fixes.
   - `ClusterFSeedNewHaven` also takes `status` (= dryrun), `sync` (= repair) and `force` (= replace)
     (`ClusterFNewHavenSeeder.cs:96-99`, verified).
   - `ClusterFSeedOldHaven` also takes `status` and `force` (`:115-116`).
   - `ClusterFBulletin` has a `load` subcommand that its Usage omits (`:150`, `:216-289`). With no `bulletins.txt`, `load`
     writes a template file.
   - `ResetGuild <key|all>` marks the argument as required, but the code defaults to `all` (`ClusterFGuildSystem.cs:1055`).

6. **`[ClusterFSouthMineDecor` treats any unknown argument as the plain run** (`ClusterFSouthMineDecor.cs:27-29`,
   verified). The plain run only places what is missing, so a typo here is harmless. I list it for consistency with item 2.

7. **`ClusterFOldHavenSeeder.cs` header bounds disagree with its code.** The header says X 3620-3760 (`:17`); the code uses
   3520-3680 (`:274-276`). Not verified by me.

8. **Eight commands have no `[Usage]`**, listed in section 4. They are not defects under the gate. For
   `GenerateNewShame`, `SetupDespise` and `SeedRoyalCity`, a Usage would let the tab show more. I did not add one, because
   the brief allows the declaration only.

9. **Commands that change the world at every start, with nothing run:**
   - `ClusterFInstitutionSeeder`, always (`:34-41`).
   - `ClusterFSouthMineDecor`, while `clusterf.southMineDecor.enabled` is true, which is the default (`:12`, `:35-43`).
   - `ClusterFRoyalCitySeeder`, when no GargoyleAlchemist is on Ter Mur.
   - These are why "the console cannot tell whether a world has had these" is literally true: some of them run
     themselves.

10. **`docs/client-test-queue.md:48` cites "Live-Deploy-Runbook 6b".** No file by that name exists in shard-migration.
    Found by the research sweep; I did not re-check it.

### Errors in the brief

- **`[ClusterFSeedNewHaven repair` is not a dry run.**
  - It moves the 18 New Haven NPCs onto their floors (P17:631; `ClusterFNewHavenSeeder.cs:98`).
  - The dry run is `dryrun`, or its undocumented alias `status`.
  - A tab that rendered `repair` as the dry run would have moved NPCs on a live world. A console fact pins
    `[ClusterFSeedNewHaven dryrun`.
- **57 is 58** (section 1).
- **The brief's eleven are all world-setup, and the list is not complete.** It omits `PlaceNewHavenQuestBoard`
  (world-setup) and the three removals, `ClearRoyalCityVendors`, `DeleteShame` and `DeleteDespise`.

## 8. Duplicate-safety: note claims against the code

"Most seeders claim duplicate-safe."

**Every claim I found in a note agrees with the code for the plain form and the modes the note describes:** P15:273-274,
P16:226-227, P16:336, P16:338, P17:629, P17:631, P18:193-197, new-haven-quest-board.md:320-321 and shard-console.md:591-594.

**The claims that do not hold are in code comments, not notes:**
- `ClusterFRoyalCitySeeder.cs:20`, `:24`: "idempotent" (item 4).
- P17:60-61, on what `ClusterFOldHavenCleanup` deletes (item 2).

**Modes that delete are described by no note:**
- `ClusterFSeedNewHaven replace` deletes every seed-type mobile in the area (`:129-141`).
- `ClusterFSeedOldHaven replace` deletes every managed spawner (`:149-159`).
- `ClusterFSouthMineDecor replace` (`:54-60`).
- Each Summary says so in capitals.

## 9. Build

```
docker/uo/build.sh -t sl-modernuo:cc-p21-commands
```

**Green: `Total tests: 328, Passed: 328`**, then `Built sl-modernuo:cc-p21-commands with patches applied and 328 shard
test(s) passing.` That is 323 before, plus this task's 5. The image is `05ebfdd4f25f`.

**`sl-modernuo:latest` is `16b0f49e6828` before and after the build.** `build.sh -t` tags only the name given
(`build.sh:32`, `:43`, `:110`). The builder stage retags `sl-uo-builder:latest`, as every build does.

## 10. For Chase

1. **Commit** with `Commit-ShardWork.ps1`. There are 36 files in `D:\ShatteredLegacy` (`git status` shows 34 modified
   and 2 new) plus this note:
   - 32 customizations files, each with added lines only;
   - `ShardCommandAttribute.cs` (new);
   - `CommandDeclarationVerification.cs` (new);
   - the two console scripts.
2. **Decide `[stats`** (section 6). Nothing players can reach today uses our gump.
3. **Do not run `[ClusterFOldHavenCleanup` on a world that has New Haven's vendor spawners** until item 2 is looked at.
4. Open the console's World setup tab, or run `.\scripts\Shard-Console.ps1 -WorldCommands` for the same content as text.
5. **P19:** `ClusterFSeedRegistrarOffice` needs a `[ShardCommand(...)]` or its build fails. If it belongs in a sequence, it
   also needs an entry in `$script:WorldSetupOrder` with a cited source; until then it appears under "no order
   established".
