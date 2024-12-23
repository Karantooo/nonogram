import numpy as np
import pygame

from nonogram.visual.boton import Boton


class Tablero:
    valores: np.ndarray # Matriz que representa la imagen en Blanco o Negro que condiciona la creacion de los botones
    marcados: int       # Contador de botones marcados
    vistos: int         # Contador de botones vistos
    correctos: int      # Contador de botones correctos
    vidas: int          # Contador de vidas restantes

    def __init__(self, marcados: int, vidas: int = 3, vistos: int = 0, correctos: int = 0):
        self.marcados = marcados
        self.vistos = vistos
        self.correctos = correctos
        self.vidas = vidas

    def validar_click(self,mouse_pos: tuple[int,int], botones: list[list[Boton]], array_pos: tuple[int,int]):
        correcto = botones[array_pos[1]][array_pos[0]].validar_click(mouse_pos)

        if correcto != 2:
            self.vistos += 1
            if correcto:
                self.correctos += 1
            else:
                self.vidas -= 1

    def get_vidas(self) -> int:
        return self.vidas

    def get_vistos(self) -> int:
        return self.vistos

    def ganado(self) -> bool:
        return self.correctos == self.marcados
