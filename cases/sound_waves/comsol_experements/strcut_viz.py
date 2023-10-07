import pickle
from pathlib import Path

import matplotlib.pyplot as plt
import os

from cases.sound_waves.experements.poly_from_point import poly_from_comsol_txt
from gefest.core.structure.structure import Structure
from gefest.tools.utils.count_files import count_files
from cases.sound_waves.experements.microphone_points import Microphone
from cases.main_conf import opt_params
from cases.sound_waves.configuration_comsol import sound_domain,sound_sampler, sound_estimator
from gefest.tools.estimators.simulators.sound_wave.sound_interface import SoundSimulator
from cases.sound_waves.experements.microphone_points import Microphone

def upload_file(path: str):
    with open(path, "rb") as f:
        file = pickle.load(f)
        f.close()
    return file

domain, task_setup = sound_domain.configurate_domain(
    poly_num=opt_params.n_polys,
    points_num=opt_params.n_points,
    is_closed=opt_params.is_closed,
)
root_path = Path(__file__).parent.parent.parent.parent
struct = upload_file(f'{root_path}/cases/sound_waves/comsol_experements/2407_no_del_add_MSE_p_size_20_n_stps_15_m_rate_0.9_extra_True/structures/4935b4c3-0fe2-4e93-80c9-60901ecb7cf8.str')

struct.plot(structure=struct)