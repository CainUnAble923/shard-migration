# Port assessment: servuo.dev code downloads (cc-P93, 2026-10-13)

Read-only assessment of the code that the daily art task downloaded from servuo.dev on 2026-10-13, judged for a
port to the shard's ModernUO. Nothing here was built, run, installed or extracted. Copies:
`D:\UO\third-party\code\PORT-ASSESSMENT.md` and `D:\UO\shard-migration\notes\servuo-code-port-assessment.md` (the
project copy, for Chase to add to the Claude project as `claude/servuo-code-port-assessment.md`).

**Baseline.** Engine citations are from `D:\UO\ModernUO-pinned` at **d4531cd94**, the commit the shard runs
(AGENTS.md); paths are under `Projects\`. ServUO citations are from `D:\UO\ServUO-pub57`. Shard citations are from
`D:\ShatteredLegacy\server`. Statements marked **(guess)** were not verified.

**Frame.** Chase's direction (2026-10-13): a faithful port comes first, our feature customizations after it. The
agreed port list (`notes\port-list-2026-10-13.md`, `tools\port-list.json`) is the faithful port. Every module below
is custom content, so none of it goes into the port list or its headline. It belongs to the separate custom lane
(`docs\community-scripts-wishlist.md` rules: license first, design description not a file to copy, base-class edits
argued first, anything player-facing gets a wiki entry). Staff-only tools carry no fidelity or wiki cost, so they can
run at any time without jumping the port queue.

## Summary

| Module | Serves | Effort | ModernUO blockers | License | Recommendation |
|---|---|---|---|---|---|
| Vita-Nex Core 5.3.1.0 | Library for Power Hour and the Vault modules | L (months) | Packet internals, SuperGump entries, 16 EventSink events, side-file IO | MIT | **Skip** the port; rebuild modules natively |
| Power Hour (Vita-Nex) | Play-test gain boosts; none in the feature queue | S, rebuild | Needs Vita-Nex Core (CoreModule, SuperGumps, TimeBoosts, BinaryDataStore) | none stated (Vita-Nex community) | **Borrow the idea only**, if wanted |
| Hunter's Bestiary | F-24 monster hunts, F-13 achievements | M | No `OnBeforeDamage`; EventSink; XML side file; 10 creatures missing | none stated | **Port later** (rebuild), with F-24 hunts |
| Tamable specimen rating | Companions, F-35 evo pets, breeding | S, rebuild | XmlAttachment cache; no `GetProperties` override | none stated | **Port later** (rebuild), after Pet Training |
| Animal Lore dashboard | Pet Training port, Animal Lore to 200 | M, after Pet Training | Needs OSI pet training (ModernUO has none); ShrinkSystem; ServUO `BaseGump` | GPL-3.0 header; derived from GPL ServUO | **Port later**, right after the Pet Training port |
| Virtual storage chests | Bulk reagents, herbalism, resource storage | M, rebuild | Hand serialization; house access (`ISecurable`) | none stated | **Borrow the idea only**: High exploit findings |
| Craft from bank | F-34 bank access item | S-M | Patches CraftItem where our patch already sits; signatures changed | none stated (AI-written) | **Skip**: F-34 already has our engine |
| Visual Builder | Staff building, F-21, server-placed buildings | S | Gump signatures, enumerator `.Free()` | none stated | **Port later** (staff tool), with an undo fix |
| Building Duplicator | Staff tool, guild halls, New Haven layouts | S | Gump signatures, `GetStaticTiles` overload | none stated | **Port now (adapted)**: write our layout JSON |
| Invasions (Feng) | F-30 Events tab surges, League culling | M | ServUO `Persistence`, `GuardedRegion.Disabled` | **GPL-3.0** | **Borrow the idea only** |
| Apex Hunt | F-24 League hunts, events | M | EventSink, raw `BinaryWriter` save, `Serial` width | permissive ("free to use, distribute, and modify") | **Port later**, as the F-24 hunt skeleton |
| UORespawn | Spawning | L | Separate MUO script set, target version unstated | MIT per GitHub README (verify) | **Borrow the idea only**: fights stock spawns |
| Runebook / Runic Atlas gump | Travel UI | S (reorder) | Needs Vita-Nex `Swap`; pinned gump is a `DynamicGump`; no RunicAtlas in pinned | none stated | **Borrow the idea only** (rune reordering) |
| Seagulls, Butterflies | New Haven ambience | S | Trivial | none stated; **art ripped from other games** | **Skip the art**; stock-body ambient critters if wanted |
| Level System Extreme | F-12 levels | Rebuild | XmlSpawner fork, 9 distro edits, gone EventSink events | none at all | **Borrow the idea only** (already F-12's ruling) |
| Client plugins | Player package | n/a | n/a | n/a | **None in any download** |

**The Vita-Nex answer in one line:** do not port Vita-Nex Core. It is 147,294 lines, its value sits in exactly the
parts ModernUO changed most (packets and gump entries), Power Hour is a 2-4 day native rebuild, and the Vault Pass
modules are better read as design than bought as code.

## Per module

### 1. Vita-Nex Core 5.3.1.0 (`code\vitanex-core`)

1. **What it does.** A large extension library for ServUO: a gump framework (SuperGumps), services (schedules,
   notifications, time boosts, web API), a module system and many ready modules (AutoPVP, voting, toolbars, trash
   collection, arcade). Serves: none directly; it is the base for Power Hour and every Vault module.
2. **Dependencies.** 582 .cs, 147,294 lines (counted). Largest parts: Modules 48,720 (AutoPVP alone 25,176),
   Extensions 20,498, SuperGumps 18,918, Items 14,401, Services 11,209. No core file edits, but it reaches into
   ServUO internals through hook points ServUO exposes:
   - outgoing packet rewriting through `NetState.PacketEncoder` and `CreatedCallback`
     (`Network\OutgoingPacketOverrides.cs:51,58`);
   - incoming handler replacement with `PacketHandlers.Register`, `RegisterExtended`, `Register6017`
     (`Network\ExtendedOPL.cs:131-142`, `Modules\EquipmentSets\EquipmentSets_Init.cs:48-63`);
   - reflection into private fields (`Network\NetworkBuffers.cs:27-39`, `Extensions\Server\RegionExt.cs:438`) and
     runtime DLL loading that overwrites `ScriptCompiler.Assemblies` (`VitaNex_Modules.cs:97-110`);
   - `Core.Slice` tick hook (`VitaNex_Init.cs:104`); 16 EventSink events; its own side-file persistence
     (`IO\DataStores\BinaryDataStore.cs`, 23 users) written on WorldSave.
3. **ModernUO fit.** `PacketEncoder`, `CreatedCallback`, `Get6017Handler`, `BufferPool` and `Core.Slice` do not exist
   in pinned. SuperGump subclasses the legacy `Gump` and about 20 custom entries override `AppendTo(IGumpWriter)`;
   pinned's `GumpEntry.AppendTo` takes `ref SpanWriter` (`UOContent\Gumps\Base\Legacy\GumpEntry.cs:26`), so every
   custom entry and the compile path are rewrites. Login, PlayerDeath, CharacterCreated, CastSpellRequest,
   CheckEquipItem and DeleteRequest are not pinned EventSink events (Login is `PlayerMobile.PlayerLoginEvent`,
   `UOContent\Mobiles\PlayerMobile.cs:1234`). Side stores would move to `GenericPersistence`. Not ModernUO-ready:
   the release has `#if MUO` blocks in 2 files only (`VitaNex_Init.cs`, `Extensions\Server\SerializeExt.cs`), and
   the 5.3.1.0 notes call it "beginning support for ModernUO". No finished port was found on disk or by one web search.
