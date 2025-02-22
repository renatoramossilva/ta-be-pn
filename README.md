# Mobile Network Coverage API

## Table of Contents

- [Requirements](#requirements)
- [Dependency Management with Poetry](#dependency-management-with-poetry)
- [Code Quality](#code-quality)
- [Unit tests](#unit-tests)


## Requirements

Before you begin, ensure you have the following prerequisites installed on your machine:

- [Python 3.9](https://www.python.org/downloads/) or higher
- [Poetry](https://python-poetry.org/docs/#installation)


## Dependency Management with Poetry

This project uses [Poetry](https://python-poetry.org/) for dependency management. Poetry simplifies the process of managing dependencies and packaging Python projects.

Once installed, you can easily manage dependencies by running `poetry add <dependency>` to add the new dependency and running `poetry install --no-root`, to install all the required packages listed in the [`pyproject.toml`](pyproject.toml)
 file.


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