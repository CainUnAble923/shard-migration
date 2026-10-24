# P516: guild hall design compared with main

October 24, 2026. Notes only. Compared the P151 survey, P265 decor design, and P281 placements with local main: code `6f540be8b84f63f76b8852fe638039b363b66a6b`, notes `51acde636bed2fcb5aceaf9dd450f3157934e4fa`. Both work-copy HEADs matched their local main refs before this work. No remote refresh was attempted.

Main implements 18 hall placements and leaves Maritime waiting. The counted list is the per-guild table below, from `design/guild-halls/halls.json` and `server/customizations/ClusterFGuildHallPlacementData.cs:40`. Of those entries, 13 reuse empty stock buildings, three share stock buildings with their vendors, and two create Guild House multis. P151's five proposed new buildings became two after Chase's choices and P281's site checks.

"Placed" here means P281 recorded placement and screenshots on a private proof shard. P281 then cleared the halls and removed that shard. The code is on main, but that is no evidence that the halls stand on the shared Test Shard or live today. Current placement is **unverified for every guild**. Place, clear, and rune creation still refuse when `testCenter.enable` is false (`ClusterFGuildHallPlacement.cs:56`, `:103`, `:255`, `:353`). There is no automatic real-hall placement on world load.

## Per guild

Sizes below are inclusive X by Y dimensions calculated from each design `rect`, not measured usable floor space. The Lycaeum is a complex, and shared buildings include space occupied by stock shops. For the new halls, the stock Guild House body is 14x14 plus steps; its surrounding design rectangle is a separate measurement. Pinned `Projects/UOContent/Multis/Houses/Houses.cs:43` defines that body and its four doors.

Every implemented row has its guildmaster, a named stock-art guild sign, and a travel-stop coordinate. "No pack" means no P265 decor group is assigned; existing stock furniture remains. It does not mean an empty building or an unfulfilled promise to supply new furniture. **No row assigns a P265 tower or balustrade.** The door column names the entrance used by its travel stop. Stock doors are not installed or repaired by P281; only the two new buildings receive its door objects.

Remaining-work sizes are estimates, not measured hours: S is a localized content or data change with checks; M needs layout, seeder, or player-routing work; L needs structural or movement work and client proof. Shared gaps are listed after the table and apply to every hall where relevant.

