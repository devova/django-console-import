# django-console-import
This is the test task I received during interview process

# Table of content
[Assumptions](#assumptions) |
[Things to improve](#things-to-improve) |
[Getting Started](#getting-started) |
[Prerequisites](#prerequisites) |
[Installation](#installation) |
[How to run](#how-to-run) |
[Contributing](#contributing)

# Assumptions
- The `pol_pol` table has some string length constraints that were not explicitly defined but follow logical rules.
- There is no dedicated `pol_ratings` table because this data isn't going to be updated
- Identifiers in imported files are treated as external ones


# Things to improve
- [ ] use debug tools to optimise DB (admin with 1B records feels slow), more likely CTA
- [ ] "ask product" for more use cases, perhaps there is a reason to have dedicated `pol_ratings` table
- [ ] properly handle script termination
- [ ] check whether `import_export` package can do input validation, avoid using Pydantic
- [ ] introduce [tqdm](https://github.com/tqdm/tqdm) for console progress
- [ ] change namings from POL to POI
- [ ] try concurrent import or even introduce distributed import (a.k.a. celery or similar)

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

## How to run API
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

## How to import files
Or as python
```shell
docker compose up migrate
python src/manage.py import-pol --filename <file> --stop-on-error --no-dry-run
```

## Contributing

### Setup & run checks
Sources formatted using `pre-commit`
```shell
pre-commit install
pre-commit run --all-files
```
