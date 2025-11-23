"""
birdhouse — generate and export CAD geometry for a simple laser-cut birdhouse.

This module builds CadQuery solids for a simple birdhouse (front, back and side
plates), applies connector cutouts and entrance holes, exports 2D DXF files for
laser cutting, and displays the parts in the ocp_vscode viewer.

Primary outputs / side effects:
- Creates CadQuery solids: front_plate, back_plate, side_plate, side_plate2.
- Exports DXF files to: construction_files/front_plate.dxf,
  construction_files/side_plate.dxf, construction_files/back_plate.dxf.
- Calls show_object(...) to display parts in the ocp_vscode viewer.

Key behavior and dependencies:
- Uses constants from constants.py: WALLTHICKNESS, BIRDHOUSE_WIDTH,
  BIRDHOUSE_DEPTH, BIRDHOUSE_HEIGHT, BIRDHOUSE_SPACE_TOP, BIRDHOUSE_SPACE_BOTTOM.
- Uses distribute_connectors(length) from connectors.py to generate connector
  cutouts. Connector geometry assumes spacing and sizes based on WALLTHICKNESS.
- Units are those used in constants.py (typically millimeters).
- Intended for simple prototyping and DXF export for laser cutting; geometry may
  need adjustment for other manufacturing tolerances.

Notes:
- Running this module will produce files and viewer output as described above.
- To change layout or spacing, modify the constants or the connector logic in
  connectors.py.
"""

from cadquery import cq, exporters

from ocp_vscode import show_object

from connectors import distribute_connectors
from constants import (
    WALLTHICKNESS,
    BIRDHOUSE_WIDTH,
    BIRDHOUSE_DEPTH,
    BIRDHOUSE_WIDTH_INNER,
    BIRDHOUSE_SPACE_BOTTOM,
    SLIDE_LENGTH_MID,
    SLIDE_LENGTH_TOP,
    SLIDE_LENGTH_BOTTOM,
    SLIDE_ANGLE,
    FRONT_PLATE_HEIGHT_SIDE,
    FRONT_PLATE_HEIGHT_MIDDLE,
    BACK_PLATE_HEIGHT,
    SIDE_PLATE_HEIGHT,
    ROOF_LENGTH,
)

# Create front plate with entrance holes
front_plate = (
    cq.Workplane("XZ")
    .lineTo(0, FRONT_PLATE_HEIGHT_SIDE)
    .lineTo(-WALLTHICKNESS, FRONT_PLATE_HEIGHT_SIDE)
    .lineTo(BIRDHOUSE_WIDTH_INNER / 2, FRONT_PLATE_HEIGHT_MIDDLE)
    .lineTo(BIRDHOUSE_WIDTH_INNER + WALLTHICKNESS, FRONT_PLATE_HEIGHT_SIDE)
    .lineTo(BIRDHOUSE_WIDTH_INNER, FRONT_PLATE_HEIGHT_SIDE)
    .lineTo(BIRDHOUSE_WIDTH_INNER, 0)
    .close()
    .moveTo(BIRDHOUSE_WIDTH_INNER / 2, FRONT_PLATE_HEIGHT_MIDDLE * 0.5)
    .circle(BIRDHOUSE_WIDTH_INNER / 6)
    .moveTo(BIRDHOUSE_WIDTH_INNER / 2, FRONT_PLATE_HEIGHT_MIDDLE * 0.75)
    .circle(BIRDHOUSE_WIDTH_INNER / 6)
    .extrude(WALLTHICKNESS)
)

# add connectors to front plate
front_plate_connectors = distribute_connectors(FRONT_PLATE_HEIGHT_SIDE).rotate(
    (0, 0, 0), (1, 0, 0), 90
)
front_plate = front_plate + front_plate_connectors
front_plate = front_plate + front_plate_connectors.translate(
    (BIRDHOUSE_WIDTH_INNER, 0, 0)
)
front_plate = front_plate.translate(
    (WALLTHICKNESS, WALLTHICKNESS, BIRDHOUSE_SPACE_BOTTOM)
)


# Create back plate
back_plate = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(0, BACK_PLATE_HEIGHT)
    .lineTo(BIRDHOUSE_WIDTH_INNER, BACK_PLATE_HEIGHT)
    .lineTo(BIRDHOUSE_WIDTH_INNER, 0)
    .close()
    .extrude(WALLTHICKNESS)
)
# add connectors to side plate
back_plate_connectors = distribute_connectors(FRONT_PLATE_HEIGHT_SIDE).rotate(
    (0, 0, 0), (1, 0, 0), 90
)
back_plate = back_plate + back_plate_connectors
back_plate = back_plate + back_plate_connectors.translate((BIRDHOUSE_WIDTH_INNER, 0, 0))
back_plate = back_plate.translate((WALLTHICKNESS, BIRDHOUSE_DEPTH, 0))

# Create side plates
side_plate = (
    cq.Workplane("YZ")
    .lineTo(0, SIDE_PLATE_HEIGHT)
    .lineTo(BIRDHOUSE_DEPTH, SIDE_PLATE_HEIGHT)
    .lineTo(BIRDHOUSE_DEPTH, 0)
    .close()
    .extrude(WALLTHICKNESS)
)


# Create bottom slide
bottom_slide = (
    cq.Workplane("XY")
    .rect(BIRDHOUSE_WIDTH_INNER, SLIDE_LENGTH_BOTTOM, centered=False)
    .extrude(WALLTHICKNESS)
)

