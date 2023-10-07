import timeit
import pickle

from gefest.core.opt.operators.operators import default_operators
from gefest.core.structure.prohibited import create_prohibited
from gefest.core.opt.gen_design import design
from gefest.core.structure.structure import get_random_structure
from cases.main_conf import opt_params
from cases.sound_waves.experements.configuration_exp import (
    sound_domain,
    sound_estimator,
    sound_optimizer,
    sound_sampler,
)
from poly_from_point import poly_from_comsol_txt
import numpy as np
import os
import shutil
from cases.sound_waves.experements.microphone_points import Microphone
# If the value is False, pretrained models will be selected
# otherwise put path to your model
opt_params.is_closed = True
opt_params.pop_size = 25
opt_params.n_steps = 100
opt_params.n_polys = 1
opt_params.n_points = 10
opt_params.m_rate = 0.9
opt_params.c_rate = 0
is_extra = True
LOSS = 'MSE'
micro = Microphone().array()[-1::]
point_cnt_mes = len(micro)

figure_file_names = os.listdir('Comsol_points/figuers')#Search names of txt files with points of polygons, drawn in comsol
figure_names = [i.split(sep='.')[0] for i in figure_file_names]#Split name of files for create dir name, based on prepared polygons names
for n, fig in enumerate(figure_names):
    ################################
    new_path = f'Result/{fig}_exp'     #path to create new dir of experiment iteration
    ###############################
    if os.path.exists(new_path):#
        shutil.rmtree(new_path) #
    os.makedirs(new_path)       #
    # ------------
    # GEFEST tools configuration
    # ------------
    domain, task_setup = sound_domain.configurate_domain(
        poly_num=opt_params.n_polys,
        points_num=opt_params.n_points,
        is_closed=opt_params.is_closed,
    )
    print(figure_file_names)
    best_structure = poly_from_comsol_txt(path='Comsol_points/figuers/'+figure_file_names[n])#upload new best struct from figure files
    #best_structure = get_random_structure(domain)

    with open(new_path+"/best_structure.pickle", "wb") as handle:
        pickle.dump(best_structure, handle, protocol=pickle.HIGHEST_PROTOCOL)


    #for i in range(len(micro)):
    #Last of microphones numbers (full matrix)
    estimator = sound_estimator.configurate_estimator(
        domain=domain, path_best_struct=new_path+"/best_structure.pickle",iters=3
    )

    sampler = sound_sampler.configurate_sampler(domain=domain)

    optimizer = sound_optimizer.configurate_optimizer(
        pop_size=opt_params.pop_size,
        crossover_rate=opt_params.c_rate,
        mutation_rate=opt_params.m_rate,
        task_setup=task_setup,
        evolutionary_operators=default_operators

    )

    # ------------
    # Generative design stage
    # ------------
    i=0
    start = timeit.default_timer()
    optimized_pop = design(
        n_steps=opt_params.n_steps,
        pop_size=opt_params.pop_size,
        estimator=estimator,
        sampler=sampler,
        optimizer=optimizer,
        extra=is_extra,
        path=new_path+f'/History_{i}',
        extra_break=opt_params.n_steps
    )
    spend_time = timeit.default_timer() - start
    print(f"spent time {spend_time} sec")

    with open(new_path+f"/optimized_structure_{i}.pickle", "wb") as handle:
        pickle.dump(optimized_pop, handle, protocol=pickle.HIGHEST_PROTOCOL)
        #next = i+1
