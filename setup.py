import os
from setuptools import setup, find_packages

setup(
    name='nb_dea',
    version='0.0.0',
    description='Project',
    author='Vedika Harnathka',
    author_email='vharnathka@ucsd.edu',
    packages=find_packages(),
    install_requires=[
        'rpy2',
    ],
    entry_points={
        "console_scripts": [
            "nb_dea=nb_dea.nb_dea:main"
        ],
    },
)
