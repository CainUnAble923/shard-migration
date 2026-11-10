# Codex review: P867

CC task P867: fix-up for P855 (CC task P855: port a data-driven decor addon, then the housing furnit. Reviewed by Codex (`codex exec review`, read-only) after P867 DONE and before the Golem's commit, 2026-11-10 12:49.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.92). The wall-box change and review artifacts address much of the request, but the modified fireplace's required player-placement and walking verification remains incomplete. The reported gated build passed; I did not independently rerun it.

- **medium** [P2] Verify the revised fireplace through player placement (`server\data\Decoration\Addons\holiday-fireplace.cfg:4`)
  The changed holiday fireplace still lacks the required player-path verification: `cc-P867-tools/run4/walk.txt` records its owner placement as FAIL, while the final town run uses `[DecorAddon place`, bypassing `BaseAddon.CouldFit`, and teleports the character into position. Those shots establish appearance but not that the revised design fits against an owned house wall or can be approached normally. Complete a successful deed placement and real-character walk around this fireplace, retaining the logs and shots requested by task steps 2???3.

(1.5 minutes, 757,482 tokens)

## shard-migration

Verdict: patch is incorrect (confidence 0.95). The requested review artifacts are substantially present, but wall-backed coverage and the real-character walkthrough remain incomplete. The imported probe also masks build and test failures. Server implementation changes are outside this repository diff and were not independently verified.

- **medium** [P2] Propagate compilation and test failures from the probe (`D:/UO/golems/Iron/shard-migration/notes/cc-P855-tools/probe-inner.sh:17`)
  If compilation fails, this pipeline returns `head`'s status and continues into `dotnet test --no-build`, which can exercise stale assemblies. The final reporting pipeline also masks a failing test command. P855's imported notes already record stale tests running after a compile error, so this is an observed failure mode rather than a hypothetical one. Stop on compilation failure and preserve the test exit status, consistent with the repository's [verification-gate requirement](../../AGENTS.md#L339-L345).
- **medium** [P2] Walk the final decorated rooms before clearing each design (`D:/UO/golems/Iron/shard-migration/notes/cc-P867-tools/kit/Walk867Town.py:111`)
  The final proof teleports the character to its screenshot position and immediately clears the furniture after shooting; its PASS lines only confirm teleport coordinates. The two startup steps occur before any furniture is placed, and run 4's steps likewise precede its placements. Consequently the requested real-character walkthrough of the changed decoration has not happened, and these logs cannot demonstrate that the decorated approaches remain traversable. Add client-driven approach and return walks after placement, following the [guide's real-walk procedure](../guides/building-and-decorating.md#L385-L386).
- **medium** [P2] Include the north- and west-facing couches in wall-backed proof (`D:/UO/golems/Iron/shard-migration/notes/cc-P867-tools/kit/Walk867Town.py:33`)
  The final run includes only the east and south couches, although `placed.md` explicitly describes the north and west variants as backed against south and east walls. Neither omitted variant has a new wall-backed shot or isorender, so the claim that every wall-backed design was checked is incomplete. Add both variants against their corresponding walls, including checking camera-side occlusion, as required by reviewer item 2 and the [guide's facing checklist](../guides/building-and-decorating.md#L39-L40).

(1.4 minutes, 548,006 tokens)
