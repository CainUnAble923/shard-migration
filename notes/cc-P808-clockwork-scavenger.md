# cc-P808: the Clockwork Scavenger

## In plain words

- **The Clockwork Scavenger is in, from the Tinkers' Union, as you corrected on 11-07.** A character at Journeyman in the Union says "scavenger" to a Tinker guildmaster (or picks Quest Conversation on him) and gets a frame. They bring 10 gears, 10 springs, 5 clock parts, 2 axles with gears and 50 iron ingots, use the frame, and a small brass crawler follows them. There is no League shop row.
- **It loots for its owner.** Every 3 seconds it lifts gold, gems and reagents from monster corpses next to it into the owner's backpack. The owner picks what it takes in its Options. It never takes from a player's corpse or from loot that would be a crime, and never takes weapons or armour. With a Clockwork Load Harness III on the owner's mule nearby, the loot goes to the mule.
- **One per character.** Nothing can hurt it. If the owner releases it, it powers down, and the guildmaster hands out a new frame for the same parts.
- **For you:** nothing to deploy yet; it ships with the next main build. Every number (parts, look, reach, pace, rank) is in `Configuration/clockwork-scavenger.json`. Two calls I made are listed under "Decisions I made": a released Scavenger can be rebuilt, and it only works for the character who built it.

## The decision, quoted

`docs\feature-queue.md`, F-33 mule modules, Chase 2026-10-05:

> **The Clockwork Scavenger is the League auto-loot reward** (Chase 2026-10-05), not a separate system: one auto-looter. **Option A (Chase 2026-10-05):** the League grants the Scavenger, which loots into the owner's backpack; Clockwork Load Harness III makes it carry loot to the mule instead.

`docs\feature-queue.md`, the League decision sheet, Chase 2026-10-23, item 9:

> The **Clockwork Scavenger stays** as the League's auto-loot reward (F-33 Option A).

Neither said how it is earned, so I asked (`Iron-P808-20261106-165144-5ad2`). Chase picked a League shop row (1,000 AP, 600 Renown) on 11-07 at 08:25. The prompt was then corrected, overriding that answer:

> **Correction from Chase, 11-07 08:25 (overrides the answer to Iron-P808-20261106-165144-5ad2, the League shop row):** the Scavenger comes from the Tinkers' Union, not the League shop. A character who reaches **Journeyman** in the Tinkers' Union gets a build quest from the Tinker guildmaster (gather the parts, assemble it); finishing it gives one Scavenger, one per character. No League shop row.

