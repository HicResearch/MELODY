import subprocess
import sys

from melody_wrapper.checks import check_flwrcrate_usage
from melody_wrapper.config import find_and_strip_config_arg, load_config
from melody_wrapper.git_snapshot import snapshot, resolve_app_path
from melody_wrapper.sacroml_runner import gen_attack, gen_target, run_attacks

_melody_SUBCOMMANDS = {"attack", "gen-target", "gen-attack"}


def main() -> None:
    config_path, args = find_and_strip_config_arg(sys.argv[1:])

    config: dict = {}
    if config_path is not None:
        if not config_path.exists():
            print(f"melody: config file not found: {config_path}", file=sys.stderr)
            sys.exit(1)
        config = load_config(config_path)

    subcommand = args[0] if args else None

    if subcommand == "run":
        app_path = resolve_app_path(args).resolve()
        check_flwrcrate_usage(app_path)
        snapshot(args, config)
        result = subprocess.run(["flwr"] + args)
        sys.exit(result.returncode)

    if subcommand == "attack":
        sys.exit(run_attacks(args[1:], config))

    if subcommand == "gen-target":
        sys.exit(gen_target())

    if subcommand == "gen-attack":
        sys.exit(gen_attack())

    # Everything else passes through to flwr unchanged
    result = subprocess.run(["flwr"] + args)
    sys.exit(result.returncode)
