#!/usr/bin/env bash
# cc-P802 (P817's run-facts.sh): a throwaway container from main's builder image (sl-uo-builder:cc-P813, this branch's base)
# for quick compile checks and red/green runs; the gate is the gated build.
#   run-facts.sh <log> green|red [filter]
#   green: every file this prompt changed, as they are.
#   red:   the same files with mutate.sh run over them, which turns each new behaviour off (one sed each), so every P802
#          fact is watched failing against the real code, not a stub.
set -u
LOG="$1"; WHICH_="$2"; FILTER="${3:-FullyQualifiedName~P802_}"
IMG=sl-uo-builder:cc-P813
S=D:/UO/golems/Iron/ShatteredLegacy/server
T=D:/UO/golems/Iron/shard-migration/notes/cc-P802-tools
(cd D:/UO/golems/Iron/ShatteredLegacy && git status --short --untracked-files=all | sed "s/^...//") > "$T/changed.txt"
MSYS_NO_PATHCONV=1 docker run --rm --network=none --security-opt seccomp=unconfined -e MODE= -e FILTER="$FILTER" -e WHICH="$WHICH_" \
  -v "$S/customizations:/m/c:ro" -v "$S/tests:/m/t:ro" -v "$S/patches:/m/p:ro" -v "$T:/m/tools:ro" "$IMG" bash -c 'cd /build/modernuo
U=Projects/UOContent
TT=Projects/UOContent.Tests/Tests
# where the image keeps our customizations: find each changed file by name and copy ours over it
for f in $(grep "^server/customizations/.*\.cs$" /m/tools/changed.txt | sed "s#^server/customizations/#./#"); do
  dest=$(find $U -name "$(basename $f)" -path "*$(basename $(dirname $f))*" | head -1)
  [ -z "$dest" ] && dest=$U/$(dirname $f | sed "s#^\./##")/$(basename $f) && mkdir -p $(dirname $dest)
  cp /m/c/$f "$dest"
done
for f in $(grep "^server/tests/.*\.cs$" /m/tools/changed.txt | sed "s#^server/tests/#./#"); do mkdir -p $TT/$(dirname $f); cp /m/t/$f $TT/$f; done
# the patched Account.cs: our patch line, applied to the pinned file as apply-patches.sh does
grep -q "ClusterFYoungPlayer.SendLoginMessage" $U/Accounting/Account.cs || sed -i "s#pm.SendAsciiMessage(ClusterFYoungPlayer.LoginMessage(ts));#ClusterFYoungPlayer.SendLoginMessage(pm, ts);#" $U/Accounting/Account.cs
if [ "$WHICH" = red ]; then bash /m/tools/mutate.sh $U; fi
dotnet build Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore -v q 2>&1 | grep -E " error " | sort -u | head -40
dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-build --filter "$FILTER" --logger "console;verbosity=normal" 2>&1 | grep -v warning' > "$LOG" 2>&1
grep -a -E '^\s*(Passed|Failed|Total tests):|^\s+Failed | error |Assert\.|Expected:|Actual:|Exception :' "$LOG" | sed -E 's/\[\/build.*//' | cut -c1-220 | head -80
