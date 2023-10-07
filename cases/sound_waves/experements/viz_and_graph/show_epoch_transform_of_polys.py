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
import numpy as np
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
ls = os.listdir(path='.')
lenght = count_files(path ='.', like ='optimized_structure_')
archs = count_files(path ='./History_0', like ='performance_')
pwd = os.getcwd()
dir_name = os.path.basename(pwd)

micro = Microphone().array()
####
LAST = True#Set what a case (with point or half perimeter)
####
best_fit =[]

for a in range(lenght):
    performance_path_2 = ([f"History_{a}/performance_{i}.pickle" for i in range(archs)])
    stractures = ([upload_file(f"History_{a}/population_{i}.pickle") for i in range(archs)])
    fitness = ([upload_file(i) for i in performance_path_2])
for r in range(5):
    best_fit.append([round(i[r]/10000,0) for i in fitness])

# for i in range(len(best_fit)):#Визуализация сходимости по местам в популяции.
#     if i == 0:
#         plt.plot(best_fit[i], label=f'best fitness  in pop')
#     else:
#         plt.plot(best_fit[i] ,label=f'ftss of {i} place in pop')
#     plt.xlabel("Итерации")
#     plt.ylabel("Fitness *10.000")
#     plt.legend()
# plt.grid()
# plt.show()


#viz polygons of pop
path_fig = 'gefest/tools/estimators/simulators/comsol/sound/model/figures/'
root_path = Path(__file__).parent.parent.parent.parent.parent.parent
path_fig = f'{root_path}/{path_fig}'
figure_file_names = os.listdir(path_fig)
best_structure = poly_from_comsol_txt(path=path_fig+figure_file_names[0])

fig, axs = plt.subplots(nrows=2, ncols=archs//2, figsize=(22, 22), sharey=True)
gen = 0
for i,ax,f in zip(stractures,axs.flat,fitness):#Structures if structures of every populations
    #ax.plot([x[0] for x in domain.allowed_area],[y[1] for y in domain.allowed_area])
    #x = [point._x for point in best_structure.polygons[0].points]
    #y = [point._y for point in best_structure.polygons[0].points]
    #ax.plot(x, y,'go--',label='reference poly')
    ax.legend()
    for ind,n in enumerate(i):
        x = [point._x for point in n.polygons[0].points]
        y = [point._y for point in n.polygons[0].points]
        ax.plot(x, y,label=f'poly{ind}, fit: {round(f[ind]/100000,0)}')
        ax.set_title(f'fitnes of polys of generation{gen}')
        ax.legend()
        #plt.title(label=f'pop_{i}')
        #n.plot(n)

    gen+=1
plt.show()