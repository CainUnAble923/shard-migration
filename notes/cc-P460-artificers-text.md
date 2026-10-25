# P460: the Artificers' guildmaster and join text match the current rules

Done 2026-10-24 by the Iron Golem. Code copy D:\UO\golems\Iron\ShatteredLegacy, branch golem/Iron/P460.
Source: the cc-P383 guide's "Contradictions" (Codex), checked by Crystal's cc-P429 (draft W7).

## In plain words

- The Artificers' guildmaster's "Rewards" page no longer says joining pays Standing and Essence Shards. It says joining
  is free and gives the satchel and toolkit, and that the Apprentice task pays the Standing and Shards.
- The "What We Enhance" page and the welcome message no longer promise higher caps and more slots as your rank grows.
  They say what is true since the imbuing rework: what you can imbue, and how strongly, depends on the formula tiers
  your account learns, and Overcharged work needs a soul forge.
- Nothing for you to do; the change ships with the next deploy (CHANGELOG 2026.10.24.17, a Fixed line).

## What changed

| Text | Was | Now |
|---|---|---|
| `server/customizations/ArtificersGuildmasterGump.cs` Rewards page (old :197) | "Upon joining the Artificers' Order you receive:" (then +25 Standing, +10 Shards) | "Joining is free and issues an Essence Satchel and a Toolkit. Completing the Order's Apprentice task (see Joining Requirements) pays:" (the same two lines, from `GuildDef.JoinReputation`/`JoinScrip`, which `ClusterFGuildSystem.CompleteApprenticeTask` pays) |
| same file, What We Enhance page (old :156-158) | "...reach property intensities beyond vanilla limits. Higher ranks unlock greater caps." | "Order members can imbue already-enchanted items. How strong a property you can imbue depends on what your account has learned: each property is known up to a tier (Basic, Refined, Full) from the Order's formula books, and Overcharged tiers also need a soul forge close by. Standing alone raises no limit; it opens the rank that sells the next book." |
| `server/customizations/ClusterFGuildSystem.cs` join message (old :508) | "As your Artificers' Standing grows, you will unlock higher intensity caps and more property slots." | Two lines: "Complete the Apprentice task for your first Standing and Essence Shards." and "What you can imbue, and how strongly, comes from the property tiers your account learns from the Order's formula books; Overcharged work also needs a soul forge." |

The wording follows the P383 guide (`notes/wiki-drafts/artificers-order.md`: "Joining and your first task" :11-26,
"gates what you can imbue by the property you know and its learned intensity tier" :60, the forge rule :98). It was
checked against the code: `CompleteApprenticeTask` pays the old join rewards (ClusterFGuildSystem.cs:382-427), and the
imbue apply step refuses a target above the account's known tier (`ClusterFImbueKnowledge.KnownTier`,
ArtificersImbueGump.cs:1767-1779), with the place resolved by `ImbueSites`. The sixth slot (the Master Formulary) is
not mentioned in the new text; the Rewards page's existing rank list already says so.

## Tests

No existing test pinned any of the three texts (searched `server/tests` for the phrases and the gump). New file
`server/tests/Misc/ArtificersTextVerification.cs`, three facts:

- `TheRewardsPageCreditsTheApprenticeTaskNotJoining`: the Rewards view's HTML has no "Upon joining" and names the
  Apprentice task and free joining.
- `TheEnhancePageSaysLearnedTiersAndPlaceNotRankCaps`: no "greater caps" or "Higher ranks unlock"; names tiers, the
  formula books and the soul forge.
- `TheJoinMessagePointsAtTheApprenticeTaskAndLearnedTiers`: a real `ClusterFGuildSystem.Join` on a test NetState; the
  welcome line is on the wire, the caps and slots promise is not, and the Apprentice task and formula books are.

Runs (`docker/uo/build.sh -t sl-modernuo:cc-P460`, under the `docker-build` lock, taken and released; free memory
6.4-12.7 GB after dropping the Docker VM's page cache):

| Run | Tree | Result |
|---|---|---|
| red 1 (`--tests-only`) | new facts, old texts | 2,337 passed, 3 failed. The two page facts were red on the old text ("Upon joining the Arti...", "Higher ranks unlock greater caps"). The join fact failed its own sanity check ("the join message was not seen on the wire"): `Join` returns at once for a mobile with no account, and I had set the account only on the NetState. Fixed the test. |
| red 2 (`--tests-only`) | same, test fixed | 2,337 passed, **3 failed**, each at its content check, the join fact with "the join message still promises standing-based caps" |
| green 1 (full build) | fixed texts | stopped in apply-patches: "Loot-hat-types-orc-tribal-mask.patch - present in /patches but never applied", the known pipefail flake; reran once |
| green 2 (full build) | same | **2,340 passed, 0 failed, 4 skipped**; image `sl-modernuo:cc-P460` built with patches applied |

## Deviations and decisions for Chase

- **A CHANGELOG line the prompt did not ask for** (2026.10.24.17, Fixed; VERSION bumped): players read this text.
- The welcome message is now two lines instead of one.
- Nothing else; no Haven connection, no test-shard start, no player package build.

## Files changed

Code copy: `CHANGELOG.md`, `VERSION`, `server/customizations/ArtificersGuildmasterGump.cs`,
`server/customizations/ClusterFGuildSystem.cs`, `server/tests/Misc/ArtificersTextVerification.cs` (new).
Docs copy: this file.

P460 DONE
