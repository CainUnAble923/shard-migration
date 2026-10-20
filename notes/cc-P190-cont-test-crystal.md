# cc-P190: the Test Crystal (a per-character skill gain booster for testing)

Gold Golem, 2026-10-20. Branch golem/Gold/P190 in both repos. Image `sl-modernuo:cc-P190`.

## Headlines

- **The test shard trains at the real shard's rates now.** The global `testCenter.skillGainMultiplier` (5.0 on the
  test shard, every skill's GainFactor for everyone) is retired: it changes nothing and logs a line at start saying so.
- **The Test Crystal replaces it, per character.** A blessed crystal bound to its owner, in their bank. Double-click it
  for a small gump: Off, 2x, 5x, 10x, 25x, the current setting, and "Only affects its owner, <name>. Test Center only."
  The setting is saved on the crystal. It multiplies the owner's gain chance at exactly the spot the old multiplier did
  (pinned SkillCheck.cs:133, `gc *= skill.Info.GainFactor`), so 5x on a crystal is what the whole test shard had before,
  for one character.
- **Off by default, Test Center only.** New crystals are Off. On a shard with the Test Center off it multiplies nothing,
  and it deletes itself when loaded or double-clicked there.
- **Getting one:** `[TCFill` (and Test Center character creation, the same kit placement) puts one in the bank if the
  character has none; `[GiveTestCrystal` (GameMaster, Test Center only) gives one to a target.
- **With P189:** the crystal raises the chance that a use gains; P189's Old Haven apprentice boost multiplies how much a
  gain is worth. They multiply, in that order (section 4).

## 1. Where the multiplier applies (re-checked)

GainFactor has one reader in pinned: `UOContent/Skills/SkillCheck.cs:133` (`gc *= skill.Info.GainFactor;`) in
CheckSkill, at d4531cd9. The old TestCenterSkillGain comment said :119 (written before the cc-P38 bump); the line moved,
the meaning did not. Grep of `Projects/` for GainFactor: Skills.cs:414 and :443 (the property) and that one use.

