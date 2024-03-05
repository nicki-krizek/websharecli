import os
import yaml


class Configuration:

    TOR_DEFAULT_PORT = 9050
    CHUNK_SIZE = 1024
    THREAD_POOL_SIZE = 4

    def __init__(self, config_path):
        try:
            with open(config_path, 'r') as f:
                data = yaml.safe_load(f)
        except IOError:
            data = {}

        self.quality = data['quality'] if 'quality' in data else []
        if not self.quality:
            self.quality = ['']
        self.force_vip = data['force_vip'] if 'force_vip' in data else False
        self.types = data['types'] if 'types' in data else None
        self.wst = data['wst'] if 'wst' in data else ''
        self.exclude = data['exclude'] if 'exclude' in data else []
        # downloader config
        self.tor_port = data['tor_port'] if 'tor_port' in data else self.TOR_DEFAULT_PORT
        self.chunk_size = data['chunk_size'] if 'chunk_sze' in data else self.CHUNK_SIZE
        self.pool_size = data['pool_size'] if 'pool_size' in data else self.THREAD_POOL_SIZE


CONFIG_FILE_TEMPLATE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'static', 'config.yaml')
CONFIG_FILE = os.path.expanduser("~/.config/webshare/config.yaml")
CONFIG = Configuration(CONFIG_FILE)
