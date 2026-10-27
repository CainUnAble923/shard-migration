#!/usr/bin/env bash
# cc-P665 probe: the edited Tutorial and Fold folders and tests bind-mounted over sl-uo-builder's copies; runs the tests
# matching $1. Usage: probe.sh <filter> [image]. TUT=<folder> mounts another Tutorial folder (a red-run mutant).
set -u
FILTER="$1"
IMAGE="${2:-sl-uo-builder:cc-P705}"
CODE="D:/UO/golems/Iron/ShatteredLegacy/server"
UC=/build/modernuo/Projects/UOContent
UT=/build/modernuo/Projects/UOContent.Tests/Tests
MSYS_NO_PATHCONV=1 docker run --rm --network=none --security-opt seccomp=unconfined \
  -v "${TUT:-$CODE/customizations/Tutorial}:$UC/Tutorial" \
  -v "$CODE/customizations/Fold:$UC/Fold" \
  -v "$CODE/tests/Tutorial:$UT/Tutorial" \
  -v "$CODE/tests/Misc/TutorialVerification.cs:$UT/Misc/TutorialVerification.cs" \
  "$IMAGE" bash -c "cd /build/modernuo && dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore --filter '$FILTER' --logger 'console;verbosity=normal' 2>&1 | grep -v warning"
