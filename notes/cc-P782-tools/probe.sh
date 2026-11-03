#!/usr/bin/env bash
# cc-P782 probe (P781's): runs the tests matching $1 in the builder image of this branch's base (P780, now main) with
# the grave digging sources, the loot box roller and the test mounted over it. PROBE_MODE=red mounts the new test file
# alone (the code before the change); PROBE_MODE=green (default) mounts the change too; SRC=<dir> mounts another
# GraveDigging folder (a mutant; touch it first: a file older than the image's build is not recompiled).
# The SBTinker patch is not in a probe (only the gated build applies patches), so fact 7 fails here until the gate.
set -u
FILTER="$1"
IMAGE="${2:-sl-uo-builder:cc-p780}"
MODE="${PROBE_MODE:-green}"
CODE="D:/UO/golems/Iron/ShatteredLegacy/server"
SRC="${SRC:-$CODE/customizations/GraveDigging}"
UC=/build/modernuo/Projects/UOContent
UT=/build/modernuo/Projects/UOContent.Tests/Tests
M=(-v "$CODE/tests/Misc/GraveDiggingVerification.cs:$UT/Misc/GraveDiggingVerification.cs")
if [ "$MODE" = green ]; then
  M+=(-v "$SRC:$UC/GraveDigging")
  M+=(-v "$CODE/customizations/LootBoxes/LootBoxRoller.cs:$UC/LootBoxes/LootBoxRoller.cs")
fi
MSYS_NO_PATHCONV=1 docker run --rm --network=none --security-opt seccomp=unconfined "${M[@]}" \
  "$IMAGE" bash -c "cd /build/modernuo && dotnet build Projects/UOContent/UOContent.csproj -c Release --no-restore 2>&1 | grep -E ' error ' | sort -u | head -30 ; dotnet build Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore 2>&1 | grep -E ' error |Build succeeded' | sort -u | head -30 ; dotnet test --no-build Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore --filter '$FILTER' --logger 'console;verbosity=normal' 2>&1 | grep -v warning"
