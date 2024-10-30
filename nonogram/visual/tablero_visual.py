import pickle
from nonogram.logica.tablero import Tablero
from nonogram.visual.boton import Boton
import numpy as np
import pygame

from nonogram.visual.boton_pista import BotonPista
from nonogram.visual.colores import Colores
from nonogram.logica.casilla import Casilla
from nonogram.logica.sistema_guardado import SistemaGuardado
from nonogram.logica.Excepciones.mouse_fuera_del_tablero import MouseFueraDelTablero


class TableroVisual:
    numero_botones: int         # Cantidad de botones en el tablero
    fuente: pygame.font.Font    # Fuente para el texto
    ancho_boton: int            # Ancho de los botones
    alto_boton: int             # Alto de los botones
    espacio: int                # Espacio entre los botones
    botones: list[list[Boton]]  # Matriz de botones
    numeros_superiores: list[list[int]]     # Números en la parte superior
    numeros_laterales: list[list[int]]      # Números en los laterales
    valores: np.ndarray[bool]
    tablero_logica: Tablero
    dimensiones: tuple
    tiempo_transcurrido: tuple   # Indica el tiempo transcurrido del juego
    tamaño_fuente: int
    pistas = 3


    def __calculo_num_superiores(self) -> list[list[int]]:
        valores = []

        for j in range(self.numero_botones):
            auxiliar = []
            contador = 0

    def __init__(
            self,
            numero_botones: int = 4,
            imagen: np.ndarray[bool] = None,
            dimensiones: tuple = (1000, 700),
            guardado_previo: SistemaGuardado = None
    ) -> None:
        self.numero_botones = numero_botones
        self.tamaño_fuente = int(54 - ((5/4) * self.numero_botones))
        self.tiempo_transcurrido = (0,0)
        self.fuente = pygame.font.SysFont('Arial', self.tamaño_fuente)
        self.dimensiones = dimensiones

        # Tamaño de los botones, hacer resize
        self.ancho_boton = int((self.dimensiones[0] * 0.6) // self.numero_botones)
        self.alto_boton = int((self.dimensiones[1] * 0.6) // self.numero_botones)
        self.espacio = 0

        # Crear una matriz nxn de None
        self.botones = [[None for _ in range(self.numero_botones)] for _ in range(self.numero_botones)]
        self.valores = imagen if imagen is not None else np.random.choice([True, False], size=self.numero_botones ** 2)

        contador = 0
        for fila in range(self.numero_botones):
            for columna in range(self.numero_botones):
                casilla_especifica = None if guardado_previo is None else guardado_previo.casillas[fila][columna]

                marcado = self.valores[fila * self.numero_botones + columna].item()
                self.botones[fila][columna] = Boton(fila=fila, columna=columna,
                                                    alto=self.alto_boton, ancho=self.ancho_boton,
                                                    espacio=self.espacio, marcado=marcado,
                                                    identificador=contador, fuente=self.fuente,
                                                    dimensiones=self.dimensiones, casilla=casilla_especifica)

                contador += 1
        self.boton_pista = BotonPista(ancho = self.ancho_boton, alto =self.alto_boton, dimensiones = self.dimensiones, tablero = self.botones, valores = self.valores)
        self.numeros_superiores = self.__calculo_num_superiores()
        self.numeros_laterales = self.__calculo_num_laterales()

        marcados = 0
        for i in range(self.numero_botones**2):
            if self.valores[i]:
                marcados += 1

        vidas = 3 if guardado_previo is None else guardado_previo.vidas_restantes

        self.tablero_logica = Tablero(marcados=marcados, vidas=vidas)

    def imprimir(self, screen: pygame.Surface) -> None:
        for array_botones in self.botones:
            for botones in array_botones:
                botones.imprimir(screen)

        # Imprimir los numeros superiores
        for i, valores in enumerate(self.numeros_superiores):
            for j, valor in enumerate(valores[::-1]):
                texto = self.fuente.render(str(valor), True, Colores.NEGRO)
                texto_rect = texto.get_rect(center=(int((self.dimensiones[0] * 0.2) + self.ancho_boton * 0.5)  + i * (self.ancho_boton + self.espacio), int(self.dimensiones[1]*0.15) - j * self.tamaño_fuente))
                screen.blit(texto, texto_rect)

        # Imprimir los numeros laterales
        for i, valores in enumerate(self.numeros_laterales):
            for j, valor in enumerate(valores[::-1]):
                texto = self.fuente.render(str(valor), True, Colores.NEGRO)
                texto_rect = texto.get_rect(center=(int((self.dimensiones[0] * 0.17)) - j * int(self.tamaño_fuente * 6/5), int(self.dimensiones[1]*0.2 + self.alto_boton *0.5) + i * (self.alto_boton + self.espacio)))
                screen.blit(texto, texto_rect)

        # Dibujar el contador de vidas en la esquina superior derecha
        texto_vidas = self.fuente.render(f'Vidas: {self.tablero_logica.get_vidas()}', True, Colores.NEGRO)
        screen.blit(texto_vidas, (screen.get_width() - texto_vidas.get_width() - 20, 20))

        # Temporizador
        self.tiempo_ejecucion()
        fuente_temporizador = pygame.font.SysFont('Arial', 39)
        texto_temporizador = fuente_temporizador.render(f'Tiempo: {self.tiempo_transcurrido[0]*60 + self.tiempo_transcurrido[1]} segundos', True, Colores.NEGRO)
        screen.blit(texto_temporizador, (self.dimensiones[0] * 0.4, self.dimensiones[1] * 0.9))

        #contador de pistas
        texto_pistas = self.fuente.render(f'Pistas: {self.pistas}', True, Colores.NEGRO)
        screen.blit(texto_pistas, (screen.get_width() - texto_pistas.get_width() - 20, 40))
        #boton pistas
        pygame.draw.rect(screen, Colores.VERDE, self.boton_pista.boton_visual)


    def validar_click(self,mouse_pos: tuple[int,int]) -> None:
        try:
            array_pos = self.__mouse_posicion_to_indices_array(mouse_pos)
            self.tablero_logica.validar_click(mouse_pos, self.botones, array_pos)
        except MouseFueraDelTablero:
            pass

    def marcar_bandera(self,mouse_pos: tuple[int,int]) -> None:
        try:
            array_pos = self.__mouse_posicion_to_indices_array(mouse_pos)
            self.botones[array_pos[1]][array_pos[0]].alterar_estado_bandera()
        except MouseFueraDelTablero:
            pass

    def get_vidas(self) -> int:
        return self.tablero_logica.get_vidas()

    def __mouse_posicion_to_indices_array(self, mouse_pos: tuple[int, int]) -> tuple[int, int]:
        fuera_de_limites = lambda x, dim: x < int(dim * 0.2) or x >= int(dim - int(dim * 0.2))

        # Verificar si la posición del mouse está fuera de los márgenes
        if fuera_de_limites(mouse_pos[0], self.dimensiones[0]) or fuera_de_limites(mouse_pos[1], self.dimensiones[1]):
            #print("Fuera de los limites")
            raise MouseFueraDelTablero

        # Calcular la posición en el array
        array_pos = (mouse_pos[0] - int(self.dimensiones[0] * 0.2), mouse_pos[1] - int(self.dimensiones[1] * 0.2))
        array_pos = (array_pos[0] // self.ancho_boton, array_pos[1] // self.alto_boton)

        return array_pos

    def get_vistos(self) -> int:
        return self.tablero_logica.get_vistos()

    def ganado(self) -> bool:
        return self.tablero_logica.ganado()

    # Metodo para
    def tiempo_ejecucion(self):
        tiempo = pygame.time.get_ticks() // 1000                     # Tiempo de ejecucion en segundos

        self.tiempo_transcurrido = (tiempo // 60, tiempo % 60)       # Tupla con los segundos y minutos
    def guardar_estado(self, ruta: str = r"game_data.bin"):
        guardado = self.__obetener_datos_partida__()
        with open(ruta, "wb") as archivo:
            pickle.dump(guardado, archivo)

    @staticmethod
    def cargar_estado(ruta: str = r"game_data.bin") -> SistemaGuardado:
        with open(ruta, "rb") as archivo:
            casillas = pickle.load(archivo)
        return casillas

    def __obetener_datos_partida__(self):
        casillas = []
        for columna_boton in self.botones:
            columna_casillas = []
            for boton in columna_boton:
                columna_casillas.append(boton.casilla)

            casillas.append(columna_casillas)

        guardado = SistemaGuardado(casillas=casillas, vidas_restantes=self.get_vidas(), tiempo=0)
        return guardado

    def __calculo_num_superiores(self) -> list[list[int]]:
        valores = []

        for j in range(self.numero_botones):
            auxiliar = []
            contador = 0

            for i in range(self.numero_botones):
                if self.botones[i][j].get_marcado():
                    contador += 1
                else:
                    if contador > 0:
                        auxiliar.append(contador)
                        contador = 0

            if contador > 0:
                auxiliar.append(contador)

            valores.append(auxiliar)

        return valores

    def __calculo_num_laterales(self) -> list[list[int]]:
        valores = []

        for i in range(self.numero_botones):
            auxiliar = []
            contador = 0

            for j in range(self.numero_botones):
                if self.botones[i][j].get_marcado():
                    contador += 1
                else:
                    if contador > 0:
                        auxiliar.append(contador)
                        contador = 0

            if contador > 0:
                auxiliar.append(contador)

            valores.append(auxiliar)

        return valores
