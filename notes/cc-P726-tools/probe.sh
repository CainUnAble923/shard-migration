#!/usr/bin/env bash
# cc-P726 probe (P728's): the edited customizations and tests over sl-uo-builder:cc-P728's copies (that image has P728,
# its PlayerMobile patch included); runs the tests matching $1. Usage: probe.sh <filter> [image]. SRC (default: the code
# copy's customizations) may point at a mutant copy.
set -u
FILTER="$1"
IMAGE="${2:-sl-uo-builder:cc-P728}"
CODE="D:/UO/golems/Iron/ShatteredLegacy/server"
SRC="${SRC:-$CODE/customizations}"
UC=/build/modernuo/Projects/UOContent
UT=/build/modernuo/Projects/UOContent.Tests/Tests
MSYS_NO_PATHCONV=1 docker run --rm --network=none --security-opt seccomp=unconfined \
  -v "$SRC/Tutorial:$UC/Tutorial" \
  -v "$SRC/Fold:$UC/Fold" \
  -v "$SRC/Mobiles/Evo:$UC/Mobiles/Evo" \
  -v "$SRC/LeagueRegistrar.cs:$UC/Misc/LeagueRegistrar.cs" \
  -v "$SRC/ClusterFSkillGain.cs:$UC/Misc/ClusterFSkillGain.cs" \
  -v "$SRC/ClusterFAchievements.cs:$UC/Misc/ClusterFAchievements.cs" \
  -v "$SRC/ClusterFBulletin.cs:$UC/Misc/ClusterFBulletin.cs" \
  -v "$SRC/ClusterFGuildStarterPath.cs:$UC/Misc/ClusterFGuildStarterPath.cs" \
  -v "$SRC/RegenRates.cs:$UC/Misc/RegenRates.cs" \
  -v "$SRC/ShardClilocs.cs:$UC/Misc/ShardClilocs.cs" \
  -v "$SRC/CharacterCreation.cs:$UC/Engines/Character Creation/CharacterCreation.cs" \
  -v "$CODE/tests/Tutorial:$UT/Tutorial" \
  -v "$CODE/tests/Misc/TutorialVerification.cs:$UT/Misc/TutorialVerification.cs" \
  "$IMAGE" bash -c "cd /build/modernuo && dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore --filter '$FILTER' --logger 'console;verbosity=normal' 2>&1 | grep -v warning"
