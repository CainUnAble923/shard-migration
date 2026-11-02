#!/usr/bin/env bash
# cc-P776 probe (P763's and P773's, cut down): runs the facts matching $1 in a builder image (default P774's, built from
# this branch's base) with the encounter facts, and in green mode the encounter code, mounted over its copies.
#   PROBE_MODE=red    the new facts alone, over the code before the change
#   PROBE_MODE=green  (default) the facts and server/customizations/Encounters (or $SRC776, a mutant's copy)
# UOContent is built, then the tests, then the facts run with --no-build (memory: probe-env-mode-and-stale-uocontent).
# A failed build stops the run, and the test runner's exit code is the probe's (P774's review finding).
# Usage: probe776.sh <filter> [image]
set -u
FILTER="$1"
IMAGE="${2:-sl-uo-builder:cc-P774}"
MODE="${PROBE_MODE:-green}"
CODE="D:/UO/golems/Iron/ShatteredLegacy/server"
SRC="${SRC776:-$CODE/customizations/Encounters}"
UC=/build/modernuo/Projects/UOContent
UT=/build/modernuo/Projects/UOContent.Tests/Tests
M=(-v "$CODE/tests/Misc/RandomEncounterVerification.cs:$UT/Misc/RandomEncounterVerification.cs")
if [ "$MODE" = green ]; then
  M+=(-v "$SRC:$UC/Encounters")
fi
MSYS_NO_PATHCONV=1 docker run --rm --network=none --security-opt seccomp=unconfined -e MODE= "${M[@]}" \
  "$IMAGE" bash -c "cd /build/modernuo && { dotnet build Projects/UOContent/UOContent.csproj -c Release --no-restore -v q > /tmp/b1.txt 2>&1 || { grep ' error ' /tmp/b1.txt | sort -u; echo BUILD1_FAILED; exit 2; }; } && { dotnet build Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore -v q > /tmp/b2.txt 2>&1 || { grep ' error ' /tmp/b2.txt | sort -u; echo BUILD2_FAILED; exit 3; }; } && { dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-build --filter '$FILTER' --logger 'console;verbosity=normal' > /tmp/t.txt 2>&1; rc=\$?; grep -v warning /tmp/t.txt; exit \$rc; }"
echo "PROBE_EXIT=$?"
