import typer
import sys
import logging

from .melody import melody
from .run import run
from .list import list
from .log import log
from .pull import pull
from .stop import stop
from .config import configSetup
from .helpers import melodyLogging

configSetup.setup()#TODO want to user override location if exists


melodyLogging.setupLogger()#TODO pass in logging level?


l = logging.getLogger("MELODY")
app = typer.Typer()
app.command(help="Run a Flower App")(run)
app.command(help="List the details of one provided run ID or all runs")(list)
app.command(help="Get logs from a run")(log)
app.command(help="Pull artifacts from a run")(pull)
app.command(help="Stop a run")(stop)


if __name__ == "__main__":
    app()