# P504: Rootdeep goes into the world review

Reviewed 2026-10-23. Notes only. P188 commit `394051a` is an ancestor of local `main`; the code work copy reviewed is `579ad58f8f478280b03b8cf80f1ee9a5b3001a27`.

Read `cc-P188-cont-rootdeep-goes-in.md`, its listed server and map-delivery changes and tests, and the P425 and P430 reviews and their Codex reviews. Their findings, and P141's existing multiplayer loot-rights and Young death-routing findings, are excluded here. Paths below are relative to the code work copy unless prefixed `ModernUO-pinned/`.

## Findings

1. **risk**, `player-package/payload/app/Build-UoOverrides.ps1:782` and `player-package/payload/app/Play.ps1:333`: map preparation errors are swallowed and the client still launches using EA's map, so a character saved inside the built Burrows can log into void terrain with no visible floor or ladder, while the server uses the overlay. Require successful preparation of the shipped map before launch, report the recovery step, and test a failed map build through the launcher; include the Trammel map, statics, and index in setup validation, which currently requires only the Felucca map at `player-package/payload/app/Setup.ps1:34`.

2. **risk**, `server/tests/Regions/RootdeepWayInVerification.cs:174`: W1's walker is not marked Young and the test checks location without checking the dungeon warning or loss of Young protection, so it would still pass if entry silently stopped warning new players. Add a Young player with a test connection, assert that entry sends `YoungDungeonWarningGump`, and verify the protection change between the Old Haven approach and the Burrows landing.

## Evidence and limits

- The map failure behavior was reproduced under Windows PowerShell 5.1 by calling the unchanged override builder with the shipped map patch and an empty temporary input directory, with unrelated optional inputs pointed at missing files: it printed "Starting without it" and returned normally with a null override list. The temporary directory was removed; no client was launched. `Play.ps1:339` continues into client-launch preparation with that result. The resulting client movement problem is a source-based risk, not a reproduced player incident; this differs from P425's server-start-without-overlay finding.
- By source inspection, the normal entry warning currently exists: `OldHavenBurrowsRegion` inherits `DungeonRegion.YoungProtected == false` (`ModernUO-pinned/Projects/UOContent/Regions/DungeonRegion.cs:21`), and `BaseRegion.OnEnter` sends the Young warning (`ModernUO-pinned/Projects/UOContent/Regions/BaseRegion.cs:76`). `PlayerMobile.CheckYoungProtection` reads that region property at `ModernUO-pinned/Projects/UOContent/Mobiles/PlayerMobile.cs:4028`. Finding 2 is a missing regression test, not a claim that the warning is currently broken.
- No additional confirmed stranding spawn, excessive loot payout, or unwarned Young death defect was found beyond the earlier reviews. The fixed Vault drops and the Warren, Tangle, Dawnseam, and Gloom loot paths were inspected; live earning rates and combat balance remain unverified.
- The pristine ModernUO reference is clean at `d4531cd94b739613155225c234900de9f47d2c88`, matching the Dockerfile.
- `powershell.exe -NoProfile -ExecutionPolicy Bypass -File player-package/tests/Map-Overrides.Tests.ps1`: all seven existing facts passed. No tests were added or changed. C# fixtures were read, not run; no Docker build, shard startup, package build, real-map rebuild, save/reload test, or client walk was performed.
- The progress reporter completed against these work copies with its `progress.json` write suppressed in memory. No progress artifacts were changed. No code changes, commits, deployments, or connections to Haven were made.

P504 DONE
