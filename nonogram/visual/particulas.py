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


    def __init__(self, posicion_actual: list[float]):
        self.posicion_actual = posicion_actual
        self.radio = random.randint(self.radio_minimo, self.radio_maximo)


    def imprimir(self, screen: pygame.Surface):
        color = random.choice([Colores.ROJO,Colores.AMARILLO])
        posicion_impresion_x = self.posicion_actual[0] + random.randint(self.dispercion_maxima * -1, self.dispercion_maxima)
        posicion_impresion_y = self.posicion_actual[1] + random.randint(self.dispercion_maxima * -1, self.dispercion_maxima)
        pygame.draw.circle(screen, color, [posicion_impresion_x,posicion_impresion_y], self.radio)


    def tick_de_vida(self, velocidad: float) -> bool:
        self.radio -= velocidad / self.taza_de_reduccion_del_radio
        if self.radio <= 0:
            return False
        return True


    def set_radio_minimo(self, cambio: int):
        self.radio_minimo = cambio


    def set_radio_maximo(self, cambio: int):
        self.radio_maximo = cambio


    def set_dispercion_maxima(self, cambio: int):
        self.dispercion_maxima = cambio


    def set_taza_de_reduccion_del_radio(self, cambio: float):
        self.taza_de_reduccion_del_radio = cambio
