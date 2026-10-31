#!/usr/bin/env bash
# cc-P708 probe (P741's probe.sh, for the guild hall files): the code copy's guild hall customizations and facts over
# sl-uo-builder:cc-P708's copies; runs the tests matching $1. SRC (default: the code copy's customizations) may point at
# a mutant copy holding the same file names. Usage: probe-guild.sh <filter> [image]
set -u
FILTER="$1"
IMAGE="${2:-sl-uo-builder:cc-P708}"
CODE="D:/UO/golems/Iron/ShatteredLegacy/server"
SRC="${SRC:-$CODE/customizations}"
UC=/build/modernuo/Projects/UOContent
UT=/build/modernuo/Projects/UOContent.Tests/Tests
M=""
for f in ClusterFGuildHallPlacementData.cs ClusterFGuildHallPlacement.cs ClusterFGuildHallMoves.cs LeagueSteward.cs ClusterFGuildStarterPath.cs; do
  M="$M -v $SRC/$f:$UC/Misc/$f"
done
for f in GuildHallSosMovesVerification.cs GuildHallPlacementVerification.cs GuildHallPlacementDesignCopy.cs; do
  M="$M -v $CODE/tests/Misc/$f:$UT/Misc/$f"
done
MSYS_NO_PATHCONV=1 docker run --rm --network=none --security-opt seccomp=unconfined $M \
  "$IMAGE" bash -c "cd /build/modernuo && dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore --filter '$FILTER' --logger 'console;verbosity=normal' 2>&1 | grep -v warning"
