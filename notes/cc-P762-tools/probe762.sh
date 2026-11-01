#!/usr/bin/env bash
# cc-P762 probe (P761's, cut down): a mutant's Tutorial customizations and ClusterFDevTools.cs, and the code copy's
# Tutorial and character-creation tests, over sl-uo-builder:cc-p762's copies; runs the tests matching $1.
# Usage: SRC=<mutant folder> probe762.sh <filter> [image]
set -u
FILTER="$1"
IMAGE="${2:-sl-uo-builder:cc-p762}"
CODE="D:/UO/golems/Iron/ShatteredLegacy/server"
SRC="${SRC:-$CODE/customizations}"
UC=/build/modernuo/Projects/UOContent
UT=/build/modernuo/Projects/UOContent.Tests/Tests
MSYS_NO_PATHCONV=1 docker run --rm --network=none --security-opt seccomp=unconfined \
  -v "$SRC/Tutorial:$UC/Tutorial" \
  -v "$SRC/ClusterFDevTools.cs:$UC/Misc/ClusterFDevTools.cs" \
  -v "$CODE/tests/Tutorial:$UT/Tutorial" \
  -v "$CODE/tests/Engines/CharacterCreation:$UT/Engines/CharacterCreation" \
  "$IMAGE" bash -c "cd /build/modernuo && dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore --filter '$FILTER' --logger 'console;verbosity=normal' 2>&1 | grep -v warning"
