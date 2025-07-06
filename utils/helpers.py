import numpy as np
import cv2
from scipy.spatial.distance import cosine
from PIL import Image
import onnxruntime
import pickle
from models.schemas import MetaResponse, ApiResponse
import base64


def audio_to_base64(file_path):
    with open(file_path, "rb") as audio_file:
        audio_base64 = base64.b64encode(audio_file.read()).decode("utf-8")
    return audio_base64


def create_response(status: str, code: int, message: str, data: dict = None) -> ApiResponse:
    meta = MetaResponse(status=status, code=code, message=message)
    return ApiResponse(meta=meta, data=data)

# Load FaceNet ONNX model
facenet_session = onnxruntime.InferenceSession('model_weights/facenet_model.onnx')

def preprocess_face(face_image: np.ndarray) -> np.ndarray:
    img = Image.fromarray(cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB))
    img = img.resize((160, 160))
    img = np.array(img).astype(np.float32)
    img = (img - 127.5) / 128.0
    img = np.transpose(img, (2, 0, 1))
    img = np.expand_dims(img, axis=0)
    return img

def extract_embedding(face_image: np.ndarray) -> np.ndarray:
    preprocessed_face = preprocess_face(face_image)
    embedding = facenet_session.run(None, {'input': preprocessed_face})[0].flatten()
    return embedding

def match_face(embedding: np.ndarray, threshold: float = 0.6) -> tuple[str, float]:
    # Load embeddings from pickle file
    with open('model_weights/new_embeddings.pkl', 'rb') as f:
        embeddings_db = pickle.load(f)

    min_distance = float('inf')
    best_match = "Unknown"
    best_similarity = 0.0

    for person_name, saved_embedding in embeddings_db.items():
        distance = cosine(embedding, saved_embedding)
        similarity = 1 - distance

        if distance < min_distance and distance < threshold:
            min_distance = distance
            best_match = person_name
            best_similarity = float(similarity)

    return best_match, best_similarity
