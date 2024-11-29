from model import config as models_cfg
from insightface import model_zoo

class Detector:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Detector, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.model = model_zoo.get_model(models_cfg['Detector']['names'][models_cfg.name])

class Recognizer:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Recognizer, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.model = model_zoo.get_model(models_cfg['Recognizer']['names'][models_cfg.name])

def get_model(type: str):
    if type == 'Detector':
        return Detector().model
    elif type == 'Recognizer':
        return Recognizer().model