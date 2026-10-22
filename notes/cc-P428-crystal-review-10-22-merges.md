# cc-P428: a read-only code review of the 10-22 server merges

**Golem:** Crystal (cloud). **Date:** 2026-10-22. **Branch:** `golem/Crystal/P428` (shard-migration only; no code changed).

## In plain words

- Nothing serious: no crash, no broken save, no merge that lost or doubled code.
- Three merges landed on 10-22 before this review: P354 (the Eodon port, P198's code), P380 (chopped tree stumps,
  P359's code) and P274 (Fable week tracking, Golem tooling only, nothing under `server\`). P408, P289 and P410 had not
  merged when I ran.
- One real gameplay bug: a tamed dragon turtle hatchling keeps about 90% of its very high wild skills (wrestling,
  magery and resist around 120-135) where ServUO cuts them to 45%, and it loses half its stats, which ServUO does not
  do. Today it can only come from a staff `[add`, so no player has one yet. Codex's P407 found the same thing
  (its finding 2). I confirmed it on my own; there should be one fix prompt, not two.
- Two small ones: the Eodon climbing vine lifts a paralyzed or frozen player 40-60 tiles up a cliff, out of a fight;
  and the two 10-22 merges put their patch notes under yesterday's version `2026.10.21.24` without a new version.
  That second one only matters if a server already ran .24 before them: then players who saw the .24 bulletin are
  never shown the Eodon and stump lines.
- The stumps code is clean apart from the floating stump that P412 already fixes. I found nothing new to add there.
  Codex's P400 has one more small stump bug (a polearm gets the "equip an axe" message), which P429 handles.
- I read the code here and pinned ModernUO (`d4531cd9`), and ServUO where the port follows it. Nothing was built or
  run, because a cloud Golem cannot build the shard.

## Findings (most severe first)

### 1. A tamed dragon turtle hatchling keeps near-wild skills and loses half its stats (wrong behavior)

- **Where:** `server/customizations/Services/Expansions/Time Of Legends/Mobiles/DragonTurtleHatchling.cs:9-11` (the
  header), `:54` (`ControlSlots = 5`), `:65` (`StatLossAfterTame => true`); no `OnAfterTame` override.
- **What goes wrong:** ServUO's hatchling (`Scripts/Services/Expansions/Time Of Legends/Mobiles/DragonTurtleHatchling.cs:56-71`)
  overrides `OnAfterTame`. On a first tame it caps each skill and takes 55% off it (`sk.Base - sk.Base * .55`). It does
  not set `StatLossAfterTame`, so ServUO keeps its stats. The port's header says "OnAfterTame has no hook in pinned"
  and uses `StatLossAfterTame` instead. But the shard already has the hook: `BaseCreature.PetTraining.cs:152` declares
  `public virtual void OnAfterTame(Mobile tamer)`. `PetTrainingHooks.OnTamed` (`PetTrainingHooks.cs:170-172`) calls it,
  and `server/patches/AnimalTaming-pet-training.patch:27` wires it into every successful tame. So the port went for the
  substitute while the real hook was there. The result after a first tame:
  - Pinned's own `ScaleSkills(0.90)` (pinned `Skills/AnimalTaming.cs:423`) leaves wrestling at 126-135, magery at
    117-126, magic resist at 117-126 and eval int at 90-107. ServUO's version leaves about 63-68, 58-63, 58-63 and
    45-54.
  - `ScaleStats(0.50)` (pinned `:426-429`) halves str, dex, int and hits: 550-850 hits become 275-425. ServUO keeps
    them.
  - The pet keeps DragonBreath and BleedAttack and costs 3-4 slots (Pet Training's clamp, test `:184-187`). The result
    is a pet much stronger in skill and weaker in hits than ServUO's.
- **How it is hit:** a GM `[add`s a hatchling (CHANGELOG 2026.10.21.24 Staff: "On no spawner yet, for [add: ... the
  dragon turtle hatchling (tamable ...)") and a tamer with 104.7 taming tames it. No spawner places one today. It
  becomes real when the Dragon Turtle champion or the nests come in, or when staff hand one out at an event.
- **Order to keep in mind:** pinned adds the owner (`AnimalTaming.cs:440`) before our hook runs (the patch at
  `:442+`). ServUO's `Owners.Count == 0` first-tame test would therefore never be true here. "First tame" is
  `Owners.Count == 1` at the hook. Also, pinned's 0.90 skill scale has already run, so ServUO's 55% cut has to come
  from the creature's own pre-tame base, or be applied on top with the numbers worked out. P407's finding 2 says the
  same.
- **Test that cannot fail:** `server/tests/Services/TimeOfLegends/EodonRemainderVerification.cs:189` only asserts the
  flag `StatLossAfterTame`. Nothing tames a hatchling.
- **Needs a server?** No for the logic. A test host can tame one through `PetTrainingHooks.OnTamed` after setting the
  owner, as the patch does.

**Prompt draft:**

```
# CC task P??: dragon turtle hatchling: ServUO's first-tame skill cut, through the shard's OnAfterTame hook

**Model:** Sonnet
**Touches:** server
**Golem:** any

**Summary:** The P198 port gave the dragon turtle hatchling StatLossAfterTame (half stats) in place of ServUO's
OnAfterTame (skills cut to 45% and capped, stats kept), saying pinned has no hook. The shard has had the hook since
cc-P130 (BaseCreature.PetTraining.cs:152, called by PetTrainingHooks.OnTamed from the AnimalTaming patch). Port the
real override and drop the substitute.

Found by cc-P428 (Crystal's review of the 10-22 merges), finding 1, and Codex's cc-P407, finding 2. One prompt for both.

## What to do

1. `server/customizations/Services/Expansions/Time Of Legends/Mobiles/DragonTurtleHatchling.cs`: remove
   `StatLossAfterTame => true` (:65). Override `OnAfterTame(Mobile tamer)` with ServUO's body
   (DragonTurtleHatchling.cs:56-71 in ServUO pub57): for each skill with Base > 0, Cap = max(100, Base - Base * 10),
   Base = Base - Base * .55; SkillsCap = Skills.Total. The guard: pinned adds the owner before our hook
   (AnimalTaming.cs:440, patch :27), so a first tame is `Owners.Count == 1` here, not ServUO's `== 0`. Decide and
   write down whether the 55% applies on top of pinned's 0.90 (ScaleSkills ran first, AnimalTaming.cs:423) or to the
   pre-tame base. ServUO's own AnimalTaming also scales by 0.90 before OnAfterTame, so "on top" is the faithful one.
2. Fix the header comment (:9-11): the hook exists.
3. Tests (`server/tests/Services/TimeOfLegends/EodonRemainderVerification.cs`): tame a hatchling the way the patch
   does (Owners.Add, SetControlMaster, PetTrainingHooks.OnTamed) and assert wrestling, magery and resist are
   about 0.9 x 0.45 of the wild values, str and hits unchanged, and a second tame by another owner changes nothing.
   Show it red against today's code first. Replace the flag-only assert at :189.
4. Build and run the tests (`docker\uo\build.sh -t sl-modernuo:cc-P??`).
5. CHANGELOG: a Staff line only (no player can get one yet): "A tamed dragon turtle hatchling now loses skill on
   taming as on OSI, and keeps its strength and hits."
6. Notes: `notes\cc-P??-hatchling-after-tame.md`. Last line `P?? DONE`.

**Done means:** a tamed hatchling's skills are ServUO's, its stats are not halved, and the test shows it.
```

### 2. The Eodon climbing vine lifts a paralyzed or frozen player up the cliff (wrong behavior, minor)

- **Where:** `server/customizations/Services/Expansions/Time Of Legends/Items/ClimbingVine.cs:33-42`.
- **What goes wrong:** `OnDoubleClick` moves the player to `_climbLocation` (679,1757,100) if they are within 2
  tiles and not above the vine. Nothing checks `Paralyzed`, `Frozen`, a spell in progress, or recent combat. Pinned's
  `Mobile.Use` only stops the dead (`Mobile.cs:4968`), not the paralyzed. ServUO has the same code, so this is a
  faithful port of a ServUO hole.
- **How it is hit:** a player fighting near the vines (desert and Barako spawns are close, `EodonSpawns.cs:86-106`)
  is paralyzed by a paralyze spell or an anchisaur's Paralyzing Blow (`Anchisaur.cs`) and double-clicks the vine. They are
  lifted out of reach 40-60 tiles up. It also carries a player out of a PvP fight in Felucca rules if Ter Mur ever
  allows one. It does not carry pets or followers.
- **Needs a server?** No for the logic. Whether the clifftop has a walking way down (so a climber is not stranded
  without recall) needs the map on the game PC.

**Prompt draft:**

```
# CC task P??: Eodon climbing vines: no climbing while paralyzed, frozen or casting

**Model:** Sonnet
**Touches:** server
**Golem:** any

**Summary:** ClimbingVine.OnDoubleClick teleports a player 40-60 tiles up the Barako cliff with no check on
paralysis, freezing or a spell in progress (a ServUO hole carried over by P198). A paralyzed player escapes a fight
with one double-click.

Found by cc-P428 (Crystal's review of the 10-22 merges), finding 2.

## What to do

1. `server/customizations/Services/Expansions/Time Of Legends/Items/ClimbingVine.cs:33-42`: before the move, refuse
   when `from.Paralyzed || from.Frozen || from.Spell != null` with "You cannot climb right now." (a cliloc if one
   fits; check `Data/Localization` on the game PC, otherwise plain text). Keep ServUO's message and range.
2. Tests (`EodonRemainderVerification.cs`, next to the existing vine facts): a paralyzed player and a frozen player
   double-clicking in range stay where they are; a free one climbs. Red first.
3. Build and run the tests (`docker\uo\build.sh -t sl-modernuo:cc-P??`).
4. On the test shard (game PC): after [GenEodon, check that the clifftop at 679,1757,100 has a walking way down.
   If it has none, say so in the notes. Do not add a down-vine in this prompt.
5. CHANGELOG: a Fixed line ("The Eodon cliff vines can no longer be climbed while paralyzed.").
6. Notes: `notes\cc-P??-eodon-vine-paralysis.md`. Last line `P?? DONE`.

**Done means:** a paralyzed, frozen or casting player cannot climb, and the test shows it.
```

### 3. The 10-22 merges' patch notes sit under yesterday's version (cosmetic, or wrong behavior if .24 already ran)

- **Where:** `CHANGELOG.md:32-49` and `VERSION` (`2026.10.21.24`).
- **What goes wrong:** P368's merge (`222f0b8`, 10-21 22:05) made `2026.10.21.24`. P354 (`b240bb4`, 10-22 00:14) and
  P380 (`1ecd9f3`, 10-22 04:03) each had their own section (`2026.10.21.8` and `2026.10.21.21` on their branches).
  When they were settled against main, their lines went into the existing .24 section, and VERSION stayed at .24 (git
  `--remerge-diff` of `9a41c24` and `044af6c`, the branches' own main merges). The file's rule (`CHANGELOG.md:6-7`) is
  one section per update, with a second update on the same day getting the next number. The login bulletin shows each
  account the notes once per version (`ShardVersion.cs:12, :314-323`, `bulletin.seenVersion`).
- **How it is hit:** if any server (live or test) ran a .24 build from `222f0b8` and a player logged in, that account
  has `seenVersion = 2026.10.21.24`. When the Eodon and stump build comes in, the bulletin does not show again, and
  the player never sees those lines in game. If no server ran .24 before the 10-22 merges, nobody misses anything, and
  this is only a 10-22 change dated 10-21. P406's package notes say the last player package before 10-22 was
  `2026.10.21.0825`, which suggests .24 never reached live. I cannot confirm that from GitHub.
- **Needs a server?** Yes for which build live and test ran. That is on the game PC (deploy log, `status.json`
  history).

**Prompt draft:**

```
# CC task P??: give the 10-22 Eodon and stump patch notes their own version

**Model:** Sonnet
**Touches:** docs-only
**Golem:** home (needs the deploy history)

**Summary:** P354 and P380 merged on 10-22 into CHANGELOG's existing 2026.10.21.24 section without a new version,
so the once-per-version login bulletin will not show their lines to anyone who already saw .24.

Found by cc-P428 (Crystal's review of the 10-22 merges), finding 3.

## What to do

1. Check whether live or the test shard ever ran VERSION 2026.10.21.24 before b240bb4 (deploy log, status.json, the
   `[version` line in the server log). If neither did, stop: write that in the notes and change nothing.
2. If one did: move the Eodon lines (Added 5, Staff 2) and the stump lines (Added 1, Staff 1) out of
   2026.10.21.24 into a new top section, 2026.10.22 (or the next free 2026.10.22.n if a 10-22 version exists by
   then), and set VERSION to match. Keep every line word for word. Settle against whatever main has by then.
3. Check that the server's parse still reads it: the ShardVersion tests (`server/tests`, the CHANGELOG parse facts)
   and `scripts/Publish-PatchNotes.ps1 -WhatIf` if it has one.
4. Notes: `notes\cc-P??-changelog-10-22-version.md`. Last line `P?? DONE`.

**Done means:** either the notes say .24 never ran anywhere, or the 10-22 lines have their own version and VERSION
matches.
```

## What I checked and found clean

**Range.** The last 10-21 version in `CHANGELOG.md` is `2026.10.21.24`. It came in with P368's merge `222f0b8`
(10-21 22:05 CDT), the last first-parent merge of 10-21. I reviewed `222f0b8..da1a0cb` (head, P274's merge) for
`server/`, `client/patches/` and `docker/uo/`. That is 21 files and about 3,100 lines, all from P354 (17 files) and
P380 (4 files). `client/patches/` did not change. P274 changed only `scripts/Shard-Console.ps1`, its test and
`web-console/static/app.js` (the Fable bar's fallback and the projection label). I read it and it is outside this
prompt's folders. P408, P289 (`golem/Iron/P289` and `golem/Valorite/P289` are on origin) and P410 were not in main.

The range between P379's head (`47b3eae`) and this one (P371, P266, P364, P368 on 10-21) belongs to neither review.
Codex covered P368 (P403) and P364 (P404). P371 and P266 have only their pre-merge Codex reviews (`notes/cc-P371-*-codex-review.md`, `notes/cc-P266-*-codex-review.md`), no review after the merge.

**Merges.** None of the three main merges hand-settled anything (`--remerge-diff` is empty). The fix-up branches'
own merges of main did:
- P354's `9a41c24`: CHANGELOG and VERSION (see finding 3). No code conflict.
- P380's `044af6c`: CHANGELOG, VERSION, and `docker/uo/apply-patches.sh`. In apply-patches, P371's three
  tutorial-island patches and P359's `HarvestBank-lumber-stumps.patch` are both kept, in that order (`:862-870`).
  Every line both sides added to CHANGELOG is in today's file once.

**Stumps (P359/P380):** `ClusterFLumberStumps.cs`, the HarvestBank patch, the `partial` sed on Lumberjacking
(`apply-patches.sh:888-894`), and the test. These were read against pinned `HarvestSystem.cs:104-250` and
`HarvestBank.cs`.
- The marker is made only when the targeted tree's own bank is below a full harvest (`:19-21`, `:53-55`).
- Its timer uses the bank's first-chop deadline. The refill hook runs only after a real refill. Deleting the stump
  forgets the bank, and stumps skip saves (pinned `GenericEntityPersistence.cs:256, :289`).
- Felucca's double harvest and the elf discount do not change the threshold or the deadline.
- No other `OnHarvestFinished` override exists on Lumberjacking (Mining has its own, `server/patches/Mining.cs:388`).
- The one known bug is the raised Z (P412).

**Eodon (P198/P354):**
- `EodonGeneration`: a rerun deletes the tagged earlier run first. Pinned's `BaseSpawner.OnDelete` removes the
  spawns, so a rerun does not double the creatures. `WeakEntityCollection` is saved (`Misc/WeakEntityCollection.cs:183`).
  The gate skip and the dry run do what they say, and the console verb posts to the game loop.
- An operational note, not a finding: pinned's `[MoonGen` (Developer) deletes every `PublicMoongate` in the world
  (`PublicMoongate.cs:101-137`), so it would take the Eodon gate with it, as it already does the Royal City one. The
  start-up `[Eodon]` status line would then say MISSING.
- `EodonSpawns`: the 46 rows compile to pinned `Spawner`. The tribe parameter is parsed by pinned's ctor matching
  (`BaseSpawner.cs:1024-1047`). The Barako rows' z band works with `GetSpawnPosition` (min 100, max 110), and if no
  spot fits it falls back to the spawner's own z 100. "Eodon_BarakoTribe #4" is used as a name twice, as in ServUO;
  only `IsEodonSpawner` reads names, and it does not care. The entry weights are Codex P407's finding 1 (P429).
- Tribesmen:
  - `_tribeType` is set before `BuildBody`/`BuildEquipment` run from the base ctor, so the switches see the right
    tribe.
  - The join-in sets `Combatant`. Pinned `MeleeAI.DoActionCombat` does not re-check `IsEnemy`, so the joiners keep
    fighting.
  - Blessed weapons go with the creature, not the corpse, as in ServUO.
- Infernus fire: serialized base, deleted on load, and its timer is cancelled on delete. ServUO's "centre is not
  guaranteed" quirk is kept on purpose and written in the header (`Infernus.cs:88`).
- Cards, scute, shaman, infantry, phoenix, anchisaur, gallusaurus, scorpion: values match their headers. Every saved
  type uses the generator at version 0, and no saved class from before the range changed shape.

**Settings and commands:** `clusterf.lumber.stumps` and `clusterf.lumber.stumpItemId` are read with
`GetOrUpdateSetting` in `Configure`. `GenEodon` and `DeleteEodon` are new names and clash with no other command.

## What I could not check from GitHub alone

- Nothing was built and no test was run. The findings come from reading the code, and each draft asks for a red test
  first.
- Which VERSION live and the test shard ran between 10-21 22:05 and the 10-22 merges (finding 3).
- The Ter Mur map around the vines: whether the Barako clifftop has a walking way down, and whether 100-110 is the
  clifftop's real z for every Barako spawner. Both need the map files on the game PC.
- Whether the card pictures (gumps 39904-39914) and the hatchling body 1294 are in the player package's client
  files. P198's notes say they were checked on the game PC.

P428 DONE
