#!/usr/bin/env bash
# cc-P783 probe (P782's): runs the tests matching $1 in the builder image of this branch's base (P781, now main) with
# the Artisan Festival sources, the loot box roller, the Festival store and the tests mounted over it. PROBE_MODE=red
# mounts the test files alone (the code before the change); PROBE_MODE=green (default) mounts the change too;
# SRC=<dir>, ROLLER=<file>, FESTIVAL=<file> mount other copies (mutants; touch them first: a file older than the image is not rebuilt).
set -u
FILTER="$1"
IMAGE="${2:-sl-uo-builder:cc-p781}"
MODE="${PROBE_MODE:-green}"
CODE="D:/UO/golems/Iron/ShatteredLegacy/server"
SRC="${SRC:-$CODE/customizations/ArtisanFestival}"
ROLLER="${ROLLER:-$CODE/customizations/LootBoxes/LootBoxRoller.cs}"
FESTIVAL="${FESTIVAL:-$CODE/customizations/RewardStores/FestivalStore.cs}"
UC=/build/modernuo/Projects/UOContent
UT=/build/modernuo/Projects/UOContent.Tests/Tests
M=(-v "$CODE/tests/Misc/ArtisanFestivalVerification.cs:$UT/Misc/ArtisanFestivalVerification.cs")
M+=(-v "$CODE/tests/Misc/LootBoxDiversityVerification.cs:$UT/Misc/LootBoxDiversityVerification.cs")
if [ "$MODE" = green ]; then
  M+=(-v "$SRC:$UC/ArtisanFestival")
  M+=(-v "$ROLLER:$UC/LootBoxes/LootBoxRoller.cs")
  M+=(-v "$FESTIVAL:$UC/RewardStores/FestivalStore.cs")
fi
MSYS_NO_PATHCONV=1 docker run --rm --network=none --security-opt seccomp=unconfined "${M[@]}" \
  "$IMAGE" bash -c "cd /build/modernuo && dotnet build Projects/UOContent/UOContent.csproj -c Release --no-restore 2>&1 | grep -E ' error ' | sort -u | head -30 ; dotnet build Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore 2>&1 | grep -E ' error |Build succeeded' | sort -u | head -30 ; dotnet test --no-build Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore --filter '$FILTER' --logger 'console;verbosity=normal' 2>&1 | grep -v warning"
