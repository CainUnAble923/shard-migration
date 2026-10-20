# cc-P192: the Fountain of Youth (make an account Young again; hidden on live)

Gold Golem, 2026-10-20. Branch golem/Gold/P192 in both repos. Image `sl-modernuo:cc-P192`.

**This note is staff reading. The fountain's live rules, pool and sample spots are in `notes/admin/secrets.md` (with
renders in `notes/admin/fountain-renders/`). Never on the wiki.**

## Headlines

- **The fountain:** pinned's stone fountain (16 pieces), pale blue (hue 0x0480), with a sparkle over the basin while
  a player is near. Double-click within 2 tiles, or say "drink" within 2 tiles: a confirm gump that says what it resets
  and what it keeps, then the account is Young again.
- **Young again** = the account flag, every character on the account, and a fresh two-week Young clock; the New Haven
  tutorial back to the start with the drinker in it (so the Rootdeep Vault lets them in); the 26 New Haven trainer
  quests can be taken again (so P189's Old Haven boost applies again). Skills, stats, items, gold, the bank, guilds,
  the League, achievements and loops are untouched.
- **A Young clock, not a game-time wipe.** Pinned ends Young when the account's total play time reaches the duration,
  so nothing could make an account Young again. Now Young counts play time from a clock start kept in an account tag;
  with no tag it is pinned's rule exactly. TotalGameTime is never changed.
- **Test shard: fixed in New Haven** at 3497,2583,14, open ground west of the plaza, 9 tiles from the arrival tile
  (rendered; it touches no wall, so no junction sheet was needed).
- **Live: it roams.** A JSON pool of 20 hard-but-fair areas (18 usable now, 2 climbing-only for later); after every
  drink and weekly it moves to a random valid tile in a different area. Within 20 tiles of it nobody can Mark, recall or
  gate in, or place a house or boat, with pinned's normal messages. Staff: `[WhereIsFountain`, `[GoFountain`,
  `[MoveFountain`, all logged.
- **A secret achievement**, "Second Childhood", for the first drink from the roaming fountain.
- **Secret by design:** only `### Staff` in the CHANGELOG (never shown to players or the wiki, proven below), the admin
  notes, and code comments that tell wiki writers to keep out.
- Chase decides: the live abuse limits (built as settings, off), whether a "???" row should show for secret
  achievements, the trainer-quest reset on live, and two "check in game" access calls in the pool.

## 1. What Young is, and who decides "new"

Pinned (cited at d4531cd9):

- Account: `Account.Young` (Account.cs:252-262) is flag 1 inverted, behind `ContentFeatureFlags.YoungPlayerSystem`.
  `RemoveYoungStatus` (:830-853) clears it and every character's Young. `CheckYoung` (:855-861) removes it once
  `TotalGameTime >= YoungDuration`; it runs from a per-account timer started at login (:779-799, `YoungTimer` :1117)
  and at load (:206-209, :322-325). The login line (:810-828) counts the hours left.
- Character: `PlayerMobile.Young` (PlayerMobile.cs:678), set only at creation when the account is Young
  (CharacterCreation.cs:242). It ends with a murder count (PlayerMobile.cs:4121-4124).
- Skill total: OSI ended Young at 450.0 (PlayerMobile.OnSkillChange); P18 removed that
  (`server/patches/PlayerMobile-young-time-only.patch`).
- "Grow up": "I renounce my young player status" and P18's "I want to grow up!" open the renounce gump, which calls
  `RemoveYoungStatus`. Nothing about it is saved: there is no "grown up" state to reset beyond the flags.

What P18 built: the 2-week duration and day-and-hour login line (`ClusterFYoungPlayer.cs`,
`Account-young-duration.patch`), the time-only rule, and the Reset Stone / `[ResetMyAccount`
(`ClusterFResetStone.cs`, `ClusterFDevTools.cs`), which resets guild and exploration data and never touches Young.

Our own "new player" state, and what the fountain does with each:

| System | Keys on | Per | Fountain |
|---|---|---|---|
| Young protection, Young death teleport, the Burrows' Young limit (OldHavenBurrowsRegion.cs) | `PlayerMobile.Young` | character | reset (every character) |
| The first real loop ends Young (Tutorial/ClusterFLoops.cs:28-37) | `RemoveYoungStatus` | account | nothing to reset; a later loop ends Young again |
| The New Haven tutorial and the Rootdeep Vault (Tutorial/ClusterFTutorial.cs, Regions/RootdeepVault.cs) | `TutorialRecord` state and character (ClusterFAccountData.cs:1204) | account | reset to NotStarted, then the drinker is entered (InCore); `WasSkipped` kept (history); setting `resetTutorial` |
| P189's Old Haven apprentice boost (Regions/ApprenticeTraining.cs) | an unfinished New Haven trainer quest, never Young | character | the 26 quests' done records cleared on every character, so they can be taken again; setting `resetApprenticeQuests` |
| Guild starter path (ClusterFGuildStarterPath.cs) | guild membership, not newness | character | not touched (guild data) |
| Achievements such as "Didn't Read the Manual" | earned once | account | not touched; re-entering the tutorial does not re-award |

## 2. What changed, file:line (D:\ShatteredLegacy)

| File | What |
|---|---|
| `server/customizations/FountainOfYouth/FountainOfYouth.cs` (new) | `:57` the addon (saved: roaming, pool key, placed time; sanctum and sparkle rebuilt on load); `:191` the system: `:231` settings and commands, `:268` weekly move check, `:282` seeding, `:323` moving, `:346` "drink", `:364` refusals (cooldowns, limits), `:423` the drink, `:453` `MakeYoung`; `:607` the confirm gump (its text is `Body`); `:647` `[WhereIsFountain`'s gump |
| `server/customizations/FountainOfYouth/FountainPool.cs` (new) | `:71` access kinds; `:161` the random pick; `:212` the spot checks; `:243` region rules; `:256` the walled-in check; `:297` the built-in pool |
| `server/customizations/FountainOfYouth/FountainSanctumRegion.cs` (new) | `:46` no houses; `:48` no Mark, no recall or gate in (staff exempt); `:69` boats |
| `server/customizations/ClusterFYoungPlayer.cs:18-49` | the Young clock (`ClockStartTag`, `YoungPlayed`) |
| `server/patches/Account-young-duration.patch` | two more lines: `CheckYoung` and the login line use `YoungPlayed` |
| `server/patches/BaseBoatDeed-fountain-sanctum.patch` (new) | the boat deed refuses a sanctum (BaseBoatDeed.cs:152-161 has no region virtual) |
| `docker/uo/apply-patches.sh:383-386, :695-698` | the comment for the changed patch; the new patch applied |
| `server/customizations/ClusterFAchievements.cs:66, :143, :1060-1072, :1101` | `TriggerKind.FountainOfYouth`, its earned line, "Second Childhood", its key. The file is now ASCII: its 3,166 box-drawing characters and 21 em dashes became hyphens (three were in code: the "ACHIEVEMENT UNLOCKED" gump label, the `[achievements` line and the persistence item's name) |
| `server/tests/Misc/FountainOfYouthVerification.cs` (new) | the facts below |
| `server/tests/Misc/AchievementEarnedLineVerification.cs:100, :323` | 78 achievements become 79 |
| `CHANGELOG.md`, `VERSION` | 2026.10.20.9, `### Staff` only |

Serialization: `FountainOfYouthAddon` is a new saved type at version 0 (two scalar fields and a string; no
collection of its own beyond BaseAddon's components). The Young clock and the last-drink time are account tags,
which pinned already saves (Account.cs:646-700). The tutorial record and quest records are existing data changed in
place; no schema changed.

## 3. Placements

**Test shard (Fixed):** centre 3497,2583,14 Trammel; pieces on x 3495-3498, y 2581-2584, all land at Z 14 with no
statics (vseUOAware `inspect_map_region`), open ground between the bank and the plaza; the nearest shard item is the
winter decor's snow pile at 3494,2583 (seasonal, beside it). Render with the fountain drawn in:
`notes/admin/fountain-renders/newhaven-fountain.png` (scripts/mapbuild `isorender.py`, art unpacked from the client's
UOP into the session scratchpad). It touches no wall, so the junction sheet does not apply.

**Live (Roaming):** the pool, the rules and 13 sample spots found on the real Trammel map are in
`notes/admin/secrets.md`; six renders in `notes/admin/fountain-renders/`. Mode is `fountainOfYouth.mode` (`auto`:
Fixed on a Test Center shard, Roaming otherwise). Nothing in New Haven on live.

How a spot is chosen (FountainPool.cs): a random eligible entry (access available, its region exists, not the
current entry), then up to 400 random tiles in it, area-weighted, until one passes: the fountain's 4x4 fits on one
flat surface where a mobile can stand (pinned `Map.CanSpawnMobile`, the check `BaseSpawner.GetSpawnPosition` uses,
BaseSpawner.cs:468), no house at any piece, every piece inside the entry's region and in no town, guarded, house,
jail, no-travel or tutorial region, and 40 standable tiles join it within 10 steps (so it is not walled into a pocket).
That last check is local. Whether an area is reached on foot or needs a boat is the entry's `access`, set by hand.

Access kinds: `none` and `boat` are available (High Seas is on); `climbing` becomes available by itself once a type
named `ClimbingBoots` exists in the build. An unknown kind is never available.

**The sanctum** (FountainSanctumRegion.cs): a 41 x 41 square (radius 20, a setting), a child of whatever region holds
the fountain, one priority above it, so it wins there and passes every other rule to that parent. Unnamed, so no
player text can name it. It refuses, to players: Mark (Mark.cs:38, :72 ask the caster's own region), recall, Sacred
Journey, Gate Travel and the Bracelet of Binding into it (RecallTo / GateTo), houses (AllowHousing) and boats (the
patch). Messages are pinned's defaults. It is removed when the fountain moves or is deleted, and rebuilt on load.

## 4. The achievement

"Second Childhood", 10 AP, Legacy, hidden; flavor "You found the Fountain of Youth. Try not to waste it this time.";
earned line "drank from the Fountain of Youth". Granted the first time an account drinks from a roaming fountain;
`TryGrant` never re-awards. Its box tier is the loot table's for 10 AP (`TierForAchievement`,
LootBoxes/ClusterFLootTable.cs:145-160) and anything below tier 4 plays the minor fanfare
(LootBoxes/ClusterFLootBoxes.cs:148-153). On the test shard the fixed
fountain does not grant it; to test it there, set `fountainOfYouth.mode` to `roaming`, seed, `[GoFountain` and drink.

Other names considered: "Back to Square One" ("The Fountain of Youth. You drank it. Everyone is very proud of you.")
and "Born Yesterday" ("You found the Fountain of Youth. The System has updated your file to 'new'.").

Not built as asked: the prompt wants a locked "???" row. This shard shows no row at all for an unearned hidden
achievement (ClusterFAchievements.cs:2002-2003; 20 hidden achievements before this one); this one follows that rule. A "???" row would
change the list for every secret achievement: Chase's call.

## 5. Secrecy, proven

- `CHANGELOG.md`'s `### Staff` is parsed into `Staff`, which is never in `Sections()`: not the login bulletin, not
  the generated wiki page (`ShardVersion.cs:24-25`, `:47`). Fact W1 renders a Staff note about the fountain and finds
  it in neither. The wiki page is built inside the server and copied out by `scripts/Publish-PatchNotes.ps1:11-31`.
- The wiki's pages are files in the code repo (`docker/wiki/content/pages/`, plus the Legion macros deploy); the
  website is `docker/website/html`; none reads the docs repo (`scripts/websites.json`). Grep of `docker/wiki`,
  `docker/website` and `website` for the fountain: no file.
- The one writer that reads `notes/` is the Crystal wiki catch-up agent (cc-P217). `notes/admin/secrets.md` opens
  with a keep-out line for wiki writers, and the code headers say SECRET. Chase: add it to that Golem's next prompt.
- No player text names a place: the confirm gump's `Body`, and the achievement's title, description, flavor and earned
  line, are checked against every pool region, key and facet name (fact W1).

## 6. Tests

Built and tested only through the repo's build script with `-t sl-modernuo:cc-P192` (docker-build lock taken and
released).

**Seen red first**, in two feature-off builds (stubs, so the tests compile):

| Fact | Red run | Red result | Green |
|---|---|---|---|
| Y1 drinking makes the account and both characters Young, resets the tutorial and the trainer quests; skills, a sword, 1,234 gold and 400 hours of play untouched | 1 (MakeYoung did nothing) | account still not Young | pass |
| Y2 the Young clock restarts; an account that never drank keeps pinned's whole-TotalGameTime rule | 1 (YoungPlayed ignored the tag) | 16 days 16 hours instead of 0 | pass |
| S1 the test seeder places it at 3497,2583,14 once, 16 pieces, blue, no sanctum | 1 (Seed placed nothing) | none placed | pass |
| R1 200 moves over a five-area test pool with a guarded strip, a climbing entry and a missing region: every spot valid, inside its area, outside the guarded strip, never the same entry twice in a row, all five used | 1 (Move found nothing) | "move 0 found no spot" | pass |
| N1 Mark refused inside (staff allowed), recall and gate in refused, houses and boats refused, the edge outside, Mark allowed again after it moves and after it is gone | 1 (sanctum rules off) | Mark allowed | pass |
| A1 the achievement: hidden; a fixed drink does not earn it; a roaming drink does and moves the fountain; no re-award | 1 (no achievement, no move) | not earned | pass |
| C1 a second drink within the misclick cooldown refused; the account cooldown, skill and age limits off by default and refusing when set; out of range refused | 2 (Refusal always null) | drink allowed | pass |
| T1 mode, pool entry, placed time and location survive a save and load; it registers and its sanctum comes back | 2 (nothing done after load) | not registered | pass |
| W1 a Staff note about it is in neither the wiki page nor the bulletin; no player text names a pool place | 2 (a pool region written into the gump text) | "names Covetous" | pass |

Red run 1 also failed `AchievementEarnedLineVerification`'s two count facts (78 achievements registered; now 79):
updated. Red run 2: exactly C1, T1 and W1 failed; everything else, the six facts above included, passed.

**Green:** 1,615 tests, 1,611 passed, 4 skipped, 0 failed ("Built sl-modernuo:cc-P192 with patches applied and 1611
shard test(s) passing"). P18's `YoungPlayerVerification` passes on the changed patch.

The test host has no map data, so R1 proves the rules, not real tiles. Real tiles: a script with cc-P15's port of
pinned `Map.CanFit` (`notes/cc-P15-tools/fit.py`) ran the same rules over the real Trammel map and found a valid spot
in every Trammel pool entry within 400 tries (`notes/admin/secrets.md`), six rendered. The Ilshenar and Malas entries
were not sampled.

**Shard Console facts:** 426 facts, 402 passed, 24 failed. None is about world commands or this change: the 23 that
fail on this PC on main (Golem buttons, Haven deploys, the player-commands list missing artificerrank and
requisitions) plus `P149_AwayModeButtonsAndTheGolemTabLines` (P149's away mode, merged into main before this branch).

## Deviations and decisions for Chase

Not a port: the fountain is ours (Chase's request), a deviation from OSI by existence; it changes nothing OSI has
except the Young duration rule's starting point, which only the fountain moves. For the register:
"Young counts from a per-account clock start; the Fountain of Youth resets it" (`ClusterFYoungPlayer.YoungPlayed`).

Decisions:

1. **Live abuse limits** (settings, all off): proposed `fountainOfYouth.accountCooldownDays` 30 (or 90),
   `maxSkillTotal` and `maxAccountAgeDays` left off (the fountain is hard to find; the cooldown is enough).
2. **Trainer quests on live:** resetting them lets a character take the 26 quests' rewards again. Proposed
   `resetApprenticeQuests` false on live unless the cooldown is long. The tutorial's graduation rewards (the first loot
   box, the starter pet) can likewise be earned again; `resetTutorial` false on live if that matters.
3. **"???" row for secret achievements** (section 4): not built; a list-wide change.
4. **Pool access to check in game:** Hythloth's isle and the Labyrinth's entry are marked as I read them (Hythloth
   `boat`, Labyrinth `none`); the two `climbing` summits' coordinates are placeholders until climbing exists.
5. **Pinned's Young timer** starts at the next login after a drink; until then nothing ends Young this session (two
   weeks of play is far off). Not patched.
6. **The Crystal wiki Golem** reads `notes/` and the code: tell it to skip `notes/admin` and anything marked SECRET.
7. **numpy and Pillow** were installed into this PC's user site-packages (python -m pip install --user) so the
   mapbuild renderer could run; scripts/mapbuild's README expects them.

## For Chase

Test shard (with this build):

1. Rebuild the test shard on `sl-modernuo:cc-P192`.
2. `[ClusterFSeedFountainOfYouth dryrun` (says it would place it in New Haven at 3497,2583,14), then
   `[ClusterFSeedFountainOfYouth`.
3. With a grown-up character (say "I want to grow up!" and confirm, if it is still Young), walk to the fountain west of the plaza, double-click it (or say "drink"), read the gump, Drink.
4. Check: "You feel young again." and the Young line ("for another 14 days of play time"); log out and in: the login
   line says the same. In Old Haven with a New Haven trainer quest (take one again: it is offered once more), the
   Accelerated Skillgain icon and faster gains. Walk to the Rootdeep hole: the Vault door lets this character in.
5. Optional, the live behaviour on the test shard: set `fountainOfYouth.mode` to `roaming` in Configuration-test's
   modernuo.json, restart, delete the fixed one (`[WhereIsFountain`, Go there, `[delete` its pieces), seed again,
   `[WhereIsFountain`, `[GoFountain`, try to Mark beside it (refused), drink (the achievement, then it moves),
   `[MoveFountain`.

Live (when there is one): `[ClusterFSeedFountainOfYouth dryrun`, then `[ClusterFSeedFountainOfYouth` (it picks a
secret pool spot), and set the cooldown you choose.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`:

```
Repo Result
---- ------
code dry run
docs dry run
```

(code: 12 files pending; docs: this note, `notes/admin/secrets.md` and 7 renders. Nothing over 5 MB: the largest render
is 828 KB. The unpacked client art (149 MB) and the scripts are in the session scratchpad, outside both repos.)

P192 DONE
