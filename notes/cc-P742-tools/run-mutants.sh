#!/usr/bin/env bash
# cc-P742: runs TutorialVisionChamberVerification on each mutant (mutate742.py) and writes mutants.txt: the facts each
# mutant fails. Usage: run-mutants.sh <mutants folder>
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
M="$1"
OUT="$HERE/mutants.txt"
: > "$OUT"
for d in "$M"/*/; do
  name="$(basename "$d")"
  SRC="${d%/}" bash "$HERE/probe.sh" "FullyQualifiedName~TutorialVisionChamberVerification" > "$M/$name.log" 2>&1
  {
    echo "== $name"
    grep -E "error CS|^  Failed |Total tests|Passed:|Failed:" "$M/$name.log" | sed 's/ShatteredLegacy.Tests.TutorialVisionChamberVerification.//'
  } >> "$OUT"
done
echo DONE >> "$OUT"
