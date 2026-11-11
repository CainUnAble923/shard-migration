#!/usr/bin/env bash
cd /build/modernuo
U=Projects/UOContent
mkdir -p $U/ShardCarpet Projects/UOContent.Tests/Tests/Carpet
cp /m/t/VariableCarpetVerification.cs Projects/UOContent.Tests/Tests/Carpet/
run() {
  echo "=================== $1"
  dotnet build Projects/UOContent.Tests/UOContent.Tests.csproj -c Release -v q > /tmp/b.txt 2>&1
  grep -E ' error |Build succeeded' /tmp/b.txt | sort -u | head -6
  dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-build \
    --filter "FullyQualifiedName~VariableCarpetVerification" --logger 'console;verbosity=normal' > /tmp/t.txt 2>&1
  grep -E '^\s+(Passed|Failed) ShatteredLegacy' /tmp/t.txt | sort -u | sed 's/ \[.*//'
  grep -E '^\s+(Passed|Failed):' /tmp/t.txt | head -2
}
for f in /m/red/stub.cs /m/red/m-*.cs; do
  cp "$f" $U/ShardCarpet/VariableCarpet.cs
  run "RED $(basename $f)"
done
cp /m/c/VariableCarpet.cs $U/ShardCarpet/VariableCarpet.cs
run "GREEN (the real code)"
