# CC task P372: fix-up for P168 (Hammer of Hephaestus T3, Craft This Order): its branch did not merge into main

**Golem:** Iron. **Date:** 2026-10-24. **Branch:** `golem/Iron/P372` in both work copies.

## In plain words

- P168's work (the Masterwork Hammer of Hephaestus, Craft This Order, and the guild-pay lines on bulk order deeds) is
  now merged with today's main and ready for the integrator. The game behaves as P168 described; nothing new was added.
- Its changelog lines now sit under version 2026.10.24.18, beside the Artificers' fix, so players see them in the next
  release notes.
- The new menu entry "Craft This Order" keeps its number (1,900,011), which main had kept free for it. The trash bag's
  two entries (1,900,012 and 1,900,013) are unchanged.
- Nothing for you to do. The menu entry's name still needs the next player package, as P168 said.

## What changed

- **ShatteredLegacy:** `origin/golem/Copper/P168` (`b8c7e6f`) merged into `golem/Iron/P372`, which starts at main
  (`608d0b4`). The hand-off says not to switch branches, so I merged P168 into this branch instead of main into P168;
  the tree is the same. The merge is staged, not committed (`MERGE_HEAD` is set), for the Golem's commit.
- **shard-migration:** P168's notes, `notes/cc-P168-hammer-t3-craft-order.md`, taken from `origin/golem/Copper/P168`
  (`30d18d5`) and staged. That was P168's only change in this repo, so there was nothing to merge.

## Conflicts resolved

| File | Main | P168 | Resolution |
|---|---|---|---|
| `VERSION` | 2026.10.24.18 | 2026.10.21.16 | 2026.10.24.18, the higher. |
| `CHANGELOG.md` | headings 2026.10.24.18 down to .10.21 | its own 2026.10.21.16 heading (Added, Staff) | P168's Added and Staff lines moved under 2026.10.24.18, beside main's Fixed line, in the order Added, Fixed, Staff. Its old heading is gone. No line changed. |
| `docker/uo/apply-patches.sh` | P263, P371, P359, P480, P427, P457, P453 patch lines at the end | P168's two lines at the end | Both kept: main's first, then P168's `BOD-properties-guild-pay.patch` and `PlayerMobile-craft-order-hurt.patch`. Each P168 patch says it goes last, against the tree the patches above leave. |
| `server/customizations/ShardClilocs.cs` | P415's `ClearACorpse` 1,900,012 and `ClearCorpsesNearby` 1,900,013, with a comment leaving 1,900,011 to P168 | `CraftThisOrder` 1,900,011 | Both kept, in number order. I removed the clause of P415's comment that said 1,900,011 was still on P168's branch. |
| `player-package/vendor/shattered-legacy-cliloc/entries.json` | rows 1900012, 1900013 | row 1900011 | All three rows, in number order (valid JSON, checked). |
| `player-package/vendor/shattered-legacy-cliloc/registry.csv` | rows 1900012, 1900013 | row 1900011 | All three rows, in number order. |

Merged cleanly, and checked by eye: `player-package/tests/Cliloc-Overrides.Tests.ps1` now expects all 14 entries
(P168's `Craft This Order` and P415's two). Main's `PlayerMobile-noted-damage-memory.patch` (P427) and P168's
`PlayerMobile-craft-order-hurt.patch` both touch `PlayerMobile.OnDamage`, in different places (about :2378 and :2406).

## Tests

I ran `docker/uo/build.sh -t sl-modernuo:cc-P372` on the merged tree once, under the `docker-build` lock (taken, then
released). There was 11.8 GB free memory at the start, and I dropped the Docker VM's page cache first.

- **2,371 tests: 2,367 passed, 0 failed, 4 skipped.** Image `sl-modernuo:cc-P372` built with patches applied, and no
  compiler warnings (`warning CS`). Nothing was red, so I fixed nothing.
- P168's own facts are all green: `HammerCraftOrderVerification` 13 of 13, `BulkOrderGuildPayVerification` 10 of 10.
- Every patch applied in order, including P168's three after main's: `CraftItem-shard-hooks.patch` (changed by P168),
  then `CraftItem-fail-streak-achievement.patch` (main) on top of it, then `PlayerMobile-noted-damage-memory.patch`,
  then `BOD-properties-guild-pay.patch` and `PlayerMobile-craft-order-hurt.patch`.
- The log has 109 `Item.Amount <= 0` stack traces, logged by passing tests: a corpse set to amount 0 in the Custodian
  facts. Older notes record the same noise (cc-P10, cc-P17, cc-P139). It has nothing to do with P168.

**Player package cliloc test:** not run, for the reason P168 gave: it compiles C# with `Add-Type`, which this
machine's SentinelOne rule blocks. I checked the three-way agreement it tests with Python instead: entries.json 14 rows,
registry.csv 14 rows, the same numbers and texts, and every number is a `ShardClilocs` constant (1,900,011
`CraftThisOrder`, 1,900,012 `ClearACorpse`, 1,900,013 `ClearCorpsesNearby`).

P372 DONE
