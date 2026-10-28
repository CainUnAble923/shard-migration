# Shattered Legacy: ServUO content on ModernUO

Working repo for **staying on ModernUO** and pulling selected ServUO content into it,
piece by piece. Reversed from the original migrate-to-ServUO plan on 2026-09-06; see
`docs/direction-decision.md` for why.

This repo is the shared source of truth for everyone working on the migration,
human or agent. If a decision is not written down here, it is not decided.

## Why we are doing this

ModernUO declares expansions through `EJ` but never implemented the content.
Measured by file count in each tree:

| Content | ServUO pub57 | ModernUO main |
|---|---|---|
| High Seas | 134 | 0 |
| Time of Legends / Eodon / Myrmidex | 74 | 0 |
| Ter Mur / Stygian | 18 | 5 (spawn data only) |

Target scope is the **full post-ML world including naval combat and Eodon**, which is
precisely the content ModernUO lacks. See `docs/direction-decision.md` for why porting
the other way was costed and rejected.

## What we give up

ServUO targets `net48` and runs under Mono off Windows, versus ModernUO's .NET 10.
Serialization goes from source-generated back to hand-written. This is a deliberate
trade of engineering quality for content reach. Do not relitigate it in code review.

## Layout

```
docs/     decisions and plans. Read these first.
tools/    converters and migration scripts (spawners, accounts)
notes/    working notes, scratch findings, anything not yet a decision
```

## Start here

1. `docs/migration-plan.md` - the seven phases, in order
2. `docs/direction-decision.md` - why ServUO and not the reverse port
3. `docs/shard-inventory.md` - what we actually have to migrate, and the revised Phase 2 scope
4. `docs/client-analysis.md` - what UOAlive and Immortal Realms customized, and the
   custom-facet finding that changes our map plans

## Current status

- [x] Direction decided: migrate to ServUO
- [ ] **URGENT** Deploy/restart the ModernUO image so startup enforces SHA2 password hashing
      (enforcement is staged in the shard infrastructure repo; live state is unverified)
- [x] Custom surface counted: **~131 files / ~39,900 lines**, already isolated from
      upstream. No Core bucket. See `docs/shard-inventory.md`
- [x] Shard located: `shattered-legacy-infrastructure` (builds ModernUO from pinned commit)
- [x] Add `client-data/` and `server/uo/` to that repo's `.gitignore`
- [ ] Stand up stock ServUO pub57 reference shard
- [x] Create the independent `ServUO-work` scratch clone; keep the pub57 reference pristine
- [ ] Write spawner JSON to XmlSpawner XML converter
- [ ] Write accounts exporter (MUO binary to ServUO accounts.xml)

## Migration progress

<!-- PROGRESS:START -->
**Direction: staying on ModernUO.** ServUO content is pulled in piece by piece.

Judgment reviewed 2026-10-25. Shard version 2026.10.28.3. Golem on, 21 queued, latest done P718. Play tests: 1384 open, 4 failed, 43 passed.

### Needs overseer review (4)

