from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb+srv://272408:xgJarlUbM9puLXWH@cluster0.qxfsslt.mongodb.net/"

client = AsyncIOMotorClient(MONGO_URI)

db = client["ZPI"]
frames_collection = db["frames"]

@router.get("/")
async def home():
    count = await frames_collection.count_documents({})
    return {"documents": count}