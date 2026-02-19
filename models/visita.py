from datetime import date, datetime, timezone
from typing import Annotated
from pydantic import BaseModel, Field


class Foto(BaseModel):
    url: str
    public_id: str


class VisitaBase(BaseModel):
    fecha: date
    sitio: str = Field(min_length=1)
    dirección: str = ""
    asistentes: list[str] = []
    fotos: list[Foto] = []
    puntuacion_comida: float = Field(default=5.0, ge=0, le=10)
    puntuacion_local: float = Field(default=5.0, ge=0, le=10)
    puntuacion_general: float = Field(default=5.0, ge=0, le=10)
    comentario: str = ""


class VisitaCreate(VisitaBase):
    pass


class VisitaUpdate(VisitaBase):
    pass


class VisitaOut(VisitaBase):
    id: Annotated[str, Field(alias="_id")]
    created_at: datetime

    model_config = {"populate_by_name": True}


def doc_to_visita(doc: dict) -> dict:
    """Convierte un documento MongoDB a dict serializable."""
    doc["_id"] = str(doc["_id"])
    if isinstance(doc.get("fecha"), date):
        doc["fecha"] = doc["fecha"].isoformat()
    return doc
