# cc-P365: reward mounts and the evo pets' young stages from art on disk

## In plain words

- **Eighteen new mounts.** Players earn each one as a statuette that calls the mount, bonded and ready to ride:
  - six in the League shop at 1,750 AP;
  - four as achievement rewards;
  - eight in the top-tier Tamer and Boss loot boxes.

  They stable, shrink and take one follower slot like any other mount.
- **Evo pets.** Two new lines:
  - **Horse:** foal, then horse, then draft horse, then warhorse, then a unicorn, emberhoof or bonewalker.
  - **Lizard:** hatchling, then ostard, then raptor, then bog strider.

  The evo dog's last stage now offers the new great grey wolf, with the windrunner kept as the other choice. The calves
  have no line yet.
- **The player package grows** by about 29 MB of animation data, about 18 MB to download. Without the update the new
  creatures do not draw.
- **For you:**
  - Rebuild the test shard from `sl-modernuo:cc-P365`, build the player package and ride a few (For Chase below).
  - Every route and price is a proposal you can move (the table below).
  - Add Thagoras and Rafael Costa, Krazy Zacks, Prapilk and Socrarr to the shard credits.

2026-10-23, the Iron Golem (Opus), branch golem/Iron/P365 of both repos. Prompt: `cc-P365-reward-mounts-and-evo-stages.md`.
Not committed (the Golem commits after DONE). Nothing was run against any world, nothing was deployed, and the package
was not built or published.

## The mounts

All IDs are new. Bodies 2088-2133 are past the client's 1973; mount items 46672-46689 (0xB650-0xB661) sit after P363's
block.

