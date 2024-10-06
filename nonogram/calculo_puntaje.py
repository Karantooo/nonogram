import time
from datetime import timedelta

class calculador_puntaje:
    """
    Esta clase se encarga de calcular el puntaje basado en el tiempo, las vidas y la dificultad del juego.
    """

    vidas: int  # Cantidad de vidas restantes
    dificultad: int  # Nivel de dificultad (1, 2, 3)
    tiempo: int  # Tiempo transcurrido en segundos

    def __init__(self,tiempo: int, vidas: int, dificultad: int):
        self.vidas = vidas
        self.dificultad = dificultad
        self.tiempo = tiempo

    def calcular(self):

        #El calculo del puntaje está basado en una función simple que depende de los tres atributos de esta clase
        #puede ser que despues se cambie pero por ahora funcionará así
        #La dificultad del nivel le sumara puntos a una base de 10000,
        #y por cada vida perdida se le descontara cierta cantidad, luego de ese total se le
        #restara un 10% por cada 15 seg que se demore en completar el nivel

        if(self.vidas == 0):
            return 0
        else:
            total = 10000

            if self.dificultad == 1:
                total += 1000  # Si dificultad es 1, suma 1000
            elif self.dificultad == 2:
                total += 2000  # Si dificultad es 2, suma 2000
            elif self.dificultad == 3:
                total += 4000  # Si dificultad es 3, suma 4000
            if self.vidas == 2:
                total -= 3000
            elif self.vidas == 1:
                total -= 5000

            if self.tiempo >= 300:
                return total*0.3

            perdida = self.tiempo//15
            perdida = ((total/10)*perdida)

            return total - perdida