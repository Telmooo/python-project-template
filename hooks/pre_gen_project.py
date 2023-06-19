import re

REGEX_PROJECT_NAME = r"^[a-z][-a-z0-9]+$"
REGEX_PACKAGE_NAME = r"^[a-z][_a-z0-9]+$"

REGEX_EMAIL = r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"


def validate_project_name(project_name: str) -> None:
    assert bool(
        re.fullmatch(REGEX_PROJECT_NAME, project_name)
    ), f"Invalid project name: {project_name}"


def validate_package_name(package_name: str) -> None:
    assert bool(
        re.fullmatch(REGEX_PACKAGE_NAME, package_name)
    ), f"Invalid package name: {package_name}"


def validate_email(email: str) -> None:
    assert bool(re.fullmatch(REGEX_EMAIL, email)), f"Invalid email: {email}"


def main() -> None:
    validate_project_name("{{ cookiecutter.project_name }}")
    validate_package_name("{{ cookiecutter.package_name }}")
    validate_email("{{ cookiecutter.email }}")


if __name__ == "__main__":
    main()
