import os
import runpy
from setuptools import setup, find_packages

metadata = runpy.run_path(os.path.join('mkatsim', '_version.py'))

# https://packaging.python.org/distributing/
setup(
    name='mkatsim',
    version=metadata['__version__'],
    description=metadata['__doc__'],
    # long_description=open('README.txt').read(),
    url=metadata['__url__'],
    author=metadata['__author__'],
    author_email=metadata['__email__'],
    license='??',  # license=open('LICENSE').read(),
    # classifiers=[...],
    keywords='MeerKAT telescope simulator',
    packages=find_packages(exclude=['docs', 'tests', 'venv']),
    install_requires=[
        'astropy',
        'python-casacore',
        ],
    # package_data={
    #     'sample': ['package_data.dat'],
    #     },
    data_files=[
        ('config', [
            'config/makems.cfg',
            'config/mkat_antennas.enu',
            ]),
        ],
    entry_points={
        'console_scripts': [
            'mkspsf=mkatsim.psf.__main__:cli',
            'mksarray=mkatsim.subarray.__main__:cli',
            ],
        },
)