The crystal's factor goes on the very next line through a new patch, `server/patches/SkillCheck-test-crystal.patch`:
`gc *= Server.Items.TestCrystal.GainScalar(from);`. A patch because gc is a local of the static CheckSkill (the reason
cc-P172 gives for its pet patch in the same method); no handler or event reaches it. ClusterFSkillGain's handlers
(the shard's 2 attempts and 1x amount since P191) sit around pinned's roll and are untouched, so with every crystal
Off a use rolls exactly as on live. Before the floor `if (gc < 0.01) gc = 0.01` (:135-138), as GainFactor is, and
before the controlled-pet x2 and P172's pet multiplier (players are never controlled, so those never apply to them).
Below 10.0 pinned gains on every use regardless of gc (:120-123), so the crystal changes nothing there, as the global
multiplier did not.

## 2. `testCenter.skillGainMultiplier`: retired

Argued: keeping it as "the default strength of a new crystal" would make new crystals start On, which is what the
prompt is getting rid of (the test shard must run at the real rates unless a tester asks). And as a global it is what
made P189 untestable. So it is retired: `TestCenterSkillGain.cs` now only logs, at start, that the key is set and does
nothing (when it is set to anything but 1.0), pointing at the crystal. GainFactor is never changed.

Live's config stays byte-identical: the key is read with GetSetting, never written (as before), and live never had it.
The test shard's `server/uo/modernuo/Configuration-test/modernuo.json:218` still says 5.0; that folder is gitignored
and not an edit target here, so Chase removes the line (or leaves it: it does nothing but log). The overnight bot's
script (`tools/playtest-bot/Run-OvernightPlaytests.ps1:248, :253`) only reports the key's value; untouched.

## 3. The crystal

`server/customizations/TestCenter/TestCrystal.cs` (new), `Server.Items.TestCrystal`:

- Saved fields (generator, version 0, a new type so nothing older to read): `_owner` (Mobile) and `_strength` (int,
  1 = Off). Blessed, weight 0.1, the same crystal art as the Dev Testing Crystal (0x1ECD), pale when Off and gold when on.
- Strengths: Off, 2x, 5x, 10x, 25x. 5x is the old test shard; 25x is for "get this skill to 100 in an afternoon";
  10x between. Anything else set on it reads as Off.
- `GainScalar(from)`: the owner's crystal strength when the Test Center is on, else 1. One crystal counts per
  character: a static owner -> crystal map, filled when a crystal is made for someone and when one loads, emptied when
  it is deleted. Where the crystal lies does not matter (bank or pack); deleting it turns the boost off.
- Double-click: owner (or staff) only, and only while it is in their bank or pack; opens the gump. On a non-Test-Center
  shard it says it crumbles and deletes itself; a loaded crystal there deletes itself on the next tick (never during
  the load).
- `EnsureFor(m)`: a crystal (Off) in the bank unless the character has one; Test Center only. Called from
  `TestCenterKit.PlaceKit` (`TestCenterKit.cs:60-74`), which both character creation on a Test Center shard and
  `[TCFill` (through `RefillBank`) use. The kit's other entries are unchanged.
- `[GiveTestCrystal` (GameMaster, registered only when the Test Center is on, as `[TCFill` is): target a player; a
  crystal goes in their bank unless they have one.

Name kept as "Test Crystal": it says what it is, matches the console art, and is distinct from the GM-only "Dev
Testing Crystal" (DevTestingCrystal.cs, cost bypasses), which it does not touch.

## 4. With P189's Old Haven apprentice boost

P189 is merged separately (this branch is cut from main before it). The two act at different points of one use:

1. The crystal multiplies the **chance** that a use gains (pinned CheckSkill's gc, SkillCheck.cs:133).
2. When a gain happens, pinned's Gain decides its size (0.1, or 0.1-0.4 below 10.0; pinned's 15-minute quest
   acceleration x2-5 at SkillCheck.cs:273-276), and P189's apprentice boost then adds x2-4 of that gain for a quest
   holder in Old Haven Training (`ApprenticeTraining.OnGain`, from `ClusterFSkillGain.ObserveAttempt`).

So they multiply: crystal (more gains) x apprentice boost (bigger gains). To test P189 cleanly, leave the crystal Off:
then every gain is the real shard's and only P189's boost differs inside and outside Old Haven.

## 5. What changed, file:line (D:\ShatteredLegacy)

| File | Change |
|---|---|
| `server/customizations/TestCenter/TestCrystal.cs` (new) | The crystal, its gump, `GainScalar`, `EnsureFor`, `[GiveTestCrystal`. |
| `server/patches/SkillCheck-test-crystal.patch` (new) | After pinned SkillCheck.cs:133: `gc *= Server.Items.TestCrystal.GainScalar(from);`. Made with `diff -u`; applies after the two existing SkillCheck patches at fuzz 0. |
| `docker/uo/apply-patches.sh:692-696` | Applies it, with the reason, after `SkillCheck-pet-gain-speed.patch`. |
| `server/customizations/TestCenter/TestCenterSkillGain.cs` | Retired: logs that the key does nothing; never changes GainFactor. `Apply` and `Restore` are gone. |
| `server/customizations/TestCenter/TestCenterKit.cs:60-74` | `PlaceKit` gives a crystal (unless the character has one) before placing the kit bag. |
| `server/tests/Misc/TestCrystalVerification.cs` (new) | C1-C6 below. |
| `server/tests/Misc/TestCenterVerification.cs:143-160` | The two facts about the old global multiplier are replaced by one: the retired key changes no GainFactor, Test Center on or off. |
| `CHANGELOG.md`, `VERSION` | 2026.10.20.7, Staff (players never see the Test Center). |

Serialization: TestCrystal is a new saved type at version 0 (owner, strength), so there is no older version to read.
The round trip (C4) has no collections to fill. No existing saved type changed.

## 6. Tests

Built and tested only through the repo's build script with `-t sl-modernuo:cc-P190` (docker-build lock taken and
released).

**Seen red first**: a build with the tests and a feature-off crystal modelled on the old test shard (GainScalar 5x for
everyone while the Test Center is on, as the global multiplier was; no refill; no self-delete; any strength kept; no
re-registering on load): 1,603 tests, 6 failed, all six crystal facts:

