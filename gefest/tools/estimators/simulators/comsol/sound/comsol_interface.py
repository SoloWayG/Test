import gc
import os
import pickledb
import numpy as np
import mph
import pickle
import time
from uuid import uuid4
from gefest.core.structure.structure import Structure
from cases.sound_waves.comsol_experements.aveop_reference import total_aveop


os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
USE_AVG_CONST = False


class Comsol:
    """
    ::TODO:: make abstract class for further specific realizations
    """
    """
    Comsol class for microfluidic problem
    """

    def __init__(self, path_to_mph,dir_path,client):
        """
        :param path_to_mph: (String), path to mph file
        """
        super(Comsol, self).__init__()

        self.client = client
        self.path_to_mph = path_to_mph
        self.dir_path = dir_path

    def estimate(self, structure: Structure, receivers = 2):
        """
        Estimation using comsol multiphysics
        :param structure: (Structure), Structure of polygons
        :return: (Int), Performance
        """
        gc.collect()
        #target, idx = self._load_fitness(structure)
        #if target is None:
            #model, idx = self._load_simulation_result(self.client, structure)
            #if model is None:
        poly_box = []
        print('Start COMSOL')
        for i, pol in enumerate(structure.polygons):
            poly_repr = []
            poly_repr.append(' '.join([str(pt.x) for pt in pol.points]))
            poly_repr.append(' '.join([str(pt.y) for pt in pol.points]))
            poly_box.append(poly_repr)

        model = self.client.load(self.path_to_mph)

        try:
            model = self._poly_add(model, poly_box)

            model.build()

            model.mesh()
            start_time = time.time()
            model.solve()
            if (time.time() - start_time) > 1200:#Check How long estimating model. If estimating longer than 10 minute - model saving as bad
                print('Model solving too long!')
                model.save(self.dir_path + f'/models/_BAD_{time.time()}.mph')
        except Exception as ex:
            print(ex)
            model.save(self.dir_path + f'/models/CRASH.mph')
            self.client.clear()
            return 0.0,model,0,self.dir_path,self.client

        idx = self._save_simulation_result(structure, model)

        try:
            if receivers == 2:
                out = [model.evaluate('avep_out'),model.evaluate('avep_out2')]
                target_evo = list(out[0][72:])+list(out[1][72:])
                #target_evo = np.array(target_evo) - np.array(total_aveop())
            else:
                out = model.evaluate('avep_out')
                target_evo = out[72:]
        except Exception as ex:
            print(ex)
            model.save(self.dir_path + f'/models/CRASH.mph')
            self.client.clear()
            return 0.0,model,idx,self.dir_path,self.client

        #self.client.clear()

        #else:
        #    print(f'Cached: {target}')

        return target_evo,model,idx,self.dir_path,self.client

    def _poly_add(self, model, polygons):
        for n, poly in enumerate(polygons):
            try:
                model.java.component('comp1').geom('geom1').create('pol' + str(n + 1), 'Polygon')
            except Exception:
                pass
            model.java.component('comp1').geom('geom1').feature('pol' + str(n + 1)).set('x', poly[0])
            model.java.component('comp1').geom('geom1').feature('pol' + str(n + 1)).set('y', poly[1])
        model.java.component("comp1").geom("geom1").create("dif1", "Difference")
        model.java.component('comp1').geom('geom1').feature("dif1").selection('input').set('r2')
        model.java.component('comp1').geom('geom1').feature("dif1").selection('input2').set('pol1')
        return model

    def _save_simulation_result(self, configuration, model):
        if not os.path.exists(self.dir_path+'/models'):
            os.mkdir(self.dir_path+'/models')
        model_uid = str(uuid4())
        #model.save(self.dir_path+f'/models/{model_uid}.mph')
        db = pickledb.load(self.dir_path+'/comsol_db.saved', False)
        db.set(str(configuration), model_uid)
        db.dump()

        if not os.path.exists(self.dir_path+'/structures'):
            os.mkdir(self.dir_path+'/structures')

        with open(self.dir_path+f'/structures/{model_uid}.str', 'wb') as f:
            pickle.dump(configuration, f)

        return model_uid

    def _load_simulation_result(self, client, configuration):
        db = pickledb.load(self.dir_path+'/comsol_db.saved', False)

        model_uid = db.get(str(configuration))

        if model_uid is False:
            return None, None

        model = client.load(self.dir_path+f'/models/{model_uid}.mph')

        return model, model_uid

    def _save_fitness(self, configuration, fitness):
        array_structure = [[[p.x, p.y] for p in poly.points] for poly in configuration.polygons]
        db = pickledb.load(self.dir_path+'/fitness_db.saved', False)
        db.set(str(array_structure), str(round(fitness, 4)))
        db.dump()

    def _load_fitness(self, configuration):
        array_structure = [[[p.x, p.y] for p in poly.points] for poly in configuration.polygons]
        db = pickledb.load(self.dir_path+'/fitness_db.saved', False)

        db_models = pickledb.load(self.dir_path+'/comsol_db.saved', False)

        model_uid = db_models.get(str(configuration))

        result = db.get(str(array_structure))

        if result is False:
            return None, None
        else:
            fitness = float(result)

        return float(fitness), model_uid
