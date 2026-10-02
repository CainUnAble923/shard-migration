#!/usr/bin/env bash
# cc-P30 compile loop: restage from the trial copy, build, group errors. $1 = log name
set -uo pipefail
W=/d/UO/cc-p30-upgrade-work
bash /d/UO/shard-migration/notes/cc-P30-tools/stage-tree.sh /d/UO/ModernUO-upstream d4531cd94 $W/sl $W/stage > $W/stage-$1.log 2>&1 || { tail -30 $W/stage-$1.log; exit 1; }
grep -E 'All [0-9]+ patches|FAILED' $W/stage-$1.log
cp $W/nuget.config $W/stage/modernuo/nuget.config
cd $W/stage/modernuo && dotnet build ModernUO.slnx -c Release -clp:NoSummary -v:q > $W/$1.log 2>&1; echo "exit=$?" | tee -a $W/$1.log
python /d/UO/shard-migration/notes/cc-P30-tools/group_errors.py $W/$1.log
