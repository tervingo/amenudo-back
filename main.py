import cloudinary
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from db.mongo import connect, disconnect
from routes.visitas import router as visitas_router
from routes.upload import router as upload_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect()
    cloudinary.config(
        cloud_name=settings.cloudinary_cloud_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
    )
    yield
    await disconnect()


app = FastAPI(title="Amenudo API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(visitas_router)
app.include_router(upload_router)


@app.get("/health")
async def health():
    return {"status": "ok"}
