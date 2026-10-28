#!/usr/bin/env bash
# cc-P707 probe (P666's): the Tutorial folder and the tests, bind-mounted over sl-uo-builder:cc-P707's copies; runs the
# tests matching $1.   TUT=<Tutorial folder> probe.sh <filter>
set -u
FILTER="$1"
IMAGE="${IMAGE:-sl-uo-builder:cc-P707}"
CODE="D:/UO/golems/Iron/ShatteredLegacy/server"
UC=/build/modernuo/Projects/UOContent
UT=/build/modernuo/Projects/UOContent.Tests/Tests
EXTRA=()
# BAND: a Bandage.cs with this branch's Bandage-tutorial-real-heal.patch applied to pinned's (the builder's copy has HEAD's)
if [ -n "${BAND:-}" ]; then EXTRA=(-v "$BAND:$UC/Items/Skill Items/Misc/Bandage.cs"); fi
MSYS_NO_PATHCONV=1 docker run --rm --network=none --security-opt seccomp=unconfined \
  -v "${TUT:-$CODE/customizations/Tutorial}:$UC/Tutorial" \
  -v "$CODE/tests/Tutorial:$UT/Tutorial" "${EXTRA[@]}" \
  "$IMAGE" bash -c "cd /build/modernuo && dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore --filter '$FILTER' --logger 'console;verbosity=normal' 2>&1 | grep -v warning"
