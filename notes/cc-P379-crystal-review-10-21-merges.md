# cc-P379: a read-only code review of the 10-21 server merges

**Golem:** Crystal (cloud). **Date:** 2026-10-21. **Branch:** `golem/Crystal/P379` (shard-migration only; no code changed).

## In plain words

- Nothing serious: no crash, no broken save, no merge that lost or doubled code. Every hand-settled CHANGELOG, VERSION
  and code conflict in the range kept both sides.
- Two real gameplay bugs came in today:
  1. Levelable gear earns XP for killing someone's pet. The code says pets pay nothing, but by the time the death event
     runs, the game has already wiped the pet's owner, so it looks like a wild creature. The test checks this by
     calling the XP code on a live pet, so it cannot catch the bug.
  2. The "orders take only crafted items" rule from today's patch notes misses fletching, carpentry and tinkering bulk
     orders. A bow, staff or cleaver bought from a shopkeeper still fills them.
- Two small ones: a hidden joke achievement ("Geography Major") is also granted when a monster did hit you, if you
  healed to full before you killed it; and a small memory leak in the same file.
- The art registry has no duplicate or reused IDs. One older row (10-17) has the wrong hex next to its ID, which is
  cosmetic.
- Everything below was checked by reading code, mine and pinned ModernUO's (commit `d4531cd`). Nothing was built or
  run: a cloud Golem cannot build the shard. Where a finding needs a real server or client, it says so.

## Findings (most severe first)

### 1. Levelable gear gains XP from a player's pet's death (wrong behavior)

- **Where:** `server/customizations/LevelGear/ClusterFLevelGear.cs:455-472` (`OnCreatureDeath`, then the check in
  `AwardDeath`).
- **What goes wrong:** `AwardDeath` refuses a creature that is `Controlled`, `Summoned`, `NoKillAwards` or has a
  player master. That is the P261 rule ("No XP from a controlled or summoned creature, one whose master is a player",
  `notes/cc-P261-levelable-gear-build.md`). But it runs from `CreatureDeathEvent`, and in pinned a non-bonded creature
  is deleted before that event:
  - `BaseCreature.OnDeath` calls `base.OnDeath(c)` and only then `CreatureEvents.CreatureDeathEvent(this)`
    (pinned `Projects/UOContent/Mobiles/BaseCreature.cs:3662-3669`).
  - `Mobile.OnDeath` deletes every non-player: `if (!m_Player) { Delete(); return; }`
    (pinned `Projects/Server/Mobiles/Mobile.cs:4899-4902`).
  - `BaseCreature.OnDelete` runs `SetControlMaster(null)` (pinned `BaseCreature.cs:3687-3688`), so `Controlled` is
    false and `GetMaster()` (`ControlMaster ?? SummonMaster`, `:3333`) is null by the time we look.
  - The damage list survives (only full HP or the 2-minute expiry clears it, pinned `Mobile.cs:2043`, `:55-59`), so the
    pool is paid out as for a wild creature.
  - P263 found exactly this and moved its own handler to `CreatureDeletedEvent`
    (`ClusterFNotedBySystem.cs:575-580`, the comment block). P261, which merged the same day through P285, did not.
- **How it is hit:** anyone wearing levelable gear who kills or helps kill a tamed, non-bonded pet. Two players can do
  it on purpose: one buys tame animals from an animal trainer (or tames them), the other kills them for XP without
  any risk. A Felucca pet kill pays too. Summons stay excluded (the `Summoned` field is not cleared on delete), and a
  bonded pet's death goes through the other `CreatureDeathEvent` at `BaseCreature.cs:3540` while still controlled, so
  it pays nothing, as intended.
- **Test that cannot fail:** `server/tests/Misc/LevelGearVerification.cs:234-238` ("A pet's death pays nothing") calls
  `ClusterFLevelGear.AwardDeath(tame, 1000)` on a live, still-controlled horse. It never goes through `Kill()`, so it
  passes whatever the event handler does. The orc case just above it (`:223-231`) does use `Kill()`, which is the shape
  the pet case needs.
