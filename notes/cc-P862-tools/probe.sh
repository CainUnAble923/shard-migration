#!/usr/bin/env bash
# cc-P862: one container on the builder image (main at P861): copy Battle Chess (server/customizations/BattleChess) and its
# facts in, build UOContent.Tests, run BattleChessVerification. With MUTANT=<file> (from red/), that file replaces the
# real one of the same name first. Output: probe-<label>.txt next to this script.
#   bash probe.sh [label] [mutant-file]
T=D:/UO/golems/Iron/shard-migration/notes/cc-P862-tools
SL=${SL:-D:/UO/golems/Iron/ShatteredLegacy/server}
IMAGE=${IMAGE:-sl-uo-builder:cc-p861}
LABEL=${1:-green}
MUTANT=${2:-}
cat > "$T/probe-inner.sh" <<'INNER'
#!/usr/bin/env bash
cd /build/modernuo
U=Projects/UOContent
mkdir -p $U/BattleChess Projects/UOContent.Tests/Tests/Misc
cp /m/c/*.cs $U/BattleChess/
if [ -n "$MUTANT" ]; then cp "/m/red/$MUTANT" "$U/BattleChess/${MUTANT#*__}"; echo "mutant: $MUTANT"; fi
if [ -z "$NOTESTFILE" ]; then cp /m/t/BattleChessVerification.cs Projects/UOContent.Tests/Tests/Misc/; fi
if [ -n "$NOCODE" ]; then rm -rf $U/BattleChess; echo "no Battle Chess code (before the change)"; fi
dotnet build Projects/UOContent.Tests/UOContent.Tests.csproj -c Release -v q > /tmp/b.txt 2>&1
grep -E " (error|warning) [A-Z]+[0-9]+" /tmp/b.txt | sed -E 's# \[/build[^]]*\]$##; s#^.*/Projects/##' | grep -v ' warning ' | sort -u | head -40
grep -E 'Build succeeded|Build FAILED' /tmp/b.txt | head -2
grep -qE 'Build succeeded' /tmp/b.txt || exit 0
dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-build \
  --filter "FullyQualifiedName~BattleChessVerification" --logger 'console;verbosity=normal' > /tmp/t.txt 2>&1
grep -E '^\s+(Passed|Failed) ShatteredLegacy' /tmp/t.txt | sort -u | sed 's/ \[.*//'
grep -B2 -A14 'Failed ShatteredLegacy' /tmp/t.txt | grep -vE '^\s*$' | head -80
grep -E '^\s+(Passed|Failed|Total tests):' /tmp/t.txt | head -3
INNER
MSYS_NO_PATHCONV=1 docker run --rm --network=none --security-opt seccomp=unconfined -e MODE= -e MUTANT="$MUTANT" \
  -e NOCODE="$NOCODE" -e NOTESTFILE="$NOTESTFILE" \
  -v "$SL/customizations/BattleChess:/m/c:ro" -v "$SL/tests/Misc:/m/t:ro" -v "$T/red:/m/red:ro" \
  -v "$T/probe-inner.sh:/m/inner.sh:ro" "$IMAGE" bash /m/inner.sh > "$T/probe-$LABEL.txt" 2>&1
echo "done: $T/probe-$LABEL.txt"
