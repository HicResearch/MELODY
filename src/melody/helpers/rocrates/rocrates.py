import datetime
import getpass
import uuid

from rocrate.model import ContextEntity
from rocrate.rocrate import ROCrate

from melody.config import configSetup


def add_authors_and_affiliations(crate: ROCrate) -> None:
    config = configSetup.getConfigFile()
    users = config["users"]
    print(users)
    for user in users:
        # uniman = crate.add(
            #     ContextEntity(
            #         crate,
            #         "https://ror.org/027m9bs27",
            #         properties={
            #             "@type": "Organization",
            #             "name": "The University of Manchester",
            #             "url": "https://www.manchester.ac.uk",
            #         },
            #     )
            # )
        affil = crate.add(
            ContextEntity(
                crate,
                user['orgROR'],
                properties=
                {
                    "@type": "Organization",
                    "name": user['orgName'],
                    "url": user['orgUrl'],
                }
            )
        )

        u = crate.add(
            ContextEntity(
                crate,
                user['orcid'],
                properties={
                    "@type": "Person",
                    "name": user['firstName'] + " " + user['lastName'],
                    "givenName": user['firstName'],
                    "familyName": user['lastName'],
                },
            )
        )
        u['affiliation'] = affil
    return


def make_crate(app: str) -> None:
    config = configSetup.getConfigFile()

    crate = ROCrate()
    output_dir = config["RO-Crates"]['outputDirectory'] + '/'+ datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    ##################
    # core metadata  #
    ##################

    crate.name=config["RO-Crates"]['name']
    crate.description=config["RO-Crates"]['description']
    # license = crate.add(
    #     ContextEntity(
    #         crate,
    #         "https://spdx.org/licenses/CC0-1.0",
    #         properties={
    #             "@type": "CreativeWork",
    #             "name": "Creative Commons Zero v1.0 Universal",
    #             "url": "https://creativecommons.org/publicdomain/zero/1.0/legalcode",
    #         },
    #     )
    # )
    # crate.license = license

    crate.root_dataset["identifier"] = "unsure how this will work with fed learn"

    add_authors_and_affiliations(crate=crate)

    # crate.root_dataset["publisher"] = crate.get(config['Dataset']['publisher'])
    # crate.root_dataset["author"] = crate.get(config['Dataset']['author'])

    ############
    # training datasets #
    ############
    datasets = []
    for dataset in config['datasets']:
        datasets += crate.add_dataset(
            source=dataset['source'],
            dest_path=None,
            properties={
                "name": dataset['name'],
                "description": dataset['description'],
                "conformsTo": dataset['conformsTo'],
                "encodingFormat": dataset['encodingFormat'],
            },
        )

    #################
    # configuration #
    #################
    # instrument - Flower
    flower = crate.add(
        ContextEntity(
            crate,
            "https://flower.ai",
            properties={
                "@type": "SoftwareApplication",
                "name": "Flower",
                "description": "Flower federated learning framework",
                "version": "1.26.1",
                "url": "https://flower.ai",
            },
        )
    )

    #Flower project files - configuration - TODO may need to add files etc in hereßß
    flower_project = crate.add_dataset(
        source='./',
        dest_path=app,
        properties={
            "name": "Flower project folder",
            "description": "A Flower projßßect",
        },
    )

    flower_config_scripts = crate.add_dataset(
        source=app,
        dest_path=app,
        properties={
            "name": "Flower configuration scripts",
            "description": "Flower scripts written in Python which configure the client app, server app, datasets, and model",
            "encodingFormat": "text/x-python",
        },
    )
    flower_config_file = crate.add_file(
        source=app +"/pyproject.toml",
        dest_path=app+"/pyproject.toml",
        properties={
            "name": "Flower project configuration TOML",
            "description": "A TOML file which includes the configuration for the Flower project. It's also a Python project configuration file.",
            "encodingFormat": "application/toml",
        },
    )
    flower_project["hasPart"] = [flower_config_scripts, flower_config_file]

    #################
    # output model #
    #################
    # TODO

    #############
    # execution #
    #############
    execution = crate.add_action(
        instrument=flower,
        identifier=f"#action-{uuid.uuid4()}",
        object=[flower_config_scripts, flower_config_file] + datasets,
        # result=[model_file],
        properties={
            "name": "Execution of federated learning process",
            "description": "Execution of the federated learning process using `flwr run`",
            # TODO "startTime"
            # TODO "endTime"
        },
    )
    execution["agent"] = getpass.getuser()

    #################
    # write & check #
    #################
    crate.root_dataset.append_to("mentions", execution)  # TODO
    # the output model is the focus of the crate
    # crate.root_dataset["mainEntity"] = model_file  # TODO
    # conforms to process run crate
    process_run_crate = crate.add(
        ContextEntity(
            crate,
            "https://w3id.org/ro/wfrun/process/0.5",
            properties={
                "name": "Process Run Crate",
                "@type": "CreativeWork",
                "version": "0.5",
            },
        )
    )
    crate.root_dataset.append_to("conformsTo", process_run_crate)

    # Writing the RO-Crate metadata:
    crate.write(output_dir)

    # validate_crate(
    #     output_dir,
    #     profile_identifier="process-run-crate-0.5",
    #     requirement_severity=models.Severity.RECOMMENDED,
    # )


if __name__ == "__main__":
    make_crate()