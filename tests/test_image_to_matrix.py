import pytest
from nonogram import ImageToMatrix, NoExisteMatrizError, ImagenError
import numpy as np


class TestImageToMatrix:
    def setup_method(self):
        pass

    def test_creation_matrix_3x3_black(self):
        imagen_matrix = ImageToMatrix(r"../assets/3X3_black_and_white.png", 3)
        expected = np.zeros((3, 3), dtype=bool)
        expected[2, 1] = expected[2, 2] = True
        expected[1, 1] = True

        generated = imagen_matrix.show_matrix()
        assert np.array_equal(expected, generated)


    def test_creation_matrix_2x2(self):
        imagen_matrix = ImageToMatrix(r"../assets/2X2.png", 2)
        expected = np.zeros((2, 2), dtype=bool)
        expected[0, 1] = expected[0, 0] = True
        generated = imagen_matrix.show_matrix()
        assert np.array_equal(expected, generated)

    def test_creation_matrix_3x2(self):
        imagen_matrix = ImageToMatrix(r"../assets/3X2.png", 3, thresh_hold=0.6)
        expected = np.zeros((3, 2), dtype=bool)
        expected[1,1] = expected[1, 0] = True
        generated = imagen_matrix.show_matrix()
        assert np.array_equal(expected, generated)

    def test_creation_matrix_3x4(self):
        imagen_matrix = ImageToMatrix(r"../assets/3X4.png", 3)
        expected = np.zeros((4, 3), dtype=bool)
        expected[1, 0] = expected[0, 0] = True
        expected[0, 2] = expected[1, 2] = True
        expected[3, 1] = True
        generated = imagen_matrix.show_matrix()
        assert np.array_equal(expected, generated)

    def test_no_hay_matriz(self):
        with pytest.raises(NoExisteMatrizError):
            matriz = ImageToMatrix(r"../assets/megumin.jpeg", 3)
            matriz.matrix = None
            matriz.show_matrix()

    def test_imagen_invalida(self):
        with pytest.raises(ImagenError):
            matriz = ImageToMatrix(r"fake_path", columns=2)

