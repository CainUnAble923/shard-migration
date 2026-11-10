#!/usr/bin/env bash
cd /build/modernuo
U=Projects/UOContent
D=Distribution/Data/ShatteredLegacy
cp /m/tests/ShardNamesVerification.cs /m/tests/AddonStatifyVerification.cs Projects/UOContent.Tests/Tests/Misc/
run() {
  echo "=================== $1"
  dotnet build Projects/UOContent.Tests/UOContent.Tests.csproj -c Release -v q > /tmp/b.txt 2>&1
  grep -E ' error |Build succeeded' /tmp/b.txt | sort -u | head -12
  dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-build \
    --filter "FullyQualifiedName~ShardNamesVerification|FullyQualifiedName~AddonStatifyVerification|FullyQualifiedName~StaffBuildToolsVerification|FullyQualifiedName~VisualBuilderVerification|FullyQualifiedName~CCP129CreatureVerification" \
    --logger 'console;verbosity=normal' > /tmp/t.txt 2>&1
  grep -E '^\s+(Passed|Failed) ShatteredLegacy' /tmp/t.txt | sort -u | sed 's/ \[.*//'
  grep -A8 'Failed ShatteredLegacy' /tmp/t.txt | grep -E 'Assert|Expected|Actual|Exception|Message' | head -30
  grep -E '^\s+(Passed|Failed|Total tests):' /tmp/t.txt | head -3
}
mkdir -p $U/Names
cp /m/red/stub.cs $U/Names/ShardNames.cs
cp /m/red/ClusterFVisualBuilder.cs /m/red/ClusterFSeasonalSwitch.cs $U/Misc/
cp /m/red/GargishOutcast.cs $U/Mobiles/Normal/
rm -f $D/names-shard.json
run "RED: the code before the change"
cp /m/c/Names/ShardNames.cs $U/Names/
mkdir -p $U/StaffBuildTools
cp /m/c/StaffBuildTools/AddonStatify.cs $U/StaffBuildTools/
cp /m/c/ClusterFVisualBuilder.cs /m/c/ClusterFSeasonalSwitch.cs $U/Misc/
cp /m/c/Mobiles/Normal/GargishOutcast.cs $U/Mobiles/Normal/
cp /m/data/names-shard.json $D/
run "GREEN: the real code and data"
