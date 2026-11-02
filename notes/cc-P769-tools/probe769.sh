#!/usr/bin/env bash
# cc-P769 probe (P762's): a mutant's Tutorial folder, HavenTownRegions.cs, LeagueRegistrar.cs and ClusterFQuestMilestones.cs,
# and the code copy's P769 tests, over sl-uo-builder:cc-p769's copies; runs the tests matching $1.
# Usage: SRC=<mutant folder> probe769.sh <filter> [image]
set -u
FILTER="$1"
IMAGE="${2:-sl-uo-builder:cc-p769}"
CODE="D:/UO/golems/Iron/ShatteredLegacy/server"
SRC="${SRC:-$CODE/customizations}"
UC=/build/modernuo/Projects/UOContent
UT=/build/modernuo/Projects/UOContent.Tests/Tests
MSYS_NO_PATHCONV=1 docker run --rm --network=none --security-opt seccomp=unconfined -e MODE= \
  -v "$SRC/Tutorial:$UC/Tutorial" \
  -v "$SRC/Regions/HavenTownRegions.cs:$UC/Regions/HavenTownRegions.cs" \
  -v "$SRC/LeagueRegistrar.cs:$UC/Misc/LeagueRegistrar.cs" \
  -v "$SRC/ClusterFQuestMilestones.cs:$UC/Misc/ClusterFQuestMilestones.cs" \
  -v "$CODE/tests/Tutorial:$UT/Tutorial" \
  -v "$CODE/tests/Regions/HavenTownVerification.cs:$UT/Regions/HavenTownVerification.cs" \
  "$IMAGE" bash -c "cd /build/modernuo && dotnet build Projects/UOContent/UOContent.csproj -c Release --no-restore -v q 2>&1 | grep -E ' error ' ; dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore --filter '$FILTER' --logger 'console;verbosity=normal' 2>&1 | grep -v warning"
