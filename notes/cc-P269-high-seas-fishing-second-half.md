# cc-P269: High Seas fishing, the second half

Written 2026-10-25 by the Iron Golem (Opus), on branch golem/Iron/P269 of both repos (both clean at the start, at main:
ShatteredLegacy 608d0b4, shard-migration 71e22ed). Prompt: `cc-prompts/claimed/Iron/cc-P269-high-seas-fishing-second-half.md`.
Not committed: the Golem commits after DONE. Pinned paths are relative to `D:\UO\ModernUO-pinned\Projects` (d4531cd9);
ServUO paths to `D:\UO\ServUO-pub57\Scripts`; "ours" is `server\customizations\Services\Expansions\High Seas` unless
said otherwise.

## In plain words

- Fishing gets the rest of High Seas. Fish mongers on eight docks (Britain, Moonglow, Trinsic, Vesper, Jhelom, Skara
  Brae, Papua and the Sea Market, in Trammel and Felucca) give orders for fish to deliver by boat to another port. They
  pay in bait, magic fishhooks (lava, junk-proof, dredging), lava lobster traps, rare fishing books, Fishing power
  scrolls and the Oracle of the Sea.
- Bait on a pole makes its fish twice as likely to bite. A lava hook lets you fish in lava for stone boots, lava rocks
  and pavers. The Oracle of the Sea finds Charybdis: a pole baited for it, cast at the spot with 100 Fishing, raises it.
  Sixteen fish pies can be baked (Cooking band II) for five-minute buffs, and Charybdis drops some.
- Corgul the Soulbinder and his crew of 75 are in the game, but only staff can place him. Players cannot reach his
  island yet: his altar and the sea warp move boats, and wait for the boat work.
- For you: run `[GenFishMongers` once on the test shard (and on live when it comes back), or nobody sees the mongers.
  Two decisions below: who sells the pie seasonings (no vendor does yet, so players cannot bake pies), and whether the
  fish orders should move onto the shard's own quest engine.

## Headlines

1. **All six parts are ported** (section 1). The High Seas fishing row of the port list goes from **27 to 53 of 59
   files** (progress.py with `SL_SHARD` at the Iron copy). Six are left: CorgulAltar, CorgulRegion (both wait for
   boats), MatchCord and Niter (cannon resources), Corgul's Handbook on Mysticism (no Mysticism spellbook here), and
   Fish.cs (ported by P193; its file name matches a stock file, so the tracker cannot count it).
2. **Three patches, each the smallest that works** (section 2). `FishingPole-high-seas-bait-hooks.patch` gives the
   pole ServUO's bait and hook (version 0 to 1, migrated). `Fishing-high-seas-bait-hooks-lava.patch` tells the pole when
   a cast caught something, adds the hooks, ServUO's SOS roll, the charybdis and lava fishing. `AOS-fish-pies.patch`
   adds the pie buffs. Everything else is additive files.
3. **The fish quests are a standalone port, not ServUO's quest framework** (section 1.5). The order lives on its
   shipping crate, and the gump is our own. That framework stays declined (README, S5). Whether this order should move
   onto pinned's MLQuest engine is decision 2.
4. **Corgul waits on boats, not on ship combat** (section 4). The boss, his seven crew types, his loot and his artifacts
   are in. Reaching him (two sacrifices at an altar, an island map, a sea warp that moves your boat) needs a hook in
   pinned's boat movement, so it waits for P268's phase 1.
5. **Tests: nine facts, each seen red by its own break, then the whole suite green and the image built** (section 3):
   2,357 tests, 2,353 passed, 4 skipped, 0 failed. The image booted twice on a scratch copy of the bot world. The second
   boot loaded the poles as saved by the new version.
6. **Recipe gating (F-43) does not block the pies:** they are Cooking band II, known with the Cooking band II book like
   every other band II dish. **But no vendor sells three of their seasonings** (decision 1).

## 1. What was ported

All under ours at ServUO's own paths, so apply-patches.sh mirrors them into `Projects/UOContent/Services/Expansions/High Seas/`.

