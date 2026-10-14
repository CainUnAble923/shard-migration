# cc-P95: D89, HEAD does not boot (ImbueCatalogue read the skill table too early)

2026-10-14. Code fix in `D:\ShatteredLegacy`, a regression test, and a real boot on the bot's scratch shard.

## Headlines

- **Cause.** Start order, not the catalogue alone. Pinned `Main.cs:667` runs every `Configure` through
  `AssemblyHandler.Invoke`, which sorts by `CallPriority` (`AssemblyHandler.cs:143`; default 50, `Attributes.cs:81`)
  with `List.Sort`, which is not stable. `SkillsInfo.Configure` (`SkillsInfo.cs:133`) and
  `ClusterFImbueKnowledge.Configure` were both at 50, so nothing promised which ran first. The imbuing one ran first:
  `ImbuingTable.LoadOrWriteDefaults` -> `ImbuingTable.Defaults` -> `BuildDefaults()` (`ImbuingTable.cs:257,267`) ->
  `ImbueCatalogue.All` -> the static initializer -> `SkillRowName` -> `SkillInfo.Table[(int)skill]` on the empty
  `Array.Empty<SkillInfo>()` (`Server/Skills.cs:451`). That is an `IndexOutOfRangeException`, wrapped in a
  `TypeInitializationException`, and the shard does not start.
- **Why making the catalogue lazy alone would not have fixed it.** `Configure` itself uses the catalogue (through
  the table's defaults, and the file's parse validates property names against it). A lazy catalogue first used inside
  that `Configure` still reads an empty skill table. The ordering has to change too.
- **The fix, two parts:**
  1. `[CallPriority(100)]` on `ClusterFImbueKnowledge.Configure`
     (`server/customizations/Imbuing/ClusterFImbueKnowledge.cs:98`). It now always runs after every default-priority
     `Configure`, `SkillsInfo.Configure` included, and still before `World.Load` (`Main.cs:671`), so the imbuing table
     is loaded before any item deserializes, exactly as before.
  2. The catalogue is built on first use, not in a static initializer: `All => _all ??= Build()`
     (`server/customizations/ArtificersImbueGump.cs:153`), with the old static constructor body now
     `internal static List<ImbuePropertyDef> Build()` (`:194`). The Add helpers append to the list being built
     (`Rows`) instead of `All`; nine lines changed, nothing else in the body. `Build()` first checks the skill table is
     filled and throws a plain `InvalidOperationException` naming D89 if not. A static initializer that throws poisons
     the type for the rest of the process; this does not, and the message says what happened.
- **Contents and order unchanged, measured.** A temporary test fingerprinted every catalogue row (all public non-delegate
  fields of `ImbuePropertyDef`, in order, plus whether each delegate is set): **124 rows,
  SHA-256 `161C716E07D357A83E304635B18E389B26CAF469226F18CC8EC61C09D63E031A`** before the fix, and the same hash
  asserted after it (green). The temporary test was then deleted; it is not in the tree.
- **Other spots: none on the start path needing a fix.** See "Other spots checked".
- **Test red, then green.** New `server/tests/Misc/ImbueStartOrderVerification.cs`, two facts. Before the fix:
  1,135 tests, 1,133 passed, 2 failed (the new priority fact, and the temporary fingerprint, which failed on purpose
  to print its hash). After: **1,136 of 1,136 passed** (the temporary fingerprint included). Final tree, with it
  removed: 1,135 tests. Excerpts below.
- **Boot proof: the working tree (HEAD 10f4088 plus this fix) starts and listens** on the bot's scratch shard,
  `[Imbuing] imbuing.json was missing; wrote the built-in defaults` on the way, which is the exact path that crashed
  (the defaults read the catalogue). **T-047: PASS, 3 of 3.** The gated build inside the run: 1,135 of 1,135 tests.
  Rule 1 held: live and test containers identical before and after.

## The regression test

`ImbueStartOrderVerification`:

1. `ImbueKnowledgeConfigureRunsAfterSkillsAreConfigured`: `ClusterFImbueKnowledge.Configure`'s `CallPriority` is
   strictly greater than `SkillsInfo.Configure`'s. Strictly, because equal priorities run in no promised order.
2. `CatalogueIsBuiltOnFirstUseNotInAStaticInitializer`: with `SkillInfo.Table` swapped to empty, `ImbueCatalogue.Build()`
   throws `InvalidOperationException`; with it restored, a fresh build matches `ImbueCatalogue.All` name for name.

