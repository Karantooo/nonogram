
class CalculadorPuntaje:
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

        total = 10000
        if(self.vidas == 0):
            return 0

        if(self.dificultad == 3):
            if(self.tiempo >= 600):
                return 0
            total += 4000
            if(self.vidas == 3):
                total -= self.tiempo * 23
            elif(self.vidas == 2):
                total -= 2000
                total -= self.tiempo * 20
            elif(self.vidas == 1):
                total -= 4000
                total -= self.tiempo * 16

        elif (self.dificultad == 2):
            if(self.tiempo >= 420):
                return 0
            total += 2000
            if(self.vidas == 3):
                total -= self.tiempo * 28
            elif (self.vidas == 2):
                total -= 2000
                total -= self.tiempo * 23
            elif (self.vidas == 1):
                total -= 4000
                total -= self.tiempo * 19

        elif (self.dificultad == 1):
            if(self.tiempo >= 300):
                return 0
            total += 1000
            if (self.vidas == 3):
                total -= self.tiempo * 36
            elif (self.vidas == 2):
                total -= 2000
                total -= self.tiempo * 30
            elif (self.vidas == 1):
                total -= 4000
                total -= self.tiempo * 23

        return total