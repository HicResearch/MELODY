from ..config import configSetup
from pathlib import Path
import os
import subprocess
def setupSourceControl():
    print("Setting up source control")
    config = configSetup.getConfigFile()
    gitDirectory = config["git"]["directory"]
    Path(gitDirectory).mkdir(parents=True,exist_ok=True)
    if( not os.path.exists(os.path.join(gitDirectory,'.git'))):
        print("Initialise git directory")
        subprocess.run(["git","init",gitDirectory])


def commit(string):
    config = configSetup.getConfigFile()
    gitDirectory = config["git"]["directory"]
    print("Committing folder: " + string)
    subprocess.run(["cp" "-rf", string,os.path.join(gitDirectory,'/')])
    subprocess.run(["cd", gitDirectory,';','git','add', string.split('/')[-1],';','git','commit', '-m','message'])
