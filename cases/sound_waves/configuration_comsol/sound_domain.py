import numpy as np

from gefest.core.geometry.geometry_2d import Geometry2D
from gefest.core.opt.setup import Setup
from gefest.core.structure.domain import Domain
from pathlib import Path
from gefest.core.structure.prohibited import create_prohibited
import pandas as pd
# ------------
# USER-DEFINED CONFIGURATION OF DOMAIN FOR BREAKWATERS TASK
# ------------

'''
Read data of allow area, where we can build polygons (from txt to pandas)
You can draw in comsol sketch some closed polygon. And then, when u see table with Coordinates 
you can save one to file and read here. 
That very comfortable to use
'''
path_allow = 'gefest/tools/estimators/simulators/comsol/sound/model/'
root_path = Path(__file__).parent.parent.parent.parent
path_allow = f'{root_path}/{path_allow}'
res = pd.read_csv(path_allow+'allow_area.txt', sep=' ',header=None)
#allow_ar = [(float(round(res.iloc[i,0], 2)), float(round(res.iloc[i, 1], 2))) for i in res.index]
allow_ar=[[0, 0], [0, 120], [120, 120], [120, 0], [0, 0]]
#(res.iloc[i,0],res.iloc[i, 1])
"""
Prohibited objects
"""
#fixed_area = [[[45, 55], [55, 55], [55, 45], [45, 45], [45, 55]]]

#prohibited = create_prohibited(fixed_area=fixed_area)


def configurate_domain(poly_num: int, points_num: int, is_closed: bool,polygon_side=0.05):
    # ------------
    # GEFEST domain based on user-defined configuration_de
    # ------------
    if is_closed:
        min_points_num = 4
    else:
        min_points_num = 2

    geometry = Geometry2D(is_closed=is_closed)
    domain = Domain(
        allowed_area=allow_ar,
        geometry=geometry,
        max_poly_num=poly_num,
        min_poly_num=1,
        max_points_num=points_num,
        min_points_num=min_points_num,
        is_closed=is_closed,
        polygon_side=polygon_side
    )
    task_setup = Setup(domain=domain)

    return domain, task_setup
