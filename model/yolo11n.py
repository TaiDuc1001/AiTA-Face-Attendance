from ultralytics import YOLO
from .config import config

if config['Detector']['name'] == 'yolo11n':
    model = YOLO(config['Detector']['path'])
else:
    raise ValueError('Invalid detector name')