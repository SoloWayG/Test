import pickle
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, FixedLocator
import matplotlib.ticker as ticker
from cases.main_conf import opt_params
from cases.sound_waves.configuration import sound_domain
from gefest.tools.estimators.simulators.sound_wave.sound_interface import SoundSimulator
from cases.sound_waves.experements.microphone_points import Microphone
import numpy as np
from gefest.tools.utils.count_files import count_files
import os
def upload_file(path: str):
    with open(path, "rb") as f:
        file = pickle.load(f)
        f.close()
    return file
#Fitness counting

paths_for_plotting = ['cases/sound_waves/experements/002_3107_roulette/iter_0/bottom_square',
                      'cases/sound_waves/experements/001_3107_roulette/iter_0/bottom_square',
                      'cases/sound_waves/experements/003_3107_roulette/iter_0/bottom_square',
                      'cases/sound_waves/experements/001_3107_tournament/iter_0/bottom_square',
                      'cases/sound_waves/experements/002_3107_tournament/iter_0/bottom_square',
                      'cases/sound_waves/experements/003_3107_tournament/iter_0/bottom_square',
                      'cases/sound_waves/experements/002_3107_roulette/iter_1/bottom_square',
                      'cases/sound_waves/experements/001_3107_roulette/iter_1/bottom_square',
                      'cases/sound_waves/experements/003_3107_roulette/iter_1/bottom_square',
                      'cases/sound_waves/experements/001_3107_tournament/iter_1/bottom_square',
                      'cases/sound_waves/experements/002_3107_tournament/iter_1/bottom_square',
                      'cases/sound_waves/experements/1_0908_roulette/iter1/bottom_square_exp',
                      'cases/sound_waves/experements/1_0908_roulette/iter0/bottom_square_exp',


     ]


root_path = Path(__file__).parent.parent.parent.parent.parent
#ls = os.listdir(path='.')

#
#pwd = os.getcwd()
#dir_name = os.path.basename(pwd)
fits ={}
dice_dict={}
for path_ind,path in enumerate(paths_for_plotting):
    lenght = count_files(path=f'{root_path}/{path}', like='optimized_structure_')
    perform_cnt = count_files(path=f'{root_path}/{path}/History_0', like='performance_')
    fits[path_ind] = []
    dice_dict[path_ind] = []
    for a in range(lenght):
        performance_path_2 = ([f"{root_path}/{path}/History_{a}/performance_{i}.pickle" for i in range(perform_cnt)])
        dice_path_2 = ([f"{root_path}/{path}/History_{a}/dice_metric_{i}.pickle" for i in range(perform_cnt)])
        fitness = ([round(upload_file(i)[0],4) for i in performance_path_2])
        dices = ([round(upload_file(i)[0],4) for i in dice_path_2])
        fits[path_ind].append(fitness)
        dice_dict[path_ind].append(dices)

for i in range(len(fits)):
    fits[i][1],fits[i][2]=fits[i][2],fits[i][1]
    dice_dict[i][1], dice_dict[i][2] = dice_dict[i][2], dice_dict[i][1]
boxs =[]
boxs_dice =[]



for iter in range(200):
    boxs.append([])
    boxs_dice.append([])
    for f in range(len(fits[0])):
        boxs[-1].append([])
        boxs_dice[-1].append([])
        for k in range(len(fits)):
            boxs[iter][-1].append(fits[k][f][iter])
            boxs_dice[iter][-1].append(dice_dict[k][f][iter])


fig, axs = plt.subplots(nrows=4, ncols=1, figsize=(12, 10))
fig.tight_layout(h_pad= 3)
receivers = [9,64,240,'Full field']

for cases,ax in enumerate(axs.flat):
    ax.set_title(f'{receivers[cases]} receivers',fontdict={'fontsize':10})
    ax.boxplot(
        list(np.array([boxs[i][cases] for i in range(len(boxs))])/np.max(np.array([boxs[i][cases] for i in range(len(boxs))]))),
        vert=True,
        sym = '',
        bootstrap =200,
        widths=1,
        medianprops=dict(color="red", linewidth=1.5),
        showmeans=True


    )


    #Next part displays the coordinate axis values in increments of 5
    ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(0.1))
    ax.set(xticklabels=[x for x in range(0,200)][::5])

    ax.set_ylabel('Loss')
    ax.set_xlabel('Iterations')
    ax.minorticks_on()
    ax.grid(which='major')
    ax.grid(which='minor',alpha = 0.2)

plt.show()
print('Dice boxes')
fig, axs = plt.subplots(nrows=4, ncols=1, figsize=(12, 10))
fig.tight_layout(h_pad= 3)
receivers = [9,64,240,'Full field']
DICE_CRITERIA =0.95
for cases,ax in enumerate(axs.flat):
    ax.set_title(f'{receivers[cases]} receivers; % of dice more than {DICE_CRITERIA} =  {np.sum(np.array([boxs_dice[i][cases] for i in range(len(boxs))])>DICE_CRITERIA)/(np.array([boxs_dice[i][cases] for i in range(len(boxs))]).size)}',fontdict={'fontsize':10})
    ax.boxplot([boxs_dice[i][cases] for i in range(len(boxs))],
        vert=True,
        sym = '',
        bootstrap =200,
               widths=1,
               medianprops=dict(color="red", linewidth=1.5)

    )


    #Next part displays the coordinate axis values in increments of 5
    ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(0.1))
    ax.set(xticklabels=[x for x in range(0,200)][::5])

    ax.set_ylabel('Dice')
    ax.set_xlabel('Iterations')
    ax.minorticks_on()
    ax.grid(which='major')
    ax.grid(which='minor',alpha = 0.2)

plt.show()