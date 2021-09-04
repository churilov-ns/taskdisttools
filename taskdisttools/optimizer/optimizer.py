"""
Интерфейс алгоритма оптимизации
"""


# =============================================================================


import abc
from taskdisttools.task import TaskManager
from taskdisttools.utils import make_timetable, get_loading


# =============================================================================


__all__ = [
    'OptimizationResults',
    'Optimizer',
]


# =============================================================================


class OptimizationResults(object):
    """Результаты оптимизации"""

    def __init__(self, start_times, tasks_data, metric, t_max):
        """
        Инициализация
        :param start_times: оптимальные t0 для каждой задачи
        :param tasks_data: словарь, содержащий данные задач
        :param metric: оптимизируемая метрика
        :param t_max: максимальная эпоха моделирования
        """
        self.start_times = start_times
        self.tasks_data = tasks_data
        self.metric = metric
        self.t_max = t_max
        self.timetable = None
        self.loading = None
        self.score = None
        self.evaluate()

    def evaluate(self):
        """
        Расчет значений оцениваемых параметров
        :return: сслыка на объект вызова
        """
        self.timetable = make_timetable(
            self.start_times, self.tasks_data, self.t_max)
        self.loading = get_loading(self.timetable, self.tasks_data)
        self.score = self.metric(self.loading)
        return self


# =============================================================================


class Optimizer(abc.ABC):
    """Интерфейс алгоритма оптимизации"""

    def __init__(self, metric):
        """
        Инициализация
        :param metric: оптимизируемая метрика
        """
        self._metric = metric
        self.results_ = None  # результаты оптимизации

    def optimize(self, task_manager, t_max):
        """
        Оптимизация
        :param task_manager: менеджер задач
        :param t_max: максимальная эпоха моделирования
        :return: оптимальное t0 для каждой задачи
        """
        assert isinstance(task_manager, TaskManager)
        self._make_baseline(task_manager, t_max)
        self._do_optimize(task_manager, t_max)
        return self.results_

    def _make_baseline(self, task_manager, t_max):
        """
        Получение базового расписания
        :param task_manager: менеджер задач
        :param t_max: максимальная эпоха моделирования
        """
        root_start_times = dict()
        for root_task in task_manager.root_tasks.values():
            root_start_times[root_task.name] = root_task.t0_min
        self.results_ = self._evaluate(
            root_start_times, task_manager, t_max
        )

    def _evaluate(self, root_start_times, task_manager, t_max):
        """
        Расчет параметров расписания для заданных значений t0
        :param root_start_times: t0 для корневых задач
        :param task_manager: менеджер задач
        :param t_max: максимальная эпоха моделирования
        :return: t0 для каждой задачи, расписание,
                 уровни загрузки системы, значение метрики
        """
        start_times, tasks_data = \
            task_manager.make_model_input(root_start_times)
        return OptimizationResults(
            start_times, tasks_data, self._metric, t_max
        )

    @abc.abstractmethod
    def _do_optimize(self, task_manager, t_max):
        """
        Непосредственно оптимизация
        :param task_manager: менеджер задач
        :param t_max: максимальная эпоха моделирования
        """
        pass
