from manager import \
    nosql_user_embed_left_schema, \
    nosql_user_embed_middle_schema, \
    nosql_user_embed_right_schema, \
    sql_role_schema, \
    sql_status_schema, \
    sql_user_schema, \
    sql_attendance_schema
from manager import Manager, User, generate_user_code
from config import nosql_cfg, objdb_cfg, sql_cfg
from utils import *
from .setup_nosql import setup_nosql
from .setup_sql import setup_sql
from .make_model import get_model

import os
from os.path import join, exists
from os import listdir, remove, symlink
import weaviate
from tqdm import tqdm
import cv2
import numpy as np
from insightface.app.common import Face
from insightface.data import get_image as ins_get_image
import PIL
import onnxruntime as ort
import subprocess

ort.set_default_logger_severity(3)  # 3 = Error level, suppresses warnings


def main():
    manager = Manager()
    detector = get_model('Detector')
    recognizer = get_model('Recognizer')
    setup_sql()
    setup_nosql()

    image_dir = objdb_cfg['names'][objdb_cfg.name]
    for person in tqdm(listdir(image_dir)):
        person_dir = join(image_dir, person)
        embeddings = []
        for face in (listdir(person_dir)[1:4]):
            face = join(person_dir, face)
            img = cv2.imread(face)
            img = cv2.resize(img, (224, 224))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            bboxes, kpss = detector.detect(img, max_num=0, metric='default', input_size=img.shape[:2])
            face = Face(bbox=bboxes[0, :4], kps=kpss[0], det_score=bboxes[0, 4])
            embedding = recognizer.get(img, face)
            embeddings.append(embedding)

        embeddings = recognize_postprocess(embeddings)
        user = User(
            name=person,
            code=generate_user_code(),
            gender=True,
            embeddings=embeddings
        )

        manager.new_row(user_object=user, identifier='code', type='nosql')

if __name__ == '__main__':
    main()