"""cc-P688: the nightly checks (uobot.run) as the overnight runner runs them, with the client data read from the
tool-trials copy (uobot.run reads Cliloc.enu from D:\\ShatteredLegacy, another desk). Run from tools\\playtest-bot:
    python -B <this> <client data folder> <uobot.run's own arguments>
"""
import os
import sys

sys.path.insert(0, os.getcwd())
from uobot import run  # noqa: E402

run.CLIENT_DATA = sys.argv[1]
sys.exit(run.main(sys.argv[2:]))
