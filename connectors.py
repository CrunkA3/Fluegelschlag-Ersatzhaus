"""
connectors — utilities to create rectangular connector extrusions along a side.

This module provides distribute_connectors(length: float) -> cq.Workplane,
which generates a CadQuery Workplane containing a row of rectangular connector
pieces distributed along a given length. Each connector is a rectangle of
width 2 * WALLTHICKNESS and height WALLTHICKNESS, extruded by WALLTHICKNESS,
with spacing equal to 2 * WALLTHICKNESS. If no connectors fit the given
length, an empty cq.Workplane("front") is returned.

Notes:
- Count is computed as int(length / (2 * WALLTHICKNESS)); any partial remaining
  space is ignored.
- Intended for use with CadQuery and the WALLTHICKNESS constant from constants.py.
"""

from cadquery import cq

from constants import WALLTHICKNESS


def distribute_connectors(length: float) -> cq.Workplane:
    """Create a Workplane containing rectangular connector pieces.
    If count is 0 an empty cq.Workplane("front") is returned.
    Parameters:
        length (float): Lenght of the side.
    Returns:
        cq.Workplane: A Workplane object containing the union of all connector extrusions,
                      or an empty Workplane if count is zero.
    """

    # number of pieces that fit with spacing = 2 * WALLTHICKNESS
    count = int(length / (WALLTHICKNESS * 2))
    pieces = []
    for i in range(count):
        # place first center at WALLTHICKNESS/2, then every 2*WALLTHICKNESS after that
        y = WALLTHICKNESS * (i * 2 + 1) + WALLTHICKNESS / 2
        pieces.append(
            cq.Workplane("front")
            .moveTo(0, y)
            .rect(WALLTHICKNESS * 2, WALLTHICKNESS)
            .extrude(WALLTHICKNESS)
        )

    if not pieces:
        return cq.Workplane("front")

    connectors = pieces[0]
    for p in pieces[1:]:
        connectors = connectors.union(p)

    return connectors
