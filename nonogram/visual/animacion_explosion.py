import pygame
from PIL import Image


class AnimacionExplosion:
    frames: list[pygame.Surface]
    frame_index: int
    gif_size: tuple[int,int]


    def __init__(self):
        gif = Image.open("assets/EXPLOSION.gif")
        self.frames = []
        for frame in range(gif.n_frames):
            gif.seek(frame)
            frame_image = gif.convert("RGBA")  # Convierte a RGBA para Pygame
            pygame_image = pygame.image.fromstring(frame_image.tobytes(), frame_image.size, frame_image.mode)
            self.frames.append(pygame_image)

        self.frame_index = 0
        self.gif_size = gif.size


    def imprimir(self, screen: pygame.Surface, posicion: tuple[int, int]) -> None:
        posicion_impresion = [posicion[0] - self.gif_size[0] / 2, posicion[1] - self.gif_size[1] / 2]
        screen.blit(self.frames[self.frame_index], posicion_impresion)
        pygame.display.flip()

        self.frame_index = (self.frame_index + 1) % len(self.frames)
