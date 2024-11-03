import numpy as np
import pygame
from nonogram.visual.boton import Boton
from nonogram.logica.pistas import Pistas


class BotonPista:
    alto: int
    ancho: int
    dimensiones_pantalla: tuple
    pistas: Pistas

    def __init__(self, alto: int, ancho: int, dimensiones: tuple, tablero: list[list[Boton]], valores: np.ndarray[bool], cant_botones :int ) -> None:
        self.alto = alto
        self.ancho = ancho
        self.dimensiones_pantalla = dimensiones
        self.pistas = Pistas(tablero = tablero, valores = valores, dificultad = 2, num_botones = cant_botones)


        # Creacion del boton en pygame

        self.boton_visual = pygame.Rect(
            10,
            # X: posición horizontal con espacio
            10,
            # Y: posición vertical con espacio
            self.ancho,  # Ancho del botón
            self.alto  # Alto del botón
        )

    def accionar_pistas(self):
        return self.pistas.get_pista()

