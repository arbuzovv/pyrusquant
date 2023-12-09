from setuptools import setup, find_packages

import pyrusquant


description_short = """
Pyrusquant is a package for interaction with alternative data, trading API of different exchanges and brokers'    
"""

with open('README.md') as file:
    description = file.read()

with open('README.md') as file:
    text_license = file.read()

with open('requirements.txt') as file:
    requirements = [pack.replace('==', '>=') for pack in file.read().splitlines()]


setup(
    name='pyrusquant',
    version=pyrusquant.__version__,
    description=description_short,
    long_description=description,
    long_description_content_type='text/markdown',
    author='Arbuzov Vyacheslav, Petukhov Maksim',
    author_email='Vyacheslav Arbuzov <noreply@github.com>',
    url='https://github.com/arbuzovv/pyrusquant',
    packages=find_packages(),
    license=text_license,
    install_requires=requirements,
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
    python_requires=">=3.7",
)