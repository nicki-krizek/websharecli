import os
import yaml


class Configuration:
    def __init__(self, config_path):
        try:
            with open(config_path, 'r') as file_:
                data = yaml.load(file_)
        except IOError:
            data = {}

        self.quality = data['quality'] if 'quality' in data else []
        if not self.quality:
            self.quality = ['']
        self.headers = data['headers'] if 'headers' in data else {}
        self.force_vip = data['force_vip'] if 'force_vip' in data else False


CONFIG_FILE_TEMPLATE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'static', 'config.yaml')
CONFIG_FILE = os.path.expanduser("~/.config/webshare/config.yaml")
CONFIG = Configuration(CONFIG_FILE)
