import cv2
import numpy as np
import math
from .excepciones_imagenes import NoExisteMatrizError, ImagenError


class ImageToMatrix:
    image_path: str  # Ruta de la imagen
    columns: int  # Cantidad de columnas en la matriz
    thresh_hold: float  # Umbral para determinar color
    original_height: int  # Altura original de la imagen
    original_width: int  # Anchura original de la imagen
    matrix: np.ndarray  # Matriz de salida (bool)
    image: np.ndarray  # Imagen cargada en escala de grises

    """
    Esta clase contiene gestiona la transformacion de una imagen a una matriz de numpy de true o false
    El objetivo es utilizarla para generar mapas de nuestro nonogram
    """

    def __init__(self, image_path: str, columns: int, thresh_hold: float = 0.5) -> None:
        """
        Constructor de la clase que genera una matriz de bool encargandose de gestionar el tamanio de la misma
        Se indica un thresh_hold que vendria siendo el porcentaje de color en gray_scale desde el cual se considera
        blanco o negro.
        Args:
            image_path: path en el sistema de la imagen que se quiere procesar
            columns: columnas que tendra la matriz de bool generada
            thresh_hold:valor que se utiliza para determinar si un pixel es True o False (negro o blanco respectivamente)
        """
        self.image_path = image_path
        self.columns = columns
        self.thresh_hold = thresh_hold
        self.original_height = None
        self.original_width = None
        self.matrix = None
        self.image = None
        self.re_generate_matrix()

    def __resize_image__(self, image: np.ndarray, columns: int = 10) -> np.ndarray:
        """
        Funcion que toma una imagen y la cambia a una nueva resolucion
        Args:
            image (np.ndarray): imagen a transformar
            columns (int): cantidad de columnas o pixeles de anchura que tendra la imagen

        Returns:
            imagen con las nuevas dimensiones

        """

        # Si las columnas son invalidas se settea las columnas al tamanio original
        columns = columns if (columns <= self.original_width or columns <= 0) else self.original_width

        # calculo de las nuevas dimensiones
        new_height = round(self.original_height * (columns / self.original_width))
        new_width = columns
        resolution = (int(new_width), int(new_height))

        return cv2.resize(image, resolution, interpolation=cv2.INTER_AREA)

    def __image_to_matrix__(self) -> np.ndarray:
        """
        Metodo encargado de transformar la imagen a una matriz de bool
        Returns:
            Una matriz de numpy de bool

        """
        img_gray_resized = self.__resize_image__(self.image, self.columns)
        shape_img = img_gray_resized.shape[:2]
        matrix = np.zeros(shape_img, dtype=bool)

        for i in range(shape_img[0]):
            for j in range(shape_img[1]):
                matrix[i, j] = (img_gray_resized[i, j] <= self.thresh_hold * 255)

        return matrix

    def re_generate_matrix(self) -> bool:
        """
        Genera la matriz de bool con la que se representa el nonogram
        Returns:
            bool: Devuelve si la ejecucion de la funcion fue exitosa con True o False
        """
        self.image = cv2.imread(self.image_path, cv2.IMREAD_GRAYSCALE)

        if self.image is None:
            raise ImagenError

        self.original_height = self.image.shape[0]
        self.original_width = self.image.shape[1]
        self.matrix = self.__image_to_matrix__()  # Obtiene una matriz de opencv que sera el nonogram

        return True

    def show_matrix(self) -> np.ndarray:
        """
        Muestra la matriz de bool generada
        Returns:
            Muestra la matriz de bool
        Raises:
            NoExisteMatrizError: Si no hay una matriz de bool generada

        """
        if self.matrix is None:
            raise NoExisteMatrizError

        else:
            return self.matrix
