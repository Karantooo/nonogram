class ImagenError(Exception):
    def __init__(self, mensaje:str = "No se a podido abrir la imagen"):
        super().__init__(mensaje)