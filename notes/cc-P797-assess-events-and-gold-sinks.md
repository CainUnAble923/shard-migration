# cc-P797: assess events, minigames and gold sinks

## In plain words

- **Of the nine downloads, none should come in as written.** Three are worth rebuilding as our own, two are ideas for later, and four should be skipped. Two would break the rules as they stand: the egg hunt and one set of slot machines hand out power scrolls.
- **The quickest win is a staff-run egg hunt.** A GM starts it, every player gets an arrow to a hidden egg, and the finder wins Festival Tokens. It would sit in the Staff Hub's Events tab.
- **The best gold sink here is a small casino:** a slot machine and blackjack that pay back a little less than they take, gold only, with shard-wide jackpot news. It's a bigger build than the goal stone P791 suggested. The two do different jobs and could live side by side.
- **A landmine maze makes a good staff event too:** a hidden minefield that players learn by dying in it, first three through win.
- **For you:** pick which to queue. The casino needs your yes first, because gambling is a theme choice. Nothing was built or changed in the game.

## Ranked list

| Rank | Item | Recommendation | Rough size | Why |
|---|---|---|---|---|
| 1 | **World egg hunt** | **Rebuild as ours**, in the Staff Hub, Festival Token prize | about 150 lines, facts | Tiny, fits P760's tokens and the Events tab. Its power scroll prize must go. |
| 2 | **CEO casino games** | **Rebuild as ours**: one slot and blackjack, gold only | about 1,000 lines, 2-3 saved types | A repeatable sink for rich players, and fun. The original is 11,135 lines with banned prizes. |
| 3 | **Landmine maze** | **Rebuild as ours**, as a staff event | about 200 lines, 1-2 saved types | An easy, original event. As written it would not compile. |
| 4 | **Group dungeon system** | **Idea only**, for League dives | none now | Dives wait on other work, and `TutorialCopies` is a better pattern. |
| 5 | **Chicken fighting** | **Idea only** | none now | Fun, but it takes no house cut and its author lists crash bugs. A later room in the casino. |
| 6 | **Town crier advanced** | **Skip** | none | Stock's town crier and our bulletin cover it. |
| 7 | **Horde spawner** | **Skip** | none | Encounters and surges cover it, and it robs player corpses. |
| 8 | **Gambling NPCs** | **Skip** | none | An older copy of the same casino code. |
| 9 | **Snipe hunt** | **Skip** | none | An annoyance by design, with nothing to win. |

## 1. Each item

All nine: `SOURCE.txt` states no license terms of its own, so each is community work: credit the author, ship only inside the player package or the private repo, do not repost. The casino's poster gives all credit to CEO of EasyUO / Alexandria. None ships new art. "Lines" are the `.cs` files, without `_zips`; "Ser" is hand-written `Serialize` overrides. None needs a core edit except the group dungeon.

### World egg hunt (Bittiez)

- **What it does:** a Seer types `[StartEggHunt`. An egg appears at their feet, the shard is told, and every 20 seconds each player on that map gets an arrow on the ground pointing to it. The first to double-click wins one of four random prizes.
- **Size:** 1 file, 191 lines, 2 Ser.
- **Art:** stock. Egg item 0x1ECD, which tiledata calls "light", so the look needs a check; arrows 0x206A-0x2071, tiledata "cursor".
- **Problems:** a prize is a **power scroll** of 95-120, against the rules. The range check has no `return`, so anyone can claim the egg from any distance. The arrows are real items laid at every player's feet on a timer.
- **Fit:** Staff Hub's Events tab (`ClusterFSurge`), Festival Tokens (`FestivalTokens.Grant`), and our quest arrow (`TutorialCoreTrials.Point`, or the `QuestArrow` other systems use).

### Snipe hunt (Hammerhand)

- **What it does:** two creatures, both named "A Snipe", with random bodies of ordinary animals. The author says they are "designed to annoy players". Tamable at 110, must be beaten down first, 350-500 hits, up to 95 physical resist, Fame 0, no loot.
- **Size:** 2 files, 136 lines, 2 Ser. Art: stock bodies.
- **Fit:** none. Staff could already fake this with a surge.

### Landmine maze (ExX)

- **What it does:** invisible tiles that kill any player who steps on them, with a blast. Staff lay them out in an unused dungeon. Players carry a Maze Token that must survive to the end, and the first three through win. It leaves the region, the no-looting rule, healers and prizes to staff.
- **Size:** 4 files, 174 lines, 3 Ser.
- **Art:** tile 1310 (stone pavers, invisible), token 0x3679 (no name in tiledata, needs a look), blast effect 0x36CB. Nothing new.
- **Problems:** **it cannot compile as written**: the constructor is `Landmine` in class `LandMine`. Mines have to be placed one at a time by hand. A dead player's loot depends on a separate region.
- **Fit:** the Staff Hub's surge has a no-loot zone already, and tokens fit as a prize. No overlap with anything we have.

