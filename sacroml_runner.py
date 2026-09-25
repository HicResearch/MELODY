import subprocess
import sys


def run_attacks(args: list[str], config: dict) -> int:
    """Run `sacroml run <target_dir> <attack_config>`, filling defaults from config."""
    sacroml_cfg = config.get("sacroml", {})

    positionals = [a for a in args if not a.startswith("-")]
    flags = [a for a in args if a.startswith("-")]

    target_dir = positionals[0] if len(positionals) > 0 else sacroml_cfg.get("target_dir")
    attack_config = positionals[1] if len(positionals) > 1 else sacroml_cfg.get("attack_config")

    if not target_dir:
        print(
            "melody attack: target directory required — pass as an argument or set "
            "sacroml.target_dir in melody.toml",
            file=sys.stderr,
        )
        return 1
    if not attack_config:
        print(
            "melody attack: attack config required — pass as an argument or set "
            "sacroml.attack_config in melody.toml",
            file=sys.stderr,
        )
        return 1

    result = subprocess.run(["sacroml", "run", str(target_dir), str(attack_config)] + flags)
    return result.returncode


def gen_target() -> int:
    return subprocess.run(["sacroml", "gen-target"]).returncode


def gen_attack() -> int:
    return subprocess.run(["sacroml", "gen-attack"]).returncode
