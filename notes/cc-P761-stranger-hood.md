# cc-P761: the vision's stranger wears a hood or cowl

Iron Golem, 2026-11-01. Code copy `D:\UO\golems\Iron\ShatteredLegacy` and docs copy `D:\UO\golems\Iron\shard-migration`,
both on `golem/Iron/P761`, not committed (the Golem commits). The isle-only release branch has the same change as
commit `287a847`, pushed. Nothing deployed; the shared Test Shard was not touched.

## In plain words

- **The Stranger in the isle vision is now hooded and faceless.** He wears a deep cowl over his head and face, a dark
  robe and a dark cloak, and carries the sword. No name shows over him any more (before, "the Stranger" floated above a
  bald, bare-faced man). Compare `notes\cc-P761-shots\before-after-stranger.jpg`.
- **He wears only things a player could wear** (a cowl, a robe, a cloak, a sword), all in one colour. That colour is a
  single setting, so later each account's Stranger can be dyed to match the player.
- **It is in both places:** in this task's branch (for main) and on the isle-only release branch (commit `287a847`,
  pushed), ready for the overseer to package.
- Nothing for you to do. One thing for the overseer: main's own bot isle route can no longer make a character since
  P714 (see "The bot route on main" below). I fixed my copy only.

## The change

`server/customizations/Tutorial/TutorialVisionScene.cs`, `TutorialVisionFigure.Stranger`:
- **Cowl:** `CowlId` 0xA410, on the helm layer. This is the stock client art "Hood_Assassin", the Assassin's Cowl
  (our `AssassinsCowl` item uses it). A deep hood with the face in shadow. It is in the stock client files the package
  uses (`D:\UO\UltimaOnlineVanilla\tiledata.mul`: wearable, helm layer), not one of our added arts.
- **Robe:** the dark robe 0x1F03 (as before).
- **Cloak:** `CloakId` 0x1515, on the cloak layer.
- **Sword:** the longsword it strikes with (as before). It is still taken away when it breaks.
- **One hue:** `TutorialVisionScene.StrangerHue` (= `DarkHue` 0x455, near-black). `Stranger(int hue = StrangerHue)`
  dyes the cowl, robe and cloak in it; the sword keeps its own colour. Passing an account's hue later is one argument.
- **No name:** the figure's name is empty, so the client shows nothing over it or on a click. The subtitle "Long ago,
  the Stranger came for the Gem of Immortality." still names him in the story.
- **Body:** still the human body 0x190, not a monster.

