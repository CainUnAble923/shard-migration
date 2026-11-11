# cc-P877: fix-up of P861 (extra NPC name lists and [VBuild statify) after its build review P876 said FAIL

## In plain words

- **Staff can no longer "freeze" the Fountain of Youth into scenery by mistake.** `[VBuild statify` now says no to it,
  and to the other pieces our seeders put back by themselves (the Battle Chess board, the fortune teller's wagon, the
  tutorial farms and the Wakening Isle's wreck, lighthouse and moongate frame). Before, freezing one left a dead copy
  behind, and the real fountain could come back on its own somewhere else.
- **Mara, New Haven's town steward, always keeps her name.** If another townsperson shares it, that person gets a
  new name instead, even if they were there first. Before, the name sweep could have renamed Mara.
- The review files P861 never left are here now: `notes\cc-P877-review\` (what was placed, a map render, the in-game
  shots).
- Nothing for you to do. The integrator queues one more build review.

Iron Golem, 2026-11-10. Code copy `D:\UO\golems\Iron\ShatteredLegacy` and docs copy, both on `golem/Iron/P877`. Read
first: `notes\guides\building-and-decorating.md`. I also wrote the review P876 this fixes up. All play on the private
proof shard (2596) under the test-shard lock.

## Step 1: P861 onto this branch

The prompt says to check out `golem/Iron/P861` and merge main into it. The Golem's hand-off says not to switch branches
or merge. As in P872, I got the same result without either: this branch is main, and `git cherry-pick --no-commit
golem/Iron/P861` put P861's change into both working trees, uncommitted, for the Golem to commit.
- shard-migration: clean.
- ShatteredLegacy: `VERSION` and `CHANGELOG.md` conflicted. P861's **2026.11.10.7** is taken on main (main is at .9:
  lamps .7, Battle Chess .8, Color Wars .9), so P861's entry is now **2026.11.10.10**, above .9. No other branch claims
  .10.

## The reviewer's list (P876) and what I did

1. **No renders or placed list left for review.** Done in `notes\cc-P877-review\`, not `cc-P861-review\`. This
   prompt's step 3 names the P877 folder, and P876's ask is met there:
   - `placed.md`: one line per piece (item IDs, location, facing). It says plainly that nothing permanent is placed in
     any shipped world, seeder or map file; everything was staged on the proof shard's throwaway world copy.
   - `p861-shots\`: P861's three fountain shots (before, after, undo), copied as P876 asked.
   - `shots\`: this run's shots `p877-1` to `p877-7` and `walk.txt`.
   - `main-square-fountains-3651-2600.jpg`: an isorender of main's New Haven square with both test fountains as staged
     (`cc-P877-tools/render877.py`; every part sits on paving at land z 0, and the two do not touch).
2. **FountainOfYouthAddon not refused.** `typeof(FountainOfYouthAddon)` is now in `AddonStatify.SeededTypes`, so
   `WhyNot` refuses it: "a seeder places and keeps the FountainOfYouthAddon; a frozen copy would sit under the one it
   puts back".
   - **Same gap, more types.** I checked every addon class in `server/customizations` for one that a seeder places and
     re-places when it is missing. Seven more had the same flaw: freeze one and its seeder sees nothing at the spot and
     lays a second copy over the frozen statics. These are now refused too:
     - `BattleChessBoard`, re-placed on world load by `BattleChessSeeder`;
     - `FortuneTellerWagon`, placed and topped up with the Festival stall;
     - `TutorialFarmAddon` and `TutorialIsleFarmAddon`, from the tutorial farm seeders;
     - `WakeningIsleShipwreckAddon`, `WakeningIsleLighthouseAddon` and `WakeningIsleMoongateFrameAddon`, from the isle
       addon seeder.
   - I did not add the other addons (deed addons players own, stock dungeon pieces): no seeder of ours re-places them.
   - **Facts** (`AddonStatifyVerification`):
     - 7 (a Theory, fixed and roaming): statify refuses a Fountain of Youth targeted by its part. The refusal names the
       type. The fountain stays on its map at its spot, every part with it, still in `FountainOfYouthSystem.Fountains`.
       No step is recorded and no Static is left beside it.
     - 8: every seeder-kept type above is on the refusal list.

**Also taken: Codex's second P2 on P861** (P876 said the fix-up may take it). The name sweep treated anyone whose name
is in a list as random-named, so Mara (the steward's fixed name, also in pinned's female list) could be renamed when an
older vendor shared it.
- **Now:** `ShardNames.FixedNameTypes` (`ClusterFTownsfolk`, i.e. Mara and Ellis, and also `TutorialGuide`,
  `TutorialHealer`, `TutorialWoundedHelper`, `ThievesDenLookout`, the NPCs whose code sets a name), plus anything that
  is an `ITalkResident`, are never renamed.
- Their names are reserved in their town: an ordinary namesake is renamed however old.
- **Fact 5** (`ShardNamesVerification`) puts an older female stand-in named Mara and a real `ClusterFTownsfolk` in one
  town and a third Mara in another.
  - After the sweep the steward is still Mara, the older one has a new name from the female list, and the one in the
    other town keeps hers.
  - A second sweep renames nothing.
- **Limit:** the list is by type. A future NPC with a hand-set name that is also in a list must be added to
  `FixedNameTypes` or implement `ITalkResident`. A staff-added NPC given a name with `[set Name` is still treated as
  ordinary.

## Proof

**Gated build** (`notes/cc-P877-tools/gated-build.ps1`, docker-build lock, page cache dropped, `latest` not moved):
`sl-modernuo:cc-P877`, **EXIT=0, 3424 passed, 0 failed, 6 skipped** (`gated-build.log`, UTF-16).
- All 15 P861/P877 facts are green: 9 statify (fact 7 runs twice) and 5 names.
- The first build (`gated-build-1-oftype.log`) did not compile: `Map.GetItemsInRange` has no LINQ `OfType`. I changed
  that check to a loop.
- Free memory was 9.6 GB before the build.

**In game** (TazUO, Player-account trainee "Iron Fixup", main's New Haven square, fresh bot-world copy on
`sl-modernuo:cc-P877`; `run877.ps1`, kit `Walk877.py` and `stage877.py`). Every check is a **PASS** (`walk.txt`):
- **Fountain of Youth:** staff added a fixed one at 3651,2600,0 and ran `[VBuild statify` on its middle part.
  - The server answered "Refused: a seeder places and keeps the FountainOfYouthAddon; …".
  - Its own middle part (same serial) still stands there, and the server holds it on Trammel at 3651,2600,0
    (`p877-1-youth-before`, `p877-2-youth-refused`; a wandering townsperson stood on it in shot 2).
- **Stone fountain** (P861's proof again): it stood as an addon. Statify said "Froze the StoneFountainAddon into 16 plain
  statics". A new item of the same art stood there and the addon was on the internal map. Undo brought the addon's own
  part back at 3655,2605,0 (`p877-3` to `p877-5`).
- **Mara:** staff added a provisioner named Mara (female), then Mara the town steward, at P861's twin spots.
  - `[ShardNames dedupe` answered "New Haven: … Mara -> Gaye ('female')".
  - Over their heads: "Gaye the provisioner" and "Mara the town steward" (`p877-6`, `p877-7`).
  - P861's rule would have renamed the steward, because she is the newer of the two.

## Files

- `ShatteredLegacy`:
  - P861's change, cherry-picked;
  - `VERSION` and `CHANGELOG.md` (2026.11.10.10, with a line that people with names of their own keep them);
  - `server/customizations/StaffBuildTools/AddonStatify.cs` (refusal list);
  - `server/customizations/Names/ShardNames.cs` (fixed identities);
  - `server/tests/Misc/AddonStatifyVerification.cs` (facts 7, 8);
  - `server/tests/Misc/ShardNamesVerification.cs` (fact 5).
- `shard-migration`:
  - P861's notes, shots and tools, cherry-picked;
  - this file;
  - `notes/cc-P877-review/`;
  - `notes/cc-P877-shots/main/`;
  - `notes/cc-P877-tools/` (P861's kit repointed, `Walk877.py`, `render877.py`, both build logs).

P877 DONE
