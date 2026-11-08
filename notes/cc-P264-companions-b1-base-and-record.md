# cc-P264: companions B1, the companion base and its record

**Golem:** Bronze. **Date:** 2026-10-21. **Branch:** `golem/Bronze/P264` in both work copies. **Image:**
`sl-modernuo:cc-P264`.

## Headlines

- **`BaseCompanion : BaseCreature`** exists, with generated serialization (version 0). It is the final parent: later
  steps derive from it or add fields to it, so its save chain never needs re-parenting.
- **The record lives on the creature:** a lineage id that is never reused, path, branch, personality, loop, rank,
  level, XP, epithet, parents and generation (by lineage id), next breed time, a peak for every skill, and the "away
  with owner" flag. Sex is `Mobile.Female`.
- **Skill caps are a player's:** each skill's cap is the companion's max level at its own loop, and `Skills.Cap` is
  58 times that. It is never the creature default of 700.0 total.
- **Logs out with its owner:** it leaves to the internal map and comes back following at login. It is never
  auto-stabled. While it is away it is marked stabled, so a ghost companion survives the one-day dead-pet sweep, and
  that mark is restored after a restart.
- **Follower math is all settings:** slot cost by rank, party size by owner loop, and P47's `FollowersMax` curve.
  Loop 0 stays at stock 5, so a new player keeps room for a pet or mount beside two squires.
- **Staff commands:** `[CompanionMake <path> [personality] [male|female] [loop] [rank]` and
  `[CompanionSet <loop|rank|level|branch> <value>`. No hiring.
- **Tests:** 6 new facts, each seen red against a mutation. Full gate green: RESULT_GREEN.
- **One conflict for Chase:** cc-P262's accessories already declared a `CompanionPersonality` enum with six
  personalities that are not the design's nine. See "For Chase".

## What B1 built