4. **Effort.** Full Core without modules: about 8-12 weeks; with modules: 4-6 months (guess). Minimal subset for Power
   Hour: about 25-35k lines, 3-5 weeks (guess), because the SuperGump framework does not split off.
5. **Risks.** Permanent merge debt against an upstream that targets ServUO; the risky parts are packet and gump
   internals. MIT: keep `LICENSE.md` with any copied code.
6. **Recommendation: Skip the Core port.** Rebuild any wanted module natively. Read Core only as reference.

**Which Core pieces each module uses.**

| Module | Core pieces used |
|---|---|
| Power Hour (downloaded) | `CoreModule` lifecycle (CMConfig/CMInvoke/CMSave/CMLoad), `CoreModuleOptions`, `PropertyObject`, `BinaryDataStore`, `SerializeExt` helpers, `Notify`, `TimeBoosts` and `TimeBoostsUI`, `ConfirmDialogGump` (SuperGumps), `MobileSelectTarget`, `CommandUtility`, assorted extensions (`PowerHour_Init.cs:24-128`, `PowerHour.cs:116,168,193,228`) |
| Deviants and Deviations (Vault, not downloaded) | **guess:** CoreModule, Schedules, Notify, SuperGumps, Effects and Geometry, BaseCreature extensions |
| Instanced Map API + Instanced Dungeons (Vault) | **guess:** Core has no map instancing, so the module carries its own; plus RegionExt (private-field reflection), Geometry, Geography, BinaryDataStore, SuperGumps. Hardest on ModernUO |
| Invasions (Vault) | **guess:** Schedules, Notify, Geometry and Geography, CoreModule, SuperGumps |
| IPL: installer, patcher, launcher (Vault) | A client-side installer and launcher, not a server module (download queue row 94). The shard already has its own player package and one-step install, so no port is needed |

### 2. Power Hour (`code\vitanex-power-hour`)

1. **What it does.** Each character can start a timed session (default 1 hour, then a 23-hour cooldown); during it,
   corpse gold is multiplied and each successful skill check gets an extra gain roll. Serves: play-test tuning only;
   no F-entry asks for it.
2. **Dependencies.** Vita-Nex Core (table above). It already hooks gains and loot itself, despite the page saying it
   needs extra work: it wraps the four `Mobile.SkillCheck*Handler` delegates and `Mobile.CreateCorpseHandler`
   (`PowerHour_Init.cs:55-68`, `PowerHour.cs:239-385`). State in a Vita-Nex side file.
3. **ModernUO fit.** The skill check delegates exist (`Server\Mobiles\Mobile.cs:177-186`); the shard already wraps
   them in `customizations\ClusterFSkillGain.cs`, so a boost is one more check there. `CreateCorpseHandler` changed
   signature and is multicast (`Mobile.cs:194`), so the swap-and-chain pattern breaks; use `+=` or a death or loot
   hook. Persistence through `GenericPersistence` or a field on PlayerMobile; a small `DynamicGump` replaces the
   SuperGump dialogs.
