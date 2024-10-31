import pygame
import math
import random

from nonogram.visual.colores import Colores

class Particula:
    posicion_actual: list[int]
    radio: int

    def __init__(self, posicion_actual: list[int]):
        self.posicion_actual = posicion_actual
        self.radio = random.randint(6, 11)


    def imprimir(self, screen: pygame.Surface):
        pygame.draw.circle(screen, Colores.ROJO, self.posicion_actual, self.radio)


class AnimacionParticulas:
    origen_particulas: list[int]  # Indica donde se generan las particulas
    objetivo: tuple[int,int]
    screen: pygame.Surface
    particulas: list[Particula]

    def __init__(self, origen_particulas, objetivo, screen):
        self.origen_particulas = origen_particulas
        self.objetivo = objetivo
        self.screen = screen
        self.particulas = []

    def imprimir(self) -> None:
        for particula in self.particulas:
            particula.imprimir(self.screen)

    def mover_origen_particulas(self, desplazamiento: int) -> None:
        resta_al_cuadrado = lambda indice: (self.objetivo[indice] - self.origen_particulas[indice]) ** 2
        distancia_al_objetivo = math.sqrt(resta_al_cuadrado(0) + resta_al_cuadrado(1))

        vector_al_objetivo = lambda indice: self.objetivo[indice] - self.origen_particulas[indice]
        vector_unitario_al_objetivo_x = vector_al_objetivo(0) / distancia_al_objetivo
        vector_unitario_al_objetivo_y = vector_al_objetivo(1) / distancia_al_objetivo

        self.origen_particulas[0] += vector_unitario_al_objetivo_x * desplazamiento
        self.origen_particulas[1] += vector_unitario_al_objetivo_y * desplazamiento

    def crear_particula(self) -> None:
        self.particulas.append(Particula(self.origen_particulas[:]))

    def animacion(self, velocidad_animacion: int):
        self.crear_particula()
        self.imprimir()
        self.mover_origen_particulas(velocidad_animacion)