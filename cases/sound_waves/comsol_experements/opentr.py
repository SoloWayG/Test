import pickle
from pathlib import Path
from gefest.core.geometry.geometry_2d import Geometry2D
import pickle
import matplotlib.pyplot as plt
from gefest.core.structure.point import Point
from gefest.core.structure.polygon import Polygon
from gefest.core.structure.structure import Structure
import random
while True:

    print(random.randint(0, 1))

# with open('best_structure(star).pickle', "rb") as f:
#     file = pickle.load(f)
# print(file)
# poly = [i for i in file.polygons]
# print(poly)
# geom_cl = Geometry2D(is_closed=True)
# geom_op = Geometry2D(is_closed=True)
#
# print(geom_cl.get_coords(poly))
# print(geom_op.get_coords(poly))