import os
import shutil
import pickle
from copy import deepcopy

from tqdm import tqdm
from pathlib import Path


def design(n_steps: int,
           pop_size: int,
           estimator,
           sampler,
           optimizer,
           extra=False,
           path = 'HistoryFiles',
           extra_break=250):
    """
    Generative design procedure
    :param n_steps: (Int) number of generative design steps
    :param pop_size: (Int) number of samples in population
    :param estimator: (Object) estimator with .estimate() method
    :param sampler: (Object) sampler with .sample() method
    :param optimizer: (Object) optimizer with .optimize() method
    :param extra: (Bool) flag for extra sampling
    :return: (List[Structure]) designed samples
    """

    def _save_res(performance, samples, dice_metric):
        """
        Saving results in pickle format
        :param performance: (List), performance of samples
        :param samples: (List), samples to save
        :return: None
        """
        with open(Path(path, f'performance_{i}.pickle'), 'wb') as handle:
            pickle.dump(performance, handle, protocol=pickle.HIGHEST_PROTOCOL)

        with open(Path(path, f'population_{i}.pickle'), 'wb') as handle:
            pickle.dump(samples, handle, protocol=pickle.HIGHEST_PROTOCOL)

        with open(Path(path, f'dice_metric_{i}.pickle'), 'wb') as handle:
            pickle.dump(dice_metric, handle, protocol=pickle.HIGHEST_PROTOCOL)

        return

    def _remain_best(performance, samples, dice_metric):
        """
        From current population we remain best only
        :param performance: (List), performance of samples
        :param samples: (List), samples to save
        :return: (Tuple), performance and samples
        """
        # Combination of performance and samples
        perf_samples = list(zip(performance, samples, dice_metric))

        # Sorting with respect to performance
        sorted_pop = sorted(perf_samples, key=lambda x: x[0])[:pop_size]

        performance = [x[0] for x in sorted_pop]
        samples = [x[1] for x in sorted_pop]
        dice_metric = [x[2] for x in sorted_pop]

        return performance, samples, dice_metric

    path = path

    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)

    samples = sampler.sample_init(n_samples=pop_size)


    for i in range(n_steps):
        performance, dice_metric = estimator.estimate(population=samples)

        # Choose best and save the results
        performance, samples, dice_metric = _remain_best(performance, samples,dice_metric)
        print(f'\nBest performance is {performance[0]},dice is {dice_metric[0]}')

        _save_res(performance, samples, dice_metric)

        if optimizer:
            samples = optimizer.step(population=samples, performance=performance, n_step=i)

        # Extra sampling if necessary
        # or if optimizer is missing
        if not optimizer or extra:
            if not optimizer:
                samples = sampler.sample(n_samples=pop_size)
            elif i<extra_break:#stop extra sampling after extra_break iterations
                extra_samples = sampler.sample(n_samples=(pop_size))
                samples = samples + extra_samples
        print('len samples',len(samples))
        if i == n_steps-1:
            i +=1
            performance, dice_metric = estimator.estimate(population=samples)

            # Choose best and save the results
            performance, samples,dice_metric = _remain_best(performance, samples,dice_metric)
            print(f'\nBest performance is {performance[0]},dice is {dice_metric[0]}')
            _save_res(performance, samples, dice_metric)

    return samples
