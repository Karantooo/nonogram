import pygame
from colores import Colores


class Boton:

    def __init__(self, fila: int, columna: int, alto: int, ancho: int, espacio: int ,marcado: bool, identificador: int, fuente: pygame.font):
        self.alto = alto
        self.ancho = ancho
        self.espacio = espacio

        # Creacion del boton en pygame
        self.boton_visual = pygame.Rect(
            300 + columna * (self.ancho + self.espacio),  # X: posición horizontal con espacio
            200 + fila * (self.alto + self.espacio),  # Y: posición vertical con espacio
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

    def imprimir(self, screen: pygame.Surface):
        if self.visibilidad:
            if self.marcado:
                pygame.draw.rect(screen, Colores.VERDE, self.boton_visual)
            else:
                pygame.draw.rect(screen, Colores.ROJO, self.boton_visual)
        else:
            pygame.draw.rect(screen, Colores.AZUL, self.boton_visual)

        pygame.draw.rect(screen, Colores.NEGRO, self.boton_visual, 2)  # Borde negro del botón

        # Renderizar el texto como "fila, columna"
        texto = self.fuente.render(f'{self.identificador}', True, Colores.NEGRO)
        texto_rect = texto.get_rect(center=self.boton_visual.center)

        # Dibujar el texto en el centro del botón
        screen.blit(texto, texto_rect)

    def validar_click(self,mouse_pos: tuple) -> int: # 0: Correcto, 1: Incorrecto, 2: No se marco este
        if self.boton_visual.collidepoint(mouse_pos):
            self.visibilidad = True
            if self.marcado:
                return 0
            else:
                return 1
        return 2