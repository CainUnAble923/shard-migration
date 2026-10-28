#!/usr/bin/env bash
# cc-P681 probe: the new customizations and the fact file bind-mounted over a builder image (main's, without this
# branch's importer patch, for the red run); runs the facts matching $1.   IMAGE=<builder> probe.sh <filter>
set -u
FILTER="$1"
IMAGE="${IMAGE:-sl-uo-builder:latest}"
C=D:/UO/golems/Iron/ShatteredLegacy/server
UC=/build/modernuo/Projects/UOContent
UT=/build/modernuo/Projects/UOContent.Tests/Tests
MSYS_NO_PATHCONV=1 docker run --rm --network=none --security-opt seccomp=unconfined \
  -v "$C/customizations/ClusterFSosSpawnPlacements.cs:$UC/Misc/ClusterFSosSpawnPlacements.cs" \
  -v "$C/customizations/ClusterFSosSpawnPlacementsTable.cs:$UC/Misc/ClusterFSosSpawnPlacementsTable.cs" \
  -v "$C/tests/Misc/SosSpawnPlacementsVerification.cs:$UT/Misc/SosSpawnPlacementsVerification.cs" \
  "$IMAGE" bash -c "cd /build/modernuo && dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore --filter '$FILTER' --logger 'console;verbosity=normal' 2>&1 | grep -v warning"
