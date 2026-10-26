# P641: review of P629, League investigation warrants

Reviewed October 26, 2026. Code HEAD: `a3f017e279e29eed0ac12c506ef51e6310291583`. Notes HEAD before this review: `67fb1629af64fed87e9997fd7fc354db47c5bab9`. Read-only ModernUO HEAD: `d4531cd94b739613155225c234900de9f47d2c88`, matching `docker/uo/Dockerfile:3`.

This reviews the disabled stage 1 foundation actually delivered by P629: catalog, site checks, warrant, marker, seeder, and their tests. The matching design is `notes/cc-P565-design-league-reward-tokens.md`. Chase's 500 AP, 300 Renown, shared 24-hour cooldown, ordinary group loot, and server-interruption restoration choices are assessed as recorded in `notes/cc-P629-build-league-warrants.md:3`. The original answer transcript was not independently inspected. The constants match those recorded choices. Shop sales, consent, combat ownership, settlement, cooldown persistence, and restart refunds are explicitly later stages, so their absence is not a finding against P629.

Read both P629 notes and the P565 design review. The earlier `cc-P629-build-league-warrants-codex-review.md` already reports the seeder's missing test-shard restriction. That finding is excluded here.

Paths beginning `server/` refer to ShatteredLegacy. Paths beginning `U/` refer to `D:/UO/ModernUO-pinned/`. Findings below follow the current source paths; no runtime or client reproduction is claimed. All are ours to fix. None establishes an active player exploit while sales and use remain disabled.

## Findings

### 1. Medium (P2): moving a containing bag bypasses the warrant's transfer restrictions

**Location:** `server/customizations/LeagueInvestigations/LeagueInvestigationWarrant.cs:205-216`.

The owner can put the warrant inside an ordinary bag in their backpack. `AccountBinding.MayRestIn` explicitly accepts any depth under the same account (`server/customizations/LootBoxes/LootBoxItems.cs:38`). The warrant then checks only drops and trades of the warrant itself. Moving that bag to the ground or trading the bag does not call the contained warrant's overrides.

The engine confirms both routes. `U/Projects/Server/Items/Item.cs:3743` permits an ordinary bag's world drop; `DropToWorld` calls the dropped item's own override at line 3996. Trade completion iterates only the direct items in the trade container and calls their `AllowSecureTrade` (`U/Projects/Server/SecureTrade.cs:195-213`), then delivers those items at lines 280-299. `Container` does not override `AllowSecureTrade` to walk descendants. The recursive `PlayerMobile.CheckContentForTrade` checks traps and stolen status, not account binding (`U/Projects/UOContent/Mobiles/PlayerMobile.cs:2200-2226`). Thus an ordinary bag can carry the warrant into another account's possession even though trading the warrant directly is refused.

The recipient still fails `Owns` and cannot use or directly lift the warrant. This is a transfer and potential item-loss defect, not a way to call another account's encounter. A paid warrant can leave its owner's custody inside a bag and be lost when that bag is deleted or decays. It violates the nontransferable contract in P565 line 56 and P629's claim that the item cannot go to ground or another account's container. The shared pattern predates P629, but the new warrant inherits this defect; the earlier warrant review did not report it.

**Fix:** enforce ownership for bound descendants when their containing item moves or trades. Evaluate layering alternatives before any upstream patch. A smaller warrant-only option is to refuse placement in movable subcontainers and allow only the owner's direct backpack/bank, with handling for any already saved nested warrant. A direct-item override alone does not close an ancestor move.

**Missing regression:** put a warrant into a real bag, then exercise the bag's ground drop and completed secure trade. Verify that no forbidden root change occurs, the same receipt survives, and ordinary bags without warrants still move normally. The existing binding fact calls only the warrant's handlers (`server/tests/Misc/LeagueInvestigationVerification.cs:267-284`), so every assertion there can pass while these routes remain open.

### 2. Medium (P2): missing map files can pass the safe-site gate

**Location:** `server/customizations/LeagueInvestigations/LeagueInvestigationCatalog.cs:197-201`, `:241-244`; placement at `server/customizations/LeagueInvestigations/LeagueInvestigationSeeder.cs:51-60`.

`CheckSite` describes a missing loaded facet as a refusal, but checks only whether the `Map` object is null or Internal. A Trammel object still exists when its map or static files are unavailable. `SpawnTiles` then relies on `GetAverageZ` and `CanSpawnMobile`, neither of which certifies that the underlying files were loaded.

Pinned `TileMatrix.GetLandBlock` returns a zero-filled fallback block when `MapStream` is null (`U/Projects/Server/TileMatrix/TileMatrix.cs:174`, `:293-298`). Missing static streams similarly return empty static data at line 223. Land tile ID 0 is not in the ignored-tile list at line 538. `Map.CanSpawnMobile` checks region spawning and physical fit, not stream availability (`U/Projects/Server/Maps/Map.cs:1104-1105`). With the test host's empty tile flags, the fallback therefore looks like open ground at Z 0. Missing statics can also erase real walls and obstacles from an otherwise loaded map.

