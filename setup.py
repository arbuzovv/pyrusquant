import sys
from setuptools import setup, find_packages

import pyrusquant

if sys.version_info < (3, 7):
    raise RuntimeError("pyrusquant requires Python 3.7+")

description_short = """
Pyrusquant is a package for interaction with alternative data, trading API of different exchanges and brokers'    
"""

with open('README.md') as file:
    description = file.read()

with open('README.md') as file:
    text_license = file.read()

with open('requirements.txt') as file:
    requirements = file.read().splitlines()


setup(
    name='pyrusquant',
    version=pyrusquant.__version__,
    description=description_short,
    long_description=description,
    author='Arbuzov Vyacheslav, Petukhov Maksim',
    url='https://github.com/arbuzovv/pyrusquant',
    packages=find_packages(),
    license=text_license,
    install_requires=requirements,
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
)
