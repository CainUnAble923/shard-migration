# cc-P717: the first character on an account must take Tutorial Island; New Haven opens after

Iron Golem, 2026-10-28. Code copy `D:\UO\golems\Iron\ShatteredLegacy`, branch `golem/Iron/P717`. Chase's decision of
2026-10-28, building on P663's start choice. Not committed; nothing deployed; Haven not touched.

## In plain words

- **A new account's first character starts on Tutorial Island (test shard only).** On the character creation screen
  the second start now reads "New Haven (locked)", with one line saying why: the account's first character starts on
  the isle, and New Haven opens once a character finishes or skips the tutorial. Picking it anyway starts on the isle.
- **After that, New Haven is open for the whole account.** As soon as any character graduates or skips, every later
  character on the account sees "New Haven" as a normal choice, and it stays open even if that character is deleted.
  Staff accounts (GameMaster and up) always see both.
- **To test day one again:** in the reset window (`[ResetMyAccount`, `[ClusterFReset` or the Reset Stone) tick
  "League, flags"; New Haven is locked again. That window has never cleared the account's tutorial record itself, so on
  an account that already finished, the next pick still starts in New Haven ("your account has finished the
  tutorial"). For a true day one, also use staff `[Tutorial reset` on one of its characters (clears the record).
- **For you:** the "why" line is new text in the player package (number 1900016). Until the package is rebuilt and
  players update, the locked entry shows only its name, "New Haven (locked)". Test accounts that finished the tutorial
  before this build also show New Haven locked until one of their characters graduates or skips again (their picks
  still start in New Haven). Nothing to decide.

## What was built

| Part | Where (code copy) | What it does |
|---|---|---|
| The unlock | `Tutorial/TutorialStart.cs` | `HavenUnlockedFlag` ("tutorial.havenUnlocked"), an account flag (`ClusterFAccountData.Flags`, already saved; no version bump). `IsHavenUnlocked(account)` reads it; `Unlock(account)` sets it. |
| Set on graduate and skip | `Tutorial/ClusterFTutorial.cs` `Graduate`, `Skip` | Both call `Unlock`. `Skip` is the one path for Tamsin's or Rook's skip and `[Tutorial skip`; `Graduate` for Rook's button and `[Tutorial graduate`. Deleting the character never touches the account's flags, so the unlock stays. |
| The per-account list | `Tutorial/TutorialStart.cs` `Cities(account)`; `CharacterCreation.cs` `GetStartingCities(account)` | Staff (account GameMaster and up) and unlocked accounts get P663's two entries. Others get "Tutorial Island" and "New Haven (locked)" (cliloc 1900016, same coordinates). `ChoiceOf` reads the locked entry as the isle. With the tutorial off (live), the shared list as before. |
| The one-line patch | `server/patches/AccountHandler-per-account-start-cities.patch`, registered in `docker/uo/apply-patches.sh` after the other AccountHandler patch | Pinned's `AccountHandler.OnGameServerLogin` hands every account the same cached list (`GetStartingCities()`), at the character list, before any character exists. The patch passes the account. Why a patch: the generated `GameServerLoginEvent` gives no handler order, so a second handler could not rely on running after AccountHandler's to replace the list. |
| A forced New Haven | `TutorialStart.Decide` | While locked, a Haven choice is decided as the isle, so a client that sends P663's "New Haven" entry (its index is the same) starts on the isle, enters the core and is not skipped. Creation's placement (`OnCreated`) and the first login (`ConsumeAtLogin`) both go through `Decide`. |
| The resets | `ClusterFDevTools.ExecuteReset` | Its "League, flags" box already clears every account flag (`data.Flags.Clear()`), the unlock with them. Its chat line and the confirm list now say New Haven is locked again. `[ResetMyAccount`, `[ClusterFReset` and the Reset Stone all run this method. |
| The text | `ShardClilocs.NewHavenLockedCity` = 1 900 016; `player-package/vendor/shattered-legacy-cliloc/entries.json`, `registry.csv` | "Locked: your account's first character starts on Tutorial Island. New Haven opens once a character finishes or skips the tutorial." |

**One place decides the start city.** It is still `TutorialStart` (`OnCreated` and `ConsumeAtLogin`, both through
`Decide`). P714 (gated skills) is not in the code copy yet; no file under `server\customizations` names P714 (searched).
The note for whoever builds it: its template or skill rules belong in the creation code beside `TutorialStart.OnCreated`,
not in a second start-city rule.

### P663's eligibility table, changed rows

| Account state | "Tutorial Island" | "New Haven" (P663) | "New Haven" (now) |
|---|---|---|---|
| Fresh | isle | skip | **isle** (locked) |
| In core on another living character | New Haven, told where the tutorial is | New Haven | **the same as the isle pick** (locked) |
| Graduated or skipped | New Haven ("finished") | New Haven | New Haven (unlocked by that graduation or skip) |
| Tutorial character deleted mid-way | isle, re-bound | skip | **isle, re-bound** (locked) |

The second row is a judgment call worth knowing: while the account's first character is still in the core, a second
character made then starts in New Haven, as P663's isle pick already did. The tutorial runs once per account (one
record), so that second character cannot also run it. Chase's rule is about the start choice, and the choice there is
the isle only; the outcome for that row was not changed.

