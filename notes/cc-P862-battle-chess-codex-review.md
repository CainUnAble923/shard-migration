# Codex review: P862

CC task P862: port Battle Chess in the New Haven inn. Reviewed by Codex (`codex exec review`, read-only) after P862 DONE and before the Golem's commit, 2026-11-10 16:21.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.98). The implementation substantially fulfills the task, with seeding, credits, tests and documented client proof. However, interrupted captures leak pieces, spectators can hide pieces, and the castling shortcut can execute unintended moves. Review was static; builds and client tests were not rerun.

- **medium** [P2] Restrict rook-target normalization to legal castling moves (`server\customizations\BattleChess\ChessRules.cs:672`)
  Targeting an own rook can silently execute an unrelated ordinary king move. For example, with `ChessPosition.FromText("Kd1 Ra1 ke8")`, requesting d1???a1 is rewritten to d1???c1 and accepted, despite there being no castling rights. Resolve this shortcut only against generated castle moves; otherwise refuse the own-rook target instead of moving the king to an unselected square.
- **medium** [P2] Protect chess pieces from spectator invisibility spells (`server\customizations\BattleChess\BattleChessPiece.cs:162`)
  A nearby player can cast Invisibility on these pieces and hide either side's army during a game. Pinned `InvisibilitySpell.Target` accepts plain mobiles through `CheckBSequence`, and neither Blessed nor this `CanBeHarmful` override blocks beneficial spells against the piece. Since the port removed the original region's invisibility protection, add equivalent protection so spectators cannot hide the pieces players need to see and select.
- **medium** [P2] Keep captured pieces tracked until their animation finishes (`server\customizations\BattleChess\BattleChessGame.cs:418`)
  If staff stops the game or deletes the board while a capturing piece is approaching its victim, the victim remains in the world indefinitely. It has already been removed from `_pieces`, so `Clear()` misses it; clearing the mover stops its walking timer before `Strike()` can delete the victim. Track pending victims separately and include them in cleanup. The current tests bypass this lifecycle with `Instant = true`.

(2.5 minutes, 982,728 tokens)

## shard-migration

Verdict: patch is incorrect (confidence 0.96). The supplied artifacts document successful gated builds and private-client gameplay, but the red/green verification violates the required build/test route. This review covers the docs repository; the production implementation and tests are outside this diff.

- **medium** [P2] Run the red/green probes through the required build gate (`notes\cc-P862-tools\probe-inner.sh:9`)
  The recorded red/green runs use this script to invoke `dotnet build` and `dotnet test` directly in the P861 builder image, despite the task explicitly requiring all building and testing through `docker/uo/build.sh`. This bypasses the canonical patch/application and test pipeline described in [AGENTS.md](../../AGENTS.md#dockeruobuildsh-is-the-build-command). The later gated green builds do not demonstrate the red cases through that pipeline. Route the probes through `build.sh` and repeat the red/green verification.

(0.9 minutes, 312,983 tokens)
