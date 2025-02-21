# Mobile Network Coverage API

## Table of Contents

- [Dependency Management with Poetry](#dependency-management-with-poetry)
- [Code Quality](#code-quality)


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
