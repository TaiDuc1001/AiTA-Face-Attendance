import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from manager import \
    nosql_user_embed_left_schema, \
    nosql_user_embed_middle_schema, \
    nosql_user_embed_right_schema, \
    Manager, \
    generate_user_code, \
    UserEmbedding
from function.make_model import get_model
from utils import detect_preprocess, recognize_postprocess, load_yaml

import os
from os.path import join, exists
from os import listdir, remove, symlink
import weaviate
from insightface.app.common import Face
from argparse import ArgumentParser
import onnxruntime as ort
import numpy as np
import pandas as pd

ort.set_default_logger_severity(3)


def setup_nosql(config: dict):
    objdb_cfg = config['ObjectDatabase']
    nosql_cfg = config['NoSQLDatabase']
    sql_cfg = config['SQLDatabase']
    user_data = pd.read_csv(join(sql_cfg['sample_data'], 'users.csv'))

    os.makedirs(nosql_cfg['persistence_data_path'], exist_ok=True)
    # client = weaviate.Client(
    #     embedded_options = weaviate.EmbeddedOptions(
    #         hostname = nosql_cfg['hostname'],
    #         port = nosql_cfg['port'],
    #         persistence_data_path=nosql_cfg['persistence_data_path']
    #     )
    # )
    client = weaviate.Client(
        url=f"http://{nosql_cfg['hostname']}:{nosql_cfg['port']}"
    )
    manager = Manager(client=client, config=config)
    for cls_name in manager.get_class_names():
        client.schema.delete_class(cls_name)

    manager.create_nosql_table(nosql_user_embed_left_schema)
    manager.create_nosql_table(nosql_user_embed_middle_schema)
    manager.create_nosql_table(nosql_user_embed_right_schema)

    detector = get_model(type='Detector', models_cfg=config)
    recognizer = get_model('Recognizer', models_cfg=config)

    people = []
    for person in listdir(objdb_cfg['names'][objdb_cfg['name']]):
        if not os.path.isdir(join(objdb_cfg['names'][objdb_cfg['name']], person)):
            continue
        people.append(person)

    for person in people:
        person_dir = join(objdb_cfg['names'][objdb_cfg['name']], person)
        embeddings = []
        for face in (listdir(person_dir)[1:4]):
            face = join(person_dir, face)
            img = detect_preprocess(face)
            bboxes, kpss = detector.detect(img, max_num=0, metric='default', input_size=img.shape[:2])
            
            if len(bboxes) == 0:
                print(f'No face detected in {join(person, face)}')
                continue
            if len(bboxes) > 1:
                print(f'More than one face detected in {join(person, face)}')
                continue

            face = Face(bbox=bboxes[0, :4], kps=kpss[0], det_score=bboxes[0, 4])
            embedding = recognizer.get(img, face)
            embeddings.append(embedding)

        embeddings = recognize_postprocess(embeddings)
        user = UserEmbedding(
            name=person,
            code=user_data[user_data['name'] == person]['code'].values[0],
            embeddings=embeddings
        )

        manager.new_row(
            user_object=user,
            identifier='code',
            type='nosql'
        )

        print(f'User {person} added to the vector database')

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--config', type=str, default='config.yaml')
    args = parser.parse_args()

    config = load_yaml(args.config)
    setup_nosql(config)