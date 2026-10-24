# P497: review of the P232 Pkcs pin and audit flag removal

Reviewed 2026-10-23. Notes only. No code changed.

P232 commit `b2faa3e1a590f35fd3f399a007ca5adcf417a7d8` is in local `main`; the reviewed code work copy matches `main` at `579ad58f8f478280b03b8cf80f1ee9a5b3001a27`. This change concerns a NuGet package version pin, not a user PIN or an account audit log.

Read `notes/cc-P232-pkcs-pin-drop-audit-flag.md` first. No separate P232 review was found beside it. Its dependency history, Clean-target correction, and recorded red/green build results are not new findings here.

## Findings

- **risk**, `docker/uo/Dockerfile:65` (also `docker/uo/build.sh:71` and `:88`): A fully cached builder can reuse the publish layer without running NuGet restore or checking newer advisories, and the subsequent test command uses `--no-restore`; this existing build behavior leaves the restored audit gate unable to catch a newly disclosed vulnerability on an otherwise unchanged build. Add a required audit step outside the cached image build that refreshes advisory data for the resolved dependency set and fails on audit errors.

- **risk**, `docker/uo/apply-patches.sh:260` and `:264`: The P232 notes record no missing-source or existing-destination failure exercise for the new installer, and no dedicated regression for these guards was found in tracked `server/tests/`, `scripts/tests/`, or `docker/` files, leaving upstream overwrite protection untested. Add scratch-tree checks that require a nonzero final script exit for both cases and verify that a colliding destination stays unchanged, with each check seen failing before its fix.

No secret logging found in P232. The changed commands contain package versions, public advisory identifiers, and build paths, with no new credential inputs or secret output. No additional defect found in the package reference or removal of the audit severity override.

## Evidence and limits

Reviewed the P232 diff and current `docker/uo/Dockerfile`, `docker/uo/apply-patches.sh`, `docker/uo/build.sh`, and `server/patches/Directory.Build.targets`, plus the P232 `CHANGELOG.md` and `VERSION` changes. Checked pinned ModernUO's `Directory.Build.props`, `Projects/UOContent/UOContent.csproj`, and `global.json`; its checkout is `d4531cd94b739613155225c234900de9f47d2c88`.

A read-only `dotnet msbuild` evaluation of pinned UOContent, importing the owned targets file through `DirectoryBuildTargetsPath`, exited 0. It evaluated `System.Security.Cryptography.Pkcs` to the declared range `[10.0.13, )`, `NuGetAudit=true`, `NuGetAuditLevel=low`, `NuGetAuditMode=all`, `TreatWarningsAsErrors=true`, and `NoWarn=NU1603`. This checks project evaluation, not a package restore or the published DLL. The available local SDK is 10.0.201; the Dockerfile specifies 10.0.203.

No lane tests were requested, and no tests were added. Git Bash syntax checks for the two shell scripts could not start because Bash failed to create its signal pipe with Win32 error 5; neither syntax check completed. PowerShell commands ran under Windows PowerShell 5.1.26100.9711. Ran the progress reporter with work-copy path overrides and `--dry-run`; it still rewrote `tools/progress.json`, so that generated file was restored to its initially clean state. Only this notes file remains changed.

The cache finding follows from the build commands and placement of restore in the Docker layer; a cached Docker build was not reproduced in this review. P232's historical red/green results were read, not rerun. Current advisory feeds, freshly resolved packages, published binaries, and running shard state remain unverified. No Docker daemon or Haven connection was made.

P497 DONE
