# cc-P70: Compact Mule modules (framework, learned schematics, crafting, all 17 modules)

Run 2026-10-12 by Claude Code (autopilot hand-off after P69). Builder, test build only. Gates at start: P69 committed
(`1fffa9f`), `git -C D:\ShatteredLegacy status --short` empty, pinned `d4531cd94b739613155225c234900de9f47d2c88` (every
pinned citation below is at that commit). The core prompt ran as **P69** (`notes\cc-P69-mule-core.md`): its hooks
(the module list, `ModuleSlots`, `PackMule.Compute` / `ModifyNumbers`, the death-drop flag, trait ids) are what this
builds on. **P** = `D:\UO\ModernUO-pinned\Projects`, **C** = `D:\ShatteredLegacy\server\customizations`.

**Where the citations come from.** Four research subagents in this session read:
- crafting, recipes and shops;
- the hauling and utility systems;
- survival, AI and dismounting;
- vendors, the bank and imbuing.

Their file:line is marked "(agent)" where I did not re-read it. I re-read everything the build calls: the craft APIs, the
patched `CraftItem.ConsumeAttributes`, `BaseCreature.Damage`, `Mobile.Animate`/`OnMove`/resurrect hooks,
`TreasureMap`'s fields, the satchel classes, the guild hall gump, our skill-gain wrapper, `RegenRates.cs` and both
exploration managers.

## Headlines

1. **All 17 modules exist as items, are craftable from learned schematics, attach and detach, and show on the mule.**
   - **Built:** 12.
   - **Partly built:** 4. The Ore Hopper III's gem chance is not wired to mining. The Clockwork Load Harness III's
     Scavenger is not built (its redirect hook is). The Field Medic Pack II's ranged bandaging waits on a Bandage
     patch. Imbuing into the Imbued Barding Socket waits on the imbuing rework (its sockets and their effects work).
   - **Stubbed:** Steady Hoof Wraps, which needs a pinned patch (Part E); the patch is planned.
   - Each tooltip says what is missing.
2. **One pinned patch, small and argued:** `CraftItem-mule-module-tier.patch` (7 lines). A tier II module is crafted
   from a tier I of the same kind, and pinned's resources match by type only. The alternative was 51 sibling classes.
3. **Trader's Ledger I-II needs no vendor patch:** our own "sell cargo" window, with the vendor's own sell info. The
   portable bank (III) needs none either.
4. **1084/1084 shard tests pass.** The 11 new facts were watched red (eleven deliberate breaks, nothing else failed)
   and then green. Image `sl-modernuo:cc-p70`.
5. **Findings worth a decision (section 9):**
   - The Artificers' Toolkit already imbues anywhere, so "the mule counts as a soul forge" gives nothing yet.
   - The Smelter's forge serves anyone beside the mule (owner-only needs a pinned hook).
   - An SOS in the mule's pack is not found when fishing (pinned Fishing reads the player's pack).
   - The tier ranks for schematics differ between this prompt (1/2/3) and cc-P78 (1/2/4).
6. **Two live exploration managers.** `ClusterFExplorationManager` and `ClusterFExplorationSync` both reveal on every
   step (C\ClusterFExplorationManager.cs:43, C\ClusterFExplorationSync.cs:43, agent). The Survey Saddle Roll's wider
   reveal went into both. That two exist at all looks like a leftover: flagged in section 9.

## 1. Part A: the module item and attaching it

- **`MuleModule : Item, ICraftable`** (`C\Mobiles\Mule\MuleModule.cs`). Saved fields: module id (enum, append-only),
  tier, the Socket's properties and the Salvage Bin's filter. Guild, name, art and effects come from the data
  (`MuleModuleData`). One class for every module and tier.
- **Tiers from data:** `MuleModuleData.MaxTier` is a server setting, `mule.modules.maxTier` (3). Nothing assumes 3:
  arrays and the craft loop read it.
