# P605: second opinion on the P481 start area design

Reviewed October 25, 2026. Design review only. No implementation decision is made here.

## What Chase should take into Monday

The Fold is a technically sound place to build the Wakening Isle. A separate server map can use Trammel's existing tile files and client map number. It gives the tutorial space of its own without teaching every player's client about a seventh facet. The linear lesson route and the final arrival beside Rook also make sense.

I would approve that location and route as a direction. I would not approve the promise that the recommended privacy mix is already designed closely enough to price at six prompts. The map registration is the easy part. Shared pests, shared NPC responses, account eligibility, pet travel, and recovery from a saved scene need more design and verification. Those are player behavior requirements, not polish.

For the privacy choice, distinguish two promises:

- **Other trainees are hidden:** P481's visibility hooks can do this, with additional work described below.
- **Other trainees cannot interrupt your lesson:** hiding them does not establish this. Shared pests and doors still change for everyone. Either give the interactive parts an owner and enforce it, or use separate map copies for the player or party.

The full-copy option deserves a fair comparison after those requirements are priced. Its object and recovery costs are real, but P481 has not measured them against the cost of making shared gameplay private. No runtime memory or concurrency measurements were supplied or made in this review.

The simpler locations remain valid scope choices. A keeps an island arrival without a new server map, B avoids building an island, and C keeps the farm close to its current site. They still need the changed lesson sequence, arrival choice, and any promised privacy. Water, walls, and distance do not provide private copies of interactive objects. Their shorter prompt counts should not be compared with the Fold unless the promised player experience is the same. I did not independently walk B or C or verify their nearby spawners.

## Evidence and scope

I read the agreements in both supplied work copies, the direction decision, and the task list. I read P481 with `git show`, without switching branches:

- Design repo ref: `origin/golem/Iron/P481`, commit `27486f06842c8cc1e79196beb79c6aa2eb4e6364`.
- Design: `notes/cc-P481-new-player-start-area-design.md`, including its six proposed build tasks.
- Supporting artifacts present under `notes/cc-P481-tools/` at that ref: `facet_plan.py`, `topdown.py`, `plan-A.json`, `plan-B.json`, `plan-C.json`.
- Code main: `fcc658b853cc81684fb0d9d5268c91b6ba99ae49`. `main` and `origin/main` resolved to that commit. The relevant code surfaces in this work copy matched main.
- Pinned upstream: `D:\UO\ModernUO-pinned`, clean at `d4531cd94b739613155225c234900de9f47d2c88`, matching main's `docker/uo/Dockerfile:3`.
- Supplemental client source: `D:\UO\tazuo-sl-build\src`, HEAD `3212623f63436be1c0f4e3b308b202b29597c026`. That tree has local changes. The city-selection, map-loader, world, and light-packet files cited below were not listed as modified. This is source evidence, not verification of the shipped executable.

Below, **shard** means paths in code main. **Pinned** means paths below `D:\UO\ModernUO-pinned`. **Client** means paths below the supplemental client source root.

The behavior findings below come from reading those implementations. They are not reproductions on a running shard.

The PNGs named by P481 are absent from its remote ref. `git ls-tree -r --name-only origin/golem/Iron/P481 notes/cc-P481-tools` lists only the supporting artifacts above. I could review the plans and drawing code, but could not inspect the promised pictures from that branch. They should be made available for Chase's visual decision.

## What holds up

### A separate world using Trammel's tiles works at the source level

Pinned `Projects/Server/Maps/Map.cs:73` separates `MapID`, `MapIndex`, and file index. Each map has its own sectors and region dictionary. The static map table is indexed separately from the client map number. `Projects/Server/Network/Packets/OutgoingMapPackets.cs:55` sends `map.MapID` to the client. Thus server index 32 with client ID 1 and file index 1 is supported by these implementations. Dynamic NPCs and items on that map do not become Trammel's NPCs and items.

Pinned `Projects/Server/Maps/MapLoader.cs:33` documents the reserved indexes, and `Distribution/Data/map-definitions.json` leaves 32 unused. I found no map-32 registration in main's customizations. Persisting maps by index is real: `Projects/Server/Serialization/BufferWriter.cs:468` writes `MapIndex` as a byte. Reserve the Fold and pool indexes permanently once saves can reference them. Never recycle an index for an unrelated world.