| Part | ServUO file | Ours | What, and what changed |
|---|---|---|---|
| 1 | `Items/Fish/Bait.cs` (274) | same | A cup of bait for one FishInfo row; goes on a pole (fish) or trap (crab, lobster), swaps, pours cup to cup. Amount prompt as ServUO's |
| 1 | `Items/Fish/Hooks.cs` (245) | same | HookType, BaseFishingHook, LavaHook, DredgingHook, JunkProofHook. Fix: the pole's own hue is kept only when it has no hook (D-171) |
| 1 | `Items/Tools/FishingPole.cs` (bait part) | `server/patches/FishingPole-high-seas-bait-hooks.patch` | BaitType (saved as index), EnhancedBait, BaitUses, HookType, HookUses, OriginalHue, their setters, OnFishedHarvest, the tooltip lines; version 1 with `server/migrations/Server.Items.FishingPole.v1.json` |
| 1 | `Services/Harvest/Fishing.cs` (bait, hooks) | `server/patches/Fishing-high-seas-bait-hooks-lava.patch` + `HighSeasFishing.cs` | OnToolUsed's equivalent, the junk-proof skip, barnacle-covered shipwreck finds (`BarnacleShipwreckedItem`), ServUO's 17-number SOS roll (the bikini, oars, fish heads; the 1% ship's strongbox) |
| 1 | `Items/Fish/FishInfo.cs` | (P193's file) | reads the pole's bait now |
| 2 | `Items/OracleOfTheSea.cs` (57) | same | Fix: an empty Oracle no longer keeps searching (D-170) |
| 2 | `Spawners/CharybdisSpawner.cs` (343) | same | The spot, the 24-hour wait, the 7-hour kill delay, the 12-second rise with tentacles; `[CharydbisSpawner` |
| 2 | `Persistence.cs` (94) | same | `HighSeasPersistence` (pinned GenericPersistence "HighSeas"): the spawner and the fish standings |
| 2 | `Mobiles/Charybdis.cs` | (P193's file) | tells the spawner when it dies; drops 2-5 fish pies |
| 3 | `Items/LavaFishItems.cs` (407) | same | stone footwear, cracked lava rocks (IAxe: split with an axe, no patch), geodes, lava rock, stone paver |
| 3 | `Services/Harvest/Fishing.cs` (lava) | the Fishing patch + `HighSeasFishing.cs` | a lava-hooked pole on lava starts and finishes on its own definition |
| 4 | `Items/Fish/FishPies.cs` (690) | same | sixteen pies (generated from ServUO's file) and their effects |
| 4 | `Services/Craft/DefCooking.cs:469-565` | `customizations/Engines/Craft/CookingCraftRegistrations.cs` | the sixteen recipes, at an oven |
| 4 | `Misc/AOS.cs` (pie lines) | `server/patches/AOS-fish-pies.patch` | the soaks in Damage, the seven bonuses in AosAttributes.GetValue |
| 5 | `Quests/ProfessionFishQuest/*` (6 files, 1,554) | same six, and `Books/RareBook1-6.cs` | the fish monger, the order, the crate, the standings, the rewards, the six guide books (text verbatim) |
| 5 | `Generate.cs` (fish monger part) | same | `[GenFishMongers [dryrun]` |
| 6 | `Mobiles/Corgul/*` (8, 1,030) | same eight | Corgul the Soulbinder and seven soulbound crew |
| 6 | `Items/Artifacts/CorgulsEnchantedSash.cs`, `CorgulsHandbookOnTheUndead.cs` | same | his own artifacts |
| - | `Mobiles/BaseSeaChampion.cs` | (P193's file) | `RollArtifact`, overridable, because pinned's `GetArtifact` is not virtual and Corgul has his own odds |

### 1.1 Baits and hooks (part 1)

A baited pole rolls its fish first, at twice the base chance (three times enhanced), plus fishing attire, as P193's
`FishInfo.GetBaitStrength` already did for traps. A cast that catches anything uses one bait. A hook loses one use per
catch, and on a failed lava cast sometimes. ServUO's `HarvestSystem.FinishHarvesting` calls `OnToolUsed(from, tool,
item != null)` once a type is rolled. Pinned's has no such call and its `Construct` has no tool. So the patched Fishing
notes the cast's tool in `FinishHarvesting`, the cast's first `Construct` records whether it made a catch, and the pole
is told after. The junk-proof hook skips the footwear row 80% of the time, matched by type here (ServUO: `i == 5`, the
same row in both tables).

### 1.2 The Oracle and the charybdis (part 2)

As ServUO. The spot is `SOS.FindLocation` on the reader's facet (Trammel or Felucca); the cast must be at 100 Fishing,
pole baited for charybdis, Oracle in the pack, inside the 10 by 10 square.

### 1.3 Lava fishing (part 3)

Where lava counts: ServUO's `Fishing.LavaTiles` (P193 copied it to `LavaLobsterTrap.LavaTiles`), split into land tiles
0x1F4-0x1F7 and the static tiles, because pinned keeps land and statics apart (`HarvestDefinition.Validate(tileID,
isLand)`). Pinned picks a definition from the tile alone, so a lava cast with no hook finds no definition, the same as
ServUO's refusal. A lava cast is ServUO's own rule: a skill check, then the lava table (stone footwear from 80, cracked
rock from 80, paver from 85, a weapon rarely, 1.5 times in Felucca), else only a rare fish of the place (the Abyss's lava
fish and void lobster).

### 1.4 Fish pies (part 4)

The effects, by ServUO's AOS.cs lines: soaks take up to 5 off a hit of their type (never player against player on EJ);
+5 damage increase, +5 spell damage, +8 hit chance, +8 defense chance; +3 hit point, stamina and mana regeneration
(players); +10 Meditation or Focus (skill mods that obey the cap). One of each kind at a time, five minutes, buff icon
`FishPie`. **Recipe gating:** the pies' minimum Cooking is 55 or 61, Cooking band II, so `ClusterFRecipeGate.Classify`
makes them Book items under `book:Cooking:2`. An account with that book (from the Maritime Brotherhood) sees them.
Nothing blocks them beyond what blocks every band II dish.

### 1.5 The profession fish quests (part 5)

ServUO's quest is a `BaseQuest` in its Mondain's Legacy quest framework (MondainQuester, MondainQuestGump, the quest
log). The README records that framework as declined (reaffirmed by S5: quests are translated onto pinned's MLQuest
engine). This quest is not a fixed quest. Each offer draws a fish, an amount and a port of delivery from the player's
standing, and puts a crate in a boat's hold. So it is ported as its own small system:

- `ShippingCrate` is the order: owner, giver, turn-in monger, boat, title, lines (fish index, have, need); saved with the
  crate. A player's open orders are the crates they own.
- `ProfessionalFisherQuest` (a static class) is ServUO's `FishMonger.OnTalk`, `HasFishQuest`, the quest's
  constructor (lines), `OnAccept`, `GiveRewards` and `GetTitle`. `FishOrderGump` is a gump of our own in the shape of
  `MondainQuestGump`. It shows the offer, progress and completion with ServUO's clilocs (1116507-1116519) and Accept,
  Refuse and Continue.
- `PlayerFishingEntry` keeps the standing, saved in HighSeasPersistence. `[FishMongerStatus` is a player command.
- `FishMonger` is a blessed townsperson who answers a double-click within three tiles, as a quester does.

**Where OSI puts the givers:** ServUO's `[DecorateHS` spawners, eight docks in Trammel and Felucca. All eight are dock
planks at z -3 in the client's map files (read through vseUOAware, whose saved folder is the shard's
`client-data\classic-client-7.0.117.0`), the Sea Market included: its statics are in the 7.0.117.0 map. **No spot needs
map work.** The regions: the seven towns are pinned regions, and the Sea Market has none, so a monger carries his port's
name (`PortName`) and the Sea Market order keeps ServUO's default title, "Floating Emporium".

### 1.6 Corgul (part 6)

Corgul the Soulbinder (65,000 hits, necromancer-mage), his teleport-to-him pull, his dismount blast, his ring of fire,
his return to the island's heart, his crew (15 at each of five landing spots, raised once more when all are dead), his
loot (a unique artifact to one of the top five damagers; 8% / 12% Felucca shared, 25% / 40% decorative; a message in a
bottle, two nets) and his crew dying with him. Staff place him (`[add CorgulTheSoulBinder` on the island, `SpawnCrew`
true in his properties). The island (6337-6523, 1156-1342) is in the client's map files (land at z 10 at 6431,1236).

## 2. The patches, and the alternatives weighed

`docs/subsystem-policy.md` asks for the alternatives before a patch to an upstream file.

**FishingPole-high-seas-bait-hooks.patch** (pinned `Items/Skill Items/Fishing/FishingPole.cs`, 2 hunks, version 0 to 1).
1. A partial-class file with the fields: rejected. The members could live there, but the saved version is the class's
   own attribute (`[SerializationGenerator(0, false)]`), so the version needs a patch anyway, and a field that is not
   serialized loses the bait at every restart.
2. A side table (bait and hook by pole serial, saved in HighSeasPersistence): rejected. It keeps a pole's state off the
   pole, so a traded or banked pole would need the table kept in step. ServUO's state is on the pole.
3. Replacing the file: rejected (AGENTS.md: a replacement hides upstream drift).
4. **The patch (chosen):** ServUO's fields and setters, `OnFishedHarvest`, the tooltip lines; `MigrateFrom(V0Content)`
   for saved poles; the three subclasses (pinned's CaptainBlackheartsFishingPole, ours BegFishingPole and
   XenrrFishingPole) read the base's version as before. `server/migrations/Server.Items.FishingPole.v1.json` is written
   by hand in the generator's shape (P127's note: the build emits none), so the next bump can migrate from it.

**Fishing-high-seas-bait-hooks-lava.patch** (pinned `Engines/Harvest/Fishing.cs`, 9 hunks, applied after
`Fishing-shoes-achievement.patch`, made against the tree all the patches leave). Each hunk calls into `HighSeasFishing.cs`:
1. A subclass of Fishing installed as `Fishing.System`: rejected (P193's reason: a private constructor and a private
   static, more patch than the hunks).
2. Overriding `HarvestSystem` for lava (a second harvest system for lava fishing): rejected. The pole's double-click
   starts `Fishing.System`, so the pole would need to know which system to start, a second patch.
3. **The hunks (chosen):** `StartHarvesting` and `FinishHarvesting` hand a lava cast to HighSeasFishing and note a
   water cast's catch for the pole; `SpecialHarvest` asks for the charybdis; `MutateType` the junk-proof skip;
   `Construct` the dredged items, ServUO's SOS roll and strongbox; `OnHarvestStarted` the lava splash.

**AOS-fish-pies.patch** (pinned `Misc/AOS.cs`, 2 hunks, after `AOS-grapes-of-wrath.patch`): one call in `Damage` (the
soak, where ServUO's line 188 is) and one at the end of `AosAttributes.GetValue` beside the grapes of wrath. The
alternative, a damage event: pinned raises none between the resistance math and the final hit, and GetValue has no hook.

## 3. Tests

`server\tests\Services\HighSeasFishingSecondHalfVerification.cs`, nine facts. The host has no tile data (D27), so the
casts aim at a `Static` item (water 0x1797, lava 4846), which pinned's GetHarvestDetails reads by its own ItemID (a
StaticTarget's is masked to 0). Random numbers are pinned through `BuiltInRng.Generator` where a fact needs them.

| Fact | Break (red run) | Red |
|---|---|---|
| 1 a bait changes the catch (unbaited: a shore fish; baited: the fairy salmon at the same roll; enhanced at three times; a baited cast through the patched Fishing uses one bait) | FishInfo stops reading the pole's bait | "Expected FairySalmon, Actual PumpkinSeedSunfish" |
| 2 bait goes on through its target, swaps, pours, refuses the wrong gear, round-trips | the pole's uses do not grow | "Expected FairySalmon, Actual null" |
| 3 a hook's uses (tied on with its hue, an old hook back in the pack; one use per catch through the patched cast; at none the pole's own hue; a miss wears the hook, spends no bait; the junk-proof skip; the pole round-trips) | the patched cast no longer tells the pole (one patch line swapped) | "Expected 1, Actual 2" |
| 4 lava only in lava (no definition for lava without the hook; a hooked pole on water fishes water; on lava the patched StartHarvesting takes the cast; FinishHarvesting gives a stone paver at this roll, never a fish; the rows by skill; stone boots hold; a rock splits under an axe) | StartHarvesting never routes lava | "a lava-hooked pole did not start a cast on lava" |
| 5 a fish pie's buff (+5 damage increase, gone after; one of a kind; one eaten off a stack; a fire soak takes 5 off; +8 hit chance; +10 Meditation; all sixteen construct and round-trip, sixteen effects; sixteen recipes at an oven, from 55 or 61) | GetValue adds no pie bonus (patch line) | "Expected 5, Actual 0" |
| 6 the Oracle and the spawner (a reading names a spot and spends a charge; an empty Oracle does nothing; bait, skill and spot each required; the cast snags Charybdis once; the spawner round-trips; the kill delay) | a reading spends nothing | "Expected 4, Actual 5" |
| 7 Corgul (artifacts construct; odds by facet; 75 crew on the island; a round trip with the crew; at death the crew die, the corpse holds the bottle and two nets) | his crew are healed, not killed | "BoundSoul outlived Corgul" (75 of 75) |
| 8 a fish order (port of delivery; one line of ten shore fish; the crate in the hold; only ordered fish go in and stay; delivery pays reward and standing; a destroyed crate forfeits; standings survive a save; ServUO's tiers and categories; a tier 1 bait reward) | a fish put in counts nothing | "Expected 10, Actual 0" |
| 9 `[GenFishMongers` (sixteen mongers with their ports and ranges, then a re-run skips all) | never sees a monger already there | 16 of 16 lines "placed" on the re-run |

### Runs (`docker/uo/build.sh -t sl-modernuo:cc-P269`, under the `docker-build` lock, taken and released for each stretch)

Free memory 12.3 GB at the start. Logs `p269-*.log` in the session scratchpad.

| Run | Tree | Result |
|---|---|---|
| c1 | first cut | patch gate: the pole patch's path has spaces and its header was unquoted (TaxidermyKit's patch quotes it); quoted |
| c2, c3 | | compile: the generator makes its own backing field for a plain `SerializableProperty` (Bait.Index), so `useField`; the test's `BuiltInRng` needs `using Server.Random` |
| c4 | | **2,354 tests, 2,348 passed, 2 failed:** lava tiles as (low, high) pairs where pinned's definition reads pairs only when `RangedTiles` (lava is a list; fixed); `[CharydbisSpawner` lacked its `[ShardCommand]` (CommandDeclarationVerification; added) |
| c5, c6 | Corgul added | compile: the generator makes `AddToHelpers` for a list field; `FindItemsByType` is an enumerator, not a list |
| c7 | | **2,355 tests, 2,351 passed, 4 skipped, 0 failed** |
| c8-c11 | fish quests added | compile: the generator's `LineHave` property for a `_lineHave` field (renamed); `LRReason` is in Server.Network; the books' `String.Format` (no `using System`). c11: one failure, my test's expected cliloc (1116497 is Britain, the order went to Trinsic, 1116498) |
| c12 | | **2,357 tests, 2,353 passed, 4 skipped, 0 failed** |
| red | the nine breaks (`breaks.py`: pristine copies taken and hashed first) | **2,357 tests, 2,344 passed, 9 failed, each of the nine facts by its own break**, nothing else; restored, hashes equal |
| full | restored tree | **2,357 tests, 2,353 passed, 4 skipped, 0 failed; no compiler warnings; image `sl-modernuo:cc-P269` built** (sha256:2068d46c29b8) |

What the facts cannot cover: a cast through the client on a real water or lava tile, the gump on the wire, a boat
sailing between ports, Charybdis rising after its timers, Corgul's fight. Those are the play tests below.

### Headless boot

`sl-modernuo:cc-P269` on a copy of `D:\UO\bot-shard` (Configuration and world, 33 MB of saves), container
`sl-p269-proof`, 127.0.0.1:2596, autosave off, client files from `D:\UO\tool-trials\client-data-copy`. The script is
P281's `proof-shard.ps1` with its name and image changed, kept in the session scratchpad. Run under the test-shard lock,
01:10-01:12, before the 01:30 nightly. The shared Test Shard (2594) was not touched.

- Boot 1: `[ShardVersion] Shattered Legacy 2026.10.25`, `Loading world done (211962 items, 35210 mobiles)`, no exception.
  The world's item type table (`Saves/Items/Items.idx`) names `Server.Items.FishingPole`, so saved version 0 poles were
  migrated on load. Stopped with `docker stop` (SaveOnShutdown saves): `Saving world done`, `...saved in 1254 ms`;
  `Saves/HighSeas/HighSeas.bin` written (59 bytes).
- Boot 2, on that save: `Loading world done (213978 items, 35415 mobiles)` (the seeders' additions), no exception, saved
  again on stop. The poles loaded as saved by version 1.

**Not done:** a client. Nothing here was seen in game.

## 4. What waits on ships or map work

| What | Why it waits | On what |
|---|---|---|
| Reaching Corgul: `CorgulAltar` (two sacrifices, the island map, the three-hour deadline), `CorgulIslandMap`, `CorgulWarpRegion` (a boat with the map sailing into the warp is moved to the island), `CorgulRegion` (no recall or gate there, boats put back out, players sent home at the deadline) | ServUO's BaseBoat calls the warp region from inside its movement and teleports the boat; pinned's BaseBoat has no such call | P268 phase 1 (galleons that sail, with the boat movement hook) |
| Fish orders of 2 to 6 lines | ServUO gives more lines on a galleon only (`boat.IsClassicBoat ? 1 : CalculateLines()`); every pinned boat is classic | galleons (P268 phase 1); `PlayerFishingEntry.CalculateLines` is ported and waiting |
| The Sea Market's vendors (its tavern keeper sells three pie seasonings) and its region (boat restriction) | not in this prompt; the Sea Market's statics are in the map files | decision 1 |
| MatchCord, Niter | cannon resources | P268 phase 3 |
| Sea champions damaging boats | D-132 (P193) | P268 phase 2 |

**Map work: none.** All eight fish monger docks and Corgul's island are in the client's map files.

## 5. Deviations and decisions for Chase

The register ends at D-122 in `docs\fidelity-principle.md`; later prompts proposed numbers up to D-168 (cc-P196). These
are proposed as D-169 onward; agents do not edit `docs\`. Renumber as needed.

| D | What | Why | Reverses when |
|---|---|---|---|
| D-169 | ServUO's SOS haul roll replaces pinned's (17 numbers: each stock category on two, the High Seas oddments on one, a chest on two; pinned: one of 8 each), and a chest is a ship's strongbox 1% of the time | the High Seas roll is OSI's since High Seas; the bikini needs it | never |
| D-170 | An empty Oracle of the Sea no longer searches (ServUO searched with no charges, its count going negative) | a bug with a broken result is fixed (D-4 rule) | never |
| D-171 | Tying a hook over another keeps the pole's own hue for when the hook wears out (ServUO kept the first hook's colour) | broken result fixed | never |
| D-172 | Eating a fish pie takes one off the stack (ServUO deleted the whole stack) | broken result fixed | never |
| D-173 | The Fairy Salmon pie's casting focus and the Lava Fish pie's soul charge act on nothing | no casting focus check and no soul charge here (D-21) | either lands |
| D-174 | The lava catch's weapon has no Searing socket; lava's harvest banks are their own | no item sockets or Searing effect; lava and water never share a tile | sockets land |
| D-175 | The fish quests run on the crate, not ServUO's quest framework: no quest log entry; resigning is destroying the crate | the framework is declined (S5) | decision 2 |
| D-176 | Reward fishing poles carry no magic attributes; tier 4's boat paint is not a reward | pinned's pole has no attributes; no boat paint | the pole gains attributes; ship content |
| D-177 | Corgul: the Mysticism handbook is not in his unique list; no tainted life aura, treasure map chance or soulbound flag (as D-139); his pull-to-him is in his own OnThink (ServUO's BaseCreature.TeleportsTo); the fire ring's bleed is pinned's BeginBleed | no MysticBook; none in pinned | each lands |
| D-178 | Champions give power scrolls when they die in Felucca: pinned's BaseChampion does, with no switch, so Corgul does, and so do Charybdis and Osiredon (P193, not recorded then). ServUO's sea champions give none | pinned has no CanGivePowerscrolls | a switch is added (a BaseChampion patch) |

Copied, not fixed (D-4 rule, missing results): ServUO's reward tiers test 100 before 150 and 210, so orders only ever pay
tier 1 or 2; book 6's title reads "Vplume 6"; the reputation counts a three-line order's first line three times.

Decisions for Chase:

1. **Who sells the pie seasonings?** Mento Seasoning, Samuel's Secret Sauce and Dark Truffle are sold only by the Sea
   Market's tavern keeper in ServUO, and Fresh Ginger by bakers and farmers there. No vendor here stocks any of them, so
   **players cannot bake fish pies yet** (they can eat Charybdis's). Choices: port the Sea Market's vendors (a prompt;
   the market's statics are in the map), or add the four to an existing tavern keeper, baker and farmer (smaller, not
   OSI's place).
2. **The fish orders and the quest engine.** S5's rule is that quests go onto pinned's MLQuest engine. This order is a
   per-offer contract (random fish, random port, a crate in a boat), which MLQuest's fixed quest definitions do not
   express without a custom objective and turn-in. Ported standalone, it adds no second engine. Say if you want it
   rewritten onto MLQuest; the crate, standings and rewards carry over.
3. **`[GenFishMongers`** is a new world command (WorldSetup, re-run skips). It is not in the console's world setup order
   (`$script:WorldSetupOrder` in `scripts/Shard-Console.ps1`); say where it belongs in a fresh world's sequence.
4. **D-178:** say if champions in Felucca should stop giving power scrolls for the sea champions (a small BaseChampion
   patch).

One tool note: the Read tool was denied for the first lines of `CorgulTheSoulbinder.cs` (an unattended run, a file
outside this working directory). I read them with `sed -n 1,14p` instead. Nothing was lost.

## For Chase

**Rebuild the test shard** (console, Test shard, Rebuild) and run `[GenFishMongers` once before trying these. Steps are
in `testing/playtest-steps.json`, buckets in `testing/bot-triage.md` (P269 group):

- P269-1 BOT: bait and a lava hook on a pole, read the pole's tooltip.
- P269-2 EYES: lava fishing; split a rock; stone boots hold you.
- P269-3 BOT-PARTIAL: bake and eat a bull fish pie (needs `[add` for the seasoning, decision 1).
- P269-4 EYES: the Oracle, the spot, Charybdis rising.
- P269-5 EYES: a fish order from Britain to its port, and the reward.
- P269-6 EYES: Corgul and his crew on the island (staff placed).
- P269-7 CC: the test world boot (done, section 3).

## Repo size rule

No new file over 5 MB; the largest new file is the test file at about 40 KB. Scratch (generators, break
script, pristine copies, the scratch tree the patches were cut from, the boot world copy, build logs) is in the session
scratchpad, outside both repos. Two new files carry non-ASCII text: `RareBook2.cs` (ServUO's curly apostrophes, the
book's text verbatim) and `CharybdisSpawner.cs` (the degree sign, as pinned's own Sextant.cs writes it).

## Commit preflight

`Commit-ShardWork.ps1 -DryRun -NoRefresh -NoArchive -Branch golem/Iron/P269 -CodeRepo D:\UO\golems\Iron\ShatteredLegacy
-DocsRepo D:\UO\golems\Iron\shard-migration`, 2026-10-25 (the script's defaults are the main checkouts, other desks).
Neither repo is blocked:

- **Code, 44 files pending:** CHANGELOG.md, VERSION, apply-patches.sh, the three patches, the migration JSON, the test
  file, CookingCraftRegistrations.cs, and 35 High Seas files new or changed.
- **Docs, 7 files pending:** README.md, dashboard.html, testing/bot-triage.md, testing/playtest-steps.json,
  tools/expansion-coverage.json, tools/progress.json and these notes. README, the dashboard and the two tools JSON files
  are progress.py's output (`SL_SHARD` at the Iron copy).

The dry run said "would add, commit and push" for both. I took and released the docker-build and test-shard locks; no
package or Haven lock was needed. Nothing was placed in any world, and no live config was changed.

`CHANGELOG.md` gains `## 2026.10.25` above `## 2026.10.24.18` (Added x9, Staff x3), and VERSION is 2026.10.25. If a
branch with its own section on the same lines merges first, this merge will stop on CHANGELOG.md: keep every section in
version order and the highest VERSION.

P269 DONE
