# P544: review of P412 chopped tree visuals

Reviewed October 24, 2026. Notes only. No code changes, new tests, builds, deployments, live connections, commits, or branch changes.

P412 code commit `b97dead4d976f206ea4f5ce3451e4e3ea8095016` is in local `main`. The production customization, client patch, and stump tests in this work copy match `main`.

## Findings

1. **bug | `server/customizations/ClusterFLumberStumps.cs:122`, `:136` | Fruit-tree trunks are excluded from tree resolution.** Harvestable fruit foliage can have a trunk that is neither harvestable nor flagged Foliage, so exhausting the peach tree at Trammel (1126, 2285) hides only its leaves, and targeting apple foliage at (1420, 1425) places the stump at Z 5 instead of its trunk's Z 4. Resolve associated trunk art independently of harvest eligibility, include it in the hide list, and add fruit-tree cases with equal and differing trunk/leaf elevations.

2. **bug | `server/customizations/ClusterFLumberStumps.cs:135`; `client/patches/0006-exhausted-trees.patch:144` | The hide list can include another tree at the same spot.** Resolution includes every harvestable trunk within 30 Z above the target, so exhausting Yew art 0x12B7 at Trammel (587, 1636, 0) also hides trunk art 0x0D86 at Z 20; the client additionally matches only facet, X, Y, and graphic, which cannot distinguish repeated art at different heights. Select components belonging to the targeted tree, carry their Z through the packet and client lookup, and cover unrelated stacked trunks and repeated graphics above the selection range.

3. **bug | `client/patches/0006-exhausted-trees.patch:45` | A hidden tree can remain the mouse target.** With the cursor and camera stationary, pinned TazUO reuses its selected static through `GameScene.IsWorldSelectionValid`, which never calls the new `CheckMouseSelection` guard, so a previously selected trunk can disappear while remaining selected for targeting. Reject exhausted statics in cached-selection validation and invalidate the selection when visibility changes, with a regression case that receives exhaustion while the cursor stays over the tree.

4. **risk | `server/customizations/ClusterFLumberStumps.cs:100`; `server/tests/Engines/Harvest/ChoppedTreeStumpsVerification.cs:301` | The single-tile fixtures miss multipart trees.** Existing jungle trees have connected trunk and canopy pieces on neighboring tiles, but resolution examines only the targeted tile, so the full-tree disappearance claim does not extend to them. Add a multipart map fixture and either extend the message to identify each component's position or explicitly limit the promised behavior to trees whose parts share one tile.

## Evidence

Read `notes/cc-P412-chopped-tree-visuals.md` and its adjacent Codex review first. Its finding about foliage below the trunk is excluded from this list. Also read the P359, P380, and P400 notes/reviews for context; the previously reported carrier-axe refusal and lifecycle test gaps are not repeated here.

Reviewed these P412 deliverables and their supporting source:

- `server/customizations/ClusterFLumberStumps.cs`
- `server/tests/Engines/Harvest/ChoppedTreeStumpsVerification.cs`
- `server/tests/Route/TestTileRows.cs`
- `client/patches/0006-exhausted-trees.patch`
- `client/README.md`, `CHANGELOG.md`, and `VERSION`
- `server/patches/HarvestBank-lumber-stumps.patch`, its build registration, and `ClusterFLumberjackingExtension.cs`
- The packet proof, result, and log in `notes/cc-P412-tools/`

Verified read-only ModernUO source at `D:/UO/ModernUO-pinned`, commit `d4531cd94b739613155225c234900de9f47d2c88`, including StaticTarget, Lumberjacking's actual tile list, HarvestDefinition.Validate, TileData, and HarvestTarget. The shard's lumber extension does not add the missing fruit trunks to that list.

