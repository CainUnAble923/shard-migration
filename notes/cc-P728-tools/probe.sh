#!/usr/bin/env bash
# cc-P728 probe (P718's, extended): the edited customizations, tests and the new PlayerMobile patch over sl-uo-builder's
# copies; runs the tests matching $1. Usage: probe.sh <filter> [image]. SRC (default: the code copy's customizations) may
# point at a mutant copy; NOPATCH=1 leaves PlayerMobile.cs as the image has it (pinned's Move, no wake hook).
set -u
FILTER="$1"
IMAGE="${2:-sl-uo-builder:cc-P727}"
CODE="D:/UO/golems/Iron/ShatteredLegacy/server"
SRC="${SRC:-$CODE/customizations}"
UC=/build/modernuo/Projects/UOContent
UT=/build/modernuo/Projects/UOContent.Tests/Tests
PATCHSTEP="patch -p1 --forward --ignore-whitespace --fuzz=0 --batch < /tmp/wake.patch && "
if [ "${NOPATCH:-0}" = "1" ]; then PATCHSTEP=""; fi
MSYS_NO_PATHCONV=1 docker run --rm --network=none --security-opt seccomp=unconfined \
  -v "$SRC/Tutorial:$UC/Tutorial" \
  -v "$SRC/Fold:$UC/Fold" \
  -v "$SRC/LeagueRegistrar.cs:$UC/Misc/LeagueRegistrar.cs" \
  -v "$SRC/ClusterFSkillGain.cs:$UC/Misc/ClusterFSkillGain.cs" \
  -v "$SRC/ClusterFAchievements.cs:$UC/Misc/ClusterFAchievements.cs" \
  -v "$SRC/ClusterFBulletin.cs:$UC/Misc/ClusterFBulletin.cs" \
  -v "$SRC/ClusterFGuildStarterPath.cs:$UC/Misc/ClusterFGuildStarterPath.cs" \
  -v "$SRC/CharacterCreation.cs:$UC/Engines/Character Creation/CharacterCreation.cs" \
  -v "$CODE/patches/PlayerMobile-tutorial-wake-move.patch:/tmp/wake.patch" \
  -v "$CODE/tests/Tutorial:$UT/Tutorial" \
  -v "$CODE/tests/Misc/TutorialVerification.cs:$UT/Misc/TutorialVerification.cs" \
  "$IMAGE" bash -c "cd /build/modernuo && ${PATCHSTEP}dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore --filter '$FILTER' --logger 'console;verbosity=normal' 2>&1 | grep -v warning"