4. **Effort.** S as a rebuild (about 300-500 lines, 2-4 days, guess). Do not port.
5. **Risks.** The stackable, blessed reset token resets the cooldown outright (`Items\PowerHourResetToken.cs:26-34`).
   Per character, so alts each get a session. A bug: a corpse with no player killer still gets the gold bonus
   (`PowerHour.cs:266-268`). The extra roll would stack with the shard's 3 attempts x5 amount and the Test Center's
   x5 gain factor (guess, verify).
6. **Recommendation: Borrow the idea only**, and only if Chase wants timed boosts. The Test Center already has a x5
   gain factor for play testing (`customizations\TestCenter\TestCenterSkillGain.cs`). Not in the top 5.

### 3. Hunter's Bestiary (`code\hunters-bestiary`)

1. **What it does.** Notable creatures drop a "Hunter's Treatise" that, once read, gives that character +20% damage
   against that creature type, pets included; a Bestiary gump tracks progress over 8 categories. Serves: F-24 monster
   hunts and F-13 achievements.
2. **Dependencies.** One core line at the end of ServUO `BaseCreature.OnBeforeDamage`
   (`ServUO-pub57\Scripts\Mobiles\Normal\BaseCreature.cs:1971`, called from `Scripts\Misc\AOS.cs:379`). EventSink
   CreatureDeath, WorldSave, WorldLoad. Profiles saved to `Data\ExileHunterProfiles.xml` by serial, outside the world
   save. Legacy gump; per-viewer tooltip through `SendPropertiesTo`. 191 creatures registered (the 193 count includes
   2 command registrations).
3. **ModernUO fit.** Pinned BaseCreature has no `OnBeforeDamage`. The faithful spot is `UOContent\Misc\AOS.cs` before
   the `totalDamage <= 0` check, where the shard already patches (`server\patches\AOS-damage-eater-hook.patch`).
   Deaths through `[OnEvent(nameof(CreatureEvents.CreatureDeathEvent))]` (`UOContent\Mobiles\CreatureEvents.cs:8-9`),
   as `ClusterFAchievements.cs` already does; guard bonded-pet deaths (no corpse). Profiles into `GenericPersistence`
   or `ClusterFAccountData`, which already has an `EncounteredCreatures` set (`customizations\ClusterFAccountData.cs:83-86`).
   10 of the 191 types exist in neither pinned nor the shard (mostly Peerless bosses: Travesty, DreadHorn,
   ChiefParoxysmus, ShimmeringEffusion, MonstrousInterredGrizzle, AbyssalInfernal, PrimevalLich, IronBeetle,
   OsseinRam, PutridUndeadGargoyle); 11 more exist only in the shard's customizations.
4. **Effort.** M.
5. **Risks.** The +20% applies after resistances and slayers (`BaseWeapon.CheckSlayers`), so it multiplies (a x2
   slayer becomes about x2.4) and sits outside damage-increase caps. A profile is created for every attacker,
   monsters included, on every hit (`Engine.cs:300-305`): unbounded growth. Drops do not exclude summoned or
   controlled creatures (treatise farming). Exact-type matching only.
6. **Recommendation: Port later, as a rebuild**, folded into F-24 hunts (and F-14 creature levels, which F-24 waits
   on). Decide the bonus size against slayers first; consider a smaller bonus or a slayer-style cap.

### 4. Tamable specimen rating (`code\tamable-rating`)

1. **What it does.** A tamable creature's tooltip shows 1 to 5 stars, scoring its rolled stats against its species'
   range (Hits 30%, Str 25%, resists 25%, damage 10%, combat skills 10%). Serves: companions, F-35 evo pets, mule
   bloodlines and breeding.
2. **Dependencies.** XmlSpawner (`XmlSpecimenQuality : XmlAttachment`); 4 lines in `BaseCreature.GetProperties`
   (`Instructions.txt:31-39`). Species bounds come from creating 20 sample creatures with `Activator.CreateInstance`
   (`SpecimenEvaluator.cs:97-167`).
3. **ModernUO fit.** No XmlSpawner; pinned BaseCreature has `AddNameProperties(IPropertyList)` (`BaseCreature.cs:3155`)
   but no `GetProperties` override, so it needs one. Replace the attachment with a value computed once at spawn or
   tame time from deterministic bounds (or a serialized byte); never spawn sample creatures in ModernUO, where each
   one takes a serial and enters the world.
4. **Effort.** S, as a rebuild of the idea.
5. **Risks.** Sample spawning (performance and constructor side effects); the cached rating never updates after Pet
   Training changes stats.
6. **Recommendation: Port later (rebuild)**, after the Pet Training port; show the stars in the Animal Lore view too.

### 5. Animal Lore dashboard (`code\animal-lore-gump`)

1. **What it does.** Replaces ServUO's tabbed Animal Lore gump with one dashboard (stats, resists, damage, skills,
   abilities, loyalty and training controls) and drops the floating training-progress gump. Serves: the Pet Training
   port (Port tier, right after Creatures) and Animal Lore to 200.
