from gefest.tools.optimizers.GA.base_GA import BaseGA
import os
import pickledb
import math
import pickle
from random import randint
from cases.sound_waves.configuration import sound_optimizer
from cases.main_conf import opt_params
from cases.sound_waves.configuration_comsol import sound_domain,sound_sampler, sound_estimator
from cases.sound_waves.experements.poly_from_point import poly_from_comsol_txt

opt_params.pop_size=15
domain, task_setup = sound_domain.configurate_domain(
    poly_num=opt_params.n_polys,
    points_num=opt_params.n_points,
    is_closed=opt_params.is_closed,
)

optimizer = sound_optimizer.configurate_optimizer(
    pop_size=opt_params.pop_size,
    crossover_rate=opt_params.c_rate,
    mutation_rate=opt_params.m_rate,
    task_setup=task_setup,
)

with open(f'1707_Denis_mut_exp_MSE_p_size_15_n_stps_20_m_rate_0.9_extra_True/History/population_{4}.pickle', 'rb') as f:
    pop = pickle.load(f)
with open(f'1707_Denis_mut_exp_MSE_p_size_15_n_stps_20_m_rate_0.9_extra_True/History/performance_{4}.pickle', 'rb') as f:
    perf = pickle.load(f)

opter = optimizer.step(pop,perf)
print(opter)