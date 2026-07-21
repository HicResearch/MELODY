from typing import Annotated, Any, Literal
import subprocess
import typer
from ..helpers import melodyLogging, melodySourceControl
from ..helpers.rocrates.rocrates import make_crate


def run(app: Annotated[
        str,
        typer.Argument(
            help="Path of the Flower App to run, or a remote app spec "
            "like '@account_name/app_name'."
        ),
    ] = "."):
    melodyLogging.log(["flwr", "run",app,"--stream"])
    melodySourceControl.commit(app)
    make_crate(app)
    melodyLogging.log(["flwr", "run","--stream"])
    with subprocess.Popen(["flwr", "run",app,"--stream"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as process:
        for line in process.stdout:
            print(line.decode('utf8'))

