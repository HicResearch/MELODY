"""Server app skeleton.


The three flwrCrate touchpoints are marked # [flwrCrate 1/3], # [flwrCrate 2/3],
and # [flwrCrate 3/3]. Everything else is standard Flower server code.

melody enforces that FLCrateTracker is present before it will run your app.
"""

from pathlib import Path

import numpy as np
from flwr.app import ArrayRecord, ConfigRecord, Context
from flwr.serverapp import Grid, ServerApp
from flwr.serverapp.strategy import FedAvg
from flwrcrate import FLCrateTracker  # [flwrCrate 1/3] import

# Absolute path to this app's root directory.
# flwr installs apps to a temporary ~/.flwr/apps/<hash>/ directory at runtime,
# so all paths passed to FLCrateTracker must be absolute.
_APP_DIR = Path(__file__).parent.parent.resolve()

app = ServerApp()


@app.main()
def main(grid: Grid, context: Context) -> None:
    num_rounds: int = context.run_config["num-server-rounds"]

    # ------------------------------------------------------------------
    # TODO: replace with your model's actual initial parameters.
    # ArrayRecord maps layer names to numpy arrays. The example below uses
    # a single array of zeros with 10 elements.
    # ------------------------------------------------------------------
    initial_weights = np.zeros(10, dtype=np.float32)
    arrays = ArrayRecord({"weights": initial_weights})

    strategy = FedAvg()

    # [flwrCrate 2/3] Wrap strategy.start() in the FLCrateTracker context
    # manager. The crate is written to output_dir/ro-crate/ on clean exit,
    # and a FailedActionStatus crate is written on error.
    with FLCrateTracker(
        context,
        strategy,
        output_dir=str(_APP_DIR / "fl_crate_out"),
        pyproject_path=str(_APP_DIR / "pyproject.toml"),
        app_name="example-app",
        # Uncomment and fill in to record authorship in the RO-Crate:
        # author={"name": "Your Name", "orcid": "https://orcid.org/0000-0000-0000-0000"},
        # license="https://spdx.org/licenses/MIT.html",
    ) as tracker:
        result = strategy.start(
            grid=grid,
            initial_arrays=arrays,
            train_config=ConfigRecord({}),
            num_rounds=num_rounds,
            # Pass tracker.wrap_evaluate(your_eval_fn) if you have a
            # server-side evaluation function; otherwise leave as None.
            evaluate_fn=None,
        )

        # ------------------------------------------------------------------
        # TODO: save your model here, then pass the path to record_result.
        # Example for a numpy model:
        #   model_path = str(_APP_DIR / "final_model.npy")
        #   np.save(model_path, result.arrays["weights"])
        #   tracker.record_result(result, model_path=model_path)
        # ------------------------------------------------------------------
        tracker.record_result(result)  # [flwrCrate 3/3]
