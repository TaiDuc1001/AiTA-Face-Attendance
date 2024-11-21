import torch
import cv2
from typing import List
from rich import print as rprint
import numpy as np
import base64

def preprocess(image_path: str,
               cropBox: List[int] = None,
               ) -> torch.Tensor:
    image = cv2.imread(image_path)
    if cropBox:
        image = image[cropBox[2]: cropBox[4], cropBox[1]: cropBox[3]]
        rprint(f'[bold blue]Found cropBox: {cropBox}[/bold green]. Cropping image...')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = torch.Tensor([image]).permute(0, 3, 1, 2)
    return image

def postprocess(embedding: torch.Tensor) -> np.ndarray:
    embedding = embedding.cpu().detach().numpy().squeeze()
    embedding = base64.b64encode(embedding.tobytes()).decode('utf-8')
    return embedding