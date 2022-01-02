import tempfile

import nox


def install_with_constraints(session, *args, **kwargs):
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--without-hashes",
            "--format=requirements.txt",
            f"--output={requirements.name}",
            external=True,
        )
        session.install(f"--constraint={requirements.name}", *args, **kwargs)


@nox.session
def typing(session):
    install_with_constraints(session, "mypy")
    session.run("mypy", ".")


@nox.session(python=["3.9"])
def testing(session):
    install_with_constraints(session, "pytest", "pytest-cov", "coverage[toml]", "loguru")
    session.run("coverage", "run", "-m", "pytest")
    session.run("coverage", "report")


@nox.session
def linting(session):
    install_with_constraints(session, "flake8")
    session.run("flake8", ".")


@nox.session
def black(session):
    install_with_constraints(session, "black")
    session.run("black", "--check", ".")
