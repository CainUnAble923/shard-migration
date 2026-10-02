# cc-P30: ModernUO upgrade research, pinned 7c9215d97 to upstream d4531cd9

Written 2026-10-02 by Claude (cc-P30). Research only: nothing in `D:\ShatteredLegacy`, `D:\UO\ModernUO-pinned`,
`D:\UO\ModernUO-reference` or `docs\` was changed, nothing was committed, and no shard was touched. My builds wrote
only `cc-p30-trial*` tags. (`sl-modernuo:latest` changed during this task, from `d353a3fb86f2` to `246b0d5813e5`;
that was the parallel P31/P32 builder, not me. It is still engine 0.15.6.52, annotations 2.14.2.) Every build and
every save load ran on copies under `D:\UO\cc-p30-upgrade-work\`.

**ShatteredLegacy HEAD moved while I worked** (`56cae9d` -> `045b313`, 25 files, P32's spawner importer, smith BOD
paths and rare self repair). The main trial is on `56cae9d`. I re-ran the bump on `045b313` as well (section 3b):
**green, 31/31 patches, 421/421 shard tests in Docker**, after 3 more small fixes.

Citation convention in this note: **P:** is pinned `7c9215d97`, **U:** is upstream `d4531cd94`, both under `Projects/`.
"Ours" is `D:\ShatteredLegacy\server\...` at HEAD `56cae9d`.

---

## Headlines

1. **It works.** Our whole tree compiles against upstream `d4531cd9`, the copied `build.sh` gate is green
   (**29/29 patches, 408/408 shard tests** at `56cae9d`; **31/31 and 421/421** at today's HEAD `045b313`), upstream's own suites pass on the same build (**Server.Tests 893 passed,
   17 skipped, 0 failed; UOContent.Tests 1,504 passed, 91 skipped, 0 failed**), and the trial image
   `sl-modernuo:cc-p30-trial` loads copies of both the test-shard and the live save.
2. **The change set is small and mostly mechanical: 52 files** (42 modified, 10 deleted), saved as
   `notes\cc-P30-tools\trial-changes-d4531cd9.diff`. Of that: 4 patch rebases, a three-way merge of our two craft
   replacements, 101 attribute rewrites done by a script (8 files), small API fixes in 10 more customization files
   (7 causes), fixes in 16 test files, and 11 type collisions to decide (10 files deleted, 1 split).
3. **Three things would have hurt us on bump day. All three were reproduced in the trial, not just read in code.**
   - **Our compose layout loses the world on the first save.** Upstream's new save publish (#2612) renames the
     `Saves` directory. Ours is a bind mount, which cannot be renamed. Trial run 2: the save failed, and **the
     host-side `Saves` copy was left with 0 files**. The good save sat in `Saves.next` inside the container's
     writable layer. Mounting the parent directory fixes it (run 3: clean publish).
   - **The first boot hangs** on a new pathfinding prompt (#2475) because both stacks set `tty: true`.
     One setting answers it.
   - **11 of our ported types now ship upstream under the same names** (SA throwing artifacts and the Ter Mur
     reptiles). On the test-shard save that means **107 creatures and 1 item cannot be read** and are deleted at
     load, behind two interactive prompts.
4. **Two of my own trial fixes were wrong the first time, and the tests caught both.**
   - `git merge-file` attached our Craft X failed-attempt hook to upstream's new T2A overload instead of the live
     one. It compiled clean; three Craft X tests went red.
   - A save-shape test failed. It pins pinned's `Item` header, which changed upstream, as designed.
   - A tool now audits hook placement (`notes\cc-P30-tools\hook_audit.py`).
5. **The bump is one-way, verified.**
   - After one save on the trial image, the `.idx` header reads version `05` (it was `03`).
   - `SerializedTypes.db` is gone.
   - The pinned image fails on that save copy, fatally: `System.Exception: Invalid type flag, expected 2 but
     received 167.`
6. **Stopping short at `fd27b7a3` buys almost nothing.** The same patch failures, the same craft merge and all 11
   collisions are already present there. What it skips is about 20 lines of mechanical fixes. In exchange it gives
   up the save-safety rewrite, the decay follow-up fix (#2583), the pets/AI batch and `SkillEvents`. It would also
   leave a second, harder bump for later, against a live world.
7. **D44 (`AOS-stat-bonus-names`) is still a defect upstream at d4531cd9** (U:UOContent/Misc/AOS.cs:723 adds by
   `GetHashCode()`, :747-749 removes by `Owner.Serial`). By upstream's own classification it is **exploit-class**
   (stat gain outside the rules), so the route is private email, not a public issue. A draft is in section 8.
   Nothing was sent.

**Recommendation: go.**
- **Target:** `d4531cd94b739613155225c234900de9f47d2c88`. Nothing landed upstream after it as of this run. Re-survey
  if the build prompt runs more than about two weeks from now.
- **Size:** about **9 units**. One unit here means one small, gated builder cycle; F-3 is "about 20" in the same
  currency.
  - 2 units: pinned-side prep that can land first and is proved on the pinned engine.
  - 4 units: the bump itself, replaying the trial diff.
  - 2 units: test-shard cutover with client checks.
  - 1 unit: docs churn.
- **Slot it as the next builder prompt after P32 finishes, and before P33.** I first wrote "before P32"; P32 landed
  while I worked. Re-running the bump on the new HEAD cost 3 small fixes (section 3b), so the window is still cheap.
  - P32's new `ImportSpawners-guid-key.patch` conflicts (upstream rewrote the importer in #2505) but rebases with the
    same intent.
  - Its test fixture needed the new `$type` discriminator.
  - P33 (F-3, about 20 units) and F-12 (about 30 more patches) would each raise the bump's cost. The bump has to precede the fresh-world wipe anyway, so that the new world is born
  idx v5 and never needs the one-way step at all.
- **The live shard can stay on pinned until the wipe.** Its save loads clean on the trial image (run 5, 0 failures),
  so either order works.

---

## 0. Before starting

- **`D:\ShatteredLegacy` state.**
  - HEAD `56cae9d` at the start; `045b313` by the end (see section 3b).
  - Dirty only in `design\registrar-office\` (P31's work): 4 modified, 5 untracked.
  - I did not build there.
- **Upstream clone.** Fresh at `D:\UO\ModernUO-upstream` (new for this task). Target `d4531cd94`, 2026-09-30 21:24
  -0700, is upstream HEAD; nothing landed after it.
- **Counted, not taken from the brief.**
  - 156 commits, 891 files, +65,953 / -18,954 lines. This matches the brief.
  - **The brief says 30 `apply_patch` lines. There are 29.** A `grep -c '^apply_patch'` gives 30 only because it
    also matches the `apply_patch() {` definition; my own survey script made the same mistake on its first run.
    `server\patches\` holds 29 `.patch` files and 5 `.cs` replacements, 34 files in all.
- **Numbering.**
  - No clash for P30.
  - One oddity: `D:\UO\cc-prompts` holds both `cc-P29-registrar-office-cleanup.md` and
    `cc-P31-registrar-office-cleanup.md`, while P29 was defect batch 2 (`notes\cc-P29-defect-batch-2.md`, per
    `apply-patches.sh`). It looks like a renumbered prompt left behind.
- **Governing-text tension (not mine to resolve).**
  - `AGENTS.md` here still says "no fresh world" (section "What this project is", and rule 7).
  - `docs\feature-queue.md:233,270` plans one.
  - The engine bump does not need a fresh world: the live save loads clean on the trial image. Section 7 is written
    for the wipe the brief assumes.

---

## 1. Patch survey (the cost driver)

- **Method.** `notes\cc-P30-tools\patch-survey.sh` applies every `apply_patch` line in file order, cumulatively, to a
  `git archive` of the target, exactly as the gate does (`-p1 --forward --ignore-whitespace --batch`). It tries
  `--fuzz=0` first, then `--fuzz=3`. The script refuses nothing.
- **Fuzz success is not trusted.** Every fuzz success was read by hand afterwards, and one of the two "successes"
  was a corruption (row 16).
- **Baseline.** The same script against pinned gives 29/29 clean, which is the control.

| # | Patch | Pinned target | Result at d4531cd9 | Upstream commit | Rebase |
|---|---|---|---|---|---|
| 1 | PlayerMobile-individual-stat-cap | UOContent/Mobiles/PlayerMobile.cs | clean (offset) | | none |
| 2 | Healer-resurrection-policy | Mobiles/Healers/Healer.cs | clean | | none |
| 3 | HealerGuildmaster-resurrection | .../Guildmasters/HealerGuildmaster.cs | clean | | none |
| 4 | AOS-pet-mimic-attribute-aggregation | Misc/AOS.cs | clean (offset) | | none |
| 5 | Bandage-pet-mimic-targeting | Items/Skill Items/Misc/Bandage.cs | clean | | none |
| 6 | BaseWeapon-talisman-durability | Items/Weapons/BaseWeapon.cs | clean (offset) | | none |
| 7 | CraftGump-MakeXClear | Engines/Craft/Core/CraftGump.cs | clean | | none |
| 8 | CraftGumpItem-MakeX | Engines/Craft/Core/CraftGumpItem.cs | **fuzz 2**, placement correct | #2476: Back now calls `CraftItem.ShowCraftMenu` | S, regenerated |
| 9 | SmallSmithBOD-PostValorite | Engines/Bulk Orders/SmallSmithBOD.cs | clean | | none |
| 10 | Mobile-set-item-resistance-hook | Server/Mobiles/Mobile.cs | clean (offset) | | none |
| 11 | AOS-set-attribute-aggregation | Misc/AOS.cs | clean (offset) | | none |
| 12 | BaseArmor-set-self-repair | Items/Armor/BaseArmor.cs | clean (offset) | | none |
| 13 | PlayerMobile-fountain-luck-bonus | Mobiles/PlayerMobile.cs | clean (offset) | | none |
| 14 | AOS-damage-eater-hook | Misc/AOS.cs | clean | | none |
| 15 | AOS-stat-bonus-names (D44) | Misc/AOS.cs | clean (offset) | **not fixed upstream** (U:Misc/AOS.cs:723 vs :747-749) | none; report (section 8) |
| 16 | UOContentFixture-npc-speeds | UOContent.Tests/Fixtures/UOContentFixture.cs | **target gone**. Fuzz 3 "succeeded" by appending code after the class's closing brace. | #2473 moved the bootstrap to U:UOContent.Tests/Fixtures/TestServerInitializer.cs. **Partly obsolete:** upstream now calls `NPCSpeeds.Configure()` itself (U:TestServerInitializer.cs:113). | S, retargeted (see below) |
| 17 | BaseCreature-PlayerMobile-can-auto-stable | Mobiles/BaseCreature.cs + PlayerMobile.cs | **fuzz 1** (offset 463), placement correct | #2611 converted BaseCreature; upstream has no `CanAutoStable` | S, regenerated |
| 18 | Beverage-chicken-lizard-egg-pour | Items/Food/Beverage.cs | clean (offset) | | none |
| 19 | Virtue-stock-pieces-set-carrier | Items/Armor/Sets/{SpiritualityHelm,ValorGauntlets}.cs | clean | | none |
| 20 | Miasma-pinned-waiting-drop | Mobiles/Monsters/ML/Labyrinth/Miasma.cs | clean | | none |
| 21 | LadyLissith-pinned-waiting-drop | .../Twisted Weald/LadyLissith.cs | clean | | none |
| 22 | Loot-hat-types-orc-tribal-mask | Misc/Loot.cs | clean (offset) | | none |
| 23 | StealableArtifacts-servuo-entries | Engines/Stealables/StealableArtifacts.cs | **conflicts** | #2512 appends `ValkyriesGlaive` as slot 80, the slot where ours puts `DyingPlantArtifact` | M, rebased (see below) |
| 24 | AccountHandler-test-center-deletion | Accounting/AccountHandler.cs | clean (offset) | not fixed upstream; #2562 and #2564 did not touch `RestrictDeletion` | none |
| 25 | Account-young-duration | Accounting/Account.cs | clean (offset) | | none |
| 26 | PlayerMobile-young-time-only | Mobiles/PlayerMobile.cs | clean (offset) | | none |
| 27 | Resmelt-smelt-one | Engines/Craft/Core/Resmelt.cs | clean (offset) | not obsolete: upstream still has the members private | none |
| 28 | SalvageBag-salvage-all | Items/Containers/SalvageBag.cs | clean | not obsolete: file unchanged upstream | none |
| 29 | BOD-combine-contained | Engines/Bulk Orders/{Small,Large}BODGump.cs | clean | not obsolete: cliloc 1157304 has no upstream use | none |

**Totals.**
- 25 apply at fuzz 0: 12 clean, 13 with offset only.
- 2 need regenerating after a correct fuzz.
- 1 needs retargeting after an incorrect fuzz.
- 1 conflicts.
- 0 obsolete outright.
- 1 partly obsolete (the NPCSpeeds call in #16).

**Row 16, retargeted.** Our four remaining calls (`SkillCheck.Initialize`, `NameList.Configure`,
`Corpse.Initialize`, `BaseCreature.Configure`) now go right after upstream's `NPCSpeeds.Configure()` in
`TestServerInitializer.Initialize()`. I checked that all four targets exist upstream (U:UOContent/Skills/SkillCheck.cs:33,
U:UOContent/Misc/NameList.cs:42, U:UOContent/Items/Misc/Corpses/Corpse.cs:594, U:UOContent/Mobiles/BaseCreature.cs:4265).
The file should be renamed `TestServerInitializer-shard-bootstrap.patch` in the real bump; I kept the old name so
`apply-patches.sh` did not need an edit in the trial. `build.sh`'s validator (no hand-registered NPC speeds) still
holds.

**Row 23, rebased.**
- Upstream's single `ValkyriesGlaive` line is replaced by our 58-entry block, which already carries `ValkyriesGlaive`
  at **our** slot 85. Saved slots map to entries by index, and our worlds hold slots 80 to 137 in our order.
- Upstream's order would shift every saved slot from 80 on.
- Result: 138 entries, the same 80 + 58 as before; `ValkyriesGlaive` appears once.

**The candidates the brief asked about.**
- **PlayerConstructed group (#2573, #2574, #2576, #2579).** None of our four patches is obsolete.
  - Resmelt, SalvageBag and SmallSmithBOD-PostValorite serve our own features. BOD-combine ports OSI's combine
    button, which upstream does not have.
  - The net upstream change to `SmallBOD.cs` across #2573 and #2579 is **zero lines**: #2573 added the player-crafted
    requirement and #2579 removed it again.
  - **The D42 clamp still holds.** `SmithGuildSalvageBag.IngotReturn` is pure arithmetic over the same inputs, and
    `PlayerConstructed` is now inherited from `Item` (#2574), so `BaseArmor { PlayerConstructed: true }` still binds.
  - **One real dependency.** #2574 stamps `PlayerConstructed` only inside `CraftItem` (U:UOContent/Engines/Craft/Core/
    CraftItem.cs, 2 sites) and removes the stamp from the three `OnCraft` overrides. Our `CraftItem.cs` is a
    full-file replacement. **A bump that kept our old file would stop flagging all crafted gear, and D42's bag would
    pay the 2-ingot floor for everything.** The trial's merged file carries both stamps.
- **D44.** Not fixed; see section 8.
- **#2611, #2670, #2674, #2591, #2473 (creature and fixture changes).**
  - Only #16 and #17 above were affected.
  - The npc-speeds part of #16 is now upstream's.
  - `CanAutoStable` is not upstream (no match in U:).
- **#2562, #2564 (accounts and login).** All four PlayerMobile/Account patches apply at fuzz 0.

**Full-file replacements (not patches, so the gate cannot see upstream drift; checked by hand).**
- 11 of the 13 replaced or sed'd files are byte-unchanged upstream.
- **`CraftItem.cs` (+636/-65 upstream, #2476 and #2574) and `CraftContext.cs` (+8, #2476) changed.** A plain bump
  would have silently reverted the T2A craft-menu work and the `PlayerConstructed` stamp.
  - **Three-way merge** (`git merge-file`, ours / pinned / upstream): 10 conflict hunks, all small. Resolved by
    explicit rule; see the diff. The T2A branches are kept intact, since T2A menus are off for us.
  - **Placement audit** (`hook_audit.py`, which compares each Shattered Legacy hook's enclosing method before and
    after) found **one hook on the wrong overload**: the failed-attempt `ClusterFCraftRun.AfterAttempt`. Fixed in the
    trial.
  - Our replacement now differs from upstream by 153 lines (169 against pinned).
  - **Recommendation: convert both to `.patch` files during the bump.** A replacement hides upstream drift
    completely, and it cost the most to reconcile here.
- **Additive copies.** No silent overwrite.
  - None of the 132 top-level customizations copied flat into `Projects/UOContent/Misc/` has a namesake upstream.
  - The structured mirror refuses overwrites anyway; it ran clean (652 files).
  - Our 9 `Server.Items.PetMimic.v0..v8.json` schemas have no namesake among upstream's 3,846 migration files.
    After the v4 build they are byte-identical, and the generator emitted no new JSON (3,855 = 3,846 + 9).

## 2. Our code against upstream APIs

### 2a. What the compile actually found

Grouped from `notes\cc-P30-tools\group_errors.py` over five local compile passes. A pass only reveals the next
layer, because `UOContent.Tests` does not compile until `UOContent` does.

| Group | Count | Files | Cause (upstream) | Fix | Size |
|---|---|---|---|---|---|
| `[SerializableFieldSaveFlag]` / `[SerializableFieldDefault]` removed | 81 + 20 = **101** | 8: `BaseSet{Armor,Clothing,Jewel,Quiver,Shield,Weapon}`, `Marksman/Swiftflight`, `FirstAidBelt` | generator 4.2.0 marks both `[Obsolete(..., true)]`; its message says "The wire format does not change" | `[SaveFlag(nameof(Should), nameof(Default))]` on the field, by script (`v4_saveflag.py`) | S |
| Type-name collisions | **11 types, 10 files + 1 split** | `Items/Artifacts/Equipment/Weapons/{BansheesCall,RaptorClaw,StoneSlithClaw,StormCaller,ValkyriesGlaive,WindOfCorruption}`, `Mobiles/Normal/{Raptor,Slith,StoneSlith,ToxicSlith,Spellbinder}` | #2453, #2512, #2515, #2516 add the same types in the same namespaces | a decision, see 2c | M (decision) |
| `BaseCreature.CreatureDeathEvent` moved | 1 | `ClusterFAchievements.cs:1058` | moved to U:UOContent/Mobiles/CreatureEvents.cs:9 | rename | S |
| `AcquireOnApproach` removed | 1 | `Mobiles/Normal/MinionOfScelestus.cs:82` | #2601: every creature now acquires on approach after `AcquireOnApproachDelay` (U:BaseCreature.cs:1326, 2 s; paragons 0) | `AcquireOnApproachDelay => TimeSpan.Zero` keeps pinned's "at once" | S |
| `run` removed from movement API | 2 overrides + helper | `Services/Revamped Dungeons/DespiseRevamped/AI.cs` | #2599: Running bit derived from pace, `WalkMobileRange(m, steps, min, max)` (U:UOContent/Mobiles/AI/BaseAI/AIMovement.cs:703) | drop the parameter | S |
| `DamageEntries` is a `ValueLinkList` | 3 + 4 tests | `DespiseRevamped/Region.cs`, `BaseSABosses.cs`, `BaseRenowned.cs`; tests CC6Batch1/5/8 | #2605; enumerator is an extension in `Server.Collections` | `using`; `.Count` instead of `Assert.Empty` / `.Any` | S |
| Talisman sub-objects take an owner | 4 | `Items/Equipment/Talismans/CollectionsBritLibraryTalismans.cs` | #2609 (U:UOContent/Items/Talismans/TalismanAttribute.cs:25-39, BaseTalisman.cs:753) | pass `this` | S |
| `Spawner.Entries` is `IReadOnlyList` | 1 | `ClusterFOldHavenCleanup.cs:197` | #2621 (U:UOContent/Engines/Spawners/BaseSpawner.Entries.cs:14) | `Select` instead of `ConvertAll` | S |
| `BufferWriter` lost its types queue | 16 sites in 14 test files | tests only | U:Server/Serialization/BufferWriter.cs:61-72 | drop the argument | S |

**Totals.** 101 mechanical attribute rewrites (8 files), plus hand edits in **10 customization files and 16 test
files** (counted from the trial's git diff; the test count includes the 5 test-run fixes in section 3), plus the
collision decision.
`[DeltaDateTime]` (2 fields: `GobletOfCelebration`, `GrapeVine`) **still compiles** under 4.2.0, despite #2589
marking `WriteDeltaTime` obsolete. Converting them is optional and needs a version bump plus `MigrateFrom` (upstream
template U:UOContent/Spells/Spellweaving/Items/TransientItem.cs:6-19).

### 2b. Inventory (counted by a read-only agent and spot-checked by me against the compile)

**Serialization.** 940 `[SerializationGenerator]` attributes in 674 files:
- `(0, false)`: 938. `(9, false)`: `PetMimic`. `(0)`: `ShrunkPet`.
- The second argument means "the version was written with `ReadInt`/`WriteInt`, not encoded". Upstream's own rule:
  "omit `encoded`" for new classes (U:../dev-docs/serialization.md:94-116; repo `CLAUDE.md` rule 9).
- It is harmless while each type stays ours. It is **exactly what broke the collisions at load** (2c).

**Hand-written `Serialize`/`Deserialize`.** 7 classes in 6 files. None sits on a base whose version changed. All
still compile and still chain.
- The bases that changed:
  - BaseCreature: hand-written v20 -> generated `(24, false)`, with `MigrateFrom(V23Content)` and a legacy reader for
    0-22 (U:BaseCreature.cs:137, :2189, :2253)
  - BaseArmor 9 -> 10, BaseWeapon 10 -> 11, BaseClothing 7 -> 8, BaseJewel 4 -> 5, Corpse 16 -> 19
  - BaseVendor -> `(2, false)`, Item 9 -> 11, Mobile 36 -> 38, BaseSpawner 12 -> 13, Spawner 1 -> 2
- The load test is the proof: on the test-shard copy, **nothing failed to deserialize except the 108 collision
  instances** (206,232 items and 35,061 mobiles loaded), and the live copy loaded with 0 failures. That covers every
  BaseCreature and BaseVendor subclass of ours that has an instance in either save.

**`server\migrations\*.json`.** Unchanged schema format. Not regenerated, no diff (see section 1).

**Creatures.**
- No overrides of the members #2611 made non-virtual (`DamageMin/Max`, `Active/PassiveSpeed`).
- `ControlMaster` and `SummonMaster` are now views over one `Master` (U:BaseCreature.cs:1158-1196).
- **One behaviour change: `Niporailem.cs:175,198`** assigns `SummonMaster` without setting `Summoned`, so the read
  comes back null. That turned `CC9CloseVerification` red. Fixed in the trial by writing and reading `Master`,
  which is upstream's prescribed form for this shape (U:../dev-docs/runuo-migration-docs/09-items-mobiles-creatures.md,
  "SummonMaster on a creature that sets it without Summoned").
- `Medusa.cs:299` reads `SummonMaster` of creatures Medusa never assigns, so it is unaffected.

**Spawners.**
- One subclass, `DespiseSpawner : Spawner` (`DespiseSpawns.cs:39`). It compiles.
- It inherits `Spawner.ToDto()`, so a JSON export would drop its `_powerMin`/`_powerMax`. That is unverified in game,
  and matters only if P32's importer round-trips it.
- Seeders: `ClusterFNewHavenServicesSeeder.cs:400`, `ClusterFOldHavenSeeder.cs:191`, `ShameSpawns.cs:278`. All
  compile, and `AddEntry` is unchanged.

**OPL.**
- 38 files override `GetProperties` / `AddNameProperties`. All compile.
- #2501 changes tooltip line order on armour, weapons and clothing. No test of ours checks order. Client-visible
  only.

**Feature flags (#2653/#2654).** No use in ours.
- The trial seeded 14 default flags on first boot (log: "Seeded 14 default feature flag(s)"). That writes new
  JSON under `Configuration/FeatureFlags/`, which is bind-mounted, so the host will see new files after the first
  boot.

**Hair (#2462).** 19 references in 7 files, all to `Mobile` properties that still exist. They compile.

**Craft (#2476).**
- `t2aCraftMenus` defaults to `!Core.UOTD` (U:UOContent/Configuration/ExpansionConfiguration.cs:15).
- `Core.UOTD => Expansion >= Expansion.UOTD` (U:Server/Main.cs:328), which is true for EJ, so **T2A menus are off for
  us**. Nothing of ours sets the key.
- It touches ours only through the `CraftItem`/`CraftContext` merge above.

### 2c. The 11 collisions: what the save test showed and what I recommend

| Type | Ours | Upstream | In test-shard save |
|---|---|---|---|
| Slith, StoneSlith, ToxicSlith | ServUO port, `(0, false)` | `(0)`, same stats, abilities, loot and taming; **StoneSlith has `GraspingClaw` and `TailSwipe` implemented, which closes our deviation D-57** | 32, 22, 18 |
| Spellbinder | ServUO port, `(0, false)` | `(0)`, identical stats and names, plus a dedicated `SpellbinderAI` | 20 |
| Raptor | ServUO port with **pack friends** (`_isFriend` serialized, `FriendsTimer`), 191 lines | `(0)`, 76 lines, no pack behaviour | 15 |
| ValkyriesGlaive, BansheesCall, RaptorClaw, StoneSlithClaw, StormCaller, WindOfCorruption | ServUO ports, `(0, false)` | `(0)`, same attributes | 1 ValkyriesGlaive |
| WindOfCorruptionHuman | ours only (in `WindOfCorruption.cs`) | absent | kept in the trial |

**Why they fail at load.** Every pair writes its version differently (4-byte int against 1 encoded byte). Each
failure reads exactly **3 bytes short** ("Serialized object was 505 bytes, but 502 bytes deserialized").

**The trial took upstream's copy of all 11.** Result on the test-shard save:
- **107 creatures and 1 item deleted at load**, behind two `Delete the object and continue? (y/n/a)` prompts (one for
  mobiles, one for items).
- The live save holds none of the 11 and loaded clean.

**Recommendation: take upstream's for all 11** (fidelity: upstream is the engine we run, and it closes D-57), keep
`WindOfCorruptionHuman`, and **purge the 11 types from the test shard on pinned before the bump** with a staff
command, then save. The bump boot then needs no prompt at all.
- The deleted creatures are spawner stock; the spawners name types by string, so they respawn as upstream's.
- The Glaive is very probably the stealable-artifact slot, which respawns.
- Both of those are **unverified in game**.

**The cost: Raptor pack behaviour.** If Chase wants it, it goes back as a patch onto upstream's Raptor, argued in
notes first. Keeping our 11 instead means routing them as explicit replacements of upstream's files. That loses
D-57's fix and becomes a new class of hidden drift, like `CraftItem.cs`.

## 3. Trial build and test run

**Setup.**
- `docker\` and `server\` (less `lib`, `uo`, `razor-scripts`) were copied to `D:\UO\cc-p30-upgrade-work\sl`, with a
  local git baseline so every edit is a reviewable diff (3 commits).
- Edits to the copy only:
  - `Dockerfile:4` -> the full target hash.
  - `build.sh` tags -> `sl-modernuo:cc-p30-trial` and **`sl-uo-builder:cc-p30-trial`**.
- **The tags matter.** `build.sh:33` hardcodes `BUILDER_TAG=sl-uo-builder:latest`, so an unmodified copy would have
  overwritten the builder image the next real build reuses. The real bump should parameterise that tag.
- **Compile loop.** Iterated locally with `notes\cc-P30-tools\stage-tree.sh`, which runs the copy's own
  `apply-patches.sh` on a local export. The authoritative runs were the copied `build.sh`.
  - Local restore needed a nuget.org source, added in a scratch `nuget.config` only. This machine's global NuGet
    config has no nuget.org source.

**Results.**

| Run | Patch gate | Compile | Shard tests | Image |
|---|---|---|---|---|
| docker 1 | 29/29 | green | **400/408**: 8 failed | none (gate held) |
| docker 2 (after fixes) | **29/29** | green | **408/408** | **`sl-modernuo:cc-p30-trial` `f3101552efcb`** |
| upstream suites on docker 2's builder | | | Server.Tests 893 pass, 17 skip, 0 fail; UOContent.Tests 1,504 pass, 91 skip, 0 fail | |

The skips are upstream's tile-data-dependent tests; the builder has no client files.

**The 8 failures, all ours, each probed before it was fixed.**
- **CraftXVerification x2 and MakeXRepeatVerification x1. My merge was wrong.**
  - Probes showed attempt 2 entering `CompleteCraft` and leaving without a hook or a return.
  - Upstream added a hue-aware `CompleteCraft` overload for T2A, and `git merge-file` attached our failed-attempt
    hook to it.
  - Fixed by moving the hook. `hook_audit.py` now checks this mechanically.
- **CC9CloseVerification x1. The `SummonMaster` view (#2670).** Fixed via `Master` (2b).
- **NewHavenQuestBoardVerification.SaveShapeIsUnchanged. Expected.**
  - It pins pinned's bytes.
  - The board's own bytes are unchanged. Item's header moved from v9 to v11, and `LastMoved` is now an 8-byte anchored
    time instead of one delta byte.
  - Re-baselined with those 8 clock-dependent bytes masked.
- **NewHavenQuestBoardVerification x3. "never reached the wire". Harness only.**
  - Probing showed `send buffer exhausted - needed 359 bytes, 44 writable, ... 4096 capacity`.
  - Upstream now keeps a connection without an account on a 4 KiB send ring and promotes it only after credentials
    verify (U:Server/Network/NetState/NetState.cs:562-567).
  - The test never drains. Fixed by giving the test's NetState an account, the same way
    `GargoyleStartingClothesVerification.cs:48-60` already does.
  - A real player is post-login and promotes to 256 KiB, so **no live effect**. That last point is reasoning, not a
    client test.
- The three quest-board ones **pass alone and fail in sequence**, which is why the first isolated run misled me. I
  re-ran the whole class after the fix: 16/16.

**Save-load test (copies only, `--network none`, no published ports).**

| Run | What | Result |
|---|---|---|
| 1 | test save, test config as-is, `tty`, `Saves` bind-mounted (the compose layout) | **hangs at the pathfinding prompt** (U:UOContent/Engines/Pathing/PathCacheCommands.cs:61,73). Banner prints `Commit: 7c9215d97` on the new engine (`entrypoint.sh:5` hardcodes it) |
| 2a | as 1, no TTY (stdin piped) | **crashes**: `HeadlessConsoleInputException` at the first bad-deserialize prompt. Headless mode never answers a prompt (U:Server/Main.cs:585) |
| 2b | as 1, plus `"pathfinding.prebakeMaps": "False"` (settings are strings; a JSON `false` is a fatal parse error) | loads after `a` answered twice. **Deleted: 32 Slith, 22 StoneSlith, 20 Spellbinder, 18 ToxicSlith, 15 Raptor, 1 ValkyriesGlaive.** 206,232 items, 35,061 mobiles. **First save fails:** `Set aside .../Saves as Saves.previous-...` then `IOException: Cannot create '/var/lib/uo/modernuo/Saves'` (U:Server/World/World.cs:421-451, 476-480). **Host `Saves` copy left with 0 files**; the good save sits in container-only `Saves.next` |
| 3 | as 2b, with the **parent** `/var/lib/uo/modernuo` mounted | load **3.51 s**; same losses; autosave publishes cleanly ("snapshot done (0.53 seconds)"). **`.idx` header now version `05`** (was `03`). `SerializedTypes.db` gone; types now inside the idx. `Mobiles.bin` 18.0 MB -> 11.7 MB |
| 4 | **pinned image** (`sl-modernuo:latest`, separate container) on a copy of run 3's save | **fatal: `Invalid type flag, expected 2 but received 167.`** The save cannot go back |
| 5/6 | **live** save, live config + prebake answer, parent mount, real entrypoint | **0 failures**, 192,177 items, 34,982 mobiles, 2.17 s. **`SaveOnShutdown` (D36) works**: `docker stop` -> "Saving the world before shutdown... saved in 534 ms", idx v5 on disk |

**Plainly: once the test shard saves on the new engine, no `7c9215d97` image can open that save again.**

Not verified:
- No client connected to the trial.
- Spawner respawn of the purged types.
- The live compose file itself (only the test-shard layout was reproduced).
- `pathfinding.prebakeMaps: "True"`.
- The New Haven seeder reported "repaired 1" on the test save under the trial. I did not check whether pinned does the
  same on that save.

### 3b. The same bump on today's HEAD (`045b313`)

- `trial-changes-d4531cd9.diff` applies to `045b313` with `git apply --3way` and no conflicts.
- HEAD adds 2 patches (31 `apply_patch` lines).

**What broke, and how it was fixed:**
- **`ImportSpawners-guid-key.patch` (P32): conflicts.**
  - Upstream rewrote `ImportSpawnersCommand.cs` in #2505 (typed `SpawnerDto`).
  - Upstream **still** deletes every same-type spawner at an x,y before placing (U:UOContent/Engines/Spawners/Commands/
    ImportSpawnersCommand.cs:231, :258-272), which is the behaviour P32 removed. So the patch's intent carries over
    unchanged: rebased, 17 changed lines.
  - The defect itself looks upstream's to report. It is not exploit-class. I have not drafted it; P32's notes have
    the evidence.
- **`BaseRunicTool-no-random-self-repair.patch` (P32): applies clean.**
- **`ClusterFRareSelfRepair.cs:42`: the same `CreatureEvents.CreatureDeathEvent` rename.**
- **`SpawnerImportVerification.cs:72`: test fixture only.** The test writes spawn JSON with pinned's `"type"`
  discriminator; upstream's polymorphic `SpawnerDto` needs `"$type"`.
  - Upstream converted all 109 shipped spawn files (`Distribution/Data/Spawns`, +5,877/-5,760).
  - **We ship no spawn JSON of our own** (none under `server\`), so only the fixture changed.
  - The fact that imports pinned's real `Vendors.json` passed unchanged.

**Results on `045b313`:**
- Docker gate: **31/31 patches, 421/421**.
- Run before the fixture fix: 418/421, with exactly those 3 failing.
- **Local Windows test runs are not authoritative.** 11 shard tests (TypeIdentity, CommandDeclaration,
  ShardStatusPublisher) fail locally on both the old and the new stage and pass in Docker.

The delta to replay is **`notes\cc-P30-tools\trial-changes-head-045b313.diff`** (54 files). It supersedes the
`56cae9d` one for P36.

## 4. Behaviour changes that touch our design

**`SkillEvents.SkillUsed` (#2636).**
- Signature: `event Action<Mobile, Skill, bool>` (U:UOContent/Skills/SkillEvents.cs:18).
- It fires once per stock handler call, with `(mobile, skill, success)`. It also fires for creatures and for
  too-hard/no-challenge attempts. It carries no gain information.
- **F-12 does not need it, and should not use it as-is.**
  - Our `ClusterFSkillGain` wraps all four handlers, and `RunBoostedCheck` calls the stock handler up to
    `chanceAttempts` times (3 on the trial, logged "3 chance attempt(s)"). So `SkillUsed` would fire up to 3 times per
    real use.
  - The F-12 XP hook belongs in `RunBoostedCheck`, which already sees each real attempt once and sees the gain.
- No SkillCheck patch exists to move.
- Side note: `docs\feature-queue.md:902-903` says skill XP "needs a SkillCheck core edit". That is out of date.
  (This finding is from the Part 4 agent; I confirmed the event signature and the 3-attempt log line.)

**Exploit fixes we gain.** No `docs\bug-list.md` row closes; none described these.
- Stealing from locked containers (#2681).
- Treasure-guardian farming (#2568, #2569).
- PlayerConstructed stack laundering (#2576, #2579): a mixed merge clears the flag, a split copies it.
- These are silent gains. Nothing of ours depends on the old behaviour.

**Save safety (#2612, #2525).**
- #2612 is the bind-mount trap above. That is a **must-fix before the bump**.
- #2525 is internal; our `WeakEntityCollection` and `SaveOnShutdown` work (run 6).

**Login (#2562, #2564, #2566).**
- The patches apply.
- #2564 disconnects a 0x91 game login whose auth id arrives from a different address than the account login. Under
  Docker Desktop NAT every client is `172.19.0.1`, so this is unaffected today. It would matter only if the host ever
  preserved real source IPs.

**Decay (#2536, #2583, #2608).**
- `Decays => Movable && Visible && Spawner == null` (U:Server/Items/Item.cs:336). Ground items now really decay
  (1 h). Contents of locked-down non-secure house containers decay too.
- Per the Part 4 agent's survey, **nothing we seed or place decays**: addons, statics, the forge and anvil,
  spawners, altars, controllers, the quest board, the Reset stone and `[Decorate` output are all `Movable=false` or
  `Decays=false`.
- What will now decay after an hour, as intended:
  - Achievement rewards dropped at a player's feet when the pack is full (`ClusterFAchievements.cs:867`).
  - Player-dropped ShrunkPets and Elixirs.
- Not observed in the trial; no hour passed.

**Insurance (#2550).** The same `insurance.enable` key is now read in the Insurance engine. Nothing of ours touches
it.

**Pets and AI batch.**
- No dependency in Pet Mimic (an equipped Item), Young (account time), or familiars (we have none).
- The Young aggro limit of 3 is decided but not built (`notes\passdown-overseer-2026-10-02.md:43`).
- **Design note for the dungeon aggro limit:** after #2601 **every** creature acquires on approach with a 2-second
  reaction delay, where pinned did this only for paragons and opt-ins. Any limit should be measured on the new
  engine.
- Niporailem: see 2b.

**Pathfinding `.swb` (#2465-#2479).**
- **The first boot blocks** unless `pathfinding.prebakeMaps` is set (run 1). Settings values are strings.
- With `"True"`, the cache goes to `/modernuo/Data/Pathfinding/<map>.swb`. That is in the image layer, so it needs a
  volume or it re-bakes on every recreate. The agent reports about 18 MB per facet from #2471; I did not measure it.
- **Recommend `"False"` now.** Runtime `[PathBake` exists for later.

**Network and host.**
- Blocklist, CrowdSec and allowlist are all opt-in and logged disabled on boot.
- Idle sleep (#2559) needs no config.
- #2561 does not change our Dockerfile: the trial runtime image works with our current package list.
- **Headless containers crash on any console prompt** (run 2a). So keep `tty: true`, and make the first boot
  prompt-free rather than headless.

**Gargoyle Throwing and SA throwing artifacts (#2510-#2516).** Noted. They caused the 11 collisions; Throwing itself
is races-last.

## 5. Stop-short option, `fd27b7a3` (2026-08-21)

Survey at `fd27b7a3c` with the same script: 88 commits, 560 files.
- Rows 8 and 16 fuzz, row 23 fails, and the craft replacements carry the same +636/-65 (#2476 and #2574 are both
  before it).
- All 11 collisions are present: #2453 and #2510-#2516 are July.
- The generator is still 2.14.3.
- I did not compile at `fd27b7a3`, so that column is **unverified**. It is reasoning from which PRs predate it.

| | fd27b7a3 | d4531cd9 |
|---|---|---|
| Patch rebases, craft merge, 11 collisions | same | same |
| 101 save-flag rewrites, API fixes in 10 files, 16 test files | avoided | needed (scripted or trivial, about 1 unit) |
| Save publish rename trap (#2612) | **not present** (pinned-style publish) | present, fixed by the mount |
| idx v5 / one-way | **probably also one-way** (Item gains `PlayerConstructed` in #2574; unverified) | verified one-way |
| Gains | network fixes, login fixes, early exploit fixes, T2A craft, throwing, decay #2536 | all of that, plus #2583 (the decay follow-up: **#2536 without #2583 can insta-decay items**), save-failure safety, pets/AI batch, SkillEvents, spawner rewrite, master refs, generator v4 |
| Leaves for later | **a second bump through the serialization overhaul, after the wipe, on a live world** | nothing pending |

**Recommendation: d4531cd9.** Stopping short saves about one unit now and costs a harder bump later, on the world
players will be in. It also lands #2536 without its own follow-up fix.

## 6. Re-pin procedure and docs churn

**Every place the pin is named** (Part 6 agent's sweep; I verified the build ones).

Must change:
- `ShatteredLegacy\docker\uo\Dockerfile:4` (`ARG MODERNUO_COMMIT`).
- **`docker\uo\docker-compose.yml:8` (`MODERNUO_COMMIT: "7c9215d97"`, a second pin that overrides the Dockerfile for
  `docker compose build`).** It is on `Sync-ShardRepos.ps1`'s protected list, so it is staged by hand (Q-009).
- `docker\uo\entrypoint.sh:5` (banner hardcode; verified wrong in run 1).
- `docker\uo\SERVER.md:38-41`.
- `ShatteredLegacy\AGENTS.md:83` and `README.md:56`.
- `shard-migration\AGENTS.md:111,123` (plus its "3,991 `.cs` files" count, which will change).
- `docs\upstream-watch.md:37,62`, `docs\shard-inventory.md:15`, `docs\community-scripts-wishlist.md:38`,
  `docs\implementation-status.md:11` (superseded file).
- `notes\passdown-architecture-2026-10-01.md:84` and `notes\port-recipe.md` (5 lines).
- `tools\README.md:57`, and `tools\progress.py:250` / README:217 ("17 patches, 5 replacements"; stale anyway, it is
  29 and 5).

Must re-check out:
- `D:\UO\ModernUO-pinned`, in the same commit as the Dockerfile (AGENTS.md rule at :131).
- `D:\UO\ModernUO-reference` is a partial-clone duplicate at the same commit. Retire it or re-point it.
- `D:\UO\ModernUO-upstream` (new) can become the new pinned tree.

Briefs P31-P34 name `7c9215d97` as the authority. Any that runs after the bump needs the hash changed.

`Check-Repos.ps1` and `Sync-ShardRepos.ps1` do not name the pin.

**Citations.** Counted by regex `\w+\.cs:\d+`.
- `docs\`: **122** in 7 files (feature-queue 70, bug-list 33, patch-backlog 6, fidelity-principle 5, gap-register 3,
  client-test-queue 3, tasks 2).
  - 66 of them point into ModernUO source (43 files).
  - **41 of those 66 point into 23 files that changed upstream.** That is an upper bound, matched by basename.
- `notes\`: **5,340** (4,358 in `.md`). These are historical task reports.
- No "as of" convention exists in `docs\` today.

**Proposal.**
- Do not rewrite. Add one line to `docs\README.md`: "file:line citations in docs/ and notes/ dated before <bump
  date> are as of `7c9215d97` unless they say otherwise".
- Keep a register (in the bump prompt's notes) of just the 41 `docs\` citations into changed files. Re-check those
  41, and re-cite only where a decision rests on the line.
- `notes\` stays as written.

**Player package and launcher: no change.** `ClientVersion*`, `ClientVerification`, `Network/Encryption/*` and the
client-facing config are byte-unchanged, and the launcher checks only its own package stamp. The trial logged
"Automatically detected client version 7.0.114.40" and "Restricting client version to 7.0.114.40 or newer", the
same as pinned.

## 7. Batched build plan

| Prompt | Kind | Content | Size | Gate / proof |
|---|---|---|---|---|
| **P35** pre-bump prep, on pinned | builder + Chase | (a) both compose files mount the **parent** directory (live: `${SERVER_PATH}/lib/uo/modernuo:/var/lib/uo/modernuo`, which already holds Saves, Backups, Archives and status; test: a new `lib/uo/modernuo-test/` holding `Saves`, so its backups persist too); (b) `"pathfinding.prebakeMaps": "False"` in both `Configuration*/modernuo.json` (pinned ignores the key; prove it); (c) `entrypoint.sh` banner from a build ARG; (d) `build.sh` builder tag follows `-t`; (e) a staff command to purge the 11 colliding types, **run on the test shard only and only once the bump is approved** | 2 | live and test boot and save on pinned with the new mounts; red-proof the mount by showing the old layout fails on the trial image (run 2b already shows it) |
| **P36** the bump | builder | replay `trial-changes-head-045b313.diff` (re-run `git apply --3way` against whatever HEAD is then); rename the fixture patch; convert `CraftItem.cs`/`CraftContext.cs` to `.patch` (recommended); the collision decision; Dockerfile + compose ARGs + ModernUO-pinned + AGENTS hash in one commit; red-proof the rebased patches (break context, watch fuzz=0 fail) | 4 | `build.sh` green; upstream suites 0 failed; `hook_audit.py` 0 real mismatches |
| **P37** test-shard cutover | Chase + builder | back up `Saves-test` (idx v3) and tag the old image; purge, save, stop; deploy; first boot; client checks: craft gump and Craft X (both modes), quest board, BOD combine, smith bag D42, Despise orb pets, stat cap, Young, a stealable slot, a Ter Mur spawn | 2 | T-rows in `docs\client-test-queue.md` |
| docs churn | Claude | the `docs\README.md` line, the 41-citation register, `docs\upstream-watch.md` refreshed for the new pin, the D-57 reversal recorded | 1 | |
| D44 disclosure | Chase | send or do not send section 8's draft | 0 | |

Total about **9 units**. **The live shard is untouched by all of it** until the wipe, or until Chase chooses to bump
it (its save is clean: run 5).

## 8. Rollback story

**Saves are one-way** (run 4). Rollback therefore means **going back to the last pre-bump save and losing
everything played since**.

Keep, before P37 boots the new image on the test shard:
1. **The image.** Re-tag whatever `sl-modernuo:latest` is at that moment as `sl-modernuo:pre-bump-7c9215d97` (it was
   `246b0d5813e5` at the end of this task), and keep the builder image. Rebuilding pinned later needs GitHub and the old `apply-patches` state; a tag needs nothing.
2. **The save.** A copy of `Saves-test` taken **after the purge save and before the new boot**, plus its
   `Saves-test.aside-*` siblings. The purge save is still idx v3 and loads on pinned.
3. **The source.** Both repos at the pre-bump commits. The bump is one commit in each, so `git revert` restores the
   pin, Dockerfile, compose and patches together.
4. **The tree.** `D:\UO\ModernUO-pinned` at `7c9215d97` until P37 passes. Then re-check it out.

To roll back:
1. `docker compose -f docker-compose.test.yml down`.
2. Point the test stack at the `pre-bump` tag.
3. Restore the copied `Saves-test`. The new-engine save cannot be opened by it; set it aside, do not delete.
4. Revert the two commits.

The live shard needs no rollback plan, because it is not bumped.

---

## Draft: D44 private disclosure (not sent)

**Verified at upstream `d4531cd9`.** Before sending, re-verify against live `main` with read-only
`gh api repos/modernuo/ModernUO/contents/Projects/UOContent/Misc/AOS.cs`, and search issues and PRs for a duplicate.
I did neither. Per upstream's `dev-docs/bug-reporting.md`, this is exploit-class ("stat gain outside the rules"), so
it goes to **hi@modernuo.com** only, not to an issue, a PR or Discord. Nothing below names the shard or quotes
non-upstream code.

> Subject: AosAttributes stat bonuses never removed (repeated equip stacks Str/Dex/Int)
>
> In Projects/UOContent/Misc/AOS.cs, AosAttributes.AddStatBonuses names its stat mods with the attributes object's
> hash code (`var hashCode = GetHashCode();` then `$"{hashCode}Str"`, `$"{hashCode}Dex"`, `$"{hashCode}Int"`), while
> AosAttributes.RemoveStatBonuses removes them by the owner's serial (`var serial = Owner.Serial;` then
> `RemoveStatMod($"{serial}Str")` and so on). The names never match, so RemoveStatBonuses removes nothing.
>
> Effect: an item that applies stats through these two methods (seen with a talisman and a quiver carrying Str, Dex or
> Int bonuses) leaves its mod on the wearer after removal, and each re-equip adds another copy under the same
> name. In a test, equip/unequip/equip left the bonus applied twice, and it persists until the mods are cleared
> (logout/restart). Other item families name these mods by serial on both sides.
>
> Lines at d4531cd94: AOS.cs:723 (hash code), :726, :731, :736 (add), :745-749 (remove).
>
> Suggested fix: name the mods by `Owner.Serial` in AddStatBonuses, matching RemoveStatBonuses.

Our fix is `server\patches\AOS-stat-bonus-names.patch` (cc-P29 D44, proved red there). It stays until upstream
ships one.

---

## Open questions for Chase

1. **Go, and when?** My recommendation: d4531cd9, as the next builder prompt once P32 is done, before P33 (F-3) and
   F-12.
2. **The 11 collisions.** Take upstream's (recommended; closes D-57; loses Raptor pack friends) or keep ours (no
   loss, but new hidden replacements)? If upstream's: purge on the test shard first (no prompts at boot), or answer
   `a` twice on the attached console at first boot?
3. **Compose mounts (Q-009, your call).** Mount the parent directory for live and test, with test moving to its own
   `lib/uo/modernuo-test/`? It is needed before any save on the new engine; it can land now, on pinned.
4. **`pathfinding.prebakeMaps`.** `"False"` (recommended) or `"True"` plus a volume for `/modernuo/Data/Pathfinding`?
5. **Craft replacements.** Convert `CraftItem.cs` and `CraftContext.cs` to `.patch` files inside the bump (+1-2 units,
   recommended), or keep them as replacements?
6. **Live shard.** Leave it on pinned until the wipe (recommended), or bump it with the test shard? Its save is clean.
7. **D44.** Send the draft to hi@modernuo.com?
8. **Scratch.** `D:\UO\cc-p30-upgrade-work` (copies of both saves, with accounts, and of both configs) and the two
   trial images (`sl-modernuo:cc-p30-trial`, about 1.3 GB; `sl-uo-builder:cc-p30-trial`, about 5 GB, last built from
   the `045b313` copy) are still on disk. Keep them for P36, or delete them?
9. **Housekeeping, not urgent.** The `cc-P29-registrar-office-cleanup.md` / `cc-P31-...` duplicate in
   `D:\UO\cc-prompts`, and `AGENTS.md`'s "no fresh world" against the planned wipe.

## Files from this task

- `notes\cc-P30-tools\`
  - `patch-survey.sh` (patch survey)
  - `type_delta.py` (collision finder)
  - `stage-tree.sh` and `rebuild.sh` (local compile loop)
  - `group_errors.py` (error grouping)
  - `v4_saveflag.py` (attribute rewriter)
  - `hook_audit.py` (merge placement audit)
  - `trial-changes-d4531cd9.diff` (the trial delta on `56cae9d`, 51 files).
  - `trial-changes-head-045b313.diff` (the same plus the P32 fixes on `045b313`, 54 files; **the one to replay**).
  - Both carry upstream code verbatim, so they are not ASCII-clean.
- Scratch, not in any repo: `D:\UO\cc-p30-upgrade-work\` (trial copy with its git history, survey output, build and
  boot logs, merge inputs, load-test copies) and `D:\UO\ModernUO-upstream` (fresh clone).
