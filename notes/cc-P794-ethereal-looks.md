# cc-P794: new earned ethereal mount looks

Iron Golem, 2026-11-04. Code copy `D:\UO\golems\Iron\ShatteredLegacy` and docs copy `D:\UO\golems\Iron\shard-migration`,
both on `golem/Iron/P794`, not committed by me. Nothing deployed, packaged or published. The shared Test Shard was not
touched; the play was on a private proof shard, 127.0.0.1:2596. Main only.

**State: finished.** Chase answered the routes question on 11-04 (`Iron-P794-20261104-090330-66a5`): the recommended mix. The routes are
wired and tested, and the CHANGELOG and version are done.

## In plain words

- **Seven new ethereal mounts can now be earned:** windrunner, lasher, dark tiger, light tiger, ancient hellhound, boura and
  peacock. Each is a blessed statuette you double-click to ride, solid rather than see-through.
- **Four are in the League shop** at 1,750 AP: the peacock for 1,500 Renown, the other three for 2,000. They never come out of a
  loot box.
- **Three are achievement rewards:** the lasher for all 38 New Haven trainer quests, the boura for all 16 ore types, the hellhound
  for 200 in three skills. Anyone who already earned one finds it in their backpack at their next login, once per account.
- **For you:** nothing to do. The prices are starting guesses, and each one is a setting if play shows it is wrong.

## How each is earned (Chase's choice, 11-04)

Nothing here is a plain store sale.

| Mount | Route | Earned how | Why |
|---|---|---|---|
| Peacock | League shop | 1750 AP, 1,500 Renown | the gentlest look, matches the top real shop mount |
| Windrunner | League shop | 1750 AP, 2,000 Renown | an ethereal cannot die, so above the real mounts' 750 to 1,500 |
| Dark tiger | League shop | 1750 AP, 2,000 Renown | as above |
| Light tiger | League shop | 1750 AP, 2,000 Renown | as above |
| Lasher | Achievement | `legacy.new_haven_all`: all 38 New Haven trainer quests | a long, finishable goal |
| Boura | Achievement | `mining.master_prospector`: all 16 ore types | a beast of burden for the miner |
| Ancient hellhound | Achievement | `skills.triple_master`: 200 in three skills | the hardest reachable skill goal |

Why these rows:
- **Shop rows** follow P365's reward mounts: kind `Mount`, 1750 AP, which already keeps them out of every loot box
  (`LeagueShop.BoxPool`). The prices are settings, placeholders to tune in play.
- **Achievements were checked as reachable.** I first picked `skills.triple_grandmaster` for the hellhound, but it is one of 6 retired
  achievements, keyed to 300 above the 200 cap, so no one can earn it. These three are not retired and have no reward yet
  (`notes\cc-P794-tools\achievements.py`).
- **Back pay:** `SpawnRewardItems` pays only at the moment of earning, and only to a character online then. Anyone who already earned
  one of the three would get nothing, so `EtherealLooks.PayOwed` pays these three instead, see below.

## How the wiring works

- **Shop:** `EtherealLooks.ShopRows()` joins `LeagueShop.Stock`, keys `ethereal.<look>`. Stock is built once, so the rows read their
  settings as they are built, and a price change needs a restart.
- **Achievements:** the three defs name their look in `rewardItems`, which gives the "+1 item" line in `[achievements`. `SpawnRewardItems`
  skips those types.
- **`PayOwed`** runs when one of them is earned by an online character, and last in every login's `GrantAtLogin`. It pays what is
  earned and unmarked, then sets `ethereal_paid.<achievement>` in the account's saved achievement counters. This needs no new saved
  field, and an existing world needs no seeding. It also covers a staff grant to an offline account.
- **One per account, not per character:** earned sets are per account, so the first character to log in gets it.
- **A revoke does not reset the mark,** so revoking and re-granting pays nothing more. The dev tools account reset clears both.
- **Rules:** no skill or stat points, power scrolls, bless deeds or property artifacts. No engine change and no patch.

