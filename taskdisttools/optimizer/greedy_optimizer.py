"""
'Жадный' алгоритм оптимизации
"""


# =============================================================================


import copy
import random
from .optimizer import Optimizer


# =============================================================================


__all__ = [
    'GreedyOptimizer',
]


# =============================================================================


class GreedyOptimizer(Optimizer):
    """'Жадный' алгоритм оптимизации"""

    def __init__(self, metric, *, n_iterations=10, random_state=None):
        """
        Инициализация
        :param metric: оптимизируемая метрика
        :param n_iterations: кол-во итераций
        :param random_state: состояние ДСЧ
        """
        super().__init__(metric)
        self._n_iterations = n_iterations
        self._random_state = random_state

    def _do_optimize(self, task_manager, t_max):
        """
        Непосредственно оптимизация
        :param task_manager: менеджер задач
        :param t_max: максимальная эпоха моделирования
        """
        print('Greedy optimization begin')
        print('=========================')

        if self._random_state is not None:
            random.seed(self._random_state)
        opt_results = None

        for i in range(self._n_iterations):
            results = self._next_iter(task_manager, t_max)
            print(f'Iteration: {i + 1}, score: {results.score}')
            if opt_results is None or results.score < opt_results.score:
                print(' >>> new best score!')
                opt_results = results

        self.results_ = opt_results

    def _next_iter(self, task_manager, t_max):
        """
        Итерация оптимизации
        :param task_manager: менеджер задач
        :param t_max: максимальная эпоха моделирования
        """
        available_tasks = list(task_manager.root_tasks.keys())[1:]
        opt_results = copy.deepcopy(self.results_)

        while len(available_tasks) > 0:
            i = random.randint(0, len(available_tasks) - 1)
            cur_task = available_tasks[i]

            for t0 in task_manager.get_start_times(cur_task, t_max):
                sts = copy.deepcopy(opt_results.start_times)
                sts[cur_task] = t0
                results = self._evaluate(sts, task_manager, t_max)
                if results.score < opt_results.score:
                    opt_results = results

            del available_tasks[i]

        return opt_results
