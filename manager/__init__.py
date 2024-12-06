from schemas import \
    nosql_user_embed_left_schema, \
    nosql_user_embed_middle_schema, \
    nosql_user_embed_right_schema, \
    sql_role_schema, \
    sql_status_schema, \
    sql_user_schema, \
    sql_attendance_schema
from utils import create_class, create_data_object
from .model import UserInfo, UserEmbedding, generate_user_code

from typing import Union
from weaviate import Client
import weaviate

class Manager:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Manager, cls).__new__(cls)
        return cls._instance

    def __init__(self, config: dict, client: Client = None):    
        self.config = config
        # self.client = weaviate.Client(
        #     embedded_options = weaviate.EmbeddedOptions(
        #         hostname = config['NoSQLDatabase']['hostname'],
        #         port = config['NoSQLDatabase']['port'],
        #         persistence_data_path = config['NoSQLDatabase']['persistence_data_path']
        #     )
        # ) if client is None else client
        self.client = weaviate.Client(
            url=f"http://{self.config['NoSQLDatabase']['hostname']}:{self.config['NoSQLDatabase']['port']}"
        ) if client is None else client
    def get_class_names(self):
        return [
            nosql_user_embed_left_schema['class'],
            nosql_user_embed_middle_schema['class'],
            nosql_user_embed_right_schema['class'],
        ]
    
    def create_nosql_table(self, config):
        create_class(config, self.client)

    def new_row(
            self,
            user_object: Union[UserInfo, UserEmbedding], 
            identifier: str,
            type: str = 'nosql') -> None:
        if type == 'nosql':
            self.create_nosql_data_object(
                user_object=user_object,
                identifier=identifier
            )

    def create_nosql_data_object(
            self,
            user_object: UserEmbedding, 
            identifier: str) -> None:
        class_names = self.get_class_names()
        user_embedding_left = {
            'code': user_object.code,
        }
        user_embedding_middle = {
            'code': user_object.code,
        }
        user_embedding_right = {
            'code': user_object.code,
        }
        create_data_object(
            class_name=class_names[0],
            data_object=user_embedding_left,
            identifier=identifier,
            vector=user_object.embeddings[0],
            client=self.client
        )
        create_data_object(
            class_name=class_names[1],
            data_object=user_embedding_middle,
            identifier=identifier,
            vector=user_object.embeddings[1],
            client=self.client
        )
        create_data_object(
            class_name=class_names[2],
            data_object=user_embedding_right,
            identifier=identifier,
            vector=user_object.embeddings[2],
            client=self.client
        )

