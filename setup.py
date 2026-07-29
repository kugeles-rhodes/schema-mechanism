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
    python_requires='>=3.9',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=[
        'anytree==2.8.0',
        'lark==1.1.1',
        'numpy==1.21.4',
        'pynput==1.7.6',
        'pyyaml==6.0',
        'scikit-learn==1.6.1',
        'scipy==1.8.0',
        'optuna==2.10.1',
        'pandas==1.4.2',
    ],
)
