import os
from pathlib import Path
import toml


def exists():
    home = Path.home()
    if not os.path.isfile(str(home) + '/.mldy/config.toml'):
        return False
    return True


def getConfigFile(configLocation):
    configFile = toml.load(configLocation)
    return configFile

def createConfigFile():
    home = str(Path.home())
    Path(home + "/.mldy").mkdir(parents=False,exist_ok=True)
    config = """
    [test]
    """
    with open(home + '/.mldy/config.toml','w') as configFile:
        configFile.write(config)


def setup():
    if not exists():
        createConfigFile()


