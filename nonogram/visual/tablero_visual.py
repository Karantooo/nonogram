import pickle

from PIL.ImageChops import screen

from nonogram.logica.tablero import Tablero
from nonogram.visual.Menus import MenuAjustes
from nonogram.visual.boton import Boton
import numpy as np
import pygame
import pygame_menu

from nonogram.visual.boton_pista import BotonPista
from nonogram.visual.colores import Colores
from nonogram.logica.calculo_puntaje import CalculadorPuntaje
from nonogram.logica.casilla import Casilla
from nonogram.logica.sistema_guardado import SistemaGuardado
from nonogram.logica.Excepciones.mouse_fuera_del_tablero import MouseFueraDelTablero
from nonogram.visual.animacion_particulas import AnimacionParticulas
from nonogram.visual.conversor import Conversor
from nonogram.visual.Menus import MenuInicio


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
    pistas: int = 3
    menu_inicio : MenuInicio
    menu_ajustes: MenuAjustes
    animacion_particulas: AnimacionParticulas
    origen_particulas: list[int]
    screen: pygame.display
    clickeado: bool
    dificultad : int


    def __init__(
            self,
            numero_botones: int = 4,
            imagen: np.ndarray[bool] = None,
            dimensiones: tuple = (1000, 700),
            guardado_previo: SistemaGuardado = None,
            menu_inicial : MenuInicio = None,
            screen: pygame.display = None
    ) -> None:
        self.numero_botones = numero_botones if guardado_previo is None else len(guardado_previo.casillas)
        self.tamaño_fuente = int(54 - ((5/4) * self.numero_botones))
        self.tiempo_transcurrido = 0
        self.fuente = pygame.font.SysFont('Arial', self.tamaño_fuente)
        self.dimensiones = dimensiones
        self.menu_inicio = menu_inicial
        self.tiempo_inicio = pygame.time.get_ticks() // 1000
        self.screen = screen

        # Tamaño de los botones, hacer resize
        self.ancho_boton = int((self.dimensiones[0] * 0.6) // self.numero_botones)
        self.alto_boton = int((self.dimensiones[1] * 0.6) // self.numero_botones)
        self.espacio = 0

        #cantidad de pistas
        if self.numero_botones <= 8 :
            self.pistas = 3
            self.dificultad = 1
        elif self.numero_botones <= 15:
            self.pistas = 4
            self.dificultad = 2
        else:
            self.pistas = 5
            self.dificultad = 3

        if guardado_previo is not None:
            self.pistas = guardado_previo.pistas

        # Crear una matriz nxn de None
        self.botones = [[None for _ in range(self.numero_botones)] for _ in range(self.numero_botones)]
        if guardado_previo is not None:
            self.valores = np.zeros((len(guardado_previo.casillas) * len(guardado_previo.casillas[0])), dtype=bool)
            identificador = 0
            for i in range(len(guardado_previo.casillas)):
                for j in range(len(guardado_previo.casillas[0])):
                    self.valores[identificador] = guardado_previo.casillas[i][j].marcado
                    identificador += 1
        else:
            if imagen is not None:
                self.valores = np.ndarray(self.numero_botones*self.numero_botones, dtype=bool)
                indice = 0
                for i in range(len(imagen)):
                    for j in range(len(imagen[i])):
                        self.valores[indice] = imagen[i][j]
                        indice += 1
            else:
                self.valores = np.random.choice([True, False], size=self.numero_botones ** 2)
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
        self.boton_ajustes_juego = BotonPista(ancho = self.ancho_boton, alto =self.alto_boton, dimensiones = self.dimensiones, tablero = self.botones, valores = self.valores, cant_botones = self.numero_botones)
        self.boton_pistas = BotonPista(ancho = self.ancho_boton, alto = self.alto_boton, dimensiones = self.dimensiones, tablero = self.botones, valores = self.valores, cant_botones = self.numero_botones)
        self.numeros_superiores = self.__calculo_num_superiores()
        self.numeros_laterales = self.__calculo_num_laterales()


        self.menu_ajustes = MenuAjustes(self.screen, self.menu_inicio, self)

        marcados = 0
        for i in range(self.numero_botones**2):
            if self.valores[i]:
                marcados += 1

        vidas = 3 if guardado_previo is None else guardado_previo.vidas_restantes
        self.tiempo_transcurrido = 0 if guardado_previo is None else guardado_previo.tiempo
        self.tiempo_inicial = pygame.time.get_ticks() // 1000
        self.tiempo_inicial -= self.tiempo_transcurrido

        vistos = 0 if guardado_previo is None else guardado_previo.vistos
        correctos = 0 if guardado_previo is None else guardado_previo.casillas_correctas

        self.tablero_logica = Tablero(marcados=marcados, vidas=vidas, vistos= vistos, correctos=correctos)


        self.animacion_particulas = None
        self.origen_particulas = [int(dimensiones[0] * 0.964), int(dimensiones[1] * 0.207)]
        self.screen = screen
        self.clickeado = False


    def imprimir(self, screen: pygame.Surface):
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

        #puntuación
        fuente_puntuacion = pygame.font.SysFont('Arial', 39)
        self.calculador = CalculadorPuntaje(vidas=self.get_vidas(), tiempo=self.tiempo_transcurrido, dificultad=self.dificultad)
        texto_puntuacion = fuente_puntuacion.render(f'Puntuación actual: {self.calculador.calcular()} puntos', True,Colores.NEGRO)
        screen.blit(texto_puntuacion, (self.dimensiones[0] * 0.4, self.dimensiones[1] * 0.8))

        #contador de pistas
        texto_pistas = self.fuente.render(f'Pistas: {self.pistas}', True, Colores.NEGRO)
        screen.blit(texto_pistas, (screen.get_width() - texto_pistas.get_width() - 20, 20 + texto_vidas.get_height() + 10))

        tamanio_botones_juego = (70, 70)

        #Exportar imagen
        imagen_boton_ajustes_juego = pygame.image.load("assets/engranaje.png")
        imagen_boton_ajustes_juego = pygame.transform.scale(imagen_boton_ajustes_juego, tamanio_botones_juego)

        #Dar imagen a el boton uwu
        self.boton_ajustes_juego.boton_visual = imagen_boton_ajustes_juego.get_rect(topleft=(20,20))
        screen.blit(imagen_boton_ajustes_juego, self.boton_ajustes_juego.boton_visual.topleft)

        #Copiamos imagen
        imagen_boton_pistas = pygame.image.load("assets/bombilla.png")
        imagen_boton_pistas = pygame.transform.scale(imagen_boton_pistas, tamanio_botones_juego)

        # Dar imagen a el boton uwu


        pygame.draw.circle(screen, (33, 33, 33), (200 , 50), 41)
        pygame.draw.circle(screen, (0, 0, 0), (200 , 50), 50, 10)

        self.boton_pistas.boton_visual = imagen_boton_pistas.get_rect(topleft=(165, 15))
        screen.blit(imagen_boton_pistas, self.boton_pistas.boton_visual.topleft)

        text_salida_juego = pygame.font.SysFont('Arial', 30).render("Para salir, presione 'Q' o 'Escape'", True,
                                                                    (0, 0, 0))
        screen.blit(text_salida_juego, (20, self.dimensiones[1] * 0.9))

        text_bombilla = pygame.font.SysFont('Arial', 30).render("Presione la bombilla para las pistas", True,
                                                                (0, 0, 0))
        screen.blit(text_bombilla, (20, self.dimensiones[1] * 0.94))

        if self.pistas == 0:
            sin_vidas_texto = self.fuente.render("No te quedan mas pistas", True, (0, 0, 0))
            screen.blit(sin_vidas_texto,( self.dimensiones[0] * 0.2, self.dimensiones[1] * 0.8))

    def validar_click(self,mouse_pos: tuple[int,int]) -> None:
        try:
            if self.boton_ajustes_juego.boton_visual.collidepoint(mouse_pos):
                self.menu_ajustes.activar_menu_ajustes()
                self.menu_ajustes.mostrar_menu_ajustes()
            elif self.boton_pistas.boton_visual.collidepoint(mouse_pos) and not self.clickeado:
                self.clickeado = True
                if self.pistas > 0:
                    self.pistas -= 1
                    indices_solucion = self.boton_pistas.accionar_pistas()

                    if indices_solucion is not None:
                        self.tablero_logica.correctos += 1
                        self.tablero_logica.vistos += 1
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
                if array_pos[0] >= len(self.botones) or array_pos[1] >= len(self.botones):
                    raise MouseFueraDelTablero
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
        self.clickeado = False


    # Metodo para
    def tiempo_ejecucion(self):                   # Tiempo de ejecucion en segundos
        tiempo = (pygame.time.get_ticks() // 1000) - self.tiempo_inicial                     # Tiempo de ejecucion en segundos
        self.tiempo_transcurrido = tiempo       # Tupla con los segundos y minutos


    def guardar_estado(self, ruta: str = r"nonogram/partidas_guardadas/partidaG.bin"):
        guardado = self.__obtener_datos_partida__()
        with open(ruta, "wb") as archivo:
            pickle.dump(guardado, archivo)


    def __obtener_datos_partida__(self) -> SistemaGuardado:
        casillas = []
        for columna_boton in self.botones:
            columna_casillas = []
            for boton in columna_boton:
                columna_casillas.append(boton.casilla)

            casillas.append(columna_casillas)

        guardado = SistemaGuardado(
            casillas = casillas,
            vidas_restantes = self.get_vidas(),
            tiempo = self.tiempo_transcurrido,
            casillas_correctas = self.tablero_logica.correctos,
            vistos= self.tablero_logica.vistos,
            pistas= self.pistas
        )
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
        array_pos = (int(array_pos[0] // self.ancho_boton), int(array_pos[1] // self.alto_boton))

        return array_pos

def volver_menu_inicio(self):
    self.menu_inicio.enable()
    self.menu_ajustes.disable()
    self.corriendo = False
