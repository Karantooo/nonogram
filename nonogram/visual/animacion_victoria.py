import pygame
from PIL import Image
from nonogram.visual.interfaz_v_d import InterfazAnimacionVD

class AnimacionVictoria(InterfazAnimacionVD):
    screen: pygame.Surface
    posicion_izquirda: tuple[int, int]
    posicion_derecha: tuple[int, int]

    frames_derecha: list[pygame.Surface]
    frame_index: int
    gif_size: tuple[int,int]

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.posicion_izquierda = (0,0)

        self.gif_size = ( pygame.display.Info().current_h,  pygame.display.Info().current_h)

        self.posicion_derecha = ( pygame.display.Info().current_w -  pygame.display.Info().current_h,0)

        gif = Image.open("assets/gif_victoria.gif")

        self.frames_izquierda = []
        self.frames_derecha = []

        for frame in range(gif.n_frames):
            gif.seek(frame)
            frame_image = gif.convert("RGBA")  # Convierte a RGBA para Pygame
            frame_image = frame_image.resize(self.gif_size)
            pygame_image = pygame.image.fromstring(frame_image.tobytes(), frame_image.size, frame_image.mode)
            self.frames_derecha.append(pygame_image)

            # Reflejar el frame en el eje Y
            pygame_image = pygame.transform.flip(pygame_image, True, False)
            self.frames_izquierda.append(pygame_image)

        self.frame_index = 0

    def imprimir(self) -> None:
        self.screen.blit(self.frames_izquierda[self.frame_index], self.posicion_izquierda)
        self.screen.blit(self.frames_derecha[self.frame_index], self.posicion_derecha)

        pygame.display.flip()
        self.frame_index = (self.frame_index + 1) % len(self.frames_derecha)