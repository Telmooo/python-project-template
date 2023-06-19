# Python Project Template with Cookiecutter

This project template contains the essentials for a well structured Python project using
Poetry as a dependency manager. Every project requires a lot of repeated actions for the
setup, this template wraps all those actions in a simple and automatic process so you
can get started as fast as possible.

Once generated, this template contains the following features:

-   Good base folder structure for a general Python project;
-   Uses `poetry` for management of dependencies and virtual environments;
-   A testing setup with `pytest`;
-   Type checking with `mypy`;
-   Code style enforcing with `flake8`;
-   Pre-configured code formatters (`prettier` and `black`);
-   Pre-configured `pre-commit` for employing standard practices on each commit;
-   Optional `click` CLI dependency;

## How to use this template

This section will guide you through the process of generating a new project using this
template.

### Requirements

-   Python 3.11
-   [Poetry](https://python-poetry.org/docs/#installation)
-   [Cookiecutter](https://cookiecutter.readthedocs.io/en/2.1.1/installation.html#)

### Generating a new project

To generate a new project, run the following command:

```bash
cookiecutter https://github.com/Telmooo/python-project-template.git
```

or, if you want a local copy of the template:

```bash
git clone https://github.com/Telmooo/python-project-template.git
cookiecutter python-project-template
```

If target project already exists, add `-f` to the command above.

You will be prompted to enter some information about your project, such as the project
name, package name, author name, etc. Default options are shown in squared brackets; to
use them, leave the response in blank. After that, the project will be generated in the
current directory.

To verify that everything is working, run the following commands:

```bash
cd <project_name>
git show-ref --verify refs/heads/main
git show-ref --verify refs/heads/dev

poetry install
```

None of these commands should return an error.

To setup a remote repository, if not existing, run the following commands:

```bash
cd <project_name>
git remote add origin https://github.com/OWNER/REPOSITORY.git
git push --all
```

## Project Options

Template options are listed below.

| **Option**               | **Default**                       | **Description**                                                                                                                                                  |
| :----------------------- | :-------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `project_name`           | `project-name`                    | The name of the project.                                                                                                                                         |
| `package_name`           | based on `project_name`           | Package name. Must be compliant with specification.                                                                                                              |
| `author`                 | `Project author name`             | Author name.                                                                                                                                                     |
| `email`                  | `Project author email`            | Author email.                                                                                                                                                    |
| `github_username`        | `Project author GitHub username`  | Author GitHub username. Used for directing homepage and repository on package configuration. Assumes `project_name` as the repository name, change if necessary. |
| `description`            | `A short description. No quotes.` | A short description of the project.                                                                                                                              |
| `version`                | `0.1.0`                           | Initial version of the project.                                                                                                                                  |
| `command_line_interface` | `click`                           | If `click` is chosen, the project will add [Click](https://click.palletsprojects.com/en/8.1.x/) dependency for creating CLI.                                     |

## Project Structure

The directory structure of the generated project is shown below.

```
example-project                 # Project root (chosen project name)
│   .flake8                     # Flake8 configuration
│   .gitignore
│   .pre-commit-config.yaml     # Pre-commit configuration
│   .prettierrc.yaml            # Prettier configuration
│   AUTHORS.md
│   CHANGELOG.md
│   CONTRIBUTING.md
│   LICENSE
│   mypy.ini
│   poetry.toml                 # Poetry configuration
│   pyproject.toml              # Package configuration
│   README.md                   # Project top-level README for developers and users using this project
│   VERSION                     # Project version
│
├───src
│   └───example_project         # Package root containing source code (chosen package name)
│           py.typed            # Marker file for PEP 561
│           __init__.py         # Makes package a Python module
│
└───tests                       # Directory containing tests
        conftest.py             # Pytest configuration
```