### Decisions

- **Shown locked, not hidden.** Chase allowed either. A hidden entry would make the list one long, and a client that
  still sent index 1 would be disconnected by pinned ("Invalid city selected during character creation",
  `IncomingAccountPackets.cs:158`) instead of starting on the isle. Shown locked keeps both indexes valid and gives the
  one line.
- **Only the flag unlocks.** A first version also counted an account whose tutorial record was already graduated or
  skipped (made before this build) as unlocked. The reset does not clear the record, so that version could not be
  locked again by the reset, and a marker flag to fix that broke `ResetStoneVerification`'s rule that a full reset
  leaves no account flag at all. So accounts finished before this build (test shard only; the tutorial is off on live)
  start locked, and their picks still start in New Haven by P663's "finished" row.

## Facts (`server\tests\Tutorial\TutorialIsleVerification.cs`)

New: a new account sees New Haven locked with its reason; graduating, and skipping (two cases), unlock it for the
account, keep it after the character is deleted, and the next character starts in New Haven; staff see both; a New
Haven pick while locked starts on the isle (core entered, not skipped, loop 0); the reset's flags lock it and the next
skip unlocks it again; an account that finished before this build sees it locked and starts in New Haven. Changed:
three eligibility rows (above), and the Graduated row now really graduates. The remedial fact skipped by choosing New
Haven on a fresh account; it now skips from the isle. The class releases idle isle copies before each fact (the new
facts claim copies; in the full suite the remedial fact ran out of them).

**Seen failing first.** The new API does not exist before the change, so the facts cannot compile there. As in P663,
`notes\cc-P717-tools\mutate.py` puts one old behaviour back behind the new API, and `probe.sh` runs the facts on
`sl-uo-builder:cc-P675` (the image of current main) with the copy mounted. `redrun.sh` ran all nine; summaries in
`notes\cc-P717-tools\red\`.

| Mutant | Failed / 32 | Facts it failed |
|---|---|---|
| `nolock`: always unlocked (P663) | 9 | the rows, new account locked, graduate/skip, forced pick, reset, finished-before |
| `forced`: a locked New Haven pick honoured | 5 | the rows, **forced pick**, finished-before |
| `hidden`: locked list drops New Haven | 2 | **new account locked**, reset |
| `nostaff`: staff get the locked list | 1 | **staff see both** |
| `deleted`: the unlock needs its character alive | 2 | **graduate/skip, kept after deletion** (both cases) |
| `nounlock`: graduate and skip set no flag | 5 | the rows, **graduate/skip**, reset's re-unlock |
| `norelock`: the reset keeps the flag | 1 | **reset** |
| `legacy`: a finished record counts as unlocked | 2 | **finished-before**, **reset** |
| `shared`: one shared list (pinned's AccountHandler) | 2 | **new account locked**, reset |

Then green: 32 of 32 on the probe.

The package's `player-package\tests\Cliloc-Overrides.Tests.ps1` failed first ("expected [16] but got [17]. one entry
per server constant") once the entry was added, and passes 10 of 10 after it was told of the new constant.

## Build

`docker/uo/build.sh -t sl-modernuo:cc-P717`, detached, under the `docker-build` lock (released). Windows had 2.4 to
4.0 GB free; the Docker VM 12.9 GB free with little cache, so nothing to drop.

1. First run: the patch failed (`Hunk #1 FAILED`). It had 3 lines of context before and 2 after, so it needed fuzz 1,
   which `apply_patch` does not allow. It was made again with `diff -u` (3 and 3) and checked at `--fuzz=0` on top of
   the test-center patch.
2. Second run: 2 of 2711 failed: `ResetStoneVerification.TheResetWithEverythingSelectedEmptiesEveryCharacter` (the
   marker flag, see Decisions) and the remedial fact (out of isle copies). Both fixed as above; the red run was made
   again against the changed code (the table above).
3. Third run: **green, `EXIT=0`**, "Built sl-modernuo:cc-P717 with patches applied and 2705 shard test(s) passing."
   2711 tests: 2705 passed, 0 failed, 6 skipped (client-data facts, for example `FoldVerification` and
   `SosMapsVerification`'s tile-and-Z facts).

## Not done, and why

- **No in-game picture of the city screen.** The isle's land is still not walkable on the test world (P663's note),
  and the line needs the package rebuilt. The list itself is pinned by the facts.
- **Nothing deployed**, no package built: not asked.

## Files

Code copy: `CHANGELOG.md` and `VERSION` (2026.10.28), `docker/uo/apply-patches.sh`,
`player-package/tests/Cliloc-Overrides.Tests.ps1`, `player-package/vendor/shattered-legacy-cliloc/entries.json` and
`registry.csv`, `server/customizations/CharacterCreation.cs`, `ClusterFDevTools.cs`, `ShardClilocs.cs`,
`Tutorial/ClusterFTutorial.cs`, `Tutorial/TutorialStart.cs`, `server/patches/AccountHandler-per-account-start-cities.patch`
(new), `server/tests/Tutorial/TutorialIsleVerification.cs`. This repo: this file and `notes/cc-P717-tools/`
(`probe.sh`, `mutate.py`, `redrun.sh`, `red/`).

P717 DONE
