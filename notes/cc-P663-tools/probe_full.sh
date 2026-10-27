#!/usr/bin/env bash
# cc-P663 probe: edited customizations and tests bind-mounted over sl-uo-builder's copies; runs the tests matching $1.
# Usage: probe.sh <filter> [image] [extra docker -v args...]
set -u
FILTER="$1"
IMAGE="${2:-sl-uo-builder:latest}"
shift 2 2>/dev/null || shift 1
CODE="D:/UO/golems/Iron/ShatteredLegacy/server"
UC=/build/modernuo/Projects/UOContent
UT=/build/modernuo/Projects/UOContent.Tests/Tests
MSYS_NO_PATHCONV=1 docker run --rm --network=none --security-opt seccomp=unconfined \
  -v "${TUT:-$CODE/customizations/Tutorial}:$UC/Tutorial" \
  -v "$CODE/customizations/Fold:$UC/Fold" \
  -v "$CODE/customizations/CharacterCreation.cs:$UC/Engines/Character Creation/CharacterCreation.cs" \
  -v "$CODE/customizations/ShardClilocs.cs:$UC/Misc/ShardClilocs.cs" \
  -v "$CODE/tests/Tutorial:$UT/Tutorial" \
  -v "$CODE/tests/Regions/FoldVerification.cs:$UT/Regions/FoldVerification.cs" \
  -v "$CODE/tests/Misc/TutorialVerification.cs:$UT/Misc/TutorialVerification.cs" \
  -v "$CODE/tests/Misc/TazUOClientCommandVerification.cs:$UT/Misc/TazUOClientCommandVerification.cs" \
  -v "$CODE/tests/Mobiles/Burrows/BurrowsCreaturesVerification.cs:$UT/Mobiles/Burrows/BurrowsCreaturesVerification.cs" \
  -v "$CODE/tests/Townsfolk/TownsfolkTalkVerification.cs:$UT/Townsfolk/TownsfolkTalkVerification.cs" \
  "$@" \
  "$IMAGE" bash -c "cd /build/modernuo && dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore --filter '$FILTER' --logger 'console;verbosity=normal' 2>&1 | grep -v warning"
