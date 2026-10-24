# Codex review: P291

CC task P291: the tutorial's wing trials, part 2: gathering, crafting, animals, bard, thieving and t. Reviewed by Codex (`codex exec review`, read-only) after P291 DONE and before the Golem's commit, 2026-10-23 21:39.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.97). The requested trial categories and per-trial tests are present, but Fishing can finish without a catch, interrupted thieving trials can permanently retain borrowed Hiding, and unrelated lessons unnecessarily block each other. Builds and runtime tests were not independently rerun during this read-only review.

- **medium** [P2] Check only the placement tiles required by each trial (`server\customizations\Tutorial\TutorialTradeTrials.cs:292`)
  While one trainee is smithing, their anvil and forge occupy the same fixed tiles checked by this default branch for every gathering and crafting lesson. Consequently another trainee cannot even start Camping or Tailoring, which place no props at all; `Fits` rejects the first trainee's equipment and repeatedly reports that staff assistance is needed. Give prop-free lessons an empty placement list and allocate independent locations for lessons that need physical props.
- **medium** [P2] Persist the original Hiding value before changing its base (`server\customizations\Tutorial\TutorialTradeTrials.cs:455`)
  If the world saves during the thieving trial and the server subsequently restarts, the raised Hiding base is saved on the character but `HidingBefore` exists only in the in-memory trial. Login cleanup cannot restore it because `Active` is empty after restart, permanently granting up to 30 Hiding instead of returning the loan. Persist recovery information or restore the real base around serialization so an interrupted lesson cannot permanently change the character.
- **medium** [P2] Wait for a caught item before completing Fishing (`server\customizations\Tutorial\TutorialTradeTrials.cs:575`)
  A successful Fishing skill check does not guarantee a catch: pinned `HarvestSystem.FinishHarvesting` subsequently calls `Fishing.MutateType`, which can return null. Completing the trial here immediately removes the fishing pole, pond and skill loan, so a trainee can receive ???done??? followed by ???fail to catch anything,??? with no harvest and no opportunity to retry. Check that the harvest actually yielded an item before finishing; the current test injects a successful roll and cannot catch this case.

(2.8 minutes, 1,043,957 tokens)

## shard-migration

Verdict: patch is incorrect (confidence 0.99). The added play-test runner falsely fails supported reruns, as its own Alchemy log confirms. The server implementation and CHANGELOG are outside this repository's diff, so their correctness could not be independently verified here.

- **medium** [P2] Skip fresh-character assertions when rerunning selected trials (`notes\cc-P291-tools\tradetrials.py:482`)
  When `--only` reuses a character whose core is already complete, this unconditional call runs `play_core` with its fresh-character assertions enabled. Rook correctly displays the unlocked wings, but the runner records a failure and exits 1 even if the selected trial passes. The supplied `playlog-alchemy-rerun.txt` demonstrates exactly this failure. Detect completed core progress or disable the fresh-character assertions for resumed runs.

(0.8 minutes, 265,153 tokens)
