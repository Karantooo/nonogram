from nonogram.logica.tablero import Tablero
from nonogram.visual.boton import Boton
import numpy as np
import pygame
from nonogram.visual.colores import Colores

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
    pistas = 3


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

    def __init__(self, numero_botones: int = 4, imagen: np.ndarray[bool] = None, dimensiones: tuple=(1000,700)) -> None:
        self.numero_botones = numero_botones
        self.fuente = pygame.font.SysFont('Arial', 24)
        self.dimensiones = dimensiones
        # Tamaño de los botones, hacer resize
        self.ancho_boton = int((self.dimensiones[0] * 0.6) // self.numero_botones)
        self.alto_boton =  int((self.dimensiones[1] * 0.6) // self.numero_botones)
        self.espacio = 0

        # Crear una matriz nxn de None
        self.botones = [[None for _ in range(self.numero_botones)] for _ in range(self.numero_botones)]
        self.valores = imagen if imagen is not None else np.random.choice([True, False], size=self.numero_botones ** 2)

        contador = 0
        for fila in range(self.numero_botones):
            for columna in range(self.numero_botones):
                marcado = self.valores[fila * self.numero_botones + columna].item()
                self.botones[fila][columna] = Boton(fila=fila, columna=columna,
                                                    alto=self.alto_boton, ancho=self.ancho_boton,
                                                    espacio=self.espacio, marcado=marcado,
                                                    identificador=contador, fuente=self.fuente,
                                                    dimensiones=self.dimensiones)
                contador += 1

        self.numeros_superiores = self.__calculo_num_superiores()
        self.numeros_laterales = self.__calculo_num_laterales()

        marcados = 0
        for i in range(self.numero_botones**2):
            if self.valores[i]:
                marcados += 1

        self.tablero_logica = Tablero(marcados=marcados)

    def imprimir(self, screen: pygame.Surface) -> None:
        for array_botones in self.botones:
            for botones in array_botones:
                botones.imprimir(screen)

        # Imprimir los numeros superiores
        for i, valores in enumerate(self.numeros_superiores):
            for j, valor in enumerate(valores[::-1]):
                texto = self.fuente.render(str(valor), True, Colores.NEGRO)
                texto_rect = texto.get_rect(center=(int((self.dimensiones[0] * 0.2) + self.ancho_boton * 0.5)  + i * (self.ancho_boton + self.espacio), int(self.dimensiones[1]*0.17) - j * 24))
                screen.blit(texto, texto_rect)

        # Imprimir los numeros laterales
        for i, valores in enumerate(self.numeros_laterales):
            for j, valor in enumerate(valores[::-1]):
                texto = self.fuente.render(str(valor), True, Colores.NEGRO)
                texto_rect = texto.get_rect(center=(int((self.dimensiones[0] * 0.17)) - j * 20, int(self.dimensiones[1]*0.2 + self.alto_boton *0.5) + i * (self.alto_boton + self.espacio)))
                screen.blit(texto, texto_rect)

        # Dibujar el contador de vidas en la esquina superior derecha
        texto_vidas = self.fuente.render(f'Vidas: {self.tablero_logica.get_vidas()}', True, Colores.NEGRO)
        screen.blit(texto_vidas, (screen.get_width() - texto_vidas.get_width() - 20, 20))

        texto_pistas = self.fuente.render(f'Pistas: {self.pistas}', True, Colores.NEGRO)
        screen.blit(texto_pistas, (screen.get_width() - texto_pistas.get_width() - 20, 40))

    def validar_click(self,mouse_pos: tuple[int,int]) -> None:
        if mouse_pos[0] < int((self.dimensiones[0] * 0.2)) or mouse_pos[1] < int((self.dimensiones[1] * 0.2)) or mouse_pos[0] >= int((self.dimensiones[0] - int((self.dimensiones[0] * 0.2)))) or mouse_pos[1] >= int((self.dimensiones[1] - int((self.dimensiones[1] * 0.2)))):
            # print("salio")
            return

        array_pos = (mouse_pos[0] - int(self.dimensiones[0] * 0.2), mouse_pos[1] - int(self.dimensiones[1] * 0.2))
        array_pos = (array_pos[0] // self.ancho_boton, array_pos[1] // self.alto_boton)

        self.tablero_logica.validar_click(mouse_pos, self.botones, array_pos)

    def get_vidas(self) -> int:
        return self.tablero_logica.get_vidas()

    def get_vistos(self) -> int:
        return self.tablero_logica.get_vistos()

    def ganado(self) -> bool:
        return self.tablero_logica.ganado()
