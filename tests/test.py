#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# =============================================================================


import numpy as np
from taskdisttools.task import RootTask, TaskManager
from taskdisttools.optimizer import GreedyOptimizer
from taskdisttools.constraint import DelayConstraint, StepConstraint
from taskdisttools.utils import Beautifier


# =============================================================================


if __name__ == '__main__':
    tm = TaskManager()
    tm.add_root_task(
        RootTask('0050 - ТЦ экспресс-оценка', 4, 25, t0_max=59)
    )
    tm.add_root_task(
        RootTask('0052 - ТЦ экспресс-оценка (без 1F)', 4, 25, t0_max=59)
    )
    tm.add_root_task(
        RootTask('0300 - ТЦ экспресс-оценка (все НКА)', 4, 25, t0_max=59)
    )

    tm.add_constraint(
        '0052 - ТЦ экспресс-оценка (без 1F)',
        StepConstraint(5)
    )
    tm.add_constraint(
        '0050 - ТЦ экспресс-оценка',
        DelayConstraint('0052 - ТЦ экспресс-оценка (без 1F)', 2)
    )

    optimizer = GreedyOptimizer(np.std, n_iterations=1)
    optimizer.optimize(tm, 1440)

    print('')
    print('Optimal start times:')
    print('====================')
    for task_name, t0 in optimizer.results_.start_times.items():
        print(f'{task_name}: {t0}')

    bf = Beautifier()
    bf.add_alignment([
        '0050 - ТЦ экспресс-оценка',
        '0052 - ТЦ экспресс-оценка (без 1F)',
        '0300 - ТЦ экспресс-оценка (все НКА)'
    ], np.max)

    bf_results = bf.apply(optimizer.results_, tm)
    print('')
    print('Beautified start times:')
    print('====================')
    for task_name, t0 in bf_results.start_times.items():
        print(f'{task_name}: {t0}')
