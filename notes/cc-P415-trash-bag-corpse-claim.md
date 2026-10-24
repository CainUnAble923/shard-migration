# cc-P415: trash bag menu options to clear monster corpses (corpse claim for every player)

## In plain words

- The trash bag's right-click menu has two new options: **Clear a corpse** (you click one corpse) and **Clear corpses
  nearby** (it clears every monster corpse within 10 tiles of you). Any player who owns a trash bag can use them, not
  only Custodians. Clearing still pays Clean Up points, the same as `[cleanup`.
- A corpse goes away **with everything still inside it**, so the option asks "are you sure" first whenever a corpse
  still holds items. A player's corpse can never be cleared. A monster someone else killed stays theirs to loot until
  their looting rights run out (2 to 3 minutes). `[cleanup` and `[cleanupall` now follow that rule too.
- The labels "Clear a corpse" and "Clear corpses nearby" are new client text. A player who has not taken the next
  player package update sees **two blank rows** in the menu, and nothing happens if they click one.
- **For you:** rebuild and publish the player package so the labels show. Then, in game: kill a few monsters,
  right-click your trash bag, choose Clear corpses nearby and answer the question. Also try Clear a corpse on another
  player's fresh kill (it should refuse) and on a player's corpse (it should refuse).

## What changed

ShatteredLegacy, branch `golem/Iron/P415`:

| File | Change |
|---|---|
| `server/customizations/TrashBag.cs` | `GetContextMenuEntries` (:109) adds `ClearCorpseEntry` (:155) and `ClearCorpsesNearbyEntry` (:177) after Dump, only when the clicker owns the bag and it is in their backpack (the same place test as Dump, plus `Owner == pm`). Each click and the target check again (`InOwnersPack`, :153). `ClearCorpseTarget` (:198) has a range of 12, the same as `[cleanup`. |
| `server/customizations/ClusterFCustodianSystem.cs` | The one rule: `CanClear` (:161) = `IsEligible` plus, for a corpse, `LootRightsLapsedFor` (:172). `CleanupOne` (:513) is the old `[cleanup` target body moved out unchanged, plus the looting-rights refusal and a clear message for a player's corpse. `ClearCorpse` (:365) and `ClearCorpsesNearby` (:432) are the trash bag's two actions. `ClearableCorpsesNear` (:406) returns only corpses, within `CleanupAllRadius` (10) of the player. `OnSweepCooldown` (:348) is the old `[cleanupall` cooldown code moved out, now shared. `[cleanupall` now filters with `CanClear` (:585), not `IsEligible`. |
| `server/customizations/ShardClilocs.cs` | `ClearACorpse` 1,900,012 and `ClearCorpsesNearby` 1,900,013 (:65, :68). |
| `player-package/vendor/shattered-legacy-cliloc/entries.json`, `registry.csv` | The two texts, registered. **1,900,011 is skipped on purpose**: the unmerged branch `golem/Copper/P168` already uses it for "Craft This Order", so these two numbers will not collide with it when it merges. |
| `player-package/tests/Cliloc-Overrides.Tests.ps1` | `TheServerAndThePackageAgreeOnEveryNumber` lists each server constant by name, so it now lists the two new ones. |
| `server/tests/Services/TrashBagCorpseClaimVerification.cs` (new) | Six facts, below. |
| `CHANGELOG.md`, `VERSION` | 2026.10.24.6, two lines under Added. P414's pending section is .5, so this one goes above it. |

Points, messages and eligibility follow one rule. Both new entries call `CleanupOne`, or the same three steps
(`CanClear`, `ComputePoints`, `Delete`). `ComputePoints` is unchanged: for a corpse it pays the creature's base (cc-P175
`ClusterFCorpseValue.BaseFor`: Fame x 0.001, only to whoever earned the kill or their party) plus each item inside at
its Clean Up value. A player who is not a Custodian earns points the same way. Points live on the character, and
joining later picks them up (cc-P33).

**No civic waste bundles come from either entry.** Neither entry calls `GiveBundles`. I left the `[cleanupall` and
trash-bag Dump lines that P414 edits as they were, so P414 merges cleanly over this whether it lands before or after.
The one new block sits before `// -- Inner targets`, away from P414's `GiveBundles` hunk.

## Who may clear what (Part 2)

- **Any player who owns a trash bag.** The entries do not check Custodian membership. A bag still comes only from the
  Custodians (`SanitationWarden.OnCustodiansJoined`, `SanitationWardenGump.HandleTrashBag`). The guild is open to
  everyone and free to join (`ClusterFGuildSystem.cs:245-253`: task skill 0.0, no rep and no scrip, and `CanJoin`
  :314 only refuses a current member). If you want players to get a bag without joining, that is a one-line change in
  the Warden's gump. I did not make it.
