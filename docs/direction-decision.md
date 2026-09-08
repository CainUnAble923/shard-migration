# Direction: stay on ModernUO. Port ServUO content in, indefinitely.

**Status: SETTLED 2026-09-06, by Chase, adamantly. Do not reopen.**

## The decision

Shattered Legacy runs on **ModernUO** and continues to. ServUO is a **content source** we
port from, one system at a time, for as long as the shard is being worked on.

Scope is **all the newer content**, worked through as an ongoing backlog. This is explicitly
not a project with a completion date. It is the shard's long-term development plan.

## History, honestly

The direction moved several times on 2026-09-06 as scope was pinned down. Recording it so
nobody re-derives it:

1. Migrate to ServUO — ModernUO ships zero High Seas and zero Time of Legends files.
2. Stay on ModernUO — the scope that justified migrating had never been checked against what
   the shard is for.
3. Migrate to ServUO — scope confirmed as all newer content, and at that scope porting into
   ModernUO looked like rebuilding ServUO inside it.
4. **Stay on ModernUO.** Final. Chase's call, made with the numbers in hand.

The analysis never changed. What kept moving was scope, and then how to weigh a large
ongoing effort against a one-time migration.

## Why this is defensible at full scope

The case against was that porting the whole post-ML catalogue is multi-year. That is true,
and it is not the objection it first appears to be:

- **This is a hobby shard with no deadline.** A backlog that never empties is a feature, not
  a cost. The alternative buys the content at once and then permanently pays a worse runtime.
- **ModernUO stays modern.** .NET 10, source-generated serialization, fast saves, real tests,
  active platform work. Migrating trades all of that away for good.
- **Nothing is ever at risk.** Every port leaves a working shard, an intact world and live
  accounts. There is no cutover, no fresh world, no compensation pass, no password window.
- **Stop anywhere and the shard is fine.** A migration half-done is a broken shard; a backlog
  half-done is just a shard with less content than it will have next month.
- **Value arrives in the right order.** Port what players will actually touch first. The
  content nobody opens simply stays unported, forever, at no cost.

## What we do not pretend

Ported content is ours to maintain, with no upstream. Five subsystems ModernUO has zero
files for — Skill Masteries, Shadowguard, Myrmidex Invasion, Vendor Searching, Instanced
Peerless — are builds, not ports, and gate the content resting on them. Those are priced in
`content-menu.md` and `highseas-eodon-feasibility.md`. They get done when they get done.

## Immediate consequences

- **No SHA2 password window.** There is no cutover; hashes never need another engine to read
  them. That urgency is cancelled.
- **No account or world migration**, and no spawner conversion. Our data stays put.
- **Our existing custom scripts are never rewritten.** They keep working as they are.
- `D:\UO\ServUO-pub57` is a **read-only content source**. Never edit, never build in, never
  migrate to.

## Still true regardless

The three setup defects are problems with the shard as it runs today, not migration concerns.
A compiling canonical tree is the prerequisite for everything. See `AGENTS.md`.