# add connectors to bottom slide
bottom_slide_connectors = distribute_connectors(SLIDE_LENGTH_BOTTOM, start=0)
bottom_slide = bottom_slide + bottom_slide_connectors
bottom_slide = bottom_slide + bottom_slide_connectors.translate(
    (BIRDHOUSE_WIDTH_INNER, 0, 0)
)

exporters.export(bottom_slide, "construction_files/bottom_slide.dxf")

# rotate and translate bottom slide to final position
bottom_slide = bottom_slide.rotate(
    (0, 0, 0),
    (1, 0, 0),
    SLIDE_ANGLE,
).translate((WALLTHICKNESS, 0, 0))


# Create mid slide
mid_slide = (
    cq.Workplane("XY")
    .rect(BIRDHOUSE_WIDTH_INNER, SLIDE_LENGTH_MID, centered=False)
    .extrude(WALLTHICKNESS)
)

# add connectors to mid slide
mid_slide_connectors = distribute_connectors(SLIDE_LENGTH_MID, start=1)
mid_slide = mid_slide + mid_slide_connectors
mid_slide = mid_slide + mid_slide_connectors.translate((BIRDHOUSE_WIDTH_INNER, 0, 0))

exporters.export(mid_slide, "construction_files/mid_slide.dxf")

# rotate and translate mid slide to final position
mid_slide = mid_slide.rotate(
    (0, 0, 0),
    (1, 0, 0),
    -SLIDE_ANGLE,
).translate((WALLTHICKNESS, WALLTHICKNESS, BACK_PLATE_HEIGHT * 0.7))


# Create top slide
top_slide = (
    cq.Workplane("XY")
    .rect(BIRDHOUSE_WIDTH_INNER, SLIDE_LENGTH_TOP, centered=False)
    .extrude(WALLTHICKNESS)
)

# add connectors to top slide
top_slide_connectors = distribute_connectors(SLIDE_LENGTH_TOP, start=0)
top_slide = top_slide + top_slide_connectors
top_slide = top_slide + top_slide_connectors.translate((BIRDHOUSE_WIDTH_INNER, 0, 0))

exporters.export(top_slide, "construction_files/top_slide.dxf")

# rotate and translate top slide to final position
top_slide = (
    top_slide.translate((0, -SLIDE_LENGTH_TOP, 0))
    .rotate(
        (0, 0, 0),
        (1, 0, 0),
        SLIDE_ANGLE,
    )
    .translate(
        (
            WALLTHICKNESS,
            BIRDHOUSE_DEPTH - WALLTHICKNESS,
            BACK_PLATE_HEIGHT - WALLTHICKNESS,
        )
    )
)


# cut out connector shapes from side plates
side_plate = side_plate - front_plate
side_plate = side_plate - back_plate
side_plate = side_plate - bottom_slide
side_plate = side_plate - mid_slide
side_plate = side_plate - top_slide
side_plate2 = side_plate.translate((BIRDHOUSE_WIDTH - WALLTHICKNESS, 0, 0))


# Create left roof plate
roof_left = (
    cq.Workplane("XY")
    .rect(ROOF_LENGTH, BIRDHOUSE_DEPTH, centered=False)
    .extrude(WALLTHICKNESS)
)

roof_left_connectors = distribute_connectors(BIRDHOUSE_DEPTH, start=1).translate(
    (ROOF_LENGTH, 0, 0)
)
roof_left = roof_left + roof_left_connectors
exporters.export(roof_left, "construction_files/roof_left.dxf")

# rotate and translate roof to final position
roof_left = roof_left.rotate((0, 0, 0), (0, 1, 0), -45).translate(
    (0, 0, SIDE_PLATE_HEIGHT)
)

# Create right roof plate
roof_right = (
    cq.Workplane("XY")
    .rect(ROOF_LENGTH + WALLTHICKNESS, BIRDHOUSE_DEPTH, centered=False)
    .extrude(WALLTHICKNESS)
    .translate((-ROOF_LENGTH - WALLTHICKNESS, 0, 0))
)

# rotate and translate roof to final position
roof_right = roof_right.rotate((0, 0, 0), (0, 1, 0), 45).translate(
    (BIRDHOUSE_WIDTH, 0, SIDE_PLATE_HEIGHT)
)
roof_right = roof_right - roof_left

exporters.export(
    roof_right.translate((-BIRDHOUSE_WIDTH, 0, SIDE_PLATE_HEIGHT)).rotate(
        (0, 0, 0), (0, 1, 0), -45
    ),
    "construction_files/roof_right.dxf",
)

# export models as dxf for laser cutting
exporters.export(front_plate, "construction_files/front_plate.dxf")
exporters.export(side_plate, "construction_files/side_plate.dxf")
exporters.export(back_plate, "construction_files/back_plate.dxf")


# show models in viewer
show_object(front_plate, options={"name": "Front Plate", "color": "#A04800"})
show_object(back_plate, options={"name": "Back Plate", "color": "#A04800"})
show_object(side_plate, options={"name": "Side Plate Left", "color": "#A02D00"})
show_object(side_plate2, options={"name": "Side Plate Right", "color": "#A02D00"})
show_object(bottom_slide, options={"name": "Bottom Slide", "color": "#806D00"})
show_object(mid_slide, options={"name": "Middle Slide", "color": "#806D00"})
show_object(top_slide, options={"name": "Top Slide", "color": "#806D00"})
show_object(roof_left, options={"name": "Left Roof", "color": "#805700"})
show_object(roof_right, options={"name": "Right Roof", "color": "#806200"})
