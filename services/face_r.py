import numpy as np
import cv2
import pickle
import os
from fastapi import UploadFile
from .yunet import YuNet
from utils.helpers import extract_embedding, match_face
from .emotion_detection import predict_emotion, class_to_emotion




# Load model paths
YUNET_MODEL = 'model_weights/face_detection_yunet_2023mar.onnx'


# Backend and target configuration (OpenCV + CPU)
BACKEND_ID = cv2.dnn.DNN_BACKEND_OPENCV
TARGET_ID = cv2.dnn.DNN_TARGET_CPU

# Initialize models
yunet = YuNet(modelPath=YUNET_MODEL, inputSize=[320, 320],
              confThreshold=0.4, nmsThreshold=0.3, topK=5000,
              backendId=BACKEND_ID, targetId=TARGET_ID)


async def detect_faces1(file: UploadFile) -> list:
    try:
        contents = await file.read()
        image = np.frombuffer(contents, np.uint8)
        frame = cv2.imdecode(image, cv2.IMREAD_COLOR)

        if frame is None:
            raise ValueError("Cannot decode image")

        yunet.setInputSize((frame.shape[1], frame.shape[0]))
        faces = yunet.infer(frame)
        detections = []

        if faces is not None and len(faces) > 0:
            # Pilih wajah dengan area terbesar
            max_area = 0
            largest_face = None
            for face in faces:
                x, y, w, h = face[:4].astype(int)
                area = w * h
                if area > max_area and w > 10 and h > 10:
                    max_area = area
                    largest_face = face

            if largest_face is not None:
                x, y, w, h, conf = largest_face[:5].astype(int)
                face_roi = frame[y:y + h, x:x + w]

                if face_roi.size != 0:

                    embedding = extract_embedding(face_roi)
                    name, similarity = match_face(embedding)
                    predicted_emotion = predict_emotion(face_roi)
                    emotion_text = class_to_emotion(predicted_emotion)

                    detections.append({
                        "bounding_box": [int(x), int(y), int(x + w), int(y + h)],
                        "name": name,
                        "similarity": similarity,
                        "emotion": emotion_text,
                    })

        return detections

    except Exception as e:
        print(f"Error in YuNet-SFace detection: {e}")
        raise e