P629's own verification record says the host had no map files, yet its seeder fact expects both sites to pass and receive markers (`server/tests/Misc/LeagueInvestigationVerification.cs:335-359`). That historical green result demonstrates the acceptance gap described here; it is not fresh verification by P641. The offline tile inspection in P629 does not make a later runtime file-loading failure safe. The seeder can certify and place a marker using fallback terrain instead of the intended facet data.

**Fix:** refuse site validation and spawn-tile generation unless the required land, static index, and static data sources are available. Preserve the existing fit and region checks after that prerequisite. Report missing data distinctly from an obstructed site. Do not treat the existence of `Map.Trammel` as proof its data loaded.

**Missing regression:** a missing-map case and a missing-statics case must refuse with no marker placement. Use explicit terrain fixtures or properly gated real-map cases for positive placement tests instead of requiring success on absent data. Observe the negative cases failing before the fix, then passing.

### 3. Medium (P2): the policy scan misses restricted regions hidden by priority or height

**Location:** `server/customizations/LeagueInvestigations/LeagueInvestigationCatalog.cs:206-213`, with ancestry-only filtering at `:165-179`.

The scan visits every X/Y coordinate, but asks `Region.Find` only at the site's center Z. That engine method returns the first containing region in priority order (`U/Projects/Server/Regions/Region.cs:291-311`, ordering at `:251-252`). `IsAllowedRegion` then visits only that region and its parents. It never examines an overlapping region that is not in that ancestry.

For example, a permitted, parentless `BaseRegion` at priority 100 can cover a forbidden `GuardedRegion` at priority 50. Every point resolves to the allowed region, so the site's region check passes despite the overlap. Separately, a restricted region whose vertical bounds cover a lower standing surface but exclude `site.Center.Z` is never sampled. `SpawnTiles` uses each tile's actual land Z, but does not apply `IsAllowedRegion` there. `CanSpawnMobile` is insufficient: an ordinary `GuardedRegion` inherits the permissive `AllowSpawn` behavior (`U/Projects/Server/Regions/Region.cs:869`).

P565 line 102 requires disabling a site when its policy footprint overlaps an incompatible special region. The current helper cannot guarantee that condition. This is a source-confirmed validation gap, not a finding that either shipped coordinate currently has such an overlap. Actual saved-world region composition remains unverified.

**Fix:** check the intended policy volume against all intersecting registered regions on that facet, including regions outside the winning region's parent chain. Define the vertical extent consistently with the future policy region. Also apply the allowed-region check at each actual candidate spawn point. Keep the existing parent-preservation requirement.

**Missing regression:** register an allowed higher-priority region over an independent forbidden region and require refusal. Add a restricted region at an actual standing Z different from the center's Z. The current helper creates only a full-height town (`server/tests/Misc/LeagueInvestigationVerification.cs:79-84`), and the region fact tests it without an allowed overlay (`:145-179`); neither case exercises these misses.

## Persistence, scope, and remaining evidence

The warrant declares generated serialization for bound account, encounter key, receipt ID, and ready/reserved state. Its existing round-trip fact checks all four and the derived name (`server/tests/Misc/LeagueInvestigationVerification.cs:297-318`). No source-confirmed save-format defect was found in this stage. A removed encounter key is preserved and refused rather than deleted. The marker declares generated serialization for its site key. Marker round-trip coverage and a withdrawn-key warrant round trip are still missing; these are coverage gaps, not proven data loss.

The moved Covetous site is disclosed and justified against the Void Pool exclusion. I did not independently reread the binary map files or walk either site, so P629's offline walkability counts remain its reported evidence. Its stated walkability heuristic and pending client/runtime checks are not promoted to runtime proof here. No boss implementation, loot path, bestiary reward path, or shop row was changed by P629.

The future runner must call the dynamic site gate again at final start. The current `LeagueInvestigationWarrant.CheckUse` checks the site's catalog `Enabled` flag only, and production `CheckSite` callers currently stop at the seeder. This is recorded as a required later integration check, not an additional missing-runner finding against stage 1. Likewise, active-run, cooldown, corpse, escrow, and refund persistence must be reviewed when their assigned stage exists.

Reviewed all three files under `server/customizations/LeagueInvestigations/`, `server/tests/Misc/LeagueInvestigationVerification.cs`, P629's changelog/version changes, the shared binding and climbing-boots precedent, bestiary spawn rows, music-region ancestry, and the pinned item, container, mobile, secure-trade, region, map, and tile-matrix paths cited above. Earlier P565/P629 reviews were read to avoid repeating findings.

No tests were added, changed, or run; no build or container operation was needed for this docs-only review. P629's red/green and full build results were read, not rerun. Current world placement, player/client behavior, and a real server save/restart remain unverified. No code, `docs/`, accounts, saves, or service configuration was edited. No Haven connection, deployment, commit, merge, push, or branch switch was performed.

## Review checks

Read both work copies' AGENTS.md and the required direction/task documents. Checked the stop-request path between review steps. Shell reads used Windows PowerShell 5.1. Ran `tools/progress.py --dry-run` with both work-copy path overrides; it exited successfully. The tool still writes `tools/progress.json` before checking its dry-run flag, so that snapshot was restored to its pre-review bytes. No generated progress change is retained. Both repositories pass `git diff --check`. This note is plain ASCII, has no trailing whitespace, and is below 5 MB. The code repository is unchanged, and this review note is the only deliverable.

P641 DONE
