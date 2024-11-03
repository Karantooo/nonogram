class SinPistasError(Exception):
    def __init__(self, mensaje : str = "Ya no tienes mas pistas disponibles") -> None:
        super().__init__(mensaje)