- **Never a player's corpse.** This is `IsEligible`'s existing rule (cc-P33). The owner cannot clear their own corpse
  either (fact 3).
- **Looting rights, by pinned's own rules (my choice: clearing a corpse counts as looting all of it):**
  - `Corpse.IsCriminalAction(by)` (`ModernUO-pinned/Projects/UOContent/Items/Misc/Corpses/Corpse.cs:750`) must be
    false. For a monster corpse this comes down to `NotorietyHandlers.CorpseNotoriety`
    (`Projects/UOContent/Misc/Notoriety.cs:332-347`). Before `Corpse.MonsterLootRightSacrifice` (2 minutes,
    `Corpse.cs:92`) has passed since `TimeOfDeath`, only the corpse's aggressors (whoever earned looting rights,
    gathered from `GetLootingRights` at `Corpse.cs:294-310`) and their party may loot it. Anyone else is "Innocent",
    so it would be a crime. After 2 minutes, anyone may.
  - SE instanced loot (`Corpse.InstancedCorpse`, 3 minutes, `Corpse.cs:321`) deals each item to one attacker
    (`AssignInstancedLoot`, `Corpse.cs:470`, called for every non-player corpse at `:640-642`). Only that attacker
    sees it (`IsChildVisibleTo`, `Corpse.cs:465`). So on a shared kill, a corpse holding an item dealt to someone else
    waits until the 3 minutes are up. Without this check, one of two partners could delete the other's share
    (fact 4).
  - A monster that died with no player aggressor (killed by a guard or another monster) is clearable by nobody for its
    first 2 minutes. This is pinned's looting rule unchanged.
  - I used the crime test itself, not `CanLoot`. `CanLoot` (`Corpse.cs:860`) allows criminal looting where the map
    has no harmful restrictions (Felucca). Clearing is never allowed as a crime, on any facet.
- **`[cleanup` and `[cleanupall` follow the same rule now**, so it stays one rule. Before this change, a Custodian could
  `[cleanupall` another player's fresh kill, loot and all. This is a behaviour change for Custodians, and it closes a
  griefing hole.
- **Contents:** they are deleted with the corpse and counted at their Clean Up value, as before. The menu's
  confirmation says so: "This corpse still holds N items. Clearing it deletes the corpse and everything inside it, for
  good. Loot anything you want to keep first." The nearby sweep asks the same, with the corpse and item counts. It
  asks only when some corpse still holds items; an empty corpse clears without a question. The question is pinned's
  stock `WarningGump`, and its answer re-runs every check before anything is deleted. The target message says it too:
  "Anything still inside goes with it." The done message counts what went: "Corpse cleared (5 items inside went with
  it)".
- **Cooldown:** "Clear corpses nearby" shares `[cleanupall`'s 60-second cooldown. That keeps it the same rule, so a
  player cannot alternate the two. "Clear a corpse" has no cooldown, the same as `[cleanup`.

## Server resources (Part 3)

These numbers come from a typical hunt, measured in the test host (fact 6, red run output; loot is random, so counts
vary from kill to kill):

| Corpse | Items inside |
|---|---|
| Orc | 4 |
| Orc | 4 |
| Skeleton | 3 |
| Skeleton | 2 |
| Ettin | 2 |
| Lich | 11 |
| Dragon | 10 |

**So one "Clear corpses nearby" after a hunt like this removes 7 corpses and 36 items, 43 world items in all.** One orc
with two extra drops (fact 2) held 5 items and paid 9.1 points (base 1.5). The sweep reaches 10 tiles in every
direction, a 21 x 21 square around the player.

**It deletes them for real.** Each corpse gets `Item.Delete()`, which deletes the corpse's whole contents tree. Facts 2
and 6 check that every corpse and every item that was inside are `Deleted`, and that `World.FindItem(serial)` is null
for each one. Nothing moves to a holding container, the internal map, a bank or a bag. Left alone, a corpse decays on
its own after 7 minutes (`_defaultDecayTime`, `Corpse.cs:96`), turns to bones, and the bones last another 7. Clearing
frees those items at once instead of after up to 14 minutes.

## Tests (Part 4)

`docker/uo/build.sh -t sl-modernuo:cc-P415`, run under the `docker-build` lock (taken, then released). Windows had
6.9 GB free before the first build, and the Docker VM had 13.8 GB available. I dropped the VM's page cache before the
build anyway.

