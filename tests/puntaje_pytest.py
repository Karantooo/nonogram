import pytest
from nonogram.calculo_puntaje import calculador_puntaje
from datetime import timedelta

def test_puntaje_1():
    #prueba q el calculo del puntaje sea correcto(ttd)
    tiempo = timedelta(seconds= 45)
    dificultad = 2
    vidas = 3
    calculador = calculador_puntaje(int(tiempo.total_seconds()), vidas, dificultad)
    puntaje  = calculador.calcular()
    assert puntaje == 9700

def test_puntaje_2():
    #prueba q el calculo del puntaje sea correcto(ttd)
    tiempo = timedelta(seconds= 60)
    dificultad = 1
    vidas = 1
    calculador = calculador_puntaje(tiempo.total_seconds(), vidas, dificultad)
    puntaje  = calculador.calcular()
    assert puntaje == 3600

def test_puntaje_3():
    #prueba q el calculo del puntaje sea correcto(ttd)
    tiempo = timedelta(seconds= 300)
    dificultad = 1
    vidas = 0
    calculador = calculador_puntaje(int(tiempo.total_seconds()), vidas, dificultad)
    puntaje  = calculador.calcular()
    assert puntaje == 0

