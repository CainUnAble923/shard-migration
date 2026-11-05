# cc-P798: assess builder tools and the art pipeline

## In plain words

- **Of the ten downloads, none should come in as written, and only two are worth building, both small staff tools.** Most overlap what we have: the Visual Builder, the vseUOAware art tools and the seasonal decor switch.
- **The Blender file is a short list of camera settings, not a way to make art.** With fixes it could light and angle new statics consistently. It does nothing for animations. It's not needed for gumps.
- **Gump and static art already have a route into the game.** The Claude Design gump art canvas can feed it, but the canvas holds page designs, not image files, so each piece needs exporting to a true-size PNG. New creature animations stay out of reach for now; buying or reusing finished `.vd` packs remains the way.
- **SVDungeon 0.8.0 changes one thing:** when dungeon dives come up, port 0.8 and not 0.7, because it already made the change P211 said a port would need.
- **For you:** two things. Have you reacted to the gump art canvas? Its import has been waiting on that since 11-01. And pick whether to queue the two staff tools. Nothing was built or changed in the game.

## Ranked list

| Rank | Item | Recommendation | Rough size | Why |
|---|---|---|---|---|
| 1 | **AddonGenerator HS** (with **Addon2Static**) | **Rebuild as ours**: a capture tool in the Visual Builder | about 250 lines, facts | Lets a human decorate in game and hand the result to a Golem as data. |
| 2 | **Animation Locator** | **Rebuild as ours**: a small staff command | about 120 lines | Shows, in the real client, what each action of one of our 74 bodies does. |
| 3 | **SVDungeon 0.8.0** | **Idea only for now**: port from 0.8 when dives are queued | none now | Its sites are the per-dungeon state P211 asked for. Dives aren't queued. |
| 4 | **UO Art in Blender** | **Idea only**: take its settings, with a small proof if Chase wants 3D statics | about half a prompt | The settings are the whole value, and they need three fixes. |
| 5 | **Decorum** | **Skip** | none | Seasonal decor already does this better, and it needs UltimaLive. |
| 6 | **Addon Editor** | **Skip** | none | Needs XmlSpawner, and our addons are seeded from code, so edits wouldn't last. |
| 7 | **Gump Image Browser** | **Skip** | none | GPL, and vseUOAware renders gumps already. |
| 8 | **Cliloc Gump** | **Skip** | none | vseUOAware searches clilocs already. |
| 9 | **CentrED+ tutorial** | **Skip**, keep on disk as reference | none | Beginner guide to an editor we don't use. |

## 1. Each item

Unless noted, `SOURCE.txt` states no license terms: treat as community work, credit the author, ship only inside the player package or the private repo, do not repost. "Lines" are the `.cs` files, without `_zips`; "Ser" is hand-written `Serialize` overrides. None ships art, and none needs a core edit. All are staff-only tools, with no player content.

### AddonGenerator through High Seas (Hammerhand; CEO's YAAAG)

- **What it does:** `[AddonGen` (Administrator) picks an area in game and writes a ready addon `.cs` from the statics, items and tiles in it. It can cover ItemIDs up to 39212.
- **Size:** 1 file, 907 lines, 3 Ser.
- **Fit:** nothing here does this. The Visual Builder (`ClusterFVisualBuilder.cs`, `[VBuild`, 1,045 lines) places plain statics but can't save them out. Our addons and layouts are data files written by hand or by script. Golems build from data and renders, so this is for the humans: decorate in game, then hand over the result.
- **Problem:** it writes ServUO-shaped C# into a folder on the server, with hand-written serialization. We'd want data, not code.

### Addon2Static (Hammerhand; author unknown)

- **What it does:** `[Addon2Static` turns a targeted addon into separate statics and deletes the addon.
- **Size:** 1 file, 58 lines, 0 Ser.
- **Fit:** a small, handy step for the capture tool. A seeded addon would come back at the next world load, so it's only for staff-placed ones.

### Addon Editor (zerodowned)

- **What it does:** `[addonedit`, a gump to select an addon and add, unlink or delete its parts.
- **Size:** 2 files, 320 lines, 1 Ser. **Needs XmlSpawner** attachments, which we don't have on ModernUO.
- **Fit:** poor. Our addons come from code and seed data, so an in-game edit is lost or fought by the next seed. For staff-placed work, the Visual Builder is enough.

### Animation Locator + Freeze Frame (zerodowned; Father Time)

- **What it does:** an item that plays a chosen action on a targeted mobile, on a loop or frozen on a frame, from a gump.
- **Size:** 1 file, 401 lines, 1 Ser. Its header asks that the header be kept.
- **Fit:** vseUOAware's `render_animation_frames` shows frames offline, and our proofs use frame bursts in a client. But neither lets staff try action numbers live on a shard body. `records.json` holds 74 custom bodies, and P139 had to work out which action each `.vd` plays. Useful but small.