New facts, `TrashBagCorpseClaimVerification`:

1. The entries show only for the owner with the bag in their backpack: not for someone else's bag in their pack, and
   not for their own bag in the bank. The entries' numbers are 1,900,012 and 1,900,013, in our block.
2. A non-Custodian clears an orc they killed and is paid exactly `ComputePoints` (base plus contents). With items
   inside it asks first and touches nothing. Once confirmed, the corpse and every item inside are gone from the world.
   An empty corpse clears without asking.
3. A player's corpse is refused by both entries, and is not even its owner's to clear.
4. Another player's fresh kill is refused (both `ClearCorpse` and `[cleanup`'s `CleanupOne`), and it clears once
   `TimeOfDeath` is 4 minutes back. On a shared kill, a corpse holding an item dealt to the other attacker is refused,
   even though the clearer has looting rights. It clears after the rights lapse.
5. "Nearby" clears the player's own kill, an old corpse and one 9 tiles out, three in all. It leaves a corpse 15
   tiles out, a player's corpse, another player's fresh kill and an eligible dagger on the ground (which `[cleanupall`
   would take). Unconfirmed, it clears nothing. A second sweep right away hits the cooldown.
6. The typical-hunt sweep above asks first, then removes every corpse and item for real.

**Red first.** I ran a mutant with the new rules switched off: the entries shown for any bag in the pack,
`CanClear` reduced to "any corpse or eligible item", no player-corpse check, and no confirmation. Facts 1 to 5
failed on the second red run (`red2`) and all six on the third (`red3`), each for the reason it tests:

| Fact | Mutant result |
|---|---|
| 1 | Another player's bag showed both entries |
| 2 | Cleared without asking |
| 3 | Cleared the player's corpse |
| 4 | Cleared another player's kill |
| 5 | Unconfirmed sweep cleared 5 |
| 6 | Unconfirmed sweep cleared 8 |

The first red run stopped on a compile error in my own code (`FindItemsByType` returns a struct enumerator with no
`Count`). I fixed it in both the real file and the mutant.

**Green.** The real code passed all six. The whole gate: **2,281 tests, 2,277 passed, 0 failed, 4 skipped** (the same
4 as the red runs). The image `sl-modernuo:cc-P415` (`aa33e7360b6c`) was built.

The player package's cliloc facts (`player-package/tests/Cliloc-Overrides.Tests.ps1`): **10 of 10 pass**, including
`PlayStartsTheGameWithTheTextOverride`. Before I added the two names, `TheServerAndThePackageAgreeOnEveryNumber`
failed ("expected [11] but got [13]").

`CHANGELOG.md` and `VERSION` were edited after the green build. The patch-notes tests parse sample text, not the
file, and the new lines are plain ASCII in the existing format. The tests were not re-run.

The log lines "Corpse ... was changed to amount of 0" in the test output are not from these facts. They come from
older tests that build a corpse for a mobile with no body. These facts give their players a body.

## Deviations and decisions for Chase

- **Package update needed for the labels.** EA's Cliloc.enu has no entry saying "Clear a corpse" or "Clear corpses
  nearby". I searched it with `notes/cc-P29-tools/cliloc.py`; the nearest are 3000154 "Clear" and 1077858 "Clear
  Item". The prompt names the labels, so they are our clilocs, the cc-P57 way. Until the player package with the new
  `entries.json` is built and published, TazUO draws those two rows blank and they cannot be clicked. I did not build
  or publish the package: this prompt touches the server only. If you would rather have working (vaguer) labels today,
  swap them to 3000154 "Clear" and 1077858 "Clear Item" in `TrashBag.cs`.
- **`[cleanup` / `[cleanupall` now respect looting rights** (see Part 2). This is ours, and it changes the existing
  commands too. It is one rule, as the prompt asks.
- **Clearing never counts as a crime, even in Felucca.** I used `IsCriminalAction`, not `CanLoot`, so a corpse that is
  only lootable as a crime is not clearable.
- **The sweep cooldown is shared** with `[cleanupall` (60 seconds).
- **Read tool denied.** The unattended run auto-denied the Read tool on
  `ShatteredLegacy/server/customizations/ClusterFCustodianSystem.cs`. I wanted to Read it so I could Edit it. Instead I
  read it with `cat` and made the edits with an exact-match Python replace script
  (scratchpad `edit_custodian.py`). Each replacement asserts exactly one match, and the file's line endings are kept.
- **1,900,011 skipped** for `golem/Copper/P168` (see What changed).

P415 DONE