- **Needs a server?** No for the logic (pinned's order is plain in the code). A test with `tame.Kill()` would prove it
  in the test host.

**Prompt draft:**

```
# CC task P??: levelable gear: no XP from a pet's death (the real death path)

**Model:** Opus
**Touches:** server
**Golem:** any

**Summary:** P261's rule says a pet's death pays no item XP, but ClusterFLevelGear reads Controlled at
CreatureDeathEvent, after pinned's OnDelete has cleared the master. A killed non-bonded pet pays like a wild creature.
Fix the check and make the test go through a real Kill().

Found by cc-P379 (Crystal's review of the 10-21 merges), finding 1.

## What to do

1. `server/customizations/LevelGear/ClusterFLevelGear.cs:455-472`: a non-bonded creature is deleted (and its master
   cleared, pinned BaseCreature.OnDelete) before CreatureDeathEvent. Decide where to read "was it a pet": move the
   award to CreatureDeletedEvent with P263's guard (`bc.Hits <= 0 && !bc.IsDeadPet`, ClusterFNotedBySystem.cs:582-587,
   where the master and the damage list are still there), or record the master on the way in. Keep a bonded pet's
   death (BaseCreature.cs:3540, still controlled) paying nothing.
2. `server/tests/Misc/LevelGearVerification.cs:234-238`: replace the direct AwardDeath call with a real death: a
   controlled, non-bonded horse damaged by the wearer, then `tame.Kill()`, and assert the sword's XP did not move. Show
   it red against today's code first. Add the same for a summoned creature.
3. Build and run the tests (`docker\uo\build.sh -t sl-modernuo:cc-P??`).
4. CHANGELOG: a Fixed line ("Levelable gear no longer gains experience from killing pets.").
5. Notes: `notes\cc-P??-level-gear-pet-death-xp.md`. Last line `P?? DONE`.
```

### 2. Fletching, carpentry and tinkering bulk orders still take store-bought items (wrong behavior)

- **Where:** `server/customizations/Services/BulkOrders/CraftBOD.cs:195-253` (`EndCombineSmall`), reached from
  `SmallFletchingBOD.cs:45-46`, `SmallCarpentryBOD.cs:44-45` and `SmallTinkerBOD.cs:156`.
- **What goes wrong:** P263 made orders take only player-crafted items, and today's patch notes promise it for every
  bulk order: "Bulk orders and smith commissions take only items a player crafted. Items bought from a shopkeeper (or
  found as loot) no longer fill them." (`CHANGELOG.md:104`, version 2026.10.21.11). The rule was put in three places:
  pinned's `SmallBOD.EndCombine` (`server/patches/SmallBOD-crafted-only.patch`), `LargeBODItemFill.cs:68-72` and the
  smith commissions. The six ported craft deeds (cc BOD part 2) override `EndCombine` and go through
  `CraftBOD.EndCombineSmall`, which checks type, material and exceptional only. It never asks
  `ClusterFStoreBought.Refuses`.
- **How it is hit:** the deeds ask for weapons pinned's shopkeepers sell:
  - Fletching: Bow, Crossbow, HeavyCrossbow (`CraftBulkEntries.cs:336-345`), sold by pinned's `SBRangedWeapon`,
    `SBWeaponSmith`, `SBBlacksmith`.
  - Carpentry: GnarledStaff, QuarterStaff, ShepherdsCrook (`CraftBulkEntries.cs:109-120`), sold by `SBStavesWeapon`,
    `SBWeaponSmith`.
  - Tinkering: Cleaver (`CraftBulkEntries.cs:638`), sold by `SBButcher`, `SBKnifeWeapon`.

  A plain deed (no material, not exceptional) is filled straight from a shop. That is the exploit P263 closed for
  smithing and tailoring. The BOD-combine-from-container path (`BODCombineContained.cs:84`) calls the same
  `EndCombine`, so it bypasses the rule too. Alchemy, cooking and inscription items are not armor, weapons or clothing,
  so the rule does not apply to them anyway.
- **Needs a server?** No. Whether the shard's vendors really stock those types depends on pinned's SBInfo lists, which
  I read at the pinned commit; the shard does not override them.

**Prompt draft:**

