# Mobile Network Coverage API

## Table of Contents

- [Requirements](#requirements)
- [Project Structure](#project-structure)
- [Dependency Management with Poetry](#dependency-management-with-poetry)
- [Project setup](#project-setup)
- [API Documentation](#api-documentation)
- [Code Quality](#code-quality)
- [Unit tests](#unit-tests)
- [Continuous Integration](#continuous-integration)


## Requirements

Before you begin, ensure you have the following prerequisites installed on your machine:

- [Python 3.10](https://www.python.org/downloads/) or higher
- [Poetry](https://python-poetry.org/docs/#installation)


## Project Structure

The project is organized following this structure:

```bash
├── app
│   ├── db
│   │   ├── 2018_01_Sites_mobiles_2G_3G_4G_France_metropolitaine_L93.csv
│   │   └── data.py
│   ├── __init__.py
│   ├── main.py
│   ├── routes.py
│   └── utils.py
├── poetry.lock
├── pyproject.toml
├── pytest.ini
├── README.md
└── tests
    └── app
        ├── db
        │   └── test_data.py
        └── test_utils.py
```

## Dependency Management with Poetry

This project uses [Poetry](https://python-poetry.org/) for dependency management. Poetry simplifies the process of managing dependencies and packaging Python projects.

Once installed, you can easily manage dependencies by running `poetry add <dependency>` to add the new dependency and running `poetry install --no-root`, to install all the required packages listed in the [`pyproject.toml`](pyproject.toml)
 file.


## Project Setup

There are two ways to set up the project:

  - Localhost
  - Docker container

### Running on the localhost

Initialize the application using `uvicorn` command:

```bash
> poetry run uvicorn app.main:app --reload

INFO:     Will watch for changes in these directories: ['~/ta-be-pn']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [8448] using StatReload
INFO:     Started server process [8459]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Running on Docker container

Initialize the application using `docker` commands:

```bash
> docker build -t ta-be-pn-image -f docker/Dockerfile .
[+] Building 2.9s (10/10) FINISHED                                                                                                       docker:default
 => [internal] load build definition from Dockerfile                                                                                               0.3s
 => => transferring dockerfile: 374B                                                                                                               0.0s
 => [internal] load metadata for docker.io/library/python:3.10-slim                                                                                0.6s
 => [internal] load .dockerignore                                                                                                                  0.3s
 => => transferring context: 2B                                                                                                                    0.0s
 => [1/5] FROM docker.io/library/python:3.10-slim@sha256:66aad90b231f011cb80e1966e03526a7175f0586724981969b23903abac19081                          0.0s
 => [internal] load build context                                                                                                                  0.4s
 => => transferring context: 123.90kB                                                                                                              0.1s
 => CACHED [2/5] WORKDIR /app                                                                                                                      0.0s
 => CACHED [3/5] COPY pyproject.toml poetry.lock* ./                                                                                               0.0s
 => CACHED [4/5] RUN pip install --no-cache-dir poetry &&     poetry install --no-root                                                             0.0s
 => CACHED [5/5] COPY . .                                                                                                                          0.0s
 => exporting to image                                                                                                                             0.2s
 => => exporting layers                                                                                                                            0.0s
 => => writing image sha256:7aee6f6ef83098d384d9278d304dfeeed30ac7ce986e3bddc3c82c1be7b1d825                                                       0.0s
 => => naming to docker.io/library/ta-be-pn-image                                                                                                  0.1s

> docker images
REPOSITORY       TAG       IMAGE ID       CREATED          SIZE
ta-be-pn-image   latest    7aee6f6ef830   48 seconds ago   569MB

> docker run -d -p 8000:8000 ta-be-pn-image

2cf614bc88d623a83284c91e188257c14a0d6157c55381ef5c22e59ed17ddd72

> docker ps
CONTAINER ID   IMAGE            COMMAND                  CREATED         STATUS         PORTS                                       NAMES
2cf614bc88d6   ta-be-pn-image   "uvicorn app.main:ap…"   6 seconds ago   Up 5 seconds   0.0.0.0:8000->8000/tcp, :::8000->8000/tcp   beautiful_spence
```

To validate the endpoint, Indepently the way that the API was started, you can use the following `curl` command:

```bash
> curl -s 'GET' 'http://127.0.0.1:8000/coverage?address=42+rue+papernest+75011+Paris' | jq .
{
  "Orange": {
    "2G": true,
    "3G": true,
    "4G": false
  },
  "SFR": {
    "2G": true,
    "3G": false,
    "4G": false
  }
}
```

## API Documentation

You can find the API documentation at the following link: [API Documentation](http://localhost:8000/docs)


## Code Quality

This project uses several tools to maintain code quality and enforce coding standards:

- **[black](https://black.readthedocs.io/)**: A code formatter that ensures consistent code style.
- **[pylint](https://pylint.pycqa.org/)**: A static code analysis tool to enforce coding standards and detect errors.
- **[isort](https://pycqa.github.io/isort/)**: A tool to sort and format imports automatically.
- **[mypy](http://mypy-lang.org/)**: A static type checker to ensure type safety in Python code.

These tools are integrated with [pre-commit](https://pre-commit.com/), ensuring that they are automatically run before each commit to maintain code quality.

To manually run these tools, you can use the following commands:

`pre-commit run --all-files` or `poetry run pre-commit run --all-files`


## Unit tests

This project uses `pytest` for unit testing to ensure the functionality of key features like car bookings and availability checks.

### Running Tests

To run the unit tests locally:

`poetry run pytest`


## Continous Integration

Whenever a pull request is opened, the GitHub Actions workflow will trigger and perform the following checks:

- Code Formatting: Run `black` and `isort` to format the code.
- Static Analysis: Execute `pylint` and `mypy` to ensure code quality.
- Unit Testing: Run `pytest` to execute the unit tests and check for coverage.

This setup ensures that only code that passes all checks is merged into the master branch, maintaining a high standard of code quality throughout the development process.