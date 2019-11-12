import threading
import configparser
import os


class Config(object):
    _instance_lock = threading.Lock()

    def __init__(self):
        config_path = os.getcwd()+'/config/config.ini'
        self.config = configparser.ConfigParser()
        self.config.read(config_path)

    def __new__(cls, *args, **kwargs):
        with Config._instance_lock:
            if hasattr(Config, 'instance'):
                return Config.instance
            else:
                Config.instance = object.__new__(cls)

        return Config.instance

