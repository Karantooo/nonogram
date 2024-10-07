class NoExisteMatrizError(Exception):
    def __init__(self, mensaje: str = "No existe una matriz generada") -> None:
        super().__init__(mensaje)


class ImagenError(Exception):
    def __init__(self, mensaje:str = "No se a podido abrir la imagen") -> None:
        super().__init__(mensaje)