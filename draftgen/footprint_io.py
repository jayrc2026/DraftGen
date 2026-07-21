"""
DraftGen Footprint Reader

Extracts all footprint information required for
assembly drawings, BOM generation and variants.
"""

import pcbnew

from draftgen.footprint import FootprintData, PadData


def load_footprints():

    board = pcbnew.GetBoard()

    if board is None:
        raise RuntimeError("No board is currently open.")

    footprints = []

    for fp in board.GetFootprints():

        data = FootprintData()

        # --------------------------------------------------
        # Basic Information
        # --------------------------------------------------

        data.reference = fp.GetReference()
        data.value = fp.GetValue()

        # UUID
        try:
            data.uuid = fp.m_Uuid.AsString()
        except Exception:
            try:
                data.uuid = str(fp.GetPath())
            except Exception:
                data.uuid = ""

        # --------------------------------------------------
        # Library Information
        # --------------------------------------------------

        try:
            libid = fp.GetFPID()

            data.library = libid.GetLibNickname()
            data.footprint = libid.GetLibItemName()

        except Exception:

            data.library = ""
            data.footprint = ""

        try:
            data.library_description = fp.GetLibDescription()
        except Exception:
            data.library_description = ""

        try:
            data.keywords = fp.GetKeywords()
        except Exception:
            data.keywords = ""

        # --------------------------------------------------
        # Placement
        # --------------------------------------------------

        position = fp.GetPosition()

        data.x = pcbnew.ToMM(position.x)
        data.y = pcbnew.ToMM(position.y)

        data.rotation = fp.GetOrientationDegrees()

        if fp.IsFlipped():
            data.side = "Bottom"
        else:
            data.side = "Top"

        # --------------------------------------------------
        # Manufacturing
        # --------------------------------------------------

        data.locked = fp.IsLocked()

        data.pad_count = fp.GetPadCount()

        data.smd = False
        data.through_hole = False

        for pad in fp.Pads():

            try:

                attribute = pad.GetAttribute()

                if attribute == pcbnew.PAD_ATTRIB_SMD:
                    data.smd = True

                elif attribute == pcbnew.PAD_ATTRIB_PTH:
                    data.through_hole = True

            except Exception:
                pass

        data.dnp = fp.IsDNP()
        data.exclude_bom = fp.IsExcludedFromBOM()
        data.exclude_pos = fp.IsExcludedFromPosFiles()

        # --------------------------------------------------
        # Physical Information
        # --------------------------------------------------

        bbox = fp.GetBoundingBox()

        data.bounding_x = pcbnew.ToMM(bbox.GetX())
        data.bounding_y = pcbnew.ToMM(bbox.GetY())

        data.width = pcbnew.ToMM(bbox.GetWidth())
        data.height = pcbnew.ToMM(bbox.GetHeight())

        # --------------------------------------------------
        # Schematic Information
        # --------------------------------------------------

        try:
            data.sheet_name = fp.GetSheetname()
        except Exception:
            data.sheet_name = ""

        try:
            data.sheet_file = fp.GetSheetfile()
        except Exception:
            data.sheet_file = ""

        # --------------------------------------------------
        # User Fields
        # --------------------------------------------------

        data.fields = {}

        try:

            for field in fp.GetFields():

                name = field.GetName()
                value = field.GetText()

                data.fields[name] = value

        except Exception:
            pass

        # --------------------------------------------------
        # Standard Documentation
        # --------------------------------------------------

        data.datasheet = data.fields.get("Datasheet", "")
        data.description = data.fields.get("Description", "")

        # --------------------------------------------------
        # Pad Extraction (M4)
        # --------------------------------------------------

        data.pads = []

        for pad in fp.Pads():

            p = PadData()

            # ----------------------------------------------
            # Identification
            # ----------------------------------------------

            p.number = pad.GetNumber()

            try:
                p.name = pad.GetName()
            except Exception:
                p.name = ""

            # Future support
            p.uuid = ""

            # ----------------------------------------------
            # Electrical
            # ----------------------------------------------

            try:
                p.net = pad.GetNetname()
            except Exception:
                p.net = ""

            try:
                p.pin_function = pad.GetPinFunction()
            except Exception:
                p.pin_function = ""

            try:
                p.pin_type = pad.GetPinType()
            except Exception:
                p.pin_type = ""

            # ----------------------------------------------
            # Placement
            # ----------------------------------------------

            pos = pad.GetPosition()

            p.x = pcbnew.ToMM(pos.x)
            p.y = pcbnew.ToMM(pos.y)

            try:
                p.rotation = pad.GetOrientation().AsDegrees()
            except Exception:
                try:
                    p.rotation = pad.GetOrientationDegrees()
                except Exception:
                    p.rotation = 0.0

            # ----------------------------------------------
            # Physical
            # ----------------------------------------------

            size = pad.GetSize()

            p.width = pcbnew.ToMM(size.x)
            p.height = pcbnew.ToMM(size.y)

            drill = pad.GetDrillSize()

            p.drill_x = pcbnew.ToMM(drill.x)
            p.drill_y = pcbnew.ToMM(drill.y)

            # ----------------------------------------------
            # Shape
            # ----------------------------------------------

            try:
                p.shape = str(pad.GetShape())
            except Exception:
                p.shape = ""

            # ----------------------------------------------
            # Manufacturing
            # ----------------------------------------------

            attr = pad.GetAttribute()

            p.smd = attr == pcbnew.PAD_ATTRIB_SMD
            p.through_hole = attr == pcbnew.PAD_ATTRIB_PTH

            # ----------------------------------------------
            # Layers
            # ----------------------------------------------

            p.layers = []

            try:
                layer_set = pad.GetLayerSet()

                for layer in range(board.GetCopperLayerCount() + 32):

                    try:
                        if layer_set.Contains(layer):
                            p.layers.append(board.GetLayerName(layer))
                    except Exception:
                        pass

            except Exception:
                pass

            data.pads.append(p)

        # --------------------------------------------------
        # Future Containers
        # --------------------------------------------------

        data.variants = {}

        data.assembly = {}

        footprints.append(data)

    return footprints

# --------------------------------------------------
# Validation Helpers
# --------------------------------------------------

def validate_footprints(footprints):

    report = {
        "total_pads": 0,
        "footprints_with_pads": 0,
        "footprints_without_pads": 0,
        "missing_pad_numbers": [],
        "invalid_pad_size": [],
        "missing_layers": [],
        "pad_count_errors": []
    }

    for fp in footprints:

        if len(fp.pads) == 0:
            report["footprints_without_pads"] += 1
        else:
            report["footprints_with_pads"] += 1

        report["total_pads"] += len(fp.pads)

        electrical = not (
            fp.exclude_bom or
            fp.exclude_pos or
            fp.reference.startswith("G") or
            fp.reference.startswith("M") or
            fp.reference.startswith("FD")
        )

        for pad in fp.pads:

            if electrical:

                if pad.number == "":
                    report["missing_pad_numbers"].append(
                        (fp.reference, pad)
                    )

            if pad.width <= 0 or pad.height <= 0:

                report["invalid_pad_size"].append(
                    (fp.reference, pad)
                )

            if len(pad.layers) == 0:

                report["missing_layers"].append(
                    (fp.reference, pad)
                )

        if fp.pad_count != len(fp.pads):

            report["pad_count_errors"].append(fp.reference)

    return report