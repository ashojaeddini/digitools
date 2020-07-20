# Packaging Python Applications

## Generating Distributables
Execute the following command to generate source and binary distributables:

```
python setup.py sdist bdist_wheel
```

References:
- [Packaging Python Projects](https://packaging.python.org/tutorials/packaging-projects)

## Creating a Virtual Environment

### Using _venv_
This option can be used for development purposes and testing installations.

```
python -m venv env
source env/bin/activate
which python
pip install <archive_path>
deactivate
```

References:
- [Installing packages using pip and virtual environments](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments)
- [venv — Creation of virtual environments](https://docs.python.org/3/library/venv.html)

### Using _pipx_
This option can be used for installing CLI applications in a virtual environment.

```
pip install pipx
pipx ensurepath
pipx install <package>
```

Requirements:
- Python 3.6+ is required to install pipx

References:
- [Installing stand alone command line tools](https://packaging.python.org/guides/installing-stand-alone-command-line-tools)
- [pipxproject / pipx](https://github.com/pipxproject/pipx)

### Using _pex_
```
pip install pex
python setup.py bdist_pex --bdist-all --bdist-dir=<path>
```

References:
- [pantsbuild / pex](https://github.com/pantsbuild/pex)
- [Building .pex files](https://github.com/pantsbuild/pex/blob/master/docs/buildingpex.rst)

### Using _pipenv_
```
pip install --user pipenv
pipenv install <package>
pipenv run python main.py
```

References:
- [Managing Application Dependencies](https://packaging.python.org/tutorials/managing-dependencies)
- [Basic Usage of Pipenv](https://pipenv.pypa.io/en/latest/basics)
