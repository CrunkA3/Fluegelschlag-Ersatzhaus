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


def distribute_connectors(length: float, start: int = 1) -> cq.Workplane:
    """
    Create a row of rectangular connector solids distributed along the Y axis.
    The function computes how many connector pieces fit into the supplied length using a spacing
    equal to two times the global WALLTHICKNESS.
    ----------
    Parameters
    ----------
    length : float
        The available length along which connectors should be placed. The number of connectors
        created is floor(length / (2 * WALLTHICKNESS)). A non-positive length will result in
        no connectors being created.
    start : int, optional
        Integer offset applied to the placement pattern (default: 1). When start == 0 the first
        connector center is at WALLTHICKNESS/2; other values shift the entire pattern by
        multiples of WALLTHICKNESS.
    Returns
    -------
    cq.Workplane
        A CadQuery Workplane (on the "front" plane) that is the union of all connector solids.
        If no connectors fit into the given length, an empty cq.Workplane("front") is returned.
    Notes
    -----
    - This function depends on the global symbol WALLTHICKNESS (float) and the CadQuery module
      imported as `cq`.
    - Each connector is a rectangular prism with XY dimensions (2*WALLTHICKNESS, WALLTHICKNESS)
      and an extrusion depth of WALLTHICKNESS.
    - No explicit validation is performed on WALLTHICKNESS; if WALLTHICKNESS is zero or negative,
      behavior will be incorrect (typically resulting in zero connectors).
    Example
    -------
    >>> # assuming WALLTHICKNESS = 2.0 and cq imported
    >>> wp = distribute_connectors(20.0)
    >>> # wp is a Workplane containing the unioned connector solids
    """
    # number of pieces that fit with spacing = 2 * WALLTHICKNESS
    count = int(length / (WALLTHICKNESS * 2))
    pieces = []
    for i in range(count):
        # place first center at WALLTHICKNESS/2, then every 2*WALLTHICKNESS after that
        y = WALLTHICKNESS * (i * 2 + start) + WALLTHICKNESS / 2
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
