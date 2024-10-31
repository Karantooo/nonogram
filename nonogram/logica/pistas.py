import numpy as np
import pygame
import random
from nonogram.logica.pistas_excepción import SinPistasError
from nonogram.visual.boton import Boton


class Pistas:
    tablero_botones: list[list[Boton]]
    reales : np.ndarray
    boton : pygame.Rect
    marcados : int
    pistas : int

    def __init__(self, tablero : list[list[Boton]], valores : np.ndarray[bool], dificultad :int):
        self.tablero_visual_info = tablero
        self.reales = valores
        if dificultad == 1:
            self.pistas = 2
        if dificultad == 2:
            self.pistas = 3
        if dificultad == 3:
            self.pistas = 5

    def encontrar_los_reales(self):
        positivos : list[list[int]]
        contrador_posicion = 0

        for i in self.reales:
            posicion_real = [0,0,0]
            if i:
                posicion_real[0] = contrador_posicion // self.tablero_visual_info.numero_botones
                posicion_real[1] = contrador_posicion % self.tablero_visual_info.numero_botones
                posicion_real[2] = 1
            contrador_posicion += 1
            if posicion_real[2] == 1:
                positivos.append(posicion_real)
        return positivos

    def get_pista(self):
        lista_posible_soluiciones = self.encontrar_los_reales()
        posicion_solucionar = random.randint(0, len(lista_posible_soluiciones) - 1)
        if self.pistas > 0:
            while self.tablero_botones[lista_posible_soluiciones[posicion_solucionar][0], lista_posible_soluiciones[posicion_solucionar][1]].visibilidad:
                lista_posible_soluiciones[posicion_solucionar].pop()
                posicion_solucionar = (posicion_solucionar + 1)%len(lista_posible_soluiciones)
            self.tablero_botones[lista_posible_soluiciones[posicion_solucionar][0], lista_posible_soluiciones[posicion_solucionar][1]].visibilidad = True

            self.pistas -= 1
        else:
            raise SinPistasError