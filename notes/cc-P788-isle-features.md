# cc-P788: loot boxes, reward stores, pet leash and random encounters for the isle release

## In plain words

- **The next isle update can carry four of main's features**: the pet leash, the new loot boxes (rarities, seasonal
  boxes, Bags of Holding and the rest), the Achievement Store and the bigger League shop, and random encounters on the
  roads. They are in one file the overseer applies to `release/isle-20261028`, and the result builds green with every
  test passing.
- **What testers will notice:** the dog or cat from the pet choice scroll comes with a leash (and animal trainers sell
  them); loot boxes show a rarity and their new prizes; `[apstore` and `[leagueshop` open the stores from anywhere;
  out in the Trammel and Felucca wilds a toll gang, a pinned-down surveyor or (Halloween nights) a lantern procession
  can turn up. Never on the Wakening Isle: a new test proves that.
- **What they will not see on this branch:** the Guild Stores and guild points (no guildmasters there), the Festival
  Peddler's stall (it belongs in the new New Haven), and the guild-only loot boxes (Society, League Dive). Festival
  Tokens still drop and are kept for when the Peddler arrives.
- **For you:** nothing in the player package changes, so the next isle package is the same client. The overseer applies
  `notes\cc-P788-tools\p788-release-isle-20261028.diff` to the release branch and ships it.

Iron Golem, 2026-11-03. Release copy: `D:\UO\golems\Iron\p788-isle`, a detached worktree at `e6aaf19` (the
`release/isle-20261028` tip), with the change staged; the overseer's `release-isle-20261028` worktree was not touched.
Nothing was committed to the release branch or main; `latest` was not moved.

## 1. What was collected

The merges on main (`git log --first-parent main`), in merge order, each taken as the merge's own change (`M^1..M`):

| Prompt | Merge on main | Files | What |
|---|---|---|---|
| P760 | `ee0f461` | 30 | reward stores: Guild Stores, Festival Tokens and the Peddler, the Achievement Store, 14 League shop rows |
| P764 | `4b8c826` | 6 | pet leash and shrink |
| P763 + P774 | `a7b7b40` | 22 | loot boxes, more varied (P763 `144faea`) with its fix-up (P774 `ffb1fb4`), merged together |
| P776 | `fbf7d9f` | 6 | random encounters |
| P775 | (none) | 0 | a build review of P774: notes only, nothing in ShatteredLegacy |

The four diffs are in `notes\cc-P788-tools\feature-<merge>.diff`. P759 was a plan only (`notes/cc-P759-loot-plan.md`);
it has no code commit of its own.

Applied with `git apply -3 --index`, in that order, with `CHANGELOG.md` and `VERSION` excluded (see below). Every other
file applied without a conflict.

## 2. Conflicts and how each was settled

| Where | Conflict | Settled |
|---|---|---|
| `CHANGELOG.md`, `VERSION` | Every feature diff adds its main version heading (2026.11.01.5 to 2026.11.02.6) where the release has its own. The first apply left both files conflicted and that stopped the next three diffs from applying at all, so the run was reset and redone with both excluded. | Release side kept; one new isle entry, **2026.11.03**, written by hand from the four features' own player lines, with the New Haven parts taken out (below). `VERSION` 2026.11.02 to 2026.11.03. |
| `docker/uo/apply-patches.sh` | The release lacks P714's school-gate patch lines. P763's hunk anchors on the `MLQuestEntry-quest-milestones.patch` line, which the release has (P769). | Applied cleanly after that line; the release's patch list is otherwise unchanged. The gated build applied all 176 patches, the two new loot-box ones included. |
| `server/tests/Misc/RandomEncounterVerification.cs` | P776's `AssertRefused` checks `SosFenceRegion.InAnyFence`, the map swap's SOS fences (P687), not on the release: the first isle build failed to compile on it (`gated-build-isle-run1-compile-error.txt`). | Release side: that one guard line is removed (there are no fences on this branch to stand under), with a comment. |
| `server/customizations/RewardStores/FestivalStore.cs` | No textual conflict, but the Festival Peddler's stall puts itself up at world load whenever a season is on, at `3636,2627,0` on Trammel: New Haven on the swapped map, which the release does not have. | Degrades quietly: a new setting `clusterf.festival.stallOnWorldLoad`, **false** on this branch, so the stall is not put up by itself (no NPC, no error, no log line). `[FestivalMarket` stays for staff. Main does not get this change. |

