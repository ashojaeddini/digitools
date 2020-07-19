# Packaging Python Applications

## Generate Distributables
Execute the following command to generate source and binary distributables:

```
python setup.py sdist bdist_wheel
```

References:
- https://packaging.python.org/tutorials/packaging-projects

## Create a Virtual Environment

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
- https://packaging.python.org/guides/installing-using-pip-and-virtual-environments
- https://docs.python.org/3/library/venv.html

### Using _pipx_
This option can be used for installing CLI applications in a virtual environment.

```
python -m pip install --user pipx
python -m pipx ensurepath
pipx install <package>
```

Requirements:
- Python 3.6+ is required to install pipx

References:
- https://packaging.python.org/guides/installing-stand-alone-command-line-tools
- https://github.com/pipxproject/pipx

### Using _pex_
```
pip install pex
python setup.py bdist_pex --bdist-all --bdist-dir=<path>
```

References:
- https://github.com/pantsbuild/pex
- https://github.com/pantsbuild/pex/blob/master/docs/buildingpex.rst
- https://pex.readthedocs.io/en/stable
- https://stackoverflow.com/questions/40470046/packaging-local-module-with-pex

### Using _pipenv_
```
pip install --user pipenv
pipenv install <package>
pipenv run python main.py
```

References:
- https://packaging.python.org/tutorials/managing-dependencies
- https://pipenv.pypa.io/en/latest/basics
