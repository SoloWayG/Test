import numpy as np

from gefest.core.geometry.geometry_2d import Geometry2D
from gefest.core.opt.setup import Setup
from gefest.core.structure.domain import Domain
from gefest.core.structure.prohibited import create_prohibited
from pathlib import Path
from gefest.core.structure.prohibited import create_prohibited
import pandas as pd
# ------------
# USER-DEFINED CONFIGURATION OF DOMAIN FOR BREAKWATERS TASK
# ------------

grid_resolution_x = 300 # Number of points on x-axis
grid_resolution_y = 300  # Number of points on y-axis
coord_X = np.linspace(20, 100, grid_resolution_x + 1)  # X coordinate for spatial grid
coord_Y = np.linspace(20, 100, grid_resolution_y + 1)  # Y coordinate for spatial grid

grid = [grid_resolution_x, grid_resolution_y]  # points grid


"""
Prohibited objects
"""
#fixed_area = [[[45, 55], [55, 55], [55, 45], [45, 45], [45, 55]]]
fixed_area = [[[0, 55], [10, 55], [10, 45], [0, 45], [0, 55]]]
#[[[60, 120], [120, 120], [120, 0], [60, 0], [90, 30], [90, 90], [60, 120]]]
#fixed_points = [[[120//2,120],[120,120],[120,0],[120//2,0],[3*120//4,120//4],[3*120//4,3*120//4],[120//2,120]]]
#prohibited = create_prohibited(fixed_area=fixed_area,fixed_points=fixed_points)
path_allow = 'sound_waves/experements/Comsol_points/'
root_path = Path(__file__).parent.parent.parent.parent
path_allow = f'{root_path}/{path_allow}'
# res = pd.read_csv(path_allow+'allow_area.txt', sep=' ',header=None)
# print(res)
# allow_ar = [(float(round(res.iloc[i,0], 2)), float(round(res.iloc[i, 1], 2))) for i in res.index]

def configurate_domain(poly_num: int, points_num: int, is_closed: bool):
    # ------------
    # GEFEST domain based on user-defined configuration_de
    # ------------
    if is_closed:
        min_points_num = 4#May be need 4 point to close poly (3 by default)
    else:
        min_points_num = 2

    geometry = Geometry2D(is_closed=is_closed)
    domain = Domain(
        allowed_area=[
            (min(coord_X), min(coord_Y)),
            (min(coord_X), max(coord_Y)),
            (max(coord_X), max(coord_Y)),
            (max(coord_X), min(coord_Y)),
            (min(coord_X), min(coord_Y)),
        ],
        geometry=geometry,
        max_poly_num=poly_num,
        min_poly_num=1,
        max_points_num=points_num,
        min_points_num=min_points_num,
        is_closed=is_closed

    )
    task_setup = Setup(domain=domain)

    return domain, task_setup
