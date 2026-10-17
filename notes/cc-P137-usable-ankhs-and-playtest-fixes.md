# cc-P137: Every ankh works like OSI's, three play-test page fixes, the non-magic disenchant bug, and satchel auto-fill

Prompt: `D:\UO\cc-prompts\cc-P137-usable-ankhs-and-playtest-fixes.md`. Server code, the play-test service, the triage,
the overnight bot. Not committed; nothing deployed. Both repos were clean at the start.

## Headlines

- **Chase's ankh was a map static,** not a working ankh. It stands at Trammel 3464,2600,27, beside the League
  Registrar's office: the thatched building with the "League of Extraordinary Citizens" sign, east of the marble
  statue.
  - It is art 0x3 over 0x2, facing west, from the client's `statics1.mul`. A static has no behavior, so nothing can
    happen when it is used.
  - New Haven's working ankh is a different one: OSI's AnkhNorth at 3526,2516, which P17's seeder places, about
    70 tiles north-east.
  - **Fixed (ours, proposed D-123):** a working `AnkhWest` now goes over that static, with the same art and facing.
    OSI's data has no working ankh there, but Chase asked for one.
- **World-wide survey of every ankh graphic** (map statics on all six facets, plus the test world's items, read from
  its save). There are 90 ankhs:
  - 4 have a working ankh item on them.
  - 86 are decoration, and 1 of those is Chase's.
  - Every working ankh in OSI's data (pinned's and ServUO's decoration sets) is checked against the world. Pinned's
    set is all in place, put there by `[Decorate` plus our seeders.
  - **8 OSI working ankhs were missing:** 2 by the Felucca champion teleporters and 6 in Ter Mur (the Stygian Abyss).
    They exist only in ServUO's data. They are now placed by the same new seeder.
  - **Every other ankh static (85) stays decoration:** OSI's data has no working ankh on any of them. They are listed
    for Chase below.
- **Repeatable:** `[ClusterFSeedAnkhs [dryrun]` (`ClusterFAnkhs.cs`) works like the New Haven and guild-hall seeders.
  It is a WorldSetup command, idempotent, and moves and deletes nothing. A world-load switch,
  `clusterf.ankhs.seedOnWorldLoad`, defaults to false, so the fresh-world wipe runs it with the other world-setup
  commands.
  - `[ClusterFAnkhSurvey` lists every ankh and whether it works.
  - The guild halls (17 in New Haven, the Artificers' in Ter Mur) and the tutorial plaza have no other ankh.
- **Lock Karma is not on OSI's ankh any more:** pinned offers it only between UOTD and AOS (`Ankhs.cs:17`). On this
  shard's era the ankh's menu is Resurrect and Tithe Gold, as on OSI since AOS. The prompt's "Lock Karma / Unlock
  Karma" play-test item is written to that (deviation 1).
- **The play-test page picks up its own new code** with no restart (section 2):
  - **Tools changes** reload in place. Running requests and imports finish first; new ones wait a moment and then run
    on the new code.
  - **A change to `server.py` itself** drains running work and exits; the container's `unless-stopped` policy starts
    it again.
  - I chose this over a restart from the commit step because the live page is on **Haven**, which gets code from a
    git-pull sidecar. A restart from this PC would not reach it.
- **The unsorted play-test items are all sorted:**
  - It was **40, not 12**: 28 arrived after the prompt was written. Each has a Who and steps.
  - Four rows that said `CHASE` (not a bucket, so their items had no Who) now name one.
  - The check (`test_play_who.py` `RealFiles`) passes, and it gained a known-bucket fact.
  - The status page's "Needs overseer review" box (P136) now lists any unsorted item.
  - **Root cause found:** a paragraph before the For Chase list makes the importer skip the whole list. P123 and P127
    to P130 lost their items that way (deviation 4).
- **P119-1's run 2 fighter died**, killed by the third creature (the Lifestealer); the creatures were fine.
  - That run (7e108ac) never refilled the fighter between creatures. P129 (b856926) has since added the refill.
  - Now the fight also tops the fighter up below half its hits. If it dies anyway, it says "the fighter died (a test
    problem)" instead of blaming the creatures.
- **Disenchanting a non-magic item:**
  - It is refused at the target, before any page, with "There is no magic in this to unravel.".
  - The view, the confirm page and the apply step refuse it the same way, even from a view left open after the last
    property was extracted.
  - No shard is paid and no skill is gained.
  - Proposed bug D95 is below.
