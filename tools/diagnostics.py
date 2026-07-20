"""
DraftGen Diagnostics

Verifies that DraftGen can communicate with KiCad and
prints all extracted information.
"""

import sys
import platform
import importlib
import pcbnew

# ----------------------------------------------------------
# Add DraftGen project to Python path
# ----------------------------------------------------------

PROJECT_ROOT = r"C:\Projects\DraftGen"

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# ----------------------------------------------------------
# Import DraftGen modules
# ----------------------------------------------------------

import draftgen.board
import draftgen.kicad_io
import draftgen.geometry
import draftgen.geometry_io

importlib.reload(draftgen.board)
importlib.reload(draftgen.kicad_io)
importlib.reload(draftgen.geometry)
importlib.reload(draftgen.geometry_io)

from draftgen.kicad_io import load_board_data
from draftgen.geometry_io import load_geometry


def separator():
    print("=" * 60)


separator()
print("DraftGen Diagnostics")
separator()

print("KiCad Version :", pcbnew.Version())
print("Python        :", sys.version.split()[0])
print("Platform      :", platform.system())
print()

# ----------------------------------------------------------
# Board Information
# ----------------------------------------------------------

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

# ----------------------------------------------------------
# Geometry Information
# ----------------------------------------------------------

geometry = load_geometry()

print("Geometry Summary")
print("-" * 30)
print("Lines          :", geometry.line_count)
print("Arcs           :", geometry.arc_count)
print("Circles        :", geometry.circle_count)
print("Rectangles     :", geometry.rectangle_count)
print("Polygons       :", geometry.polygon_count)
print()

# ----------------------------------------------------------
# Rectangle Details
# ----------------------------------------------------------

if geometry.rectangles:

    print("Rectangle Details")
    print("-" * 30)

    for i, rect in enumerate(geometry.rectangles, start=1):

        print(f"Rectangle #{i}")
        print(f"Origin X       : {rect.x:.2f} mm")
        print(f"Origin Y       : {rect.y:.2f} mm")
        print(f"Width          : {rect.width:.2f} mm")
        print(f"Height         : {rect.height:.2f} mm")
        print()

# ----------------------------------------------------------
# Line Details
# ----------------------------------------------------------

if geometry.lines:

    print("Line Details")
    print("-" * 30)

    for i, line in enumerate(geometry.lines, start=1):

        print(f"Line #{i}")
        print(
            f"Start          : ({line.start.x:.2f}, {line.start.y:.2f}) mm"
        )
        print(
            f"End            : ({line.end.x:.2f}, {line.end.y:.2f}) mm"
        )
        print()

# ----------------------------------------------------------
# Circle Details
# ----------------------------------------------------------

if geometry.circles:

    print("Circle Details")
    print("-" * 30)

    for i, circle in enumerate(geometry.circles, start=1):

        print(f"Circle #{i}")
        print(
            f"Center         : ({circle.center.x:.2f}, {circle.center.y:.2f}) mm"
        )
        print(f"Radius         : {circle.radius:.2f} mm")
        print()

# ----------------------------------------------------------
# Arc Details
# ----------------------------------------------------------

if geometry.arcs:

    print("Arc Details")
    print("-" * 30)

    for i, arc in enumerate(geometry.arcs, start=1):

        print(f"Arc #{i}")
        print(
            f"Center         : ({arc.center.x:.2f}, {arc.center.y:.2f}) mm"
        )
        print(f"Radius         : {arc.radius:.2f} mm")
        print(f"Start Angle    : {arc.start_angle:.2f}°")
        print(f"End Angle      : {arc.end_angle:.2f}°")
        print()

# ----------------------------------------------------------

separator()
print("STATUS : READY")
separator()