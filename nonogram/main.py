import sys
import pygame
import numpy as np
from logica.sistema_guardado import SistemaGuardado
from logica.calculo_puntaje import CalculadorPuntaje
from visual.tablero_visual import TableroVisual
from visual.animacion_victoria import AnimacionVictoria
from visual.animacion_derrota import AnimacionDerrota
from visual.interfaz_v_d import InterfazAnimacionVD
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


    def main(self, dimensiones: tuple=None, partida_guardada: SistemaGuardado = None, imagen: np.ndarray[bool] = None):

        screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h
        dimensiones = (int(screen_width), int(screen_height))

        # Carga de sonidos
        sonido_victoria = pygame.mixer.Sound("assets/sonidos/victoria.wav")
        sonido_derrota = pygame.mixer.Sound("assets/sonidos/derrota.wav")

        # Ajuste de volumen de sonidos
        sonido_derrota.set_volume(1)
        sonido_victoria.set_volume(1)

        # Configurar un evento para detectar cuando el sonido termina
        evento_sonido_terminado = pygame.USEREVENT + 1

        background_image = pygame.image.load("assets/fondo.png")
        background_image = pygame.transform.scale(background_image, dimensiones)

        numero_botones = self.cantidad_de_botones
        pygame.display.set_caption("Mi primer juego en Pygame")
        if partida_guardada is not None:
            tablero = TableroVisual(
                numero_botones=numero_botones,
                guardado_previo=partida_guardada,
                menu_inicial=self.menu_inicial,
                screen=screen,
                dimensiones=dimensiones
            )
        elif imagen is not None:
            tablero = TableroVisual(
                numero_botones=numero_botones,
                imagen=imagen,
                menu_inicial=self.menu_inicial,
                screen=screen,
                dimensiones=dimensiones
            )

        else:
            tablero = TableroVisual(
                numero_botones=numero_botones,
                dimensiones=dimensiones,
                menu_inicial=self.menu_inicial,
                screen=screen
            )
        corriendo = True

        numero_botones *= numero_botones
        animacion_v_d: InterfazAnimacionVD = None

        corriendo = True
        interacciones_activadas = True
        sonido_derrota_activado = False
        sonido_victoria_activado = False

        veces_reproduccion_victoria = 0

        while corriendo:
            #####################################################
            # Manejo de Eventos
            #####################################################

            for event in pygame.event.get():
                if (event.type == pygame.QUIT or
                        (event.type == pygame.KEYDOWN and
                            (event.key == pygame.K_ESCAPE or event.key == pygame.K_q)
                        )
                    ):
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN and interacciones_activadas:
                    if event.button == pygame.BUTTON_LEFT:
                        tablero.validar_click(mouse_pos=event.pos)
                    elif event.button == pygame.BUTTON_RIGHT:
                        tablero.marcar_bandera(mouse_pos=event.pos)

                if event.type == evento_sonido_terminado:
                    if sonido_derrota_activado:
                        corriendo = False

                    if sonido_victoria_activado:
                        if veces_reproduccion_victoria < 1: # Se reproducira 2 veces la animacion
                            veces_reproduccion_victoria = veces_reproduccion_victoria + 1
                            sonido_victoria_activado = False
                        else:
                            corriendo = False

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

            if animacion_v_d is not None:
                animacion_v_d.imprimir()


            # Actualizar la pantalla
            pygame.display.flip()

            #####################################################
            # Validacion de condicion de Victoria
            #####################################################

            # Se desactivan las acciones del mouse sobre el tablero
            if ((tablero.ganado() or
                 tablero.get_vidas() == 0 or
                 tablero.get_vistos() == numero_botones
                ) and interacciones_activadas
            ):
                interacciones_activadas = False

            if tablero.ganado() and tablero.animacion_particulas is None and not sonido_victoria_activado:
                sonido_victoria.play()
                duracion_sonido = int(sonido_victoria.get_length() * 1000)
                pygame.time.set_timer(evento_sonido_terminado, duracion_sonido)

                sonido_victoria_activado = True

                if veces_reproduccion_victoria == 0:
                    animacion_v_d = AnimacionVictoria(screen=screen)


            #####################################################
            # Validacion de condicion de Derrota
            #####################################################

            elif (tablero.get_vidas() == 0 or tablero.get_vistos() == numero_botones) and not sonido_derrota_activado:
                sonido_derrota.play()
                duracion_sonido = int(sonido_derrota.get_length() * 1000)
                pygame.time.set_timer(evento_sonido_terminado, duracion_sonido)

                sonido_derrota_activado = True

                animacion_v_d = AnimacionDerrota(screen=screen)

            # Limitar a 60 fps
            pygame.time.Clock().tick(60)
        # Calcular puntaje final
        calc_puntaje = CalculadorPuntaje(
            tiempo=tablero.tiempo_transcurrido,
            vidas=tablero.get_vidas(),
            dificultad=tablero.dificultad
        )
        puntaje_final = calc_puntaje.calcular()

        # Mostrar puntaje en pantalla
        screen.fill((0, 0, 255))  # Fondo negro
        self.mostrar_puntaje(screen, puntaje_final)
        pygame.display.flip()

        pygame.time.wait(4000)

        self.menu_inicial = MenuInicio(screen=screen, main=self)
        self.menu_inicial.mostrar_menu_inicio()

    def mostrar_puntaje(self, screen, puntaje):
        font = pygame.font.Font(None, 74)  # Fuente y tamaño
        texto = font.render(f"Puntaje obtenido: {puntaje}", True, (0, 0, 0))  # Color blanco
        text_rect = texto.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(texto, text_rect)

if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init()
    # Configurar la pantalla
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    main = Main()
