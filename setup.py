from setuptools import setup, find_packages
from os.path import join, dirname
import taskdisttools


setup(
    name='taskdisttools',
    version=taskdisttools.__version__,
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.txt')).read(),
    install_requires=['numpy'],
)
