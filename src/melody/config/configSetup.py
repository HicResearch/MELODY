import os
from pathlib import Path
import toml


def exists():
    home = Path.home()
    if not os.path.isfile(str(home) + '/.mldy/config.toml'):
        return False
    return True


def getConfigFile():
    home = Path.home()
    configFile = toml.load(str(home) + '/.mldy/config.toml')
    return configFile

def createConfigFile():
    home = str(Path.home())
    Path(home + "\.mldy").mkdir(parents=False,exist_ok=True)
    config = """
[git]
    directory= '{gitLocation}'    
[logging]
    file = '{fileLocation}'
    """.format(fileLocation=home + "\.mldy\melody.log").format(gitLocation=home + "\.mldy\srcControl")
    with open(home + '/.mldy/config.toml','w') as configFile:
        configFile.write(config)


def setup():
    if not exists():
        createConfigFile()


