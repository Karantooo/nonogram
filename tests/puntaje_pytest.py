from nonogram import calculo_puntaje
from datetime import timedelta
def test_puntaje_1():
    #prueba q el calculo del puntaje sea correcto(ttd)
    tiempo = timedelta(seconds= 45)
    dificultad = 1
    vidas = 3
    calculador = calculo_puntaje(tiempo, vidas, dificultad)
    puntaje  = calculador.calcular(tiempo,dificultad,vidas)
    assert puntaje == 9000

def test_puntaje_1():
    #prueba q el calculo del puntaje sea correcto(ttd)
    tiempo = timedelta(seconds= 60)
    dificultad = 1
    vidas = 1
    calculador = calculo_puntaje(tiempo, vidas, dificultad)
    puntaje  = calculador.calcular(tiempo,dificultad,vidas)
    assert puntaje == 3600

def test_puntaje_1():
    #prueba q el calculo del puntaje sea correcto(ttd)
    tiempo = timedelta(seconds= 3)
    dificultad = 1
    vidas = 0
    calculador = calculo_puntaje(tiempo, vidas, dificultad)
    puntaje  = calculador.calcular(tiempo,dificultad,vidas)
    assert puntaje == 0

