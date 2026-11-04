from fastapi import UploadFile, Form, File, APIRouter, HTTPException
from model.fit_frames_prediction import get_face_features
from model.create_dataset_brows import load_dlib_detector, visualize_detected_points, detect_landmarks
from typing import Optional
import json
import asyncio

router = APIRouter()

@router.post("/fixing")
async def control_ai(photo: UploadFile = File(...)):

    photo_path = "C:\\Users\\Kubus\\Desktop\\INZYNIERKA\\backend\\photos\\photo1.jpg" # PC
    # photo_path = "C:\\Users\\Kuba\\Desktop\\projects\\INZYNIERKA\\backend\\photos\\photo1.jpg" # LAPTOP
    
    with open(photo_path, "wb") as f:
        content = await photo.read()
        f.write(content)
        
    eye_spacing, face_shape, brows_shape = get_face_features(photo_path)


    return eye_spacing, face_shape, brows_shape



