from gefest.core.opt.operators.mutation import mutation
from gefest.core.opt.operators.crossover import crossover
from gefest.core.opt.operators.crossover_for_points_in_poly import crossover as point_cross
class EvoOperators:
    def __init__(self, crossover, mutation):
        self.crossover = crossover
        self.mutation = mutation


def default_operators():
    return EvoOperators(crossover=crossover, mutation=mutation)
def point_crossover():
    return EvoOperators(crossover=point_cross, mutation=mutation)