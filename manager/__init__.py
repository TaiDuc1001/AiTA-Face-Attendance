from .schemas import student_embedding_left_config, student_embedding_middle_config, student_embedding_right_config, student_info_config
from weaviate import Client
from utils import create_class, create_data_object
from .model import Student, generate_student_code

class Manager:
    def __init__(self, client: Client):
        self.client = client
        self.class_names = [
            'StudentEmbeddingLeft', 
            'StudentEmbeddingMiddle', 
            'StudentEmbeddingRight',
            'StudentInfo', 
        ]
    
    def create_class(self, config):
        create_class(config, self.client)

    def create_data_object(self,
                           student_object: Student, 
                           identifier: str) -> None:
        student_info = {
            'name': student_object.name,
            'code': student_object.code,
            'gender': student_object.gender
        }
        student_embedding_left = {
            'code': student_object.code,
        }
        student_embedding_middle = {
            'code': student_object.code,
        }
        student_embedding_right = {
            'code': student_object.code,
        }
        create_data_object(
            class_name=self.class_names[-1],
            data_object=student_info,
            identifier=identifier,
            vector=None,
            client=self.client
        )
        create_data_object(
            class_name=self.class_names[0],
            data_object=student_embedding_left,
            identifier=identifier,
            vector=student_object.embeddings[0],
            client=self.client
        )
        create_data_object(
            class_name=self.class_names[1],
            data_object=student_embedding_middle,
            identifier=identifier,
            vector=student_object.embeddings[1],
            client=self.client
        )
        create_data_object(
            class_name=self.class_names[2],
            data_object=student_embedding_right,
            identifier=identifier,
            vector=student_object.embeddings[2],
            client=self.client
        )