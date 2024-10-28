from pydantic import BaseModel


class Casilla(BaseModel):
    marcado: int
    visibilidad: bool = False
    bandera: bool = False


