from pydantic import BaseModel
from .casilla import Casilla


class SistemaGuardado(BaseModel):
    casillas: list[Casilla]
    vidas_restantes: int
    tiempo: int