```
# CC task P??: the crafted-only rule for the ported craft bulk orders (fletching, carpentry, tinkering)

**Model:** Sonnet
**Touches:** server
**Golem:** any

**Summary:** P263's Store-Bought fix (orders take only player-crafted items) covers pinned's small deed, the large
smith deed's item fill and the commissions, but not CraftBOD.EndCombineSmall, which the fletching, carpentry and
tinkering deeds use. A shop-bought bow, staff or cleaver still fills them, against the 2026.10.21.11 patch notes.

Found by cc-P379 (Crystal's review of the 10-21 merges), finding 2.

## What to do

1. `server/customizations/Services/BulkOrders/CraftBOD.cs`, `EndCombineSmall` (:195): after the type check, refuse
   `ClusterFStoreBought.Refuses(item)` with `ClusterFStoreBought.Refusal`, as `LargeBODItemFill.cs:68-72` does.
   Check whether `EndCombineLarge` takes items directly; if it does, the same.
2. Tests: a store-bought (not PlayerConstructed) Bow refused by a SmallFletchingBOD, a QuarterStaff by a
   SmallCarpentryBOD, a Cleaver by a SmallTinkerBOD; the crafted ones accepted; `clusterf.bods.craftedOnly` false lets
   them in. Existing CraftBOD tests that fill deeds with uncrafted items will go red (P263 hit 40 of these on the smith
   side); mark their items crafted, as P263 did.
3. Build and run the tests (`docker\uo\build.sh -t sl-modernuo:cc-P??`).
4. CHANGELOG: no new line needed if the .11 line already says "bulk orders"; otherwise a Fixed line.
5. Notes: `notes\cc-P??-craft-bod-crafted-only.md`. Last line `P?? DONE`.
```

### 3. "Geography Major" / "Rock Enthusiast" granted when the creature did reach you (wrong behavior, minor)

- **Where:** `server/customizations/ClusterFNotedBySystem.cs:609-610`.
- **What goes wrong:** "a melee creature you killed that never damaged you" is tested as
  `pm.FindDamageEntryFor(bc) == null`, the player's own damage list. In pinned that list is emptied whenever the
  player's hits reach full (`Mobile.cs:2043`, "reset damage entries on full HP"), and each entry expires 2 minutes after
  its last hit (`Mobile.cs:55-59`).
- **How it is hit:** an orc hits you, you bandage or regenerate to full, then you kill it. You get the hidden
  achievement (5 AP, 1 Renown) and progress toward Rock Enthusiast (50 kills, 15 AP), with no terrain trick at all.
  For a tank who heals to full during a fight this happens all the time.
- **Needs a server?** No for the logic. The fix needs its own memory of "this creature damaged this player" (for
  example AggressiveAction, or a damage hook), and a test that heals to full before the kill.

**Prompt draft:**

```
# CC task P??: Noted by the System: "never reached you" survives a heal to full

**Model:** Sonnet
**Touches:** server
**Golem:** any

**Summary:** ClusterFNotedBySystem decides "the melee creature never reached you" from the player's damage list,
which pinned empties at full HP and expires after 2 minutes. A creature that hit you before you healed to full counts
as never reaching you, so Geography Major and Rock Enthusiast are granted for ordinary fights.

Found by cc-P379 (Crystal's review of the 10-21 merges), finding 3.

## What to do

1. `server/customizations/ClusterFNotedBySystem.cs:609-610`: keep a per-creature record of the players it damaged
   (from a damage event the shard already hooks, or a small dictionary filled where the creature deals damage and
   cleared on its death or deletion), and test that instead of `pm.FindDamageEntryFor(bc)`.
2. Test in `server/tests/Misc/NotedBySystemVerification.cs`: an orc damages the player, the player is healed to full,
   the player kills the orc: no NeverReachedKills count. Show it red first.
3. Build and run the tests (`docker\uo\build.sh -t sl-modernuo:cc-P??`).
4. Notes: `notes\cc-P??-noted-never-reached-heal.md`. Last line `P?? DONE`.
```

### 4. Released pets are never removed from a static dictionary (cosmetic: memory only)

