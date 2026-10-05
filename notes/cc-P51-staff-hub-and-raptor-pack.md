# cc-P51: Staff Hub first build (F-30) and Raptor pack friends (F-31)

2026-10-04. Brief: `D:\UO\cc-prompts\cc-P51-staff-hub-and-raptor-pack.md`. Engine: `D:\UO\ModernUO-pinned` at
`d4531cd94b739613155225c234900de9f47d2c88` (`rev-parse HEAD` today). Shard HEAD `aa61227` (the brief read `8825eb8`;
P48 and two shard-work commits landed since). "C\" = `D:\ShatteredLegacy\server\customizations\`, "T\" =
`D:\ShatteredLegacy\server\tests\`, "P\" = `D:\UO\ModernUO-pinned\Projects\`. Scratch: `D:\UO\cc-p51-work\`.

## Headlines

1. **All five parts done, all green.** Final build (build 6) through `docker\uo\build.sh -t sl-modernuo:cc-p51`:
   **42/42 patches** (41 before plus `Raptor-pack-friends.patch`), **637/637 shard facts** (606 before plus 31 new:
   14 Raptor cases, 17 Staff Hub facts), image `sl-modernuo:cc-p51` = **`aead9f7f5e2e`**. `sl-modernuo:latest` not moved
   (`91811524c58e` before and after; it was rebuilt about 15 minutes before I started and is the same image as
   `cc-p48`). Nothing deployed, no shard touched, nothing committed. ASCII only.
2. **Every new fact watched red first.** Three scratch trees made from the final one (`D:\UO\cc-p51-work\make-red.py`,
   `make-red-b.py`, `make-red-c.py`, each built with its own `build.sh --tests-only`): **red-a** (no Raptor patch and every
   hub behaviour undone or stubbed) fails **26 of 637**: all 17 hub facts and 9 of the 14 Raptor cases. The other 5 Raptor
   cases assert an absence (a tamed raptor calls none; no drop at 0.25, at 0.9, or for a bonded pet; no change to
   Raptor's save shape), so they hold when Part A is simply missing. **red-c** breaks exactly those rules on top of the
   working patch and fails **5 of 637**, those five. Together: all 31. Table below.
3. **Raptor route (b), thinner than sketched.** The patch only adds hooks (an `OnCombatantChange` that calls base then
   `ClusterFRaptorPack`, and ServUO's pottery roll). Friends are `RaptorPackFriend : Raptor` in customizations, which
   deletes itself after load. Upstream's Raptor keeps version 0 and no field: no migration. A pure customization hook
   is impossible (argued below). Two ServUO "broken" bugs fixed under D-4: the pruning loop that could call a third
   friend, and the missing `base.OnCombatantChange()` (no war mode).
4. **Found, copied faithfully, worth knowing: a tamed raptor that is not bonded still rolls the drops.** ServUO, upstream
   and the patch all read `!Controlled` after `base.OnDeath`. By then pinned has deleted the creature
   (`P\Server\Mobiles\Mobile.cs:4899-4902`) and `BaseCreature.OnDelete` has released it (`BaseCreature.cs:3687-3688`).
   Upstream's own 0.5% claw roll has the same property. Only a bonded pet (early return, `:3482-3540`) keeps the flag
   and drops nothing. Not fixed: it makes nothing missing, and fixing it would make our pottery roll disagree with
   upstream's claw roll a line below it. The fact states the real behaviour. ServUO's to copy; possibly ModernUO's to
   report (the claw's `!Controlled` is dead code for unbonded pets). Unverified for ServUO's runtime (read only).
5. **The brief's "Woods discovered n of 6" is 8.** The code gates 8 extended woods (Ironwood to Starwood), the same as the
   8 extended ores; 6 is the vanilla coloured woods, which have no gate. Built as 8 from `CraftResource`; Part C has the
   lists. Grants recounted: **9**, as the brief says.
6. **League rank shows the real rank** (P48 landed, `aa61227`), for example "Shadow Iron Citizen" in the fixture.
7. **The hub reads commands by reflection and covers all of them.** The test host runs only a few `Configure`s, so the
   listing fact registers every `[ShardCommand]` handler in UOContent under a synthetic name for its duration: **68
   handlers** (9 Player, 1 `[SL`), so **58** listed outside Player, plus the fact's 4 probe commands: 62 = 62.
   `CommandDeclarationVerification`: 68 registrations in the IL, 68 `CommandSystem.Register(` lines (67 before, plus `[SL`).
8. **No clash with P48 or P34**: no account data, no seeder placement. The six seeders gained read-only members only, and
   their layout facts stayed green. Unrelated: `D:\UO\shard-migration` has uncommitted cc-P49 notes
   (`notes\cc-P49-dungeon-chests-research.md`, `notes\cc-P49-scratch\`) that are not mine; left alone.

## What changed

Shard (`D:\ShatteredLegacy`), uncommitted:

- `server\patches\Raptor-pack-friends.patch` (new, 38 lines): upstream `Raptor.cs`; removes the TODO (`:41-43`), adds
  `OnCombatantChange` and the pottery roll. Named in `docker\uo\apply-patches.sh:417-423` with its argument.
- `C\Mobiles\Normal\ClusterFRaptorPack.cs` (new): the timer, the friend list, `CheckFriends`.
  `C\Mobiles\Normal\RaptorPackFriend.cs` (new): the friend, `[SerializationGenerator(0, false)]`, not tamable, deletes
  itself after deserialization.
- `C\StaffHub\ClusterFStaffHub.cs` (new): `[SL` (`:38-45`), the catalog (`AllCommands :150`, `CanRun :191`, `Run :230`,
  `DryRun :247`, `RunGrant :267`), the Player panel (`FindCharacters :310`, `ExtendedOres :349`, `PlayerRows :369`,
  `GoToPlayer :421`, `BringPlayer :434`), Travel (`ShardPlaces :475`, `GuildHalls :487`, `GoTo :499`,
  `TryParseGoTo :540`).
- `C\StaffHub\ClusterFStaffHubSpots.cs` (new): saved spots and Recent (`GenericPersistence` `:39`; `SaveHere :59`,
  `Delete :104`, `AddRecent :126`, `WriteTo :152`, `ReadFrom :172`).
- `C\StaffHub\StaffHubGump.cs` (new): the gump (`Respond :539`, `BeginRun :737`), `StaffHubPromptGump :781`,
  `StaffHubConfirmGump :867`.
- Anchors, read-only: `C\ClusterFNewHavenSeeder.cs:74-96`, `C\ClusterFMineCampSeeder.cs:40-58`,
  `C\ClusterFRegistrarOfficeSeeder.cs:48-53`, `C\ClusterFGuildHallSeeder.cs:33-37`,
  `C\ClusterFFountainOfFortuneSeeder.cs:25-26`, `C\ClusterFRoyalCitySeeder.cs:41-43` (`MoongateLocation` private to
  public).
- Facts: `T\Mobiles\Normal\RaptorPackFriendsVerification.cs`, `T\Misc\StaffHubVerification.cs` (new).

This repo: this note; `README.md`, `dashboard.html`, `tools\progress.json` from `tools\progress.py`.

## Facts, red then green

Red = the scratch build that showed it failing; green = build 6 (and builds 4 and 5).

| Fact | Red in | Green |
|---|---|---|
| A1 a wild raptor gets two friends within one tile, on its combatant (and tops back up to two) | red-a | yes |
| A2 friends are not tamable and call none of their own | red-a | yes |
| A3 a tamed raptor calls none | red-c (both Controlled guards removed) | yes |
| A4 friends deleted when the caller dies / loses its combatant / leaves the map (3 cases) | red-a | yes |
| A5 friends do not survive a save and load; the caller does | red-a | yes |
| A6 a raptor saved before this change loads (version 0, no declared field, a round trip reads all it wrote) | red-c (a partial Raptor declaring `_isFriend`) | yes |
| A7 the drop: 0.0 and 0.2499 wild drop; tamed (unbonded) drops | red-a | yes |
| A7 the drop: 0.25 and 0.9 wild, and bonded, do not | red-c (the roll made unconditional) | yes |
| B1 every `[ShardCommand]` command outside Player listed under its category; undeclared and stock ones not | red-a | yes |
| B2 a TestOnly row cannot run on live (no Run button, refused), can on test | red-a | yes |
| B3 WorldRemoval hidden and refused below Administrator | red-a | yes |
| B4 Run on a confirm row does nothing until confirmed (prompt, confirm, No, Yes) | red-a | yes |
| B5 Dry run passes exactly the declared word | red-a | yes |
| B6 a Counselor gets no gump, a GameMaster does | red-a | yes |
| B7 arguments open the prompt prefilled; an unedited template is refused | red-a | yes |
| C1 the panel's nine values for the fixture character; reading creates no record | red-a | yes |
| C2 search finds an offline character; several list for picking | red-a | yes |
| C3 a Grant applies to the selected character (real `CompactGivePickaxe`); offline falls back to the cursor | red-a | yes |
| C4 offline Go and Bring: no button, refused | red-a | yes |
| D1 every place equals its seeder's member, each anchor is the seeder's own data, Go lands there | red-a | yes |
| D2 a saved spot survives a save and load, delete removes it, another account does not see it, a bad version throws | red-a | yes |
| D3 Go to refuses a bad facet, bad numbers, off-map and bad z cleanly; moves on good input | red-a | yes |
| D4 Recent caps at 5, newest first | red-a | yes |
| E1 no button ID shared between tabs or repeated in a gump | red-a (Travel's places moved onto the Run range) | yes |
| E2 a stale gump fails safely (command removed, character logged out, deleted, out-of-range button) | red-a | yes |

Two facts were wrong on the first green attempt (build 2), and the facts were changed, not the code: the tamed cases set
`Controlled` directly (now `SetControlMaster`, what taming does), and the save-load fact read `Deleted` before
`[AfterDeserialization(false)]` had run (it runs on the next timer tick, so the fact advances the clock). Build 3 then
showed the unbonded-pet drop of headline 4.

## For Chase: in game on the test shard

Deploy: `docker tag sl-modernuo:cc-p51 sl-modernuo:latest`, then `D:\ShatteredLegacy\docker\uo\Start-TestShard.ps1 -Down`,
then `D:\ShatteredLegacy\docker\uo\Start-TestShard.ps1 -SkipBuild`.

1. `[SL` as a GameMaster: the hub opens with **TEST** top right. Commands, Player and Travel switch; Events is grey.
2. Commands: click each category gem. World removal: as GM it says it needs Administrator; as Admin the rows are red.
   Pick a world setup command with a Dry run and press it: the command's own dry-run lines appear and nothing changes.
   Press Run on a removal row: a prompt, then yes or no; say No.
3. Player: search a second character by name (try one that is logged out). Check the nine rows against what you know.
   Press a Grant (CompactGivePickaxe) with the second character online beside you: the pickaxe lands in their pack,
   not yours. Log them out: Go and Bring turn grey.
4. Travel: Go to each shard place (bank, mine camp, Registrar office, each guild hall, Fountain of Fortune, Royal City).
   Save here with a name, relog (and if you like restart the shard): the spot is still there; delete it.
   Go to `1500 1610` with facet `felucca`, then with facet `narnia` (one line, no move). Recent shows the last five.
5. Raptor: find a wild raptor and attack it: two more raptors arrive within a tile and attack you. Kill the first, and
   within 30 seconds the other two vanish. Try to tame a friend: it is not tamable.
6. Live, later: `[SL` shows **LIVE** in green and `[GuildStanding` (test only) is grey with no Run button.


## Part A, written before the patch: the Raptor route

### What the three sources say

- Upstream `P\UOContent\Mobiles\Monsters\Reptile\Raptor.cs` (76 lines, `[SerializationGenerator(0)]`): the TODO at
  `:41-43` names both omissions (pack friends, the 25% `AncientPotteryFragments` drop).
- ServUO `D:\UO\ServUO-pub57\Scripts\Mobiles\Normal\Raptor.cs` (235 lines): `OnCombatantChange :109-116`, `CheckFriends
  :118-172`, the drop `:178-181`, friends deleted in `Deserialize :215-216`, `InternalTimer :219-233` (first tick at
  once, then every 30 s). Friends are `new Raptor(true)`, `Tamable = !isFriend` (`:54`), placed at X and Y each +-1
  (`Utility.Random(3) - 1`, `:153-154`).
- Ours before the upgrade, `notes\reference\Raptor-ours-pre-upgrade-045b313.cs` (191 lines): the same behaviour
  statement for statement, with two differences from ServUO:
  1. **The pruning loop.** ServUO walks `m_Friends` forward and calls `Remove` inside it (`:132-142`). Removing at i
     shifts the next friend into slot i and the loop then skips it, so a living friend after a dead one is not counted
     and a third friend is spawned (more than `MaxFriends`). Ours walks backward with `RemoveAt` (`:103-115`). That is
     a "broken" bug in D-4 terms (it makes something wrong, not something missing), so **ours is kept**: friends never
     exceed 2.
  2. Neither calls `base.OnCombatantChange()`. Pinned's `BaseCreature.OnCombatantChange` (`P\UOContent\Mobiles\
     BaseCreature.cs:3035-3045`) sets `Warmode` from the combatant and lands a flier. Skipping it would leave a raptor
     out of war mode in a fight, again broken rather than missing, so **the override calls base first**.
- ServUO's v1 branch re-adds `SetWeaponAbility(BleedAttack)` (`:212-213`): upstream already has
  `GetWeaponAbility() => BleedAttack` (`:55`), nothing to port.

### Can a customization reach it without a patch? No.

`OnCombatantChange` is a virtual on `Mobile` (`P\Server\Mobiles\Mobile.cs:3772`), called from the `Combatant` setter
(`:771`). The setter raises no `EventSink` event; its only other hook is `Region.OnCombatantChange(m, old, new)`
(`P\Server\Regions\Region.cs:790`), which would need every region a raptor can stand in to be ours. The remaining
customization-only shape is a world timer that polls every `Raptor` for a combatant: it would call friends seconds
late instead of on the change, cost a scan of every mobile, and still need `OnDeath` for the drop. Rejected. So the
hooks have to be on `Raptor` itself, which means a patch to upstream's file.

### (a) or (b)

- **(a) one patch carrying everything, `_isFriend` serialized.** Raptor goes 0 to 1, a migration JSON, and a v0
  reader for the raptors already on the test shard. It changes upstream's save shape, so every future upstream change
  to `Raptor.cs` has to be merged against our version number as well as our lines.
- **(b) friends are a subclass, `RaptorPackFriend : Raptor`, in customizations; upstream keeps version 0.** The
  friend is not tamable and deletes itself after deserialization (ServUO's rule), so it needs no flag on `Raptor`:
  being the subclass is the flag. A pre-change raptor's bytes are exactly what the post-change `Raptor` reads, because
  nothing about its serialization changed. No migration.

**Chosen: (b), and thinner than the brief sketches.** The patch adds only the hooks: `OnCombatantChange` calls base
then `ClusterFRaptorPack.OnCombatantChange(this)`, and `OnDeath` gains ServUO's pottery roll beside upstream's claw
roll. The timer, the friend list and `CheckFriends` live in `C\Mobiles\Normal\ClusterFRaptorPack.cs`, the same split
as the Young patches (pinned calls into `ClusterFYoungPlayer`). Reasons: the patch is about ten lines and only touches
lines near the TODO, so upstream drift in the rest of the file still applies at fuzz 0; the behaviour is in a file we
own and can test directly; and the friend list needs no field on `Raptor` (a dictionary keyed by the caller, emptied
when its pack ends). Not an option, and not done: our old class back as a hidden replacement (F-31; P30 `:310`).

The drop stays inline in the patch rather than in the helper, in ServUO's order (pottery roll, then claw roll), so the
patched `OnDeath` reads like ServUO's.

## Part B: the Staff Hub shell and the Commands tab

Files: `C\StaffHub\ClusterFStaffHub.cs` (what the hub shows and does), `C\StaffHub\StaffHubGump.cs` (the gump, the
argument prompt and the confirm), `C\StaffHub\ClusterFStaffHubSpots.cs` (Part D's persistence). The logic is out of the
gump so the facts call it directly; the gump's `Respond(...)` takes the text entries already read, so a fact presses a
button without building a client packet.

- **`SL` was free.** No `Register("SL"` or `[Aliases]` naming it in pinned `Projects\` or `C\` (grep, case
  ignored). `CommandSystem.Entries` is case-insensitive (`P\Server\Commands.cs:156`).
- **`[SL` is `[ShardCommand(CommandCategory.DevTool, Shard = CommandShard.Any, Summary = ...)]`**, GameMaster. The hub
  **does not list itself** (opening the hub from the hub does nothing useful).
- **Reading the commands.** `ClusterFStaffHub.AllCommands()` walks `CommandSystem.Entries`, keeps entries whose
  `Handler.Method` has `[ShardCommand]` with a category other than Player, folds a name that is one of its handler's
  `[Aliases]`, and reads `[Usage]` and `[Description]` from the same method. Nothing is hard-coded, so a new command
  appears with no upkeep.
- **Running one** is `CommandSystem.Handle(from, Prefix + name + " " + args)`, the path typed text takes
  (`Commands.cs:257-320`): pinned's access check, the command's own messages, `EventSink.InvokeCommand`. Before that the
  hub refuses three things itself: a command no longer registered (stale gump), WorldRemoval below Administrator, and
  TestOnly when `TestCenter.Enabled` is false.
- **Access.** `[SL` is GameMaster. A row is shown when the staff member has the command's own access, and for
  WorldRemoval also Administrator; below Administrator the World removal category says "World removal needs
  Administrator." A TestOnly row on live is drawn grey with "Test shard only" and no Run button.
- **Confirm rows**: `Rerun` Duplicates or DeletesAgain, or category WorldRemoval: the name is red and Run asks yes or no.
  A dry run never asks (it changes nothing).
- **Arguments**: a command whose `[Usage]` shows anything after its name opens the text entry, prefilled with that part
  (for example `<guildKey> [amount]`), with the whole usage above it. Submitting the unedited template is refused with
  one line (clear it to run with none). A command with arguments that also needs a confirm goes prompt, then confirm.
  **Targets are not read from `[Usage]`**: no usage in `C\` spells a target, so a targeting command simply opens its
  cursor when it runs, as typed.
- **Paging**: 4 rows per page (row height 72 inside the 324 high content area), "Page n of m" with 4014/4005 arrows.
- **Hues** (said in the gump's header): gold 0x386 (`C\ClusterFStatInspect.cs:40`, "gold - section headers"), white
  1153, grey 0x3B2 (`C\ForestersGuildmasterGump.cs:321`, "grey"), red 0x20 (`ClusterFStatInspect.cs:44`), green 0x44
  (`C\DevTestingCrystal.cs:33`, "Bright green"). Command names are bold HTML: #FFFFFF, red #FF5A5A, grey #9A9A9A.
- **Deviation from the mockup, small:** the Player tab's actions and grants are 4005 arrows and 0x15E1 small arrows with
  labels rather than 2445 text buttons. "Bring player here" is wider than a 2445 button, and nine 23 px grant buttons do
  not fit the 162 px under the Grants heading. Chase can say if he wants them as stone buttons in two columns instead.

## Part C: Player tab

- **Selecting**: Target (a cursor), or a name: `FindCharacters` searches every `PlayerMobile` in `World.Mobiles`
  (offline characters stay there, on Map.Internal), exact matches first, then names containing it, up to 8. One match
  selects it; several list for picking.
- **Read only.** Every value goes through the read accessors: `ClusterFAccountPersistence.Get` and `GetGuild`, never
  `GetOrCreate`, so looking at a character creates no record (a fact checks that). No field, no version.
- **Rows**: guild standing (highest `GuildRankIndex`, then standing; "and n more"), League rank (P48 has landed:
  `ClusterFLeagueRanks.RankName(GetRank(m))`, so not "not built yet"), Renown (and lifetime), Compact rank (the
  guild system's mining ladder name and the standing), Restoration unlocks (count and keys), ores and woods discovered,
  skill and stat caps (`Skills.Total`/`Skills.Cap`, `RawStatTotal`/`StatCap`, `ClusterFStatCaps.IndividualStatCap`),
  bank items (`BankBox.TotalItems` of `ClusterFBankLimit.GetMaxItems`; "no bank yet" without creating one).
- **"Ores n of 8": 8 is right; "woods n of 6" is not, it is 8.** Counted from the code: the logbook gates exactly the
  post-Valorite ores, `CompactOreSatchelRoutingHook.cs:55-65` `_extendedOreGateKeys` = Platinum, Toxic, Blaze, Frost,
  Obsidian, Mythril, Adamantium, Celestial (8), and the extended woods, `ForestersLogbookGump.cs:46-50` `ExtendedKeys` =
  Ironwood, Ghostwood, Emberbark, Frostbark, Shadowbark, Runewood, Voidwood, Starwood (8). Six is the count of vanilla
  coloured woods (`ForestersLogbookGump.cs:40`: Oak, Ash, Yew, Heartwood, Bloodwood, Frostwood), which have no gate. The
  hub derives both lists from `CraftResource` (Platinum..Celestial, Ironwood..Starwood, `C\ResourceInfo.cs:20-27,
  :50-57`), so they cannot drift from the enum; the vanilla ones (the logbook also records 8 vanilla ores and 6 vanilla
  woods) are not counted. If "of 6" meant the vanilla woods, Chase can say and it is one line.
- **Placeholder**: a dashed box at (26,330) 296 x 52, "Levels and Loops panel arrives with F-12." Nothing behind it.
- **Actions**: Go to player = stock `[Go <serial>` through `CommandSystem.Handle`, as pinned's `[Interface` does it
  (`P\UOContent\Commands\Generic\Commands\Interface.cs:560-565`); Bring = pinned's "Bring them here"
  (`Interface.cs:567-577`, which has no command of its own: the same two checks and `MoveToWorld`); Props = stock
  `[Props <serial>`. Offline: Go and Bring are drawn grey with no button, and refused if pressed from a stale gump.
- **Grants**: one row per visible command in category Grant (by reflection, as Part B). **Pre-aimed, cleanly, when the
  character is online on the staff member's facet**: the command runs as typed; every Grant command today opens a
  target cursor, and the hub answers it with the selected character through pinned's `Target.Invoke`
  (`P\Server\Targeting\Target.cs:146-214`), which makes every check a click would. It passes for staff because
  `InLOS` is always true above Player (`P\Server\Mobiles\Mobile.cs:3631-3634`) and the grants use range -1. **Falls
  back to the cursor** (with one line saying why) when the character is offline (`Target.Invoke` refuses another map,
  and an offline character is on Map.Internal, `Target.cs:180`) or on another facet. No grant command was changed.

## Part D: Travel tab

- **Every place comes from its seeder's code.** Added members (public static, derived, placing nothing):
  - `ClusterFNewHavenSeeder.Facet`, `SpotOf(Type)`, `BankAnchor` (Sarsmea Smythe, area "New Haven Bank", read from
    `Entries`) and `RegistrarAnchor` (the League Registrar's tile, inside the field office).
  - `ClusterFMineCampSeeder.Facet` and `Anchor`: the Miners' Compact Liaison's tent opening, `move.To` from
    `ClusterFMineCampLayout.Npcs`, the table its NPC move already uses.
  - `ClusterFRegistrarOfficeSeeder.Facet` and `Anchor`. The office's three addons have no standing point of their own,
    so the anchor is the Registrar's seeded tile (`ClusterFNewHavenSeeder.RegistrarAnchor`; walls x3453-3462, y2596-2603,
    she stands at 3459,2601,18). Said in the member's comment.
  - `ClusterFGuildHallSeeder.Anchors`: the Seeded `GuildLocations` its `Seed` walks, without the Thieves' Den lookout.
    The Guild halls row opens that list (the left column switches to it, with a back arrow).
  - `ClusterFFountainOfFortuneSeeder.Facet` (Location existed at `:23`), `ClusterFRoyalCitySeeder.MoongateLocation`
    made public (value and use unchanged) and `Facet`. The two `Facet` members restate the `Map.TerMur` each seeder
    places on; the placement code itself was not touched in any seeder.
  - Dungeon entrance: greyed "after P36". cc-P36 has not landed (no `DungeonRegion` subclass of ours, no P36 notes).
- **Go** is `MoveToWorld(location, map)`, what pinned's `[Go` menu does (`P\UOContent\Gumps\Go\GoGump.cs:162`); typed
  `[Go x y z` cannot change facet.
- **Saved spots**: per staff ACCOUNT (a second character on the same account sees them, another account does not), in
  their own `GenericPersistence` (`ClusterFStaffHubSpots`, file `StaffHubSpots/StaffHubSpots.bin`, priority 10),
  version 0, an unknown version throws `InvalidDataException` (the D40 rule). Not in `ClusterFAccountData`. A name is 1
  to 32 characters; the same name replaces; 100 per account. Delete checks the row still has the name the gump showed.
- **Recent is memory only**, per character, 5, newest first. A restart clears it, by choice: it is "where was I just
  now", and saved spots are the durable list.
- **Go to**: x, y, z (optional: the map's average Z), facet by name as `[Go` matches one (`Handlers.cs:456-470`),
  default the staff member's own. Bad input (not a number, off the map, z outside -128..127, unknown facet) gives one
  line and no move, never an exception.

## Part E: wiring

- `[SL` is declared (`DevTool`), so `CommandDeclarationVerification` counts one more registration and stays green.
- **Button IDs are one scheme** (constants at the top of `StaffHubGump`): chrome 0-3, Commands 10-21 and 1000+/2000+,
  Player 30-34 and 3000+/3500+, Travel 40-44 and 4000+ to 4400+. A response is routed by ID alone, so no two tabs may
  share one; a fact builds every tab and asserts it.
- **Stale gumps**: every row button indexes the gump's own snapshot, and every action re-checks live state: the command
  must still be registered with the same handler, the character must still exist (and be online for Go and Bring), a
  delete must still find the same name at that index. An index no gump drew does nothing.

## Part A after the build: what the facts showed

- The friends behave as ServUO's: called at once on the first tick, topped up every 30 s, never more than two (fact A1
  deletes one and checks it comes back), deleted on the next tick after the caller dies, loses its combatant or leaves
  the map.
- `[AfterDeserialization(false)]` defers the friend's delete to the next timer tick after a load. That is what our old
  port did (`Raptor-ours-pre-upgrade-045b313.cs:169`), and it keeps a delete out of the middle of a world load.
- The pet drop (headline 4).

## Build log

1. build 1: one compile error (a missing `using Server.Gumps;`). 42 patches applied.
2. build 2: 634/636; the two fact errors above.
3. build 3: 635/636; the unbonded-pet drop, fact restated.
4. build 4: 637/637, image built.
5. build 5: 637/637 after strengthening B1 (synthetic registration of every attributed handler).
6. build 6: 637/637 after the guild hall rows were named by guild (two guilds share the New Haven Magery School).
   **Final: `sl-modernuo:cc-p51` = `aead9f7f5e2e`.**
- red-a: 611/637 (26 fail). red-b: 633/637 (4 fail; A3 survived on ServUO's second guard in `CheckFriends`, hence
  red-c). red-c: 632/637 (5 fail). Builder tags `sl-uo-builder:cc-p51-red`, `-redb`, `-redc`; no runtime images.

## tools/progress.py

Ran at the end: "Overall: 27% of candidate content ported", Content 551/2045 (26.9%), Setup 7/7; "808 customization
files, 47 patch files, 485 tests in 95 files"; README, expansion coverage and dashboard refreshed. Its "47 patch files"
is everything in `server\patches\`: 42 `.patch` plus 5 `.cs` replacements.
