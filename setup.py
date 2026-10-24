#!/usr/bin/env python

from setuptools import find_packages
from setuptools import setup

setup(
    name='SchemaMechanism',
    version='0.1.0',
    description='A Python version of Drescher\'s Schema Mechanism',
    author='Sean Kugele',
    author_email='seankugele@gmail.com',
    url='https://github.com/skugele/schema-mechanism',
    license='MIT',
    python_requires='>=3.12',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
    ],
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    # compatible ranges; the lower bounds were verified as a set (see requirements.txt for the pinned lock)
    install_requires=[
        'anytree>=2.13,<3',
        'lark>=1.3,<2',
        'numpy>=2.1,<3',
        'pynput>=1.8,<2',
        'pyyaml>=6.0.2,<7',
        'scipy>=1.14.1,<2',
        'optuna>=4.0,<6',
        'pandas>=2.2.3,<4',
    ],
)
