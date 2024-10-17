from fastapi import FastAPI
from app.routes.user_routes import router as user_router
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import Config

app = FastAPI()

client: AsyncIOMotorClient = None

@app.on_event("startup")
async def startup_db_client():
    global client
    client = AsyncIOMotorClient(Config.MONGO_URI)
    app.db = client.user_management

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()

app.include_router(user_router, prefix="/api")
