import os
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path
from subprocess import call, check_call
from typing import Dict

from pytest_cookies.plugin import Cookies

REQUIRED_DIR = [
    "src",
    "tests",
]

REQUIRED_FILE = [
    ".flake8",
    ".gitignore",
    ".pre-commit-config.yaml",
    ".prettierrc.yaml",
    "AUTHORS.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "LICENSE",
    "README.md",
    "VERSION",
    "poetry.toml",
    "pyproject.toml",
]


@contextmanager
def chdir(path: Path) -> Generator[None, None, None]:
    """Change directory to `path` and return to previous on exit.

    Args:
        path (Path): Path to change directory to.
    """
    cwd = Path.cwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(cwd)


@contextmanager
def checkout(path: Path, branch: str) -> Generator[None, None, None]:
    """Checkout `branch` in `path` and return to previous on exit.

    Args:
        path (Path): Path to checkout branch in.
        branch (str): Branch to checkout.
    """
    with chdir(path):
        try:
            call(["git", "checkout", "--quiet", branch])
            yield
        finally:
            call(["git", "checkout", "--quiet", "-"])


def verify_git_repo(path: Path) -> None:
    assert (path / ".git").is_dir()

    assert (
        check_call(["git", "-C", str(path), "show-ref", "--verify", "refs/heads/main"])
        == 0
    )

    assert (
        check_call(["git", "-C", str(path), "show-ref", "--verify", "refs/heads/dev"])
        == 0
    )


def verify_file_structure(path: Path, context: Dict[str, str]) -> None:
    top_level_entries = [entry for entry in path.iterdir()]
    top_level_entries_name = [entry.name for entry in top_level_entries]

    for required_entry in REQUIRED_DIR:
        assert required_entry in top_level_entries_name
        assert (path / required_entry).is_dir()

    for required_entry in REQUIRED_FILE:
        assert required_entry in top_level_entries_name
        assert (path / required_entry).is_file()

    src_dir = path / "src"
    assert src_dir.is_dir()

    package_name = context.get(
        "package_name", context["project_name"].replace(" ", "_").replace("-", "_")
    )
    package_dir = src_dir / package_name
    assert package_dir.is_dir()
    assert (package_dir / "__init__.py").is_file()
    assert (package_dir / "py.typed").is_file()

    tests_dir = path / "tests"
    assert tests_dir.is_dir()


def verify_file_integrity(path: Path, context: Dict[str, str]) -> None:
    pass

    authors_content = (path / "AUTHORS.md").read_text()
    assert context.get("author", "Project author name") in authors_content
    assert context.get("email", "Project author email") in authors_content

    readme_content = (path / "README.md").read_text()
    assert (
        context.get(
            "package_name", context["project_name"].replace(" ", "_").replace("-", "_")
        )
        in readme_content
    )
    assert (
        context.get("description", "A short description. No quotes.") in readme_content
    )

    version_content = (path / "VERSION").read_text()
    assert context.get("version", "0.0.1") in version_content

    pyproject_content = (path / "pyproject.toml").read_text()
    assert context["project_name"] in pyproject_content
    assert (
        context.get("description", "A short description. No quotes.")
        in pyproject_content
    )
    assert context.get("author", "Project author name") in pyproject_content
    assert context.get("email", "Project author email") in pyproject_content
    assert (
        context.get("github_username", "Project author GitHub username")
        in pyproject_content
    )
    assert (
        context.get(
            "package_name", context["project_name"].replace(" ", "_").replace("-", "_")
        )
        in pyproject_content
    )
    assert context.get("version", "0.0.1") in pyproject_content

    if context.get("command_line_interface", "click") == "click":
        assert "click" in pyproject_content
    else:
        assert "click" not in pyproject_content


def verify_template(path: Path, context: Dict[str, str]) -> None:
    verify_git_repo(path)

    with checkout(path, "dev"):
        verify_file_structure(path, context)
        verify_file_integrity(path, context)

        assert check_call(["poetry", "install", "-q"]) == 0


def test_python_project_template_create(cookies: Cookies) -> None:
    context = {
        "project_name": "test-project",
        "author": "johndoe",
        "email": "johndoe@testemail.com",
        "github_username": "johndoe",
        "description": "A test project.",
    }

    results = cookies.bake(extra_context=context)

    assert results.exit_code == 0
    assert results.exception is None
    assert results.project_path.is_dir()
    assert results.project_path.name == "test-project"

    verify_template(results.project_path, context)


def test_python_project_template_no_cli(cookies: Cookies) -> None:
    context = {
        "project_name": "test-project",
        "author": "johndoe",
        "email": "johndoe@testemail.com",
        "github_username": "johndoe",
        "description": "A test project.",
        "command_line_interface": "none",
    }

    results = cookies.bake(extra_context=context)

    assert results.exit_code == 0
    assert results.exception is None
    assert results.project_path.is_dir()
    assert results.project_path.name == "test-project"

    verify_template(results.project_path, context)
