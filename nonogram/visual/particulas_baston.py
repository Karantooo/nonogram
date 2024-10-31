import pygame
import math
import random

from nonogram.visual.colores import Colores

class Particula:
    posicion_actual: list[float]
    radio: float

    def __init__(self, posicion_actual: list[float]):
        self.posicion_actual = posicion_actual
        self.radio = random.randint(6, 20)


    def imprimir(self, screen: pygame.Surface):
        color = random.choice([Colores.ROJO,Colores.AMARILLO])
        posicion_impresion_x = self.posicion_actual[0] + random.randint(-20, 20)
        posicion_impresion_y = self.posicion_actual[1] + random.randint(-20, 20)
        pygame.draw.circle(screen, color, [posicion_impresion_x,posicion_impresion_y], self.radio)

    def tick_de_vida(self, velocidad: float) -> bool:
        self.radio -= velocidad / 16
        if self.radio <= 0:
            return False
        return True


class AnimacionParticulas:
    origen_particulas: list[float]  # Indica donde se generan las particulas
    objetivo: tuple[int,int]
    screen: pygame.Surface
    particulas: list[Particula]
    tiempo_espera: int  # Tiempo que se espera a que termine el audio de Megumin antes de mover las particulas
    llego: bool     # Controla si se llego o no

    def __init__(self, origen_particulas, objetivo, screen):
        self.origen_particulas = origen_particulas
        self.objetivo = objetivo
        self.screen = screen
        self.particulas = []

        sonido_megumin_dice_explosion = pygame.mixer.Sound("assets/sonidos/megumin_dice_explosion.wav")
        sonido_megumin_dice_explosion.set_volume(1)
        sonido_megumin_dice_explosion.play()

        self.tiempo_espera = int(sonido_megumin_dice_explosion.get_length()) * 9
        self.llego = False

    def imprimir(self) -> None:
        for particula in self.particulas:
            particula.imprimir(self.screen)

    def mover_origen_particulas(self, desplazamiento: float) -> None:
        resta_al_cuadrado = lambda indice: (self.objetivo[indice] - self.origen_particulas[indice]) ** 2
        distancia_al_objetivo = math.sqrt(resta_al_cuadrado(0) + resta_al_cuadrado(1))

        vector_al_objetivo = lambda indice: self.objetivo[indice] - self.origen_particulas[indice]
        vector_unitario_al_objetivo_x = vector_al_objetivo(0) / distancia_al_objetivo
        vector_unitario_al_objetivo_y = vector_al_objetivo(1) / distancia_al_objetivo

        self.origen_particulas[0] += vector_unitario_al_objetivo_x * desplazamiento
        self.origen_particulas[1] += vector_unitario_al_objetivo_y * desplazamiento


    def crear_particula(self) -> None:
        self.particulas.append(Particula(self.origen_particulas[:]))

    def vida_particulas(self, velocidad: float) -> None:
        for particula in self.particulas:
            if not particula.tick_de_vida(velocidad):
                self.particulas.remove(particula)

    def animacion(self, velocidad_animacion: float):
        self.crear_particula()
        self.imprimir()

        if self.tiempo_espera > 0:
            self.tiempo_espera -= 1
        else:
            self.mover_origen_particulas(velocidad_animacion)

        self.vida_particulas(velocidad_animacion)

    def validar_llegada(self):
        if self.llego:
            return True
        distancia_x = abs(self.origen_particulas[0] - self.objetivo[0])
        distancia_y = abs(self.origen_particulas[1] - self.objetivo[1])

        if distancia_x < 50 and distancia_y < 50:
            sonido_explosion = pygame.mixer.Sound("assets/sonidos/sonido_explosion.wav")
            sonido_explosion.set_volume(1)
            sonido_explosion.play()
            self.llego = True
            return True

        return False