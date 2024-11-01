import pygame
from PIL import Image


class AnimacionExplosion:
    frames: list[pygame.Surface]
    frame_index: int
    gif_size: tuple[int,int]

    """
    Controla la animación de una explosión a partir de un GIF, cargando cada fotograma como una superficie de Pygame.
    """

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
        """
        Renderiza el fotograma actual de la explosión en la pantalla en la posición indicada y avanza al siguiente fotograma.

        Args:
            screen (pygame.Surface): Superficie de Pygame donde se renderiza la explosión.
            posicion (tuple[int, int]): Posición (x, y) en la pantalla donde se centrará la explosión.
        """
        posicion_impresion = [posicion[0] - self.gif_size[0] / 2, posicion[1] - self.gif_size[1] / 2]
        screen.blit(self.frames[self.frame_index], posicion_impresion)
        pygame.display.flip()

        self.frame_index = (self.frame_index + 1) % len(self.frames)