- **Satchel auto-fill (F-50, ours, proposed D-124):**
  - What goes in: essences from unravel (Extract) and from disenchant, and essences, magical residue and relic
    fragments a player loots or picks up. They go into the Artificers' Essence Satchel when one is in the backpack,
    nested or not.
  - What stays out: trades, bank moves, moves within the pack, crafting and buying.
  - A full satchel leaves the item in the backpack, with a message.
- **Tests:**
  - Shard: 11 new facts, plus 1 needed fix (a Diagnostic category); the full suite is **1,409 passed, 0 failed, 4
    skipped**.
  - Python: 9 new service and reload facts, 3 bot facts, 4 check facts and 2 review facts. Every one was seen failing
    first, or by a deliberate break.
  - shard-migration `tools	ests`: all 11 files green.

## 1. Ankhs

### Why Chase's ankh did nothing

- **Where it is:** Trammel 3464,2600,27 (head 0x3) and 3464,2601,27 (foot 0x2): a west-facing ankh in the client's
  map statics (`statics1.mul`).
- **What is on the tile:** in the test world's save (the automatic backup of 2026-10-17 22:35, read offline) there is
  no item on those tiles. Within a few tiles are only our League Registrar addons (`RegistrarOfficeAddon` with the
  "League of Extraordinary Citizens" sign) and spawners.
- **Why nothing happened:** a map static is art; the server never sees a double-click or a ghost walking up to it.
- **Why I am sure it is this one:**
  - It is the only ankh graphic in the New Haven region that is not working.
  - The two working ones there are the AnkhNorth at 3526,2516 (ServUO's New Haven ankh, placed by P17's seeder) and
    the AnkhNorth at 3606,2582 (pinned's pre-UOML Haven ankh, just outside the region).
  - Chase's description (thatched building, stone path, lamp posts, a marble statue to the east) is the Registrar's
    corner.

### How the survey was done

Scripts are in my session scratchpad. They are read-only and run against the server's own data:

1. **Map statics:** every `staidx<N>.mul`/`statics<N>.mul` pair the server loads, from
   `D:\ShatteredLegacy\client-data\classic-client`, for Felucca, Trammel, Ilshenar, Malas, Tokuno and TerMur. I looked
   for the eight working-ankh graphics: 0x2 to 0x5, and the bloodied 0x1D97/0x1D98 and 0x1E5C/0x1E5D.
   - The other "ankh" names in tiledata are decoration art (pumpkins, windows, vines, a vase, shields), not shrine
     ankhs. They were left out.
   - Result: 221 halves; Ilshenar 94, Trammel 42, Felucca 40, Malas 34, TerMur 11.
2. **Items:** the test world's `Items.idx` and `Items.bin` (pinned's v5 save format, base `Item` fields only). I took
   every AnkhWest/AnkhNorth, every rejuvenation ankh, the Despise ankhs, and every other item with an ankh graphic.
3. **Joined:** one row per ankh, counted by its head tile.
   - Working (an ankh item on it or beside it): 4. These are Felucca and Trammel 1854/1859,865 and their pair, all
     Destard's.
   - Not working: 86, of which 81 are map statics and 5 are `Static` items in Tokuno.
4. **OSI's working ankhs:** every AnkhWest/AnkhNorth/Rejuvination entry in pinned's and ServUO's
   `Data/Decoration`, 97 entry-facets, checked against the world's working items.
   - Every entry of pinned's set is in place.
   - Trammel Despise's rejuvenation ankh is replaced by the revamp's own `DespiseAnkh`, which works.
   - **Missing:** ServUO's two `_champion teleporters.cfg` ankhs (Felucca 6937,719 and 6947,987, hue 0x47E) and six
     from `Stygian Abyss.cfg` (TerMur 79,345/543/751 and 841,927/1094/1264).
   - None of OSI's entries stands on any of the 86 non-working statics. On OSI those statics were art too.

### What is not working, and stays decoration (for Chase)

85, all with no working ankh in OSI's data:

| Facet | Where | Ankhs | What it is |
|---|---|---|---|
| Ilshenar | 95-151, 1311-1447 | 44 | rows of ankh art in the Ankh dungeon's halls |
| Ilshenar | 719,1553; 1749,232 | 2 | single ankhs (one hued 1154) |
| Malas | 381-405, 383-409 | 6 | hued 1654, around Luna's central plaza |
| Malas | 269-358, 10-97; 384,1024 | 7 | bloodied ankh art, north coast and the Doom area |
| Malas | 72,223; 86,201; 87,244; 160,224 | 4 | west Malas |
| Felucca and Trammel | 1854 and 1859,865 | 4 | beside Destard's working ankh (1857,877 is the one that works) |
| Felucca and Trammel | 2028,2719; 5507,626 (hued 47); 5536,1880 | 6 | south of Trinsic; dungeon art |
| Felucca | 6939,1021 | 1 | bloodied ankh art |
| Trammel | 6872,3177 | 1 | far east |
| TerMur | 590,3064; 637,3054; 1168,1143; 1188,1116; 1208,1143 | 5 | Ter Mur art |
| Tokuno | 296,711; 780,1218; 1042,507; 1051,507; 717,1158 | 5 | `Static` items placed by `[Decorate` from pinned's Tokuno data |

If Chase wants any of these to work as well, the change is one line each in `ClusterFAnkhs.Placements`, marked "ours".

### What changed

- `server\customizations\ClusterFAnkhs.cs` (new, 303 lines):
  - `IsWorkingAnkh` (`:42`) counts both halves of a pinned ankh, the rejuvenation ankhs and Despise's.
  - `Placements` (`:52`) holds the 9 entries, each with its source.
  - `Seed` (`:103`) builds each entry with pinned's own `DecorationList.Read().Generate()` (through P17's
    `DecorEntry`), and skips an entry when a working ankh stands within 2 tiles.
  - `Classify` (`:161`), `Sightings` (`:207`), and `StaticSightings` (`:245`, which reads the .mul files directly,
    because `TileMatrix.GetStaticBlock` would cache every block).
  - `[ClusterFAnkhSurvey` (`:285`, Diagnostic) writes `Logs/ankh-survey.txt`.
  - `[ClusterFSeedAnkhs` (WorldSetup).
  - The `clusterf.ankhs.seedOnWorldLoad` setting (`:72`).
- `server\tests\Misc\AnkhVerification.cs` (new, 5 facts).

## 2. The play-test service reloads its own code

**Chose:** the service watches its own files. I did not choose a restart from the commit step:

- Since 2026-10-16 the live page runs on **Haven** (`D:\UO\haven-ops\state.json` mode `haven`).
- It gets code from the `sl-ops-git-pull` sidecar every 120 s, after the push.
- A restart run by `Commit-ShardWork.ps1` or the Golem on this PC would reach the game PC's container, which is not
  running, but not Haven's.

The self-watch works the same on both.

- `tools\codereload.py` (new):
  - `Gate` (`:27`): every request and every import runs inside `work()`. `drain()` waits for running work and holds
    new work until `reopen()`. Work nested inside work on the same thread never waits: `POST /api/import` runs the
    importer inside its own request.
  - `reload_modules` (`:87`): `importlib.reload` in dependency order. It deletes each module's `.pyc` first, because
    a `.pyc` records the source's time only to the second, so a quick same-size edit would load old bytecode. A test
    caught that.
  - `fingerprint` (`:110`) and `Watcher` (`:122`): a change must read the same on the next poll before it loads, so a
    file mid-pull is never loaded half written. A drain that times out is tried again on a later poll.
- `D:\ShatteredLegacy\docker\test-queue\server.py`:
  - `--reload-seconds` (`:98`, env `RELOAD_SECONDS`, default 5, 0 off).
  - `MODULES`/`GATE` (`:113-114`).
  - The running code's hash and load time in the service state (`:131`; `/api/items` `service.code` and
    `service.codeLoadedAt`).
  - `gated` wraps both listeners' GET and POST, and the importer (`:514`).
  - `reload_tools` (`:529`): drain, reload, rebuild the Access verifier, open. A module that fails to load is logged,
    and the old code keeps serving.
  - `restart_for_server_py` (`:549`): drain, then exit.
  - The two watchers (`:562-563`).
- **Never mid-request, never losing a save:**
  - A result is written by the importer's `Lock` and an atomic replace, inside a request.
  - The reload waits for every running request and import.
  - Requests that arrive during the reload wait at the gate (milliseconds) and then run.
  - Only a `server.py` change exits. A request that arrives in that second gets a refused connection, and the page
    then says "Not saved: ..." with the button enabled again (`html/index.html:406`). Nothing is lost silently.
