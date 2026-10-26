# P645: review of P633 weapon milestones

Reviewed October 26, 2026. Notes only. No code changes.

P633 implements the selected level-100, 100-point, one-proc PvE slice, including saved purchases, elemental damage, and owner/weapon cooldowns. This review adds the findings below. It does not establish readiness for player release.

## Scope and earlier reviews

`S/` is `D:/UO/golems/Verite-tower/ShatteredLegacy`, HEAD `a3f017e279e29eed0ac12c506ef51e6310291583`. P633's code commit is `46240ff35e546ae890b88ad2c93c8ff899fa2446`, merged by `9fc71c8`. `M/` is `D:/UO/golems/Verite-tower/shard-migration`, initial HEAD `2c3d9ace7b99be87de6aa06dec23d78d575d60a0`. These are the local source snapshots reviewed, not deployed server state. No fetch was performed.

Read both work-copy agreements, the required direction/task documents and governing-document index, both `cc-P633-*.md` notes, the P569 design and its review, P534's comparison, and P482's earlier gear review. Also read the completed P633 task prompt and Chase's October 25, 20:15 decision in `D:/UO/overseer/decisions-2026-10-23.md`: "P569 level 100 one PvE proc."

The earlier [P633 review](cc-P633-build-procs-milestone-codex-review.md) already reports the unenforced test-shard restriction and the unconnected proc tooltip. Both remain visible in this snapshot; neither is repeated as a new finding. P633 explicitly defers real acting-level dormancy, shared imbuing/intensity accounting, broader weapon/special-move coverage, and scratch-client/world acceptance. Those deferred stages are not new defects here. P482's older ordinary-gear findings are also excluded.

## Findings

### 1. Medium (P2): confirmation can charge more than the displayed price

**Where:** `S/server/customizations/LevelGear/LevelGearMilestoneGump.cs:118`, `:138`, `:165`; `S/server/customizations/LevelGear/LevelGearProcs.cs:277`, `:299`.

**What happens:** The confirmation retains only the player, weapon, and proc key. Its displayed price comes from the setting when the page is built. On reply, `Buy` reads the current price and deducts it without comparing it with the price shown. Open a 100-point confirmation on a level-100 weapon with 440 points, raise `pointCost` to 200 while it is open, then confirm: the source path accepts the purchase and deducts 200. The player agreed to 100. Affordability and ownership checks still work; they do not protect the quoted terms. An unlock-setting change can likewise change the saved requirement after the confirmation was shown.

**Fix:** Retain a server-side quote of the displayed price and unlock. If either changes, leave points and purchase state untouched and show a refreshed confirmation. Continue to run the authoritative purchase validator against current ownership, eligibility, settings, points, and slots. Do not accept a client-supplied price or honor an obsolete cheaper quote.

**Missing regression:** Drive the actual confirmation response after increasing the price while the weapon can still afford it. Assert no deduction or purchase until the new terms are confirmed. Include an unlock change. P569's purchase acceptance explicitly calls for a setting change between replies; the current facts call `Buy` directly and do not exercise either gump.

### 2. Medium (P2): temporarily damage-immune creatures can consume a proc

**Where:** `S/server/customizations/LevelGear/LevelGearProcs.cs:403`, `:338`, `:343`; supporting content at `S/server/customizations/Mobiles/Normal/ChestMimic.cs:594` and `:615`.

**What happens:** `IsTarget` checks `Blessed` and `CanBeHarmful`, but never `CanBeDamaged()`. A chest mimic with its lid shut is alive, wild, non-blessed, and temporarily refuses damage through that override. A weapon hit reaching this state before the mimic reopens can still reach the milestone roll and consume both cooldowns, with a visual and no actual damage.

This is not prevented by the positive `damageGiven` guard: pinned `U/Projects/UOContent/Misc/AOS.cs:239` calls the void `Mobile.Damage` and returns its calculated damage at `:240`. `U/Projects/Server/Mobiles/Mobile.cs:5963` can reject that damage without changing the returned AOS value. `U/Projects/UOContent/Mobiles/PlayerMobile.cs:1647` rejects `IsInvulnerable`, but does not cover the mimic's separate `CanBeDamaged` override. P569 requires an eligible damaging strike and no invulnerable target before drawing RNG.

**Fix:** Recheck the target's current `CanBeDamaged()` before rolling or reserving cooldowns, alongside the existing target checks. Preserve the rule that a legitimate proc still reserves cooldown before its own effect, even if a later mitigation hook reduces that effect to zero.

**Missing regression:** Drive a real equipped weapon's `OnHit` against a shut mimic, assert unchanged hits, no milestone RNG call, and no owner or weapon timer. Reopen it and verify the same weapon can attempt normally. The present zero-damage test supplies zero directly to the service; it does not cover a positive AOS return for rejected damage. This scenario is established by source tracing, not a client or runtime reproduction in P645.

### 3. Medium (P2), coverage gap: restart protection is untested for a live weapon cooldown

**Where:** `S/server/tests/Misc/LevelGearProcVerification.cs:375`, `:385`, `:401`; implementation at `S/server/customizations/LevelGear/LevelGearProcs.cs:162` and `:193`.

