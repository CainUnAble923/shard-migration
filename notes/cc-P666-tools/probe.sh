#!/usr/bin/env bash
# cc-P666 probe (P705's probe.sh): the edited Tutorial folder, VetResurrection.cs, the vet file and the tests,
# bind-mounted over sl-uo-builder:cc-P705's copies; runs the tests matching $1.
#   TUT=<Tutorial folder> VR=<VetResurrection.cs> VET=<Veterinarian.cs> probe.sh <filter>
set -u
FILTER="$1"
HERE="$(cd "$(dirname "$0")" && (pwd -W 2>/dev/null || pwd))"
IMAGE="${IMAGE:-sl-uo-builder:cc-P705}"
CODE="D:/UO/golems/Iron/ShatteredLegacy/server"
UC=/build/modernuo/Projects/UOContent
UT=/build/modernuo/Projects/UOContent.Tests/Tests
MSYS_NO_PATHCONV=1 docker run --rm --network=none --security-opt seccomp=unconfined \
  -v "${TUT:-$CODE/customizations/Tutorial}:$UC/Tutorial" \
  -v "${VR:-$CODE/customizations/Mobiles/NPCs/VetResurrection.cs}:$UC/Mobiles/NPCs/VetResurrection.cs" \
  -v "${VET:-$HERE/Veterinarian-patched.cs}:$UC/Mobiles/Vendors/NPC/Veterinarian.cs" \
  -v "$CODE/tests/Tutorial:$UT/Tutorial" \
  "$IMAGE" bash -c "cd /build/modernuo && dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore --filter '$FILTER' --logger 'console;verbosity=normal' 2>&1 | grep -v warning"
