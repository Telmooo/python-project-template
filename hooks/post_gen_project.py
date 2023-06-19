from pathlib import Path
from subprocess import DEVNULL, STDOUT, call


def is_git_repo(path: Path) -> bool:
    return call(["git", "-C", str(path), "status"], stdout=DEVNULL, stderr=STDOUT) == 0


def branch_exists(path: Path, branch: str) -> bool:
    return (
        call(
            ["git", "-C", str(path), "show-ref", "--verify", f"refs/heads/{branch}"],
            stdout=DEVNULL,
            stderr=STDOUT,
        )
        == 0
    )


def initialize_git_repo(path: Path) -> None:
    # Verify that the path is a git repo.
    if not is_git_repo(path):
        call(["git", "init", "--quiet", str(path)])

    # Verify that the main branch exists.
    if not branch_exists(path, "main"):
        call(["git", "-C", str(path), "checkout", "--quiet", "--orphan", "main"])
        call(
            [
                "git",
                "-C",
                str(path),
                "-c",
                "user.name={{ cookiecutter.author }}",
                "-c",
                "user.email={{ cookiecutter.email }}",
                "commit",
                "--quiet",
                "--allow-empty",
                "-m",
                "Create main.",
            ]
        )

    # Verify that the dev branch exists.
    if not branch_exists(path, "dev"):
        call(["git", "-C", str(path), "checkout", "--quiet", "-b", "dev"])
    else:
        call(["git", "-C", str(path), "checkout", "--quiet", "dev"])

    # Add setup to dev branch.
    call(["git", "-C", str(path), "add", "."])
    call(
        [
            "git",
            "-C",
            str(path),
            "-c",
            "user.name={{ cookiecutter.author }}",
            "-c",
            "user.email={{ cookiecutter.email }}",
            "commit",
            "--quiet",
            "-m",
            "Initial commit.",
        ]
    )


def main() -> None:
    output_dir = r"{{ cookiecutter._output_dir }}"
    project_path: Path = Path(output_dir) / "{{ cookiecutter.project_name }}"

    initialize_git_repo(project_path)


if __name__ == "__main__":
    main()
