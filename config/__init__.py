from .base import BaseConfig
import yaml
from model import resnet, yolo11n

config_path = 'config.yaml'
with open(config_path, 'r') as file:
    config = yaml.safe_load(file)

class DatabaseConfig(BaseConfig):
    def __init__(self, **kwargs):
        super().__init__(config['VectorDatabase'])
        for key, value in kwargs.items():
            setattr(self, key, value)

class DetectorConfig(BaseConfig):
    def __init__(self, **kwargs):
        super().__init__(config['Detector'])
        for key, value in kwargs.items():
            setattr(self, key, value)

class RecognizerConfig(BaseConfig):
    def __init__(self, **kwargs):
        super().__init__(config['Recognizer'])
        for key, value in kwargs.items():
            setattr(self, key, value)

db_cfg = DatabaseConfig()
detector_cfg = DetectorConfig(model=yolo11n)
recognizer_cfg = RecognizerConfig(model=resnet)