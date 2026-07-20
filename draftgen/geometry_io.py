"""
DraftGen Geometry Reader
"""

import pcbnew

from draftgen.geometry import (
    GeometryData,
    Point,
    Line,
    Arc,
    Circle,
    Rectangle,
    Polygon,
)


def mm(value):
    return pcbnew.ToMM(value)


def load_geometry():

    board = pcbnew.GetBoard()

    if board is None:
        raise RuntimeError("No board is currently open.")

    geometry = GeometryData()

    edge_layer = pcbnew.Edge_Cuts

    for drawing in board.GetDrawings():

        if drawing.GetLayer() != edge_layer:
            continue

        shape = drawing.GetShape()

        # ----------------------------
        # Line
        # ----------------------------
        if shape == pcbnew.SHAPE_T_SEGMENT:

            start = drawing.GetStart()
            end = drawing.GetEnd()

            geometry.lines.append(
                Line(
                    Point(mm(start.x), mm(start.y)),
                    Point(mm(end.x), mm(end.y)),
                )
            )

        # ----------------------------
        # Rectangle
        # ----------------------------
        elif shape == pcbnew.SHAPE_T_RECT:

            bbox = drawing.GetBoundingBox()

            geometry.rectangles.append(
                Rectangle(
                    mm(bbox.GetX()),
                    mm(bbox.GetY()),
                    mm(bbox.GetWidth()),
                    mm(bbox.GetHeight()),
                )
            )

        # ----------------------------
        # Circle
        # ----------------------------
        elif shape == pcbnew.SHAPE_T_CIRCLE:

            center = drawing.GetCenter()

            radius = drawing.GetRadius()

            geometry.circles.append(
                Circle(
                    Point(mm(center.x), mm(center.y)),
                    mm(radius),
                )
            )

        # ----------------------------
        # Arc
        # ----------------------------
        elif shape == pcbnew.SHAPE_T_ARC:

            center = drawing.GetCenter()

            geometry.arcs.append(
                Arc(
                    Point(mm(center.x), mm(center.y)),
                    mm(drawing.GetRadius()),
                    drawing.GetArcAngleStart().AsDegrees(),
                    drawing.GetArcAngleEnd().AsDegrees(),
                )
            )

        # ----------------------------
        # Polygon
        # ----------------------------
        elif shape == pcbnew.SHAPE_T_POLY:

            poly = Polygon()

            outline = drawing.GetPolyShape()

            for i in range(outline.OutlineCount()):

                contour = outline.COutline(i)

                for j in range(contour.PointCount()):

                    pt = contour.CPoint(j)

                    poly.points.append(
                        Point(mm(pt.x), mm(pt.y))
                    )

            geometry.polygons.append(poly)

    return geometry