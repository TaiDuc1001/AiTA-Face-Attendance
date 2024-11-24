from .base import BaseConfig
import yaml

config_path = 'config.yaml'
with open(config_path, 'r') as file:
    config = yaml.safe_load(file)

class DatabaseConfig(BaseConfig):
    def __init__(self, type: str, **kwargs):
        super().__init__(config[type])
        for key, value in kwargs.items():
            setattr(self, key, value)

vecdb_cfg = DatabaseConfig(type='VectorDatabase')
imgdb_cfg = DatabaseConfig(type='ImageDatabase')