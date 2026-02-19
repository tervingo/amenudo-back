from datetime import datetime, timezone
from bson import ObjectId
from bson.errors import InvalidId
from fastapi import APIRouter, HTTPException, status

from db.mongo import get_db
from models.visita import VisitaCreate, VisitaUpdate, doc_to_visita

router = APIRouter(prefix="/visitas", tags=["visitas"])

COLLECTION = "visitas"


def get_collection():
    return get_db()[COLLECTION]


def object_id(id: str) -> ObjectId:
    try:
        return ObjectId(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID inválido")


# ── GET /visitas ─────────────────────────────────────────────────────────────
@router.get("/")
async def list_visitas():
    col = get_collection()
    docs = await col.find().sort("fecha", -1).to_list(length=None)
    return [doc_to_visita(d) for d in docs]


# ── GET /visitas/{id} ────────────────────────────────────────────────────────
@router.get("/{id}")
async def get_visita(id: str):
    col = get_collection()
    doc = await col.find_one({"_id": object_id(id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Visita no encontrada")
    return doc_to_visita(doc)


# ── POST /visitas ────────────────────────────────────────────────────────────
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_visita(body: VisitaCreate):
    col = get_collection()
    data = body.model_dump()
    data["created_at"] = datetime.now(timezone.utc)
    result = await col.insert_one(data)
    doc = await col.find_one({"_id": result.inserted_id})
    return doc_to_visita(doc)


# ── PUT /visitas/{id} ────────────────────────────────────────────────────────
@router.put("/{id}")
async def update_visita(id: str, body: VisitaUpdate):
    col = get_collection()
    data = body.model_dump()
    result = await col.update_one(
        {"_id": object_id(id)},
        {"$set": data},
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Visita no encontrada")
    doc = await col.find_one({"_id": object_id(id)})
    return doc_to_visita(doc)


# ── DELETE /visitas/{id} ─────────────────────────────────────────────────────
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_visita(id: str):
    col = get_collection()
    result = await col.delete_one({"_id": object_id(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Visita no encontrada")