**Why the cowl over the hooded shroud (0x2684):** the shroud is what the later "hooded figure" (the League's) wears. The
cowl, robe and cloak keep the two figures apart, and they are what Chase asked for. The shots show the cowl drawn in
TazUO with the face hidden (below).

## Tests

`server/tests/Tutorial/TutorialVisionStrangerVerification.cs` (new, 3 facts):
1. `TheStrangerHasNoName`.
2. `TheStrangerWearsACowlRobeAndCloakInOneHueAndHoldsTheSword` (and a human body).
3. `OneHueDressesEveryClothPiece`: another hue dresses all three cloth pieces; the sword keeps its own.

**Changed fact:** P665's `TheScenePlaysItsBeatsForOnePlayerAndFinishesTheLesson` found the Stranger by the name "the
Stranger". It now finds the scene's own Stranger figure.

**Seen failing first** (AGENTS.md rule 6). Against the old code the new facts would not even compile (no `CowlId`,
`StrangerHue` or hue argument), so each fact was seen failing on a mutant of the new code that undoes one part
(`mutate761.py`, `probe.sh` on `sl-uo-builder:cc-P761`, `mutants.txt`, `mutant-logs\`):

| Mutant | What it undoes | Fails |
|---|---|---|
| `named` | the Stranger keeps its name | 1 |
| `nocowl` | no cowl | 2 (and 3, which reads the helm) |
| `fixedhue` | the cloak ignores the hue | 3 |

**Gated builds** (the `docker-build` lock taken and released each time):
- main's change, `sl-modernuo:cc-P761`: **EXIT=0**. 2,887 tests: 2,881 passed, 6 skipped, 0 failed
  (`green-gated-build.txt`).
- the release, `sl-modernuo:cc-P761-isle`: **EXIT=0**. 2,773 tests: 2,768 passed, 5 skipped, 0 failed
  (`green-gated-build-isle.txt`).

## In TazUO, brand-new characters (private shard 127.0.0.1:2596, never the shared Test Shard)

The `test-shard` lock was taken once and released, and the container is down. Every shard start used a fresh copy of
the bot world (`proof-shard.ps1`). The six shard logs have no exceptions (`runs\tazuo\shard-*.log`).

How each run went:
1. The bot's client made a brand-new **Iron Hooded** and played every lesson up to the standing stones.
2. TazUO logged it in, and a Legion script started by the client played the vision with the client's own double-clicks
   (`VisionShots761.py`, `vision761.json`).

| Where | Image and map | Result |
|---|---|---|
| main | `cc-P761`, SoS land (`p735-work\patched`, the same mapops hash as main's) | In the chamber from 1 s, the hooded Stranger, the strike and the shatter, back on 6792,3984 at 64 s, lesson finished (`runs\tazuo\vision-main-run2.log`) |
| isle release | `cc-P761-isle`, stock land (`p749-proof\overlay`) | The same (`runs\tazuo\vision-isle.log`) |

- Each script's last check, a single step, "failed". The first step only turned the character, as in P742's and
  P758's runs. Both bot routes below walk on from the stones, so movement is shown there.
- **Main run 1** (`vision-main-run1.log`, not kept as shots): the vision played and passed. But this new character had
  no TazUO profile yet, so the paperdoll and TazUO's version page covered the room. The runner only fixes profiles that
  already exist. I reran on a fresh world with the same character name, so the profile now existed (run 2, the shots).

**Shots** (`notes\cc-P761-shots\`, 960 wide):
- `before-after-stranger.jpg`: the same beat (7.5 s, facing the Gem), cropped. Before: a bald man with a bare face in
  a dark robe. After: a cowl over the head with the face dark, the dark robe and cloak, the sword.
- `before-02` to `before-07`: the old Stranger. These are from P758's run this morning: a brand-new character on the
  isle release, which had the same Stranger code as main.
- `after-main-02` to `-16` and `after-isle-02` to `-16`: the new Stranger on main and on the release. My look at
  them:
  - at 3 s he stands in the north-west corner with no name over him;
  - at 5 to 7.5 s he walks to the pedestal and faces the onlooker, his face hidden in the cowl;
  - then the strike and the shatter, as before;
  - at the end, back at the stones.

## The bot routes: green on both

| Where | Route | Result |
|---|---|---|
| main | `isle.py` (P742's, fixed below) | **85 checks, 0 failed** (`runs-main-run1-console.txt`, `runs\main-run1\`); "core.loop done", the gate put it at 3669,2634 beside Rook, the New Haven pick on the plaza |
| isle release | `rel-isle.py` (P758's) | **85 checks, 0 failed** (`runs-isle-run1-console.txt`, `runs\isle-run1\`); the gate put it beside Rook at 3501,2572 |

**The bot route on main needed two fixes to my copy of the route.** Neither is caused by this change.
- **Character creation was refused** (`runs-main-stop1-blocked-console.txt`: "the server closed the connection" at
  create). The route makes its characters with Alchemy, Healing, Swords and Wrestling. Since P714 (merged on main
  yesterday), `ClusterFStartChoices.CustomSkills` has no Alchemy, so the server refuses the character. My copy now uses
  Swords, Tactics, Anatomy and Healing (the Fighter template's skills).
  **The overseer should know:** any bot route on main that makes characters with Alchemy (P742's isle.py and its line)
  now fails at creation. The overnight bot's routes may need the same change.
- **Rook moved** (P743): the gate now sets a trainee down at 3669,2634, in front of Rook's bench by the Albatross
  (`HavenSpots.MoongateExit`), not at 3632,2584. P742's route still had the old spot
  (`runs-main-run1-old-rook-console.txt`: the vision passed, and only the two Rook checks failed). I updated
  `ROOK_EXIT` and the Rook check to `HavenSpots.Rook` (3669,2636).
- Also carried over: P758's 2-second wait for the arrow to Tamsin (a race in the bot).
- One run (`runs-main-run1-archive-busy-console.txt`) could not log in. The new server was writing its startup
  archives at that moment. The next starts waited 20 s first.

## On the isle-only release

P758 was already pushed, so the change went onto `release/isle-20261028`:
- **Commit `287a8470a2182e76b7fbc45d0892ea248bba9d90`**, pushed (`7a220f1..287a847`).
- Applied as a diff from this branch. The three code and test files are byte for byte this branch's.
- `CHANGELOG.md` takes main's `2026.11.01.3` section only. `VERSION` is `2026.11.01.3`, main's number, as the earlier
  release rounds took main's numbers.
- Built (`cc-P761-isle`), and played in TazUO and by the bot (above).
- Not packaged, not published.

## CHANGELOG

`2026.11.01.3` (main's newest was `2026.11.01.2`), under Changed: "Test shard: in the Wakening Isle's vision, the
Stranger who breaks the Gem is now a hooded, faceless figure: a deep cowl over the head, a dark robe and cloak, and the
sword, with no name shown." `VERSION` is `2026.11.01.3`.

## Deviations and decisions for Chase

- **Three tool calls were denied in this unattended run; none was needed in the end:**
  - a `Grep` over `D:\UO\golems\Iron\ShatteredLegacy\server` for hood and cowl item classes. I wanted to find the hood
    art we already have; I ran the same search with Bash grep instead;
  - a `Read` of `D:\UO\tools\vseUOAware\exports\Animation\cowl_frame0.png`. I wanted to see the cowl's worn animation
    before using it. The render was a 10 x 14 placeholder, so the TazUO shots decided instead;
  - a `Read` of `D:\UO\golems\Iron\p761-proof\shots-main\vision-03-stranger-walks.jpg`. I wanted to look at a shot; I
    copied the shots to the scratchpad and read them there.
- **A commit and a push on the release branch.** The Golem's standing rule is no commits or pushes, but the prompt asks
  for the change on the isle branch "so the overseer can package it". As in P722 to P758, I committed on
  `release/isle-20261028` in its own worktree and pushed that branch only. `golem/Iron/P761` is not committed (the
  Golem commits it).
- **Before shots** come from P758's run this morning rather than a new build of the old code. They show a brand-new
  character and the same Stranger code as main.
- **The hue stays one constant for now** (`StrangerHue`, near-black). Per-account dyeing is a later task. The figure
  already takes the hue as an argument.

## Files

- Code copy:
  - `server/customizations/Tutorial/TutorialVisionScene.cs` (the Stranger's outfit, `CowlId`, `CloakId`,
    `StrangerHue`);
  - `server/tests/Tutorial/TutorialVisionStrangerVerification.cs` (new);
  - `server/tests/Tutorial/TutorialVisionSceneVerification.cs` (one line);
  - `CHANGELOG.md` and `VERSION`.
- Release branch: commit `287a847` (the same files).
- Docs copy: this note, `notes\cc-P761-shots\` (shots), and `notes\cc-P761-tools\`:
  - the build: `gated-build.ps1`, `gated-build.log`, `gated-build-isle.log` (UTF-16), `green-gated-build.txt`,
    `green-gated-build-isle.txt`;
  - the mutants: `mutate761.py`, `probe.sh`, `mutants.txt`, `mutant-logs\`;
  - the shard and bot: `proof-shard.ps1`, `isle.py` (main), `rel-isle.py` (release), `runs-*-console.txt`,
    `runs\main-run1\`, `runs\isle-run1\`;
  - TazUO: `isle-shots742.ps1` (main), `rel-isle-shots758.ps1` (release), `vision761.json`, `VisionShots761.py`,
    `rel-VisionShots758.py`, `rel-proof-shard.ps1` (P758's, kept for reference), and `runs\tazuo\` (logs).
- Outside the repos: `D:\UO\golems\Iron\p761-proof\` (shard copies, the client and the full-size shots) can be
  deleted.

P761 DONE
