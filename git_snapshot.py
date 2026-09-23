import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

_IGNORE = shutil.ignore_patterns(".git", "__pycache__", "*.pyc", ".venv", "venv")


def resolve_app_path(flwr_args: list[str]) -> Path:
    """Return the APP path from `flwr run [APP] ...`, defaulting to cwd."""
    # Skip "run" itself, then take the first non-flag positional as APP
    for arg in flwr_args[1:]:
        if not arg.startswith("-"):
            return Path(arg)
    return Path(".")


def snapshot(flwr_args: list[str], config: dict) -> None:
    """Copy the Flower app into the configured git directory and commit it."""
    git_dir = Path(config.get("git", {}).get("directory", ""))
    if not git_dir or not git_dir.exists():
        print(
            f"mldy: git.directory '{git_dir}' not found — set it in your mldy.toml",
            file=sys.stderr,
        )
        sys.exit(1)

    app_path = resolve_app_path(flwr_args).resolve()
    if not app_path.exists():
        print(f"mldy: app path not found: {app_path}", file=sys.stderr)
        sys.exit(1)

    dest = git_dir / app_path.name
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(app_path, dest, ignore=_IGNORE)

    subprocess.run(["git", "-C", str(git_dir), "add", "-A"], check=True)

    status = subprocess.run(
        ["git", "-C", str(git_dir), "status", "--porcelain"],
        capture_output=True,
        text=True,
        check=True,
    )
    if not status.stdout.strip():
        return  # nothing changed since last snapshot

    timestamp = datetime.now().isoformat(timespec="seconds")
    subprocess.run(
        [
            "git", "-C", str(git_dir),
            "commit", "-m", f"mldy snapshot {app_path.name}: {timestamp}",
        ],
        check=True,
    )