**Why not a test that calls the catalogue the way a start does.** The test host fills `SkillInfo.Table` before any test
runs, and by then something has usually touched the catalogue, so no test can reproduce the real order by calling it.
That is also why 1,133 tests passed over a shard that would not start (D89's "tests pass because none boots the world in
that order"). Fact 1 checks the ordering rule the start depends on instead; fact 2 checks the catalogue fails cleanly and
retryably if that rule is ever broken. Fact 2 did not compile before the fix (`Build()` did not exist), so it was held
behind `#if` for the red run and is shown green only.

Red (before the fix), from `build.sh -t sl-modernuo:cc-p95 --tests-only`:

```
  Failed ShatteredLegacy.Tests.ImbueStartOrderVerification.ImbueKnowledgeConfigureRunsAfterSkillsAreConfigured [< 1 ms]
   ClusterFImbueKnowledge.Configure is at CallPriority 50 and SkillsInfo.Configure at 50: the imbuing table can load before the skill table is filled (D89).
  Failed ShatteredLegacy.Tests.ImbueCatalogueDumpTemp.Fingerprint [1 ms]
   P95FINGERPRINT rows=124 sha256=161C716E07D357A83E304635B18E389B26CAF469226F18CC8EC61C09D63E031A
Test Run Failed.
Total tests: 1135
     Passed: 1133
     Failed: 2
BUILD FAILED: ShatteredLegacy.Tests tests did not pass. No image was built.
```

Green (after the fix, same command):

```
Total tests: 1136
     Passed: 1136
```

## Other spots checked

Searched every file that touches `ImbueCatalogue`, `ImbuingTable`, `ClusterFImbueKnowledge` or `ImbueTiers`, every
`SkillInfo.Table` read in `server/customizations`, and every static constructor there.

| Spot | On the start path? | Verdict |
|---|---|---|
| `ImbuingTable.Defaults`/`BuildDefaults` (`ImbuingTable.cs:257,267`) | yes, from `ClusterFImbueKnowledge.Configure` | already lazy; safe now that the Configure runs at 100 |
| `ImbuingTable.Parse` (validates names against the catalogue) | yes, same Configure | same |
| `ClusterFImbueEffects.Configure` (`Imbuing/ClusterFImbueEffects.cs:49`) | yes | registers a store and a tooltip hook; reads no catalogue or skill table |
| `ClusterFRecipeStore.Configure` (`Engines/Craft/ClusterFRecipeStore.cs:53`) | yes | loads `RecipeGatingTable`; `ClusterFRecipeTable.cs` reads no `SkillInfo`, `CraftSystem`, recipe table or catalogue |
| `ArtificerWorkOrderCatalogue` static ctor (`ArtificerWorkOrderSystem.cs:123`) | no, used only from gumps | its `Build()` reads no catalogue or skill table; left alone |
| `SmithCommissionPool`, `SmithCommissionSetPool` static ctors (`ClusterFSmithCommissions.cs:160,347`) | no | pure data from their own arrays |
| `CraftAttributeInfo` static ctor (`ResourceInfo.cs:97`) | upstream replacement | not touched by this prompt |
| `Meditation.Initialize` (`Meditation.cs:17`) | yes | `Initialize` runs after every `Configure` (`Main.cs:674`); safe |
| `ClusterFSkillCaps.TotalSkillCap` (`:128`), `ClusterFAchievements`, `ClusterFGuildStarterPath`, `ClusterFRecipeGate`, `ClusterFRecipeStore`, `CleanUpBritanniaRewards` | no | read at runtime, after start |
| `JewelrySkillGroups`, `CrafterSkillGroups`, `SuperSlayers` (static readonly in `ImbueCatalogue`) | type init | enum arrays only; still run at type init, which is harmless |

## Boot proof

Command, as the prompt gives it (no `-Commit`, so it built the working tree through `build.sh -t sl-modernuo:bot`):

```
powershell -NoProfile -ExecutionPolicy Bypass -File D:\ShatteredLegacy\tools\playtest-bot\Run-OvernightPlaytests.ps1 -Only T-047 -SkipSoak -NoEmail
```

Run folder `testing\bot-runs\2026-10-14-0817\` (report.md, results.json, run.log, shard-start.log, transcripts). Its
`run.log` holds the build: `Total tests: 1135, Passed: 1135`.

Start lines up to "Listening", from `shard-start.log` with the console colour codes and source tags stripped:

```
[SL] Starting Shattered Legacy ModernUO...
[SL] Commit: d4531cd94b739613155225c234900de9f47d2c88  .NET: 10.0.203
[SL] Syncing Projects from bind mount...
ModernUO - [https://github.com/modernuo/modernuo] Version 0.15.6.208
Copyright 2019-2026 ModernUO Development Team
This program comes with ABSOLUTELY NO WARRANTY;
This is free software, and you are welcome to redistribute it under certain conditions.
You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
[08:19:48 INF] Reading server configuration from Configuration/modernuo.json...
[08:19:48 INF] Reading server configuration done
[08:19:49 INF] Running on .NET 10.0.7
[08:19:49 INF] Loading Map Definitions
[08:19:49 INF] Loading map definitions done (7 maps, 0 failures) (0.00 seconds)
[08:19:50 INF] Email configuration read from Configuration/email-settings.json
[SaveOnShutdown] listening for SIGTERM: a stop saves the world first (D36)
[08:19:50 INF] Protected accounts registered: aetherion, admin
[08:19:50 INF] Registered connection filter 'firewall'
[08:19:50 INF] Registered connection filter 'auto-denylist'
[08:19:50 INF] Ban channel registered reporter 'auto-denylist'
[08:19:50 INF] Ban channel registered reporter 'crowdsec'
[08:19:50 INF] Registered connection filter 'blocklist'
[League] Loaded the League ladder table from /modernuo/Configuration/league-ladder.json.
ClusterF skill scaling: curve 1.5; at 200: Nerve Strike 0.9 -> 0.95, stable slots per skill 3 -> 6, Fire Horn x1.1, Stealth steps 24 -> 34, bandage average 57.5 -> 72.
[08:19:50 INF] Encryption support enabled: Both
[08:19:50 INF] Automatically detected client version 7.0.114.40
[RecipeGating] recipe-gating.json was missing; wrote the built-in defaults to /modernuo/Configuration/recipe-gating.json.
[08:19:50 WRN] Command stats already registered to Stats_OnCommand.
[08:19:50 INF] Discovered 3 spawner JSON type(s)
[ShardVersion] Shattered Legacy 2026.10.14.2 (35 version(s) in the changelog)
[LootBox] loot-boxes.json was missing; wrote the built-in defaults to /modernuo/Configuration/loot-boxes.json.
[Fanfare] fanfare-lines.json was missing; wrote the approved pools to /modernuo/Configuration/fanfare-lines.json.
[Imbuing] imbuing.json was missing; wrote the built-in defaults to /modernuo/Configuration/imbuing.json.
[08:19:50 INF] Loading maps
[08:19:50 INF] Loading maps done (0.00 seconds)
[08:19:50 INF] Loading regions
[08:19:50 INF] Loading regions done (371 regions) (0.13 seconds)
[08:19:50 INF] Loading world
[ClusterFLumberjackingExtension] Extended lumber veins registered: 8 new wood types (Ironwood through Starwood). Groves are permanent (RandomizeVeins=false).
[ClusterFMiningExtension] Extended mining veins registered: 8 new ore types (Platinum through Celestial). Veins are permanent (RandomizeVeins=false).
ClusterF New Haven seed complete: created 0, repaired 0, skipped 40, deleted 0.
[ClusterFRangersSystem] Re-applied skill mods for 1 Outriders Crook(s).
ClusterF south mine decor complete: placed 0, skipped 2.
ClusterF stat caps applied to 9 loaded player(s): 500 per stat, 1500 total.
[08:19:53 INF] Loading world done (206959 items, 35041 mobiles) (2.84 seconds)
[08:19:53 INF] Manual allowlist disabled ("enabled" false in ip-allowlist.json)
[08:19:53 INF] Login allowlist empty: no file at "/modernuo/Configuration/login-allowlist.txt"
[08:19:53 INF] Restricting client version to 7.0.117.0 or newer. Action to be taken: Kick
[08:19:53 INF] Test Center skill gain multiplier 5 applied to 58 skills
[08:19:53 INF] Server listing address set from config: 127.0.0.1
[08:19:54 INF] Feature Flag system initialized with 14 flags, 0 gump blocks, 0 item blocks, 0 skill blocks, 0 spell blocks
ClusterF skill gain: rate enabled, 3 chance attempt(s), 5x gain amount; past stock ceilings on.
[AccountWipe] census: 7 accounts, 9 characters, 0 houses
[AccountWipe] audit: 0 houses (0 with a player owner, 0 with none), 0 owned boats, 0 tamed or summoned creatures, 0 player vendors, 0 player corpses, 0 items in a deleted container, 1107 loose items on Map.Internal, 6 ClusterF account records, 35041 mobiles, 206960 items
[AccountWipe] wiped in memory; saving the world before the request is removed.
[AccountWipe] census: 1 account, 0 characters, 0 houses
[08:19:54 INF] CrowdSec reporter disabled (machineId/password empty in crowdsec.json)
[08:19:54 INF] Blocklist disabled ("enabled" false in blocklist.json)
[08:19:54 INF] Listening: 127.0.0.1:2595
[08:19:54 INF] Listening: 172.30.0.2:2595
[08:19:54 INF] Listening: 127.0.0.1:12000 (Pings)
[08:19:54 INF] Listening: 172.30.0.2:12000 (Pings)
```

The one check:

```
08:20:01    checks: 1 (T-047)
08:20:05    T-047      run 1: PASS  countdown 'You will enjoy the benefits and relatively safe status of a young player for another 13 days and 23 hours of play time. Say "I want to grow
08:20:08    T-047      run 2: PASS  ...
08:20:11    T-047      run 3: PASS  ...
08:20:13    rule 1 held: both real shards are exactly as they were
08:20:14    Overnight play tests: 1 pass, 0 fail, 0 flaky
```

`shard.log` and `shard-start.log` contain no line with "exception". The shard did not crash, so no further exception
needed following. `Command stats already registered` is a warning that predates this change, not from it (not
investigated here).

## Patch notes

`CHANGELOG.md`: the 2026.10.14 section was already committed, so a new **2026.10.14.2** with one `### Staff` line,
"Fixed a start-up crash in the Imbuing catalogue." `VERSION` bumped to `2026.10.14.2`. Wiki not published.

## Deviations and decisions for Chase

- **Two changes, not one.** The prompt offered a lazy catalogue *or* an explicit build from `Initialize`. A lazy
  catalogue alone does not fix it (the first use is inside a `Configure`), and moving the table load to `Initialize`
  would put it after `World.Load`, a behaviour change for anything that reads the table while items load. The
  `CallPriority` keeps the load before `World.Load` and fixes the order. The lazy build is kept as well, so a future
  early use fails with a clear, non-poisoning message.
- **The `InvalidOperationException` guard is new behaviour** only on a path that crashed anyway.
- **Checked: no other `Configure` with a raised priority could now run before the imbuing one.** There are 91
  `public static void Configure` methods in `server/customizations`; three touch an Imbuing type
  (`ClusterFImbueKnowledge`, `ClusterFImbueEffects`, `ClusterFRecipeStore`). The other `CallPriority` attributes in the
  tree are `RegenRates.Configure` (10, earlier, reads no Imbuing type), `ClusterFSkillGain.Initialize` (100),
  `TestAccountWipe`'s two `Initialize` methods (int.MaxValue and int.MinValue), and `OnLogin` handlers in
  `ClusterFSkillCaps` and `ClusterFStatCaps` (100). None is a `Configure` that reads the table. Patched upstream files
  under `server/patches/` were not searched for imbuing reads (the Imbuing types are ours, so a stock file cannot
  name them, but a `.patch` could): `Imbue-custom-property-hooks.patch` is the one candidate and it adds runtime hooks,
  not start code. Unverified beyond that read.

## Repo size and preflight

No file over 5 MB in either repo: the bot-run folder is 400 KB, and `find -size +5M` over it, this note and the
changed code found nothing. The run's `*.log` files (run.log, shard.log, shard-start.log) are not committed:
`git check-ignore -v` shows `.gitignore:29:testing/bot-runs/*/*.log` for them. Scratch (test logs, fingerprint run) stayed in
the session scratchpad, outside both repos.

`Commit-ShardWork.ps1 -DryRun`:

```
=== code  (D:\ShatteredLegacy) ===
  5 file(s) pending:
    CHANGELOG.md
    VERSION
    server/customizations/ArtificersImbueGump.cs
    server/customizations/Imbuing/ClusterFImbueKnowledge.cs
    server/tests/Misc/ImbueStartOrderVerification.cs
  dry run: would add, commit and push

=== docs  (D:\UO\shard-migration) ===
  11 file(s) pending:
    notes/cc-P95-imbue-boot-fix.md
    testing/bot-runs/2026-10-14-0817/ (email.txt, real-shards-after.json, real-shards-before.json, report.md,
      results.json, world.json, transcripts/T-047-run1..3.txt, transcripts/session.txt)
  dry run: would add, commit and push

Repo Result
---- ------
code dry run
docs dry run
```

## For Chase

- **D89 can move to section 2 of `docs\bug-list.md`** (fixed), citing this note. Not edited here; `docs\` is the
  overseer's.
- The overnight bot can drop `-Commit 36c7ae9` now: HEAD with this fix boots (see Boot proof).
- The boot-proof run left `testing\bot-runs\2026-10-14-0817\` in this repo (the runner writes there; 1 check). It is
  evidence for this note, so it is left in to be committed.
- Files changed in `D:\ShatteredLegacy`: `server/customizations/ArtificersImbueGump.cs`,
  `server/customizations/Imbuing/ClusterFImbueKnowledge.cs`, `server/tests/Misc/ImbueStartOrderVerification.cs` (new),
  `CHANGELOG.md`, `VERSION`.

P95 DONE
