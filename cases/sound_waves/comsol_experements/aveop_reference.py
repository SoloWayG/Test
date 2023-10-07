import pandas as pd
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

def total_aveop(sep = '\t',
                path1='/gefest/tools/estimators/simulators/comsol/sound/model/aveop1.txt',
                path2='/gefest/tools/estimators/simulators/comsol/sound/model/aveop2.txt'):
    """
    Function calculate a total vector of 2 receivers in flaw detector in comsol model
    Args:
        sep: separator, that declared in comsol, when saved txt file


    Returns:

    """
    root_path = Path(__file__).parent.parent.parent.parent
    path_to_aveop_1 = f'{root_path}'+f'{path1}'
    path_to_aveop_2 = f'{root_path}'+f'{path2}'
    res1 = pd.read_csv(path_to_aveop_1, sep=sep, header=None)
    res2 = pd.read_csv(path_to_aveop_2, sep=sep, header=None)

    aveop_1 = [float(round(res1.iloc[i, 1], 2)) for i in res1.index][72:]
    aveop_2 = [float(round(res2.iloc[i, 1], 2)) for i in res2.index][72:]


    # mean_left = np.mean(abs(np.array(aveop_1)))
    # mean_right = np.mean(abs(np.array(aveop_2)))
    # power = mean_left/mean_right
    # powered_avp2 = np.array(aveop_2)*10
    # max_aveop = np.max(abs(powered_avp2))
    tot_aveop = aveop_1 + aveop_2
    return np.array(tot_aveop)
#plt.plot(total_aveop()[0])
#plt.show()
# print(len(total_aveop()))
# #print(len(total_aveop()))
# #print(len(aveop_1+aveop_2))
# #points = [Point(i[0], i[1]) for i in np.array(points)]
# # print('aveop',total_aveop())
# star = total_aveop(path1='/gefest/tools/estimators/simulators/comsol/sound/model/aveop1_star.txt',
#                   path2='/gefest/tools/estimators/simulators/comsol/sound/model/aveop2_star.txt')
# print(len(star))
# print(total_aveop(),star)
# print(list(star - np.array(total_aveop())))
#
# #plt.plot(abs(np.array(total_aveop())),label='total_aveop')
# plt.plot(abs(star),label='star')
# #plt.plot(abs((star - np.array(total_aveop()))),label='delta')
# plt.show()
# plt.legend()
# plt.grid()