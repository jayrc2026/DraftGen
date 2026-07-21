"""
DraftGen Test Launcher

Run this file from the KiCad Python Console.

Example:

exec(open(r"C:\Projects\DraftGen\run.py").read())
"""

import sys

PROJECT_ROOT = r"C:\Projects\DraftGen"

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# --------------------------------------------------
# Select which milestone to run
# --------------------------------------------------

TEST = "m1"

# --------------------------------------------------

if TEST == "m1":
    import tools.m1_board_test

elif TEST == "m2":
    import tools.m2_geometry_test

elif TEST == "m3":
    import tools.m3_footprint_test

elif TEST == "m4":
    import tools.m4_pad_test

elif TEST == "full":
    import tools.full_validation

else:
    print("Unknown test:", TEST)