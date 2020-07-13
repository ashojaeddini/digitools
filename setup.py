from setuptools import setup, find_packages

setup(
    name='digitone',
    version='0.1',
    url='https://github.com/ashojaeddini/digitone',
    author='Ali Shojaeddini',
    license='MIT',
    packages=find_packages(),
    entry_points= {'console_scripts': ['digitone = digitone.__main__:main']},
    description='A set of utilities for managing the Elektron Digitone'
)