| Name in game | Source (author: file) | Walks on body | Ridden look (mount item's Animation) | Mount item | Reward route |
|---|---|---|---|---|---|
| a marsh raptor | Thagoras: Dino Raptor 01 | 2088 | 2088 | 46672 (0xB650) | Boss box, tier 6 |
| a dusk raptor | Thagoras: Dino Raptor 02 | 2089 | 2089 | 46673 (0xB651) | Boss box, tier 6 |
| a sky raptor | Thagoras: Dino Raptor 03 | 2090 | 2090 | 46674 (0xB652) | Boss box, tier 6 |
| a chestnut draft horse | Thagoras: Horse 01 + Horse 01 Saddle | 2091 | 2104 | 46675 (0xB653) | League shop, 1750 AP, 750 Renown |
| a bay draft horse | Thagoras: Horse 02 + Horse 02 Saddle | 2092 | 2105 | 46676 (0xB654) | League shop, 1750 AP, 750 Renown |
| a grey draft horse | Thagoras: Horse 03 + Horse 03 Saddle | 2093 | 2106 | 46677 (0xB655) | League shop, 1750 AP, 750 Renown |
| a palomino draft horse | Thagoras: Horse 04 + Horse 04 Saddle | 2094 | 2108 | 46678 (0xB656) | League shop, 1750 AP, 750 Renown |
| a barded warhorse | Thagoras: Horse 05 Saddle | 2095 | 2095 | 46679 (0xB657) | League shop, 1750 AP, 1000 Renown |
| a gilded charger | Thagoras: Horse 06 Saddle | 2096 | 2096 | 46680 (0xB658) | League shop, 1750 AP, 1500 Renown |
| a moonlit unicorn | Thagoras: Horse Unicorn 1 | 2097 | 2097 | 46681 (0xB659) | achievement `exploration.all_facets` (visit all five facets) |
| a bonewalker steed | Thagoras: L_Horse Death Mount | 2098 | 2098 | 46682 (0xB65A) | achievement `combat.undead_hunter` (50 undead) |
| an emberhoof | Thagoras: L_Horse Nightmare | 2099 | 2099 | 46683 (0xB65B) | achievement `combat.ten_thousand` (10,000 kills) |
| a bog strider | Thagoras: L_Swamp Lizard | 2100 | 2100 | 46684 (0xB65C) | Boss box, tier 6 |
| a war wolf | Thagoras: Warg1 | 2102 | 2102 | 46685 (0xB65D) | achievement `league.ap_500` (500 AP) |
| a riding drake | Krazy Zacks: P_01 (unmodified) | stock drake 0x3C | 2109 | 46686 (0xB65E) | Tamer box, tier 5-6 |
| a riding bear | Krazy Zacks: P_02 (unmodified) | stock polar bear 0xD5 | 2110 | 46687 (0xB65F) | Tamer box, tier 5-6 |
| a riding wolf | Prapilk: prapilk_reitwolf P_01 | stock timber wolf 0xE1 | 2111 | 46688 (0xB660) | Tamer box, tier 5-6 |
| a saddled horse | Socrarr: P_pferdesattel | stock horse 0xC8 | 2112 | 46689 (0xB661) | Tamer box, tier 5-6 |

Every Thagoras creature is renamed: the pack is likely ripped from World of Warcraft (his words), so no Blizzard names
are used.

**Box chances** (settings):
- `clusterf.rewardMounts.tamerBoxChance`: 0.10 for each tier above 4, so 10% at tier 5 and 20% at tier 6.
- `clusterf.rewardMounts.bossBoxChance`: 0.15 at tier 6.

### The evo stages

| Line | Stage | Bodies (picks) | Source |
|---|---|---|---|
| Dog | 5 "great wolf" | **2133 great grey wolf** (default), 1410 windrunner | Prapilk, KR Wolf (`kr-wolf`), as its SOURCE.txt names it |
| Horse (new) | 1 foal | 2113, 2114, 2115, 2118 | Prapilk, colts L_01-L_04 |
| | 2 yearling | stock horses 200, 226, 228, 204 | client |
| | 3 draft horse | 2091-2094 | Thagoras |
| | 4 warhorse (loop 1) | 2095, 2096 | Thagoras |
| | 5 legend (loop 5, Bond Trial) | 2097 unicorn, 2099 emberhoof, 2098 bonewalker | Thagoras |
| Lizard (new) | 1 hatchling | 2119, 2125, 2126 | Prapilk, young lizards L_01-L_03 |
| | 2 runner | stock ostards 210, 219, 218 | client |
| | 3 raptor (loop 1) | 2088, 2089, 2090 | Thagoras |
| | 4 bog strider (loop 5, Bond Trial) | 2100 | Thagoras |

**Gaps that remain** (the art library's Gaps line): puppy, kitten, fox kit and chick. None of the art on disk fills
them.

**Calves:** Prapilk's four calves (2129-2132) are registered and encoded, but no evo line or companion fits a calf.
- P264's companions are human-bodied.
- The tutorial farm's animals are not evo pets.

They wait for a line (a farm line, say).

## 1. Registration

Read first:
- `ART-LIBRARY.md` section 3 and its Gaps line;
- the three folders' `SOURCE.txt`;
- the registry rules;
- P277's notes (the pattern: body + mount item whose tiledata Animation names the body);
- the evo code (EvoPetData, EvoPet, ShardBodyTypes).

**How the files were handled:**
- The `.vd` files were **copied to the session scratchpad first** and registered from the copy. The tool is
  `notes\cc-P365-tools\p365_art.py` (`check`, `copy`, `registry`, `records`, `icons`).
- Each `.vd` is in the repo byte for byte as `anim-src\bodies\<body>.vd`. Its SHA-256 is in its registry row.

**Slots:** `validate-art.py propose` on the 34 files in order.
- Low layout: ANIMAL, anim7 slots 209-238.
- People layout: HUMAN, slots 401-404.
- Its body numbers skip the ones the client's data names (2101, 2103, 2107, 2116-2117, 2120-2124, 2127-2128).

**Encoding:** `build-equip-anims.py`, then `--check`:
- "anim7 matches";
- each new body "every block the .vd's bytes and every pixel identical";
- `sl-anim7.bin` grows from 51.9 MB to 80.8 MB (git-ignored build output).

**Mount items:**
- Tiledata on the Mount layer (25), Wearable 0x00400000, weight 255, the Animation set to the ridden body (as P277).
- The icons are the ridden look's stand frame (action 2, or 4 for the people layout, direction 2), scaled to 44 px.

**Checks:**
- `validate-art.py check-registry`: **0 of 772 rows have problems.**
- `find-free-art.py --check-registry`: **0 of 772 registered IDs are no longer free.**

**Credits:** `SOURCE.txt` has a new section.

**What each pack turned out to hold** (rendered and looked at):
- **Thagoras' "Horse 0n Saddle" files** (four of them) are the same horse saddled, with only walk, run, stand and eat.
  - Those are exactly what a mount under a rider plays.
  - So each plain horse is the creature on the ground, and its saddled file is the ridden look.
- **The four people-layout files** (Krazy Zacks' drake and bear, Prapilk's riding wolf, Socrarr's saddled horse) hold
  the **whole animal** in the rider's mounted actions 23-29.
  - TazUO draws a people-typed mount with the rider's mounted groups (`MobileAnimation.GetGroupForAnimation`).
  - So they work as a ridden look named by a mount item, **unmodified**.
  - The creature walks on the matching stock body, as Krazy Zacks' own mod did.
  - **Krazy Zacks' "Do not modify"** is kept: his two files ship byte for byte, with no recolour, resize or frame
    change. A package fact checks their SHA-256 against the registry.
  - His `Patch.exe` and `AVATAR.EXE` were never extracted or run.
- **Skipped:**
  - **Arx's goliath beetle:** its stand frame is about 35 px, so a rider would dwarf it, and resizing is not ours to do
    here.
  - **The leopard and the griffon small animals:** not part of this prompt.

## 2. Server

- **`Mobiles\Mounts\RewardMounts.cs` (new):**
  - `RewardMounts.Defs` is the table above (key, name, body, mount item, ridden body, sound, route, mount type).
  - `RewardMount : BaseMount` and its 18 classes are `[Constructible(AccessLevel.GameMaster)]`. They take a horse's
    numbers (P277's placeholder), are never tamable and take one control slot.
  - `SummonFor` follows PackMule's steps: it checks the follower slot, then `SetControlMaster`, bonded, following.
  - `ShopRows` and `LootBoxMount` are the routes.
- **`Mobiles\Mounts\RewardMountStatuette.cs` (new):**
  - A blessed statuette drawn with the mount item's icon, weight 1. It is never equipped: its art's tiledata is on the
    Mount layer.
  - Double-click in the pack calls the mount and uses the statuette up.
  - Four subclasses exist for the achievement routes, because an achievement's reward is a type.
- **The League shop:** a new kind `Mount` and six rows at 1750 AP, appended through `RewardMounts.ShopRows()`. They sit
  past the Gold box's 1000 AP, so the League boxes never draw one.
- **The loot boxes:** `LootBoxRoller.ThemeSlot`, the Tamer and Boss cases.
- **Achievements:** `rewardItems` on the four achievements.
- **Evo:**
  - `EvoPetData` gains the Horse and Lizard lines and the dog's stage-5 pick. The stage-5 change means the owner now
    picks at stage 5, as at stage 3.
  - `EvoPet` updates its error text.
  - `ShardBodyTypes` adds the 34 bodies: Animal, and Human for the four people-layout looks, which are never a mobile's
    body.
- **Part 3, the shard's systems:**
  - Shrink (`ShrunkPet`): no lookup by body, so nothing to add.
  - Stable: pinned `AnimalTrainer.EndStable`. It refuses only human bodies; none of these is one.
  - Follower slots: `ControlSlots` 1.
  - Pet training: not tamable, so no training row.
  - All of these are exercised by the server facts.

## Tests

### Server facts

New file `server\tests\Mobiles\Mounts\RewardMountVerification.cs`, 3 facts with 18 cases on the first.

| Fact | Pins | Seen red (scratch copy, its own break) |
|---|---|---|
| `EachMountIsCalledMountedDismountedStabledAndShrunk` (18 cases) | The statuette calls it, bonded, one slot. It walks on its body (animal, or the stock drake's monster body). The owner rides it: the mount item on the Mount layer, the mount off the map. It dismounts back at the rider. It shrinks and comes back (followers 0, then 1). An animal trainer stables it (`EndStable`, 30 gold). It round-trips the serializer | red A, the mount item replaced by the stock horse's: 18 cases fail, `Expected: 46683 Actual: 16032` |
| `EachEvoStageChangeShowsItsBody` | Every body of the horse and lizard lines through `StaffSetStage`, each an Animal. The dog's top stage is 2133 by default and 1410 as the pick | red B, the dog's bodies reversed: `Expected: 2133 Actual: 1410` |
| `EveryMountHasItsRoute` | Six shop rows at 1750 AP, past the Gold box, each handing over its statuette. The four achievements' reward types make their mounts' statuettes. Tamer and Boss pools are exact; nothing below the tier, in another theme, or above the chance | red C, a Tamer box of any tier always holds a mount: `Assert.Null() Failure` (line 241) |

Existing facts updated for this change:
- `EvoPetVerification`: six lines; the dog's stage 5; the classic body list gains the stock horses and ostards, and our
  anim7 bodies (2048 up) use classic animal actions, so they are not remapped; the dog's walk now picks at stage 5.
- `LeagueShopVerification`: the starter table gains the six mount rows.
- `TutorialFarmVerification.TheEvoDogAndCatStagesAreChasesPicks`: the dog's stage 5 is {2133, 1410}.

**Probes** (`sl-uo-builder:cc-P291` with the changed files mounted):
- red: 19 of 20 failed (A and B), then the route fact red under C;
- green: 40 of 42 in the three classes.
- The 2 that failed in the probe also fail on the untouched image with the same filter (1 of 22 shown there):
  `LeagueShopVerification`'s Tokuno null and an `EvoPetVerification` password-setting fact. Both are filtered-run
  artefacts, and both pass in the full gate.

### Package facts

File: `player-package\tests\Build-UoOverrides.Tests.ps1`.

**New fact `TheRewardMountsAndEvoStagesAreTheServersAndNoStockBodyOrIdIsOverwritten`.** It checks:
- The C# table's 18 rows: the mount items consecutive, the routes 6/4/8.
- Each mount item has one record on the Mount layer, Wearable, naming its ridden body, registered with its PNG.
- Each ridden body is registered with one bodyAnims entry: ANIMAL in an animal slot, or HUMAN in a people slot with the
  creature on a stock body that stays the client's.
- Every evo body of ours is registered as ANIMAL.
- **No stock ID is overwritten:** no record or PNG on OSI's mount items 0x3E90-0x3EFF, and no bodyAnims entry on the four
  stock bodies.
- The 52 P365 rows: no body is a stock body, and every art ID is in the block.
- Krazy Zacks' two files are his bytes (SHA-256) and carry his rule.

The existing `NoRegisteredCreatureBodyIsAStockBodyAndNoTwoShareASlot` covers all 74 bodies.

**Other changes in that file:**
- The ledger: 720 to **772 rows**, 40 to **74 bodies**, 634 to **652 art**.
- The records fact's carve-out gains 46672-46689.
- The synthetic tiledata and animdata grow to 1,460 groups and 46,720 entries, so 46672-46689 land inside them. This is
  P363's exact change, and the two merge as one hunk.
- `Cliloc-Overrides.Tests.ps1` gets P363's same fixture fix: it was red at the base, skipping P265's IDs.

**Runs:**

| Run | Result |
|---|---|
| Red, HEAD with the new tests | 2 failed: the ledger "expected [772] but got [720]", and the new fact (no RewardMounts.cs) |
| Red, mutation (mount item 46686 naming stock body 60) | "expected [2109] but got [60]" |
| Green | **23 of 23**; `Cliloc-Overrides` **10 of 10**; `scripts\tests` **58 OK** |

### Full gate

`docker\uo\build.sh -t sl-modernuo:cc-P365`, run detached, under the docker-build lock. Free memory was 12.4 GB, so no
cache drop was needed.

| Cycle | Result |
|---|---|
| 1 | 2,263 tests, 1 failed: `TutorialFarmVerification.TheEvoDogAndCatStagesAreChasesPicks`, which pins F-35's dog bodies. It was updated for this prompt's top stage; see Decisions 2 |
| 2 | **green: 2,263 tests, 2,259 passed, 4 skipped, 0 failed**; image `sl-modernuo:cc-P365` (b3a6711c1fbd) built. It carries VERSION 2026.10.23.9 and the new CHANGELOG section (read back from the container) |

## Credits (for the shard credits list)

- **Thagoras** and **Rafael Costa (UoBrazilian)**, "Mount Pack", https://www.servuo.dev/archive/mount-pack.1979/. The
  creatures are renamed; likely ripped from World of Warcraft.
- **Krazy Zacks**, "Mountable drake and Bear", uo-pixel.de. Shipped unmodified, as his readme asks.
- **Prapilk**:
  - "KR Wolf", https://www.servuo.dev/archive/kr-wolf.1717/;
  - on uo-pixel.de, the riding wolf, colts (foals), Echsen (young lizards) and Rindviehcher (calves).
- **Socrarr**, "Pferdesattel" (the saddled horse), uo-pixel.de.

These are in `SOURCE.txt` and the CHANGELOG's Staff list. Neither repo has a credits file; P243 and P265 did the same.

## Decisions and deviations for Chase

1. **The routes and prices are proposals:** the table above. They are each one line in `RewardMounts.Defs` (plus the
   achievement line).
   - The four achievements were picked for fit: undead for the bonewalker, facets for the unicorn, a big kill count for
     the emberhoof, AP for the war wolf.
   - The war wolf first went on `league.veteran`, which is 10 logins; I moved it to 500 AP as too cheap for a mount.
2. **The evo dog's stage 5 is now a pick:** the KR Wolf (default), or the windrunner.
   - F-35's picks had the windrunner alone, and `TutorialFarmVerification` pinned that. This prompt asks for the KR Wolf
     there, so the pin is updated.
   - The owner must now pick at stage 5, as at stage 3.
   - Pets already at stage 5 with no pick take Bodies[0], the KR Wolf, on their next stage change. Say if existing
     windrunners should keep theirs, and I'll record their pick.
3. **Two new evo lines (Horse, Lizard)** are not offered in the tutorial pick (`StarterPetLines` is unchanged).
   - Their stats use the shared curve.
   - Their statues are the horse 0x2121 and lizard 0x2131 figurines.
4. **The stats:** every mount is a stock horse for now (P277's placeholder).
5. **Skipped:**
   - the goliath beetle (too small to ride);
   - Thagoras' saddle files as creatures (they are ridden looks);
   - the leopard (not in this task).
6. **Calves are registered with no line.** Packaging them costs about 1.3 MB of anim7. If you'd rather not ship unused
   art, they can come out of the registry.
7. **The package and repo grow:**
   - `sl-anim7.bin` grows by 28.9 MB (about 18 MB in the zip, estimated from P277's ratio).
   - The repo grows by 28 MB of `.vd` files. The largest is the bog strider at 2.3 MB; none is near 5 MB.
8. **Not seen in a client.** The ridden people-layout looks (drake, bear, riding wolf, saddled horse) follow TazUO's code
   path, but nobody has ridden one yet. If one draws wrong when ridden, its mount item can point at a plain body
   instead. The rider's seat height has P277's open question (TazUO's default offset for an unknown mount).

## For Chase

1. **Rebuild** the test shard from `sl-modernuo:cc-P365`, build the player package, and update a test client.
2. **Ride them.** Run `[add RewardMarshRaptor` (or any `Reward*` class).
   - As staff it rides at once. A player gets it through `[add RewardMountStatuette "marsh-raptor"`, then double-clicks
     the statuette.
   - Check the people-layout four especially: `riding-drake`, `riding-bear`, `riding-wolf`, `saddled-horse`. Do they
     draw under the rider?
3. **Evo:** `[EvoPet` gives a horse or lizard line pet (keys `horse`, `lizard`). Staff stage it up with the evo
   commands and look at each body.
4. **Credits:** add the four credit lines.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun -NoRefresh -NoArchive
-CodeRepo D:\UO\golems\Iron\ShatteredLegacy -DocsRepo D:\UO\golems\Iron\shard-migration -Branch golem/Iron/P365`.

| Repo | Pending | What | Blocked |
|---|---|---|---|
| Code | 71 files | 16 changed; 55 new: 34 `.vd`, 18 icons, 3 `.cs` | no |
| Docs | 2 | this note and `cc-P365-tools\p365_art.py` | no |

Neither repo got a file near 5 MB (the largest new file is 2.3 MB). The red dragon's `2086.vd`, which the encoder
fetched, stays git-ignored. Nothing under `docs\` was edited.

P365 DONE
