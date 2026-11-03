# cc-P786: Halloween witch field boss

## In plain words

- **A wicked witch now haunts the Halloween season.** While Halloween is on, one stands near each of the Yew, Cove and
  Britain graveyards (Trammel). Players travelling in the wild at night may also meet one coming for them, through the
  random encounters.
- **She is a strong mage, about 900 hits.** Her corpse holds one prize: a witch's Ouija board (a toy that glows and
  moans), a torture block deed or a gore rack deed for a house. Whoever hurt her most gets 5 Festival Tokens.
- **She comes and goes by herself.** A slain witch returns to her graveyard after 30 minutes, and every witch leaves when
  Halloween ends. She will first appear next October; this year's window has just closed.
- **For you:** nothing to do. To see her now on the proof shard, force Halloween with `[FestivalMarket season halloween`
  and then run `[HalloweenWitch sync`. Every number is in `Configuration/halloween-witch.json`.

Iron Golem, 2026-11-03. Code in `D:\UO\golems\Iron\ShatteredLegacy` (branch `golem/Iron/P786`), image
`sl-modernuo:cc-p786` (`latest` not touched). Built as our own code from P779's sketch. The idea is from **Milva's
"Halloween Witch With Drop Items 2.0"** (`D:\UO\third-party\code\halloween-witch`, reference only, never built or
run). Milva is credited in the CHANGELOG line and here. As P779 recommended, these were not ported:
- the Shroud of the Wicked Witch: 13 in every resist, night sight, and a frog form with +5 Str and Int that never
  expires;
- the witch's broom (self repair);
- the witch house addon.

## What was built

- **The witch** (`HalloweenWitch`, `server/customizations/HalloweenWitch/`).
  - A female mage (AI_Mage) with 850-950 hits and Magery 110, plus Eval Int 110, Meditation 100, Magic Resist 110,
    Tactics and Wrestling 100.
  - Resists 50-65, damage 15-22, fame 15,000, karma -15,000, and 400-700 gold. All of these come from the table.
  - Her robe, hat, cloak and shoes are costume: they cannot be moved, so they never reach her corpse. She has no broom.
  - One saved field, her wild spot (`[SerializationGenerator(0, false)]`, D40).
- **The drop** (`OnDeath`): her corpse holds one prize drawn by weight, at `dropChancePercent` (100). The defaults are
  the Ouija board (weight 2), the torture block deed (1) and the gore rack deed (1). All three are ours, D40:
  - `WitchOuijaBoard`: a toy. Double-clicking it sends a random coloured light and a sound, at most once every 5
    seconds. It does nothing to anyone, and has none of the source's charge bookkeeping.
  - `TortureBlockDeed`/`TortureBlockAddon` and `GoreRackDeed`/`GoreRackAddon`: house decor addons, laid out as the
    source laid out its stock tiles.
- **The tokens** (`AwardTokens`): her top damager gets `tokens` (5) Festival Tokens through `FestivalTokens.Grant`.
  - A pet's or summon's master stands in (`FestivalTokens.TopDamager`).
  - Tokens are paid only in a festival season, which is the Festival Tokens rule.
  - At fame 15,000, FestivalTokens' ordinary in-season creature drop may also give that player 1 token (up to 25%).
- **Wild spots** (`HalloweenWitchSpawns`).
  - The spots are three of pinned's Trammel graveyard spawner spots (`Data/Spawns/shared/trammel/Graveyards.json`):
    Yew (722,1119), Cove (2438,1100) and Britain (1369,1475). These are the classic unguarded cemeteries, so they are
    "wild" without being remote.
  - While the Halloween season is on (`FestivalSeasons`, the same switch the Festival stall uses, which staff can force),
    one witch stands at each spot, placed with the requisition seeder's `Fit` and wandering up to 8 tiles. A spot whose
    witch died gets a new one `respawnMinutes` (30) later.
  - Out of the season, every placed witch is taken away. Corpses are never touched.
  - The check runs on every world load (so an existing world gets the witches by itself), every `checkMinutes` (5), and
    on `[HalloweenWitch sync`. It is idempotent: one witch per spot. Placed witches are tracked by serial in
    `ClusterFSeasonalState` ("halloween-witch").
- **The random encounter (P776).**
  - The engine gains one kind, `EncounterKind.Boss`: one strong creature that comes for the player (FightMode
    Closest, its combatant set to the player, homed on the spot). Its death ends the encounter, and the creature pays
    its own reward.
  - The witch's entry: id `witch`, at night, in the "halloween" season, level 40 and up, Trammel and Felucca,
    weight 2.
  - **Existing worlds:** `encounters.json` is written once with the defaults, so an existing world's file would never
    get a new built-in encounter. Instead, `EncounterTable` gained a `Supplement` event that runs whenever a table comes
    into force (start or `[Encounters reload`). The witch adds her entry there, from her own table, unless the table
    already has an encounter with the id `witch`. That lets Chase override her in `encounters.json`.
- **Staff:** `[HalloweenWitch status|reload|sync|clear]` (GameMaster), with `[ShardCommand]`.

## The table and the rules

`Configuration/halloween-witch.json` is written with the defaults on first start, read at start and by
`[HalloweenWitch reload`, and refused whole if anything in it is bad (the GoldPanningTable pattern). It holds:
- her name, title and hue;
- hits, Str, Dex, Int, damage, resists and armour;
- her six skills, fame and karma;
- gold;
- the drop chance and the drops by weight;
- the tokens;
- the spots, the wander range, the respawn and check minutes;
- the encounter (on/off, weight, minimum level, facets, and its two lines).

