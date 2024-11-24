from .schemas import student_embedding_left_config, student_embedding_middle_config, student_embedding_right_config, student_info_config
from weaviate import Client
from utils import create_class, create_data_object
from .model import Student

class Manager:
    def __init__(self, client: Client):
        self.client = client
        self.class_names = [
            'StudentEmbeddingLeft', 
            'StudentEmbeddingMiddle', 
            'StudentEmbeddingRight'
            'StudentInfo', 
        ]
    
    def create_class(self, config):
        create_class(config, self.client)

    def create_data_object(self,
                           student_object: Student, 
                           identifier: str) -> None:
        student_info = {
            'name': student_object.name,
            'gender': student_object.gender
        }
        student_embedding_left = {
            'name': student_object.name,
            'embedding': student_object.embeddings[0]
        }
        student_embedding_middle = {
            'name': student_object.name,
            'embedding': student_object.embeddings[1]
        }
        student_embedding_right = {
            'name': student_object.name,
            'embedding': student_object.embeddings[2]
        }
        create_data_object(self.class_names[-1], student_info, identifier, self.client)
        create_data_object(self.class_names[0], student_embedding_left, identifier, self.client)
        create_data_object(self.class_names[1], student_embedding_middle, identifier, self.client)
        create_data_object(self.class_names[2], student_embedding_right, identifier, self.client)