P481's startup uncertainty can be narrowed. Pinned `Projects/Server/Main.cs:667` invokes all `Configure` methods before region loading and `World.Load`. `MapLoader.Configure` has priority 2; `Projects/Server/Attributes.cs:40` sorts priorities ascending and defaults unmarked methods to 50. An additive customization can construct the map and register it in both `Map.Maps` and `Map.AllMaps` after stock map configuration and before world load. An explicit priority avoids reliance on equal-priority ordering. This needs a build and save/reload proof, but does not inherently require an upstream JSON patch.

### The proposed void really is empty in the local reference files

I independently read the inclusive rectangle x 6160 through 6639, y 1832 through 2279 using `scripts/mapbuild/uofiles.py` from the design repo:

| Artifact counted | Result |
|---|---|
| `D:\UO\UltimaOnlineVanilla\map1LegacyMUL.uop` | 215,040 land cells, all tile `0x0244`, Z 0 |
| `D:\UO\UltimaOnlineVanilla\staidx1.mul` and `statics1.mul` | No statics in the rectangle |

The read used `MapFile.get` across the rectangle and `statics_in` over the same bounds. It wrote no client data. This confirms the empty terrain claim for those files. It does not prove that every custom region, future event, or teleporter will leave the space unused.

### The existing package route fits the idea

Shard `player-package/payload/app/Apply-MapOps.ps1:125` reads land and static operations and makes local overrides. `docker/uo/Build-MapOverlay.ps1:33` calls that same applier for the server overlay. There is no inherent need for `map6`, a seventh client map setting, or new client code to show the Fold as map 1.

P481's warning about a new client facet is supported by client `src/ClassicUO.Assets/MapLoader.cs:23,102` and `src/ClassicUO.Client/Game/World.cs:205`: the default map count is six, settings can expand it, and an out-of-range incoming map number falls back to 0. This is a constraint of the current package configuration, not a universal six-facet limit in ModernUO or ClassicUO.

### The city list can carry the proposed choice

Shard `server/customizations/CharacterCreation.cs:129` currently returns one New Haven city. At `:268` it moves the new mobile to the chosen start; at `:298` the SA path returns `args.City`. Both tutorial and skip entries can be advertised on Trammel, then the tutorial entry can resolve to a Fold destination on the server.

Client `src/ClassicUO.Client/Game/UI/Gumps/CharCreation/CreateCharCityGump.cs:59,104,165` supports the default city, map image, description, and coordinate-based buttons described by P481. Its facet-name array is only six entries, so advertising map 32 or map 6 here would be wrong. Advertising map 1 is appropriate. The display coordinates must remain separate from the actual arrival point.

Pinned `Projects/UOContent/Network/Packets/IncomingAccountPackets.cs:198` raises character creation before assigning `m.NetState`. Deferring tutorial entry and skip actions to login is justified. Character creation still has `args.State`; the limitation is that the new mobile is not attached to it yet.

### The lesson framework and graduation can be reused

Shard `server/customizations/Tutorial/TutorialStations.cs:54` defines the core sequence, and `ClusterFTutorial.cs:129` derives unfinished stations from saved keys. Reordering travel to the end can preserve completed lesson keys if the conversion rule is explicit. Rook's existing town role, skip, remedial training, graduation rewards, and one-pet account rule are useful foundations.

Keeping the vision harmless also matches main. `server/customizations/Tutorial/ClusterFLoops.cs:67` contains the existing narrative, while the current scene in `TutorialCoreTrials.cs:222` advances messages and completion evidence without resetting character progression.

## Risks and corrections before implementation

### 1. Visibility is not private gameplay

Pinned `Projects/UOContent/Mobiles/PlayerMobile.cs:3239,3282` provides the proposed mobile and item visibility hooks. Pinned `Projects/Server/Mobiles/Mobile.cs:5611` filters nearby spoken messages through the listener's `CanSee`. Those parts of P481 are correct.

However, main's `server/customizations/Tutorial/TutorialCreature.cs:35` admits any active tutorial participant. There is no per-trainee owner. `TutorialFarm.cs:242` credits participants who damaged the same dying pest, and `:402` seeds shared spawners. Two hidden trainees can still compete for a pest, see its health change, or see it disappear when the other trainee kills it. A shared lodge door also has shared open/closed state.

Shared NPC speech remains visible to everyone who can see the NPC. For example, `TutorialRecruiter.cs:54` uses `Say`, so a shared greeter using that behavior would broadcast its response even when the person who triggered it is hidden. Private replies should use a directed response.

