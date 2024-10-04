'''
This class is created with the objective of transforming an image into an image made up with ascii characters instead of
pixels.
'''
import cv2
import numpy as np
import math


class ImageToMatrix:

    def __init__(self, image_path: str, columns: int, thresh_hold: float = 0.5):
        self.image_path = image_path
        self.columns = columns
        self.thresh_hold = thresh_hold
        self.original_height = None
        self.original_width = None
        self.matrix = None
        self.image = None
        self.re_generate_image()

    # This function takes an image and resize it to a new format
    # This has to be do to make the image on the correct size so a terminal can show the ascii image with no problem
    # the image is just an opencv image, the default rescaling means a 1//rescaling

    def __resize_image__(self, image: np.ndarray, columns: int = 10):

        # Si las columnas son invalidas se settea las columnas al tamanio original
        columns = columns if (columns <= self.original_width or columns <= 0) else self.original_width

        # calculo de las nuevas dimensiones
        new_height = round(self.original_height * (columns / self.original_width))
        new_width = columns
        resolution = (int(new_width), int(new_height))

        return cv2.resize(image, resolution, interpolation=cv2.INTER_AREA)

        # This function handles the main focus of this class that is the translation of the image into ascii
        # It takes 1 single opencv image and it return an string with the frame already translate it

    def __image_to_matrix__(self) -> np.ndarray:
        img_gray_resized = self.__resize_image__(self.image, self.columns)
        shape_img = img_gray_resized.shape[:2]
        matrix = np.zeros(shape_img, dtype=bool)

        for i in range(shape_img[0]):
            for j in range(shape_img[1]):
                matrix[i, j] = (img_gray_resized[i, j] <= self.thresh_hold * 255)

        return matrix

    #  function tries to generate the ascii image using the path on the constructor
    # If the program couldn't find the image it will return false
    def re_generate_image(self) -> bool:
        """
        Genera la matriz de bool con la que se representa el nonogram
        Returns:
            bool: Devuelve si la ejecucion de la funcion fue exitosa con True o False
        """
        self.image = cv2.imread(self.image_path, cv2.IMREAD_GRAYSCALE)

        if self.image is None:
            print("WARNING!!!\nCouldn't find the image to transform, please verify the path of the image.")
            return False

        self.original_height = self.image.shape[0]
        self.original_width = self.image.shape[1]
        self.matrix = self.__image_to_matrix__()  # Obtiene una matriz de opencv que sera el nonogram

        return True

    def show_matrix(self):

        if self.matrix is None:
            pass

        else:
            return self.matrix
