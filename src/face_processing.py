import boto3
import cv2
import numpy as np

def extract_faces(image_bytes, rekognition_client=None, min_confidence=90):
    if rekognition_client is None:
        rekognition_client = boto3.client('rekognition')

    response = rekognition_client.detect_faces(
        Image={'Bytes': image_bytes},
        Attributes=['ALL']
    )
    
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    extracted_faces = []

    for face in response.get('FaceDetails', []):
        if face['Confidence'] < min_confidence:
            continue
        
        box = face['BoundingBox']
        h, w = img.shape[:2]
        left = int(box['Left'] * w)
        top = int(box['Top'] * h)
        width = int(box['Width'] * w)
        height = int(box['Height'] * h)

        face_img = img[top:top+height, left:left+width]
        _, face_bytes = cv2.imencode('.jpg', face_img)
        extracted_faces.append(face_bytes.tobytes())

    return extracted_faces


def compare_faces(source_bytes, target_bytes, rekognition_client=None, threshold=80):
    if rekognition_client is None:
        rekognition_client = boto3.client('rekognition')

    response = rekognition_client.compare_faces(
        SourceImage={'Bytes': source_bytes},
        TargetImage={'Bytes': target_bytes},
        SimilarityThreshold=threshold
    )
    matches = response.get('FaceMatches', [])
    if matches:
        return matches[0]['Similarity']
    return 0
