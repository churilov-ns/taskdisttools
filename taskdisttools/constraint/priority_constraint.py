"""
Относительное ограничение на время запуска (с учетом очередности)
"""


# =============================================================================


from taskdisttools.constraint import DelayConstraint


# =============================================================================


__all__ = [
    'PriorityConstraint',
]


# =============================================================================


class PriorityConstraint(DelayConstraint):
    """Относительное ограничение на время запуска (с учетом очередности)"""

    def __init__(self, target, max_delay):
        """
        Инициализация
        :param target: целевая задача
        :param max_delay: максимальная зедружка старта
        """
        super().__init__(target, abs(max_delay))

    def test(self, t0, start_times):
        """
        Проверка ограничения
        :param t0: тестируемое значение
        :param start_times: t0 для всех задач
        :return: True если t0 удовлетворяет ограничению, инче False
        """
        target_t0 = start_times[self.target]
        return 0 <= t0 - target_t0 <= self._max_delay

    def apply(self, t0, start_times):
        """
        Применение ограничения
        :param t0: корректируемое значение
        :param start_times: t0 для всех задач
        :return: скорректированное значение t0
        """
        target_t0 = start_times[self.target]
        if t0 - target_t0 > self._max_delay:
            t0 = target_t0 + self._max_delay
        elif t0 < target_t0:
            t0 = target_t0
        return t0
