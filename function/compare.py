from utils import detect_preprocess, recognize_postprocess
from manager import Manager

from insightface.app.common import Face
from function.make_model import get_model
import numpy as np
from typing import List, Tuple

def compare(
        frame: np.ndarray,
        config: dict
    ) -> Tuple[str, float, List[float]]:
    # Load models
    detector = get_model(type='Detector', models_cfg=config)
    recognizer = get_model(type='Recognizer', models_cfg=config)

    # Preprocess the image
    img = detect_preprocess(frame)

    # Detect faces in the image
    bboxes, kpss = detector.detect(img, max_num=0, metric='default', input_size=img.shape[:2])
    if len(bboxes) == 0:
        print("No face detected")
        return None
    if len(bboxes) > 1:
        print("More than one face detected")
        return None

    # Get the face embedding
    face = Face(bbox=bboxes[0, :4], kps=kpss[0], det_score=bboxes[0, 4])
    embedding = recognizer.get(img, face)
    embedding = recognize_postprocess(embedding)

    manager = Manager(config=config)
    client = manager.client
    # Query the database for the student code
    response = (
        client.query
        .get("UserEmbeddingLeft", ["code"])
        .with_near_vector({"vector": embedding})
        .with_limit(1)
        .with_additional(["certainty", "distance"])
        .do()
    )
    results = (None, response['data']['Get']['UserEmbeddingLeft'][0]['certainty'], bboxes[0, :4])
    if response['data']['Get']['UserEmbeddingLeft']:
        student_code = response['data']['Get']['UserEmbeddingLeft'][0]['code']
        results[0] = student_code
    else:
        print("No matching student code found")
    return results