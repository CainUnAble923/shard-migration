# cc-P689: credits, the fidelity register and the wiki (SoS swap S16)

Iron Golem, 2026-10-30. Code copy `D:\UO\golems\Iron\ShatteredLegacy`, docs copy `D:\UO\golems\Iron\shard-migration`,
both on `golem/Iron/P689` (main at the P687 merge). Not committed; nothing published, deployed or put on the wiki.

## In plain words

- **Zigholtul is credited everywhere the plan lists, ready for the swap day.** The download's README already names his
  map (P674). His source file now also lists every change we made on top of his land, and records that his terms were
  re-read today, unchanged.
- **What players will be told on the swap day is written but held back.** Patch notes go straight to players (the
  login bulletin and the wiki), so the swap day's lines wait in one file beside the map's on/off switch. The release
  that turns the map on copies them in. A new check stops the build's tests if they leak out early, or if the map is
  turned on without them.
- **The wiki has a world map page for the new land**, kept in the drafts until the swap day: the towns you know and
  what moved, the seven new towns and how to reach each, the keeps, the sealed dungeons and the fenced-off land, and
  how Felucca differs. Every line was checked against the merged swap work, which corrected several of the earlier
  draft's guesses.
- **For you: nothing to do now.** The overseer has two things to look at before the swap release (see "For the
  overseer"), and one register row to add.

## What was done, by the list in P673 section 4

| Destination | State before | What P689 did |
|---|---|---|
| Package README (`player-package/payload/README.txt`) | P674 wrote the `app\map\` entry crediting "Siege of Sosaria Trammel Map 3.0 by Zigholtul" with the URL and that Trammel and Felucca are built on it; P713 makes the build drop it while the switch is off, and gate 4 wants it when on | Checked against P673's wording; nothing to change |
| `SOURCE.txt` (`player-package/vendor/sos-trammel-map/`) | Source, version, terms quoted with the 2026-10-12 read date | Terms re-read 2026-10-30 (WebFetch of the servuo.dev page): the same invitation, no license, update 2 "the final update". New section "Our changes on top of his map": the patch (Burrows, isle, P687's 8,389 boulders, none of his statics removed) and the server side (P676 to P687 by prompt). New section on the go-live release's three credit steps |
| CHANGELOG player line and in-game patch notes | none | **Held**, not written into CHANGELOG.md: `player-package/vendor/sos-trammel-map/go-live-changelog.md` holds the go-live section's Changed lines (6) and a Staff line, with the conditions to check before copying (Blackthorn and P691, Rootdeep's opening, Valunstead's access, any opened dungeon). The in-game patch notes are the same lines: the server reads them from CHANGELOG.md. CHANGELOG.md got only a Staff line (2026.10.30) saying where they wait |
| The wiki's world-map page | P697 drafted three pages in markdown on its own branch (not merged) | `docker/wiki/content/pages/uo/drafts/world_map.txt` (`uo:drafts:world_map`, DokuWiki), linked from the drafts list; the go-live file lists the five wiki steps for the swap day (move it to `uo:world`, link it, rewrite New Haven's Old Haven directions and the Rootdeep draft's way in, Blackthorn on the dungeons page, overwrite-sync) |
| Fidelity register row | none | Proposed below for the overseer: `docs\` in the docs repo is not ours to edit (AGENTS.md working agreement 2) |
| Data-file headers (S3's regions, S6's decoration) | written by those prompts | Not in this prompt's list (P689's list is section 4's first six); not checked |

Chase's decisions applied: **a fresh test world on swap day**: this prompt planned no migration, so there was none to
drop; nothing in the held lines or the wiki talks about moved characters or houses. **Blackthorn moves in P691**: the
held Blackthorn line is conditional on P691 not having shipped, and the wiki page says it "will come back in a new
place". **Fence and seal for 1.0**: the page and the lines describe the five fences and the 34 sealed dungeons.

## Why the player-facing credit is held, not written

`CHANGELOG.md` is "the only place patch notes are written" (its own header): the server shows every Added, Changed
and Fixed line in the login bulletin, and `Publish-PatchNotes.ps1` puts them on the wiki. P713 keeps the map out of
releases until the swap goes live (switch.txt `off`), and its gate refuses a README that credits the map while off.
A player line saying "Trammel and Felucca are a new land" in the next release would announce land the download does
not have. So the lines wait beside the switch, as P713's README credit does, and the new fact holds both states.

## The world map page, checked against the merged swap

P697's prompt asked to "check it on the map rather than redoing it". Its drafts were written on 10-27, before S3 to
S15 merged; checked against those prompts' notes and outputs on 2026-10-30:

| P697's draft said | What merged | Source |
|---|---|---|
| Valunstead is landmark country round Yew | an island in the far north-west with no dock, moongate or teleporter: boat or magic | P688 table, group 7 |
| "A new desert landmass joins Nujel'm to Moonglow" | Moonglow, Magincia and Nujel'm are one land | P688 group 2 |
| (not covered) | Buccaneer's Den and Serpent's Hold are walkable from the mainland | P688 "What changed from stock" |
| the extra gate landmarks at Hammerhill, Kameron Kove and Dragonstorm remain scenery | his three extra gate spots have no gate art at all; nothing to see | P679 plain words |
| (not covered) | Felucca's way to Ter Mur is gone with its old land; Trammel's remains | P679 |
| Blackthorn proposed to stay out of 1.0 | switched off until P691 moves it into the Fold (Chase's 10-27 decision) | P677, P689 prompt |
| closed areas planned with a fog message | five fenced areas, the line "Thick fog rolls in; the way is lost.", no recall, gate, mark or housing, boats pass, both facets | P687 |
| custom dungeons sealed | 34: 33 teleporter-only plus the walkable Swamp of Desolation fenced; the list includes his own Khaldun, Solen Hives and Britain Sewers, so the page names them to avoid "the classic X is closed" confusion | `notes/cc-P687-tools/out/dungeon-entrances.json` |
| new towns' services "still need verification" | six towns have bankers, healers, smiths, provisioners, guards and townsfolk; Elandrim Nur Shaz is a guarded town with no people; five keeps garrisoned | P682, P676 |
| Fort Yondall (not covered) | its main gate is static doors that do not open; the gatehouse stairs lead in | P688 section 1 |
| New Haven in the author's Haven | yes: square start, League office and guilds in his buildings, gate east of the square; Felucca names the ground Ocllo | P678, P679, P686 |

What the page does not claim: which classic dungeons are open (it points to the existing Dungeons page), Rootdeep's
opening (the Burrows are a draft), opening dates, and anything about other facets beyond "do not change".
Coordinates are the author's region boxes from `notes/sos-map-author-spots.md` and P688's bank points. Not checked in
a game client: the swap is not live anywhere players or the bot can see it with our client (P688 left that for P735).

## Tests

`player-package/tests/Map-Overrides.Tests.ps1`, new fact `P689_TheSwapDaysCreditWaitsForTheSwitch`:
- switch off: `go-live-changelog.md` exists, holds at least three Changed lines, the first credits "Siege of Sosaria
  map by Zigholtul"; none of the held lines is in CHANGELOG.md; the wiki page is in `uo:drafts`, credits him, and is
  not in `uo:world` yet;
- switch on: the newest CHANGELOG section's player lines credit Zigholtul, and the page is in `uo:world`.

| Run | Result | Output |
|---|---|---|
| Red: the new test file on a `git archive HEAD` copy | the new fact fails ("go-live-changelog.md holds..."), the other 16 pass | `notes\cc-P689-tools\red-map-overrides-on-head.txt` |
| Green: the work copy | 17 facts, 0 failed | `green-map-overrides.txt` |
| Mutant: a held line pasted into CHANGELOG's 2026.10.30 Changed list | the fact fails, naming the line | `mutant-held-line-leaked.txt` |
| Mutant: switch.txt `on` with no go-live steps done | the fact fails ("the newest CHANGELOG section credits Zigholtul") | `mutant-switch-on-not-done.txt` |

The mutant copies held only the folders the fact reads, so the two P713 gate-4 facts also fail there (the build
script cannot run in a partial copy); they pass on the full work copy. `player-package/tests/No-TazUO-Page.Tests.ps1`
(it reads CHANGELOG.md): 7 of 7. A Staff-only newest section is a shape the server's parser already covers
(`server/tests/Misc/PatchNotesVerification.cs`, `StaffOnlyOnTop`); no server build was run, as nothing in the
server changed. Windows PowerShell 5.1 throughout.

`tools/progress.py` run with `SL_SHARD` and `SL_MIGRATE` at the Iron copies: README.md, dashboard.html and
tools/progress.json regenerated.

## For the overseer

1. **The fidelity register row** (for `docs\fidelity-principle.md`; next free number when written, D-179 by the
   notes on 2026-10-30, since notes have issued up to D-178):

   | # | What changed | What a player notices | Status | Note |
   |---|---|---|---|---|
   | D-179 | **Ours (cc-P669, P673, Chase 2026-10-26).** Trammel's and Felucca's land is Zigholtul's Siege of Sosaria Trammel Map 3.0, not OSI's: new towns, keeps, islands and 34 dungeons of his (sealed until each has monsters), five unfinished areas fenced, New Haven in his Haven town, Moonglow, Magincia and Nujel'm one land, Felucca's Ter Mur route and T2A Arena gone, Blackthorn's dungeon off until P691 moves it. Goes live with the swap release (switch.txt on) | every route, coordinate and outside-guide map for Trammel and Felucca is different; the shard wiki's world map page (uo:world:world_map from the swap day) documents it | `visible` | `cc-P673`, `cc-P689` |

   The register's own "wiki debt" reading applies: this is the largest single item of it, which is why the page exists.
2. **The server picks the new map by the files, not the switch.** `docker/uo/Start-TestShard.ps1:179` builds the
   overlay from the SoS map whenever `player-package/vendor/sos-trammel-map/files/base-map1legacymul.uop` exists;
   `switch.txt` is read only by the package build. A desk with `files\` (any Golem that ran `Add-SosMap.ps1`) starts a
   test shard on the new land while a switch-off package draws stock Trammel. Releases are held, so this matters only
   if a server release goes out before the swap's.
3. **The map patch is now made on his land, and an off package applies it to stock Trammel.** `trammel.mapops` was
   re-based on SoS by P675, and P687 added 8,389 boulders at the foot of his cliffs. With the switch off,
   `Apply-MapOps.ps1` puts the same patch on the player's stock Trammel; its blocks report as drifted and are still
   patched (the fact `ADriftedBlockIsReportedAndStillPatchedAndAMovedRemovalIsLeft`). The isle and Burrows sit on void
   in both maps, but the boulders would stand on stock Trammel ground near towns. Not checked in a client here; worth
   a look before any switch-off package release after P687's merge.

## Deviations

- **The fidelity row is a proposal in these notes, not an edit**: the prompt names `docs\fidelity-principle.md`, and
  AGENTS.md's working agreement 2 says never edit `docs\` in the docs repo; P701's cross-check says the same for P689
  ("hand fidelity changes to the overseer").
- **The CHANGELOG player lines and the wiki page are held, not live** (reasons above). The prompt's list is done in
  the form that can ship; the copy-in is one step of the swap release, written beside the switch.
- **The Read tool was denied** on `player-package/vendor/sos-trammel-map/SOURCE.txt` (unattended run). I wanted to
  read it before editing it; I had already read it whole with `cat`, and edited it with a short Python script that
  asserts each anchor occurs once.
- **P697 is not merged** (it is on `golem/Verite/P697`); its drafts were read with `git show` as input, not copied in.
  Its markdown drafts stay on its branch; the wiki page here is the one to publish.

## Files

- Code copy:
  - `player-package/vendor/sos-trammel-map/SOURCE.txt` (terms re-read, our changes, go-live credit steps);
  - `player-package/vendor/sos-trammel-map/go-live-changelog.md` (new: the held lines and the wiki steps);
  - `docker/wiki/content/pages/uo/drafts/world_map.txt` (new) and `uo/drafts/start.txt` (its line);
  - `player-package/tests/Map-Overrides.Tests.ps1` (the P689 fact);
  - `CHANGELOG.md` (2026.10.30, Staff) and `VERSION`.
- Docs copy: this note, `notes\cc-P689-tools\` (red, green and mutant outputs), and progress.py's regenerated
  `README.md`, `dashboard.html`, `tools/progress.json`.

P689 DONE
