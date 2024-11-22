from pydantic import BaseModel
from .casilla import Casilla


class SistemaGuardado(BaseModel):
    casillas: list[list[Casilla]]
    vidas_restantes: int
    tiempo: int
    casillas_correctas: int
    vistos: int
    pistas: int


    def __str__(self):
        answer = f"{self.casillas}\n"
        answer += str(self.vidas_restantes) + "\n"
        answer += str(self.tiempo) + "\n"
        return answer
