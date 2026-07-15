"""
DraftGen Diagnostics
"""

import sys
import platform
import importlib
import pcbnew

PROJECT_ROOT = r"C:\Projects\DraftGen"

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import draftgen.board
import draftgen.kicad_io

# Force reload during development
importlib.reload(draftgen.board)
importlib.reload(draftgen.kicad_io)

from draftgen.kicad_io import load_board_data


def separator():
    print("=" * 60)


separator()
print("DraftGen Diagnostics")
separator()

print("KiCad Version :", pcbnew.Version())
print("Python        :", sys.version.split()[0])
print("Platform      :", platform.system())
print()

board = load_board_data()

print("Project")
print("-" * 30)
print("Name           :", board.project_name)
print("File           :", board.filename)
print()

print("Board")
print("-" * 30)
print(f"Width          : {board.width:.2f} mm")
print(f"Height         : {board.height:.2f} mm")
print(f"Thickness      : {board.board_thickness:.2f} mm")
print()

print("Layers")
print("-" * 30)
print("Copper Layers  :", board.copper_layers)
print()

print("Objects")
print("-" * 30)
print("Footprints     :", board.footprint_count)
print("Tracks         :", board.track_count)
print("Vias           :", board.via_count)
print("Zones          :", board.zone_count)
print()

separator()
print("STATUS : READY")
separator()