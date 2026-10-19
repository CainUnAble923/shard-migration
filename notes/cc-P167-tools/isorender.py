"""cc-P181: isorender moved to scripts/mapbuild/isorender.py (the general renderer); this shim keeps the old import
and command line working for the Rootdeep scripts and notes that name it."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'scripts'))
from mapbuild.isorender import *  # noqa: F401,F403,E402
from mapbuild import isorender as _iso  # noqa: E402

if __name__ == '__main__':
    sys.argv[0] = _iso.__file__
    exec(open(_iso.__file__, encoding='utf-8').read().split("if __name__ == '__main__':")[1].replace('\n    ', '\n'), vars(_iso))
