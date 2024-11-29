from .base import BaseConfig
import yaml

config_path = 'config.yaml'
with open(config_path, 'r') as file:
    config = yaml.safe_load(file)

class DatabaseConfig(BaseConfig):
    _instance = None
    def __new__(cls, **kwargs):
        if cls._instance is None:
            cls._instance = super(DatabaseConfig, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, **kwargs):
        super(DatabaseConfig, self).__init__(config['database'], **kwargs)
        for key, value in kwargs.items():
            setattr(self, key, value)

nosql_cfg = DatabaseConfig(type='NoSQLDatabase')
objdb_cfg = DatabaseConfig(type='ObjectDatabase')
sql_cfg = DatabaseConfig(type='SQLDatabase')