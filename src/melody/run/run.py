from typing import Annotated, Any, Literal
import subprocess
import typer
from ..helpers import melodyLogging

def run(app: Annotated[
        str,
        typer.Argument(
            help="Path of the Flower App to run, or a remote app spec "
            "like '@account_name/app_name'."
        ),
    ] = "."):
    melodyLogging.log(["flwr", "run",app,"--stream"])
    with subprocess.Popen(["flwr", "run",app,"--stream"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as process:
        for line in process.stdout:
            print(line.decode('utf8'))

