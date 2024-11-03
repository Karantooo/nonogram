import sys
import pygame
import pygame_menu

from visual.tablero_visual import TableroVisual
from visual.animacion_particulas import AnimacionParticulas
from visual.conversor import Conversor

def abrir_menu_opciones():
    menu_opciones_juego.enable()
    menu_principal.disable()

def abrir_menu_configuracion():
    menu_configuracion.enable()
    menu_principal.disable()

def volver_menu_principal_opciones():
    menu_principal.enable()
    menu_opciones_juego.disable()

def volver_menu_principal_configuracion():
    menu_principal.enable()
    menu_configuracion.disable()


def main(dimensiones: tuple=None):

    global tablero
    pygame.init()
    pygame.mixer.init()


    # Configurar la pantalla
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h
    dimensiones = (int(screen_width), int(screen_height))

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
    pygame.mixer.music.set_volume(0.05)

    background_image = pygame.image.load("assets/fondo.png")
    background_image = pygame.transform.scale(background_image, dimensiones)

    numero_botones = 3
    pygame.display.set_caption("Mi primer juego en Pygame")
    tablero = TableroVisual(
        numero_botones=numero_botones,
        dimensiones=dimensiones,
        screen=screen
    ) # Podemos elegir el tamaño que deseamos agregando un argumento al constructor
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

        # Animacion de particulas desde el baston de Megumin hacia un punto objetivo
        if tablero.get_animacion_particulas() is not None:
            tablero.get_animacion_particulas().animacion(velocidad_animacion=60)
            if tablero.get_animacion_particulas().validar_llegada():
                tablero.set_animacion_particulas()


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


#if __name__ == '__main__':
    #main()

pygame.init()
surface = pygame.display.set_mode((600, 400))

menu_principal = pygame_menu.Menu('Welcome', 600, 400, theme=pygame_menu.themes.THEME_BLUE)
menu_opciones_juego = pygame_menu.Menu('Opciones', 600, 400, theme=pygame_menu.themes.THEME_BLUE)
menu_configuracion = pygame_menu.Menu('COnfiguracion', 600, 400, theme=pygame_menu.themes.THEME_BLUE)


# ----------------- MENU PRINCIPAL -----------------
menu_principal.add.text_input('Name :', default='John Doe')
menu_principal.add.button('Play', abrir_menu_opciones)
menu_principal.add.button('Configure', abrir_menu_configuracion)
menu_principal.add.button('Quit', pygame_menu.events.EXIT)

# ----------------- MENU OPCIONES JUEGO -----------------
menu_opciones_juego.add.selector('Dificultad :', [('Hard', 1), ('Medium', 2), ('Easy', 3)])
menu_opciones_juego.add.button('Play', main)
menu_opciones_juego.add.button('Back', volver_menu_principal_opciones)

# ----------------- MENU CONFIGURACIONES -----------------
menu_configuracion.add.selector('Dimensiones ventana :', [('1920x1080', (1920,1080)), ('1280x720', (1280, 720))])
menu_configuracion.add.button('Back', volver_menu_principal_configuracion)

# ----------------- MENU HABILITADO -----------------
menu_principal.enable()
menu_configuracion.disable()
menu_opciones_juego.disable()
screen_menu = pygame.display.set_mode((600, 400))

while True:

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()

    if menu_principal.is_enabled():
        menu_principal.draw(screen_menu)
        menu_principal.update(events)
    if menu_configuracion.is_enabled():
        menu_configuracion.draw(screen_menu)
        menu_configuracion.update(events)
    if menu_opciones_juego.is_enabled():
        menu_opciones_juego.draw(screen_menu)
        menu_opciones_juego.update(events)

    pygame.display.flip()



