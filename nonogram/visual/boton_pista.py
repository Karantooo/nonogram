import pygame
import nonogram.logica.pistas
from nonogram.logica.pistas import Pistas


class BotonPista:

    alto: int
    ancho: int
    pista: Pistas

    def __init__(self, int, alto: int, ancho: int, espacio: int,) -> None:
        self.alto = alto
        self.ancho = ancho
        self.espacio = espacio

        # Creacion del boton en pygame
        self.boton_visual = pygame.Rect(
            int(self.dimensiones[0] * 0.2) + columna * (self.ancho + self.espacio),
            # X: posición horizontal con espacio
            int(self.dimensiones[1] * 0.2) + fila * (self.alto + self.espacio),  # Y: posición vertical con espacio
            self.ancho,  # Ancho del botón
            self.alto  # Alto del botón
        )