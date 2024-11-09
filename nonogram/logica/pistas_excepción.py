class SinPistasError(Exception):
    def __init__(self, mensaje : str = "Ya no tienes mas pistas disponibles"):
        super().__init__(mensaje)