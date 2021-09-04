"""
Ограничение на время запуска ТЦ
"""


# =============================================================================


import abc


# =============================================================================


__all__ = [
    'Constraint',
    'AbsoluteConstraint',
    'RelativeConstraint',
]


# =============================================================================


class Constraint(abc.ABC):
    """Ограничение на время запуска ТЦ"""

    @abc.abstractmethod
    def test(self, t0, start_times):
        """
        Проверка ограничения
        :param t0: тестируемое значение
        :param start_times: t0 для всех задач
        :return: True если t0 удовлетворяет ограничению, инче False
        """
        pass

    @abc.abstractmethod
    def apply(self, t0, start_times):
        """
        Применение ограничения
        :param t0: корректируемое значение
        :param start_times: t0 для всех задач
        :return: скорректированное значение t0
        """
        pass


# =============================================================================


class AbsoluteConstraint(Constraint, abc.ABC):
    """Абсолютное ограничение"""
    pass


# =============================================================================


class RelativeConstraint(Constraint, abc.ABC):
    """Относительное ограничение"""

    def __init__(self, target):
        """
        Инициализация
        :param target: целевая задача
        """
        self.target = target
