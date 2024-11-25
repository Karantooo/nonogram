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
    alpha: int
    alpha_incremento: int

    def __init__(self, screen: pygame.Surface):
        self.screen = screen

        screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h
        self.posicion = (int(screen_width / 2), int(screen_height / 2))

        self.gif_size = (screen_width,  screen_height)

        gif = Image.open("assets/gif_game_over.gif")

        self.frames = []

        for frame in range(gif.n_frames):
            gif.seek(frame)
            frame_image = gif.convert("RGBA")  # Convierte a RGBA para Pygame
            frame_image = frame_image.resize(self.gif_size)
            pygame_image = pygame.image.fromstring(frame_image.tobytes(), frame_image.size, frame_image.mode)
            self.frames.append(pygame_image)

        self.frame_index = len(self.frames) - 1
        self.orden_impresion = False
        self.alpha = 0
        self.alpha_incremento = 7

    def imprimir(self) -> None:
        x = self.posicion[0] - self.gif_size[0] / 2
        y = self.posicion[1] - self.gif_size[1] / 2

        # Incrementar el alpha hasta el máximo (255)
        if self.alpha < 255:
            self.alpha += self.alpha_incremento
        if self.alpha > 255:
            self.alpha = 255  # Limitar el valor máximo

        # Aplicar el alpha al frame actual
        frame = self.frames[self.frame_index].copy()  # Copia para aplicar transparencia
        frame.set_alpha(self.alpha)
        self.screen.blit(frame, (x, y))

        pygame.display.flip()

        if self.orden_impresion:
            self.frame_index = (self.frame_index + 1)
            if self.frame_index == len(self.frames) - 1:
                self.orden_impresion = False
        else:
            self.frame_index = self.frame_index - 1
            if self.frame_index == 0:
                self.orden_impresion = True
