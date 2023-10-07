import numpy as np
import pickle

from gefest.core.structure.structure import Structure, get_random_structure
from gefest.tools.estimators.simulators.comsol.sound.comsol_interface import Comsol
import mph
from gefest.tools.estimators.estimator_comsol import Estimator
from gefest.tools.estimators.simulators.sound_wave.sound_interface import generate_map#, SoundSimulator
from pathlib import Path
from cases.sound_waves.comsol_experements.aveop_reference import total_aveop
from cases.sound_waves.dice_from_struct_poly import dice

def configurate_estimator(domain: "Domain", path_best_struct=None,receivers = 2,path_to_sim=False,dir_path=""):
    # ------------
    # User-defined estimator
    # it should be created as object with .estimate() method
    # ------------
    if not path_to_sim:
        root_path = Path(__file__).parent.parent.parent.parent
        path_to_sim = f'{root_path}/gefest/tools/estimators/simulators/comsol/sound/model/Reflect_run_two_recivers2.mph'
    print(path_to_sim)
    client = mph.Client(cores=8)
    print('Open Client',client)
    sound = Comsol(path_to_mph=path_to_sim,dir_path=dir_path,client=client)
    best_spl_path = dir_path + '/best_spl.pickle'
    # try:
    #     with open(best_spl_path, "rb") as f:
    #         best_spl = pickle.load(f)
    #     print('best_spl is opend')
    # except:
    if path_best_struct is None:
        print("please, set up the best spl matrix into configuration")
        print("the best structure will be generated randomly")
        rnd_structure = get_random_structure(domain)
        best_spl = generate_map(domain, rnd_structure)
    else:
        with open(path_best_struct, "rb") as f:
            best_structure = pickle.load(f)
        print('Estimating best_structure')
        best_spl,_,_,_,client_ = sound.estimate(structure = best_structure,receivers = receivers)
        client_.clear()
        print(best_spl,len(best_spl))
        best_spl = np.nan_to_num(best_spl, nan=0, neginf=0, posinf=0)
        best_spl = np.array(best_spl)-total_aveop()#Cleared from noise
        #############
        mean_left=np.mean(abs(best_spl[:len(best_spl)//2]))
        mean_right=np.mean(abs(best_spl[len(best_spl)//2:]))
        powering = mean_left/mean_right
        best_spl = np.array(list(best_spl[:len(best_spl) // 2]) + list(best_spl[len(best_spl) // 2:] * powering))
        max_ref = np.max(abs(best_spl))
        best_spl = best_spl/max_ref
        with open(best_spl_path, "wb") as handle:
            pickle.dump(best_spl, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # Loss for minimizing, it is optional function
    def loss(struct: Structure, estimator):
        spl, model, idx, dir_path, client = estimator.estimate(struct)
        if spl == 0:
            return np.inf, 0, model, idx, dir_path, client
        current_spl = np.nan_to_num(spl, nan=0, neginf=0, posinf=0)
        current_spl = np.array(current_spl) - total_aveop()
        current_spl = np.array(list(current_spl[:len(current_spl) // 2]) + list(current_spl[len(current_spl) // 2:] * powering))
        current_spl = current_spl/max_ref
        l_f = np.sum((best_spl - current_spl)**2)/len(np.array(current_spl))

        dice_metric = dice(best_structure,struct)

        return l_f, dice_metric,model,idx,dir_path,client

    # ------------
    # GEFEST estimator
    # ------------

    # Here loss is an optional argument, otherwise estimator will be considered as loss for minimizing
    estimator = Estimator(estimator=sound, loss=loss)

    return estimator
