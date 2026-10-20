# cc-P193: port High Seas, the fishing half (first sitting)

Written 2026-10-20 by the Bronze Golem (Fable), on branch golem/Bronze/P193 of both repos. Prompt:
`cc-prompts/cc-P193-port-high-seas-fishing.md`. Both repos were clean at the start. Not committed: the Golem commits after
DONE. Pinned paths are relative to `D:\UO\ModernUO-pinned\Projects` (d4531cd9); ServUO paths to
`D:\UO\ServUO-pub57\Scripts`; "ours" is `server\customizations\Services\Expansions\High Seas` unless said otherwise.

## Headlines

1. **The row moves from 4 of 59 files to 27 of 59** (progress.py, stem proxy, `SL_SHARD` at the Bronze copy). What is in:
   the whole fish catalogue (42 common High Seas fish in three pools, 20 crabs and lobsters, 16 rare and 19 legendary
   fish with their 13 steaks and 3 meats, and the FishInfo table that says where each is caught), the lobster trap and
   the lava lobster trap, the fish trophies, the two sea champions (Charybdis, Osiredon the Scalis Enforcer) with their
   spawn (giant tentacle, parasitic eel), ten of their artifacts, the yellow polka dot bikini, the four human pieces of
   the Fisherman's set, and four of the pies' ingredients. The 23 stems counted are listed in section 1; ServUO's
   `Fish.cs` is ported too but its stem is pinned's, so the proxy does not count it.