| Guild / key | Hall placed in P281; current code | Design rectangle and size | P265 decor assigned | Doors and towers | Specific gap and estimated size |
|---|---|---|---|---|---|
| The League / `league` | Yes, reuse Castle British's keep, Britain, Trammel. P151 pick retained. | 1320,1586 to 1366,1665; 47x80 across rooms. | No pack. | Stock east door, travel Z50. No new tower. | HQ creates another Elara Voss with New Haven dialogue. Choose an HQ officer or a clerk arrangement before changing the story. S after that choice. |
| Warriors' Brotherhood / `warriors` | Yes, reuse Brothers in Arms, Jhelom, Trammel. P151 pick retained. | 1352,3696 to 1376,3720; 25x25. | No pack. | Stock east doors. No new tower. | No additional guild-specific omission from P151/P281 found; shared readiness work remains. |
| Arcane Society / `arcane` | Yes, reuse the Lycaeum, Moonglow, Trammel. P151 pick retained. | 4278,915 to 4336,1017; 59x103 enclosing the complex. | No pack. | Stock south front. No new tower. | No working guild travel link to this distant hall. Shared travel work is M. No new shop or trial room layout was promised by P281. |
| Healers' Covenant / `healers` | Yes, reuse Empath Abbey's church, Trammel. P151 pick retained. | 623,816 to 647,856; 25x41. | No pack. | Stock south doors. No new tower. | No additional guild-specific omission found; shared readiness work remains. |
| Rangers' League / `rangers` | Yes, share the stock Rangers' Guild, Skara Brae, Trammel. Chase selected sharing instead of P151's free Counselor's Guild. | 552,2136 to 576,2160; 25x25. | No pack. | Stock east doors. No new tower. | Our OutridersGuildmaster is additional to the stock RangerGuildmaster by design. Preserve stock vendor access during any later dressing. S for a layout-only addition. |
| Miners' Compact / `mining` | Yes, reuse Minoc Town Hall, Trammel. P151 pick retained. | 2416,520 to 2440,536; 25x17. | No pack. | Stock south doors. No new tower. | No additional guild-specific omission found; shared readiness work remains. |
| Society of Smiths / `smithing` | Yes, new Guild House, Serpent's Hold, Trammel, centered at 3032,3444,15. P281 used P151's southeast-court fallback. | 3025,3437 to 3045,3457; 21x21 survey/check area around a 14x14 body. | `smiths/forge`, five items: lit pit, cold pit, forge, anvil, animated smith prop. Anchor 3034,3446,22. | Four real dark wood doors, front pair linked. No new tower. | The first-choice court beside the stock forge contains training targets and dummies. Current site is a documented fallback, not missing construction. Keep it unless Chase requests a new site. Door rerun defects below need M work. |
| Tinkers' Union / `tinkers` | Yes, reuse The Musician's Hall, Vesper, Trammel. P151 pick retained. | 2880,736 to 2904,752; 25x17. | No pack. | Stock east door. No new tower. | No additional guild-specific omission found; shared readiness work remains. |
| Thieves' Den / `thieves` | Yes, reuse Buccaneer's Bath, Buccaneer's Den, Felucca. P151's proposed facet was retained by the chosen plan. | 2655,2072 to 2681,2096; 27x25. | No pack. | Stock south doors, travel Z5. No new tower. | No additional guild-specific omission found. Felucca is an intentional site choice. |
| Twin Paths Dojo / `dojo` | Yes, share Iroha Armorer and Musha-Shugyo Dojo, Zento, Tokuno. Chase chose sharing instead of the proposed north-field build. | 735,1296 to 789,1316; 55x21 including the stock shops. | No pack. | Stock north front. No new tower. | No separate new dojo is missing. Any later layout must retain the stock armorers' routes. S for a layout-only addition. |
| Keepers of the Last Door / `keepers` | Yes, reuse the west-side empty hall, Umbra, Malas. P151 pick retained. | 1983,1351 to 1999,1365; 17x15. | No pack. | Stock southeast steps, stop Z-89 to NPC Z-80. No new tower. | Small overall footprint and stepped entrance; usable interior capacity was not measured. Verify that route in a client before adding structure. S check; M if a redesign is needed. |
| Foresters' Union / `foresters` | Yes, reuse Yew Mill, Trammel. P151 pick retained. | 544,808 to 567,831; 24x24. | No pack. | Stock south doors. No new tower. | No additional guild-specific omission found; shared readiness work remains. |
| Tailors' Circle / `tailoring` | Yes, reuse Counselor's Guild, Nujel'm, Trammel. P151 pick retained. | 3760,1184 to 3783,1207; 24x24. | No pack. | Stock south doors. No new tower. | No additional guild-specific omission found; shared readiness work remains. |
| Maritime Brotherhood / `maritime` | **No.** Only a `waiting` entry; no building, NPC post, sign, decor anchor, or travel stop in the placement table. | No adopted rectangle. P151's unused Ocllo proposal was 3600,2496 to 3616,2512, 17x17, Felucca. | None. | No implemented hall doors or assigned tower. | Confirm a suitable Sea Market dock site, or choose another port; then design and implement a hall. M for reusing a verified building; L if a new dock or structure is needed. P268 did not finish the map check. |
| Merchants' Exchange / `merchants` | Yes, new Guild House, Magincia, Trammel, centered at 3709,2176,20. P281 shifted the center away from P151's obstructed spot. | 3702,2169 to 3716,2184; 15x16 check area around a 14x14 body. | No pack. | Four real dark wood doors, front pair linked. No new tower. | Smaller than P151's 22x22 candidate plot, with the standard Guild House body. No additional capacity requirement was measured. Door rerun defects below need M work. |
| Bards' Consortium / `bards` | Yes, reuse The King's Men Theater, Britain, Trammel. P151 pick retained. | 1440,1576 to 1460,1600; 21x25. | No pack. | Stock south doors, travel Z20. No new tower. | No additional guild-specific omission found; shared readiness work remains. |
| Artificers' Order / `artificers` | Yes, reuse the free hall north of Royal City bank, Ter Mur. Chase chose P151's larger fallback instead of building on the plaza. | 809,3344 to 841,3373; 33x30, larger than the proposed 14x18 plaza plot. | `artificers/gate`, eight items: arc gate, field, crystals, pillars, orbs. Anchor 820,3362,-20. | Stock south front. No new tower. | The old outdoor guildmaster at 797,3431,-10 is still seeded and listed. Decide its role with the hall's adoption. S data change, M with seeder reconciliation. The arc gate is decor, not travel. |
| Order of the Alembic / `alembic` | Yes, share Tricks of the Trade and The Reagent Shoppe, Papua, Trammel. Chase chose sharing over the proposed swamp-edge build. | 5723,3182 to 5762,3209; 40x28 enclosing the shared shop. | Only `alembic/scrying`, two items, cloth and lit ball. Anchor 5746,3192,15; actual item tile 5748,3197. | Stock south door and stilt stairs; stop Z-1 to shop Z15. No new tower. | Vat, both tank rows, and flask bench remain unassigned. P281 says they do not fit without moving stock furniture. M for a carefully fitted layout; L if a separate lab or extension is chosen. |
| The Custodians / `custodians` | Yes, reuse the empty brick hall by First Bank of Britain, Trammel. P151 pick retained; no new hall was required. | 1447,1701 to 1474,1716; **28x16** by the current rectangle. P151's prose says about 26x15. | No pack. | Stock east porch, stop Z0 to NPC Z5. No new tower. | No dedicated new decor was promised. Treat 28x16 as the recorded bounding rectangle, not a corrected measurement of interior floor. Shared readiness work remains. |

