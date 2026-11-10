#!/usr/bin/env bash
# cc-P858: every red copy in red/ (stub, then each mutant) in one container, a build and the facts per copy, then the real
# code again (green). Output: red-all.txt.
T=D:/UO/golems/Iron/shard-migration/notes/cc-P858-tools
SL=${SL:-D:/UO/golems/Iron/ShatteredLegacy/server}
IMAGE=${IMAGE:-sl-uo-builder:bot}
cat > "$T/red-all-inner.sh" <<'INNER'
#!/usr/bin/env bash
cd /build/modernuo
U=Projects/UOContent
TT=Projects/UOContent.Tests/Tests
mkdir -p $U/ShardLamps $U/FestivalWagon $TT/P858
cp /m/t/Items/LampsAndWagonVerification.cs /m/t/Misc/RewardStoreVerification.cs $TT/P858/
rm -f $TT/Misc/RewardStoreVerification.cs
real() {
  cp /m/c/Items/Lights/ShardLamps.cs $U/ShardLamps/
  rm -f $U/FestivalWagon/*.cs; cp /m/c/FestivalWagon/*.cs $U/FestivalWagon/
  cp /m/c/RewardStores/AchievementStore.cs /m/c/RewardStores/FestivalStore.cs $U/RewardStores/
}
run() {
  echo "=================== $1"
  dotnet build Projects/UOContent.Tests/UOContent.Tests.csproj -c Release -v q > /tmp/b.txt 2>&1
  grep -E ' error |Build succeeded' /tmp/b.txt | sort -u | head -6
  dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-build \
    --filter "FullyQualifiedName~LampsAndWagonVerification|FullyQualifiedName~RewardStoreVerification" --logger 'console;verbosity=normal' > /tmp/t.txt 2>&1
  grep -E '^\s+Failed ShatteredLegacy' /tmp/t.txt | sort -u | sed 's/ \[.*//'
  grep -E '^\s+(Passed|Failed):' /tmp/t.txt | head -2
}
for d in /m/red/*/; do
  n=$(basename $d)
  real
  [ -f $d/ShardLamps.cs ] && cp $d/ShardLamps.cs $U/ShardLamps/
  [ -d $d/FestivalWagon ] && rm -f $U/FestivalWagon/*.cs && cp $d/FestivalWagon/*.cs $U/FestivalWagon/
  for f in AchievementStore.cs FestivalStore.cs; do [ -f $d/$f ] && cp $d/$f $U/RewardStores/; done
  run "RED $n"
done
real
run "GREEN (the real code)"
INNER
MSYS_NO_PATHCONV=1 docker run --rm --network=none --security-opt seccomp=unconfined -e MODE= \
  -v "$SL/customizations:/m/c:ro" -v "$SL/tests:/m/t:ro" -v "$T/red:/m/red:ro" \
  -v "$T/red-all-inner.sh:/m/inner.sh:ro" "$IMAGE" bash /m/inner.sh > "$T/red-all.txt" 2>&1
echo done
