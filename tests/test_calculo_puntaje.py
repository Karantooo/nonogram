import pytest
from nonogram.logica.calculo_puntaje import calculador_puntaje
from datetime import timedelta

def test_puntaje_max_d3():
    #test para puntaje maximo en dificultad 3
    tiempo = timedelta(seconds= 0)
    dificultad = 3
    vidas = 3
    calculador = calculador_puntaje(int(tiempo.total_seconds()), vidas, dificultad)
    puntaje  = calculador.calcular()
    assert puntaje == 14000

def test_puntaje_max_d2():
    # test para puntaje maximo en dificultad 2
    tiempo = timedelta(seconds=0)
    dificultad = 2
    vidas = 3
    calculador = calculador_puntaje(int(tiempo.total_seconds()), vidas, dificultad)
    puntaje = calculador.calcular()
    assert puntaje == 12000

def test_puntaje_max_d1():
    #test para puntaje maximo en dificultad 1
    tiempo = timedelta(seconds= 0)
    dificultad = 1
    vidas = 3
    calculador = calculador_puntaje(int(tiempo.total_seconds()), vidas, dificultad)
    puntaje  = calculador.calcular()
    assert puntaje == 11000

def test_puntaje_0v_d3():
    #testea que el puntaje sea 0 si las vidas son 0 en cualquier tiempo
    tiempo = timedelta(seconds= 60)
    dificultad = 3
    vidas = 0
    calculador = calculador_puntaje(int(tiempo.total_seconds()), vidas, dificultad)
    puntaje  = calculador.calcular()
    assert puntaje == 0

def test_puntaje_0v_d2():
    #testea que el puntaje sea 0 si las vidas son 0 en cualquier tiempo
    tiempo = timedelta(seconds= 160)
    dificultad = 2
    vidas = 0
    calculador = calculador_puntaje(int(tiempo.total_seconds()), vidas, dificultad)
    puntaje  = calculador.calcular()
    assert puntaje == 0

def test_puntaje_0v_d1():
    #testea que el puntaje sea 0 si las vidas son 0 en cualquier tiempo
    tiempo = timedelta(seconds= 60)
    dificultad = 1
    vidas = 0
    calculador = calculador_puntaje(int(tiempo.total_seconds()), vidas, dificultad)
    puntaje  = calculador.calcular()
    assert puntaje == 0

def test_puntaje_0t_d3():
    #testea que el puntaje sea 0 si el tiempo es mayor a 10 min
    tiempo = timedelta(seconds= 600)
    dificultad = 3
    vidas = 2
    calculador = calculador_puntaje(int(tiempo.total_seconds()), vidas, dificultad)
    puntaje  = calculador.calcular()
    assert puntaje == 0

def test_puntaje_0t_d2():
    #testea que el puntaje sea 0 si el tiempo es mayor a 7 min
    tiempo = timedelta(seconds= 420)
    dificultad = 2
    vidas = 2
    calculador = calculador_puntaje(int(tiempo.total_seconds()), vidas, dificultad)
    puntaje  = calculador.calcular()
    assert puntaje == 0

def test_puntaje_0t_d1():
    #testea que el puntaje sea 0 si el tiempo es mayor a 5 min
    tiempo = timedelta(seconds= 300)
    dificultad = 1
    vidas = 2
    calculador = calculador_puntaje(int(tiempo.total_seconds()), vidas, dificultad)
    puntaje  = calculador.calcular()
    assert puntaje == 0

def test_puntaje_d3_r1():
    #testea que el puntaje el adecuado para ciertos valores randoms en la dificultad 3
    tiempo = timedelta(seconds= 500)
    dificultad = 3
    vidas = 3
    calculador = calculador_puntaje(int(tiempo.total_seconds()), vidas, dificultad)
    puntaje  = calculador.calcular()
    assert puntaje == 2500

def test_puntaje_d3_r2():
    #testea que el puntaje el adecuado para ciertos valores randoms en la dificultad 3
    tiempo = timedelta(seconds= 360)
    dificultad = 3
    vidas = 2
    calculador = calculador_puntaje(int(tiempo.total_seconds()), vidas, dificultad)
    puntaje  = calculador.calcular()
    assert puntaje == 4800

def test_puntaje_d3_r3():
    #testea que el puntaje el adecuado para ciertos valores randoms en la dificultad 3
    tiempo = timedelta(seconds= 120)
    dificultad = 3
    vidas = 1
    calculador = calculador_puntaje(int(tiempo.total_seconds()), vidas, dificultad)
    puntaje  = calculador.calcular()
    assert puntaje == 8080

def test_puntaje_d2_r1():
    #testea que el puntaje el adecuado para ciertos valores randoms en la dificultad 2
    tiempo = timedelta(seconds= 250)
    dificultad = 2
    vidas = 3
    calculador = calculador_puntaje(int(tiempo.total_seconds()), vidas, dificultad)
    puntaje  = calculador.calcular()
    assert puntaje == 5000

def test_puntaje_d2_r2():
    #testea que el puntaje el adecuado para ciertos valores randoms en la dificultad 2
    tiempo = timedelta(seconds= 400)
    dificultad = 2
    vidas = 2
    calculador = calculador_puntaje(int(tiempo.total_seconds()), vidas, dificultad)
    puntaje  = calculador.calcular()
    assert puntaje == 800

def test_puntaje_d2_r3():
    #testea que el puntaje el adecuado para ciertos valores randoms en la dificultad 2
    tiempo = timedelta(seconds= 300)
    dificultad = 2
    vidas = 1
    calculador = calculador_puntaje(int(tiempo.total_seconds()), vidas, dificultad)
    puntaje  = calculador.calcular()
    assert puntaje == 2300

def test_puntaje_d1_r1():
    #testea que el puntaje el adecuado para ciertos valores randoms en la dificultad 1
    tiempo = timedelta(seconds= 150)
    dificultad = 1
    vidas = 3
    calculador = calculador_puntaje(int(tiempo.total_seconds()), vidas, dificultad)
    puntaje  = calculador.calcular()
    assert puntaje == 5600

def test_puntaje_d1_r2():
    #testea que el puntaje el adecuado para ciertos valores randoms en la dificultad 1
    tiempo = timedelta(seconds= 100)
    dificultad = 1
    vidas = 2
    calculador = calculador_puntaje(int(tiempo.total_seconds()), vidas, dificultad)
    puntaje  = calculador.calcular()
    assert puntaje == 6000

def test_puntaje_d1_r3():
    #testea que el puntaje el adecuado para ciertos valores randoms en la dificultad 1
    tiempo = timedelta(seconds= 250)
    dificultad = 1
    vidas = 1
    calculador = calculador_puntaje(int(tiempo.total_seconds()), vidas, dificultad)
    puntaje  = calculador.calcular()
    assert puntaje == 1250