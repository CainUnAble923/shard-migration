# The League storyline: The Shattered Legacy (draft 2, 2026-10-03)

Overseer draft for Chase to edit. Ours, documented on our own wiki. Source decisions: feature-queue F-24
(League build-out), Chase 2026-10-03: trials are chapters of an overarching League story, at milestone ranks, and
**the broken sword is what broke time**; recovering its shards reveals why Britannia loops.

Nothing here is built. Names, places and chapter count are proposals.

## The idea in one paragraph

Long ago the Stranger shattered Mondain's Gem of Immortality, and the world split into shards (this is UO's own
explanation for its many shards). Our addition: the blade that struck the Gem broke with it. The Gem's power was
immortality, life that does not end, and when the blade shattered, that power soaked into its pieces. Britannia did
not end; it **repeats**. Heroes who reach their limit wake again, weaker but remembering, and climb again. That is
the loop every player lives. The League of Extraordinary Citizens was founded by people who noticed. Its real purpose,
told only to those who climb its ranks, is to find the five pieces of the blade and learn whether the loop can be
mended, or should be.

## Why it fits the game

- **Loops and resets** are the story's core event, not a menu option. Reaching the level cap and starting again is
  what a "legacy" is: the character carries forward what the world forgets.
- **Loop memory** (gains faster below a previous peak) is called the **echo** in game: the shard's pull on someone
  who has walked this road before. F-12 already uses "echo multipliers"; the story names them.
- **The crest** (stone ring, broken sword) is the story's image: the ring is the empty setting where the Gem sat,
  the broken sword is the blade that struck it.
- **The League as "the guild for the guilds"**: it needs every guild because each piece of the blade is guarded by
  something only a combination of trades can reach. Multi-guild jobs (F-33) are the League gathering what it needs.

## The six chapters

**Draft 2 (Chase, 2026-10-03): the story runs all the way to Celestial.** Six chapters, every third rank from Dull
Copper, ending exactly at Celestial: the five pieces of the blade, then the ring from the crest.

**Places rule (Chase, 2026-10-03):** a chapter goes either to a **custom dungeon** (ours) or to a **vanilla dungeon
kept safe**: the trial uses quest-only spawns, items and areas there and never changes the dungeon for players who
are not on that chapter. The places below are proposals under that rule.

**Instancing is possible on our engine (overseer, checked 2026-10-03 against ModernUO `d4531cd`):** maps are defined
in `Distribution/Data/map-definitions.json` (`Projects/Server/Maps/MapLoader.cs:30-44`). Indexes 0-31, 127 and 255 are
reserved; any other index is free (the table holds 256). A visible map's client `id` and `fileIndex` must be 0-5, so a
new map can **reuse Trammel's (or Malas's) map files** while being a separate world space on the server: same tiles,
none of the other map's players, items or spawns. That is how Felucca and Trammel are two worlds. A small pool of
"trial maps" (say 8) gives each party a private copy of a dungeon, emptied and released after. Works with stock and
TazUO clients (the client just sees Trammel). To check when built: regions are per map (copy the dungeon's region
to each trial map), memory per extra map, and that recall, gates, death and logout inside a trial map send the
player back to the real map.

One trial chapter per milestone rank (every third rank from Copper). Each chapter recovers one piece of the blade
and answers one question.

| # | Rank (of 17) | Piece | Where (proposal) | The question it answers |
|---|---|---|---|---|
| 1 | Dull Copper (2) | The Pommel | under New Haven (the P36 dungeon) | Is the loop real? |
| 2 | Bronze (5) | The Grip | Despise | Who has noticed it before? |
| 3 | Verite (8) | The Crossguard | Doom (Malas) | What does the loop want? |
| 4 | Blaze (12) | The Blade | Ice Dungeon | What happens if it breaks for good? |
| 5 | Mythril (15) | The Point | Exodus (Ilshenar) | Mend it, or sunder it? |
| 6 | Celestial (17) | The Ring | custom: the Setting | What comes after the choice? |

Chapter 1 now comes early (rank 2), so a new player meets the story in their first days. Ranks in between are
promotion jobs only.

### Chapter 1: The Pommel (Dull Copper Citizen)

The Registrar sends the player to look into "a miner's complaint": the same cave-in, in the same tunnel under New
Haven, reported every few weeks for years, by miners who swear it has never happened before. Below it the player
finds a sealed chamber and a heavy pommel of black metal that is warm to the touch. Holding it, the player hears
their own voice from a loop they do not remember. The Registrar is not surprised. "You hear it too. Welcome to the
League. The real one."
- Trial: survive the repeating cave-in (a timed event that resets until solved) and find the chamber.
- Teaches: the loop is real, and the League knows.

### Chapter 2: The Grip (Bronze Citizen)

