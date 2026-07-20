"""
DraftGen Footprint Reader

Extracts all footprint information required for
assembly drawings, BOM generation and variants.
"""

import pcbnew

from draftgen.footprint import FootprintData


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
        # Future Containers
        # --------------------------------------------------

        data.pads = []

        data.variants = {}

        data.assembly = {}

        footprints.append(data)

    return footprints