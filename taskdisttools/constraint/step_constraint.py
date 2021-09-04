"""
Абсолютное ограничение на шаг t0
"""


# =============================================================================


from taskdisttools.constraint import AbsoluteConstraint


# =============================================================================


__all__ = [
    'StepConstraint',
]


# =============================================================================


class StepConstraint(AbsoluteConstraint):
    """Абсолютное ограничение на шаг t0"""

    def __init__(self, step_size):
        """
        Инициализация
        :param step_size: размер шага
        """
        self._step_size = step_size

    def test(self, t0, start_times):
        """
        Проверка ограничения
        :param t0: тестируемое значение
        :param start_times: t0 для всех задач
        :return: True если t0 удовлетворяет ограничению, инче False
        """
        return t0 % self._step_size == 0

    def apply(self, t0, start_times):
        """
        Применение ограничения
        :param t0: корректируемое значение
        :param start_times: t0 для всех задач
        :return: скорректированное значение t0
        """
        remainder = t0 % self._step_size
        if remainder != 0:
            t_lower = t0 - remainder
            t_upper = t_lower + self._step_size
            if t0 - t_lower <= t_upper - t0:
                t0 = t_lower
            else:
                t0 = t_upper

        return t0