The helper behind the proposed short patch must therefore define more than an allowlist. It needs ownership for interactive actors and dropped supplies, behavior for neutral decor and NPC equipment, party membership changes, visibility refresh when membership changes, corpse ownership, and interaction rules. Preserve normal map, hidden-staff, container, and ghost checks rather than returning true merely because an entity is allowed by the tutorial policy. Pinned `Projects/Server/Mobiles/Mobile.cs:7190,7232` contains those checks; `PlayerMobile.cs:3246` also has an early visibility-list return that needs deliberate ordering.

Two small hook calls are plausible. A complete private tutorial implemented in about 20 lines is not established.

### 2. The sounds claim is too broad, and the mix is not required for private light

Pinned `Projects/Server/Effects.cs:66,130,168` broadcasts location sound and effects to nearby clients. P481 correctly identifies that leak. Main's walking-tile sparkles already use the location API (`TutorialCoreTrials.cs:206`), so the audit must cover ordinary lessons as well as the vision.

But pinned `Projects/Server/Mobiles/Mobile.cs:6853` filters **mobile** `PlaySound` by `CanSee`. All sound APIs do not behave alike. Shared pests and shared NPCs remain visible sound sources, which is another reason ownership matters.

P481 also says visibility alone leaves the vision's lights shared. The per-player light approach it proposes for the chamber can equally read the current viewer in a shared region: `Projects/Server/Mobiles/Mobile.cs:3092` passes that mobile to `Region.AlterLightLevel`, and `PlayerMobile.cs:1168` sends the resulting light to that player's connection. A separate chamber is useful for scene objects and isolation. Private lighting alone does not require one.

### 3. Moving the tutorial is more than changing placement constants

Shard `TutorialCorePlacement.cs:18,47,70`, `TutorialCoreTrials.cs:151,157,256`, `TutorialRecruiter.cs:81`, and `TutorialFarm.cs:157,373,588` hard-code Trammel in fit checks, searches, arrows, proximity checks, death handling, or seeding. These must agree on the active lesson map. Otherwise the isle can look correct while its lessons fail every proximity test.

The farm is currently optional content, not a core prerequisite. `TutorialFarm.cs:52` completes `animals.taming` and `combat.healing`; `ClusterFTutorial.CoreDone` at `:140` and `Graduate` at `:289` require core stations only. Putting the farm between chat and death needs an explicit sequencing and graduation rule. Otherwise the next core action skips it. Making it mandatory also changes the pet choice from the current graduation choices to dog or cat for a first-time trainee. Chase should knowingly choose that tradeoff.

The current travel item at `TutorialCorePlacement.cs:168` responds to **double-click**, not walking into it. P481's walk-through wording requires a movement handler or revised instructions.

Completed station keys persist, but the existing practice supplies do not have P481's promised persistence. Login cancels the active trial (`ClusterFTutorial.cs:83`), cancellation deletes its supply (`TutorialCoreTrials.cs:176`), and the practice bag, cloak, and token delete themselves after deserialization (`TutorialCorePlacement.cs:197,204,212`). Keep regeneration as an explicit reconnect rule or implement persistent ownership deliberately. Do not treat the current item classes as already persistent private props.

### 4. The cross-map exit must take the pet

That travel item currently calls only `pm.MoveToWorld`. Pinned `Projects/Server/Mobiles/Mobile.cs:2602` moves the mobile and its carried items, not its followers. Stock moongates explicitly call `BaseCreature.TeleportPets` before moving the player (`Projects/UOContent/Items/Skill Items/Magical/Misc/Moongate.cs:113`). Simply reusing the tutorial gate for a different map strands the farm pet on the Fold.

Define transfer at the pier, return to the isle for remedial training, and vision entry/exit. For the vision, either keep the pet safely at the stones or transfer it and return it before releasing the chamber. The stock pet helper has range and follow-order restrictions (`Projects/UOContent/Mobiles/BaseCreature.cs:4092`); do not assume it collects every pet everywhere.

Also handle Haven-to-Fold travel for a loop-0 character who starts voluntarily at Rook. `TutorialIslandGate.cs:24` currently treats a destination outside Haven and Rootdeep as leaving the island, and `server/patches/PlayerMobile-tutorial-island-gate.patch` enforces that on `MoveToWorld`. The intended tutorial transfer needs an explicit permitted route. The pier trip from the Fold to Haven is not subject to that current source-side restriction.

