# Direction: stay on ModernUO, pull ServUO content in piece by piece

**Status: DECIDED 2026-09-06. This reverses the earlier decision, deliberately.**

## What changed

The original call was to migrate the shard from ModernUO to ServUO, on the grounds that
ServUO ships post-ML content ModernUO never implemented. That reasoning was sound but it
rested on a scope answer given in four words ("full post-ML world including naval combat
and Eodon") that was never checked against what this shard is actually for.

This is a private shard for a family and possibly a small school, as an alternative to
Roblox. Naval combat and Eodon were the two things that made the reverse direction
expensive. For this audience they are not load-bearing.

## The decision

**Stay on ModernUO. Port ServUO content into it selectively and incrementally.**

## Why this is right

**Modernization.** ModernUO is .NET 10, source-generated serialization, fast saves, a real
test suite, and active platform work. ServUO is .NET Framework 4.8 under Mono on anything
that is not Windows. Migrating to ServUO is a step backward on every one of those, and the
gap widens over time. Content is something you can write; a runtime is something you inherit.

**Reversibility, which was under-weighted before.** Porting content into ModernUO is
stoppable at any point and still leaves a working shard, an intact world, and live player
accounts. Migrating to ServUO is a one-way door: it costs the world, the accounts, and a
rewrite of all 111 custom scripts, and regretting it a year later means doing it all again.

**No migration event.** No fresh world. No compensation pass. No password conversion window.
No rewriting working code just to keep it working.

**The existing architecture already supports it.** The shard builds ModernUO from a pinned
commit and layers `server/customizations` and `server/patches` on top. Ported ServUO content
lands in exactly the same place, through exactly the same mechanism. Nothing structural
changes.

## What this costs

Honest accounting. Each ported system is code we own and maintain forever, with no upstream
fixing it for us. Some ServUO content depends on subsystems ModernUO has **zero** files for:
Skill Masteries, Shadowguard, Myrmidex Invasion, Vendor Searching, Instanced Peerless.
Anything resting on those is expensive and should be declined rather than attempted.

Specifically **not** planned, unless the shard's actual users ask for it:

- **High Seas naval combat.** `BaseGalleon` (1,848 lines) plus two cannon files (~3,000)
  extend and partly replace ModernUO's `BaseBoat`. Core surgery, not content.
- **Eodon / Time of Legends.** 18,828 lines resting on Myrmidex Invasion and Skill Masteries.

## What is cheap and worth doing

- Leaf content: items, decorations, food, fishing. Few dependencies, drops straight in.
- Data: spawn definitions, location tables. ServUO XML converts to ModernUO JSON with no
  logic in between.
- Custom facets, which ModernUO supports and ClassicUO reads well past index 5.

## Licensing note

ServUO is GPL-2.0, ModernUO is GPL-3.0. This only matters if we distribute source. Not legal
advice; worth a look before publishing anything that combines both.

## What carries over from the earlier work

Still valid and still worth acting on, because they are defects in the current setup rather
than migration concerns:

- `server/customizations` does not compile on its own. Three pieces are missing and exist
  only in `server/uo/`. See `AGENTS.md`.
- `apply-patches.sh` converts patch failures to warnings and exits 0. Seven patches
  currently fail. A green build proves nothing.
- `server/customizations/migrations/` holds stale PetMimic JSONs that diverge from
  `server/migrations/`.

No longer relevant: the SHA2 password window, the accounts exporter, world-save migration,
and the ModernUO-to-ServUO spawner converter.
