"""
Свойства задачи
"""


# =============================================================================


__all__ = [
    'Task',
    'RootTask',
]


# =============================================================================


class Task(object):
    """Базовые свойства задачи"""

    def __init__(self, name, span, *, weight=1):
        """
        Инициализация
        :param name: идентификатор
        :param span: продолжительность выполнения
        :param weight: "вес" при расчете загрузки системы
        """
        self.name = name
        self.span = span
        self.weight = weight
        self.dependent_tasks = list()

    def add_dependent_task(self, task, delay):
        """
        Добавление зависимой задачи
        :param task: свойства задачи
        :param delay: задержка запуска
        :return: ссылка на объект вызова
        """
        assert isinstance(task, Task)
        self.dependent_tasks.append((task, delay))
        return self


# =============================================================================


class RootTask(Task):
    """Свойства корневой задачи"""

    def __init__(self, name, span, frequency, *,
                 t0_min=0, t0_max=None, weight=1):
        """
        Инициалиация
        :param name: идентификатор
        :param span: продолжительность выполнения
        :param frequency: частота выполнения
        :param t0_min: минимальное время начала
        :param t0_max: максимальное время начала
        :param weight: "вес" при расчете загрузки системы
        """
        super().__init__(name, span, weight=weight)
        self.frequency = frequency
        self.t0_min = t0_min
        self.t0_max = t0_max
