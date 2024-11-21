from manager import student_embedding_left_config, student_embedding_middle_config, student_embedding_right_config, student_info_config
from manager import Manager
import weaviate

from config import weaviate_config, resnet_config, yolo_config

def main():
    client = weaviate.Client(
        embedded_options = weaviate.EmbeddedOptions(
            host = weaviate_config.host,
            port = weaviate_config.port
        )
    )
    manager = Manager(client=client)
    manager.create_class(student_info_config)
    manager.create_class(student_embedding_left_config)
    manager.create_class(student_embedding_middle_config)
    manager.create_class(student_embedding_right_config)

    extractor = resnet_config.model
    detector = yolo_config.model
