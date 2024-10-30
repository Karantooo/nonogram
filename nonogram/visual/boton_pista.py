import numpy as np
import pygame
from nonogram.visual.boton import Boton
from nonogram.logica.pistas import Pistas


class BotonPista:

    alto: int
    ancho: int
    dimensiones_pantalla: tuple
    pista: Pistas

    def __init__(self, alto: int, ancho: int, dimensiones: tuple, tablero: list[list[Boton]], valores: np.ndarray[bool]) -> None:
        self.alto = alto
        self.ancho = ancho
        self.dimensiones_pantalla = dimensiones
        self.pistas = Pistas(tablero = tablero, valores = valores, dificultad = 2);
        # Creacion del boton en pygame
        self.boton_visual = pygame.Rect(
            dimensiones[0] - self.ancho - 20,
            # X: posición horizontal con espacio
            dimensiones[1] - self.alto - 20,
            # Y: posición vertical con espacio
            self.ancho,  # Ancho del botón
            self.alto  # Alto del botón
        )

   # def get_click(self):
