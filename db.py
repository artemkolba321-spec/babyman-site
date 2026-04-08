from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client.babyman  # база данных
requests_collection = db.sudo_requests