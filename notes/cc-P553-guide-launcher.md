# P553: launcher and updater player guide

October 24, 2026. Documentation only. Draft: [Launcher and updater help](wiki-drafts/launcher-help.md).

## Delivered

The short player page covers first-run discovery and EA installation, SmartScreen for the unsigned package, update prompts and preserved settings, P411's art progress bar and fallback, stuck-Play recovery, and log locations. Plain American English, with no em dashes. No code changed.

The outer lane instructions name `cc-P553-guide-launcher-troubleshooting.md`; the embedded task also requests this file. Both notes are supplied, with the outer file linking here.

## Sources checked

Read both work-copy AGENTS.md files and the direction and task documents. Code paths below are relative to the ShatteredLegacy work copy.

- `player-package/payload/README.txt`: first-run instructions, approximate download and space requirements, unsigned-package warnings, update behavior, test-shard notice, recovery shortcut, and logs.
- `player-package/payload/app/Setup.ps1`: automatic continuation after EA patching, warning against EA's Play button, space/connection recovery, and existing-install update handling.
- `player-package/payload/app/Play.ps1`: update offer and new window, transcript naming, setup and connection checks, and skip-art behavior.
- `player-package/payload/app/Overrides-Launch.ps1`: step-specific progress/counts, default 60-second rebuild wait, previous-art/first-install fallback, and background preparation.
- `player-package/payload/app/Update.ps1`: preservation of player settings and profiles, close-game wait, preparation before handoff to Play, and root-level `update-log.txt`.
- `player-package/payload/Play Shattered Legacy.bat` and `player-package/payload/app/Play-Skip-Art.bat`: actual shortcut entry points and the skip-art switch.
- `player-package/payload/app/Build-UoOverrides.ps1`: rebuild trace naming and retention.
- [P411 implementation notes](cc-P411-launcher-always-starts.md) and [P411 review](cc-P411-launcher-always-starts-codex-review.md).
- [P543 restoration notes](cc-P543-cont-fixup-launcher-always-starts.md) and [P549 review](cc-P549-review-launcher-always-starts.md).

## Accuracy and limits

The page avoids repeating P411's absolute claim that the game always starts within a minute. Its review identified synchronous freshness checks outside the timer and a second rebuild wait during updater handoff. P549 confirmed additional swap delays and other fallback/progress risks. The page describes the intended rebuild fallback, explicitly distinguishes it from total launch time, and offers the shipped shortcut if preparation stays stuck. It tells players to close a stuck launcher before retrying rather than encouraging simultaneous Play calls; P549 found a concurrent-builder race.

The download size and free-space figures are attributed estimates from the README, not new measurements. A per-step count is not presented as overall completion. The shortcut skips art only, and declining an update on that attempt avoids the updater's separate art preparation path.

Unverified: the published package version, actual SmartScreen appearance on a player's PC, first-run downloads, the work PC's hang, fallback timing in a real game session, and live connectivity. No Haven connection, download, game launch, package build, deployment, or account action was performed.

## Validation

- No lane tests requested. No tests added or run for this prose-only task.
- Reviewed the full draft against the local sources above and checked American English and absence of em dashes.
- Ran `tools/progress.py --dry-run` with `SL_SHARD` and `SL_MIGRATE` pointing at these work copies: exit 0. The tool writes `tools/progress.json` even in dry-run mode; restored its pre-run bytes, leaving no generated change. The first capture wrapper hit a console encoding error after the tool returned 0; restoration completed in `finally`, then the corrected capture returned 0 too. Progress figures are unrelated to this guide and are not quoted here.
- Final review: only the guide and the two requested notes files are new; the code work copy is clean. All three files are below 5 MB, with no em dashes or trailing whitespace. `git diff --check` reported no tracked whitespace issues. No stop request was present.

P553 DONE
