# cc-P37: ModernUO upgrade, part 1 of 3: prep on the current engine

2026-10-02. Brief: `D:\UO\cc-prompts\cc-P37-upgrade-prep.md`. Work is in `D:\ShatteredLegacy`, **uncommitted, live not
deployed or touched**. Final image `sl-modernuo:cc-p37` (`0e65420330ca`), builder `sl-uo-builder:cc-p37`.
`sl-modernuo:latest` (`246b0d5813e5`) and `sl-uo-builder:latest` (`ea126d1c4493`) were not moved. No commit landed in
either repo while I worked (`5d1e15a` / `d67f587` at start and end). P33 was committed (`5d1e15a`) before I started:
no clash.

Citations are pinned `7c9215d97` unless marked **U:** (upstream `d4531cd9`).

## Headlines

1. **All seven items are done and proved on the current engine.** Gate: **455/455** shard tests (447 before, **8 new
   facts**), every new fact watched red for its own mutation first (section 4).
2. **The mount fix works, and the old layout loses the world on the new engine, reproduced again.** The test shard
   now runs for real on `server\lib\uo\modernuo-test\` (its save moved there, backups now persist on the host). A
   live-shaped copy booted and autosaved twice through the real new `docker-compose.yml`. On the trial (upgrade)
   image, the old Saves-only mount failed the first save and left the host `Saves` with **0 files**; the parent
   mount published cleanly, idx header v3 -> **v5**.
3. **The purge command finds exactly P30's numbers on a copy of the test save: 107 creatures and 1 item** (32 Slith,
   22 StoneSlith, 20 Spellbinder, 18 ToxicSlith, 15 Raptor, 1 ValkyriesGlaive), none tamed or held, plus 27 spawners
   that name one of the types. After purge and save, **the new engine loads that save with no prompt at all**
   (no bad-deserialize prompt, no pathfinding prompt). Not run on the real test shard: that is P39's.
4. **`"pathfinding.prebakeMaps": "False"` is proved both ways.** The current engine ignores it and keeps it when it
   rewrites the config. On the upgrade image under a TTY, with the key the shard boots straight to `Listening`;
   without it, it blocks at "Pre-bake the pathfinding cache for your selected maps now?".
5. **Groves are permanent now, and that exposed a real defect: Starwood can never be chopped**, before or after
   this change. Pinned's `GetVeinFrom` tests `randomValue <= VeinChance` (`HarvestDefinition.cs:155`), so the first
   vein gets one value too many and the last one too few. Starwood is last with weight 1, so it gets **0 of 1,036**
   (measured over 6,246,932 banks). Upstream d4531cd9 has the same line. It needs an engine patch, which this prompt
   rules out, so the fact pins the measurement and **Decision 1** asks how to fix it. Mining's Celestial is in the
   same position (deduced from the same code, **not probed**).
6. **Two things for Chase about live, neither caused here.** (a) The live container has been stuck at the D40
   `Bad deserialize of Server.ClusterFAccountPersistence ... (y/n/a)` prompt since its 06:57 boot today (and since
   2026-09-29 14:16 before that). That is D40, already moot by your 2026-09-30 decision; recorded only because it
   decides when to deploy the compose change (section 5). (b) After the live compose change, the shard console's
   status-publisher line will say "written by: none" (section 7, item 3).

## 1. What changed, file by file (`D:\ShatteredLegacy`)

| File | Change |
|---|---|
| `docker/uo/docker-compose.yml` | **Protected (Q-009), Chase stages it.** The four mounts Saves, Backups, Archives and status become one: `${SERVER_PATH}/lib/uo/modernuo:/var/lib/uo/modernuo`, with the reason in a comment. Nothing else touched (the `build:` block is the runbook's step 2, still pending). |
| `docker/uo/docker-compose.test.yml` | `.../modernuo/Saves-test:/var/lib/uo/modernuo/Saves` becomes `${SERVER_PATH}/lib/uo/modernuo-test:/var/lib/uo/modernuo`. |
| `docker/uo/test-shard.sh`, `docker/uo/Start-TestShard.ps1` | Test save is `server/lib/uo/modernuo-test/Saves`. Both **refuse to start while an old `modernuo/Saves-test` exists**, so a forgotten move cannot seed a fresh world beside an orphaned old one. `-Fresh` still deletes only `Saves`. |
| `scripts/Shard-Console.ps1` | Test shard's `Saves` path, plus three texts that named `Saves-test`. Asides now appear as `modernuo-test\Saves.aside-*` (the console's generic `<save>.aside-*` rule, unchanged). |
| `scripts/tests/Shard-Console.Tests.ps1` | One message text; the red-commands list gains `[ClusterFPurgeUpgradeCollisions` and its `dryrun` (test-only commands are red by design). |
| `docker/uo/Dockerfile` | `ARG MODERNUO_COMMIT=7c9215d97` moves before the first `FROM` (**now line 3**, was 4; P30 section 6's re-pin list says `:4`). The runtime stage sets `ENV SL_MODERNUO_COMMIT`. |
| `docker/uo/entrypoint.sh` | Banner prints `${SL_MODERNUO_COMMIT:-unknown}`, not a hardcode. |
| `docker/uo/build.sh` | Builder tag follows `-t` (`-t sl-modernuo:cc-p37` builds `sl-uo-builder:cc-p37`; default stays `latest`), with `--builder-tag` to name it outright. It prints both tags at start. |
| `server/customizations/ClusterFPurgeUpgradeCollisions.cs` | **New.** The purge command, section 3. |
| `server/customizations/ClusterFLumberjackingExtension.cs` | The vein code moves into `public static int ApplyExtendedVeins(HarvestDefinition)` (so a test can apply it to a fresh definition), which ends with `def.RandomizeVeins = false`, as `ClusterFMiningExtension.cs:131` does. The startup log line says groves are permanent. |
| `server/tests/Misc/PurgeUpgradeCollisionsVerification.cs` | **New**, 5 facts. |
| `server/tests/Engines/Harvest/PermanentGrovesVerification.cs` | **New**, 3 facts. |

Outside git:
- **`server/uo/modernuo/Configuration{,-test}/modernuo.json`**: `"pathfinding.prebakeMaps": "False"` added after
  `pathfinding.maxResidentChunks` (alphabetical, where the server writes it). Copies from before the edit are in my
  scratchpad. Gitignored, so there is nothing to stage.
- **Test world moved.** `server/lib/uo/modernuo/Saves-test` became `server/lib/uo/modernuo-test/Saves`. Its three
  `Saves-test.aside-*` folders became `modernuo-test/Saves.aside-*`, same stamps. The container's own `Backups` and
  `Archives` (205 MB and 207 MB, which a recreate would have thrown away) were copied out into
  `modernuo-test/`. A byte copy of the save as it was at the move is at `D:\UO\cc-p37-work\test-save-orig` (`diff -r`
  identical).
- **Test shard restarted on the new mount** with the same image as before (`sl-modernuo:latest`). It is up now, as
  it was before I started.

Not done, on purpose: no engine change; no edit to `docs\`. The citation line for `docs\README.md` is the
overseer's.

## 2. Proofs

All runs except "test shard, for real" were on copies under `D:\UO\cc-p37-work\` with `--network none` (or compose
`network_mode: none`). The live container was never touched: `sl-modernuo` showed "Up 8 hours" before and after.

| # | What | Image | Mount | Result |
|---|---|---|---|---|
| T | **Test shard, for real**, via `Start-TestShard.ps1 -SkipBuild` | `sl-modernuo:latest` (current engine) | new parent `modernuo-test` | Loaded the moved save (206,501 items, 35,179 mobiles). The 15:05 autosave wrote `modernuo-test/Saves` (Mobiles.bin 15:05:01), and the backup landed on the host (`modernuo-test/Backups/Automatic/2026-10-02-20-05-01`). Before the move, `docker compose stop` had saved through SaveOnShutdown ("saved in 1218 ms"). |
| L | **Live-shaped copy**: the real new `docker-compose.yml` plus an override (`container_name`, `ports: !reset []`, `network_mode: none`, `image`), live Configuration copy (with the prebake key), `SERVER_PATH` pointed at a scratch tree | `sl-modernuo:latest` (what the runbook deploys) | new parent | Listening on 2593, status.json written to the host `status/` through the parent mount, autosaves 15:10 and 15:15 into `Saves`, backups on the host. **Save content:** a copy of the test world, not the live save. The live save cannot be loaded by any image (D40; `uo-modernuo` on a live copy stops at the same prompt live is stuck at). That world is retired anyway, and the test world is the next live's base. |
| B | Purge dry run, purge, save, dry run; config rewrite forced by deleting `timer.maxPoolCapacity` from the copy | `sl-modernuo:cc-p37` | parent | Section 3. Config rewritten at boot (15:19:29) with `timer.maxPoolCapacity` back and **`pathfinding.prebakeMaps` kept**. |
| C (red) | Run B's purged save, **old Saves-only mount** | `sl-modernuo:cc-p30-trial` (upgrade) | `Saves` only | Loads with **no prompt** (207,152 items, 35,199 mobiles). First save: `Set aside .../Saves as Saves.previous-...`, then `IOException: Cannot create '/var/lib/uo/modernuo/Saves'` (`World.cs:451/488`), repeated each autosave. **Host `Saves`: 0 files.** P30 run 2b, reproduced. |
| D (green) | the same, **parent mount** | `sl-modernuo:cc-p30-trial` | parent | Autosaves 15:35 and 15:40 published, backups on the host, `docker stop` -> SaveOnShutdown "saved in 496 ms". Host `Saves` has 20 files; `Mobiles.idx` header **05** (run B's was **03**). |
| P | Prompt check, TTY attached, run B's purged save | `sl-modernuo:cc-p30-trial` | parent | **With the key:** loads and listens, no prompt. **Without it:** blocks at "Pre-bake the pathfinding cache for your selected maps now?". (Runs C and D piped stdin, which skips that prompt anyway (U:PathCacheCommands.cs:61), so they could not show this.) |
| E | Banner | `cc-p37` | | `SL_MODERNUO_COMMIT=7c9215d97` in the image. Run with `-e SL_MODERNUO_COMMIT=d4531cd9`, the banner line prints `Commit: d4531cd9`. The trial image still shows the old hardcode. |
| F | No engine change | `cc-p37` vs `cc-p33` (HEAD build) | | `Server.dll` byte-identical (`917dc6a9...`, also in cc-p32, cc-p31-office and latest). `ModernUO.dll` differs, but it differs between **every** pair of our builds (cc-p32, cc-p33 and latest all differ), so it is not a deterministic output and says nothing. `UOContent.dll` differs, as it must. |

**"The current engine ignores the key":** the name appears nowhere in pinned (`grep -rn prebakeMaps` over
`Projects/` gives 0 hits; upstream's is U:PathCacheCommands.cs:28). Runs T, L and B booted with it and logged nothing
about it. Pinned keeps unknown keys in its settings dictionary and writes them back (run B).

Build logs: `D:\UO\cc-p37-work\build1.log` (first run, 454/455: the Starwood probe), `build-red.log` (mutations,
447/455), `build2.log` (green, 455/455). Run logs: `runB..runD/run.log`, `liveproof.log`.

## 3. The purge command

`[ClusterFPurgeUpgradeCollisions` (Administrator, `[ShardCommand(WorldRemoval, Rerun = DeletesAgain, Shard = TestOnly,
DryRun = "dryrun")]`). Same verb on the server console: `purgecollisions` / `purgecollisions dryrun` (through `docker
attach sl-modernuo-test`). **As with every world command here, the plain form acts and `dryrun` reports.** `purge` is
accepted as an explicit synonym; any other word does nothing. I first wrote "no argument = dry run". I changed it
because the console presents the plain form as the destructive one, and a command that differed would mislabel itself
there.

- **Deletes** every mobile and item whose type is one of the 11 or derives from one (none derives today:
  `WindOfCorruptionHuman` is a `Bow`). A creature's pack goes with it. Tamed, stabled and `Map.Internal` (shrunk)
  creatures are named with their owner, and items with their holder. `ShrunkPet` already handles a deleted pet
  (`ShrunkPet.cs:75-81`).
- **Keeps spawner entries, and holds those spawners for 30 minutes.** Reading "and their spawner entries" literally
  would have deleted the entries. I did not: entries are type **names**, they read fine on the new engine, and they
  are what refills Ter Mur with upstream's creatures (P30 2c). The hold exists because deleting a spawned creature
  restarts its spawner (`BaseSpawner.cs:463-475`), so our type could respawn and then be saved by SaveOnShutdown
  between the purge and the stop. `End` is saved (`BaseSpawner.cs:1462`), so on the new engine the hold has long run
  out and the spawner fills at once. **Spawner refill on the new engine is still unverified in game**, as in P30.
- **Guard.** It refuses unless all 11 still carry `[SerializationGenerator(_, false)]`, which is the exact property
  that breaks the load. After the bump the names are upstream's encoded types, so a stray run deletes nothing. P38
  should delete the command and its test with our 11 files anyway.
- The ValkyriesGlaive stealable slot needs nothing (`StealableArtifacts.cs:385-388, :409-419`).

**Dry run on a copy of the test save** (run B, the save as it was at 15:02, full output in `runB/run.log`):

```
DRY RUN, nothing changed: 107 mobile(s), 1 item(s), 27 spawner(s) naming one of the 11.
  Raptor: 15
  Slith: 32
  Spellbinder: 20
  StoneSlith: 22
  ToxicSlith: 18
  ValkyriesGlaive: 1
  item: ValkyriesGlaive 0x40037E87 at (843, 665, 27) TerMur
  spawner: 0x40005746 at (1134, 3483, -42) TerMur, running True: ChickenLizard, GreaterMongbat, Mongbat, RuddyBoura, SilverSerpent, Slith, Bird
  ... 24 more Ter Mur spawners (Raptor, Slith, StoneSlith, ToxicSlith entries) ...
  spawner: 0x4000B146 at (3650, 2509, 0) Trammel, running True: Zombie, Skeleton, spellbinder
  spawner: 0x4000B255 at (3598, 2450, 16) Trammel, running True: spellbinder, Zombie, Skeleton
TOTAL (dry run): would delete 108 and hold 27 spawner(s) for 30 min.
```

No "owned:" line: none of the 107 is tamed, stabled or shrunk. Then `purgecollisions` gave `TOTAL: deleted 108, held
27 spawner(s) for 30 min`, `save`, and the second dry run gave `would delete 0`. The two Trammel spawners in Old
Haven name `spellbinder` in lower case; `FindTypeByName` is case-insensitive, so they were caught. That is 27
spawners **counted from the output**, not from P30.

## 4. Tests and red proofs

| Fact | Mutation that turned it red | Red message |
|---|---|---|
| Purge 1 `AllElevenStillHaveOurSerializationShape` | (f) `Raptor` given upstream's `[SerializationGenerator(0)]` | `Collection: [typeof(Server.Mobiles.Raptor)]` |
| Purge 2 `TheGuardRefusesWhenATypeIsEncodedAndDeletesNothing` | (e) the guard never refuses | `Assert.True` at `report.Refused` (line 72) |
| Purge 3a `DryrunReportsThePlainFormAndPurgeDeleteAnythingElseDoesNothing` | (b) the plain form becomes a dry run | `ParseMode(null)` (line 89) |
| Purge 3b `ADryRunReportsAndDeletesNothing` | (d) a dry run deletes | `report.Deleted` expected 0 (line 116) |
| Purge 4 `APurgeDeletesTheElevenKeepsTheRestAndHoldsTheirSpawners` | (c) no spawner hold | `InRange (00:29:00 - 00:30:00)` |
| Groves 1 `ExtendedLumberIsNotRandomizedAndWeighsTheCombinedList` | (a) `RandomizeVeins = false` removed | `Assert.False` at `def.RandomizeVeins` |
| Groves 2 `TheSameSpotKeepsItsWoodAcrossDefinitionsAndAfterTheBankCacheIsCleared` | (a) | `Felucca 3,99: OakLog vs fresh definition Heartwood`, ... |
| Groves 3 `EveryWoodButStarwoodOccursAtAboutItsShare` | (a) | `IronwoodLog: 0 banks, expected about 48239; ...` (randomized veins draw `Random(1000)` at first touch, `HarvestDefinition.cs:138`, so no extended wood) |

All six mutations went into one tests-only build (`build-red.log`): **447 passed, exactly these 8 failed**, each at its
own assertion. Restored from backup (`grep MUTATION` = 0, `Raptor.cs` unchanged in git), then green 455/455.

**Shard console suite (PowerShell): 83/84.** The one failure, `PlayerCommandsNeverAppearInTheWorldTab`, also fails on
a clean `git archive HEAD` copy (`version` is a Player command its list predates). **Pre-existing, not mine**, not
fixed.

## 5. Groves: what changed, the defect, P13's ledger

- **Before:** `RandomizeVeins = Core.ML` (`Lumberjacking.cs:118`), true here. A bank rolled `Random(1000)` on first touch
  (`HarvestDefinition.cs:136-139`), which can never reach the extended woods (they sit at 1000..1035 of 1036). It
  rolled `Random(VeinWeights)` again on every respawn (`HarvestBank.cs:60-63`). So **a spot's wood changed on every
  respawn, not only on restart**, and the extended woods came only from respawned banks.
- **After:** a stable function of the bank's x, y and map (`HarvestDefinition.cs:141-143`), over `VeinWeights` = 1036
  (the `Veins` setter, `:66-77`, recomputes it; fact 1). The same wood came back across fresh definitions and after
  `Banks.Clear()` at 30,656 grid spots on six facets (fact 2). Over every real bank cell of six facets (6,246,932;
  **lumber banks are 4x3 tiles**, `Lumberjacking.cs:43-44`, not mining's 8x8), every wood but Starwood occurs at 0.87
  to 1.15 of its share (table in `build1.log`; the code and so the numbers are deterministic).
- **The defect (proposed bug-list row, ModernUO's code, ours to patch, fine to report publicly, not exploit-class):**
  `GetVeinFrom` uses `<=` (`HarvestDefinition.cs:155`; also U:HarvestDefinition.cs:155). Exact shares over 0..1035:
  Log 491, ..., Voidwood 2, **Starwood 0**. Starwood has never been choppable on this shard. Mining's Celestial is
  the same shape (last vein, weight 1, `ClusterFMiningExtension.cs:117`): **deduced, not probed.** Stock ModernUO
  loses one value from its last vein (Frostwood 9 of 1000 instead of 10). Reverses when either:
  - (a) a one-character engine patch makes it `<`. That shifts every stock share by one value per 1000, and mining's
    too.
  - (b) ours reorders the veins so a weight-1 vein is not last. That is a data hack against an engine bug.

  I recommend (a) in P38, with the fact's Starwood line flipped to its weight. **Decision 1.**
- **P13's ledger still matches, and is now worth more.** It records where the **player** stood (`m.Location`), and
  merges finds of one wood within 15 tiles on the same facet and region (`ClusterFLumberjackingExtension.cs:142`,
  `WoodDiscoveryEntry.cs:133`). A tree's 4x3 bank is within reach of that point, and its wood no longer changes, so a
  recorded grove leads back to that wood. Two caveats for the teleport feature:
  - A 15-tile grove spans several banks, and those banks need not share the wood. The record means "this wood was
    found near here", not "every tree here".
  - Groves recorded before this change may point at banks whose wood was a random roll that is now replaced by the
    stable one.
- **Upstream did not touch `Lumberjacking.cs` or `HarvestDefinition.cs`** between 7c9215d97 and d4531cd9 (`git diff
  --stat` over `Engines/Harvest`: only `HarvestSystem.cs`, 1 line). P38's re-check is already answered: nothing to
  redo.

**Deviation text for the register (`docs/fidelity-principle.md`, overseer's):**

> **Permanent groves (cc-P37, Chase 2026-10-02).** Since Mondain's Legacy OSI gives each tree bank a random wood that
> re-rolls when the bank regrows (pinned `Lumberjacking.cs:118`, `HarvestBank.cs:60-63`). Ours fixes each bank's
> wood by its location (`ClusterFLumberjackingExtension.ApplyExtendedVeins`, `RandomizeVeins = false`), as our mining
> already does for ore, so the logging book's recorded groves keep their wood. The proportions of each wood across
> the world are unchanged. Reverses when the logging book no longer relies on a recorded spot.

## 6. What Chase stages and deploys for live, and when

**Stage (any time):** `docker/uo/docker-compose.yml` is on `Sync-ShardRepos.ps1`'s protected list, so `-All` will
report it as "PROTECTED, not staged". Stage it by hand before your commit script:

```powershell
cd D:\ShatteredLegacy; git add docker/uo/docker-compose.yml
```

Everything else in section 1 goes in with your normal `Commit-ShardWork.ps1` run.

**Deploy: at the wipe, together with the runbook's step 2. Not now.**
- It is safe on the current engine at any time (run L).
- But it must be live **before live's first save on the new engine**. A live recreate today would only boot back into
  D40's prompt, which nobody is answering because that world is retired. So deploying now buys nothing.
- At the wipe, `Live-Deploy-Runbook.md` step 2 (replace `build:` with `image: sl-modernuo:latest`) and this mount
  change edit the same service block. Make both edits, then `docker compose up -d modernuo` (the runbook's step 5)
  recreates the container with both.
- The runbook's step 4 moves `Saves` aside within the same parent folder, which the new mount still covers. No change
  is needed there.
- The live `Configuration` already has `pathfinding.prebakeMaps` (gitignored). The stuck live process will not rewrite
  it; check with `Select-String prebakeMaps D:\ShatteredLegacy\server\uo\modernuo\Configuration\modernuo.json` before
  the wipe.

**After the new mount, the live container also sees** `Snapshots\` (the console's save snapshots, test ones included)
and the old `temp\` in that folder. Both are harmless. The test world no longer lives there.

## 7. Found on the way, not fixed (out of scope)

1. **Starwood unreachable** (section 5). Decision 1.
2. **D40, live stuck at a load prompt since 06:57 today** (log above). Known and moot; mentioned only for section 6.
3. **The shard console's publisher check will go wrong once live mounts the parent.** `Shard-Console.ps1:996` counts a
   container as the status writer only if a mount's destination is exactly `/var/lib/uo/modernuo/status`. After the
   live change it will report "written by: none", and the "only TEST writes status" warning can no longer fire (the
   test shard now writes `modernuo-test\status`, which nothing serves, which is correct). Fix: capture each mount's
   `Source` beside `Destination` (`:205`), and count a writer when the destination is the target or an ancestor of it
   and the source maps to `Publisher.Folder`. Out of this prompt's script scope (only paths naming Saves); **before the
   live deploy**.
4. **`PlayerCommandsNeverAppearInTheWorldTab` already fails at HEAD** (`version`), section 4.
5. **The upgrade image ignores piped console commands.** In runs C and D, `save` and `shutdown` did nothing, and the
   runs ended on autosave and `docker stop`; pinned obeyed the same input (run B). Unexplored, and it does not affect
   a TTY attach. It matters only to anyone scripting the new engine's console.
6. **After the bump, the test-shard seeding copies `SerializedTypes.db` from live**, and the new engine has no such
   file (P30 run 3: types live in the idx). The `Test-Path` guards make that a harmless no-op, but the D19 comment
   will then describe a file that no longer exists. That is P38's.

## 8. For P38 and P39

- P38: delete `ClusterFPurgeUpgradeCollisions.cs` and `PurgeUpgradeCollisionsVerification.cs` with our 11 collision
  files. Its "all ours" fact goes red on the bump by design, so the gate forces it.
- P38: the pin is `Dockerfile:3` now, and `docker-compose.yml:8`'s build arg is still a second pin until the runbook's
  step 2 removes the `build:` block.
- P38: build with `-t sl-modernuo:cc-p38`. The builder tag now follows it.
- P38/P39: groves need nothing on the bump (section 5).

## 9. Checklist for Chase

- [ ] Read Decision 1 (Starwood): engine patch `<` in P38 (recommended), reorder our veins, or leave it.
- [ ] Commit: stage `docker/uo/docker-compose.yml` by hand (section 6), then `Commit-ShardWork.ps1`.
- [ ] Do **not** deploy live now. At the wipe: runbook step 2 plus this mount, together. Before that, fix the
      console's publisher check (section 7.3), or accept "written by: none" for a while.
- [ ] Test shard: nothing to do. It is up on its new folder `server\lib\uo\modernuo-test`. Its old save is at
      `D:\UO\cc-p37-work\test-save-orig`.
- [ ] P39, on the test shard only, after the P38 image is approved: `[ClusterFPurgeUpgradeCollisions dryrun` (expect
      about 107 + 1, plus anything spawned since), `[ClusterFPurgeUpgradeCollisions`, `[save`, dryrun again (expect
      "would delete 0"), then stop **within 30 minutes**. Then the P30 rollback copies, then the new image.
- [ ] Scratch to delete when the upgrade is done: `D:\UO\cc-p37-work\` (save copies with accounts, the live-shaped
      copy, run logs), `sl-modernuo:cc-p37`, `sl-uo-builder:cc-p37` (about 5 GB). I deleted my red builder image.
