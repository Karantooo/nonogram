from pydantic import BaseModel


class Casilla(BaseModel):
    marcado: bool
    visibilidad: bool = False
    bandera: bool = False

    def __str__(self):
        if self.visibilidad:
            return 'O'
        if self.bandera:
            return 'B'
        return 'X'