2. **Dependencies.** Diffed against stock pub57 (whitespace ignored): `Gumps.cs` +11/-18 of 1,918 lines (removes the
   progress gump launch, swaps 9 references to the new gump; the old gumps remain as dead code); `AnimalLore.cs`
   +14/-6 (opens the dashboard; adds `using ShrinkSystem;` and shrunk-statue targets, a third-party dependency not in
   ServUO; also allows hirelings and mounts as targets); `PetTrainingGate.cs` +3/-3 (an overhead message; no
   auto-open). New `DashboardAnimalLoreGump.cs`, 531 lines. Needs ServUO Pet Training and ServUO's `BaseGump`.
3. **ModernUO fit.** Pinned has no OSI pet training at all (0 hits for PetTraining, TrainingProfile, AbilityProfile);
   its Animal Lore is the old multi-page gump (`UOContent\Skills\AnimalLore.cs:71`). Pinned's `BaseGump` is unrelated
   to ServUO's; port to `DynamicGump` with `NetStateGumps.Find/Close` (`NetStateGumps.cs:39-81`).
4. **Effort.** M, and only after Pet Training is ported.
5. **Risks.** The dashboard file declares GPL-3.0 (`DashboardAnimalLoreGump.cs:1-6`) and the rest derives from ServUO
   (GPL). Its `OnResponse` drops stock's alive, map and dead-pet guard (stock `Gumps.cs:443-444`), and training
   begin and cancel are not re-checked for ownership on response.
6. **Recommendation: Port later, right after the Pet Training port.** It is a customization, not part of the faithful
   port: the Pet Training port keeps the stock gumps first, then this replaces them. Leave out ShrinkSystem and the
   hireling and mount targets unless Chase wants them.

### 6. Virtual storage chests (`code\virtual-storage`)

1. **What it does.** House-locked stockpiles delete what you deposit and keep a count per type; a paged gump hands
   back up to 100 at a time. Serves: bulk reagent harvests, herbalism, resource storage.
2. **Dependencies.** No core edits. Hand-written serialization (version written, then ignored on read; types by name).
   House check is only `IsLockedDown || IsSecure`. Legacy gumps.
3. **ModernUO fit.** `[SerializationGenerator]` with a `Dictionary<Type,int>` field (pinned serializes `Type`). Pinned
   `BaseHouse.CheckAccessibility` (`Multis\Houses\BaseHouse.cs:1427`) refuses a locked-down non-container item that is
   not `ISecurable`, so the chest must implement it and re-check secure access on every response.
4. **Effort.** M, as a rebuild.
5. **Risks (checked in code, High first).**
   - **High:** the ADD target scans any targeted container within 12 tiles, recursively, and deletes what it finds
     into the chest (`VirtualStorageGump.cs:201-211`): other players' corpses and monster corpses with no looting-rights
     or criminal check.
   - **High:** withdraw responses check only "chest not deleted" and range (`VirtualStorageGump.cs:167`): no house
     access, lockdown, alive or owner check, so an open gump keeps working after a co-owner is removed or the house
     changes hands.
   - **High:** `RefinementCabinet` responses have no checks and act on stale references, a theft and dupe path
     (`RefinementCabinet.cs:176-231`).
   - **Medium:** properties lost on deposit (hue, blessed, crafter, rare fish names); subclasses accepted; dye tubs come
     back fresh and unbound (a recharge exploit); a released chest with unlimited stock weighs 10 stones and can be
     carried off, sidestepping the bank limit.
6. **Recommendation: Borrow the idea only.** A native rebuild: `ISecurable`, exact-type whitelist, deposits from your
   own backpack only, withdraw sized to what you can carry, every response re-checking house access, range and alive,
   and immovable while it holds stock. Overlaps F-19 (1,000-item banks) and satchels, so ask whether it is needed at all.

### 7. Craft from bank (`code\craft-from-bank`)

1. **What it does.** Routes crafting's resource count and consumption through a chain: backpack, optional providers,
   then the bank box (recursive); an add-on draws from virtual storage chests linked by account tag. Serves: F-34.
2. **Dependencies.** Three edits to ServUO `Services\Craft\Core\CraftItem.cs` (`:994` count, `:1093` and `:1125`
   consume). Account tag `VirtualStorage.LinkedChestSerials`; `EventSink.Login`. The author says it was "vibe coded
   using gpt-5.2".
3. **ModernUO fit.** Pinned `CraftItem` consume has no `ResValidator` parameter (`Server\Items\Container.cs:660,697`),
   and the shard's `patches\CraftItem-shard-hooks.patch` already owns the count line, so it conflicts.
4. **Effort.** S-M, but not worth it as written.
5. **Risks.** The pre-craft check is not routed, so bank-only resources fail and stack crafting can break (read, not
   tested); same-hue grouping mixes across sources; partial consumption is never rolled back; nothing ever links a
   chest (`AddChest` has no caller); the storage provider has no owner or house check.
6. **Recommendation: Skip.** F-34 (bank access item) is already designed and its engine is built:
   `customizations\GuildResources.cs` counts and takes across pack and bank, all or nothing. F-34's remaining work is
   one hook in our own craft patch. Nothing here improves on that.

### 8. Visual Builder (`code\visual-builder`)

1. **What it does.** A GM palette gump of every item ID from tile data, with paint, fill box, erase, wipe box, nudge,
   hue and clone; everything placed is a `Static`. Serves: staff building, F-21 New Haven art, server-placed buildings.
