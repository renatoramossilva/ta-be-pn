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

Clone this repository to your local machine and navigate to the project directory:

```bash
git clone https://github.com/renatoramossilva/ta-be-pn
cd ta-be-pn
```

There are two ways to set up the project:

  - Localhost
  - Docker container

### Running on the localhost

Initialize the application using `uvicorn` command:

```bash
> poetry run uvicorn app.main:app --reload
```

### Running on Docker container

Initialize the application using `docker` commands:

```bash
> docker build -t ta-be-pn-image -f docker/Dockerfile .
> docker run -d -p 8000:8000 ta-be-pn-image
```
- `-p 8000:8000`: This maps port 8000  (The FastAPI application runs on this port) inside the container to port 8000 on your local machine. You can access the app locally at http://localhost:5001.
- `--rm`: Automatically removes the container when it is stopped.
- `-d`: Runs the container in detached mode (in the background).

To validate the endpoint, independently the way that the API was started, you can use the following `curl` command:

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