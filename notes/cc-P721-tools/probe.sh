#!/usr/bin/env bash
# cc-P721 probe: the edited customizations and tests bind-mounted over sl-uo-builder's copies; runs the tests matching $1.
# Usage: probe.sh <filter> [image]. SRC (default: the code copy's customizations) may point at a mutant copy.
set -u
FILTER="$1"
IMAGE="${2:-sl-uo-builder:cc-P717}"
CODE="D:/UO/golems/Iron/ShatteredLegacy/server"
SRC="${SRC:-$CODE/customizations}"
UC=/build/modernuo/Projects/UOContent
UT=/build/modernuo/Projects/UOContent.Tests/Tests
MSYS_NO_PATHCONV=1 docker run --rm --network=none --security-opt seccomp=unconfined \
  -v "$SRC/Tutorial:$UC/Tutorial" \
  -v "$SRC/Fold:$UC/Fold" \
  -v "$SRC/LeagueRegistrar.cs:$UC/Misc/LeagueRegistrar.cs" \
  -v "$SRC/ClusterFSkillGain.cs:$UC/Misc/ClusterFSkillGain.cs" \
  -v "$CODE/tests/Tutorial:$UT/Tutorial" \
  -v "$CODE/tests/Misc/TutorialVerification.cs:$UT/Misc/TutorialVerification.cs" \
  "$IMAGE" bash -c "cd /build/modernuo && dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore --filter '$FILTER' --logger 'console;verbosity=normal' 2>&1 | grep -v warning"