The pommel pulls toward Despise. The player follows the trail of an earlier League expedition, centuries old by
their dates, a few weeks old by their bodies, which are fresh. Their journals describe the player's own trial.
The Grip is held by the expedition's last survivor, who has looped so long inside Despise that she no longer
remembers leaving. She gives it up only if the player helps her finish her loop.
- Trial: an escort and a fight through Despise; ties to the Wisp Orb. The Grip sits in a scripted mimic, a nod to
  F-32's mimics, which can be any dungeon chest on the shard (rare chance), not only in Despise.
- Teaches: others have walked this; the League has done this before, and failed.

### Chapter 3: The Crossguard (Verite Citizen)

Doom's Gauntlet is a loop made into a dungeon: the same rooms, the same deaths, forever. The Crossguard holds it
together. The player learns that the pieces do not only cause the loop, they **feed on it**: every reset makes them
stronger. Taking the Crossguard frees Doom's dead for the player's party only; Doom
itself stays vanilla for everyone else (places rule).
- Trial: a party trial in Doom (shareable, F-24 rule).
- Teaches: the loop has a want. It keeps heroes because heroes feed it.

### Chapter 4: The Blade (Blaze Citizen)

The blade is frozen into the deepest ice, where a rival faction wants it: the **Unbound**, former League members
who decided the loop is a prison and the pieces should be destroyed even if Britannia goes with them. The player sees
what an unlooped world would look like through the Blade: a quiet, empty Britannia that ended.
- Trial: a race against the Unbound to the blade; their leader is a past League champion the Registrar knew.
- Teaches: ending the loop has a cost. The story turns from "fix it" to "choose".

### Chapter 5: The Point (Mythril Citizen)

The last piece is with Exodus, Mondain's heir, who has kept the Point since the Gem broke and has been trying to
re-forge the blade to become the Gem's new keeper. With all five pieces the player stands where the loop began.
- Trial: the Exodus encounter, re-themed as the story's end.
- The choice: **Mend** the blade or **Sunder** it. Chase 2026-10-03: the choice has **lasting effects, a title and a
  cosmetic**. It is per character and permanent (not undone by a reset).
  - **Mend (Keeper of the Loop):** the loop stays, gentler. Lasting effect: a higher top on the echo (loop memory
    regains faster after each reset). Title "Keeper", a Keeper's hue or cloak. The Registrar's people trust you.
  - **Sunder (Breaker):** the loop stays but no one holds it. Lasting effect (Chase 2026-10-03: "a few skills"):
    **three chosen skills keep a floor through every reset** (overseer default: half their peak), plus three more
    skills per loop, until all 58 are kept at full peak at loop 21 (max level 200). Title "Breaker", a cracked-steel hue. The Unbound treat you as one of theirs.
  - Chase 2026-10-03: in the end **Breakers keep every skill through a reset**, and **Keepers regain skills almost
    instantly**, so the two end even. Curves in feature-queue F-12 (post-cap loops).
  - Both are sidegrades, never a strict win. The shard also keeps a **tally** of Keepers and Breakers; the larger
    side colors seasonal events (Dispatch notices, event spawns). That is the only world-wide effect.

### Chapter 6: The Ring (Celestial Citizen)

The crest's stone ring is the empty setting where the Gem sat. With the blade mended or sundered, the setting wakes,
and something that was held back by the loop starts coming through it. This chapter is a **custom dungeon** (the
Setting): no vanilla place fits where the Gem was.
- Keepers hold the setting closed; Breakers walk through it. Same dungeon, two routes and two final bosses, so the
  choice in chapter 5 changes what chapter 6 is.
- The end is not an end: the story closes on the next loop starting, now with the character knowing why. Room for
  future chapters (an expansion) beyond Celestial if the ladder ever grows.

### Epilogue: The Unbroken (loop 21, max level 200)

Chase 2026-10-03: a "happy 20": twenty +5 scroll loops take the cap from 100 to 200 at loop 21. The Setting has 20
floors, one opened per loop from loop 2. On loop 21 the character reaches the last floor and **re-forges the crest**: the ring and the
blade made whole, in the Keeper or the Breaker version. The loop does not end for the world, but this character is no
longer bound by it. Title "the Unbroken", the crest as a wearable and as decor, and a name in the League's Hall of
Legacies. Details in feature-queue F-12 (post-cap loops).

## Decided (Chase, 2026-10-03)

1. Runs all the way to Celestial: six chapters (above).
2. **Keep the UO lore link** (the Stranger, the Gem of Immortality, Exodus).
3. **Keep the Unbound** as they are.
4. **The final choice has lasting effects plus a title and cosmetic** (above; effects are overseer suggestions).
5. **Chapters are either solo or party.** Each runs in a private trial map (instancing, above).
6. **Custom dungeons where appropriate.** Overseer: chapter 1 is our New Haven dungeon and chapter 6 is custom;
   chapters 2 to 5 use private copies of the vanilla dungeons.

## Still open

- The two lasting effects: react to Keeper (higher echo top) and Breaker (one skill keeps a floor through resets).
- The tally's seasonal effect: keep or drop.