2. **Players get it from a fishing pole and a lobster trap, through two small patches** (section 2): pinned
   `Engines/Harvest/Fishing.cs` asks `FishInfo.GetSpecialItem` first when a cast succeeds (from 50 Fishing a High Seas
   fish of the water, and the rare and legendary fish at ServUO's places, chances and skills), leaves a rare fish alone
   in `MutateType`, weighs and signs it in `Give` and announces it in `SendSuccessTo`; pinned `TaxidermyKit` makes a fish
   trophy deed from a rare fish, crab or lobster. Both patches are hooks into our own additive files.
3. **Left for the next prompt** (section 5): the baits and hooks (they need bait and hook fields on pinned's
   FishingPole: a stock saved type to bump), the Oracle of the Sea and the charybdis spawner (they need the pole's bait),
   lava fishing with a pole and the lava items, the fish pies (ten engine hooks across AOS, Spell and soul charge), the
   profession fish quests (ServUO's quest framework, which pinned lacks), the bikini's place in the SOS chest roll, the
   four gargish set pieces, and Corgul (the prompt excludes it). None of it blocks what is in: the fish are caught, the
   traps work, the trophies hang, the champions fight and drop.
4. **Where the port met the shard's rules.** The chance of a common High Seas fish grows with Fishing as skill / 121.5;
   with the shard's 200 cap a player counts at most at OSI's 120 there (cc-P67 B's `ClusterFSkillClamps.FishingFindSkill`,
   the same clamp the deep-water finds already use), or every cast past 121.5 would be a High Seas fish. The per-fish
   minimum skills (81.9 to 120) are ServUO's and read the real skill.
5. **Deviations** (section 4, D-132 to D-140 proposed): boats are pushed but not damaged (pinned boats have no hull
   points); no fish-finder school bonus; the corpses hold a plain fishing pole and no fish pies yet; three missing hit
   attributes on the artifacts (HitManaDrain is D-75 already; HitFatigue and BattleLust are new); Osiredon's shared list is
   empty (no mini soul forge deed); two ServUO bugs fixed rather than copied, each argued; the Wand of Thundering Glory
   carries a dummy wand effect at zero charges.
6. **Client check: nothing blocked.** Every item id the port uses (fish 17154-17159, 17603-17606, 17637-17638, crabs and
   lobsters 17617-17620, the trap 17615-17616 and buoy 17611, trophies 17639-17646, 18106-18109, 19280-19287, the addons
   14240 and 14284, the ingredients 2454, 2463, 3352, 11235) is named in the client's tiledata (read from the
   7.0.116.0 UOAlive copy at `D:\UO\UOAlive`, the shard's 7.0.117.0 being another desk; High Seas art is 7.0.9+ in both),
   and the three bodies (1244 Water Spirit, 1245 its tentacle, 1068 Scalis) are in mobtypes.txt.
7. **Tests: nine facts in `server\tests\Services\HighSeasFishingVerification.cs`, each seen red by its own break**
   (section 3), then the full suite green and the image built.
8. **For the integrator:** `CHANGELOG.md` gains a `## 2026.10.20` section above `## 2026.10.19.5` and VERSION becomes
   2026.10.20. Branches P202 (P191's lines inside 2026.10.19.5) and P203 (a `## 2026.10.19.6` section above it) touch the
   same lines, so whichever merges after another will stop on CHANGELOG.md; keep every section in version order (.20
   above .19.6 above .19.5, P191's lines inside .5) and the highest VERSION. Nothing else overlaps with either branch.

## 1. What was ported, with file:line

All under `server\customizations\Services\Expansions\High Seas\` at ServUO's own paths, so apply-patches.sh mirrors them
into `Projects/UOContent/Services/Expansions/High Seas/`.

| ServUO file | Ours | What, and what changed |
|---|---|---|
| `Items/Fish/Fish.cs` (1,176 lines) | `Items/Fish/Fish.cs` (468) | `BaseHighseasFish` (stackable commodity, carves to raw fish steaks, the six type pools) and 42 common fish. Generated by the session's `gen_fish.py` from the ServUO file, boilerplate removed; the bases are hand-written. ServUO's Carve refused inside a quest ShippingCrate and carried a Caddellite socket: neither exists here |
| `Items/Fish/CrabsAndLobsters.cs` (702) | same (303) | `BaseCrabAndLobster` (two stones, no carve of its own), `RareCrabAndLobster` (fisher, date), 6 crabs, 6 lobsters, 4 rare crabs, 4 rare lobsters, the plain `Crab` and `Lobster`, 3 meats |
| `Items/Fish/RareFish.cs` (737) | same (380) | `RareFish` (fisher, date, the "Caught by" tooltip), 13 rare fish, 13 steaks |
| `Items/Fish/LegendaryFish.cs` (368) | same (179) | 14 of the 19 legendary fish (the other five, the rare crabs and lobsters, are in CrabsAndLobsters.cs) |
| `Items/Fish/FishInfo.cs` (449) | same (~330) | the 36-row table and `GetSpecialItem`, `GetBaitStrength`, `Roll`, the water tests. Built lazily (no Configure plus a ten-second timer); no MagicalFishFinder; bait read from a trap only; the skill clamp (headline 4); no SOSArtifacts array (pinned fills its own SOS chests); `IsFireIsland`'s dead second rectangle copied as it is |
| `Items/Fish/Trophies.cs` (415) | same (~380) | `FishTrophyDeed`, `FishTrophy`, `TrophyComponent`, `TrophyStyle`, plus `FishTrophies` (the 35 fish rows ServUO keeps in TaxidermyKit's private table, and `TryMake`, the kit patch's hook). Pinned `BaseHouse.Addons` is a list, so taking a trophy down is the co-owner test alone |
| `Items/LobsterTrap.cs` (472) | same (~450) | the trap (section 2.3). ServUO's party test passed two unpartied strangers; here the party must exist (D-4 rule: broken is fixed). Bait as an index int, -1 none |
| `Items/LavaLobsterTrap.cs` (36) | same | the lava trap; `LavaTiles` (ServUO's `Fishing.LavaTiles`) lives here since pinned Fishing has none |
| `Items/Resources/Cooking Ingrediants.cs` (177) | same | `MentoSeasoning`, `SamuelsSecretSauce`, `DarkTruffle`, `FreshGinger`. Not `FishOilFlask`: pinned declares one (`Items/Misc/OilFlask.cs`), the first build cycle's duplicate-type failure; the Oracle it charges is next prompt's |
| `Mobiles/BaseSeaChampion.cs` (274) | same | the champion base: damage tracking through pet masters, `AwardArtifact` (ServUO's shape, roll over eligible damage, walk over all), boat push without damage, `GetValidPoint` with the classic boat's size |
| `Mobiles/Charybdis.cs` (776) | same | `Charydbis`, `GiantTentacle`, `CharydbisEffectSpawn` (ServUO's nested `EffectSpawn`, top-level for the generator). Tentacle list not saved on the champion (each tentacle saves its master and re-registers) |
| `Mobiles/OsiredonTheScalisEnforcer.cs` (374) | same | `Osiredon`, `ParasiticEel` (ServUO's `Poison.Parasitic` is its DeadlyParasitic, `Server/Poison.cs:56`; pinned has `Poison.DeadlyParasitic`) |
| `Items/Artifacts/{CullingBlade, RuneEngravedPegLeg, HelmOfVengence, SmilingMoonBlade, WandOfThunderingGlory, EnchantedCoralBracelet, RingOfTheSoulbinder, LeviathanHideBracers, EnchantedBlade, EnchantedVortex}.cs` | same ten | the champions' artifacts. `LeviathanHideBracers` goes on `BaseSetArmor` (it carries `AbsorptionAttributes.CastingFocus`; the final-parent rule) with LeatherArms's members inlined. Not the three Corgul files (`CorgulsEnchantedSash`, two handbooks) |
| `Items/SOS Artifacts/YellowPolkaDotBikini.cs` | same | the bikini |
| `Items/Sets/FishermansSet.cs` (525) | same (~190) | `IFishingAttire` and the four human pieces on `BaseSetClothing` / `BaseSetArmor` with the stock bases' members inlined (the Hunter and Sorcerer sets' way) |
| `server/patches/Fishing-high-seas-fish.patch` (new) | | four hunks in pinned `Engines/Harvest/Fishing.cs`, after `Fishing-deep-water-finds-osi.patch` (section 2.1) |
| `server/patches/TaxidermyKit-fish-trophies.patch` (new) | | one hunk in pinned `Items/Skill Items/Carpenter Items/TaxidermyKit.cs` (section 2.2) |
| `docker/uo/apply-patches.sh:547-552` | | the two patches registered after the deep-water one |
| `server/tests/Services/HighSeasFishingVerification.cs` (new) | | nine facts (section 3) |
| `CHANGELOG.md`, `VERSION` | | `## 2026.10.20` (Added x4, Staff x1); VERSION 2026.10.20 |

The 23 stems the port list now counts for this row: CrabsAndLobsters, FishInfo, RareFish, LegendaryFish, Trophies,
LobsterTrap, LavaLobsterTrap, Cooking Ingrediants, BaseSeaChampion, Charybdis, OsiredonTheScalisEnforcer, CullingBlade,
EnchantedBlade, EnchantedCoralBracelet, EnchantedVortex, HelmOfVengence, LeviathanHideBracers, RingOfTheSoulbinder,
RuneEngravedPegLeg, SmilingMoonBlade, WandOfThunderingGlory, YellowPolkaDotBikini, FishermansSet; plus the four already
there (BlackPowder, Charcoal, Potash, SaltPeter) = 27. Fish.cs is ported but not counted (stem "Fish" is stock).

Not ported from the row's prefixes, each with its reason, in section 5.

## 2. How a player reaches it

### 2.1 The Fishing patch (`Fishing-high-seas-fish.patch`)

Pinned `HarvestSystem.FinishHarvesting` (`Engines/Harvest/Core/HarvestSystem.cs:146-162`) calls, on a successful skill
check, `GetResourceType`, then `MutateType`, then `Construct`, then `Give` and `SendSuccessTo`. ServUO's Fishing overrides
`GetResourceType` to ask FishInfo first (`Services/Harvest/Fishing.cs:919-927`), guards `MutateType` for a rare fish
(`:259`), stamps a rare fish in `Give` (`:559-573`) and names a High Seas fish in `SendSuccessTo` (`:644-657`). Pinned
Fishing overrides the last three already and not the first, so the four hunks are:

- `GetResourceType`: `FishInfo.GetSpecialItem(from, tool, loc, false) ?? base.GetResourceType(...)`.
- `MutateType`: `if (FishInfo.IsRareFish(type)) return type;` before the find table.
- `Give`: fisher, date, `Stackable = false`, weight `max(1, 200 - sqrt(random 0..40000))` for a `RareFish`.
- `SendSuccessTo`: a `BaseHighseasFish` says 1043297 with "a rare fish", "a fish" or `#label`.

Alternatives weighed, as `docs/subsystem-policy.md` asks before any patch to an upstream file:

1. **A partial-class file adding `GetResourceType` only, no patch.** Pinned `Fishing` is not `partial`, so this needs a
   one-line patch anyway (apply-patches.sh already seds Lumberjacking.cs partial), and `MutateType`, `Give` and
   `SendSuccessTo` are already overridden in pinned Fishing, so a partial file cannot add to them: a rare fish would be
   swapped for a boot or a net at the find table's odds, would not be weighed or signed, and the catch message would be
   the stock one. Rejected: three of the four behaviours need edits inside existing overrides.
2. **Replacing `Fishing.cs` wholesale** (the `replace_file` route). Hides upstream drift; the file is 549 lines of which 20
   change. Rejected per AGENTS.md ("a replacement hides upstream drift").
3. **A subclass `HighSeasFishing : Fishing` installed as `Fishing.System`.** `_system` is a private static with a
   get-only property, and `Fishing`'s constructor is private; both need a patch, and the pole's `Fishing.System` reads
   would then run a type pinned never tests. Rejected: more patch surface than the hunks, for no gain.
4. **The four hunks (chosen).** 32 added lines, no removed lines, each hunk a comment naming its ServUO line, applied
   after `Fishing-deep-water-finds-osi.patch` (cc-P67 B) which touches `MutateType`'s loop, so the two hunks in that
   method do not overlap. The patch was produced by applying the deep-water patch to pinned's file in the scratchpad and
   diffing the edited copy, so it applies on the real tree in that order (dry-run clean, then four build cycles).

### 2.2 The TaxidermyKit patch (`TaxidermyKit-fish-trophies.patch`)

One hunk: after the Carpentry 90 test in `CorpseTarget.OnTarget`, `if (FishTrophies.TryMake(from, _kit, targeted)) return;`.
ServUO adds 35 rows to TaxidermyKit's own private table and two branches to the target (`Items/Consumables/TaxidermyKit.cs:
236-268`); here the rows and the branch live in our `Trophies.cs` and the kit asks once. Alternatives: patching the 35
rows into pinned's `_table` (a larger patch over a stock list that pinned may change) or a second kit type (not ServUO's,
a wiki difference). The hook is the smallest.

### 2.3 The lobster trap

Double-click the trap in the pack, target water (or lava, for the lava trap) within six tiles: it becomes a buoy at the
spot, bobs once a minute (`**bob**` overhead), each bob trains Fishing (deep water only from 75), is lost with chance
5% x bobs so far (the buoy "is pulled beneath the waves", everyone within 12 tiles hears), else rolls
`FishInfo.GetSpecialItem` for a crab or lobster (a rare one is signed, dated, weighed 10 to 200 and made one catch) or,
half the time, a plain crab or lobster. Double-clicking the buoy (or Telekinesis on it) pulls it and its catch back to
the pack; double-clicking the trap in the pack dumps the catch. Owner, guild, party; in Felucca anyone, as a crime.

## 3. Tests

`server\tests\Services\HighSeasFishingVerification.cs`, nine facts, run through the gate (`docker/uo/build.sh -t
sl-modernuo:cc-P193`, `--tests-only` for the compile cycles), the docker-build lock held and released after. Logs
`build-P193-cycle1.log` to `build-P193-cycleN.log` in the session scratchpad.

| Cycle | Tree | Result |
|---|---|---|
| 1 (`--tests-only`) | the port as first written | builder stage red: the serialization generator refused a second `FishOilFlask` (pinned has one, `Items/Misc/OilFlask.cs`). Removed from Cooking Ingrediants.cs; every other new type name checked against pinned and ours (148 names, one collision) |
| 2 | | red: `TreasureMapChance` has no pinned member (both champions). Dropped, D-139 |
| 3 | | red: `ValueLinkList<DamageEntry>` needs `using Server.Collections` to enumerate; `HitManaDrain` and `HitFatigue` are not pinned weapon attributes. Fixed and dropped, D-75 and D-135 |
| 4 | | red: the fact file lacked `using Server.Engines.CannedEvil` |
| 5 | | compiles; **1,558 tests, 1,550 passed, 4 failed**, all four mine: the round-trip helper built the base type (a `RareFish` variable holding a BlueMarlin), the table has 36 rows not 35 (ServUO has 19 legendary fish; my count was wrong), Osiredon has 65,000 hits (pinned's clamp, D-140), and `EquipItem` refuses a hat in the host (AddItem, as the set tests do) |
| 6 | | 1,558 tests, 1,553 passed, 1 failed: a tentacle's master came back null after a round trip. Probed inside the builder image (a copy of the fact with `World.FindMobile` printed): the champion itself had been round-tripped earlier in the fact, and deleting the copy, which carries the same serial, drops that serial from the world. The fact's order, not the port; the champion round trips moved to the end |
| 7 | | 1,558 tests, 1,553 passed, 1 failed: `WispOrbPossessionVerification` ForestNymph vs Phantom, the known flaky fact (D56; cc-P50, P135, P142 saw it), unrelated; all nine of mine green |
| 8 (red) | the nine breaks, first cut | the **patch gate** failed the build: two breaks deleted `+` lines from the patches, so their hunk counts no longer matched. A gate seen failing, if not the one meant; the two breaks rewritten to swap a line each |
| 9 (red) | the nine breaks | **1,558 tests, 1,545 passed, 9 failed, each of my nine facts by its own break** (table below); everything else green, the wisp orb fact included |
| 10 (full) | restored, hashes byte-identical to the pristine snapshot (eight files) | **green: 1,558 tests, 1,554 passed, 4 skipped, 0 failed; image `sl-modernuo:cc-P193` built** (label sl.commit=7083632 and sl.dirty=1, the branch being uncommitted) |

Before cycle 1: free memory 10 GB of 31.7 GB; docker-build lock taken 11:23 and released 11:53 (the cycles run detached from
the agent shell, logs in the session scratchpad). The two probe runs (cycle 6) ran `dotnet test` on the builder image with
the fact file bind-mounted over its copy, about a minute each, no lock needed and no image touched.

The breaks (`p193_breaks.py` in the session scratchpad; pristine copies snapshotted first, hashed before and after):

| Fact | Break | Red |
|---|---|---|
| 1 every fish constructs, has a label, round-trips | `Amberjack.LabelNumber => 0` | "Amberjack has no label" |
| 2 the table has 36 rows and knows its indexes | the charybdis row removed | Expected 36, actual 35 |
| 3 the pole gives shore fish from 50 and the trap crabs | shore pool from 40 Fishing | Assert.Null: a pole at 49.9 gave PumpkinSeedSunfish |
| 4 bait strength | enhanced bait 2.5, not 3.0 | Expected 3, actual 2.5 |
| 5 the Fishing patch hands out fish and signs a rare one | the `rare.Fisher = m` line dropped from the patch | Assert.Same: the marlin's Fisher is null |
| 6 the trap bobs, catches crabs, is lost by the twentieth bob | a bob counts two | Expected -4, actual -3 |
| 7 the kit makes a deed and the deed builds the addon | the `TryMake` hook dropped from the kit patch | "the fish was not used up" |
| 8 the champions construct, round-trip, spawn, award | the tentacle does not register with its master | Expected 1 tentacle, actual 0 |
| 9 the artifacts and the set | the vest says five pieces | Expected 4 pieces, actual 5 |

What the facts cannot cover here: the test host has no tile data (D27), so deep water and the shore-versus-dungeon test
by tile are exercised through regions only (fact 3 registers a Twisted Weald region); a cast through
`FinishHarvesting` on a real water tile, the trap's `OnTarget` on a real tile, and the catch message on the wire are the
play tests below.

## 4. Deviations and decisions for Chase

The register ends at D-122 in `docs\fidelity-principle.md`; D-123 to D-131 are proposed in cc-P66, P67, P71 and P150. These
are proposed as D-132 onward; agents do not edit `docs\`.

| D | What | Why | Reverses when |
|---|---|---|---|
| D-132 | A sea champion pushes a boat but does not damage it (ServUO: 5-15 or 3-8 hull damage, `BaseBoat.OnTakenDamage`) | pinned boats have no hull points | High Seas ship combat is ported |
| D-133 | No fish-finder "school": a rare fish's chance is never multiplied by ten | `MagicalFishFinder` is not ported | the fish finder is ported |
| D-134 | Charybdis's corpse holds no fish pies (ServUO: 2-5), and both champions drop a plain fishing pole (ServUO: 2-5 magic attributes) | the pies need ten engine hooks (section 5); pinned's pole has no attributes | the pies land; the pole patch lands |
| D-135 | Culling Blade without HitFatigue 30; Smiling Moon Blade without BattleLust 1 (HitManaDrain on both is D-75) | pinned `AosWeaponAttribute` has neither (`Misc/AOS.cs:755-790`; BattleLust is a TODO at `Items/Weapons/Throwing/StormCaller.cs:12`) | the two attributes exist |
| D-136 | Osiredon's shared artifact list is empty (ServUO: MiniSoulForgeDeed), so the 10% shared roll gives nothing | no mini soul forge deed in pinned or ours | a mini soul forge deed exists |
| D-137 | Wand of Thundering Glory carries WandEffect.Clumsiness at zero charges (ServUO: WandEffect.None) | pinned's enum has no None; at zero charges nothing casts and the name is the label | a None effect exists |
| D-138 | Two ServUO bugs fixed, not copied: Charybdis's wave spouts read the land tile at the path offset, so they never appeared (now the world point); SpawnTentacle rolled x and y from mixed bounds (now each axis its own). And the trap's party test (headline 1 of the trap) | each made OSI's visible behaviour silent or wrong: broken is fixed (D-4 rule) | never |
| D-139 | `TaintedLifeAura` (Osiredon), `SkillMasteryPrimer` drops, `IsSoulbound`, `TreasureMapChance .50` on both champions | none exists in pinned (TreasureMapChance as CC4 recorded for Shame) | each lands |
| D-140 | Osiredon has 65,000 hits (ServUO: 75,000) | pinned `BaseCreature.HitsMax` clamps at 65,000 (`Mobiles/BaseCreature.cs:1043`); found by fact 8, not by reading | the clamp is raised |

Decisions for Chase:

1. **The second sitting's order** (section 5). The baits and hooks come first because the Oracle, the charybdis spawner
   and lava fishing all wait on the pole's bait and hook fields; that is a version bump of pinned's `FishingPole` (a stock
   saved type, the TreasureMap route of cc-P127) and is why it did not fit this sitting.
2. **Where the fish are.** The FishInfo rows name regions (Shame, Destard, Doom, Ice, Terathan Keep, Labyrinth, Prism of
   Light, Twisted Weald, Underworld, Abyss, Gravewater Lake) and maps (Trammel, Felucca, Tokuno, Ilshenar, TerMur). The
   shard's `Configuration/expansion.json` says Endless Journey, so every one is in scope, but which of those regions is
   loaded and has water is not something this prompt could verify headlessly (the rule: configured is not present). The
   play tests below start with the shore and Trammel's deep water.
3. **The common-fish clamp** (headline 4) is cc-P67 B's rule applied to a new place; say if the shard's 200-skill fisher
   should instead see a High Seas fish on every cast.

## 5. Left for the next prompt

| Piece | ServUO files | Why not this sitting | Cost |
|---|---|---|---|
| Baits and hooks | `Items/Fish/Bait.cs` (274), `Hooks.cs` (245) | the pole carries BaitType, EnhancedBait, BaitUses, HookType, HookUses and the fish-attire bonus; pinned `FishingPole` is a 50-line saved type with no fields: a version bump with a migration (cc-P127's TreasureMap route) plus `OnFishedHarvest` hooks in `FinishHarvesting` | medium; one patch or replacement, two files |
| Oracle of the Sea, charybdis spawner | `Items/OracleOfTheSea.cs` (57), `Spawners/CharybdisSpawner.cs` (343), `Persistence.cs` (94) | the spawn fires from `Fishing.SpecialHarvest` when the pole is baited for charybdis; also `FishOilFlask` (pinned has a type of that name) | after the baits |
| Lava fishing | `Items/LavaFishItems.cs` (407), the lava hunks of ServUO `Fishing.cs:789-1060` | the lava hook, `GetDefinition` for lava tiles, and the cracked lava rocks are cracked by a pickaxe (`Services/Harvest/Core/HarvestTarget.cs:85`, a pinned HarvestTarget patch) | medium |
| Fish pies | `Items/Fish/FishPies.cs` (690) and Cooking recipes | 16 pies whose effects are read in ten places pinned lacks: `AOS.cs:188, :663, :695, :810, :837, :849, :865, :883`, `Spell.cs:271`, `SAPropEffects.cs:193`; the shard's `CookingCraftRegistrations` can take the recipes | large; a patch set |
| Profession fish quests | `Quests/ProfessionFishQuest/*` (12 files, 2,796 lines) | ServUO's `BaseQuest`/`BaseObjective` framework (the Mondain's Legacy quest framework, 21 files, `docs/subsystem-policy.md`) is in neither pinned nor ours; the FishMonger stands in the Sea Market (ship content) | a subsystem decision |
| The bikini in SOS chests | ServUO `Fishing.cs` Construct | pinned's `Fishing.Construct` fills SOS chests from its own list; one more hunk | small, with the pole patch |
| Gargish Fisherman's pieces | `Items/Sets/FishermansSet.cs` lower half | GargishPlateChest and GargishEarrings have no pinned equivalent; the kilt and arms do (`GargishClothKiltType1/2`, `GargishLeatherArmsType1/2`); none drops here (Corgul's) | with Corgul |
| Corgul and his altar, region, soulbound crew | `Mobiles/Corgul/*` (8), `Items/CorgulAltar.cs`, `Regions/CorgulRegion.cs`, three Corgul artifacts | the prompt excludes Corgul (ship content) | a prompt of its own |
| `MatchCord.cs`, `Niter.cs` | `Items/Resources/` | cannon resources, the naval half | with ship combat |

## 6. For Chase

**Rebuild the test shard** (console, Test shard, Rebuild) before trying these.

1. **Fish the shore:** with Fishing 60 and a pole, fish from a dock or beach (Trammel, `[go 3450 2560 2` by the New Haven
   docks) for a few minutes: beside the usual fish you pull up named shore fish (a yellow perch, a walleye, a brook
   trout; "You pull out an item: a brook trout"), four stones each, which carve into four raw fish steaks.
2. **Fish deep water:** with Fishing 85 on a boat out at sea (deep water for 25 tiles around), the catch adds ocean fish
   (a mahi mahi, an amberjack, a yellowfin tuna); from 106 in a dungeon's water (Despise, Shame) dungeon fish (a demon
   trout, an orc bass). A rare fish is rare (0.75% a cast where it lives) and legendary rarer (0.1%): `[add BlueMarlin`
   and `[add VoidLobster` to see one hued and signed ("Caught by", a date, one catch, its own weight).
3. **Lobster trap:** `[add LobsterTrap`, double-click it and target water within six tiles: it becomes a buoy, bobs once
   a minute, your Fishing rises, and after a few bobs double-click the buoy: it returns to your pack with crabs and
   lobsters in it (double-click the trap in the pack to dump them). Leave one out twenty minutes and it is gone.
4. **Trophy:** with Carpentry 90, `[add TaxidermyKit`, ten boards and `[add BlackMarlin` (set Weight 150 in `[props`):
   double-click the kit and target the marlin: a "Black Marlin Trophy" deed; in your house, double-click it facing a wall:
   a three-piece marlin hung on the wall, hued dark blue, showing 150 stones and "Caught by". Chop it: the deed is back.
5. **The champions (staff):** on a boat at sea, `[add Charydbis`: it raises tentacles around the boat, every minute hides
   and strikes everyone aboard with lightning, and sends a wave that shoves the boat; `[add Osiredon`: water balls that
   dismount, fire bursts, eels when you cast at it. `[kill` either: fish steaks, a message in a bottle, nets and a pole
   in the corpse, an artifact to a damager now and then (`[add CullingBlade`, `[add FishermansHat` to see them).
6. **The set:** `[add FishermansHat`, `[add FishermansVest`, `[add FishermansEelskinGloves`, `[add FishermansTrousers`,
   wear all four: the set bonus lights; the trap and pole read their bait bonus once baits land.
7. **Test world boot:** done by CC on a scratch copy (section 7).

## 7. Headless boot

`sl-modernuo:cc-P193` on a copy of the overnight bot's scratch world (`D:\UO\bot-shard\world\Saves`, 29 MB, the newest
world this desk may read; the test shard's own backups live on another desk), the world folder mounted as the compose file
mounts it (`/var/lib/uo/modernuo`), client data from the 7.0.116.0 UOAlive client folder (the image detected 7.0.116.0
and restricts clients to 7.0.117.0 as configured), loopback only, no port published, autosave off, under the test-shard
lock (12:01 to 12:08). The running test shard and the bot's own world were not touched.

- boot 2 (the first with the folder mounted right): `[ShardVersion] Shattered Legacy 2026.10.20 (103 version(s) in the
  changelog)`, `Loading world done (210896 items, 35139 mobiles) (2.76 seconds)`; stopped with `docker stop`, which the
  shard's SaveOnShutdown (D36) turns into a save: `Saving world done`, `Writing world save snapshot done`, `...saved in
  1088 ms`, `Shutting down`.
- boot 3 on that save: `Loading world done (212643 items, 35326 mobiles) (2.41 seconds)` (the seeders' additions), saved
  the same way on stop. Zero `Exception` lines in either log.
- boot 1 before them taught two things: with `Saves` mounted on its own (the recipe's older invocation) the staged save
  cannot rename over the mount point and fails (`IOException: Cannot create '/var/lib/uo/modernuo/Saves'`), so mount the
  parent folder as the compose file does; and once the harness backgrounds a piped `docker run -i`, neither the pipe nor
  `docker attach` reaches the console, so the save is the SIGTERM one.
- Nothing in that world is a type of this port yet; the patched `Fishing` and `TaxidermyKit` add no field to any saved
  type, so no migration JSON was needed, and every item and mobile the world holds loaded and saved as before.

**Not done:** a client. Nothing here was seen in game.

## Play-test items added

Through the For Chase list above; Who and steps in `testing/bot-triage.md` (P193 group) and `testing/playtest-steps.json`:
P193-1 BOT-PARTIAL (shore fish), P193-2 EYES (deep and dungeon fish), P193-3 BOT (lobster trap), P193-4 BOT-PARTIAL
(trophy), P193-5 EYES (the champions), P193-6 BOT-PARTIAL (the set), P193-7 CC (test world boot).

## Repo size rule

No new file over 5 MB: the largest is `Fish.cs` at about 15 KB. Scratch (the generator, the break script, the pristine
copies, the patch work trees, the build logs) is in the session scratchpad, outside both repos.

## Commit preflight

`Commit-ShardWork.ps1 -DryRun -NoRefresh -NoArchive -Branch golem/Bronze/P193 -CodeRepo D:\UO\golems\Bronze\ShatteredLegacy
-DocsRepo D:\UO\golems\Bronze\shard-migration`, 2026-10-20 12:09 (the script's defaults are the main checkouts, other
desks). Neither repo BLOCKED. No file over 5 MB in either repo (find -size +5M: none). Every touched file is ASCII. The
docker-build lock (11:23-11:53) and the test-shard lock (12:01-12:08) were taken and released; no package or haven lock
was needed; nothing was placed in any world and no live config was changed.

```
=== code  (D:\UO\golems\Bronze\ShatteredLegacy) ===
  30 file(s) pending:
    CHANGELOG.md
    VERSION
    docker/uo/apply-patches.sh
    server/customizations/Services/Expansions/High Seas/... (24 .cs files: Items/Artifacts x10, Items/Fish x6,
      Items/LobsterTrap.cs, Items/LavaLobsterTrap.cs, Items/Resources/Cooking Ingrediants.cs,
      Items/SOS Artifacts/YellowPolkaDotBikini.cs, Items/Sets/FishermansSet.cs, Mobiles x3)
    server/patches/Fishing-high-seas-fish.patch
    server/patches/TaxidermyKit-fish-trophies.patch
    server/tests/Services/HighSeasFishingVerification.cs
  dry run: would add, commit and push

=== docs  (D:\UO\golems\Bronze\shard-migration) ===
  7 file(s) pending:
    README.md
    dashboard.html
    testing/bot-triage.md
    testing/playtest-steps.json
    tools/expansion-coverage.json
    tools/progress.json
    notes/cc-P193-port-high-seas-fishing.md
  dry run: would add, commit and push

Repo Result
---- ------
code dry run
docs dry run
```

`tools/progress.py` was run with `SL_SHARD` at the Bronze copy (README block, dashboard, progress.json and
expansion-coverage.json above are its output): Port list 478 of 983 files (49%), this row 27 / 59.

P193 DONE
