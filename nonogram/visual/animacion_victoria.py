import pygame
from PIL import Image
from nonogram.visual.interfaz_v_d import InterfazAnimacionVD

class AnimacionVictoria(InterfazAnimacionVD):
    screen: pygame.Surface
    posicion_potato_gg: tuple[int, int]
    frames_potato_gg: list[pygame.Surface]
    frame_potato_gg_index: int
    gif_potato_gg_size: tuple[int,int]

    alpha: int
    alpha_incremento: int

    def __init__(self, screen: pygame.Surface):
        self.screen = screen

        screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h
        self.posicion_potato_gg = (int(screen_width / 2), int(screen_height / 2))

        lado_que_manda = int(min(screen_width, screen_height))
        self.gif_potato_gg_size = (lado_que_manda, lado_que_manda)

        gif_potato_gg = Image.open("assets/gif_potato_gg.gif")

        self.frames_potato_gg = []
        for frame in range(gif_potato_gg.n_frames):
            gif_potato_gg.seek(frame)
            frame_image = gif_potato_gg.convert("RGBA")  # Convierte a RGBA para Pygame
            frame_image = frame_image.resize(self.gif_potato_gg_size)
            pygame_image = pygame.image.fromstring(frame_image.tobytes(), frame_image.size, frame_image.mode)
            self.frames_potato_gg.append(pygame_image)

        self.frame_potato_gg_index = 0
        self.alpha = 0
        self.alpha_incremento = 8

    def imprimir(self) -> None:
        posicion_impresion_potato_gg = (
            int(self.posicion_potato_gg[0] - self.gif_potato_gg_size[0] / 2),
            int(self.posicion_potato_gg[1] - self.gif_potato_gg_size[1] / 2)
        )


        # Incrementar el alpha hasta el máximo (255)
        if self.alpha < 255:
            self.alpha += self.alpha_incremento
        if self.alpha > 255:
            self.alpha = 255  # Limitar el valor máximo

        frame = self.frames_potato_gg[self.frame_potato_gg_index].copy()  # Copia para aplicar transparencia
        frame.set_alpha(self.alpha)
        self.screen.blit(frame, posicion_impresion_potato_gg)

        pygame.display.flip()

        self.frame_potato_gg_index = (self.frame_potato_gg_index + 1) % len(self.frames_potato_gg)