### Chicken fighting (dragon slayer2)

- **What it does:** a control stone in an arena. Players each pay a bet and get a chicken, the chickens fight, and the winner's owner gets the whole pot as a bank check.
- **Size:** 2 files, 534 lines, 2 Ser. Requirements say RunUO. Art: stock chicken body 0xD0.
- **Problems:** **no house cut, so it moves gold and sinks none.** The author lists server crashes when one person bets, or when a GM removes a chicken. The one-bet-per-account lock sits on an account tag.
- **Fit:** an arena game, no skill involved. The name would need changing ("CockFighting" in the code).

### CEO casino games (Ixtabay; CEO's code)

- **What it does:** slot machines with 14 or more themes, progressive linked jackpots, a bonus round, a top-ten board and staff stats; a video blackjack; and Hi-Lo cards. The machines have a credit and "ATM" from the bank. Payback is settable, from Loose (96-98%) to Extremely Tight (85-88%).
- **Size:** 9 files, 11,135 lines, 10 Ser. `turboslot.cs` alone is 5,535 lines.
- **Art:** stock items only: machine 3804, blackjack 4465, Hi-Lo 4479, and item art in the gumps. Nothing new.
- **Problems:**
  - **Banned prizes:** the `PowerScrolls` and `StatScrolls` themes pay power scrolls and stat cap scrolls. `GruesomeGambling` pays a Hooded Shroud of Shadows; `LadyLuck` gives luck items.
  - **It can make gold.** Its own notes warn that Normal and Loose machines can be gold farms, and that the blackjack can be "a gold mine instead of a gold sink".
  - It was written for RunUO 2.0 and has an XmlSpawner switch.
- **Fit:** no casino, gambling or slot machine on the shard. On gold sinks, a correction: **P791 said the shard has none, and its Codex review was right to object.** Gold does leave the game in nine of our files: guild purchases (`GuildResources`), Miners' Compact restoration, bulk orders, vet resurrection, initiation and more. But those are fixed costs tied to a job. What's missing is a sink a rich player will feed by choice, again and again. Nothing here measured how much gold is about.

### Gambling NPCs (dragon slayer2)

- **What it does:** a Gambler NPC who plays blackjack and poker by speech and gump, a miner-theme slot, a simpler slot machine, casino tokens and a tarot deck.
- **Size:** 11 files, 7,828 lines, 7 Ser.
- **Overlap:** `CEOBlackJack.cs` and `HiLoCards.cs` are almost the same as the CEO pack's (28 and 4 diff lines). The rest is older, simpler work. It offers nothing the CEO pack doesn't, and the Gambler's own game is the worst of the three to rebuild.

### Group dungeon system (Crowthelas; -The Jedi-, Dpayne2841)

- **What it does:** instanced-style dungeons. A stone makes a square region, and a teleporter lets in one party at a time, by party size and skill limits, with or without pets. Dead stay dead, it resets when empty, wipes send everyone out with blessed corpses, and a clear gives 10 minutes to leave. Doors with one-use keys.
- **Size:** 4 files, 873 lines, 4 Ser, plus a readme. **One core edit:** `PlayerMobile.OnLogin`. Beta, by its own name. Art: stock.
- **Fit:** F-24's dungeon dives, which wait on the New Haven dungeon research. It's only one party per dungeon. `TutorialCopies` already runs 16 reusable copies, keeps a party together, seeds them and frees them, which is a closer model for us.

### Horde spawner (RedBeard)

- **What it does:** a hidden band of ratmen, orcs or brigands waits near a road or in the woods, ambushes passers-by, **loots corpses into a treasure bag**, and hides again.
- **Size:** 4 files, 1,828 lines, 14 Ser. Art: stock bodies. Each member has 250-350 hits and rich loot packs.
- **Fit:** covered twice. `ClusterFEncounters` (P776) does random ambushes with a careful never-do list, and Staff Hub surges do staff-run raids. Robbing a player's corpse would break the spirit of that list.

### Town crier advanced (Shazzy)

- **What it does:** criers that read lines from `Data/news.txt`, set by a staff gump with speed and random order, and a stone that controls them all.
- **Size:** 4 files, 971 lines, 3 Ser. Art: stock.
- **Fit:** pinned's `TownCrier` has global and per-crier news with a gump, and our `ClusterFBulletin` does login news. The file-based list adds little, and writes to the server's `Data` folder.

