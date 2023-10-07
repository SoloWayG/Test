import pickle
import matplotlib.pyplot as plt
import numpy as np
import os
list_dir=os.listdir('.')
list_dir.remove('load_sigmas.py')
means = []
for i in list_dir:
    with open(f'{i}/spl_for_check_{i}.pickle', "rb") as f:
        best_structure = pickle.load(f)
        means.append([np.mean(np.nan_to_num(np.array(i), nan=0, neginf=0, posinf=0)) for i in best_structure])
for m,i in enumerate(means):
    plt.plot(i,label=list_dir[m])

plt.legend()
plt.grid()
plt.show()
print(means)