# Codex review: P855

CC task P855: port a data-driven decor addon, then the housing furniture batch. Reviewed by Codex (`codex exec review`, read-only) after P855 DONE and before the Golem's commit, 2026-11-10 08:06.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.92). The requested furniture data and store integration are present, but reloading a removed design can break an outstanding placement target. Successful player housing placement and redeeding also remain unverified despite the explicit completion requirements. I did not rerun the Docker gates.

- **medium** [P2] Verify successful placement and chopping in an owned house (`server\tests\Misc\ShardDecorAddonVerification.cs:303`)
  This test constructs `deed.Addon` directly and only invokes the real placement target outside a house. The proof notes likewise explicitly omit player placement inside an owned house. Consequently neither the tests nor the screenshots establish the central requested behavior: successful placement, deed consumption, house addon registration, and chopping back into a usable deed. Add an owned-house placement/redeeding test and the corresponding player proof before declaring completion; this also supplies the player-reaching subsystem coverage required by [AGENTS.md](D:/UO/golems/Iron/ShatteredLegacy/AGENTS.md#L152-L154).
- **medium** [P2] Revalidate the selected design when placement completes (`server\customizations\Items\Addons\ShardDecor\ShardDecorAddon.cs:475`)
  If staff removes or invalidates a design and runs `[DecorAddon reload` while a player has its placement cursor open, `Design` still names the removed file. Completing the target constructs an empty `ShardDecorAddon`; pinned `BaseAddon.CouldFit` then skips its component loop and dereferences the null house at `house.Doors`. Revalidate at target completion and refuse placement while retaining the deed instead of allowing this exception.

(1.9 minutes, 637,762 tokens)

## shard-migration

Verdict: patch is incorrect (confidence 0.94). The submitted proof omits successful player installation, and the probe can silently test stale assemblies after compilation fails. The server implementation is outside this repository's changes, so its correctness could not be independently established from this diff.

- **medium** [P2] Preserve build and test failures in the probe (`notes\cc-P855-tools\probe-inner.sh:17`)
  When compilation fails, the pipeline returns `head`'s status and execution continues into `dotnet test --no-build`, potentially testing stale assemblies; test failures are likewise masked by the final reporting pipeline. The notes acknowledge that an earlier compile error caused unchanged tests to run. Propagate both commands' failure statuses and stop before testing after a failed build, consistent with the repository's requirement that verification failures actually fail ([AGENTS.md](../../AGENTS.md#L339-L345)).
- **medium** [P2] Prove successful player placement before marking the task done (`notes\cc-P855-decor-addon-housing-furniture.md:142`)
  The proof stops at rejecting placement outside a house; all furniture screenshots use a staff command that bypasses house placement checks. Consequently, it does not establish that players can actually install their purchased furniture, the central behavior required by the prompt's ???Working in game??? criterion. Stage an owned house and demonstrate successful placement and redeeding before declaring completion.

(0.9 minutes, 285,588 tokens)
