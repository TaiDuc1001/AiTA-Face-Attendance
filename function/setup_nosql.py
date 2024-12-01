from manager import \
    nosql_user_embed_left_schema, \
    nosql_user_embed_middle_schema, \
    nosql_user_embed_right_schema, \
    Manager
from .make_model import get_model
from utils import detect_preprocess, recognize_postprocess

import os
from os.path import join, exists
from os import listdir, remove, symlink
import weaviate
from insightface.app.common import Face


def setup_nosql(config: dict):
    objdb_cfg = config['ObjectDatabase']
    nosql_cfg = config['NoSQLDatabase']
    models_cfg = config

    os.makedirs(nosql_cfg.persistence_data_path, exist_ok=True)
    client = weaviate.Client(
        embedded_options = weaviate.EmbeddedOptions(
            host = nosql_cfg.host,
            port = nosql_cfg.port,
            persistence_data_path=nosql_cfg.persistence_data_path
        )
    )
    manager = Manager(client=client)
    for cls_name in manager.class_names:
        client.schema.delete_class(cls_name)

    manager.create_nosql_table(nosql_user_embed_left_schema)
    manager.create_nosql_table(nosql_user_embed_middle_schema)
    manager.create_nosql_table(nosql_user_embed_right_schema)

    detector = get_model(type='Detector', models_cfg=models_cfg)
    recognizer = get_model('Recognizer', models_cfg=models_cfg)

    for person in listdir(objdb_cfg.names[objdb_cfg.name]):
        person_dir = join(objdb_cfg.names[objdb_cfg.name], person)
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

        user = {
            'name': person,
            'embeddings': embeddings
        }

        manager.new_row(
            user_object=user,
            identifier='code',
            type='nosql'
        )

        print(f'User {person} added to the vector database')