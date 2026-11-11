# cc-P861: extra NPC name lists and [VBuild statify

## In plain words

- **People in the same town no longer share a name.** When two shopkeepers or townsfolk in one town have the same name,
  the newer one gets a new name; the older keeps theirs. It runs by itself after every restart, again five minutes
  later, and then hourly. On a copy of the live world it renamed 8 repeats on Trammel and 2 on Felucca at start-up. Named
  characters like Elara Voss or Mara are never touched.
- **More names** for gargoyles, elves, druids, paladins (with titles), gladiators (with titles), juka and meer, after
  Sirenix's name lists. The gargoyle shopkeepers had only 19 names and now have 145. The gargish outcast is named from
  the gargoyle lists again, as in ServUO.
- **For staff: `[VBuild statify`** freezes a placed addon (a fountain, a forge) into plain statics where it stood, so it
  looks the same but is no longer a live addon. `[VBuild undo` puts the addon back. It refuses an addon in a player's
  house or one our seeders put back by themselves.
- Nothing for you to do.

Iron Golem, 2026-11-10. Code copy `D:\UO\golems\Iron\ShatteredLegacy` and docs copy on `golem/Iron/P861`. Main only.
Read first: P854's notes (items 1 and 2). The downloads `D:\UO\third-party\code\expanded-names` (Sirenix) and
`addon-converter` (The_Ice_Phoenyx_Rising) were read as reference; nothing built, run or copied from them. Only the
names were read out of the `names.xml`. All play on the private proof shard (2596).

## 1. The name lists

**Data, beside pinned's:** `server/data/names-shard.json`, made by `notes/cc-P861-tools/names861.py` from the
download's `names.xml`. The Dockerfile copies it to `Data/ShatteredLegacy/` (pinned's `Data/names.json` is never
edited). It has two kinds of row:
- **12 new lists**, P854's pick: elf male (143) and female (171), gargoyle male (45) and female (45), druid (75),
  paladin (190) and paladin title (52), juka (146), meer (126), gladiator male (107), female (111) and title (100).
- **3 extensions** of pinned lists, the author's own "expanded" lists, adding only names pinned lacks: gargoyle vendor
  (+126), savage rider (+47), golem controller (+50).
- Left out, as P854 advised: the Greek, graveyard and drow lists, and the author's copies of pinned's other lists. His
  male and female lists are identical to pinned's.

**Read by eye**, as P854 asked:
- The elf names carry accents; they are folded to plain letters (a name goes to the client as ASCII), each starts
  with a capital, and a few entries the author ran together with full stops are split.
- Typos are corrected in the titles and druid names ("the Victorius", "the Grizley", "Mountiangleam", and others), and
  one paladin title was missing its "the".
- Dropped: two gladiator titles unfit for a town NPC ("the Bastard", "the Lecherous") and the paladin title "the
  Paladin of Fist of Dauros".
- The paladin first names are invented syllables, as P854 warned; they read as names, so they stay.

**Code, `server/customizations/Names/ShardNames.cs`** (new):
- **Initialize:** reads the file and adds the new lists to pinned's name table, so `NameList.RandomName` finds them.
  It extends the three lists with only the missing names. A second apply changes nothing.
  - Pinned keeps that table private, so ours reaches it by reflection, as `ShardBodyTypes` does for body types. If
    pinned changes the field, the start fails loudly and the facts go red.
- **The town rule.** Within one town region, people (not players, pets or summons) whose names came from a list never
  share one:
  - every repeat but the oldest (lowest serial) gets a new name from the same list, one nobody in that town has;
  - a fixed name (not in any list) is never touched.
  - It runs on the tick after every world load (the hook is set in Configure), five minutes later (the spawners fill
    the towns after a start), then hourly. An existing world is fixed by itself.
  - Staff: `[ShardNames status | dedupe [dryrun]`.
- **`GargishOutcast`** now takes its name from "gargoyle male" or "gargoyle female", as in ServUO, through
  `ShardNames.RandomName(type, fallback)`. Where our lists are not loaded (the test host), it falls back to pinned's
  "gargoyle vendor" as before.

"New Haven townsfolk and League NPCs": the rule covers every town region, New Haven's included. The League's own NPCs
(Elara Voss, Aldous Penhallow) have fixed names, so the rule leaves them alone, and the stock vendors and townsfolk
around them are what it renames.

## 2. [VBuild statify

`server/customizations/StaffBuildTools/AddonStatify.cs` (new), after The_Ice_Phoenyx_Rising's A2S, rebuilt in the
Visual Builder's way. `[VBuild statify`, then target any part of an addon. Each part becomes a plain `Static` where it
stood, keeping its art, hue, name and light.

Unlike the A2S:
- **It is one undo step.** The addon is parked on the internal map, not deleted, so `[VBuild undo` puts it back exactly
  with all its parts. It is deleted for good when its step falls off the 100-step history or the session is
  forgotten (`[VBuild forget`).
