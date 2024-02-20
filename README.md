# django-console-import
This is the test task I received during interview process

# Table of content
[Features](#features) |
[Getting Started](#getting-started) |
[Prerequisites](#prerequisites) |
[Installation](#installation) |
[How to run](#how-to-run) |
[Contributing](#contributing)

# Introduction


# Features
It has BackOffice view at /admin
...

# Getting Started

## Prerequisites

- Install [poetry](https://python-poetry.org/docs/#installation).

This is `Poetry`-bootstrapped project thus all Python dependencies are in `pyproject.toml`. The rest of the stack consists of Docker and Linux.


## Installation
```shell
git clone git@github.com:devova/django-console-import.git
cd django-console-import
poetry install
```
Activate virtual env
```shell
poetry shell
```
Create hardcoded superuser (once)
```shell
docker compose up createsuperuser
```

## How to run
As docker container
```shell
docker compose up api
```
Or as python
```shell
docker compose up migrate collectstatic
python src/manage.py runserver localhost:8000
```
Then navigate to [admin](http://localhost:8000/admin).
  
## Contributing

### Setup & run checks
Sources formatted using `pre-commit`
```shell
pre-commit install
pre-commit run --all-files
```
