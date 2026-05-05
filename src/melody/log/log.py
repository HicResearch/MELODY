from typing import Annotated, Any, Literal
import subprocess
import typer
from ..helpers import melodyLogging


def log(run_id: Annotated[
        int,
        typer.Argument(
            help="run ID to Query"
        ),
    ] = "."):
    melodyLogging.log(["flwr", "log", run_id])
    with subprocess.Popen(["flwr", "log", run_id], stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT) as process:
        for line in process.stdout:
            print(line.decode('utf8'))
