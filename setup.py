#!/usr/bin/env python
from setuptools import setup


if __name__ == '__main__':
    setup(
        name='ue4rl',
        version='0.0.0',
        description='Utilities to run UE4 games as RL environment on top of ue4ml',
        author='Pierre Delaunay',
        packages=[
            'ue4rl',
        ],
        setup_requires=['setuptools'],
        tests_require=['pytest', 'flake8', 'codecov', 'pytest-cov'],
    )
