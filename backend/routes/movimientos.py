from fastapi import APIRouter, HTTPException
from models import Movimiento
from db import coleccion
from bson import ObjectId

router = APIRouter()

# Helper para convertir _id de Mongo a string
def movimiento_con_id(m):
    m["id"] = str(m["_id"])
    del m["_id"]
    return m

#Get
@router.get("/")
def leer_movimiento():
    movimientos = list(coleccion.find())
    return[movimiento_con_id(m) for m in movimientos]

#Post

@router.post("/")
def crear_movimiento(mov: Movimiento):
    resultado = coleccion.insert_one(mov.dict())
    return {"id":str(resultado.inserted_id)}


# Delete

@router.delete("/{id}")
def borrar_movimiento(id:str):
    resultado = coleccion.delete_one({"_id":ObjectId(id)})
    if resultado.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Movimiento no encontrado")
    return {"mensaje": "Movimiento no encontrado"}

# Put / Update

@router.put("/{id}")
def actualizar_movimiento(id:str, mov: Movimiento):
    resultado = coleccion.update_one(
        {"_id": ObjectId(id)},
        {"$set": mov.dict()}
    )
    if resultado.matched_count == 0:
        raise HTTPException(status_code=404, detail="Movimiento no encontrado")
    return {"mensaje": "Movimiento actualizado"}

