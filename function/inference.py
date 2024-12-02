from os import listdir
from os.path import join
from insightface import model_zoo
from insightface.app.common import Face
from tqdm import tqdm
import cv2
import os
import weaviate
import argparse
from function.live import CameraManager


def main(config: dict):
    imgdb_cfg = config['ObjectDatabase']
    vecdb_cfg = config['NoSQLDatabase']
    models_cfg = config['Models']

    os.makedirs(vecdb_cfg.persistence_data_path, exist_ok=True)
    client = weaviate.Client(
        embedded_options = weaviate.EmbeddedOptions(
            host = vecdb_cfg.host,
            port = vecdb_cfg.port,
            persistence_data_path=vecdb_cfg.persistence_data_path
        )
    )
    detector = model_zoo.get_model(models_cfg['Detector']['names'][models_cfg.name])
    recognizer = model_zoo.get_model(models_cfg['Recognizer']['names'][models_cfg.name])

    camera_manager = CameraManager(config)
    camera_manager.live()

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, help="Path to configuration file", default='config.yaml')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    main(args.config)