P735 (the bot route, `e77eba1`) shares only `CHANGELOG.md` and `VERSION` with the feature files, and P714 (`ceb7bcd`)
those and `apply-patches.sh` (counted with `git diff --name-only` against the diff's file list). Of everything main changed
between the release's branch point `9ee74b6` and P760, four code files are also feature files
(`ClusterFAchievements.cs`, `ClusterFAlembicGuild.cs`, `LeagueRegistrarGump.cs`, `Tutorial/TutorialGateSkip.cs`); their
feature hunks applied cleanly on the release's versions and the build compiled them.

### What degrades on the release (testers will not see it)

Checked against the code, not assumed:

- **Guild Stores and guild points.** The stores open only from a guildmaster's window or with `[guildstore` beside one.
  With none placed on this world, `[guildstore` answers "Stand beside the guildmaster of a guild you belong to" (a
  plain line, no error). Guild points from bulk orders and requisitions go only to members, and joining needs a
  guildmaster.
- **The Festival Peddler's stall**: see above. Festival Tokens are still earned (in season: drops from strong
  creatures, Sorcerer's Dungeon hand-ins, the first login of the day) and kept on the character for later; the isle
  CHANGELOG says so.
- **Society and League Dive loot boxes**: both come from guilds (a new rank in a crafting guild; every tenth guild work
  order), so they cannot be earned here. The isle CHANGELOG lists the four new kinds that can be: Fisher's, Sailor's,
  Herbalist's, Delver's.
- **The requisitions board** is not on this world, so nothing it pays (guild points included) is reachable.

Reachable everywhere: `[apstore` (also the achievements window's AP Store button), `[leagueshop`, the pet leash
(animal trainers are stock vendors, and the pet choice scroll from P762 now includes one), every loot box source that
is not a guild's, and random encounters.

## 3. Random encounters stay off the Wakening Isle

On the release, as on main, the isle is the Fold (`TutorialWorld.Isle => FoldMaps.Fold`) and each trainee walks a copy
of it (`FoldMaps.Copy(1..16)`). `ClusterFEncounters.WhyNotHere` refuses any map from the Fold's index up as "the
Wakening Isle", before any other check.

P776's own `NeverOnTheWakeningIsle` checks one tile on the Fold itself. A new fact in the diff,
**`P788_NoEncounterEverStartsOnTheIsleOrAnyCopyOfIt`**, puts a traveler on the release's isle start tile
(`TutorialWorld.Arrival`) on the Fold and on every one of its 16 copies, with the roll certain and the Fold listed as an
encounter facet, and asserts each is refused as "the Wakening Isle" and that nothing starts.

- **Green** on the release image `sl-modernuo:cc-p788-isle` (the gated build below).
- **Seen red**: with the isle rule cut down to the Fold alone (`mutant/ClusterFEncounters.cs`, probed on the release's
  builder image), the new fact fails on copy 1 ("TheFold 1 is not an encounter facet" instead of "the Wakening
  Isle"); the other 27 encounter facts, P776's isle fact included, still pass, so only the new one guards the copies
  (`red-mutant-isle-copies.txt`). The first mutant run passed by mistake: the mutant file was older than the image's
  build, so MSBuild skipped recompiling it; touched and run again.

## 4. Client package

**No change.** None of the four diffs touches `player-package/` or `client/`. The art, cliloc and music registries
(`player-package/vendor/shattered-legacy-*/registry.csv`) are identical on `e6aaf19` and main, so every art id these
features use on main is already registered for the release. The only package differences between the two are the
swapped map's files (`sos-trammel-map`), which the release does not use. With nothing to carry, there was no scratch
package build to gate; the next isle package is the same client.

## 5. Build

`docker\uo\build.sh -t sl-modernuo:cc-p788-isle` on the release copy (`cc-P788-tools\gated-build.ps1`, the
`docker-build` lock taken and released each time):

1. EXIT=1: the `SosFenceRegion` compile error above (`gated-build-isle-run1-compile-error.txt`). Fixed.
2. EXIT=0: 2,868 tests, 2,863 passed, 5 skipped, 0 failed; 176 patches applied
   (`gated-build-isle-run2-green-before-changelog-fix.log`, kept locally: `*.log` is git-ignored). The CHANGELOG then lost its League Dive mention (see
   above), so the image was built again to match the diff exactly.
3. **EXIT=0, the image that matches the diff: 2,868 tests, 2,863 passed, 5 skipped, 0 failed**
   (`green-gated-build-isle.txt`). Its builder stage, patches included, was Docker's cache of run 2 (same inputs:
   only the CHANGELOG changed), where all 176 patches applied; the image's `CHANGELOG.md` has the corrected entry and
   `VERSION` reads 2026.11.03 (read inside `sl-modernuo:cc-p788-isle`).

Among the passes: `RandomEncounterVerification` 28 (the new fact included), `PetLeashVerification` 9,
`LootBoxDiversityVerification` 9, `RewardStoreVerification` 14, `LeagueShopVerification` 12.

## The release diff

`notes\cc-P788-tools\p788-release-isle-20261028.diff`: 58 files, 8,615 insertions, 254 deletions, against `e6aaf19`.
`git apply --check` on a fresh detached worktree at `e6aaf19`: **clean** (rc 0). The diff is the release copy's staged
change, which is also its whole working tree (nothing unstaged or untracked), so it is exactly what was built.

## For Chase

- **Testers get:** the pet leash; loot box rarities, seasonal slots, the four new box kinds and the new prizes; the
  Achievement Store and the bigger League shop (`[apstore`, `[leagueshop`); Festival Tokens (earned, kept); random
  encounters in the Trammel and Felucca wilds, never on the isle.
- **Quietly missing on the isle branch:** Guild Stores and guild points, the Festival Peddler's stall, the Society and
  League Dive boxes, anything from the requisitions board.
- **Player package:** unchanged.

## Deviations and notes

- The CHANGELOG and VERSION from main were not carried; the isle entry is written for this branch (its own version,
  New Haven lines out). The isle version 2026.11.03 is the same string as main's newest (P780's); the P773 isle entry
  shared 2026.11.02 with main the same way.
- No in-game proof run on the private shard: not in "Done means", and the encounter rule is covered by the new fact.
- Worktree left for the overseer and me to remove after the release ships: `D:\UO\golems\Iron\p788-isle` (detached,
  staged).

## Files

- shard-migration: this file; `notes\cc-P788-tools\` (the release diff, the four feature diffs, the gate script and
  log summaries (the raw `.log` files stay local, git-ignored), the probe script, the mutant and its log).
- ShatteredLegacy `golem/Iron/P788`: no change. Everything for the release is in the diff.

P788 DONE
