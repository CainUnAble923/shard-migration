# cc-P779: seasonal content for the Festival store and boxes, assessed

Iron Golem, 2026-11-02. Assessment only, no code. I read the five packages in `D:\UO\third-party\code\` (reference
only: nothing there was built, run or copied) and checked them against the P760 Festival store
(`server/customizations/RewardStores/FestivalStore.cs`) and the P763 seasonal box slots
(`notes/cc-P763-cont-loot-boxes-diversified.md`). Docs copy `D:\UO\golems\Iron\shard-migration` on `golem/Iron/P779`,
not committed.

## In plain words

- **Five holiday add-ons looked at:** a Christmas gift box, a Christmas stocking and talking snowman, a Halloween
  witch, Artisan Festival decorations (lanterns, pillows, tapestries, carvings), and a poisonous swamp event.
- **Worth bringing in, best first:**
  - the Artisan Festival decorations, as new stock for the Festival Peddler (spring has only 5 things to buy now,
    against 13 at Halloween and 15 in winter). This only works if our game client has their pictures, which I could
    not confirm;
  - a Christmas stocking at the Festival stall that players can grab a treat from once a day;
  - a Halloween witch who roams in October and drops spooky house decorations.
- **Not worth it:** the gift box hands out power scrolls and runic tools; the swamp event's boss drops a deed that
  permanently raises how many pets you can have; the witch's robe has armour-level resists and a stat boost. The
  talking snowman and swamp poison are ideas only.
- **For you:** pick which ports to queue. The decorations need an art check first (one line in the prompt).

## 1. Each item

Sizes are the downloaded .cs files. "Ser" counts classes with a hand-written Serialize (each is a D40 conversion).
None of the five has a license: each is community work (credit the author, ship only inside the player package or
the private repo, do not repost).

**What we have now:**
- **The Festival Peddler's stall** in New Haven, up while Halloween, winter or spring is on. It sells for Festival
  Tokens:
  - Halloween: 13 rows (masks, pumpkins, webs, a guillotine);
  - winter: 15 rows (snow globe, snowman, wreath, presents, trees);
  - spring: only 5 rows (chocolates, seeds, garland, potted plant, heart box).
- **Festival Tokens** come only in season (drops, the daily login, 2 per artifact; `FestivalTokens.Grant`).
- **Loot boxes** add one seasonal item in each window (P763); the spring pool "runs on stock items" until the spring
  art intake.

### Christmas Gift Box (DragnMaw)

- **What it does:** a gift box (0x46A2) in one of 20 hues. Opening it puts a fixed reward list from the author's own
  server into the pack:
  - a fireworks wand;
  - ServUO heritage and holiday tokens (150 Heritage Sovereigns, 2018 and 2019 gift tokens);
  - 100 each of barbed leather, valorite and heartwood;
  - three runic tools (barbed/valorite/heartwood tier, then horned/gold/ash, then spined/shadow/oak);
  - **seven power scrolls**: 150 in a weapon skill and in a support skill, 120 in a craft, a caster skill, a tamer
    skill and a bard skill.
  
  The author says "modify the script to give out the rewards you would like".
- **Size:** 1 .cs, 392 lines, 2 Ser. It uses ServUO-only token types.
- **Fit and overlap:** the winter loot-box slot (P763) and the winter Festival rows already do "a holiday box with
  presents". The box itself is a hued container with a fixed list.

### Stocking full of goodies and Talking Snowman (Candy Apple)

- **What it does:**
  - **The stocking** (0x2BDC) is placed and works like apple bobbing. A player at the stocking holds still for 6 s.
    Then there is a 30% chance of one of nine prizes: jelly beans, cookies, a candy cane, cake, chocolate, a holiday
    bow, a holiday bell, "Olive the Other Reindeer" (a reindeer statue, 0x3A5F), or a **holiday tree deed**.
  - **The snowman** (`MrSnowman`, flipping 0x1A01-0x1A04) is locked down and says one of six puns within 4 tiles
    ("Chillin' with my Snowmies").
- **Size:** 5 .cs, 326 lines, 5 Ser.
- **Faults and gaps:**
  - The stocking has no per-player limit, so a player can grab again every 6 s, without end (holiday tree deeds
    included).
  - It freezes the player with `CantWalk` before its null check.
  - The snowman derives from `TalkingStatueBase`, which is in neither the package nor ModernUO.
  - The bell and bow use art 40384 and 40386 (0x9DC0 and 0x9DC2). Their names, "XmasBell" and "XmasBow", are
    unspaced.
  - "Olive, the Other Reindeer" is the title of a 1999 TV special.
- **Fit and overlap:** a stall-side activity for winter (and, re-skinned, any season) that gives our existing treats.
  ModernUO already has `HolidayBell`, `HolidayTreeDeed`, `JellyBeans` and candy canes. The winter stock already sells
  a snowman.

### Halloween Witch With Drop Items 2.0 (Milva)

- **What it does:**
  - **The witch:** "Halloween Witch", human body, 800-900 hits, 20-30 damage, Magery 110, always a murderer, Karma
    -24,000. She wields a broom (13-14 damage, self repair 25) and carries 100 gold.
  - **Her drops:** a 50% roll, then `Random(6)` over four cases, so about a 33% chance of one of:
    - the Shroud of the Wicked Witch (see below);
    - a Ouija board (a toy: random coloured effects and sounds when used);
    - a torture block addon deed;
    - a gore rack addon deed.
  - **The Shroud of the Wicked Witch** is a robe with 13 in each resist and night sight. Using it turns the wearer into
    a frog (body 81) with +5 Str and +5 Int as stat mods with no expiry, until they use it again.
  - **The Witch House addon** has about 500 components, for her lair.
- **Size:** 7 .cs, 1,183 lines (the house addon is most of it), 7 Ser. No core edits.
- **Fit and overlap:** a Halloween field boss whose drops are house decor, a good fit for the Halloween window and
  Festival Tokens (`FestivalTokens.Grant` already rewards the top damager of P776's lantern procession). It overlaps a
  little with the stock Halloween creatures. `code/season-of-the-witch` (another download on disk) has no intake
  row or assessment yet; a witch port should look at it first so the two do not both land.

### Artisan Festival reward items 2016-2019 (Sareus)

- **What it does:** 64 simple decor classes from OSI's Artisan Festival (Publish 101 art):
  - paper lanterns for the virtues and dungeons (Honor, Sacrifice, Hythloth, Destard and others), as lights;
  - throw pillows for virtues and anti-virtues;
  - tapestries;
  - wooden sculptures, as lights.
  
  Each is a named, flippable item. There are no mechanics.
- **Size:** 4 .cs, 2,966 lines of near-identical item classes, 4 Ser per file (64 classes in all). It could be about 300
  lines of data in a port.
- **Art:** item IDs 40423-40600 (0x9DE7-0x9E80). Our client data copy (`D:\UO\tool-trials\client-data-copy\tiledata.mul`)
  names 0x9DE7, 0x9DC0 and 0x9E80 "BritanianShip MainHu", which are ship hull parts. Either that tiledata is older than
  the art, or these IDs do not show the festival art in our client. **This must be checked with the art tools
  before any port.**
- **Fit and overlap:** spring is the thin season (5 rows) and its box pool waits on art. Virtue decor also suits the
  Artificers' Order or the League shop. Nothing like it is in our stores now.

### Poisonous Swamp event stuff (manwitch, with Milva's Halloween pieces)

- **What it does:**
  - **Swamp poison:** an `EventSink.Movement` hook on every player step poisons the walker on swamp land or statics:
    15% Regular on deep swamp, 5% Lesser on light swamp. Staff, the dead, the mounted, the already poisoned and
    anyone wearing swamp boots are spared.
  - **Blackwater Hattie:** a witch boss with 2,800-3,900 hits, 29-39 damage, Necromancy 120, a plague-spawn summon on
    25% of hits, 1,000-10,000 gold, and FilthyRich ×2 plus MedScrolls ×2. She has a 20% drop of one of:
    - swamp boots (thigh boots, random green);
    - a witch's broom spear (self repair 25);
    - a **Pet Slot Deed**, +1 to max followers, up to 11.
  - **A swamp shack addon.**
- **Size:** 6 .cs, 758 lines, 5 Ser. The movement hook runs on every step of every player.
- **Fit and overlap:** not seasonal. Swamp poison is a world rule, and it would hit the swamps our SOS map work
  fenced and reopens (the Swamp of Desolation is a sealed dungeon fence today). The broom duplicates the witch's.

## 2. Rules check

The rules: nothing that grants skill or stat points, power scrolls, bless deeds or property artifacts, and items
usable now and mostly helpful.

| Item | Skill or stat points | Power scrolls | Bless deeds | Property items | Usable now, helpful | Verdict |
|---|---|---|---|---|---|---|
| Christmas gift box | none | **seven, up to 150** | none | **runic tools** (they make property items) | the list is one server's | **fails** |
| Stocking and snowman | none | none | none | none | treats and decor; the stocking is endless as written | **passes** once limited |
| Halloween witch | the robe's **+5 Str/Int with no expiry** while a frog | none | none | **the robe: 13 to every resist, night sight**; the broom: self repair | the decor deeds and the Ouija toy are fine | **passes without the robe and broom** |
| Artisan Festival decor | none | none | none | none (lights and decor) | yes, if the art is in our client | **passes** |
| Poisonous swamp | none | none | none | the broom (self repair) | **the Pet Slot Deed**: a permanent +1 follower slot, a character power the rules' spirit forbids; poison on every swamp step is a hazard, not a reward | **fails** as a package |

## 3. Recommendations

| Item | Call | Why |
|---|---|---|
| Artisan Festival decor | **port** (small, if the art checks out) | Plain decor, no mechanics, 64 pieces, and it fills the thinnest Festival season (spring) or a guild shop. |
| Stocking | **port** (small), rebuilt | A cheap, social stall-side activity: grab a treat once a day per account in season, from our own treats. |
| Halloween witch | **port** (small), trimmed | A Halloween field boss with decor drops and Festival Tokens to the top damager. Drop the robe and the broom; keep the Ouija board and the two gore decor deeds; the house addon is optional lair dressing. |
| Talking snowman | **idea only** | Speaking decor is a nice touch, but its base class is missing and the puns are not our voice. Fold a speaking snowman into the stocking port if wanted. |
| Christmas gift box | **skip** | Power scrolls, runics and ServUO tokens; the P763 winter slot already is our holiday box. |
| Poisonous swamp | **skip** the boss and the Pet Slot Deed; swamp poison **idea only** | The deed breaks the follower cap for good. Swamp poison is a world rule for later, if swamps ever want danger (and swamp boots could then be a Festival or League item). |

### Ranked ports, with prompt sketches

1. **Artisan Festival decor** (one small Golem task; about 300 lines of data plus facts).
   - Sketch: "First check art 0x9DE7-0x9E80 in our client with the art tools; if present, add the 64 Artisan Festival
     pieces (lanterns and sculptures as lights, pillows and tapestries flippable) as data-driven decor, put 8-12 of
     them in the spring Festival stock at 10-25 tokens and the rest in the spring box pool. Credit Sareus. Tests for
     each row and flip pair." If the art is missing, the task stops after the check.
   - First because spring is the thinnest season and it is pure decor.
2. **Holiday stocking** (one small Golem task; about 200 lines plus facts).
   - Sketch: "Add a stocking to the winter Festival stall: a player at it holds still 6 s and, once a day per
     account in season, gets one of our winter treats or small decor (no deeds), with a System line; one Festival
     Token on the first grab of the day. Tests for the daily limit, the season gate and the prize table."
   - Second because it is small and makes the stall something to visit, not only a shop.
3. **Halloween witch** (one small to medium Golem task; about 400 lines plus facts, more with the house).
   - Sketch: "Add a Halloween witch: a field boss spawned in the Halloween window at a few wild spots (or as a P776
     encounter), about 900 hits, Magery 110; drops one of a Ouija board, a torture block deed or a gore rack deed,
     and Festival Tokens to the top damager. No robe, no broom; the witch house only as a placed lair if Chase wants
     it. Tests for the season gate, the drop table and the token award."
   - Third because Halloween already has the most stock and the lantern procession; it is ready for next October.

Idea only, not ranked: a speaking snowman for the winter stall, and swamp poison with swamp boots as a later world
hazard.

## Notes for the record

- `D:\UO\third-party\CODE-INTAKE.md`: none of the five had a row. I added five rows after P778's rows, each with
  Overseer `assess (P779)` and the call above. A copy of the file from before the edit is in this session's
  scratchpad.
- The art lookup used `D:\UO\tool-trials\client-data-copy\tiledata.mul` (not the main desk's client data). That
  tiledata may be older than the client players run, so "unverified" is the honest state of the art.
- Credits to keep if ported: Sareus (Artisan decor), Candy Apple (the stocking), Milva (the witch and her decor).

P779 DONE
