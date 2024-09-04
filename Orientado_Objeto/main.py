import sys
import pygame

from Colores import Colores
from Tablero import Tablero

# Inicializar Pygame
pygame.init()

# Configurar la pantalla
screen = pygame.display.set_mode((1000, 700))
pygame.display.set_caption("Mi primer juego en Pygame")

tablero = Tablero()

corriendo = True

while corriendo:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos  # Obtener la posición del ratón al hacer clic
            tablero.validar_click(mouse_pos)

    if tablero.ganado():
        print("gg")
        corriendo = False

    if tablero.get_vidas() == 0 or tablero.get_vistos() == 16:
        corriendo = False

    # Llenar la pantalla de blanco
    screen.fill(Colores.BLANCO)

    tablero.imprimir(screen)

    # Actualizar la pantalla
    pygame.display.flip()

    # Controlar los FPS
    pygame.time.Clock().tick(60)


# Salir de Pygame
pygame.quit()
