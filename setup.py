#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

from os import path

README_FILE = 'README.rst'

long_description = None
if path.exists(README_FILE):
    with open(README_FILE) as fh:
        long_description = fh.read()

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

with open('dev-requirements.txt') as f:
    tests_require = f.read().splitlines()

entry_points = {
    'console_scripts': [
        'cfssl-cli = cfsslcli.__main__:main'
    ],
}

setup(
    name='cfssl-cli',
    version='1.0.0',
    author='Rémi Alvergnat',
    author_email='toilal.dev@gmail.com',
    description='This CLI tool allows you to interact with a remote CFSSL server.',
    packages=find_packages(),
    install_requires=install_requires,
    tests_require=tests_require,
    entry_points=entry_points,
    long_description=long_description,
    url='https://toilal.github.io/python-cfssl-cli',
    download_url='https://github.com/Toilal/python-cfssl-cli',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers'
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: System :: Networking',
    ],
)
