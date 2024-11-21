import torch
import cv2
from typing import List, Union
from rich import print
import base64

def preprocess(image_path: str,
               cropBox: List[int] = None,
               ) -> torch.Tensor:
    image = cv2.imread(image_path)
    if cropBox:
        image = image[cropBox[2]: cropBox[4], cropBox[1]: cropBox[3]]
        print(f'[bold blue]Found cropBox: {cropBox}[/bold green]. Cropping image...')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = torch.Tensor([image]).permute(0, 3, 1, 2)
    return image

def postprocess(embeddings: Union[List[torch.Tensor], torch.Tensor]) -> Union[List[str], str]:
    if isinstance(embeddings, List):
        embeddings = [postprocess(embedding) for embedding in embeddings]
        return embeddings
    
    embedding = embeddings
    if not isinstance(embedding, torch.Tensor):
        embedding = torch.Tensor(embedding)
    embedding = embedding.cpu().detach().numpy().squeeze()
    embedding = base64.b64encode(embedding.tobytes()).decode('utf-8')
    return embedding
