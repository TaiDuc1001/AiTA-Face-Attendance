from .database import weaviate_config
from .base import BaseConfig
from .recognition_model import resnet_config
from .detection_model import yolo_config

class WeaviateConfig(BaseConfig):
    def __init__(self):
        super().__init__(weaviate_config)

class RecognitionModelConfig(BaseConfig):
    def __init__(self):
        super().__init__(resnet_config)

class DetectionModelConfig(BaseConfig):
    def __init__(self):
        super().__init__(yolo_config)

weaviate_config = WeaviateConfig()
resnet_config = RecognitionModelConfig()
yolo_config = DetectionModelConfig()