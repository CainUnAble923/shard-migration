#!/usr/bin/env bash
# cc-P763 probe (P761's, cut down): runs the tests matching $1 in a builder image (default P761's, built from this
# branch's base) with the loot box sources and tests mounted over its copies. PROBE_MODE=red mounts the new test file alone
# (the code before the change); PROBE_MODE=green (default) mounts the change too; PROBE_MODE=base mounts nothing. Usage: probe.sh <filter> [image].
# dotnet test alone reused the image's UOContent.dll (its CoreCompile skipped), and building the test project skipped it too: UOContent is built, then the test project, and the run uses that build.
# The patches (Fishing.cs, SetToDecorativeGump.cs) are not in a probe: only the gated build applies them.
set -u
FILTER="$1"
IMAGE="${2:-sl-uo-builder:cc-P761}"
MODE="${PROBE_MODE:-green}"
CODE="D:/UO/golems/Iron/ShatteredLegacy/server"
SRC="${SRC:-$CODE/customizations}"
UC=/build/modernuo/Projects/UOContent
UT=/build/modernuo/Projects/UOContent.Tests/Tests
M=()
if [ "$MODE" != base ]; then
  M+=(-v "$CODE/tests/Misc/LootBoxDiversityVerification.cs:$UT/Misc/LootBoxDiversityVerification.cs")
fi
if [ "$MODE" = green ]; then
  M+=(-v "$SRC/LootBoxes:$UC/LootBoxes")
  for f in ClusterFSeasonalSwitch.cs ClusterFGuildPromotion.cs GuildContractLedgerGump.cs; do
    M+=(-v "$SRC/$f:$UC/Misc/$f")
  done
  M+=(-v "$CODE/migrations/Server.Items.LootBox.v0.json:$UC/Migrations/Server.Items.LootBox.v0.json")
  for f in LootBoxFanfareVerification LootBoxFlyingLootVerification DeathHooksVerification NotedBySystemVerification NotedFixupsVerification; do
    M+=(-v "$CODE/tests/Misc/$f.cs:$UT/Misc/$f.cs")
  done
fi
MSYS_NO_PATHCONV=1 docker run --rm --network=none --security-opt seccomp=unconfined "${M[@]}" \
  "$IMAGE" bash -c "cd /build/modernuo && dotnet build Projects/UOContent/UOContent.csproj -c Release --no-restore 2>&1 | grep -E ' error ' | sort -u ; dotnet build Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore 2>&1 | grep -E ' error |Build succeeded|Error\(s\)' | sort -u ; dotnet test --no-build Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore --filter '$FILTER' --logger 'console;verbosity=normal' 2>&1 | grep -v warning"
