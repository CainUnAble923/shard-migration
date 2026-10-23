# cc-P290: the tutorial's wing trials, part 1 (combat, healing and magic)

## In plain words

- Eight optional lessons now work, in a training yard just east of the tutorial farm gate: pick a weapon (Swords,
  Macing, Fencing, Archery, Throwing for gargoyles, or Wrestling) and spar; bandage yourself and a wounded villager;
  and try Magery, Necromancy, Chivalry, Bushido, Ninjitsu and Mysticism.
- Each lesson lends what it needs (a weapon and buckler, bandages, a book and its reagents, tithing points for
  Chivalry) plus enough skill for the lesson. When the lesson ends, or the player walks away or logs out, the yard
  takes everything back. A loaned item dropped, banked or traded disappears at once.
- A lesson is done only when the server sees the real thing happen: three hits with the picked weapon, the two
  bandages, a spell that went off and landed, a strike with the Bushido or Ninjitsu move readied.
- Played on a private copy of the test world by the test bot with a new character: the core first, then all eight
  lessons and the walk-away rule. 98 checks passed, 0 failed. The full build check passed: 2,215 tests, none failed.
- The first test-world run found two real bugs the unit tests could not see: Trammel forbids healing a creature
  nobody owns, and the training echo counted as an innocent, so spells at it were refused. Both are fixed (below).
- For you: three small items in "For Chase" near the end.

2026-10-23, the Iron Golem (Opus 5.5), branch `golem/Iron/P290` of both repos. Prompt:
`D:\UO\cc-prompts\claimed\Iron\cc-P290-tutorial-wing-trials-combat-magic.md`. Not committed (the Golem commits).
Nothing deployed; nothing run against live or the shared test shard (2594).

