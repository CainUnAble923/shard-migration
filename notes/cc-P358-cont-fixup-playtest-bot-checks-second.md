# cc-P358: fix-up for P224 (play-test bot checks, second half): merge main in again

2026-10-21, the Silver Golem (Opus). Prompt: `D:\UO\cc-prompts\claimed\Silver\cc-P358-cont-fixup-playtest-bot-checks-second.md`.

## Headlines

- **P224 is merged with main in both repos, on branch `golem/Silver/P358`.** The hand-off says not to switch branches,
  and P358 already sits on main's tip (ShatteredLegacy `48191cd`, docs `815f989`). So I merged `golem/Silver/P224` into
  P358 (`git merge --no-commit --no-ff`) instead of merging main into P224. The result is the same tree. The Golem
  commits it.
- **Two files conflicted, both in ShatteredLegacy:** `tools/playtest-bot/uobot/client.py` and `uobot/run.py`. Main's
  P215 (each Golem gets its own Admin and Player accounts, plus `golemcheck`) and P224 both changed the bot's targeting.
  I kept both. Nothing contradicted.
- **The docs repo merged cleanly** (P224's notes, bot run `testing/bot-runs/2026-10-21-0601/`, `docs/bug-list.md`,
  `testing/playtest-steps.json`).
- **Tests are green:** all 50 `tools\playtest-bot` unit tests pass, including P215's `test_golemcheck` and P224's
  safety tests, and every `uobot` module compiles. No file under `server\` or `docker\uo\` changed, so I did not build
  the image.

## The conflicts and how I resolved them

The two sides took different routes to "talk to a test shard":

- **Main (P215):** `Client(..., test_target=(host, port))` for the Golem login checks. That path uses
  `check_test_target` and `check_test_relay`, dials the host it was given, and imported `HOST`, `PORT` and the checks
  from `safety` by name.
- **P224:** `safety.configure("scratch"|"test")` for the whole run (`run.py --target`). Every call goes through
  `safety.` because `configure()` changes module globals. The relay's address is never dialled: the bot reconnects to
  `safety.HOST:safety.PORT`.

`client.py`, hunk by hunk:

1. **Imports:** only `from . import safety`. Importing `HOST` and `PORT` by name would freeze the scratch values and
   quietly break `--target test`. All of P215's calls now go through `safety.`.
2. **State in `__init__`:** both sets of lines are kept: `self.trades` (P215) and `self.context_menus` and
   `self.arrows` (P224).
3. **`_connect`:** with `test_target` it calls `safety.check_test_target`, otherwise `safety.check_target`.
4. **First connection:** `host0, port0 = self.test_target or (safety.HOST, safety.PORT)`.
5. **Relay check:** with `test_target` it calls `safety.check_test_relay(ip, port, host0, port0)`, otherwise
   `safety.check_relay(ip, port)`.
6. **Relay log line:** P215's line on the `test_target` path. On the run's path, P224's line plus its NOTE when the
   relay advertises an address other than loopback.
7. **Game reconnect:** this line merged without a conflict, but it was wrong for P215. It now dials `(host, port)` with
   `test_target` (the dialled host, which `check_test_relay` returns) and `(safety.HOST, safety.PORT)` otherwise. With
   P224's line alone, golemcheck would have reconnected to 127.0.0.1 instead of the test shard it logged in to.

`run.py`: both arguments are kept, `--no-golem` (P215) and `--target` (P224). They are independent.

`safety.py` (auto-merged) now defines `LIVE_PORT = 2593` twice: once in P224's block and once in P215's block. The
value is the same, so I left both.

## Checks run

- `python -m compileall -q uobot`: clean.
- `python -m unittest discover -s tests`: **50 tests, OK**.
- A self-check in the session ran both targets (`scratch`, `test`). In each, a run client refuses 127.0.0.1:2593 and
  192.168.1.58:2594, and a golemcheck client (`test_target=("chases-tower", 2594)`) refuses port 2593. The run relay
  returns the advertised address, which is logged and not dialled. `check_test_relay` returns the dialled host.
- I did not rerun the bot against a live test shard. The merge changes no check logic, only how the two targeting
  paths sit side by side.

P358 DONE
