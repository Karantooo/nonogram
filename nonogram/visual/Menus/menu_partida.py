import pygame_menu
import pygame

from .menu_niveles import MenuNiveles
from .menu_opciones_juego import MenuOpcionesJuego


class MenuPartida:
    def __init__(self, screen: pygame.display, menu_inicial, main):
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
        self.main_juego = main
        self.menu_inicio = menu_inicial
        self.menu_partida = pygame_menu.Menu(title="Seleccione partida", width=1000, height=700, theme=custom_theme)

    def mostrar_menu_partida(self):
        self.menu_partida.clear()
        self.menu_partida.add.button(title="Partida Guardada", )
        self.menu_partida.add.button(title="Nueva Partida", action=self.activar_menu_opciones_juego)
        self.menu_partida.add.button(title="Niveles", action=self.activar_menu_niveles)
        self.menu_partida.add.button(title="Volver", action=self.menu_inicio.mostrar_menu_inicio)

        self.menu_partida.mainloop(self.pantalla)

    def activar_menu_opciones_juego(self):
        menu_opciones_juego = MenuOpcionesJuego(self.pantalla, self, self.main_juego)
        menu_opciones_juego.mostrar_menu_opciones_juego()

    def activar_menu_niveles(self):
        menu_niveles = MenuNiveles(self.pantalla, self, self.main_juego)
        menu_niveles.mostrar_menu_niveles()