**Rules check:** a drop is refused if it is any of these:
- a `SpecialScroll` (power, stat cap, alacrity or transcendence: no skill or stat points);
- a weapon, armour, jewellery, clothing or a talisman (no property items or artifacts, and no robe);
- a container;
- a deed that is not a house addon deed, so a bless deed is refused while the decor deeds pass.

The defaults are a toy and two decor deeds, usable at once.

## Tests

`server/tests/Misc/HalloweenWitchVerification.cs`, five facts:

1. **The table:** the defaults validate (hits 850-950, Magery 110, the three drops, the spots, the tokens) and
   round-trip as JSON. Each of these drops is refused whole: a power scroll, a clothing bless deed, a longsword, a robe
   and a bag; so is an unknown setting. A made witch has the table's hits and Magery, and nothing of her costume can be
   looted.
2. **The season gate, wild spots:**
   - out of season and in winter, there is no witch at any spot;
   - in Halloween there is one witch at each spot, homed there, however often the check runs;
   - a killed spot's witch is not back after 29 minutes, and is back after 31;
   - when the season ends, every witch is taken away;
   - with the table off, there is none even in Halloween.
3. **The season gate, encounter:**
   - any encounter table that comes into force gets the witch's entry, once, as a night Boss in "halloween", and the
     table still validates;
   - a player qualifies at night in Halloween, but not out of season and not by day;
   - started, the encounter brings one witch who is hostile to the player;
   - with the witch's encounter off, a new table has none.
4. **The drop table:**
   - each prize owns its weight's share of the roll, and there is none past the chance;
   - a killed witch's corpse holds the drawn prize and none of her clothes;
   - each deed makes its addon.
5. **The token award:**
   - nothing out of season, and nothing with no player;
   - in Halloween, the table's 5 tokens;
   - in a real kill, the player who did 200 damage gets them (5, or 6 when FestivalTokens' own creature drop also
     rolls), and the one who did 5 gets none.

**Seen failing first** (probe `cc-P786-tools/probe.sh`: builder image `sl-uo-builder:cc-p784`, this branch's base,
with the witch folder and the encounters folder mounted):

- Against the code before the change, the test file does not compile: `HalloweenWitch` is unknown (`red-probe.txt`).
- First green run (`green-probe1.txt`): 4 of 5. The encounter fact found no witch entry, because the test host runs no
  `Configure`, so nothing had joined `EncounterTable.Supplement`. I added `HookEncounters()` (idempotent; `Configure`
  calls it, and the test does too), which gave 5 of 5 (`green-probe2.txt`).
- The witch facts together with `RandomEncounterVerification` and `RewardStoreVerification`, in one process: 46 of 46
  (`green-probe3.txt`). The witch joining every encounter table changes nothing for P776's facts.
- One mutant per fact (`red-mutants.txt`). Each fact failed on its own break:
  1. the refused-kinds check switched off;
  2. the wild spots ignore the season;
  3. the encounter has no season;
  4. the drop ignores its roll;
  5. tokens are paid out of season.

**Gated build** (`cc-P786-tools/gated-build.ps1` runs `docker/uo/build.sh -t sl-modernuo:cc-p786`, under the
`docker-build` lock, which I took and released):
- **EXIT=0**: 3,022 tests, 3,016 passed, 6 skipped, 0 failed. All 187 patches applied; this prompt adds none.
- The five witch facts and every `RandomEncounterVerification` fact are among the passes (32 listed, 0 failed, in
  `cc-P786-tools/green-gated-build.txt`). The raw log is git-ignored (`*.log`).
- **Memory:** before the first probe, Windows had only **0.8 GB free**, under the prompt's 3 GB line. The Docker VM's
  page cache was the cause. Dropping it (the memory note's privileged alpine `drop_caches`) brought it to 9.2 GB, so I
  went on without stopping. It was 11.1 GB before the gate.

## Deviations and notes for Chase

- **No in-game proof run** on the private shard: it is not in "Done means". The facts run the real placement, death,
  corpse and token code.
- **The spots are graveyards near Yew, Cove and Britain,** not remote wilderness. If they are too close to town, move
  them in the file. Grave diggers (P782) at those three cemeteries will meet her in October.
- **Her look is our own:** a green-skinned human woman in dark robes and a wizard's hat. There is no witch body art.
- **The extra creature token:** at fame 15,000 the ordinary in-season creature drop can add a token to her 5. Lower her
  fame in the file to turn that off.
- **After a restart**, a spot whose witch died before it is refilled at once: the respawn wait is not saved.
- **The art check** (`cc-P786-tools/art-check.txt`, `artcheck.py`, which reads our client's `artLegacyMUL.uop` and
  `tiledata.mul`): every tile is stock and present. That covers the Ouija board 0xFAD (a backgammon board, hued), the
  torture block 0x126B-0x1273 with the bone pile, and the rack, blood, whip, torso and rib cage.
- **Version `2026.11.03.7`.** P785's branch, not yet merged, is `.6`, as main is. The integrator may need to renumber.

## Files

- ShatteredLegacy:
  - new: `server/customizations/HalloweenWitch/` (`HalloweenWitch.cs`, `HalloweenWitchSpawns.cs`,
    `HalloweenWitchTable.cs`);
  - changed: `server/customizations/Encounters/EncounterTable.cs` (`EncounterKind.Boss`, the `Supplement` event);
  - changed: `server/customizations/Encounters/ClusterFEncounters.cs` (the Boss start and death cases; header);
  - new: `server/tests/Misc/HalloweenWitchVerification.cs`;
  - `CHANGELOG.md`, `VERSION`.
- shard-migration: this file; `notes/cc-P786-tools/` (the art check, the probe and gate scripts, red and green logs).
- `D:\UO\third-party\CODE-INTAKE.md`: the halloween-witch row's call and status now read "built (P786)". A backup of
  the file from before the edit is in this session's scratchpad.

P786 DONE
