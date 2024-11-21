from manager import student_embedding_left_config, student_embedding_middle_config, student_embedding_right_config, student_info_config
from manager import Manager, client

def main():
    manager = Manager(client=client)
    manager.create_class(student_info_config)
    manager.create_class(student_embedding_left_config)
    manager.create_class(student_embedding_middle_config)
    manager.create_class(student_embedding_right_config)