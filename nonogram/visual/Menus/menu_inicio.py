import pygame_menu
import pygame
from .menu_configuracion import MenuConfiguracion
from .menu_opciones_juego import MenuOpcionesJuego
from .menu_partida import MenuPartida



class MenuInicio:
    def __init__(self, screen: pygame.display, main):
        custom_theme = pygame_menu.Theme(background_color=(17, 84, 143), title_font=pygame_menu.font.FONT_FRANCHISE,
                                         title_font_size=100,
                                         title_background_color=(13, 62, 105),
                                         widget_font=pygame_menu.font.FONT_FRANCHISE,
                                         widget_font_color=(255, 255, 255),
                                         widget_font_size=70,
                                         widget_background_color=(13, 62, 105),
                                         selection_color=(25, 122, 207),
                                         widget_padding=(10, 15),
                                         )

        self.pantalla = screen
        self.main = main
        self.menu_inicio = pygame_menu.Menu(title="Nonogram", width=1000, height=700, theme=custom_theme)

    def mostrar_menu_inicio(self):
        self.menu_inicio.clear()
        self.menu_inicio.add.button('Jugar', self.activar_menu_partida)
        self.menu_inicio.add.button('Configuracion', self.activar_menu_configuracion)
        self.menu_inicio.add.button('Salir', pygame_menu.events.EXIT)

        self.menu_inicio.mainloop(self.pantalla)

    def activar_menu_configuracion(self):
        menu_configuracion = MenuConfiguracion(self.pantalla, self, self.main)
        menu_configuracion.mostrar_menu_configuracion()

    def activar_menu_partida(self):
        menu_partida = MenuPartida(self.pantalla, self, self.main)
        menu_partida.mostrar_menu_partida()