- **The statics count as the session's own,** so erase, hue, nudge and the capture work on them at once.
- **It refuses:**
  - something that is not an addon in the world;
  - an addon in a house (a player's);
  - an addon a seasonal decor tracks (`ClusterFSeasonalState.IsTracked`, new) or a winter decor piece;
  - the addon types our seeders place and keep (Alembic hall, the two mine camp tents, the three registrar office
    pieces, the League hall). The seeder would put one back, and the frozen copy would sit under it.

Changes to `ClusterFVisualBuilder.cs`:
- the verb, and the usage and description text;
- each undo step gains a parked-addon list;
- undo restores the parked addon;
- a dropped step or `forget` deletes it;
- the store moves to **version 1** (it saves the parked list), and a version 0 save still reads.

## Tests

Two new fact files, ten facts:
- **`server/tests/Misc/ShardNamesVerification.cs`:**
  1. The shipped file is clean and sits beside pinned's.
  2. Apply adds and extends once, and refuses what pinned lacks.
  3. In one town the repeats are renamed but the oldest, and nothing else is: another town, a fixed name and a pet
     are left alone; a dry run renames nothing; a second sweep renames nothing.
  4. The outcast is named from the gargoyle lists by sex.
- **`server/tests/Misc/AddonStatifyVerification.cs`:**
  1. Statify leaves a plain static per part (art, hue, name, light) and parks the addon.
  2. Undo brings it back.
  3. The refusals change nothing.
  4. A step falling off the history, or `forget`, deletes the parked addon.
  5. The store keeps a statify across a restart and reads a version 0 save.
  6. The command targets a part.

**Watched red, then green** (`notes/cc-P861-tools/red-all.txt`; `red-all.sh`, one container on `sl-uo-builder:bot`):
- **Red:** the code before the change (git HEAD's builder plus the two names the facts compile against, HEAD's
  seasonal switch and outcast, an inert stub of the new classes, no data file). **All 10 new facts failed.**
- **Green:** all 45 passed with the real code and data, including the existing Visual Builder, decor capture and
  creature facts.

**Gated builds** (`gated-build.ps1`: docker-build lock, page cache dropped first, `latest` not moved; logs UTF-16).
Final `sl-modernuo:cc-p861`: **EXIT=0, 3375 passed, 0 failed, 6 skipped** (`gated-build.log`). Two earlier builds are
kept:
- `gated-build-1-outcast-name.log`: two existing gargish outcast facts went red because the test host has no name lists
  of ours, which is why the fallback was added;
- `gated-build-2-before-load-hook.log`: green, before the load-hook fix below.

## In game (TazUO, `notes\cc-P861-shots\main\`)

Private proof shard (2596) only, under the test-shard lock, on a fresh copy of the bot world on `sl-modernuo:cc-p861`
(`run861.ps1`, kit in `notes/cc-P861-tools/kit`: P859's, repointed, with `Walk861.py` and `stage861.py`).
- The Player-account trainee "Iron Names" stands on main's New Haven square and watches.
- Staff hands did only what only staff can: added two provisioners named Aaron and a stone fountain, ran the sweep,
  `[VBuild statify` and `[VBuild undo`, and read back where the server holds the addon.

**Every check PASS** (`walk.txt`):
- **Names:**
  - Both provisioners read "Aaron the provisioner" (`p861-1-twins-before.jpg`).
  - After the sweep the older is still Aaron and the other is "Casey the provisioner" (`p861-2-twins-after.jpg`).
  - Stage-out: `New Haven: ... Aaron -> Casey ('male')`.
- **On its own at start-up,** the shard log says: lists applied, `12 list(s) added, 3 extended, 1534 name(s) new`,
  then the load sweep `Trammel: 8 repeated name(s) renamed across 1842 town people` and `Felucca: 2`. The copied
  world was fixed by itself.
- **Statify:**
  - The fountain stood as an addon (`p861-3-fountain-addon.jpg`).
  - Statify said "Froze the StoneFountainAddon into 16 plain statics".
  - The same art now stands there as new items (`p861-4-fountain-statics.jpg`, which looks the same), and the server
    holds that addon on the internal map.
  - Undo ("Undone: 17 item(s)") brought the addon's own parts back at 3655,2605,0 (`p861-5-fountain-back.jpg`).

**Run 1** (`cc-P861-shots/run1/`, kept) showed two things:
- **My check was too strict:** a wandering townsperson stepped onto a twin spot. The rule itself worked there too
  ("Aaron -> Alastair").
- **A real bug: the sweep never ran by itself.** The shard log had the lists applied but no load sweep, because the
  world loads before Initialize, so a WorldLoad hook set there never fires. The manual sweep then found 9 repeats on
  Trammel. The hook moved to Configure (the Peacock's way), and the five-minute sweep was added for the start's spawns.
  Run 2 shows it working.

## Deviations and decisions for Chase

- The "unique in a town" rule is my reading of "so New Haven townsfolk and League NPCs stop sharing names". Bigger
  lists alone could not do it: pinned's male and female lists already hold 1,500 and 2,132 names, and sixty-odd random
  picks from them repeat often. The rule renames only list-drawn names, never a fixed identity.
- `[VBuild statify` cannot be tested inside a house in the facts (a test house is costly to raise); the house refusal
  is in the code and was not exercised.
- Free memory was 3.0 to 4.3 GB at each build.

## Files

- `ShatteredLegacy`:
  - new: `server/customizations/Names/ShardNames.cs`, `server/customizations/StaffBuildTools/AddonStatify.cs`,
    `server/data/names-shard.json`, `server/tests/Misc/ShardNamesVerification.cs`,
    `server/tests/Misc/AddonStatifyVerification.cs`;
  - changed: `server/customizations/ClusterFVisualBuilder.cs`, `ClusterFSeasonalSwitch.cs`,
    `Mobiles/Normal/GargishOutcast.cs`, `docker/uo/Dockerfile`, `CHANGELOG.md`, `VERSION` (**2026.11.10.7**: .3 to .6
    are P869, P872, P871 and P860).
- `shard-migration`:
  - this file;
  - `notes/cc-P861-tools/` (names861.py and its output, edit_vbuild.py, the red copies, red-all.sh and results,
    gated-build.ps1 and the three logs, build-then-run.ps1, run861.ps1, the kit);
  - `notes/cc-P861-shots/` (`main\`, `run1\`).

P861 DONE
