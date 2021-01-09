import os
import subprocess
from pathlib import Path

import click
from loguru import logger

from run import run_fbref

THIS_DIRECTORY = Path(__file__).parent


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
    logger.info("Completed succeessfully")


@click.command()
def fbref_scraper():
    logger.info("Starting scraping for Fbref...")
    run_fbref(debug=True)


@click.command()
def test_script():
    subprocess.run(["echo", "Subprocess works --->"])