2. **Dependencies.** None beyond ServUO: reads `TileData.ItemTable` (`ServUOVisualBuilder.cs:284-289`), in-memory
   session, commands at GameMaster.
3. **ModernUO fit.** `TileData.ItemTable` exists (`Server\TileData.cs:288-291`). Mechanical changes only: gump
   `OnResponse(NetState, in RelayInfo)`, `Dragable` to `Draggable`, `CloseGump<T>()`, drop `.Free()` on the item
   enumerator (`Server\Maps\Map.ItemEnumerator.cs:80`).
4. **Effort.** S.
5. **Risks.** World Static Edit mode can wipe any dynamic `Static` in a 50x50 box, and undo only removes what the tool
   placed, so wiped items cannot come back; undo is lost on restart.
6. **Recommendation: Port later**, after the duplicator. It overlaps pinned's `[Tile`, `[Wipe`, `[Add` menu and
   `[AddonGen`; it adds the visual palette. Make wipe and erase record what they delete.

### 9. Building Duplicator (`code\building-duplicator`)

1. **What it does.** Box-select an area, capture its items and map statics as offsets in a text file, then stamp it
   anywhere with nudge and undo. Serves: staff tools, guild halls, New Haven layouts. (The "second .cs" is a
   byte-identical copy in `_zips\`.)
2. **Dependencies.** None beyond ServUO: `map.Tiles.GetStaticTiles(x, y, true)` (`BuildingDuplicator.cs:189`),
   in-memory undo, `[BuildDupe` at GameMaster.
3. **ModernUO fit.** `GetStaticTiles` / `GetStaticAndMultiTiles` (`Server\TileMatrix\TileMatrix.cs:271,274`), item
   enumerator without `.Free()`, gump signatures. Its AddOn export duplicates pinned's `[AddonGen`.
4. **Effort.** S.
5. **Risks.** No size cap on the capture box (a huge box loops on the main thread); multi tiles get captured as
   statics; a bad line aborts a paste and the partial paste is not undoable (undo is pushed after the loop, `:458`).
   Only item ID and hue are copied, so no item dupe.
6. **Recommendation: Port now, adapted.** The shard builds structures from a design `layout.json` through a generator
   into a C# table and an idempotent seeder (`ClusterFRegistrarOfficeLayout.cs`, `ClusterFGuildHallSeeder.cs`), but
   has no in-game "capture this area" step. The duplicator is that front end if it writes our layout JSON.

### 10. Invasions, modernized (`code\invasions-feng`)

1. **What it does.** An Administrator schedules a town invasion (12 Felucca towns, 10 monster themes, 8 champions):
   monsters spawn, the town's guards go off, and a champion appears when the wave is cleared. Serves: F-30 Events tab
   surges (Chase named ServUO's town invasions as prior art) and League culling.
2. **Dependencies.** ServUO `Persistence.Serialize` to `Saves\Invasions\Persistence.bin`, EventSink WorldSave and
   WorldLoad, `GuardedRegion.Disabled`, one gump.
3. **ModernUO fit.** `GenericPersistence`; `GuardsDisabled` and `IsDisabled()`
   (`UOContent\Regions\GuardedRegion.cs:33,50`); `Region.Find(name, map)`. Pinned also ships an `EventScheduler`
   (`UOContent\Engines\Events\EventScheduler.cs`).
4. **Effort.** M as a port.
5. **Risks.** **GPL-3.0 copyleft**: fine in the private repo, but any distributed derivative must be GPL. Region lookup
   ignores the map, so a Felucca invasion also turns off Trammel's guards (`InvasionSystem.cs:406-411`). After a
   restart an active invasion resumes with Moonglow defaults (champion in Moonglow, wrong town's guards re-enabled).
   The Harrower can be picked as a town champion. No New Haven.
6. **Recommendation: Borrow the idea only.** Rebuild the F-30 surge natively; ServUO's Blackthorn `InvasionSpawner` is
   already in the Port tier and is the faithful base.

### 11. Apex Hunt (`code\apex-hunt`)

1. **What it does.** Every 4 hours the server picks a creature from 41 in 4 tiers with a kill goal and 25-45 minutes,
   shows a HUD, runs a 60-second tie breaker and banks gold to the top three and to anyone with 10% of the goal.
   Serves: F-24 League hunts and events.
2. **Dependencies.** EventSink WorldSave, CreatureDeath, Login; raw `BinaryWriter` to `Saves\ApexHuntEvent.bin`;
   a 1-second tick; HUD refresh every 5 seconds.
3. **ModernUO fit.** The same `[OnEvent]` pattern the shard uses (`ClusterFAchievements.cs:1298,1344`);
   `GenericPersistence`; `Serial.Value` is `uint` now (`Server\Serial.cs:29`), so the save's `ReadInt32` round trip
   breaks.
4. **Effort.** M.
5. **Risks.** Only the last hit counts (kill stealing, no party or damage-share credit); the guard check tests the
   killer's region, not the creature's; about 50k gold plus 5k per participant, 6 times a day (inflation); alts each
   qualify. License is permissive.
6. **Recommendation: Port later, as the F-24 hunt skeleton**, after F-14 (F-24's hunts wait on it): League points
   instead of gold, damage-share credit through `Mobile.DamageEntries` (as cc-P72 already planned for XP), creature
   lists per facet.

### 12. UORespawn (`code\uorespawn`)

1. **What it does.** Spawns creatures around active players by terrain, region, priority boxes and shop-sign vendors,
   and recycles mobs, with a desktop editor and binary spawn packs. Serves: none on the current plan.
2. **Where the server source is.** It is already on disk; `SOURCE.txt`'s "0 .cs" is wrong. The editor zip holds nested
   zips `Data\SERVER\MUO\UORespawnServer.zip` (77 .cs plus `DOCS\SERVER_README.md`) and `Data\SERVER\SERVUO\...`
   (78 .cs). The MUO zip is already outside the binaries at
   `code\uorespawn\_app-resources-binaries-removed\Data\SERVER\MUO\UORespawnServer.zip` (checked: 77 .cs). Upstream is
   public at https://github.com/Kita72/UORespawnProject (README says MIT; that Kita72 is Wilson is a guess). **To get
   it:** Chase unzips that MUO zip into a new folder such as `code\uorespawn\server-muo\` (or clones the GitHub repo),
   and SOURCE.txt is corrected.
3. **ModernUO fit.** There is a ModernUO-specific script set, but its target version is unstated. Its own
   `Spawners\RegionSpawner.cs` may collide with pinned's `Server.Engines.Spawners.RegionSpawner` (guess; not read).
4. **Effort.** L.
5. **Risks.** It would duplicate or fight the stock JSON spawners the shard imports and protects
   (`patches\ImportSpawners-guid-key.patch`, `tests\Misc\SpawnerImportVerification.cs`), and player-anchored spawning
   replaces OSI's fixed spawns, against "faithful port first". Binary spawn packs cannot be reviewed in a diff. The
   editor is a staff-only Windows app; never in the player package.
6. **Recommendation: Borrow the idea only**, for now. Possible later narrow uses: weather or night ambience, rifts,
   wilderness fill in custom areas, never over stock spawns.

### 13. Runebook and Runic Atlas gump (`runebook-gump`)

1. **What it does.** Rune reordering (from Orion's organizer) and spell icons instead of text buttons; also raises
   Runic Atlas charges from 100 to 1,000, unannounced. Serves: travel UI.
2. **Dependencies.** `Entries.Swap` is Vita-Nex's `EnumerableExt.Swap`, so it does depend on Vita-Nex, despite
   SOURCE.txt.
3. **ModernUO fit.** Pinned `UOContent\Gumps\RunebookGump.cs` is a `DynamicGump` with different button encoding and
   already shows icon buttons when `!Core.AOS`. Pinned has no Runic Atlas at all.
4. **Effort.** S for reordering in pinned's gump.
5. **Risks.** The reorder handlers do not bounds-check a crafted button ID (an exception) and skip `CheckAccess`, so
   anyone in range can reorder a locked-down book.
6. **Recommendation: Borrow the idea only**: add bounds- and access-checked reordering to pinned's runebook gump if
   Chase wants it. Skip the 1,000-charge atlas.

### 14. Seagulls and Butterflies (`seagulls`, `butterflies`)

1. **What they do.** Blessed, invulnerable ambient creatures on new animation bodies (seagulls 6501-6505 with sounds;
   butterflies 2967-2969, one script with BOD cloth hues). Serves: New Haven and garden ambience.
2. **Dependencies.** Only the new `.vd` animations and `.wav` sounds patched into the client.
3. **ModernUO fit.** About 30 lines each with `[SerializationGenerator]`. Pinned has `Bird`, `TropicalBird`, `Parrot`;
   no seagull or butterfly creature.
4. **Effort.** S server side; S-M for client art.
5. **Risks.** The art is flagged as ripped ("IE seagull", Infinity Engine; "Legend of Zhao Yun"); sound sources unstated.
6. **Recommendation: Skip the art.** If wanted, an ambient critter on stock bodies (a `Bird` named seagull at the docks).

### 15. Level System Extreme (`level-system-extreme`)

1. **What it does.** Player and pet levels, XP from kills and skills, point-buy skills and stats, level gates, vendors,
   tokens and gear requirements. Serves: F-12 (already assessed 2026-09-30).
2. **Dependencies.** 55 .cs, about 24,100 lines; its own XmlSpawner attachment fork (about 4,100 lines); a hidden
   control item at a fixed Trammel spot; 9 distro edits (BaseArmor, BaseWeapon, BaseClothing, BaseJewel, SkillCheck,
   Titles, PlayerMobile.GetProperties, BaseVendor, ConfirmBankPointsGump); EventSink SkillGain, CheckEquipItem,
   CreatureDeath, Login and more.
3. **ModernUO fit.** None of those EventSink events exist in pinned; no XmlSpawner. A rebuild in practice.
4. **Effort.** Rebuild from the idea.
5. **Risks.** No license anywhere; point-buy skills and XP tokens conflict with F-12 (level = skill cap, loops, "XP for
   the act, never for a currency turn-in"); attachment saves can desync from the world save.
6. **Recommendation: Borrow the idea only**, as F-12 already ruled. Possibly useful shapes: a `RequiredLevel` gate or
   tile, a per-creature XP table, a party XP split. No levelable gear in it (cc-P72 covers that).

### Client plugins

None. No folder holds a ClassicUO or TazUO plugin, plugin API use, client assembly or script. The only client-side
content is the seagull and butterfly art (flagged above). Nothing here needs to ship in the player package; the
UORespawn editor is a staff tool and must not.

## Proposed order of work

The port list comes first; these are after it or beside it. Staff tools (1, 2) touch no player content, so they can
run whenever a builder slot is free. The rest wait for the faithful work they sit on.

| Order | Work | Effort | Waits on |
|---|---|---|---|
| 1 | Building Duplicator, adapted to write the shard's layout JSON | S | nothing (staff tool) |
| 2 | Visual Builder, with safe wipe and erase | S | 1 (shares the capture and undo code) |
| 3 | Animal Lore dashboard on the ported Pet Training | M | the Pet Training port (Port tier) |
| 4 | Specimen star rating, rebuilt | S | 3 (shown in the dashboard too) |
| 5 | League hunts on Apex Hunt's skeleton, with the bestiary idea folded in later | M | F-14 creature levels, F-24 hunt design |

Not in the top 5: virtual storage (needs Chase to say it is wanted beside F-19 and satchels), Power Hour (Test Center
already boosts gains), runebook reordering (small; any batch), the invasion surge (F-30 batch 2 designs its own).

### Draft prompts (not saved to the queue until Chase says go)

Numbers are proposals: next free is P94. Each follows the house style of `D:\UO\cc-prompts`.

#### Draft P94: Building Duplicator as the capture step for layout JSON

- **Goal.** A GM command that captures a box of items and statics in game and writes it as the shard's layout JSON, so
  a hand-built room becomes a seeded structure (guild halls, New Haven, F-21 art). Credit Kamras.
- **Kind.** Builder in `D:\ShatteredLegacy`; staff only; no player-facing change; Staff line in CHANGELOG.
- **Read first.** `D:\UO\third-party\code\building-duplicator\BuildingDuplicator.cs` (design reference; rewrite, do
  not copy the file); `server\customizations\ClusterFRegistrarOfficeLayout.cs`, `ClusterFGuildHallSeeder.cs` and the
  `design\...\layout.json` plus generator they come from; pinned `Server\TileMatrix\TileMatrix.cs:271,274`,
  `Server\Maps\Map.ItemEnumerator.cs`, `UOContent\Commands\AddonGenerator.cs`.
- **Steps.** (1) `[CaptureLayout` with a box target, size cap (for example 64x64) and Z range; skip multis, doors and
  addon bases; read statics with `GetStaticTiles` (not multi tiles). (2) Write the same JSON shape the generator reads,
  under a staff-only folder. (3) `[StampLayout` places from that JSON with a full undo that records every placed item
  before placing (undo covers a partial stamp). (4) No AddOn `.cs` export (pinned has `[AddonGen`).
- **Test plan.** Unit tests: capture of a fixture area round-trips through the generator to the same table; size cap
  refuses a big box; a bad line in the file stops before placing anything; undo after a partial stamp removes every
  placed item. Watch each fail first. Manual: capture and re-stamp one guild hall room on the test shard.

#### Draft P95: Visual Builder for staff, with recorded erase and wipe

- **Goal.** An in-game art palette for staff (search tile data, paint, fill box, nudge, hue) on top of pinned's
  `[Tile` and `[Wipe`, whose erase and wipe can always be undone. Credit Kamras.
- **Kind.** Builder; staff only; Staff line.
- **Read first.** `D:\UO\third-party\code\visual-builder\ServUOVisualBuilder.cs`; pinned `Server\TileData.cs:288-291`,
  `UOContent\Gumps\Base\DynamicGump.cs`, `UOContent\Commands\Wipe.cs`; P94's undo code.
- **Steps.** (1) A `DynamicGump` palette from `TileData.ItemTable`, paged and searchable. (2) Paint, fill box, nudge,
  hue as `Static` items. (3) Erase and wipe record each deleted item (type, ID, hue, location) before deleting, so undo
  restores them; World mode stays off by default and is Administrator only. (4) Session undo saved across a restart
  or clearly cleared with a warning.
- **Test plan.** Tests for: wipe then undo restores every item; World mode refused below Administrator; fill box cap.
  Watch each fail first. Manual: decorate a corner of New Haven on the test shard, wipe it, undo it.

#### Draft P96: Animal Lore dashboard on ported Pet Training

- **Goal.** After the Pet Training port lands with ServUO's stock gumps, replace them with a one-page Animal Lore
  dashboard (stats, resists, damage, skills, abilities, loyalty, training). Credit Feng.
- **Kind.** Builder; player-facing customization (log the deviation in `docs\fidelity-principle.md` through Claude; a
  wiki entry). **Runs only after** the Pet Training port is committed.
- **Read first.** `D:\UO\third-party\code\animal-lore-gump\` (all 4 files; the dashboard declares GPL-3.0, the repo is
  private, keep the notice), the stock pub57 `Scripts\Services\Pet Training\Gumps.cs`, `Scripts\Skills\AnimalLore.cs`,
  `PetTrainingGate.cs`; the ported Pet Training in `server\customizations`; pinned `UOContent\Skills\AnimalLore.cs`,
  `UOContent\Gumps\Base\DynamicGump.cs`, `NetStateGumps.cs:39-81`.
- **Steps.** (1) Rebuild the dashboard as a `DynamicGump`. (2) Swap the call sites the author changed (9 in
  `Gumps.cs`, 1 in `AnimalLore.cs`). (3) Keep stock's alive, map and dead-pet guards and re-check ownership on every
  training button. (4) Leave out ShrinkSystem and the hireling and mount targets unless Chase says otherwise. (5) Leave
  room for Animal Lore 200 thresholds.
- **Test plan.** Tests: a dead or unowned pet's training buttons do nothing; the dashboard opens from the lore target
  and from the training gate. Watch each fail first. A play test: lore a trained pet and start a training round.

#### Draft P97: Specimen star rating, rebuilt

- **Goal.** A 1 to 5 star rating in a tamable creature's tooltip and in the Animal Lore dashboard, scored against its
  species' range, computed once without spawning sample creatures. Credit Imagine for the idea.
- **Kind.** Builder; player-facing customization; wiki entry.
- **Read first.** `D:\UO\third-party\code\tamable-rating\` (weights and normalization only); pinned
  `UOContent\Mobiles\BaseCreature.cs` (`AddNameProperties` near 3155, `StatLossAfterTame` near 964),
  `UOContent\Skills\AnimalTaming.cs:426-428`; P96.
- **Steps.** (1) Species bounds from the creature's own `SetStr`/`SetHits`/`SetResistance` ranges, read once per
  type (no instances). (2) Score with the author's weights, normalized for stat loss after taming. (3) Store as a
  serialized byte set at spawn or tame (or recompute on demand; pick one and say why). (4) A tooltip line on tamables
  only.
- **Test plan.** Tests: a creature at the top of every range rates 5, at the bottom 1; taming does not change the
  rating; no creature is created by the evaluator. Watch each fail first.

#### Draft P98: League hunts on the Apex Hunt skeleton

- **Goal.** Timed server-wide hunts for the League (F-24): a target species with a goal and a time limit, a HUD, a tie
  breaker and League rewards. Credit Imagine.
- **Kind.** Builder; player-facing; wiki entry. **Runs after** F-14 creature levels and F-24's hunt design.
- **Read first.** `D:\UO\third-party\code\apex-hunt\` (design reference); `docs\feature-queue.md` F-24 and F-14;
  `notes\cc-P72-level-items-research.md` (damage-share credit through `Mobile.DamageEntries`);
  `server\customizations\ClusterFAchievements.cs` (`OnCreatureDeath`), `ClusterFLeagueSystem.cs`; pinned
  `Server\Serialization\GenericPersistence.cs`.
- **Steps.** (1) Hunt state through `GenericPersistence`. (2) Credit by damage share, masters credited for pets and
  summons, kills inside guarded regions (by the creature's region) excluded. (3) Rewards in League standing or points,
  not raw gold; one claim per account. (4) Creature lists per facet sized by F-14 levels. (5) HUD as a small gump with
  a slow refresh. (6) Optional: fold in the bestiary idea (study a species after enough hunt credit).
- **Test plan.** Tests: last-hit stealing earns nothing without damage share; a pet's kill credits its master; a
  second character on the same account cannot claim twice; a restart mid-hunt resumes the same target and time. Watch
  each fail first.

## Open questions for Chase

1. **Go on the drafts?** Say which of P94 to P98 to save to the queue (and in what order). Until then they stay here.
2. **Vault Pass: worth buying?** My answer is no for porting: every Vault module needs Vita-Nex Core, and a Core port
   is months. IPL is a launcher the shard does not need. Buy it only if you want to read Deviants or Instanced Dungeons
   as design ideas.
3. **Virtual storage: wanted at all,** given F-19's 1,000-item banks, the satchels and the mule? If yes, it is a native
   rebuild (M) with the safety rules above.
4. **Power Hour: wanted?** It would be a small native rebuild in `ClusterFSkillGain`; the Test Center already has a x5
   gain factor for play testing.
5. **Animal Lore dashboard license:** the file declares GPL-3.0. Fine in the private repo; it constrains any future
   public release of the server code. OK to use?
6. **Hunter's Bestiary bonus size:** +20% stacks on slayers (about x2.4). Keep, shrink, or cap it when it joins F-24?
7. **UORespawn:** keep it as an idea only, or unzip its ModernUO server scripts for a closer read? (Unzipping is yours
   to do; this task does not extract third-party code.)
8. **Project copy:** this file is at `notes\servuo-code-port-assessment.md`; there is no `claude\` folder on disk, so
   please add it to the Claude project as `claude/servuo-code-port-assessment.md`.

## Corrections to the download records (for the features overseer)

- `code\uorespawn\SOURCE.txt` says 0 .cs and no server source; the MUO server scripts are in the nested zip (77 .cs),
  and upstream states MIT.
- `runebook-gump\SOURCE.txt` says neither file references Vita-Nex; `Entries.Swap` is Vita-Nex's.
- `code\hunters-bestiary` registers 191 creatures, not 193.
- `code\animal-lore-gump\SOURCE.txt` says no stated terms; the dashboard file header says GPL-3.0. It also needs
  ShrinkSystem.
- `code\building-duplicator` has one source file; the second .cs is a byte-identical copy in `_zips\`.
- `code\vitanex-power-hour`: it already hooks gains and corpse gold; the "needs extra development" note is mostly out
  of date.
