import sys
import pygame
from PIL import Image

from visual.tablero_visual import TableroVisual
from visual.colores import Colores


def main(dimensiones: tuple=(1000,700)):
    global tablero
    # Inicializar Pygame
    pygame.init()
    # Configurar la pantalla
    screen = pygame.display.set_mode(dimensiones)

    # Fondo de pantalla
    frames = []
    gif_path = 'assets/martillo.gif'
    gif = Image.open(gif_path)
    try:
        while True:
            # Convertir cada fotograma a un formato compatible con Pygame
            frame = gif.copy().convert('RGBA')
            frame_data = frame.tobytes()
            surface = pygame.image.fromstring(frame_data, gif.size, 'RGBA')
            surface = pygame.transform.scale(surface, dimensiones)
            frames.append(surface)
            gif.seek(gif.tell() + 1)
    except EOFError:
        pass  # Se alcanzó el final del GIF

    clock = pygame.time.Clock()
    current_frame = 0


    pygame.display.set_caption("Mi primer juego en Pygame")
    tablero = TableroVisual(numero_botones=6, dimensiones=dimensiones) # Podemos elegir el tamaño que deseamos agregando un argumento al constructor
    corriendo = True
    while corriendo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos  # Obtener la posición del ratón al hacer clic
                tablero.validar_click(mouse_pos)

        if tablero.ganado():
            print("gg")
            corriendo = False

        if tablero.get_vidas() == 0 or tablero.get_vistos() == 16:
            corriendo = False

        # Llenar la pantalla de blanco
        screen.fill(Colores.BLANCO)

        screen.blit(frames[current_frame], (0, 0))

        tablero.imprimir(screen)

        pygame.display.flip()

        current_frame = (current_frame + 1) % len(frames)

        pygame.time.Clock().tick(60)

        clock.tick(10)



    # Salir de Pygame
    pygame.quit()

if __name__ == '__main__':
    main((800, 600))
