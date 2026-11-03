#!/usr/bin/env bash
# cc-P780 probe (P763's, cut down): runs the tests matching $1 in the builder image of this branch's base (P776) with the
# hunt sources and tests mounted over its copies. PROBE_MODE=red mounts the new test file alone (the code before the
# change); PROBE_MODE=green (default) mounts the change too; SRC=<dir> mounts another customizations copy (a mutant).
# UOContent is built, then the test project, and the run uses that build (dotnet test alone reused a stale UOContent.dll).
set -u
FILTER="$1"
IMAGE="${2:-sl-uo-builder:cc-P776}"
MODE="${PROBE_MODE:-green}"
CODE="D:/UO/golems/Iron/ShatteredLegacy/server"
SRC="${SRC:-$CODE/customizations}"
UC=/build/modernuo/Projects/UOContent
UT=/build/modernuo/Projects/UOContent.Tests/Tests
M=(-v "$CODE/tests/Misc/LeagueHuntsVerification.cs:$UT/Misc/LeagueHuntsVerification.cs")
if [ "$MODE" = green ]; then
  M+=(-v "$SRC/Requisitions:$UC/Requisitions")
  M+=(-v "$SRC/ClusterFLeagueBestiary.cs:$UC/Misc/ClusterFLeagueBestiary.cs")
fi
MSYS_NO_PATHCONV=1 docker run --rm --network=none --security-opt seccomp=unconfined "${M[@]}" \
  "$IMAGE" bash -c "cd /build/modernuo && dotnet build Projects/UOContent/UOContent.csproj -c Release --no-restore 2>&1 | grep -E ' error ' | sort -u | head -40 ; dotnet build Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore 2>&1 | grep -E ' error |Build succeeded|Error\(s\)' | sort -u | head -40 ; dotnet test --no-build Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore --filter '$FILTER' --logger 'console;verbosity=normal' 2>&1 | grep -v warning"
