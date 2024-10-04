class NoExisteMatrizError(Exception):
    def __init__(self, mensaje: str = "No existe una matriz generada"):
        super().__init__(mensaje)