## 2. Rules check

| Item | Skill or stat points | Power scrolls, bless deeds, property artifacts | Usable now | Mostly helpful |
|---|---|---|---|---|
| Egg hunt | None | **FAIL as written: power scrolls.** Fine with tokens. | Yes | Yes |
| Snipe | None | None | Yes | No, by design |
| Landmine maze | None | None. Staff set the prizes. | Yes, once rebuilt | Yes, as an opt-in event |
| Chicken fighting | None | None | Yes | Mixed: crash bugs |
| CEO casino | **FAIL as written: stat cap scrolls** | **FAIL as written: power scrolls, a Hooded Shroud, luck items.** Fine with those themes cut. | Yes | Yes, gold only |
| Gambling NPCs | None | None found | Yes | Adds nothing |
| Group dungeon | None | None | No: waits on dives | Later |
| Horde | None | None found | Yes | No: robs corpses |
| Town crier | None | None | Yes | Adds little |

## 3. Recommendations and prompt sketches

**1. Egg hunt (rebuild).** Sketch: "Add an Egg Hunt to the Staff Hub's Events tab: a GM places a hidden egg on a map, players online get a quest arrow, the first to reach and double-click it wins Festival Tokens (`FestivalTokens.Grant`, in season) or a GM-named prize, with a shard-wide line; a time limit removes it; a restart removes it." About 150 lines and facts. The egg's art needs a look.

**2. Casino (rebuild, after Chase's yes).** Sketch: "A small casino: one slot machine and one blackjack table, gold only, payback fixed in settings below 100% (start at 90% for slots, and rules that keep the house edge at blackjack), a per-play and per-day limit, jackpot news and a top-ten board; staff place them; facts simulate many plays and prove the take is within a set band." About 1,000 lines. Our own code, using the CEO pack's odds tables as the guide. The simulation fact matters most, as the original warns it can pay out more than it takes. At 90%, every 100 gold played removes about 10. **Chase's calls:** is gambling on theme, and where does it stand? A sink's size also depends on how much players play, which we can't know beforehand. **It doesn't replace P791's goal stone:** the stone is a one-off shared goal, this is a steady personal drain.

**3. Landmine maze (rebuild).** Sketch: "A staff event: a `[MineField` tool lays hidden mines over a marked area from a seed, leaving one safe path; players get a token on entry, and a finish tile checks it; a no-loot zone covers the area as a surge's does; first three win; `[MineField clear` removes it all." About 200 lines, 1-2 saved types and facts. Young characters and the isle stay out.

**4. Group dungeon (idea only).** When F-24's dives come up, take its rules: party-only entry, wipe sends you out with your corpse, a clear gives 10 minutes to leave. Build on the `TutorialCopies` pattern, not a stone.

**5. Chicken fighting (idea only).** If the casino does well, a betting pit could join it: a house cut, a rename, and chicken lizards in the ring.

**6-9. Town crier, Horde, Gambling NPCs, Snipe (skip).** Reasons in the table.

## How this was checked

- Read every small pack in full, and the key parts of the large ones: the header notes, prize code and payback of `turboslot.cs`, gold handling in the blackjack and Hi-Lo, `gambler.cs`, the group dungeon's readme and region, and `HordeSystem.cs`. Searched all nine for scrolls, bless deeds and artifacts.
- Read our side in `D:\UO\golems\Iron\ShatteredLegacy`: `FestivalStore.cs`, `ClusterFSeasonalSwitch.cs`, `ClusterFEncounters.cs`, `TutorialCopies.cs`, `ClusterFBulletin.cs`, the list of files that take gold, and pinned's `TownCrier.cs`. Also notes for P230, P760, P765, P776 and P791 with its Codex review, and `docs\feature-queue.md`.
- Art names read from the client copy's tiledata.

**Not verified.** Nothing was built or run, from `D:\UO\third-party` or anywhere else. No art was seen in a client. Rebuild sizes are my estimates. I did not measure the economy, or work out the real payback of any machine; the percentages are the pack's own.

## Other

- **`D:\UO\third-party\CODE-INTAKE.md`:** none of the nine had a row, so I added nine, marked `assess (P797)`. Backup: `CODE-INTAKE.md.bak-20261105-p797`.
- **P791's goal stone** isn't built or queued as far as I could find. It remains a good small companion to the casino.
- **Follow-ups:** none queued. Chase picks.

P797 DONE
