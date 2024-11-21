class BaseConfig:
    def __init__(self, config: dict, **kwargs):
        for key, value in config.items():
            setattr(self, key, value)
        
        for key, value in kwargs.items():
            setattr(self, key, value)