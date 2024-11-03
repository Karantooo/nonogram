from os import remove

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
    numero_botones : int

    def __init__(self, tablero : list[list[Boton]], valores : np.ndarray[bool], dificultad :int, num_botones : int):
        self.tablero_botones = tablero
        self.reales = valores
        self.numero_botones = num_botones
        if dificultad == 1:
            self.pistas = 2
        if dificultad == 2:
            self.pistas = 3
        if dificultad == 3:
            self.pistas = 5


    def encontrar_los_reales(self):
        positivos =  []

        # Recorremos cada valor en `self.reales` y su índice
        for index, valor in enumerate(self.reales):
            if valor:  # Solo consideramos los valores que son True
                # Calculamos la fila y columna a partir del índice
                fila = index // self.numero_botones
                columna = index % self.numero_botones
                positivos.append([fila, columna])  # Agregamos la posición a la lista
        print(positivos)
        return positivos

    def get_pista(self):
        lista_posible_soluiciones = self.encontrar_los_reales()
        print(f"lsita = {lista_posible_soluiciones}")
        # Elegir una posición aleatoria de la lista de posibles soluciones
        posicion_solucionar = lista_posible_soluiciones[random.randint(0, len(lista_posible_soluiciones) - 1)]

        # Verificar visibilidad del botón en la posición seleccionada
        if not self.tablero_botones[posicion_solucionar[0]][posicion_solucionar[1]].get_visibilidad():
            # Si no está visible, marcar la casilla y reducir las pistas
            print(posicion_solucionar)
            self.tablero_botones[posicion_solucionar[0]][posicion_solucionar[1]].casilla.visibilidad = True
            self.pistas -= 1
            print(1)
            return  # Salir después de marcar una casilla válida

        # Eliminar la posición ya revisada de la lista de posibles soluciones
        lista_posible_soluiciones.remove(posicion_solucionar)
        print(f"lsita2 : {lista_posible_soluiciones}")