## Decor still on the shelf

Counted from `design/guild-hall-decor/templates.json` and checked against `server/customizations/GuildHallDecor/GuildHallDecorTemplates.cs:24`:

| Set/group | Template rows | Assigned to a real hall? |
|---|---:|---|
| `alembic/vat` | 9 | No |
| `alembic/tanks-north` | 12 | No |
| `alembic/tanks-west` | 12 | No |
| `alembic/bench` | 16 | No |
| `alembic/scrying` | 2 | Papua only |
| `smiths/forge` | 5 | Serpent's Hold only |
| `artificers/gate` | 8 | Royal City only |
| `structure/tower-large` | 15 | No |
| `structure/tower-medium` | 7 | No |
| `structure/tower-small` | 5 | No |
| `structure/tower-white-brick` | 11 | No |
| `structure/tower-white-column` | 21 | No |
| `structure/balustrade` | 10 | No |

The halls assign 15 decor items total: Smiths five, Artificers eight, Alembic two. Alembic's omitted groups account for 49 template rows. The complete Alembic template spans offsets X -6 through 5 and Y -6 through 8, a 12x15 bounding box before clearance. The vat alone has a 5x5 row bounding box even though its description calls it "3 tiles across." These are occupied item-coordinate bounds; image overhang and usable floor are separate questions. Applying the full generic template at the scrying anchor is not a validated Papua layout.

The animated blacksmith is a `GuildHallDecor` item, not another working NPC. The arc gate has no teleport behavior. All groups use the same plain immovable `GuildHallDecor : Item` constructor (`GuildHallDecorSeeder.cs:98`, `:240`, `:258`). The functional guild services come from the separately placed guildmasters.

