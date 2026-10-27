#!/usr/bin/env bash
# cc-P664 probe (P663's probe_full.sh, with the CharacterCreation copy selectable): the edited customizations and tests
# bind-mounted over sl-uo-builder's copies; runs the tests matching $1.
#   TUT=<Tutorial folder> CC=<CharacterCreation.cs> probe.sh <filter>
set -u
FILTER="$1"
IMAGE="${IMAGE:-sl-uo-builder:latest}"
CODE="D:/UO/golems/Iron/ShatteredLegacy/server"
UC=/build/modernuo/Projects/UOContent
UT=/build/modernuo/Projects/UOContent.Tests/Tests
MSYS_NO_PATHCONV=1 docker run --rm --network=none --security-opt seccomp=unconfined \
  -v "${TUT:-$CODE/customizations/Tutorial}:$UC/Tutorial" \
  -v "$CODE/customizations/Fold:$UC/Fold" \
  -v "${CC:-$CODE/customizations/CharacterCreation.cs}:$UC/Engines/Character Creation/CharacterCreation.cs" \
  -v "$CODE/customizations/ShardClilocs.cs:$UC/Misc/ShardClilocs.cs" \
  -v "$CODE/tests/Tutorial:$UT/Tutorial" \
  -v "$CODE/tests/Regions/FoldVerification.cs:$UT/Regions/FoldVerification.cs" \
  -v "$CODE/tests/Misc/TutorialVerification.cs:$UT/Misc/TutorialVerification.cs" \
  "$IMAGE" bash -c "cd /build/modernuo && dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore --filter '$FILTER' --logger 'console;verbosity=normal' 2>&1 | grep -v warning"
