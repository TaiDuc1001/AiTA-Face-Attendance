from manager import student_embedding_left_config, student_embedding_middle_config, student_embedding_right_config, student_info_config
from manager import Manager
import weaviate
from utils import *
from config import db_cfg, detector_cfg, recognizer_cfg

def main():
    client = weaviate.Client(
        embedded_options = weaviate.EmbeddedOptions(
            host = db_cfg.host,
            port = db_cfg.port
        )
    )
    manager = Manager(client=client)
    manager.create_class(student_info_config)
    manager.create_class(student_embedding_left_config)
    manager.create_class(student_embedding_middle_config)
    manager.create_class(student_embedding_right_config)

    extractor = recognizer_cfg.model
    detector = detector_cfg.model
