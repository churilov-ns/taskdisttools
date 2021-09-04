"""
Функция расчета загруженности системы
"""


# =============================================================================


import numpy as _np


# =============================================================================


__all__ = [
    'get_loading',
]


# =============================================================================


def get_loading(timetable, tasks_data):
    """
    Функция расчета загрузки системы
    :param timetable: расписание выполнения задач
    :param tasks_data: словарь, содержащий данные задач (вес)
    :return: массив уровней загрузки системы на каждую эпоху
    """
    loading = [0] * len(timetable)
    for t, tasks in enumerate(timetable):
        if tasks_data is None:
            loading[t] += len(tasks)
        else:
            for task in tasks:
                loading[t] += tasks_data[task].weight

    return _np.array(loading)
