#!/usr/bin/env bash
# cc-P845 (P806's): seeing the new and changed facts fail on the code before the fix. M_REV (a shard-repo tree, the release copy with P806's
# Tutorial changes reverted one at a time by M_SED) is mounted over the builder image's; UOContent, then the tests, then test --no-build.
#   IMAGE=sl-uo-builder:cc-P845 M_NAME=m1 M_FILE=NewHavenLessons.cs M_SED='s/...//' mutant.sh <filter>
set -u
FILTER="$1"
IMAGE="${IMAGE:-sl-uo-builder:cc-P845}"
CODE="${M_CODE:-D:/UO/golems/Iron/ShatteredLegacy}/server"
WORK="C:/Users/ckfle/AppData/Local/Temp/claude/136edbd9b201f108/15e6fa9c-8cb3-47f1-bb71-188d0f606ebb/scratchpad/mut-$M_NAME"
rm -rf "$WORK"; mkdir -p "$WORK"
cp -r "$CODE/customizations/Tutorial" "$WORK/Tutorial"
sed -i -E "$M_SED" "$WORK/Tutorial/$M_FILE"
touch "$WORK/Tutorial/$M_FILE"
diff -q "$CODE/customizations/Tutorial/$M_FILE" "$WORK/Tutorial/$M_FILE" >/dev/null && { echo "the mutation changed nothing"; exit 3; }
UC=/build/modernuo/Projects/UOContent
UT=/build/modernuo/Projects/UOContent.Tests/Tests
MSYS_NO_PATHCONV=1 docker run --rm --network=none --security-opt seccomp=unconfined \
  -v "$WORK/Tutorial:$UC/Tutorial" -v "$CODE/tests/Tutorial:$UT/Tutorial" \
  "$IMAGE" bash -c "cd /build/modernuo && touch $UC/Tutorial/$M_FILE && dotnet build Projects/UOContent/UOContent.csproj -c Release --no-restore 2>&1 | grep -E 'error CS|Elapsed' | sort -u | head -5; dotnet build Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore 2>&1 | grep -E 'error CS' | sort -u | head -5; dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-build --filter '$FILTER' --logger 'console;verbosity=normal' 2>&1 | grep -E '^ +(Failed|Passed):|Failed [A-Z]|Assert\.|Total tests|Passed!|Failed!' | head -30"
