# Codex review: P820

CC task P820: overseer fix-up for P801 (Name Colors jail lesson): its build review said FAIL. Reviewed by Codex (`codex exec review`, read-only) after P820 DONE and before the Golem's commit, 2026-11-08 01:00.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.99). The placement fixes and upgrade logic address the four reported items, with build and client evidence supplied. However, the integration leaves the lesson's dedicated window stale after completed steps and opens an obstructing generic window instead.

- **medium** [P2] Refresh the jail-specific window after each completed step (`server\customizations\Tutorial\TutorialTradeTrials.cs:689`)
  During the jail lesson, `Step` calls `Refresh`, which always opens `TutorialWingTrialGump` instead of updating `TutorialJailGump`. Consequently, the jail window retains stale instructions and ???Not met yet??? labels while another window covers the hall. This is visible in `3z-window-all-five.jpg`: all five generic steps are done, but the jail window still asks the player to meet everyone. Route jail updates through its specialized window, including after returning the pouch and reading the ledger. This also violates the next-step requirement in [the building guide](../shard-migration/notes/guides/building-and-decorating.md#L39).

(0.9 minutes, 597,231 tokens)

## shard-migration

Verdict: patch is incorrect (confidence 0.99). The four placement fixes appear implemented, with screenshots and successful build logs. However, the imported P801 implementation and replacement release diff still ship inventory loss, duplicate-door seeding, and incorrect guard instruction.

- **high** [P1] Prevent personal belongings from entering the disposable pouch (`notes\cc-P820-tools\p820-release-isle-20261028.diff:394`)
  If a trainee puts gold or equipment inside the marked pouch, returning it destroys those belongings: this is an ordinary usable `Pouch`, and `JailPutBack` deletes it recursively. Cancellation and loan cleanup have the same risk. Reject deposits or preserve player-owned contents on every cleanup path before shipping this release diff.
- **medium** [P2] Teach the actual guarded-town rules for murderers (`notes\cc-P820-tools\p820-release-isle-20261028.diff:157`)
  Under this shard's AOS rules, pinned `GuardedRegion.AllowReds` is true, so murder counts alone do not make someone a guard candidate. This completion text nevertheless promises that calling guards kills any nearby murderer, and Black Tam's introduction also claims guards kill him on sight. Correct both explanations so the lesson does not teach players to rely on protection the real guards will not provide.
- **medium** [P2] Recognize an existing door saved in its open position (`notes\cc-P820-tools\p820-release-isle-20261028.diff:253`)
  If the world saves while the jail door is open, load-time seeding creates another door because this check searches only its closed tile. Pinned `BaseDoor` offsets its location when opened and preserves that state across loading; the original then closes onto the replacement. Match doors by their closed origin, accounting for `Open` and `Offset`, and test reseeding an open door. This also violates the [building guide's idempotent-seeding requirement](../guides/building-and-decorating.md#L358-L359).

(1.5 minutes, 719,198 tokens)
