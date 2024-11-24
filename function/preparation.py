import os
from os.path import join, exists
from os import listdir, remove, symlink

from manager import student_embedding_left_config, student_embedding_middle_config, student_embedding_right_config, student_info_config
from manager import Manager, Student, generate_student_code
from model import config as models_cfg
from config import vecdb_cfg, imgdb_cfg
from utils import *

import weaviate
from tqdm import tqdm
import cv2
import numpy as np
from insightface import model_zoo
from insightface.app.common import Face
from insightface.data import get_image as ins_get_image
import PIL
import onnxruntime as ort

ort.set_default_logger_severity(3)  # 3 = Error level, suppresses warnings

def main():
    os.makedirs(vecdb_cfg.persistence_data_path, exist_ok=True)
    client = weaviate.Client(
        embedded_options = weaviate.EmbeddedOptions(
            host = vecdb_cfg.host,
            port = vecdb_cfg.port,
            persistence_data_path=vecdb_cfg.persistence_data_path
        )
    )
    manager = Manager(client=client)
    for cls_name in manager.class_names:
        client.schema.delete_class(cls_name)

    manager.create_class(student_info_config)
    manager.create_class(student_embedding_left_config)
    manager.create_class(student_embedding_middle_config)
    manager.create_class(student_embedding_right_config)

    detector = model_zoo.get_model(models_cfg['Detector']['names'][models_cfg.name])
    recognizer = model_zoo.get_model(models_cfg['Recognizer']['names'][models_cfg.name])

    image_dir = imgdb_cfg['names'][imgdb_cfg.name]
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
        student = Student(
            name=person,
            code=generate_student_code(),
            gender=True,
            embeddings=embeddings
        )

        manager.create_data_object(student_object=student, identifier='code')

if __name__ == '__main__':
    main()