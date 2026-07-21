# MELODY : federated Machine Learning fOr dermatologY
![MELODy Logo](./assets/MELODY_LIGHT_WIDE.png)
MELODY is a project funded under the [DARE UK Real World Exemplar Programme](https://www.ukri.org/opportunity/dare-uk-real-world-research-exemplar-programme/). The aim of the project is to develop and test federated machine learning approaches for dermatology research using clinical images from NHS Tayside and Oxford University Hospitals. By training AI models across multiple TREs without centralising data, the project aims to support the development of more inclusive and representative dermatology AI systems.

# Preamble & Terminology
MELODY uses the [Flower Framework](https://flower.ai/docs/framework/main/en/index.html) to enable federated machine learning (FML).
Details on how to set up a Flower network are detailed in the [Flower.AI Setup](Flower.AI%20Setup.md) document.

MELODY uses a custom wrapper around the existing flwr tooling to provide
* Enhanced auditing
* Information to improve TRE/SDE Egress


# Benefits
<!-- WIP -->
## Enhanced Auditing
<!-- WIP -->
## TRE/SDE Egress Information
<!-- WIP -->

# Installation & Use
The MELODY cli tool is available from the [Release](https://github.com/HicResearch/MELODY/releases) section of this Github repo.
It is built as a linux standalone application, and can be used simply by running
```
./cli
```

## Configuration
To maximise the benefit of the MELODY cli,  there are several configuration options to set up:
<!-- git -->
## RO-Crates
[RO-Crates](https://www.researchobject.org/ro-crate/) are a method to package up your ML jobs with their metadata. To set up RO-Crates to work with MELODY:
1. Create a .toml config file with your RO-Crate details See the [sample config](./src/melody/config/sample_config.toml) example for more details.
2. When you next run a MELODY job, an RO-Crate will be generated detailing everything about the run.

## Logging
MELODY provides advanced logging for FML jobs. These logs are automatically generated and stored in ~/.mldy/melody.log This can be overwiitten via the config file.

# CLI Commands
## Run
## List
## Log
## Pull
## Stop







# Contributing

We welcome contributions. Please see our [contributing guide](CONTRIBUTING.md) to get started.

# Acknowledgements

<!-- // WIP -->
