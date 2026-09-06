# Direction: migrate the shard from ModernUO to ServUO

**Status: DECIDED (again) 2026-09-06. This is the third and final entry. Read the history
before proposing a change; the analysis never moved, only the scope did.**

## History, honestly

1. **Decided: migrate to ServUO.** ModernUO ships zero files for High Seas and zero for Time
   of Legends; ServUO ships 134 and 74. Scope was given as "full post-ML including naval
   combat and Eodon."
2. **Reversed: stay on ModernUO.** That scope had never been checked against what the shard
   is for (a family, possibly a small school). On the assumption the scope was smaller than
   stated, staying on the better engine and porting selectively won on every axis.
3. **Reversed back: migrate to ServUO.** The scope was confirmed as stated: **all** newer
   content, not a chosen subset. At that scope the arithmetic is not close.

The analysis was consistent throughout. What changed was one input, and it was the input
nobody had pinned down.

## The arithmetic at "all newer content"

ServUO content absent from ModernUO: **3,091 files, 548,912 lines.** Narrowing to just the
post-ML systems (expansions, revamped dungeons, seasonal events, Skill Masteries, Vice vs
Virtue, City Loyalty, Exploring the Deep) is still roughly **780 files and 134,000 lines**,
before the artifacts, mobiles and gumps that dress them.

Five of those are subsystems ModernUO has **zero** files for and would be built from scratch,
not ported: Skill Masteries, Shadowguard, Myrmidex Invasion, Vendor Searching, Instanced
Peerless.

Porting all of that into ModernUO is rebuilding ServUO inside ModernUO, and leaves us
maintaining every line with no upstream. On ServUO it already works and is maintained.

## What this costs, stated plainly

Nothing about the engine comparison changed and none of these shrank:

- **Runtime.** .NET 10 down to `net48` under Mono. This is a real regression.
- **Serialization.** Source-generated back to hand-written with a version int.
- **The world.** Characters, items and houses do not port. Fresh world plus a compensation pass.
- **Our own code.** All 111 custom scripts get rewritten.

Accepted deliberately, in exchange for a content catalogue we would otherwise spend years
writing and then own forever.

## What makes it affordable

The port triage (`port-triage.md`) measured our side: **82 trivial, 25 mechanical, 3
repetitive, 1 genuinely hard.** No Core bucket at all, because the shard was already built as
pinned upstream plus an isolated customization layer. That architecture is why this is weeks
rather than months.

## Time-boxed, act now

**Switch ModernUO to SHA2 password hashing while the old shard is still taking logins.**
Default is Argon2, which ServUO cannot read; SHA2 is marked "ServUO compatibility" in
ModernUO's own source and rehashes on successful login. Miss this window and every player
needs a password reset. Full detail in `migration-plan.md` Phase 0.

## Still true regardless of direction

The three setup defects were never migration concerns; they are problems with the shard as it
runs today, and a compiling canonical tree is a prerequisite to porting *from*. See `AGENTS.md`.
