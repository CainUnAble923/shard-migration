# Codex review: P838

CC task P838: fix-up for P820 (CC task P820: overseer fix-up for P801 (Name Colors jail lesson): its. Reviewed by Codex (`codex exec review`, read-only) after P838 DONE and before the Golem's commit, 2026-11-08 04:21.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.98). The requested bar and divider fixes are implemented, with upgrade cleanup and supporting proof artifacts. However, the imported lesson implementation leaves its main instruction window stale throughout step progression, confirmed by the supplied client screenshot. Builds and client runs were not independently rerun.

- **medium** [P2] Route step refreshes through the jail-specific window (`server\customizations\Tutorial\TutorialWingTrials.cs:310`)
  After each name click, `Step` calls `Refresh`, which still opens `TutorialWingTrialGump` instead of updating `TutorialJailGump`. Consequently, the jail window keeps saying everyone is ???Not met yet,??? never reveals the color explanations, and continues requesting name clicks after all five are complete; a second generic window also obscures the hall. This is visible in the supplied `shots-main/3z-window-all-five.jpg`. Apply the jail-specific routing to `Refresh` as well as `Show`, and verify the window's updated contents rather than merely its continued existence.

(0.8 minutes, 386,938 tokens)

## shard-migration

Verdict: patch is incorrect (confidence 0.98). The requested bar and partition fixes have updated renders, client shots, placement records, and build evidence. However, the imported implementation and replacement release diff still introduce inventory loss, duplicate-door seeding, and incorrect guard instruction relative to HEAD. Tests were not independently rerun during this read-only review.

- **high** [P1] Preserve player belongings inside the disposable pouch (`notes\cc-P838-tools\p838-release-isle-20261028.diff:428`)
  The replacement release diff lends an ordinary `Pouch`, which accepts personal gold and equipment, then deletes it recursively when returned. A trainee who stores belongings inside loses them permanently; cancellation cleanup poses the same risk. Reject deposits or preserve player-owned contents on every cleanup path.
- **medium** [P2] Teach the configured guard rules for murderers (`notes\cc-P838-tools\p838-release-isle-20261028.diff:158`)
  On this AOS-enabled shard, pinned `GuardedRegion.AllowReds` returns true, and murder counts alone do not make someone a guard candidate. This completion text nevertheless promises that calling guards kills any nearby murderer; Black Tam's introduction also promises death on sight. Correct both explanations so players do not rely on protection the actual guards will not provide.
- **medium** [P2] Recognize an existing jail door saved open (`notes\cc-P838-tools\p838-release-isle-20261028.diff:260`)
  When a world saves with the jail door open, pinned ModernUO's `BaseDoor` preserves its offset position. Searching only the closed tile therefore seeds a second door on load, leaving overlapping doors when the original closes. Match the closed origin using `Open` and `Offset`, and test reseeding an open door, as required by the [idempotent-seeding rule](../guides/building-and-decorating.md#L358-L359).

(1.2 minutes, 469,342 tokens)
