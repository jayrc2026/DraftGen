"""
DraftGen Board Data Model
"""


class BoardData:

    def __init__(self):

        self.filename = ""
        self.project_name = ""

        self.copper_layers = 0
        self.board_thickness = 0.0

        self.width = 0.0
        self.height = 0.0

        self.track_count = 0
        self.via_count = 0
        self.footprint_count = 0
        self.zone_count = 0