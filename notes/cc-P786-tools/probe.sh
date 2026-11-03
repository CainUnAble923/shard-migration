#!/usr/bin/env bash
# cc-P786 probe (P785's): runs the tests matching $1 in the builder image of this branch's base (P784) with the witch
# sources and test mounted over it. PROBE_MODE=red mounts the new test file alone (the code before the change);
# PROBE_MODE=green (default) mounts the change too: the HalloweenWitch folder (SRC=<dir> for a mutant) and the
# Encounters folder (ENC=<dir> for a mutant). Touch mounted files first: a file older than the image build is not
# recompiled.
set -u
FILTER="$1"
IMAGE="${2:-sl-uo-builder:cc-p784}"
MODE="${PROBE_MODE:-green}"
CODE="D:/UO/golems/Iron/ShatteredLegacy/server"
SRC="${SRC:-$CODE/customizations/HalloweenWitch}"
ENC="${ENC:-$CODE/customizations/Encounters}"
UC=/build/modernuo/Projects/UOContent
UT=/build/modernuo/Projects/UOContent.Tests/Tests
M=(-v "$CODE/tests/Misc/HalloweenWitchVerification.cs:$UT/Misc/HalloweenWitchVerification.cs")
if [ "$MODE" = green ]; then
  M+=(-v "$SRC:$UC/HalloweenWitch" -v "$ENC:$UC/Encounters")
fi
MSYS_NO_PATHCONV=1 docker run --rm --network=none --security-opt seccomp=unconfined "${M[@]}" \
  "$IMAGE" bash -c "cd /build/modernuo && dotnet build Projects/UOContent/UOContent.csproj -c Release --no-restore 2>&1 | grep -E ' error ' | sort -u | head -30 ; dotnet build Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore 2>&1 | grep -E ' error |Build succeeded' | sort -u | head -30 ; dotnet test --no-build Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore --filter '$FILTER' --logger 'console;verbosity=normal' 2>&1 | grep -v warning"
