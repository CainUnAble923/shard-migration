#!/usr/bin/env bash
# cc-P820: the clean run, then each mutant in red/ (one container each). Output: probe-clean.txt, red-<mutant>.txt.
cd "$(dirname "$0")"
bash probe.sh > probe-clean.txt 2>&1
for m in old-layout crate-in-corner no-retire new-crate; do
  RED=$m FILTER='FullyQualifiedName~TutorialJailVerification' bash probe.sh > red-$m.txt 2>&1
done
echo finished > probe-all.done
