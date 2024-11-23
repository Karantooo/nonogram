import pygame
from PIL import Image
from nonogram.visual.interfaz_v_d import InterfazAnimacionVD

class AnimacionDerrota(InterfazAnimacionVD):
    screen: pygame.Surface
    posicion: tuple[int, int]

    frames: list[pygame.Surface]
    frame_index: int
    gif_size: tuple[int,int]

    orden_impresion: bool

    def __init__(self, screen: pygame.Surface):
        self.screen = screen

        screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h
        self.posicion = (int(screen_width / 2), int(screen_height / 2))

        self.gif_size = (screen_height,  screen_height)

        gif = Image.open("assets/gif_derrota.gif")

        self.frames = []

        for frame in range(gif.n_frames):
            gif.seek(frame)
            frame_image = gif.convert("RGBA")  # Convierte a RGBA para Pygame
            frame_image = frame_image.resize(self.gif_size)
            pygame_image = pygame.image.fromstring(frame_image.tobytes(), frame_image.size, frame_image.mode)
            self.frames.append(pygame_image)

        self.frame_index = len(self.frames) - 1
        self.orden_impresion = False

    def imprimir(self) -> None:
        x = self.posicion[0] - self.gif_size[0] / 2
        y = self.posicion[1] - self.gif_size[1] / 2
        self.screen.blit(self.frames[self.frame_index], (x, y))

        pygame.display.flip()

        if self.orden_impresion:
            self.frame_index = (self.frame_index + 1)
            if self.frame_index == len(self.frames) - 1:
                self.orden_impresion = False
        else:
            self.frame_index = self.frame_index - 1
            if self.frame_index == 0:
                self.orden_impresion = True
