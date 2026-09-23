"""Client app skeleton.

Each federated client runs client_fn() to create a Client instance.
Replace the no-op implementations with your actual training and evaluation logic.
"""


import numpy as np
from flwr.client import ClientApp, NumPyClient
from flwr.common import Context, NDArrays


class ExampleClient(NumPyClient):

    def get_parameters(self, config) -> NDArrays:
        # TODO: return your model's current weights as a list of numpy arrays.
        return [np.zeros(10, dtype=np.float32)]

    def fit(self, parameters: NDArrays, config) -> tuple[NDArrays, int, dict]:
        # TODO: load your local data, train your model for one round, and
        # return (updated_parameters, num_training_examples, metrics_dict).
        updated_parameters = parameters  # no-op: return received weights unchanged
        num_examples = 0
        metrics: dict = {}
        return updated_parameters, num_examples, metrics

    def evaluate(self, parameters: NDArrays, config) -> tuple[float, int, dict]:
        # TODO: evaluate the received parameters on your local test data and
        # return (loss, num_test_examples, metrics_dict).
        loss = 0.0
        num_examples = 0
        metrics: dict = {"accuracy": 0.0}
        return loss, num_examples, metrics


def client_fn(context: Context) -> ExampleClient:
    # TODO: use context.node_config or context.run_config to select which
    # partition of the data this client should use, e.g.:
    #   partition_id = context.node_config["partition-id"]
    return ExampleClient().to_client()


app = ClientApp(client_fn=client_fn)
