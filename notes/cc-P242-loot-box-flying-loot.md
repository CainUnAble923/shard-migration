# cc-P242: Loot that flies out of the box (CC-BY 3.0 Flying Loot)

2026-10-21, the Bronze Golem (Opus), branch golem/Bronze/P242 of both repos. Prompt: `cc-P242-loot-box-flying-loot.md`.
Not committed (the Golem commits after DONE). Both repos were clean at the start. Nothing was run against any world,
nothing was deployed, and the package was not built or published.

## Headlines

- **Opening a loot box now sends the best thing inside flying out of it**, just before P79's fanfare. Nine animations
  ship: sword, bow, staff, armor, shield, ring, gem, potion, clothes.
  - **The art:** Clint Bellanger's Flying Loot set (CC-BY 3.0), reworked for UO, art 15536-15589.
  - **How it is sent:** a location effect over the opener, because the box is in their pack.
  - **Who sees it:** a tier 4+ box (a major fanfare) shows it to everyone nearby; a smaller box to the opener alone, as
    the fanfare does.
  - **When it is off:** `clusterf.lootBoxes.flyingLoot = false` turns it off for everyone, and a muted fanfare
    (`[FanfareMute`) hides it too.
  - Nothing changes what a box holds or hands over.
- **The best item decides the animation, by the type of the item handed over.** Gear (weapons, armor, shields,
  jewelry) beats the box cosmetic (clothing), which beats gems, which beat potions; the first rolled wins a tie.
  - **The stated fallback:** gold, Renown, bandages, resources, reagents, scrolls, maps, recipes, placeholders,
    components and a box in a box have no animation, so the fanfare plays alone.
- **The rework keeps the author's pixels.**
  - The pink background and the flat black drop shadow became transparent.
  - Near-black pixels were lifted to (8,8,8) so 16-bit art keeps them.
  - The frames were cut to a shared box.
  - **Not resized:** the items are already UO's size (measured below).
  - Every change is listed in each registry row and in `SOURCE.txt`, as CC-BY asks.
- **Tests:**
  - Server: 4 new facts, each seen red first.
  - Package: 1 new fact, red on two mutations; the registry ledger was updated.
  - Full gate green twice: `sl-modernuo:cc-P242`, **2,021 tests, 2,017 passed, 4 skipped, 0 failed**.
  - P26's gates pass.
- **Not seen in a client.** "For Chase" lists what to look at, mainly whether the ring and the gem read at all (they
  are 5 px, as OSI's ring is).

## 1. Facts

- **The set** (`D:\UO\third-party\oga-flying-loot`, `SOURCE.txt` read):
  - 23 PNG strips, each **384 x 128 RGB = 6 frames of 64 x 128**, pink (255,0,255) background, plus Blender sources.
  - In each frame the item flies up out of a container on an arc and lands, with a flat **pure-black** drop shadow
    below it (frames 1-4) or merged with it (frames 5-6).
  - Pure-black pixels per strip run from 1 (gem) to 1,355 (steel armor), almost all of them shadow.
  - No pixel is near-pink, so there are no anti-aliased edges to clean.
- **Scale, measured against OSI's art** (drawn pixels, rendered from the client's `artLegacyMUL.uop`):

  | Thing | OSI art (drawn) | Flying Loot item |
  |---|---|---|
  | Metal chest 0xE40 | 36 x 45 | — |
  | Longsword | 0xF61, 30 x 30 | about 30 px long |
  | Potion | 0xF0C, 9 x 17 | about 8 x 8 |
  | Ring | 0x108A, 5 x 6 | 5 x 5 |

  The items are already UO scale at 1:1. The arc (about 100 px tall once cut) rises above a character and lands at the
  feet, about two chest heights. So the rework does not resize. Halving, which "64x128" invites, would make a ring 2 px.
