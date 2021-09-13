import setuptools

VERSION = '0.3'

DEPENDENCIES = [
    'fire'
]

setuptools.setup(
    name='digitools',
    version=VERSION,
    author='Ali Shojaeddini',
    description="Digitools is a collection of utilities for Elektron devices.",
    url='https://github.com/ashojaeddini/digitools',
    license='MIT',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=DEPENDENCIES,
    entry_points={'console_scripts': ['digitools = digitools.__main__:main']}
)