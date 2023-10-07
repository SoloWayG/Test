import numpy as np
import pickle
from pathlib import Path

from gefest.core.structure.structure import Structure, get_random_structure
from gefest.tools.estimators.DL.bw_surrogate.sound_cnn import BWCNN###add sound CNN
from gefest.tools.estimators.simulators.sound_wave.sound_interface import (
    SoundSimulator,
    generate_map,
)
from gefest.tools.estimators.estimator import Estimator


def configurate_estimator(domain: "Domain", path_best_struct=None):
    # ------------
    # User-defined estimator
    # it should be created as object with .estimate() method
    # ------------
    root_path = Path(__file__).parent.parent.parent.parent
    path_to_surr = f'{root_path}/gefest/tools/estimators/DL/bw_surrogate/bw_surrogate_700_train.h5'

    sound = SoundSimulator(domain=domain)
    cnn = BWCNN(domain=domain,
                path=path_to_surr,
                main_model=sound)

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

    # Loss for minimizing, it is optional function
    def loss(struct: Structure, estimator):
        spl = estimator.estimate(struct)
        current_spl = np.nan_to_num(spl, nan=0, neginf=0, posinf=0)

        l_f = np.sum(np.abs(best_spl - current_spl))

        return l_f

    # ------------
    # GEFEST estimator
    # ------------

    # Here loss is an optional argument, otherwise estimator will be considered as loss for minimizing
    estimator = Estimator(estimator=cnn, loss=loss)

    return estimator
