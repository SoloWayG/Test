import numpy as np
import pickle
from copy import deepcopy
from gefest.core.structure.structure import Structure, get_random_structure
from gefest.tools.estimators.simulators.sound_wave.sound_interface import (
    SoundSimulator,
    generate_map,
)
from gefest.tools.estimators.simulators.sound_wave.sound_interface_double import (
    SoundSimulator as SoundSimulator2,
    generate_map as generate_map2,
)
from cases.sound_waves.experements.microphone_points import Microphone
from gefest.tools.estimators.estimator_double import Estimator
from cases.sound_waves.dice_from_struct_poly import dice
def configurate_estimator(domain: "Domain", path_best_struct=None, iters = None):
    # ------------
    # User-defined estimator
    # it should be created as object with .estimate() method
    # ------------
    sound = SoundSimulator(domain=domain)
    sound2 = SoundSimulator2(domain=domain)
    if path_best_struct is None:
        print("please, set up the best spl matrix into configuration")
        print("the best structure will be generated randomly")
        rnd_structure = get_random_structure(domain)
        best_spl = generate_map(domain, rnd_structure)
    else:
        with open(path_best_struct, "rb") as f:
            best_structure = pickle.load(f)
        best_spl = sound.estimate(best_structure)
        best_spl = np.nan_to_num(best_spl, nan=0, neginf=0, posinf=0)
        micro = Microphone(matrix=best_spl).array()
        best_spl = np.concatenate(micro[iters])

        best_spl2 = sound2.estimate(best_structure)
        best_spl2 = np.nan_to_num(best_spl2, nan=0, neginf=0, posinf=0)
        micro2 = Microphone(matrix=best_spl2).reflect_array()
        best_spl2 = np.concatenate(micro2[iters])

        best = np.concatenate([best_spl,best_spl2])
    # Loss for minimizing, it is optional function
    def loss(struct: Structure, estimator,estimator2):

        spl = estimator.estimate(struct)
        micro_spl = Microphone(matrix=spl).array()
        spl = np.concatenate(micro_spl[iters])
        lenght = len(spl)*2
        current_spl = np.nan_to_num(spl, nan=0, neginf=0, posinf=0)

        spl2 = estimator2.estimate(struct)
        micro_spl2 = Microphone(matrix=spl2).reflect_array()
        spl2 = np.concatenate(micro_spl2[iters])
        current_spl2 = np.nan_to_num(spl2, nan=0, neginf=0, posinf=0)

        crnt_spl = np.concatenate([current_spl,current_spl2])

        metric = dice(best_structure, struct)
        print('Dice is',dice(best_structure, struct))
        l_f = np.sum((best - crnt_spl)**2)/lenght + (1-dice(best_structure, struct))*10


        return l_f, metric

    # ------------
    # GEFEST estimator
    # ------------

    # Here loss is an optional argument, otherwise estimator will be considered as loss for minimizing
    estimator = Estimator(estimator=sound, estimator2=sound2, loss=loss)

    return estimator
