import sys
from pathlib import Path

if sys.version_info >= (3, 11):
    import tomllib
else:
    try:
        import tomllib
    except ImportError:
        import tomli as tomllib  # type: ignore[no-redef]

DEFAULT_CONFIG_FILENAME = "mldy.toml"


def find_and_strip_config_arg(args: list[str]) -> tuple[Path | None, list[str]]:
    """Strip --config/-c <path> from leading flags only (before the subcommand).

    Stops scanning at the first positional argument so that flags belonging to
    flwr subcommands (e.g. `flwr run -c run-config.toml`) are never consumed.
    """
    leading: list[str] = []
    config_path: Path | None = None
    i = 0
    while i < len(args):
        arg = args[i]
        if arg in ("--config", "-c") and i + 1 < len(args):
            config_path = Path(args[i + 1])
            i += 2
        elif arg.startswith("-"):
            leading.append(arg)
            i += 1
        else:
            # First positional (the subcommand) — stop scanning
            remaining = leading + args[i:]
            break
    else:
        remaining = leading

    if config_path is None:
        default = Path(DEFAULT_CONFIG_FILENAME)
        if default.exists():
            config_path = default

    return config_path, remaining


def load_config(path: Path) -> dict:
    with open(path, "rb") as fh:
        return tomllib.load(fh)