- **Where:** `server/customizations/ClusterFNotedBySystem.cs:647-661`.
- **What goes wrong:** `Released` adds every released pet to `_released` (keyed by the `BaseCreature`). Only `Tamed`
  removes it. A released pet that is deleted (pinned deletes many on release) or dies stays in the dictionary, and
  the deleted creature with it, until the next restart.
- **How it is hit:** every [release of a pet that is not tamed back. It only grows memory between restarts; no player
  sees it. The other per-player dictionaries in that file (`_steps`, `_recalls` and the rest) are keyed by player
  mobiles, so they are bounded by the number of characters, which is fine.
- **Needs a server?** No.

**Prompt draft:**

```
# CC task P??: Noted by the System: forget released pets that are gone

**Model:** Sonnet
**Touches:** server
**Golem:** any

**Summary:** ClusterFNotedBySystem._released keeps every released pet until it is tamed again, deleted ones included,
so it grows for as long as the server runs. Prune it.

Found by cc-P379 (Crystal's review of the 10-21 merges), finding 4.

## What to do

1. `server/customizations/ClusterFNotedBySystem.cs:647-661`: remove the creature from `_released` in
   `OnCreatureDeleted` (the CreatureDeletedEvent handler is already there, :582), and drop entries older than
   `RetameWindow` when adding one.
2. A test: release a pet, delete it, and the dictionary no longer holds it (expose a count for tests).
3. Build and run the tests (`docker\uo\build.sh -t sl-modernuo:cc-P??`).
4. Notes: `notes\cc-P??-noted-released-prune.md`. Last line `P?? DONE`.
```

### 5. Art registry: one row's hex is wrong (cosmetic, older than the range)

- **Where:** `player-package/vendor/shattered-legacy-art/registry.csv:55`: `54783,0xD5EF,...` (the kitsune ears' male
  paperdoll gump, cc-P138 on 10-17). 54783 is `0xD5FF`; `0xD5EF` is 54767.
- **Effect:** none in the tools I found. `scripts/find-free-art.py` and the tests key on the decimal `id` column.
  A person reading the hex column would look in the wrong place.
- **No prompt needed.** One character; it can ride along with the next registry change.

## What I checked and found clean

**Range.** The prompt calls 2026.10.21.10 the first 10-21 version, but it is not: `CHANGELOG.md` has 2026.10.21 and
.2 to .9 before it. I reviewed what the prompt asked for: from the commit before .10 to the head, `e8f4b92..47b3eae`
(`ebc7b9e`, Merge P286, brought in .10; head is the P280 merge, 2026.10.21.20). That covers 145 files under `server/`
and `docker/uo/`, about 21,700 lines added. Versions .1 to .9 (P228, P196, P177, P229, P272, P230, P231, P278, P237,
P159, P215, P239, P284, P197) were not reviewed.

**P372 is not in main.** It is still in the queue (`cc-P372-cont-fixup-hammer-t3-craft-order.md`), and neither
`golem/Copper/P168` nor a P372 branch is on the code repo's origin, so there was nothing of it to review.

**Hand-settled merges** (git `--remerge-diff`, which shows exactly what the person merging changed against git's own
merge):
- **P361 (P263 Noted by the System onto main with P262 accessory slots and P243):** both sides kept everywhere.
  `TriggerKind` keeps P262's four values and then P263's (`ClusterFAchievements.cs:83-121`). That is safe: the enum
  is never saved (achievements are saved by key), and P262's values kept the numbers they had on main. Both
  `RegisterAccessories()` and `RegisterNoted()` are called (`:1217-1218`). `TitleDef`'s two spellings of the same flag
  (`Secret` from P263, `HiddenUntilHeld` from P262) became one, `HiddenUntilHeld`. No `.Secret` reference is left, and
  the title gump's count and list loops both use it (`LeagueShopGumps.cs:381, :407`). The counts in tests are right:
  100 + 45 = 145 definitions, 45 + 5 = 50 with the `noted.` prefix (P262's keys use it). `apply-patches.sh` keeps
  P262's, P261's and P263's blocks.
- **P285 (P261 levelable gear), P355 (P262), P271 (P195 Exodus), P369 (P264 companions):** `apply-patches.sh` blocks
  all kept. The two `AosAttributes.GetValue` patches (`AOS-accessory-container-aggregation`,
  `AOS-level-gear-attribute-aggregation`) touch different hunks, and both are applied. P271 settled
  `BaseDecayingItem.cs` by keeping main's (P199's) class, generated `TimeLeft` property and timer, and P195's shared
  `DecayingLifespan` helper. The P199 and P195 layouts are the same: one saved int at index 0, so nothing on disk
  changes. P271 kept P199's `AbyssalCloth.cs` (P195's copy was a duplicate). P355 and P369 changed only flaky tests, and
  both test changes still assert the behavior they had.