### Gump Image Browser, SGI command (Lokai)

- **What it does:** `[SGI` (Administrator) browses gump images, keeps editable descriptions, pins images into a mock gump and writes it to a `.cs` file.
- **Size:** 2 files, 912 lines, 0 Ser. It requires Lokai's Custom Gump, and that file is included. It locks to one user at a time.
- **Terms: GPL v2 or later.** A port must keep the header and stays GPL.
- **Fit:** vseUOAware's `render_gump` and sheet scripts show gumps to Golems without a server. `code/gumpstudio` is on disk for design. New gumps are written as code.

### Cliloc Gump (Lokai)

- **What it does:** `[Cliloc` (Administrator) shows and searches client strings in game.
- **Size:** 1 file, 312 lines, 0 Ser.
- **Fit:** vseUOAware's `search_localized_strings` and `get_localized_string` already do this, and the bot's `cliloc.py` reads the file too.

### SVDungeon 0.8.0 (ScriptVisitor), against 0.7.0

- **Size:** 79 files, 13,339 lines, 1 Ser (a new rescue chest). 0.7.0 was 77 files, 12,363 lines, 0 Ser. Terms: free to use and modify, credit appreciated.
- **What changed:** **instances.** Besides a dungeon on the real map, there can be slots that are maps of their own showing a base map's terrain. A dungeon's state is now an object per site and build (`SVSite`, `SVGeometry`) instead of static fields, and `SVDungeonState.cs` is gone. Removing a slot rescues loose items into a chest. Off by default.
- **Its own limit:** the changelog says instances are "infrastructure for now": there is no way in for players, and tickets are future work.
- **Fit:** P211 found the single-dungeon state would need to become per-instance for League dives, and 0.8 did that. Everything else P211 found stands: dynamic items, fails four playbook rules as built, two to three weeks of prompts by its guess, port only once dives are on the board.
- **New traps:**
  - Its default slots start at map 32, **which is ours**: the Fold is map 32 and its 16 copies are 33-48. Slots must start at 49 or later.
  - It writes `Map.Maps[index]` directly. Pinned's `RegisterMap` is private (P76), so the port should use our existing facet pattern.
  - Our 16 Fold copies already do much of this, with parties and clean-up.

### Decorum (Gargouille)

- **What it does:** staff record named sets of decoration for a place and flip between them by gump or script. Each flip deletes items and rebuilds them from stored ID, hue, name and place.
- **Size:** 2 files, 1,386 lines, 1 Ser. **Needs UltimaLive** for land changes, which we don't run. Its land handling can turn tiles black by its own warning.
- **Fit:** `ClusterFSeasonalSwitch` plus the Halloween and winter decor do this with dated windows and tracking by serial, so they delete exactly what they placed. Decorum deletes anything in a set except a few listed types.

### CentrED+ tutorial (by Nylo; posted by TheArt)

- **What it is:** a beginner's PDF to CentrED+'s tool buttons, 1.6 MB, read here as text.
- **Fit:** we build maps with `scripts\mapbuild`, mapops and the UORegionEditor (P214), and CentrED# source is on disk. Nothing in it improves `notes\guides\building-and-decorating.md`. Its rule of thumb of 20 up for a floor is already in the guide. It is **not** an artwork tutorial.

### UO Art in Blender (Feynman)

- **What it is:** one scene, `basicUO.blend`, Blender 2.76, 501 KB. No models to ship, no rig, no script, no animation.
- **What's in it:** I read the file's data directly, without opening it in Blender:

| Setting | Value |
|---|---|
| Camera | orthographic, rotation 45, 0, 45 degrees, scale 10 |
| Lights | two hemi lamps, energy 1.0 and 0.5 |
| Render | 200 x 200, Blender Internal, anti-aliasing 8, alpha mode 0 (sky) |

- **Fixes it needs (my working, not tested in Blender):**
  1. **Projection.** At 45 degrees, a square tile draws 0.71 as tall as wide. UO's land tile is 44 by 44. So a render needs stretching 1.41 tall (a pixel aspect setting) to sit on a tile.
  2. **Scale.** At 20 pixels a unit, the 2-unit starter cube is 57 pixels wide, not a tile's 44.
  3. **Transparency and renderer.** Alpha mode "sky" needs to be transparent, and Blender Internal left Blender in 2.80, so the look has to be rebuilt in a current renderer.
- **Blender isn't on this PC** (P214 said the same; its installer is machine-wide).

## 2. Rules check

Every item passes. A search of the code packs found no power scrolls, stat scrolls, bless deeds or skill balls, and the two tutorials contain no game content. SVDungeon's population stage spawns creatures from a pool we'd write ourselves, so its loot stays ours to set.

