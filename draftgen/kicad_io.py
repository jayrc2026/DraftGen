"""
DraftGen KiCad I/O

Reads information from the currently opened KiCad PCB.
"""

import os
import pcbnew

from draftgen.board import BoardData


def load_board_data():

    board = pcbnew.GetBoard()

    if board is None:
        raise RuntimeError("No board is currently open.")

    data = BoardData()

    # ----------------------------------------------------------
    # Project Information
    # ----------------------------------------------------------

    data.filename = board.GetFileName()

    data.project_name = os.path.splitext(
        os.path.basename(data.filename)
    )[0]

    # ----------------------------------------------------------
    # Board Information
    # ----------------------------------------------------------

    data.copper_layers = board.GetCopperLayerCount()

    # Convert KiCad internal units to mm
    thickness = board.GetDesignSettings().GetBoardThickness()
    data.board_thickness = pcbnew.ToMM(thickness)

    bbox = board.GetBoardEdgesBoundingBox()

    data.width = pcbnew.ToMM(bbox.GetWidth())
    data.height = pcbnew.ToMM(bbox.GetHeight())

    # ----------------------------------------------------------
    # Statistics
    # ----------------------------------------------------------

    tracks = list(board.GetTracks())

    data.track_count = len(tracks)

    data.via_count = sum(
        1 for t in tracks if isinstance(t, pcbnew.PCB_VIA)
    )

    data.footprint_count = len(list(board.GetFootprints()))

    data.zone_count = board.GetAreaCount()

    return data