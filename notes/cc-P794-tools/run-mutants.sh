#!/usr/bin/env bash
# cc-P794 (P764's method): the EtherealLooks facts on the unmutated copy (_base) and each mutant (mutate794.py), over
# sl-uo-builder:cc-p794's copies, one container and one log each. Usage: run-mutants.sh <mutants folder> <log folder>
set -u
MUT="$1"; LOGS="$2"
CODE="D:/UO/golems/Iron/ShatteredLegacy/server"
UC=/build/modernuo/Projects/UOContent
UT=/build/modernuo/Projects/UOContent.Tests/Tests
FILTER='FullyQualifiedName~EtherealLooksVerification'
mkdir -p "$LOGS"
for d in "$MUT"/*/; do
  name=$(basename "$d")
  MSYS_NO_PATHCONV=1 docker run --rm --network=none --security-opt seccomp=unconfined -e MODE= \
    -v "${d%/}/EtherealLooks.cs:$UC/Mobiles/Mounts/EtherealLooks.cs" \
    -v "$CODE/tests/Mobiles/Mounts/EtherealLooksVerification.cs:$UT/Mobiles/Mounts/EtherealLooksVerification.cs" \
    sl-uo-builder:cc-p794 bash -c "cd /build/modernuo && touch Projects/UOContent/Mobiles/Mounts/EtherealLooks.cs; dotnet build Projects/UOContent/UOContent.csproj -c Release --no-restore -v q 2>&1 | grep -E ' error ' ; dotnet build Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore -v q 2>&1 | grep -E ' error ' ; dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-build --filter '$FILTER' --logger 'console;verbosity=normal' 2>&1 | grep -v warning" > "$LOGS/$name.log" 2>&1
  failed=$(grep -a -E '^\s+Failed ShatteredLegacy' "$LOGS/$name.log" | sed -E 's/^\s+Failed ShatteredLegacy\.Tests\.[A-Za-z]+\.//; s/\(.*$//; s/ \[.*$//' | sort -u | tr '\n' ';')
  echo "$name: $(grep -a -E '^\s*(Passed|Failed|Total tests):' "$LOGS/$name.log" | tr -s ' ' | tr '\n' ' ') $(grep -a -c ' error ' "$LOGS/$name.log") errors | $failed"
done
