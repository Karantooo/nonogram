import pygame
import math

from nonogram.visual.animacion_explosion import AnimacionExplosion
from nonogram.visual.boton import Boton
from nonogram.visual.particulas import Particula


class AnimacionParticulas:
    origen_particulas: list[float]  # Indica donde se generan las particulas
    objetivo: tuple[int,int]
    indice_objetivo: tuple[int,int]
    screen: pygame.Surface
    particulas: list[Particula]
    tiempo_espera_inicio: int  # Tiempo que se espera a que termine el audio de Megumin antes de mover las particulas
    tiempo_espera_final: int    # Tiempo que espera a que termine el audio del final
    tiempo_espera_final_faltante: int    # Tiempo que falta a que termine el audio del final
    llego: bool     # Controla si se llego o no al objetivo
    animacion_explosion: AnimacionExplosion
    tablero_botones: list[list[Boton]]

    cantidad_particulas_generadas_por_iteracion = 3
    distancia_aceptacion_llegada_al_objetivo = 50

    """
    Controla la animación de partículas en movimiento hacia un objetivo con un efecto de explosión al llegar.
    """


    def __init__(self, origen_particulas, objetivo, indice_objetivo, screen, tablero_botones: list[list[Boton]]):
        self.origen_particulas = origen_particulas
        self.objetivo = objetivo
        self.indice_objetivo = indice_objetivo
        self.screen = screen
        self.tablero_botones = tablero_botones
        self.particulas = []

        # Inicializacion sonido
        sonido_megumin_dice_explosion = pygame.mixer.Sound("assets/sonidos/megumin_dice_explosion.wav")
        sonido_megumin_dice_explosion.set_volume(1)
        sonido_megumin_dice_explosion.play()

        self.tiempo_espera_inicio = int(sonido_megumin_dice_explosion.get_length()) * 9
        self.tiempo_espera_final = 10
        self.tiempo_espera_final_faltante = self.tiempo_espera_final
        self.llego = False

        self.animacion_explosion = AnimacionExplosion((tablero_botones[0][0].ancho,tablero_botones[0][0].alto))


    def animacion(self, velocidad_animacion: float) -> None:
        """
        Ejecuta la animacion, creando particulas, imprimiendolas, moviendo el origen de las particulas y
        controlando la vida de las particulas

        Args:
            velocidad_animacion (float): Controla el desplazamiento del origen de las particulas en esta iteracion
        """
        for i in range(self.cantidad_particulas_generadas_por_iteracion):
            self.__crear_particula()
        self.__imprimir()

        if self.tiempo_espera_inicio > 0:
            self.tiempo_espera_inicio -= 1
        else:
            self.__mover_origen_particulas(velocidad_animacion)

        self.__vida_particulas(velocidad_animacion)


    def validar_llegada(self) -> bool:
        """
        Valida si se llego a un rango aceptable de distancia con respecto al objetivo,
        si este es el caso, ejecuta una animacion de explocion

        Returns:
            True si se llego y se termino de ejecutar el sonido que acompana a la explosion
            False en caso contrario
        """
        if self.llego:
            if self.tiempo_espera_final_faltante > 0:
                self.tiempo_espera_final_faltante -= 1
                if self.tiempo_espera_final_faltante <= self.tiempo_espera_final / 2:
                    self.tablero_botones[self.indice_objetivo[0]][self.indice_objetivo[1]].casilla.visibilidad = True
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


    def set_cantidad_particulas_generadas_por_iteracion(self, cambio: int):
        self.cantidad_particulas_generadas_por_iteracion = cambio

    def set_distancia_aceptacion_llegada_al_objetivo(self, cambio: int):
        self.distancia_aceptacion_llegada_al_objetivo = cambio


    def __mover_origen_particulas(self, desplazamiento: float):
        """
        Mueve el origen de las partículas hacia el objetivo en cada ciclo de animación

        Args:
            desplazamiento (float): Indica cuantas unidades se va a desplazar el origen
        """
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
        """
        Ejecuta el ciclo de vida de las particulas, si estas ya no son capoces de existir las elimina

        Args:
            velocidad (float): Velocidad de desplazamiento del origen
        """
        for particula in self.particulas:
            if not particula.tick_de_vida(velocidad):
                self.particulas.remove(particula)

    def get_indice_objetivo(self):
        return self.indice_objetivo

    def __imprimir(self) -> None:
        for particula in self.particulas:
            particula.imprimir(self.screen)
