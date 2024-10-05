class NoExisteMatrizError(Exception):
    def __init__(self, mensaje: str = "No existe una matriz generada"):
        super().__init__(mensaje)


class ImagenError(Exception):
    def __init__(self, mensaje:str = "No se a podido abrir la imagen"):
        super().__init__(mensaje)