from typing import Annotated, Any, Literal
import subprocess
import typer
from ..helpers import melodyLogging

def pull(run_id: Annotated[
        int,
        typer.Argument(
            help="run ID to Query"
        ),
    ] = "."):
    melodyLogging.log(["flwr", "pull", run_id])
    with subprocess.Popen(["flwr", "pull", run_id], stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT) as process:
        for line in process.stdout:
            print(line.decode('utf8'))