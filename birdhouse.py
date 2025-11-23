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
    BIRDHOUSE_HEIGHT,
    BIRDHOUSE_SPACE_TOP,
    BIRDHOUSE_SPACE_BOTTOM,
)


FRONT_PLATE_HEIGHT_MIDDLE = BIRDHOUSE_HEIGHT - BIRDHOUSE_SPACE_BOTTOM
FRONT_PLATE_HEIGHT_SIDE = FRONT_PLATE_HEIGHT_MIDDLE - BIRDHOUSE_WIDTH * 0.4
SIDE_PLATE_HEIGHT = FRONT_PLATE_HEIGHT_SIDE + BIRDHOUSE_SPACE_BOTTOM
BACK_PLATE_HEIGHT = SIDE_PLATE_HEIGHT - BIRDHOUSE_SPACE_TOP

# Create front plate with entrance holes
front_plate = (
    cq.Workplane("XZ")
    .lineTo(0, FRONT_PLATE_HEIGHT_SIDE)
    .lineTo(BIRDHOUSE_WIDTH / 2, FRONT_PLATE_HEIGHT_MIDDLE)
    .lineTo(BIRDHOUSE_WIDTH, FRONT_PLATE_HEIGHT_SIDE)
    .lineTo(BIRDHOUSE_WIDTH, 0)
    .close()
    .moveTo(BIRDHOUSE_WIDTH / 2, FRONT_PLATE_HEIGHT_MIDDLE * 0.5)
    .circle(BIRDHOUSE_WIDTH / 6)
    .moveTo(BIRDHOUSE_WIDTH / 2, FRONT_PLATE_HEIGHT_MIDDLE * 0.75)
    .circle(BIRDHOUSE_WIDTH / 6)
    .extrude(WALLTHICKNESS)
)

# add connectors to front plate
front_plate_connectors = distribute_connectors(FRONT_PLATE_HEIGHT_SIDE).rotate(
    (0, 0, 0), (1, 0, 0), 90
)
front_plate = front_plate - front_plate_connectors
front_plate = front_plate - front_plate_connectors.translate((BIRDHOUSE_WIDTH, 0, 0))
front_plate = front_plate.translate((0, WALLTHICKNESS, BIRDHOUSE_SPACE_BOTTOM))


# Create back plate
back_plate = (
    cq.Workplane("XZ")
    .lineTo(0, BACK_PLATE_HEIGHT)
    .lineTo(BIRDHOUSE_WIDTH, BACK_PLATE_HEIGHT)
    .lineTo(BIRDHOUSE_WIDTH, 0)
    .close()
    .extrude(WALLTHICKNESS)
)
# add connectors to side plate
back_plate_connectors = distribute_connectors(FRONT_PLATE_HEIGHT_SIDE).rotate(
    (0, 0, 0), (1, 0, 0), 90
)
back_plate = back_plate - back_plate_connectors
back_plate = back_plate - back_plate_connectors.translate((BIRDHOUSE_WIDTH, 0, 0))
back_plate = back_plate.translate((0, BIRDHOUSE_DEPTH, 0))

# Create side plates
side_plate = (
    cq.Workplane("YZ")
    .lineTo(0, SIDE_PLATE_HEIGHT)
    .lineTo(BIRDHOUSE_DEPTH, SIDE_PLATE_HEIGHT)
    .lineTo(BIRDHOUSE_DEPTH, 0)
    .close()
    .extrude(WALLTHICKNESS)
)

# cut out front plate shape from side plates
side_plate = side_plate - front_plate
side_plate = side_plate - back_plate
side_plate2 = side_plate.translate((BIRDHOUSE_WIDTH - WALLTHICKNESS, 0, 0))


# export models as dxf for laser cutting
exporters.export(front_plate, "construction_files/front_plate.dxf")
exporters.export(side_plate, "construction_files/side_plate.dxf")
exporters.export(back_plate, "construction_files/back_plate.dxf")


# show models in viewer
show_object(front_plate, options={"name": "Front Plate", "color": "#A04800"})
show_object(back_plate, options={"name": "Back Plate", "color": "#A04800"})
show_object(side_plate, options={"name": "Side Plate Left", "color": "#A02D00"})
show_object(side_plate2, options={"name": "Side Plate Right", "color": "#A02D00"})
# show_object(back_plate_connectors, options={"alpha": 0.5, "color": "red"})