### 5. Account eligibility needs a complete rule

Shard `ClusterFTutorial.cs:61,109,225` makes participation once per account and binds it to one character serial. `CharacterCreation.GetStartingCities` caches a global list. Adding a tutorial city does not make a second character eligible to replay an account's completed tutorial.

Specify the result for a fresh account, an account already in progress on another character, a graduated account, a skipped account, and a deleted tutorial character. Do not send an ineligible character to an isle whose lessons reject them. Keep the current one-pet and reward records intact.

P481's exclusion of pre-launch characters is a proposed change, not present behavior. Today's login calls `TryEnter` for a NotStarted account with no creation-date filter (`ClusterFTutorial.cs:84,109`). Record eligibility and the creation-screen choice against the intended character, persist it through a disconnect before first login, and consume it once. A loose pending account flag needs safeguards so an older character cannot consume another character's choice.

The skip behavior is mostly described correctly: `Skip` gives the achievement and, under the default setting, loop 1 without the separate tutorial graduation reward. It does still invoke the loop reward path: `ClusterFLoops.cs:54` calls `ClusterFLootBoxes.OnLoopCompleted`, which awards a loop box (`server/customizations/LootBoxes/ClusterFLootBoxes.cs:224`). Say "no tutorial graduation box," not "no box."

### 6. The vision pool needs saved recovery, and its fallback contradicts privacy

P481 says a busy pool can play the scene at the shared stones with only its owner seeing the figures. Its visibility table simultaneously says unowned shared NPCs are visible. The fallback actors therefore require ownership, private effects, private speech, and reliable cleanup too. If those are built, explain what the separate chamber buys. Otherwise prefer a clear retry or queue to an unproven fallback.

The more serious recovery case is a restart during the scene. A logout callback alone does not cover a process ending between beats. Pinned `Projects/Server/Mobiles/Mobile.cs:1567,2457,9062` stores logout location and map separately from the mobile's current map. Save enough state to return a player to the stones on startup/login, restore the prior frozen and light state, and clean up actors. Keep every saved chamber index registered before world load, even when its slot is free. A slot is not reusable while any online character, offline return location, pet, or scene object still depends on it.

Reuse of this pool for League trials is a reasonable architectural goal. It is not evidence that a short visual scene and a persistent dungeon trial have the same ownership, reset, or reconnect contract. Define those contracts before pricing the reuse as free.

### 7. Light is not a guaranteed blackout, and a stock Clone has gameplay effects

Client `src/ClassicUO.Client/Network/PacketHandlers/LightLevel.cs:22` and `PersonalLightLevel.cs:23` allow profile lighting settings to override server light. Light level 30 is therefore not a guaranteed fade to black, and level 0 does not establish a full-screen white flash. Pinned has `NetState.SendScreenEffect` (`Projects/Server/Network/Packets/OutgoingEffectPackets.cs:322`), which is a candidate for a client proof. Keep the subtitles understandable when lighting is overridden. Actual fade, subtitle placement, sound quality, and accessibility remain client checks.

Pinned `Projects/UOContent/Spells/Ninjitsu/MirrorImage.cs:119` is useful appearance-copying source, but its `Clone` is not a passive mannequin. Construction copies skills, sets combat/follow state, starts an unsummon timer, and registers a Mirror Image clone; deletion unregisters it and emits effects. A passive scene figure that copies appearance avoids those gameplay side effects. Reusing the class itself needs explicit justification.

The narration also describes future progression. `ClusterFLoops.cs:39` has an empty skill/level-reset hook. The review confirms that the current vision does not change those values; it does not confirm that the loop system described by the story exists yet.

### 8. Correct the map cost and package wording

P481 says maps with the same file index share one tile matrix. More precisely, pinned `Projects/Server/Maps/Map.cs:105` creates a matrix per map. `Projects/Server/TileMatrix/TileMatrix.cs:79,174,235` links matrices so cached blocks can be reused, while each matrix still has arrays, streams, and patch state. Map sectors and dynamic entities are separate as well. Shared tiles are cheaper than independent tile data, but not zero-cost worlds.

The statement that all resulting client file sizes stay fixed is also wrong. Shard `Apply-MapOps.ps1:222` copies the original statics into a stream, appends changed static blocks, and repoints the index. New island statics grow `statics1.mul`; land edits preserve the map file's existing layout. This does not defeat the proposal or require committing binary files.