- **To see it work:** `/api/items` `service.code` and `service.codeLoadedAt` change within about 10 s of a tools file
  changing on disk (on Haven, within about two minutes of a push). The process stays the same.
  - The log says `new tools code loaded (<hash>)`, or `NOT loaded, still running the old: <error>`.
  - **One restart is needed once,** to start the code that does the watching (For Chase).

## 3. Twelve items had no Who (forty by today)

- `/api/items` on today's `testing/play-tests.json` listed **40 unsorted**:
  - the prompt's 12;
  - the `-0` placeholders of P126 to P130, P132 and P133;
  - P131-1 to -6, P134-1 to -3, P135-1 to -3, P154-1 to -3 and P155-1 to -6.
- All 40 are sorted in a new group, "Sorted by cc-P137", at the end of `testing/bot-triage.md`, each with steps in
  `testing/playtest-steps.json`:

  | Bucket | Items |
  |---|---|
  | DEPLOY | P115-1, P115-3, P116-0, P117-0, P124-0, P125-1 to -5, P131-1 to -5, P133-0, P154-3, P155-1 to -4, P155-6 (23) |
  | EYES | P115-2, P132-0, P154-1, P154-2 (4) |
  | DECISION | P126-0, P155-5 (2) |
  | CC | P123-0, P127-0 to P130-0, P131-6, P134-1 to -3, P135-1, P135-2 (11) |
  | BOT-PARTIAL | P135-3 (1) |

  - The placeholders of prompts whose own rows are already here (P123, P127 to P130) are CC. Their steps say to mark
    the placeholder Moot once the real items are on the page.
  - P134-3 ("ask the vseUOAware server something") is CC with evidence: this session used that MCP server from a CC
    session in shard-migration.
- **One more arrived during the preflight:** the dry run's Haven mirror brought P136-0, the placeholder for P136's
  one-line For Chase. It is sorted DEPLOY in the same group (a web page), so 41 were sorted in all.
- **Four rows named a bucket the page does not know:** P128-8, P129-9, P130-6 and P130-8 said `CHASE`, so the parser
  dropped them. They now read EYES, DEPLOY, DEPLOY and DEPLOY.
- **P122-2, P122-3 and P122-4 had steps of the wrong shape:** each gained its check line, from the row's own reason.
- **The check:** `tools\tests\test_play_who.py` `RealFiles`.
  - `test_every_open_item_has_a_who` (`:288`) fails while any open item is unsorted.
  - New: `test_every_triage_row_names_a_known_bucket` (`:298`), with `playwho.malformed_rows` (`tools\playwho.py:56`).
  - The steps-shape fact is unchanged.
  - The old comparison of the triage's hand-kept Counts table with the page is gone. Every result and every new
    prompt's items broke it, so it failed for no fault. The Counts section now points at the page's live header and
    records the 2026-10-17 totals (deviation 3).
- **From now on (written into the triage, "Where a new prompt's items are sorted"):**
  - The prompt that writes items sorts them before DONE, under its own `### P<nn>` group, with steps, and runs that
    check.
  - Its For Chase list needs a "To try it" (or "in game", "checklist") line right before it, or the importer skips
    the list.
  - Anything that slips through shows in the status page's **Needs overseer review** box as "play-test items not
    sorted": `tools\progress.py` `review_playtests` (`:442`, wired in at `:496`).

## 4. P119-1 was a dead fighter, not the creatures

