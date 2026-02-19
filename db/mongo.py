from motor.motor_asyncio import AsyncIOMotorClient
from config import settings

client: AsyncIOMotorClient | None = None


def get_db():
    return client[settings.db_name]


async def connect():
    global client
    client = AsyncIOMotorClient(settings.mongodb_uri)


async def disconnect():
    global client
    if client:
        client.close()