"No new client files" should mean **no new facet file family or executable change**. Players still need an updated package containing the island map operations and cliloc entries. A stale package sees the old void rather than the island. F2/F3 must remain a coordinated package and server release.

Finally, P481 section 3.3's listed route legs total 185 tiles, not 165. `facet_plan.py` separately computes a sketch route and allows diagonal moves without checking blocked corners in `walk`. The island drawing also iterates inclusive bounds from center minus 110 through center plus 110, making that square 221 tiles wide. None is a location blocker. Do not promise a measured 165-tile walk until a built map with doors, farm geometry, collision, and lesson detours has been walked.

## Effort check and a useful build order

P481's F1 through F6 are sensible work areas. They are not comparable units of effort, and this review has no measured basis for a replacement prompt count or schedule.

| P481 area | Assessment |
|---|---|
| F1, map and regions | Relatively bounded. Additive registration has a supported startup path. Prove client display, save/reload, housing exclusion, travel, and recovery before permanent content uses its indexes. A plain BaseRegion is not automatically a NoHousingRegion. |
| F2, map and package | Real map construction work. Empty land is verified; shoreline, buildings, collision, art choices, and in-client appearance are not. Do not add rectangle-fill syntax merely to make the tutorial possible; the current operation format can express it. |
| F3, moving the tutorial | Broadest integration task: map-aware placement and checks, new sequence, farm requirements, eligibility, skip/remedial, and pet transfers. Calling it a move understates the behavior changes. |
| F4, privacy | Needs its own player behavior specification. Hiding other players is small compared with making pests, NPC responses, objects, and party transitions private. Ship the promised behavior with F3. |
| F5, scene and pool | A state and recovery feature plus presentation work. Build cancellation and restart recovery before expanding the visual beats. A reusable League pool adds scope. |
| F6, pet protection | Separate policy and implementation. Main's tutorial vet charges Young owners zero, but still refuses an existing corpse and subtracts 0.2 from each skill (`TutorialPetCare.cs:145`). Immediate resurrection with returned corpse contents and no skill loss is new behavior. Updating all stock vets is broader than relocating Tobin. |

Housing and travel hooks exist: pinned `Projects/UOContent/Multis/Houses/HousePlacement.cs:76` honors the NoHousing region types, and `Projects/UOContent/Spells/Base/SpellHelper.cs:633` asks current and destination BaseRegions about travel. Register explicit coverage for the intended map and preserve those types or equivalent effective behavior. A region spell ban does not automatically govern every direct item teleport.

My suggested first deliverable after Chase's location choice is a narrow proof on a disposable world: map 32, a standable arrival tile, an exit, save/reload, and two clients. Then prove the privacy policy with shared pests and a door before building the whole island around it. Those proofs can settle whether the mix or complete copies is actually cheaper for the required experience.

For implementation, require tests written against the old behavior and seen failing before fixes. Useful checks include two trainees affecting the same pest, directed NPC replies, a pet crossing the pier gate, an account's second character, and restart during a vision. Follow with the full solo and party client playthroughs, including custom lighting. This review adds no tests; these are future acceptance cases.

## Limits and handoff

Verified here: the cited source paths, main and pinned revisions, the supported map identity and startup design, the character creation path, existing tutorial constraints, client source behavior, and the empty reference rectangle.

Unverified: a compiled Fold, a running privacy implementation, the precise client executable shipped to players, the PNG appearance, collision and walking time on a built isle, all custom-region overlaps, spell/item travel coverage on a running Fold, memory per occupied map, concurrency limits, scene sound and fade quality, and pool recovery. P481 itself has implemented none of these new systems.

No Haven connection, deployment, Docker operation, account change, code edit, branch switch, commit, or push was performed. No build or test lane was run because this is a notes-only review. The source and map reads ran locally; the PowerShell host was Windows PowerShell 5.1. Optional illustration panels remain P481's later art work, not a new art request from this review.

The required progress reporter completed with both work-copy paths set and `--dry-run`. Its implementation still writes `tools/progress.json` during report construction, so I intercepted that write in memory for this review. No progress, README, or dashboard files were changed.

Chase can choose the Fold confidently as a location. Before choosing the privacy mix, decide whether hidden classmates are enough or whether the farm and other interactions must be private too. That choice controls the implementation cost more than the facet does.

P605 DONE
