import sys
import pygame
from logica.sistema_guardado import SistemaGuardado


from visual.tablero_visual import TableroVisual
from visual.animacion_particulas import AnimacionParticulas
from visual.conversor import Conversor

from visual.Menus import MenuInicio



class Main:
    tablero: TableroVisual
    cantidad_de_botones: int

    def __init__(self):
        # Musica inicio
        pygame.mixer.music.load("assets/sonidos/musica_ambiental.wav")

        # Reproducir la música en bucle (-1 hace que se reproduzca indefinidamente)
        pygame.mixer.music.play(-1)

        # Ajustar volumen de la musica [0, 1]
        pygame.mixer.music.set_volume(0.05)

        self.cantidad_de_botones = 3

        # Se inicializa el menu incio para trabajar correctamente
        self.menu_inicial = MenuInicio(screen=screen, main=self)
        self.menu_inicial.mostrar_menu_inicio()

    def select_cant_botones(self, value):
        self.cantidad_de_botones = int(value)
        print(self.cantidad_de_botones)

    def cambiar_volumen_musica(self, value):
        pygame.mixer.music.set_volume(value)

    def main(self, dimensiones: tuple=None, partida_guardada: SistemaGuardado = None):

        print(self.cantidad_de_botones)
        num_botones = self.cantidad_de_botones

        screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h
        dimensiones = (int(screen_width), int(screen_height))

        # Carga de sonidos
        sonido_victoria = pygame.mixer.Sound("assets/sonidos/victoria.wav")
        sonido_derrota = pygame.mixer.Sound("assets/sonidos/derrota.wav")

        # Ajuste de volumen de sonidos
        sonido_derrota.set_volume(1)
        sonido_victoria.set_volume(1)

        background_image = pygame.image.load("assets/fondo.png")
        background_image = pygame.transform.scale(background_image, dimensiones)

        numero_botones = self.cantidad_de_botones

        pygame.display.set_caption("Mi primer juego en Pygame")

        if partida_guardada == None:
            tablero = TableroVisual(
                numero_botones=numero_botones,
                dimensiones=dimensiones,
                menu_inicial=self.menu_inicial,
                screen=screen
            ) # Podemos elegir el tamaño que deseamos agregando un argumento al constructor
        else:
            tablero = TableroVisual(
                numero_botones=numero_botones,
                guardado_previo=partida_guardada,
                menu_inicial=self.menu_inicial,
                screen=screen
            )
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

            if tablero.ganado() and tablero.animacion_particulas is None:
                ########
                # Se vuelve a imprimir pero sin animaciones ni decoraciones
                ########
                # Impresion de la imagen de fondo
                screen.blit(background_image, (0, 0))

                # Dibujar el tablero
                tablero.imprimir(screen)

                # Actualizar la pantalla
                pygame.display.flip()

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

        self.menu_inicial = MenuInicio(screen=screen, main=self)
        self.menu_inicial.mostrar_menu_inicio()


if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init()
    # Configurar la pantalla
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    main = Main()



