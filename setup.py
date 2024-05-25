setup(
    name='nb-dea',
    version=VERSION,
    description='Project',
    author='Vedika Harnathka',
    author_email='vharnathka@ucsd.edu'
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "nb-dea=nb-dea.nb-dea:main"
        ],
    },
)