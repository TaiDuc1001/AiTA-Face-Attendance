from typing import Tuple, List
import torch
import cv2

def top1(results):
    scores = []
    for result in results:
        scores.append(result.boxes.conf)
    max_idx = scores.index(max(scores))
    xyxy = results[max_idx].boxes.xyxy[0]
    xyxy = map(int, list(xyxy))
    return xyxy

def preprocess(image_path: str,
               cropBox: List[int] = None,
               img_size: Tuple[int, int] = (224, 224),
               verbose: bool = False):
    image = cv2.imread(image_path)
    if cropBox:
        image = image[cropBox[1]: cropBox[3], cropBox[0]: cropBox[2]]
        if verbose:
            print(f'[bold green]Found cropBox: {cropBox}[/bold green]. Cropping image...')
    image = cv2.resize(image, img_size)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image