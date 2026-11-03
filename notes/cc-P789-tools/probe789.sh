#!/usr/bin/env bash
# cc-P789 probe (P785's shape): runs the play test facts in the builder image of this branch's base (P786, which has
# P773) with files mounted over it. SRC=<PlayTestTasks.cs> (default: the code copy's; P773's or a mutant for red) and
# TEST=<PlayTestTasksVerification.cs> (default: the code copy's). Touch mounted files first: a file older than the
# image build is not recompiled.
set -u
FILTER="${1:-FullyQualifiedName~PlayTestTasksVerification}"
IMAGE="${2:-sl-uo-builder:cc-p786}"
CODE="D:/UO/golems/Iron/ShatteredLegacy/server"
SRC="${SRC:-$CODE/customizations/PlayTest/PlayTestTasks.cs}"
TEST="${TEST:-$CODE/tests/PlayTest/PlayTestTasksVerification.cs}"
UC=/build/modernuo/Projects/UOContent
UT=/build/modernuo/Projects/UOContent.Tests/Tests
MSYS_NO_PATHCONV=1 docker run --rm --network=none --security-opt seccomp=unconfined \
  -v "$SRC:$UC/PlayTest/PlayTestTasks.cs" -v "$TEST:$UT/PlayTest/PlayTestTasksVerification.cs" \
  "$IMAGE" bash -c "cd /build/modernuo && dotnet build Projects/UOContent/UOContent.csproj -c Release --no-restore 2>&1 | grep -E ' error ' | sort -u | head -30 ; dotnet build Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore 2>&1 | grep -E ' error |Build succeeded' | sort -u | head -30 ; dotnet test --no-build Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore --filter '$FILTER' --logger 'console;verbosity=normal' 2>&1 | grep -v warning"
