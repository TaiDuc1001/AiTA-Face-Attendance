from .schemas import student_embedding_left_config, student_embedding_middle_config, student_embedding_right_config, student_info_config
from weaviate import Client
from utils import create_class, create_data_object

class Manager:
    def __init__(self, client: Client):
        self.client = client
    
    def create_class(self, config):
        create_class(config, self.client)

    def create_data_object(self, class_name: str, data_object: dict, identifier: str):
        create_data_object(class_name, data_object, identifier, self.client)