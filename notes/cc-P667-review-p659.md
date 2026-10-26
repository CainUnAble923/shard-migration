# P667: review of P659

Reviewed October 26, 2026. Notes only. Reviewed code commit
`ca2f941ce0052b404a890d02df0a11c2acd773ef`, merged at code HEAD `28a2093`.
The notes work copy started at `c6967ee`. Pinned ModernUO was clean at
`d4531cd94b739613155225c234900de9f47d2c88`.

## Findings

No new actionable findings. P659 addresses both Medium findings in
`notes/cc-P657-review-p647.md` on the paths reviewed. No code change is proposed.

## What was checked

**Courier replacement across restarts:**
`server/customizations/ClusterFExchangeLetter.cs:100-111` deletes the losing
letter in either load order. When a later-expiring letter replaces the current
one, it enters the table before the old one is deleted. The identity check in
`OnAfterDelete` at `:122-124` therefore preserves the winner's entry. When the
later-expiring letter loads first, the older letter deletes itself instead.
Deletion makes the replacement survive subsequent saves without adding saved
fields. The payment path in `server/customizations/ClusterFPersuasion.cs:542-582`
still rejects a deleted or non-outstanding letter before awarding practice.

The regression at `server/tests/Skills/PersuasionVerification.cs:720` covers
both load orders, followed by delivery or deletion of the winner, another
restart, and an attempted delivery of the loser. The single-letter control at
`:768` checks that a valid letter can still pay. Its restart helper at `:692`
clears the actual registry and invokes the actual hook, but does not serialize
or reconstruct a world. That limitation is correctly disclosed in P659's note.

**Separate crimes in the same moment and place:**
`server/customizations/ClusterFGuardWitness.cs:401-404` now accepts only an open,
victimless criminal flag as the existing incident, and only a callback naming a
victim can complete it. An incoming victimless crime always starts an incident.
A completed aggression or assist cannot be reopened by that matcher. The merge
at `:320-325` sets the kind, victim and action location and removes witnesses
who cannot see that location.

The pinned engine raises the flag before the aggression or assist callback on
the ordinary paths inspected: `Projects/Server/Mobiles/Mobile.cs:8297-8315` and
`:8386-8404`, with the region calls at `:3930` and `:4537`.
`server/patches/GuardedRegion-witness-observe.patch` observes those callbacks.
The new regression at `server/tests/Regions/GuardWitnessVerification.cs:291`
keeps the clock and culprit position fixed, introduces a newcomer after the
first attack, and requires separate incidents for a victimless crime and a
second attack on the same victim. It also checks that the newcomer is absent
from the first attack. Existing attack, assist, sight and pet controls were
read alongside it.

The action matcher still relies on callback order. P659 already discloses the
unmatched-flag and duplicate-flag limitations. The independent pet-owner
suppression defect is already reported in
`notes/cc-P647-fix-weekend-review-findings-codex-review.md` and explicitly left
outside P659. Those existing findings and limitations are not counted again.

## Scope and verification limits

Read both work-copy `AGENTS.md` files, the direction decision and task-list
instructions, both `notes/cc-P659-*.md` files, P657's review, and the earlier P647
inline review to avoid repeating its finding. Read the complete P659 diff and
the listed production and test files:

- `server/customizations/ClusterFExchangeLetter.cs`
- `server/customizations/ClusterFGuardWitness.cs`
- `server/tests/Skills/PersuasionVerification.cs`
- `server/tests/Regions/GuardWitnessVerification.cs`
- `CHANGELOG.md` and `VERSION`

Also traced the supporting Persuasion issuance and delivery code, the guard
observation patch, the test clock, and pinned mobile crime callbacks, item
deletion, persistence and startup timer order. The version and changelog agree
on `2026.10.26.10` and describe the changes reviewed. The generated `server/uo/`
tree was not used.

Lane tests are none. No tests were added or changed. P659's reported failing
then passing regressions and gated build were read, not independently rerun.
Full world save/load behavior, actual legacy letter stockpiles, and client
gameplay remain unverified. The deferred hook was not exercised through the
serialization generator in this review. Pinned startup loads the world before
slicing timers (`Projects/Server/Main.cs:672`, `:725`), and its zero-delay
`Timer.DelayCall` schedules a callback rather than invoking it inline
(`Projects/Server/Timer/Timer.DelayCall.cs:31-53`). These source checks do not
replace a full restart test.

No Docker build, container, shard startup, save/account operation, or Haven
connection was performed. No code, `docs/` file, branch or commit was changed.
The required progress reporter completed with `--dry-run` and both work-copy
path overrides; its incidental `tools/progress.json` write was suppressed in
memory so generated files stayed unchanged.

Both repositories passed `git diff --check`. The note passed ASCII, no-em-dash,
trailing-whitespace and size checks. Windows PowerShell was 5.1.26100.9711. The
code work copy is clean; this note is the only notes-repo change. No commit,
merge, push or branch switch was performed. The stop request was absent at the
final checkpoint.

P667 DONE