- **gate The player package installs on a clean PC**: Waits on a confirmation: Chase: which package is published on get.shatteredlegacyuo.com (the one with the 10-24 launcher?), and has a package with our TazUO build passed a clean-PC install? Settle it with whoever was asked, then record the answer (or re-confirm as it stands). `python tools/judge.py gate "The player package installs on a clean PC" --done no --detail "..."` or `python tools/judge.py confirm gate "The player package installs on a clean PC"`
- **gate What is built is seen in a client, not only compiled**: Waits on a confirmation: Chase: deploy main (2026.10.25.7) to the test shard, and mark the bot's 10-25 evidence on the play-test page? Settle it with whoever was asked, then record the answer (or re-confirm as it stands). `python tools/judge.py gate "What is built is seen in a client, not only compiled" --done yes --detail "..."` or `python tools/judge.py confirm gate "What is built is seen in a client, not only compiled"`
- **gate Somewhere to go**: Waits on a confirmation: Chase: which of [GenWrongRevamp, [SetupNewCovetous, [GenExodusEncounter, [GenBlackthorn and [GenEodon have been run on the test world? Settle it with whoever was asked, then record the answer (or re-confirm as it stands). `python tools/judge.py gate "Somewhere to go" --done yes --detail "..."` or `python tools/judge.py confirm gate "Somewhere to go"`
- **play tests not sorted**: 941 open play-test item(s) have no Who: M-001, P163-0, P164-0, P165-1, P165-2, P165-3, P165-4, P165-5, P165-6, P174-0, P152-0, P182-0, P183-0, P184-1, P184-2, P184-3, P184-4, P184-5, P184-6, P184-7 .... Sort each into testing/bot-triage.md with its steps in testing/playtest-steps.json (that file's 'Where a new prompt's items are sorted'), then run the check. `python -m unittest tools/tests/test_play_who.py`

## Port list: 6 of 16 systems in. 833 of 983 files (85%).

**Next to land: Bulk orders, all crafts.** A faithful port comes first, our feature customizations after it; work already started or already requested is still finished (Chase, 2026-10-13).

```
Port list ███████████████████░░░  833/983   84.7%
Setup     ██████████████████████  7/7     blocking defects resolved
```

| System | Done / files | | Feeds |
|---|---|---|---|
| Bulk orders, all crafts | 22 / 28 | `█████████░░░` | F-18, F-20, F-25, F-37 |
| Treasure maps revamp (in) | 2 / 2 | `████████████` | F-20; gate: train without a wall |
| Monster stealing (in) | 14 / 14 | `████████████` | gate: train without a wall |
| Despise and Shame (revamped) (in) | 15 / 15 | `████████████` | gate: somewhere to go |
| Blackthorn Dungeon (revamped) | 138 / 147 | `███████████░` | gate: somewhere to go; F-24, F-32 |
| Covetous Void Spawn | 25 / 29 | `██████████░░` | gate: somewhere to go; F-24, F-32 |
| Wrong (revamped) (in) | 26 / 26 | `████████████` | gate: somewhere to go; F-24, F-32 |
| The Exodus Encounter (in) | 38 / 38 | `████████████` | gate: somewhere to go; F-40 boss boxes |
| Underworld (Stygian Abyss) + mini champions (in) | 27 / 27 | `████████████` | gate: somewhere to go; F-24 culling |
| Creatures: Mobiles/Normal remainder, bosses, Void creatures, AI | 138 / 193 | `█████████░░░` | gate: things to fight; F-24, F-40, F-42 |
| Pet Training (OSI animal training) | 10 / 11 | `███████████░` | F-35 evo pets, companions, Animal Lore to 200 |
| Eodon (Time of Legends) remainder, no Myrmidex or Shadowguard | 16 / 19 | `██████████░░` | gate: somewhere to go, things to fight |
| High Seas, fishing half | 53 / 59 | `███████████░` | F-20 Fishing; Maritime Brotherhood |
| Crafting gaps: basket weaving, armor refinement, craft helpers, raised gardens | 23 / 33 | `████████░░░░` | F-43 recipe gating; Herbalism |
| Food, drink and potions | 36 / 44 | `██████████░░` | F-43; Alembic, Cooking designs |
| Base items: resources, equipment, containers, tools, functional | 250 / 298 | `██████████░░` | everything above |

Not counted: ride 361 files (19 in); reward 717 files (297 in); source 178 files (7 in); later 307 files (33 in); drop 304 files (10 in). Every candidate belongs to a system. _Counted by filename stem (not behavior) against `server/customizations`; the list itself is `tools/port-list.json`, kept by hand._

### Playable? **Not yet: 2 of 11 gates met.** The next one to fall is *A new character can train without hitting a wall*.

'Playable' is a judgement, so it is written down as gates rather than felt. Each one is a thing a player would actually hit, and cites what it rests on. Update one with python tools/judge.py gate.

| | Gate | Where it stands |
|---|---|---|
| **yes** | The shard runs and holds a world | Main at 57924e6 (version 2026.10.25.7) builds green: every Golem branch is built and tested before Shadow Iron merges it (the merge Golem now retries a red build once, 2026.10.24). The test shard on 2594 is up and healthy, running sl-modernuo:latest built 2026-10-23 from 0f1871f (2026.10.23.2; docker image label sl.commit, sl.dirty 0), up since 2026-10-23 09:44 CDT; the overnight bot boots the newest main on a copy of the test world each night (2026-10-25 run: commit 6b74371, 45 of 61 checks pass, both shards untouched). There is no live shard: retired 2026-10-14 until the fresh 1.0 world. _Sources: docker image inspect sl-modernuo:latest (sl.commit 0f1871f, created 2026-10-23T13:43Z), 2026-10-25; http://192.168.1.58:8092/shards.json (test up, 2026-10-26T00:11Z); testing/bot-runs/2026-10-25-0130/report.md; ShatteredLegacy CHANGELOG.md 2026.10.14.14, 2026.10.24._ _Confirmed 2026-10-25._ |
| **yes** | The player package installs on a clean PC | Still rests on T-049, T-020 and T-021 (passed 2026-10-05). Since then the package has gained our TazUO build (2026.10.15.9), the scripts updater (2026.10.18.4), the launcher's art preparation with a progress bar and a one-minute fallback, launch logs, and Play pointed at the test shard (2026.10.24.2), about 29 MB of mount animations (2026.10.23.9), the fog-of-war and appearance options (2026.10.21.11, 2026.10.23.8), and launcher fixes waiting for the next package (2026.10.25.6). None of these builds has a recorded clean-PC pass, and which zip is published cannot be seen from the repos. _Sources: testing/play-tests.json T-049, T-020, T-021; ShatteredLegacy CHANGELOG.md 2026.10.15.9, 2026.10.18.4, 2026.10.21.11, 2026.10.23.8, 2026.10.23.9, 2026.10.24.2, 2026.10.25.6._ _Confirmed 2026-10-25._ |
| no | A new character can train without hitting a wall | Built, not seen in a client. The base rate is 2 chance attempts and a 1x gain (ClusterFSkillGain.cs:40-41, P191 with P202 and P204). Hook G gives 17 skills a path past their stock ceiling, and since 10-20 Arms Lore trains to 200 on gear (P226, 2026.10.20.19), Appraisal trains past 100 on creatures (2026.10.21.9), Remove Trap has trap kits and deployable traps (2026.10.20.16, 2026.10.21.17), and Old Haven speeds the New Haven trainer quests (2026.10.20.8). The test shard trains at the real rates now, with a per-tester Test Crystal (2026.10.20.15). Still open: the casting schools above about 120 are excluded on purpose (ClusterFSkillGain.cs:24), and no play test of the rate has a result marked after 2026-10-18. _Sources: ShatteredLegacy server/customizations/ClusterFSkillGain.cs:24, :40-41; notes/cc-P191-cont-earned-skill-gain.md section 6; notes/cc-P226-arms-lore-matters.md; ShatteredLegacy CHANGELOG.md 2026.10.20.8, 2026.10.20.15, 2026.10.20.16, 2026.10.20.19, 2026.10.21.9, 2026.10.21.17; testing/play-tests.json (latest resultAt 2026-10-18T19:35Z, counted 2026-10-25)._ _Confirmed 2026-10-25._ |
| no | A new character's first hour | Built on the test world, not yet seen in a client. Since 10-20 every lesson is playable (the training yard's combat and magic, the trades yard's nine crafts, gathering, bard and thief skills, the farm and its pet, four walking tours; 2026.10.23.5, 2026.10.23.6), the farm is placed (2026.10.21.18), the words were rewritten plainly (2026.10.25.3), graduation records the first loop and opens the island (2026.10.21.21; ClusterFTutorial.cs:107, :230, :330), and the Rootdeep Burrows the tutorial fights in are in the map (2026.10.20.16). The tutorial still runs only on a Test Center shard (ClusterFTutorial.cs:54-55; "live tutorial entry stays disabled", 2026.10.23.2), fix-ups were still landing on 10-25 (2026.10.25.5, 2026.10.25.7), and the test shard's image (2026.10.23.2) predates the playable lessons. _Sources: ShatteredLegacy server/customizations/Tutorial/ClusterFTutorial.cs:54-55, :107, :230, :330; ShatteredLegacy CHANGELOG.md 2026.10.20.16, 2026.10.21.18, 2026.10.21.21, 2026.10.23.2, 2026.10.23.5, 2026.10.23.6, 2026.10.25.3, 2026.10.25.5, 2026.10.25.7; notes/cc-P371-graduation-is-the-first-loop.md._ _Confirmed 2026-10-25._ |
| no | Levels and loops work end to end | Half a step: graduation now records loop 1, with its fanfare and Loop box (P371; ClusterFLoops.cs:34 Graduate, called from ClusterFTutorial.cs:107, :230, :330). F-12 itself is still not built: no level, skill reset or cap is applied by a loop (ResetLevelAndSkillsForF12 is empty, ClusterFLoops.cs:36-42), the loot boxes' LevelOf is a placeholder (LootBoxes/ClusterFLootBoxes.cs:18-19), and the extra ring slots and several achievements wait for loops (2026.10.21.10, 2026.10.21.14). Parked until after the port (decisions-2026-10-14, Tutorial 7). _Sources: ShatteredLegacy server/customizations/Tutorial/ClusterFLoops.cs:1-9, :34, :36-42; ShatteredLegacy server/customizations/LootBoxes/ClusterFLootBoxes.cs:12, :18-19; notes/cc-P371-graduation-is-the-first-loop.md; notes/decisions-2026-10-14.md (Tutorial 7)._ _Confirmed 2026-10-25._ |
| no | What is built is seen in a client, not only compiled | testing/play-tests.json holds 1,246 items: 1,190 open, 43 passed, 4 failed, 8 later, 1 blocked (counted 2026-10-25); no result has been marked since 2026-10-18. The overnight bot runs each night on the newest main (2026-10-25: 61 checks, 45 pass, 11 fail, 1 flaky, 4 could not run), but the bot only gathers evidence and Chase marks the results. The test shard runs 2026.10.23.2 (built from 0f1871f), 33 merges behind main, so the playable tutorial lessons, Blackthorn's and Eodon's placement commands, the fishing second half and the 10-24 and 10-25 fixes are not on it. _Sources: testing/play-tests.json (counted 2026-10-25); testing/SUMMARY.md; testing/bot-runs/2026-10-25-0130/report.md; docker image inspect sl-modernuo:latest, 2026-10-25._ _Confirmed 2026-10-25._ |
| no | Somewhere to go | Built, not placed or seen. Since 10-20 the port list counts Wrong, Exodus and the Underworld in, and Blackthorn (145 of 147 by hand; the invasion waits on a decision), Covetous (25 of 29) and the Eodon remainder (16 of 19, with its moongate and 46 spawners) most of the way: 6 of 16 systems in. The Rootdeep Burrows are in the map with a wide way down from Old Haven (2026.10.20.16, 2026.10.24.4). But nothing is placed at boot: Wrong, Covetous, Exodus, Blackthorn and Eodon each wait for their [Gen command on a world (2026.10.20.15, 2026.10.20.23, 2026.10.21.11, 2026.10.21.24), and none has a client pass. Despise is client-verified (10-03); Shame is still unseen (T-007 open). _Sources: notes/port-list-2026-10-13.md (recounted 2026-10-25); README.md port list; notes/cc-P194-port-wrong-and-covetous-void.md; notes/cc-P195-port-exodus-encounter.md; notes/cc-P196-port-blackthorn-dungeon.md; notes/cc-P197-port-underworld-mini-champions.md; notes/cc-P198-port-eodon-remainder.md; notes/cc-P188-cont-rootdeep-goes-in.md; ShatteredLegacy CHANGELOG.md 2026.10.20.15, 2026.10.20.16, 2026.10.20.23, 2026.10.21.11, 2026.10.21.24, 2026.10.24.4._ _Confirmed 2026-10-25._ |
| no | Things to fight | Much more on spawners than on 10-20, nearly all by staff command: the 14 League bestiary creatures ([ClusterFSeedBestiary, 2026.10.21.23), Eodon's 46 spawners and 345 creatures (P198), Blackthorn's 44, Wrong's 38, the Void Pool's waves, the Exodus spawners, the Underworld through pinned's own Underworld.json, and the Halloween Sorcerer's Dungeon event, which runs by itself from 10-24 to 11-02 (2026.10.22). Creatures row 138 of 193. The 29 of part 1 (P119) are still on no spawner, nor are the greater phoenix, the infernus and the dragon turtle hatchling (2026.10.21.24). Spawn orphans recounted 2026-10-25: 17 (tools/spawn_orphans.py --dry-run, same list as the file's 2026-10-16 count; 11 of them are Underworld NPCs). _Sources: ShatteredLegacy CHANGELOG.md 2026.10.15.5, 2026.10.21.23, 2026.10.21.24, 2026.10.22; notes/cc-P198-port-eodon-remainder.md; notes/cc-P196-port-blackthorn-dungeon.md; tools/spawn-orphans.txt (17, recounted 2026-10-25 by cc-P273)._ _Confirmed 2026-10-25._ |
| no | Set mechanics actually fire | Unchanged: EpiphanyHelper and BeastialSetHelper are still called only from their own set files (grep of server/customizations at 57924e6, 2026-10-25; the one other hit, Mobiles/Normal/DespiseCreature.cs:4, is a comment). Bestial rage, the Epiphany burst, the sculpture's luck and set self-repair are ported but inert until the set-mechanic hooks row is built. _Sources: ShatteredLegacy server/customizations/Items/Artifacts/Equipment/Armor/Sets/Epiphany/VillainousEpiphany.cs:8-9; docs/gap-register.md section A; docs/patch-backlog.md P3; a grep of server/customizations, 2026-10-25._ _Confirmed 2026-10-25._ |
| no | No live gap a player would call a bug | docs/bug-list.md section 1 has 67 rows (counted 2026-10-25; 65 on 10-20), highest D97; the file was last changed 2026-10-21. Read the way the website feed reads it (FIXED or CLOSED in the row, or filed under section 2 or 4), 18 of 70 tracked rows are closed and 52 open, and 15 rows in open sections read as fixed (D24, D27, D37, D44, D46, D50, D51, D52, D53, D54, D58, D87, D88, D89, D93). D50, D89, D93 and D94, owed since 10-14, are all still in section 1. The list needs its pass before this gate can be read from it. _Sources: docs/bug-list.md (counted 2026-10-25); ShatteredLegacy scripts/Build-MigrationStatus.ps1 (run to the session scratchpad, 2026-10-25); notes/passdown-overseer-2026-10-14.md (Record-keeping owed)._ _Confirmed 2026-10-25._ |
| no | The fresh-world wipe is ready | Still no single plan. Unchanged since 10-20 in substance: live is deleted, so D50's live stop timeout is moot; every account is wiped at the tutorial update (decisions-2026-10-14, Tutorial 1), and the tutorial now handles a deleted or moved tutorial character (2026.10.25.7). Still scattered: D34, T-006 and T-010, F-4 (one character per account), and P73's test-account wipe (CHANGELOG 2026.10.12), which refuses live. New to gather: the world commands a fresh world must run, since nothing is placed at boot (the [Gen commands of Wrong, Covetous, Exodus, Blackthorn and Eodon, [ClusterFSeedBestiary, [ClusterFSeedRootdeep, [ClusterFSeedTutorialFarm, [ClusterFGuildHalls, [GenFishMongers, [ClusterFCommunityArt). _Sources: notes/passdown-overseer-2026-10-14.md; notes/decisions-2026-10-14.md (Tutorial 1); docs/bug-list.md D34; docs/client-test-queue.md T-006, T-010; docs/feature-queue.md F-4; ShatteredLegacy CHANGELOG.md 2026.10.12, 2026.10.20.15, 2026.10.20.23, 2026.10.21.11, 2026.10.21.18, 2026.10.21.23, 2026.10.21.24, 2026.10.23, 2026.10.25, 2026.10.25.7._ _Confirmed 2026-10-25._ |

| Setup defect | Resolved |
|---|---|
| CraftContext members (RepeatCount, RepeatItem, RepeatTypeRes) recovered | yes |
| ResourceInfo extended wood enum members (8) recovered | yes |
| OutridersGuildmaster recovered | yes |
| server/customizations compiles standalone | yes |
| apply-patches.sh fails on failed patch | yes |
| stale server/customizations/migrations removed | yes |
| RegenRates routing made explicit | yes |

**Patches:** 16 total, **0 currently failing to apply**, 8 triaged, 3 found obsolete. `apply-patches.sh` fails the build on a failed patch, so a green build means every patch applied.

### Every ServUO file ModernUO lacks, by area (not a target): 937 of 2,045 (45.8%)

```
TOTAL                          ████████░░░░░░░░░░  937/2045   45.8%

Items/Artifacts                ████████████████░░  283/325    87.1%
Services/Revamped Dungeons     █████████████████░  143/150    95.3%
Items/Equipment                ███████████████░░░  127/148    85.8%
Mobiles/Normal                 ██████████████░░░░  110/138    79.7%
Services/Expansions            ████████░░░░░░░░░░   74/175    42.3%
Items/Resource                 ████████████████░░   55/61     90.2%
Items/Functional               ██████████████░░░░   37/49     75.5%
Items/Consumables              ███████████░░░░░░░   36/59     61.0%
Services/BulkOrders            ██████████████░░░░   22/28     78.6%
Items/Containers               ████████████░░░░░░   20/31     64.5%
Items/Quest                    ██░░░░░░░░░░░░░░░░    9/78     11.5%
Items/Addons                   █░░░░░░░░░░░░░░░░░    6/169     3.6%
Services/CleanUpBritannia      █░░░░░░░░░░░░░░░░░    4/52      7.7%
Mobiles/NPCs                   █░░░░░░░░░░░░░░░░░    3/222     1.4%
Items/Decorative               █░░░░░░░░░░░░░░░░░    3/88      3.4%
Quests                         █░░░░░░░░░░░░░░░░░    3/84      3.6%
Services/New Magincia          █░░░░░░░░░░░░░░░░░    2/40      5.0%
Services/XmlSpawner            ░░░░░░░░░░░░░░░░░░    0/97      0.0%
Items/StoreBought              ░░░░░░░░░░░░░░░░░░    0/51      0.0%
```

_Counted by matching ServUO file stems (excluding those stock ModernUO already has) against `server/customizations`. Auto-counted, never hand-edited._

**Ported systems logged: 48**

| Content | Task | Notes |
|---|---|---|
| CC9 batch 5: Swiftflight, the in-row remainder, the whole plain bucket (136 files, 240 types) | CC9 | Closes the 320 and 81 buckets. Swiftflight is Bow, ISetItem with BaseSetWeapon's fields inlined and no carrier (Q-041), proven by the first content-level set test (real Feathernock + Swiftflight complete the Marksman set through the interface alone; round-trip of the set fields on a Bow subclass). 116 files generated from ServUO values by a refusing generator, 19 hand-written; every override and constructor value re-diffed (1,085 + 821, 0 findings, diff proved red). One base needs a carrier (LeatherTalons -> BaseSetClothing, for UnicornManeWovenTalons' absorption). Three more mechanics ported whole and inert pending engine hooks, the D-14 shape: Epiphany burst (12 Villainous pieces), TenthAnniversarySculpture luck, FirstAidBelt healing bonus (Q-043). Three files found already in ModernUO under other names and not ported (gargish cloth arms, HMS Cape model, mystic book). Three build cycles (two single-error failures: a Container.CheckStack that ModernUO gates through CheckHold, a third SoulCharge, a missing using), then green in 4.5 min, 44 tests. 237/237 reflected; headless fresh save and reload clean. The brief's 120/29 were 107/30 when counted from the trees. Nothing seen in a client; spot check now 381 files. |
| PlagueRat | P1 | P1 reference port. 88 lines to 55. Builds, spawns, survives save/reload. No speed override: SpeedClass Medium, per the Q-008 answer (ModernUO's npc-speeds.json fallback is the standing rule for all ported creatures). |
| GreaterPoisonElemental | P2 | P2 timed port, headless. 123 lines to 80. Compiles clean, server starts, world saves and reloads; type registration proven by reflection over the shipped assembly. Adds PackItem, multi-AddLoot, an OnDeath override, AI_Mage and the two-argument stat overloads over what PlagueRat covered. No speed override, per Q-008. An instance in a saved world is NOT verified: headless has no spawn - batched for a later client spot check. |
| LuckyCoin | P2, completed by S2 | Forced dependency of GreaterPoisonElemental; ModernUO has no LuckyCoin. P2 ported it without OnDoubleClick because that targets a FountainOfFortune (Q-010). S2 built the Fountain and RESTORED OnDoubleClick and its InternalTarget, so Q-010 is CLOSED and docs/fidelity-principle.md should drop its entry. Pinned by ShatteredLegacy.Tests.FountainOfFortuneVerification.DoubleClickingACoinInTheBackpackAsksForATarget. Reused by 12 Mobiles/Normal creatures, of which 1 (GreaterPoisonElemental) is in the tree today. |
| RaptorTeeth | CC3 | ICommodity stackable resource. ServUO's TextDefinition Description becomes ModernUO's int DescriptionNumber; the Constructable X()/X(int) pair collapses to one [Constructible] X(int amount = 1). |
| AncientPotteryFragments | CC3 | Forced dependency of Raptor; ModernUO has none. Trivial Item, ported complete, no deviation. One extracted type per file, per the LuckyCoin precedent (Q-010). |
| PerfectBanana | CC3 | Forced dependency of SilverbackGorilla; ModernUO has none. Trivial stackable Item, ported complete, no deviation. |
| RaptorClaw | CC3 | Boomerang artifact. Boomerang, Slayer, Attributes and WeaponAttributes.HitLeechStam all exist in ModernUO. Only IsArtifact dropped: it is a ServUO-only Server.Item virtual whose every consumer (pigments, NaturalDye, AlterItem, RunicReforging) is also ServUO-only, so it has zero readers in ModernUO. |
| StretchedDinosaurHide | CC3 | One of six TOL tribal reward decorations split out of a single ServUO file, one type per file. Derives from Item, not ModernUO's BaseDecorationArtifact, because ServUO sets ShowArtifactRarity=false and ModernUO's base adds the rarity line unconditionally; the three members that base contributes are reproduced so the rendered properties match ServUO exactly. |
| CarvedMyrmydexGlyph | CC3 | One of six TOL tribal reward decorations split out of a single ServUO file, one type per file. Derives from Item, not ModernUO's BaseDecorationArtifact, because ServUO sets ShowArtifactRarity=false and ModernUO's base adds the rarity line unconditionally; the three members that base contributes are reproduced so the rendered properties match ServUO exactly. |
| WakuOnASpit | CC3 | One of six TOL tribal reward decorations split out of a single ServUO file, one type per file. Derives from Item, not ModernUO's BaseDecorationArtifact, because ServUO sets ShowArtifactRarity=false and ModernUO's base adds the rarity line unconditionally; the three members that base contributes are reproduced so the rendered properties match ServUO exactly. |
| SacredLavaRock | CC3 | One of six TOL tribal reward decorations split out of a single ServUO file, one type per file. Derives from Item, not ModernUO's BaseDecorationArtifact, because ServUO sets ShowArtifactRarity=false and ModernUO's base adds the rarity line unconditionally; the three members that base contributes are reproduced so the rendered properties match ServUO exactly. |
| WhiteTigerFigurine | CC3 | One of six TOL tribal reward decorations split out of a single ServUO file, one type per file. Derives from Item, not ModernUO's BaseDecorationArtifact, because ServUO sets ShowArtifactRarity=false and ModernUO's base adds the rarity line unconditionally; the three members that base contributes are reproduced so the rendered properties match ServUO exactly. |
| DragonTurtleHatchlingNet | CC3 | One of six TOL tribal reward decorations split out of a single ServUO file, one type per file. Derives from Item, not ModernUO's BaseDecorationArtifact, because ServUO sets ShowArtifactRarity=false and ModernUO's base adds the rarity line unconditionally; the three members that base contributes are reproduced so the rendered properties match ServUO exactly. |
| Allosaurus | CC3 | Three SetWeaponAbility calls become one GetWeaponAbility() over Utility.Random(3). GenerateLoot's IsChampionSpawn branch collapses to the non-champion arm and SetToChampionSpawn is dropped: ModernUO's BaseCreature has neither, and its ChampionSpawn never calls back into the creature. AttacksFocus dropped. |
| Archaeosaurus | CC3 | Two SetWeaponAbility calls become GetWeaponAbility() over Utility.RandomBool(). DragonBlood => 6 dropped: ModernUO has neither the carving property nor the item. AttacksFocus dropped. |
| Dimetrosaur | CC3 | SetWeaponAbility x2 become GetWeaponAbility(). Two behaviours dropped with no ModernUO equivalent: SetAreaEffect(AreaEffect.PoisonBreath), and OnAfterTame, which quartered Hits on first tame - StatLossAfterTame gives AnimalTaming's ScaleStats(0.50) instead. FruitsAndVegies -> FruitsAndVeggies. AttacksFocus and the champion-spawn hooks dropped. |
| Najasaurus | CC3 | Clean. Its only PetTrainingHelper call is in the version-0 deserialize upgrade path, which new content at version 0 never runs, and the constructor already sets Poisoning skill and HitPoison - so dropping it is a no-op. AttacksFocus dropped. |
| Saurosaurus | CC3 | SetWeaponAbility(ConcussionBlow) becomes GetWeaponAbility(). SetSpecialAbility(TailSwipe) and SetSpecialAbility(LifeLeech) dropped - PetTrainingHelper, which ModernUO lacks; ServUO's own source carries the comment "Missing: Life Leech, Tail Swipe ability". DragonBlood => 8 dropped. AttacksFocus dropped. |
| SilverbackGorilla | CC3 | The only candidate creature calling no PetTrainingHelper method. Banana-throw OnActionCombat ported intact: the 13-argument MovingParticles overload with EffectLayer, AOS.Damage and Region.IsPartOf(string) all exist unchanged. DateTime.UtcNow -> Core.Now. |
| Raptor | CC3 | The only ported creature with real persisted state: m_IsFriend becomes [SerializableField(0, setter: "private")] and ServUO's delete-on-deserialize becomes [AfterDeserialization(false)]. The Raptor()/Raptor(bool) Constructable pair collapses to one [Constructible] Raptor(bool isFriend = false). Pack-friend spawn timer, PackInstinct.Ostard, Map.CanFit and AIObject.Action all port unchanged. SetWeaponAbility(BleedAttack) becomes GetWeaponAbility(). Drops AncientPotteryFragments and RaptorClaw, both ported alongside. |
| Eodon core content (17 files) | CC3 | Six dinosaurs, Raptor, RaptorClaw, RaptorTeeth, six TOL decorations, PerfectBanana, AncientPotteryFragments. Four build batches, zero failures. All 17 types verified registered by reflection over the shipped assembly. Deviations logged in docs/fidelity-principle.md. |
| SetItem (SetItem enum, ISetItem, SetHelper) | S1 | The Mondain's Legacy armour set-bonus subsystem. Ported to ModernUO's IPropertyList, StatMod and AosSkillBonuses APIs. Omits SetHelper.GetSetSlayer (ModernUO's SlayerName has no Dinosaur/Myrmidex; consumers are BaseWeapon combat code, out of scope) and the IFishingAttire branch (no such interface in ModernUO; Fisherman set not ported). Deviations D-2 and D-4 in notes/s1-armour-sets.md. |
| BaseSetArmor | S1 | The key design decision of S1. ServUO puts set state on BaseArmor itself; doing that in ModernUO would mean bumping BaseArmor's [SerializationGenerator(9)] to 10 and owning a migration for an upstream file. Instead this additive abstract class at version 0 carries the state and set content derives from it. Behaviourally identical for set content, because no stock ModernUO armour is a set item (verified at runtime). |
| PlayerMobile set resistances | S1 | Additive partial class, no patch needed: PlayerMobile is already partial and is not source-generated. Overrides the GetItemResistance virtual that Mobile-set-item-resistance-hook.patch introduces. |
| TigerPelt armour (8 files) | S1 | CC3 called these 'itself set-bonus content'. That was wrong: grep SetID over all eight returns nothing. They are plain BaseArmor leaf armour and were never blocked. Ported unchanged, re-parented to BaseSetArmor so the Aloron pieces that derive from them can carry set state. Weight moves from a ctor assignment to a DefaultWeight override, the ModernUO idiom. |
| Aloron's Armor set (8 files) | S1 | The CC3 decline, reversed. Four-piece set (SetItem.Aloron), SetAttributes BonusMana 15 / LowerManaCost 20, SetSelfRepair 3, per-piece resist bonuses 8/8/9/8/8. Verified at runtime: four pieces worn gives 60/60/60/60/60 resists and BonusMana 15 through AosAttributes.GetValue. Two deviations: AbsorptionAttributes.EaterCold=2 omitted (SAAbsorptionAttributes is a separate missing subsystem that drags in three more), and the Dinosaur Slayer omitted along with its tooltip line, rather than advertise a bonus that does nothing. D-1 and D-2 in notes/s1-armour-sets.md. |
| Armour set-bonus subsystem + Aloron set + TigerPelt | S1 | First subsystem built rather than ported. Unblocks 114 further ServUO files. Three patches, one of them the first into the ModernUO core project (Mobile.ComputeResistances), allowed because no UOContent hook exists and the alternative was copied upstream logic. Four deviations logged, all omissions. |
| FountainOfFortune | S2 | BaseAddon with a reward loop, three static tables, a defrag timer and a resurrect hook. Subsystem-shaped, so it ships with a test per docs/subsystem-policy.md - the first content task to use S4's route. Needs server/patches/PlayerMobile-fountain-luck-bonus.patch: ServUO routes the luck reward through PlayerMobile.RealLuck, which ModernUO does not have, and its three luck consumers all read Mobile.Luck. ModernUO's ResurrectGump takes no callback, so FountainResurrectGump subclasses it rather than patching upstream. Two reward cases are unreachable in ServUO too (Random(4) over a six-case switch) and were ported unchanged. NOTHING PLACES ONE: ServUO builds it in Services/Underworld/Generate.cs, which is not ported. Q-021. |
| GemologistsSatchel | S2 | The reward branch that blew S2 past its estimate. Reads Imbuing.IngredTypes, a 42-entry Type[] at Services/LootGeneration/Imbuing/Core/Imbuing.cs:1735, of which 35 were missing from ModernUO. Not a subsystem pull-in - all 35 are leaf items - so all 35 were ported (Q-020, Chase chose option A). The 42-entry array now lives in this file as a private static, verbatim and complete; verified at runtime as length 42 with no nulls. |
| SolesOfProvidence | S2 | Sandals with Attributes.Luck = 80. Loses ServUO's IsArtifact override: ModernUO has no such member and every ServUO consumer of it (RunicReforging, BasePigmentsOfTokuno, NaturalDye, AlterItem, ArcaneGem) is also absent, so it is inert. Deviation D-1. |
| Imbuing ingredient set (35 leaf items) | S2 | EnchantedEssence and RelicFragment are core cluster members; the other 33 are forced dependencies of GemologistsSatchel. All are Item or Item,ICommodity stackables with an ItemID and a cliloc and nothing else - grep for 'new X(' across all 31 Resource files returns zero matches. Files are named after the class, so ServUO's SeedRenewal.cs, LavaSerpenCrust.cs and ElvenFletchings.cs become SeedOfRenewal.cs, LavaSerpentCrust.cs and ElvenFletching.cs; the TypeAlias attributes are carried across unchanged. These are Stygian Abyss drops that CC5 and CC6 want regardless, so the overrun buys reusable content. |
| Fountain of Fortune cluster (38 files) | S2 | Reverses the second decline. Restores LuckyCoin's OnDoubleClick for all 12 coin droppers. One patch: PlayerMobile.Luck, because ServUO routes the reward through RealLuck which ModernUO lacks. Ships with a regression test. Nothing places a fountain yet - Q-021 gives the OSI coordinates. |
| JourneyToTheAthenaeumIsle + QueenZhah | S5 | First ServUO quest on ModernUO's MLQuest engine. SlayObjective -> KillObjective, 10x ObtainObjective -> 10x CollectObjective with ShowDetailed=false carrying clilocs 1150933-1150942, BaseReward -> ItemReward. Registered from a Configure() hook via MLQuestSystem.Register, because apply-patches.sh mirrors .cs only and Data/MLQuests.cfg is CRLF data. Deviation D-S5-3: QueenZhah is undressed, her seven gargoyle items (~470 ServUO lines) are all absent from ModernUO. Pinned by 5 tests in ShatteredLegacy.Tests.AthenaeumIsleQuestVerification. |
| MinionOfScelestus | S5 | Kill-objective target for the S5 quest. Stats, resistances, skills, loot, HitPoison, treasure level, mount knockoff and home-return are verbatim. Two deviations: D-S5-1 loses SetSpecialAbility(DragonBreath) (Pet Training, CC6 decline, Saurosaurus precedent); D-S5-2 loses TaintedLifeAura, which would need additive patches into BaseWeapon and AOS. ServUO's Poison.Parasitic maps to ModernUO's Poison.LethalParasitic (Misc/PoisonKinds.cs). Not spawned - batched for the client spot check. |
| GargishDocuments (12 types) + BaseLocalizedBook + Note | S5 | The ten Collect-objective targets, the reward book, and the two base classes underneath them. Forced dependencies found by the array walk, ported to the leaf per LuckyCoin: ModernUO's Items/Books has BaseBook/BookContent/BookPageInfo, all authored-text, none cliloc-paged, so this is additive and not a duplicate. Both reader gumps were rewritten from ServUO's Gump API onto DynamicGumpBuilder - a real rewrite, and UNVERIFIED without a client. D-S5-4: ChronicleOfTheGargoyleQueen1.Initialize() became a static initializer; the values are constants so behaviour is identical. |
| SAAbsorptionAttributes + DamageEaterContext | S6 | Subsystem, not content. Additive against BaseAttributes, which ModernUO already ships. The property reaches items through an additive IAbsorptionItem interface rather than fields on BaseArmor/BaseWeapon/BaseJewel/BaseClothing, so no upstream serialization version is bumped - S1's decision, reused. BaseSetArmor is the only carrier today, at serialization field 11. The effect reaches combat through AOS-damage-eater-hook.patch, 16 added lines in Projects/UOContent/Misc/AOS.cs at ServUO's own call site. Pinned by six tests in ShatteredLegacy.Tests.AbsorptionAttributesVerification, of which ColdDamageThroughAosDamageReachesTheEater was proved to fail with the patch skipped. |
| Gargoyle wearables, row share (9 files, 11 types) | CC9 | GargishGlasses, GargishPlateChest, GargishPlateLegs, GargishEarrings, GargishNecklace (+GargishAmulet, GargishStoneAmulet), GargishGnarledStaff, GargishKatana, GargishDagger, LargeStoneShield. ServUO's 'Race RequiredRace => Race.Gargoyle' is ModernUO's 'int RequiredRaces => Race.AllowGargoylesOnly' on armour/weapons/shields (Item.cs:2110); CanBeWornByGargoyles has zero readers and is dropped. S9's other three gargoyle files in this row (GargishClothArmor.cs, GargishLeatherArms, GargishStoneChest) were NOT ported: ModernUO already ships them as Gargish<Material><Slot>Type1/Type2 with the same item IDs, found by an item-ID cross-check, not by name. |
| Greymist (Acolyte) armour set (4 files) | CC9 | ServUO derives these from stock Leather* and reads set state off BaseArmor; here they derive from S1's BaseSetArmor and reproduce the stock parent's members, the TigerPelt/Aloron shape. This is the transformation every one of the row's 83 set-armour files needs and S9's name scan could not see. Set bonus firing is NOT verified headlessly; batched for the client spot check. |
| BaseCostume | CC9 | Shield-slot mask that body-mods the wearer; carrier for the 34 costumes in the in-row bucket, all now plain ports. Two persisted ints (CostumeBody, CostumeHue) at version 0; ServUO's three save versions collapse. Deviation D-5: ServUO knocks the costume off from AOS.Damage (AOS.cs:417); ModernUO has no call site, so a masked player keeps the mask through combat. One line added to the existing AOS-damage-eater-hook.patch would restore it. |
| CC9 batch 2: 33 costumes + 7 unblocked artifacts (40 files, 41 types) | CC9 | The 33 costumes are one template on BaseCostume (body, one hue, creature name, cliloc or default name) and were generated from the ServUO values by a script that refuses any file whose constructor or overrides differ from the template; it refused none. CastOffZombieSkin, CuffsOfTheArchmage (2 types), PillarOfStrength, BreastplateOfTheBerserker, GiantSteps, Glasses, NightEyes hand-written; three of them derive from ModernUO's own Gargish*Type1/Type2 classes rather than a ported parent. Green first cycle (95 s), 41/41 reflected, headless save/reload clean. Reading the 19 in-row artifacts batch 1 supposedly unblocked found 6 more absorption users and 5 set pieces on gargish jewellery, so only 8 were plain - S9's in-row bucket checked one member per file. |
| CC9 batch 1: artifacts and equipment (31 files, 34 types) | CC9 | 2,604 ServUO lines in, 1,324 out. Category-spread sample chosen to test S9's 'drops straight in' claim: 20 of 34 types needed only the standard conversion, 8 would not have compiled mechanically (four set pieces re-parented, fishing-pole attributes, BattleLust, two non-virtual overrides on earrings/necklace, IRepairable), 3 must not be ported at all (already in ModernUO). Real persisted state exercised on GobletOfCelebration (SerializableProperty + DeltaDateTime + AfterDeserialization timer rebuild), AmuletOfRighteousness (IUsesRemaining) and BaseCostume. Deviations D-3 AxeOfAbandon BattleLust, D-4 XenrrFishingPole SpellChanneling/CastSpeed (ModernUO's FishingPole has no attribute block and AosAttributes.GetValue aggregates only the seven equipment bases), D-5 costume damage hook. Gated build 86 s; 33/33 types reflected; headless save and reload clean. |
| The carrier family: BaseSetWeapon, BaseSetJewel, BaseSetClothing, BaseSetQuiver, BaseSetShield (5 files) | S10 | Subsystem, not content: the set state ServUO puts on each base class, on an additive intermediate class of ours instead (the S1 decision, applied four more times). 1,426 lines, zero patches, zero migrations, 15 tests, every gate watched fail. Field layout identical to BaseSetArmor on every carrier (0-9, then SetSelfRepair 10 and absorption 11 where the ServUO base has them; jewel has absorption at 10; quiver has neither). SetSelfRepair inert on weapon/clothing/shield (Q-038). The four ported gargish armour-class bases were re-parented onto BaseSetArmor in the same commit, before any instance reached a save. Unblocks CC9 batch 4 (13 set pieces + 9 non-armour absorption users + 5 gargish-jewellery set pieces) and CC4's ReforgedSuffix route C. |
| CC9 batch 3: the plain remainder (49 files, 49 types) | CC9 | 21 weapons, 11 jewellery, 17 armour and shields; 4,636 ServUO lines in, 1,740 out. Pre-flighted with the section-3 method before any build: every override checked against a pinned ModernUO virtual, every attribute member against the Aos* enums, item IDs cross-checked, and every ServUO descendant of all 49 walked transitively for set or absorption state. Nine bases got a carrier parent at port time because a descendant needs it (GargishPlateArms, GargishPlateKilt, the five DragonTurtleHide pieces on BaseSetArmor; GargishKiteShield on BaseSetShield; GargishBattleAxe on BaseSetWeapon, the ninth, found because GargishPincer assigns SetSkillBonuses, a token the AGENTS.md grep does not list - Q-040). The other 40 are on stock bases per docs/tasks.md. RandomWand is a static helper, not an item. Every override value re-diffed mechanically against ServUO after writing: 524 compared, 0 mismatches. Deviations D-10 (GargishWarHammer flip typo 0x481 -> 0x48C1), D-11 (EvilOrcHelm's two zero-reader virtuals), D-12 (OrcishBow one durability line, not two), D-13 (StaffRing IsPlayer; not OSI content). Gated build green first cycle, 101 s, 42 tests; 49/49 reflected; headless fresh save and reload clean. |
| CC9 batch 4: the one re-parent, the 41 carrier-blocked, the set-armour bucket (125 files, 127 types; 3 edited) | CC9 | GargishDagger moved from BaseKnife to BaseSetWeapon (Q-040: StoneDragonsTooth needs AbsorptionAttributes), after re-verifying no instance in any save by reading the type tables of the live save (2026-07-06, 1,468 types, no Gargish* at all), the three Backups snapshots and the newest daily and hourly Archives (decompressed), not by date alone. The 41 carrier-blocked: 40 ported, Swiftflight declined (Bow sits on BaseRanged, no carrier can sit above it; Q-041). Two talismans ported on stock BaseTalisman with the eater dropped, which is behaviour-identical: ServUO never aggregates a talisman's absorption (RunicReforging.GetSAAbsorptionAttributes). The set-armour bucket counts 85, not 79: 79 set pieces plus the 6 Phoenix suit files that sit under Sets/ with no SetID and stay on stock parents. All 85 generated from ServUO values plus a dump of the pinned stock parent's members ([Flippable] copied because ModernUO reads it inherit:false; IArcaneEquip dropped on 6 gloves per D-7). Two corrections found by reading the parents: batch 3's GargishBattleAxe had lost BaseAxe (Slash1H, sword sounds, no harvesting) and S10's BaseSetWeapon skipped BaseMeleeWeapon's AbsorbDamage; both fixed, both save-neutral today. Bestial pieces ported with the berserk helper inert (its AOS.Damage/heal hooks do not exist here; Q-042). Deviations D-14..D-19. Value diff over 126 files: 0 findings, proved red with three injected faults. One failed build cycle (28 s, one inlined member), then green in 99 s with 42 tests; 130/130 reflected; headless fresh save and reload clean. 10,062 ServUO lines in, 6,363 out. See notes/cc9-artifacts.md section 14. |
| CC4 Despise: the Revamped Despise dungeon (12 ServUO files + XmlSpawner XML -> 14 files, 4,684 lines) | CC4 | Regions are ServUO dynamic BaseRegions re-created by the controller; ModernUO's Region maps member for member except CheckTravel (now on BaseRegion with an out message), the absent EventSink.OnEnterRegion (DespiseRegion.OnExit instead), and priority: every pinned region is Dynamic so the tie with regions.json's Despise dungeon went to list order - priority 51. XmlSpawner XML became a 47-row table plus DespiseSpawner (PowerMin/PowerMax) applied in OnAfterSpawn, because ModernUO entries take fixed parameters. Headless on the real map: 227 creatures generated in bounds (capacity 227 of 229 requested: two XML rows exceed their entries), power 1-5 upper / 4-8 lower, 15+15 army spawners found, save/reload identical. 48 tests green, auto-stable gate proved red. Deviations (note-local D-29..D-36 in notes/cc4-despise.md): PutridHeart inert, MysteriousWisp not placed, Town Cryer hooks dropped, Silenii/Phantom Discordance dropped, ForceNotoriety absent, Container orb hook absent, lower level 4-8 vs a broken 2-arg XML, FightMode.Good/Evil -> Closest (behaviour-identical on pub57). |
| CC6 batch 1: twenty creatures the stock spawn data places and could not spawn (20 files + GoblinOppositionGroup, 1 test) | CC6 | Selection rule: pinned ModernUO's Distribution/Data/Spawns names 109 types no loaded assembly declares (BaseSpawner marks them InvalidType and spawns nothing); the twenty are the low-to-mid-level Mobiles/Normal part that is clean to port (Underworld goblins, Abyss enslaved goblins, Ter Mur spiders/skree/undead guardians, Old Haven spellbinders). Headless on the real map: the probe imported the four stock files (168 spawners, 0 failures), all twenty spawned by their stock spawners (127 live), save and reload identical; 60 tests green incl. 6 new (values, every stock entry now resolves and 89 names remain, gray/green goblin enmity, trapdoor stealth walk, tangling roots entangle+acid, the rest's shape). TribeType -> a fourth OppositionGroup, additive; CanStealth -> ServUO's BaseCreature.OnMove branch inlined in TrapdoorSpider. Deviations D-44 GreenGoblinScout on AI_Melee (no OrcScout AI), D-45 Spellbinder on AI_Mage (no Spellbinder AI), Skree on AI_Mage (D-41's shape), D-46 ShameWall constructor sets Visible (Q-046). Route extended: the test fixture never wired the skill-check handlers, so every CheckSkill failed in the test host; SkillCheck.Initialize added to the S8 fixture patch, proved red first. Nothing seen in a client; Q-048 asks whether the live world's Ter Mur spawners exist so these start on deploy. |
| CC4 Shame: the Revamped Shame dungeon on both facets (19 ServUO files + XmlSpawner XML -> 20 files, 3,772 lines) | CC4 | The brief's 11 files are 19 plus the XML: 116 of the XML's 194 rows spawn TreasureLevel1-4 (Nerun's chest pack, not in ModernUO, ported levels 1-4; Q-047), and the cave troll's four High Seas powder ingredients and the vortex's VoidCore are leaf items ported at ServUO's paths. No region layer: Shame constructs none, the creatures test regions.json's static Shame DungeonRegion by name on both facets, so Despise's priority trap does not arise. XmlSpawner XML became a 194-row table on plain Spawners (no constructor arguments in this file; Q-044's shape does not occur), 97 per facet and identical. Headless on the real map: 384 of 386 requested (two rows exceed their entries) all inside their rectangles and inside the Shame region on both facets, 58 locked chests with loot per facet, 6 altars / 6 walls / 6 trolls / 22 wall teleporters, save/reload identical, 54 tests green, ClayGolem gate proved red, no patch. Deviations (note-local D-37..D-43 in notes/cc4-shame.md): crystal points inert behind a seam for S7 so the altars answer 'not yet worthy' and the guardians are GM-only until then; chest loot unreforged and no refinement roll; StickySkin/ColossalRage/SearingWounds dropped; LifeLeech is DrainLifeAttack; CrazedMage on AI_Mage; TreasureMapChance absent; a timed-out challenge now frees the altar (ServUO leaves it stuck). ServUO's wall teleporters reproduced as read - inert until the first troll dies, then active whenever the wall stands (Q-046). |

### Task list (0 of 6 done)

```
Tasks          ░░░░░░░░░░░░░░░░░░░░░░  0/6   Open work the overseer tracks
```

| | Task | Status | Notes | Confirmed |
|---|---|---|---|---|
| `DEPLOY` | Deploy main to the test shard and run its play tests | todo | The test shard runs sl-modernuo:latest built 2026-10-23 from 0f1871f (2026.10.23.2); main is 2026.10.25.7, 33 merges ahead (docker image inspect, 2026-10-25). Deploy main, run the placement commands the new content needs, then work the play-test page (1,190 open items on 2026-10-25). | 2026-10-25 |
| `TUTORIAL` | New Haven tutorial trials | **in progress** | Every lesson is playable in main (2026.10.23.5, 2026.10.23.6), with the farm (2026.10.21.18), graduation as the first loop (P371, 2026.10.21.21) and plain words (2026.10.25.3); fix-ups were still landing on 10-25. Runs on Test Center shards only (ClusterFTutorial.cs:54-55). Left: a client pass on the test shard, then live entry. | 2026-10-25 |
| `WIPE` | Fresh-world wipe plan | todo | No single plan document. Live was deleted 2026-10-14; every account is wiped at the tutorial update (decisions-2026-10-14); gather D34, T-006, T-010, F-4, P73's console wipe and the list of placement commands a fresh world must run (nothing new is placed at boot) into one. | 2026-10-25 |
| `BUGS` | Bug list pass | todo | 67 rows in section 1 (counted 2026-10-25), highest D97; 15 rows in open sections read as FIXED or CLOSED (Build-MigrationStatus.ps1's warning lists them), D50, D89, D93 and D94 among them, owed since 10-14. Close or move them. | 2026-10-25 |
| `F-12` | Levels and loops | todo | After the port (Chase 2026-10-13; decisions-2026-10-14 Tutorial 7). Research done (P54, P72), decisions in notes/f12-decisions-2026-10-05.md. Built so far: graduation records loop 1 (P371, Tutorial/ClusterFLoops.cs:34); levels, skill resets and caps are not (ResetLevelAndSkillsForF12 is empty, :36-42). | 2026-10-25 |
| `F-37` | Commissions move to the League | todo | After the port. Commissions have not moved to the League. Renown is now spent: the League Shop (2026.10.21.3), its Hall page (2026.10.21.14) and the League Register's goods (2026.10.21.20), and the Register opens and turns in bound guilds' contracts from Bronze and Verite rank. | 2026-10-25 |

_Status lives in `tools/progress-state.json`; `python tools/judge.py` updates one row and its date._

### Queue (Golem on; 578 prompts done, 5 more stopped early and not counted)

| Prompt | State | When |
|---|---|---|
| P676 sos-s3-trammel-s-regions-and-guard-zones-redraw | queued |  |
| P677 sos-s8-our-code-and-ea-s-later-dungeons-on-the | queued |  |
| P679 sos-s4-moongates-teleporters-and-the-staff-go-m | queued |  |
| P680 sos-s5-stock-decoration-on-the-new-land | queued |  |
| P682 sos-s10-people-for-the-author-s-new-towns-and-ke | queued |  |
| P683 sos-s6-the-author-s-775-decoration-lines-for-hi | queued |  |
| P684 sos-s11-treasure-maps-houses-boats-docks-and-sos | queued |  |
| P685 sos-s12-felucca-s-champion-spawns | queued |  |
| P686 sos-s13-felucca-s-regions | queued |  |
| P687 sos-s14-fences-for-the-unfinished-areas-and-the | queued |  |
| P688 sos-s15-the-walk-between-places-and-the-bot-s-ro | queued |  |
| P689 sos-s16-credits-the-fidelity-register-and-the-wi | queued |  |
| P690 sos-s17-the-whole-swapped-world-played-through-t | queued |  |
| P691 blackthorn-to-fold | queued |  |
| P708 guild-hqs-on-sos | queued |  |
| P714 gated-chivalry-necromancy-and-start-skills | queued |  |
| P715 ask-expires-too-soon | queued |  |
| P716 cont-sos-s2-tazuo-shots | queued |  |
| P719 client-always-run-off | queued |  |
| P720 isle-walkthrough-fixes-2 | queued |  |
| P722 isle-only-release-branch | queued |  |
| P718 isle-walkthrough-fixes-1 | done | 2026-10-28 |
| P717 isle-first | done | 2026-10-28 |
| P713 sos-map-switch | done | 2026-10-27 |
| P710 cont-fixup-private-isle-copies | done | 2026-10-27 |
| P709 gated-skills-and-start-choices | done | 2026-10-27 |
| P707 isle-playthrough | done | 2026-10-27 |
| P706 bot-runs-out-of-repo | done | 2026-10-27 |
| P705 fix-p663-codex | done | 2026-10-27 |
| P704 guild-hq-proposal | done | 2026-10-27 |
| P702 tutorial-new-player-text | done | 2026-10-27 |

### Needs reconciling on a `MODERNUO_COMMIT` bump: 172 patches, 12 replacements

_Counted from `server/patches/` and `apply-patches.sh`. The table below is hand-kept in `progress-state.json` and lists 17 rows; it is a partial risk register, not the count._

What a MODERNUO_COMMIT bump must reconcile. Patches fail LOUDLY - apply-patches.sh stops the build. Full-file replacements fail SILENTLY: they always apply, and quietly discard whatever upstream changed in that file.

| Upstream file | Patch | Diff | Risk | Breaks when |
|---|---|---|---|---|
| `Projects/Server/Mobiles/Mobile.cs` | Mobile-set-item-resistance-hook | +18/-5 | **high** | any upstream change to ComputeResistances or the resistance pipeline |
| `Projects/UOContent/Misc/AOS.cs` | AOS-damage-eater-hook | +15/-0 | **high** | any change to AOS.Damage's signature or damage ordering |
| `Projects/UOContent/Misc/AOS.cs` | AOS-set-attribute-aggregation | +11/-0 | **high** | changes to attribute aggregation; three patches share this file |
| `Projects/UOContent/Misc/AOS.cs` | AOS-pet-mimic-attribute-aggregation | +8/-0 | **high** | same file as the two above; upstream just changed OPL hashing nearby |
| `Projects/UOContent/Mobiles/PlayerMobile.cs` | PlayerMobile-fountain-luck-bonus | +1/-1 | **medium** | any change to how loot reads Mobile.Luck. Pinned by a test |
| `Projects/UOContent/Mobiles/PlayerMobile.cs` | PlayerMobile-individual-stat-cap | +3/-3 | **medium** | stat cap handling; second patch on this file |
| `Projects/UOContent/Items/Armor/BaseArmor.cs` | BaseArmor-set-self-repair | +4/-1 | **medium** | changes to self-repair or durability |
| `Projects/UOContent/Items/Weapons/BaseWeapon.cs` | BaseWeapon-talisman-durability | +5/-0 | **medium** | durability handling |
| `Projects/UOContent/Items/Skill Items/Misc/Bandage.cs` | Bandage-pet-mimic-targeting | +9/-0 | **low** | bandage targeting rewrite |
| `Projects/UOContent/Engines/Craft/Core/CraftGumpItem.cs` | CraftGumpItem-MakeX | +15/-1 | **low** | craft gump layout. Label still renders invisible (known) |
| `Projects/UOContent/Engines/Craft/Core/CraftGump.cs` | CraftGump-MakeXClear | +4/-0 | **low** | craft gump layout |
| `Projects/UOContent/Mobiles/Healers/Healer.cs` | Healer-resurrection-policy | +2/-2 | **low** | healer logic |
| `Projects/UOContent/Mobiles/Vendors/NPC/Guildmasters/HealerGuildmaster.cs` | HealerGuildmaster-resurrection | +27/-0 | **low** | guildmaster logic |
| `Projects/UOContent/Engines/Bulk Orders/SmallSmithBOD.cs` | SmallSmithBOD-PostValorite | +33/-0 | **low** | BOD generation |
| `Projects/UOContent.Tests/Fixtures/UOContentFixture.cs` | UOContentFixture-npc-speeds | +13/-0 | **low** | any upstream edit to UOContentFixture's constructor near SkillsInfo.Configure, or a change to what NPCSpeeds.Configure does; either way every creature test fails loudly in the constructor |
| `Projects/UOContent/Mobiles/BaseCreature.cs` | BaseCreature-PlayerMobile-can-auto-stable | +4/-0 | **low** | nothing likely; an added virtual next to IsBondable |
| `Projects/UOContent/Mobiles/PlayerMobile.cs` | BaseCreature-PlayerMobile-can-auto-stable | +6/-0 | **low** | a rewrite of AutoStablePets; three patches now share PlayerMobile.cs |

**12 full-file replacements fail silently on a bump** and must be diffed by hand: `BaseGuildmaster.cs`, `BulkMaterialType.cs`, `CharacterCreation.cs`, `HammerOfHephaestus.cs`, `JacobsPickaxe.cs`, `LargeSmithBOD.cs`, `Meditation.cs`, `Mining.cs`, `RegenRates.cs`, `ResourceInfo.cs`, `TreasureMap.cs`, `TreasureMapChest.cs`.

**Deliberately declined:**

- **Eodon: the Valley of One quest line - REOPENED, and a poor first batch** — Declined by CC3 because ModernUO 'ships a different quest engine'. S3 found ModernUO already ships Engines/ML Quests: 109 files, 240 quests, 205 of ServUO's 408 present by name. S5 then translated one quest end to end and CONFIRMED the objective mapping holds, so this decline is reversed and these are content work. Q-023 answered. But S5 also read all seven: none uses two objective types and THREE of the seven (EmptyNest, TheGreatVolcano, PrideOfTheAmbush) use a hand-written InternalObjective with no counterpart on either side of the mapping, against 19% bespoke across the 203. Reopened, but do not start the quest work here - pick from the 164 single-standard-objective quests instead. See notes/s5-quest-spike.md sections 1 and 8.
- **Eodon: MoonstonePowerGenerator** — CC3. It is Myrmidex Invasion content, not Eodon. It lives inside Services/Expansions/Time Of Legends/Myrmidex Invasion/, spawns Zipactriotl (the Myrmidex boss) and IgnisFatalis, subclasses DamageableItem (absent from ModernUO), and is referenced only by Myrmidex Invasion/System.cs and the MyrmidexThreat quest. It reached the CC3 list because the keyword moonstone matched and nobody opened the file.
- **S3 costed menu - declines upheld with their ratios recorded** — Measured 2026-09-07, notes/s3-decline-costs.md. Skill Masteries (45 files/8,542 lines, unblocks 14, patches 35 upstream files - fails the layering test). Vice vs Virtue (57/9,613, unblocks 5, patches 21). Exploring the Deep (70/10,292, unblocks 2 - structurally the safest build here and the worst ratio). Shadowguard (14/11,222, unblocks 8). City Loyalty (28/8,177, unblocks 15 - decline on ratio, not structure; revisit with Town Cryer). Instanced Peerless (13/1,543, unblocks 2, and BasePeerless and PeerlessAltar are both absent from ModernUO, so there is no base to instance - cost Services/Peerless first). ServUO's ML quest framework (22 files/6,269 lines, not the 21/5,625 the brief stated) - declined because ModernUO already ships the same OSI system. NOT declined and recommended instead: SAAbsorptionAttributes, the TribeType transformation, and a one-quest spike onto ModernUO's ML quest engine. Vendor Searching (4/2,545) is a player feature, not content; the unblock ratio is the wrong test and it is Chase's call.
- **ServUO ML quest framework - decline REAFFIRMED by S5** — S5 translated one quest end to end and the objective mapping holds for 4 of 5 types, two of them pinned by tests. Porting ServUO's 22-file, 6,269-line framework would put a second engine in the tree to do a job the engine we already have does correctly. The decline was always on two-engines-for-one-job; it now rests on measurement rather than on principle alone. What is NOT declined: the 164 of 203 missing quests that use a single standard objective type. The 39 that hand-write a BaseObjective subclass (25 InternalObjective, 3 CollectionsObtain, 2 QuestionAndAnswer, ~9 one-offs) are per-quest work, not a framework port, and are the thing to cost before the next quest batch.

Counted from the trees: 1690 customization files, 179 patch files, 1855 tests in 272 files.
Shard status: the test shard is the only shard: live was retired and deleted on 2026-10-14 until the fresh 1.0 world, and the launcher's Play button now connects to the test shard (2026.10.24.2); the test shard (2594, up) runs sl-modernuo:latest, built 2026-10-23 from main 0f1871f (version 2026.10.23.2), while main is 2026.10.25.7, 33 merges ahead; the overnight bot tests the newest main on its own world copy each night; which player package is published is not visible from the repos (confirmed 2026-10-25).
<!-- PROGRESS:END -->

## Expansion coverage

<!-- EXPANSION:START -->
### Content by expansion

**4,247 of 6,144 ServUO files present** (69%), of which **1,208 ported by us**.

```
Pre-AoS (T2A/UOR/LBR)     ██████████████░░░░░░  3106/4294    72%   +883
Age of Shadows            █████████████████░░░   258/309     84%   +57
Samurai Empire            █████████████████░░░    97/115     84%   +10
Mondain's Legacy          ███████████░░░░░░░░░   263/471     56%   +22
Stygian Abyss (Ter Mur)   ████████████░░░░░░░░   256/444     58%   +131
High Seas                 ██████████░░░░░░░░░░   165/334     49%   +69
Time of Legends (Eodon)   ███████████░░░░░░░░░    85/157     54%   +32
Endless Journey           █████████████████░░░    17/20      85%   +4
TOTAL                     ██████████████░░░░░░  4247/6144    69%   +1208
```

_Filename-stem matching: a proxy for presence, not behaviour. Unclassified files fall into Pre-AoS, inflating it. Directional, not a completion percentage._
<!-- EXPANSION:END -->