## The parts

| # | Part | State |
|---|---|---|
| 1 | The looks | **Done.** `server/customizations/Mobiles/Mounts/EtherealLooks.cs`: `EtherealLook : EtherealMount` and seven classes, generated serialization, no fields of their own, no core edit, no patch. |
| 2 | Solid | **Done.** `EtherealHue` reads the setting, default 0. Pinned's `MountMe` only applies that hue, so they stay solid. Seen in the client, hue 0 on all seven. |
| 3 | Companion | **Confirmed on the server, see below.** |
| 4 | Rewards | **Done:** Chase's mix, below. |
| 5 | Config | **Done:** `clusterf.etherealLooks.hue` 0, `.followerSlots` 1, `.shopAp` 1750, `.renown.peacock` 1500, `.renown.windrunner`, `.renown.tiger` and `.renown.light-tiger` 2000. |

### IDs

The prompt says IDs from ServUO stock `Ethereals.cs`. Five of the seven are there (lines 1080 to 1243): boura, hellhound, both tigers,
lasher. **Stock has no ethereal windrunner or peacock**, so those two came from the prompt and were checked against the client instead.
`notes\cc-P794-tools\tile.py` reads all seven: every statuette's tiledata name matches its creature (`windrunner_south`,
`Bird_Peacock_Mount`, `Tiger Statue` and so on), and TazUO's table maps every mount item to the right body. The prompt gives the tiger
as 0x3EC7 "light and dark": per stock, 0x3EC7 is the light one and 0x3EC8 the dark. Two classes, because a reward is made from a
type with no arguments. `EtherealTiger` is the dark one, as stock's default is.

### Decisions in the code

- **They cost one follower slot while ridden.** P790's notes said ethereals cost no slots, and the Codex review was right that this is
  wrong: pinned's `FollowerSlots => 1`, and ServUO stock agrees. Kept stock, per the fidelity rule. The setting can make it 0 if Chase wants.
- **Their own names**, not stock's labels: `DefaultName`, so they read correctly whatever the client's labels hold.
- **Single click:** pinned labels every ethereal "Veteran Reward", wrong here, so `EtherealLook` overrides it.

## Companions

**What is proven:** facts on all seven: a bonded companion wears the mount, saves and loads ridden, dismounts into its own pack, and its
owner's follower count does not change. One that dies becomes a ghost and keeps the ethereal.

**What is not:**
- **No game path puts a companion on one.** `BaseCompanion` has no mount code. The research note's "hand it over and it mounts when you
  do" is not built, and this prompt asked to confirm, not build. The facts set `Rider` directly.
- **Not seen in the client.** Only the facts cover it.
- **Unbonded is a different story:** a Blessed item in an unbonded pet's pack dies with the pet. Real companions are always bonded
  (`CompanionParty.cs:108`), so this does not arise for them.

## Tests

`server/tests/Mobiles/Mounts/EtherealLooksVerification.cs`: 7 fact names, 31 cases, each look through its art, the real double-click
and cast, save and load in the pack and ridden, and a companion ride.

