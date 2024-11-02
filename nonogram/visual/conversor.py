class Conversor:
    """
    Proporciona métodos estáticos para la conversión de índices de botones en una matriz
    a coordenadas de pantalla, facilitando el posicionamiento de elementos gráficos en la interfaz.
    """

    @staticmethod
    def conversor_matriz_botones_to_coordenadas_pantalla(
            indice_boton: tuple[int, int],
            dimencion_pantalla: tuple[float, float],
            dimencion_boton: tuple[float, float]
    ) -> tuple[float, float]:
        """
        Convierte un índice de botón en una matriz a coordenadas de pantalla en el centro dedl boton

        Args:
            indice_boton (tuple[int, int]): Indice en el tablero del boton al que se le quiere extrar las coordenadas de pantalla
            dimencion_pantalla (tuple[float, float]): Dimenciones de la pantalla en la que se muestra el boton
            dimencion_boton (tuple[float, float]): Dimenciones del boton

        Returns:
            tuple[float, float]: Coordenadas del centro del boton
        """

        conversor = lambda i, p, b: i * b + p * 0.2 + b / 2

        coordenada_x = conversor(indice_boton[0], dimencion_pantalla[0], dimencion_boton[0])
        coordenada_y = conversor(indice_boton[1], dimencion_pantalla[1], dimencion_boton[1])

        return coordenada_x, coordenada_y