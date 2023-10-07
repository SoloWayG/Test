from typing import Optional, Callable, List
from gefest.core.structure.structure import Structure
import numpy as np

class Estimator:
    """
    ::TODO:: make abstract class for further specific realizations in different problems
    """

    def __init__(self, estimator,estimator2, loss: Optional[Callable] = None):
        """
        Base estimator class, Structure -> Performance
        :param estimator: estimator with .estimate() method
        :param loss: function for minimizing, it takes estimator as argument,
                     if None estimator using as cost function
        """
        self.estimator = estimator
        self.estimator2 = estimator2
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
        if self.loss:
            for i in range(size):
                one_perf, one_dice= self.loss(population[i], self.estimator,self.estimator2)
                performance.append(one_perf)
                dice_metric.append(one_dice)

        else:
            for i in range(size):
                one_perf = self.estimator.estimate(population[i])
                performance.append(one_perf)

        return performance, dice_metric
