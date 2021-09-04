"""
Функции для формирования расписания выполнения задач
"""


# =============================================================================


__all__ = [
    'model_launches',
    'make_timetable',
]


# =============================================================================


def model_launches(t0, f, s, t_max):
    """
    Моделирование запусков задачи
    :param t0: время первого запуска
    :param f: частота запусков
    :param s: продолжительность работы
    :param t_max: максимальная эпоха моделирования
    :return: генератор эпох, на которые приходтся активность задачи
    """
    t = t0
    while t < t_max:
        yield t
        if t - t0 < s - 1:
            t += 1
        else:
            t0 += f
            t = t0


# =============================================================================


def make_timetable(start_times, task_data, t_max):
    """
    Формирование расписания выполнения задач
    :param start_times: словарь, содержащий время первого запуска задач
    :param task_data: словарь, содержащий данные задач
        (частота, продолжительность выполнения)
    :param t_max: максимальная эпоха моделирования
    :return: список активных задач на каждую эпоху моделирования
    """
    timetable = list()
    while len(timetable) < t_max:
        timetable.append(list())

    for task, t0 in start_times.items():
        data = task_data[task]
        for t in model_launches(t0, data.frequency, data.span, t_max):
            timetable[t].append(task)

    return timetable
