import cloudinary.uploader
from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel

router = APIRouter(prefix="/upload", tags=["upload"])

FOLDER = "amenudo"


# ── POST /upload ─────────────────────────────────────────────────────────────
@router.post("/")
async def upload_foto(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="El archivo debe ser una imagen")

    contents = await file.read()
    try:
        result = cloudinary.uploader.upload(
            contents,
            folder=FOLDER,
            resource_type="image",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al subir la imagen: {e}")

    return {
        "url": result["secure_url"],
        "public_id": result["public_id"],
    }


# ── DELETE /upload ───────────────────────────────────────────────────────────
class DeleteRequest(BaseModel):
    public_id: str


@router.delete("/")
async def delete_foto(body: DeleteRequest):
    try:
        result = cloudinary.uploader.destroy(body.public_id, resource_type="image")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al borrar la imagen: {e}")

    if result.get("result") not in ("ok", "not found"):
        raise HTTPException(status_code=500, detail="No se pudo eliminar la imagen")

    return {"deleted": body.public_id}
