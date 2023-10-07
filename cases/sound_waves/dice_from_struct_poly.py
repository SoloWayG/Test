from shapely.geometry import Polygon as shpoly
from gefest.core.structure.structure import Structure
from gefest.core.structure.point import Point
from gefest.core.structure.polygon import Polygon

def dice(stract1: Structure, stract2: Structure):
    """
    Dice score for only one polygon in structure. This func calculate dice between two polygons.

    Args:
        stract1: Stacture with poly
        stract2: Stacture with poly

    Returns: [0;1] Coef how polygons similar to each other

    """

    try:
        p1 = shpoly([a.coords()[:2] for a in [i.points for i in stract1.polygons][0]])
        p2 = shpoly([a.coords()[:2] for a in [i.points for i in stract2.polygons][0]])
        dice = 2 * p1.intersection(p2).area / (p1.area + p2.area)
    except:
        dice = 0

    return dice
