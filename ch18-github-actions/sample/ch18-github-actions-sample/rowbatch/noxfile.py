"""Run the test suite on every supported Python: `nox`, or `nox -p 3.12`."""

import nox

nox.options.default_venv_backend = "uv"


@nox.session(python=["3.12", "3.13", "3.14"])
def tests(session: nox.Session) -> None:
    session.run_install(
        "uv",
        "sync",
        "--locked",
        f"--python={session.virtualenv.location}",
        env={"UV_PROJECT_ENVIRONMENT": session.virtualenv.location},
    )
    session.run("pytest", *session.posargs)
