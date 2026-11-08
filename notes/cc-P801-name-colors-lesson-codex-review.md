# Codex review: P801

CC task P801: rethink the New Haven 'Name Colors, Reputation and Guards' lesson. Reviewed by Codex (`codex exec review`, read-only) after P801 DONE and before the Golem's commit, 2026-11-06 09:38.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.98). The redesign largely implements the approved jail lesson and includes main/isle build logs and client proof. However, it introduces potential inventory loss, duplicate doors after reload, and incorrect guard instruction; builds and play tests were not independently rerun during this read-only review.

- **high** [P1] Prevent personal items from entering the disposable pouch (`server\customizations\Tutorial\TutorialJail.cs:273`)
  The marked pouch is an ordinary usable container, so a player can put their own gold or equipment inside it. Returning the pouch, cancelling the lesson, or leaving the area then deletes it recursively, permanently destroying those belongings. Use a non-container prop, reject deposits, or preserve its contents on every cleanup path.
- **medium** [P2] Teach the actual guarded-town rules for murderers (`server\customizations\Tutorial\TutorialJail.cs:66`)
  The new lesson says guards kill red players on sight, and `DoneText` also promises that calling guards kills any nearby murderer. Pinned ModernUO's `GuardedRegion.AllowReds` returns `Core.AOS`, so under this shard's AOS rules murder counts alone do not make someone a guard candidate. Ordinary criminal candidates also have a limited reporting window. Correct both explanations so the staged demonstration does not teach players to rely on protection the real guards will not provide.
- **medium** [P2] Recognize the existing door when it is saved open (`server\customizations\Tutorial\TutorialJail.cs:146`)
  If the world is saved while the jail door is open, `BaseDoor` persists its offset location and reopens there after loading. This check searches only the closed tile, so the load-time seed creates a second door. The overlapping doors remain after the original closes and can accumulate across restarts. Compare doors by their closed location, accounting for `Open` and `Offset`, to preserve the [building guide's idempotent-seeding requirement](D:/UO/golems/Iron/shard-migration/notes/guides/building-and-decorating.md#L358-L359).

(2.7 minutes, 1,110,575 tokens)

## shard-migration

Verdict: patch is incorrect (confidence 0.98). The supplied release implementation substantially delivers the requested redesign and includes build and client evidence. However, its disposable pouch can destroy player possessions, and its door seeding duplicates doors after an open-door save.

- **high** [P1] Prevent personal items from entering the disposable pouch (`notes\cc-P801-tools\p801-release-isle-20261028.diff:355`)
  If a trainee puts personal belongings into the marked pouch, returning it destroys those belongings: the loan is an ordinary usable `Pouch`, and `Item.Delete()` recursively deletes its contents. Leaving or cancelling the lesson also deletes the loan. Use a pouch that refuses deposits, or preserve non-lesson contents before every cleanup path.
- **medium** [P2] Recognize the jail door in its open position when seeding (`notes\cc-P801-tools\p801-release-isle-20261028.diff:228`)
  If the world is saved with the jail door open, the next load creates another door. Pinned `BaseDoor` moves its location by `Offset` when opened and preserves that state across deserialization, but this check searches only the closed tile. The original subsequently closes onto the replacement, leaving overlapping doors. Match the door's closed origin regardless of its current state and test reseeding an open door; the applicable [building guide](../guides/building-and-decorating.md#7-lessons-and-the-existing-world) requires idempotent world-load seeding.

(2 minutes, 1,114,632 tokens)
