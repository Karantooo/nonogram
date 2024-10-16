import sys
import pygame
from PIL import Image

from visual.tablero_visual import TableroVisual
from visual.colores import Colores


def main(dimensiones: tuple=None):
    global tablero
    pygame.init()

    screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h
    dimensiones = (int(screen_width), int(screen_height))

    # Configurar la pantalla
    screen = pygame.display.set_mode(dimensiones)

    background_image = pygame.image.load("assets/fondo.png")
    background_image = pygame.transform.scale(background_image, dimensiones)

    numero_botones = 20
    pygame.display.set_caption("Mi primer juego en Pygame")
    tablero = TableroVisual(numero_botones=numero_botones, dimensiones=dimensiones) # Podemos elegir el tamaño que deseamos agregando un argumento al constructor
    corriendo = True

    numero_botones *= numero_botones
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

        if tablero.get_vidas() == 0 or tablero.get_vistos() == numero_botones:
            corriendo = False

        screen.blit(background_image, (0, 0))

        # Dibujar el tablero
        tablero.imprimir(screen)

        # Actualizar la pantalla
        pygame.display.flip()

        # Limitar a 60 fps
        pygame.time.Clock().tick(60)

    # Salir de Pygame
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
