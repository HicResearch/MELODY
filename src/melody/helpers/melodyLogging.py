import logging
import os
from ..config import configSetup

def setupLogger():
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(user)s - %(levelname)s - %(message)s',
        defaults={"user":os.environ.get('USER', os.environ.get('USERNAME'))}
    )

    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)

    config = configSetup.getConfigFile()
    logFile = config["logging"]["file"]
    #TODO this isn't working with the ~
    fileHandler = logging.FileHandler(logFile)
    fileHandler.setFormatter(formatter)
    fileHandler.setLevel(logging.DEBUG)

    logger = getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(streamHandler)
    logger.addHandler(fileHandler)
    return logger

def getLogger():
    return logging.getLogger("MELODY")


def log(args):
    getLogger().info(args)
