import pygame
import math
import random
from PIL import Image
from PIL.ImageFile import ImageFile

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



class AnimacionExplosion:
    frames: list[pygame.Surface]
    frame_index: int
    gif_size: tuple[int,int]


    def __init__(self):
        gif = Image.open("assets/EXPLOSION.gif")
        self.frames = []
        for frame in range(gif.n_frames):
            gif.seek(frame)
            frame_image = gif.convert("RGBA")  # Convierte a RGBA para Pygame
            pygame_image = pygame.image.fromstring(frame_image.tobytes(), frame_image.size, frame_image.mode)
            self.frames.append(pygame_image)

        self.frame_index = 0
        self.gif_size = gif.size


    def imprimir(self, screen: pygame.Surface, posicion: tuple[int, int]) -> None:
        posicion_impresion = [posicion[0] - self.gif_size[0] / 2, posicion[1] - self.gif_size[1] / 2]
        screen.blit(self.frames[self.frame_index], posicion_impresion)
        pygame.display.flip()

        self.frame_index = (self.frame_index + 1) % len(self.frames)


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
