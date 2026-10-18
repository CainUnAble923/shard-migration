# cc-P141: Rootdeep Burrows 3 of 3: the Vault and the layout spec for the map batch

2026-10-18. Prompt: `D:\UO\cc-prompts\cc-P141-rootdeep-burrows-vault-layout.md` (Part D of the features chat's
`cc-P-rootdeep-burrows-creatures.md`, with the overseer's 10-17 16:20 mockup change). P140 is DONE and committed (its
notes end `P140 DONE`; code `73a0348`, docs `4197f6b`). Both repos were clean at the start. Model: Opus. Not
committed. Scratch: `D:\UO\cc-p139-work\` (the build and bot logs, `cc-p141-*.log`) and the session scratchpad (the
clean copies and green hashes).

## Headlines

1. **The Vault exists in code** (`server\customizations\Regions\RootdeepVault.cs`): a child region of the Burrows over
   x 5142-5178, y 1132-1159. Only a tutorial participant (and their pet) can walk in from the landing; a graduate, a
   skipper or anyone else is turned back with an Echo line, and teleport in is refused. When the Overdraft dies, every
   participant who damaged it (or whose pet did) is credited, the cave-in in the Strongroom's south wall opens for two
   minutes, and a credited player who steps on it lands in the Warren with their pet. The doorway then refuses them
   (the Vault seals behind them), and a player who logs in inside without the right to be there wakes on the landing.
2. **The landing ankh and every spawner are data in a seeder** (`ClusterFRootdeepSeeder.cs`, `[ClusterFSeedRootdeep
   [dryrun | force]`): 33 stock spawners, P137's working `AnkhWest` placed P137's way, and the crawlway item. It refuses
   while the landing is still void land, so the map batch runs it once the floors exist. Nothing is placed today.
3. **The layout spec and the mockup are ready for Chase:** `notes\art\rootdeep-mockup\index.html` with `layout.png`
   (the rectangle to scale, one cell per tile, over a vseUOAware radar export), every zone and room, the walls, the
   doorway, the one-way crawlway, the ankh, the decoy chests, every spawner with its creatures and pack size, and the
   Overdraft's fight space with its two kite loops. Look swatches per zone (19 stock sets and third-party kits, flags
   beside each). **The page asks Chase to approve the layout and look or say what to change; the map batch waits on
   it** (P141-1).
4. **The enlarged Vault fits the fight.** The Strongroom alone is 37 x 16 tiles (556 walkable after two 3 x 6 pillars);
   each pillar loop is 22 tiles round, the decoy chests sit a room away. No more room is needed (section 3).
5. **A finding against the prompt's premise:** a Young player who dies in the Burrows is not sent to the region's
   Entrance. Pinned sends the ghost to the death destination nearest the Entrance (PlayerMobile.cs:2563 and 4065-4128
   at d4531cd9), which is New Haven's 3665,2587, about 57 tiles from the Old Haven hole. So the landing ankh serves
   ghosts that are not Young (graduates' groups), and a Young trainee who dies in the Vault wakes by New Haven's healer
   and walks back for the corpse. Kept as pinned does it; a decision for Chase (P141-5).
6. **Facts:** 6 new shard facts, each seen red under its own break (section 6); the full build green at **1,430 tests,
   1,426 passed, 0 failed, 4 skipped**; image `sl-modernuo:cc-P141` = `e89d95c8ad61`; `sl-modernuo:latest` still
   `8e1a1916a752`. The scratch test shard booted clean twice on the image (the bot's runner, rule 1 held). One
   pre-existing test is flaky and not mine: `RaisedGardenVerification.AMoundGrowsWithoutWaterOrMaladies` (P128) failed
   3 of 7 builds on pinned's random growth roll (section 6).
7. **I broke tonight's nightly bot run:** my second boot check (01:40) used the same scratch shard and tore it down
   under the scheduled run that started at 01:30; its checks from 01:43 read connection errors. It needs a re-run
   (section 6).

---

## 0. Before starting

- `git --no-optional-locks status --short`: both repos clean (ShatteredLegacy `73a0348`, shard-migration `4197f6b`).
- P134 is DONE, but this prompt makes **no art slot decision** (no body, item or gump is registered: the crawlway and
  ankh are stock graphics, the creatures are P140's), so `validate-art.py` had nothing to check. No third-party pack
  was registered, so no `SOURCE.txt` flag line changed.
- Read: P24 (sections 4 and 6), P36 (the region), P80 (A.6, `TutorialCreature`), the 10-14 tutorial decisions (the
  "System:" voice is the Echo, item 3), F-32/F-35/F-45/F-46, P50, P137 (the ankh method), P139 and P140 (bodies and
  creatures, as built), P134 (vseUOAware, its fixed UOP map reader), the original draft's lineup and Part D.

## 1. Part D.1: the Vault sub-region (as built)

`RootdeepVaultRegion : BaseRegion`, parent `OldHavenBurrowsRegion`, priority 51, `Initialize` registers the parent
first (idempotent), so the order the two `Initialize` methods run in does not matter.

| Rule | How (pinned file:line at d4531cd9) |
|---|---|
| Everything the Burrows does still holds inside | A child region hands each hook to its parent: `AllowHarmful` (the 3-hostile Young limit), `OnDeath`, light, housing (Region.cs:793-874), `CheckTravel` (BaseRegion.cs:171-180, so recall and gate stay refused); `GetRegion<DungeonRegion>` walks to the parent (Region.cs:458-470), so the Young death teleport finds the Burrows' Entrance |
| Walking in: participants and their pets only | `OnMoveInto`, asked of the region being entered on every step (Region.CanMove, Region.cs:887-900, from Mobile.cs:4164). A pet counts as its master (`ClusterFTutorial.IsParticipant`). Wild creatures keep the base walk rule |
| The refusal lines (the Echo, "System:") | non-participant: "The Vault is for the League's trainees. You are not one. The door has excellent judgement."; graduate: "You graduated. The Vault does not do reunions."; sealed: "The Vault sealed behind you. Nothing in there owes you anything now." |
| Teleport in | refused from outside the Vault for everyone below staff ("The Vault's walls are thicker than your spell."); the doorway is the way in |
| The Overdraft's death | `TheOverdraft.OnDeath` calls `RootdeepVault.OnOverdraftDeath` **before** `base.OnDeath`, because pinned deletes a dead creature there (Mobile.OnDeath, Mobile.cs:4900-4904) and its map with it (my first green run found this). Every participant in its `DamageEntries` (a pet credits its master) gets the key `burrows.vault` in `TutorialRecord.StationsDone` and the line "Something gave way in the south wall. A crawlway. One way, I am told. Do not get sentimental about the Vault." |
| The crawlway | `RootdeepCrawlway`: rocks 0x1367 (tiledata Impassable, so nothing steps on it shut), an open hole 0x1B71 for `CrawlwayOpenFor` (2 minutes) after the death, with a sound and dust. Stepping on it (or double-clicking it) moves a credited, living player and their following pets to the Warren side (5160,1163), as pinned's Teleporter does (Teleporter.cs:258-267), with "You squeeze through the crawlway. Behind you the earth settles. The Vault is sealed." An uncredited player is told "That crawlway opened for whoever fought the Overdraft. That was not you." The open state is a runtime field, never saved: a restart closes it |
| One way | the crawlway has one mouth, inside the Vault; the Warren side is solid wall in the layout |
| Sealed, graduates out | `MayEnter` refuses a credited player and anyone not a participant (a graduate is not: `IsActive` is false) |
| Login inside | `[OnEvent(PlayerLoginEvent)]` puts a player who may not be there on the landing (5182,1137) with their pets: "You wake on the landing. The Vault is not for you any more." |
| Staff | exempt from every refusal |

**Why the credit is a key in `StationsDone`:** it is the account's saved set of strings (ClusterFAccountData.cs:1173,
TutorialRecord v0), so no schema change; `CoreDone` counts only core station keys (ClusterFTutorial.cs:96-104), so the
key changes nothing else, and `[Tutorial reset` clears it with the record. The Vault is not a tutorial station (P80 has
no Vault row); when the trial prompts make it one, the key can become that station's key.

**Two tutorial players at once (no instancing): what breaks.**
- They share every spawn. One can clear the bats, rats or chests the other needed; group spawners respawn only once the
  room is clear (1 to 3 minutes), so the second waits.
- The Overdraft: everyone who damaged it is credited, so two who fight it together both pass. One who did not hit it
  cannot use the crawlway (the Echo says so) and waits for the respawn (3 to 4 minutes), or walks out by the doorway.
- **The looting lesson can fail for the second player:** the Overdraft's corpse follows pinned's looting rights (top
  damagers, BaseCreature.GetLootingRights), so the one who did less may not be allowed to loot its fixed drop. A fix
  (a drop per credited player) is a decision, not done (Decisions, item 4).
- The open crawlway looks open to both; only the credited pass.
- The Young limit is per player (3 hostiles each), so two trainees can pull six.
- A trainee's corpse in the Vault is theirs alone (Trammel), as anywhere.
- A graduate cannot help: tutorial creatures ignore non-participants' damage (P80) and the doorway refuses them.

## 2. Part D.2: resurrection at the landing

- **What pinned does** (the finding in headline 5): a Young ghost goes to the Trammel death destination nearest the
  region's Entrance (`m_TrammelDeathDestinations`, PlayerMobile.cs:104-121; `YoungDeathTeleport`, :4065-4128, called
  from :2563). The Entrance is Old Haven's hole 3619,2620 (P36, provisional), so that is New Haven's 3665,2587. The
  Burrows' Entrance was not changed: pointing it at the landing would send Young ghosts to whatever death destination
  is nearest x 5193, far away.
- **The landing ankh:** P137's working `AnkhWest` (header `AnkhWest 0x0003`), built by pinned's `DecorationList`
  through `ClusterFNewHavenServicesSeeder.DecorEntry(...).Read().Generate`, exactly as `ClusterFAnkhs.Seed` places its
  ankhs, at **5206,1136** (its foot at 5206,1137) against the landing's east wall, facing the arrival. Idempotent
  through `ClusterFAnkhs.WorkingAnkhNear` (2 tiles). Placed by `[ClusterFSeedRootdeep`, not map art.
- No wandering healer: the ankh is enough on the landing, and a healer NPC would be a spawn on the safe tile.

## 3. Part D.3: the layout spec for the map batch

Authority: `notes\art\rootdeep-mockup\layout.json` (floors and solid blocks, inclusive tiles) plus the seeder
(spawners, arrival, ankh) and `RootdeepVault.cs` (doorway, crawlway). The mockup is drawn from exactly these.
`build_mockup.py` checks the spec before it draws: every floor and wall inside x 5136-5247, y 1128-1263 and east of
x 5140, every spawner, the arrival, the ankh and both crawlway ends on a floor of the right zone, the doorway joining
the Vault to the landing, and every spawner's home range reachable inside its room (a range that crosses a wall would
spawn into the next room; that check was seen red on two of my first ranges, which were tightened). It reads
"problems: none".

**Zones** (Chase's approved draft, unchanged; depth and tier rise to the south):

| Zone | Tiles | Tier | Rooms |
|---|---|---|---|
| The Landing | x 5180-5206, y 1132-1144 | safe | the arrival (5193,1138) from the B1 hole; the ankh; the Vault doorway in the west wall (x 5179, y 1137-1138); a 4-wide tunnel south x 5192-5195, y 1145-1161 into the Warren |
| The Vault | x 5142-5178, y 1132-1159 | tutorial | Counting Room x 5170-5178, y 1132-1142 (bats); The Stacks x 5156-5168, y 1132-1142, three 3-tile aisles between two shelf rows (y 1135 x 5156-5166, y 1139 x 5158-5168), a serpentine (rats); Deposit Hall x 5142-5154, y 1132-1142 (three decoy chests); Strongroom x 5142-5178, y 1144-1159 (the Overdraft). Gaps: x 5169 y 1140-1141, x 5155 y 1133-1134, y 1143 x 5146-5148. Wall tiles kept: x 5179 to the landing, y 1160-1161 to the Warren |
| The crawlway | 5160,1159 (mouth, in the Strongroom) through 5160,1160-1161 to 5160,1162 | | one tile wide, south only; the map batch draws the two wall tiles as a low tunnel (impassable statics: the crawlway item moves the player past them) |
| The Warren | x 5142-5242, y 1162-1192 | 1 | Crawl Den x 5146-5170, y 1162-1172 (the crawlway lands here); Tunnel Foot x 5186-5200, y 1162-1170 (the landing tunnel lands here); joined by x 5171-5185, y 1165-1167; Great Burrow x 5146-5208, y 1176-1192, joined by x 5156-5159 and x 5192-5195, y 1173-1175; descents x 5160-5163 and x 5200-5203, y 1193-1197 |
| Brood Pit | x 5212-5240, y 1168-1188 | 1, boss | one mouth from the Great Burrow, x 5209-5211, y 1180-1183 |
| The Tangle | x 5142-5188, y 1198-1228 | 2 | one root cavern (5 root masses as solid blocks); the Thicket x 5142-5156, y 1218-1228 behind a root wall, gap x 5157 y 1222-1223 (Bramblehulk); joined to the Dawnseam x 5189-5193, y 1212-1214 |
| The Dawnseam | x 5194-5242, y 1198-1228 | 2 | one crystal seam (5 clusters); the Seam Heart x 5228-5242, y 1218-1228, gap x 5227 y 1222-1223 (Seamguard) |
| The Gloom | x 5150-5236, y 1234-1260 | 3 | a ring of tunnels round the lair (north y 1234-1236, west x 5150-5182, east x 5228-5236, south y 1258-1260), 3 web masses; descents from the Tangle x 5166-5169 and the Dawnseam x 5214-5217, y 1229-1233 |
| Gloom Queen's lair | x 5184-5226, y 1238-1256 | 3, boss | walled inside the Gloom, one mouth in the west wall x 5183, y 1246-1248; two web pillars |

8,555 floor tiles, 1,618 wall tiles, 272 solid tiles. The map batch also needs: the teleporter from the B1 hole (Old
Haven 3619,2620) to the arrival 5193,1138 and back; the floor Z it picks (the seeder reads it with `GetAverageZ`); and,
if Chase wants it, `GoLocation` moved from the provisional 5191,1195 to the arrival (staff `[go` only).

**Does the enlarged Vault fit the 1.5x Overdraft fight with the decoy chests and room to kite?** Yes. The Overdraft is
one mobile on one tile, drawn about 89 x 83 px at 1.5x (P140), walking 0.4 s a tile against a running player's 0.2 s.
The Strongroom is 37 x 16 (556 walkable): two loops of 22 tiles round the pillars, a 13-tile gap between them for a
figure eight, 9 tiles of floor west and east of the pillars and 5 north and south. The decoy chests are in the Deposit
Hall, a room away, so springing one never joins the boss fight. Nothing more is needed.

## 4. Part D.4: the spawners (the seeder's data)

Stock `Spawner`; `Group = true` where a room should respawn only when cleared. Pack sizes respect the 3-hostile Young
limit: no spawner holds more than 3; the Hoarding Rat spawns alone because it calls 2 Penny Rats (P140); the Burrow
Mother's own brood (3 at once) makes her room 4, and the region's limit stops the fourth striking a Young player.

| # | Where | Tile | Creatures | At once | Home | Group | Respawn (min) |
|---|---|---|---|---|---|---|---|
| 1 | Counting Room | 5174,1137 | LedgerBat | 3 | 4 | yes | 1-2 |
| 2 | The Stacks | 5163,1141 | PennyRat | 2 | 1 | yes | 1-2 |
| 3 | The Stacks | 5160,1133 | HoardingRat | 1 | 2 | no | 2-3 |
| 4-6 | Deposit Hall | 5150,1133; 5143,1137; 5152,1141 | SafeDepositBox | 1 each | 0 | no | 2-3 |
| 7 | Strongroom | 5160,1151 | TheOverdraft | 1 | 6 | no | 3-4 (after the crawlway shuts) |
| 8 | Crawl Den | 5158,1167 | BurrowGrub | 2 | 5 | yes | 3-5 |
| 9 | Crawl Den | 5150,1170 | BurrowHog | 1 | 4 | no | 5-8 |
| 10 | Tunnel Foot | 5193,1166 | BurrowScamp | 2 | 4 | yes | 3-5 |
| 11 | Great Burrow west | 5156,1184 | BurrowGrub, BurrowScamp | 3 | 6 | yes | 4-6 |
| 12 | Great Burrow middle | 5177,1184 | BurrowScamp, RedcapScamp | 2 | 6 | yes | 4-6 |
| 13 | Great Burrow east | 5200,1186 | RedcapScamp, BurrowGrub | 2 | 5 | yes | 4-6 |
| 14 | Great Burrow | 5190,1188 | BurrowHog | 2 | 6 | no | 5-8 |
| 15 | Great Burrow | 5170,1190 | Rotworm (rare tank) | 1 | 6 | no | 8-12 |
| 16 | Great Burrow | 5186,1178 | Grubber (rare runner) | 1 | 8 | no | 20-30 |
| 17 | Brood Pit | 5226,1178 | TheBurrowMother | 1 | 4 | no | 20-30 |
| 18 | Tangle north | 5160,1202 | Rootling | 2 | 5 | yes | 4-6 |
| 19 | Tangle | 5176,1201 | Sporecap | 2 | 5 | yes | 4-6 |
| 20 | Tangle south | 5168,1224 | Rootling, Sporecap | 3 | 6 | yes | 5-7 |
| 21 | Tangle east | 5184,1216 | Rootling | 2 | 4 | yes | 4-6 |
| 22 | The Thicket | 5148,1223 | Bramblehulk | 1 | 4 | no | 10-15 |
| 23 | Dawnseam north | 5209,1201 | Dawnshard | 2 | 5 | yes | 4-6 |
| 24 | Dawnseam west | 5200,1222 | Dawnshard | 2 | 5 | yes | 4-6 |
| 25 | Dawnseam east | 5222,1209 | Dawnshard | 3 | 6 | yes | 5-7 |
| 26 | The Seam Heart | 5236,1223 | Seamguard | 1 | 4 | no | 10-15 |
| 27 | Gloom north hatchery | 5166,1236 | Gloomling | 3 | 5 | yes | 4-6 |
| 28 | Gloom west | 5156,1248 | Gloomspinner | 2 | 5 | yes | 5-7 |
| 29 | Gloom south run | 5205,1259 | Gloomling, Gloomspinner | 3 | 2 | yes | 5-7 |
| 30 | Gloom east | 5232,1250 | Gloomweaver, Gloomspinner | 2 | 4 | yes | 6-8 |
| 31 | Gloom | 5176,1258 | BloodWorm (rare) | 1 | 6 | no | 15-20 |
| 32 | Queen's lair | 5198,1242 | Gloomweaver, Gloomspinner | 2 | 3 | yes | 10-15 |
| 33 | Queen's lair | 5212,1252 | TheGloomQueen | 1 | 5 | no | 30-45 |

The mockup numbers rows 1 to 33 in this order (the three chests are 4, 5, 6). **The Warren's stock fillers:** P140
noted pinned has no Rotworm, Bloodworm or Grubber; P119 ported all three (`Mobiles\Normal\`). Rotworm (200-250 hits,
1-5 damage) and Grubber (it flees) fit the Warren as rare spawns; **BloodWorm (374-422 hits, 11-17 damage) is far past
tier 1**, so it is a rare Gloom spawn instead (Decisions, item 3).

## 5. The mockup and the look swatches

`notes\art\rootdeep-mockup\` (325 KB committed; no file over 75 KB):
- `index.html`: the question at the top, the plan, the fit answer, the spawner table, the swatches, the spec table.
  ASCII, light and dark themes.
- `layout.png` (1176 x 1288, 74 KB): drawn by `build_mockup.py` from the spec over `radar-base.png`, vseUOAware's
  `export_map_region_png` of x 5104-5271, y 1104-1287 (the rectangle plus a margin: void land inside, the sea west of
  x 5120 and the next area's roofs south of y 1284 show), through P134's fixed UOP map reader.
- `swatches\` (47 PNGs): every stock candidate rendered by vseUOAware's `render_art_tile` from the client's art.
- `dungeon-survey.json` and `survey_dungeons.py`: the floors and walls OSI's own Trammel dungeons use, counted with
  vseUOAware's `inspect_map_region` over Covetous, Deceit, Despise, Shame, Wrong, Terathan Keep, the Orc Cave, Destard
  and Hythloth (pinned's regions.json rectangles). Every stock candidate is one of those or a stock tile of the theme.
- `vse.py`: a batch client for the local vseUOAware MCP server (the same stdio JSON-RPC as P134's `mcp_smoke.py`).
- `local-previews\` (git-ignored, `.gitignore:34`, proven with `git check-ignore -v`): the third-party previews.

**Sets proposed (Chase picks; nothing decided):** Landing L-A dungeon stone cave (Deceit, Hythloth) or L-B rough cave
(Orc Cave, Covetous); Vault V-A marble strongroom (metal door), V-B sandstone vault (iron gate), V-C dungeon stone
vault (portcullis); Warren W-A dirt burrows or W-B cave burrows; Tangle T-A rooted cave (vines, mushrooms, fallen
logs) or T-B root forest under earth; Dawnseam D-A crystal seam or D-B stone seam (flowstone); Gloom G-A Terathan dark
stone with webs or G-B webbed cave; the lair Q-A; the crawlway C-A as built. Third-party beside them, with flags: X-1
custom cave entrances (otimpyre: CREDIT, never repost), X-2 blue stone and X-3/X-5 the Ultimate Dungeon Wall Set
(DRC1K: CREDIT, non-commercial, no redistribution outside the client, **no modifications** without his OK), X-4 gray
rocks (DRC1K), X-6 the cave hole (otimpyre, EA-derived: patch records only). Queued, not on disk: giant mushrooms
(Q#235, Q#236), the crystal set and wall (Q#284, Q#302), cave entrances (Q#347).

**vseUOAware gaps (said, not patched):** it has no texture (texmaps) renderer, so floors show as their land-art
diamond (how the client draws flat land anyway); and every export lands under its own `exports\` folder whatever path
is given (P134 section 7.2's rule), so `build_mockup.py` copies each file from the path the tool returns.

## 6. Facts, red then green

`server\tests\Regions\RootdeepVaultVerification.cs`, 6 facts:

1. **V1** The Vault is a child of the Burrows over x 5142-5178, y 1132-1159 exactly (corners in; the doorway wall, the
   Warren wall and the landing out); the Burrows' Entrance is found from inside; recall in is refused with the Burrows'
   line; the region's player name is the Rootdeep Burrows.
2. **V2** The doorway refuses a skipper and a graduate, each with its line, and a non-participant's pet; lets in a
   participant, their pet, staff and a wild creature; teleport in from the landing is refused for a participant and
   allowed for staff.
3. **V3** The crawlway is shut before; another Vault creature's death (a Hoarding Rat) opens nothing; a shut crawlway
   refuses; a hurt Overdraft opens nothing; on its death the fighter and the master of the dog that bit it are credited
   and a bystander is not; the bystander cannot crawl; the dog's master and the dog land at 5160,1163 in the Burrows;
   closed again it refuses.
4. **V4** A credited participant is refused with the sealed line and is turned out at login; a participant inside
   stays; a graduate inside is turned out to the landing.
5. **V5** Every seeder type resolves to a creature; every row is in its zone, at most 3, Vault rows inside the Vault;
   the Overdraft respawns after the crawlway shuts; on void land it refuses and places nothing; a dry run counts 33 + 1
   + 1; the run places each spawner with its count, Group, home range, entries and delay, a working AnkhWest and the
   crawlway shut; a re-run places nothing (35 present).
6. **V6** The crawlway round-trips the serializer and comes back shut and immovable.

| Run | Break | Result |
|---|---|---|
| red 1 (`--tests-only`) | one per fact: V1 the Vault's end x 5180 (it swallows the doorway); V2 the teleport refusal skipped; V3 the Overdraft's hook commented out; V4 the login handler empty; V5 the void-land gate skipped; V6 the load reset empty | did not compile: a `ValueLinkList` has only a ref-struct enumerator (walked through `ToArray()` instead) |
| red 2 | the same six | **exactly the six facts red, each on its own line:** V1 :149 (the doorway is the Vault), V2 :194 (teleport allowed), V3 :240 (crawlway not open), V4 :284 (stayed at 5160,1150), V5 :333 (not refused), V6 :407 (open after load). 1,430 tests, 1,419 passed, 7 failed (the seventh the flaky garden test below), "No image was built" |
| green 1 | none | V3, V5, V6 red: my real bug (pinned deletes the creature in `base.OnDeath`, so the crawlway search had no map; the hook moved first), V6 (the generated `[AfterDeserialization]` runs delayed, so the open graphic survived a load: the open state became a runtime field), V5 a knock-on of V3's leftover crawlway (V3 now cleans up in `finally`) |
| red 3 | V3 the hook after `base.OnDeath` (the real bug); V6 `IsOpen` read from the graphic again | V3 red at :246; V6 stayed green (the copy's graphic was not open), so V6 needed a break that fits the new design |
| red 4 | V6 the open state starting true | V6 red at :418 (V3 :221 and V5 :382 too, from the same break) |
| green 2 | none | 1,430 tests, **1,426 passed, 0 failed**, 4 skipped |
| final | the seeder's five tightened home ranges and the new VERSION | one build red on the garden test only, the next green: 1,430, **1,426 passed, 0 failed**, 4 skipped; image `sl-modernuo:cc-P141` = `e89d95c8ad61`; `sl-modernuo:latest` still `8e1a1916a752` |

**The flaky garden test (not mine, for the overseer):** `RaisedGardenVerification.AMoundGrowsWithoutWaterOrMaladies`
(P128, `server\tests\Services\Plants\RaisedGardenVerification.cs:243`) expects a dry stock bowl's seed to survive one
`DoGrowthCheck`; pinned's growth check rolls random infestation and damage, so it sometimes dies to BowlOfDirt. It
failed 3 of the 7 builds here (red 2, red 4, final 1) and passed in the others; I did not touch it.

**The mockup's own check** (`build_mockup.py`'s home-range rule) was seen red: run on the first Penny Rat range (3) and
lair guard spot (5196,1240, range 4) it named both ("reaches 14 floor tiles beyond a wall", "9 tiles"); the seeder rows
were tightened and it reads "problems: none".

**Test shard boot:** the bot's runner (`Run-OvernightPlaytests.ps1 -SkipBuild -Only P140-1 -SkipSoak -NoEmail -Runs
1`, the image tagged `sl-modernuo:bot`) booted the scratch shard on a copy of the test world's newest backup twice:
on the green-2 image (`testing\bot-runs\2026-10-18-0129\`) and on the final image (`2026-10-18-0140\`). shard.log:
0 exceptions, 0 errors, one warning that P140's run has too ("Command stats already registered"). P140-1 passed both
times. Rule 1 held both times (the live and the real test shard untouched).

**I broke tonight's nightly bot run.** The `2026-10-18-0130\` folder is the scheduled nightly run
(`Run-OvernightPlaytests.ps1 -Commit HEAD`, started 01:30, building 73a0348 without this prompt's code). It shares the
scratch shard (compose project `sl-uo-bot`, `D:\UO\bot-shard\world`, tag `sl-modernuo:bot`) with a manual run, and
nothing locks it. My first boot check (01:29 to 01:30:45) ended before the nightly started its shard (01:32:31). My
second (01:40) re-copied the world, retagged `sl-modernuo:bot` to my image and tore the container down at 01:41:56
while the nightly was mid-run: from 01:43:54 its checks read `ConnectionRefusedError` (T-039 first), and its later
checks and its soak will too. Its results before 01:40 stand (P62-7 read FAIL at 01:38, before I touched anything;
not mine to judge). I left the nightly process running rather than kill a scheduled job, so its after-email will
report the errors. **It should be re-run** (`Run-OvernightPlaytests.ps1 -Force`, or tomorrow's run: its work check
will still see the code as untested). A memory note now says to check for a running nightly before any manual bot run.

**Gates outside the shard:** none touched (no package, art or launcher change). `tools\tests\test_play_who.py` after
the triage rows: section 9.

## 7. For the overseer: deviations to register

1. **The Vault** (ours, F-45): a tutorial-only room with a one-way exit. Its credit is the key `burrows.vault` in the
   account's `TutorialRecord.StationsDone` (not a station; no schema change).
2. **Teleport into the Vault is refused** even for participants (the doorway is the way in); the Burrows already refuse
   recall, gate and outside teleport.
3. **A player who logs in inside the Vault without the right to be there is moved to the landing.**
4. **The crawlway** opens for 2 minutes on the Overdraft's death, passes only credited players, and its open state is
   not saved; the Overdraft respawns after 3 to 4 minutes.
5. **Every participant who damaged the Overdraft is credited**, not only the killer.
6. **The landing ankh** (an `AnkhWest` at 5206,1136): ours; OSI has no Burrows.
7. **Every spawner number** (counts, home ranges, Group, delays) is ours, first proposals.
8. **BloodWorm in the Gloom, not the Warren**; Rotworm and Grubber as rare Warren spawns (the draft listed all three as
   Warren fillers).
9. **The region's player name** is now "the Rootdeep Burrows" (`OldHavenBurrowsRegion.RegionName`; the class keeps its
   name). Nothing saved used the old name (the map does not exist yet).
10. Unchanged from pinned, recorded because the prompt assumed otherwise: a Young death in the Burrows goes to New
    Haven's healer, not the Entrance.

## 8. Decisions for Chase

1. **Approve the layout and look, or say what to change** (`notes\art\rootdeep-mockup\index.html`; P141-1). The map
   batch does not start until you do. The open choices: the layout as drawn; one look per zone (sets above, or mix);
   items 2 to 5 here.
2. **A Young trainee's death in the Vault** (P141-5): keep pinned's rule (the ghost wakes by New Haven's healer, about
   57 tiles from the hole, and walks back down for the corpse: a real death-and-recovery lesson), or a Vault rule that
   keeps the ghost in the Burrows so it uses the landing ankh. The second needs a pinned patch: `YoungDeathTeleport` is
   not virtual and its region test is by name (PlayerMobile.cs:4065-4072).
3. **The Warren fillers** (P141-6): keep Rotworm and Grubber as rare Warren spawns and BloodWorm as a rare Gloom spawn,
   move them, or drop them.
4. **Two trainees at once and the Overdraft's loot:** today the corpse follows pinned's looting rights, so the one who
   did less damage may not loot the fixed drop. Keep, or give each credited trainee their own drop (a small change in
   `TheOverdraft.OnDeath`).
5. **Third-party kits:** DRC1K's packs forbid modifications and reposting (his terms; the previews stay on your PC).
   Say whether any of X-2 to X-5 should be used or asked about; otimpyre's X-1 and X-6 have no terms beyond credit.
6. **`GoLocation`** (staff `[go`): move it to the arrival 5193,1138 with the map batch, or leave it.
7. **Re-run tonight's bot** (section 6: my second boot check took the scratch shard from under it at 01:41).

## 9. Play-test items and their sorting

The seven items below are sorted in `testing\bot-triage.md` (`### P141`: 1 DECISION, 2 BOT, 3 BOT-PARTIAL, 4 EYES, 5
DECISION, 6 DECISION, 7 DEPLOY) with steps in `testing\playtest-steps.json`. The two BOT checks are not written yet:
the floor is void land, so nothing can walk the doorway until the map batch. The items the prompt lists that belong
to P140 (each body draws, the archer's colour, the crow's hue, the Overdraft's scale, the decoy chests bite) are
P140-3 to P140-7 already.

## 10. Repo size

Largest new files: `layout.png` 74 KB, `index.html` 30 KB, `build_mockup.py` 28 KB; the mockup folder is 325 KB
committed in all (47 swatches, 266 KB). `local-previews\` (148 KB, third-party) is git-ignored and proven with
`git check-ignore -v`. Build and bot logs are in `D:\UO\cc-p139-work\`, outside both repos.

## 11. Deviations in how the work was done

- **One Read was denied by the unattended hook:** `Read D:\ShatteredLegacy\server\customizations\Mobiles\Burrows\
  VaultCreatures.cs` (offset 280), to place the Overdraft's hook before editing it. Every later read used `cat`/`sed`
  and every edit a short Python script, as the memory note says; nothing was skipped.
- **A manual bot run during the nightly window broke the nightly run** (section 6). I did not check for a running
  nightly first; I should have.
- **The Golem's task-list tool was not available in this session**, so there was no live task list to mark (as P140).
- The red breaks were applied to the repo copies only and the clean copies (session scratchpad, `p141\clean\`)
  restored over them; the five files' SHA-256 are in `scratchpad\p141\green-hashes.txt` and match the repo.

## For Chase

To try it in game once the map batch has built the floors (item 1 comes first; the mockup needs no deploy):

1. **Approve the layout and look** (a decision, before anything else): open
   `D:\UO\shard-migration\notes\art\rootdeep-mockup\index.html`, look over the plan and the swatches, and answer the
   open choices at the top: approve, or say what to change.
2. **The Vault doorway:** on the test shard, a fresh tutorial character with a pet walks west through the doorway at
   5179,1137; a graduated character and one that skipped the tutorial try the same. Pass: the trainee and pet walk in;
   the graduate gets "System: You graduated. The Vault does not do reunions." and the other the trainees-only line.
3. **The crawlway:** after `[ClusterFSeedRootdeep`, a fresh tutorial character kills The Overdraft in the Strongroom
   and steps on the rocks at 5160,1159. Pass: the Echo says a crawlway opened, the rocks become a hole with dust, you
   and your pet land in the Warren at 5160,1163, and the Vault doorway refuses you afterwards.
4. **The landing ankh:** a west-facing ankh stands on the landing's east wall at 5206,1136 (not floating or sunk), and a
   ghost that is not Young walking up to it is offered resurrection.
5. **Young deaths** (a decision): keep pinned's rule (a Young trainee's ghost wakes by New Haven's healer) or ask for a
   Vault rule (Decisions, item 2).
6. **The Warren fillers** (a decision): Rotworm and Grubber rare in the Warren, BloodWorm rare in the Gloom, or change
   it (Decisions, item 3).
7. **Seed it:** as Administrator, `[ClusterFSeedRootdeep dryrun` then `[ClusterFSeedRootdeep`. Pass: "would place 33
   spawners, 1 ankh, 1 crawlway", then the same placed; each spawner where the mockup's table says, its creatures in
   their room.

## 12. Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun` (run with this note written,
before its last line), commits nothing. It refreshed the play-test mirror from Haven first (`testing/SUMMARY.md`,
`testing/play-tests.json`: machine output). Code: 7 files (`CHANGELOG.md`, `VERSION`, `VaultCreatures.cs`,
`OldHavenBurrowsRegion.cs`, `ClusterFRootdeepSeeder.cs`, `RootdeepVault.cs`, `RootdeepVaultVerification.cs`). Docs:
124 files (`.gitignore`, the triage and steps, the mockup folder, this note, the bot-run folders).

```
Repo Result
---- ------
code dry run
docs dry run
```

P141 DONE
