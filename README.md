
# Welcome to your Python project!

## compile protobuf files into python
```
protoc -I ./protobuf/core_helper --python_out=./models/core_helper ./protobuf/core_helper/*.proto


```

## misc

This project is set up Python project with dev tooling pre-configured

* black
* flake8
* isort
* mypy
* VS Code support

## Setup
```
# create virtualenv
$ poetry shell

# install dependencies
(.venv)$ poetry install

```

## Develop the code for the stack
```
# run unit tests
pytest

```