**What happens:** The persistence fact saves an unexpired owner timer but deliberately makes the only weapon timer expired. After load, it expects the weapon map to be empty. It therefore passes if persistence drops every weapon cooldown. The trade test checks an in-memory timer only. Together they leave the specific restart-then-transfer bypass unguarded: a regression could load the owner's timer correctly while letting a different owner use the same weapon immediately after restart.

**Fix:** Add a buffer round trip with both maps unexpired, clear both maps, and advance the injected clock during the simulated restart. Transfer the restored weapon to another player with no owner timer. Assert no roll just before the saved weapon deadline and an attempt exactly at it. Keep a separate expired/deleted-entry case. Prove the new regression fails when weapon-map persistence is omitted, then passes after restoration.

The current serializer and reader use matching field order for both maps; no existing timer-loss bug is claimed. This finding concerns the missing executable guarantee for the trade-reset rule. It is narrower than P633's already disclosed lack of full-world restart acceptance. Unknown-key preservation and unsupported-version rejection also have no assertions in this proc persistence fact, although both corresponding source branches are present.

### 4. Low (P3): a disabled purchased effect is displayed as ready

**Where:** `S/server/customizations/LevelGear/LevelGearMilestoneGump.cs:39`, `:50`; entry visibility at `S/server/customizations/LevelGear/LevelGearGump.cs:46`.

**What happens:** Purchased weapons retain their Milestone button while the feature is off. The bound-effect page always advertises the current chance and says `Your cooldown: ready` when the owner's timer has expired. It never checks global enablement or whether that particular choice is disabled. After the stage-one switch is turned off or the server restarts, a player can see a ready proc that cannot fire. The title also uses the current global unlock instead of the purchase's saved `RequiredLevel`, so later unlock tuning mislabels existing purchases. This is separate from the earlier missing-tooltip finding.

**Fix:** Show an explicit unavailable/disabled status for a bound effect, and display its saved required level. Keep viewer-specific readiness on this page. Add response/layout coverage for global off, choice off, and an unlock setting changed after purchase. Acting-level dormancy remains the separately scheduled stage.

### 5. Low (P3): the new cooldown maps never prune expired or deleted entries from memory

**Where:** `S/server/customizations/LevelGear/LevelGearProcs.cs:149`, `:166`, `:332`, `:411`.

**What happens:** Saving filters entries into a temporary list, but removes none from either dictionary. Access also leaves expired entries in place. Every distinct owner and weapon that ever procs remains represented until restart, including destroyed weapons. Save work consequently follows historical participants rather than only live cooldowns. P569's persistence section explicitly requires pruning on access and save. This concerns P633's new timer maps, not the older `LevelGearStore.Rows` cleanup issue already reported in P482.

**Fix:** Remove expired/deleted entries safely on the game thread, with cleanup coordinated with save enumeration. Add an assertion against the in-memory maps after cleanup, including a deleted weapon and an expired owner, while retaining a future deadline. The existing save fact proves only omission from disk. No memory or save-time impact was measured here.

## Source checks and limits

Read all P633-listed implementation and test files: `S/server/customizations/LevelGear/LevelGearProcs.cs`, `LevelGearMilestoneGump.cs`, `LevelGearGump.cs`, `ClusterFLevelGear.cs`, `S/server/patches/BaseWeapon-level-gear-proc-hit.patch`, its registration in `S/docker/uo/apply-patches.sh`, `S/server/tests/Misc/LevelGearProcVerification.cs`, `S/CHANGELOG.md`, and `S/VERSION`. Followed relevant existing imbuing/AOS patches and companion ownership, and inspected pinned melee, ranged, thrown, Double Strike, Whirlwind, damage, and persistence paths. `U/` is the clean read-only `D:/UO/ModernUO-pinned` checkout at `d4531cd94b739613155225c234900de9f47d2c88`, matching `S/docker/uo/Dockerfile:3`. No `server/uo/` source was read.

The base-hit patch is inside the positive-damage branch, after native weapon effects and before creature/ability callbacks. Owner and weapon cooldowns are reserved before the elemental effect and protected by a `finally`-cleared reentry guard. Purchase checks reject dead players, lost possession, repeat purchases, insufficient points, and full gear-side slots. The version-1 purchase writer/reader order matches, version-0 rows load without a proc, and unknown keys are retained but do not dispatch. UTC timestamps use ordinary `Write(DateTime)` and `ReadDateTime`, so the inspected format preserves absolute deadlines rather than restarting a duration. These are source observations, not runtime passes.

No build, server test, scratch shard, client session, or live save inspection was performed. P633's reported red/green runs and gated build were read but not independently rerun. Actual UI rendering, companion damage credit, recursion through native hooks, weapon/special-move integration beyond the existing katana fact, full world persistence, and combat balance remain unverified here. No new tests were added in this docs-only task.

The required progress reporter completed with `--dry-run` and both work-copy path overrides. Its incidental `progress.json` write was suppressed in memory; no generated file was changed. Document checks use Windows PowerShell 5.1.26100.9711. Final checks cover whitespace, plain ASCII punctuation with no em dashes, file size below 5 MB, unchanged code work copy, and only this requested note changed in the migration copy. No Haven connection, deployment, commit, merge, push, or branch switch was made.

P645 DONE
