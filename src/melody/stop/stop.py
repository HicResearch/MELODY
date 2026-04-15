from typing import Annotated, Any, Literal
import subprocess
import typer


def stop(run_id: Annotated[
        int,
        typer.Argument(
            help="run ID to Query"
        ),
    ] = "."):
    with subprocess.Popen(["flwr", "stop", run_id], stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT) as process:
        for line in process.stdout:
            print(line.decode('utf8'))