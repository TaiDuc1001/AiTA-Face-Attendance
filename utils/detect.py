from typing import Tuple, List
import cv2
import numpy as np

def top1(results):
    scores = []
    for result in results:
        scores.append(result.boxes.conf)
    max_idx = scores.index(max(scores))
    xyxy = results[max_idx].boxes.xyxy[0]
    xyxy = map(int, list(xyxy))
    return xyxy

def preprocess(image: str,
               cropBox: List[int] = None,
               img_size: Tuple[int, int] = (224, 224),
               verbose: bool = False):
    if type(image) == str:
        image = cv2.imread(image)
    elif type(image) == np.ndarray:
        image = image
    if cropBox:
        image = image[cropBox[1]: cropBox[3], cropBox[0]: cropBox[2]]
        if verbose:
            print(f'[bold green]Found cropBox: {cropBox}[/bold green]. Cropping image...')
    image = cv2.resize(image, img_size)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image