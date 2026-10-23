# P490: Review of achievement category icons (P241)

Reviewed 2026-10-23 against the two Verite-tower work copies, shard version 2026.10.23.4. Review only; no tracked code or tests changed.

Read P241's implementation note first, plus the relevant art inventory in `cc-P379-crystal-review-10-21-merges.md` and the P241 client checks in `cc-P378-playtest-plans-10-21.md`. No separate P241 review note was present. The finding below does not repeat P241's recorded build flakes, additional page count, or outstanding client checks.

## Finding

1. **bug** | `server/customizations/ClusterFAchievements.cs:2368` (category rows inserted at `:2165`): Pagination treats a category heading as an independent row, so it can leave the icon and name at the bottom of one page and put that category's first achievement on the next page with no heading. Keep the heading with its first achievement, repeat the heading on continuation pages, and add a boundary regression test because `server/tests/Misc/AchievementCategoryIconsVerification.cs:131-166` checks the union of headings across pages and the first page of each category, without checking these page breaks.

### Evidence for the finding

Ran the exact, unchanged `Paginate` method extracted from the current canonical C# file in an isolated .NET 10 console probe. It used synthetic rows, not a saved account or a live shard:

| Row | Height |
|---|---:|
| Not Yet section divider | 26 |
| Combat heading | 50 |
| Combat A | 54 |
| Combat B | 54 |
| Combat C | 54 |
| Skills heading | 50 |
| Skills A | 54 |

The room is 326 pixels, the current `ContentBottom - ListY`. These are supported row heights: section dividers are 26, category headings are 50, and an item-bearing achievement with two unwrapped text lines is 54 (`RowHeight`, `:2347-2356`). Output:

```text
Page 1: rows 0..5; first=Not Yet; last=Skills heading
Page 2: rows 6..6; first=Skills A; last=Skills A
```

The rendering loop at `:2215-2246` draws only each page's selected rows and does not recreate its category heading. This confirms the boundary behavior with valid row sizes; which current player records produce that boundary was not tested. Probe files are under ignored `server/lib/p490-review/`, confirmed with `git check-ignore`; none exceeds 5 MB. No regression test was added and no fix was attempted.

## Art IDs and package checks

No colliding category gump IDs or missing source package PNGs found. Each entry below has exactly one registry row of kind `gump`, a distinct 44 x 44 RGBA PNG that Pillow fully decoded, and the expected author credit. Paths are relative to `player-package/vendor/shattered-legacy-art/`.

| Category | Gump ID | File |
|---|---:|---|
| Combat | 22459 | `gumps/22459.png` |
| Skills | 22460 | `gumps/22460.png` |
| Exploration | 22461 | `gumps/22461.png` |
| Mining | 22462 | `gumps/22462.png` |
| Crafting | 22463 | `gumps/22463.png` |
| Legacy | 22464 | `gumps/22464.png` |
| Discovery | 22465 | `gumps/22465.png` |
| Collection | 22466 | `gumps/22466.png` |
| League | 22467 | `gumps/22467.png` |
| Mischief | 22468 | `gumps/22468.png` |

- Ran the existing `EveryAchievementCategoryIconIsARegisteredGumpWithItsPngAndItsAuthorsCredit` fact from `player-package/tests/Build-UoOverrides.Tests.ps1:478-510`: PASS under Windows PowerShell 5.1.26100.9711. Used AST extraction of that fact and its existing assertion functions so the suite's unrelated launcher facts would not contact a shard.
- Ran `scripts/find-free-art.py --data D:\UO\tool-trials\client-data-copy --tazuo D:\UO\cc-p40-work\tazuo-3212623f --explain-gump 22459 22460 22461 22462 22463 22464 22465 22466 22467 22468`. For every listed ID, the only blockers were its intended `ClusterFAchievements.cs` reference and its own registry entry. No stock art, definition, pinned server, client code, or other vendor override collision was reported. An independent scan of vendor gump PNG/BMP filenames found no competing override for these IDs.
- Read package staging at `player-package/Build-PlayerPackage.ps1:790-799` and zip checks at `:352-372`: the registry includes these icons, staging copies their PNGs to `app/tazuo/ExternalImages/gumps/`, and the zip gate requires every registered gump file. No omission found in that path. No package zip was built or inspected during this review.

## Client without the art and remaining limits

No additional missing-art failure found in source. `ClusterFAchievements.cs:2229-2230` emits the icon and category name independently. The pinned TazUO source named by `client/TAZUO_COMMIT` (`3212623f63436be1c0f4e3b308b202b29597c026`) disposes only the missing picture when its texture is null (`src/ClassicUO.Client/Game/UI/Controls/GumpPic.cs:31-37`); the category label remains a separate control. Read the shard's client patches and found no change to that behavior.

Actual client rendering remains unverified, including official clients and other client data versions. P241 and P378 already record the updated-client and retained-old-package checks, so those are not new findings. The server icon and layout test files were reviewed but their xUnit suites were not run; no Docker build, deployment, or Haven connection was made. Ran the progress reporter with the work-copy paths and `--dry-run`; it unexpectedly rewrote `tools/progress.json`, which was restored byte for byte from HEAD so only this note remains changed.

P490 DONE
