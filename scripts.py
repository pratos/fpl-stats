import os
import subprocess
import sys
from pathlib import Path
from subprocess import CalledProcessError, check_call

import click
from loguru import logger

from run import run_fbref

THIS_DIRECTORY = Path(__file__).parent

files = ["tests/", "src/", "scripts.py"]


def _call(cmd, options=[]) -> None:
    command = cmd.split(" ") + options
    logger.info(">>>>>>>>     {}".format(" ".join(command)))
    try:
        check_call(command)
    except CalledProcessError as ex:
        print(f"[FAIL]  {ex}")
        logger.info("<<<<<<<<<< ")
        sys.exit(2)
    logger.info("<<<<<<<<<< ")


def lint() -> None:
    _call("black --check --diff --color", files)


def test() -> None:
    _call("pytest --disable-pytest-warnings -v -s")


@click.command()
def st_server():
    logger.info("Starting server...")
    subprocess.run(
        [
            "poetry",
            "run",
            "streamlit",
            "run",
            str(THIS_DIRECTORY / "src/app/home.py"),
        ],
        check=True,
        universal_newlines=True,
    )


@click.command()
def migrations():
    logger.info("Running migrations...")
    os.chdir(THIS_DIRECTORY / "db")
    subprocess.run(
        ["poetry", "run", "alembic", "upgrade", "head"],
        check=True,
        universal_newlines=True,
    )

    logger.info("Completed successfully")


@click.command()
@click.argument("debug", envvar="DEBUG", type=bool)
def fbref_scraper(debug: bool):
    logger.info("Starting scraping for Fbref...")
    run_fbref(debug=debug)


@click.command()
def test_script():
    subprocess.run(["echo", "Subprocess works --->"])
