from ..config import configSetup
from pathlib import Path
import os
import subprocess
def setupSourceControl():
    print("Setting up source control")
    config = configSetup.getConfigFile()
    if config.get("git",None) is None:
      return
    gitDirectory = config["git"]["directory"]
    Path(gitDirectory).mkdir(parents=True,exist_ok=True)
    if( not os.path.exists(os.path.join(gitDirectory,'.git'))):
        print("Initialise git directory")
        subprocess.run("git init " + gitDirectory,shell=True)


def commit(string):
    config = configSetup.getConfigFile()
    if config.get("git",None) is None:
        return
    gitDirectory = config["git"]["directory"]
    print("Committing folder: " + string)
    print("git dir: " + gitDirectory)
    subprocess.run("cp -rf " +  string + ' ' +  gitDirectory+'/', shell=True)
    subprocess.run("cd "+ gitDirectory + "; git add " + string.split('/')[-1] + "; git commit -m 'message'",shell=True)
    #subprocess.run(["cd", gitDirectory,';','git','add', string.split('/')[-1],';','git','commit', '-m','message'])
