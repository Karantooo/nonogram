import pytest
from nonogram import ImageToMatrix
import numpy as np

class TestImageToMatrix:
    def setup_method(self):
        pass

    def test_creation_matrix_2x2(self):
        imagen_matrix = ImageToMatrix(r"../assets/2X2.png")
        imagen_matrix.generate_image()
        expected = np.zeros((2, 2))
        expected[1,1] = expected[1, 0] = 1
        generated = imagen_matrix.show_matrix()
        assert np.array_equal(expected, generated)
