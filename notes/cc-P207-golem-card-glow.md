# cc-P207: a pulsing glow behind each Golem's portrait (web console)

Gold Golem, 2026-10-20. From Chase's request: "A pulsing glow behind golem icons on console would help show if they
are working or not. The eye brightness is too small to tell." I read P186's notes (cards, portraits) and P187's (web
console parity, already in main) first. No server or shard code changed, so there was no Docker build, test shard or
lock.

## Headlines

- **Every Golem card's portrait now glows by state**, in the Golem's own metal: Iron grey-blue, Bronze, Gold, Copper,
  Silver, Stone, plus Shadow Iron, Agapite, Verite and Valorite, all tuned for the dark card background.
  - **Working** (RUNNING, last activity under 10 minutes): a steady pulse on a 2 s cycle, swelling to a 20 px halo.
  - **Running but quiet** (10 minutes or more since the last activity, before the stall email): the same color, a
    4.5 s cycle, about half as bright.
  - **Waiting** (IDLE, RESTING, WAITING, PAUSED: resting, back-off, outside hours, waiting for a model, pace): a faint
    static ring, no pulse.
  - **Needs you** (NEEDS YOU, STOPPED, a needs-you reason, or a stall: RUNNING with no activity for settings.json
    `stallMinutes`, 45 here, the same threshold as golem.ps1's stall email): a fast amber ring and halo, 0.9 s.
  - **Off or offline** (OFF, DISABLED, UNKNOWN, disabled in golems.json, or a remote Golem whose agent has not polled
    in the last 3 minutes): no glow, and the portrait is faded (50% opacity, part greyscale).
- **The eyes are unchanged.** The glow is extra: the stand-in figure and its eyes are not touched.
- **Reduced motion:** under `prefers-reduced-motion: reduce` nothing animates. Each state keeps a static ring or halo
  at about its mid strength, so the state still reads.
- **Legend:** a small "?" by the Golems heading. Its tooltip (hover) is the whole legend in one line; tapping it
  shows one line with five live swatches: Working, Quiet 10+ min, Waiting, Needs you, Off or offline. Each portrait
  also has a tooltip naming its state ("Copper: Needs you").
- **Phone width:** checked at 390 px in headless Edge. The glow is a box-shadow, so it never adds width. No sideways
  scroll, with or without the legend open.

## How the state is worked out

Where: the server, not the page. `panels.glow_state(card, status, now, stall_minutes)` is a pure function.
`server.Console.golem_cards` calls it for every card and sets `card.glow`, as it already refreshes each card's remote
status, readiness and portrait address.
- **The card's state:** a local Golem's comes from the status document; a remote Golem's from the status its agent
  posted.
- **Last activity:** that Golem's own status file, `lastActivityUtc` (written by the Activity hooks; golem.ps1's stall
  check reads the same field), else `startedAt`. For a local Golem the file is `status-<name>.json` under the Golem
  root; for a remote one it is its posted `remote\<name>\status.json`.
- **Stall limit:** `stallMinutes` from the Golem root's `settings.json`.
- **Clock:** the console's own `clock`, so tests can pin it.

The page (`app.js`) only applies the result: `portraitNode` wraps `img.portrait` in a
`span.portrait-glow glow-<state> metal-<name>`. The CSS is one self-contained block after `img.portrait` in `app.css`.

Why there: the Golem scripts in `D:\UO\golem` (Get-GolemCards) are not in either repo, so the card could not carry
the last activity from there. The web console already reads each Golem's status and remote files, so the rule sits
with it and is unit tested in Python.

Choices I made:
- A running Golem with no activity time and no start time shows **working**: there is nothing to judge by, and
  golem.ps1 does not call that stalled either.
- UNKNOWN (a remote Golem that has never posted) shows **off**.
- A needs-you reason on the card turns any running state to **needs**.

## Files

`D:\ShatteredLegacy`:

| File | Change |
| --- | --- |
| `web-console/panels.py` | `QUIET_MINUTES`, `STALL_MINUTES`, `_epoch`, `glow_state` (and `calendar`, `time` imports). |
| `web-console/server.py` | `golem_cards`: reads `stallMinutes`, a local Golem's `status-<name>.json`, and sets `c["glow"]`. |
| `web-console/static/app.js` | `GLOW_WORDS`, `portraitNode` (used by `golemCard` and `mergeCard`); the "?" toggle at start. |
| `web-console/static/app.css` | The cc-P207 block: metal colors, three keyframes, five state classes, reduced motion, legend. |
| `web-console/static/index.html` | The "?" button and the one-line legend in the Golems card. |
| `web-console/tests/test_golem_glow.py` (new) | Below. |
| `web-console/tests/fixtures/golem-status/status-{Iron,Gold,Bronze}.json` (new) | The real status files of 2026-10-20 cut to the fields the glow reads (no away, mail, plan or pace detail). Bronze's real file is on the game PC, so its fixture is the same schema, RESTING. |
| `CHANGELOG.md`, `VERSION` | 2026.10.20.17, one Staff line. |

`D:\UO\shard-migration`: these notes and `notes/cc-P207-glow/golem-tab-phone.png`.

The running copy of the console (`D:\UO\web-console`, outside git) is not updated by this prompt. The glow reaches
Chase's phone with the console's next install from the repo (`web-console\Install-WebConsole.ps1`).

## Tests

`python -I -m unittest discover -s tests` in `web-console`: **76 tests, OK (1 skipped, the same skip as before;
68 before this prompt)**.

`tests/test_golem_glow.py`, 8 tests:
- **GlowState: the real status files.** Gold's (RUNNING) is working 2 minutes after its last activity, quiet at 15
  and needs at 46. Iron's (OFF, disabled) is off. Bronze's (RESTING) is waiting.
- **GlowState: every state maps to its glow class:** RUNNING, IDLE, RESTING, WAITING, PAUSED, NEEDS YOU, STOPPED, OFF,
  DISABLED, UNKNOWN, and empty.
- **GlowState: what overrides the state:** a needs-you reason, disabled, a remote agent offline or online.
- **GlowState: the edges:** 9 and 11 minutes, 44 and 45, a `stall_minutes` of 60, the `startedAt` fallback, no
  times, a bad time.
- **GlowCards:** the server sets each card's glow from its own status file (Iron local working, Bronze waiting, Gold
  remote quiet from its posted status, Silver disabled off). `stallMinutes` 12 in settings.json makes Gold's 15 quiet
  minutes needs-you. Gold's agent gone makes it off.
- **PhoneGlow** (headless Edge, 390 x 844, through the tailnet listener as the sidecar passes it): five Golems in the
  five states with the real portraits.
  - Each has its glow and metal class and the right animation (glow-pulse, glow-soft, none, glow-alarm, none).
  - Waiting has a static ring; off has no shadow and a faded image; the tooltip says "Copper: Needs you".
  - The legend is hidden until "?", then lists the five states with aria-expanded true. No sideways scroll.
  - With `prefers-reduced-motion: reduce` emulated, nothing animates and every state but off keeps its shadow.

Screenshot (from that test, `GLOW_SCREENSHOT=...`): `notes/cc-P207-glow/golem-tab-phone.png`, at phone width with the
legend open. It shows Iron working (blue-grey pulse), Bronze waiting (faint bronze ring) and Gold quiet (dim gold).
Copper (needs you) and Silver (off) are further down the same page; the test checks them.

Not done (the prompt leaves it for later): the same glow on the Shard Console's (PowerShell) Golem tab.

P207 DONE
