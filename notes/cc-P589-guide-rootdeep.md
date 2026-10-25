# P589: Rootdeep player guide draft

Written October 25, 2026. Documentation only.

## Deliverables

- `notes/wiki-drafts/rootdeep.md`: a standalone player guide covering the P413 mound entrance, ladder exit, tutorial-only Vault, ordinary dungeon route, creatures, bosses, floor traps, supplies, travel restrictions, and dangers for Young players.
- This note records the source evidence and verification limits. No code or files under `docs/` were changed.

Both work copies' `AGENTS.md` files were read, along with `docs/direction-decision.md` and `docs/tasks.md`. The prompt's paths were mapped to these work copies. No skill was needed for the explicitly requested Markdown files.

## Evidence

Code paths below are relative to the ShatteredLegacy work copy. Pinned paths are relative to read-only `D:/UO/ModernUO-pinned/Projects/`.

| Guide claim | Source checked |
| --- | --- |
| Second Bank entrance, dark mouth, arrival, ankh, north-wall ladder, return outside the collapsed south wall | `server/customizations/ClusterFRootdeepSeeder.cs:54`, `:81`, `:92`, `:100`; `server/customizations/Regions/OldHavenBurrowsRegion.cs:38`; P188 and P413 implementation notes, plus P545 review. P413 supersedes P188's single hole and old return point. The ordinary south tunnel is in P141's layout table and `notes/art/rootdeep-mockup/layout.json`; its current client walk remains unverified. |
| Monsters in each area and floor hazards | Actual `Spawners` and `FloorTraps` arrays in `server/customizations/ClusterFRootdeepSeeder.cs:122` and `:134`. Read the creature implementations in `server/customizations/Mobiles/Burrows/VaultCreatures.cs`, `WarrenCreatures.cs`, `GloomCreatures.cs`, and relevant definitions in `TangleDawnseamCreatures.cs` and `FarmCreatures.cs`. No total creature or spawner count is claimed. |
| Vault eligibility, credit, two-minute crawlway, one-way exit, immediate reentry refusal, login ejection | `server/customizations/Regions/RootdeepVault.cs:107`, `:123`, `:171`, `:204`, `:232`; `server/customizations/Tutorial/ClusterFTutorial.cs:53`. Credit is account tutorial progress, separate from the ordinary route. |
| Practice net lesson | `server/customizations/Items/Traps/Deployable/TrapLesson.cs`, especially `OnEnterStacks` and `OnNetted`. |
| Overdraft loot is shared corpse loot | `server/customizations/Mobiles/Burrows/VaultCreatures.cs`, `TheOverdraft.OnDeath`; no per-attacker reward grant exists there. |
| Three hostile attackers per Young player; magical entry and Mark blocked, no gate out, Recall out permitted by this region | `server/customizations/Regions/OldHavenBurrowsRegion.cs:50`, `:83`, and `AllowHarmful`; pinned `UOContent/Regions/DungeonRegion.cs` and `UOContent/Mobiles/PlayerMobile.cs:4021` for ordinary Young protection being disabled in a dungeon. |
| New Haven island graduation restriction also includes Rootdeep | `server/customizations/Tutorial/TutorialIslandGate.cs`, `IsOnIsland`, `NeedsGraduation`, and `CanTravel`. The guide describes the default restriction and does not claim current server settings were inspected. |
| Pets must be close and on Follow, Come, or Guard orders | Pinned `UOContent/Items/Misc/Teleporter.cs:236` and `UOContent/Mobiles/BaseCreature.cs:4092`; the crawlway calls the same pet helper at `server/customizations/Regions/RootdeepVault.cs:225`. |
| Young poison immunity survives the lack of ordinary monster protection | Pinned `UOContent/Mobiles/PlayerMobile.cs`, `CheckPoisonImmunity` and `OnPoisonImmunity`. Searched canonical patches for overrides; none found. The guide distinguishes being poisoned from other damage and does not extend the immunity to pets. |
| Young death routes to the New Haven healer area | Pinned `UOContent/Mobiles/PlayerMobile.cs`, `YoungDeathTeleport` and `m_TrammelDeathDestinations`; the dungeon's `Entrance` is the Old Haven mouth. Also checked the explanation in the seeder header and P529 review. No promise that Young ghosts remain at the landing's ankh. |
| Drops, carving, and planned part spending | `server/customizations/Mobiles/Burrows/BurrowsCommon.cs`, creature drop and carve overrides, and the P529 design-versus-build review. The guide describes material drops without promising a working giant-root harvesting route or completed set-upgrade quest. |

## Existing issues carried into the draft

These are existing shard-code issues, ours to fix in a separate code task. They were previously recorded in `notes/cc-P430-review-rootdeep-burrows-build.md`. Current source still shows the relevant behavior:

- Boss credit immediately blocks Vault reentry, while login calls `TurnOut`. A credited player's loot or corpse recovery can therefore be cut off. The guide explicitly warns players before the crawlway instructions lead them out.
- `OnOverdraftDeath` searches for the crawlway within 24 tiles of the boss's death position. The guide advises fighting near the Strongroom and notes that a distant kill can fail to open it.
- Pet-only credit uses the pet's current owner. A pet deleted before boss death can lose that connection. The guide says eligible attackers can receive credit and does not guarantee that every pet-assisted kill is credited.

P425, P504, and P545 reviews were also consulted for entrance, map readiness, Young-warning, and travel limits. Historical P413 private-shard walking results are prior evidence, not a new runtime check in this task.

## Validation and limits

No lane tests are required by P589. No tests were added or changed, so there is no new red/green claim. No builds, shard starts, deployments, package publication, or connections to Haven were performed. No live/client availability, current map installation, actual item placement, balance, or save/reload behavior was verified.

The progress reporter completed against these two work copies using its dry-run path, with its unconditional `tools/progress.json` write suppressed in memory. No progress artifacts were changed. Its hand-kept shard status is older than this task and was not treated as live evidence. Aggregate progress counts are omitted here because this task does not publish the underlying file lists.

Final review completed: both requested files are UTF-8 plain American English with no em dashes or other non-ASCII characters, trailing whitespace, or missing final newline. Each is below 5 MB. `git diff --check` passed in both work copies; the separate whitespace inspection also covered these new, untracked files. The code work copy is clean. The notes work copy contains only the two requested new files. No commits, merges, pushes, or branch switches were made. Stop-request checks between steps found no request.

P589 DONE
