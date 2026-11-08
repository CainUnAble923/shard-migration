# cc-P363: quest markers over NPCs, key items, and coloured moongates as new gates

## In plain words

- **Quest markers.** A gold "!" now floats over someone who has something new for you, and a "?" over someone waiting
  for you to hand something in. You see them over:
  - Rook and the farmhand in the tutorial;
  - the League Registrar;
  - the guildmaster of each guild you belong to.

  Each player sees only their own markers. One setting turns them off for everyone.
- **Keys.** Hestia's 34 keys and 12 gem tokens are real items now. Three things use them:
  - boss room doors that open only for their own key;
  - League trial gates that let through only the holder of that chapter's key;
  - top-tier (tier 6) loot boxes, which come locked and open with a Vault key. Bosses sometimes drop Vault keys. Boxes
    already earned stay unlocked.
- **Moongates.** Carl Hamilton's spinning gates come in blue, red, black and white as new items. The old moongates are
  unchanged.
  - A command places a white gate at League Headquarters that goes to any guild hall, and a blue gate at each hall
    that comes back.
  - The Valley of Eodon gate turns red the next time it is generated.
- **For you:**
  - Rebuild the test shard from this branch and update a test client with the player package.
  - Run `[ShardGates guildhalls dryrun` and then `[ShardGates guildhalls` if you want the gate network.
  - Decide whether tier-6 boxes should stay locked by default (Decisions 1).
  - Add RedRooster, Hestia and Carl Hamilton to the shard credits list.

2026-10-23, the Iron Golem (Opus), branch golem/Iron/P363 of both repos. Prompt: `cc-P363-quest-markers-keys-gates.md`.
Not committed (the Golem commits after DONE). Nothing was run against any world. Nothing was deployed. The package was
not built or published.

## 1. The art (task 1 of the prompt's Read first)

Read first:
- `ART-LIBRARY.md` sections 2 and 3.
- The six `SOURCE.txt` files.
- The registry rules.
- P243's notes and tool (`notes/cc-P243-tools/hall_art.py`), which this follows.

The packs were **copied to the session scratchpad first** and converted from the copy (the prompt: never build from
`D:\UO\third-party`). The tool is `notes/cc-P363-tools/p363_art.py` (registry, then PNGs, then records).

**IDs: 46592-46663 (0xB600-0xB647), 72 in one block.**

| IDs | What | Author |
|---|---|---|
| 46592-46594 | "!" frames E1-E3 | RedRooster |
| 46595-46597 | "?" frames Q1-Q3 | RedRooster |
| 46598-46602 | blue gate, five frames | Carl Hamilton |
| 46603-46607 | red gate | Carl Hamilton |
| 46608-46612 | black gate | Carl Hamilton |
| 46613-46617 | white gate | Carl Hamilton |
| 46618-46629 | gem tokens, in her readme's order (Amber to Tourmaline) | Hestia |
| 46630-46663 | Item Key 1-34 (1 is her blank partial-hue key) | Hestia |

Counted: 6 marker BMPs, 20 gate BMPs, 12 tokens, 34 keys = 72 images. Hestia's folder holds 47 files: these 46 plus a
preview .jpg (her readme is a 48th file, not counted by the art library). The jpg and readme are not shipped.

How the block was chosen:
- `find-free-art.py --data D:\UO\tool-trials\client-data-copy --run 72` listed 57 free runs. I took the start of the
  second longest (0xB5A5-0xBB7F), so a Golem taking "the longest run" (0xD801) does not collide.
- No unmerged Golem branch registers anything in this block. Only P362 has registry rows unmerged, at 13049-23080.

