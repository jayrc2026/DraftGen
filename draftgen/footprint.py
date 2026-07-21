"""
DraftGen Footprint Data Model
"""


class PadData:

    def __init__(self):

        # --------------------------------------------------
        # Identification
        # --------------------------------------------------

        self.number = ""
        self.name = ""
        self.uuid = ""

        # --------------------------------------------------
        # Electrical Information
        # --------------------------------------------------

        self.net = ""
        self.pin_function = ""
        self.pin_type = ""

        # --------------------------------------------------
        # Placement
        # --------------------------------------------------

        self.x = 0.0
        self.y = 0.0
        self.rotation = 0.0

        # --------------------------------------------------
        # Physical Information
        # --------------------------------------------------

        self.width = 0.0
        self.height = 0.0

        self.drill_x = 0.0
        self.drill_y = 0.0

        self.shape = ""

        # --------------------------------------------------
        # Manufacturing
        # --------------------------------------------------

        self.smd = False
        self.through_hole = False

        self.layers = []


class FootprintData:

    def __init__(self):

        # --------------------------------------------------
        # Basic Information
        # --------------------------------------------------

        self.reference = ""
        self.value = ""
        self.uuid = ""

        # --------------------------------------------------
        # Library Information
        # --------------------------------------------------

        self.library = ""
        self.footprint = ""
        self.library_description = ""
        self.keywords = ""

        # --------------------------------------------------
        # Placement
        # --------------------------------------------------

        self.x = 0.0
        self.y = 0.0
        self.rotation = 0.0
        self.side = ""

        # --------------------------------------------------
        # Manufacturing
        # --------------------------------------------------

        self.locked = False

        self.smd = False
        self.through_hole = False

        self.dnp = False
        self.exclude_bom = False
        self.exclude_pos = False

        # --------------------------------------------------
        # Physical Information
        # --------------------------------------------------

        self.pad_count = 0

        self.width = 0.0
        self.height = 0.0

        self.bounding_x = 0.0
        self.bounding_y = 0.0

        # --------------------------------------------------
        # Schematic Information
        # --------------------------------------------------

        self.sheet_name = ""
        self.sheet_file = ""

        # --------------------------------------------------
        # Documentation
        # --------------------------------------------------

        self.datasheet = ""
        self.description = ""

        # --------------------------------------------------
        # User Fields
        # --------------------------------------------------

        self.fields = {}

        # --------------------------------------------------
        # Pad Information
        # --------------------------------------------------

        self.pads = []

        # --------------------------------------------------
        # Future Expansion
        # --------------------------------------------------

        self.variants = {}

        self.assembly = {}