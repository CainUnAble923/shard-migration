#!/usr/bin/env bash
# cc-P806: each fix put back as it was, one at a time; each must turn a fact red. Logs in mutant-logs/.
cd /d/UO/golems/Iron/shard-migration/notes/cc-P806-tools
mkdir -p mutant-logs
F='FullyQualifiedName~NewHaven'
run() { M_NAME=$1 M_FILE=$2 M_SED=$3 bash mutant.sh "$F" > mutant-logs/$1.txt 2>&1; }
run m1-old-bench-stays NewHavenLessons.cs 's/moved743 \+= TakeAwayOldBench\(map, dryRun\);//'
run m2-rook-not-turned NewHavenLessons.cs 's/ \|\| TurnRook\(dryRun\)//'
run m3-crosswise-piece NewHavenLessons.cs 's/RookBenchId = 0x0B2D/RookBenchId = 0x0B2C/'
run m4-rook-faces-north HavenSpots.cs 's/RookFacing = Direction\.South/RookFacing = Direction.North/'
run m5-echo-under-canopy NewHavenLessons.cs 's/BardEchoA = new\(3412, 2604, 60\)/BardEchoA = new(3410, 2603, 60)/'
run m6-bucket-behind-wall NewHavenLessons.cs 's/new Point3D\(3534, 2574, 8\), "bucket/new Point3D(3535, 2575, 7), "bucket/'
run m7-mine-sign-old-spot NewHavenLessons.cs 's/new Point3D\(3469, 2624, 0\), "To the mine/new Point3D(3477, 2617, 0), "To the mine/'
run m8-stop1-sign-far NewHavenLessons.cs 's/Ground\(3468, 2591\)/Ground(3465, 2596)/'
echo ALLDONE > mutant-logs/done.txt
