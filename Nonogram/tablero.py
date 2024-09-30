from boton import Boton
import numpy as np
import pygame

from colores import Colores


class Tablero:

    def __calculo_num_superiores(self) -> list[list[int]]:
        valores = []

        for j in range(4):
            auxiliar = []
            contador = 0

            for i in range(4):
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

        for i in range(4):
            auxiliar = []
            contador = 0

            for j in range(4):
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

    def __init__(self):
        self.fuente = pygame.font.SysFont('Arial', 24)

        # Tamaño de los botones
        self.ancho_boton = 100
        self.alto_boton = 100
        self.espacio = 0

        # Crear una matriz 4x4 de None
        self.botones = [[None for _ in range(4)] for _ in range(4)]
        valores = np.random.choice([True, False], size=16)

        contador = 0
        for fila in range(4):
            for columna in range(4):
                marcado = valores[fila * 4 + columna].item()
                self.botones[fila][columna] = Boton(fila=fila, columna=columna,
                alto=self.alto_boton, ancho=self.ancho_boton, espacio=self.espacio,
                marcado=marcado, identificador=contador, fuente=self.fuente)
                contador += 1

        self.numeros_superiores = self.__calculo_num_superiores()
        self.numeros_laterales = self.__calculo_num_laterales()


        self.marcados = 0
        for i in range(16):
            if valores[i] == True:
                self.marcados += 1

        self.vistos = 0
        self.correctos = 0
        self.vidas = 3

    def imprimir(self, screen: pygame.Surface):
        for array_botones in self.botones:
            for botones in array_botones:
                botones.imprimir(screen)

        # Imprimir los numeros superiores
        for i, valores in enumerate(self.numeros_superiores):
            for j, valor in enumerate(valores[::-1]):
                texto = self.fuente.render(str(valor), True, Colores.NEGRO)
                texto_rect = texto.get_rect(center=(350 + i * (self.ancho_boton + self.espacio), 150 - j * 30))
                screen.blit(texto, texto_rect)

        # Imprimir los numeros laterales
        for i, valores in enumerate(self.numeros_laterales):
            for j, valor in enumerate(valores[::-1]):
                texto = self.fuente.render(str(valor), True, Colores.NEGRO)
                texto_rect = texto.get_rect(center=(250 - j * 30, 225 + i * (self.alto_boton + self.espacio)))
                screen.blit(texto, texto_rect)

        # Dibujar el contador de vidas en la esquina superior derecha
        texto_vidas = self.fuente.render(f'Vidas: {self.vidas}', True, Colores.NEGRO)
        screen.blit(texto_vidas, (screen.get_width() - texto_vidas.get_width() - 20, 20))

    def validar_click(self,mouse_pos: tuple):
        for fila_botones in self.botones:
            for boton in fila_botones:
                correcto = boton.validar_click(mouse_pos)

                if correcto != 2:
                    self.vistos += 1
                if correcto == 0:
                    self.correctos += 1
                if correcto == 1:
                    self.vidas -= 1

    def get_vidas(self) -> int:
        return self.vidas

    def get_vistos(self) -> int:
        return self.vistos

    def ganado(self) -> bool:
        return self.correctos == self.marcados
