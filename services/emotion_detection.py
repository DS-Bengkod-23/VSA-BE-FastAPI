import cv2
import numpy as np
import onnxruntime

# Load Emotion Detection ONNX model
emotion_session = onnxruntime.InferenceSession('model_weights/emotion.onnx')

def preprocess_emotion_image(face_image: np.ndarray) -> np.ndarray:
    img = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, (48, 48)).astype(np.float32) / 255.0
    img = np.expand_dims(img, axis=(0, -1))
    return img

def predict_emotion(face_image: np.ndarray) -> int:
    preprocessed_img = preprocess_emotion_image(face_image)
    input_name = emotion_session.get_inputs()[0].name
    output_name = emotion_session.get_outputs()[0].name
    result = emotion_session.run([output_name], {input_name: preprocessed_img})
    return int(np.argmax(result[0]))

def class_to_emotion(predicted_emotion: int) -> str:
    res_dict = {0: 'angry', 1: 'disgusted', 2: 'fearful', 3: 'happy', 4: 'neutral', 5: 'sad', 6: 'surprised'}
    return res_dict.get(predicted_emotion, "Unknown")
