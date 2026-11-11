#!/usr/bin/env bash
# cc-P857: every red copy in red/ (stub.cs, then each mutant), one container, a build and the facts per copy; then the
# real code again (green). Output: red-all.txt.
T=D:/UO/golems/Iron/shard-migration/notes/cc-P857-tools
SL=${SL:-D:/UO/golems/Iron/ShatteredLegacy/server}
IMAGE=${IMAGE:-sl-uo-builder:bot}
cat > "$T/red-all-inner.sh" <<'INNER'
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
INNER
MSYS_NO_PATHCONV=1 docker run --rm --network=none --security-opt seccomp=unconfined -e MODE= \
  -v "$SL/customizations/Items/Addons:/m/c:ro" -v "$SL/tests/Items/Addons:/m/t:ro" -v "$T/red:/m/red:ro" \
  -v "$T/red-all-inner.sh:/m/inner.sh:ro" "$IMAGE" bash /m/inner.sh > "$T/red-all.txt" 2>&1
echo done
