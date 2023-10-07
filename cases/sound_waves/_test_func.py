import random

from gefest.core.structure.structure import get_random_structure
from gefest.core.viz.struct_vizualizer import StructVizualizer
import numpy as np
from cases.sound_waves.configuration_comsol import sound_domain
import pandas as pd
from cases.main_conf import opt_params
from gefest.core.structure.structure import Structure, get_random_structure
from gefest.core.structure.point import Point
from gefest.core.structure.polygon import Polygon
from gefest.core.geometry.geometry_2d import Geometry2D
from gefest.core.opt.operators.mutation import add_delete_point_mutation, pos_change_point_mutation, points_mutation, \
    mutation
import os
import matplotlib.pyplot as plt
from gefest.core.viz.struct_vizualizer import StructVizualizer
from shapely.geometry import Polygon as shpoly
import time
opt_params.is_closed = True
domain, task_setup = sound_domain.configurate_domain(
    poly_num=1,
    points_num=14,
    is_closed=opt_params.is_closed,
    polygon_side=0.05
)

# start_time = time.time()
#
# while (time.time() - start_time) < 6333:
print(None in [2,1,2])

# for _ in range(10):
#     p1 = get_random_structure(domain)
#     vizer = StructVizualizer(domain)
#     vizer.plot_structure(p1,'Start')
#     p0 = shpoly([a.coords()[:2] for a in [i.points for i in p1.polygons][0]])
#     print('Создали, теперь мутируем№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№')
#     for i in range(10):
#
#         p1 = mutation(p1, domain)
#         #p1 = pos_change_point_mutation(p1, 0, random.randint(1, len(p0.exterior.xy) - 1), domain)
#
#
#     #plt.plot(domain.allowed_area,label ='Allow area')
#         # plt.plot(*p2.exterior.xy)
#         # print(p1,p2)
#     vizer.plot_structure(p1, f'p{i}')
# plt.legend()
# plt.show()