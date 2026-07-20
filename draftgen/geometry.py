"""
DraftGen Geometry Model

Stores geometry in DraftGen's own format.
All dimensions are stored in millimeters.
"""

from dataclasses import dataclass, field


@dataclass
class Point:
    x: float
    y: float


@dataclass
class Line:
    start: Point
    end: Point


@dataclass
class Arc:
    center: Point
    radius: float
    start_angle: float
    end_angle: float


@dataclass
class Circle:
    center: Point
    radius: float


@dataclass
class Rectangle:
    x: float
    y: float
    width: float
    height: float


@dataclass
class Polygon:
    points: list[Point] = field(default_factory=list)


class GeometryData:

    def __init__(self):

        self.lines = []
        self.arcs = []
        self.circles = []
        self.rectangles = []
        self.polygons = []

    @property
    def line_count(self):
        return len(self.lines)

    @property
    def arc_count(self):
        return len(self.arcs)

    @property
    def circle_count(self):
        return len(self.circles)

    @property
    def rectangle_count(self):
        return len(self.rectangles)

    @property
    def polygon_count(self):
        return len(self.polygons)