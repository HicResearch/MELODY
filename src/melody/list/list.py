from typing import Annotated, Any, Literal
import subprocess
import typer

def list(
        run_id: Annotated[
            int | None,
            typer.Option(
                "--run-id",
                help="Specific run ID to display",
            ),
        ] = None,
        limit: Annotated[
            int | None,
            typer.Option(
                "--limit",
                help="Maximum number of runs to display",
                min=1,
            ),
        ] = None,
        output_format: Annotated[
            Literal["default", "json"],
            typer.Option(
                "--format",
                case_sensitive=False,
                help="Format output using 'default' view or 'json'",
            ),
        ] = "default",
):
    args = ["flwr","list"]
    if run_id is not None:
        args.append("--run-id")
        args.append(run_id)
    if limit is not None:
        args.append("--limit")
        args.append(limit)
    if output_format is not "default":
        args.append("--format")
        args.append(output_format)
    with subprocess.Popen(args, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT) as process:
        for line in process.stdout:
            print(line.decode('utf8'))