Read the existing patched client source at `D:/UO/golems/Iron/tazuo-p412/src`, whose HEAD matches `client/TAZUO_COMMIT`, `3212623f63436be1c0f4e3b308b202b29597c026`. The cache path cited in finding 3 is unchanged upstream code: `src/ClassicUO.Client/Game/Scenes/GameScene.cs:761` and `:780`, with static validation in `GameSceneDrawingSorting.cs:700`. Its static case returns true without checking the exhausted-tree list. The patch changes drawing and fresh pixel selection, and does not change that cache path.

Read binary records directly from `D:/UO/tool-trials/client-data-copy/staidx1.mul`, `statics1.mul`, and `tiledata.mul`, using the pinned formats. The relevant records are:

| Trammel position | Static records | Consequence under the reviewed conditions |
| --- | --- | --- |
| (1126, 2285) | 0x0D9C peach trunk Z 0; 0x0D9E peach foliage Z 0 | Only 0x0D9E passes the component filter. |
| (1420, 1425) | 0x0D98 apple trunk Z 4; 0x0D99 foliage Z 5 | The foliage is harvestable; the trunk is not, so base resolution retains Z 5. |
| (587, 1636) | 0x12B7 Yew trunk Z 0; 0x0D86 tree piece Z 20 | Both pass the 0 through 30 component filter when targeting the Yew. |
| (5363, 3149) | 0x0D57 Z 17; 0x0D57, 0x0D5A, and 0x0D67 Z 18 | Repeated graphic IDs at differing elevations occur in the actual data. |

None of these blocks appears in `stadifl1.mul`, so the static-diff overlay does not replace the cited records. These are local data observations, not confirmation of the files used by a running shard or a player's client.

For finding 4, the same map has trunk/foliage pairs 0x0D42/0x0D48 at (1049, 3176, 0), 0x0D43/0x0D49 at (1050, 3175, 0), and 0x0D44/0x0D4A at (1051, 3174, 0). Pinned TazUO explicitly groups this canopy in `GameSceneDrawingSorting.cs:25` and walks neighboring positions in `IsFoliageUnion` at `:244`. The new hide list does not follow those component positions. This is a coverage and scope risk because P412's original prompt explicitly specified matching at one X,Y.

## Other requested checks and limits

- **Visibility:** `ClusterFLumberStumps.cs:260` broadcasts to all connected players, and `:279` supplies every live exhausted tree at login. Hiding is shared among supported clients, including observers who never chopped. P412's notes explicitly choose this and its original prompt tells the server to notify clients on login/range entry, so I found no evidence of a required chopper-only view and do not label the shared behavior a bug.
- **Height:** Subtracting StaticTarget.CalcHeight fixes the original raised-target error for ordinary single-tile trees; dynamic Static targets keep their own location. Finding 1 identifies a separate remaining base-resolution problem.
- **Polearms:** The equipped BasePoleArm/Lumberjacking pattern accepts Bardiche and reaches cliloc 500493. The existing Bardiche fact checks double-click and IChoppable message output; it calls IChoppable directly rather than driving an actual HarvestTarget. No new polearm defect found.
- **Missing tests:** The fixtures cover same-tile 0x0CCD/0x0CCE parts, an unrelated wall, packet contents, manager expiry/reset, and the Bardiche message. They do not cover fruit trunks, unrelated stacked trees, multipart components, or the cached mouse-selection route identified above. Client manager tests do not exercise StaticView drawing.
- **Runtime limits:** No lane tests were requested or run. No new tests were authored, so there is no new red/green claim. The binary probes and source checks support these findings; the proposed fixes, actual rendered appearance, and stationary-cursor behavior remain unverified in a running client. P412's reported build and test results were read, not rerun.

Ran `tools/progress.py --dry-run` with both work-copy path overrides, exit 0. Its existing dry-run side effect rewrites `tools/progress.json`; restored the original bytes immediately, preserving the notes-only deliverable.

Final checks: code work copy clean; only this note added in the notes work copy; progress.json unchanged; whitespace, UTF-8, file size, and no-em-dash checks passed. Windows PowerShell was verified as 5.1. No stop request was present at the final checkpoint.

P544 DONE