- **Confirmed** from `testing/bot-runs/2026-10-16-0130/transcripts/P119-1-run2.txt`:
  - `[set RawStr 250 Hits 175` once, at 5.74 s.
  - The ice hound and the orc chopper were killed.
  - The Lifestealer (`AI_Mage` since P119's port) was added at 14.29 s and pinned to 1 hit.
  - The fighter's status read 38/176 at 17.84 s, then 0/176 at 21.36 s, with the "So THAT'S What Resurrection Feels
    Like" achievement.
  - "You have died" followed at 23.85 s.
  - The last two creatures were spawned next to a ghost and timed out at 60 s.
  - The report and `run.log:3170` give run 2 as 0/176. Runs 1 and 3 ended at 113 and 163.
- **Cause:** that run's code (7e108ac) never refilled the fighter between fights, and the mage finished a fighter
  already worn down by two fights.
- **Already partly fixed:** P129 (b856926, after the run) refills to 175 before each creature and gives Dex 100.
- **Added now** (`tools\playtest-bot\uobot\checks.py`):
  - `_wait_kill` (`:626`): while waiting for the kill, it tops the fighter up with `[set Hits 175` whenever it drops
    below half its hits (at most every 3 s), so a single long fight cannot wear it down either.
  - When the fighter dies anyway (a ghost body, `GHOST_BODIES` `:623`, or 0 hits), the fight stops, saying "the
    fighter died (a test problem, not this creature's)" and "not fought: the fighter was dead" for the rest, instead
    of "never killed". It is used at `:677` and serves P129-1 as well.
  - The creatures are unchanged.
- **Not run against a shard here:** the next overnight run is the proof (play-test item P137-7). Last night's run
  (2026-10-17 01:30) did not get that far: the shard build failed on one test,
  `RaisedGardenVerification.AMoundGrowsWithoutWaterOrMaladies`, at 206d5a7. It passed in all three of my full runs
  today, so it looks time-dependent; see deviation 6.

## 5. Disenchanting a non-magic item paid an Essence Shard

**Proposed bug-list row (agents never edit `docs\`):**

> | **D95** | **A full disenchant of an item with no magic paid one Essence Shard** (`ArtificersImbueGump.HandleFullDisenchant`, "bare minimum for unenchanted items"), so vendor daggers farmed the Artificers' currency; OSI refuses to unravel an item with no magic. **FIXED cc-P137:** refused at the target with "There is no magic in this to unravel.", and the view, the confirm page and the apply refuse the same way; no shard, no skill gain. Facts `UnravelSatchelVerification` 1 and 2. | Chase 2026-10-16 11:20 |

- `server\customizations\ArtificersImbueGump.cs`:
  - `NoMagicToUnravel` (`:1501`).
  - The view shows it and no options (`:1283`).
  - The view's Full Disenchant button refuses (`:1567`).
  - The confirm page shows it and no apply button (`:1363`).
  - `HandleFullDisenchant` refuses before paying (`:1824`). The "1 shard minimum" line is gone.
  - The disenchant target refuses before any page (`:2005`).
- **Skill gain only on a real disenchant:** fact 2 sets Imbuing 50 with every roll passing. After a refused view
  button and a refused apply, the skill is unchanged; a real disenchant then raises it.

## 6. Unravel results go into the Artificers' satchel (F-50, ours)

**Proposed deviation row (`docs\fidelity-principle.md`):**

> | D-124 | **Ours (cc-P137, F-50, Chase 2026-10-16).** With an Artificers' Essence Satchel in the backpack, what Unravel produces (essences from extract and disenchant; stock magical residue, enchanted essence and relic fragments when looted or picked up) goes straight into it; OSI drops them in the backpack. A full satchel leaves the item in the backpack. Not on trades, bank moves, pack moves, crafting or buying. | Unravel results skip the backpack | `visible` | `cc-P137` 6 |

And for the ankh:

> | D-123 | **Ours (cc-P137, Chase 2026-10-16).** The ankh art beside New Haven's League Registrar (Trammel 3464,2600) is a working ankh (AnkhWest); OSI's data has no working ankh there, only the one at 3526,2516. | A ghost can resurrect there too | `visible` | `cc-P137` 1 |

- **What this shard's Unravel is:**
  - Our imbuing (P82) has no stock Unravel. "Unravel" here is the gump's Extract (`HandleExtractProperty`), which
    gives a `PropertyEssence` and Essence Shards, and Full Disenchant, which gives shards plus a 25% essence chance
    per property.
  - Essence Shards are **guild currency** (`guild.AddCurrency("artificers")`), not items, so there is nothing of them
    to put in a satchel (deviation 2).
  - Stock `MagicalResidue`, `EnchantedEssence` and `RelicFragment` exist as items (the Fountain of Fortune gives
    them). They are covered when looted or picked up.
- `server\customizations\ArtificersSatchel.cs`:
  - It now holds those four kinds (`CheckHold` `:49`, `IsUnravelResult` `:68`). It held essences only before.
  - `Find` (`:70`) uses `FindItemByType`, which recurses, so a nested satchel counts, as the ore satchel finds its
    own.
  - `TryStore` (`:73`) uses `TryDropItem`, which refuses past MaxItems or MaxWeight, and gives the full message.
  - `Deliver` (`:96`): the satchel first, else the backpack.
  - `IsLootPickup` (`:109`): the item's bounce record names where it was lifted from. The ground counts, and so does
    a container no mobile holds (a corpse, a chest). The player's own pack, bank, pack animals and trade windows do
    not.
- **Reused from the ore satchel:** its routing shape. `CompactOreSatchelRoutingHook.TryRouteToSatchel` filters with
  `Accepts`, finds with `FindItemByType` and stores with `TryDropItem`, falling through to the stock path. It hooks the
  Mining harvest, so there was no code to call; the same three steps are written for these items.
- `ArtificersImbueGump.cs:1844` and `:1906`: disenchant and extract deliver through the satchel. Crafting an essence
  (`HandleCraftEssence`) still uses the backpack.
- `server\customizations\ClusterFBackpack.cs:48`, `:59`: `OnDragDrop` and `OnDragDropInto` route loot pickups. Pinned
  calls these when an item is dropped on the pack or into its gump. `AddToBackpack` goes through `TryDropItem`
  instead, which the hunter's satchel hooks, so crafting, buying and quest rewards are untouched.
- Patch notes: one Added line.

## What changed (files)

**D:\ShatteredLegacy**:
- New:
  - `server\customizations\ClusterFAnkhs.cs`
  - `server\tests\Misc\AnkhVerification.cs`
  - `server\tests\Misc\UnravelSatchelVerification.cs`
- Changed:
  - `server\customizations\ArtificersImbueGump.cs`, `ArtificersSatchel.cs`, `ClusterFBackpack.cs`
  - `docker\test-queue\server.py`
  - `tools\playtest-bot\uobot\checks.py`, `tools\playtest-bot\tests\test_bot.py`
  - `CHANGELOG.md`, `VERSION`

**D:\UO\shard-migration**:
- New:
  - `tools\codereload.py`
  - `tools\tests\test_codereload.py`
  - this note
- Changed:
  - `tools\playwho.py`, `tools\progress.py`
  - `tools\tests\test_play_who.py`, `tools\tests\test_self_judging.py`
  - `testing\bot-triage.md`, `testing\playtest-steps.json`

The commit's `progress.py` run regenerates README, the dashboard and progress.json.

## Tests

Each new fact was seen failing first. Where the code came first, a deliberate break was applied to the code alone,
seen failing, and the file restored byte-identical (checked with `cmp` or a byte compare).

**Shard (`server\tests`), built and run in the builder image as `build.sh` does:**

- `UnravelSatchelVerification`: 6 facts.
  - Red before any code: **all 6 failed**. The plain dagger was not refused; the stale view paid; the essences
    landed in the pack, not the satchel; there was no full-satchel message.
  - Two failures were the tests' own and were fixed in the tests: a lift from a closed bank is refused, and 125
    satchel items overfill the test pack too.
- `AnkhVerification`: 5 facts.
  - The seeder came before them, so they were proven red by two break builds:
    - **A** dropped the New Haven entry and swapped the survey's block x/y: **all 5 failed**.
    - **B** made the "already there" test always false and dropped the second half from `IsWorkingAnkh`: **3
      failed** (seeding twice, the kept hand-placed ankh, and the survey).
  - The first version's Lock Karma fact failed against pinned (`Core.AOS`); that finding is deviation 1.
- `CommandDeclarationVerification` caught `[ClusterFAnkhSurvey` with no `[ShardCommand]`. It now has a Diagnostic
  category.
- **Full suite:** `Passed! - Failed: 0, Passed: 1409, Skipped: 4, Total: 1413`.

**shard-migration `tools\tests`:**

- `test_codereload.py`, 9 facts: gate, nested work, watcher, reload, and the real service.
  - The three service facts were red before `server.py` was wired ("unrecognized arguments: --reload-seconds").
  - The `.pyc` fact was red and found the stale-bytecode bug.
  - The nested-work fact was red before `Gate` was made re-entrant.
  - The gate and watcher came first, so they got six breaks, each caught:

    | Break | Failing |
    |---|---|
    | drain does not wait | 1 |
    | new work does not wait at a closed gate | 1 |
    | a change fires on first sight | 2 |
    | a refused reload is not retried | 1 |
    | nested work waits for the drain | 1 |
    | the stale .pyc is kept | 1 |

  - One flaky run after the breaks came from the test: two same-size writes in the same tick read as one file. Each
    touch now moves the time on by a second. That hid the stale-`.pyc` case, so the reload fact now keeps the file's
    time on purpose. After that, the break script caught all six, and the restored file passed (one run plus five
    more).
- `test_play_who.py`:
  - `RealFiles.test_every_open_item_has_a_who` failed before the sort with 40 unsorted.
  - `test_every_triage_row_names_a_known_bucket` and `MalformedRows` were red before `malformed_rows`; on HEAD's
    triage the function reports the four `CHASE` rows.
  - The steps-shape fact failed on P122-2, then P122-3 and P122-4.
  - The file passes **17 of 17**. Before this task, 2 of its tests failed on the real data, as P136 noted.
- `test_self_judging.py` `PlaytestSortReview`: 2 facts, red before `review_playtests`. Together with
  `test_status_dashboard` and `test_port_list`: **42 of 42**.
- The rest of `tools\tests` was green.

**Bot (`D:\ShatteredLegacy\tools\playtest-bot`):**

- `P119FightWatch`: 3 facts, red before `_wait_kill`.
- `python -m unittest discover -s tests`: **40 of 41**. The one failure is P112's known environmental one,
  `test_installer_dry_run_prints_the_call_and_registers_nothing`: the nightly task really is installed on this PC.

## Play-test items added

Seven, from the For Chase list. Their Who and steps are in `testing/bot-triage.md` (P137 group) and
`testing/playtest-steps.json`:

| Item | Bucket | Why |
|---|---|---|
| P137-1 | BOT | The ghost at the New Haven ankh. **The bot can die and walk:** run 2 above died, and the soak's walker walks, so it can walk a ghost to the ankh and read the resurrection gump. A check is not written yet (sketch in the row) |
| P137-2 | BOT | The ankh's context menu and the tithing gump |
| P137-3 | DEPLOY | The survey and the seeder on the test shard, after a deploy |
| P137-4 | BOT | The non-magic refusal and the unchanged shards |
| P137-5 | BOT | Satchel auto-fill |
| P137-6 | CC | The play-test page reloading new code (after the one restart) |
| P137-7 | BOT | P119-1 3 of 3 on the next overnight run |

## Deviations and decisions for Chase

1. **No Lock Karma at the ankh.**
   - The prompt asked for Lock Karma and Unlock Karma on the ankh's context menu. Pinned offers that only in the
     UOTD-to-AOS era (`Ankhs.cs:17`, `Core.UOTD && !Core.AOS`). This shard is past AOS, so its ankh menu is Resurrect
     and Tithe Gold, as on OSI since AOS.
   - I followed pinned and OSI (the fidelity principle). The play-test item says so.
   - If you want karma locking back at ankhs, that is a deviation for you to decide.
2. **Essence Shards are not items,** so the satchel cannot hold them. They are guild currency and go to the guild
   account as before. Everything Unravel gives as an item goes to the satchel.
3. **The triage's Counts table is no longer tested against the page.** Every result and every new prompt changed the
   real counts, so that check was always failing, and an always-failing check is how the 40 unsorted items went
   unnoticed. The page's header has the live counts.
4. **P123 and P127 to P130 never reached the page.**
   - Their For Chase lists start after a paragraph such as "**Rebuild the test shard** ... before trying these.". That
     paragraph puts the importer in "other" mode, which skips the whole list, so each left one "checklist not parsed"
     placeholder instead.
   - Their own triage rows describe items that do not exist on the page.
   - I did **not** add the marker to those old notes. Parsed today, P123's list gives 8 items against its 6 rows, and
     P130's numbers run one off from the seventh, so importing them would attach the wrong Who and steps.
   - **Proposed:** a small prompt to reconcile each of the five (or to make the importer treat a non-marker paragraph
     in For Chase as no change of mode), then mark the placeholders Moot.
5. **Eight more working ankhs in Felucca and Ter Mur** (the champion teleporters and the Stygian Abyss) come from
   ServUO's data only; pinned's has none of them. They are OSI's, so they are placed. If Ter Mur should stay closed
   until the races, `[ClusterFSeedAnkhs` places them harmlessly anyway.
6. **Last night's overnight run (2026-10-17 01:30) stopped at the build.** One shard test,
   `RaisedGardenVerification.AMoundGrowsWithoutWaterOrMaladies`, failed at 206d5a7. It passed in all three of my
   full-suite runs today, so it looks time- or order-dependent. Not mine; worth a look by P128's owner. P119-1's fix
   is proven by the next run that builds.
7. **The service reload works on a running request boundary, not a socket handoff.** A `server.py` change exits
   (drained), and the container comes back on the new file. A tools change, the normal case, never restarts.

## For Chase

**Where the ankhs were broken, and what changed:**
- The New Haven ankh you used (by the League Registrar, Trammel 3464,2600) was map art, so using it did nothing. It
  now gets a working ankh on top, with the same look; this is ours, since OSI's data has no working ankh there.
- Eight working ankhs OSI had but our world lacked (Felucca champion teleporters, Ter Mur) are placed too.
- The other 85 ankh statics were art on OSI as well, and stay decoration (table in section 1). Say if you want any of
  them working.
- Note: the ankh's menu is Resurrect and Tithe Gold. Lock Karma is not offered on this shard's era, as on OSI since
  AOS.

**To see the reload work:**
- Restart the play-test page once (Shard Console > Websites > **Ops pages: deploy**, or on Haven
  `docker restart sl-play-tests`) after this commit is pulled.
- From then on, after any commit that changes `tools\`, the page's `/api/items` `service.code` and
  `service.codeLoadedAt` change within about two minutes of Haven's pull, with no restart.

To try it in game, after this build is deployed to the test shard and `[ClusterFSeedAnkhs` has been run there as Administrator:

1. **A ghost at the New Haven ankh:** kill a test character and walk its ghost up to the ankh by the League Registrar (3464,2600): the resurrection gump opens.
2. **A living player at that ankh:** its context menu offers Resurrect and Tithe Gold (no Lock Karma, as on OSI since AOS); Tithe Gold opens the tithing gump.
3. **The ankh survey:** as staff, `[ClusterFAnkhSurvey` gives the counts (working, waiting for the seeder, decoration) and writes Logs/ankh-survey.txt; after the seeder, nothing is waiting.
4. **No magic, no shard:** at the imbuing table, disenchant a vendor dagger: "There is no magic in this to unravel." before any page, and your Essence Shards are unchanged.
5. **Into the satchel:** with the Artificers' Essence Satchel in your backpack (in a bag is fine), extract a property from a magic weapon: the essence is in the satchel; pick up magical residue from the ground: into the satchel; with the satchel full, the next one stays in the backpack with a message.
6. **The play-test page reloads itself:** after the one restart, a later commit that changes `tools\` shows a new `service.code` on `/api/items` within about two minutes, with no restart.
7. **P119-1 overnight:** the next overnight run that builds passes P119-1 3 of 3, or, if a fighter dies, says "the fighter died (a test problem ...)" instead of blaming the creatures.

## Patch notes

`D:\ShatteredLegacy\CHANGELOG.md` has a new section, 2026.10.17.7, because 2026.10.17.6 was committed with P136:
- Added: the satchel auto-fill.
- Fixed: the New Haven ankh, and the non-magic disenchant.
- Staff: the survey and seeder, the page reload, and the bot fight.

`VERSION` is 2026.10.17.7. The wiki was not published.

## Repo size

No pending file is over 5 MB; the largest new file is `ClusterFAnkhs.cs` (about 13 KB). The world-save reads, the
survey outputs and the builder logs stayed in my session scratchpad, outside both repos. The scratch builder images
are `sl-uo-builder:p137` and `sl-uo-builder:p137m`; `latest` was not moved.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`, after the last edit:

```
Repo Result
---- ------
code dry run
docs dry run
```

- **code** (11 files): the three new files (`ClusterFAnkhs.cs`, `AnkhVerification.cs`, `UnravelSatchelVerification.cs`)
  and the changed `ArtificersImbueGump.cs`, `ArtificersSatchel.cs`, `ClusterFBackpack.cs`, `docker/test-queue/server.py`,
  the bot's `checks.py` and `test_bot.py`, `CHANGELOG.md` and `VERSION`.
- **docs:** this note, `tools/codereload.py`, its test, `playwho.py`, `progress.py`, the two changed test files, the
  triage and steps, and the importer's machine output (`testing/SUMMARY.md`, `testing/play-tests.json`).

P137 DONE
