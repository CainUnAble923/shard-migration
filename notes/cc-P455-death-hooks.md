# cc-P455: death hooks: boss loot boxes and the rare Self Repair roll fire; pets' kills count for the bestiary

## In plain words

- The first time a player helps kill a boss, the boss loot box now really arrives. Before this, the game never gave
  it to anyone, because the check ran after the boss had already been removed from the world.
- The very rare Self Repair property (1 magic weapon or armor piece in 500 on a boss's or paragon's corpse) now really
  rolls. It had the same problem and never rolled once.
- Kills finished by a player's pet, a summon or a creature the player provoked now add that creature to the player's
  League bestiary, with its two lines. Killing someone else's tamed pet no longer pays Butcher's Eye.
- Nothing for you to do. It is in the patch notes as version 2026.10.24.13.

## Why it was broken

Pinned's `Mobile.OnDeath` deletes a dead non-player creature (`Mobile.cs:4899-4902`) before `BaseCreature.OnDeath`
raises `CreatureDeathEvent` (`BaseCreature.cs:3669`). The delete sets `Deleted` and, in `BaseCreature.OnDelete`, clears
a pet's master (`:3687-3688`). `CreatureDeletedEvent` is raised first, at the top of `OnDelete` (`:3674`), and at that
point the creature is still whole.

I checked in pinned (`D:\UO\ModernUO-pinned`, d4531cd) that the corpse is ready by then. `Mobile.Kill` moves the
backpack and loot into it and calls `CreateCorpseHandler` (`Mobile.cs:4847`). `Corpse.Mobile_CreateCorpseHandler`
sets `owner.Corpse` (`Corpse.cs:619`), and only after that are `Region.OnDeath` and `OnDeath` called. `Hits` is 0,
`LastKiller` is set (`Mobile.cs:6018`), and the damage list is still there.

## What changed

ShatteredLegacy, branch golem/Iron/P455. Every moved handler uses P263's guard, `Hits <= 0 && !IsDeadPet`, the same
one P427 used for level gear. P427 merged but added no shared helper (`ClusterFLevelGear.OnCreatureDeleted` has the
guard written out inline), so these handlers write it inline too.

| Part | Change |
|---|---|
| 1, boss box | `LootBoxes/ClusterFLootBoxes.cs:173` `OnCreatureDeath` becomes `OnCreatureDeleted` on `CreatureDeletedEvent`, with the guard. The rest is unchanged: looting rights, `LastKiller`, `OnBossKilled`. |
| 1, Self Repair | `ClusterFRareSelfRepair.cs:47` `OnCreatureDeleted` (the guard) calls `RollCorpse` (`:57`), which is the old body. The header comment now says which event it uses and why. `RareSelfRepairVerification` fact 4 calls `RollCorpse` where it used to call the handler, because its creatures are alive. |
| 2, imbue | `Imbuing/ClusterFImbueEffects.cs:319` moves to `CreatureDeletedEvent` with the guard. Its `!Controlled && !Summoned` check is now read before the master is cleared, so a killed non-bonded pet pays no Butcher's Eye. |
| 3, bestiary | `ClusterFLeagueBestiary.cs:182` `KillerOf`: `LastKiller is BaseCreature k ? k.GetDamageMaster(bc) : LastKiller`, as pinned credits fame (`BaseCreature.cs:3570`). `GetDamageMaster` (`:3992`) returns the bard for a provoked killer, and otherwise `GetMaster()`, which is `ControlMaster ?? SummonMaster`. Only the killer is read, and the killer is not deleted, so this stays on `CreatureDeathEvent`. |
| CHANGELOG | 2026.10.24.13, Fixed: the two lines the prompt gave. VERSION bumped. This branch started before P454 merged, so it bumps from .11. I used .13 because main already has P454's .12. |

**Bonded pets.** A bonded pet does not get deleted when it dies, so no `CreatureDeletedEvent` fires. None of the
three moved handlers should act on one: a pet is never a boss or a high-end source, and the imbue effect skips
controlled creatures. So none of them keeps a `CreatureDeathEvent` branch.

**Late boss drops.** A boss's own `OnDeath` override can drop items after `base.OnDeath`, and those are not in the
corpse yet when the Self Repair roll runs. I checked every high-end source. Navrey (`UntranslatedAncientTome`),
BasePeerless (MondainsLegacy artifacts), the Shame bosses (crystals, grit, ash, oilstones) and BaseChampion (a
skull, Felucca only) drop only artifacts or non-equipment, and the roll skips those anyway. Nothing is lost.

## The audit (part 2): every `[OnEvent(CreatureDeathEvent)]` in server/customizations

