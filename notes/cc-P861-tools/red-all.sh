#!/usr/bin/env bash
# cc-P861 (P860's red-all.sh): one container on the builder image. RED: the code before the change (red/: git HEAD's
# builder plus the step's Stashed name, HEAD's seasonal switch and gargish outcast, an inert stub of the new classes; no
# names-shard.json). GREEN: the real code and data. The ten new facts (ShardNamesVerification, AddonStatifyVerification)
# each time. Output: red-all.txt.
T=D:/UO/golems/Iron/shard-migration/notes/cc-P861-tools
SL=${SL:-D:/UO/golems/Iron/ShatteredLegacy/server}
IMAGE=${IMAGE:-sl-uo-builder:bot}
cat > "$T/red-all-inner.sh" <<'INNER'
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
INNER
MSYS_NO_PATHCONV=1 docker run --rm --network=none --security-opt seccomp=unconfined -e MODE= \
  -v "$SL/customizations:/m/c:ro" -v "$SL/tests/Misc:/m/tests:ro" -v "$SL/data:/m/data:ro" -v "$T/red:/m/red:ro" \
  -v "$T/red-all-inner.sh:/m/inner.sh:ro" "$IMAGE" bash /m/inner.sh > "$T/red-all.txt" 2>&1
echo done
