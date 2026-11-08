# cc-P854: staff tools and minigames from the 11-07 and 11-08 scout, assessed

## In plain words

- **11 downloads were looked at:** six staff tools, a spell hotbar, a bestiary page maker, ticket teleporters, a
  list of NPC names, and two event games (a team battle and a living chess board).
- **Worth taking:** the **name lists**, which add elf, gargoyle, druid, paladin, juka and meer names so NPCs in
  one room stop sharing a name. Later, **Battle Chess**, where two players move living pieces that fight for each
  square: a showpiece game for the Haven inn next to the casino.
- **Already covered:** the two static copy and export tools do what the decor capture (P812) already does. The
  spell hotbar is built into TazUO. The "Retouching Tool" is not a decorating tool: it makes an ethereal mount
  see-through.
- **For you:** pick from the "port first" list below. One thing to decide is whether you want a staff-run team PvP
  event (Color Wars) at all. Also, the bestiary folder holds a `.dll` and a `.bat` that the scout says it left
  zipped but are in fact unpacked; nobody should run them.

Iron Golem, 2026-11-08. Assessment only: no code, nothing built, run or copied out of `D:\UO\third-party`. Docs copy
`D:\UO\golems\Iron\shard-migration` on `golem/Iron/P854`; code copy `D:\UO\golems\Iron\ShatteredLegacy` read only.
`docs\` not edited. The 11 rows are now in `D:\UO\third-party\CODE-INTAKE.md` (none existed; backup
`CODE-INTAKE.md.bak-20261108-p854`).

## What was compared

- **Staff and Golem tools:**
  - P812's decor capture: `server/customizations/StaffBuildTools/DecorCapture.cs` and `[VBuild capture`. It writes
    items, and map statics when `CaptureMapStatics` is on, to `[Decorate` data. Addon parts are written as plain
    statics. Doors keep their facing. There is a build form and a world form.
  - P798's suggested `[VBuild statify`, which is not in `ClusterFVisualBuilder.cs`'s usage line.
  - `[AnimLocate` (P812) and vseUOAware's `search_sounds` and `export_sound`.
- **Player features:**
  - TazUO at our pinned commit `3212623f` has its own `SpellBarManager`
    (`src/ClassicUO.Client/Game/Managers/SpellBarManager.cs`, in my `D:\UO\golems\Iron\tazuo-p374` checkout).
  - Our bestiary work is the League hunt bestiary (`server/customizations/Mobiles/Bestiary`: parts, mini bosses,
    cull packs), not a book or web pages.
  - Travel is `ShardMoongates.cs` and the school gate. Pinned has the stock teleporter family, with none that takes
    an item.
  - Pinned's names live in `Distribution/Data/names.json`: 28 lists.
- **Events:** P810's Staff Hub Events tab (egg hunt, mine maze, Festival Tokens) and P811's gold-only casino in the
  Haven inn.

## Every folder

Terms: no folder states a license. The scout's default applies: community work, credit the author, ship only inside
the player package or the private repo, do not repost. "Ser" counts hand-written Serialize overrides.

| Folder | What it is | Fit | Port cost | Terms | Recommendation |
|---|---|---|---|---|---|
| `addon-converter` (The_Ice_Phoenyx_Rising) | A2S: target a placed addon and it is replaced by statics with the same name, hue, light and weight | Deco Golems and staff: freeze a placed addon into the map dressing | 1 .cs, 59 lines, 0 Ser | credit the author | **Idea only.** P798 suggested `[VBuild statify` (break a staff-placed addon into statics, refuse a seeded one); P812 built the capture and not this. About 60 lines of ours in StaffBuildTools when a deco job needs it. |
| `copystatics` (Ravenwolfe, after Arya) | Copy the map statics in a box into a generated addon `.cs` | Staff tools | 1 .cs, 581 lines, 0 Ser | credit Ravenwolfe and Arya | **Skip.** `[VBuild capture` with `CaptureMapStatics` reads map statics into decoration data, and data is what Golems want (no generated C#). |
| `nerun-static-exporter` (Norman Lancaster, after NeRun and Joeku) | `[StaticExport <file>`: items in a box written to a `[Decorate` `.cfg` | Staff tools | 1 .cs, 329 lines, 0 Ser | "all credit goes to" NeRun and Joeku | **Skip.** The same job and the same format as `[VBuild capture`, which also keeps door facings and offers a relative (build) form. |
| `retouching-tool` (xG00BERx) | OSI's Retouching Tool: target an ethereal mount in your pack to switch it between solid and translucent (hue -1) | Ethereal mount owners; a reward store row | 1 .cs, 82 lines, 2 Ser; the tool is Blessed (a tool, not a bless deed) | credit xG00BERx | **Idea only.** Not a deco tool, despite the name. A small reward if Chase wants see-through ethereals; check first that TazUO draws hue -1 as translucent. |
| `soundpicker` (Ravenwolfe, after Miracle99) | `[soundpicker`: a gump that steps through sound IDs, plays each and shows its number | Staff picking sounds for NPCs and items | 1 .cs, 145 lines, 0 Ser | credit Ravenwolfe and Miracle99 | **Idea only.** A `[SoundPick` beside `[AnimLocate` if staff ask. Golems cannot hear a sound, and vseUOAware already searches and exports them by name. |
| `spellbar` (zerodowned, after Djeryv) | Server-side spell hotbar gump for magery, necro, chivalry, bushido, ninjitsu, spellweaving and mysticism, with a position picker | Casters | 3 .cs, 6.9k lines, 1 Ser; XmlSpawner attachments; edits to stock ninjitsu and bushido files | credit zerodowned and Ravenwolfe | **Skip.** TazUO's own spell bar does this in the client, with no server gumps or traffic. |
| `tass23-bestiary` (tass23) | An offline generator of HTML pages per creature (stats, resists, a terrain picture), driven by an old Ultima.dll; its author calls it broken | The shard wiki | 5 .cs, 1,563 lines, 0 Ser, plus `Ultima-Bestiary.dll` and `bgen - bestiary.bat` | credit tass23 | **Idea only.** Creature pages for our wiki are better made by a test-host script that reads our own types (BaseCreature and its subclasses, which this tool cannot list). **Flag:** the `.dll` and `.bat` are extracted in the folder although `SOURCE.txt` says they were left in the archive. Never run them. |
| `ticket-teleporters` (jingz2k2) | A teleporter that takes a ticket deed from the backpack and moves the player; the ticket is a deed item | Travel, League dives, festival grounds | 2 .cs, 109 lines, 2 Ser | credit jingz2k2 | **Idea only.** A "pass" teleporter of ours (one ticket type per destination, refuse without it) when a job needs paid or earned passage, for example a dive entry pass. |
| `expanded-names` (Sirenix) | A names.xml of 43 lists; 17 are not in pinned: paladin and paladin title, meer, juka, drow male, drow lord, gladiator male, female and title, Greek, druid, elf male and female, gargoyle male and female, gargoyle quester, graveyard | NPC naming: New Haven townsfolk, League NPCs, juka and meer, gargoyle vendors | Data only: convert the chosen lists into our names data (pinned reads `Data/names.json`), then use `NameList.RandomName` where a type names itself | credit Sirenix | **Port (data).** Take elf, gargoyle, druid, paladin (with titles), juka, meer and gladiator. Leave out the Greek, graveyard and drow lists unless a use comes up. Read the names by eye before shipping: the paladin list is invented syllables. |
| `color-wars` (Omni) | Staff team battle for 2 or 4 colours: entry gates, walls up and down, a blessed event kit, winning stones that pay 10 tokens to each winner's bank | Staff events (P810), PvP | 21 .cs, 3.4k lines, 23 Ser; edits PlayerMobile (team flags and colours) | credit Omni | **Idea only.** If Chase wants staff-run PvP, rebuild it as an opt-in team event on the Events tab with Festival Tokens, kit lent and taken back, and no PlayerMobile edit. The shard has leaned PvM so far (the P792 and P796 skips), so this is Chase's call. |
| `battle-chess` (Arya; kept up by dragon slayer2) | Two players move living chess pieces; a capture is a fight between the two pieces; a GM places the board; the winner gets a score paper | Minigames: the Haven inn beside the P811 casino; the League lounge | 24 .cs, 5.9k lines, 3 Ser; self-contained (own region, gumps and timers); no gold and no core edits. Pinned's `Chessboard` is the plain table board | credit Arya and dragon slayer2 | **Port (later, medium).** A no-stakes showpiece. Rebuild the persistence and gumps for ModernUO; keep the rules engine. No betting. |

Totals: **port 2, idea only 6, skip 3.** Nothing here grants skill or stat points, power scrolls, bless deeds or
property artifacts. Color Wars' event kit is blessed gear handed out for the event only (in the rebuild it is lent
and taken back). The Retouching Tool is itself blessed; neither is a bless deed.

## Port first (for the overseer to put to Chase)

1. **The extra name lists (data only).** *Why:* the cheapest win in the batch. NPCs of the same kind stop sharing a
   name, which helps New Haven's townsfolk and the League NPCs, and nothing in it is code.
2. **`[VBuild statify`** (from the Addon Converter idea). *Why:* the one deco-tool gap left after P812. Staff can
   freeze a placed addon into plain statics, so a dressed corner stops being a live addon. Small; take it with the
   next StaffBuildTools job.
3. **Battle Chess in the Haven inn.** *Why:* a free-to-play showpiece next to the casino, with no gold or reward
   risk. Medium: about 6k lines to bring to ModernUO, three saved types.
4. **A pass teleporter** (from Ticket Teleporters). *Why:* tiny, and the natural gate for a dive entry or a festival
   ground. Only when such a job is queued.
5. **Color Wars as an opt-in team event**, only if Chase wants staff-run PvP. *Why:* the Events tab has two
   solo-race events (P810); this would be its first team event.

## Not done

- No client check that TazUO draws a hue -1 ethereal as translucent (it matters only if the Retouching Tool is
  wanted).
- The bestiary `.dll` and `.bat` were not opened or run; the overseer may want the scout to move them back into
  `_zips\`.

P854 DONE
