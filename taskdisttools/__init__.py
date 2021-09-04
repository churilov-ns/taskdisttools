"""
TaskDistTools
=============

Библиотека, предназначенная для распределения выполняемых задач (ТЦ)
во времени с точки зрения оптимизации нагрузки на вычислительную систему.
"""

#  Версия
__version__ = '0.0.15'

# Модули
from . import constraint
from . import optimizer
from . import task
from . import utils
