#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import find_packages
from cx_Freeze import setup, Executable

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

include_files = [("cfssl.yml.dist", "cfssl.yml")]

setup(
    name='cfssl-cli',
    version='0.0.1',
    author='Rémi Alvergnat',
    author_email='toilal.dev@gmail.com',
    description='This CLI tool allows you to interact with a remote CFSSL server.',
    options={"build_exe": {"packages": ["multiprocessing", "idna", "_cffi_backend", "pkg_resources._vendor"], "include_files": include_files}},
    executables=[Executable("cfsslcli/__main__.py", targetName="cfssl.exe")],
    packages=find_packages(),
    install_requires=install_requires,
    tests_require=tests_require,
    entry_points=entry_points,
    long_description=long_description,
    url='https://toilal.github.io/python-cfssl-cli',
    download_url='https://github.com/Toilal/python-cfssl-cli',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers'
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: System :: Networking',
    ],
)
