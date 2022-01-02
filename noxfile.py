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


@nox.session(python=["3.9"])
def tests(session):
    session.install("poetry")
    session.run("poetry", "install")
    session.run("coverage", "run", "-m", "pytest")
    session.run("coverage", "report")


@nox.session
def lint(session):
    install_with_constraints(session, "flake8")
    session.run("flake8", ".")


@nox.session
def black(session):
    install_with_constraints(session, "black")
    session.run("black", "--check", ".")


# @nox.session
# def lint(session):
#     args = session.posargs or locations
#     session.install("poetry")
#     session.run("poetry", "install")
#     session.run("black", "--check", ".")
#     session.run("flake8", *args)


# @nox.session
# def typing(session):
#     session.install("poetry")
#     session.run("poetry", "install")
#     session.run("mypy", ".")
