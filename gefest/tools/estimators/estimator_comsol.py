from typing import Optional, Callable, List
from gefest.core.structure.structure import Structure
import numpy as np

class Estimator:
    """
    ::TODO:: make abstract class for further specific realizations in different problems
    """

    def __init__(self, estimator, loss: Optional[Callable] = None):
        """
        Base estimator class, Structure -> Performance
        :param estimator: estimator with .estimate() method
        :param loss: function for minimizing, it takes estimator as argument,
                     if None estimator using as cost function
        """
        self.estimator = estimator
        self.loss = loss

    def estimate(self, population: List[Structure]):
        """
        Estimation of performance
        :param population: List(Structure) population of structures for estimation
        :return: List(Float) performance of population
        """
        performance = []
        dice_metric = []
        size = len(population)
        best_fitness = np.inf
        if self.loss:
            for i in range(size):
                one_perf, one_dice, model, idx, dir_path, client = self.loss(population[i], self.estimator)
                if None in [one_perf, one_dice, model, idx, dir_path, client]:#Check if is estimate ends with errors
                    continue
                if one_perf < best_fitness:
                    best_fitness = one_perf
                    model.save(dir_path + f'/models/_{idx}_{best_fitness}.mph')
                client.clear()
                performance.append(one_perf)
                dice_metric.append(one_dice)

        else:
            for i in range(size):
                one_perf = self.estimator.estimate(population[i])
                performance.append(one_perf)

        return performance, dice_metric
