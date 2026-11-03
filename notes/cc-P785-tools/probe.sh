#!/usr/bin/env bash
# cc-P785 probe (P784's): runs the tests matching $1 in the builder image of this branch's base (P783) with the
# chocolatiering sources and test mounted over it. PROBE_MODE=red mounts the new test file alone (the code before the
# change); PROBE_MODE=green (default) mounts the change too: the Chocolatiering folder (SRC=<dir> for a mutant), the
# edited Nutcrackers.cs and CookingCraftRegistrations.cs, and Provisioner.cs with Provisioner-chocolatiering.patch
# applied (Provisioner.patched.cs here; PATCHCHECK=1 instead checks the patch itself with --fuzz=0).
# NUT=<file> and PROV=<file> mount another Nutcrackers.cs or Provisioner.cs (mutants).
# Touch mounted files first: a file older than the image build is not recompiled.
set -u
FILTER="$1"
IMAGE="${2:-sl-uo-builder:cc-p783}"
MODE="${PROBE_MODE:-green}"
CODE="D:/UO/golems/Iron/ShatteredLegacy/server"
HERE="D:/UO/golems/Iron/shard-migration/notes/cc-P785-tools"
SRC="${SRC:-$CODE/customizations/Chocolatiering}"
NUT="${NUT:-$CODE/customizations/Items/Consumables/Nutcrackers.cs}"
PROV="${PROV:-$HERE/Provisioner.patched.cs}"
UC=/build/modernuo/Projects/UOContent
UT=/build/modernuo/Projects/UOContent.Tests/Tests
if [ "${PATCHCHECK:-0}" = 1 ]; then
  MSYS_NO_PATHCONV=1 docker run --rm --network=none -v "$CODE/patches/Provisioner-chocolatiering.patch:/p.patch" "$IMAGE" \
    bash -c "cd /build/modernuo && git checkout -q -- Projects/UOContent/Mobiles/Vendors/NPC/Provisioner.cs 2>/dev/null; patch -p1 -R --dry-run --fuzz=0 < /p.patch && echo REVERSE-OK-ALREADY-APPLIED || patch -p1 --dry-run --fuzz=0 < /p.patch"
  exit
fi
M=(-v "$CODE/tests/Misc/ChocolatieringVerification.cs:$UT/Misc/ChocolatieringVerification.cs")
if [ "$MODE" = green ]; then
  M+=(-v "$SRC:$UC/Chocolatiering"
      -v "$NUT:$UC/Items/Consumables/Nutcrackers.cs"
      -v "$CODE/customizations/Engines/Craft/CookingCraftRegistrations.cs:$UC/Engines/Craft/CookingCraftRegistrations.cs"
      -v "$PROV:$UC/Mobiles/Vendors/NPC/Provisioner.cs")
fi
MSYS_NO_PATHCONV=1 docker run --rm --network=none --security-opt seccomp=unconfined "${M[@]}" \
  "$IMAGE" bash -c "cd /build/modernuo && dotnet build Projects/UOContent/UOContent.csproj -c Release --no-restore 2>&1 | grep -E ' error ' | sort -u | head -30 ; dotnet build Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore 2>&1 | grep -E ' error |Build succeeded' | sort -u | head -30 ; dotnet test --no-build Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore --filter '$FILTER' --logger 'console;verbosity=normal' 2>&1 | grep -v warning"