- **P360 / P366 (P242 flying loot):** the server side merged as one new file plus the hook in `LootBox.Open`. The art
  IDs 15536-15589 do not overlap P243's 15592-15629 (`LeagueHall.cs` uses 0x3CE8-0x3D0D, which is inside 15592-15629).
- **CHANGELOG and VERSION:** for every merge in the range, I checked each line its branch added to `CHANGELOG.md`, and
  every one is in today's file. No line is in two places. No version heading is repeated (the only repeat,
  `## 2026.10.02`, is the example inside the header comment). The headings run .10 to .20 in order, and `VERSION`
  reads `2026.10.21.20`.

**Serialization:**
- `CharacterLeagueData` v1 to v2 (P280, `ClusterFAccountData.cs:688-773`): it writes and reads the same fields in the
  same order, behind `version >= 2`.
- `LevelGearStore` (`ClusterFLevelGear.cs:249-312`) and `CompanionLineage`: own versioned GenericPersistence. Their
  file names ("LevelGear", "Companions") clash with no other store.
- Every new item uses the serialization generator.
- The one saved class whose fields changed in the range (`LootBox`) gained only methods, in a partial
  (`NotedJokeItems.cs:22-40`).

**Patches:** the new one-line hooks were read against pinned: Recall, Moongate, Runebook (`Entries.Count >= 16`),
PetOrders, CraftItem (all four sites), Resmelt, SalvageBag, SmallBOD, DetectHidden, the two AOS patches and the
PlayerMobile hooks. `Mining.cs`'s new `CheckResources` override fires only on the starting check
(`timed == false`, pinned `HarvestSystem.cs:462`), as its comment says. Every `.patch` file is applied by name.

**Settings:** every new `clusterf.*` key is read with `GetOrUpdateSetting`, so it loads and is written with its
default. No key is defined twice with different defaults. `ClusterFStoreBought` and `SmithCommissionSystem` set
theirs in `Configure`, which pinned runs on every type. No duplicate command names.

**Hot paths:**
- Read: `AosAttributes.GetValue`'s two new calls, both movement handlers (accessories and Noted), `DeployedTrap`'s
  step watcher and the flying loot send.
- I found no missing null check that can throw. `GetValue` dereferences `m` before our calls (pinned `AOS.cs:628`).
  `GroundAt` and `BoxOpened` guard null and internal maps.
- Not measured: `ClusterFAccessories.AttributeTotal` builds a list and checks two achievements for each jewel on every
  `GetValue` call, for players who have an accessory container. It is correct but not cheap. Only a profile on a live
  shard would say whether it matters.

**Art registry:**
- 561 rows: 521 art, 24 body, 15 gump, 1 anim.
- No ID appears twice within a kind.
- Every art and gump row has its PNG, and no PNG is unregistered.
- The rows added in the range: 15536-15589 (P242), 15592-15629 (P243), gumps 22459-22468 (P241) and 28016-28294
  (P265).
- Whether 28016-28294 (0x6D70-0x6E86) is free in the client's own art cannot be checked from GitHub. P265 says
  `find-free-art.py` checked it on the game PC.

## What I could not check from GitHub alone

- Nothing was built and no test was run. Findings 1 to 3 are from reading the code; each prompt draft asks for a red
  test first.
- Patch hunks applying at fuzz 0 against the pinned tree: I read the context against pinned, and the integrator's
  builds were green. I did not apply them here.
- The client side of flying loot and the hall decor (tiledata and animdata in the player package) needs the game PC.

P379 DONE