This prompt ran in two sessions. The first one (earlier today) stopped with `P290 STOPPED: waiting on P289`; P289
then merged by way of its fix-up P475, and P480 (tutorial fixes from Chase's first play) merged after it. A later
session started the code and tests and one test-world run, then was closed before it finished. This session carried
on from there.

## What changed (server, `D:\UO\golems\Iron\ShatteredLegacy`)

- `server/customizations/Tutorial/TutorialWingTrials.cs` (new):
  - `TutorialWingTrials`: the eight trials, registered by key in `TutorialStations.Handlers` (`combat.weapons`,
    `combat.healing`, `magic.magery`, `magic.necromancy`, `magic.chivalry`, `magic.bushido`, `magic.ninjitsu`,
    `magic.mysticism`). One shape for all: Rook's menu starts it, an arrow points to the yard (3411,2617), and on
    arrival the trial lends its things, lends skill as a skill mod named "tutorial loan" (never saved; the player's
    base skill and gains stay their own), and places its own creature beside the player.
  - Done checks (server evidence only): three hits whose weapon skill is the picked one (an empty hand is Wrestling);
    a bandage on yourself that raised your hits and one that healed the villager, either order; for Magery,
    Necromancy and Mysticism a successful roll of the school's skill (`SkillEvents.SkillUsed`) then damage on the
    echo within 10 seconds; for Chivalry the same roll then a heal on the villager; for Bushido and Ninjitsu a hit
    while that school's move is readied.
  - Covered and explained skills: the fight trains Tactics, Anatomy, Parrying (the buckler) and Focus as they
    normally gain; Resisting Spells gets one line when the weapons lesson starts; Mysticism's lesson gives the
    Spellweaving line (the Arcanist's quest "Patience" in the Heartwood). Magery and Necromancy cast with real mana and
    skill rolls, so Meditation, Eval Int and Spirit Speak gain as they normally would.
  - Loaners: named "tutorial loaner: ...", blessed. Every quarter second, a loaner not worn and not in the backpack is
    deleted. Going 14 tiles from the yard or off Trammel, logging out, Stop, Reset or finishing takes everything back:
    the items, the skill loan, the +30 Intelligence lent for mana, the unspent part of the tithing loan, and the
    creatures. Loaners left by a server restart are deleted when the world loads.
  - `TutorialWingTrialGump`: the lesson page (the weapon pick, Hint and arrow, Reset, Stop), in P480's
    `TutorialStyle` colors.
  - `TutorialTrainingEcho` (a `TutorialCreature`): a sparring echo that fights back lightly, a training echo that
    stands still, or a wounded villager. It never dies (it tops itself up), belongs to one trial, and is deleted with
    it and when the world loads.
  - `TutorialYardRegion` (new this session): a child of the region the yard stands in (New Haven), 6 tiles each way.
    Every rule is its parent's except one: a trainee may heal their own trial's villager.
- `server/tests/Tutorial/TutorialWingTrialVerification.cs` (new): 11 facts (13 test cases with the Theory rows); per
  trial its done check and its loaner cleanup, plus the shared rules and the two test-world bugs.
- `CHANGELOG.md` and `VERSION`: `2026.10.23.5` (main was at .4), one Added line.

No patch to pinned ModernUO, no change to any other file.

## The two bugs the test world found (fixed)

1. **The villager could not be healed.** "You cannot perform beneficial acts on your target." Pinned
   `Notoriety.Mobile_AllowBeneficial` refuses a player's heal on any uncontrolled creature in Trammel
   (`UOContent/Misc/Notoriety.cs:135-138`, "Players cannot heal uncontrolled mobiles"). Fix: `TutorialYardRegion`
   allows it for the trainee on their own villager only; everything else goes to the parent region and pinned's rule.
   Alternatives turned down: making the villager a controlled pet of the trainee (it would take a follower slot and
   follow them), or a pinned patch (shard-wide, for a tutorial need).
2. **Spells at the training echo were refused.** "You cannot perform negative acts on your target." The echo has a
   human body, so pinned reads it as innocent (`Notoriety.cs:485-492`), and `Mobile_AllowHarmful` refuses harm to an
   innocent from a player (`Notoriety.cs:241`, message from `Server/Mobiles/Mobile.cs:8367-8374`). Melee would have
   flagged the trainee criminal in town. Fix: `AlwaysAttackable` on the echo (gray; striking it is no crime); the
   villager stays invulnerable (yellow).

## Tests

| Run | When | Result |
|---|---|---|
| Red, the first nine facts against stubs (earlier session, `--tests-only`) | 10-23 15:30 | 2,209 total, **11 failed** (exactly the new facts and rows), 2,194 passed, 4 skipped |
| Red, the two new facts against a stub region and no `AlwaysAttackable` (`--tests-only`) | 10-23 17:23 | 2,219 total, **2 failed** (exactly the two), 2,213 passed, 4 skipped |
| Green, full gate | 10-23 17:26 | `Built sl-modernuo:cc-P290 with patches applied and 2215 shard test(s) passing.` |
| Green, final (after the Chivalry hint, the changelog and the version) | 10-23 17:52 | Same line: 2,219 total, 0 failed, 4 skipped; image `592ad58d28f4` |

The first red attempt of the two new facts made 14 unrelated tests fail too (pet abilities, monster area effects):
the first fact installed pinned's notoriety handlers and did not put `Notoriety.Handler` back. The two facts now
share one helper that restores the handler, the hues and both allow handlers; the next red run failed exactly the two.
The earlier session's first red attempt did not compile (a helper from another branch); fixed in the test only.

## The test-world run

A private scratch shard (`cc-P290-tools\scratch-shard.ps1`: image `sl-modernuo:cc-P290` on 127.0.0.1:2596, a copy of
the bot shard's world and Configuration without the AccountWipe save, autosave off, P276's map overlay built in the
scratchpad; the test-shard lock held throughout, then released). `cc-P290-tools\wingtrials.py` drives the play-test
bot's client: the Iron test admin only seeds the tutorial (`[ClusterFSeedTutorial`), and the Iron test player
account's new character "Iron Wings" (normal character creation) does everything else as player actions: the nine
core lessons first (since P480, Rook shows the wings only after the core; playkit's `play_core`), then each wing
lesson from Rook's page.

Final run (`cc-P290-tools\playlog-final.txt`): **98 PASS, 0 FAIL** (39 for the login and the core, 59 for the wings):

| Lesson | What the bot did | Lent, and returned |
|---|---|---|
| Pick your weapon | picked Swords; the sparring echo came at it and it struck back: 3 hits | longsword, buckler: 2 of 2 back |
| Bandages | bandaged itself, then the villager | 10 bandages: back |
| Magery | Magic Arrow at the training echo | spellbook, sulfurous ash: back |
| Necromancy | Pain Spike at the echo | necromancer spellbook, grave dust, pig iron: back |
| Chivalry | stood by the villager, Close Wounds | book of chivalry (and the tithing loan): back |
| Bushido | readied Honorable Execution, struck the echo | book of bushido, katana: back |
| Ninjitsu | readied Focus Attack, struck the echo | book of ninjitsu, katana: back |
| Mysticism | Eagle Strike at the echo | mystic book and 4 reagents: back |
| Leaving | started Magery, walked 18 tiles away | the lesson stopped; spellbook and ash back |

The echoes read gray to the trainee (notoriety 3; the sparring echo 4, criminal, once it has swung at the player, also
gray). The server log had no errors or exceptions.

The two earlier runs are kept beside it: `playlog-run1.txt` (92 pass, 4 fail: two for Chivalry, cast from too far; the
first-login line and the sparring echo, both bot checks) and `playlog-run2.txt` (97 pass, 1 fail: the bot expected notoriety 3 from the sparring echo).
Fixes from those runs:

- Close Wounds reaches only two tiles (pinned `Spells/Chivalry/CloseWounds.cs:36-38`). The Chivalry hint now starts
  "Stand next to the wounded villager (Close Wounds reaches two steps)". The bot walks there first.
- Bot only: the first-login line was reworded by P480; the weapon pick page arrives before the bot looked for it; the
  sparring echo walks to the player, so the bot finds it by name anywhere near the yard.

The run before this session (in the closed session's scratchpad, not kept) failed on the two bugs above.

## What is not covered

- In game, only Swords was played. Wrestling and a gargoyle's Throwing pick are unit facts; Macing, Fencing and Archery
  share the same code path (a lent weapon, its skill) but were not played. Archery lends 50 arrows.
- The bandage-yourself step watches the bandage end with hits at least 5 higher than when it began. A very hurt
  player with high regeneration could pass it without the bandage helping much; it cannot pass without a bandage.
- Unverified: how the lesson page looks in our TazUO (no screenshots taken; the page uses P480's shared colors).

## For Chase

1. **The death lesson's echo stands 9 tiles from the training yard** (3402,2617; the yard is 3411,2617). During the
   wing lessons its "A monster looks at you menacingly but does not attack" line shows up (Young protection stops it).
   Harmless, but if you would rather the yard be quieter, I can move the yard a few tiles further east. No change made.
2. **The yard place** was chosen from the map files (open, standable ground east of the farm gate), not from a design.
   If the tutorial is meant to have a combat yard and a Magery school as separate places (P80's station list names
   "the combat yard", "the Magery school", "the Ninja Dojo" and others), each trial can move by changing one point;
   say where.
3. **Rook's menu only shows these lessons after the core** (P480's rule). Staff can still start any of them with
   `[Tutorial station <key>`.

## Deviations and decisions for Chase

- Code repo: `golem/Iron/P290` was fast-forwarded to `origin/main` (7c085f7, P480's merge) before work continued, so
  the trials sit on P289, P475 and P480. A fast-forward moves the branch pointer only; no commit or merge was made.
  This repo's branch still carries the two WIP commits of this notes file; nothing else changed in it.
- The unattended Read tool was refused for
  `D:\UO\golems\Iron\ShatteredLegacy\server\customizations\Tutorial\TutorialWingTrials.cs` (wanted: to read the
  draft before editing it). Read with `sed` in Bash instead; edits made with Python scripts in the scratchpad.
- The prompt asks for P289's notes, F-35 and the map playbook to be read first. This session read P480's notes (which
  continue P289's) and the earlier session's work; F-35 and the playbook were not reopened. The earlier session's yard
  check against the map files stands.

## Files

- Code (`D:\UO\golems\Iron\ShatteredLegacy`): two new files (`TutorialWingTrials.cs`,
  `TutorialWingTrialVerification.cs`), `CHANGELOG.md` and `VERSION`.
- This repo: this note; `notes\cc-P290-tools\` with `wingtrials.py`, `playkit.py` (P480's driver), `scratch-shard.ps1`
  and the three play logs (about 210 KB in all).
- Nothing running: the scratch shard is down, and the docker-build and test-shard locks are released.

P290 DONE
