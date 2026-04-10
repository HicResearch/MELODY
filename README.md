# MELODY : federated Machine Learning fOr dermatologY
![MELODy Logo](./assets/MELODY_LIGHT_WIDE.png)
MELODY is a project funded under the [DARE UK Real World Exemplar Programme](https://www.ukri.org/opportunity/dare-uk-real-world-research-exemplar-programme/). The aim of the project is to develop and test federated machine learning approaches for dermatology research using clinical images from NHS Tayside and Oxford University Hospitals. By training AI models across multiple TREs without centralising data, the project aims to support the development of more inclusive and representative dermatology AI systems.

# Preamble & Terminology
MELODY uses the [Flower Framework](https://flower.ai/docs/framework/main/en/index.html) to enable federated machine learning (FML). The Flower Framework providers **SuperLinks** and **SuperNodes** to facilitate FML.

A **SuperLink** acts as a central orchestrator and communication hub. It allows for new FML jobs to be sent to superNodes.

A **SuperNode** is a remote client in the FML workflow. a SuperNode receives requests from a SuperLink and sends back the local training and testing results.

```mermaid
flowchart TD
    A[Researcher] -->|1. Submits FML Job| B(SuperLink)
    B <-->|2. Federated Training|C(SuperLink 1)
    B <-->|2. Federated Training|D(SuperLink 2)
    B <-->|2. Federated Training|E(SuperLink 3)
    B --> |3. Returns Results|A
```

# Installation
## Prerequisites
Both the SuperLink and SuperNode require a Linux environment to run with Python3 and pip installed.

It is recommended to use a Python virtual environment when installing the required dependencies.

Both the SuperLink and SuperNode require the same dependencies, they can be installed the Flower package ``flwr``:
```
$ pip install flwr
```
# Deploy

## Deploy a SuperLink
Deploying a SuperLink can be as simple as
```
$ flower-superlink --insecure
```
This will launch a SuperLink and bind it to the default ports ``9091, 9092, 9093``.

While this is sufficient for testing, there are a number of configuration options to improve the auditability of the SuperLink:
```
--database DATABASE  A string representing the path to the database file that will be opened.

--storage-dir STORAGE_DIR The base directory to store the objects for the Flower File System.

--log-file LOG_FILE  Path to the SuperLink log file.
```
<!--May want to talk about certs & auth in the future -->
Using these options will allow for improved audition of the system (See [Auditing](#Auditing)).

The ports that your SuperLink binds to can also be set to suit your needs:
```
--serverappio-api-address SERVERAPPIO_API_ADDRESS This defaults to 0.0.0.0:9091

--fleet-api-address FLEET_API_ADDRESS This default to 0.0.0.0:9092

--control-api-address CONTROL_API_ADDRESS This defaults to 0.0.0.0:9093
```
## Deploy a SuperNode
Deploying a SuperNode is slightly more complicated than deploying a SuperLink.
The simplest deployment of a SuperNode is
```
$ flower-supernode \
--insecure \
--superlink 127.0.0.1:9092 \
--clientappio-api-address 127.0.0.1:9095
```

This deployment would expect an insecure SuperNode to be listening on 127.0.0.1:9092 and is configuring the SuperNode to bind to port 9095.

SuperNodes allow for localised configuration to be set when running a Supernode via the ``--node-config`` command line option. An example can be seen below:
```
--node-config partition-id=1 data-dir=/tmp/mydata/
```
This node config allows for instance specific values to be set that can then be referenced in the source code of the FML Job (See [Using Node Config](#NodeConfig)).


## Deploy Using Docker
An Example Docker Compose file is located in [docker/compose_example/compose.yml](./docker/compose_example/compose.yml)

# Running a Job
Flower Apps are used to enable FML.
We recommend following one of the [Flower quickstart tutorials](https://flower.ai/docs/framework/tutorial-quickstart.html) to give you an understanding of how Flower Apps work.

 A new app can be created by running the following command:
```
$ flwr new APP_SPEC
```
A list of all available Apps can be found at [https://flower.ai/apps/](https://flower.ai/apps/).
These can be used as a base to develop your FML Job.

## Connecting To a SuperLink
To connect to a specific SuperLink, you need to configure it in your local .flwr configuration.
This configuration is ususally found at ``~/.flwr/config.toml`` but can also be found by running the command ``flwr config ls``.

To add a new SuperLink at 1.1.1.1:9093 you would add the following to your .flwr config
```
[superlink.my_remote_deployment]
address = "1.1.1.1:9093"
insecure=true
```

This will now let you connect to the SuperLink by providing the friendly name `my_remote_deployment` when running a flower command, such as:
```
$flwr run my_job my_remote_deployment
```

## <a name="NodeConfig"></a>Using Node Configurations
Node configurations can be used to access SuperNode specific configurations, such as data locations.
They are accessed in your Flower App via ```context.node_config["some_key"]```

## Using App Configurations
App configurations are similar to Node Configurations, in that they can be used to make your app more generic.
They are set in your ``.toml`` config and are accessed using ``context.run_config["some_key"]``


# <a name="Auditing"></a>Auditing
<!-- WIP -->

# Contributing

We welcome contributions. Please see our [contributing guide](CONTRIBUTING.md) to get started.

# Acknowledgements

<!-- // WIP -->
