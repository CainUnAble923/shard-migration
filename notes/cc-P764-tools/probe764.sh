#!/usr/bin/env bash
# cc-P764 probe (P762's and P769's method): a mutant's ClusterFPetLeash.cs and Tutorial folder, and the code copy's
# leash tests, over sl-uo-builder:cc-p764's copies; runs the tests matching $1.
# Usage: SRC=<mutant folder> probe764.sh <filter> [image]
set -u
FILTER="$1"
IMAGE="${2:-sl-uo-builder:cc-p764}"
CODE="D:/UO/golems/Iron/ShatteredLegacy/server"
SRC="${SRC:-$CODE/customizations}"
UC=/build/modernuo/Projects/UOContent
UT=/build/modernuo/Projects/UOContent.Tests/Tests
MSYS_NO_PATHCONV=1 docker run --rm --network=none --security-opt seccomp=unconfined -e MODE= \
  -v "$SRC/Tutorial:$UC/Tutorial" \
  -v "$SRC/ClusterFPetLeash.cs:$UC/Misc/ClusterFPetLeash.cs" \
  -v "$CODE/tests/Items/PetLeashVerification.cs:$UT/Items/PetLeashVerification.cs" \
  "$IMAGE" bash -c "cd /build/modernuo && dotnet build Projects/UOContent/UOContent.csproj -c Release --no-restore -v q 2>&1 | grep -E ' error ' ; dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore --filter '$FILTER' --logger 'console;verbosity=normal' 2>&1 | grep -v warning"
