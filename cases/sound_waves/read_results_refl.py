import pandas as pd
import gc
import os
import pickledb
import numpy as np
import mph
import pickle
import matplotlib.pyplot as plt
from uuid import uuid4
from gefest.core.structure.structure import Structure, get_random_structure
from cases.sound_waves.configuration_comsol import sound_domain,sound_sampler
from cases.main_conf import opt_params

##########
opt_params.is_closed = True
opt_params.pop_size = 10
opt_params.n_steps = 2
opt_params.n_polys = 1
opt_params.n_points = 30
##########

domain, task_setup = sound_domain.configurate_domain(
    poly_num=opt_params.n_polys,
    points_num=opt_params.n_points,
    is_closed=opt_params.is_closed,
)
print(domain.min_dist)
print(domain.allowed_area)
best_structure = get_random_structure(domain)
with open("best_structure.pickle", "wb") as handle:
    pickle.dump(best_structure, handle, protocol=pickle.HIGHEST_PROTOCOL)
print(best_structure)
sampler = sound_sampler.configurate_sampler(domain=domain)
def _poly_add(model, polygons):
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

def _save_simulation_result(configuration, model):
    if not os.path.exists('./models'):
        os.mkdir('./models')
    model_uid = str(uuid4())
    model.save(f'./models/{model_uid}.mph')
    db = pickledb.load('comsol_db.saved', False)
    db.set(str(configuration), model_uid)
    db.dump()

    if not os.path.exists('./structures'):
        os.mkdir('./structures')

    with open(f'./structures/{model_uid}.str', 'wb') as f:
        pickle.dump(configuration, f)

    return model_uid


client = mph.Client()
model = client.load('gefest/tools/estimators/simulators/comsol/sound/model/Reflect_run.mph')
poly_box = []
print('Start COMSOL')
for i, pol in enumerate(best_structure.polygons):
    poly_repr = []
    poly_repr.append(' '.join([str(pt.x) for pt in pol.points]))
    poly_repr.append(' '.join([str(pt.y) for pt in pol.points]))
    poly_box.append(poly_repr)
#print(poly_box)

try:
    #model = _poly_add(model, poly_box)

    model.build()
    model.mesh()
    model.solve()
except Exception as ex:
    print(ex)
    client.clear()

print(model.exports())
idx = _save_simulation_result(best_structure, model)
out = model.evaluate('avep_out')
print(out)

client.clear()
##########################################

model = client.load('gefest/tools/estimators/simulators/comsol/sound/model/Reflect_run.mph')
poly_box = []
print('Start COMSOL')
for i, pol in enumerate(best_structure.polygons):
    poly_repr = []
    poly_repr.append(' '.join([str(pt.x) for pt in pol.points]))
    poly_repr.append(' '.join([str(pt.y) for pt in pol.points]))
    poly_box.append(poly_repr)
#print(poly_box)

try:
    model = _poly_add(model, poly_box)

    model.build()
    model.mesh()
    model.solve()
except Exception as ex:
    print(ex)
    client.clear()
#############################################
print(model.exports())
idx = _save_simulation_result(best_structure, model)

out_def = model.evaluate('avep_out')
plt.plot(out,label='w/o def')
plt.plot(out_def,label='with def')
plt.show()