- **Attach:** drop the module on the mule (`PackMule.OnDragDrop`, ours). `MuleModules.RefuseAttach` checks:
  - owner only;
  - mule alive;
  - **the module's tier at most the mule's tier**;
  - **one per guild**;
  - a free slot (slots = the mule's tier, 1 to 5).
  A refused module stays with the player and is never deleted (fact 2). Attached, it moves to the internal map, into
  the saved list P69 left.
- **Remove:** the mule's Options window lists the modules with a Remove button each. The module goes to the owner's
  pack, or the bank if the pack is full, tier kept.
  - **The menu entry:** one context entry, stock cliloc 3000127 "Options". A new cliloc needs a player package update,
    which is outside this task's scope.
- **Shown:** each installed module is a line in the mule's properties. The module's tooltip shows guild, tier, the
  tier's effect, "needs a tier N mule", any "Not yet:" note, and its sockets.
- **Hue:** by tier, the same metal as a mule of that tier (`MuleModuleData.HueFor`, from `MuleData.Tiers`, which
  reads `CraftResources.GetHue`). Tier I Dull Copper, II Bronze, III Shadow Iron.
- **Serialization:** the mule's module list is P69's field 14 (no new mule version). `MuleModule` is new at version 0.
- **A deleted mule** returns its modules to the owner's bank; with no owner, they go with it.

## 2. Part B: learned schematics and crafting

**Recipes are pinned's own.**
- `Recipe` and `PlayerMobile.AcquireRecipe`/`HasRecipe`, per character (P\UOContent\Mobiles\PlayerMobile.cs:4178-4194, agent).
- Registered with `CraftSystem.AddQuestRecipe` so no loot or Craftsman's Satchel hands them out (CraftSystem.cs:298).
- **Ids:** `9000 + module x 10 + tier`, 9011 to 9173. Stock stops at 602.
- **Loop reset:** none exists yet (P69 section 1). The stand-in `ClusterFDevTools.ExecuteReset` never touches recipes,
  so they survive it.
- **Proposal:** keep them through loops. cc-P78 (F-43) moves them to an account store, which survives everything.
- A player without the recipe sees the item in the menu with MAKE NOW greyed and "You have not learned this recipe"
  (CraftGumpItem.cs:72-84, agent). Pinned's refusal says "from a scroll", which is cosmetic.

**Crafting:** each module and tier is a `CraftItem` in the building guild's craft system, in a "Mule Modules" group
(`MuleModuleCrafts.Register`, the `TinkeringCraftRegistrations` pattern, on ServerStarted).
- Main skill from 50 / 70 / 90 for tiers I / II / III, to +40.
- Secondary skill (where the row has one) from 30 / 50 / 70, to +20.
- Never exceptional.
- The crafted module takes its id and tier through `ICraftable.OnCraft` (pinned CraftItem.cs:21-27): no patch.

**Upgrade: tier II is built from a tier I of the same kind, III from II.**
- **The problem:** pinned's resources match by type (`Container.ConsumeTotal`, `IsInstanceOfType`, agent: Container.cs:841, 879, 907).
- **The alternatives:**
  - (a) 51 sibling classes, one per module per tier, each a separate `AddRes` type. That is 51 types now, and more each
    time Chase raises the tier count.
  - (b) A check in `CraftItem.ConsumeAttributes`. It runs with `consume=false` on every check and `consume=true` only on
    a successful skill check, and never on the failure path (agent: CraftItem.cs:997, 1348, 1388, 1588), so a failed
    craft keeps the old module.
- **Built (b):** `CraftItem-mule-module-tier.patch`, one hunk calling `MuleModuleCrafts.CheckPreviousTier`.
  - It applies on top of `CraftItem-shard-hooks.patch`, at `--fuzz=0`; the reasoning is in `apply-patches.sh`.
  - The testing crystal waives it, as the other craft bypasses do.
  - Limitation: the old module is not listed among the gump's resources; the refusal names it.

**Schematics:** `GuildSchematicsGump`, opened from each guild hall page (`GuildTaskDetailGump`, a new "Mule module
schematics" button for members at the guildmaster). The Smith and Custodian guildmaster gumps, which never open the
hall page, got their own button.
- **Rank** (`ClusterFGuildSystem.GuildRankIndex`): tier I Apprentice (1), II Journeyman (2), III Master (3), as this
  prompt says. Five-rung ladders (Artificers, Custodians) have no 4, so 3 is used there too. cc-P78 Part G says 1, 2, 4:
  one line in `MuleSchematics.RankFor`.
- **Price, in that guild's currency plus Mining Vouchers:**

| Tier | Guild currency | Mining Vouchers | Custodians (Clean Up points) |
|---|---|---|---|
| I | 20 | 5 | 2,000 |
| II | 50 | 10 | 6,000 |
| III | 120 | 25 | 15,000 |

  - For the Miners' own module (Ore Hopper) both are Mining Vouchers, summed.
  - Custodians pay with `CleanUpBritanniaData.Instance.DeductPoints`, which never lowers their rank (rank follows
    lifetime points; agent: CleanUpBritanniaData.cs:88-97).
- Every check is made again on the press, at the guildmaster.

## 3. The 17 modules as built

Craft: the building guild's craft, or P47 5.3's craft-by table (*proposal* where P47 has no row). Materials per tier
I/II/III: the first resource, the second, and the monster part (I bone x10, II daemon bone x5, III the named part x2).
All parts are existing pinned items. None of the module-specific III parts is a drop invented here; where they drop is
stock. Effects are per tier I / II / III.

| Module (guild) | Craft (secondary) | Materials I/II/III | III part | Effects I / II / III | State |
|---|---|---|---|---|---|
| Ore Hopper (Miners) | Blacksmithy (Mining) *proposal* | iron ingots 20/40/80; leather 5/10/20 | dark sapphire | ore, ingots, granite, gems -25% / -50% / -50% + gem chance | **Partial**: I-II built; III's gem chance on mining is not wired |
| Timber Rack (Foresters) | Carpentry (Lumberjacking) | boards 30/60/120; ingots 5/10/20 | bark fragment | logs, boards -25% / -50% / -50% + 10 logs to boards every 5 min | **Built** |
| Reinforced Saddlebags (Tailors) | Tailoring | leather 20/40/80; cloth 20/40/80 | switch | +50 / +100 / +150 items | **Built** |
| Clockwork Load Harness (Tinkers) | Tinkering | ingots 15/30/60; gears 2/4/8 | ecru citrine | +10% / +20% weight / +30% and the Scavenger's loot to the mule | **Partial**: weight built; the II auto-sort and the III Scavenger are not (the Scavenger, the League's auto-loot reward, does not exist) |
| Trailwise Tack (Rangers) | Tailoring (Animal Lore) *proposal* | leather 20/40/80; feathers 10/20/40 | turquoise | +20% stamina, regen, hostile warning in 12 / Homing, "all come" from anywhere / 0 follower slots | **Built** |
| Field Medic Pack (Healers) | Alchemy (Healing) *proposal* | bandages 20/40/80; ginseng 10/20/40 | luminescent fungi | heal 2% / 10 s out of combat / self-cure / emergency heal at 25% (5 min) + aura on owner and companions within 3 | **Partial**: II's bandaging from 6 tiles needs a Bandage patch (section 5) |
| Expedition Barding (Warriors) | Blacksmithy (Tactics) | ingots 30/60/120; leather 10/20/40 | brilliant amber | -10% / -20% +10% hits / -30% +20% hits | **Built** |
| Arcane Ward Harness (Arcane) | Inscription (Magery) *proposal* | blank scrolls 10/20/40; black pearl 10/20/40 | blue diamond | +15 Magic Resist / absorbs one damage spell, 60 s recharge / below 15% hits, sent to the stable | **Built** |
| Soul Tether (Keepers) | Inscription (Spirit Speak) | blank scrolls 10/20/40; grave dust 10/20/40 | taint | rises on its own after 2 minutes, no fee / pack kept on death / no skill loss on resurrection | **Built** |
| Field Smelter Rig (Smiths) | Blacksmithy (Arms Lore) *proposal* | ingots 25/50/100; sulfurous ash 10/20/40 | fire ruby | smelts one ore pile a minute / a forge beside the mule / also an anvil | **Built** |
| Survey Saddle Roll (Maritime) | Cartography (Fishing) *proposal* | blank maps 5/10/20; leather 5/10/20 | white pearl | maps and SOS weigh 0, reveal +1 chunk / quest arrow to a map or SOS / the mule digs the chest | **Built** |
| Shadow Cloak (Thieves) | Tailoring (Hiding) | cloth 20/40/80; nightshade 10/20/40 | corruption | hides with the owner / stays hidden while the owner stealths / hides when attacked | **Built** |
| Salvage Bin (Custodians) | Tinkering | ingots 15/30/60; boards 10/20/40 | parasitic plant | trash for Clean Up points / picks up filtered items near the owner / salvages a salvage bag + Clean Up points | **Built** |
| Minstrel's Bells (Bards) | Tinkering (Musicianship) | ingots 10/20/40; gears 1/2/4 | perfect emerald | monsters lose the mule now and then / 10% to calm an attacker / owner's bard skills easier within 8 | **Built** |
| Trader's Ledger (Merchants) | Inscription | blank scrolls 10/20/40; leather 5/10/20 | turquoise | sell cargo (100 lines) / 250 lines, +10% / portable bank | **Built** |
| Steady Hoof Wraps (Dojo) | Tailoring (Bushido) | leather 15/30/60; cloth 10/20/40 | ecru citrine | resist dismount 25% / 50% / immune + shorter remount | **Stubbed** (section 5) |
| Imbued Barding Socket (Artificers) | Tinkering (Imbuing) *proposal* | ingots 10/20/40; amethysts 5/10/20 | blue diamond | 1 / 2 / 3 mule properties; unravel / imbue near the mule | **Partial**: the sockets and their effects (resists, hits, carry, hits and stamina regen, capped) work; putting a property in goes with the imbuing rework (section 5) |

The Ore Hopper III gem chance is in the effect text but not wired to mining yet; its tooltip says so. It needs a
hook in our mining extension (section 9).

**How the effects are built (one line each).**
- **Numbers:** through P69's `ModifyNumbers` (`MuleModules.Apply`): Saddlebags, Harness, Trailwise stamina and slot 0,
  Barding hits and reduction, Ward resist, Tether II keep-pack, Socket values.
- **Every hit, once:** `PackMule.Damage` (pinned `Mobile.Damage` is the one choke point for all damage, Mobile.cs:5956).
  Barding and Deepdelver apply there. Deepdelver used to sit only in the melee and spell hooks.
- **Weight:** `PackMuleBackpack.GetTotal` and `CheckHold` take the discount, the pinned `BaseQuiver` way
  (BaseQuiver.cs:114-128). Items inside a satchel are not discounted twice.
- **Timed effects:** one static two-second tick over the mules with modules (`MuleModules.Tick`), not `OnThink`: a pet's
  AI stops when its sector goes idle (agent: BaseCreature.cs:4186-4199).
- **Homing:** left behind more than 12 tiles on the same map for 3 seconds, the mule moves to the owner. Not when
  ridden, stabled, dead, or told to stay. "All come" reaches it from any distance through `EventSink.Speech`, which fires
  before speech range (agent: Mobile.cs:5590).
  - `Teleporter.DenyFollowers` is not a thing in pinned. The condition teleporter refuses the *owner* if they have
    followers (agent: Teleporter.cs:869). Homing does not go through teleporters, it follows the owner's map.
- **Arcane Ward III:** the stable trainer's own public steps (AnimalTrainer.cs:253-267, agent); the stable limit is
  respected (`GetMaxStabled`). The pack goes with the mule.
- **Soul Tether III:** pinned takes skill only after `ResurrectPet` returns (PetResurrectGump.cs:76-81 and Bandage.cs:270-274,
  agent), so the mule snapshots in `OnBeforeResurrect` and restores a tick after `OnAfterResurrect`.
- **Smelter I:** our smelt patch's `SmeltAt` with the mule's pack as the ingot destination.
- **Smelter II and III:** a hidden `[Forge]` and `[Anvil]` item that follows the mule. Pinned's check reads items only,
  never a mobile (DefBlacksmithy.CheckAnvilAndForge, agent: :30-90). The helpers delete themselves on load; the mule
  puts new ones down.
- **Survey I:** both exploration managers add `MuleModules.ExploreBonus(pm)` to the radius. The wider reveal marks
  chunks the same way walked chunks are marked, so it counts as they do.
- **Survey II:** the stock `QuestArrow` to a decoded treasure map or an SOS in the mule's pack (nearest by default).
- **Survey III:** the mule digs `TreasureMapChest` + guardians the way pinned's DigTimer does (TreasureMap.cs:776-812),
  with no shovel and no Mining check, within 6 tiles of the spot.
- **Shadow Cloak:**
  - I: the owner hiding raises no event, so the tick polls it.
  - II: `PackMule.OnMove` keeps the mule hidden beside a hidden, unmounted, walking owner.
  - III: hides on damage, 30 s cooldown.
- **Salvage Bin:**
  - I: the trash bag's own rules (`ClusterFCustodianSystem`).
  - II: picks up loose items within 3 tiles of the owner that match the filter (reagents, gems, gold, ore and ingots,
    hides and leather, logs and boards, bandages). Never inside a house, locked down, spawner or corpse items. It does
    **not** trash anything on the ground: those might be someone else's.
  - III: salvages the salvage bags in the mule's pack (`SalvageBag.SalvageAll`, made internal by our patch) and awards
    Clean Up points for each eligible item.
- **Minstrel's Bells:**
  - I: hostiles fixed on the mule lose it 25% of the time each tick and wait 4 s to re-acquire (`NextReacquireTime`),
    with no pinned AI change.
  - II: `Pacify` on an attacker (10%), respecting Bard-immune and Uncalmable.
  - III: our skill-check wrapper lowers the window by 10 for Peacemaking, Provocation and Discordance within 8 tiles of
    the mule.
- **Trader's Ledger III:** `BankBox.Open()`. Pinned closes it on the owner's next move or turn, as at a banker (agent:
  Mobile.cs:4329).
  - Refused in a `DungeonRegion`, while criminal, or with a combatant or any aggression in the last 30 s, monsters
    included.
  - Whether our custom dungeon regions derive from `DungeonRegion` is unverified.
- **Satchels "Unload":**
  - stock cliloc 1116072 "Unload", on the ore, lumber and hunting satchel families from tier 3, to the owner's mule
    within 12 tiles;
  - the tier 5 ore satchel reaches it anywhere on the same map;
  - lumber and hunting satchels top out at tier 3, so nothing of theirs reaches across a map;
  - `MuleSatchels.AutoUnload` is the hook for automatic sending later.

## 4. Traits boost modules (`MuleModuleData.TraitBoosts`, per grade I / II / III)

| Trait | Module | I | II | III |
|---|---|---|---|---|
| Emberblood | Field Smelter Rig | smelts 20% faster | 40% | 60% |
| Burdened Bloodline | Ore Hopper, Timber Rack | 5 more points of weight saved | 10 | 15 |
| Burdened Bloodline | Clockwork Load Harness | 5 more points of pack weight | 10 | 15 |
| Surefooted | Trailwise Tack | 10% more stamina, warning range 10% wider | 20% | 30% |
| Stoneback | Expedition Barding | 3 more points of damage reduction | 6 | 9 |
| Nightmare-Kin | Arcane Ward Harness | 5 more Magic Resist, ward recharges 5% faster | 10 | 15 |
| Deepdelver | Field Medic Pack | heals 25% faster in dungeons | 50% | 75% |
| Celestial Tempered | every installed module | module numbers +2% | +4% | +6% |

Weight saved is capped at 90%, and damage reduction at 50%.

## 5. Part E: what needs a pinned change

**Steady Hoof Wraps (stubbed).**
- **The dismount paths** (agent, all under `P\UOContent\`):
  - `Dismount.DoDismount` (Items\Weapons\Abilities\Dismount.cs:63), used by the ability, monsters and InfusedThrow;
  - `RidingSwipe` (RidingSwipe.cs:38, through `BaseMount.Dismount`);
  - `Bola`, which nulls `Rider` directly (Items\Misc\Bola.cs:71-74, so `SetMountBlock` alone would not catch it: a
    correction to P47 5.4);
  - Meraktus's area dismount (Meraktus.cs:238);
  - the icy patch (IcyPatch.cs:66).
- **Alternatives:**
  - (a) No patch: re-mount the owner on the next tick after an unwanted drop. It cannot tell a dismount from a
    voluntary one, and the rider still falls for a tick.
  - (b) Make the `Rider` setter virtual. It is a core change, and it is not where the cause is known.
  - (c) One static check in our code, `PackMule.ResistsDismount(rider, attacker)` (roll by tier, message), called with
    an early return at the four sites above.
- **Plan (c):** one `.patch` of about 15-20 lines.
  - Sites: `DoDismount` entry, `RidingSwipe` before `BaseMount.Dismount`, `Bola` around `Rider = null`, and
    optionally Meraktus and IcyPatch.
  - **F-39's new dismount sources call the same check**, so the module covers them.
- **Shorter remount (III):** no patch. `PackMule.OnDoubleClick` is ours, so it can set `Rider` past the block. We track
  the time ourselves, since the block's expiry is private (PlayerMobile.cs:1089-1107, agent).
- **Self-dismounts are never resisted:** transform, polymorph and flying.

**Trader's Ledger I-II, sell from the mule's pack: built with our own flow, no patch.**
- **Pinned:** the sell list scans only the seller's backpack, and the reply refuses items whose `RootParent` is not the
  seller (BaseVendor.cs:1039-1065, :435, agent).
- **Option B, a `BaseVendor` patch:** about 20 lines and the native window. But it patches a busy pinned file, it is
  unverified whether the client lists items from a container it has never seen, and the bonus would need a second hook.
- **Option A, chosen:** a mule window that targets a vendor and lists what it buys from the mule's pack. It uses the
  vendor's own `IShopSellInfo` (types, sellable, price), resells into its `BuyPack` what it resells, and caps the lines
  per trip (100 at I, 250 at II, pinned's own cap is 500). II adds 10% to the price, far under the 1.9x resale margin
  (GenericSell.cs:83, agent).

**Field Medic Pack II, bandaging the mule from 6 tiles: not built.**
- `Bandage.Range` is a global static checked three times (Bandage.cs:16, :84, :215, agent).
- **Plan:** extend the existing `Bandage-pet-mimic-targeting.patch` style, about 10 lines. `InternalTarget` gets an
  `OnTargetOutOfRange` override that calls our hook, and `:215` reads a range from our static.
- The self-cure half of II is built.

**Minstrel's Bells I and III:** sized first. Both done without a pinned change (section 3), so nothing moved here.

**The soul forge (Imbued Barding Socket II-III) and imbuing into the socket.**
- **Pinned has no Imbuing engine.** The shard's imbuing is `C\ArtificersImbueGump.cs`, which has no soul-forge concept,
  and the `ArtificersToolkit` already opens it anywhere for members (agent: C\ArtificersToolkit.cs:31-59). So "the mule
  counts as a soul forge" grants nothing until imbuing gets a location gate.
- **The design doc** (`docs\artificers-imbuing-design.md`, "Mule soul forge") describes tiers and a forge bonus that do
  not exist in code.
- **Built:** the socket item, its caps, and the effects of its values.
- **Not built:**
  - adding a `MuleSocket` flag and catalogue rows to the imbue gump (about 60 lines, agent);
  - an `ImbueSite` resolver (mule II/III, guildmaster forge, toolkit) for the rework.
  Both belong to the imbuing rework prompt, not here.

**Also outside this task:**
- An SOS in the mule's pack can be tracked (Survey II) but is not found by fishing: pinned Fishing scans the player's
  own pack (Fishing.cs:201, 241, agent).
- The Survey Saddle Roll III digs treasure maps only. An SOS is fished, never dug.

## 6. Build and tests

Through `docker\uo\build.sh -t sl-modernuo:cc-p70`; `latest` not moved; nothing deployed, restarted or committed. Logs
`D:\UO\cc-p70-build*.log` (not committed).

| Run | Result |
|---|---|
| 1-3 (`--tests-only`) | compile: the generator's own `Sockets`/`Filter` properties (fields renamed); pooled enumerators (`FindItems`, `GetItemsInRange`) cannot take LINQ or `yield`; `using` for `StaticTarget`, `BaseHouse`; `IShopSellInfo.IsResellable` instead of a buy-info type; a gump `in` argument used in a lambda. Run 3: compiles, every existing test passes |
| 4 (`--tests-only`) | 1080/1084: the module numbers hook was not subscribed in the test host (it runs no `Configure`; made idempotent and called by the fixture), and my hauling arithmetic was wrong (ingots weigh 0.1) |
| 5 (`--tests-only`) | 1084/1084 |
| 6 **red** (`--tests-only`) | eleven deliberate breaks (a duplicate guild, no tier check, no previous-tier check, no rank check, no weight factor, no Trailwise stamina, no ward, no forge, no pickup filter, no sellables, satchel tier 4): **all 11 module facts failed**, nothing else (1073 passed) |
| 7 to 10 | **1084/1084; image `sl-modernuo:cc-p70` built** ("Built sl-modernuo:cc-p70 with patches applied and 1084 shard test(s) passing"; the last after the CHANGELOG and the corrected module states) |

**The facts** (`server\tests\Mobiles\Mule\MuleModuleVerification.cs`):
1. The data.
2. Attach and detach rules.
3. Recipes and the previous-tier rule.
4. Schematic gates and purchase.
5. Hauling weights and room.
6. Survival: Trailwise, Homing, Medic, Barding and Tether.
7. Arcane Ward: resist, absorb and stable.
8. Utility: forge and anvil, Survey reveal, track and dig, Shadow.
9. Salvage Bin and Bells.
10. Ledger sale, bank gate, Socket and the stubbed Wraps.
11. Satchel Unload.

## 7. Patch notes

`CHANGELOG.md` 2026.10.12.9:
- **Added:** the modules; schematics and crafting; satchels unloading to the mule; the Options menu.
- **Changed:** traits strengthen modules.
- **Staff:** `[add MuleModule`, and what is not yet working.

`VERSION` is 2026.10.12.9.

## 8. Register (proposed for the overseer; agents do not edit `docs\`)

The last number read was **D-122**; cc-P69's note proposed D-123 for the mule. Re-check before numbering.
- **D-124 | Ours (cc-P70, F-33).** Mule modules: 17 guild modules, three tiers, learned schematics, crafted with
  monster parts, one per guild, as many as the mule's tier. | logistics companion | `visible` | `cc-P70`
- **D-125 | Ours.** A portable bank (Trader's Ledger III): the bank box opens from the mule anywhere but dungeons,
  combat or while criminal. | convenience | `visible` | `cc-P70`
- **D-126 | Ours.** The mule digs a treasure map's chest without a shovel or a Mining check (Survey Saddle Roll III).
  | convenience | `visible` | `cc-P70`
- **D-127 | Ours.** A wider exploration reveal with the Survey Saddle Roll, counting as walked chunks. | exploration
  | `visible` | `cc-P70`
- **D-128 | Ours, not yet active.** The mule as a portable soul forge (Imbued Barding Socket II-III): it waits on the
  imbuing rework, since the Toolkit already imbues anywhere. | crafting | `visible` | `cc-P70`

## 9. Deviations and decisions for Chase

1. **Schematic ranks:** this prompt's Apprentice / Journeyman / Master (1/2/3), or cc-P78's 1/2/4.
   `MuleSchematics.RankFor`.
2. **Craft-by proposals** (italic in the table): Miners on Blacksmithy, Rangers on Tailoring, Healers on Alchemy,
   Arcane on Inscription, Maritime on Cartography, Smiths' secondary Arms Lore, Artificers on Tinkering with Imbuing.
3. **Materials and the III parts** (section 3): proposals, modest, existing items only. Where the named ML/SA parts
   drop on this shard is stock and unchecked. A feature chat may want mule-specific drops.
4. **Prices** (section 2) and **effect numbers** (sections 3-4): all in data, for tuning.
5. **The Smelter's forge and anvil serve anyone beside the mule.** Owner-only needs a pinned hook in
   `DefBlacksmithy.CheckAnvilAndForge`. Keep, or patch.
6. **The soul forge clash:** decide what the Artificers' Toolkit becomes (for example browsing only, or Basic tiers
   only), so the mule's forge means something.
7. **Ore Hopper III's gem chance** is not wired to mining. It needs a hook in our mining extension (one call). Next
   prompt or a defect.
8. **The Clockwork Scavenger** (League auto-loot) does not exist. Load Harness III's redirect waits on it. The II
   auto-sort into bags is also not built (its categories need your call).
9. **Patches still to write:** Steady Hoof Wraps (section 5, the F-39 shared check) and ranged bandaging. Say if they
   should come next.
10. **Salvage Bin II never trashes ground items**, only picks up what the filter keeps. "Junk to the bin" is the
    owner's own manual trash (I).
11. **Two exploration managers** run on every step (headline 6). Worth a cleanup task to keep one.
12. **Soul Tether I** is a self-resurrection after 2 minutes, no fee. "Cheaper, faster" had no pinned fee to cut, since
    pets are resurrected only by Veterinary, Gift of Life or staff (agent).

## For Chase

**Deploy (when you choose):** commit (autopilot does), build with `docker/uo/build.sh`, recreate the test shard. No
player package change. The mule's menu uses stock text, so existing clients show "Options" and "Unload".

**In-game checklist (test shard):**
1. **Learn a schematic:** join the Tinkers' Union, reach Apprentice, hold 20 Tinkers' scrip and 5 Mining Vouchers (or
   staff-set them). At the guildmaster's hall page, choose "Mule module schematics" and buy Clockwork Load Harness I.
2. **Craft it:** tinker tools, the "Mule Modules" group. With 15 ingots, 2 gears and 10 bone, make it. Without them
   the gump refuses.
3. **Attach and detach:** drop it on your mule. Its properties list it. Mule menu "Options", Remove: it is back in
   your pack, still tier I.
4. **Refused on a low tier:** `[add MuleModule TimberRack 3` and drop it on a tier 1 mule: refused, still yours.
5. **Upgrade:** learn tier II and make it with a tier I in your pack; the tier I is used up only if the craft
   succeeds.
6. **Trailwise Tack III:** fit it on a tier 3 mule. Your follower count drops by one; take it off and it comes back.
7. **Homing:** with Trailwise II, go through a gate without the mule. Within a few seconds on the same map it is
   beside you. Say "all come" from far away.
8. **Soul Tether II:** kill the mule with its pack full. The corpse is empty and the pack is still on the mule ghost.
   Resurrect it.
9. **Hauling:** 100 iron ingots in the pack, then fit an Ore Hopper. The pack's weight drops.
10. **Track map and dig:** decode a treasure map and put it in the mule's pack. With Survey II: Options, then a map
    name, and the arrow points there. With III, at the spot: Options, "Dig here". The chest and guardians appear.
11. **Bank refused in a dungeon:** with Trader's Ledger III, Options, "Open your bank box": works in town, refused in
    a dungeon, while criminal, or right after a fight.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`, after the last change:

```
Repo Result
---- ------
code dry run
docs dry run
```

21 files pending in code and 1 in docs (this note). Nothing was refused and nothing is near 5 MB. Every file this task
wrote is ASCII, and so is every line it added to an existing file. Four files I edited keep their old box-drawing
banners: `ClusterFExplorationManager.cs`, `ClusterFExplorationSync.cs`, `ForestersLumberSatchel.cs` and `PackMuleBackpack.cs`.

P70 DONE
