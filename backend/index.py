from fastapi import FastAPI, HTTPException, Form, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.staticfiles import StaticFiles

from routes import user, frames, fixing

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def fix_id(doc):
    doc["_id"] = str(doc["_id"])
    return doc

app.mount("/public", StaticFiles(directory="C:\\Users\\Kubus\\Desktop\\INZYNIERKA\\src\\public"), name="public") # PC
# app.mount("/public", StaticFiles(directory="C:\\Users\\Kuba\\Desktop\\projects\\INZYNIERKA\\src\\public"), name="public") # LAPTOP




app.include_router(user.router)
app.include_router(frames.router)
app.include_router(fixing.router)
    

    
    