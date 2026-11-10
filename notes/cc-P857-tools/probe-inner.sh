#!/usr/bin/env bash
# cc-P857: inside a builder image. Install the copy's carpet code and facts, then build and run the facts.
cd /build/modernuo
U=Projects/UOContent
mkdir -p $U/ShardCarpet Projects/UOContent.Tests/Tests/Carpet
cp /m/t/VariableCarpetVerification.cs Projects/UOContent.Tests/Tests/Carpet/
cp /m/c/VariableCarpet.cs $U/ShardCarpet/
if [ -n "${RED:-}" ]; then
  echo "== RED mutant: $RED"
  cp /m/red/$RED $U/ShardCarpet/VariableCarpet.cs
fi
dotnet build Projects/UOContent.Tests/UOContent.Tests.csproj -c Release -v q > /tmp/b.txt 2>&1
grep -E ' error |Build succeeded' /tmp/b.txt | sort -u | head -20
dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-build \
  --filter "FullyQualifiedName~VariableCarpetVerification" \
  --logger 'console;verbosity=normal' > /tmp/t.txt 2>&1
grep -E '^\s+(Passed|Failed) ' /tmp/t.txt | head -20
grep -A12 'Failed ShatteredLegacy' /tmp/t.txt | head -120
grep -E 'Total tests|Passed:|Failed:' /tmp/t.txt
