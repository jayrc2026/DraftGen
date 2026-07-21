"""
DraftGen M1 - Board Reader Test

Validates the Board Data Reader.

Milestone:
M1 - Board Information
"""
import os
import sys

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))

if TOOLS_DIR not in sys.path:
    sys.path.insert(0, TOOLS_DIR)

from common import *

banner("DraftGen M1 - Board Reader")

print_environment()

# ----------------------------------------------------------
# Load Board
# ----------------------------------------------------------

board = load_board_data()

# ----------------------------------------------------------
# Project
# ----------------------------------------------------------

section("Project")

print(f"Name            : {board.project_name}")
print(f"File            : {board.filename}")

blank()

# ----------------------------------------------------------
# Board Dimensions
# ----------------------------------------------------------

section("Board")

print(f"Width           : {board.width:.2f} mm")
print(f"Height          : {board.height:.2f} mm")
print(f"Thickness       : {board.board_thickness:.2f} mm")

blank()

# ----------------------------------------------------------
# Layer Information
# ----------------------------------------------------------

section("Layers")

print(f"Copper Layers   : {board.copper_layers}")

blank()

# ----------------------------------------------------------
# Object Counts
# ----------------------------------------------------------

section("Objects")

print(f"Footprints      : {board.footprint_count}")
print(f"Tracks          : {board.track_count}")
print(f"Vias            : {board.via_count}")
print(f"Zones           : {board.zone_count}")

blank()

# ----------------------------------------------------------
# Validation
# ----------------------------------------------------------

section("Validation")

errors = 0

if board.width > 0:
    pass_msg("Board width detected")
else:
    fail_msg("Invalid board width")
    errors += 1

if board.height > 0:
    pass_msg("Board height detected")
else:
    fail_msg("Invalid board height")
    errors += 1

if board.board_thickness > 0:
    pass_msg("Board thickness detected")
else:
    fail_msg("Invalid board thickness")
    errors += 1

if board.copper_layers > 0:
    pass_msg("Copper layers detected")
else:
    fail_msg("No copper layers found")
    errors += 1

if board.footprint_count >= 0:
    pass_msg("Footprint count available")
else:
    fail_msg("Invalid footprint count")
    errors += 1

blank()

# ----------------------------------------------------------
# Final Status
# ----------------------------------------------------------

if errors == 0:
    status_ready()
else:
    status_failed()