**Pixels.** BMP to PNG, with pure black made transparent.
- Tokens, keys and gates keep their canvas (`--keep-geometry`).
- **The markers are cut to their frames' union and stood 92 px above the tile's front tip (`--bottom-pad 92`).**
  - Why: RedRooster's 44x100 canvas puts the mark 60 px up, which is about chest height on a person.
  - Drawn as an effect on an NPC, the mark has to clear the head. TazUO draws an effect like a static (bottom row on the
    tile's front tip: `View.DrawStaticRotated`, `GameEffectView.Draw`).
  - 92 px puts it about 70 px above the feet. Not seen in a client (For Chase 2).
- The white gate has a pure-black centre, which becomes see-through, as it would in an art file.

**Records** (`records.json`, and the server's copy `ShardItemArt.Records`): only each animation's base ID gets a record
(Build-UoOverrides skips an animation whose other frames have records).

| Piece | Flags | Weight / height | Animdata | Source |
|---|---|---|---|---|
| Markers 46592, 46595 | Animation | 255 / 0 | frames 0,1,2,1 at interval 3 | RedRooster's words: "1,2,3,2", "frame rate 3" |
| Gates 46598, 46603, 46608, 46613 | 0x05804000 | 255 / 0 | frames 0-4 at interval 2 | OSI's blue moongate 0xF6C, read from the client's tiledata.mul 2026-10-23 |
| Tokens, keys | ArticleA (key 1 also PartialHue) | 1 / 1 | none | OSI's copper key 0x100E |

That is 52 tiledata and 6 animdata records.

**Registry and credits:**
- `registry.csv`: 72 rows. Each license names the author's terms and the credit.
- `SOURCE.txt`: a new section with the packs, links, terms, ranges, pixels and records.

**Checks:**
- `validate-art.py check-registry`: **0 of 699 rows have problems.**
- `find-free-art.py --check-registry`: **0 of 699 registered IDs are no longer free.**

## 2. Quest markers (`server/customizations/QuestMarkers.cs`, new)

**How it draws:**
- Every 3 s, each online player is sent a **fixed effect on each NPC within 14 tiles** that has something for them.
- It goes to that player's NetState only, so it is per player.
- TazUO moves a fixed effect with its mobile (`FixedEffect.Update`), draws it one depth above it, and animates it from our
  animdata.
- Each effect lasts 3.2 s (duration x 50 ms, `EffectManager.CreateEffect`), so a change ("!" to "?", or gone) shows
  within one pulse.
- I chose an effect over an item because an item is seen by everyone. Pinned has no per-viewer item short of a
  `SendWorldPacketTo` trick (InvisibleTile's), which would also need its own movement following.

**Sources.** All checks are read-only, as the survey warned: `GetOrCreate*`, `RequisitionSystem.Open` and
`BulkOrderSystem.CanGetBulkOrder` all change state, and none is called.

| NPC | "!" | "?" |
|---|---|---|
| League Registrar | not registered with the League; or the mule errand can be taken (`MuleErrand.RefuseOffer == null`) | `ClusterFLeagueRanks.Evaluate(pm).CanPromote`; or the mule is delivered |
| Rook Hallowell | in the tutorial with core lessons left; or a skipped tutorial (the remedial offer) | the core is done (graduation); or the graduation companion waits |
| Wren Tallow (farm) | step 1 (the pet) | step 3 (pests cleared: "go back to the Farmhand") |
| A guildmaster, for a member of its guild (`GetDefForGuildmaster`) | a work order can be accepted; for the Society of Smiths also a small or large BOD under the cap, or a commission (cap, cooldown) | a work order's requirements are met; for smiths a completed BOD in the pack, or an item that fills a commission |

- **Trial NPCs:** trials finish on the spot (`TutorialCoreTrials.Observe`, `TutorialWingTrials.Finish`). No trial NPC
  has a turn-in, so the next lesson is Rook's "!".
- **League quest givers:** none exists beyond the Registrar. Hunts, bounties, story trials and the squire quest are not
  built, as the survey found.
- **Other systems** add a source with `QuestMarkers.Sources.Add`.

The setting **`clusterf.questMarkers`** (default on) is read each pulse.

The smith's BOD caps were private. They are now public, unchanged (`ClusterFSmithBODSystem.cs:56-58`).

## 3. Keys (`server/customizations/ShardKeys.cs`, new)

- **`ShardKey : Item`**: name, hue, one of Hestia's 34 designs (`Design` in [props), and a **lock tag**.
  - It opens a lock only when the tags are equal and not empty (`Opens`).
  - Double-click, then target a lock.
  - It is **not** a stock `Key`. A stock key blank copies any Key's KeyValue (pinned `Key.CopyTarget`), and a blank's
    KeyValue 0 would match a door left at 0. Fact 2 proves the blank does not open ours.
- **`IShardLock`**: anything a key opens (`LockTag`, `LockName`).

The three uses the prompt asked for:

1. **League trial gate keys.**
   - `ShardKeys.LeagueTrialGateKey(chapter)` makes the key: design 30, a blue star.
   - `ShardGates.LeagueTrialGate(chapter, to, map)` makes the gate: a **Black** ShardMoongate that lets only that key's
     carrier through.
   - No League trial area exists yet (the story trials are not built), so nothing is placed. Staff can place one.
2. **Dungeon boss room key.**
   - `ShardLockedDoor` is a dungeon metal door (MetalDoor2) that opens only for a carrier of its key. Staff pass.
   - `ConsumeKey` makes the door take the key.
   - `ShardLockedDoor.BossRoom(facing, dungeon)` and `ShardKeys.BossRoomKey(dungeon)` make the pair (design 12, a
     skull).
   - The only keyed door in the shard is the Underworld puzzle room (stock keys). No custom boss room had a door to
     lock, so this one is placed by staff.
3. **A loot box tier's key-to-open.**
   - Boxes of tier `clusterf.lootBoxes.keyTier` (default 6, the top) are made as `ShardLockedLootBox` (in `MakeBox`).
   - They open only with a **Vault key** (design 14, a padlock), which the box takes.
   - A Vault key drops on a boss kill with chance `clusterf.lootBoxes.vaultKeyChance` (default 0.25), on every kill,
     not only the first, into the killer's pack.
   - Boxes earned before this update are plain LootBoxes and stay keyless. It is a new class, so no save migration was
     needed.

**Other good uses** (not built):
- altar keys for a Peerless-style encounter;
- a key ring gump that holds ShardKeys;
- quest-chain keys handed out by NPCs (with a "?" marker when held);
- the gem tokens as League discount tokens or event currency (the art library's suggestion);
- guild hall vault rooms;
- seasonal event gates;
- a Rootdeep Vault key replacing its region gate;
- treasure map chests that need a found key.

## 4. Gates (`server/customizations/ShardMoongates.cs`, new)

- **`ShardMoongate : Moongate`** keeps pinned's delay, confirmation gump, young, murderer and sigil rules, and pets.
  - It adds a `Color` (Blue, Red, Black, White, picking the art), an optional `LockTag`, and an optional `Network`.
  - Staff: `[add ShardMoongate Red`. The art is reapplied from Color after a load.
- **Guild hall gates (P281's halls).** `[ShardGates guildhalls [dryrun] | clear | status` (Administrator). Nothing is
  placed until it is run.
  - It places a **White hub** at the League's headquarters, on its hall's Travel point (1362,1624,50 Trammel). Using the
    hub opens a list of every other hall (guild and town), and a pick sends you to that hall's Travel point.
  - It places a **Blue gate** at every other hall's Travel point, back to the headquarters.
  - Travellers arrive on the destination's gate, as on OSI's public moongates.
- **League hall gates:** the League's hall is the headquarters row of P281's table, so its gate is the White hub. The
  League trial gates are the Black keyed gates (section 3).
- **Eodon.** P198 left the Valley of Eodon gate on the stock look: a `PublicMoongate` at 719,1863,40 Ter Mur, 0xF6C,
  `EodonGeneration.cs`.
  - [GenEodon now places it with the **red** spinning art, keeping the PublicMoongate class.
  - An existing world keeps its stock gate until [GenEodon (or the console `eodon generate`) runs again.
- **Stock unchanged:** OSI's 0xF6C, 0xDDA and 0x1FD4 and their frames, pinned's Moongate and PublicMoongate, and every
  gate in the world keep their IDs. The package fact checks this.

## Tests

### Server facts

File: `server/tests/Misc/QuestMarkersKeysGatesVerification.cs`.

| Fact | Pins | Seen red (scratch copy, each its own break) |
|---|---|---|
| `AMarkerShowsForAnOfferedQuestAndSwitchesToReadyWhenItIs` | Rook: "!" to a participant, then "?" once every core station is done. The 0xC0 fixed effect on Rook, with the marker's ID, is in the trainee's send buffer only; the bystander's buffer is unchanged and shows nothing over Rook. The Registrar: "!" to an unregistered account. Setting off: nothing | red A, Rook always "!": `Assert.Contains() Failure: Item not found in collection` (line 152, the "?") |
| `AKeyOpensOnlyItsLock` | A boss door stays shut with no key, another lock's key, or a stock blank; opens for its own key (still locked behind, key kept). A consuming door takes its key. Staff pass. A tier-6 box: shut without a Vault key, opens with one, which it takes; tier 5 is a plain LootBox. A boss kill's Vault key below and at the chance | red B, any key opens any lock: `Assert.False() Failure` (line 207, the wrong key) |
| `EachGateColourPlacesAndTeleports` | Each colour: its own art in the block, never a stock moongate ID, its name, and UseGate moves the player to the target. Recolour follows the art. A trial gate passes only its chapter's key. The hub sends a traveller to another hall's Travel point and keeps no target | red C, the gate keeps 0xF6C: `Expected: 46598 Actual: 3948` (line 306) |

**Probes.** Run on the builder image `sl-uo-builder:cc-P291` (this branch's base), with the changed files bind-mounted
(no lock needed).
- Red: **3 failed, 0 passed**, each at the line above.
- Green: **3 of 3**.
- The related classes (LootBox, Eodon, Smith, Tutorial, League, Boss, GuildHall): 366 tests, 1 failed:
  `LeagueShopVerification.TheStockIsF13sStarterTableAndHandsOverNoMagicItem`, a null in stock
  `TreasuresOfTokuno.RewardEra`.
  - The same filter on the untouched image fails the same test, 1 of 363.
  - It is a filtered-run artefact, not this change; the full gate below decides.

### Package facts

File: `player-package/tests/Build-UoOverrides.Tests.ps1`.

**New fact `TheMarkerGateTokenAndKeyRecordsAreTheServersTableAndNoStockIdIsOverwritten`.** It checks:
- The C# table equals records.json: IDs in order, names, flags by value (named constants resolved), weight, height.
- The 6 animdata entries.
- Every non-base frame has no record.
- All 72 rows are registered once as art, with a PNG and the author's credit.
- **No stock ID is overwritten:** OSI's moongates (0xF6C-0xF70, 0xDDA-0xDDE, 0x1FD4-0x1FDE) and keys
  (0x100E-0x1013) have no PNG, registry row, record or animdata entry of ours.
- Every item-ID constant in ShardItemArt.cs lies in 0xB600-0xB647.

**Other changes in that file:**
- The ledger: 627 to **699 rows**, 570 to **642 art rows**.
- The records fact's carve-out gains 46592-46663.
- **The synthetic tiledata and animdata grow** from 900 groups and 28,800 entries to 1,460 groups and 46,720 entries,
  so the new IDs land inside the fixtures, as P265 did for its own.

**Runs:**

| Run | Result |
|---|---|
| Red, the tree at HEAD with the new test | 2 failed: the new fact ("Could not find file ...ShardItemArt.cs") and the ledger |
| Red, mutation (a PNG named 3948.png, stock 0xF6C) | 2 failed: "no PNG overrides stock 0xF6C", and the PNG count |
| Green | **23 of 23** |

**Found on the way: `Cliloc-Overrides.Tests.ps1` was already red at HEAD.**
- The failing fact: `AMissingClilocIsOneYellowLineAndTheArtStillShips`.
- The cause: its synthetic tiledata (500 groups) is too small for P265's guild hall decor (28016-), and now for ours.
- The fix: grown the same way (1,460 groups, 46,720 animdata entries).
- Before: 9 of 10 at HEAD and on this branch. After: **10 of 10**.

### Full gate

The gated build (`docker\uo\build.sh -t sl-modernuo:cc-P363`) ran detached, under the docker-build lock (22:40-23:35
CDT).
- Free memory before the first cycle: 12.3 GB; the VM had 13.1 GB free, so no page cache drop was needed.
- Logs: `gate1.log` to `gate4.log` in the session scratchpad.

| Cycle | Result |
|---|---|
| 1 | 2,246 tests, 1 failed: `CommandDeclarationVerification.EveryCommandWeRegisterDeclaresACategory`. My new `[ShardGates` had no `[ShardCommand]`; one was added (WorldSetup, Replaces, TestFirst) |
| 2 | 1 failed: the same class's dry-run fact. The declared DryRun must be one word of the usage line that the class reads ("dryrun"); fixed |
| 3 | 1 failed: `CreatureLevelsVerification.BelowPinnedsCapTheUncappedDifficultyIsPinnedsExactly` ("TheButcher: uncapped 159.2 under pinned's cap 160"). A random stat roll on a creature this branch does not touch; it passed in cycles 1 and 2. Rerun unchanged |
| 4 | **green: 2,246 tests, 2,242 passed, 4 skipped, 0 failed**; image `sl-modernuo:cc-P363` (cd5e7f579bee) built. It carries VERSION 2026.10.23.7 and the new CHANGELOG section (read back from the container) |

The creature-level fact is flaky and worth a look of its own: a random roll can land TheButcher just under the cap, and
the fact then fails.

## Website credits

For the shard credits list (each author's terms, as in SOURCE.txt):

- **Quest markers by RedRooster (Steven Armstrong)**, "Quest Markers",
  https://www.servuo.dev/archive/quest-markers.1823/. He asks to be listed in shard credits.
- **Keys and gem tokens by Hestia**, "Quest, Item, Token Keys",
  https://www.servuo.dev/archive/quest-item-token-keys.1809/ ("use however you want, drops, gate keys, items keys").
- **Spinning moongates by Carl Hamilton**, "NEW Blue / Red / Black / White Spinning Moongate", servuo.dev 2309, 2310,
  2312, 2313.

None states a license beyond Hestia's line. Each is treated as community work: credit the author, ship only inside the
player package or the private repo, do not repost.

There is no credits list in either repo. Earlier prompts (P243, P265) put the lines here and in the CHANGELOG's Staff
list, and so does this one.

## Decisions and deviations for Chase

1. **Tier-6 loot boxes now come locked by default** (`clusterf.lootBoxes.keyTier` 6), and Vault keys come only from
   boss kills (25% a kill).
   - A player who earns a tier-6 box (top League ranks, trial chapters, reaching 200) needs a boss kill before opening
     it.
   - Set the key tier to 0 to turn locked boxes off, or raise the chance.
   - The prompt asked for a tier's key-to-open; the tier and the source of keys are my proposal.
2. **The marker height (92 px) is a guess** from TazUO's draw code, not seen in a client. If the "!" sits in the head
   or too high, the pad is one number in `p363_art.py` (re-run `png`).
3. **Markers are an effect re-sent every 3 s**, not an item. Cost: one 36-byte packet per marked NPC per nearby player
   per pulse.
4. **No trial-NPC "?"**: no trial has a report-back step. **No League quest-giver markers** beyond the Registrar: none
   exists.
5. **The League trial gate and boss room door are not placed anywhere.** Neither a League trial area nor a boss room
   door exists to put them on. They are ready for staff ([add) and for code.
6. **The gate network is placed only by command**, on each hall's P281 Travel point. Some Travel points are at a door
   ("the keep's east door"), so a gate may stand in a doorway. Staff can move one with [props after placing.
7. **The Eodon gate keeps its stock look in the current world** until [GenEodon runs again (it deletes and re-places
   its own objects).
8. **A client without the package update** draws OSI's "UNUSED" placeholder for every new ID, the Eodon gate included
   once it is regenerated.
9. **Merge note:**
   - This branch bumps VERSION to 2026.10.23.7 and the ledger to 699 rows and 642 art rows.
   - P362 (unmerged) adds registry rows of its own (13049-23080), so the integrator adds the two counts.
   - Both this branch and P265 grew the synthetic fixtures; there is no other fixture conflict.

## For Chase

1. **Rebuild** the test shard from `sl-modernuo:cc-P363`, build the player package, and update a test client.
2. **Markers.** On a fresh character in the tutorial, stand near Rook: a gold "!" should bob above his head. Does it
   clear the head (Decisions 2)?
   - Finish the core lessons: it turns to "?".
   - Unregistered, visit Elara Voss: "!".
   - Join the Society of Smiths: "!" over the smith guildmaster; fill a BOD: "?".
   - A second character beside you sees only their own.
3. **Gates.** Run `[add ShardMoongate Blue` (then Red, Black, White). Each spins and takes you to its `Target`
   ([props).
   - Run `[ShardGates guildhalls dryrun`, then `[ShardGates guildhalls`, and use the white hub at Castle British.
4. **Keys.**
   - Run `[add ShardLockedDoor WestCW "boss.test" "the test key"` and `[add ShardKey "boss.test" "the test key" 12`.
     The door opens only with that key.
   - Run `[LootBox give Boss 6`: the box says Locked; kill a boss (or `[add ShardKey "lootbox.vault" "a Vault key" 14`)
     and open it.
5. **Eodon:** `[GenEodon` re-places the valley's gate in red.
6. **Credits:** add the three "Website credits" lines.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun -NoRefresh -NoArchive
-CodeRepo D:\UO\golems\Iron\ShatteredLegacy -DocsRepo D:\UO\golems\Iron\shard-migration -Branch golem/Iron/P363`.

| Repo | Pending | What | Blocked |
|---|---|---|---|
| Code | 88 files | 11 changed, 72 PNGs, 4 new .cs files and the new test | no |
| Docs | 2 files | this note and `cc-P363-tools/p363_art.py` | no |

The 72 PNGs total 328 KB; nothing is near 5 MB.

```
Repo Result
---- ------
code dry run
docs dry run
```

P363 DONE
