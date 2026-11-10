#!/usr/bin/env bash
cd /build/modernuo
U=Projects/UOContent
mkdir -p Projects/UOContent.Tests/Tests/Mobiles/Mounts
cp /m/t/RidablePolarBearVerification.cs Projects/UOContent.Tests/Tests/Mobiles/Mounts/
run() {
  echo "=================== $1"
  dotnet build Projects/UOContent.Tests/UOContent.Tests.csproj -c Release -v q > /tmp/b.txt 2>&1
  grep -E ' error |Build succeeded' /tmp/b.txt | sort -u | head -8
  dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-build \
    --filter "FullyQualifiedName~RidablePolarBearVerification" --logger 'console;verbosity=normal' > /tmp/t.txt 2>&1
  grep -E '^\s+(Passed|Failed) ShatteredLegacy' /tmp/t.txt | sort -u | sed 's/ \[.*//'
  grep -A6 'Failed ShatteredLegacy' /tmp/t.txt | grep -E 'Assert|Expected|Actual|Exception' | head -24
  grep -E '^\s+(Passed|Failed|Total tests):' /tmp/t.txt | head -3
}
cp /m/red/stub.cs "$U/Mobiles/Mounts/RidablePolarBear.cs"
run "RED: the stub (the code before the change)"
cp /m/c/RidablePolarBear.cs /m/c/RidablePolarBearDens.cs "$U/Mobiles/Mounts/"
cp /m/red/m-fence-dens.cs "$U/Mobiles/Mounts/RidablePolarBearDens.cs"
run "RED mutant m-fence-dens: a den moved under the north-east snow isles' fence"
cp /m/c/RidablePolarBearDens.cs "$U/Mobiles/Mounts/"
cp /m/red/m-loot-bear.cs "$U/Mobiles/Mounts/RidablePolarBear.cs"
run "RED mutant m-loot-bear: the bear carries gold and a treasure map level"
cp /m/c/RidablePolarBear.cs "$U/Mobiles/Mounts/"
run "GREEN: the real code"
