# cc-P811: a small casino (slots and blackjack)

## In plain words

- **The Haven inn has a small casino now: two slot machines and a blackjack table, gold only.** They placed themselves when the world loaded, in the inn's east room, between the guest bedrooms.
- **The house keeps a little over time.** The slots pay back 94.8% of what's played (a 5.2% edge, worked out exactly). Blackjack keeps about 3%, measured over a million simulated hands. The whole shard hears about big wins, in the System's voice.
- **You can see the sink.** `[Casino status` shows gold taken in, paid out and kept, for each game, today and all time. The same line goes to `Logs/casino.log` at every save. In the proof run, 1,100 gold was played and 900 of it was kept.
- **For you:** the spot is a corridor between bedrooms, so it's a bit cramped (shot 1). If you'd like it somewhere roomier, the spots are three lines in `Configuration/casino.json`. Tell me where, or move them there and run `[Casino seed`.

## What was built

All of this is in `D:\UO\golems\Iron\ShatteredLegacy\server\customizations\Casino\`, with its facts in `server\tests\Misc\CasinoVerification.cs`.

| File | What it is |
|---|---|
| `CasinoSettings.cs` | `Configuration/casino.json`: written with the defaults on first start, and refused whole when wrong. It also works out the slot table's exact payback. |
| `CasinoLedger.cs` | The books (GenericPersistence `Casino`, versioned), the daily limit, payouts, refunds after a restart, and `Logs/casino.log` |
| `SlotMachine.cs` | The game (`SlotGame`), the item (`SlotMachine`, saved) and its window (`SlotGump`) |
| `Blackjack.cs` | The rules and the table (`BlackjackGame`), the item (`BlackjackTable`, saved, with playing cards on top) and its window (`BlackjackGump`) |
| `CasinoSeeder.cs` | Places the casino at world load, and the `[Casino status|reload|seed` command |

`CHANGELOG.md` and `VERSION` are at `2026.11.07.4`, with one Added line and one Staff line.

There are three saved types: `SlotMachine`, `BlackjackTable` and `CasinoLedger`. There is no engine change and no `.patch` file.

Credit: the idea of a weighted reel with a pay table, and of a video blackjack, came from CEO's casino games (third-party, reference only; the poster credits CEO of EasyUO / Alexandria). No code was taken. P797's Codex review notes that `CEOBlackJack.cs` and `HiLoCards.cs` carry their own terms (no copying without permission, and a fee for shard use), which is one more reason this is an independent rebuild of the behaviour, not a reuse of their code. Their power scroll, stat scroll, shroud and luck-item themes are gone.

### Slots

- **The reels:** three reels share one weighted strip: Cherry 8, Lemon 7, Bell 5, Bar 4, Seven 2 and Gem 1, out of 27.
- **The pay table:**

  | Line | Pays (times the bet) |
  |---|---|
  | Three Cherries | 8 |
  | Three Lemons | 10 |
  | Three Bells | 25 |
  | Three Bars | 40 |
  | Three Sevens | 100 |
  | Three Gems | 1,000 |
  | Exactly two cherries | 1 (the bet back) |

- **Bets:** 10, 100, 1,000 or 5,000 gold.
- **Payback is computed, not typed in.** `CasinoSettings.SlotPayback` works it out exactly from the weights and the pay table: **94.80%**. A million simulated spins through the machine's own functions gave 94.66%.
  - A table that would pay back `MaxPaybackPercent` (99%) or more is refused at load. To change the edge, change the weights or pays, and `[Casino status` shows the new figure.
- **Shard news:** a win of 100 times the bet or more (three Sevens or Gems), or any win of 25,000 gold or more, is told to the shard: *"System: <name> lines up three Gems on the slot machine in the Haven inn and wins 10,000 gold!"*

### Blackjack

- **The table's rules:**
  - an endless shoe;
  - a natural pays **6:5**;
  - the dealer **hits soft 17**;
  - a player may double on the first two cards;
  - no splitting and no insurance.
  - All of these are in config. A natural can't be set to pay more than 3:2.
- **Measured edge:** over a million hands of sound, simple play, run through the table's own rule functions, the player got back **97.07%**: the house keeps about 2.9%. With classic rules (3:2, dealer stands on soft 17) the same hands returned 98.54%, so the house rules are what keep the edge.
- **Bets:** 100, 500, 1,000 or 5,000 gold. One hand at a time per player.
- **Restarts:** a bet stays on the table from the deal until the hand ends. If the server restarts mid-hand, the bet goes back to the player's bank at the next start and is booked as never played.

### For everyone

- **Gold only.** Stakes come from the backpack first, then the bank. A win is paid into the backpack when it fits, otherwise into the bank (always the bank over 60,000).
- **Limits:**
  - each account can play up to 250,000 gold a day (`DailyWagerLimit`);
  - Young characters are refused (`AllowYoung` false);
  - the dead are refused;
  - you must be within 2 tiles.
- **No prizes but gold:** no items, power scrolls, stat scrolls, bless deeds or artifacts.

### Placement

- **The building:** the Haven inn on Trammel, where Asandos keeps the inn. I printed a floor plan from the map files: the inn is the block at 3663-3679, 2607-2617.
- **The spots:**
  - slot machines at 3670, 2608 and 3672, 2608;
  - the blackjack table at 3671, 2610, with a player standing at 3671, 2609.
- **Art:** the slot machine is the brass contraption at 0x9A96 (tiledata calls it "machine coffee"), in a gold hue; the client has no slot machine art. The table is the plain table at 0xB34, with a deck of playing cards (0xFA3) on top.
- **What I learned in the client:** that "room" is the corridor between the inn's guest bedrooms, so it works but feels cramped (shot 1). I didn't ask before placing, because a corner of the town inn fits the prompt's "fitting building". The spots are three entries in `casino.json`, so moving them is a config change plus `[Casino seed`. The old pieces would then need deleting by hand.
- **Placement runs by itself:** at every world load, `CasinoSeeder.Seed` places any machine or table missing from its spot, and does nothing when one already stands there. When `Enabled` is false, it places nothing.

### Rules check

- **Nothing grants** skill or stat points, power scrolls, bless deeds or property artifacts. Gold is the only prize.
- **All numbers are in** `casino.json`.
- **It appears on an existing world by itself,** seeded on load and idempotently.
- **No engine change.**
- **Serialization (D40):**
  - `SlotMachine` and `BlackjackTable` use the generator at version 0.
  - `CasinoLedger` writes its own version, and an unknown version throws `InvalidDataException`.

## Tests

- **Facts:** 11, in `CasinoVerification`.
- **Red:** I wrote the facts beside the code, so to see each one fail I broke the code on purpose: 32 breaks (`mutate811.py`, results in `mutants.txt`). Every fact went red at least once.
  - One break went unseen at first (`anybet`: a bet the machine doesn't take). The player in that check was also too poor to bet, so I gave the check a rich player, and the break then failed it (`anybet.log`).
  - All 11 pass on the real code (`green2.log`). The measured paybacks are in `edges.log`.
- **Gated build:** `sl-modernuo:cc-p811`, 198 patches applied, **3,230 shard tests passing, `EXIT=0`**. `latest` was not moved.

## Proof shots (TazUO, private proof shard 127.0.0.1:2596)

These are in `notes\cc-P811-shots\`. A new character went to the inn and played. Every check in `walk.log` passed.

1. `1-casino-room.jpg`: the two brass slot machines and the card table in the inn, placed by themselves at world load.
2. `2-books-before.jpg`: `[Casino status` before playing: everything at 0, with the slot payback (94.80%) and the blackjack rules.
3. `3-slot-machine.jpg` and `4-slot-after-pulls.jpg`: the slot window after ten pulls at 100 gold.
4. `5-blackjack-table.jpg`, `6-blackjack-dealt.jpg` and `7-blackjack-result.jpg`: a hand of blackjack. The dealer's 8, 5, A, 7 made 21 against the player's 13, and the house won.
5. `8-books-after.jpg`: the books after play.
   - Slots: in 1,000, out 200, kept 800.
   - Blackjack: in 100, out 0, kept 100.
   - In all, 900 gold left the world.

The script's "9 win(s)" in `walk.log` is wrong. Clearing the journal didn't clear the script's own "win:" lines, so it kept counting the same message. The books show the true result: two "two cherries" returns of 100. No big win came up in ten pulls, so the shard-news line is proven by the facts, not a shot.

## Deviations and decisions for Chase

- **The cramped spot**, above. I placed it without asking; moving it is a config change.
- **The edge:** 5.2% on slots and about 3% on blackjack. The slot table is easy to tune in config, and the server refuses any table at 99% or more. Every gold piece the house keeps leaves the world, since it is never paid to anyone.
- **Memory:** free memory was 3.7 GB before the build. I dropped the Docker VM's file cache first, which brought it to 5.1 GB.

## Tools

These are in `notes\cc-P811-tools\`:

- `run-facts.sh` and `run-facts-detailed.sh`: quick fact runs.
- `mutate811.py` and `run-mutants*.sh`: the deliberate breaks.
- `gated-build.ps1`: the gated build.
- `shots.ps1`, `Shots811.py` and the TazUO rig copied from P804's.

Both locks have been released.

P811 DONE
