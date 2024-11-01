import pygame
import math

from nonogram.visual.animacion_explosion import AnimacionExplosion
from nonogram.visual.particulas import Particula


class AnimacionParticulas:
    origen_particulas: list[float]  # Indica donde se generan las particulas
    objetivo: tuple[int,int]
    screen: pygame.Surface
    particulas: list[Particula]
    tiempo_espera_inicio: int  # Tiempo que se espera a que termine el audio de Megumin antes de mover las particulas
    tiempo_espera_final: int    # Tiempo que espera a que termine el audio del final
    llego: bool     # Controla si se llego o no al objetivo
    animacion_explosion: AnimacionExplosion

    cantidad_particulas_generadas_por_iteracion = 3
    distancia_aceptacion_llegada_al_objetivo = 50


    def __init__(self, origen_particulas, objetivo, screen):
        self.origen_particulas = origen_particulas
        self.objetivo = objetivo
        self.screen = screen
        self.particulas = []

        sonido_megumin_dice_explosion = pygame.mixer.Sound("assets/sonidos/megumin_dice_explosion.wav")
        sonido_megumin_dice_explosion.set_volume(1)
        sonido_megumin_dice_explosion.play()

        self.tiempo_espera_inicio = int(sonido_megumin_dice_explosion.get_length()) * 9
        self.tiempo_espera_final = 10
        self.llego = False

        self.animacion_explosion = AnimacionExplosion()


    def animacion(self, velocidad_animacion: float):
        for i in range(self.cantidad_particulas_generadas_por_iteracion):
            self.__crear_particula()
        self.__imprimir()

        if self.tiempo_espera_inicio > 0:
            self.tiempo_espera_inicio -= 1
        else:
            self.__mover_origen_particulas(velocidad_animacion)

        self.__vida_particulas(velocidad_animacion)


    def validar_llegada(self) -> bool:
        if self.llego:
            if self.tiempo_espera_final > 0:
                self.tiempo_espera_final -= 1
                self.animacion_explosion.imprimir(self.screen, self.objetivo)
                return False
            else:
                return True
        distancia_x = abs(self.origen_particulas[0] - self.objetivo[0])
        distancia_y = abs(self.origen_particulas[1] - self.objetivo[1])

        if (
                distancia_x < self.distancia_aceptacion_llegada_al_objetivo and
                distancia_y < self.distancia_aceptacion_llegada_al_objetivo
        ):
            sonido_explosion = pygame.mixer.Sound("assets/sonidos/sonido_explosion.wav")
            sonido_explosion.set_volume(1)
            sonido_explosion.play()
            self.llego = True

        return False


    def set_cantidad_particulas_generadas_por_iteracion(self, cambio: int) -> None:
        self.cantidad_particulas_generadas_por_iteracion = cambio

    def set_distancia_aceptacion_llegada_al_objetivo(self, cambio: int) -> None:
        self.distancia_aceptacion_llegada_al_objetivo = cambio


    def __mover_origen_particulas(self, desplazamiento: float) -> None:
        resta_al_cuadrado = lambda indice: (self.objetivo[indice] - self.origen_particulas[indice]) ** 2
        distancia_al_objetivo = math.sqrt(resta_al_cuadrado(0) + resta_al_cuadrado(1))

        vector_al_objetivo = lambda indice: self.objetivo[indice] - self.origen_particulas[indice]
        vector_unitario_al_objetivo_x = vector_al_objetivo(0) / distancia_al_objetivo
        vector_unitario_al_objetivo_y = vector_al_objetivo(1) / distancia_al_objetivo

        self.origen_particulas[0] += vector_unitario_al_objetivo_x * desplazamiento
        self.origen_particulas[1] += vector_unitario_al_objetivo_y * desplazamiento


    def __crear_particula(self) -> None:
        self.particulas.append(Particula(self.origen_particulas[:]))


    def __vida_particulas(self, velocidad: float) -> None:
        for particula in self.particulas:
            if not particula.tick_de_vida(velocidad):
                self.particulas.remove(particula)


    def __imprimir(self) -> None:
        for particula in self.particulas:
            particula.imprimir(self.screen)
