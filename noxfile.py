from __future__ import annotations

import os
import pathlib
import shutil

import nox

PROJECT = "standard_names"
ROOT = pathlib.Path(__file__).parent
PYTHON_VERSION = "3.12"


@nox.session
def test(session: nox.Session) -> None:
    """Run the tests."""
    session.install(".[peg,testing]")

    args = ["--cov", PROJECT, "-vvv"] + session.posargs

    if "CI" in os.environ:
        args.append(f"--cov-report=xml:{ROOT.absolute()!s}/coverage.xml")
    session.run("pytest", *args)

    if "CI" not in os.environ:
        session.run("coverage", "report", "--ignore-errors", "--show-missing")


@nox.session(name="test-cli")
def test_cli(session: nox.Session) -> None:
    """Test the cli."""
    session.install(".[peg]")

    session.run("standard-names", "--help")
    session.run("standard-names", "--version")
    for cmd in ("build", "dump", "scrape", "sql", "validate"):
        session.run("standard-names", cmd, "--help")
        session.run("standard-names", cmd)


@nox.session
def lint(session: nox.Session) -> None:
    """Look for lint."""
    session.install("pre-commit")
    session.run("pre-commit", "run", "--all-files")


@nox.session
def build(session: nox.Session) -> None:
    session.install("pip")
    session.install("build")
    session.run("python", "--version")
    session.run("pip", "--version")
    session.run("python", "-m", "build", "--outdir", "./build/wheelhouse")


@nox.session(name="build-docs")
def build_docs(session: nox.Session) -> None:
    """Build the docs."""

    session.install(
        *("-r", "requirements-docs.in"),
        *("-r", "requirements.in"),
    )
    session.install(".")

    pathlib.Path("build").mkdir(exist_ok=True)

    session.run(
        "sphinx-build",
        "-b",
        "html",
        "-W",
        "--keep-going",
        "docs",
        "build/html",
    )
    session.log("generated docs at build/html")


@nox.session(name="publish-testpypi")
def publish_testpypi(session):
    """Publish wheelhouse/* to TestPyPI."""
    session.run("twine", "check", "build/wheelhouse/*")
    session.run(
        "twine",
        "upload",
        "--skip-existing",
        "--repository-url",
        "https://test.pypi.org/legacy/",
        "build/wheelhouse/*.tar.gz",
    )


@nox.session(name="publish-pypi")
def publish_pypi(session):
    """Publish wheelhouse/* to PyPI."""
    session.run("twine", "check", "build/wheelhouse/*")
    session.run(
        "twine",
        "upload",
        "--skip-existing",
        "build/wheelhouse/*.tar.gz",
    )


@nox.session(python=False)
def clean(session):
    """Remove all .venv's, build files and caches in the directory."""
    folders = (
        (ROOT,) if not session.posargs else (pathlib.Path(f) for f in session.posargs)
    )

    for folder in folders:
        if not str(folder.resolve()).startswith(str(ROOT.resolve())):
            session.log(f"skipping {folder}: folder is outside of repository")
            continue

        with session.chdir(folder):
            session.log(f"cleaning {folder}")

            shutil.rmtree("build", ignore_errors=True)
            shutil.rmtree("dist", ignore_errors=True)
            shutil.rmtree(f"src/{PROJECT}.egg-info", ignore_errors=True)
            shutil.rmtree(".pytest_cache", ignore_errors=True)
            shutil.rmtree(".venv", ignore_errors=True)

            for d in ("src", "tests"):
                with session.chdir(d):
                    for pattern in ["*.py[co]", "__pycache__", "*.c", "*.so"]:
                        _clean_rglob(pattern)


def _clean_rglob(pattern):
    nox_dir = pathlib.Path(".nox")

    for p in pathlib.Path(".").rglob(pattern):
        if nox_dir in p.parents:
            continue
        if p.is_dir():
            p.rmdir()
        else:
            p.unlink()