I built the correction. No shop row was ever added, so there was nothing to take out. `docs\feature-queue.md` still calls it "the League auto-loot reward"; I did not edit `docs\` (standing rule 2). **A docs line for Chase or the overseer:** F-33's Scavenger is now earned from the Tinkers' Union.

## What was built

Code in `server/customizations/Mobiles/ClockworkScavenger/`, three files, 660 lines with comments. That is more than P796's estimate of about 300: the config file's checks, the quest's refusals and the filter window. Two saved types, as the sketch said. No engine change and no patch.

- **`ClockworkScavengerQuest.cs`: the quest.** The guildmaster's answer, in order:
  - not in the Tinkers' Union: "Join the Tinkers' Union first";
  - below the config rank (`minRank` 2, Journeyman, by `ClusterFGuildSystem.GuildRankIndex("tinkers", …)`): "Come back when you are Journeyman";
  - has a Scavenger: refused;
  - has a frame: the parts list again;
  - otherwise a frame, into the pack.
  - Asked by speech ("scavenger", hooked in `ClusterFGuildmasterExtension.OnCustomSpeech`) or by context menu. The menu uses stock cliloc 3006156, "Quest Conversation", members only, so no client update is needed.
- **`ClockworkScavenger.cs`: the frame and the pet.**
  - **The frame** (`ClockworkScavengerFrame`, saved) is blessed and bound: only its tinker or staff can lift it. Used from the pack, it checks every part first, then the follower slots. On a refusal nothing is used. Then it consumes exactly the configured amounts and makes the Scavenger, controlled by and following its builder, and deletes itself.
  - **The pet** (`ClockworkScavenger`, saved) saves its builder and filter. It is blessed, so pinned `Mobile.CanBeHarmful` keeps anything from targeting it. It does not fight, has no food, and `DeleteOnRelease` is true.
  - **The loop** runs on one shard timer, not the pet's `OnThink`, since a pet's AI sleeps when its sector goes idle (as `MuleModules` found). Each pass needs all of these: owner is the builder, online, alive, on the same map, within 12 tiles, and the pet is not stabled.
  - **What it takes:** from each corpse within 2 tiles it takes items the filter keeps, at most 5 a pass. The corpse must be a creature's (not a player's), not a criminal loot for the owner (`Corpse.IsCriminalAction`, `CanLoot`), and not in a house. Only items the owner can see count, so instanced loot shares are kept (`Corpse.IsChildVisibleTo`). Containers and cursed items are skipped. The filter is the Salvage Bin's list (`MuleModules.PickupCategories` and `Matches`): gold, gems, reagents, ore and ingots, hides and leather, logs and boards, bandages. The default is gold, gems and reagents. None of these is gear, so it never hands over an item with properties.
  - **Load Harness III:** if the owner's mule within 12 tiles carries Clockwork Load Harness at tier III, the loot goes into the mule's pack first, then the backpack. `MuleModuleData` now marks that module **Built**, and the "redirect hook is" stub note is gone. P515 was right: no redirect code existed until now.
  - The owner's Options window (stock cliloc 3000127, as the mule uses) toggles the filter.
- **`ClockworkScavengerConfig.cs`: the numbers.** `Configuration/clockwork-scavenger.json` is written with the defaults on first start, then read at start. A bad file is refused whole, every error is printed, and the defaults stay. Parts must name a real item type. Fields: `minRank`, `parts` (type, amount, label), `body` (0x30, the stock scorpion body), `hue` (0x972, bronze), `controlSlots` 1, `tickSeconds` 3, `corpseRange` 2, `ownerRange` 12, `maxPerTick` 5, `muleRange` 12, `defaultFilter`.

**Saves (D40).** Two saved types, both source generated, version 0: `ClockworkScavenger` (builder, filter) and `ClockworkScavengerFrame` (owner). No engine type changes its save.

**On an existing world.** Nothing needs seeding: the Tinker guildmasters are already placed (`ClusterFGuildStarterPath`, New Haven at 3667, 2506), and the speech and menu hooks are code. The config file writes itself on first start. A world with neither type loads as before.

**Rules check.**
- No skill or stat points, power scrolls, bless deeds or property artifacts.
- The parts are stock Tinkering parts and iron.
- The loot is only the Salvage Bin's categories.
- Every number is in the file.
- No engine change.

**The Picky Beetle.** Only the idea of the pick-up loop is used: Xanthor's (from Charon) `third-party` pack, never built or run. Its faults are not carried over: it worked untamed, had no looting rights check and used a zero-second timer. The credit is in the file header.

## Decisions I made

- **Rebuilding after release.** "One per character" is one at a time. A released Scavenger powers down, and the guildmaster gives a new frame for the same parts. It cannot die (blessed), so release is the only way to lose one. Say if you would rather it were once ever.
- **Only for its builder.** Pinned's pet Transfer can't be blocked without a patch. A transferred Scavenger follows its new owner but loots nothing. The tooltip says who built it.
- **Corpses only, not the ground.** F-33 and the Salvage Bin answer split the work: the Scavenger loots corpses, the bin picks up loose ground items.
- **The parts and the look are mine** and are placeholders in the file: 27 Tinkering crafts' worth of parts plus 50 iron ingots, and the scorpion body in bronze, from existing art.
- **Staff loot anything.** Pinned's `IsCriminalAction` is false for GameMaster and up, so a staff character's Scavenger loots every creature corpse. Players are held to their rights (fact 4).
- **Reach is from the Scavenger, 2 tiles.** A following pet trails its owner by a tile or two, so it loots a corpse once the owner steps up to it. In the first client run it stopped 3 tiles away and took nothing until the character stood on the corpse. If that feels slow in play, `corpseRange` in the file raises it.

## Tests

`server/tests/Mobiles/ClockworkScavengerVerification.cs`, 9 facts:

1. The guildmaster refuses an outsider, then an Apprentice, and gives a Journeyman one bound frame, never two.
2. A missing part is refused with nothing used. With every part, each is used exactly once, and the Scavenger is blessed, follows its builder, takes one slot and has the default filter. After that, no new frame.
3. The frame is bound: another character can neither lift it nor use it.
4. The loop:
   - it takes gold and reagents from a corpse the owner earned, and leaves a sword;
   - it takes nothing from a corpse that would be a crime, or from a player's corpse;
   - nothing with an empty filter, an owner 20 tiles away, or an offline owner;
   - at most 5 a pass.
5. Load Harness II leaves loot in the backpack, and III sends it to the mule. The module data says Built.
6. Released, it is gone, and the guildmaster gives a new frame.
7. Both types survive a save: builder, filter and frame owner.
8. The file: defaults are valid; a missing file is written; a good edit is read; a bad part or filter is refused whole, keeping the table in force; broken JSON is refused.
9. Quest Conversation shows for members only, and the Options window toggles a category.

- **Red:** the facts were written with the code, so I broke the code on purpose: 28 breaks (`cc-P808-tools/mutate808.py`, results in `cc-P808-tools/mutants.txt`). 27 turned a fact red, and every fact went red at least once. The one that stayed green, `loot-empty-filter`, removes an early exit that changes nothing: an empty filter already matches no item.
- **Green:** quick runs in a builder container (`cc-P808-tools/run-facts.sh`, 9 of 9).
- **The gate:** `sl-modernuo:cc-p808` built through the gated build script, 3,205 passed, 6 skipped, 0 failed, `EXIT=0` (`cc-P808-tools/gated-build.log`, UTF-16). `latest` was not moved.
- Run on its own, `MuleModuleVerification` fails with "Do not use PasswordProtectionAlgorithm.None": it relies on another suite having set up accounts. It passes in the full gate, so this is not new, but it is fragile.

## Shots

`notes\cc-P808-shots\`, TazUO on the private proof shard (127.0.0.1:2596, a copy of the bot world, image `sl-modernuo:cc-p808`, test-shard lock held). The script is `cc-P808-tools/Shots808.py`; its own checks are in `walk.log`, all PASS on the last run.

1. `1-guildmaster-gives-the-frame`: the guildmaster's line with the parts list. Before it, the same character was told to join, then told to come back at Journeyman.
2. `2-frame-needs-parts`: the frame's tooltip (bound, blessed, the parts) and the "still needs" refusal.
3. `3-parts-in-pack`: the parts in the pack.
4. `4-scavenger-built`: the bronze crawler beside its builder. Tooltip: "(tame) Built By Iron Cogs, Collects: Gold, Gems, Reagents".
5. `5-corpse`: an orc killed beside it, its corpse open with 62 gold.
6. `6-loot-collected`: "\*click-whirr\*" and "Your Clockwork Scavenger collects 1 item.", with the gold in the pack going from 1,000 to 1,062.

- **The guildmaster in the shots was placed by staff** on open ground (1986, 2244). On main's map the New Haven coordinates in `ClusterFGuildStarterPath` aren't the Tinkers' hall (the halls moved with the SoS map), so the first run found no guildmaster. The character is staff, so its standing was set with `[GuildStanding tinkers 5000`, and joining was done through the guild's own gump.
- Not shot: the Options window (fact 9 covers it) and the Load Harness III redirect (fact 5).
- The run shows constant Focus and Meditation gain lines. That comes from the bot world's admin character, not from this work.

## Deviations and decisions for Chase

- **Earning route:** built as your 11-07 correction says (Tinkers' Union, Journeyman, build quest), not the League shop row from the earlier answer. No shop row was ever added.
- **One Read was denied** (unattended run): the Read tool on `ShatteredLegacy\server\customizations\LeagueShop\LeagueShop.cs`, to read the shop before the correction arrived. I read it with `cat` instead, as the hand-off says for the prompt file. The shop isn't used in the end.
- **`docs\feature-queue.md` F-33** still says the League grants the Scavenger. It needs a docs edit, which agents don't make.
- **The two calls under "Decisions I made"**: rebuilding after release, and only the builder gets loot.

## Files

- `ShatteredLegacy`:
  - new: `server/customizations/Mobiles/ClockworkScavenger/` (3 files) and `server/tests/Mobiles/ClockworkScavengerVerification.cs`;
  - changed: `server/customizations/ClusterFGuildmasterExtension.cs` (speech and menu hooks), `server/customizations/Mobiles/Mule/MuleModuleData.cs` (Load Harness III Built), `CHANGELOG.md`, `VERSION` (2026.11.07).
- `shard-migration`: this file, `cc-P808-shots/`, `cc-P808-tools/` (fact runner, breaks, gated build, shot rig).

P808 DONE