- **Code re-verified on the current tree:**
  - `LootBox.OnDoubleClick` is at `LootBoxes/LootBoxItems.cs:185` (as the prompt says): account check, pack check,
    `IsSafeToOpen`, then `Open`.
  - The fanfare's `Effects.SendLocationEffect` is at `LootBoxes/ClusterFFanfare.cs:225` (as the prompt says). The
    fanfare is queued in `Open` and plays when its 2.5 s merge window closes (`:91-105`).
- **The roller's categories** (`LootBoxRoller.cs`):
  - theme slots: ore, logs, leather, craft resources, a treasure map, scrolls, placeholders, a fragment and a sash;
  - pools (`BoxPool`, `ClusterFLootTable.cs:32`): Consumables (bandages or potions), Resources (metal, wood, leather or
    gems), MagicGear (`Loot.RandomArmorOrShieldOrWeaponOrJewelry`), Recipes, Cosmetics (`BoundCosmeticSash`) and Rare
    (fragments, placeholders, schematics, components, a box in a box).

  Mapped by the item's type:

  | Item | Animation | Strip |
  |---|---|---|
  | Swords, axes, knives, any other weapon | Blade | longsword |
  | Bows and crossbows (`BaseRanged`) | Bow | longbow |
  | Staves, maces, spears, polearms | Staff | staff |
  | Armor | Armor | steel_armor |
  | Shields (checked before armor; a shield is armor in pinned) | Shield | shield |
  | Jewelry | Jewelry | ring |
  | `Loot.GemTypes` | Gem | gem |
  | Potions | Potion | health_potion |
  | Clothing (the cosmetic sash) | Clothing | clothes |

  The roller never makes footwear, wands or belts, so those strips (and the other 14) do not ship.
- **How TazUO plays an effect** (TazUO 3212623f):
  - `GameEffect.cs:15-55`: each animdata frame lasts `FrameInterval x speed x 10` ms, and the frames loop.
  - `EffectManager.cs:70`: the effect ends after `duration x 50` ms.
  - Our animdata is interval 1 with the landed frame held twice (8 frames), and the server sends speed 10 and
    duration 16. So the flight plays once, in 800 ms, and ends resting on the landed frame.

## 2. Rework (every change, as CC-BY 3.0 asks)

