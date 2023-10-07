import timeit
import pickle

from gefest.core.opt.gen_design import design
from gefest.core.opt.operators.operators import point_crossover
from gefest.core.structure.structure import get_random_structure
from cases.main_conf import opt_params
from cases.sound_waves.configuration import sound_optimizer

import shutil
from pathlib import Path
import os
from cases.sound_waves.configuration_comsol import sound_domain,sound_sampler, sound_estimator
from cases.sound_waves.experements.poly_from_point import poly_from_comsol_txt
# If the value is False, pretrained models will be selected
# otherwise put path to your model
opt_params.is_closed = True
opt_params.pop_size = 30
opt_params.n_steps = 100
opt_params.n_polys = 1
opt_params.n_points = 10
opt_params.c_rate = 0.2
LOSS ='MSE'
is_extra = True
# ------------
# GEFEST tools configuration
# ------------
domain, task_setup = sound_domain.configurate_domain(
    poly_num=opt_params.n_polys,
    points_num=opt_params.n_points,
    is_closed=opt_params.is_closed,
    polygon_side = 0.1
)

#-----Upload reference structure from comsol txt polygons
path_fig = 'gefest/tools/estimators/simulators/comsol/sound/model/figures/'
root_path = Path(__file__).parent.parent.parent.parent
path_fig = f'{root_path}/{path_fig}'
#try to read initial pop if it need


figure_file_names = os.listdir(path_fig)#Search names of txt files with points of polygons, drawn in comsol
print(figure_file_names)
figure_names = [i.split(sep='.')[0] for i in figure_file_names]#Split name of files for create dir name, based on prepared polygons names
print(figure_names)
best_structure = poly_from_comsol_txt(path=path_fig+figure_file_names[0])#upload new best struct from figure files

new_path = f'1408_new_no_del_add_{LOSS}_p_size_{opt_params.pop_size}_n_stps_{opt_params.n_steps}_m_rate_{opt_params.m_rate}_extra_{is_extra}'     #path to create new dir of experement iteration
###############################
if os.path.exists(new_path):#
    shutil.rmtree(new_path) #
os.makedirs(new_path)       #

#best_structure = get_random_structure(domain)

path_best_struct = new_path+f"/best_structure({figure_names[0]}).pickle"
with open(path_best_struct, "wb") as handle:
    pickle.dump(best_structure, handle, protocol=pickle.HIGHEST_PROTOCOL)

estimator = sound_estimator.configurate_estimator(
    domain=domain,
    path_best_struct=path_best_struct,
    dir_path=new_path,
    receivers=2
)

try:
    with open(f'{root_path}/cases/sound_waves/comsol_experements/0408_no_del_add_MSE_p_size_40_n_stps_50_m_rate_0.9_extra_True/History/population_9.pickle', "rb") as f:
        init_pop = pickle.load(f)
except:
    init_pop=None
sampler = sound_sampler.configurate_sampler(domain=domain,initial_state=None)

optimizer = sound_optimizer.configurate_optimizer(
    pop_size=opt_params.pop_size,
    crossover_rate=opt_params.c_rate,
    mutation_rate=opt_params.m_rate,
    task_setup=task_setup,
    evolutionary_operators=point_crossover
)

# ------------
# Generative design stage
# ------------

start = timeit.default_timer()
optimized_pop = design(
    n_steps=opt_params.n_steps,
    pop_size=opt_params.pop_size,
    estimator=estimator,
    sampler=sampler,
    optimizer=optimizer,
    path=new_path+f'/History',
    extra=is_extra,
    extra_break=opt_params.n_steps
)
spend_time = timeit.default_timer() - start
print(f"spent time {spend_time} sec")

with open(new_path+"/optimized_structure.pickle", "wb") as handle:
    pickle.dump(optimized_pop, handle, protocol=pickle.HIGHEST_PROTOCOL)
