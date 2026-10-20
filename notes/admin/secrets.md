# Admin notes: staff-only secrets

**STAFF ONLY. Never on the wiki, the website, the player patch notes, the Discord or any player-facing text.**
Wiki writers (people or Golems, including the Crystal wiki catch-up): skip everything in `notes/admin/` and every
feature this file names. If a feature is listed here, it does not exist as far as the wiki is concerned.

Why this folder is safe (checked 2026-10-20, cc-P192):

- The wiki's patch notes page is generated inside the server from `CHANGELOG.md`'s player sections only
  (`server/customizations/ShardVersion.cs:47`: `### Staff` is never in `Sections()`, the bulletin or the wiki), then
  copied out of the running container by `scripts/Publish-PatchNotes.ps1:11-31`. Nothing reads this repo.
- The wiki's pages are files in the code repo, `docker/wiki/content/pages/`, and only what is written there is
  published; its Macros pages come from the TazUO Legion scripts (`scripts/websites.json` deploy "wiki-macros"). The
  public website is `docker/website/html` in the code repo (deploy "website"). None of them reads `D:\UO\shard-migration`.
  So a secret reaches the wiki only if someone writes it into `docker/wiki/content/pages/`.
- The only other wiki writer is the Crystal Golem's catch-up (cc-P217), an agent that reads the code, `CHANGELOG.md`
  and `notes/`. It is told not to by this file's header; Chase should also add "skip notes/admin and anything marked
  SECRET" to its next prompt (cc-P192 notes, For Chase).

## The Fountain of Youth (cc-P192)

What it does: drinking makes the drinker's whole account Young again (the flag, every character, a fresh two-week
Young clock), restarts the New Haven tutorial with the drinker and clears the done records of the 26 New Haven
trainer quests. It keeps skills, items, gold, guilds, the League, achievements and loops. Code:
`server/customizations/FountainOfYouth/` in the code repo; full notes `notes/cc-P192-cont-fountain-of-youth.md`.

### Test shard

Fixed in New Haven, centred on 3497,2583,14 (open ground west of the plaza, 9 tiles from the arrival tile). Render:
`fountain-renders/newhaven-fountain.png`.

### Live: it roams

- It stands at a random valid spot in one pool area. After every drink, and every `fountainOfYouth.moveEveryDays`
  (7), it vanishes with an effect and appears in a different pool area (never the same area twice in a row).
- The pool is `Configuration/fountain-of-youth.json` on the shard (written from the built-in list on first start;
  edit the file to add areas, it is read at every move). Each entry: `key`, `map`, `region` (a pinned region name) or
  `rects`, `access` (`none`, `boat`, `climbing`) and `why`. Entries whose access does not exist yet are skipped:
  `climbing` waits for a ClimbingBoots item.
- A valid spot: the 4x4 fountain on one flat surface where a mobile can stand, no house, inside the entry's region, not
  in a town, guarded, house, jail, no-travel or tutorial region, and not walled in (40 standable tiles join it within 10
  steps). Whether the area is reached on foot or by boat is the entry's `access`, chosen by hand.
- Within 20 tiles of it (`fountainOfYouth.noMarkRadius`), players cannot Mark, cannot recall or gate in, and cannot
  place houses or boats. They get the normal "cannot" messages, nothing that hints at a fountain.
- The secret achievement "Second Childhood" ("You found the Fountain of Youth. Try not to waste it this time.") is
  earned the first time an account drinks from the roaming fountain; hidden until earned; 10 AP.

The built-in pool (20 entries; 18 used now, 2 climbing-only):

| Key | Map | Area | Access | Why |
|---|---|---|---|---|
| covetous | Trammel | Covetous | none | deep dungeon behind Vesper's mountains |
| destard | Trammel | Destard | none | dragon dungeon west of Trinsic |
| shame | Trammel | Shame | none | elemental dungeon west of Britain |
| wrong | Trammel | Wrong | none | prison dungeon north of Yew, mazy |
| hythloth | Trammel | Hythloth | boat | daemon dungeon (check whether its isle needs a boat) |
| fire | Trammel | Fire | boat | Fire Island |
| ice | Trammel | Ice | boat | Dagger Isle |
| terathan-keep | Trammel | Terathan Keep | none | past the swamps, fought through |
| orc-cave | Trammel | Orc Cave | none | three-level orc warren |
| ice-isle-cave | Trammel | Ice Isle Cave 2 | boat | island on purpose |
| avatar-isle-cave | Trammel | Avatar Isle Cave | boat | island on purpose |
| north-territory-mine | Trammel | North Territory Mine 2 | none | forgotten mine in the north |
| mt-kendall | Trammel | Mt Kendall | none | mine tunnels under Mt Kendall |
| spectre | Ilshenar | Spectre Dungeon | none | moongate, then a long walk |
| sorcerers | Ilshenar | Sorcerer's Dungeon | none | five levels of casters |
| ancient-lair | Ilshenar | Ancient Lair | none | the ancient wyrm's lair |
| labyrinth | Malas | Labyrinth | none | a maze (check its entry in game) |
| yomotsu | Malas | Yomotsu Mines | none | through the elder gazers |
| peak-kendall | Trammel | 2576-2600, 360-384 | climbing | a summit above Minoc (coordinates to check) |
| peak-serpent | Trammel | 1680-1704, 600-624 | climbing | a crag in the Serpent's Spine (coordinates to check) |

Sample placements found on the real Trammel map with the same rules (cc-P15's CanFit port; renders in
`fountain-renders/`): Covetous 5452,1815,0; Destard 5236,970,-40; Shame 5605,196,0; Wrong 5732,974,0; Hythloth
5948,102,22; Fire 5829,1418,0; Ice 5676,329,0; Terathan Keep 5434,3134,-60; Orc Cave 5357,2017,0; Ice Isle Cave 2
4013,306,0; Avatar Isle Cave 4609,3819,0; North Territory Mine 2 1607,1005,0; Mt Kendall 2593,479,60. These are
samples, not where it is: `[WhereIsFountain` says that.

### Staff commands (all logged)

- `[WhereIsFountain`: map, coordinates, region, pool entry, how long it has been there, and a Go there button.
- `[GoFountain`: puts you beside it.
- `[MoveFountain`: moves the roaming fountain now.
- `[ClusterFSeedFountainOfYouth [dryrun]`: places one if none exists (New Haven on a Test Center shard, a pool spot
  elsewhere). `fountainOfYouth.mode` (auto, fixed, roaming) overrides the choice.

### Settings (`modernuo.json`)

`fountainOfYouth.enabled` (true), `.mode` (auto), `.moveEveryDays` (7), `.noMarkRadius` (20),
`.misclickCooldownMinutes` (5), `.accountCooldownDays` (0 = off), `.maxSkillTotal` (0 = off),
`.maxAccountAgeDays` (0 = off), `.resetTutorial` (true), `.resetApprenticeQuests` (true), `.seedOnWorldLoad` (false).
Proposed for live (Chase decides): `accountCooldownDays` 30 or 90; `resetApprenticeQuests` false if quest rewards
being taken twice matters; the skill-total and age limits off.
