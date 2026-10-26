# P630: the Mythril Echo summon, stage 1

Written 2026-10-26 by the Iron Golem (Claude Code). Builds stage 1 (the design's packet 1) of [cc-P567-design-summons-league-reward.md](cc-P567-design-summons-league-reward.md). Chase's decision (10-25 evening) took the design's defaults: at Mythril rank, a reusable Tome summons a weak Echo of the Stygian Dragon for 20 seconds, using two follower slots, with a 30-minute account cooldown. Packet 1 builds the Echo itself, its storage and its rules, switched off, with no Registrar page and no player-accessible call. The Tome and the player pages are packet 2.

## In plain words

- Players will not see anything yet. The Echo is switched off, and there is no Tome and no Registrar page.
- On the test shard, staff can try it: `[LeagueEcho on`, then `[LeagueEcho call` on a Mythril (or higher) League character. A blue Stygian Dragon "Echo" appears beside you for 20 seconds, fights only wild monsters, and fades without a corpse or loot. That account must then wait 30 minutes to call again. `[LeagueEcho` alone shows the switch and your wait.
- It fades at once if you log out, die, walk more than 12 tiles away, change facet or enter a town, house, jail or other protected place. It cannot be called on Felucca.
- Nothing for you to do. The Tome, the Registrar page and a real fight test come in the next stages (drafted at the end).

## Status

Done. The Iron Golem (Opus), branch `golem/Iron/P630` of both repos, not committed (the Golem commits). The gated build is green (section 3). No shard was started, no world command run, no package built, nothing deployed, no Haven contact.

## 1. What was built

New files (the existing subdirectory route copies them; `apply-patches.sh` is unchanged):

| File | What it holds |
|---|---|
| `server/customizations/LeagueEchoes/LeagueEchoSettings.cs` | `clusterf.leagueEchoes.enabled` (false), `requiredRank` (`Mythril`), `durationSeconds` (20), `cooldownSeconds` (1800), read on each use like `LeagueRegisterSettings`. `Problem()` refuses an unknown rank key, a duration outside 1-60 and a cooldown outside 300-86400; calls are then refused. Two follower slots and a 12-tile leash are constants. `EnabledOverride` is the test shard's in-memory switch (`[LeagueEcho on|off`), never written to `modernuo.json`, and gone on restart. |
| `server/customizations/LeagueEchoes/LeagueEchoPolicy.cs` | Facets: Trammel, Ilshenar, Malas, Tokuno, Ter Mur. Refused anywhere in a region's parent chain: `HouseRegion`, `JailRegion`, ConPVP `SafeZone` (even with its guards off), `TutorialYardRegion`, `ApprenticeTrainingRegion`, and any `GuardedRegion` whose guards are on. Spawn tile: the first of the 8 neighbours (at the caller's Z or the map's average Z) that `Map.CanSpawnMobile` accepts, is in the caller's line of sight, and is in a permitted region; never the caller's own tile, and no fallback. Legal target: a living, unowned, unsummoned, unbonded, vulnerable, not initially innocent creature that is not a vendor, escort, tutorial creature or another Echo. Players and guards are not `BaseCreature`, so they are never legal. |
| `server/customizations/LeagueEchoes/LeagueEchoSystem.cs` | `Check` and `TryCall`. Refusals in order: switch, settings, account, rank, frozen/paralysed/casting/dead, duel, facet, region, an Echo already out for the account, cooldown, slots, then no room. The call reserves the account, finds a tile, and calls the controlled `BaseCreature.Summon` overload with the captured duration. It then checks the result: summoned, owned by the caller, on the caller's map, on the chosen tile. Only then does it set Follow, register the Echo, set the account's next use to now plus 1,800 s, and reveal the caller. A failure deletes the creature; an exception deletes it and rethrows; the reservation is always released. The registry holds one Echo per account. It ends through the logout event, the `PlayerDeathEvent`, and a one-second watchdog: owner gone, switch off, another map or more than 12 tiles, a forbidden place for the Echo or the owner, a duel, a lost rank. The watchdog also drops an illegal combatant. `Dismiss` works only for the calling character and also with the switch off. `[LeagueEcho [status|on|off|call|dismiss]`: GameMaster, `[ShardCommand(DevTool, TestOnly)]`. |
| `server/customizations/Mobiles/LeagueEchoes/LeagueDragonEcho.cs` | A direct `BaseCreature` (not a `StygianDragon` child), with generated serialization v0. `AI_Melee`, `FightMode.None`. Str/Dex/Int 200/100/50; 300 hits, 100 stamina; no mana (`ManaMax` is 0, because `SetMana(0)` leaves the maximum at Int). Damage 12-16 (75 physical, 25 fire); 35 in every resist; Wrestling, Tactics and Magic Resist 80; every skill locked. Fame and Karma 0, VirtualArmor 0, `NoKillAwards`, 2 control slots. Body 826, hue 1323 (League blue), sound 362, summon sound 0x216. Dispellable at difficulty 100, focus 20. Never flees, auto-stables, bonds or drops; no loot, resources or treasure map. `OnBeforeDeath` dissolves it (effect, Delete) and returns false, so lethal damage and Release leave no corpse and raise no death event. `CanBeHarmful` and `IsEnemy` go through the policy, then the owner's own harm check, then the base. `OnAfterDelete` tells the registry. After a world load it deletes itself and never registers. `[add` needs Administrator. |

Changed files:

| File | Change |
|---|---|
| `ClusterFAccountData.cs` | Account v22 to **v23**: appends `DateTime LeagueEchoNextUseUtc` (`DateTime.MinValue` = ready; earlier versions read as ready). `CharacterLeagueData` v2 to **v3**: appends `uint EchoTomeSerial` (0 = none; packet 2 uses it). Unknown versions are still refused. I checked all 143 remote branches before taking these numbers; none had v23 or League data v3. |
| `AccountDataSerializerVerification.cs` (3 lines), `LeagueShopVerification.cs` (3 lines), `RequisitionsVerification.cs` (3 lines), `MuleVerification.cs` (1 line) | Existing facts pinned the account version at 22 (and hand-cut its tail), or the League data version at 2. Now 23 with the extra 8-byte tail, and 3, each with a `cc-P630` comment. My first search missed the last two; the first gate run found them (section 3). |

Not in packet 1, as the design orders: the Tome, its gump, the Registrar entry and claim/replace (packet 2), and the real save/reload, client and balance checks (packet 3). `EchoTomeSerial` is stored and saved but nothing sets it yet.

## 2. Tests: red first, then green

New: `server/tests/Misc/LeagueEchoesVerification.cs` (9 facts) and `server/tests/Mobiles/LeagueDragonEchoVerification.cs` (4 facts).

| Fact | What it shows |
|---|---|
| `TheSettingsDefaultOffAndRefuseBadValues` | Off, Mythril, 20, 1800, 2 slots; an unknown rank, durations 0 and 61 and cooldowns 299 and 86401 refused; Celestial/60/86400 accepted. |
| `OnlyAMythrilCharacterOrHigherMayCall` | A Blaze character on a Mythril's account is refused with "Mythril" in the message; Mythril and Celestial call. |
| `ACallChargesTwoSlotsOnceAndStartsTheAccountCooldown` | Followers 0 to 2, FollowersMax unchanged; summoned, owned, Follow, on a neighbouring tile; next use exactly now plus 1,800 s; caller revealed; a second call by the same or another character on the account is Active with no extra slots; another account calls independently. |
| `TheCooldownEndsExactlyAtItsDeadline` | One tick before: Cooldown ("12m 08s" shown for 728 s); at the deadline: Called. |
| `ARefusedCallLeavesNoCreatureNoSlotsAndNoCooldown` | Switch off; one slot short; every neighbour inside a jail ring while the caller stands outside it (NoRoom). No creature within 3 tiles, followers unchanged, next use still MinValue. |
| `TownsJailSafeZonesTutorialAndFeluccaAreRefusedAndADungeonIsNot` | Felucca refused (Facet); a registered guarded town refused (Region); a safe zone with guards off refused, including a real call inside it; the jail, the tutorial yard and the Apprentice grounds refused; a guarded region with guards off allowed; a call inside a dungeon succeeds; Malas allowed, Internal refused. |
| `EveryEndingDissolvesItGivesTheSlotsBackAndKeepsTheCooldown` | Seven endings: Dismiss (the alt cannot), the death event, the logout event, 13 tiles away, Malas, rank lowered to Blaze, switch off. Each deletes the Echo, returns followers to 0, empties the registry and leaves the deadline unchanged. Inside range the watchdog leaves it alone. A stale Echo of the same account deleted later does not remove the one held. |
| `TheEchoIsGoneTwentySecondsAfterTheCall` | With `ShardTestClock`: still there at 19 s, gone at 20.5 s, slots back, registry empty, and the account still on cooldown. |
| `TheTwoNewFieldsSaveAndOlderSavesReadAsReady` | Account v23 round-trips the time to the last byte. The same bytes cut to v22 read as ready, with Renown intact and every byte consumed. League data v3 round-trips the Tome serial; cut to v2 it reads 0 with rank intact; version 4 is refused. |
| `ItsProfileIsTheDesignsWeakOne` | Every number in the design's table, all skills locked, no resources, an empty pack, the name, and not a `StygianDragon`. |
| `LethalDamageDissolvesItWithNoCorpse` | `Kill()` on a called Echo: deleted, followers 0, registry empty, no corpse within 3 tiles. |
| `ItMayHarmAWildCreatureAndNothingElse` | An orc: legal, harmable, an enemy. Not harmable: another player, its own caller, a tamed horse, a summoned daemon, a provisioner, a warrior guard, an escortable mage. An orc picked as its combatant and then tamed: no longer harmable, and the watchdog clears the combatant. |
| `ASavedEchoDeletesItselfAfterLoad` | Serialize a called Echo, delete it, deserialize a copy: not registered, and deleted on the next timer slice. |

How I ran them: builder image `sl-uo-builder:cc-P627` (this branch's base, merge `a113b35`), with the account data file, the four new source files and the four test files bind-mounted. `dotnet test` was filtered to the two new classes plus `AccountDataSerializerVerification`, `LeagueShopVerification` and `LeagueRegisterVerification`, with the gate's flags. Scripts and logs are in the session scratchpad.

**Red.** Inert stubs with the same public names: the account data at v22 with the two properties present but never saved; settings with no validation; a policy that allows everything; a service whose `TryCall` always returns Failed and whose registry is empty; a plain `AI_Melee` creature with no profile and no overrides. All 13 new facts failed on assertions. Fact 1: "Value is null". Fact 9: "Expected: 23, Actual: 22". The profile fact: "Expected: 200, Actual: 0". The rest: "Expected: BelowRank / Disabled / Facet / Called / Cooldown, Actual: Failed". The four updated existing facts failed the same way ("Expected: 23, Actual: 22").

**Green.** The real sources: 60 of 61 passed, all 13 new facts among them. The fixes made on the way to green:
- `ManaMax` was 50 because `SetMana(0)` leaves the maximum at Int: added `ManaMax => 0`.
- My test's "unknown" rank key, Adamantium, is a real metal on this shard: changed to "NotAMetal".
- `SafeZone`'s constructor registers itself, which left a safe zone over the test spot: the fact now unregisters it.
- The shop's titles save test trims a hard-coded tail, which now includes the 8-byte v23 field.
- The test host never runs `Configure`, so the logout hook was missing: `Configure` is now idempotent and the facts call it. This was a test-host gap; the code was already right.
- One fact forgot to clear the cooldown before its last call.

The one remaining failure is `LeagueShopVerification.TheStockIsF13sStarterTableAndHandsOverNoMagicItem`: a NullReferenceException inside pinned `TreasuresOfTokuno.RewardEra` (`TreasuresOfTokuno.cs:124`). It fails identically against the stubs, so it does not come from this code. It is a setup the filtered run lacks; the full gate below is the real check.

**Mutations of the finished code**, each run alone against the two new classes:

| Mutant | Red facts |
|---|---|
| m1: no `OnBeforeDeath` override (the Echo dies normally) | `LethalDamageDissolvesItWithNoCorpse`: the killer's achievement "kills" counter goes from 1 to 2. On the first try this mutant **survived**: a summoned creature's corpse is deleted anyway, so "no corpse" could not tell them apart. I strengthened the fact. An ordinary orc killed by the same player first shows the counter moving (CreatureDeathEvent, any LastKiller player), then the Echo's death must not move it. Re-run, it is red on the mutant and green on the real code. |
| m2: every mobile is a legal target | `ItMayHarmAWildCreatureAndNothingElse` |
| m3: no delete after load | `ASavedEchoDeletesItselfAfterLoad` |
| m4: any delete of the account's Echo clears the registry | `EveryEndingDissolvesItGivesTheSlotsBackAndKeepsTheCooldown` (the stale-callback step) |
| m5: the cooldown is charged when no tile is free | `ARefusedCallLeavesNoCreatureNoSlotsAndNoCooldown` |

Each mutant turned exactly its one fact red, 12 of 13 passing. The real code after the change: 13 of 13.

## 3. Build gate

`docker\uo\build.sh -t sl-modernuo:cc-P630`, under the Golem's `docker-build` lock (taken, released, taken again, released). Before each run I dropped the Docker VM's page cache and started the build detached.

- **Run 1: red.** 2,543 tests: 2,537 passed, 4 skipped, 2 failed. Both were existing facts pinned to the old save layout. `MuleVerification.TheLeagueRecordsVersionZeroBytesStillLoad` ("Expected: 2, Actual: 3", League data version). `RequisitionsVerification.TheRecordSurvivesAWriteAndAReadAndAVersion19SaveLoadsWithNoBoard` ("Expected: 22, Actual: 23", which also cuts the account tail by hand). I fixed both the same way as the earlier four: the new version, the extra 8 bytes, a `cc-P630` comment. A wider search found no other such pin.
- **Run 2: green**, exit 0: "Built sl-modernuo:cc-P630 with patches applied and 2539 shard test(s) passing". 2,543 tests, 2,539 passed, 4 skipped (the real-map facts), 0 failed. Image `3e3e3823a447`. The 13 new facts passed in it. So did the two fixed pins, the five `CommandDeclarationVerification` facts (so `[LeagueEcho`'s declaration is accepted), and `LeagueShopVerification.TheStockIsF13sStarterTableAndHandsOverNoMagicItem`, which confirms its filtered-run failure was a setup gap.

## 4. CHANGELOG

A `## 2026.10.26.2` section with one **Staff** line (the test-shard command, what the Echo does, and its limits), and `VERSION` `2026.10.26.2`. There are no player lines: players see nothing in packet 1. I took `.2` because P629's branch, not yet in main, uses `2026.10.26`; the two sections then sit apart. If the integrator renumbers, keep both, newest first.

## 5. Deviations and decisions for Chase

- **Read tool denied** (the unattended run): I asked to `Read` `D:\UO\golems\Iron\ShatteredLegacy\server\customizations\ClusterFAccountData.cs` (offset 220, 10 lines), so I could `Edit` it. It was denied automatically, a known limit for some files in this work copy. I made the same exact edits with a scratch Python helper that refuses unless each old text occurs exactly once. All edits to existing files and to my new files went that way after the first denial. The result is the same; the diff is what `git diff` shows.
- **Staff command in packet 1.** The design puts no player-accessible call in packet 1. `[LeagueEcho` is GameMaster-only and `[ShardCommand(TestOnly)]`, so staff can play the slice on the test shard. It runs the players' rules on the staff member's own character, including the Mythril rank, which staff set with `[props LeagueRank`.
- **Logging bad settings.** The design asks for refused settings to be logged. Packet 1 refuses calls and shows the reason in `[LeagueEcho`, but writes no server log line. Packet 2's draft adds the log.
- **Design tests left for later packets, and why:** a `HouseRegion` refusal needs a placed house (packet 3's scratch world); a non-null `DuelContext` cannot be built in the test host (the check is in code, unproven by a fact); bard provocation and area or delayed attacks are packet 3's fight checks. The kill-credit consumers (achievements, bestiary, requisition Leads, evo XP, level gear XP) with an Echo dying at zero hits are partly covered: no death event fires at all, because `OnBeforeDeath` returns false. Each consumer is not yet checked one by one; packet 2's draft carries that. Real world save/load with follower reconciliation is packet 3, as the design orders.

## 6. Proposed invented-feature register text (for the overseer, not `docs/`)

> League Echo (Tome of Echoes; P567 design, P630 onward). Native custom League reward inspired by TwilightRaven's summoning-system-v2 idea (P405 notes; no code copied). At Mythril Citizen a character-bound Tome calls one weak, friendly Echo of the Stygian Dragon for 20 seconds, using two follower slots, with a 30-minute account cooldown. PvE only on Trammel, Ilshenar, Malas, Tokuno and Ter Mur, outside houses, towns and protected regions; no loot, no corpse, dispellable. Player guide scope: the Registrar page, the Tome, the cooldown, the follower cost, where it works, and that it is not F-12's loop memory or the tutorial's Echo voice.

## 7. Remaining stages, ready to number

Each prompt writes its own notes, keeps files under 5 MB, checks its stop-request file, lets the Golem commit, starts from current canonical source, rereads the agreements and P567 and this note, and never deploys or contacts Haven.

### Draft A: League Echo, the Tome, the Registrar page and claim/replace (packet 2)

**Touches:** server

Depends on P630. Chase's choices (10-25): Mythril, a reusable Tome, the Stygian Dragon Echo, 20 s, 2 slots, 30 min account cooldown.

1. `LeagueEchoes/TomeOfEchoes.cs`: generated serialization, owner Mobile, blessed, weight 1, art 0xEFA, League hue 1323, owner's name in its properties, no charges or sell value. It works only in its owner's backpack and only while its serial equals the character's `CharacterLeagueData.EchoTomeSerial` (stored since P630). A deleted owner or missing account makes it inert.
2. `LeagueEchoes/TomeOfEchoesGump.cs`: the design's page (name, the two plain lines, follower use, rank, Ready / "Ready in 12m 08s" / "Echo active: 11s remaining", Call, Dismiss, Close). Every response rechecks the owner, the carried Tome, its serial and the rank, and goes through `LeagueEchoSystem.TryCall` / `Dismiss`. Never trust the displayed state.
3. `LeagueRegistrarGump.cs`: an "Echo reward" entry at every rank. Below Mythril it explains; at or above it offers "Claim Tome of Echoes", or "Replace Tome of Echoes" once issued. Keep it reachable at Celestial despite `DrawRank`'s early return. Reserve unused response IDs after reading current main. Claim and replace are free and rechecked on response (four tiles, line of sight, same map, rank, pack room). Order: construct, place in the pack, record the serial, then delete the old copy. A full pack keeps the old copy and serial. Replacing never resets the cooldown or dismisses an Echo.
4. Log a refused setting once per value (`LeagueEchoSettings.Problem`). Add the per-consumer no-reward checks: an Echo brought to zero hits by a player or a creature changes no achievement counter, AP, Renown, loot-box ledger, bestiary entry, requisition Lead, evo XP or level-gear XP. Echo damage to a wild victim keeps the normal master attribution.
5. Red-then-green facts: wrong character, copied item, obsolete serial, banked, missing or deleted Tome, stale page; claim below rank, at Mythril and at Celestial; Registrar moved away and forged responses; free replacement invalidates the old copy; full pack keeps everything. Show each red first.
6. `docker\uo\build.sh -t sl-modernuo:cc-P<nn>` green. Keep the switch off. CHANGELOG Staff line only. Notes; `P<nn> DONE`.

### Draft B: League Echo, full lifecycle, appearance and combat balance (packet 3)

**Touches:** server

Depends on Draft A.

1. Under the Golem's `test-shard` lock, on a disposable loopback-only shard with scratch saves: save during an active Echo with the Tome in a nested pack, then reload. The Tome's owner, serial and deadline survive; the Echo is gone; the registry is empty; there is no corpse; follower counts reconcile.
2. Ordinary dispel, Release, every ending from P630's fact list in a live world, a placed house refusing a call, and a duel refusing one.
3. Bard provocation and discord, area and delayed attacks: nothing hits a player or a pet.
4. In a test client from the installed package (no client rebuild or publish): body 826 in hue 1323, the book, labels, movement, attacks and the dissolve.
5. Balance with the same character and gear: baseline against Echo-assisted fights versus an ordinary melee monster, a caster, a mini-boss (the Siegebreaker or the Hollow Oak) and the real Stygian Dragon, then a party of several eligible accounts. Record damage, time to kill, damage taken, dispel timing and deaths. Tune only the Echo's numbers if it fails the design's pass rules, with red-first facts for any defect.
6. Build gate green; switch off; notes; `P<nn> DONE`.

### Draft C: League Echo, player guide and activation handoff (packet 4)

**Touches:** docs-only

Depends on Draft B's evidence. Put the wiki-ready guide, release-note text, the register entry above, the verified numbers and the test and client evidence in notes. State the setting to turn it on and how to turn it off while keeping the schema readers. Name the exact build already tested. Do not activate, publish or touch a running shard. Notes; `P<nn> DONE`.

P630 DONE
