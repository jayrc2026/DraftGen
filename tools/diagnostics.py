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
import draftgen.footprint
import draftgen.footprint_io

importlib.reload(draftgen.board)
importlib.reload(draftgen.kicad_io)
importlib.reload(draftgen.geometry)
importlib.reload(draftgen.geometry_io)
importlib.reload(draftgen.footprint)
importlib.reload(draftgen.footprint_io)

from draftgen.kicad_io import load_board_data
from draftgen.geometry_io import load_geometry
from draftgen.footprint_io import load_footprints


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
# Footprints
# ----------------------------------------------------------

footprints = load_footprints()

print("Footprints")
print("-" * 30)
print("Total          :", len(footprints))
print()

for fp in footprints[:10]:

    print("Reference      :", fp.reference)
    print("Value          :", fp.value)
    print("UUID           :", fp.uuid)
    print()

    print("Library")
    print("--------------")
    print("Library        :", fp.library)
    print("Footprint      :", fp.footprint)
    print("Description    :", fp.library_description)
    print("Keywords       :", fp.keywords)
    print()

    print("Placement")
    print("--------------")
    print(f"Position       : ({fp.x:.2f}, {fp.y:.2f}) mm")
    print(f"Rotation       : {fp.rotation:.2f}°")
    print("Side           :", fp.side)
    print("Locked         :", fp.locked)
    print()

    print("Manufacturing")
    print("--------------")
    print("Pad Count      :", fp.pad_count)
    print("SMD            :", fp.smd)
    print("Through Hole   :", fp.through_hole)
    print("DNP            :", fp.dnp)
    print("Exclude BOM    :", fp.exclude_bom)
    print("Exclude POS    :", fp.exclude_pos)
    print()

    print("Bounding Box")
    print("--------------")
    print(f"Origin         : ({fp.bounding_x:.2f}, {fp.bounding_y:.2f}) mm")
    print(f"Width          : {fp.width:.2f} mm")
    print(f"Height         : {fp.height:.2f} mm")
    print()

    print("Schematic")
    print("--------------")
    print("Sheet Name     :", fp.sheet_name)
    print("Sheet File     :", fp.sheet_file)
    print()

    print("Documentation")
    print("--------------")
    print("Datasheet      :", fp.datasheet)
    print("Description    :", fp.description)
    print()

    print("Fields")
    print("--------------")

    if fp.fields:

        for name, value in fp.fields.items():
            print(f"{name:<20}: {value}")

    else:
        print("None")

    print()
    print("-" * 60)

# ----------------------------------------------------------
# Pad Extraction Summary
# ----------------------------------------------------------

print()
print("Pad Extraction")
print("-" * 30)

total_pads = 0
footprints_with_pads = 0
footprints_without_pads = 0

for fp in footprints:

    total_pads += len(fp.pads)

    if fp.pads:
        footprints_with_pads += 1
    else:
        footprints_without_pads += 1

print(f"Total Pads         : {total_pads}")
print(f"Footprints w/Pads  : {footprints_with_pads}")
print(f"No Pad Footprints  : {footprints_without_pads}")
print()

# ----------------------------------------------------------
# Sample Pad Data
# ----------------------------------------------------------

print("Sample Pad Data")
print("-" * 30)

sample = None

for fp in footprints:
    if fp.pads:
        sample = fp
        break

if sample is None:

    print("No pads extracted.")

else:

    print(f"Reference : {sample.reference}")
    print(f"Value     : {sample.value}")
    print()

    for pad in sample.pads[:5]:

        print(f"Pad {pad.number}")
        print(f"Net        : {pad.net}")
        print(f"Position   : ({pad.x:.2f}, {pad.y:.2f}) mm")
        print(f"Size       : {pad.width:.2f} x {pad.height:.2f} mm")
        print(f"Shape      : {pad.shape}")
        print(f"SMD        : {pad.smd}")
        print(f"PTH        : {pad.through_hole}")
        print(f"Layers     : {', '.join(pad.layers)}")
        print()

# ----------------------------------------------------------
# Pad Validation
# ----------------------------------------------------------

print("Pad Validation")
print("-" * 30)

missing_numbers = []
missing_size = []
missing_layers = []
pad_count_errors = []

for fp in footprints:

    if len(fp.pads) != fp.pad_count:
        pad_count_errors.append(fp.reference)

    for pad in fp.pads:

        if pad.number == "":
            missing_numbers.append((fp.reference, pad))

        if pad.width <= 0 or pad.height <= 0:
            missing_size.append((fp.reference, pad.number))

        if len(pad.layers) == 0:
            missing_layers.append((fp.reference, pad.number))

if not missing_numbers:
    print("PASS : Every pad has a number.")
else:
    print(f"FAIL : {len(missing_numbers)} pads missing numbers.")

if not missing_size:
    print("PASS : Every pad has valid dimensions.")
else:
    print(f"FAIL : {len(missing_size)} pads missing size.")

if not missing_layers:
    print("PASS : Every pad belongs to at least one layer.")
else:
    print(f"FAIL : {len(missing_layers)} pads missing layers.")

if not pad_count_errors:
    print("PASS : Footprint pad counts match extracted pads.")
else:
    print("FAIL : Pad count mismatch:")
    for ref in pad_count_errors:
        print("   ", ref)

print()

# ----------------------------------------------------------
# DNP Validation
# ----------------------------------------------------------

print("DNP Components")
print("-" * 30)

dnp_parts = [fp for fp in footprints if fp.dnp]

if not dnp_parts:

    print("No DNP components found.")

else:

    for fp in dnp_parts:

        print(f"{fp.reference:<10} {fp.value:<20} UUID={fp.uuid}")

print()

# ----------------------------------------------------------
# UUID Validation
# ----------------------------------------------------------

print("UUID Validation")
print("-" * 30)

missing_uuid = [fp.reference for fp in footprints if not fp.uuid]

if not missing_uuid:

    print("PASS : All footprints have UUIDs.")

else:

    print("FAIL : Missing UUIDs")

    for ref in missing_uuid:
        print(ref)

print()

separator()
print("STATUS : READY")
separator()