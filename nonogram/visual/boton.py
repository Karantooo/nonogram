import pygame
from nonogram.visual.colores import Colores

class Boton:
    """
    Esta clase representa un botón en el tablero del juego.
    """

    fila: int                   # Fila en la que se encuentra el botón
    columna: int                # Columna en la que se encuentra el botón
    alto: int                   # Altura del botón
    ancho: int                  # Anchura del botón
    espacio: int                # Espacio entre botones
    marcado: bool               # Estado del botón (marcado o no)
    identificador: int          # Identificador único del botón
    visibilidad: bool           # Estado de visibilidad del botón
    fuente: pygame.font.Font    # Fuente utilizada para renderizar texto
    boton_visual: pygame.Rect   # Rectángulo que define la posición y tamaño del botón
    dimensiones: tuple          # Dimensiones de la ventana

    def __init__(self, fila: int, columna: int, alto: int, ancho: int, espacio: int ,marcado: bool, identificador: int, fuente: pygame.font, dimensiones: tuple=(1000, 700)) -> None:
        self.alto = alto
        self.ancho = ancho
        self.espacio = espacio
        self.dimensiones = dimensiones

        # Creacion del boton en pygame
        self.boton_visual = pygame.Rect(
                int(self.dimensiones[0] * 0.3) + columna * (self.ancho + self.espacio),  # X: posición horizontal con espacio
                int(self.dimensiones[1] * 0.28) + fila * (self.alto + self.espacio),  # Y: posición vertical con espacio
                self.ancho,  # Ancho del botón
                self.alto  # Alto del botón
        )

        self.identificador = identificador
        self.marcado = marcado
        self.visibilidad = False
        self.fuente = fuente

    def get_marcado(self) -> bool:
        return self.marcado

    def get_visibilidad(self) -> bool:
        return self.visibilidad

    def imprimir(self, screen: pygame.Surface) -> None:
        if self.visibilidad:
            if self.marcado:
                pygame.draw.rect(screen, Colores.NEGRO, self.boton_visual)
            else:
                pygame.draw.rect(screen, Colores.ROJO, self.boton_visual)
        else:
            pygame.draw.rect(screen, Colores.BLANCO, self.boton_visual)

        pygame.draw.rect(screen, Colores.NEGRO, self.boton_visual, 2)  # Borde negro del botón

        # Renderizar el texto como "fila, columna"
        #texto = self.fuente.render(f'{self.identificador}', True, Colores.NEGRO)
        #texto_rect = texto.get_rect(center=self.boton_visual.center)

        # Dibujar el texto en el centro del botón
        #screen.blit(texto, texto_rect)

    def validar_click(self,mouse_pos: tuple[int,int]) -> int: # 0: Incorrecto, 1: Correcto, 2: No se marco este
        if self.boton_visual.collidepoint(mouse_pos) and self.visibilidad == False:
            self.visibilidad = True
            if self.marcado:
                return 1
            else:
                return 0
        return 2