The outstanding NPC choices also remain in source: `LeagueRegistrar.cs:27`, `:41`, and `:199` retain Elara's name and New Haven lines; `ClusterFInstitutionSeeder.cs:98` still seeds the Royal City plaza post, and `ClusterFGuildStarterPath.cs:229` still lists it.

## Towers and doors: P459 remains open in this main

Chase's decision is already recorded in `D:/UO/cc-prompts/queue/cc-P459-fix-guild-hall-decor-seeder-refuse-overlapping.md`, under "Chase decided (10-23 07:40)": each tower must have a real door and a walkable inside, with floors and stairs where needed, a door-to-walkable-tile test, and a rendered tower. P516 does not ask for that decision again or implement it.

Main still uses a fixed wall image at each tower's apparent doorway:

| Tower template | Door piece / art ID | Current row-coordinate bounds | Structure gap |
|---|---|---|---|
| Large brick | `large-2q`, 0x6E59 | 6x6; turret at Z+20 | Fixed door wall; no usable interior-floor or stair rows. |
| Medium brick | `medium-1h`, 0x6E64 | 5x5; turret at Z+28 | Fixed door wall; no interior-floor or stair rows. |
| Small brick | `small-a8`, 0x6E6B | 2x2; top at Z+22 | Fixed door wall; interior space is especially constrained by the current wall arrangement. A walkable redesign must establish usable space. |
| White brick | `wbrick-12`, 0x6E78 | 7x7; dome at Z+24 | Fixed door wall; no interior-floor or stair rows. |
| White column | `wcol-11`, 0x6E84 | 7x7; wall rings at Z and Z+22, dome at Z+44 | Fixed door wall; no intermediate floor or stair rows despite the two-story appearance. |

Evidence: `GuildHallDecorArt.cs:151`, `:162`, `:169`, `:182`, `:194` marks all five door pieces Wall and Impassable, height 20. `GuildHallDecorTemplates.cs:118` lists the tower rows; its tops and domes are Roof art rather than an interior-floor plan. `GuildHallDecorSeeder.cs:98` creates plain items for every row, with no door subtype or opening behavior. The separate balustrade group has a ladder, but no hall or tower attaches it as a route between floors. These row-coordinate bounds do not establish rendered width or traversable interior size.

**Estimated remaining work: L for the shared tower capability**, then M per chosen hall attachment for footprint, door swing, stairs, routes, and client checks. Finishing P459 will not assign towers to guilds by itself. A separate layout choice must identify which guilds receive which tower, where they connect, and how their floors meet. P151 and P281 did not specify those attachments. No existing castle tower is being classified here as missing or blocked; this finding concerns P265's decorative tower templates.

The new Smiths and Merchants halls already use `GuildHallDoor : BaseDoor` (`ClusterFGuildHallPlacement.cs:523`), with four positions at `:43` and front links at `:180`. They do not share the tower's fixed-image problem. Other halls depend on their stock map and generated doors; P281 adds no replacement doors there.

## Shared gaps and order of work