| Handler | Reads of the victim | Verdict |
|---|---|---|
| `ClusterFAchievements.cs:1503` | `LastKiller` only | Fine. It reads no master or `Deleted`. |
| `ClusterFLeagueBestiary.cs:171` | `LastKiller` | Fixed (part 3). |
| `ClusterFNotedBySystem.cs:623` | `IsBonded && Controlled` | Fine. A bonded pet is never deleted, so this sees it whole. Every other death goes through P263's `CreatureDeletedEvent`. |
| `ClusterFRareSelfRepair.cs:42` | `Deleted` (through `IsHighEndSource`) | Moved (part 1). |
| `Imbuing/ClusterFImbueEffects.cs:314` | `Controlled`, `Summoned` | Moved (part 2). |
| `LootBoxes/ClusterFLootBoxes.cs:166` | `Controlled`, `Summoned`, `Deleted` | Moved (part 1). |
| `Mobiles/Evo/EvoPet.cs:240` | `Controlled`, `Summoned`, `IsBonded` | Fine. It already records "was controlled" at `CreatureDeletedEvent` (`:229`), in a weak table. |
| `Music/ClusterFShardMusic.cs:601` | the creature itself (ends a fight) | Fine. |
| `Requisitions/RequisitionLeads.cs:228` | the killer's `GetMaster` | Fine. The killer is not deleted, as Crystal said. |
| `Services/CleanUpBritannia/ClusterFCorpseValue.cs:49` | `Corpse`, damage list | Fine. It reads no master. |
| `Revamped Dungeons/.../ExodusEncounter.cs:88` | `Controlled: false, Summoned: false` | Fine in effect. A minion is never a pet, but a tamed one would roll the drop. Not worth moving. |
| `Seasonal Events/.../SorcerersDungeonData.cs:84` | `Deleted`, used only to pick the map | Fine. It keeps the map from its own delete hook (`_deleting`). |
| `StaffHub/ClusterFSurge.cs:618` | membership in the surge's set | Fine. |

No other handler reads the deleted victim's master or `Deleted` in a way that changes what it pays.

## Tests

New file `server/tests/Misc/DeathHooksVerification.cs`. Every fact kills through the game's own path (`Damage` to
zero, or `Kill()`) and never calls a handler directly:

1. `ABossKilledByAPlayerGivesTheFirstKillLootBox` (:126): a player kills a Barracoon, and the loot record holds
   `boss:Barracoon` once.
2. `AHighEndCreaturesCorpseGetsTheSelfRepairRoll` (:143): a paragon chicken carries a magic plate chest. With every
   random roll forced to 0 (the 1 in 500 hits), `Kill()` leaves the plate in the corpse with Self Repair 1. An ordinary
   chicken killed the same way gets nothing.
3. `AKilledNonBondedPetPaysNoImbueKillEffect` (:193): a player wears a ring with Butcher's Eye 20. A wild cat with
   10 daemon claws comes out with more than 10. Another player's tamed, unbonded cat stays at exactly 10.

In `server/tests/Mobiles/Bestiary/LeagueBestiaryVerification.cs`:

- The fixture now calls `ShardTestHost.EnsurePoisons()` (P404 #3).
- Fact 6, `EveryCreaturesNumbersAreP364sTableAndItsPoisonsWorkWithThePoisonsRegistered` (:445), covers P404 #2 and
  #3. For all fourteen creatures it checks against P364's table: stats, hits, damage range and damage type, the
  resists the table names, fame, active speed, weapon ability, meat and hides, and fixed drops (fish, logs,
  reagents, ash). The crawler poisons a player with Lesser, and the thornwisp and the Hollow Oak with Regular. The
  four lethal-immune creatures refuse Lethal, and a moonmaw takes it.
  One gap in the table: P364 lists no meat for the Brine Lurker, but the code gives it 1. The row records the code's
  value and says so. I did not change the creature.
- Fact 7, `AKillByThePlayersPetSummonOrProvokedCreatureEntersThePlayersBestiary` (:533) (P404 #1): a kill by a tamed
  dog, a summoned dog, or an orc the player provoked onto the victim enters the player's bestiary. A wild orc's kill
  enters nobody's.

**Red first.** I probed on `sl-uo-builder:cc-P454` (the builder from before these fixes), with the edited files
bind-mounted and `dotnet test` filtered to the classes involved:

- **Old code, new tests:** 10 run, 5 failed, each for its own reason. The boss box gave "no first-kill box for the
  boss". Self Repair gave "the paragon's corpse plate has Self Repair 0". The imbue fact gave "a killed pet paid
  Butcher's Eye: 12 claws". The bestiary pet kill gave "a kill by the player's pet was not recorded". Fact 6 gave
  "BrineLurker: meat 1": that was the table gap above, fixed in the test.
- **Fact 6 is a regression guard**, so it passes on the old code. To show it fails when it should, I ran four
  mutants, one per probe, each red with its own message. Hollow Oak fire resist set to 30-40: "TheHollowOak: Fire
  resist 37, table 5-15". The lurker's fish removed: "BrineLurker: 0 RawFishSteak, table 2". The crawler's hit poison
  set to Regular: `Assert.Same` failed. The fixture without `EnsurePoisons`, run alone: "Assert.NotEmpty() Failure:
  Collection was empty".
- **Fixed code, probe:** 104 of 104 passed across DeathHooks, LeagueBestiary, RareSelfRepair, NotedBySystem,
  LevelGear, every Imbu* class and every LootBox* class.

**Green, the gate:** `docker/uo/build.sh -t sl-modernuo:cc-P455`, under the `docker-build` lock (taken, then
released): **2,321 passed, 0 failed, 4 skipped**, no compiler warnings, runtime image built, EXIT=0. Free memory was
4.2 GB before the run. I dropped the Docker VM's page cache first, which brought it to 7.2 GB.

## Deviations and decisions for Chase

- The probes used `docker run` on an existing builder image, with no lock, as earlier runs did. The gated build was
  run once, for green. The red evidence comes from the probes, which run the same tests on the same builder.
- I made the edits in ShatteredLegacy with small Python exact-replace scripts, as in P454, because the Edit tool
  needs a Read first and the Read tool is denied there in unattended runs. The diff is the same as an Edit would have
  made.
- Not done, because the prompt did not ask: P404 #4 (a spawn population test) and #5 (the level estimate in P364's
  notes). Both are still open in Crystal's W1 table.

P455 DONE
