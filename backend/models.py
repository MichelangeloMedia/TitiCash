from pydantic import BaseModel
from datetime import datetime
from typing import TypeAlias, Literal


class Movimiento(BaseModel):
    tipo: Literal["Ingreso", "Egreso"]
    monto: float
    descripcion: str
    categoria: str
    metodo: str
    fecha: datetime