`notes/cc-P242-tools/flying_loot.py` (frames) and `scripts\anchor-art-frames.py` (P26's tool):

1. **The pink background** becomes transparent.
2. **Pure black (0,0,0), the drop shadow,** becomes transparent. UO art means black as transparent, and an effect drawn
   over a character has no ground for a shadow. Per strip: longsword 206 px, longbow 288, staff 371, steel armor
   1,355, shield 658, ring 67, gem 1, potion 184, clothes 655.
3. **Near-black pixels are lifted.** A pixel with every channel under 8 becomes (8,8,8), the darkest colour that
   survives 16-bit art (5 bits a channel), so dark edges never become holes. Per strip: 12, 9, 10, 90, 42, 5, 0, 11,
   34 px.
4. **Not resized** (part 1).
5. **Cut to each animation's shared box.** `anchor-art-frames.py --bottom-pad 0` centres the box and puts its bottom
   row on the tile's tip, so the item lands at the opener's feet. No pixel is changed by that step, and the tool
   re-read every PNG against its frame.
   - Boxes: longsword 42x103, longbow 39x99, staff 49x117, armor 29x98, shield 23x97, ring 6x83, gem 4x87, potion
     10x83, clothes 18x92.

Nothing else: no recolouring, no redrawing, and the author's frame order is kept. Without the shadows, each item rises
and falls in roughly one column. The preview (`notes/art/flying-loot/preview.png`, by `notes/cc-P242-tools/preview.py`)
shows every frame at 2x beside a 36 x 45 outline of OSI's chest. The outline was measured from the client, and no EA
pixel is in the image.

## 3. What shipped

| File:line (ShatteredLegacy) | Change |
|---|---|
| `player-package/vendor/shattered-legacy-art/registry.csv:188-241` | 54 rows, 15536-15589, kind art, written first. The license column is `CC-BY 3.0, Clint Bellanger; changed: <the five changes>; credit Clint Bellanger and Blarumyrran (base icon styles)`, and the source column names the strip and frame |
| `.../art/15536.png` to `15589.png` | 54 PNGs, 87 KB in all |
| `.../records.json:57-65` (tiledata), `:79-87` (animdata) | 9 + 9 records on the base IDs. Tiledata copies OSI's effect art, the fanfare's sparkle 0x373A (read 2026-10-21: Animation 0x01000000 only, weight 255, height 0); names of 19 ASCII characters at most (`flying longsword` ...). Animdata is frames 0-5 then 5, 5, interval 1. Inserted as lines, so the hand layout is kept |
| `.../SOURCE.txt:313-331` | The set's section: author, license and credit rule (copied from `oga-flying-loot\SOURCE.txt`), files, every change, records |
| `server/customizations/LootBoxes/ClusterFFlyingLoot.cs` (new, 164 lines) | `FlyingLootKind` (`:30`); the setting `clusterf.lootBoxes.flyingLoot`, default on (`:49`); the timing and tiledata constants; `Records`, the server's copy of the nine records (`:62`); `KindOf` (`:89`); `Rank`/`Best` (`:104`, `:114`); `Sent`, an event the tests watch (`:130`); `Play` (`:133`), which sends a public location effect for a major box and the private hued effect packet otherwise, and nothing when off, muted or with nothing animated |
| `server/customizations/LootBoxes/LootBoxItems.cs:213-216, 222, 250, 263-265` | `Open` keeps the items it hands over and calls `ClusterFFlyingLoot.Play` right before queueing the fanfare. The refusals in `OnDoubleClick` return before `Open`, so a refused box sends nothing |
| `server/tests/Misc/LootBoxFlyingLootVerification.cs` (new) | 4 facts, below |
| `player-package/tests/Build-UoOverrides.Tests.ps1:253-254` | The records fact skips 15536-15589 (this set has its own fact) |
| `:293-297` | Ledger: 234 registry rows, 204 art rows (+54, cc-P242) |
| `:446-492` | New fact `TheFlyingLootRecordsAreTheServersTableAndEveryFrameIsRegisteredWithItsPngAndCredit` |
| `CHANGELOG.md`, `VERSION` | 2026.10.21.13 (Added, Staff) |

shard-migration: this note; `notes/cc-P242-tools/flying_loot.py` (registry rows, frames, records) and `preview.py`;
`notes/art/flying-loot/preview.png` (52 KB).

## 4. Play it

- **When:** on a successful open, at once. The fanfare follows when its merge window closes (2.5 s), unchanged and still
  queued as before, so the flight and the fanfare play together and neither replaces the other.
- **Who sees it:** the same audience as the fanfare. A major (tier 4+) box sends `Effects.SendLocationEffect` to
  everyone in range; a minor box sends the hued effect packet to the opener's client only, as P79's minor fanfare does.
- **Off switches:**
  - **Setting:** `clusterf.lootBoxes.flyingLoot` in `modernuo.json`, default true. It is read live, so no restart is
    needed.
  - **Mute:** `[FanfareMute` silences it for that player.
- **Drops:** unchanged. `Play` only reads the list of items `Open` already handed over. Fact 3 checks the sword arrives
  in the pack, and fact 4 checks the box still opens and delivers with the effect off.

## Tests

Server facts (`server/tests/Misc/LootBoxFlyingLootVerification.cs`), each seen red first:

| Fact | Pins | Seen red |
|---|---|---|
| `EveryKindOfItemMapsToARegisteredAnimationOrTheStatedFallback` (`:160`) | 9 records, distinct, 6-aligned inside 15536-15589, names of 19 ASCII characters at most. 31 named items map to their kind or to None (the fallback). 8 rolls of every theme at every tier: every weapon, armor, jewel, potion, clothing and gem rolled has an animation, every animated kind is in the set, and the fallback occurs | red B (spears dropped from Staff): "Spear: Blade, not Staff" |
| `TheBestItemWinsAndNothingAnimatedSendsNothing` (`:250`) | gear > clothing > gem > potion > none; the first rolled wins a tie | red A (clothing ranked above gear): "Values differ" |
| `OneEffectPerOpenForTheBestItemAndNoneWhenOpeningIsRefused` (`:280`) | Refused in the wild: nothing sent, box kept. In a guarded town: exactly one effect (Blade, to the opener alone at tier 2), and the sword is in the pack. Tier 4: one public Potion effect. A box of bandages and ingots: none. In a house, a stranger is refused and sends nothing; the owner sends one (Jewelry) | red B (sent before the checks): "Collection was not empty" |
| `TheSettingOffOrAMutedFanfareSendsNothingAndTheBoxStillOpens` (`:349`) | Setting off: no effect, box opened, shield handed over. Muted: no effect, box opened. Both back on: one Shield effect. The setting is restored after | red A (setting and mute ignored): "Collection was not empty"; also red in B ("contained 2 items") |

Package fact (`Build-UoOverrides.Tests.ps1:446`): the C# records equal records.json (IDs in order, names, flags, weight,
height, interval, frame order). Every frame is registered once as art, with its PNG, a license beginning
`CC-BY 3.0, Clint Bellanger; changed: ` and naming Blarumyrran. The set has exactly 54 rows.
- Red on scratch copy a (frame 15563's license without "changed:"): "frame 15563 license ...".
- Red on scratch copy b (C# potion renamed): "expected [flying red potion] but got [flying potion]".
- Green on the tree: **17 of 17**.

P26's gates:
- `find-free-art.py --data D:\UO\tool-trials\client-data-copy --tazuo D:\UO\cc-p40-work\tazuo-3212623f --run 54 --from
  15530` found the one free run, 15530-15633. I took 15536-15589.
- No other branch's registry and no claimed prompt uses the range.
- `--check-registry`: **0 of 234 registered IDs are no longer free.**
- `validate-art.py check-registry`: **0 of 234 rows have problems.**
- `scripts\tests`: **55 of 55.**

The probes changed the two server files in place. They were saved first, restored after, and compared byte for byte
before the green build.

**Build record** (`docker\uo\build.sh -t sl-modernuo:cc-P242`, each run detached, docker-build lock 09:42-09:54 CDT,
Docker VM page cache dropped before runs). Logs are `build-P242-*.log` in the session scratchpad.

| Run | Result |
|---|---|
| red A | 2,021 tests, 3 failed: facts 2 and 4, plus `CC6Batch1CreatureVerification.TheRestOfTheBatchKeepsItsServUOShape` ("Expected 3, Actual 2"; a creature test with nothing to do with loot boxes, green in both later runs) |
| red B | 3 failed: facts 1 and 3, and fact 4 as collateral |
| cycle 1 | **green: 2,021 tests, 2,017 passed, 4 skipped, 0 failed** |
| cycle 2 (after the patch notes) | **green, the same**; image 7a7f4df664a6 carries VERSION 2026.10.21.13 and the notes (read back from the container) |

All eight of P79's `LootBoxFanfareVerification` facts pass with the change.

Repo size rule: nothing new is over 5 MB. Two pre-existing large files are git-ignored (`git check-ignore`:
`.gitignore:100` `shattered-legacy-art/build/`, `.gitignore:95` `tools/playtest-bot/cache/`).

## 5. Website credits

For the shard credits list (CC-BY 3.0 requires it):

- **Flying loot animations by Clint Bellanger**, "Flying Loot Animations",
  https://opengameart.org/content/flying-loot-animations, licensed under Creative Commons Attribution 3.0 (CC-BY 3.0).
  Base icon styles by **Blarumyrran**.
- **Changes made for Shattered Legacy:**
  - the background and the drop shadow made transparent;
  - the darkest pixels lifted one step for 16-bit colour;
  - frames cropped;
  - not resized or recoloured.

The rule as `D:\UO\third-party\oga-flying-loot\SOURCE.txt` states it (copied into each registry row and `SOURCE.txt`):
"TERMS: CC-BY 3.0. Attribution required: credit Clint Bellanger (and Blarumyrran for the base icon styles) in the shard
credits."

## Deviations and decisions for Chase

1. **Not resized.** The prompt says rework "to UO scale (resize ...)", but measured against OSI's art the items already
   are UO scale at 1:1 (part 1). Shrinking them would make jewelry and gems invisible.
2. **The shadows are gone.** They are pure black, which UO draws as transparent; that is the prompt's "black to
   transparent". The item no longer has a shadow under it in flight.
3. **It plays at the moment of opening, not at the fanfare's flush.** The fanfare waits 2.5 s to merge celebrations, and
   the flight is the box opening, so it goes first and the fireworks follow. Moving it to the flush would be a one-line
   change in `Open`.
4. **Nine animations, not 23.** Only the kinds a box can hand over ship. Boots, belt, wand, rod, slingshot and the
   other weapon sizes are left in `third-party`.
5. **Fallback = no animation** for gold, bandages, resources, scrolls, maps, recipes, placeholders, components and a box
   in a box (fanfare only). A gold or chest effect would need art that is not in the set.
6. **Mute also hides it**, since it is part of the player's own celebration effects.
7. **Merge note for the integrator:** P241 (already committed) also changed the registry ledger line in
   `Build-UoOverrides.Tests.ps1` (180 -> 190 rows, 5 -> 15 gump rows). Merging both gives **244 rows, 15 gump rows, 204
   art rows**. The two branches touch the same lines, so the second merge will conflict there.
8. **A flaky test seen:** `CC6Batch1CreatureVerification.TheRestOfTheBatchKeepsItsServUOShape` failed once
   (red A), unrelated to this work. It joins the flakes listed in P241 and P271.
9. **Players who have not updated see a flying "UNUSED" tile.** The IDs are placeholder slots in EA's art, as for every
   art set the package adds (P236's satchels note the same). The server cannot tell whether a client has the package.
   If that is unwelcome until the package is out, set `clusterf.lootBoxes.flyingLoot` to false on live until the
   package with this art is published, then turn it on.

## For Chase

- **Setup:** rebuild the test shard from this branch (`sl-modernuo:cc-P242`), build the player package so the art and
  records ship, and update a test client.
- **A minor box:** in a guarded town, open a box holding gear (any tier 1-3 box from `[LootBox` (GameMaster) or
  an achievement).
  - Does the item arc up from your character and land at your feet, once, before the fireworks?
  - Is it visible only to you?
- **A major box:** open a tier 4+ box with a second character beside you; both should see it.
- **Small items:** open boxes holding only a ring, a gem or a potion. Are 5 px items worth showing, or should those
  kinds fall back to nothing?
- **Off switches:** `[FanfareMute` hides it, and `clusterf.lootBoxes.flyingLoot` false (test shard) turns it off for
  everyone. Turn it back on after.
- **No update:** a client that has not updated draws EA's own art in these slots, which is the "UNUSED" placeholder
  (`find-free-art.py --explain 15589`: "art placeholder"). So until a player updates, a small placeholder tile flies out
  of the box instead of the item. The fanfare is unchanged. See Deviations 9.
- **Credits:** add the "Website credits" lines above to the shard credits list.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun -NoRefresh -NoArchive -CodeRepo
D:\UO\golems\Bronze\ShatteredLegacy -DocsRepo D:\UO\golems\Bronze\shard-migration -Branch golem/Bronze/P242`. It points at
this Golem's work copies; the defaults are the main checkouts, which this desk may not touch. Code: 63 files pending
(7 changed, 54 PNGs, ClusterFFlyingLoot.cs, the new test). Docs: 4 (this note, the two tools, the preview). Neither is
BLOCKED.

```
Repo Result
---- ------
code dry run
docs dry run
```

P242 DONE