1. **Harden placement before tuning layouts, M plus P459's L tower work.** P419's source findings remain visible: decor reruns recognize only the exact anchor and row number, do not save a template hash, and do not preflight collisions (`GuildHallDecorSeeder.cs:75` through `:98`). P459 covers overlap refusal, stale templates, real-design-file tests, and now walkable towers; its terrain/door preflight section is optional in that prompt. Review optional clearance work before adding dense decor to shared shops.
2. **Fix hall rerun and cleanup behavior, M.** P463's findings remain in `ClusterFGuildHallPlacement.cs`: `FindNpc` at `:69` and `Clear` at `:290` can adopt/delete a preexisting same-type NPC near a post; `place ... dryrun` still assigns existing front-door links at `:180`. P281's earlier review also records open-door duplication and replacement stock-sign handling. Current placement matches doors only at their closed positions (`:151`) and skips stock-sign handling when its guild sign already exists (`:187`). These are review findings from source, not runtime reproductions in P516.
3. **Keep design and implementation together, S to M.** The current files agree, but both C# design tests read generated copies, not the real JSON (`GuildHallDecorVerification.cs:62`, `GuildHallPlacementVerification.cs:54`). P459 covers the decor half. The hall-table half remains a separate gap identified by P463. A green copied-design test does not establish that a future JSON-only edit reached the server. P281's generator also still invokes the checker without forwarding its selected repository (`notes/cc-P281-tools/gen.py:129`); the checker defaults to Iron's work copy. P516 verified the generated files and separately redirected the map checker to the actual audited work copy.
4. **Resolve the concrete content choices, S to L as in the table.** League officer identity, the old Royal City post, Alembic laboratory space, Maritime's site, and which halls receive towers remain. Maritime's `waiting` text says "waits on P268," but P268's assessment is already written: its section 3 leaves Sea Market map presence unverified (`cc-P268-high-seas-ships-assessment.md:317`). It does not supply an approved hall footprint. No naval engine port is proven necessary merely to choose a dockside hall.
5. **Adopt and expose the halls only after approval, M.** Place on the intended test world, walk entrances, stairs, and shared vendor routes, then obtain Chase's placement approval. Before any live adoption, provide the authorized placement path and update `GuildLocations` and player directions while retaining the New Haven chapters as decided. `ClusterFGuildStarterPath.cs:208` still lists chapter posts and the old Royal City outdoor post; it does not list these real halls. The hall command supplies staff `go` and marked runes, not a player travel network (`ClusterFGuildHallPlacement.cs:352`, `:434`). Live rollout is outside P516.

## Evidence and verification limits

Design history read: [P151 survey](cc-P151-guild-halls-survey.md), [P265 decor packs](cc-P265-guild-hall-decor-packs.md), [P281 placement and private-shard proof](cc-P281-guild-halls-placement.md), [P281 review](cc-P281-guild-halls-placement-codex-review.md), [P419 decor review](cc-P419-review-guild-hall-decor-packs.md), [P463 placement review](cc-P463-review-guild-halls-placement.md), and the Sea Market passages in [P268 assessment](cc-P268-high-seas-ships-assessment.md). The source paths cited above are relative to the code repository unless explicitly named otherwise.

Read-only checks performed against the work copies:

- P281's existing `gen.py <code-work-copy> --verify` passed: the placement table and test copy match the real hall design.
- Compared every decor group's generated row ID, piece key, offset, and hue with the real template and art catalog. All matched. Used P265's newline normalization: SHA-256 `1f6657ad5fb46118ffa263015c7335317548381652af5c9678bd7a5b48f2aa77`. An initial scratch comparison included the final newline; rerunning with the generator's documented normalization resolved that probe error without changing files.
- Ran P281's existing offline checker for the full hall list above, with `CODE`, `PLAN`, and `TEMPLATES` redirected in memory to this work copy and every hall key supplied so it would not rewrite its stored output. Every hall returned `ok`, exit 0. Its dependencies read local client data under `D:/UO/tool-trials/client-data-copy` and the read-only pinned tree. Local `ModernUO-pinned` HEAD is `d4531cd94b739613155225c234900de9f47d2c88`.
- Ran `tools/progress.py --dry-run` with `SL_SHARD` and `SL_MIGRATE` pointing to these work copies; exit 0. Its dry run still rewrites `tools/progress.json`, so restored that initially clean file from its original bytes and verified byte equality. No progress artifacts remain changed.

The map checker simplifies movement and stairs, omits the engine's diagonal-corner rules, and does not model the new multis' interiors. Its success establishes no client walk-through or current-world collision result. Current saves, hand-placed items, roaming vendors, recall execution, current package delivery, and restart persistence were not verified. Historical proof remains P281's proof, not a fresh deployment claim.

No code, tests, art, configuration, or world data changed. No new tests were written, and no C# suite or server build was run; lane tests are none. No Haven connection, shard connection, deployment, container operation, or account operation occurred.

P516 DONE
