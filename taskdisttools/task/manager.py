"""
Менеджер задач
"""


# =============================================================================


from collections import namedtuple
from collections import defaultdict
from taskdisttools.task import RootTask
from taskdisttools.constraint import Constraint
from taskdisttools.constraint import RelativeConstraint as RelConst


# =============================================================================


__all__ = [
    'TaskManager',
]


# =============================================================================


_TaskData = namedtuple('_TaskData', 'frequency span weight')


# =============================================================================


class TaskManager(object):
    """
    Менеджер задач
     - хранение списка задач
     - хранение ограничений
     - формирование ИД для расчета с учетом ограничений
    """

    def __init__(self):
        """Инициализация"""
        self._root_tasks = dict()
        self._constraints = defaultdict(list)

    @property
    def root_tasks(self):
        """Получение корневых задач"""
        return self._root_tasks

    def add_root_task(self, root_task):
        """
        Добавление корневой задачи
        :param root_task: корневая задача
        :return: ссылка на объект вызова
        """
        assert isinstance(root_task, RootTask)
        self._root_tasks[root_task.name] = root_task
        return self

    def add_constraint(self, name, constraint):
        """
        Добавление ограничения на t0 для заданной задачи
        :param name: идентификатор задачи
        :param constraint: ограничение
        :return: ссылка на объект вызова
        """
        assert isinstance(constraint, Constraint)
        self._constraints[name].append(constraint)
        return self

    def get_start_times(self, name, t_max):
        """
        Генерация возможных значений t0 для корневой задачи
        :param name: идентификатор задачи
        :param t_max: максимальная эпоха моделирования
        :return: генератор t0 для корневой задачи
        """
        task = self._root_tasks[name]
        if task.t0_max is None:
            return range(task.t0_min, t_max)
        else:
            return range(task.t0_min, task.t0_max + 1)

    def make_model_input(self, root_start_times, *,
                         apply_constraints=True):
        """
        Формирование ИД для моделирования
        :param root_start_times: t0 для корневых задач
        :param apply_constraints: флаг применения ограничений
        :return: t0 и данные по всем задачам
        """
        start_times = dict()
        tasks_data = dict()
        for task in self._root_tasks.values():
            t0 = root_start_times[task.name]
            self._append_task_input(start_times, tasks_data, task, t0)
            self._process_dependent_tasks(
                start_times, tasks_data, task.dependent_tasks,
                t0, task.span, task.frequency
            )

        if apply_constraints:
            start_times = self._apply_constraints(start_times)
        return start_times, tasks_data

    def _apply_constraints(self, start_times):
        """
        Применение ограничений
        :param start_times: словарь исходных значений t0
        :return: словарь скорректированных значений t0
        """
        resolved_tasks = set()
        for task in self._constraints.keys():
            self._resolve_constraints(
                start_times, task, resolved_tasks, set()
            )

        return start_times

    def _resolve_constraints(self, start_times, task, resolved, unresolved):
        """
        Разрешение ограничений
        :param start_times: словарь исходных значений t0
        :param task: идентификатор текущей задачи
        :param resolved: множество задач с разрешенными ограничениями
        :param unresolved: множество задач с неразрешенными ограничениями
        """
        if task in resolved or task not in self._constraints:
            return
        if task in unresolved:
            raise RuntimeError(f'Circular constraints on task "{task}"')

        unresolved.add(task)
        constraints = sorted(
            self._constraints[task], key=lambda c: isinstance(c, RelConst))

        for cnt in constraints:
            if isinstance(cnt, RelConst):
                self._resolve_constraints(
                    start_times, cnt.target, resolved, unresolved)
            start_times[task] = cnt.apply(start_times[task], start_times)

        for cnt in constraints:
            if not cnt.test(start_times[task], start_times):
                raise RuntimeError(f'Constraints conflict on task "{task}"')

        unresolved.remove(task)
        resolved.add(task)

    @staticmethod
    def _process_dependent_tasks(start_times, tasks_data, dependent_tasks,
                                 parent_t0, parent_span, parent_frequency):
        """
        Обработка зависимых задач
        :param start_times: словарь t0
        :param tasks_data: данные задач
        :param dependent_tasks: список зависимых задач
        :param parent_t0: t0 родительской задачи
        :param parent_span: длительность выполнения родительской задачи
        :param parent_frequency: частота запуска родительской задачи
        """
        for task, delay in dependent_tasks:
            task_t0 = parent_t0 + parent_span + delay
            TaskManager._append_task_input(
                start_times, tasks_data,
                task, task_t0, parent_frequency
            )
            TaskManager._process_dependent_tasks(
                start_times, tasks_data, task.dependent_tasks,
                task_t0, task.span, parent_frequency
            )

    @staticmethod
    def _append_task_input(start_times, tasks_data,
                           task, t0, frequency=None):
        """
        Добавление ИД по задаче
        :param start_times: словарь t0
        :param tasks_data: данные задач
        :param task: задача
        :param t0: время запуска
        :param frequency: частота выполнения
        """
        if isinstance(task, RootTask):
            frequency = task.frequency
        start_times[task.name] = t0
        tasks_data[task.name] = _TaskData(
            frequency=frequency,
            span=task.span,
            weight=task.weight
        )
