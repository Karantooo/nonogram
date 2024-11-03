import pickle

from PIL.ImageChops import screen

from nonogram.logica.tablero import Tablero
from nonogram.visual.boton import Boton
import numpy as np
import pygame
import pygame_menu

from nonogram.visual.boton_pista import BotonPista
from nonogram.visual.colores import Colores
from nonogram.logica.casilla import Casilla
from nonogram.logica.sistema_guardado import SistemaGuardado
from nonogram.logica.Excepciones.mouse_fuera_del_tablero import MouseFueraDelTablero
from nonogram.visual.animacion_particulas import AnimacionParticulas
from nonogram.visual.conversor import Conversor

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
    dimensiones: tuple[float,float]
    tiempo_transcurrido: int   # Indica el tiempo transcurrido del juego
    tamaño_fuente: int
    pistas = 3
    menu_inicio : pygame_menu.Menu
    menu_ajustes: pygame_menu.Menu
    animacion_particulas: AnimacionParticulas
    origen_particulas: list[int]
    screen: pygame.display



    def __init__(
            self,
            numero_botones: int = 4,
            imagen: np.ndarray[bool] = None,
            dimensiones: tuple = (1000, 700),
            guardado_previo: SistemaGuardado = None,
            menu_inicial : pygame_menu.Menu = None,
            screen: pygame.display = None
    ) -> None:
        self.numero_botones = numero_botones
        self.tamaño_fuente = int(54 - ((5/4) * self.numero_botones))
        self.tiempo_transcurrido = 0
        self.fuente = pygame.font.SysFont('Arial', self.tamaño_fuente)
        self.dimensiones = dimensiones
        self.menu_inicio = menu_inicial
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
        self.boton_ajustes_juego = BotonPista(ancho = self.ancho_boton, alto =self.alto_boton, dimensiones = self.dimensiones, tablero = self.botones, valores = self.valores, cant_botones = numero_botones)
        self.boton_pistas = BotonPista(ancho = self.ancho_boton, alto = self.alto_boton, dimensiones = self.dimensiones, tablero = self.botones, valores = self.valores, cant_botones = numero_botones)
        self.numeros_superiores = self.__calculo_num_superiores()
        self.numeros_laterales = self.__calculo_num_laterales()

        marcados = 0
        for i in range(self.numero_botones**2):
            if self.valores[i]:
                marcados += 1

        vidas = 3 if guardado_previo is None else guardado_previo.vidas_restantes
        self.tiempo_transcurrido = 0 if guardado_previo is None else guardado_previo.tiempo

        self.tablero_logica = Tablero(marcados=marcados, vidas=vidas)

        self.menu_ajustes = pygame_menu.Menu("Ajustes", 500, 400, theme=pygame_menu.themes.THEME_BLUE)
        self.menu_ajustes.add.button("Pista", None)
        self.menu_ajustes.add.button("Inicio", volver_menu_inicio)
        self.menu_ajustes.disable()

        self.animacion_particulas = None
        self.origen_particulas = [int(dimensiones[0] * 0.964), int(dimensiones[1] * 0.207)]
        self.screen = screen


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
        texto_temporizador = fuente_temporizador.render(f'Tiempo: {self.tiempo_transcurrido} segundos', True, Colores.NEGRO)
        screen.blit(texto_temporizador, (self.dimensiones[0] * 0.4, self.dimensiones[1] * 0.9))

        #contador de pistas
        texto_pistas = self.fuente.render(f'Pistas: {self.pistas}', True, Colores.NEGRO)
        screen.blit(texto_pistas, (screen.get_width() - texto_pistas.get_width() - 20, 20 + texto_vidas.get_height() + 10))

        # Exportar imagen
        imagen_boton_ajustes_juego = pygame.image.load("assets/engranaje.png")
        imagen_boton_ajustes_juego = pygame.transform.scale(imagen_boton_ajustes_juego, (self.ancho_boton, self.alto_boton))

        # Dar imagen a el boton uwu
        self.boton_ajustes_juego.boton_visual = imagen_boton_ajustes_juego.get_rect(topleft=(20,20))
        screen.blit(imagen_boton_ajustes_juego, self.boton_ajustes_juego.boton_visual.topleft)

        #Copiamos imagen
        imagen_boton_pistas = pygame.image.load("assets/bombilla.png")
        imagen_boton_pistas = pygame.transform.scale(imagen_boton_pistas, (self.ancho_boton, self.alto_boton))

        # Dar imagen a el boton uwu
        self.boton_pistas.boton_visual = imagen_boton_pistas.get_rect(topleft=(50 + self.alto_boton, 20))
        screen.blit(imagen_boton_pistas, self.boton_pistas.boton_visual.topleft)

        if self.pistas == 0:
            sin_vidas_texto = self.fuente.render("No te quedan mas pistas", True, (0, 0, 0))
            screen.blit(sin_vidas_texto,( self.dimensiones[0] * 0.2, self.dimensiones[1] * 0.8))

    def validar_click(self,mouse_pos: tuple[int,int]) -> None:
        try:
            if self.boton_ajustes_juego.boton_visual.collidepoint(mouse_pos):
                print("Boton")
                self.menu_ajustes.enable()
            elif self.boton_pistas.boton_visual.collidepoint(mouse_pos):
                if self.pistas > 0:
                    self.pistas -= 1
                    indices_solucion = self.boton_pistas.accionar_pistas()

                    if indices_solucion is not None:
                        indices_solucion_invertido = (indices_solucion[1],indices_solucion[0])
                        coordenadas = Conversor.conversor_matriz_botones_to_coordenadas_pantalla(
                            indices_solucion_invertido,
                            self.dimensiones,
                            (self.ancho_boton,self.alto_boton)
                        )

                        self.animacion_particulas = AnimacionParticulas(
                            origen_particulas=self.origen_particulas[:],
                            objetivo=coordenadas,
                            indice_objetivo=indices_solucion,
                            screen=self.screen,
                            tablero_botones=self.botones
                        )

            else:
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


    def get_vistos(self) -> int:
        return self.tablero_logica.get_vistos()


    def ganado(self) -> bool:
        return self.tablero_logica.ganado()


    def get_ancho_boton(self) -> int:
        return self.ancho_boton


    def get_alto_boton(self) -> int:
        return self.alto_boton

    def get_animacion_particulas(self):
        return self.animacion_particulas

    def set_animacion_particulas(self):
        self.animacion_particulas = None


    # Metodo para
    def tiempo_ejecucion(self):
        tiempo = pygame.time.get_ticks() // 1000                     # Tiempo de ejecucion en segundos
        self.tiempo_transcurrido = tiempo       # Tupla con los segundos y minutos


    def guardar_estado(self, ruta: str = r"game_data.bin"):
        guardado = self.__obtener_datos_partida__()
        with open(ruta, "wb") as archivo:
            pickle.dump(guardado, archivo)


    @staticmethod
    def cargar_estado(ruta: str = r"game_data.bin") -> SistemaGuardado:
        with open(ruta, "rb") as archivo:
            casillas = pickle.load(archivo)
        return casillas


    def __obtener_datos_partida__(self):
        casillas = []
        for columna_boton in self.botones:
            columna_casillas = []
            for boton in columna_boton:
                columna_casillas.append(boton.casilla)

            casillas.append(columna_casillas)

        guardado = SistemaGuardado(casillas=casillas, vidas_restantes=self.get_vidas(), tiempo=self.tiempo_transcurrido)
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

def volver_menu_inicio(self):
    self.menu_inicio.enable()
    self.menu_ajustes.disable()
    self.corriendo = False
