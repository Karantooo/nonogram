import pytest
from nonogram.scripts_de_prueba import pruebaspygame
import numpy as np
from nonogram.scripts_de_prueba.pruebaspygame import get_num_arriba, get_num_lado


def test_num_sup_1():
    matriz = np.array([[1, 0, 1, 0, 1],
                       [0, 1, 0, 0, 1],
                       [0, 0, 1, 1, 0],
                       [1, 1, 1, 0, 1]])
    num_up = get_num_arriba(matriz)
    assert num_up == [[1, 1], [1, 1], [2, 1], [1], [1, 2]]

def test_num_sup_2():
    matriz = np.array([
        [1, 0, 1, 0, 1, 0, 1, 1, 0, 0],
        [0, 1, 0, 1, 0, 1, 0, 1, 1, 0],
        [1, 1, 0, 0, 1, 0, 1, 0, 1, 0],
        [0, 0, 1, 1, 0, 1, 0, 1, 0, 0],
        [1, 0, 1, 0, 1, 1, 0, 1, 1, 0],
        [0, 1, 0, 1, 0, 1, 1, 1, 1, 0],
        [1, 0, 1, 0, 1, 1, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1, 1, 0],
        [1, 1, 0, 0, 1, 1, 0, 0, 1, 0],
        [0, 0, 1, 1, 0, 0, 1, 1, 0, 0]
    ])

    num_up = get_num_arriba(matriz)
    assert num_up == [[1, 1, 1, 1, 1], [2, 1, 2], [1, 1, 2, 1],
                      [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [6, 1],
                      [1, 2, 1, 1], [1, 1, 3, 2], [5, 2],[]]

def test_num_lat_1():
    matriz = np.array([[1, 0, 1, 0, 1],
                       [0, 1, 0, 0, 1],
                       [0, 0, 1, 1, 0],
                       [1, 1, 1, 0, 1]])
    num_up = get_num_lado(matriz)
    assert num_up == [[1, 1, 1], [1, 1], [2], [1, 3]]

def test_num_lat_2():
    matriz = np.array([
        [1, 0, 1, 0, 1, 0, 1, 1, 0, 0],
        [0, 1, 0, 1, 0, 1, 0, 1, 1, 0],
        [1, 1, 0, 0, 1, 0, 1, 0, 1, 0],
        [0, 0, 1, 1, 0, 1, 0, 1, 0, 0],
        [1, 0, 1, 0, 1, 1, 0, 1, 1, 0],
        [0, 1, 0, 1, 0, 1, 1, 1, 1, 0],
        [1, 0, 1, 0, 1, 1, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1, 1, 0],
        [1, 1, 0, 0, 1, 1, 0, 0, 1, 0],
        [0, 0, 1, 1, 0, 0, 1, 1, 0, 0]
    ])

    num_up = get_num_lado(matriz)
    assert num_up == [[2, 1, 1, 1], [2, 1, 1, 1], [1, 1, 1, 2],
                      [1, 1, 2], [2, 2, 1, 1], [4, 1, 1],
                      [1, 3, 1, 1], [2, 1, 1, 1], [1, 2, 2], [2, 2]]