| Item | Usable now | Mostly helpful |
|---|---|---|
| AddonGenerator | Yes, once rebuilt | Yes |
| Addon2Static | Yes | Yes, in small uses |
| Addon Editor | No: needs XmlSpawner | Little |
| Animation Locator | Yes, once rebuilt | Yes, for staff |
| Gump Image Browser | Yes, once ported, under GPL | Little |
| Cliloc Gump | Yes | Little: a duplicate |
| SVDungeon 0.8.0 | No: nothing to enter it by, and dives aren't queued | Later |
| Decorum | No: needs UltimaLive | Little |
| CentrED+ tutorial | Reference only | Little |
| UO Art in Blender | Only with its fixes, and Blender installed | For statics only |

## 3. Recommendations and prompt sketches

**1. Visual Builder capture (rebuild).** Sketch: "Add `[VBuild capture`: mark a box, and it writes the statics and items in it to a data file (id, offset, hue, name) in our layout shape, for a Golem or a seed to place; add `[VBuild statify` to break a staff-placed addon into statics, refusing a seeded one." About 250 lines and facts. Data, not generated C#. Ideas from AddonGenerator and Addon2Static; credit both.

**2. Animation test (rebuild).** Sketch: "Add a GameMaster command `[AnimTest`: target a mobile, then a gump steps through actions and frames, with play, loop and freeze." About 120 lines. Credit Father Time and zerodowned.

**3. SVDungeon (idea only).** Change P211's draft port prompt when it's queued: base it on 0.8.0, start slots at 49 or later, and add a way in. Nothing to do now.

**4. Blender (idea only).** If Chase wants 3D-made statics: "Install a portable Blender in a tool-trial folder, write one script that renders a model to a transparent PNG with UO's projection, tile scale and two facings, and put one test piece through `art\` and a client shot." About half a prompt.

**5-9. Decorum, Addon Editor, Gump Image Browser, Cliloc Gump, CentrED+ tutorial (skip).** Reasons above.

## The art question: is there a usable path?

| Art | Route today | Works now? | What's missing |
|---|---|---|---|
| **Gumps** | PNG to `shattered-legacy-art\gumps\<id>.png` (56 there), with a `registry.csv` row | **Yes** | True-size export from the canvas |
| **Statics** | PNG to `art\<id>.png` (672 there), plus a `records.json` tiledata record and a registry row | **Yes** | Same, plus two facings when a piece needs them |
| **Generated images** | Codex route from P152: `scripts\art\Art.ps1`, `art_process.py`, review folder, budget | **Yes** | Nothing |
| **New creature animations** | `.vd` packs copied into anim7 by `build-equip-anims.py`, with `bodyAnims` (74 bodies) | **Only for finished `.vd` files** | A way to draw them, below |

**Claude Design.** The canvas "Shattered Legacy gump art" holds the pet choice scroll, moongate skip achievement, reward store window and the Hall of Finishers banner (a 44 x 88 static at 4x). Its files are HTML designs (`project\*.dc.html`) and a tokens file; **it holds no image files**. So an import needs a step that renders each to PNG at true size, then checks it in a client: fine lines at 4x can vanish at 1x. The overseer's log has Chase reacting first, and I found no record that he has.

**Blender adds** consistent light and shape for statics made from 3D models, including both facings of one piece, which is hard to get from image generation. It's not needed for gumps.

**Animations are a different size of job.** A `.vd` holds 13 to 35 actions, each in 5 directions, each with its own 256-colour palette; the fox has 295 frames. It needs a rigged model, renders of every frame, and a writer for the format. I found tools that copy and read `.vd` blocks and no writer. `basicUO.blend` has none of this. The nearest thing on disk is **SpriteMotion** (MIT, `code\spritemotion`), which P214 deferred until a creature or gear rework is queued. That's still the right call. It's built around the human body, not creatures.

## How this was checked

- Read `SOURCE.txt` and code for each pack; for SVDungeon, its changelog, README, instance config and a file diff against 0.7.0. Read the PDF as text. Read `basicUO.blend`'s data with a small read-only script of mine in the scratchpad, which ran nothing from the file.
- Our side: `ClusterFVisualBuilder.cs`, `ClusterFSeasonalSwitch.cs`, `TutorialCopies.cs`, `records.json`, the art vendor folder and its `SOURCE.txt`. Notes for P100, P139, P152, P211 and P214, the P59 `.vd` format, the building guide, and the overseer's log for the canvas.
- Canvas: listed its files, without opening the designs.

**Not verified.** Nothing was built or run, from `D:\UO\third-party` or anywhere else. The Blender fixes are worked on paper. Rebuild sizes are my estimates. "No `.vd` writer" means I found none by name and text search in the code copy and notes, not that I read every tool. I can't see whether Chase reacted to the canvas outside the overseer's log.

## Other

- **`D:\UO\third-party\CODE-INTAKE.md`:** none of the ten had a row, so I added ten, marked `assess (P798)`. Backup: `CODE-INTAKE.md.bak-20261105-p798`.
- **Follow-ups:** none queued. Chase picks.

P798 DONE
