from facenet_pytorch import InceptionResnetV1
from .config import config

if config['Recognizer']['name'] == 'resnet':
    model = InceptionResnetV1(pretrained='vggface2').eval()
else:
    raise ValueError('Invalid recognizer name')