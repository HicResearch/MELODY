import sys
from pathlib import Path


def check_flwrcrate_usage(app_path: Path) -> None:
    """Abort if no Python file in the app uses FLCrateTracker from flwrcrate."""
    py_files = list(app_path.rglob("*.py"))
    for py_file in py_files:
        try:
            source = py_file.read_text(encoding="utf-8")
        except OSError:
            continue
        if "FLCrateTracker" in source:
            return

    print(
        "mldy: this app does not use FLCrateTracker from flwrcrate.\n"
        "\n"
        "All runs must capture provenance via flwrCrate. To fix this, update\n"
        "your server_app.py:\n"
        "\n"
        "  1. Add flwrcrate to your app's dependencies:\n"
        "       pip install flwrcrate\n"
        "\n"
        "  2. Wrap your strategy in server_app.py:\n"
        "       from flwrcrate import FLCrateTracker\n"
        "       strategy = FLCrateTracker(context, your_strategy, ...)\n"
        "\n"
        "See https://github.com/eScienceLab/flwrCrate for full integration details.",
        file=sys.stderr,
    )
    sys.exit(1)
