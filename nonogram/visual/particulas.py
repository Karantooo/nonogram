import pygame
import random

from nonogram.visual.colores import Colores


class Particula:
    posicion_actual: list[float]
    radio: float
    radio_minimo = 8
    radio_maximo = 15
    dispercion_maxima = 20

    # Mientras mas alta la taza_de_reduccion_del_radio mas se demora en desaparecer la particula,
    # esto genera una cola como de cometa en la animacion
    taza_de_reduccion_del_radio = 16

    """
    Representa una partícula en una animación, que disminuye de tamaño con el tiempo simulando una estela o cola.
    """

    def __init__(self, posicion_actual: list[float]) -> None:
        self.posicion_actual = posicion_actual
        self.radio = random.randint(self.radio_minimo, self.radio_maximo)


    def imprimir(self, screen: pygame.Surface) -> None:
        """
        Renderiza la partícula en la pantalla con un color aleatorio entre rojo y amarillo,
        y una posición desplazada aleatoriamente para simular dispersión.

        Args:
            screen (pygame.Surface): Superficie en la que se renderizará la partícula.
        """

        color = random.choice([Colores.ROJO, Colores.AMARILLO])
        posicion_impresion_x = self.posicion_actual[0] + random.randint(self.dispercion_maxima * -1, self.dispercion_maxima)
        posicion_impresion_y = self.posicion_actual[1] + random.randint(self.dispercion_maxima * -1, self.dispercion_maxima)
        pygame.draw.circle(screen, color, [posicion_impresion_x,posicion_impresion_y], self.radio)


    def tick_de_vida(self, velocidad: float) -> bool:
        """
        Reduce el radio de la partícula según la velocidad proporcionada y verifica si debe desaparecer.

        Args:
            velocidad (float): Factor que determina la rapidez de reducción del radio;
                               valores más altos aceleran la desaparición de la partícula.

        Returns:
            True si la partícula sigue visible; False si su radio es cero o menor,
                  indicando que debe desaparecer.
        """

        self.radio -= velocidad / self.taza_de_reduccion_del_radio
        if self.radio <= 0:
            return False
        return True


    def set_radio_minimo(self, cambio: int) -> None:
        self.radio_minimo = cambio


    def set_radio_maximo(self, cambio: int) -> None:
        self.radio_maximo = cambio


    def set_dispercion_maxima(self, cambio: int) -> None:
        self.dispercion_maxima = cambio


    def set_taza_de_reduccion_del_radio(self, cambio: float) -> None:
        self.taza_de_reduccion_del_radio = cambio
