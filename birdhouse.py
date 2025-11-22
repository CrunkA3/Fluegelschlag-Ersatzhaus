"""
birdhouse model
"""

from cadquery import cq, exporters

from ocp_vscode import show_object

from constants import (
    WALLTHICKNESS,
    BIRDHOUSE_WIDTH,
    BIRDHOUSE_DEPTH,
    BIRDHOUSE_HEIGHT,
    BIRDHOUSE_SPACE_BOTTOM,
)


FRONT_PLATE_HEIGHT_MIDDLE = BIRDHOUSE_HEIGHT - BIRDHOUSE_SPACE_BOTTOM
FRONT_PLATE_HEIGHT_SIDE = FRONT_PLATE_HEIGHT_MIDDLE - BIRDHOUSE_WIDTH / 2
NUM_FRONT_PLATE_CONNECTORS = int(FRONT_PLATE_HEIGHT_SIDE / (WALLTHICKNESS * 2))


front_plate = (
    cq.Workplane("front")
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


front_plate_connectors = cq.Workplane("front")

for y in range(NUM_FRONT_PLATE_CONNECTORS):
    front_plate_connectors = front_plate_connectors + (
        front_plate_connectors.moveTo(
            0, WALLTHICKNESS * (y * 2 + 1) + WALLTHICKNESS / 2
        )
        .rect(WALLTHICKNESS * 2, WALLTHICKNESS)
        .extrude(WALLTHICKNESS)
    )

front_plate = front_plate - front_plate_connectors
front_plate = front_plate - front_plate_connectors.translate((BIRDHOUSE_WIDTH, 0, 0))

exporters.export(front_plate, "construction_files/front_plate.dxf")

show_object(front_plate)
