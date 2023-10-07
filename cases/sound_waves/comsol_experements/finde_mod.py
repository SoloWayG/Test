import os
import pickledb
import numpy as np
import mph
import pickle
import argparse
from pathlib import Path
root_path = Path(__file__).parent.parent.parent.parent
db = pickledb.load(f'{root_path}/cases/sound_waves/comsol_experements/0408_no_del_add_MSE_p_size_40_n_stps_50_m_rate_0.9_extra_True/comsol_db.saved', False)
last=int(len(os.listdir(f'{root_path}/cases/sound_waves/comsol_experements/0408_no_del_add_MSE_p_size_40_n_stps_50_m_rate_0.9_extra_True/History'))/3)-1
print(last)
with open(f'{root_path}/cases/sound_waves/comsol_experements/0408_no_del_add_MSE_p_size_40_n_stps_50_m_rate_0.9_extra_True/History/population_{last}.pickle', 'rb') as f:
    pop = pickle.load(f)
indexis=[]
for i in range(last):
    with open(f'{root_path}/cases/sound_waves/comsol_experements/0408_no_del_add_MSE_p_size_40_n_stps_50_m_rate_0.9_extra_True/History/performance_{i}.pickle', 'rb') as f:
        perf = pickle.load(f)
        print(perf)
for i in range(3):
    print(db.get(str(pop[i])))