| Fact | Red | Green |
|---|---|---|
| C1 Off gives exactly the base chance (gain at 0.999 gc, none at 1.001 gc) | scalar 5, expected 1 | pass |
| C2 at 5x the owner gains at 0.999 x 5gc and not at 1.001 x 5gc; a second character rolling the same numbers gets the base chance | the other character also 5x | pass |
| C3 Test Center off: no multiplier, and double-click deletes it, and none is handed out | not deleted | pass |
| C4 owner and setting survive a save and load; the loaded crystal is the one that counts | 5x with no crystal at all | pass |
| C5 the refill puts one crystal, Off, blessed, bound, in the bank, and never a second | bank had none | pass |
| C6 only Off, 2x, 5x, 10x, 25x are kept | 3 was kept | pass |

TestCenterVerification's replaced fact (the retired key changes nothing) passed in both runs; it is a rewrite of a fact
whose subject is gone, not new behaviour, so it has no red to show.

**Green**: first full run 1,603 tests, 1 failed: `LootBoxFanfareVerification.ContentsAreRolledAtEarnAndOpening...`,
which rolled two identical "50 x Obsidian Ingot" stacks that merged when handed over (its output shows them), a random
roll unrelated to skill gain; it passed in the red run. The rerun: 1,603 tests, 1,599 passed, 4 skipped, 0 failed,
"Built sl-modernuo:cc-P190 with patches applied and 1599 shard test(s) passing". That loot box fact is flaky on a
repeated stack roll; worth its own small fix (not done here).

**Shard Console facts**: 425 facts, 402 passed, 23 failed, the same 23 that fail on main on this PC (Golem buttons,
Haven deploys, P107-P208 ops facts, and the player-commands list missing artificerrank and requisitions); none involves
this change.

## Deviations and decisions for Chase

- **Not a port**: the Test Crystal is ours, a test-shard tool; it cannot act on live (Test Center only, deletes itself
  elsewhere). Nothing to record in the fidelity register.
- **Decided: `testCenter.skillGainMultiplier` retired**, not kept as a crystal default (section 2). The test shard's
  `Configuration-test/modernuo.json:218` still says 5.0 and now only logs a warning at start; delete that line when
  convenient. Live config unchanged.
- **Decided: crystals also come with a new Test Center character** (character creation and `[TCFill` share
  `PlaceKit`), not only through `[TCFill`. Off, so it changes nothing until used.
- **Strengths**: Off, 2x, 5x, 10x, 25x. Say if you want others.
- **The prompt's figures are out of date**: it says the shard runs `amountMultiplier` 5 and `chanceAttempts` 3. P191
  set the defaults to 2 attempts and 1x in code, but this PC's copies of the test shard's `Configuration-test/modernuo.json:117-118` (and
  live's `Configuration/modernuo.json:107-108`) still set 5 and 3 explicitly, and a set key wins over a default. Neither
  was changed here (out of scope, and gitignored); P191's notes have the config change for you.
- `LootBoxFanfareVerification` has a flaky fact (identical stacks merge); flagged, not fixed.

## For Chase

1. Rebuild the test shard on `sl-modernuo:cc-P190` (and, if you like, delete `testCenter.skillGainMultiplier` from
   `server\uo\modernuo\Configuration-test\modernuo.json`).
2. Log in a test character and type `[TCFill`; the bank now has a Test Crystal (and characters made from now on get
   one at creation).
3. Double-click it: Off is selected, and the gump says it only affects you.
4. With it Off, train one skill (Tactics or Wrestling on a training dummy, about 5 minutes) and note the gains; set it
   to 5x and do the same: gains should come about five times as often (the old test shard speed). A second character
   training next to you is unaffected.
5. For P189's play test, set it Off: Old Haven's apprentice boost is then the only thing that differs.

Staff: `[GiveTestCrystal` then target a player. No world command is needed: nothing is placed in any world by this
change, and live has no Test Center, so the crystal and the command do not exist there.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`:

```
Repo Result
---- ------
code dry run
docs dry run
```

(code: 9 files pending, docs: 1. Nothing over 5 MB; the largest touched file is CHANGELOG.md at 80 KB. Scratch,
red-run logs and patch trials are in the session scratchpad, outside both repos.)

P190 DONE
