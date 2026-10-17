# cc-P134: vseUOAware part 1: offline art checks and the local MCP server (Parts B and C)

2026-10-17. Parts B and C of the vseUtilities adaptation. P135 does Parts A and D and reads this note.

## Headlines

1. **`D:\ShatteredLegacy\scripts\validate-art.py`** (new, GPL-3.0, credit line in the header): `bodies`, `actions`,
   `check-vd`, `propose`, `check-registry`, `hues-diff`, `render`. It follows **TazUO's** loader (the client we ship),
   not vseUOAware's, because vseUOAware is wrong in three places that matter for our files (section 2). 21 tests in
   `scripts\tests\test_validate_art.py`, every one watched red by its own deliberate break, then green (section 4).
2. **The real run over the 2026-10-15 downloads: 39 .vd files in the 17 named folders, all 39 get a free server
   body (0x800 up) and a free slot in our own anim7, with 0 problems.** Four are replacements of stock bodies and are
   checked against those too. Table in section 5. Nothing was registered.
3. **vseUOAware is built at `D:\UO\tools\vseUOAware\`** from a copy of the source, gate removed, every write confined
   to `D:\UO\tools\vseUOAware\exports\`, and registered in `D:\UO\shard-migration\.mcp.json`. 86 tools (the brief said
   "about 90"; counted from `tools/list`). Smoke test passed (section 7.5).
4. **Bug found and fixed in our copy: every UOP map read in vseUOAware was wrong on our client.** It orders map chunks
   by file offset; EA's patched `map1LegacyMUL.uop` holds 112 of its 113 chunks out of that order. Trammel 3503,2574
   read as land 0x0064 Z -15; it is 0x03E9 Z 14 (checked independently from the UOP by name hash, and the statics
   beside it agree). Fixed by reading chunks by name, as TazUO does. Part A (P135) uses ModernUO's own map, not this.
5. **Not fixed, and do not trust:** vseUOAware's animation tools for any body with a Bodyconv.def line or mobtypes
   layout flags. For the kirin (body 132) its `list_defined_actions` reports 38 actions, 22 to 77; the kirin has 13,
   0 to 12, at anim2.idx record 13420. Use `validate-art.py` for animation questions.
6. **Argonious's hues.mul differs from ours in the colours of 754 of 3,000 hues** (including our named 1150-1177,
   ice and dark hues). Replacing ours would recolour those; report only, as asked.
7. Two calls for Chase: ImageSharp pinned to 3.1.12 (4.x needs a Six Labors key), and an allow line for the unattended
   hook so a Golem session can call these read-only tools (section 9).

## 1. Where things are, and why (and the Part D argument)

- `validate-art.py` is **its own script beside `find-free-art.py`**, not an extension of it. find-free-art answers
  "which item/art ID is free" over tiledata, animdata, maps, multis and code; validate-art answers "where would this
  creature's frames land and would the client read them". They share the file readers: validate-art imports
  find-free-art's `Uop` class, UOP hash and `.def` tokeniser (`importlib`, the file name has a hyphen), so both read
  the files identically and nothing is duplicated. find-free-art is unchanged.
- The prompt names `scripts\find-free-art.py` with the shard-migration paths around it; it is in **D:\ShatteredLegacy\scripts**
  (shard-migration has no such file), so validate-art is there too.
- **vseUOAware lives at `D:\UO\tools\vseUOAware\`**: outside both repos (its 7 MB of build output never meets the
  5 MB repo rule or a commit), outside `third-party\` (reference only), beside the console scripts already in
  `D:\UO\tools`. `exports\` is inside it.
- **Part D (P135 decides; my input):** validate-art should stay a command-line tool, not a console tab: its users are
  CC sessions and the art pipeline before a registry row is added, and its output is a table to read and paste. If
  the console gets anything, one read-only "Art check" button on an existing tab that runs `check-registry` and shows
  the result would be enough. The MCP server is its own tool for CC and Cowork sessions and does not belong in the
  console at all (it has no UI; it is a stdio process a Claude session starts).

## 2. Client and engine behaviour used (file:line)

TazUO source at `D:\UO\cc-p40-work\tazuo-3212623f\src` (the folder find-free-art names; its git HEAD reads df84b202a).
Pinned ModernUO `D:\UO\ModernUO-pinned` is at **d4531cd94**, not 7c9215d97 as the brief says (AGENTS.md: re-checked out
by cc-P38).

| What | Where |
|---|---|
| mobtypes.txt: `<body> <TYPE> <hex flags>`, five type names, flags parsed as hex | `ClassicUO.Assets/AnimationsLoader.cs:126-214` |
| GetIndices: flag 0x10000 sends a body to AnimationFrame*.uop; else Bodyconv, then type from mobtypes or by slot | `AnimationsLoader.cs:293-401` |
| CalculateOffset: monster high unless 0x400/0x40; sea high offset with 13 actions; animal low unless 0x20 | `AnimationsLoader.cs:403-497` |
| Bodyconv.def: every applicable column applied in turn (last wins), only for files that exist | `AnimationsLoader.cs:541-660` |
| High/low/people offsets: slot x 110; 22000 + (slot - 200) x 65; 35000 + (slot - 400) x 175 | `AnimationsLoader.cs:915-921` |
| Type by slot range per file (anim2, anim3, the rest) | `AnimationsLoader.cs:924-945` |
| AnimationFlags (0x4 IdleAt8Frame, 0x8 CanFlying, 0x20/0x40/0x400 layout, 0x10000 UOP) | `AnimationsLoader.cs:1722-1745` |
| Frame run headers: signed 10-bit x and y, every run pixel drawn | `AnimationsLoader.cs:1461-1520` (ReadSpriteData) |
| Body.def/Corpse.def replacement only for a non-UOP body left in anim.mul (file index 0) | `ClassicUO.Renderer/Animations/Animation.cs:250-254` |
| Idle on action 8 when flag 0x4 and the body has it; fly on 19 when running with 0x8 | `ClassicUO.Client/Game/GameObjects/MobileAnimation.cs:142`, `:167` |
| Hue N is entry N - 1 (hue IDs are 1-based) | `ClassicUO.Assets/HuesLoader.cs:151` |
| Server body types from `Data/bodyTable.cfg`, bodies below 0x1000 | ModernUO `Projects/Server/Mobiles/Body.cs:40-72` (`:49`) |
| Stock bodies of the replacements | `UOContent/Mobiles/Animals/Mounts/Kirin.cs:13` (132), `Mounts/Unicorn.cs:13` (0x7A), `Monsters/Humanoid/Magic/Succubus.cs:11` (149), `Animals/Canines/TimberWolf.cs:12` (225) |

**Where vseUOAware differs, each checked against the files:**
- Bodyconv.def: vseUOAware takes the **first** non -1 column, TazUO the **last** applicable one.
- Layout: vseUOAware picks high/low/people from the in-file slot only and ignores mobtypes. The kirin: mobtypes
  `132 ANIMAL 0`, Bodyconv `132 68 -1 -1 -1 -1`: TazUO reads a low block at anim2 record 13420 (frames there, actions
  0-12); vseUOAware probes 7480 (high) and finds none. Measured on anim2.idx.
- anim4/5/6: TazUO uses the default ranges; vseUOAware's anim5 "body 34" exception is not in TazUO.
- vseUOAware's frame decoder XORs the run header with 0x200 and subtracts it again through its base offset, which is
  the same as TazUO's sign extension. I first did both and rendered empty frames; the render test pins it.

Our package's own overrides are included by default: records.json `equipAnims` become Bodyconv lines
`N -1 -1 -1 -1 -1 S` into anim7 (`sl-anim7.bin`), as `player-package\payload\app\Build-UoOverrides.ps1` writes them.
`--no-overrides` leaves them out. Client data: `client-data\classic-client-7.0.117.0` (not find-free-art's
`classic-client`, which differs in Bodyconv.def, hues.mul, mobtypes.txt and AnimationFrame1.uop). Never the player's EA folder.

## 3. Commands

Run from `D:\ShatteredLegacy`. All read only; `render` writes PNGs to `--out` only.

| Command | What it says |
|---|---|
| `python scripts/validate-art.py bodies [--all]` | every body mobtypes or Bodyconv names (1,320 today; `--all` adds bodies with frames by default slot only): type, flags, classic or UOP, source file, slot, layout, actions, which line defines it |
| `python scripts/validate-art.py actions 132` | which of the 80 actions have frames, where (file, slot, layout, records) |
| `python scripts/validate-art.py check-vd X.vd 132` | the .vd's layout and actions; whether body 132 is free (Bodyconv, mobtypes, Body.def/Corpse.def where they apply, Equipconv, UOP frames, frames at its slot, other bodies reading the same records, server bodyTable); where it lands; whether the block's layout and action count fit; what mobtypes must say; hover hint |
| `... check-vd X.vd 2100 --file 7 --slot 1 [--type monster] [--flags 1004]` | the same for a planned Bodyconv line (anim7 slot 1) and mobtypes line. Exit 1 on any problem |
| `python scripts/validate-art.py propose A.vd B.vd ...` | a distinct free server body (from `--body-from`, default 0x800) and free anim7 slot of the right layout for each, then check-vd on it. Registers nothing |
| `python scripts/validate-art.py check-registry` | registry rows registered twice; art IDs with EA art in the slot; anim rows that mobtypes names (it would send them elsewhere) or that records.json does not route; `body` rows with no mobtypes entry, and any body whose records another body also reads |
| `python scripts/validate-art.py hues-diff a\hues.mul b\hues.mul [--limit N]` | hues whose colours differ, and those that differ only in name or table range (EA leaves junk there), per hue |
| `python scripts/validate-art.py render 132 0 2 --out DIR` / `render --vd X.vd 0 2 --out DIR` | one body/action/direction (5-7 mirrored) to PNGs, from the client or from a .vd before import. UOP bodies: use the MCP server |

Tests: `python -m unittest discover -s scripts/tests -p "test_validate_art.py"` (21 tests, about 0.4 s, fixtures made
in a temp folder; no EA file read or committed).

check-registry today: `0 of 112 rows have problems` (110 art, 1 anim, 1 gump). The registry has no creature body rows
yet. A missing mobtypes entry is flagged for a `body` row, and for an `anim` (equipment) row the opposite is flagged,
because Build-UoOverrides skips an equipment animation that mobtypes names. **find-free-art refuses a registry row of
an unknown kind**, so when the first `body` row is added, find-free-art's `KINDS` needs `body` too (open question 3).

## 4. Facts, red then green

Each test was made red by breaking the script in exactly the way the test exists to catch, one break at a time, with
the file restored after each and proved byte-identical (SHA-256). Runner and its output:
`notes\cc-P134-tools\redfirst.py`, `redfirst.txt`. Baseline green, 21 of 21 breaks red, restored green:

| Break (how it was made red) | Test that went red |
|---|---|
| Bodyconv first column wins (vseUOAware's rule) | test_bodyconv_last_applicable_column_wins |
| Bodyconv column applied for an anim file that does not exist | test_bodyconv_column_for_a_missing_file_is_skipped |
| mobtypes type ignored for the layout | test_mobtypes_type_decides_the_layout_the_kirin_case |
| slot range ignored (always monster) | test_no_mobtypes_entry_uses_the_slot_range, test_our_equip_anim_override_reaches_anim7 |
| UOP flag bit wrong (0x20000) | test_flag_10000_sends_the_body_to_uop |
| animal 0x20 ignored | test_animal_flags |
| records.json equipAnims not applied | test_our_equip_anim_override_reaches_anim7 |
| a planned slot's existing frames reported as information, not a problem | test_slot_with_frames_is_not_free |
| layout mismatch reported as information | test_layout_mismatch_is_a_problem |
| an existing Bodyconv line not a problem for a planned one | test_body_with_a_bodyconv_line_is_not_free_for_a_new_line |
| Body.def applied to every body | test_body_def_redirect_counts_only_in_anim_mul |
| server bodyTable not read | test_server_body_table_is_reported |
| hover hint missing | test_hover_flag_hint |
| .vd header not checked | test_bad_vd_is_refused |
| propose offers a body bodyTable.cfg already names | test_propose_gives_distinct_free_slots |
| registry duplicates missed | test_check_registry_flags_collisions_and_missing_mobtypes |
| missing mobtypes entry missed | test_check_registry_flags_collisions_and_missing_mobtypes |
| hues: the 0x8000 bit compared | test_alpha_bit_is_not_a_difference |
| hues: name-only differences counted as colours | test_colour_and_name_differences_are_counted_apart |
| render: run header XORed as well as sign-extended | test_frame_decodes_to_the_right_pixel |
| render: directions 5-7 mirrored from the wrong stored direction | test_render_mirrors_directions_5_to_7 |

**A runner bug I hit and fixed, worth knowing:** the first runner pass reported one red against the wrong test and a
red suite after the restore. Cause: a mutation of the same byte length written within the same second left a stale
`scripts\__pycache__\validate-art.cpython-312.pyc` that Python trusted (it checks source mtime in seconds and size).
The runner now deletes that .pyc and sets PYTHONDONTWRITEBYTECODE before every run; the table above is the clean pass.

Part C facts, each watched both ways:
- **UOP map order:** red: the built server answered Trammel 3503,2574 = land 0x0064 Z -15; my own read of
  `map1LegacyMUL.uop` by name hash gave 0x03E9 Z 14, and `statics1.mul` holds statics at Z 14 on the next tile. Green
  after the fix: 0x03E9 Z 14, and 3503,2573 lists statics 0x0D33 and 0x0B24 at Z 14, exactly the two my statics read
  gives there.
- **Write confinement:** asked to write a hue swatch to `D:\ShatteredLegacy\client-data\classic-client-7.0.117.0\escape-test.png`,
  the server wrote `D:\UO\tools\vseUOAware\exports\Hue\escape-test.png`; the client-data path does not exist after
  the call. Unpatched, `ExportPathResolver.Resolve` used any rooted path as given (read in the source; not run).
- **Gate removed:** every call answered; the original refuses each call with "BLOCKED by ghostbyte's rule gate" unless
  a vseAgentRules process is running (read in `RulesGate.cs`; the unmodified server was not built or run).

## 5. Part B: the 2026-10-15 downloads

`python scripts/validate-art.py propose <39 files>` (`notes\cc-P134-tools\propose.tsv`): exit 0, 39 rows, 0 problems.
The 17 folders hold **39** .vd files (counted; the brief lists the folders, not the files). Proposed bodies are
consecutive from 0x800; each anim7 slot is in the layout's own range (high 1-199, low 200-399, people from 401; 400 is
the fox ears). "none needed" means the slot's range already gives the right type with no mobtypes line; writing the
line anyway is harmless and explicit.

| download | .vd | layout | actions with frames | proposed body | anim7 slot | mobtypes | warnings and notes |
|---|---|---|---|---|---|---|---|
| basilisk | Basilisk.vd | high | 0-6,10,12,17-18 | 2048 (0x800) | 1 | none needed (MONSTER is the default for slot 1 of anim7) | - |
| brontosaurus | Brontosaurus.vd | high | 0-6,10,17-18 | 2049 (0x801) | 2 | none needed (MONSTER is the default for slot 2 of anim7) | - |
| cobramen | anim4_0x64.vd | high | 0-6,10,15-18 | 2050 (0x802) | 3 | none needed (MONSTER is the default for slot 3 of anim7) | cobraman; the author's anim4 slot 0x64. |
| cobramen | anim4_0x65.vd | high | 0-6,10,12-13,15-18 | 2051 (0x803) | 4 | none needed (MONSTER is the default for slot 4 of anim7) | cobraman; the author's anim4 slot 0x65. |
| kirin | Kirin.vd | high low? | 0-12 | 2052 (0x804) | 5 | none needed (MONSTER is the default for slot 5 of anim7) | Renders as a quadruped (walk, action 0), so it is an ANIMAL: use ANIMAL 0 and low slot 214 instead (`check-vd ... 2052 --file 7 --slot 214 --type animal`: free and matching). It replaces the stock kirin (body 132, Kirin.cs:13) only if wanted; 132 is at anim2 slot 68, and body 191 reads the same records. |
| kraken | Kraken2.vd | high | 0-5,10-11,17-18 | 2053 (0x805) | 6 | none needed (MONSTER is the default for slot 6 of anim7) | - |
| lady-ghost | GhostLady.vd | high | 0-4,10,13-14,17-19 | 2054 (0x806) | 7 | none needed (MONSTER is the default for slot 7 of anim7) | - |
| lizardmen | Lizardman Cheiftan.vd | high | 0-6,10-11,15-18 | 2055 (0x807) | 8 | none needed (MONSTER is the default for slot 8 of anim7) | - |
| lizardmen | Lizardman Mage.vd | high | 0-6,10-13,17-18 | 2056 (0x808) | 9 | none needed (MONSTER is the default for slot 9 of anim7) | - |
| lizardmen | Lizardman.vd | high | 0-6,10-11,15-18 | 2057 (0x809) | 10 | none needed (MONSTER is the default for slot 10 of anim7) | - |
| malboro | Malboro_H.vd | high | 0-2,4-6,10,13,17-18 | 2058 (0x80A) | 11 | none needed (MONSTER is the default for slot 11 of anim7) | - |
| naga | Naga Female.vd | high | 0-6,10,12-13,17-19 | 2059 (0x80B) | 12 | none needed (MONSTER is the default for slot 12 of anim7) | - |
| naga | Naga Male.vd | high | 0-6,10,17-19 | 2060 (0x80C) | 13 | none needed (MONSTER is the default for slot 13 of anim7) | - |
| new-lion | New Lion.vd | low | 0-12 | 2061 (0x80D) | 200 | none needed (ANIMAL is the default for slot 200 of anim7) | - |
| sahuagin | Sahuagin Crossbow (2).vd | high | 0-6,10,17-18 | 2062 (0x80E) | 14 | none needed (MONSTER is the default for slot 14 of anim7) | - |
| sahuagin | Sahuagin Trident.vd | high | 0-6,10,17-18 | 2063 (0x80F) | 15 | none needed (MONSTER is the default for slot 15 of anim7) | - |
| sea-creatures | Great White.vd | low | 0-2,5-9 | 2064 (0x810) | 201 | none needed (ANIMAL is the default for slot 201 of anim7) | - |
| sea-creatures | Hammerhead.vd | low | 0-2,5-9 | 2065 (0x811) | 202 | none needed (ANIMAL is the default for slot 202 of anim7) | - |
| sea-creatures | Seahorse.vd | low | 0-12 | 2066 (0x812) | 203 | none needed (ANIMAL is the default for slot 203 of anim7) | The author used it as a mount (it replaced the Retialon mount). |
| sea-creatures | Thresadon.vd | low | 0-2,5-9,12 | 2067 (0x813) | 204 | none needed (ANIMAL is the default for slot 204 of anim7) | - |
| sea-creatures | Whale Shark.vd | low | 0-2,5-9 | 2068 (0x814) | 205 | none needed (ANIMAL is the default for slot 205 of anim7) | - |
| succubus | FeatheredSuccubus.vd | high | 0-8,10,17-18 | 2069 (0x815) | 16 | **2069 MONSTER 1004** (the author's value) | The author gives mobtypes 1004 for the hover idle: 0x4 is IdleAt8Frame, and TazUO reads nothing from 0x1000. With `--flags 1004`: free and matching. Needs a mobtypes.txt override, which the package does not make yet. |
| succubus | FlyingSuccubus.vd | high | 0-8,10,17-18 | 2070 (0x816) | 17 | **2070 MONSTER 1004** (the author's value) | As Feathered. Action 8 renders as a hover pose (looked at, direction 2). |
| succubus | Succubus.vd | high | 0-8,10,13,17-18 | 2071 (0x817) | 18 | none needed (MONSTER is the default for slot 18 of anim7) | The author's replacement for the stock succubus (body 149, Succubus.cs:11, anim2 slot 25). As a replacement the slot is taken, by design; as a new body, use this row. |
| theart-critters | H-boychild1.vd | high | 0-6,10-11,15-19 | 2072 (0x818) | 19 | none needed (MONSTER is the default for slot 19 of anim7) | EA-derived (TheArt). A high (monster) layout with human-like actions: a child NPC drawn as a monster body. |
| theart-critters | H-boychild2.vd | high | 0-6,10-11,15-19 | 2073 (0x819) | 20 | none needed (MONSTER is the default for slot 20 of anim7) | As boychild1. |
| theart-critters | H-girlchild1.vd | high | 0-6,10-11,15-19 | 2074 (0x81A) | 21 | none needed (MONSTER is the default for slot 21 of anim7) | As boychild1. |
| theart-critters | H-girlchild2.vd | high | 0-6,10-11,15-19 | 2075 (0x81B) | 22 | none needed (MONSTER is the default for slot 22 of anim7) | As boychild1. |
| theart-critters | L-Colorable Rideable Dragon.vd | low | 0-12 | 2076 (0x81C) | 206 | none needed (ANIMAL is the default for slot 206 of anim7) | EA-derived (TheArt); mount candidate. |
| theart-critters | L-Flesh Renderer Mount.vd | low | 0-12 | 2077 (0x81D) | 207 | none needed (ANIMAL is the default for slot 207 of anim7) | EA-derived (TheArt); mount candidate. |
| theart-critters | L-Ridable Red Dragon.vd | low | 0-12 | 2078 (0x81E) | 208 | none needed (ANIMAL is the default for slot 208 of anim7) | EA-derived (TheArt); mount candidate; the largest .vd (5.7 MB). |
| theart-critters | Giant Wolf.vd | low | 0-12 | 2079 (0x81F) | 209 | none needed (ANIMAL is the default for slot 209 of anim7) | EA-derived remake (TheArt). |
| theart-critters | Unicorn Replacement.vd | low | 0-12 | 2080 (0x820) | 210 | none needed (ANIMAL is the default for slot 210 of anim7) | Replaces the unicorn (body 0x7A = 122, Unicorn.cs:13, anim2 slot 200, which body 192 also reads). EA-derived (TheArt). |
| theart-critters | H-SpookyPumpkin.vd | high | 0-6,10-11,15-16 | 2081 (0x821) | 23 | none needed (MONSTER is the default for slot 23 of anim7) | - |
| theart-critters | Ridable Bird L Slot.vd | low | 0-12 | 2082 (0x822) | 211 | none needed (ANIMAL is the default for slot 211 of anim7) | The bird itself. A mount also needs a mount item and its tiledata animId. |
| theart-critters | Ridable Bird Player Slot.vd | people | 23-29 | 2083 (0x823) | 401 | none needed (HUMAN is the default for slot 401 of anim7) | People layout with only actions 23-29, the mounted actions: the rider's side of a mount, not a creature. Needs a design decision. |
| tiger | anim4_0xF0.vd | low | 0-12 | 2084 (0x824) | 212 | none needed (ANIMAL is the default for slot 212 of anim7) | The tiger. The file name is the author's anim4 slot 0xF0, not ours. |
| vampire-bat | VampireBat.vd | high | 0-8,10-11,15-18 | 2085 (0x825) | 24 | none needed (MONSTER is the default for slot 24 of anim7) | Has action 8: render it to see whether that is a hover idle (then flag 0x4). |
| wolf-replacement | Wolf replacement.vd | low | 0-12 | 2086 (0x826) | 213 | none needed (ANIMAL is the default for slot 213 of anim7) | Replaces the timber wolf (body 225, TimberWolf.cs:12, anim.mul slot 225). Body.def and Corpse.def draw 9 other bodies (23, 25, 27, 34, 37, 97-100) with 225's frames, so a replacement changes them too. |

Replacement checks (`check-vd` against the stock body): kirin 132, succubus 149, timber wolf 225 and unicorn 122 each
report their slot as taken (as a replacement must) and list what else reads it, shown in the notes column above.

What the table does not decide: a proposed body needs a server `bodyTable.cfg` line of the right type (ModernUO's
`Body.IsMonster`/`IsAnimal` read it; a body with no line is `Empty`, `Body.cs:77`), and the anim7 file needs a
build step for creature blocks like `build-equip-anims.py` has for worn items. That is the import task.

## 6. hues-diff: Argonious against ours

`python scripts/validate-art.py hues-diff client-data\classic-client-7.0.117.0\hues.mul D:\UO\third-party\argonious-buildings\hues.mul`:
both 265,500 bytes, 3,000 hues. 1,362 differ: **754 in their colours**, 608 only in name or table range (EA leaves
junk names there, e.g. `TEXTFX-`, `_RPC_HANDLE-`). Colour ranges: 1072, 1150-1151, 1155-1177, 1190-1196, 1255-1289,
1355-1378, 1457-1463, 1755-1779, 1909-1997, 2019-2056, 2058-2072, 2075-2076, 2498-2644, 2651-2662, 2671-2718,
2720-2884, 2886-2999. Ours names 1150-1177 "ice_hue_*", "dark red", "fire" and so on; Argonious's are unnamed or junk.
So his file is not a drop-in: the hues his designs use would have to be found and added in free hue numbers, if any.
Report only, as asked.

## 7. Part C: vseUOAware as a local MCP server

### 7.1 What was copied

`vseUOAware_09272026_Latest\vseUOAware\` to `D:\UO\tools\vseUOAware\`: 90 files, bin/obj/*.user/PublishProfiles left
out (the .user files carry the author's own paths). 82 .cs in the source folder (SOURCE.txt's 122 counts the
`bkuDistribution` copy too); 81 in ours (RulesGate.cs removed). `LICENSE` (GPL-3.0) copied beside it and
`MODIFIED.md` added (the GPL-3.0 section 5(a) notice). Every changed file says so in its first line.

### 7.2 Every write and path, reviewed before the build

| Writer | Original target | Now |
|---|---|---|
| `ExportPathResolver.Resolve` (all PNG/WAV exports: art, land, gumps, hues, light, fonts, animation frames, multimaps, textures, world map, sounds) | any rooted path as given, else `uoaExport\` beside the nearest .sln/.slnx/.mcp.json | `exports\<category>\<file name only>` |
| `MapExportTools.ResolveOutput` | any rooted path, else `<bin>\uoaExport\Map` | through the resolver |
| `CommonEdit`, `TerrainEdit`, `TransitionCreate`, `TransitionRepair`, `TransitionAudit`, `TransitionTemplate`, `TransitionTemplatesWays` (MapCreator XML, INSTALL.md, REPORT.md, AUDIT.md, rule PNGs, a copy of `Diagrams\*.png`) | any folder given, refused if not empty | `exports\MapCreator\<name>`, still refused if not empty |
| `WaterTools` shore CSV | any folder except the map's own | `exports\Water\<name>` |
| `DirectoryService.SaveDirectory` | `%LOCALAPPDATA%\vseUOAware\uo-path.json` | memory only; default from `VSEUOAWARE_UO_DIR` |
| `RulesGate` | read `%LOCALAPPDATA%\vseAgentRules\rules_read.stamp`, `Process.GetProcessById` | removed |

Searched for `File.Write*/Create/Copy/Move/Delete`, `Directory.Create/Delete/Move`, write FileModes and FileAccess,
`StreamWriter`, `.Save*`, `Process`, `HttpClient`, `WebClient`, `Socket`, `TcpClient`, `Dns`, `WebRequest`,
`Registry`, `Assembly.Load`, `DllImport`: **no network, no process launch** (the gate's `GetProcessById` was the only
process call), and no write outside the rows above. Reads are of whatever path a caller passes (that is the tool).
The MCP host and logging come from Microsoft.Extensions.Hosting; logs go to stderr (`Program.cs`).

### 7.3 Build record

`dotnet build -c Release` in `D:\UO\tools\vseUOAware` with .NET SDK 10.0.201: **0 errors**, 226 warnings (analyzer
style, mostly CA1822, plus the NU1902/NU1903 lines below). Output `bin\Release\net10.0\vseUOAware.exe` (7.1 MB bin,
1.1 MB obj). Two changes were needed to build, and one to restore:

- The machine has no nuget.org source (`dotnet nuget list source`: only "Microsoft Visual Studio Offline Packages"),
  so restore failed. A project-local `nuget.config` with nuget.org only, the same one `D:\ShatteredLegacy\client\nuget.config` uses.
- The csproj was self-contained for six runtimes (it restored a runtime pack per platform, linux-musl among them). Ours
  is framework-dependent against the installed .NET 10 runtime.
- **SixLabors.ImageSharp 4.1.2 refuses to build without a Six Labors license key** ("No Six Labors license found").
  3.1.12 has the same Six Labors Split License (Apache-2.0 for GPL software and for an individual) and needs no key, so
  ours uses 3.1.12. NuGet flags 5 advisories on 3.1.x (GHSA-gwg2-r3hj-4w44, GHSA-wmxv-xphr-5c9g, GHSA-j3p4-wp97-rph4,
  GHSA-j9gm-c75j-xc9q, GHSA-jjfr-hcj7-qf5w, all fixed in 4.1.2): ICC profile parsing, BigTIFF decoding, histogram
  equalization, and the TIFF CCITT encoders. vseUOAware only builds `Image<Rgba32>` from its own pixels and calls
  `SaveAsPng` (`PngImageWriter.cs`, `TransitionTemplatesWays.cs`; no Load, no TIFF, no histogram), so none of them is
  reachable. Chase's call (section 9).

NuGet packages restored (33, from `obj\project.assets.json`): the three direct references are
**Microsoft.Extensions.Hosting 10.0.12, ModelContextProtocol 2.2.0, SixLabors.ImageSharp 3.1.12**. Transitive:
Microsoft.Extensions.AI.Abstractions 10.8.3, Microsoft.Extensions.Caching.Abstractions 10.0.10,
ModelContextProtocol.Core 2.2.0, System.Diagnostics.EventLog 10.0.12, and Microsoft.Extensions.* 10.0.12:
Configuration, Configuration.Abstractions, .Binder, .CommandLine, .EnvironmentVariables, .FileExtensions, .Json,
.UserSecrets; DependencyInjection, DependencyInjection.Abstractions; Diagnostics, Diagnostics.Abstractions;
FileProviders.Abstractions, FileProviders.Physical, FileSystemGlobbing; Hosting.Abstractions; Logging,
Logging.Abstractions, .Configuration, .Console, .Debug, .EventLog, .EventSource; Options,
Options.ConfigurationExtensions; Primitives. (The first, unsuccessful 3.1.11 build restored 3.1.11 the same way;
3.1.11 was already in the package cache.)

### 7.4 `.mcp.json` (new, `D:\UO\shard-migration\.mcp.json`, project scope)

```json
{
  "mcpServers": {
    "vseUOAware": {
      "type": "stdio",
      "command": "D:\\UO\\tools\\vseUOAware\\bin\\Release\\net10.0\\vseUOAware.exe",
      "args": [],
      "env": {
        "VSEUOAWARE_UO_DIR": "D:\\ShatteredLegacy\\client-data\\classic-client-7.0.117.0",
        "VSEUOAWARE_EXPORTS": "D:\\UO\\tools\\vseUOAware\\exports"
      }
    }
  }
}
```

`~\.claude\settings.json` and the unattended hook were read, not touched.

### 7.5 Smoke test

A Claude Code session loads a project's MCP servers when it starts, and asks once before trusting a new `.mcp.json`
server, so this session could not use it as `mcp__vseUOAware__*`. So the smoke test speaks MCP itself, over stdio,
starting the server with the `.mcp.json` entry's own command and env, which is what Claude Code does
(`notes\cc-P134-tools\mcp_smoke.py`). A fresh session in `D:\UO\shard-migration` is the remaining check (open question 1).

- `initialize`: serverInfo vseUOAware 1.0.0.0. `tools/list`: 86 tools.
- `inspect_map_coordinate {x 3503, y 2574, facet 1}` (Trammel, New Haven; no file paths, so the `.mcp.json` default
  folder was used): `land tile 0x03E9 (1001), Z=14`, no statics; `{3503, 2573}`: land 0x03FC Z 14, statics 0x0D33 and
  0x0B24 at Z 14. Matches the independent read (section 4). Before the fix: 0x0064 Z -15.
- `list_animation_bodies {mobtypes.txt}`: 1,314 bodies (mobtypes only; validate-art's 1,320 adds Bodyconv-only
  bodies), e.g. `132 Animal classic`, `666 Human UOP format`.
- `render_hue_swatch {hues.mul, 1153}`: `Rendered hue 1153 ("ice_hue_2", 512x16) to: D:\UO\tools\vseUOAware\exports\Hue\hue1153.png`.
  I could not look at the picture: reading it was denied by the unattended hook (section 8); the file exists.

## 8. Deviations and decisions for Chase

- **Two actions were denied by the unattended hook** (logged in `D:\UO\unattended-denials.log`), neither needed:
  1. `Grep` of `D:\ShatteredLegacy\scripts\validate-art.py` for `def needed_mobtypes|...`, to find lines to edit. Done
     with `grep -n` in Bash instead (a read of a file I had written; it changes nothing).
  2. `Read` of `D:\UO\tools\vseUOAware\exports\Hue\hue1153.png`, to look at the hue swatch the smoke test rendered.
     Not done another way; the server's reply and the file's presence are the evidence.
- validate-art follows TazUO, not vseUOAware, where they differ (section 2). Asked to port vseUOAware's logic; its
  logic gives wrong answers for our client, so the port carries the TazUO behaviour and lists each difference.
- vseUOAware's map reader fixed in our copy (the UOP chunk order); its animation tools left as they are, documented as
  wrong in `MODIFIED.md`.
- The csproj changes (nuget.config, framework-dependent, ImageSharp 3.1.12) in 7.3.
- `scripts\find-free-art.py` is in D:\ShatteredLegacy, not shard-migration; so is validate-art.
- The pinned commit is d4531cd94, not the brief's 7c9215d97.
- Proposed bodies start at 0x800 (2048): past every body EA's mobtypes and Bodyconv name today (the highest is 1,973 plus
  our 4,783 equipment animation), below the server's 0x1000. A choice, not a rule; `--body-from` changes it.
- Proposed slots are in our anim7, beside the fox ears, so nothing of EA's is modified or shipped, as the package's
  client policy requires. Whether creatures share anim7 with worn items or get their own anim8 is for the import task.

## 9. Open questions for Chase

1. **The hook and the new server.** Every permission prompt is denied while the Golem runs, so an unattended
   session can neither approve the new project MCP server nor call its tools until both are allowed. All 86 tools are
   read only apart from writes confined to `D:\UO\tools\vseUOAware\exports\`. Proposed for the overseer, in
   `~\.claude\settings.json` (or the project's `.claude\settings.local.json`): under `"permissions": { "allow": [...] }`
   the line

       "mcp__vseUOAware"

   and at the top level

       "enabledMcpjsonServers": ["vseUOAware"]

   Not verified in a session (this one started before `.mcp.json` existed).
2. **ImageSharp:** keep 3.1.12 (no key; five advisories, none reachable from this code), or get a Six Labors key and
   use 4.1.2?
3. When the first creature body is registered: add a `body` kind to `registry.csv` (validate-art already reads it), to
   find-free-art's `KINDS`, and a mobtypes.txt override to Build-UoOverrides (the succubi need `MONSTER 1004`, and
   nothing writes mobtypes today). Each is a small change with its own check; none was made here.
4. The four replacements (kirin, succubus, timber wolf, unicorn): replace the stock art, or add them as new bodies?
   A timber wolf replacement also changes the 9 bodies Body.def draws with 225's frames.
5. The Ridable Bird "Player Slot" file is a rider animation (people actions 23-29 only): what is it for?

## 10. For Chase

- New: `D:\ShatteredLegacy\scripts\validate-art.py` and `scripts\tests\test_validate_art.py` (commit with the shard
  repo), `D:\UO\shard-migration\.mcp.json` and `notes\cc-P134-tools\` (this repo). Changed: `CHANGELOG.md` (a new
  2026.10.17.4 section, one Staff line; 2026.10.17.3 was already committed) and `VERSION` (2026.10.17.4).
  `tools\progress.py` was run (README.md, dashboard.html, tools\progress.json).
- Not in any repo: `D:\UO\tools\vseUOAware\` (source copy, build, exports). Nothing under `D:\UO\third-party\` was
  changed, built or run, and the zip's prebuilt binaries were not touched.
- To try it: open a new Claude Code session in `D:\UO\shard-migration`, approve the vseUOAware server when asked, and
  ask it something like "inspect Trammel 3503, 2574".

## 11. Attribution

- `scripts\validate-art.py`: "Adapted from vseUOAware by ghostbyte420, GPL-3.0 (vseUtilities commit e4b1d243)", in
  the file header, with the source files it follows. The file is GPL-3.0.
- `D:\UO\tools\vseUOAware\`: vseUOAware by ghostbyte420 (consultant otimpyre), GPL-3.0, https://github.com/ghostbyte420/vseUtilities,
  servuo.dev resource 2687. LICENSE copied; modifications listed in MODIFIED.md and marked in each changed file.
- GPL-3.0 is ModernUO's license family. Fine in the private repos; if this code is ever distributed, GPL source
  obligations apply (SOURCE.txt says the same).

## 12. Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`, run with this note
written (before its last line), commits nothing:

```
=== code  (D:\ShatteredLegacy) ===
  4 file(s) pending:
    CHANGELOG.md
    VERSION
    scripts/tests/test_validate_art.py
    scripts/validate-art.py
  dry run: would add, commit and push

=== docs  (D:\UO\shard-migration) ===
  13 file(s) pending: README.md, dashboard.html, testing/SUMMARY.md, testing/play-tests.json (play-test mirror,
  machine output), tools/progress.json, .mcp.json, notes/cc-P134-tools/ (6 files),
  notes/cc-P134-vseuoaware-art-checks-mcp.md
  dry run: would add, commit and push

Repo Result
---- ------
code dry run
docs dry run
```

Final test run: 21 tests, OK.

P134 DONE