**Seen failing first** (P764's method, `mutate794.py`, `run-mutants.sh`, `mutant-logs\`, `mutant-summary.txt`). The unchanged code passes
31 of 31. All 11 mutants go red, and all 7 fact names go red in at least one: translucent, slots, click, nocast, wrongmount, wrongdark,
wrongart, name, nosave, death, unblessed.

**The routes:** `server/tests/Mobiles/Mounts/EtherealRoutesVerification.cs`: 7 fact names, 18 cases with the two existing facts that
list the shop's rows. Those two were updated: F-13's table gained the four rows, and `EveryMountHasItsRoute` now looks at `mount.` rows
only. `mutate794routes.py`, `run-route-mutants.sh`, `route-mutant-logs\`, `route-mutant-summary.txt`. All 13 mutants add failures over
the unchanged code: norows, wrongprice, boxable, wrongrow, apfixed, renownfixed, nomark, noread, unearned, nologin, nograntpay, double,
noreward.

One failure runs through that summary, `_base` included: `TheStockIsF13sStarterTable...` fails under this narrow filter with a
null in `TreasuresOfTokuno.RewardEra`, reached through the older pigment row. Something the full suite sets up first is missing. It passes
in the gated build below, so no mutant is counted as red on that fact alone.

**Gated build** (`docker\uo\build.sh -t sl-modernuo:cc-p794`, logs in `notes\cc-P794-tools\`, UTF-16):

| Run | Result | Cause |
|---|---|---|
| 1 | compile error | missing `using Server.Companions` in my test |
| 2 | 1 failure | my death fact used an unbonded companion, which cannot exist in play |
| **3** | **green: `gated-build.log`** | 3,072 tests: 3,066 passed, 6 skipped, 0 failed. `EXIT=0` |

Built on this branch's base, **without P793's peacock**, which main has since merged. This branch was not rebased, as the rules say. Its `VERSION` and CHANGELOG section (2026.11.04.2) sit on an older base, so expect a small conflict at the merge there. `EtherealPeacock` needs only client art, so it does not
depend on it. If both merge, `Peacock` and `EtherealPeacock` are separate classes and do not clash.

**Memory:** free memory read 7.4 GB before the first build, then 3.1 GB when the harness killed my background watcher (the build itself
was detached and finished), then 1.7 GB after the mutants. Each time it was WSL page cache: the documented drop returned 6.1 and 10.7 GB
and touched no container or image. It was never truly under 3 GB. I used foreground polls after that.

## TazUO shots

`notes\cc-P794-shots\`, one real TazUO run on the private proof shard (`sl-modernuo:cc-p794`, the test-shard lock held), rig copied from
P764 into `notes\cc-P794-tools\`, with `Shots794.py`. On that copy only, `clusterf.tutorial.islandGate` is off.

All 29 checks in `walk.log` pass. For each look: the statuette in the pack, ridden through the real cast with the right mount item,
solid, dismounted with the statuette back. `sheet-all-seven.jpg` shows all seven, ridden and after walking; `<look>-1-ridden.jpg` and
`<look>-2-walked.jpg` are the full shots. I looked at all seven on the sheet.

**A mount actually earned:** `earned\`, a second run on the routes' image. `Iron Earned` starts with no statuette. The real `TryGrant`, through a
staff grant of the mining chain, shows the achievement window and the boura statuette arrives by itself, and the character rides it. All
4 checks in `earned\walk.log` pass, and I looked at both shots: `earned-1-popup.jpg` and `earned-2-ridden.jpg`.

**Not seen in the client:** a shop purchase (the row in the gump) and the login hand-over. Both are covered by facts through the real
`Purchase` and `GrantAtLogin`. No fact saves and reloads the paid mark: it relies on the achievement counters' existing save, which the
reward stores already use.

**Not proved:** the ride's walking animation (stills only, the character was stopped when shot), and the statuettes' art in the backpack,
which the proof's checks found by ID but I did not look at.

## Files

- **ShatteredLegacy:** new `server/customizations/Mobiles/Mounts/EtherealLooks.cs`, `server/tests/Mobiles/Mounts/EtherealLooksVerification.cs`,
  `server/tests/Mobiles/Mounts/EtherealRoutesVerification.cs`; changed `server/customizations/ClusterFAchievements.cs`,
  `server/customizations/LeagueShop/LeagueShop.cs`, `server/tests/Misc/LeagueShopVerification.cs`,
  `server/tests/Mobiles/Mounts/RewardMountVerification.cs`, `CHANGELOG.md`, `VERSION`.
- **shard-migration:** this file, `notes\cc-P794-tools\`, `notes\cc-P794-shots\`.

P794 DONE
