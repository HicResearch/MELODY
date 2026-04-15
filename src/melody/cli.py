import typer

from .melody import melody
from .run import run
from .list import list
from .log import log
from .pull import pull
from .stop import stop

app = typer.Typer()
app.command()(run)
app.command()(list)
app.command()(log)
app.command()(pull)
app.command()(stop)


if __name__ == "__main__":
    app()