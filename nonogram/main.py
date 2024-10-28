import sys
import pygame

from visual.tablero_visual import TableroVisual

def main(dimensiones: tuple=None):
    global tablero
    pygame.init()
    pygame.mixer.init()

    screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h
    dimensiones = (int(screen_width), int(screen_height))

    # Configurar la pantalla
    screen = pygame.display.set_mode(dimensiones)

    # Carga de sonidos
    sonido_victoria = pygame.mixer.Sound("assets/sonidos/victoria.wav")
    sonido_derrota = pygame.mixer.Sound("assets/sonidos/derrota.wav")

    # Ajuste de volumen de sonidos
    sonido_derrota.set_volume(1)
    sonido_victoria.set_volume(1)

    # Carga de musica ambiente del juego
    pygame.mixer.music.load("assets/sonidos/musica_ambiental.wav")

    # Reproducir la música en bucle (-1 hace que se reproduzca indefinidamente)
    pygame.mixer.music.play(-1)

    # Ajustar volumen de la musica [0, 1]
    pygame.mixer.music.set_volume(0.6)

    background_image = pygame.image.load("assets/fondo.png")
    background_image = pygame.transform.scale(background_image, dimensiones)

    numero_botones = 2
    pygame.display.set_caption("Mi primer juego en Pygame")
    tablero = TableroVisual(numero_botones=numero_botones, dimensiones=dimensiones) # Podemos elegir el tamaño que deseamos agregando un argumento al constructor
    corriendo = True

    numero_botones *= numero_botones
    while corriendo:
        #####################################################
        # Manejo de Eventos
        #####################################################

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    tablero.validar_click(mouse_pos=event.pos)
                elif event.button == pygame.BUTTON_RIGHT:
                    tablero.marcar_bandera(mouse_pos=event.pos)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q: #salir con la q o con el esc
                    pygame.quit()
                    sys.exit()

        #####################################################
        # Seccion de Impresion
        #####################################################

        # Impresion de la imagen de fondo
        screen.blit(background_image, (0, 0))

        # Dibujar el tablero
        tablero.imprimir(screen)

        # Actualizar la pantalla
        pygame.display.flip()

        #####################################################
        # Validacion de condicion de Victoria
        #####################################################

        if tablero.ganado():
            sonido_victoria.play()
            pygame.time.delay(int(sonido_victoria.get_length() * 1000))  # Delay en milisegundos
            print("gg")
            corriendo = False

        #####################################################
        # Validacion de condicion de Derrota
        #####################################################

        elif tablero.get_vidas() == 0 or tablero.get_vistos() == numero_botones:
            sonido_derrota.play()
            pygame.time.delay(int(sonido_derrota.get_length() * 1000))  # Delay en milisegundos
            corriendo = False

        # Limitar a 60 fps
        pygame.time.Clock().tick(60)

    # Salir de Pygame
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
