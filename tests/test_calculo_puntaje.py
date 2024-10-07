import pytest
from nonogram import calculador_puntaje
from datetime import timedelta

def test_puntaje_1():
    #prueba q el calculo del puntaje sea correcto(ttd)
    tiempo = timedelta(seconds= 45)
    dificultad = 2
    vidas = 3
    calculador = calculador_puntaje(int(tiempo.total_seconds()), vidas, dificultad)
    puntaje  = calculador.calcular()
    assert puntaje == 8400

def test_puntaje_2():
    tiempo = timedelta(seconds= 60)
    dificultad = 1
    vidas = 1
    calculador = calculador_puntaje(int(tiempo.total_seconds()), vidas, dificultad)
    puntaje  = calculador.calcular()
    assert puntaje == 3600

def test_puntaje_3():
    tiempo = timedelta(seconds= 90)
    dificultad = 1
    vidas = 0
    calculador = calculador_puntaje(int(tiempo.total_seconds()), vidas, dificultad)
    puntaje  = calculador.calcular()
    assert puntaje == 0

def test_puntaje_4():
    #test para verificar q el puntaje sea el 30% del maximo acumulado, si se demora demasiado en resolver el problema
    tiempo = timedelta(seconds= 300)
    dificultad = 3
    vidas = 2
    calculador = calculador_puntaje(int(tiempo.total_seconds()), vidas, dificultad)
    puntaje = calculador.calcular()
    assert puntaje == 3300