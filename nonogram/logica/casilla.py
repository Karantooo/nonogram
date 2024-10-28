from pydantic import BaseModel


class Casilla(BaseModel):
    marcado: bool
    visibilidad: bool = False
    bandera: bool = False


