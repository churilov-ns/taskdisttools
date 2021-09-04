"""
Класс постобработки расписания
"""


# =============================================================================


import copy
import numpy as _np


# =============================================================================


__all__ = [
    'Aligner',
    'Beautifier',
]


# =============================================================================


class Aligner(object):
    """Правило выравнивания"""

    def __init__(self, func=_np.max):
        """
        Инициализация
        :param func: функция выравнивания
        """
        self.func = func
        self.cache = None

    def __call__(self, *args, **kwargs):
        """Применение функции с кешированием результата"""
        self.cache = self.func(*args, **kwargs)
        return self.cache


# =============================================================================


class _Alignment(object):
    """Вспомогательный класс"""

    def __init__(self, tasks, aligner_or_id):
        """
        Инициализация
        :param tasks: список задач
        :param aligner_or_id: новое правило или id существующего
        """
        self.tasks = tasks
        if isinstance(aligner_or_id, int):
            self.aligner = None
            self.aid = aligner_or_id
        elif isinstance(aligner_or_id, Aligner):
            self.aligner = aligner_or_id
            self.aid = None
        else:
            self.aligner = Aligner(aligner_or_id)
            self.aid = None


# =============================================================================


class Beautifier(object):
    """Класс постобработки расписания"""

    def __init__(self):
        """Инициализация"""
        self._alignments = list()

    def add_alignment(self, tasks, aligner_or_id):
        """
        Добавить правило
        :param tasks: список задач
        :param aligner_or_id: новое правило или id существующего
        :return: id добавленного правила
        """
        aid = len(self._alignments)
        self._alignments.append(_Alignment(tasks, aligner_or_id))
        if self._alignments[-1].aligner is None:
            return None
        else:
            return aid

    def apply(self, opt_results, task_manager, *, inplace=False):
        """
        Постобработка
        :param opt_results: результаты оптимизации
        :param task_manager: менеджер задач
        :param inplace: флаг изменения объекта opt_results
        :return: результаты постобработки
        """
        if inplace:
            target = opt_results
        else:
            target = copy.deepcopy(opt_results)

        for alignment in self._alignments:
            self._apply(target, alignment)

        target.start_times, target.tasks_data = \
            task_manager.make_model_input(
                target.start_times, apply_constraints=False
            )

        return target.evaluate()

    def _apply(self, target, alignment):
        """
        Применение правила
        :param target: результаты оптимизации
        :param alignment: правило выравнивания
        """
        assert isinstance(alignment, _Alignment)

        if alignment.aligner:
            aligner = alignment.aligner
        else:
            aligner = self._alignments[alignment.aid].aligner.cache
            if aligner is None:
                raise RuntimeError(
                    f'Alignment at {alignment.aid} '
                    f'referenced before being evaluated'
                )

        self._do_alignment(target, alignment.tasks, aligner)

    @staticmethod
    def _do_alignment(target, tasks, aligner):
        """
        Непосредственно применение правила
        :param target: результаты оптимизации
        :param tasks: список задач
        :param aligner: функция/значение выравнивания
        """
        tasks_data = [(task, target.start_times[task]) for task in tasks]
        tasks_data.sort(key=lambda item: item[1])

        t0_deltas = list()
        for i in range(1, len(tasks_data)):
            t0_deltas.append(tasks_data[i][1] - tasks_data[i-1][1])

        if isinstance(aligner, Aligner):
            aligned_delta = aligner(t0_deltas)
        else:
            aligned_delta = aligner

        base_task_id = None
        min_t0_delta = None
        for i, t0_delta in enumerate(t0_deltas):
            cur_t0_delta = abs(t0_delta - aligned_delta)
            if min_t0_delta is None or cur_t0_delta < min_t0_delta:
                min_t0_delta = cur_t0_delta
                base_task_id = i
        if tasks_data[base_task_id][1] - aligned_delta * base_task_id < 0:
            base_task_id = 0

        t0_base = tasks_data[base_task_id][1]
        for i, task in enumerate(tasks_data):
            target.start_times[task[0]] = int(
                t0_base + aligned_delta * (i - base_task_id)
            )