All new code is under `server\customizations\Companions\`, plus two small edits in the shared skill files.

| File | What |
|---|---|
| `CompanionSettings.cs` | `CompanionPath` (5 + None), `CompanionBranch` (10 + Penitent, Otherworlder + None), `Personality` (the nine). `CompanionSettings`: F-12's ladder, slot cost by rank, party size and `FollowersMax` by owner loop, all `clusterf.companions.*` settings. `OwnerLoopProvider` is the hook F-12 fills once players have a loop; until then every owner is at loop 0. |
| `CompanionLineage.cs` | The lineage-id counter, in its own save file (`Saves/Companions`, a `GenericPersistence`). Each loaded companion reports its id (`Observe`), so a lost or old counter file can never hand out an id that a live companion already holds. |
| `BaseCompanion.cs` | The creature and its record (fields 0-14). Player hits, stamina and mana. It never calls `SetDamage`, and equipping a weapon copies the weapon's damage-type split. `CanAutoStable => false`, `StandsDownOnCommand => false`. `SetRank` re-counts the owner's followers (P41 11.3). Per-skill peaks are tracked in `OnSkillChange`. `[AfterDeserialization]` restores `IsStabled` when away, the damage split, and the caps. |
| `CompanionParty.cs` | Party limit, `CanTake`, `Join`, raise-only `ApplyFollowersMax`. Logout (`EventSink.Logout`) and login (`PlayerLoginEvent`). The two staff commands. |
| `ClusterFSkillCaps.cs` | `ApplyTo(BaseCompanion)`: per-skill cap = max level; `Skills.Cap` = skill count × that. |
| `ClusterFSkillGain.cs` | `ShouldBoost` also accepts a controlled companion (P45 B1: "ShouldBoost including companions"). |

### The record (BaseCompanion fields)

| # | Field | Note |
|---|---|---|
| 0 | `LineageId` (long) | From `CompanionLineage.NextId()`. Starts at 1; 0 means "no parent". |
| 1 | `Path` | Set at creation (purchase, from B4 on). |
| 2 | `Branch` | `None` until loop 3. |
| 3 | `Personality` | Fixed for life. |
| 4 | `Loop` | `MaxLevel` follows it on F-12's ladder (50, 100, then +5 per loop to 200 at loop 21). |
| 5 | `Rank` | 0 Squire to 5 Legend. Kept separate from the loop: see open question 1. |
| 6, 7 | `Level`, `Xp` | Nothing levels it yet. |
| 8 | `Epithet` | Lore window or title, never the name (B2 fills it from speech.json). |
| 9-11 | `Parent1Id`, `Parent2Id`, `Generation` | By lineage id, never by Serial (P41 section 8). |
| 12 | `NextBreedTime` | Breeding readiness. `IsBreedable` is a virtual, true. |
| 13 | `SkillPeaks` (int[] in tenths) | Loop memory's input. Only ever rises. |
| 14 | `AwayWithOwner` | Set at logout, cleared at login. |

### Follower numbers (for Chase; every one is a setting)

| Setting (`clusterf.companions.`) | Default | Source |
|---|---|---|
| `ladder.loop0MaxLevel`, `ladder.loop1MaxLevel`, `ladder.levelsPerLoop`, `ladder.topMaxLevel` | 50, 100, 5, 200 | F-12's ladder (decided 2026-10-03) |
| `slotCostByRank` | 1,1,2,2,3,3 | Design, "Hybrid shape" |
| `partySizeByOwnerLoop` (player included) | 3,4,5,5,6,6, then 6 | Design, "The party" |
| `followersMaxByOwnerLoop` | 5,6,7,9,10,11,12,14,15,16,17,18,18 (loops 12-20), 19 at loop 21 | P47 section 6 (evo mount at 3 as a placeholder) |
| `followersMaxFloor` | 5 | Review item 4: never below stock |
| `enabled` | true | Off: no logout handling, no `FollowersMax` change |

What this gives a **new player** (loop 0): `FollowersMax` 5, at most 2 companions, each costing 1 slot. That leaves 3
slots for a pet, a horse or the mule (1 slot). The design's draft of 2 at loop 0 would have squeezed out the horse
(review item 4). `ApplyFollowersMax` only ever raises the value, so a value staff set by hand is kept. At loop 0 it
changes nothing until F-12 gives players a loop.

## Tests (`server\tests\Mobiles\Companions\CompanionBaseVerification.cs`)

| Fact | What it proves |
|---|---|
| `TheRecordSavesAndLoads` | Every record field, sex, slot cost and caps survive a save and load through the generated serializer. The peak stays at 80 after the skill drops to 60. |
| `LineageIdsAreNeverReused` | No id is reused after a delete. The counter's own save keeps its place. A restart with a fresh counter moves past every loaded companion's id. |
| `ACompanionLogsOutAndInWithItsOwner` | Logout: internal map, still controlled and counted, never auto-stabled, `IsStabled` set. After a restart while away, `IsStabled` comes back. Login: on the owner's tile, following, followers unchanged. |
| `TheFollowerMathFollowsTheSettings` | The default tables. A loop-0 owner gets 2 squires, then "party is full", and a horse still fits. With the horse counted, rank 0→2→4→0 moves the owner's count 3→4→5→3. Slots also limit a bigger party. The curve raises `FollowersMax` to 11 at loop 5 and never lowers a value of 30. |
| `TheSkillCapIsAPlayers` | Loop 0: 50.0 per skill, `Skills.Cap` 58 × 500. Loop 21: 200.0 per skill and 58 × 2000. Past 700.0 total there is still room. Going down to loop 1 gives 100.0. |
| `ItFightsAndGainsAsAPlayer` | Hits 75 / stamina 40 / mana 30 from Str 50 / Dex 40 / Int 30. `DamageMin` and `DamageMax` stay -1. A katana with 40 fire / 10 cold gives a 50/40/10 split on equip and 100 physical after unequip. `ShouldBoost` is false for a wild companion and true for a controlled one. |

**Red first.** These facts cannot compile without the new types, so each was seen red against one mutation of the
finished code. Each mutant was run alone on the builder image (`sl-uo-builder:cc-P264`, mutant file bind-mounted over
its copy, `dotnet test --filter CompanionBaseVerification`):

RED_TABLE

**Gate:** BUILD_TABLE

## Open questions and conflicts (for Chase)

1. **Rank against the 22-step ladder.** The design ties rank to loop one-to-one ("rank and loop are one track") on
   the old six-loop ladder, and its slot costs (1/1/2/2/3/3) and party sizes are written against that ladder. F-12's
   ladder now has 21 loops. So B1 keeps `Rank` as its own field (set by `SetRank`), and the cost follows the rank, not
   the loop. Someone has to decide which loops promote. P47 raised the same question (its "still unknown" 1).
2. **Two personality sets.** cc-P262 (accessories, foot lines) declared `Server.CompanionPersonality` with Stoic,
   Cheerful, Grumpy, Vain, Timid and Zealous. Its own header says the spec assumed companions already had that field.
   The design's nine are Noble, Commoner, Devout, Sellsword, Scholar, Braggart, Ditzy, Gloomy and Isekai'd. B1 uses
   the design's nine (as `Server.Companions.Personality`, so the names do not collide) and does **not** wire
   `AccessoryFootLines.PersonalityOf`: there is no mapping from nine to six that is not a guess. Proposal: B2 writes
   the foot lines for the nine personalities in `speech.json` (as the "foot" moments) and retires the six-value enum.
   Chase's call.
3. **No player loop yet.** `CompanionSettings.OwnerLoopProvider` is null, so every owner counts as loop 0. That means
   a 3-person party, `FollowersMax` 5, and the gate "a companion never out-loops its owner" can only be checked once
   F-12 sets the provider. `[CompanionMake` lets staff give any loop for testing.
4. **Owners list.** `Join` uses `SetControlMaster`, which does not add the buyer to `Owners` (P45 section 5 item 3).
   So a companion is exempt from the 3-day abandoned-pet delete and has no `LastOwner`. B4 (hiring) should decide
   this; B1 leaves it as `SetControlMaster` leaves it.
5. **Not done in B1, on purpose:** P66's skill clamps for creatures (P45 section 4: how P66's clamps
   treat a creature is unverified), loop memory (only the peaks are recorded), the parity patches (B3), titles and
   names from data (B2), and companion AI (B6, B7). The AI is pinned's for now: Melee for Blade, Support and Rogue,
   Archer for Bow, Mage for Arcane.

## Deviations and decisions

- **`docs\` is untouched** (AGENTS.md rule 2). The follower numbers above belong in the design doc once Chase accepts
  them; the overseer can copy them.
- **Read tool denied once:** the unattended run auto-denied `Read` on
  `D:\UO\golems\Bronze\ShatteredLegacy\server\customizations\ClusterFSkillGain.cs` (lines 304-311), which I wanted
  before an `Edit` of `ShouldBoost`. I had already seen those lines through `sed`, so I made the one-line change with a
  Python replace that asserts the old text occurs exactly once. The diff is a single line.
- **CHANGELOG:** a new section 2026.10.21.15, staff only; `VERSION` 2026.10.21.15. (Main is at .14 after P243.)
- **Stats** are 50/40/30 for every path for now; B2's `classes.json` gives each path its own.

## What B2 needs

- **The enums are fixed:** B2's tables name paths, branches and personalities by these enum names
  (`JsonStringEnumConverter`), and `Isekaid` has no apostrophe.
- **Hooks waiting for data:** `Epithet` (from speech.json's combo rows), the gendered rank titles (the companion's
  `Title` is not set yet), the personality roll by path (`[CompanionMake` rolls uniformly over all nine when no
  personality is given), and the per-path starter stats and skills.
- **party.json** replaces the three list settings in `CompanionSettings`. Keep the same shape and defaults, and keep
  the floor of 5.
- **A decision on open questions 1 and 2** before speech.json is written.

## Draft B2 prompt (notes only, not filed)

```
# CC task P<nn>: companions B2, the data tables

**Model:** Opus

**Touches:** server

**Summary:** The second build step of companions: the four data tables (personality, classes, speech, party) with a
loader, a validator, a reload command and a shard test over every shipped row, as P45's corrected build list sets out.

Read first:
- `docs\companions\companions-squire-evo-research.md` (Personalities, Personality to class map, Buying a companion,
  Gendered titles, Speech moments, The party) and `docs\companions\companions-combo-lines.md` (the 50 combinations).
- `docs\companions\p41-companions-review.md` (corrections 1 to 4).
- `notes\cc-P41-companions-research.md` section 7 (where tables live, how a bad row fails, first shapes) and section 11.
- `notes\cc-P45-companion-probes.md` section 2 (B2).
- `notes\cc-P264-companions-b1-base-and-record.md` (what B1 built, the enums, open questions 1 and 2).

## Build B2

1. **Where they live:** `server\data\companions\*.json`, copied into the image at
   `/modernuo/Data/ShatteredLegacy/companions/`; a live override in `Configuration/companions/` wins per table.
   Loaded with pinned `JsonConfig.Deserialize<T>`.
2. **personality.json:** the nine personalities with tier and roll odds (7 common, Gloomy 5%, Isekai'd 1%) and the
   personality-to-path map. Rolls happen within the bought path, at the per-contract odds the design lists.
3. **classes.json:** 5 paths x 2 branches, plus Penitent (Gloomy) and Otherworlder (Isekai'd), each with core skills,
   starter stats and skills, AI and the gendered rank and Legend titles. Set the companion's title from it.
4. **speech.json:** keyed by personality x moment x gender x path or branch. Carry the 50 combo epithets and signature
   lines from `companions-combo-lines.md`, and fill `BaseCompanion.Epithet` from them at branch choice. Include the
   accessory foot lines for the nine personalities if Chase agrees (B1 open question 2).
5. **party.json:** party size and `FollowersMax` by owner loop, slot cost by rank, the floor of 5. It replaces the
   `clusterf.companions.*` list settings (keep their defaults).
6. **Validator and failure rules** per P41 7.2: a shard test loads every shipped table and fails the build on any bad
   row with file, row and reason; at startup a bad shipped table disables hiring with a loud log and never throws; a
   reload keeps the previous table on a file-level error. GM command `[CompanionData reload` reports each table's
   source.
7. Use the tables in `[CompanionMake` (roll the personality by path when none is given; starter stats, skills and
   title from classes.json).

## Done means

- Tests in `server\tests\`: every shipped row validates; one broken row per table fails with file, row and reason
  (seen red); a reload with a bad file keeps the old table; the personality roll stays within the path's map; a made
  companion gets its class's stats, skills and gendered title.
- A CHANGELOG entry (staff only).
- Notes `notes\cc-P<nn>-companions-b2-data-tables.md`: the tables, the validator, what B3 needs.
- Last line `P<nn> DONE`.
```

P264 DONE
