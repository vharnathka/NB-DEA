import os
from setuptools import setup, find_packages

curdir = os.path.abspath(os.path.dirname(__file__))
MAJ = 0
MIN = 0
REV = 0
VERSION = '%d.%d.%d' % (MAJ, MIN, REV)
with open(os.path.join(curdir, 'nb_dea/version.py'), 'w') as fout:
        fout.write(
            "\n".join(["",
                       "# THIS FILE IS GENERATED FROM SETUP.PY",
                       "version = '{version}'",
                       "__version__ = version"]).format(version=VERSION)
        )
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
