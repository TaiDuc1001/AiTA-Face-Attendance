from manager import \
    nosql_user_embed_left_schema, \
    nosql_user_embed_middle_schema, \
    nosql_user_embed_right_schema, \
    sql_role_schema, \
    sql_status_schema, \
    sql_user_schema, \
    sql_attendance_schema
from manager import Manager, User, generate_user_code
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
import onnx
import argparse

ort.set_default_logger_severity(3)  # 3 = Error level, suppresses warnings

def main(config: dict):
    manager = Manager()
    detector = get_model(type='Detector', models_cfg=config)
    recognizer = get_model(type='Recognizer', models_cfg=config)
    setup_sql()
    setup_nosql()

def parse_args():
    parser = argparse.ArgumentParser(description='Prepare the database')
    parser.add_argument('--config', type=str, default='config.yaml', help='Path to the config file')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    config = load_yaml(args.config)
    main()