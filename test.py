import pygame
import sys


def main():
    pygame.init()

    # Configuracion de la pantalla
    ancho, alto = 800, 600
    pantalla = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("nonagram")

    # Colores
    blanco = (255, 255, 255)
    negro = (0, 0, 0)

    # Bucle principal
    color = blanco
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_e:
                    if color == blanco:
                        color = negro
                    else:
                        color = blanco

        # Rellena la pantalla con el color blanco
        pantalla.fill(color)

        # Actualiza la pantalla
        pygame.display.flip()

if __name__:
    main()