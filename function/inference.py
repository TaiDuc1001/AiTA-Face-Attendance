from os import listdir
from os.path import join
from insightface import model_zoo
from insightface.app.common import Face
from tqdm import tqdm
import cv2
import os
from config import vecdb_cfg, imgdb_cfg
from model import config as models_cfg
import weaviate


def main():
    os.makedirs(vecdb_cfg.persistence_data_path, exist_ok=True)
    client = weaviate.Client(
        embedded_options = weaviate.EmbeddedOptions(
            host = vecdb_cfg.host,
            port = vecdb_cfg.port,
            persistence_data_path=vecdb_cfg.persistence_data_path
        )
    )
    detector = model_zoo.get_model(models_cfg['Detector']['names'][models_cfg.name])
    recognizer = model_zoo.get_model(models_cfg['Recognizer']['names'][models_cfg.name])

    image_dir = imgdb_cfg['names'][imgdb_cfg.name]
    for person in tqdm(listdir(image_dir)):
        person_dir = join(image_dir, person)
        embeddings = []
        print(person)
        for face in listdir(person_dir):
            face = join(person_dir, face)
            img = cv2.imread(face)
            img = cv2.resize(img, (224, 224))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            bboxes, kpss = detector.detect(img, max_num=0, metric='default',input_size=img.shape[:2])
            face = Face(bbox=bboxes[0, :4], kps=kpss[0], det_score=bboxes[0, 4])
            embedding = recognizer.get(img, face)
            embeddings.append(embedding)

        response = (
            client.query
            .get("StudentEmbeddingLeft", ["code"])
            .with_near_vector({"vector": embeddings[0]})
            .with_limit(2).with_additional(["certainty", "distance"])
            .do()
        )

        try:
            for i in range(len(response['data']['Get']['StudentEmbeddingLeft'])):
                found = response['data']['Get']['StudentEmbeddingLeft'][i]['code']
                student_info_response = client.query.get(
                    "StudentInfo",  
                    ["name", "code", "gender"]  
                ).with_where({
                    "path": ["code"],  
                    "operator": "Equal",
                    "valueText": found  
                }).do()

                try:
                    student_name = student_info_response['data']['Get']['StudentInfo'][0]['name']
                    certainty = response['data']['Get']['StudentEmbeddingLeft'][i]["_additional"]['certainty']
                    distance = response['data']['Get']['StudentEmbeddingLeft'][i]["_additional"]['distance']
                    print(f"Found student info: {student_name} Certainty: {certainty} distance: {distance}")
                except Exception as e:
                    print("No student info found for the given ID")

        except Exception as e:
            print("No student found")
            
        break