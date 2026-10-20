# Code intake assessment, batch 1 (cc-P212, 2026-10-20): six downloads of 2026-10-14 to 10-20

Read-only assessment of six code downloads listed in `D:\UO\third-party\CODE-INTAKE.md`, judged for the shard's
ModernUO in the format of P93 (`D:\UO\third-party\code\PORT-ASSESSMENT.md`). Nothing was built, run, installed,
extracted or copied; `CODE-INTAKE.md` was not edited. SVDungeon 0.7.0 is P211 and Great Pumpkin is parked, so neither
is here; the three tool trials are P214.

**Baseline.** Engine citations are from `D:\UO\ModernUO-pinned` at **d4531cd94** (paths under `Projects\`). ServUO
citations are from `D:\UO\ServUO-pub57`. Shard citations are from `D:\ShatteredLegacy\server` (read in the Bronze
work copy). Tile names are from the vanilla 7.0.117.0 `tiledata.mul` through vseUOAware. Statements marked
**(guess)** were not verified. Every count below was counted (`wc`, `grep -c`, `find | wc -l`), and the P93 rulings
stand: Feng's Invasions and Virtual Storage are "borrow the idea only", Level System Extreme is idea only, and F-12
gives no free skill or stat points.

**Frame.** As in P93: the faithful port comes first, these are custom-lane work (`docs\community-scripts-wishlist.md`
rules: license first, design description not a file to copy, base-class edits argued first, player-facing work gets
a wiki entry). None of the six is a port-list item.

## Summary

| Module | Serves | Effort | ModernUO blockers | License | Recommendation |
|---|---|---|---|---|---|
| Flying System (Wilson) | Flying mounts, flying bosses, F-35 bird line | Rebuild only (the design does not survive) | Static shared state, Z written straight, shadow mobiles every 300 ms, `EventSink.Login`, 57 hand Serialize | none stated | **Skip the code; borrow one idea** (a flying mount crosses water, on pinned's `Flying` flag) |
| Rune marking chest (Dameon) | Travel QoL, F-13 League rune, F-35 beat 9 | 0 (pinned has it) | none; movable version is an exploit | none stated | **Skip: pinned's `MarkContainer` already does it** |
| Animal Taming BODs (ScriptVisitor) | Companions taming loop, F-18, F-20 | S-M as ours, on the P122/P123 BOD plumbing | 22-file patch incl. core `Gump.cs`; BOB entry serialization; spawns creatures to score rewards; needs ScriptVisitor Utils | none stated | **Borrow the idea only** (a Rangers' taming order type) |
| Double light saber (Dameon, art by Erad) | F-levelable gear looks | S, if art existed | The art is on neither disk nor in the client (0xC4E0 is empty) | none stated; Star Wars look | **Skip** (stock `DoubleBladedStaff` reskin without its art) |
| ServUO PlayerBot (bpace) | Overnight play-test bot (P91, P102) | M whole; S per piece | `IPooledEnumerable.Free`, `GenericWriter`, `MovementPath` ctor, murder-system API, `Serial` width; PK and thief roles hit real players; LAN dashboard | MIT | **Borrow the approach** (citizens for the soak, a walkability audit, stuck telemetry); never the dashboard, PK, thief, shop or guild pieces |
| UO Wildlands scripts (Feng) | Companions, spawns, invasions, townhouses, QoL | per system, section 6 | ServUO Pet Training API in 37 mobiles and the pet gump; 11 stock-file replacements that collide with pinned; `Persistence`; a core `Server` change for free skills | **GPL-3.0**, reference only | **Idea only, per system**: pet gump slayer block (P96), legendary-hue tier, wave-spawner shape, townhouse region for F-44; free skills **skip** (F-12); invasions and virtual storage keep P93's rulings |

**In one line:** nothing in this batch is a port. Two give ideas worth a design line later (a flying mount on
pinned's own flag; a taming order type on our BOD engine), the chest is already in pinned under another name, the
saber has no art, the player bot gives the overnight bot three borrowed pieces, and Feng's collection is a per-system
idea list under a GPL caveat Chase has not yet ruled on.

## Per module

### 1. Flying System, GD13 (`code\flying-system`)

1. **What it does.** Three things in one zip. (a) Player flight by wire: with a Golden Feather while riding a
   `FlyingHiryu`, or with a Magic Flying Rug or Magic Flying Device unmounted, a 300 ms timer reads the player's
   facing and running bit and writes `Z`, `X` and `Y` straight: running climbs, walking descends, and the player is
   carried one tile per tick in the facing direction while `CantWalk` refuses their own steps (`FlyingTimer.cs:11`,
   `:244-540`; `GoldenFeather.cs:27-35`; `FlyingRug.cs:41-55`). A Flight Totem in the pack toggles level flight
   (`FlightTotem.cs:25-45`). (b) Flying creatures: `BaseFlying : BaseCreature` moves itself the same way in `OnThink`
   with a fly stamina, lands when it runs out, and turns around at map edges, water, rock, lava and tall statics
   (`BaseFlying.cs:89-224`; `FlyingMap.cs:118-194`; `FlyingTileCheck.cs:102-187`). (c) Shadows: every tick a
   throwaway `BaseCreature` (or a 9-piece rug `BaseAddon`) is spawned on the ground under the flier and deleted
   300-450 ms later (`FlyingTimer.cs:45-227`; `FlyingPlayerShadow.cs:9-27`; `FlyingBlueFancyRug.cs:7-26`). Serves:
   flying mounts and bosses, which the intake list ties to the mounts work and F-35's bird line.
2. **Dependencies and counts.** 62 .cs, 7,510 lines (`wc`), 57 with a hand `Serialize` (the 5 without: Direction,
   Login, Map, TileCheck, Timer), matching SOURCE.txt. 41 creature classes in 40 files (`FlyingBird.cs` also holds
   `FlyingTropicalBird`): 29 are copies of a stock type with "Flying" prefixed (Balron, Bird, CrystalWisp, Daemon,
   DarkWisp, Dragon, Drake, Eagle, Efreet, ElderGazer, EtherealWarrior, Gargoyle, GargoyleDestroyer,
   GargoyleEnforcer, Gazer, GreaterDragon, GreaterMongbat, Harpy, Mongbat, Pixie, ShadowWisp, ShadowWyrm,
   StoneGargoyle, StoneHarpy, StrongMongbat, TropicalBird, VampireBat, WhiteWyrm, Wisp; all 29 exist in pinned), 12
   have no pinned namesake (ColdDrake, CrimsonDrake, EffetePutridGargoyle, EffeteUndeadGargoyle, FireDaemon,
   FrostDragon, FrostDrake, GargoyleGuardian, GargoyleShade, PlatinumDrake, SAPixie, UndeadGargoyle; shard
   customizations not checked). `FlyingHiryu` is a stat-for-stat copy of ServUO's `Hiryu` with no flight code of its
   own (`FlyingHiryu.cs:11-50`): the flight is the feather plus the timer, keyed on `pm.Mount is FlyingHiryu`
   (`GoldenFeather.cs:27`) and body 243 for the shadow (`FlyingTimer.cs:199-203`). `EventSink.Login` resets state on
   login (`FlyingLogin.cs:9-41`). Items: feather 0x1BD1, rug 0xA57 (tiledata: "bedroll"), device 0x1B7A as a
   `BaseShield`, totem 0x2F5A (tiledata: "Talisman"). Active state is kept in the item's `Name` string
   ("Magic Flying Rug-Active", `FlyingRug.cs:53-54`, `FlyingLogin.cs:25-35`).
3. **ModernUO fit, and what pinned's own flying is.** Pinned has `Mobile.Flying` (`Server\Mobiles\Mobile.cs:1193`), a
   status flag only: it is sent as flag 0x04 in SA-era mobile packets (`:7083-7086`), remaps gargoyle animations
   (`:6796-6810`), lets a flier step onto "hover over" tiles (`UOContent\Engines\Pathing\Movement.cs:277, :370`),
   counts as mounted for Dismount and Infused Throw (`Items\Weapons\Abilities\Dismount.cs:33-85`,
   `InfusedThrow.cs:31`) and for AI speed (`Mobiles\AI\BaseAI\AIMovement.cs:97`). Only gargoyles toggle it, through
   packet 0xBF sub 0x32 (`Network\Packets\IncomingExtendedCommandPackets.cs:61, :272`), `PlayerMobile.ToggleFlying`
   (`PlayerMobile.cs:750-822`) and `FlySpell` (`Spells\Gargoyle\SpellDefinitions\FlySpell.cs:7`). **Pinned never
   changes Z for flight; the client draws the hover.** Wilson's system is the opposite: a server-side altitude
   written into `Mobile.Z` every 300 ms, which the client receives as a stream of teleports (guess: not run). The
   mechanical port items (`[SerializationGenerator]` on 57 files, `PlayerLoginEvent` for `EventSink.Login`,
   `GetStaticAndMultiTiles` for `GetStaticTiles(x, y, true)`, `GetWeaponAbility` for `SetWeaponAbility`, no
   `Regions.Jail` class in pinned) are the small part; the design is what does not fit.
4. **Effort.** Not portable as written; a rebuild from the idea only (see 6). As a straight port it would be M for
   the code and then unusable (5 below).
5. **Risks (read in code, worst first).**
   - **Every flier shares one state.** `FlyingTimer`'s `Ground`, `HasTakingOff`, `LastDirection`, `flyCnt` and
     `RugPicked` are `static` (`FlyingTimer.cs:12-17`), so two players flying at once overwrite each other's ground
     height and landing flag. `BaseFlying`'s `Ground`, `LastDirection`, `Landing`, `M_FlyStam`, `F_Stam` and
     `F_Shadow` are static too (`BaseFlying.cs:10-27`) and are serialized per instance from the static
     (`:349-365`): every flying creature on the shard shares one stamina and lands together.
   - **Movement validation is bypassed.** `Z`, `X` and `Y` are assigned directly (`FlyingTimer.cs:338-540`,
     `BaseFlying.cs:130-152`), so a flier moves while paralyzed or frozen, and nothing but the author's own tile
     checks keeps them out of walls: the look-ahead checks one tile in the facing direction only, static water
     checks are commented out (`FlyingTileCheck.cs:150-170`), multi and mobile checks are marked "NOT WORKING CODE"
     (`:200-289`).
   - **Melee is zeroed by height** for creatures (`BaseFlying.AlterMeleeDamageFrom`, `:264-285`; the `To` override
     calls `base.AlterMeleeDamageFrom`, a copy-paste bug, `:287-311`), so a hovering creature cannot be meleed at
     all from the ground; ground monsters cannot path to a player at Z+20 (guess: pinned's `InRange` is 2D, so a
     monster standing under the flier may still hit; not run).
   - **Pet loss.** `BadLocationCleanup` deletes (not kills) a grounded flying creature whose Z is below the land or
     that stands on impassable land (`BaseFlying.cs:75-86`); `FlyingDragon` and others are tamable (`FlyingDragon.cs:47-49`).
   - **Object churn.** One shadow mobile per flier per 300-450 ms (a serial, `World.AddMobile`, a timer each), or a
     9-component addon for rugs; a save during flight writes them (they delete on load, `FlyingPlayerShadow.cs:26`).
   - Plain bugs: `flyRug = ft as MagicFlyingRug` uses the totem variable, so the rug never resets on landing
     (`FlyingTimer.cs:250`); `flyTot.Delete()` throws if the totem was dropped (`:311, :640`); `OnBeforeDeath` spins
     in a `while` loop with no delay to "fall" (`BaseFlying.cs:314-331`); direction is matched by its enum string,
     including the running bit as "129".."134" (`FlyingDirection.cs:7-50`); `CantWalk` is saved on the player
     (`Mobile.cs:2382`) and only login clears it.
   - Fit with the mount plans: the F-35 bird line ends on Lesser Hiryu body 243 (`docs\feature-queue.md:2990`), the
     companions design reserves "one evolution mount" (`:2584`; `notes\cc-P41-companions-research.md:598`), and the
     candidate rideable red dragon is TheArt's `L-Ridable Red Dragon.vd` (5.7 MB, over the repo rule, P139-D6 open:
     `notes\cc-P134-vseuoaware-art-checks-mcp.md:192`, `cc-P146-playtest-decisions-inbox.md:358`). None of those
     needs altitude; a dragon that cannot be meleed and carries its rider over the sea would need rules of its own.
6. **Recommendation: skip the code; borrow one idea.** When a flying mount exists (hiryu stage, red dragon), give it
   flight on pinned's terms: the rider gets `Flying = true` while mounted, which already makes Dismount and Infused
   Throw treat them as mounted, and one small `Movement.cs` patch lets a `Flying` rider cross `Wet` land the way
   `CanSwim` does (`Movement.cs:496` is the line; argue the patch in notes first). No altitude, no shadows, no new
   creature AI. Flying bosses "out of melee reach" are a dive-room design (a platform or region rule), not a Z hack.
   Credit Wilson for the idea if it lands.

### 2. Rune marking chest (`code\rune-marking-chest`, "Marking Mailbox.cs")

1. **What it does.** `RuneMailbox : Container`, item 0x9AB (tiledata: "metal chest", not a mailbox), 10 stones and
   movable (`:11-16`). Dropping a blank recall rune into it marks the rune **at the dropper's current location**
   through `rune.Mark(from)`, names it "Mailbox Rune" if unnamed, and stores it (`:23-82`). Nothing else. Serves:
   travel QoL (a rune without Magery).
2. **Dependencies.** None beyond `RecallRune.Mark(Mobile)`. 1 .cs, 99 lines, 1 hand Serialize (SOURCE.txt is right).
3. **ModernUO fit, and what the shard already has.** Pinned ships `MarkContainer` (`UOContent\Items\Containers\MarkContainer.cs:7-262`): a
   chest (plain 0xE79 or bone 0xECA, `:48-62`) that marks any rune dropped or placed into it (`:200-220`) to a
   staff-set `Target`, `TargetMap` and `Description` (`:34-45`), **immovable** (`:51`), optionally magic-locked with
   a 5-minute relock (`:63-80`, `:230-258`), spawned by `Decorate` and `DecorateMag` and by `[SecretLocGen` for the
   Malas secret passages (`:116-135`). `RecallRune.Mark(Mobile)` is in pinned too (`RecallRune.cs:121`), so Dameon's
   "mark where I stand" variant would be a 15-line override if it were ever wanted. Shard travel work that could
   want a marking chest: the F-13 League reward "blessed recall rune marked to the League Registrar"
   (`docs\feature-queue.md:1345`; not built, 0 hits for `RecallRune` or `LeagueRune` in `server\customizations`),
   F-35 beat 9 "home by rune or gate" (`:2791`), and the Staff Hub Travel tab (`:2362`). All of them are served by
   placing a `MarkContainer` with its target set: zero code.
4. **Effort.** 0.
5. **Risks.** The movable chest is the exploit: `RecallRune.Mark(Mobile)` does not run the Mark spell's
   `SpellHelper.CheckTravel`, which is exactly what the shard's no-mark zone relies on
   (`customizations\FountainOfYouth\FountainSanctumRegion.cs:10-11`), so a player carrying this chest marks runes
   inside any no-mark region and without Magery. Pinned's version avoids both by being immovable and staff-targeted.
6. **Recommendation: skip.** Pinned already has it under another name (the AGENTS.md "equivalents hide under
   different names" rule). If the tutorial or the League wants a "mark your rune here" chest at the Registrar, use
   `[add MarkContainer` and set `Target`/`TargetMap`/`Description`; log it in the seeder if it should survive a
   fresh world. Never a movable marking container.

### 3. Animal Taming BODs, FS-ATS inspired (`code\fs-ats-taming-bods`)

1. **What it does.** A bulk-order type for tamers on ServUO's 2016 BOD engine. A `BodAnimalTrainer : AnimalTrainer`
   hands out deeds to anyone with Animal Taming above 0, once per cooldown of 1, 2 or 6 hours by skill, with a large
   deed chance of (skill - 40) / 300 above 70.1 (`NPC\BodAnimalTrainer.cs:14-62`). A small deed asks for 10, 15 or 20
   of one species from a 70-entry list (`Data\Bulk Orders\Taming\smalls.cfg`, 70 data lines), rolled by skill
   (`SmallTamingBOD.cs:76-93`). The player fills it by targeting **their own controlled pet, which is deleted** and
   counted; bonded pets, summons, other players' pets and polymorphed creatures are refused (`SmallTamingBOD.cs:155-205`).
   A large deed asks for one of ten families (mounts, hard mounts, dragons, farm animals, spiders, felines, canines,
   bears, birds, rodents: `LargeTamingBOD.cs:44-58`, one `.cfg` each). Rewards: points of 10/25/50 by amount plus a
   per-creature bonus `(cap / 100 x MinTameSkill x ControlSlots / 3) x 2`, capped at 450
   (`TamingRewardFormula.cs:8-30`), gold 3,600 to 30,000 by family size and amount (`TamingRewardCalculator.cs:129-158`),
   and reward items from `Data\TamingBodRewards.xml` (3 entries: a wooden horse statue at 10 points, a Pet Power
   Scroll 105 at 50, an Animal Lore power scroll 115 at 80). The Pet Power Scroll is a cursed scroll that raises one
   of 21 pet skill caps (`PetPowerScroll.cs:9-33`). Serves: the companions taming loop, F-18 (BODs that grow skill),
   F-20 (BODs for other crafts), F-25 (banked rewards).
2. **Dependencies and counts.** 33 .cs in all (SOURCE.txt), of which 10 are the author's (1,910 lines, `wc`) and 23
   are patched copies of stock pub57 files. `patch.diff` touches **22 files in 52 hunks** (`grep -c` of
   `diff --git` and `@@`), among them core `Server\Gumps\Gump.cs` and `GumpTooltip.cs` (custom tooltip text in the
   reward gump), `PlayerMobile.cs` (a `NextTamingBulkOrder` timer), `BODType.cs` (a `Taming` value),
   `BulkOrderSystem.cs` (11 hunks), and the Bulk Order Book entries `BOBSmallEntry.cs` and `BOBLargeSubEntry.cs`,
   whose serialization version changes: the readme warns the system cannot be removed once a world is saved
   (`readme.txt`, DISCLAIMER). Needs ScriptVisitor Utils v1.0.2 (an `SVLogger`, `TamingRewardCalculator.cs:2`), not
   on disk. 8 hand Serialize among the author's files (SOURCE.txt says 8; `grep -l` finds 8 across the whole
   folder's author files, consistent).
3. **ModernUO fit, and what the shard already has.** The intake row is right: the shard already replaces
   `LargeSmithBOD.cs` and `BulkMaterialType.cs` (`server\patches\`), and P122/P123 built the shard's BOD engine on
   pinned's `SmallBOD`/`LargeBOD`: `BODType` is extended by `patches\BODType-all-crafts.patch` (six crafts appended
   after Smith and Tailor), the Bulk Order Book by `BOB-all-crafts.patch`, the new deed pairs share
   `customizations\Services\BulkOrders\CraftBOD.cs` (`:1-60`), and each guild hands out its own types through
   `BulkOrderGivers.cs:37-38`. So a taming order type is **one more `BODType` value, a Small/Large pair on the
   existing pattern, and a giver line for the Rangers' League**: ours, not a port, and the patch's 52 hunks reduce
   to the enum and book hunks the shard has already paid for. Pet Training is ported
   (`customizations\Services\Pet Training\TrainingProfile.cs`), so a pet-cap reward has somewhere to point.
   The reward calculator scores a deed by **instantiating the creature type with `Activator.CreateInstance` and
   deleting it** (`TamingRewardCalculator.cs:47-57`, `:80-92`): the same anti-pattern P93 flagged in the specimen
   rating (never spawn sample creatures in ModernUO; read `MinTameSkill` and `ControlSlots` from a per-type table).
4. **Effort.** S-M as our own order type on the P123 plumbing (the deeds and giver are a day; the design below is the
   work). Not worth porting the patch.
5. **Risks.** The loop is "tame, hand over, pet deleted": at odds with companions as lasting partners, and farmable
   from pens (10 chickens score the 10 base points; the per-creature bonus is 0 at `MinTameSkill` 0, so the gold
   table, 3,600 per small deed, is the farm). The reward tooltip needs a core gump patch in ServUO; pinned's
   `DynamicGump` tooltips need none (guess, not checked against `BODRewardsGump.cs`). Power-scroll rewards sit
   inside F-12's rule set (per-skill cap = level cap; scrolls past 120 are "rebranded", `docs\feature-queue.md`
   F-12 decisions), and a Pet Power Scroll is a pet-cap item that F-12 has not ruled on. No license stated.
6. **Recommendation: borrow the idea only**, written up here for the companions plan:
   - **A Rangers' League taming order** (small: N of one species; large: a family set) handed out by the Rangers'
     guildmaster the way the Foresters hand out Carpentry and Fletching orders (`BulkOrderGivers.cs:37`). Rewards in
     the guild's own currency and points, like P122's Seals, never the 30,000-gold table.
   - **Species picked from the player's gain window** (F-18's approved rule applied to taming: `MinTameSkill` in the
     range the player can still gain from), with the low-skill track under 50 (farm animals only, 10 per deed).
   - **Turn-in is a stable hand-over, not a delete**: the creature goes to the Rangers' pen (deleted in code, but
     the fiction is a release) and the deed credits only creatures the player tamed themselves (pinned marks
     `Owners`/`ControlMaster` at tame time; check `AnimalTaming.cs:426-428` for what P93 #4 reads) and never bonded
     ones. Per-account daily cap on turned-in deeds to kill pen farming.
   - **Quality as a lever** once P93's specimen rating exists: a deed may ask for 3-star specimens, which is the real
     taming skill test and feeds the breeding plan.
   - **Rewards that fit F-35 and F-12**: pet-training resources, a stable slot, the Animal Lore dashboard's cosmetic
     bits, a "pet alacrity" rather than a pet cap scroll until F-12 rules on pet caps.
   - Effort S-M, after F-18's tailoring batch and before any breeding work. Credit ScriptVisitor and RoninGT.

### 4. Double light saber (`code\double-lightsaber`, "DoubleLightSable.cs")

1. **What it does.** `DoubleLightSaber : BaseSpear`, item ID 0xC4E0, Double Strike and Infectious Strike, Str 50,
   AoS damage 11-14, speed 49, ML speed 2.25, durability 31-80 (`:7-105`). Those are pinned's `DoubleBladedStaff`
   numbers (`UOContent\Items\Weapons\SpearsAndForks\DoubleBladedStaff.cs:16-31`) with the damage spread widened from
   12-13 to 11-14 (same average). So it is a double-bladed staff reskin. Serves: a look for levelable gear.
2. **Dependencies.** The art. The author posted "script and art", but only the script was attached (SOURCE.txt), so
   the art must come from Erad's set. **It is not there:** Erad's pack on disk (`D:\UO\third-party\erads-custom-content`,
   683 files) holds paperdoll gumps only for this shape, a "Double Bladed Staff.bmp" under
   `Custom UO Clothing GumpArt\Human & Elves\Weapons, Shields\Staffs\` and nine Star Wars light-saber gumps under
   `...\Inspired Assets\Star Wars\`; no item art and no `.vd` for 0xC4E0 (find for "saber", "double", "blade":
   those are the only hits). **Nor is it in the client:** item 0xC4E0 in the vanilla 7.0.117.0 tiledata is empty
   (name "", no flags). **Nor in our art store:** `player-package\vendor\shattered-legacy-art\registry.csv` (147
   lines) has no 0xC4E0 and nothing from Erad's pack; `ART-LIBRARY.md` lists Erad's pack under UI skins (`:318`).
3. **ModernUO fit.** Trivial: `BaseSpear` and both abilities exist (`WeaponAbility.cs:24, :58`); one
   `[SerializationGenerator]` file. Without art the item renders as nothing.
4. **Effort.** S for the script; the art job is the whole cost (item art, paperdoll gump, and the two-handed equip
   animation layer, as the kitsune work in F-35 showed for a worn layer).
5. **Risks.** A recognizable Star Wars prop: the paperdoll gumps in Erad's pack are literally named for Luke, Vader
   and Mace Windu. Rename is not enough if the art is the saber. No license stated for the script; Erad's terms are
   "free to use", credit Erachiro.
6. **Recommendation: skip.** P72's levelable gear takes any crafted weapon (C.1: `PlayerConstructed`, any weapon
   type), so looks come from recipes, not from one found-only reskin, and a weapon that is not in a craft table
   never qualifies. If an energy-blade look is wanted for a League dive or Rootdeep reward, file an art request for
   an original design (`scripts\art\New-ArtRequest.ps1`) and derive the item from `DoubleBladedStaff`; the script
   here adds nothing a derived class would not.

### 5. ServUO PlayerBot (`code\servuo-playerbot`)

Read by a subagent; the citations below were spot-checked in the files (the `Player = false` trick, the pinned
Internal-map rule, the `HttpListener`, the PK targeting, the 250 ms timer, the world scans).

1. **What it does.** Server-side headless "players": `PlayerBot : PlayerMobile` with `Player = false` so the core
   does not park it on the Internal map at load (`PlayerBot.cs:228-232`, again after `Deserialize`, `:477`), no
   account and no `NetState`. Roles: Traveler, Banker, Adventurer, Townie and a sparse Tamer in the random
   population; PlayerKiller, Thief and TreasureHunter only by staff spawn or stored spawns (`FEATURE-GUIDE.md`;
   `PlayerBotService.cs:484-489`). One service timer at 250 ms ticks every bot (`PlayerBotService.cs:110`,
   `:626-661`), population to 250 per facet (`:232`, `:2225`) plus fixed bank crowds. Bots walk an authored waypoint
   graph from `Data\PlayerBots\world-data.xml` (`PlayerBotWorldData.cs:132`, schema `:43-101`), BFS over audited
   legs with `Movement.CheckMovement` and ServUO `MovementPath` A* for the connectors (`:501-580`, `:920-947`); they
   bank real gold, run real harvest and craft systems as labor (`PlayerBotLabor.cs:92-110`, `:308-370`), form
   engine parties and a persistent guild, tame, dig real treasure maps, and die and self-loot. A LAN dashboard on
   `System.Net.HttpListener` (`PlayerBotDashboard.cs:56`, default `127.0.0.1:8081`, `:37-46`) draws a radar map from
   `radarcol.mul` with live bot and **real player** positions (`:239-315`, `:348-376`) and takes enable, spawn,
   remove and world-data edits through a queue drained on the game thread (`:151-237`). Serves: the overnight
   play-test bot (P91, P102).
2. **Dependencies and counts.** 16 .cs, 7,874 lines (`wc`), 2 hand Serialize (`PlayerBot.cs:356`,
   `PlayerBotShop.cs:22`; SOURCE.txt is right), 7 commands registered (`PlayerBotService.cs:95-101`: `[PlayerBots`
   with 22 subcommands, `[BotWhere`, `[BotGoto`, `[BotInfo`, and the player-level `[JoinBotParty`, `[LeadBotParty`,
   `[JoinBotGuild`). No XmlSpawner, no `Persistence`, no Vita-Nex; its XML is `System.Xml.Serialization`. Runtime
   files: `Data\PlayerBots\world-data.xml` (plus `.tmp`, `.bak`), `Data\PlayerBots\dungeon-pad-audit-<Map>.txt`,
   `Config\PlayerBotsDashboard.cfg` (rewritten at every start, `PlayerBotDashboard.cs:87-92`). MIT, with an
   `UPSTREAM-LICENSE.txt` for the uo-offline project it is modelled on. Of the two zipped tools, `Sync-Upstream.ps1`
   is documented (`UPSTREAM-CONVERSION-PIPELINE.md`) and `Import-UOOfflineRoutes.ps1` is mentioned by no shipped
   document (0 hits), so what it imports is unknown.
3. **Compared with our bot (P91).** They are different animals. Ours (`tools\playtest-bot`, Python, 2,892 lines
   across `uobot\`) is a **wire client**: it logs into a scratch copy of the test world on `127.0.0.1:2595`, speaks
   the 7.0.117.0 packets cited line by line to pinned, runs one check per open play-test id (`uobot\checks.py`,
   `p64_1` to `t_046`) three times each, and soaks with three characters for two hours; it changes no server code and
   refuses any other host or port (`uobot\safety.py`). Theirs lives **inside** the server as fake citizens. What
   theirs does better: (a) **scale**: hundreds of actors with no sockets, where our soak had 3 characters and
   22,699 steps (`notes\cc-P91-overnight-playtest-bot.md`, The soak); (b) **a route audit** that replays every
   waypoint leg incrementally (32 legs per 2 s, `PlayerBotWorldData.cs:632-696`) and a **dungeon pad audit** that
   checks live teleporters near each entrance and writes a report (`:709-781`), which is a world-walkability tool
   in its own right; (c) **stuck telemetry** clustering movement failures per bot (`PlayerBotStuckTelemetry.cs:24-55`);
   (d) a **danger map** (murder heat with a 45-minute half-life steering destination choice,
   `PlayerBotDangerMap.cs:11-45`); (e) the live map. What ours does better: it proves the wire (framing
   self-check, cliloc decoding), it produces honest per-item evidence Chase marks himself, and it cannot touch the
   live or test shards by construction. The LAN controls are the part we must never want on a shard that players
   reach (intake row), and our live container publishes 2593 only.
4. **ModernUO fit.** The headless trick carries: pinned moves `Player` mobiles to Internal at load exactly as
   ServUO does (`Server\Mobiles\Mobile.cs:6510-6515`), so `Player = false` works. `EventSink.WorldLoad` is
   `WorldEvents.cs:20`; `Timer.DelayCall`, `CommandSystem.Register`, `Movement.CheckMovement`, `Map.CanFit`,
   `BandageContext`, `Hiding.OnUse`, `Banker.Deposit`, `Party`, `Guild`, `Teleporter`, `CraftItem.Craft` all exist.
   Compile blockers in a straight port: `IPooledEnumerable` and `.Free()` (14 declarations, 17 calls),
   `GenericWriter`/`GenericReader`, `MovementPath(from, to, map)` (pinned's is `MovementPath(Mobile, Point3D)`,
   `Engines\Pathing\MovementPath.cs:12`), `NegativeAttributes.OnCombatAction`, `ReportMurdererGump.CheckMurderer`
   (pinned's murder state is `Engines\Player Murder System`), `IsStaff()`, `TargetByResourceMacroEventArgs` (pinned:
   `InvokeTargetByResourceMacro`, `IncomingExtendedCommandPackets.cs:437`), `CurrentTameSkill`,
   `Banker.Withdraw` without the bool (`Banker.cs:209`), `Serial.Value` as `int` (59 uses), `OnResponse(NetState,
   in RelayInfo)`. Effort: M for the whole thing; S for any one borrowed piece.
5. **Risks (worst first).**
   - **It hits real players.** PK bots target any living non-staff `PlayerMobile` within 12 tiles on Felucca
     outside guard zones (`PlayerBotService.cs:1137-1166`, `:1068-1074`); a bot's death files a murder report that
     raises the killer's `Kills` and `ShortTermMurders` with no consent step (`:2194-2196`); the thief test steals
     a real item with the real `Stealing` skill (`:1080-1113`); a Hawker purchase withdraws from the **player's**
     bank (`PlayerBotShop.cs:503`); a bot guild recruits real players (`PlayerBotGuilds.cs:59-84`).
   - **Load.** Every 250 ms tick scans `World.Mobiles.Values` to find the bots (`:556-562`, `:651`), the dashboard
     snapshot does two more full scans every 2 s whether or not a browser is open (`PlayerBotDashboard.cs:241-243`),
     each bot's action runs `GetMobilesInRange(8)` or `(12)` (20 range-scan sites), and every failed move re-plans
     with BFS plus A* (`PlayerBotService.cs:961-967`).
   - **Dashboard trust model.** IP allow-list only, no token or password (the token UI is under `#if false`,
     `:463-471`); `BindAddress` may be a LAN or `0.0.0.0` address; `/api/state` publishes real players' map and
     coordinates; `/api/action remove` deletes every bot; `/api/editor` writes the XML.
   - Hidden `PlayerBotShopStockMarker` items persist in bot packs (`PlayerBotShop.cs:9-35`); population reconcile
     never removes a surplus (`PlayerBotService.cs:450-467`).
6. **Recommendation: borrow the approach, port nothing.** Three pieces fit the overnight bot, in this order:
   - **Citizens for the soak.** A staff command in `server\customizations`, gated like TestAccountWipe to
     `SL_SHARD_ROLE=test` (P73), that spawns N headless `Player = false` `PlayerMobile` walkers and fighters on the
     scratch shard for the P102 soak, so the open question from P91 (memory rose 0.9 MB a minute with 3 actors)
     gets a real load of 50 or more. No routes file: loops through the seeded New Haven square and the Rootdeep
     entrance, from our seeders' coordinates. Never on `sl-modernuo` or `sl-modernuo-test`.
   - **A walkability audit.** Their route and dungeon-pad audits as one `[AuditWalk` over our seeded structures
     (New Haven, the mine camp, the guild halls, Rootdeep, the Registrar), writing a report the bot run archives:
     pinned `Movement.CheckMovement` and `MovementPath` do the work; the Staff Hub Travel tab already lists the
     seeder coordinates (`docs\feature-queue.md:2362`).
   - **Stuck telemetry** as a counter in the soak report beside saves and memory.
   - Never: the dashboard, PK and thief roles, the shop, the guild and party recruiting. Keep the MIT notice with
     any lines copied. A draft prompt for the first two is below (a "borrow" verdict, offered because it closes
     P91's open soak question).

### 6. UO Wildlands scripts (`code\uo-wildlands-scripts`)

Surveyed by a subagent folder by folder; I re-ran the counts and spot-checked the claims that carry weight (the
free-skills set, the townhouse region, the wave spawner's `Tamable = false`, the power-scroll picker's
serialization, the instant logout, the virtual-storage range).

1. **Shape and counts.** 304 .cs (SOURCE.txt is right), 79,546 lines, **276** hand Serialize (32 system, 34
   commands, 154 items, 56 mobiles: `grep -l`), matching the intake row. No XmlSpawner, no Vita-Nex; the
   `ShrinkSystem` it uses is Feng's own, inside `CUSTOM ITEMS\PetLeash.cs:19-30`. Every custom file carries a
   GPL-3.0 header crediting Feng and the original author where there is one (Voxpire, Ravenwolfe, Felladrin,
   Tresdni, JesteR). **Three sub-packs are the same code as downloads P93 already assessed:** Custom Pet Gump is
   `code\animal-lore-gump` (`diff -w` of the three stock files is empty; the dashboard is 55 lines newer, a
   "Slayer Vulnerabilities" block from `SlayerGroup.Groups`, `DashboardAnimalLoreGump.cs:308-331, :552-583`), the
   Invasion System is `code\invasions-feng` (both files identical), and Virtual Storage is `code\virtual-storage`
   (12 of 13 files identical, one differs in whitespace). P93's rulings on those three stand.
2. **System by system: what Feng has, what we have, what overlaps the queue, what to borrow.**

   | System (folder) | What Feng's does | What the shard has | Overlaps in the queue | Borrow |
   |---|---|---|---|---|
   | Pet gump (CHANGED, Custom Pet Gump) | One-page Animal Lore dashboard on ServUO `BaseGump`, plus a slayer-vulnerability block | Pet Training is ported now (`customizations\Services\Pet Training\TrainingProfile.cs`), so P93's "after Pet Training" gate is open; P96 draft exists | #82 (this), #438 MyStats | **Yes, the slayer block** goes into the P96 rebuild; nothing else new |
   | Companions (MOBILES\Companions) | 6 dog breeds as `BaseMount` clones, bodies 0x60A-0x610 (1546-1552), mount art 0x3ED4-0x3ED9, statues 0xA76B-0xA770; `bodyTable.cfg` is byte-identical to stock and adds nothing | F-35's stage-3 dog pick **is these six bodies** (1546 Newfoundland to 1552 Rottweiler, `docs\feature-queue.md`, stage picks), rendered by P59 and built by P65 | #435 Custom Pet Bundle (Feng), #456 Malamute, #455 Companions | Nothing: the bodies are already in the evo framework; the statues are a stable-slot idea F-35 does not need |
   | Legendary pets (MOBILES\Legendary) | 8 stock types replaced: 10% (Phoenix 15%) spawn roll gives a special hue, 1-3 slots, tame 120, extra training abilities, "Legendary" label (`FireSteed.cs:13-16`; `Nightmare.cs:216-232`) | P93 #4 specimen star rating (draft P97); evo pets | #489, #490 tamable packs | **The idea of a visible rarity tier** folds into P97: a 5-star roll could carry a hue, no file replacements |
   | Named pets and wave spawners (MOBILES\Named, COMMANDS\Spawners) | 16 new tamable mounts spawned by one 384-line wave-spawner item each (25 clones plus LunaInvasion): waves, lightning telegraph, boss, 1-hour cooldown, proximity trigger (`WaveSpawnBlackUnicorn.cs:38-71, :315-328`); 5 need custom bodies | Stock JSON spawners, champion spawns, Rootdeep and Despise seeders, P211's SVDungeon population stage | #442 Better-Dungeon Boss, #449 Interactive Boss, #491 Dynamic Invasion | **The shape** (one data-driven wave item with telegraph and cooldown) for League dives, not 25 clones. Bug to avoid: `bc.Tamable = false` on every spawn, boss included (`:306`), against its own header (`:9`) |
   | Free skills (CHANGED, Free Skills) | 19 skills outside the 720 total (`Skills.cs:660-682`): excluded from `Skills.Total` (`:305, :1016, :1081`), no cap check in `SkillCheck.Gain` (`:440-445`), sent to the client as base 0 (`Packets.cs:2548, :2588`); a `Server` assembly change | F-12 decided **total skill cap unlimited** and per-skill cap = level cap, skills by use only | #462 Free Skill System | **Skip.** Redundant once the total cap is gone, against F-12's ruling meanwhile, and the hidden-zero packet trick is bad UX |
   | Townhouses (COMMANDS\Townhouses, Voxpire) | A sign item defines a rectangle `TownHouseRegion : Region` (`TownHouseController.cs:158`) with `OnMoveInto` ban and private checks (`:180-209`) and secured-item gating in `OnDoubleClick` (`:214-233`); owner, co-owners, friends, bans, 1,500 lockdowns, purchase from the bank (default 250,000), sale, transfer, evict, 3 per account; 4 patched deed files | F-44 inn room (a tiny instanced first home), F-49 guild halls, pinned houses | none queued | **The region shape for F-44**: a staff-placed sign that sells a room inside a seeded inn, lockdowns by `Movable`, no multi. Both virtuals exist in pinned (`Region.cs:748, :865`). Rebuild, M |
   | Invasions (COMMANDS\Invasion System) | Identical to P93 #10 | F-30 Events tab design, Blackthorn `InvasionSpawner` in the Port tier | #491 | P93 ruling: idea only |
   | Virtual storage (ITEMS\Virtual Storage) | Identical to P93 #6; withdraw still checks only a 25-tile range (`VirtualStorageGump.cs:25, :167, :207`) | F-19 banks, satchels | #83, #84 | P93 ruling: idea only, native rebuild with access checks if wanted at all |
   | Treasures of Events items (ITEMS) | 118 classes for seven 2023-25 EA event reward sets (Ice Dragon, Fey Wrath, Hythloth, Archlich, Feudal Lands, Undead Lords, Wildfire): none exist in pub57 or pinned; `BasePeerless.cs` is patched to drop them at 5% and 1% (`:137-140, :305-368`) | F-40 loot boxes, F-47 requisitions want reward pools | #447 Treasures of Events (the framework) | **Ask Chase** (question 5): a GPL reward pool versus waiting for #447 |
   | Pet items (ITEMS) | PetLeash with its own shrink system, pet dye tub, 28 cub dyes, powder of temperament replaced | `customizations\ShrunkPet.cs` (a shrink exists), evo hue pick at stage 1 | #434 hitching post | Nothing new |
   | QoL commands and items | Corpse retrieval stone and death gump (hard-coded Trammel spot, `DeathTeleportGump.cs:34`), global chat, emotes with sounds, MyStats, Wallet, MyHouses, password changer (**echoes passwords to the journal**, `PasswordChanger.cs:100, :108`), unique names, runebook and spellbook straps, runic atlas with 1,000 charges and reordering, moongate entries, training dummies to 120, instant logout (`PlayerMobile.cs:6157-6160`), doubled summons, 120-skill mercenaries, store catalogue with stat-cap scrolls for sovereigns (`UltimaStore.cs:99-104`) | ClusterFSelfResurrect, ClusterFAnkhs, Healer policy, Staff Hub, Clean Up Britannia (P33), our own skill-gain and cap engines | #438 MyStats, #451 transmogger | Only what P93 already took (runebook reordering, access-checked). The rest are shard-specific balance choices against fidelity (instant logout, dummies to 120, free stat caps) |
   | Bosses (MOBILES) | Garthok and Xorvintaal champions on custom bodies with top-3 looter rewards, Manticore, OrcBruteBoss, Murderer NPC, OrcHound and statue | League dives, Rootdeep bosses | #442, #449, #504 | The "top-3 looters get the reward" credit is `DamageStore`/`GetLootingRights`, already in pinned; nothing to take |

3. **ModernUO fit.** The largest ServUO-only dependency is the Pet Training API (`PetTrainingHelper`,
   `TrainingDefinition`, `MagicalAbility`, `SpecialAbility`: 37 mobile files and the pet gump), which pinned lacks
   and the shard has as its own port, so any pet piece is rewritten against ours. `Persistence.Serialize`
   (invasions), `EventSink` Login, PlayerDeath, WorldSave and WorldLoad, `Account` gold and sovereigns, and the
   `Server` assembly edits for free skills are the other gaps. **Name collisions against pinned** (the subagent's
   list, names I could reconcile): `BaseAddonDeed`, `PowderOfTemperament`, `DragonBardingDeed`, `SwampDragon`,
   `FireSteed`, `Kirin`, `Nightmare`, `Phoenix`, `PolarBear`, `ShadowWyrm`, `TsukiWolf` (11 replacement files),
   plus `AnimalLore` from the pet gump, and nested `ShrinkTable` (twice), `InternalBuyInfo`/`InternalSellInfo`,
   `ResurrectEntry`. Everything else is new by name.
4. **Effort.** Per idea: slayer block S inside P96; rarity tier S inside P97; wave item M; townhouse region M;
   nothing else costed.
5. **Risks.** **GPL-3.0 copyleft** on the whole collection (P93's caveat; fine in the private repo, constrains a
   public release of the server code). Correctness bugs seen: `PowerScrollPicker` writes a `double` and reads an
   `int` (`:515`, `:521`: a corrupted save), the spawner `Tamable = false` above, `Mannequin.cs:216` tests
   `IsOwner(Owner)`, the password echo, the virtual-storage withdraw hole. Tight coupling: the store sells nearly
   every custom item, `BasePeerless` drops the event items, the pet gump and store need the leash's shrink code,
   the deed patches need the townhouse region, the spawners need the named mobiles: taking one piece means taking
   its dependents or rewriting around them.
6. **Recommendation: reference only, idea by idea** (table above). No file from it enters the repos; the four
   ideas worth a line are the pet gump's slayer block (into P96), a rarity tier (into P97), the wave-spawner shape
   (for League dives, beside P211), and the townhouse region shape (for F-44). Free skills: skip. Credit Feng and
   the original authors on any idea that lands.

## Proposed order of work

The port list comes first; these are after it or beside it. The first row is staff and test-shard tooling, so it
can run whenever a builder slot is free. Nothing here is a port.

| Order | Work | Effort | Waits on |
|---|---|---|---|
| 1 | Citizens for the overnight soak plus a walkability audit (player bot ideas) | S-M | nothing (test shard only; closes P91's memory question) |
| 2 | Rangers' League taming orders on the P123 BOD plumbing (taming BOD idea) | S-M | F-18's tailoring batch (same item rule), the Rangers' guildmaster giver |
| 3 | Pet gump slayer block and a rarity tier | S each | P96 and P97 (P93's drafts), when Chase says go |
| 4 | A flying mount on pinned's `Flying` flag (one Movement patch) | S-M | a flying mount existing (F-35 bird stage 5 or the red dragon .vd, P139-D6) |
| 5 | F-44 inn room as a townhouse-style region | M | Chase's answer to question 6 |

Not ranked: the chest (0 work: place a `MarkContainer`), the saber (skip), free skills (skip), the wave-spawner
shape (fold into P211's population stage or the League dive design when it is written).

## Draft prompts (not saved to the queue until Chase says go)

Numbers are proposals: the highest prompt on disk is P222, so these are P223 and P224; the overseer renumbers.
Both are "borrow" verdicts offered as prompts because each is small and sits on work already in the repo.

### Draft P223: citizens for the overnight soak, and a walkability audit

- **Goal.** The P102 nightly soak runs with dozens of headless citizens instead of three wire clients, and a staff
  command audits that every seeded area is walkable, so stuck spots and the P91 memory rise get real evidence.
  Credit bpace's ServUO PlayerBot for the approach (MIT; keep the notice with any copied lines).
- **Kind.** Builder in `D:\ShatteredLegacy`; staff and test-shard only; no player-facing change; Staff line in
  CHANGELOG. **Touches:** `server\customizations` (one new file), `tools\playtest-bot` (soak and report), tests.
- **Read first.** `D:\UO\third-party\code\servuo-playerbot\servuo-playerbot-main\Scripts\Custom\PlayerBots\PlayerBot.cs:226-234`
  (the `Player = false` headless actor), `PlayerBotService.cs:626-661` (the tick), `PlayerBotWorldData.cs:632-696,
  :709-781` (the audits), `PlayerBotStuckTelemetry.cs` (design references; rewrite, do not copy); pinned
  `Server\Mobiles\Mobile.cs:6510-6515`, `UOContent\Engines\Pathing\Movement.cs`, `MovementPath.cs:12`;
  `customizations\TestCenter\` and P73's `SL_SHARD_ROLE=test` gate; `tools\playtest-bot\uobot\soak.py`,
  `notes\cc-P91-overnight-playtest-bot.md` (The soak).
- **Steps.** (1) `[Citizens <n> [walk|fight]`, Administrator, refused unless `SL_SHARD_ROLE=test`: spawns n
  `PlayerMobile` actors with `Player = false`, no account, looping between seeder coordinates (New Haven square,
  the Registrar, the mine camp, the Rootdeep entrance) with pinned's `MovementPath`; fighters attack spawned
  mongbats as P91's soak did. One timer for all citizens, no per-tick world scans. `[Citizens remove` deletes them
  all; a world load deletes any left over. (2) `[AuditWalk`, Administrator: for each seeded structure, path between
  its doors and anchors with `MovementPath`, report unreachable pairs and the first blocked tile to a file under
  the run folder. (3) The soak calls both through the admin client and reports steps, failures per citizen, saves
  and memory as today. (4) Nothing touches `sl-modernuo` or `sl-modernuo-test` (Rule 1 unchanged).
- **Test plan.** Tests: the command is refused when the role is not test; citizens are deleted on world load; a
  citizen never blocks a real player's account (no account, no NetState); the audit reports a deliberately walled
  fixture as unreachable. Watch each fail first. A two-hour soak with 50 citizens on the scratch shard, memory
  curve in the report.

### Draft P224: Rangers' League taming orders

- **Goal.** A taming order type on the shard's BOD engine, handed out by the Rangers' guildmaster: tame N of a
  species from your gain window, hand them to the Rangers' pen, earn Rangers' Seals and points. Credit
  ScriptVisitor and RoninGT for the loop.
- **Kind.** Builder; player-facing customization (log it in `docs\fidelity-principle.md` through Claude; a wiki
  entry). **Touches:** `server\customizations\Services\BulkOrders` (two deed files, a giver line), `server\patches`
  (one new `BODType` value in `BODType-all-crafts.patch` and the book patch), tests. **Runs after** F-18's tailoring
  batch so the item rule is shared.
- **Read first.** `D:\UO\third-party\code\fs-ats-taming-bods\...\SmallTamingBOD.cs:155-205` (the hand-over guards)
  and `TamingRewardFormula.cs` (design reference only); `customizations\Services\BulkOrders\CraftBOD.cs`,
  `BulkOrderGivers.cs:24-60`, `SmallCarpentryBOD.cs` (the pattern), `ClusterFRangersSystem.cs`; pinned
  `UOContent\Skills\AnimalTaming.cs:426-428` (who tamed it); `docs\feature-queue.md` F-18, F-20, F-25, F-35 and
  F-12's pet-cap gap; P93 #4 (the rating).
- **Steps.** (1) `BODType.Taming` appended; `SmallTamingBOD` and `LargeTamingBOD` on pinned's bases as P123 did.
  (2) Species picked from a per-type table of `MinTameSkill` and `ControlSlots` built once from the creature types
  (never by spawning one), inside the player's gain window; under 50 skill, farm animals only, 10 per deed. (3)
  Hand-over by target: own controlled pet, tamed by this character, not bonded, not summoned, not polymorphed; the
  creature is removed and counted. One large and three small deeds held at a time, a daily per-account turn-in cap.
  (4) Rewards in Rangers' Seals and points through the P122 reward gump; no gold table; no pet cap scroll until F-12
  rules on pet caps. (5) Leave a hook for a star-rating requirement (P97).
- **Test plan.** Tests: a 30-skill tamer never gets a species above their window; a bonded pet is refused; another
  player's pet is refused; the daily cap refuses the extra deed; no creature is constructed by the reward
  calculator. Watch each fail first. Play test: one small and one large order end to end on the test shard.

## Open questions for Chase

1. **Go on the drafts?** P223 (soak citizens and audit) and P224 (taming orders), either, both, or neither.
2. **GPL stance for Feng's code,** still open from P93 question 5 and now covering the whole Wildlands collection:
   ideas only (this note's assumption), or may the P96 dashboard carry his GPL file with its slayer block?
3. **A flying mount at all?** If the red dragon (P139-D6, the 5.7 MB `.vd`) or the hiryu stage should fly, the
   proposal is pinned's `Flying` flag plus one Movement patch (cross water), never Wilson's altitude. Yes or no
   decides whether row 4 above exists.
4. **Pet caps under F-12:** does "per-skill cap = level cap" apply to pets? It decides whether any pet power scroll
   (ScriptVisitor's reward, ServUO's own stock item too) can be a reward on this shard.
5. **Treasures of Events items:** 118 EA event reward classes exist only in Feng's GPL collection. Wanted as a
   reward pool for F-40 loot boxes and F-47 requisitions (then a rebuild from the item stats, not the files), or
   wait for the queued #447 framework download and decide then?
6. **F-44 inn room shape:** an instanced room (the entry as written) or a townhouse-style region sold by a sign in a
   seeded inn (Feng's and Voxpire's shape, which needs no house multi and keeps the room in the world)?
7. **Rangers' pen fiction:** when a taming order is handed in, is the animal released (deleted) or does the shard
   want a visible pen that fills up? The second is decor plus a cap, a day more.

## Corrections to the download records (for the scout and the overseer)

- `code\flying-system\SOURCE.txt` says "~40 flying mobiles": 41 creature classes in 40 files (`FlyingBird.cs` holds
  two), 29 of them stock types with "Flying" prefixed. The rug is a bedroll ID and the device is a `BaseShield`.
- `code\rune-marking-chest`: the item is a metal chest (0x9AB), not a mailbox, and pinned already ships
  `MarkContainer`, so the intake's "small port" is zero work.
- `code\fs-ats-taming-bods`: the intake row's "2 core BOD patches" are 2 diff files; `patch.diff` touches 22 files
  in 52 hunks, including core `Server\Gumps\Gump.cs` and `GumpTooltip.cs`. ScriptVisitor Utils v1.0.2 is required
  and not on disk.
- `code\double-lightsaber\SOURCE.txt` says the art "appears to come from Erad's set": it does not. Erad's pack on
  disk has paperdoll gumps only (a double-bladed staff and nine sabers), no item art, and 0xC4E0 is empty in the
  client. The art was never downloaded.
- `code\servuo-playerbot\SOURCE.txt`: `Import-UOOfflineRoutes.ps1` is documented nowhere in the package; the
  dashboard defaults to `127.0.0.1:8081` and its config file is rewritten at every server start.
- `code\uo-wildlands-scripts\SOURCE.txt` should say that Custom Pet Gump, Invasion System and Virtual Storage are
  the same code as `animal-lore-gump`, `invasions-feng` and `virtual-storage` (one 55-line addition), that
  `bodyTable.cfg` is byte-identical to stock pub57's, and that the six companion dog bodies are the ones F-35
  already chose (1546-1552).

P212 DONE
